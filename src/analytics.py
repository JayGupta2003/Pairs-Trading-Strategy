import numpy as np
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm

def find_cointegrated_pairs(data, significance_level=0.05):
    """
    Loops through stocks and finds pairs with a p-value < 0.05 on the Engle-Granger Cointegration Test.
    """
    n = data.shape[1]
    keys = data.keys()
    pvalue_matrix = np.ones((n, n))
    pairs = []

    print("Running Cointegration Tests...")

    for i in range(n):
        for j in range(i + 1, n):
            stock1 = data[keys[i]]
            stock2 = data[keys[j]]

            coint_test = coint(stock1, stock2)
            pvalue = coint_test[1]
            pvalue_matrix[i, j] = pvalue

            if pvalue < significance_level:
                pairs.append((keys[i], keys[j], pvalue))

    return pvalue_matrix, pairs

def calculate_zscore(series):
    """
    Computes the z-score of a pandas Series.
    Z = (Value - Mean) / StdDev
    """
    res = (series - series.mean()) / series.std()
    return res

def get_trade_signal(stock_a, stock_b, data, window=60):
    """
    Calculates the latest Hedge Ratio and Z-Score for a pair.
    Uses a rolling window (default 60 days) to adapt to recent market changes.
    """

    s1 = data[stock_a].iloc[-window:]
    s2 = data[stock_b].iloc[-window:]
    
    s1_const = sm.add_constant(s1)
    model = sm.OLS(s2, s1_const).fit()
    hedge_ratio = model.params[stock_a]
    
    spread = s2 - (hedge_ratio * s1)
    
    z_score = (spread.iloc[-1] - spread.mean()) / spread.std()
    
    return hedge_ratio, z_score