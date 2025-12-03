import matplotlib.pyplot as plt

def plot_pair_analysis(results_df, stock_a, stock_b, z_score):
    """
    Generates a 3-panel dashboard for the pair.
    1. Z-Score History (Signals)
    2. Spread History
    3. PnL Curve
    """
    fig, axes = plt.subplots(3, 1, figsize=(12, 12), sharex=True)
    
    # Panel 1: Z-Score & Signals
    axes[0].plot(results_df.index, z_score, label='Z-Score', color='blue', alpha=0.6)
    axes[0].axhline(0, color='black', linestyle='-')
    axes[0].axhline(2.0, color='red', linestyle='--')
    axes[0].axhline(-2.0, color='green', linestyle='--')
    axes[0].set_title(f"Z-Score Analysis: {stock_a} - {stock_b}")
    axes[0].legend()
    
    # Panel 2: The Positions Taken
    axes[1].plot(results_df.index, results_df['pos_b'], label='Position (1=Long Spread, -1=Short)', color='purple')
    axes[1].set_title("Trading Signals")
    axes[1].set_ylabel("Position Direction")
    
    # Panel 3: Equity Curve
    axes[2].plot(results_df.index, results_df['cumulative_return'], label='Strategy Return', color='darkgreen', linewidth=2)
    axes[2].set_title(f"Cumulative Performance (Growth of $1)")
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig