# Pairs Trading Analysis Engine

## Executive Summary

This project implements a comprehensive **Statistical Arbitrage (Pairs Trading)** framework designed to identify and exploit mean-reverting relationships in equity markets. By leveraging **Cointegration** rather than simple correlation, the system detects fundamentally linked asset pairs that have temporarily diverged from their historical equilibrium.

The engine features a robust **Sector-Based Research Module** to filter for high-quality, economically intuitive pairs, a **Vectorized Backtesting Core** for rigorous historical validation, and an **Automated Reporting Pipeline** that generates detailed PDF briefings with Z-Score and PnL visualizations.

## Project Architecture

The repository is structured to separate the research, data engineering, and operational reporting layers, ensuring a modular and scalable codebase.

```text
Pairs-Trading-Strategy/
│
├── data/           # Source: SSGA Sector ETF holdings (CSVs)
│   └── best_pairs.csv # Output: Calibrated pairs for trading
│
├── src/
│   ├── data_loader.py      # Ingests YFinance data & Local Sector CSVs
│   ├── analytics.py        # Cointegration tests (Engle-Granger) & Z-Score math
│   ├── backtest.py         # Vectorized mean-reversion simulation engine
│   ├── plots.py            # To Generate charts effectively
│   ├── pdf_report.py       # PDF report generation engine
│   └── screener.py         # Daily operational script
│
├── notebooks/
│   └── strategy.ipynb  # Research environment for model calibration
│
├── reports/                # Generated PDF briefings & charts
├── requirements.txt
└── README.md
```

## Strategy Methodology

1.  **Stocks Data (Sector-Neutral):**

    - The system ingests 11 distinct Sector ETF CSVs (obtained from SSGA for each of their Sector ETFs (XL\_)) to ensure pairs are economically linked.
    - This "Intra-Sector" constraint significantly reduces spurious correlations compared to a global search.

2.  **Statistical Identification:**

    - **Cointegration:** Pairs are validated using the **Engle-Granger Two-Step Method**. Only pairs with a p-value \< 0.05 are retained.
    - **Hedge Ratio:** Calculated dynamically using OLS Regression ($\beta$) to ensure market neutrality.

3.  **Signal Generation:**

    - The spread is modeled as: $Spread = Price_B - (\beta \times Price_A)$
    - **Z-Score:** The spread is normalized to a standard normal distribution.
    - **Entry:** $|Z| > 2.0$ (Statistically extended).
    - **Exit:** $Z = 0.0$ (Mean reversion).

## Getting Started

### Prerequisites

- Python 3.8+
- Virtual Environment (Recommended)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/JayGupta2003/pairs-trading-strategy.git
    cd pairs-trading-strategy
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Data Setup:**

    - Place your sector constituent CSVs into the `data` directory.

### Workflow

1.  **Research & Calibration (Monthly):**

    - Run `notebooks/strategy.ipynb`.
    - This scans all sectors, runs cointegration tests on years of data (I recommend setting those values yourself), and saves the best pairs to `data/best_pairs.csv`.

2.  **Daily Operations:**

    - Run the screener to check for live signals through the notebook or using terminal:

    <!-- end list -->

    ```bash
    python src/screener.py
    ```

    - If active signals are found, a PDF report will be generated in `reports/`.

## Sample Output (PDF Report)

The automated `Daily_Brief.pdf` includes:

- **Executive Summary:** Table of all active BUY/SELL signals.
- **Deep Dive Analysis:** For every signaled pair, a dedicated page showing:
  - **Z-Score History:** Visualizing the entry signal.
  - **Historical Backtest:** 1-Year equity curve to validate the pair's behavior.
  - **Risk Metrics:** Historical Sharpe Ratio and Drawdown.

## Risk Disclaimers

- **Stationarity Breakdown:** Cointegration relationships can break down during structural market shifts (e.g., M\&A, regulatory changes).
- **Execution Risk:** This simulation assumes ideal execution at closing prices. Real-world slippage and bid-ask spreads are not modeled.
- **Look-Ahead Bias:** While the trading logic avoids look-ahead bias, the stocks selection (based on current ETF holdings) contains inherent survivorship bias.

## Tech Stack

- **Statsmodels:** Cointegration (ADF/Engle-Granger) & Regression.
- **Pandas/NumPy:** Vectorized timeseries analysis.
- **Matplotlib/Seaborn:** Financial visualization.
- **FPDF2:** Automated reporting engine.
- **YFinance:** Market data API.

## License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).
