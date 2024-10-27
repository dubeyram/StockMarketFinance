import yfinance as yf
import pandas as pd

def get_stock_info(nse_code):
    """
    This function takes an NSE code as input and returns a dictionary containing:
        - current market price (CMP)
        - all-time high (ATH)
        - percentage difference between CMP and ATH
    """
    try:
        # Download stock information using yfinance with multi_level_index set to False
        stock_data = yf.download(f"{nse_code}.NS", period="max", multi_level_index=False)

        # Check if the DataFrame is empty
        if stock_data.empty:
            return {
                "nse_code": nse_code,
                "error": "No data available for the specified NSE code."
            }

        # Get current market price (CMP)
        current_price = stock_data["Close"].iloc[-1] 

        # Get all-time high (ATH) price
        all_time_high = stock_data["High"].max()

        # Calculate percentage difference
        if all_time_high > 0:
            percentage_difference = (
                (current_price - all_time_high) / all_time_high * 100
            )
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
            "error": f"Invalid NSE code or data unavailable: {str(e)}",
        }

# Example usage
if __name__ == "__main__":
    nse_codes = input("Enter the list of stocks nse code separated by commas: (e.g: TCS, TITAN) ")
    stocks_list = [stock.strip() for stock in nse_codes.split(',')]

    for nse_code in stocks_list:
        stock_info = get_stock_info(nse_code)

        if "error" in stock_info:
            print(f"Error: {stock_info['error']}")
        else:
            print(f"NSE Code: {stock_info['nse_code']}")
            print(f"Current Price (CMP): ₹{stock_info['current_price']:.2f}")
            print(f"All-Time High (ATH): ₹{stock_info['all_time_high']:.2f}")
            print(f"Difference between CMP and ATH: {stock_info['percentage_difference']:.2f}%\n")
