import tkinter as tk
from tkinter import ttk

from backend import add_service_bill


class ServiceBilTab:
    def __init__(self, frame: ttk.Notebook):
        self.notebook = frame
        self.main_frame = ttk.Frame(frame)
        self.PADX = 10
        self.PADY = 5
        self.cols = ["SN", "Procedure", "Amount"]
        self.bill_json = list()
        self.init_vars()
        self.create_tab()
        self.refresh_tab()
        self.events()

    def init_vars(self):
        self.name = tk.StringVar()
        self.total = tk.DoubleVar()
        self.sum_total = tk.DoubleVar()
        self.discount = tk.DoubleVar()
        self.net_total = tk.DoubleVar()

    def create_tab(self):
        self.add_bill_frame = ttk.LabelFrame(self.main_frame, text="Add Service Bill")
        self.add_bill_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # -------------------------------------------------------------------------------
        self.float_validation = self.main_frame.register(lambda x: x.replace(".", "", 1).isdigit() or (not x))
        self.int_validation = self.main_frame.register(lambda x: x.isdigit() or (not x))
        # -------------------------------------------------------------------------------

        self.customer_name_label = ttk.Label(self.add_bill_frame, text="Patient's Name: ")
        self.customer_name_label.grid(row=0, column=0, padx=self.PADX, pady=(15, 5), sticky="e")
        self.customer_name_entry = ttk.Entry(self.add_bill_frame)
        self.customer_name_entry.grid(row=0, column=1, padx=self.PADX, pady=(15, 5), sticky="ew")

        # -------------------------------------------------------------------------------
        self.separator = ttk.Frame(self.add_bill_frame, borderwidth=5, relief="sunken")
        self.separator.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        # -------------------------------------------------------------------------------

        self.name_label = ttk.Label(self.add_bill_frame, text="Service: ")
        self.name_label.grid(row=2, column=0, padx=self.PADX, pady=(15, 5), sticky="e")
        self.name_entry = ttk.Entry(self.add_bill_frame, textvariable=self.name)
        self.name_entry.grid(row=2, column=1, padx=self.PADX, pady=(15, 5), sticky="ew")

        self.amount_label = ttk.Label(self.add_bill_frame, text="Amount: ")
        self.amount_label.grid(row=3, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.amount_entry = ttk.Spinbox(
            self.add_bill_frame, from_=0, to=999999, format="%.3f", textvariable=self.total,
            validate="key", validatecommand=(self.float_validation, "%P")
        )
        self.amount_entry.grid(row=3, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.submit_button = ttk.Button(self.add_bill_frame, text="Add Service", command=self.add_item_to_bill)
        self.submit_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

        self.delete_button = ttk.Button(self.add_bill_frame, text="Remove Service", command=self.remove_item_from_bill)
        self.delete_button.grid(row=5, column=0, columnspan=2, padx=10, pady=(0, 20), sticky="ew")

        # -------------------------------------------------------------------------------
        self.separator_2 = ttk.Frame(self.add_bill_frame, borderwidth=5, relief="sunken")
        self.separator_2.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        # -------------------------------------------------------------------------------

        self.payment_type_label = ttk.Label(self.add_bill_frame, text="Payment Type: ")
        self.payment_type_label.grid(row=7, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.payment_type_entry = ttk.Combobox(self.add_bill_frame, state="readonly", values=["Cash", "eSewa", "eBank"])
        self.payment_type_entry.grid(row=7, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.discount_label_2 = ttk.Label(self.add_bill_frame, text="Discount: ")
        self.discount_label_2.grid(row=8, column=0, padx=self.PADX, pady=self.PADY, sticky="e")
        self.discount_entry_2 = ttk.Spinbox(
            self.add_bill_frame, from_=0, to=999999, format="%.2f", textvariable=self.discount,
            validate="key", validatecommand=(self.float_validation, "%S")
        )
        self.discount_entry_2.grid(row=8, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

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
        self.bill_table.column("SN", width=20, anchor="e")
        self.bill_table.column("Procedure", width=500)
        self.bill_table.column("Amount", width=80, anchor="e")
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

        self.create_bill_button = ttk.Button(self.bill_footer, text="Save Service Bill", width=50, command=self.save_bill_to_db)
        self.create_bill_button.grid(row=1, column=3, rowspan=2, sticky="e")

    def add_item_to_bill(self):
        name = self.name.get()
        amount = self.total.get()
        if not (name and amount):
            return None
        sn = len(self.bill_table.get_children()) + 1
        self.bill_json.append({
            "sn": sn,
            "procedure": name,
            "amount": amount,
        })
        self.bill_table.insert('', "end", values=(sn, name, amount))
        self.sum_total.set(self.sum_total.get() + amount)
        self.refresh_entry()
        self.calculate_net_total()

    def remove_item_from_bill(self):
        rows = self.bill_table.get_children()
        if not rows:
            return None
        self.bill_table.delete(rows[-1])
        last_entry = self.bill_json.pop()
        self.sum_total.set(self.sum_total.get() - last_entry.get("amount", 0))
        self.calculate_net_total()

    def save_bill_to_db(self):
        if not self.bill_json:
            return None
        patient_name = self.customer_name_entry.get()
        payment_type = self.payment_type_entry.get()
        add_service_bill(patient_name, self.bill_json, self.sum_total.get(), self.discount.get(), self.net_total.get(), payment_type)
        self.notebook.select(6)

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
        self.total.set(0)

    def events(self):
        self.discount.trace_add("write", self.calculate_net_total)

    def calculate_net_total(self, *args):
        sum_total = self.sum_total.get() or 0
        discount = self.discount.get() or 0
        self.net_total.set(max((sum_total - discount), 0))
