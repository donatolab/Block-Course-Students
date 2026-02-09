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

## Task 1: Tracking Data Analysis (DeepLabCut)

**Goal:** Load and inspect DeepLabCut tracking data, analyze estimator quality, and identify the most reliable body part for tracking.

### Questions

| # | Question |
|---|----------|
| Q1.1 | What are the dimensions of the tracking data matrix? How many time points, rows, and columns does it have? |
| Q1.2 | Inspect the first 5 rows and columns of the matrix. What do they represent? |
| Q1.3 | Extract the first column — which part of the data does it represent? |
| Q1.4 | What does the first row represent? |
| Q1.5 | After watching the DLC tracking video, which body part do you expect to be tracked best? Which is tracked worst? |
| Q1.6 | What are the column indices for the first body part's data (X, Y, Likelihood)? |
| Q1.7 | Think of a statistical operation to calculate the overall tracking accuracy for each body part. The output should be a single value per body part. |
| Q1.8 | What is the best-tracked body part according to the estimator values? Why is your chosen operator more suitable than others? |
| Q1.9 | The estimator matrix has different dimensions than the raw matrix. What are they? What do we need to keep in mind when mapping back to the raw data? |

### Coding Tasks

| # | Task |
|---|------|
| T1.1 | Load `Bodyparts.csv` and `raw_trackingdata.csv` using Pandas |
| T1.2 | Extract estimator (likelihood) columns by slicing every 3rd column |
| T1.3 | Calculate a summary statistic (mean) for each body part's estimator |
| T1.4 | Plot the trajectory of the best-tracked body part |

---

## Task 2: Behavioral Metrics (Speed & Distance)

**Goal:** Calculate physical metrics like distance and speed from tracking coordinates, including coordinate correction, smoothing, and unit conversion.

### Questions

| # | Question |
|---|----------|
| Q2.1 | Look at the `head_neck` matrix — what data is given in each column? |
| Q2.2 | How can we calculate coordinates for a new reference point? What information do we need? |
| Q2.3 | What are the X and Y pixel coordinates for the upper-left corner of the arena? |
| Q2.4 | What does the smoothing parameter `k` do? How does the rolling mean smoothing work? |
| Q2.5 | What happens when you increase the `k` value? How does the plot change? |
| Q2.6 | Why do we calculate `to_x - from_x` and `to_y - from_y` in the Pythagorean equation? |
| Q2.7 | In what unit is the distance between two points of an image given? |
| Q2.8 | What is the length of the arena side wall in pixels? What is the cm/pixel ratio? |
| Q2.9 | How many distance values do we have compared to position values? Why? |
| Q2.10 | How do we convert the frame-based time scale to seconds? |

### Coding Tasks

| # | Task |
|---|------|
| T2.1 | Load `head_neck.csv` and the arena still-frame image |
| T2.2 | Find the pixel coordinates of the arena corner and shift the coordinate system |
| T2.3 | Smooth X and Y coordinates using `rolling().mean()` |
| T2.4 | Calculate the Euclidean distance between the first two consecutive points |
| T2.5 | Calculate distances between all consecutive frames using `np.diff()` |
| T2.6 | Convert pixel distances to centimeters using a calibration factor |
| T2.7 | Calculate total distance traveled in cm and meters |
| T2.8 | Calculate speed in cm/s using the frame rate (20 Hz) |

---

## Task 3: Neuronal Activity & Place Cells

**Goal:** Correlate animal behavior (running vs. resting) with calcium imaging data and discover Place Cells in the hippocampus.

### Questions

| # | Question |
|---|----------|
| Q3.1 | How do you choose the `k` value for smoothing the speed? What biological and computational aspects do you consider? |
| Q3.3 | Find a good lower-bound threshold for running speed. What ratio of running vs. resting frames do you get? Is this expected? |
| Q3.4 | Did your considerations turn out as expected? If not, explain why and how you adjusted. |
| Q3.6 | How many cells were detected in the dataset? (Derive from matrix dimensions) |
| Q3.7 | What can you derive from the raster plot? Where do neuronal events have the highest frequency? |
| Q3.8 | Calculate the smoothed event rate for the entire neuronal network. |
| Q3.9 | Plot the animal's running path and overlay neuronal events. Identify Place Cells vs. non-Place Cells. |

### Coding Tasks

| # | Task |
|---|------|
| T3.1 | Load speed data and smooth it using a rolling mean |
| T3.2 | Binarize behavior into running and resting using a speed threshold |
| T3.3 | Calculate the percentage of time the animal spends running |
| T3.4 | Load binarized neuronal traces and inspect the raster plot |
| T3.5 | Calculate and plot the smoothed event rate across all neurons |
| T3.6 | Load smoothed coordinates and extract activity for a single cell |
| T3.7 | Plot neuronal activity overlaid on the animal's trajectory |
| T3.8 | Explore multiple cells and compare Place Cells vs. non-Place Cells in a grid |

---

## Summary

| Task | Topic | Key Skills |
|------|-------|------------|
| **Task 0** | Python Basics | Variables, arrays, matrices, loading CSV, indexing, slicing, logic |
| **Task 1** | Tracking Data | Loading DLC data, inspecting matrices, estimator analysis, plotting trajectories |
| **Task 2** | Behavioral Metrics | Coordinate correction, smoothing, Euclidean distance, unit conversion, speed |
| **Task 3** | Neuronal Activity | Behavior binarization, raster plots, event rates, Place Cell discovery |
