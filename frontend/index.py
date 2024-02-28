import tkinter as tk
from tkinter import ttk
from dotenv import dotenv_values
import sv_ttk

from frontend.item_tab import ItemTab
from frontend.stock_tab import StockTab
from frontend.bill_tab import BillTab
from frontend.bill_history_tab import BillHistory
from frontend.edit_tab import EditTab
from frontend.service_bill_tab import ServiceBilTab
from frontend.service_bill_history_tab import ServiceBillHistory

root = tk.Tk()
root.title("Pharma App")
root.state("zoomed")
env = dotenv_values(".env")

frame = ttk.Frame(root)
frame.pack(expand=True, fill="both")
frame.columnconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)


header_frame = ttk.Frame(frame)
header_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
header_frame.columnconfigure((0, 1), weight=1)

pharma_name_label = ttk.Label(header_frame, font=("Arial", 25, "bold"), text=env.get("PHARMACY_NAME", "PHARMACY NAME"))
pharma_name_label.grid(row=0, column=0, columnspan=2)

pharma_address_label = ttk.Label(header_frame, font=("Arial", 8), text=env.get("PHARMACY_ADDRESS", "Pharmacy Address"))
pharma_address_label.grid(row=1, column=0, columnspan=2)

pharma_pan_label = ttk.Label(header_frame, text=f'PAN No.: {env.get("PAN_NO", "xxxxxxxxx")}')
pharma_pan_label.grid(row=2, column=0, sticky="w")

pharma_dda_label = ttk.Label(header_frame, text=f'DDA No.: {env.get("DDA_NO", "xxxxxxxxxxxxxxxx")}')
pharma_dda_label.grid(row=2, column=1, sticky="e")

header_separator = ttk.Frame(header_frame, borderwidth=10, relief='sunken')
header_separator.grid(row=3, column=0, columnspan=2, sticky="ew")


body_frame = ttk.Notebook(frame)
body_frame.grid(row=1, column=0, padx=20, pady=10)

tabs: tuple[tuple[ItemTab, str], tuple[StockTab, str], tuple[StockTab, str]] = [
    (ItemTab(body_frame), "Item"),
    (StockTab(body_frame), "Stock"),
    (BillTab(body_frame), "Create Bill"),
    (BillHistory(body_frame), "Bill History"),
    (EditTab(body_frame), "Edit Stock"),
    (ServiceBilTab(body_frame), "Service Bill"),
    (ServiceBillHistory(body_frame), "Service Bill History"),
]
for tab in tabs:
    body_frame.add(tab[0].main_frame, text=tab[1])


def tab_changed(*args):
    index: int = body_frame.index(body_frame.select())
    tabs[index][0].refresh_tab()


body_frame.bind("<<NotebookTabChanged>>", tab_changed)

sv_ttk.set_theme(env.get("THEME"))


def start():
    root.mainloop()
