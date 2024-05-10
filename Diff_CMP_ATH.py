# Required library: yfinance
# Description:
#   - yfinance is a popular open-source Python library for downloading financial data from Yahoo Finance.
#   - It provides a convenient way to access historical and current market data for stocks, currencies, and other financial instruments.
#   - You can install yfinance using the following command in your terminal:
#       pip install yfinance

import yfinance as yf

def get_stock_info(nse_code):
    """
    This function takes an NSE code as input and returns a dictionary containing:
        - current market price (CMP)
        - all-time high (ATH)
        - percentage difference between CMP and ATH
    """
    try:
        # Download stock information using yfinance
        stock_data = yf.download(f"{nse_code}.NS", period="max")

        # Get current market price (CMP)
        current_price = stock_data["Close"][-1]

        # Get all-time high (ATH) price
        all_time_high = stock_data["High"].max()

        # Calculate percentage difference
        if all_time_high > 0:
            percentage_difference = (
                (current_price - all_time_high) / all_time_high
            ) * 100
        else:
            percentage_difference = 0

        # Return dictionary containing all the information
        return {
            "nse_code": nse_code,
            "current_price": current_price,
            "all_time_high": all_time_high,
            "percentage_difference": percentage_difference,
        }
    except (yf.DownloadError, KeyError):
        # Handle errors if NSE code is invalid or data cannot be downloaded
        return {
            "nse_code": nse_code,
            "error": "Invalid NSE code or data unavailable",
        }


# Example usage
if __name__ == "__main__":
    nse_code = input("Enter NSE code: ")
    stock_info = get_stock_info(nse_code)

    if "error" in stock_info:
        print(f"Error: {stock_info['error']}")
    else:
        print(f"NSE Code: {stock_info['nse_code']}")
        print(f"Current Price (CMP): ₹{stock_info['current_price']:.2f}")
        print(f"All-Time High (ATH): ₹{stock_info['all_time_high']:.2f}")
        print(
            f"Difference between CMP and ATH: {stock_info['percentage_difference']:.2f}%"
        )


"""
This script utilizes the `yfinance` library to retrieve historical data for a given NSE code, 
calculates the current market price (CMP), all-time high (ATH), and the percentage difference between CMP and ATH.

Here's how it works:

1. It defines a function `get_stock_info(nse_code)` which takes an NSE code as input.
2. Inside the function, it tries to download the stock information using `yfinance`.
3. It extracts the current market price (`current_price`) and all-time high (`all_time_high`) from the downloaded data.
4. It calculates the percentage difference between CMP and ATH, taking care to handle cases where the all-time high is zero.
5. It returns a dictionary containing all the information.
6. In case of errors (such as an invalid NSE code or inability to download data), it handles the exceptions and returns a dictionary with an error message.

You can easily use this script by providing an NSE code when prompted. It will then fetch the required data and 
display the CMP, ATH, and the percentage difference between them.
"""

# Explanation about yf.download period parameter
"""
The `period` parameter in `yf.download()` function specifies the time period for which historical data will be downloaded.
When you set `period="max"`, it means you want to download historical data for the maximum available time period.

Here's how it works:

- `period="max"`: This downloads historical data from the earliest available date up to the current date.
- `period="1d"`: This downloads intraday data for the most recent trading day.
- `period="1mo"`, `period="1y"`, `period="5y"`, etc.: These download historical data for the past month, year, 5 years, etc.

So, when you specify `period="max"`, `yfinance` will attempt to download historical data for the entire available history of the stock,
starting from its IPO date or the earliest available date in its dataset up to the current date.
"""