import tkinter as tk
from tkinter import messagebox
import yfinance as yf


def get_stock_info(nse_codes):
    results = []
    for nse_code in nse_codes:
        try:
            stock_data = yf.download(f"{nse_code}.NS", period="max", multi_level_index=False)
            if stock_data.empty:
                return {
                    "nse_code": nse_code,
                    "error": "No data available for the specified NSE code."
                }
            current_price = stock_data["Close"].iloc[-1] 
            all_time_high = stock_data["High"].max()
            percentage_difference = (
                (current_price - all_time_high) / all_time_high
            ) * 100
            results.append(
                f"NSE Code: {nse_code}\nCurrent Price (CMP): Rs.{current_price:.2f}\nAll-Time High (ATH): Rs.{all_time_high:.2f}\nDifference between CMP and ATH: {percentage_difference:.2f}%\n\n"
            )
        except Exception as e:
            results.append(f"Error fetching data for {nse_code}: {e}\n\n")
    return "\n".join(results)


def on_submit():
    nse_codes = entry.get().split(",")
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
    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.geometry("400x300")  # Set custom size
    label = tk.Label(dialog, text=message)
    label.pack()
    # Remove the line below to prevent the dialog from becoming modal
    # dialog.grab_set()  # Make it modal
    window.wait_window(dialog)


# Create the main window
window = tk.Tk()
window.title("Stock Market Analysis")
window.geometry("300x150")

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
