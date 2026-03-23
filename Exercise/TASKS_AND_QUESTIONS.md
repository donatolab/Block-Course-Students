# Block Course – Tasks and Questions Overview

This document provides a complete list of all tasks and questions that students will encounter throughout the course.

---

## Task 0: Python Basics

**Goal:** Get comfortable with Python syntax, variables, lists, arrays, matrices, loading data, indexing, slicing, and logical operations.

### Guided Exercises

| # | Topic | Description |
|---|-------|-------------|
| 1 | Creating Variables | Create variables `a` and `b`, calculate their sum |
| 2 | Lists and Arrays | Create a Python list and convert it to a NumPy array |
| 3 | Creating Ranges | Use `np.arange()` to create ranges with different step sizes |
| 4 | Matrices | Create a 2D NumPy array (matrix) |
| 5 | Loading Data | Load a `.csv` file using Pandas |
| 6 | Indexing and Slicing | Access specific elements, rows, columns, and blocks from a matrix |
| 7 | Pandas DataFrames | Work with DataFrames, use `.loc[]` and `.iloc[]` for slicing |
| 8 | Logical Operations | Use comparison operators and boolean indexing on arrays |
| 9 | Getting Help | Use `help()` and `?` to read function documentation |

### Test Your Skills

| # | Question |
|---|----------|
| 1 | Find a NumPy function to sum all values in a matrix and read its documentation |
| 2 | Calculate the sum of the center 3×3 block of the magic square matrix |
| 3 | Calculate the sum of all rows of the magic square matrix |

---

## Task 1: Neuronal Activity Analysis

**Goal:** Explore calcium imaging data from hippocampal neurons. Analyze dF/F fluorescence traces, binarize activity, compare binarization methods, investigate correlation structure, cluster neurons into functional groups, and test statistical significance with shuffle methods.

Data: `dF_F_traces.npz` (432 neurons × 36025 frames), `binarized_traces.npz` (432 neurons × 36025 frames, our-extracted)

### Questions

| # | Question |
|---|----------|
| Q1.1 | What does dF/F represent biologically? What does a high dF/F value indicate? |
| Q1.2 | What does the pairwise correlation matrix of 4 neurons tell you? What do values near 1 and near 0 indicate? |
| Q1.3 | What is the effect of a low vs. high threshold on binarization? What are the consequences of each? |
| Q1.4 | How does binarization change the correlation structure compared to continuous dF/F? |
| Q1.5 | Compare the threshold-based and algorithm-based binarizations. Do they capture the same events? Does one seem more sensitive or specific than the other? |
| Q1.6 | What do the clusters in hierarchical clustering of the full population reveal? |
| Q1.7 | What does the Sankey plot show when comparing dF/F vs. binarized clustering? |
| Q1.8 | Which shuffling method is most appropriate for testing pairwise correlations, and why? |

### Coding Tasks

| # | Task |
|---|------|
| T1.1 | Load `dF_F_traces.npz` and inspect the shape |
| T1.2 | Select 4 random neurons and plot their dF/F traces as line plots over time |
| T1.3 | Compute and visualize the pairwise correlation matrix for the 4 neurons |
| T1.4 | Binarize dF/F traces using at least 3 different threshold values; overlay on continuous traces |
| T1.5 | Compute the correlation matrix of the binarized 4 neurons; compare to the dF/F matrix |
| T1.6 | Load `binarized_traces.npz` (algorithm-based); compare mean firing rate and overlay both binarizations on dF/F traces for the 4 selected neurons |
| T1.7 | Compute and visualize the full correlation matrix for all neurons with hierarchical clustering (both dF/F and binarized) |
| T1.8 | Create a raster plot sorted by mean firing rate |
| T1.9 | Build a Sankey/alluvial diagram comparing cluster assignments from dF/F vs. binarized clustering |
| T1.10 | Implement a shuffle test (try circular, random, and vertical methods) and visualize the significant correlation network; validate using a randomized control dataset |

---

## Task 2: Behavioral Data Analysis

**Goal:** Move from raw DeepLabCut tracking data to calibrated behavioral metrics. Assess tracking quality, select the best-tracked body part, apply coordinate calibration and smoothing, then compute distance and speed.

