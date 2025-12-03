import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Modules
from data_loader import download_sector_price_data
from analytics import get_trade_signal
from backtest import backtest_pair
from plots import plot_pair_analysis
from pdf_report import create_daily_report

def analyze_and_chart(stock_a, stock_b, price_data, ratio, z_score):
    """
    Runs backtest, saves chart, returns metrics.
    """
    # 1. Backtest
    results = backtest_pair(stock_a, stock_b, price_data, ratio, z_score)
    
    # 2. Metrics
    daily_vol = results['strategy_return'].std()
    sharpe = 0.0
    if daily_vol > 0:
        total_ret = results['cumulative_return'].iloc[-1] - 1
        sharpe = total_ret / (daily_vol * np.sqrt(252))
    
    # 3. Chart
    if not os.path.exists('../reports/images'):
        os.makedirs('../reports/images')
        
    fig = plot_pair_analysis(results, stock_a, stock_b, results['zscore'])
    
    chart_path = f"../reports/images/{stock_a}-{stock_b}.png"
    plt.savefig(chart_path, bbox_inches='tight')
    plt.close()
    
    return sharpe, chart_path

def run_pdf_screener(stocks):
    print(f"\n--- 🤖 PDF REPORT GENERATOR ({datetime.now().date()}) ---")

    if len(stocks) == 0: 
        print("stocks file not found.")
        return

    # Data Loading
    print("Downloading market data...")
    all_tickers = list(set(stocks['Stock A'].tolist() + stocks['Stock B'].tolist()))
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    data = download_sector_price_data(all_tickers, start_date=start_date, end_date=None)
    
    active_opportunities = []
    
    print("Scanning pairs...")
    for _, row in stocks.iterrows():
        a, b, sector = row['Stock A'], row['Stock B'], row['Sector']
        
        try:
            ratio, z = get_trade_signal(a, b, data)
            
            # Signal Logic
            signal_type = None
            if z > 2.0: signal_type = "SELL SPREAD"
            elif z < -2.0: signal_type = "BUY SPREAD"
            
            if signal_type:
                print(f"   -> Signal found: {a}-{b} ({signal_type})")
                
                # Analyze & Chart
                sharpe, chart_path = analyze_and_chart(a, b, data, ratio, z)
                
                # Add to report list
                active_opportunities.append({
                    'Stock A': a,
                    'Stock B': b,
                    'Sector': sector,
                    'Z-Score': z,
                    'Ratio': ratio,
                    'Signal_Type': signal_type,
                    'Sharpe': sharpe,
                    'Chart_Path': chart_path
                })
                
        except Exception:
            continue

    # Generate the PDF
    if active_opportunities:
        create_daily_report(active_opportunities)
    else:
        print("No active signals today. No PDF generated.")