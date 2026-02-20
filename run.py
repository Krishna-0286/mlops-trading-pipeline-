import argparse
import yaml
import pandas as pd
import numpy as np
import sys
import logging
import time
import json
import traceback

def setup_logger(log_file):
    # Configures the logging to include timestamps and info levels [cite: 23, 27]
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def write_json(output_path, payload):
    # Helper function to write the metrics out to a JSON file [cite: 21]
    with open(output_path, 'w') as f:
        json.dump(payload, f, indent=4)

def main():
    start_time = time.time() # Measure total program execution time [cite: 19]
    
    # Adhere to the required command-line argument structure [cite: 3]
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)
    args = parser.parse_args()

    setup_logger(args.log_file)
    logging.info("Job started")

    try:
        # 1. Configuration Loading [cite: 8]
        with open(args.config, 'r') as file:
            config = yaml.safe_load(file)
        
        seed = config['seed']
        window = config['window']
        version = config['version']
        
        logging.info(f"Config loaded: seed={seed}, window={window}, version={version}")
        
        # Set the random seed using numpy [cite: 9]
        np.random.seed(seed)

        # 2. Input Data Ingestion [cite: 10]
        try:
            df = pd.read_csv(args.input)
        except Exception:
            raise ValueError("Missing input file or Invalid CSV file format.") # Gracefully manage missing/invalid files [cite: 20]
            
        if df.empty:
            raise ValueError("Empty input file.") # Gracefully manage empty files [cite: 20]
            
        # Ensure the presence of the required close column [cite: 11]
        if 'close' not in df.columns:
            raise ValueError("Missing required columns in the dataset.") 
            
        rows_processed = len(df)
        logging.info(f"Data loaded: {rows_processed} rows")

        # 3. Rolling Mean Computation [cite: 12]
        # Handle the initial rows where insufficient data exists using min_periods=1 [cite: 13]
        df['rolling_mean'] = df['close'].rolling(window=window, min_periods=1).mean()
        logging.info(f"Rolling mean calculated with window={window}")

        # 4. Signal Generation [cite: 14]
        # Value of 1 if close > rolling_mean, else 0 [cite: 15, 16]
        df['signal'] = np.where(df['close'] > df['rolling_mean'], 1, 0)
        logging.info("Signals generated")

        # 5. Metrics Calculation [cite: 17]
        signal_rate = float(df['signal'].mean()) # Proportion of 1s [cite: 18]
        latency_ms = int((time.time() - start_time) * 1000)
        
        logging.info(f"Metrics: signal_rate={signal_rate:.4f} rows_processed={rows_processed}")
        logging.info(f"Job completed successfully in {latency_ms}ms")

        # Expected Metrics Output (JSON) [cite: 21]
        metrics = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }
        
        # Print final metrics to standard output (stdout) [cite: 34]
        print(json.dumps(metrics, indent=4))
        write_json(args.output, metrics)
        sys.exit(0) # Exit with a return code of 0 upon successful completion [cite: 35]

    except Exception as e:
        error_msg = str(e)
        logging.error(f"Job failed: {error_msg}")
        
        # Error Output Format [cite: 22]
        error_metrics = {
            "version": config.get('version', 'unknown') if 'config' in locals() else 'unknown',
            "status": "error",
            "error_message": error_msg
        }
        
        print(json.dumps(error_metrics, indent=4))
        write_json(args.output, error_metrics)
        sys.exit(1) # Exit with a non-zero code on failure  

if __name__ == "__main__":
    main()