import pandas as pd
import yfinance as yf # type: ignore
import os
import glob

def get_sector_files(data_dir='../data/'):
    """Returns a list of all CSV files in the sector directory."""
    # Matches any .csv file in the folder
    files = glob.glob(os.path.join(data_dir, "*.csv"))
    if not files:
        print(f"Warning: No CSV files found in {data_dir}")
    return files

def extract_tickers_from_csv(file_path):
    """
    Smart CSV reader that finds the header row containing 'Ticker' or 'Symbol'.
    """
    try:
        # 1. Read first few lines to find where the data starts
        # SSGA files often skip the first few rows
        df = pd.read_csv(file_path, skiprows=lambda x: x > 20) # Read basic to peek? No, simpler way:
        
        # Robust method: Loop rows until we find 'Ticker'
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        header_row = 0
        for i, line in enumerate(lines):
            if 'Ticker' in line or 'Symbol' in line:
                header_row = i
                break
        
        # 2. Read the actual data
        df = pd.read_csv(file_path, header=header_row)
        
        # 3. Clean column names (strip whitespace)
        df.columns = [c.strip() for c in df.columns]
        
        # 4. Find the ticker column
        possible_cols = ['Ticker', 'Symbol', 'Holding']
        ticker_col = next((c for c in df.columns if c in possible_cols), None)
        
        if ticker_col:
            tickers = df[ticker_col].dropna().astype(str).tolist()
            # Clean weird tickers (remove non-alpha chars if needed)
            tickers = [t for t in tickers if t.isalpha()]
            return tickers
        else:
            print(f"Could not find Ticker column in {file_path}")
            return []
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def download_sector_price_data(tickers, start_date, end_date):
    """Downloads prices for a specific list of tickers."""
    if not tickers:
        return pd.DataFrame()
        
    print(f"  Downloading {len(tickers)} symbols...")
    # Using 'threads=True' for speed
    data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True, threads=True)['Close']
    
    # Drop columns with too much missing data (e.g., < 90% valid)
    threshold = len(data) * 0.9
    data = data.dropna(axis=1, thresh=threshold)
    
    # Forward fill remaining small gaps
    data = data.ffill()
    return data