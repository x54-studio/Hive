
# Contributing to Hive

Thank you for your interest in contributing to the Hive project! This document describes how to set up your local environment, run lint checks, and follow our coding standards for both the back end and front end.

## Table of Contents
1. [Development Prerequisites](#development-prerequisites)  
2. [Repository Structure](#repository-structure)  
3. [Setting Up Python Linting](#setting-up-python-linting)  
4. [Managing Python Dependencies](#managing-python-dependencies)  
5. [Setting Up JavaScript Linting](#setting-up-javascript-linting)  
6. [Running and Fixing Lint Checks](#running-and-fixing-lint-checks)  
7. [Pull Requests](#pull-requests)

---

## Development Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)  
- [Node.js 16+ and npm](https://nodejs.org/)  
- A Git client (e.g., Git CLI or GitKraken)  
- Basic familiarity with Docker (optional, but recommended for containerizing your environment)

---

## Repository Structure

Below is a simplified version of our directory layout:

```
PROJECT_ROOT/
├─ backend/
│  ├─ .flake8             # Flake8 config
│  ├─ .pylintrc           # Pylint config
│  ├─ requirements.txt
│  └─ ...
├─ frontend/
│  ├─ eslint.config.mjs   # ESLint config
│  ├─ .prettierrc         # Prettier config
│  └─ ...
├─ CONTRIBUTING.md
└─ ...
```

---

## Setting Up Python Linting

1. **Install Dependencies**  
   - In the `backend/` folder, install Python packages (including linters):  
     ```bash
     cd backend
     pip install -r requirements.txt
     ```
   - This should install **Flake8**, **Black**, **Pylint**, and any additional dependencies.

2. **Configuration Files**  
   - `.flake8`  
   - `.pylintrc`  
   - These files define our Python style and linting rules.  
   - **Do not** modify them without team approval.

---

## Managing Python Dependencies

When you add new libraries in the **backend**, you’ll need to update `requirements.txt`. We recommend using [pipreqs](https://github.com/bndr/pipreqs) to automatically scan your imports and generate or update the requirements file:

```bash
cd backend
pipreqs .
```

This command outputs a fresh `requirements.txt` based on your code’s dependencies.

> **Important**: After running `pipreqs .`, **manually replace** `bcrypt==4.2.1` (or confirm that exact line is preserved). Pipreqs sometimes picks a conflicting library name or version (such as `py-bcrypt`), so it’s crucial to keep `bcrypt==4.2.1` in the file.

---

## Setting Up JavaScript Linting

1. **Install Dependencies**  
   - In the `frontend/` folder, install Node.js modules:  
     ```bash
     cd frontend
     npm install
     ```
   - This installs **ESLint** and **Prettier** (along with other frontend dependencies).

2. **Configuration Files**  
   - `eslint.config.mjs`  
   - `.prettierrc`  
   - These files define the JavaScript and JSX styling rules.  
   - Keep any changes consistent with our project standards.

---

## Running and Fixing Lint Checks

Below are the common commands for linting and formatting. Please run these **before** committing any new changes, so your pull requests remain clean.

### Python Commands

```bash
# Flake8
cd backend
flake8 .
```
- Checks for style issues based on `.flake8`.

```bash
# Black
black .
```
- Automatically formats Python code in-place.

```bash
# Pylint
pylint app/ tests/ --rcfile=.pylintrc
```
- Performs deeper code analysis on the specified directories.

### JavaScript Commands

```bash
# ESLint
cd frontend
npx eslint . --config ./eslint.config.mjs
```
- Checks your JS/JSX files for errors and style issues.

```bash
# Prettier (Dry Run)
npx prettier --config .prettierrc --check .
```
- Displays any formatting issues without modifying files.

```bash
# Prettier (Fix in Place)
npx prettier --config .prettierrc --write .
```
- Automatically fixes formatting issues.

---

## Pull Requests

1. **Create a Feature Branch**  
   - Use a descriptive name for your branch, e.g. `feature/add-article-search`.

2. **Implement and Test**  
   - Add unit/integration tests if you introduce new functionality.

3. **Run Lint Checks**  
   - **Python**: `flake8 .`, `black .`, `pylint ...`  
   - **JavaScript**: `eslint .`, `prettier --check .`

4. **Submit a Pull Request**  
   - Make sure your PR description includes:
     - A summary of changes.
     - Any relevant issue references.
     - Confirmation you’ve run lint checks and resolved issues.

5. **Code Review and Merge**  
   - Once we implement a CI pipeline, it will run lint checks automatically.
   - For now, please ensure all checks pass locally before merging.
   - If any checks fail, please address them before merging.

---

## Questions or Feedback?

If you have any questions about the guidelines, codebase, or contribution process, feel free to:
- Ask in our team Slack channel.
- Open a GitHub issue with the “question” label.
- Mention one of the core maintainers in your pull request.

Thank you for helping us maintain a clean, consistent codebase for Hive!