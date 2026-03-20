"""
Block Course helper functions for visualization and data loading.

Usage in solution notebooks:
    import sys, os
    sys.path.insert(0, os.path.abspath('../../Students/Exercise'))
    from helper import *
"""
import os
from typing import Union, List
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.axes import Axes


# ─── Data loading ─────────────────────────────────────────────────────────────

def load_npz_as_df(path, data_key='data', columns_key='columns'):
    """Load an NPZ file and return a pandas DataFrame.

    Parameters
    ----------
    path : str
        Path to the .npz file.
    data_key : str
        Key for the data array inside the NPZ (default 'data').
    columns_key : str
        Key for the column names array (default 'columns').
        If the key is absent, columns are auto-named col_0, col_1, ...

    Returns
    -------
    pd.DataFrame
    """
    d = np.load(path, allow_pickle=True)
    data = d[data_key]
    if columns_key in d:
        cols = list(d[columns_key])
    else:
        cols = [f'col_{i}' for i in range(data.shape[1] if data.ndim > 1 else 1)]
    if data.ndim == 1:
        return pd.DataFrame({cols[0]: data})
    return pd.DataFrame(data, columns=cols)


def dataset_summary(arrays_dict, fps=20):
    """Return a styled DataFrame summary of loaded arrays.

    Parameters
    ----------
    arrays_dict : dict[str, np.ndarray]
        Mapping of variable name → array.
    fps : int
        Frames per second used to compute duration.

    Returns
    -------
    pd.DataFrame
    """
    rows = []
    for name, arr in arrays_dict.items():
        n_frames = arr.shape[0] if arr.ndim > 1 else len(arr)
        rows.append({
            'Variable': name,
            'Shape': str(arr.shape),
            'dtype': str(arr.dtype),
            'Frames': n_frames,
            'Duration (min)': f'{n_frames / fps / 60:.1f}',
        })
    return pd.DataFrame(rows).set_index('Variable')


# ─── Neural activity ──────────────────────────────────────────────────────────

def plot_dfF_traces(dF_F, neuron_ids, time_s, title='dF/F traces — selected neurons'):
    """Plot multiple dF/F traces offset on a single axis for easy comparison.

    Parameters
    ----------
    dF_F : np.ndarray, shape (n_neurons, n_frames)
    neuron_ids : list[int]
    time_s : np.ndarray
    title : str

    Returns
    -------
    fig, ax
    """
    colors = plt.cm.tab10.colors
    offset_scale = float(np.percentile(np.abs(dF_F[neuron_ids]), 99)) * 2.0

    fig, ax = plt.subplots(figsize=(14, 4))
    for i, nid in enumerate(neuron_ids):
        offset = i * offset_scale
        ax.plot(time_s, dF_F[nid] + offset, lw=0.6,
                color=colors[i % len(colors)], label=f'Neuron {nid}')
        ax.axhline(offset, color=colors[i % len(colors)], lw=0.4, ls='--', alpha=0.4)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('dF/F (offset per neuron)')
    ax.set_title(title)
    ax.legend(loc='upper right', fontsize=9)
    ax.set_yticks([i * offset_scale for i in range(len(neuron_ids))])
    ax.set_yticklabels([f'N{n}' for n in neuron_ids], fontsize=9)
    plt.tight_layout()
    return fig, ax


def plot_corr_heatmap(corr_mat, labels, ax, title='', mask_diagonal=True, vmin=None, vmax=None):
    """Plot a small correlation heatmap with text annotations.

    Parameters
    ----------
    corr_mat : np.ndarray, shape (n, n)
    labels : list[str]
    ax : matplotlib Axes
    title : str
    mask_diagonal : bool
        If True, set the diagonal to NaN so it does not dominate the color scale.
    vmin, vmax : float or None
        Color scale limits.  If None, auto-scales to the max absolute off-diagonal value.

    Returns
    -------
    matplotlib.image.AxesImage
    """
    mat = corr_mat.copy().astype(float)
    if mask_diagonal:
        np.fill_diagonal(mat, np.nan)
    # Auto-scale from actual off-diagonal values if not provided
    if vmin is None or vmax is None:
        offdiag = mat[~np.isnan(mat)]
        auto_max = float(np.abs(offdiag).max()) if len(offdiag) > 0 else 1.0
        if vmin is None:
            vmin = -auto_max
        if vmax is None:
            vmax = auto_max
    n = len(labels)
    im = ax.imshow(mat, vmin=vmin, vmax=vmax, cmap='RdBu_r')
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
    ax.set_yticklabels(labels, fontsize=9)
    for i in range(n):
        for j in range(n):
            if not (mask_diagonal and i == j):
                ax.text(j, i, f'{mat[i, j]:.2f}', ha='center', va='center', fontsize=8)
    plt.colorbar(im, ax=ax, label='Pearson r')
    ax.set_title(title)
    return im

