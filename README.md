# Stock Analyzer

Stock Analyzer is a Python-based tool that evaluates and rates stocks based on key financial metrics. It helps users make informed investment decisions by analyzing a stock's performance and comparing it against ideal metrics.

## Features

Stock Analyzer evaluates stocks based on the following financial metrics:

- P/E Ratio
- Forward P/E Ratio
- Dividend Yield
- Beta
- Revenue Growth
- Earnings Growth
- Return on Equity
- Debt-to-Equity Ratio
- Gross Margin
- Operating Margin
- Net Profit Margin

Each metric is rated as Excellent, Great, Good, Fair, or Poor based on how closely it aligns with the ideal value. The Investment Score Potential is also calculated as an average of the scores for each metric, providing an overall assessment of the stock.

## Usage

To use Stock Analyzer, simply input the stock ticker symbol of the company you want to analyze. The script will fetch the stock data using the yfinance library and display the results, including the rating for each financial metric and the Investment Score Potential.

## Limitations

Stock Analyzer is designed to provide a quick and easy way to assess stocks based on key financial metrics. However, it should be noted that a variety of other factors can impact a stock's performance, such as market conditions, news, and the overall economic climate. Therefore, it's important to use this tool as a starting point for your analysis and not as the sole basis for your investment decisions.
