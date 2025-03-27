"""
This is a GUI application that allows users to enter NSE codes and get the stock information.
"""
import tkinter as tk
from tkinter import messagebox
import yfinance as yf
from functools import lru_cache


@lru_cache(maxsize=5)
def get_nse_data(nse_code):
    """
    This function is used to get the NSE data for the given NSE code.
    """
    return yf.download(f"{nse_code}.NS", period="max", multi_level_index=False)


def get_stock_info(nse_codes):
    """
    This function is used to get the stock information for the given NSE codes.
    """
    results = []
    for nse_code in nse_codes:
        try:
            stock_data = get_nse_data(nse_code)
            if stock_data.empty:
                return {
                    "nse_code": nse_code,
                    "error": "No data available for the specified NSE code.",
                }
            current_price = stock_data["Close"].iloc[-1]
            all_time_high = stock_data["High"].max()
            percentage_difference = (
                (current_price - all_time_high) / all_time_high
            ) * 100
            results.append(
                f"NSE Code: {nse_code}\n"
                f"Current Price (CMP): Rs.{current_price:.2f}\n"
                f"All-Time High (ATH): Rs.{all_time_high:.2f}\n"
                f"Difference between CMP and ATH: {percentage_difference:.2f}%\n\n"
            )
        except Exception as e:
            results.append(f"Error fetching data for {nse_code}: {e}\n\n")
    return "\n".join(results)


def on_submit():
    """
    This function is used to submit the NSE codes and get the stock information.
    """
    nse_codes = list(
        dict.fromkeys([code.strip() for code in entry.get().split(",")])
    )

    if nse_codes:
        stock_info = get_stock_info(nse_codes)
        if "error" in stock_info:
            info = stock_info["error"]
            show_custom_dialog("Stock Information", info)
            return False
        show_custom_dialog("Stock Information", stock_info)
    else:
        messagebox.showerror("Error", "Please enter at least one NSE code.")


def show_custom_dialog(title, message):
    """
    This function is used to show a custom dialog box with a title and message.
    """
    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.geometry("400x300")  # Set custom size
    label = tk.Label(dialog, text=message)
    label.pack()
    window.wait_window(dialog)


if __name__ == "__main__":
    # Create the main window
    window = tk.Tk()
    window.title("Stock Market Analysis")
    window.geometry("500x250")

    # Create label and entry widget for user input
    label = tk.Label(window, text="Enter NSE Codes separated by comma (,):")
    label.pack()
    entry = tk.Entry(window)
    entry.pack()

    # Create submit button
    button = tk.Button(window, text="Submit", command=on_submit)
    button.pack()

    # Run the main event loop
    window.mainloop()

 