def plot_clustered_corr(corr_mat: Union[np.ndarray, List[np.ndarray]], order: Union[np.ndarray, List[np.ndarray]], ax: Union[Axes, List[Axes]], title: Union[str, List[str]] = '') -> Union[object, List[object]]:
    """Plot one or more correlation heatmaps reordered by cluster, with diagonal masked.

    Parameters
    ----------
    corr_mat : np.ndarray or list of np.ndarray, shape (n, n)
        Single correlation matrix or list of matrices
    order : np.ndarray[int] or list of np.ndarray[int]
        Neuron indices sorted by cluster assignment(s)
    ax : matplotlib Axes or list of matplotlib Axes
        Single axis or list of axes for plotting
    title : str or list of str
        Single title or list of titles

    Returns
    -------
    matplotlib.image.AxesImage or list of matplotlib.image.AxesImage
    """
    # Check if we have multiple matrices
    is_multiple = isinstance(corr_mat, list) and not isinstance(corr_mat, np.ndarray)
    
    if not is_multiple:
        # Single matrix case - original behavior
        mat = corr_mat.copy().astype(float)
        np.fill_diagonal(mat, np.nan)
        reordered = mat[np.ix_(order, order)]
        vmax = float(np.nanpercentile(np.abs(reordered), 99))
        im = ax.imshow(reordered, vmin=-vmax, vmax=vmax, cmap='RdBu_r', aspect='auto')
        plt.colorbar(im, ax=ax, label='Pearson r')
        ax.set_title(title)
        ax.set_xlabel('Neuron (sorted by cluster)')
        ax.set_ylabel('Neuron (sorted by cluster)')
        return im
    
    # Multiple matrices case
    # Ensure all inputs are lists
    if not isinstance(order, list):
        order = [order]
    if not isinstance(ax, list):
        ax = [ax]
    if isinstance(title, str):
        title = [title] * len(corr_mat)
    
    # Process all matrices and find shared vmax
    processed_mats = []
    vmaxes = []
    for i, mat in enumerate(corr_mat):
        mat_copy = np.asarray(mat).copy().astype(float)
        np.fill_diagonal(mat_copy, np.nan)
        processed_mats.append(mat_copy)
        vmax = float(np.nanpercentile(np.abs(mat_copy), 99))
        vmaxes.append(vmax)
    
    shared_vmax = max(vmaxes)
    
    # Plot all matrices with shared color scale
    ims = []
    for processed_mat, ord, axis, ttl in zip(processed_mats, order, ax, title):
        reordered = processed_mat[np.ix_(ord, ord)]
        im = axis.imshow(reordered, vmin=-shared_vmax, vmax=shared_vmax, 
                         cmap='RdBu_r', aspect='auto')
        axis.set_title(ttl)
        axis.set_xlabel('Neuron (sorted by cluster)')
        axis.set_ylabel('Neuron (sorted by cluster)')
        ims.append(im)
    
    # Create single colorbar to the right of all subplots
    fig = ax[0].get_figure()
    # move to most right subplot colorbar position
    cbar_ax = fig.add_axes([1, 0.15, 0.015, 0.7])  # [left, bottom, width, height]
    plt.colorbar(ims[0], cax=cbar_ax, label='Pearson r')
    
    
    return ims


