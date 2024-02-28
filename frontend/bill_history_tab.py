import os
import json
from datetime import date, timedelta
import tkinter as tk
from tkinter import ttk
from backend import get_bills_by_date, get_bill_json_by_id, get_bill
from docx import Document


class BillHistory:
    def __init__(self, frame: ttk.Notebook):
        self.main_frame = ttk.Frame(frame)
        self.PADX = 10
        self.PADY = 5
        self.current_date = date.today()
        self.days_total = tk.DoubleVar()
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
            height=20,
        )
        for col_name in ["SN", "Customers Name", "Net Total", "Bill Date"]:
            self.bill_list_table.heading(col_name, text=col_name)
        self.bill_list_table.column("SN", width=50, anchor="e")
        self.bill_list_table.column("Customers Name", width=150)
        self.bill_list_table.column("Net Total", width=80, anchor="e")
        self.bill_list_table.column("Bill Date", width=125)
        self.bill_list_table.grid(row=0, column=0, sticky="nsew")

        self.page_frame = ttk.Frame(self.bill_list_frame)
        self.page_frame.grid(row=1, column=0, sticky="e")

        self.prev_page_button = ttk.Button(self.page_frame, text="<<", command=lambda: self.date_changed(-1))
        self.prev_page_button.grid(row=0, column=0)

        self.date_label = ttk.Label(self.page_frame, text=self.current_date, width=10)
        self.date_label.grid(row=0, column=1)

        self.next_page_button = ttk.Button(self.page_frame, text=">>", command=lambda: self.date_changed(1))
        self.next_page_button.grid(row=0, column=2)

        ttk.Label(self.page_frame, width=5).grid(row=0, column=3)

        self.days_total_label = ttk.Label(self.page_frame, text="Total: ", font=("Aerial", 12, "bold"))
        self.days_total_label.grid(row=0, column=4)

        self.days_total_entry = ttk.Label(self.page_frame, textvariable=self.days_total, font=("Aerial", 11), width=10, anchor="e")
        self.days_total_entry.grid(row=0, column=5)

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

        self.bill_footer = ttk.Frame(self.table_frame)
        self.bill_footer.grid(row=1, column=0, sticky="e")

        self.print_button = ttk.Button(self.bill_footer, text="Print Bill", width=20, command=self.print_bill)
        self.print_button.grid(row=0, column=0, pady=10, sticky="e")

    def print_bill(self):
        selected_row = self.bill_list_table.selection()
        if not selected_row:
            return None
        bill_id: int = self.bill_list_table.item(selected_row[0]).get("values", [0])[0]
        bill = get_bill(id=bill_id)

        document = Document("bill_sample.docx")
        id_string = f"[{bill.id:04d}]"
        date_string = bill.bill_date.strftime("%d/%m/%Y")
        customer_name = bill.customer_name
        items = ""
        total = f"{bill.total_amount:8.2f}"
        discount = f"{bill.discount:8.2f}"
        net_total = f"{bill.net_amount:8.2f}"
        payment_type = f"[{bill.payment_type}]".rjust(11)

        for item in json.loads(bill.bill_json):
            sn = f"{item.get("sn", 0):02d}  "

            particular = item.get("particular", "Oth. ---")[5:]
            particular_length = len(particular)
            if particular_length < 10:
                particular = f"{particular}\t\t"
            elif particular_length < 16:
                particular = f"{particular}\t"
            else:
                particular = particular[:15] + "\t"

            batch_no = item.get("batch_no", "")
            batch_no_length = len(batch_no)
            if batch_no_length < 7:
                batch_no = f"{batch_no}\t\t"
            elif batch_no_length < 12:
                batch_no = f"{batch_no}\t"
            else:
                batch_no = batch_no[:11] + "\t"

            exp = item.get("exp_date", "YYYY-MM")
            exp = f"{exp[5:7]}/{exp[2:4]}\t"
            qty = item.get("quantity", 0)
            qty = f"{qty}".ljust(5)
            price = item.get("price", 0)
            price = f"{price:.2f}\t"
            amount = item.get("total", 0)
            amount = f"{amount:.2f}".rjust(9)

            items += f"{sn}{particular}{batch_no}{exp}{qty}{price}{amount}\n"

        replacement_dictionary = {
            "[----]": id_string,
            "DD/MM/YYYY": date_string,
            "[Customer Name]": customer_name,
            "[Bill]": "\n" + items,
            "[TTTTT.00]": total,
            "[DDDDD.00]": discount,
            "[NNNNN.00]": net_total,
            "[PPPPPPPPPPP]": payment_type,
        }

        def replace_string(paragraph, old_string, new_string):
            inline = paragraph.runs
            for i in range(len(inline)):
                if old_string in inline[i].text:
                    text = inline[i].text.replace(str(old_string), str(new_string))
                    inline[i].text = text

        for paragraph in document.paragraphs:
            for old_string, new_string in replacement_dictionary.items():
                if old_string in paragraph.text:
                    replace_string(paragraph, old_string, new_string)
        document.save("bill_output.docx")
        os.startfile("bill_output.docx", "print")

    def refresh_tab(self):
        self.bill_list_table.delete(*self.bill_list_table.get_children())
        self.bill_table.delete(*self.bill_table.get_children())
        bills = get_bills_by_date(date=self.current_date)
        if not bills:
            self.days_total.set(0.0)
            return None
        total = 0
        for bill in bills:
            self.bill_list_table.insert('', "end", values=bill)
            total += bill[2]
        self.days_total.set(total)
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

    def date_changed(self, day_increase: int):
        self.current_date = self.current_date + timedelta(days=day_increase)
        self.date_label["text"] = self.current_date
        self.refresh_tab()
