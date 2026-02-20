# MLOps Trading Signal Generator

A miniature MLOps pipeline demonstrating reproducibility, deployment, logging, and metrics output.

## 1. Setup Instructions
To set up the environment locally, install the required dependencies:
```bash
# MLOps Trading Signal Generator

## Task Overview
This project is a miniature MLOps pipeline developed to demonstrate the principles of reproducibility, fundamental deployment, structured logging, and automated metrics output. It simulates the backend data processing workload for a trading system by ingesting cryptocurrency OHLCV data, computing rolling statistical indicators, and generating binary trading signals.

## Project Workflow: What I Have Done
To build this production-ready pipeline, I implemented the following steps:

1. **Configuration & Determinism:** The pipeline reads inputs through a Command-Line Interface (CLI). I set it to dynamically load parameters (like the random seed and rolling window size) from an external `config.yaml` file. Setting a strict random seed ensures the entire execution is 100% reproducible.
2. **Data Ingestion & Validation:** The script loads the dataset (`data.csv`) into a Pandas DataFrame. I added robust error handling to validate that the required `close` price column exists and to safely catch edge cases like missing or empty files without crashing.
3. **Algorithmic Signal Generation:** The core logic calculates a rolling mean on the closing price based on the configured window size. It then generates a binary trading signal (1 if the close price is greater than the rolling mean, and 0 otherwise).
4. **Metrics Calculation & JSON Export:** The system tracks the total execution time (`latency_ms`) and the `signal_rate`. It writes these results to a machine-readable JSON file (`metrics.json`). If the pipeline fails, it outputs a safely formatted error JSON instead.
5. **Structured Logging:** A customized logger writes timestamped updates to `run.log`. This creates a permanent audit trail of job starts, data loaded, operations performed, and system completions.
6. **Docker Containerization:** To ensure the code runs flawlessly on any machine without dependency issues, I packaged the entire environment in a lightweight Python Docker container (`python:3.9-slim`). 

## 1. Setup Instructions
To set up the environment locally, ensure you have Python 3.9+ installed, and then install the required dependencies:

```bash
pip install -r requirements.txt
