# OpenEnv: SQLite Retail Data Environment

A fully standard-compliant OpenEnv specification environment replicating a real-world Data Engineering / Data Analysis task.

## Description

This `OpenEnv` sandbox provides AI agents with an interactive SQLite database (e-commerce scenario) to assess their Data Engineering capability. It implements the standard Gymnasium-style `step()` / `reset()` / `state()` HTTP JSON API endpoints natively compatible with the OpenEnv Hub and Hugging Face Docker Spaces.

### Action Space
The agent responds with a JSON `Action` model:
- `query` (string, optional): A SQL command to execute (SELECT, INSERT, UPDATE, etc.) inside the sandbox.
- `submit_answer` (string, optional): Submit a final string answer to complete the task and receive a grade.

### Observation Space
The environment responds with a JSON `Observation` model:
- `result` (string): The output of the query block (Pandas DataFrame as string, rowcount, or response acknowledgement text).
- `error` (string, optional): Stack trace / SQL Syntax Error if the query fails.

## Tasks & Agent Graders

The environment comes populated with 3 scenarios progressing in difficulty:
1. **Easy Task**: Calculate the total revenue from all `COMPLETED` orders. The Grader parses the correct integer matching the actual SQL engine calculation.
2. **Medium Task**: Cancel all pending orders placed by specific clients. The Grader verifies that specific row statuses have been successfully pushed with the `UPDATE` mutation.
3. **Hard Task**: Discover the top product categories driving maximal revenue. The Grader matches the output category against complex `JOIN` logic ensuring the query logic aligns with standard relational properties.

> Scores/rewards are floating values constrained between `0.0` and `1.0`. 

## Setup Instructions

### 1. Local Deployment (FastAPI natively)
```bash
pip install -r requirements.txt
uvicorn app:app --port 7860
```

### 2. Hugging Face Spaces (Docker)
This repository is configured correctly with a standard `openenv.yaml` and a `Dockerfile`.
Upload the dataset to a new Docker Hugging Face Space. Port `7860` is automatically exposed.

## Execution Baseline Evaluation
Run `inference.py` to test the HTTP APIs in sequence using baseline queries resulting in a full 1.0 (100%) score sequence:
```bash
python inference.py
```