Data: `raw_trackingdata.npz` (36000 frames × 43 columns), `head_neck.npz` (36000 frames × 3 columns), `arena_still_frame.png`

### Questions

| # | Question |
|---|----------|
| Q2.1 | What does the DeepLabCut data matrix contain and how is it structured? What does each column group represent? |
| Q2.2 | What statistical measure is used to assess tracking quality per body part, and why is it appropriate? |
| Q2.3 | Which body part is best tracked and why? What feature of body part position affects tracking reliability? |
| Q2.4 | What does the smoothing parameter `k` control? What are the trade-offs between large and small `k`? |
| Q2.5 | How is the coordinate system shifted to the arena origin? What information do you need? |
| Q2.6 | Why does the distance array have N−1 values for N position values? |
| Q2.7 | How is the pixel-to-cm calibration factor computed? What measurements are required? |
| Q2.8 | How is distance per frame converted to speed in cm/s? What is the role of the frame rate? |

### Coding Tasks

| # | Task |
|---|------|
| T2.1 | Load `raw_trackingdata.npz` and inspect the matrix shape and column structure |
| T2.2 | Extract likelihood columns using stride slicing (`[:, 3::3]`) |
| T2.3 | Compute mean likelihood per body part and plot a bar chart |
| T2.4 | Plot the raw trajectory of the best-tracked body part (invert Y-axis) |
| T2.5 | Load `head_neck.npz` and the arena still frame; identify the corner reference point |
| T2.6 | Shift the coordinate system to the arena origin |
| T2.7 | Apply a rolling mean (k=20) and compare smoothed vs. raw trajectory |
| T2.8 | Compute Euclidean frame-to-frame displacement using `np.diff()` |
| T2.9 | Convert pixel displacement to centimetres using the arena calibration |
| T2.10 | Compute speed in cm/s and visualize speed over time and trajectory colored by speed |

---

## Task 3: Integration and Place Cells

**Goal:** Link behavioral state to neuronal activity. Segment behavior into running and resting, construct raster plots with speed overlay, map individual neuron activity to arena positions, and identify place cells.

Data: `binarized_traces.npz` (36025 frames × 365 neurons), `head_neck_smooth.npz` (36000 frames × 2), `speed.npz` (36000 frames × 1)

### Questions

| # | Question |
|---|----------|
| Q3.1 | Why should you truncate (not zero-pad) when aligning neural and behavioral data with different frame counts? |
| Q3.2 | How do you choose the smoothing window `k` and speed threshold for running detection? Justify biologically. |
| Q3.3 | What running/resting ratio do you observe? Is this expected? What would cause a ratio outside the typical range? |
| Q3.4 | What patterns are visible in the raster plot when speed is overlaid? Do network events co-occur with running? |
| Q3.5 | How do you identify a place cell from a spatial firing map? What distinguishes it from a non-place cell? |
| Q3.6 | How does the Task 1 correlation structure relate to observed place fields? |

### Coding Tasks

| # | Task |
|---|------|
| T3.1 | Load all three NPZ datasets and print their shapes |
| T3.2 | Align frame counts by truncating to the minimum length |
| T3.3 | Smooth speed with k=10 and binarize running with a 4 cm/s threshold |
| T3.4 | Compute and report the running/resting ratio |
| T3.5 | Build the enriched raster plot: neural activity + firing rate + network event rate + speed overlay |
| T3.6 | Extract active-frame positions for a single neuron and plot on the trajectory |
| T3.7 | Build a 4×4 grid of spatial firing maps for 16 different neurons |
| T3.8 | Identify and describe at least one strong place-cell candidate and one non-place-cell |

---

## Summary

| Task | Topic | Key Skills |
|------|-------|------------|
| **Task 0** | Python Basics | Variables, arrays, matrices, loading CSV, indexing, slicing, logic |
| **Task 1** | Neuronal Activity Analysis | dF/F, binarization, binarization method comparison, correlation matrices, hierarchical clustering, Sankey, shuffle tests |
| **Task 2** | Behavioral Data Analysis | Tracking quality, trajectory extraction, coordinate calibration, smoothing, distance, speed |
| **Task 3** | Integration and Place Cells | Frame alignment, run/rest segmentation, raster + behavior, spatial firing maps, place cells |
