import re
import tkinter as tk
from tkinter import ttk

from backend import type_dict, get_batch, get_filtered_items, get_item_by_code, get_batch_nos_from_item_id, add_bill


class BillTab:
    def __init__(self, frame: ttk.Notebook):
        self.notebook = frame
        self.main_frame = ttk.Frame(frame)
        self.PADX = 10
        self.PADY = 5
        self.cols = ["SN", "Particular", "Batch No", "Mfg Date", "Exp Date", "Quantity", "Price", "Total"]
        self.bill_json = list()
        self.init_vars()
        self.create_tab()
        self.refresh_tab()
        self.events()

    def init_vars(self):
        self.name = tk.StringVar()
        self.batch_no = tk.StringVar()
        self.price = tk.DoubleVar()
        self.quantity = tk.IntVar()
        self.total = tk.DoubleVar()
        self.sum_total = tk.DoubleVar()
        self.discount = tk.DoubleVar()
        self.net_total = tk.DoubleVar()

    def create_tab(self):
        self.add_bill_frame = ttk.LabelFrame(self.main_frame, text="Add Bill")
        self.add_bill_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # -------------------------------------------------------------------------------
        self.float_validation = self.main_frame.register(lambda x: x.replace(".", "", 1).isdigit() or (not x))
        self.int_validation = self.main_frame.register(lambda x: x.isdigit() or (not x))
        # -------------------------------------------------------------------------------

        self.customer_name_label = ttk.Label(self.add_bill_frame, text="Customer's Name: ")
        self.customer_name_label.grid(row=0, column=0, padx=self.PADX, pady=(15, 5), sticky="e")
        self.customer_name_entry = ttk.Entry(self.add_bill_frame)
        self.customer_name_entry.grid(row=0, column=1, padx=self.PADX, pady=(15, 5), sticky="ew")

        # -------------------------------------------------------------------------------
        self.separator = ttk.Frame(self.add_bill_frame, borderwidth=5, relief="sunken")
        self.separator.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        # -------------------------------------------------------------------------------

        self.name_label = ttk.Label(self.add_bill_frame, text="Name: ")
        self.name_label.grid(row=2, column=0, padx=self.PADX, pady=(15, 5), sticky="e")
        self.name_entry = ttk.Entry(self.add_bill_frame, textvariable=self.name)
        self.name_entry.grid(row=2, column=1, padx=self.PADX, pady=(15, 5), sticky="ew")

        self.batch_no_label = ttk.Label(self.add_bill_frame, text="Batch No.: ")
        self.batch_no_label.grid(row=3, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.batch_no_entry = ttk.Combobox(self.add_bill_frame, state="readonly", textvariable=self.batch_no)
        self.batch_no_entry.grid(row=3, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.quantity_label = ttk.Label(self.add_bill_frame, text="Quantity: ")
        self.quantity_label.grid(row=4, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.quantity_entry = ttk.Spinbox(
            self.add_bill_frame, from_=0, to=999999, textvariable=self.quantity,
            validate="key", validatecommand=(self.int_validation, "%P")
        )
        self.quantity_entry.grid(row=4, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.price_label = ttk.Label(self.add_bill_frame, text="Price: ")
        self.price_label.grid(row=5, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.price_entry = ttk.Spinbox(
            self.add_bill_frame, from_=0, to=999999, format="%.3f", textvariable=self.price,
            validate="key", validatecommand=(self.float_validation, "%P")
        )
        self.price_entry.grid(row=5, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.total_label = ttk.Label(self.add_bill_frame, text="Total: ")
        self.total_label.grid(row=6, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.total_entry = ttk.Spinbox(self.add_bill_frame, state="disabled", format="%.3f", textvariable=self.total)
        self.total_entry.grid(row=6, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.submit_button = ttk.Button(self.add_bill_frame, text="Add Item", command=self.add_item_to_bill)
        self.submit_button.grid(row=7, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

        self.delete_button = ttk.Button(self.add_bill_frame, text="Remove Item", command=self.remove_item_from_bill)
        self.delete_button.grid(row=8, column=0, columnspan=2, padx=10, pady=(0, 20), sticky="ew")

        # -------------------------------------------------------------------------------
        self.separator_2 = ttk.Frame(self.add_bill_frame, borderwidth=5, relief="sunken")
        self.separator_2.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        # -------------------------------------------------------------------------------

        self.payment_type_label = ttk.Label(self.add_bill_frame, text="Payment Type: ")
        self.payment_type_label.grid(row=10, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.payment_type_entry = ttk.Combobox(self.add_bill_frame, state="readonly", values=["Cash", "eSewa", "eBank"])
        self.payment_type_entry.grid(row=10, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.discount_label_2 = ttk.Label(self.add_bill_frame, text="Discount: ")
        self.discount_label_2.grid(row=11, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.discount_entry_2 = ttk.Spinbox(
            self.add_bill_frame, from_=0, to=999999, format="%.2f", textvariable=self.discount,
            validate="key", validatecommand=(self.float_validation, "%S")
        )
        self.discount_entry_2.grid(row=11, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.possible_names_list = tk.Listbox(self.add_bill_frame, font=("Aerial", 10))

        # -------------------------------------------------------------------------------
        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")
        self.bill_table = ttk.Treeview(
            self.table_frame,
            show="headings",
            columns=self.cols,
            height=20,
            selectmode="browse",
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

        self.bill_footer = ttk.Frame(self.table_frame)
        self.bill_footer.grid(row=1, column=0, sticky="ew")

        self.sum_total_label = ttk.Label(self.bill_footer, text="Sum Total: Rs.", font=("Aerial", 10, "bold"))
        self.sum_total_label.grid(row=0, column=0, sticky="e")
        self.sum_total_entry = ttk.Label(self.bill_footer, textvariable=self.sum_total)
        self.sum_total_entry.grid(row=0, column=1, sticky="w")

        self.discount_label = ttk.Label(self.bill_footer, text="Discount: Rs.", font=("Aerial", 10, "bold"))
        self.discount_label.grid(row=1, column=0, sticky="e")
        self.discount_entry = ttk.Label(self.bill_footer, textvariable=self.discount)
        self.discount_entry.grid(row=1, column=1, sticky="w")

        self.net_total_label = ttk.Label(self.bill_footer, text="Net Total: Rs.", font=("Aerial", 10, "bold"))
        self.net_total_label.grid(row=2, column=0, sticky="e")
        self.net_total_entry = ttk.Label(self.bill_footer, width=25, textvariable=self.net_total)
        self.net_total_entry.grid(row=2, column=1, sticky="w")

        self.create_bill_button = ttk.Button(self.bill_footer, text="Save Bill", width=50, command=self.save_bill_to_db)
        self.create_bill_button.grid(row=1, column=3, rowspan=2, sticky="e")

    def add_item_to_bill(self):
        name = self.name.get()
        batch_no = self.batch_no.get()
        quantity = self.quantity.get()
        if not (name and batch_no and quantity):
            return None
        price = self.price.get()
        total = self.total.get()
        batch = get_batch(item_code=re.sub('[^A-Za-z0-9]+', '', name).lower(), batch_no=batch_no)
        if not batch:
            return None
        sn = len(self.bill_table.get_children()) + 1
        mfg_date = str(batch.mfg_date)[:-3]
        exp_date = str(batch.exp_date)[:-3]
        self.bill_json.append({
            "sn": sn,
            "particular": name,
            "batch_id": batch.id,
            "batch_no": batch_no,
            "mfg_date": mfg_date,
            "exp_date": exp_date,
            "quantity": quantity,
            "price": price,
            "total": total
        })
        self.bill_table.insert('', tk.END, values=(sn, name, batch_no, mfg_date, exp_date, quantity, price, total))
        self.sum_total.set(self.sum_total.get() + total)
        self.refresh_entry()
        self.calculate_net_total()

    def remove_item_from_bill(self):
        rows = self.bill_table.get_children()
        if not rows:
            return None
        self.bill_table.delete(rows[-1])
        last_entry = self.bill_json.pop()
        self.sum_total.set(self.sum_total.get() - last_entry.get("total", 0))
        self.calculate_net_total()

    def save_bill_to_db(self):
        if not self.bill_json:
            return None
        customer_name = self.customer_name_entry.get()
        payment_type = self.payment_type_entry.get()
        add_bill(customer_name, self.bill_json, self.sum_total.get(), self.discount.get(), self.net_total.get(), payment_type)
        self.notebook.select(3)

    def refresh_tab(self):
        self.customer_name_entry.delete(0, "end")
        self.refresh_entry()
        self.bill_table.delete(*self.bill_table.get_children())
        self.sum_total.set(0)
        self.discount.set(0)
        self.net_total.set(0)
        self.payment_type_entry.current(0)
        self.bill_json = list()

    def refresh_entry(self):
        self.name.set("")
        self.batch_no_entry["values"] = []
        self.batch_no.set("")
        self.quantity.set(0)
        self.price.set(0)
        self.total.set(0)

    def events(self):
        self.name_entry.bind("<FocusIn>", self.show_possible_name_list)
        self.name_entry.bind("<FocusOut>", lambda x: self.possible_names_list.place_forget())
        self.name_entry.bind("<Return>", self.select_first_name)
        self.name_entry.bind("<Tab>", self.select_first_name)
        self.possible_names_list.bind("<<ListboxSelect>>", self.select_name)
        self.name.trace_add("write", self.list_possible_names)
        self.batch_no.trace_add("write", self.update_price)
        self.quantity.trace_add("write", self.calculate_total)
        self.price.trace_add("write", self.calculate_total)
        self.discount.trace_add("write", self.calculate_net_total)

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

        batches = get_batch_nos_from_item_id(item_id=item.id)
        if not batches:
            self.batch_no_entry["values"] = []
            self.batch_no_entry.set("")
            return None
        self.batch_no_entry["values"] = batches
        self.batch_no_entry.current(0)

    def update_price(self, *args):
        if not self.name.get():
            return None
        item_code = re.sub('[^A-Za-z0-9]+', '', self.name.get()).lower()
        batch = get_batch(item_code, self.batch_no.get())
        if not batch:
            return None
        self.price.set(batch.price)

    def calculate_total(self, *args):
        quantity = self.quantity.get() or 0
        price = self.price.get() or 0
        self.total.set(quantity * price)

    def calculate_net_total(self, *args):
        sum_total = self.sum_total.get() or 0
        discount = self.discount.get() or 0
        self.net_total.set(max((sum_total - discount), 0))
