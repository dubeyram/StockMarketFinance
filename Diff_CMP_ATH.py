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
    except Exception as e:
        # Handle errors if NSE code is invalid or data cannot be downloaded
        return {
            "nse_code": nse_code,
            "error": "Invalid NSE code or data unavailable",
        }


# Example usage
if __name__ == "__main__":
    # Take input as a string containing stock names separated by commas
    nse_codes = input("Enter the list of stocks nse code separated by commas: (e.g: TCS, TITAN) ")

    # Split the input string into individual stock names
    stocks_list = nse_codes.split(',')

    # Remove leading and trailing whitespaces from each stock name
    stocks_list = [stock.strip() for stock in stocks_list]

    print("Stocks list:", stocks_list)
    for nse_code in stocks_list:
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

