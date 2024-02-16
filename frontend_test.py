import tkinter as tk
from tkinter import ttk
import sv_ttk


root = tk.Tk()

frame = ttk.Frame(root)
frame.pack()

header_frame = ttk.LabelFrame(frame, text="Header")
header_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

title_label = ttk.Label(header_frame, text="Main Window")
title_label.grid(row=0, column=0, sticky="ew")

subtitle_label = ttk.Label(header_frame, text="Subtitle")
subtitle_label.grid(row=1, column=0, sticky="ew")


body_frame = ttk.LabelFrame(frame, text="Body")
body_frame.grid(row=1, column=0, padx=20, pady=10)

name_entry = ttk.Entry(body_frame)
name_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="ew")
name_entry.insert(0, "Name")
name_entry.bind("<FocusIn>", lambda _: name_entry.delete('0', 'end') if name_entry.get() == "Name" else None)

age_spinbox = ttk.Spinbox(body_frame, from_=18, to=100)
age_spinbox.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
age_spinbox.insert(0, "Age")
age_spinbox.bind("<FocusIn>", lambda _: age_spinbox.set(18) if age_spinbox.get() == "Age" else None)

status_combobox = ttk.Combobox(body_frame, values=["Not Started", "Incomplete", "Complete"])
status_combobox.current(0)
status_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

is_enabled = tk.BooleanVar()
check_button = ttk.Checkbutton(body_frame, text="Enabled", variable=is_enabled)
check_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

button = ttk.Button(body_frame, text="Submit")
button.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

separator = ttk.Separator(body_frame)
separator.grid(row=4, column=0, columnspan=2, padx=(20, 10), pady=10, sticky="ew")


sv_ttk.set_theme("dark")
root.mainloop()