def plot_raster(binary_neurons_x_frames, fps, order=None, event_rate_smooth=None,
                speed=None, run_threshold=2.0, frames_show=100000,
                cluster_labels=None, n_clusters=5,
                title='Population raster plot'):
    """Population raster plot with optional speed overlay.

    Parameters
    ----------
    binary_neurons_x_frames : np.ndarray, shape (n_neurons, n_frames)
        Binarized activity matrix — rows = neurons, cols = frames.
    fps : int
    order : np.ndarray[int] or None
        Neuron sort order. None = keep original order.
    event_rate_smooth : np.ndarray or None
        Pre-computed smooth network event rate. Computed internally if None.
    speed : np.ndarray or None
        Speed trace. If provided, an extra subplot is added below.
    run_threshold : float
        Running threshold (dashed line in speed panel).
    frames_show : int
        Number of frames to display (performance limit).
    title : str

    Returns
    -------
    matplotlib.figure.Figure
    """
    n_neurons, n_total = binary_neurons_x_frames.shape
    frames_show = min(n_total, frames_show)

    if order is None:
        order = np.arange(n_neurons)

    firing_rate = binary_neurons_x_frames.mean(axis=1)

    if event_rate_smooth is None:
        er = binary_neurons_x_frames.sum(axis=0)
        event_rate_smooth = (pd.Series(er[:frames_show])
                             .rolling(50, center=True, min_periods=1).mean().values)
    else:
        event_rate_smooth = event_rate_smooth[:frames_show]

    has_speed = speed is not None
    n_rows = 3 if has_speed else 2
    height_ratios = [4, 1, 1] if has_speed else [4, 1]
    fig_h = 10 if has_speed else 7

    fig = plt.figure(figsize=(14, fig_h))
    gs = fig.add_gridspec(n_rows, 2,
                          width_ratios=[6, 1],
                          height_ratios=height_ratios,
                          hspace=0.05, wspace=0.05)

    ax_raster = fig.add_subplot(gs[0, 0])
    ax_rate   = fig.add_subplot(gs[0, 1], sharey=ax_raster)
    ax_net    = fig.add_subplot(gs[1, 0], sharex=ax_raster)
    fig.add_subplot(gs[1, 1]).axis('off')

    raster_img = binary_neurons_x_frames[order, :frames_show]
    t_show = np.arange(frames_show) / fps

    ax_raster.imshow(raster_img, aspect='auto', cmap='binary', interpolation='none',
                     extent=[0, frames_show / fps, n_neurons, 0])
    ax_raster.set_ylabel('Neuron (sorted)')
    ax_raster.tick_params(labelbottom=False)

    if cluster_labels is not None:
        # Color each bar by its cluster
        colors_tab = plt.cm.tab10.colors
        labels_sorted = cluster_labels[order]
        bar_colors = [colors_tab[int(l) % len(colors_tab)] for l in labels_sorted]
        ax_rate.barh(np.arange(n_neurons), firing_rate[order],
                     color=bar_colors, height=1)
        # Draw yellow lines between clusters in the raster
        for b in np.where(np.diff(labels_sorted) != 0)[0] + 1:
            ax_raster.axhline(b, color='darkgray', lw=0.6, alpha=0.7)
    else:
        ax_rate.plot(firing_rate[order], np.arange(n_neurons), color='steelblue', lw=1.5)
        # fill between firing_rate and 0 with light steelblue
        ax_rate.fill_betweenx(np.arange(n_neurons), 0, firing_rate[order],
                            color='lightsteelblue', alpha=0.5)
    ax_rate.set_xlabel('Mean\nfiring rate')
    ax_rate.tick_params(labelleft=False)

    ax_net.plot(t_show, event_rate_smooth, color='darkgreen', lw=0.7)
    ax_net.fill_between(t_show, 0, event_rate_smooth, color='lightgreen', alpha=0.5)
    ax_net.set_ylabel('Active\nneurons')

    if has_speed:
        ax_net.tick_params(labelbottom=False)
        ax_spd = fig.add_subplot(gs[2, 0], sharex=ax_raster)
        fig.add_subplot(gs[2, 1]).axis('off')
        ax_spd.plot(t_show, speed[:frames_show], color='darkorange', lw=0.7)
        ax_spd.axhline(run_threshold, color='red', ls='--', lw=0.8,
                       label=f'{run_threshold} cm/s')
        ax_spd.set_ylabel('Speed\n(cm/s)')
        ax_spd.set_xlabel('Time (s)')
        ax_spd.legend(fontsize=8, loc='upper right')
    else:
        ax_net.set_xlabel('Time (s)')

    fig.suptitle(title, y=1.01)
    plt.tight_layout()
    return fig


# ─── Clustering / Sankey ──────────────────────────────────────────────────────

