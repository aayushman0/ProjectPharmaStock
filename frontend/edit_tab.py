import re
from datetime import datetime, date
import tkinter as tk
from tkinter import ttk
from backend import type_dict, get_filtered_items, get_item_by_code, get_batch_nos_from_item_id
from backend import get_batch, edit_item, edit_batch


class EditTab:
    def __init__(self, frame: ttk.Notebook):
        self.main_frame = ttk.Frame(frame)
        self.PADX = 10
        self.PADY = 5
        self.init_vars()
        self.create_tab()
        self.refresh_tab()
        self.events()

    def init_vars(self):
        self.item_name = tk.StringVar()
        self.item_price = tk.DoubleVar()
        self.item_best_before = tk.IntVar()

        self.name = tk.StringVar()
        self.batch_no = tk.StringVar()
        self.price = tk.DoubleVar()
        self.quantity = tk.IntVar()
        self.best_before = 0
        self.mfg_month = tk.IntVar()
        self.mfg_year = tk.IntVar()
        self.exp_month = tk.IntVar()
        self.exp_year = tk.IntVar()

    def create_tab(self):
        self.float_validation = self.main_frame.register(lambda x: x.replace(".", "", 1).isdigit() or (not x))
        self.int_validation = self.main_frame.register(lambda x: x.isdigit() or (not x))
        # -------------------------------------------------------------------------------

        self.add_item_frame = ttk.LabelFrame(self.main_frame, text="Edit Item")
        self.add_item_frame.grid(row=0, column=1, padx=20, pady=10)

        self.item_name_label = ttk.Label(self.add_item_frame, text="Name: ")
        self.item_name_label.grid(row=0, column=0, padx=self.PADX, pady=(15, 5), sticky="e")
        self.item_name_entry = ttk.Entry(self.add_item_frame, textvariable=self.item_name)
        self.item_name_entry.grid(row=0, column=1, padx=self.PADX, pady=(15, 5), sticky="ew")

        self.item_type_label = ttk.Label(self.add_item_frame, text="Type: ")
        self.item_type_label.grid(row=1, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.item_type_entry = ttk.Combobox(
            self.add_item_frame, state="readonly",
            values=[key.capitalize() for key in type_dict.keys()]
        )
        self.item_type_entry.current(0)
        self.item_type_entry.grid(row=1, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.item_new_name_label = ttk.Label(self.add_item_frame, text="New Name: ")
        self.item_new_name_label.grid(row=2, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.item_new_name_entry = ttk.Entry(self.add_item_frame)
        self.item_new_name_entry.grid(row=2, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.item_price_label = ttk.Label(self.add_item_frame, text="Price: ")
        self.item_price_label.grid(row=3, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.item_price_entry = ttk.Spinbox(
            self.add_item_frame, from_=0, to=999999, format="%.3f", textvariable=self.item_price,
            validate="key", validatecommand=(self.float_validation, "%P")
        )
        self.item_price_entry.grid(row=3, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.item_best_before_label = ttk.Label(self.add_item_frame, text="Best Before: ")
        self.item_best_before_label.grid(row=4, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.item_best_before_entry = ttk.Spinbox(
            self.add_item_frame, from_=0, to=999,  textvariable=self.item_best_before,
            validate="key", validatecommand=(self.int_validation, "%P")
        )
        self.item_best_before_entry.grid(row=4, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.item_submit_button = ttk.Button(self.add_item_frame, text="Edit Item", command=self.edit_item_in_db)
        self.item_submit_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

        self.item_possible_names_list = tk.Listbox(self.add_item_frame, font=("Aerial", 10))

        # -------------------------------------------------------------------------------

        self.add_stock_frame = ttk.LabelFrame(self.main_frame, text="Edit Stock")
        self.add_stock_frame.grid(row=0, column=0, padx=20, pady=10)

        self.name_label = ttk.Label(self.add_stock_frame, text="Name: ")
        self.name_label.grid(row=0, column=0, padx=self.PADX, pady=(15, 5), sticky="e")
        self.name_entry = ttk.Entry(self.add_stock_frame, textvariable=self.name)
        self.name_entry.grid(row=0, column=1, padx=self.PADX, pady=(15, 5), sticky="ew")

        self.batch_no_label = ttk.Label(self.add_stock_frame, text="Batch No.: ")
        self.batch_no_label.grid(row=1, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.batch_no_entry = ttk.Combobox(self.add_stock_frame, state="readonly", textvariable=self.batch_no)
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

        self.stock_submit_button = ttk.Button(self.add_stock_frame, text="Edit Stock", command=self.edit_stock_in_db)
        self.stock_submit_button.grid(row=7, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

        self.possible_names_list = tk.Listbox(self.add_stock_frame, font=("Aerial", 10))

    def edit_item_in_db(self):
        old_name = self.item_name.get()
        type = self.item_type_entry.get()
        new_name = self.item_new_name_entry.get()
        if not (old_name and type and new_name):
            return None
        code = re.sub('[^A-Za-z0-9]+', '', old_name).lower()
        price = self.item_price.get() or 0
        best_before = self.item_best_before.get() or 0
        edit_item(code=code, name=new_name, type=type, price=price, best_before=best_before)
        self.refresh_tab()

    def edit_stock_in_db(self):
        name = self.name.get()
        batch_no = self.batch_no.get()
        if not (name or batch_no):
            return None
        code = re.sub('[^A-Za-z0-9]+', '', name).lower()
        price = self.price.get() or 0
        quantity = self.quantity.get() or 0
        mfg_date = date(int(self.mfg_year.get()), int(self.mfg_month.get()), 1)
        exp_date = date(int(self.exp_year.get()), int(self.exp_month.get()), 1)
        distributor = self.distributor_entry.get()
        edit_batch(code=code, batch_no=batch_no, price=price, quantity=quantity, mfg_date=mfg_date, exp_date=exp_date, distributor=distributor)
        self.refresh_tab()

    def refresh_tab(self):
        self.item_name.set("")
        self.item_type_entry.current(0)
        self.item_new_name_entry.delete(0, "end")
        self.item_price.set(0)
        self.item_best_before.set(0)

        self.name.set("")
        self.batch_no_entry["values"] = []
        self.price.set(0)
        self.quantity.set(0)
        today = datetime.now()
        self.mfg_month.set(today.month)
        self.mfg_year.set(today.year)
        self.exp_month.set(today.month)
        self.exp_year.set(today.year)
        self.distributor_entry.delete(0, "end")

    def events(self):
        self.item_name_entry.bind("<FocusIn>", self.item_show_possible_name_list)
        self.item_name_entry.bind("<FocusOut>", lambda x: self.item_possible_names_list.place_forget())
        self.item_name_entry.bind("<Return>", self.item_select_first_name)
        self.item_name_entry.bind("<Tab>", self.item_select_first_name)
        self.item_possible_names_list.bind("<<ListboxSelect>>", self.item_select_name)
        self.item_name.trace_add("write", self.item_list_possible_names)

        self.name_entry.bind("<FocusIn>", self.show_possible_name_list)
        self.name_entry.bind("<FocusOut>", lambda x: self.possible_names_list.place_forget())
        self.name_entry.bind("<Return>", self.select_first_name)
        self.name_entry.bind("<Tab>", self.select_first_name)
        self.possible_names_list.bind("<<ListboxSelect>>", self.select_name)
        self.name.trace_add("write", self.list_possible_names)
        self.batch_no.trace_add("write", self.update_stock_fields)
        self.mfg_month.trace_add("write", self.update_date)
        self.mfg_year.trace_add("write", self.update_date)

    def item_show_possible_name_list(self, *args):
        index = self.item_possible_names_list.index("end")
        if not index:
            return None
        self.item_possible_names_list.place(in_=self.item_name_entry, x=0, rely=1, relwidth=1.0)

    def item_list_possible_names(self, *args):
        entry = self.item_name.get() or ""
        entry = re.sub('[^A-Za-z0-9]+', '', entry).lower()
        self.item_possible_names_list.delete(0, "end")
        if len(entry) <= 3:
            return None
        self.item_possible_names_list.place(in_=self.item_name_entry, x=0, rely=1, relwidth=1.0)
        possible_items = get_filtered_items(code=entry)
        for possible_item in possible_items:
            self.item_possible_names_list.insert(
                "end",
                f"{type_dict.get(possible_item[2].lower(), "oth").capitalize()}. {possible_item[1]}"
            )

    def item_select_first_name(self, *args):
        first_name = self.item_possible_names_list.get(0)
        if not first_name:
            return None
        item = get_item_by_code(code=re.sub('[^A-Za-z0-9]+', '', first_name).lower())
        if not item:
            return None
        self.item_name.set(first_name)
        self.item_new_name_entry.delete(0, "end")
        self.item_new_name_entry.insert(0, item.name)
        self.item_price.set(item.price)
        self.item_best_before.set(item.best_before)
        self.item_possible_names_list.place_forget()

        for i, type_name in enumerate(type_dict.keys()):
            if type_name == item.type.lower():
                self.item_type_entry.current(i)
                break

    def item_select_name(self, *args):
        selected_index = self.item_possible_names_list.curselection()
        if not selected_index:
            return None
        selected_name: str = self.item_possible_names_list.get(selected_index)
        item = get_item_by_code(code=re.sub('[^A-Za-z0-9]+', '', selected_name).lower())
        if not item:
            return None
        self.item_name.set(selected_name)
        self.item_new_name_entry.delete(0, "end")
        self.item_new_name_entry.insert(0, item.name)
        self.item_price.set(item.price)
        self.item_best_before.set(item.best_before)

        for i, type_name in enumerate(type_dict.keys()):
            if type_name == item.type.lower():
                self.item_type_entry.current(i)
                break

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
            return None
        self.possible_names_list.place(in_=self.name_entry, x=0, rely=1, relwidth=1.0)
        possible_items = get_filtered_items(code=entry)
        for possible_item in possible_items:
            self.possible_names_list.insert(
                "end",
                f"{type_dict.get(possible_item[2].lower(), "oth").capitalize()}. {possible_item[1]}"
            )

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

        batches = get_batch_nos_from_item_id(item_id=item.id)
        if not batches:
            self.batch_no_entry["values"] = []
            self.batch_no_entry.set("")
            return None
        self.batch_no_entry["values"] = batches
        self.batch_no_entry.current(0)

    def update_stock_fields(self, *args):
        name = self.name.get()
        batch_no = self.batch_no.get()
        if not (name and batch_no):
            return None
        batch = get_batch(item_code=re.sub('[^A-Za-z0-9]+', '', name).lower(), batch_no=batch_no)
        if not batch:
            return None
        self.price.set(batch.price)
        self.quantity.set(batch.quantity)
        self.mfg_month.set(batch.mfg_date.month)
        self.mfg_year.set(batch.mfg_date.year)
        self.exp_month.set(batch.exp_date.month)
        self.exp_year.set(batch.exp_date.year)
        self.distributor_entry.insert(0, batch.distributor or "")

    def update_date(self, *args):
        best_before = self.best_before
        mfg_month = int(self.mfg_month.get() or 0)
        mfg_year = int(self.mfg_year.get() or 0)
        if not (best_before and mfg_month and mfg_year):
            return None
        self.exp_month.set(((mfg_month + best_before) % 12) or 12)
        self.exp_year.set((mfg_year + (mfg_month + best_before - 1) // 12))
