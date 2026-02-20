import streamlit as st
import pandas as pd
import numpy as np
import time

# 1. Page Header
st.set_page_config(page_title="Trading Signal Bot", layout="wide")
st.title("📈 MLOps Trading Signal Generator")
st.markdown("An interactive dashboard demonstrating rolling technical indicators and deterministic signal generation.")

# 2. Sidebar Configuration (Replacing config.yaml)
st.sidebar.header("⚙️ Configuration")
seed = st.sidebar.number_input("Random Seed", value=42, step=1)
window = st.sidebar.slider("Rolling Window Size", min_value=1, max_value=50, value=5)
version = st.sidebar.selectbox("Version", ["v1", "v2-beta"])

# 3. File Uploader (Replacing --input argument)
uploaded_file = st.file_uploader("Upload your OHLCV Data (CSV file)", type="csv")

if uploaded_file is not None:
    start_time = time.time()
    
    # Set deterministic seed
    np.random.seed(seed)
    
    try:
        # Load Data
        df = pd.read_csv(uploaded_file)
        
        if 'close' not in df.columns:
            st.error("❌ Error: The dataset must contain a 'close' column.")
        else:
            st.success(f"✅ Successfully loaded {len(df)} rows.")
            
            # Core Math (Same as your run.py!)
            df['rolling_mean'] = df['close'].rolling(window=window, min_periods=1).mean()
            df['signal'] = np.where(df['close'] > df['rolling_mean'], 1, 0)
            
            # Metrics Calculation
            signal_rate = float(df['signal'].mean())
            latency_ms = int((time.time() - start_time) * 1000)
            
            st.markdown("---")
            
            # 4. Beautiful Metrics Display (Replacing metrics.json)
            st.subheader("📊 Execution Metrics")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Rows Processed", len(df))
            col2.metric("Signal Rate", f"{signal_rate:.4f}")
            col3.metric("Latency", f"{latency_ms} ms")
            col4.metric("Status", "Success")
            
            st.markdown("---")
            
            # 5. Visualizing the Results
            st.subheader(f"📈 Price vs. {window}-Period Rolling Mean")
            # We plot the last 200 rows so the chart isn't too crowded
            chart_data = df[['close', 'rolling_mean']].tail(200)
            st.line_chart(chart_data)
            
            st.subheader("Raw Generated Signals (Recent)")
            # Display the actual dataframe
            display_df = df[['timestamp', 'close', 'rolling_mean', 'signal']] if 'timestamp' in df.columns else df[['close', 'rolling_mean', 'signal']]
            st.dataframe(display_df.tail(15), use_container_width=True)
            
    except Exception as e:
        st.error(f"❌ An error occurred during processing: {e}")
else:
    st.info("👆 Please upload the `data.csv` file to begin processing.")