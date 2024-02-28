import re
import tkinter as tk
from tkinter import ttk
from datetime import date, datetime
from backend import type_dict, no_of_rows, add_item, add_batch
from backend import get_item_by_code, get_paginated_items, get_filtered_items


class ItemTab:
    def __init__(self, frame: ttk.Notebook):
        self.main_frame = ttk.Frame(frame)
        self.PADX = 10
        self.PADY = 5
        self.cols = ["ID", "Name", "Type", "Code", "Price", "Best Before"]
        self.init_vars()
        self.create_tab()
        self.refresh_tab()
        self.events()

    def init_vars(self):
        self.name = tk.StringVar()
        self.price = tk.DoubleVar()
        self.best_before = tk.IntVar()
        self.quantity = tk.IntVar()
        self.mfg_month = tk.IntVar()
        self.mfg_year = tk.IntVar()
        self.exp_month = tk.IntVar()
        self.exp_year = tk.IntVar()
        self.current_page = tk.IntVar()
        self.total_page = tk.IntVar()

    def create_tab(self):
        self.add_item_frame = ttk.LabelFrame(self.main_frame, text="Add Item")
        self.add_item_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # -------------------------------------------------------------------------------
        self.float_validation = self.main_frame.register(lambda x: x.replace(".", "", 1).isdigit() or (not x))
        self.int_validation = self.main_frame.register(lambda x: x.isdigit() or (not x))
        # -------------------------------------------------------------------------------
        self.name_label = ttk.Label(self.add_item_frame, text="Name: ")
        self.name_label.grid(row=0, column=0, padx=self.PADX, pady=(15, 5), sticky="e")
        self.name_entry = ttk.Entry(self.add_item_frame, textvariable=self.name)
        self.name_entry.grid(row=0, column=1, padx=self.PADX, pady=(15, 5), sticky="ew")

        self.type_label = ttk.Label(self.add_item_frame, text="Type: ")
        self.type_label.grid(row=1, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.type_entry = ttk.Combobox(
            self.add_item_frame, state="readonly",
            values=[key.capitalize() for key in type_dict.keys()]
        )
        self.type_entry.current(0)
        self.type_entry.grid(row=1, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.price_label = ttk.Label(self.add_item_frame, text="Price: ")
        self.price_label.grid(row=2, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.price_entry = ttk.Spinbox(
            self.add_item_frame, from_=0, to=999999, format="%.3f", textvariable=self.price,
            validate="key", validatecommand=(self.float_validation, "%P")
        )
        self.price_entry.grid(row=2, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.best_before_label = ttk.Label(self.add_item_frame, text="Best Before: ")
        self.best_before_label.grid(row=3, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.best_before_entry = ttk.Spinbox(
            self.add_item_frame, from_=0, to=999, state="disabled",  textvariable=self.best_before,
            validate="key", validatecommand=(self.int_validation, "%P")
        )
        self.best_before_entry.grid(row=3, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        # -------------------------------------------------------------------------------
        self.separator = ttk.Frame(self.add_item_frame, borderwidth=5, relief="sunken")
        self.separator.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        # -------------------------------------------------------------------------------

        self.batch_no_label = ttk.Label(self.add_item_frame, text="Batch No.: ")
        self.batch_no_label.grid(row=5, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.batch_no_entry = ttk.Entry(self.add_item_frame)
        self.batch_no_entry.grid(row=5, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.quantity_label = ttk.Label(self.add_item_frame, text="Quantity: ")
        self.quantity_label.grid(row=6, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.quantity_entry = ttk.Spinbox(
            self.add_item_frame, from_=0, to=999999, textvariable=self.quantity,
            validate="key", validatecommand=(self.int_validation, "%P")
        )
        self.quantity_entry.grid(row=6, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.mfg_date_label = ttk.Label(self.add_item_frame, text="Mfg. Date: ")
        self.mfg_date_label.grid(row=7, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.mfg_date_frame = ttk.Frame(self.add_item_frame)
        self.mfg_date_frame.grid(row=7, column=1, padx=self.PADX, pady=self.PADY)
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

        self.exp_date_label = ttk.Label(self.add_item_frame, text="Exp. Date: ")
        self.exp_date_label.grid(row=8, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.exp_date_frame = ttk.Frame(self.add_item_frame)
        self.exp_date_frame.grid(row=8, column=1, padx=self.PADX, pady=self.PADY)
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

        self.distributor_label = ttk.Label(self.add_item_frame, text="Distributor: ")
        self.distributor_label.grid(row=9, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.distributor_entry = ttk.Entry(self.add_item_frame)
        self.distributor_entry.grid(row=9, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.submit_button = ttk.Button(self.add_item_frame, text="Add Item", command=self.add_item_to_db)
        self.submit_button.grid(row=10, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

        self.possible_names_list = tk.Listbox(self.add_item_frame, font=("Aerial", 10))

        # -------------------------------------------------------------------------------
        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")
        self.item_table = ttk.Treeview(
            self.table_frame,
            show="headings",
            columns=self.cols,
            height=no_of_rows,
            selectmode="browse",
        )
        for col_name in self.cols:
            self.item_table.heading(col_name, text=col_name)
        self.item_table.column("ID", width=50, anchor="e")
        self.item_table.column("Price", width=100, anchor="e")
        self.item_table.column("Best Before", width=100, anchor="e")
        self.item_table.grid(row=0, column=0, sticky="nsew")

        self.item_page_number = ttk.Frame(self.table_frame)
        self.item_page_number.grid(row=1, column=0, sticky="n")

        self.current_page_entry = ttk.Spinbox(
            self.item_page_number, from_=1, state="readonly", width=3, textvariable=self.current_page
        )
        self.current_page_entry.grid(row=0, column=0)
        self.divider = ttk.Label(self.item_page_number, text=" / ", width=2)
        self.divider.grid(row=0, column=1)
        self.total_page_entry = ttk.Label(self.item_page_number, font=("Aerial", 12, "bold"), textvariable=self.total_page)
        self.total_page_entry.grid(row=0, column=2)

    def add_item_to_db(self):
        name: str = self.name.get()
        if not name:
            return None
        type: str = self.type_entry.get()
        price: float = float(self.price.get())
        best_before: int = int(self.best_before.get())
        item = add_item(name, type, price, best_before)

        batch_no: str = self.batch_no_entry.get()
        if batch_no:
            quantity: int = int(self.quantity.get())
            mfg_date: date = date(int(self.mfg_year.get()), int(self.mfg_month.get()), 1)
            exp_date: date = date(int(self.exp_year.get()), int(self.exp_month.get()), 1)
            distributor: str = self.distributor_entry.get()
            add_batch(item.id, batch_no, price, quantity, mfg_date, exp_date, distributor)
        self.refresh_tab()

    def refresh_tab(self):
        self.name_entry.delete(0, "end")
        self.type_entry.current(0)
        self.price.set(0)
        self.best_before.set(0)
        self.batch_no_entry.delete(0, "end")
        self.quantity.set(0)
        today = datetime.now()
        self.mfg_month.set(today.month)
        self.mfg_year.set(today.year)
        self.exp_month.set(today.month)
        self.exp_year.set(today.year)
        self.distributor_entry.delete(0, "end")
        self.current_page.set(1)
        self.refresh_table(page=1)

    def refresh_table(self, page: int):
        self.item_table.delete(*self.item_table.get_children())
        table_data, total_count = get_paginated_items(page=page)
        total_page = total_count // no_of_rows + 1
        self.total_page.set(total_page)
        self.current_page_entry.config(to=total_page)
        for row_data in table_data:
            self.item_table.insert('', tk.END, values=row_data)

    def events(self):
        self.name_entry.bind("<FocusIn>", self.show_possible_name_list)
        self.name_entry.bind("<FocusOut>", lambda x: self.possible_names_list.place_forget())
        self.possible_names_list.bind("<<ListboxSelect>>", self.select_name)
        self.name.trace_add("write", self.list_possible_names)
        self.mfg_month.trace_add("write", self.update_date)
        self.mfg_year.trace_add("write", self.update_date)
        self.exp_month.trace_add("write", self.update_best_before)
        self.exp_year.trace_add("write", self.update_best_before)
        self.current_page.trace_add("write", lambda *x: self.refresh_table(page=self.current_page.get()))

    def show_possible_name_list(self, *args):
        index = self.possible_names_list.index("end")
        if not index:
            return None
        self.possible_names_list.place(in_=self.name_entry, x=0, rely=1, relwidth=1.0)

    def list_possible_names(self, *args):
        entry = self.name.get() or ""
        entry = re.sub('[^A-Za-z0-9]+', '', entry).lower()
        self.possible_names_list.delete(0, "end")
        if len(entry) <= 3:
            self.possible_names_list.place_forget()
            return None
        self.possible_names_list.place(in_=self.name_entry, x=0, rely=1, relwidth=1.0)
        possible_items = get_filtered_items(code=entry)
        for possible_item in possible_items:
            self.possible_names_list.insert(
                "end",
                f"{type_dict.get(possible_item[2].lower(), "oth").capitalize()}. {possible_item[1]}"
            )

    def select_name(self, *args):
        selected_index = self.possible_names_list.curselection()
        if not selected_index:
            return None
        selected_name: str = self.possible_names_list.get(selected_index)
        item = get_item_by_code(code=re.sub('[^A-Za-z0-9]+', '', selected_name).lower())
        if not item:
            return None
        self.name.set(item.name)
        self.price.set(item.price)
        self.best_before.set(item.best_before)

        for i, type_name in enumerate(type_dict.keys()):
            if type_name == item.type.lower():
                self.type_entry.current(i)
                break
        self.update_date()

    def update_date(self, *args):
        best_before = int(self.best_before.get() or 0)
        mfg_month = int(self.mfg_month.get() or 0)
        mfg_year = int(self.mfg_year.get() or 0)
        if not (best_before and mfg_month and mfg_year):
            return None
        self.exp_month.set(((mfg_month + best_before) % 12) or 12)
        self.exp_year.set((mfg_year + (mfg_month + best_before - 1) // 12))

    def update_best_before(self, *args):
        mfg_month = int(self.mfg_month.get() or 0)
        mfg_year = int(self.mfg_year.get() or 0)
        exp_month = int(self.exp_month.get() or 0)
        exp_year = int(self.exp_year.get() or 0)
        if not (mfg_month and mfg_year and exp_month and exp_year):
            return None
        month_diff = (exp_year - mfg_year) * 12 + (exp_month - mfg_month)
        self.best_before.set(max(month_diff, 0))
