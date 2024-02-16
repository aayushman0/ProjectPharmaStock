import re
from datetime import date
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from backend import type_dict, no_of_rows, add_batch, get_item_by_code, get_paginated_batches, get_filtered_items


class StockTab:
    def __init__(self, frame: ttk.Notebook):
        self.main_frame = ttk.Frame(frame)
        self.PADX = 10
        self.PADY = 5
        self.cols = ["Name", "Batch No.", "Quantity", "Price", "Total", "Mfg Date", "Exp Date", "Distributor"]
        self.best_before = 0
        self.init_vars()
        self.create_tab()
        self.refresh_tab()
        self.events()

    def init_vars(self):
        self.name = tk.StringVar()
        self.price = tk.DoubleVar()
        self.quantity = tk.IntVar()
        self.mfg_month = tk.IntVar()
        self.mfg_year = tk.IntVar()
        self.exp_month = tk.IntVar()
        self.exp_year = tk.IntVar()
        self.current_page = tk.IntVar()
        self.total_page = tk.IntVar()

    def create_tab(self):
        self.add_stock_frame = ttk.LabelFrame(self.main_frame, text="Add Stock")
        self.add_stock_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # -------------------------------------------------------------------------------
        self.float_validation = self.add_stock_frame.register(lambda x: x.replace(".", "", 1).isdigit() or (not x))
        self.int_validation = self.add_stock_frame.register(lambda x: x.isdigit() or (not x))
        # -------------------------------------------------------------------------------
        self.name_label = ttk.Label(self.add_stock_frame, text="Name: ")
        self.name_label.grid(row=0, column=0, padx=self.PADX, pady=(15, 5), sticky="e")
        self.name_entry = ttk.Entry(self.add_stock_frame, textvariable=self.name)
        self.name_entry.grid(row=0, column=1, padx=self.PADX, pady=(15, 5), sticky="ew")

        self.batch_no_label = ttk.Label(self.add_stock_frame, text="Batch No.: ")
        self.batch_no_label.grid(row=1, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.batch_no_entry = ttk.Entry(self.add_stock_frame)
        self.batch_no_entry.grid(row=1, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.price_label = ttk.Label(self.add_stock_frame, text="Price: ")
        self.price_label.grid(row=2, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.price_entry = ttk.Spinbox(
            self.add_stock_frame, from_=0, to=999999, format="%.3f", textvariable=self.price,
            validate="key", validatecommand=(self.float_validation, "%P")
        )
        self.price_entry.grid(row=2, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.quantity_label = ttk.Label(self.add_stock_frame, text="Quantity: ")
        self.quantity_label.grid(row=3, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.quantity_entry = ttk.Spinbox(
            self.add_stock_frame, from_=0, to=999999, textvariable=self.quantity,
            validate="key", validatecommand=(self.int_validation, "%P")
        )
        self.quantity_entry.grid(row=3, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.mfg_date_label = ttk.Label(self.add_stock_frame, text="Mfg. Date: ")
        self.mfg_date_label.grid(row=4, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.mfg_date_frame = ttk.Frame(self.add_stock_frame)
        self.mfg_date_frame.grid(row=4, column=1, padx=self.PADX, pady=self.PADY)
        self.mfg_month_box = ttk.Spinbox(
            self.mfg_date_frame, from_=1, to=12, width=4, textvariable=self.mfg_month,
            validate="key", validatecommand=(self.int_validation, "%P")
        )
        self.mfg_month_box.grid(row=0, column=0, sticky="ew")
        self.mfg_year_box = ttk.Spinbox(
            self.mfg_date_frame, from_=2000, to=2999, width=6, textvariable=self.mfg_year,
            validate="key", validatecommand=(self.int_validation, "%P")
        )
        self.mfg_year_box.grid(row=0, column=1, sticky="ew")

        self.exp_date_label = ttk.Label(self.add_stock_frame, text="Exp. Date: ")
        self.exp_date_label.grid(row=5, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.exp_date_frame = ttk.Frame(self.add_stock_frame)
        self.exp_date_frame.grid(row=5, column=1, padx=self.PADX, pady=self.PADY)
        self.exp_month_box = ttk.Spinbox(
            self.exp_date_frame, from_=1, to=12, width=4, textvariable=self.exp_month,
            validate="key", validatecommand=(self.int_validation, "%P")
        )
        self.exp_month_box.grid(row=0, column=0, sticky="ew")
        self.exp_year_box = ttk.Spinbox(
            self.exp_date_frame, from_=2000, to=2999, width=6, textvariable=self.exp_year,
            validate="key", validatecommand=(self.int_validation, "%P")
        )
        self.exp_year_box.grid(row=0, column=1, sticky="ew")

        self.distributor_label = ttk.Label(self.add_stock_frame, text="Distributor: ")
        self.distributor_label.grid(row=6, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.distributor_entry = ttk.Entry(self.add_stock_frame)
        self.distributor_entry.grid(row=6, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.submit_button = ttk.Button(self.add_stock_frame, text="Add Stock", command=self.add_stock_to_db)
        self.submit_button.grid(row=7, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

        self.possible_names_list = tk.Listbox(self.add_stock_frame, font=("Aerial", 10))

        # -------------------------------------------------------------------------------
        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")
        self.stock_table = ttk.Treeview(
            self.table_frame,
            show="headings",
            columns=self.cols,
            height=no_of_rows,
            selectmode="browse",
        )
        for col_name in self.cols:
            self.stock_table.heading(col_name, text=col_name)
        self.stock_table.column("Batch No.", width=150)
        self.stock_table.column("Quantity", width=50, anchor="e")
        self.stock_table.column("Price", width=70, anchor="e")
        self.stock_table.column("Total", width=70, anchor="e")
        self.stock_table.column("Mfg Date", width=70, anchor="e")
        self.stock_table.column("Exp Date", width=70, anchor="e")
        self.stock_table.column("Distributor", width=100, anchor="e")
        self.stock_table.grid(row=0, column=0, sticky="nsew")

        self.stock_page_number = ttk.Frame(self.table_frame)
        self.stock_page_number.grid(row=1, column=0, sticky="n")

        self.current_page_entry = ttk.Spinbox(
            self.stock_page_number, from_=1, state="readonly", width=3, textvariable=self.current_page
        )
        self.current_page_entry.grid(row=0, column=0)
        self.divider = ttk.Label(self.stock_page_number, text=" / ", width=2)
        self.divider.grid(row=0, column=1)
        self.total_page_entry = ttk.Label(self.stock_page_number, font=("Aerial", 12, "bold"), textvariable=self.total_page)
        self.total_page_entry.grid(row=0, column=2)

    def add_stock_to_db(self):
        name: str = self.name.get()
        batch_no: str = self.batch_no_entry.get()
        if not (name and batch_no):
            return None
        item = get_item_by_code(code=re.sub('[^A-Za-z0-9]+', '', name).lower())
        if not item:
            return None
        price: float = self.price.get()
        quantity: int = self.quantity.get()
        mfg_date: date = date(int(self.mfg_year.get()), int(self.mfg_month.get()), 1)
        exp_date: date = date(int(self.exp_year.get()), int(self.exp_month.get()), 1)
        distributor: str = self.distributor_entry.get()
        add_batch(item.id, batch_no, price, quantity, mfg_date, exp_date, distributor)
        self.refresh_tab()

    def refresh_tab(self):
        self.name.set("")
        self.batch_no_entry.delete(0, "end")
        self.price_entry.set(0)
        self.quantity_entry.set(0)
        today = datetime.now()
        self.mfg_month.set(today.month)
        self.mfg_year.set(today.year)
        self.exp_month.set(today.month)
        self.exp_year.set(today.year)
        self.distributor_entry.delete(0, "end")
        self.current_page.set(1)
        self.refresh_table(page=1)

    def refresh_table(self, page: int, code: str | None = None):
        self.stock_table.delete(*self.stock_table.get_children())
        table_data, total_count = get_paginated_batches(page=page, code=code)
        total_page = total_count // no_of_rows + 1
        self.total_page.set(total_page)
        self.current_page_entry.config(to=total_page)
        for row_data in table_data:
            self.stock_table.insert('', tk.END, values=row_data)

    def events(self):
        self.name_entry.bind("<FocusIn>", self.show_possible_name_list)
        self.name_entry.bind("<FocusOut>", self.hide_possible_name_list)
        self.name_entry.bind("<Return>", self.select_first_name)
        self.name_entry.bind("<Tab>", self.select_first_name)
        self.possible_names_list.bind("<<ListboxSelect>>", self.select_name)
        self.name.trace_add("write", self.list_possible_names)
        self.mfg_month.trace_add("write", self.update_date)
        self.mfg_year.trace_add("write", self.update_date)
        self.current_page.trace_add("write", lambda *x: self.refresh_table(page=self.current_page.get()))

    def show_possible_name_list(self, *args):
        index = self.possible_names_list.index("end")
        if not index:
            return None
        self.possible_names_list.place(in_=self.name_entry, x=0, rely=1, relwidth=1.0)

    def hide_possible_name_list(self, *args):
        self.possible_names_list.place_forget()
        self.refresh_table(page=1)

    def list_possible_names(self, *args):
        entry = self.name.get() or ""
        entry = re.sub('[^A-Za-z0-9]+', '', entry).lower()
        self.possible_names_list.delete(0, "end")
        if len(entry) <= 3:
            return None
        self.possible_names_list.place(in_=self.name_entry, x=0, rely=1, relwidth=1.0)
        possible_items = get_filtered_items(code=entry)
        for possible_item in possible_items:
            self.possible_names_list.insert(
                "end",
                f"{type_dict.get(possible_item[2].lower(), "oth").capitalize()}. {possible_item[1]}"
            )
        self.refresh_table(page=1, code=entry)

    def select_first_name(self, *args):
        first_name = self.possible_names_list.get(0)
        if not first_name:
            return None
        self.update_item_fields(name=first_name)
        self.possible_names_list.place_forget()

    def select_name(self, *args):
        selected_index = self.possible_names_list.curselection()
        if not selected_index:
            return None
        self.update_item_fields(name=self.possible_names_list.get(selected_index))

    def update_item_fields(self, name: str):
        item = get_item_by_code(code=re.sub('[^A-Za-z0-9]+', '', name).lower())
        if not item:
            return None
        self.name.set(name)
        self.price.set(item.price)
        self.best_before = item.best_before

    def update_date(self, *args):
        best_before = self.best_before
        mfg_month = int(self.mfg_month.get() or 0)
        mfg_year = int(self.mfg_year.get() or 0)
        if not (best_before and mfg_month and mfg_year):
            return None
        self.exp_month.set(((mfg_month + best_before) % 12) or 12)
        self.exp_year.set((mfg_year + (mfg_month + best_before - 1) // 12))