def draw_alluvial(labels_L, labels_R, ax, n_clusters=5, colors=None,
                  label_L='', label_R=''):
    """Sankey/alluvial diagram comparing two cluster assignment vectors.

    Parameters
    ----------
    labels_L : np.ndarray[int]   cluster labels (left side)
    labels_R : np.ndarray[int]   cluster labels (right side)
    ax : matplotlib Axes
    n_clusters : int
    colors : sequence or None
    label_L, label_R : str       axis labels for left/right
    """
    if colors is None:
        colors = plt.cm.tab10.colors

    counts_L = np.bincount(labels_L, minlength=n_clusters)
    counts_R = np.bincount(labels_R, minlength=n_clusters)
    total = len(labels_L)

    y_L = np.zeros(n_clusters + 1)
    y_R = np.zeros(n_clusters + 1)
    for i in range(n_clusters):
        y_L[i + 1] = y_L[i] + counts_L[i] / total
        y_R[i + 1] = y_R[i] + counts_R[i] / total

    for i in range(n_clusters):
        ax.add_patch(plt.Rectangle((0, y_L[i]), 0.08, y_L[i+1] - y_L[i],
                                   color=colors[i % len(colors)], zorder=3))
        ax.text(-0.01, (y_L[i] + y_L[i+1]) / 2, f'C{i+1} ({counts_L[i]})',
                ha='right', va='center', fontsize=8)

    for j in range(n_clusters):
        ax.add_patch(plt.Rectangle((0.92, y_R[j]), 0.08, y_R[j+1] - y_R[j],
                                   color=colors[j % len(colors)], zorder=3))
        ax.text(1.01, (y_R[j] + y_R[j+1]) / 2, f'C{j+1} ({counts_R[j]})',
                ha='left', va='center', fontsize=8)

    flow_y_L = y_L[:-1].copy()
    flow_y_R = y_R[:-1].copy()
    for i in range(n_clusters):
        for j in range(n_clusters):
            cnt = int(((labels_L == i) & (labels_R == j)).sum())
            if cnt == 0:
                continue
            h = cnt / total
            x0, x1 = 0.08, 0.92
            y0, y1 = flow_y_L[i], flow_y_R[j]
            verts = [(x0, y0), (0.5, y0), (0.5, y1), (x1, y1),
                     (x1, y1 + h), (0.5, y1 + h), (0.5, y0 + h), (x0, y0 + h), (x0, y0)]
            codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
                     Path.LINETO, Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.CLOSEPOLY]
            ax.add_patch(PathPatch(Path(verts, codes),
                                   facecolor=colors[i % len(colors)],
                                   alpha=0.35, edgecolor='none', zorder=2))
            flow_y_L[i] += h
            flow_y_R[j] += h

    if label_L:
        ax.text(0.04, 1.02, label_L, ha='center', fontsize=10, transform=ax.transAxes)
    if label_R:
        ax.text(0.96, 1.02, label_R, ha='center', fontsize=10, transform=ax.transAxes)

    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(-0.05, 1.05)
    ax.axis('off')


def plot_binarization_thresholds(trace, time_s, thresholds, colors=None, title='Binarization sensitivity'):
    """Show one continuous trace with multiple binarization thresholds overlaid.

    Each sub-panel shows the same dF/F trace with a different threshold: the shaded area
    marks frames where the signal exceeds the threshold (i.e., the neuron is detected as active).

    Parameters
    ----------
    trace : np.ndarray, shape (n_frames,)
        Single neuron's dF/F time series.
    time_s : np.ndarray
        Time axis in seconds, same length as trace.
    thresholds : list[float]
        List of threshold values to compare.
    colors : list or None
        One color per threshold. Defaults to red/orange/purple.
    title : str

    Returns
    -------
    fig
    """
    if colors is None:
        colors = ['tomato', 'darkorange', 'purple', 'green', 'navy']
    fig, axes = plt.subplots(len(thresholds), 1, figsize=(14, 2.5 * len(thresholds)), sharex=True)
    if len(thresholds) == 1:
        axes = [axes]
    tmax = float(trace.max())
    for ax, thr, col in zip(axes, thresholds, colors):
        binary = (trace >= thr).astype(float)
        ax.plot(time_s, trace, lw=0.7, color='steelblue', label='dF/F')
        ax.fill_between(time_s, 0, binary * tmax * 0.9,
                        alpha=0.4, color=col, label=f'threshold = {thr}')
        ax.axhline(thr, color=col, lw=0.8, ls='--')
        ax.set_ylabel('dF/F', fontsize=9)
        ax.legend(fontsize=8, loc='upper right')
    axes[-1].set_xlabel('Time (s)')
    axes[0].set_title(title)
    plt.tight_layout()
    return fig


