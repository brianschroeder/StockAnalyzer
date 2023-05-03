import yfinance as yf

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    stock_info = stock.info
    return stock_info

def rate_metric(actual, ideal, higher_is_better=True):
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
    pe_ratio_score = 100 - min(100, stock_data["trailingPE"] / 2)
    forward_pe_ratio_score = 100 - min(100, stock_data["forwardPE"] / 2)
    dividend_yield_score = min(100, stock_data["dividendYield"] * 2000)
    beta_score = 100 - min(100, abs(stock_data["beta"]) * 100)
    revenue_growth_score = max(0, min(100, stock_data["revenueGrowth"] * 200))
    earnings_growth_score = max(0, min(100, stock_data["earningsGrowth"] * 200))
    roe_score = max(0, min(100, stock_data["returnOnEquity"] * 100))
    debt_to_equity_score = max(0, min(100, (1 - stock_data["debtToEquity"]) * 100))
    gross_margin_score = min(100, stock_data["grossMargins"] * 100)
    operating_margin_score = min(100, stock_data["operatingMargins"] * 100)
    net_profit_margin_score = min(100, stock_data["profitMargins"] * 100)

    total_score = (pe_ratio_score + forward_pe_ratio_score + dividend_yield_score + 
                   beta_score + revenue_growth_score + earnings_growth_score + roe_score +
                   debt_to_equity_score + gross_margin_score + operating_margin_score + net_profit_margin_score) / 11

    return total_score

def display_stock_info(stock_data):
    print("Stock Information for", stock_data["shortName"])
    print("Current Stock Price:", stock_data["currentPrice"])
    print("52-Week High:", stock_data["fiftyTwoWeekHigh"])
    print("52-Week Low:", stock_data["fiftyTwoWeekLow"])
    print("P/E Ratio:", round(stock_data["trailingPE"], 4), "(Ideal: < 20)", "| Rating:", rate_metric(stock_data["trailingPE"], 20, False))
    print("Forward P/E Ratio:", round(stock_data["forwardPE"], 4), "(Ideal: < 20)", "| Rating:", rate_metric(stock_data["forwardPE"], 20, False))
    print("Dividend Yield:", round(stock_data["dividendYield"], 4), "(Ideal: > 2%)", "| Rating:", rate_metric(stock_data["dividendYield"], 0.02))
    print("Beta:", round(stock_data["beta"], 4), "(Ideal: < 1)", "| Rating:", rate_metric(stock_data["beta"], 1, False))
    print("Revenue Growth:", round(stock_data["revenueGrowth"], 4), "(Ideal: > 5%)", "| Rating:", rate_metric(stock_data["revenueGrowth"], 0.05))
    print("Earnings Growth:", round(stock_data["earningsGrowth"], 4), "(Ideal: > 5%)", "| Rating:", rate_metric(stock_data["earningsGrowth"], 0.05))
    print("Return on Equity:", round(stock_data["returnOnEquity"], 4), "(Ideal: > 15%)", "| Rating:", rate_metric(stock_data["returnOnEquity"], 0.15))
    print("Debt-to-Equity Ratio:", round(stock_data["debtToEquity"], 4), "(Ideal: < 1)", "| Rating:", rate_metric(stock_data["debtToEquity"], 1, False))
    print("Gross Margin:", round(stock_data["grossMargins"], 4), "(Ideal: > 40%)", "| Rating:", rate_metric(stock_data["grossMargins"], 0.4))
    print("Operating Margin:", round(stock_data["operatingMargins"], 4), "(Ideal: > 20%)", "| Rating:", rate_metric(stock_data["operatingMargins"], 0.2))
    print("Net Profit Margin:", round(stock_data["profitMargins"], 4), "(Ideal: > 10%)", "| Rating:", rate_metric(stock_data["profitMargins"], 0.1))
    investment_score = calculate_investment_score(stock_data)
    print("Investment Score Potential:", round(investment_score, 4))

ticker = "AAPL"
stock_data = fetch_stock_data(ticker)
display_stock_info(stock_data)
