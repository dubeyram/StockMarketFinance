"""
This program calculates the 20-day, 50-day, and 100-day EMAs for a stock.
"""
import diff_cmp_ath
import diff_cmp_ath_gui


def get_ema(symbol, period):
    """
    This function downloads historical closing prices for a stock and calculates its EMA for a given period.
    """
    try:
        # Download historical closing prices
        stock_data = diff_cmp_ath_gui.get_nse_data(symbol)["Close"]

        # Calculate the EMA using pandas
        ema = stock_data.ewm(span=period, min_periods=period).mean()

        return ema.iloc[-1]  # Return the latest EMA value

    except Exception as e:  # Catch any exception during download
        print(f"Error downloading data for {symbol}: {e}")
        return None  # Return None on errors


def get_stock_emas(symbol):
    """
    This function calculates the 20-day, 50-day, and 100-day EMAs for a stock.
    """
    ema_20 = get_ema(symbol, 20)
    ema_50 = get_ema(symbol, 50)
    ema_100 = get_ema(symbol, 100)

    if ema_20 is None or ema_50 is None or ema_100 is None:
        print(f"Error downloading data for {symbol}.")
        return None

    current_market_price = diff_cmp_ath.get_stock_info(nse_code=symbol)
    c_m_p = None
    if current_market_price:
        c_m_p = current_market_price.get("current_price")
    # Return a dictionary with the calculated EMAs
    return {
        "symbol": symbol,
        "c_m_p": c_m_p,
        "20ema": ema_20,
        "50ema": ema_50,
        "100ema": ema_100,
    }


# Example usage
while True:
    """
    This is the main loop that allows the user to enter an NSE code and get the stock information.
    """
    nse_code = input("Enter NSE code: ")
    stock_emas = get_stock_emas(nse_code)

    if stock_emas:
        print(f"Stock: {stock_emas['symbol']}")
        print(f"Current Market Price: {stock_emas['c_m_p']:.2f}")
        print(f"20-day EMA: {stock_emas['20ema']:.2f}")
        print(f"50-day EMA: {stock_emas['50ema']:.2f}")
        print(f"100-day EMA: {stock_emas['100ema']:.2f}")

    else:
        print("Error retrieving EMA data.")
