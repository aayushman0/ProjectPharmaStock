from tkinter import ttk
from backend import no_of_rows, get_paginated_bills, get_bill_json_by_id


class BillHistory:
    def __init__(self, frame: ttk.Notebook):
        self.main_frame = ttk.Frame(frame)
        self.PADX = 10
        self.PADY = 5
        self.cols = ["SN", "Particular", "Batch No", "Mfg Date", "Exp Date", "Quantity", "Price", "Total"]
        self.create_tab()
        self.refresh_tab()
        self.events()

    def create_tab(self):
        self.bill_list_frame = ttk.Frame(self.main_frame)
        self.bill_list_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.bill_list_table = ttk.Treeview(
            self.bill_list_frame,
            show="headings",
            columns=["SN", "Customers Name", "Net Total", "Bill Date"],
            height=no_of_rows,
        )
        for col_name in ["SN", "Customers Name", "Net Total", "Bill Date"]:
            self.bill_list_table.heading(col_name, text=col_name)
        self.bill_list_table.column("SN", width=50, anchor="e")
        self.bill_list_table.column("Customers Name", width=150)
        self.bill_list_table.column("Net Total", width=80, anchor="e")
        self.bill_list_table.column("Bill Date", width=120)
        self.bill_list_table.grid(row=0, column=0, sticky="nsew")

        # -------------------------------------------------------------------------------
        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")
        self.bill_table = ttk.Treeview(
            self.table_frame,
            show="headings",
            columns=self.cols,
            height=20,
        )
        for col_name in self.cols:
            self.bill_table.heading(col_name, text=col_name)
        self.bill_table.column("SN", width=50, anchor="e")
        self.bill_table.column("Mfg Date", width=80, anchor="e")
        self.bill_table.column("Exp Date", width=80, anchor="e")
        self.bill_table.column("Quantity", width=70, anchor="e")
        self.bill_table.column("Price", width=70, anchor="e")
        self.bill_table.column("Total", width=80, anchor="e")
        self.bill_table.grid(row=0, column=0, sticky="nsew")

    def refresh_tab(self):
        self.bill_list_table.delete(*self.bill_list_table.get_children())
        self.bill_table.delete(*self.bill_table.get_children())
        bills, bill_count = get_paginated_bills(page=1)
        for bill in bills:
            self.bill_list_table.insert('', "end", values=bill)
        self.bill_list_table.selection_set(self.bill_list_table.get_children()[0])

    def events(self):
        self.bill_list_table.bind("<<TreeviewSelect>>", self.display_bill_detail)

    def display_bill_detail(self, *args):
        selected_row = self.bill_list_table.selection()
        if not selected_row:
            return None
        bill_id: int = self.bill_list_table.item(selected_row[0]).get("values", [0])[0]
        bill_json = get_bill_json_by_id(id=bill_id)
        self.bill_table.delete(*self.bill_table.get_children())
        if not bill_json:
            return None
        for row in bill_json:
            self.bill_table.insert("", "end", values=row)
