# MLOps Trading Signal Generator

A miniature MLOps pipeline demonstrating reproducibility, deployment, logging, and metrics output.

## 1. Setup Instructions
To set up the environment locally, install the required dependencies:
```bash
## Project Workflow: What This Pipeline Does

To build this robust, production-ready MLOps pipeline, I implemented the following sequential steps:

1.  **Configuration & Determinism:** The pipeline reads inputs through a Command-Line Interface (CLI)[cite: 7, 8]. [cite_start]It dynamically loads parameters (such as the random seed and rolling window size) from an external `config.yaml` file[cite: 26, 27]. [cite_start]Setting the numpy random seed ensures the entire execution is deterministic and 100% reproducible[cite: 28].
2.  **Data Ingestion & Validation:** The script loads the cryptocurrency dataset (`data.csv`) into a Pandas DataFrame[cite: 29, 30]. [cite_start]It includes robust error handling to strictly validate the presence of the required `close` price column and safely catch edge cases like missing or empty input files[cite: 31, 46, 47, 49].
3.  **Algorithmic Signal Generation:** The core logic calculates a rolling mean on the closing price based on the window size defined in the configuration[cite: 33, 34]. [cite_start]It then generates a binary trading signal: assigning a `1` if the current close price is strictly greater than the rolling mean, and a `0` otherwise[cite: 37, 38, 39].
4.  **Metrics Calculation & JSON Export:** The system calculates the total execution time (`latency_ms`) and the `signal_rate` (the mean of all generated signals)[cite: 42, 44]. [cite_start]It then writes these results to a machine-readable JSON file (`metrics.json`)[cite: 52, 53]. [cite_start]If the pipeline fails, it outputs a safely formatted error JSON instead[cite: 80, 84].
5.  **Structured Logging:** Throughout the execution, a logger writes timestamped updates to `run.log`[cite: 86, 87]. [cite_start]This creates a permanent audit trail of job starts, data loaded, math operations performed, and system completions[cite: 88, 90, 91, 93].
6.  **Docker Containerization:** To eliminate the "it works on my machine" problem, the entire environment is packaged in a lightweight Python Docker container (`python:3.9-slim`)[cite: 104, 107]. [cite_start]This guarantees the pipeline executes flawlessly on any host machine[cite: 104].