def plot_threshold_vs_cnmf(dF_F, binary_cnmf, neuron_ids, time_s, threshold, title='Threshold vs. CNMF binarization'):
    """Compare threshold binarization against CNMF binarization for selected neurons.

    For each neuron one sub-panel shows: (1) the raw dF/F trace in blue, (2) the threshold
    binarization in red, and (3) the CNMF binarization in green.  This lets you judge whether
    the two methods agree on when the neuron was active.

    Parameters
    ----------
    dF_F : np.ndarray, shape (n_neurons, n_frames)
    binary_cnmf : np.ndarray, shape (n_neurons, n_frames)
    neuron_ids : list[int]
    time_s : np.ndarray
    threshold : float
    title : str

    Returns
    -------
    fig
    """
    fig, axes = plt.subplots(len(neuron_ids), 1, figsize=(14, 2.5 * len(neuron_ids)), sharex=True)
    if len(neuron_ids) == 1:
        axes = [axes]
    for ax, nid in zip(axes, neuron_ids):
        trace = dF_F[nid, :len(time_s)]
        tmax = float(trace.max())
        ax.plot(time_s, trace, lw=0.6, color='steelblue', label='dF/F')
        ax.fill_between(time_s, 0,
                        (trace >= threshold).astype(float) * tmax * 0.9,
                        alpha=0.4, color='tomato', label=f'Threshold ({threshold})')
        ax.fill_between(time_s, 0,
                        binary_cnmf[nid, :len(time_s)] * tmax * 0.7,
                        alpha=0.4, color='green', label='CNMF')
        ax.set_ylabel(f'N{nid}', fontsize=9)
        if ax is axes[0]:
            ax.legend(fontsize=8, loc='upper right')
    axes[-1].set_xlabel('Time (s)')
    axes[0].set_title(title)
    plt.tight_layout()
    return fig


def plot_shuffle_significance(z_scores, sig_mask, n_sub, cluster_labels, corr_obs):
    """Two-panel shuffle significance plot: Z-score heatmap + circular network graph.

    Left panel — heatmap of Z-scores for all neuron pairs.  Hot colours = highly significant.
    Right panel — circular network where each node is a neuron (coloured by cluster) and each
    edge connects a significantly correlated pair (edge width ∝ observed correlation).

    Parameters
    ----------
    z_scores : np.ndarray, shape (n_sub, n_sub)
    sig_mask : np.ndarray[bool], shape (n_sub, n_sub)
    n_sub : int
    cluster_labels : np.ndarray[int], shape (n_sub,)   used to colour nodes
    corr_obs : np.ndarray, shape (n_sub, n_sub)

    Returns
    -------
    fig
    """
    n_sig = int(sig_mask.sum()) // 2
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    im = axes[0].imshow(z_scores, cmap='hot', vmin=0, vmax=10, aspect='auto')
    plt.colorbar(im, ax=axes[0], label='Z-score')
    axes[0].set_title(f'Pairwise correlation Z-scores\n({n_sub} neurons, circular time-shift null)')
    axes[0].set_xlabel('Neuron')
    axes[0].set_ylabel('Neuron')

    ax = axes[1]
    angles = np.linspace(0, 2 * np.pi, n_sub, endpoint=False)
    nx, ny = np.cos(angles), np.sin(angles)
    rows, cols = np.where(sig_mask)
    for r, c in zip(rows, cols):
        if r < c:
            ax.plot([nx[r], nx[c]], [ny[r], ny[c]],
                    color='steelblue', lw=float(corr_obs[r, c]) * 3, alpha=0.5)
    ax.scatter(nx, ny, s=40, c=cluster_labels, cmap='tab10',
               zorder=5, edgecolors='k', linewidths=0.5)
    for i, (x, y) in enumerate(zip(nx, ny)):
        ax.text(x * 1.12, y * 1.12, str(i), fontsize=6, ha='center', va='center')
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f'Significant correlation network\n(edge width ∝ r, n_sig={n_sig})')
    plt.tight_layout()
    return fig


# ─── Behavioral / spatial ─────────────────────────────────────────────────────

def plot_raw_trajectory(x, y, title='Raw trajectory'):
    """Plot raw (pixel-space) X/Y trajectory of a body part.

    Parameters
    ----------
    x, y : np.ndarray   pixel coordinates
    title : str

    Returns
    -------
    fig, ax
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(x, y, lw=0.3, color='steelblue', alpha=0.6)
    ax.set_xlabel('X position (px)')
    ax.set_ylabel('Y position (px)')
    ax.invert_yaxis()
    ax.set_title(title)
    ax.set_aspect('equal')
    plt.tight_layout()
    return fig, ax


def plot_arena_image(arena, points=None, point_labels=None, title='Arena'):
    """Display the arena still-frame image with optional reference points.

    Parameters
    ----------
    arena : np.ndarray
        RGB image array loaded with matplotlib.image.imread.
    points : list of (x, y) tuples or None
        Pixel coordinates to mark on the image.
    point_labels : list[str] or None
        Labels for each point.  Must match length of points if provided.
    title : str

    Returns
    -------
    fig, ax
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(arena)
    if points:
        for i, (px, py) in enumerate(points):
            label = point_labels[i] if point_labels and i < len(point_labels) else f'({px},{py})'
            ax.scatter([px], [py], color='red', s=100, zorder=5)
            ax.text(px + 15, py, label, color='red', fontsize=9, va='center')
    ax.set_title(title)
    plt.tight_layout()
    return fig, ax


