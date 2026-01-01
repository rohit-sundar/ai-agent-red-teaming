## Overview

This is a security-AI combined mini research project which involves red teaming against simple AI agents. The agent is a python coding agent based on [freeCodeCamp.org x Boot.dev's tutorial](https://youtu.be/YtHdaXuOAks?si=iwdqDT9TP7n_mZBS) and uses the [AgentFence](https://github.com/agentfence/agentfence) framework for testing the AI agent.

## Installation
Prerequisites

- Python 3.13 or newer
- A Gemini API key (set in `GEMINI_API_KEY`)

### Install `uv`

```bash
pip install uv
```
### Initializing the project

```bash
uv init
```
### Creating a virtual environment

```bash
uv venv
```
### Activate the virtual environment
- **Windows (PowerShell)**
```powershell
.\.venv\Scripts\activate.ps1
```
- **Linux / macOS**
```bash
source .venv/bin/activate
```
### Installing required dependencies
The `pyproject.toml` specifies the dependencies:
- `agentfence`
- `google-genai`
- `python-dotenv`

Install them with:

```bash
uv sync
```
This will install dependencies and lock them into the environment.

## Configuration

Create a `.env` file in the project root and add your Gemini API key:

```
GEMINI_API_KEY="<gemini-api-key>"
```
Environment variables are loaded via `python-dotenv` at runtime.

You can also configure tuning parameters such as:
- MAX_CHARS – maximum characters to read from a file
- MAX_ITERS – maximum number of agentic loop iterations

in `config.py`.

## Usage

Run the CLI agent with a short prompt:

```bash
python main.py "Fix my calculator app; it’s not working correctly."
```

The agent will iteratively call the available tools (`get_files_info`, `get_file_content`, `run_python_file`, `write_file`) while staying within the configured working directory.

### Run function-level tests
Ad-hoc tests for helper functions under `functions/`:

```bash
python function_tests.py
```
### Run AgentFence probes
Run AgentFence probes againtst the agent (requires `agentfence` and a valid `GEMINI_API_KEY`):

```bash
python agent_tests.py
```

## Features

- Gemini-based `CodingAgent` with function-call tools for file inspection, editing, and execution.
- An AgentFence wrapper for Gemini-based agents and evaluator integration for running security probes (prompt injection, secret leakage, etc.).
- Utilities under `functions/` designed to be invoked by model function-calls with path restricted to a working directory.

## Project Structure
- `main.py` — CLI entrypoint for the `CodingAgent`.
- `call_function.py` — Adapter mapping model function-calls to local helper functions in `functions/`.
- `functions/` — Tool implementations used by the agent:
  - `get_files_info.py` — list a directory's contents (shows size and is_dir flag)
  - `get_file_content.py` — read a file (truncated at `MAX_CHARS`)
  - `write_file.py` — create/overwrite files safely inside the working dir
  - `run_python_file.py` — run a Python script and capture stdout/stderr
- `agentfence_gemini/` — AgentFence-compatible wrapper and evaluator for Gemini
- `function_tests.py` — Manual tests for the `functions/` utilities
- `agent_tests.py` — Runs AgentFence probes against the agent
- `config.py` — Configuration constants (`MAX_CHARS`, `MAX_ITERS`)

The default working directory used by `call_function` is `calculator`. All file operations are intentionally constrained to that directory to prevent escape and accidental modification of unrelated files.