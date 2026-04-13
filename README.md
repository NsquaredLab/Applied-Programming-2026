# Applied Programming 2026

Welcome, Students! 👋

This repository contains exercises and materials for the Applied Programming course in 2026. We're excited to have you on the first version of this course!

---

## Exercise Preparation

Before starting the exercises, please complete the following setup steps. This ensures that everyone has a consistent development environment.

### 1. Create a GitHub Account

You will need a GitHub account to access repositories and submit your work.

* Sign up here: [https://github.com/](https://github.com/)

---

### 2. Install Git

Git is required to clone and manage repositories.

* Download Git: [https://git-scm.com/downloads](https://git-scm.com/downloads)

* Verify installation (optional):

```bash
git --version
```

---

### 3. Install Python 3.13

We will use Python 3.13 for this course.

* Download Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)

* Make sure to check **"Add Python to PATH"** during installation (Windows)

* Verify installation:

```bash
python --version
```

---

### 4. Install an IDE (Choose One)

You need a code editor or IDE to work on the exercises.

#### Option A: PyCharm (Recommended)

* Download: [https://www.jetbrains.com/pycharm/](https://www.jetbrains.com/pycharm/)
* Student license (free): [https://www.jetbrains.com/community/education/#students](https://www.jetbrains.com/community/education/#students)

#### Option B: VS Code

* Download: [https://code.visualstudio.com/](https://code.visualstudio.com/)
* Recommended extension: Python (by Microsoft)

---

### 5. Install uv

We use `uv` to manage Python dependencies.

**Windows:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**

```bash
curl -sSf https://astral.sh/uv/install.sh | bash
```

* Official documentation: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)

---

### ✅ Final Check

Before proceeding, make sure:

* GitHub account is created
* Git is installed and working
* Python 3.13 is installed
* IDE is installed
* `uv` is installed

---

## Getting Started

### Fork the Repository

Before you start, click the **"Fork"** button on GitHub (top right of this repository page). This creates your own copy of the repository under your account.

---

### Cloning the Repository

Now you will download your fork to your computer.

#### Step 1: Open a Terminal (Command Line)

If you have never used a terminal before, here are simple ways to open one:

**Option A (Recommended – easiest):**

* Open the folder where you want to store the project (e.g., Documents)
* Right-click inside the folder
* Select **"Open in Terminal"** or **"Open PowerShell window here"** (Windows)

**Option B:**

* Press `Windows Key + R`
* Type `cmd` and press Enter

---

#### Step 2: Navigate to a Folder (if needed)

If you opened `cmd` directly, you may need to move to a folder where you want to store the project.

Use the `cd` command ("change directory"):

```bash
cd Documents
```

You can always check where you are with:

```bash
pwd
```

---

#### Step 3: Clone Your Repository

Go to your fork on GitHub and copy the repository URL (green **Code** button).

Then run:

```bash
git clone YOUR_FORK_URL
```

---

#### Step 4: Open the Project Folder

After cloning, move into the project directory:

```bash
cd applied-programming
```

You are now ready to start working with the project locally.

---

### Setting Up Your Environment

After installing uv and cloning the repository, simply run:

```bash
uv sync
```

This will install all required dependencies for the course exercises.

---

### Running Exercises with Marimo

We will use Marimo, a reactive Python notebook, for some exercises. Marimo notebooks are stored as pure Python files (`.py`) and can be run interactively as web applications.

To run the first exercise, navigate to the project's root directory in your terminal and execute:

```bash
uv run marimo run exercises/01/01_understand_git.py
```

This command launches the exercise as an interactive app in your browser.

---

## Recommended Tools

Here are the IDEs that we previously worked with and thus know how to fix most problems:

* **PyCharm Professional** - Full-featured Python IDE (free for students)

  * Download: [https://www.jetbrains.com/pycharm/](https://www.jetbrains.com/pycharm/)
  * Student license: [https://www.jetbrains.com/community/education/#students](https://www.jetbrains.com/community/education/#students)

* **VS Code** - A lightweight, powerful code editor with excellent Python support

  * Download: [https://code.visualstudio.com/](https://code.visualstudio.com/)

---

## Important Note on AI Tools

> [!WARNING]
> As you are learning to program, **DO NOT** use AI tools like ChatGPT or GitHub Copilot for generating code in this course.
>
> At this stage in your learning journey, you need to:
>
> * Understand the logic behind each line of code you write
> * Experience the problem-solving process
> * Learn from your mistakes
> * Develop debugging skills
>
> **What is allowed**: Basic autocompletion features that your IDE provides.
>
> **What is not allowed**: Asking AI to write code solutions for your assignments.

> [!CAUTION]
> Be wary of "vibe coding" - where AI tools generate complete code based on vague requirements. For effective learning, YOU should provide the programming approach and logic.

---

## Course Structure

Each week's exercises will be organized in separate folders. Check the course schedule for deadlines and requirements.

---

## Getting Help

* Use the course forum for questions
* Attend office hours
* Form study groups with classmates

---

Happy coding! 🚀
