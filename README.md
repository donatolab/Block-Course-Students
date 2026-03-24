# Block Course - Student Exercises

Welcome to the Block Course on Behavioral and Neuronal Data Analysis!

This repository contains the exercises you will need to complete during the course. The course is designed to take you from the basics of Python programming to advanced topics like analyzing behavioral tracking data and correlating it with neuronal activity.

## Course Structure

The course is divided into 4 tasks, each building on the previous one:

*   **Task 0**: Python Basics — A warm-up to get comfortable with Python syntax, lists, arrays, indexing, slicing, and loading data.
*   **Task 1**: Neuronal Activity Analysis — Loading and exploring calcium imaging dF/F traces, binarizing activity, computing correlation matrices, hierarchical clustering, shuffle tests, and PCA.
*   **Task 2**: Behavioral Data Analysis — Assessing DeepLabCut tracking quality, calibrating coordinates, smoothing trajectories, and converting position data to distance and speed.
*   **Task 3**: Integration and Place Cells — Combining neural and behavioral data to segment running/resting states, explore population dynamics, and discover place cells.

📋 For a detailed overview of all tasks and questions, see [**Exercise/TASKS_AND_QUESTIONS.md**](Exercise/TASKS_AND_QUESTIONS.md).

## Getting Started

To get started, you will need to set up your computer with the necessary tools. Please follow the instructions below carefully.

### 1. Install Visual Studio Code (VS Code)

VS Code is a powerful and popular code editor that we will use to write and run our Python code.

1.  Go to the [VS Code Website](https://code.visualstudio.com/).
2.  Download the installer for your operating system.
3.  Run the installer and follow the instructions.

### 2. Install VS Code Extensions

VS Code needs some extensions to work well with Python and Jupyter Notebooks.

1.  Open VS Code.
2.  Click on the Extensions icon in the Activity Bar on the side of the window (or press `Ctrl+Shift+X`).
3.  Search for and install the following extensions:
    *   [**XLSX, CSV, TSV & Markdown Editor**](https://marketplace.visualstudio.com/items?itemName=Muhammad-Ahmad.xlsx-viewer)
    *   [**Python**](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
    *   [**Jupyter**](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)
    *   [**Data Wrangler**](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.datawrangler)
    *   [**TODO Highlight**](https://marketplace.visualstudio.com/items?itemName=wayou.vscode-todo-highlight)
4.  Additional recommended extensions:
    *   [**GitHub Copilot Chat**](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)

### 3. Install Python (Miniconda)

We recommend using **Miniconda**, a minimal installer for Conda. Conda is an open-source package and environment management system.

1.  Go to the [Miniconda Download Page](https://www.anaconda.com/download/success).
2.  Download the installer for your operating system (Windows, macOS, or Linux).
3.  Run the installer and follow the on-screen instructions.
    *   **Windows Users**: It is recommended to check the box "Add Miniconda3 to my PATH environment variable" only if you know what you are doing. Otherwise, use the "Anaconda Prompt" (search for it in the Start Menu) to run conda commands.

### 4. Create the Course Environment

We have provided a file called `environment.yml` which lists all the Python libraries (packages) we will use. Conda will read this file and create a specific "environment" for this course. This keeps our course tools separate from other things on your computer.

1.  Download [this repository](https://github.com/donatolab/Block-Course-Students/archive/refs/heads/master.zip) and extract the content from the .zip file.
2.  Open the **Anaconda Prompt** (Windows) or Terminal (macOS/Linux).
3.  Navigate to this folder (the folder where this README is located).
    *   *Tip: You can copy the path from your file explorer and type `cd ` followed by pasting the path.*
    *   Example: `cd "C:\Users\YourName\Documents\Block Course\Block-Course-Students"`
4.  Run the following command:
    ```bash
    conda env create -f environment.yml
    ```
5.  Wait for the installation to finish. It might take a few minutes.

### 5. Start Working

1.  Open VS Code.
2.  Go to **File > Open Folder...** and select this folder.
3.  Open the first exercise notebook: `Exercise/Task 0/Task0.ipynb`.
4.  **Select the Kernel**:
    *   In the top-right corner of the notebook editor, you will see a "Select Kernel" button (or it might say "Python 3...").
    *   Click it and select **Python Environments...**.
    *   Choose the environment we just created, which should be named `block_course`.
5.  You are now ready to run the cells and write code!

## Directory Structure

```
Block-Course-Students/
├── environment.yml               # Conda environment definition
├── README.md                     # This file
└── Exercise/
    ├── TASKS_AND_QUESTIONS.md    # Overview of all tasks and questions
    ├── helper.py                 # Shared visualization and data-loading helpers
    ├── Task 0/                   # Python Basics
    │   ├── Task0.ipynb
    │   └── magic.csv
    ├── Task 1/                   # Neuronal Activity Analysis
    │   ├── Task1.ipynb
    │   ├── dF_F_traces.npz       # dF/F fluorescence traces  (432 neurons × 36025 frames)
    │   ├── binarized_traces.npz  # CNMF binarized traces     (432 neurons × 36025 frames)
    │   └── raw_trackingdata.npz  # DeepLabCut tracking data  (36000 frames × 43 columns)
    ├── Task 2/                   # Behavioral Data Analysis
    │   ├── Task2.ipynb
    │   ├── head_neck.npz         # Head-neck coordinates     (36000 frames × 3 columns)
    │   └── arena_still_frame.png # Arena reference image
    └── Task 3/                   # Integration and Place Cells
        ├── Task3.ipynb
        ├── binarized_traces.npz  # Curated neural traces     (36025 frames × 365 neurons)
        ├── head_neck_smooth.npz  # Smoothed position         (36000 frames × 2 columns)
        └── speed.npz             # Speed in cm/s             (36000 frames × 1 column)
```

## Need Help?

If you get stuck, don't hesitate to ask the tutors! Also remember:
- Use `help(function_name)` or `function_name?` in Python to read documentation.
- Google your error messages — most Python errors have been encountered (and solved!) by others before.
- The [Python documentation](https://docs.python.org/3/) and [NumPy documentation](https://numpy.org/doc/) are great references.
