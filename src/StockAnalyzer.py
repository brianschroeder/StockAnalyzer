import yfinance as yf
import pandas as pd
import requests
from datapackage import Package

metrics = [
    ("trailingPE", 20, False, "P/E Ratio"),
    ("forwardPE", 20, False, "Forward P/E Ratio"),
    ("dividendYield", 0.02, True, "Dividend Yield"),
    ("beta", 1, False, "Beta"),
    ("revenueGrowth", 0.05, True, "Revenue Growth"),
    ("earningsGrowth", 0.05, True, "Earnings Growth"),
    ("returnOnEquity", 0.15, True, "Return on Equity"),
    ("debtToEquity", 1, False, "Debt-to-Equity Ratio"),
    ("grossMargins", 0.4, True, "Gross Margin"),
    ("operatingMargins", 0.2, True, "Operating Margin"),
    ("profitMargins", 0.1, True, "Net Profit Margin")
]

def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info
        return stock_info
    except requests.exceptions.HTTPError:
        print(f"Error fetching data for {ticker}")
        return {}

def rate_metric(actual, ideal, higher_is_better=True):
    if actual is None or actual == "N/A":
        return "N/A"

    try:
        actual = float(actual)
    except ValueError:
        return "N/A"

    if higher_is_better:
        if actual >= ideal:
            return "Excellent"
        elif actual >= ideal * 0.8:
            return "Great"
        elif actual >= ideal * 0.6:
            return "Good"
        elif actual >= ideal * 0.4:
            return "Fair"
        else:
            return "Poor"
    else:
        if actual <= ideal:
            return "Excellent"
        elif actual <= ideal * 1.25:
            return "Great"
        elif actual <= ideal * 1.5:
            return "Good"
        elif actual <= ideal * 2:
            return "Fair"
        else:
            return "Poor"

def calculate_investment_score(stock_data):
    total_score = 0
    num_metrics = 0

    for metric, ideal, higher_is_better, display_name in metrics:
        value = stock_data.get(metric)
        if value is not None and value != "N/A":
            try:
                value = float(value)
                total_score += value
                num_metrics += 1
            except ValueError:
                pass

    if num_metrics == 0:
        return 0

    return total_score / num_metrics

def create_stock_info_dataframe(stock_data):
    data = {
        "Stock": [stock_data.get("shortName", "N/A")],
        "Current Stock Price": [stock_data.get("currentPrice", "N/A")],
        "52-Week High": [stock_data.get("fiftyTwoWeekHigh", "N/A")],
        "52-Week Low": [stock_data.get("fiftyTwoWeekLow", "N/A")],
    }
    
    for metric, ideal, higher_is_better, display_name in metrics:
        value = stock_data.get(metric, None)
        if value is not None:
            data[f"{display_name}"] = [value]
            data[f"{display_name} Rating"] = [rate_metric(value, ideal, higher_is_better)]
        else:
            data[f"{display_name}"] = [None]
            data[f"{display_name} Rating"] = ["N/A"]
    
    investment_score = calculate_investment_score(stock_data)
    data["Investment Score Potential"] = [investment_score]
    
    return pd.DataFrame(data)

df_list = []
package = Package('https://datahub.io/core/s-and-p-500-companies/datapackage.json')

# print processed tabular data (if exists any)
for resource in package.resources:
    if resource.descriptor['datahub']['type'] == 'derived/csv':
        companies = resource.read()
        for company in companies:
            stock_data = fetch_stock_data(company[0])
            df = create_stock_info_dataframe(stock_data)
            df_list.append(df)

result = pd.concat(df_list)
result.to_excel("stock_information.xlsx", index=False)