def plot_behavior_speed(t, speed_smooth, is_running, run_threshold, title='Behavioral state segmentation'):
    """Speed trace with running/resting classification overlay.

    Parameters
    ----------
    t : np.ndarray          time axis in seconds
    speed_smooth : np.ndarray   smoothed speed trace (cm/s)
    is_running : np.ndarray[int]  binary array (1 = running, 0 = resting)
    run_threshold : float
    title : str

    Returns
    -------
    fig, ax
    """
    fig, ax = plt.subplots(figsize=(14, 3))
    ax.plot(t, speed_smooth, lw=0.6, color='darkorange', label='Smoothed speed')
    ax.axhline(run_threshold, color='red', ls='--', lw=1,
               label=f'Threshold {run_threshold} cm/s')
    ax.fill_between(t, 0, speed_smooth, where=(is_running == 1),
                    alpha=0.3, color='green', label='Running')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Speed (cm/s)')
    ax.set_title(title)
    ax.legend(fontsize=9)
    plt.tight_layout()
    return fig, ax


def plot_tracking_quality(mean_likelihood, bodypart_names, title='Tracking quality per body part'):
    """Bar chart of mean likelihood per body part with actual names.

    Parameters
    ----------
    mean_likelihood : np.ndarray, shape (n_parts,)
    bodypart_names : list[str]
    title : str

    Returns
    -------
    fig, ax
    """
    n_parts = len(mean_likelihood)
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.bar(range(n_parts), mean_likelihood, color='steelblue',
           edgecolor='k', linewidth=0.5)
    for i, v in enumerate(mean_likelihood):
        ax.text(i, v + 0.01, f'{v:.2f}', ha='center', va='bottom', fontsize=7, rotation=0)
    ax.set_xticks(range(n_parts))
    ax.set_xticklabels(bodypart_names, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('Mean likelihood')
    ax.set_ylim(0, 1)
    ax.set_title(title)
    ax.axhline(mean_likelihood.max(), color='red', ls='--', lw=0.8, label='Best')
    ax.legend()
    plt.tight_layout()
    return fig, ax


def plot_trajectory_comparison(x_raw, y_raw, x_smooth, y_smooth, k, n_show=2000):
    """3-panel comparison: raw, smoothed, and overlay.

    Parameters
    ----------
    x_raw, y_raw : np.ndarray    raw (shifted) coordinates
    x_smooth, y_smooth : np.ndarray    smoothed coordinates
    k : int    smoothing window size
    n_show : int    number of frames to display

    Returns
    -------
    fig
    """
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    axes[0].plot(x_raw[:n_show], y_raw[:n_show], lw=0.4, color='gray', alpha=0.8)
    axes[0].set_title('Raw (shifted)')

    axes[1].plot(x_smooth[:n_show], y_smooth[:n_show], lw=0.4, color='steelblue')
    axes[1].set_title(f'Smoothed (k={k})')

    axes[2].plot(x_raw[:n_show], y_raw[:n_show], lw=0.4, color='gray', alpha=0.5, label='Raw')
    axes[2].plot(x_smooth[:n_show], y_smooth[:n_show], lw=0.8, color='steelblue',
                 label=f'Smoothed k={k}')
    axes[2].set_title(f'Overlay (first {n_show // 20} s)')
    axes[2].legend(fontsize=8)

    for ax in axes:
        ax.invert_yaxis()
        ax.set_aspect('equal')
        ax.set_xlabel('X (px)')
        ax.set_ylabel('Y (px)')

    fig.suptitle('Trajectory smoothing comparison')
    plt.tight_layout()
    return fig


def plot_speed_summary(time_s, speed_cm_s, x_pos, y_pos):
    """3-panel speed summary: speed over time, distribution histogram, trajectory.

    Parameters
    ----------
    time_s : np.ndarray    time axis in seconds
    speed_cm_s : np.ndarray    speed in cm/s (length = n_frames - 1 or n_frames)
    x_pos, y_pos : np.ndarray    position arrays aligned with speed_cm_s

    Returns
    -------
    fig
    """
    fig, axes = plt.subplots(1, 3, figsize=(16, 4))

    axes[0].plot(time_s[:len(speed_cm_s)], speed_cm_s, lw=0.5, color='darkorange')
    axes[0].set_xlabel('Time (s)')
    axes[0].set_ylabel('Speed (cm/s)')
    axes[0].set_title('Speed over time')

    axes[1].hist(speed_cm_s, bins=80, color='darkorange', edgecolor='none')
    axes[1].set_xlabel('Speed (cm/s)')
    axes[1].set_ylabel('Frame count')
    axes[1].set_title('Speed distribution')
    med = float(np.median(speed_cm_s))
    axes[1].axvline(med, color='black', lw=1.5, ls='--', label=f'Median: {med:.1f} cm/s')
    axes[1].legend(fontsize=9)

    sc = axes[2].scatter(x_pos[:len(speed_cm_s)], y_pos[:len(speed_cm_s)],
                         c=speed_cm_s, cmap='hot_r', s=0.5,
                         vmin=0, vmax=float(np.percentile(speed_cm_s, 98)))
    plt.colorbar(sc, ax=axes[2], label='Speed (cm/s)')
    axes[2].invert_yaxis()
    axes[2].set_aspect('equal')
    axes[2].set_title('Trajectory colored by speed')
    axes[2].set_xlabel('X (px)')
    axes[2].set_ylabel('Y (px)')

    fig.suptitle('Speed analysis summary')
    plt.tight_layout()
    return fig


def plot_place_map(cell_id, ax, x, y, F_bin, title=None):
    """Spatial firing map for a single neuron.

    Parameters
    ----------
    cell_id : int    column index in F_bin
    ax : matplotlib Axes
    x, y : np.ndarray    smoothed position (n_frames,)
    F_bin : np.ndarray, shape (n_frames, n_neurons)    binarized activity
    title : str or None
    """
    cell_trace = F_bin[:, cell_id]
    active = cell_trace > 0
    n_active = int(active.sum())
    rate_pct = n_active / len(cell_trace) * 100

    ax.plot(x, y, lw=0.2, color='darkgray', alpha=0.8)
    ax.scatter(x[active], y[active], s=3, color='red', alpha=0.6, zorder=3)
    label = title if title is not None else f'Neuron {cell_id}'
    ax.set_title(f'{label}\n{n_active} events ({rate_pct:.1f}%)', fontsize=9)
    ax.invert_yaxis()
    ax.set_aspect('equal')
    ax.axis('off')


def plot_place_map_grid(cell_ids, x, y, F_bin, ncols=4, figsize=(12, 12),
                        suptitle='Spatial firing maps'):
    """Grid of spatial firing maps.

    Parameters
    ----------
    cell_ids : list[int]
    x, y : np.ndarray
    F_bin : np.ndarray, shape (n_frames, n_neurons)
    ncols : int
    figsize : tuple
    suptitle : str

    Returns
    -------
    fig
    """
    nrows = int(np.ceil(len(cell_ids) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    axes_flat = axes.flat if hasattr(axes, 'flat') else [axes]
    for ax, cid in zip(axes_flat, cell_ids):
        plot_place_map(cid, ax, x, y, F_bin)
    for ax in list(axes_flat)[len(cell_ids):]:
        ax.axis('off')
    fig.suptitle(f'{suptitle}\n(red = active positions, gray = full trajectory)',
                 fontsize=12, y=1.01)
    plt.tight_layout()
    return fig


# ─── Analysis utilities ───────────────────────────────────────────────────────

def run_clustering(corr_mat, n_clusters, method='ward'):
    """Hierarchical clustering on a correlation matrix.

    Converts correlation to distance, builds a dendrogram with Ward linkage,
    then cuts it to return exactly `n_clusters` groups.  This wraps the scipy
    clustering workflow so notebooks can stay focused on interpretation.

    Parameters
    ----------
    corr_mat : np.ndarray, shape (n, n)
        Pairwise Pearson correlation matrix.
    n_clusters : int
        Number of clusters to cut the dendrogram into.
    method : str
        Linkage method passed to ``scipy.cluster.hierarchy.linkage``.

    Returns
    -------
    dict with keys:
        ``labels``  — np.ndarray[int], shape (n,), 0-indexed cluster assignment
        ``order``   — np.ndarray[int], neurons sorted by cluster
        ``Z``       — linkage matrix (for dendrogram if needed)
        ``counts``  — np.ndarray[int], neurons per cluster
    """
    from scipy.cluster.hierarchy import linkage, fcluster
    from scipy.spatial.distance import squareform

    # Distance = 1 − correlation. Clipped to [0, 2] to handle floating-point rounding.
    dist = np.clip(1 - corr_mat, 0, 2)
    np.fill_diagonal(dist, 0)
    Z = linkage(squareform(dist, checks=False), method=method)
    labels = fcluster(Z, n_clusters, criterion='maxclust') - 1   # 0-indexed
    order = np.argsort(labels)
    counts = np.bincount(labels, minlength=n_clusters)
    return {'labels': labels, 'order': order, 'Z': Z, 'counts': counts}


def run_shuffle_test(data, n_shuffles=200, method='circular', rng_seed=0):
    """Permutation test for significant pairwise correlations.

    Builds a null distribution by shuffling the data in one of three ways,
    recomputing correlations each time, then converts observed correlations to
    Z-scores relative to the null.

    Parameters
    ----------
    data : np.ndarray, shape (n_neurons, n_frames)
        Binarized (or continuous) activity matrix.
    n_shuffles : int
        Number of shuffle iterations (more = more stable null distribution).
    method : str
        How to destroy the cross-neuron signal while keeping each neuron's
        own statistics:

        * ``'circular'``  — shift each neuron's trace by a random lag (wraps
          around); **preserves autocorrelation** of individual neurons.
          Best choice for correlation significance testing.
        * ``'random'``    — randomly permute the frames of each neuron
          independently; destroys both autocorrelation and cross-correlations.
          Most aggressive / most liberal.
        * ``'vertical'``  — randomly swap neuron identities at each shuffle;
          preserves all temporal structure but destroys neuron–neuron assignment.
    rng_seed : int
        Random seed for reproducibility.

    Returns
    -------
    corr_obs : np.ndarray, shape (n, n)  — observed correlation matrix (diagonal = NaN)
    z_scores : np.ndarray, shape (n, n)  — Z-score of each observed pair vs null
    sig_mask : np.ndarray[bool]          — True where Z > 2.58 (p < 0.005)
    n_sig    : int                       — number of significant pairs (unique)
    """
    n_sub, n_frames = data.shape
    rng = np.random.default_rng(rng_seed)

    corr_obs = np.corrcoef(data)
    np.fill_diagonal(corr_obs, np.nan)

    null_corrs = []
    for _ in range(n_shuffles):
        if method == 'circular':
            shifts   = rng.integers(0, n_frames, size=n_sub)
            shuffled = np.array([np.roll(data[i], shifts[i]) for i in range(n_sub)])
        elif method == 'random':
            shuffled = np.array([rng.permutation(data[i]) for i in range(n_sub)])
        elif method == 'vertical':
            shuffled = data[rng.permutation(n_sub)]
        else:
            raise ValueError(f"method must be 'circular', 'random', or 'vertical'; got '{method}'")
        c = np.corrcoef(shuffled)
        np.fill_diagonal(c, np.nan)
        null_corrs.append(c)

    null_arr  = np.array(null_corrs)                           # (n_shuffles, n, n)
    z_scores  = ((corr_obs - np.nanmean(null_arr, axis=0))
                 / (np.nanstd(null_arr, axis=0) + 1e-10))
    sig_mask  = z_scores > 2.58
    np.fill_diagonal(sig_mask, False)
    n_sig     = int(sig_mask.sum()) // 2
    return corr_obs, z_scores, sig_mask, n_sig


def plot_pca_3d(pc_list, var_list, titles, color_by=None):
    """Side-by-side 3D PCA scatter plots.

    Each panel shows the population activity trajectory in the space of the
    first three principal components.  Points are colored by time (or by a
    custom array) to reveal any temporal structure (e.g., a ring arising from
    spatial navigation).

    Parameters
    ----------
    pc_list : list of np.ndarray, each shape (n_timepoints, 3)
        PC-projected time series for each condition/representation.
    var_list : list of np.ndarray, each shape (3,)
        Explained variance (%) for PC1/PC2/PC3 per condition.
    titles : list[str]
        Subplot titles (one per element of ``pc_list``).
    color_by : np.ndarray or None
        Values used to color the scatter points.  If None, colors by time index.

    Returns
    -------
    fig
    """
    n = len(pc_list)
    fig = plt.figure(figsize=(7 * n, 5))
    for idx, (pc, var, title) in enumerate(zip(pc_list, var_list, titles)):
        ax = fig.add_subplot(1, n, idx + 1, projection='3d')
        c = color_by if color_by is not None else np.arange(len(pc))
        ax.scatter(pc[:, 0], pc[:, 1], pc[:, 2],
                   c=c, cmap='plasma', s=1, alpha=0.4)
        ax.set_xlabel(f'PC1 ({var[0]:.1f}%)')
        ax.set_ylabel(f'PC2 ({var[1]:.1f}%)')
        ax.set_zlabel(f'PC3 ({var[2]:.1f}%)')
        ax.set_title(f'PCA — {title}')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
    fig.suptitle('3D PCA of population activity (colored by time)', y=1.01)
    #plt.tight_layout()
    return fig
