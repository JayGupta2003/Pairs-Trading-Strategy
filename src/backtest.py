import pandas as pd

def backtest_pair(stock_a, stock_b, price_data, hedge_ratio, z_score, entry_threshold=2.0, exit_threshold=0.0):
    """
    Simulates trading a mean-reversion strategy on a pair of stocks.
    """
    df = pd.DataFrame()
    df[stock_a] = price_data[stock_a]
    df[stock_b] = price_data[stock_b]
    df['zscore'] = z_score
    
    df['position_a'] = 0.0
    df['position_b'] = 0.0
    
    # Vectorized logic is hard for state-dependent exits (exit at 0), 
    # so we use a fast loop for signal logic.
    current_pos = 0 # 0, 1, or -1
    
    pos_a = []
    pos_b = []
    
    for z in df['zscore']:
        if z > entry_threshold:
            current_pos = -1 # Sell Spread (Sell B, Buy A)
            
        elif z < -entry_threshold:
            current_pos = 1 # Long Spread (Buy B, Sell A)
            
        elif abs(z) < 0.1: # Near Mean
            current_pos = 0 # Exit
            
        # Position sizing: 
        # If +1 (Long Spread): Buy 1.0 of B, Short Ratio of A
        # If -1 (Short Spread): Sell 1.0 of B, Buy Ratio of A
        pos_b.append(current_pos * 1.0)
        pos_a.append(current_pos * -hedge_ratio)
        
    df['pos_a'] = pos_a
    df['pos_b'] = pos_b
    
    # 3. Calculate Returns
    # Shift(1) because we own the position based on Yesterday's signal
    daily_ret_a = df[stock_a].pct_change()
    daily_ret_b = df[stock_b].pct_change()
    
    # Portfolio Return = (Pos_A * Ret_A) + (Pos_B * Ret_B)
    # We divide by 2 assuming 50% capital allocated to each leg roughly
    df['strategy_return'] = (df['pos_a'].shift(1) * daily_ret_a) + (df['pos_b'].shift(1) * daily_ret_b)
    
    # 4. Cumulative Returns
    df['cumulative_return'] = (1 + df['strategy_return'].fillna(0)).cumprod()
    
    return df