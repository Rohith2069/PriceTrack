import tkinter as tk
from tkinter import ttk
from ui.styles import *
from database.db_operations import get_purchase_history

class HistoryPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_COLOR)
        self.setup_ui()
        
    def setup_ui(self):
        # 1. Page Title
        title_lbl = tk.Label(self, text="Purchase History", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR)
        title_lbl.pack(pady=(30, 10), anchor="w", padx=40)
        
        # 2. Filters Section (Product and Shop fields)
        filter_frame = tk.Frame(self, bg=BG_COLOR)
        filter_frame.pack(fill=tk.X, padx=40, pady=10)
        
        # Product Filter
        tk.Label(filter_frame, text="Filter by Product:", font=FONT_NORMAL, bg=BG_COLOR, fg=TEXT_COLOR).pack(side=tk.LEFT, padx=(0, 5))
        self.filter_product = ttk.Entry(filter_frame, font=FONT_NORMAL, width=20)
        self.filter_product.pack(side=tk.LEFT, padx=(0, 20))
        
        # Shop Filter
        tk.Label(filter_frame, text="Filter by Shop:", font=FONT_NORMAL, bg=BG_COLOR, fg=TEXT_COLOR).pack(side=tk.LEFT, padx=(0, 5))
        self.filter_shop = ttk.Entry(filter_frame, font=FONT_NORMAL, width=20)
        self.filter_shop.pack(side=tk.LEFT, padx=(0, 20))
        
        # Filter Action Buttons
        filter_btn = tk.Button(filter_frame, text="Apply Filters", font=FONT_BOLD, bg=ACCENT_COLOR, fg="white", bd=0, cursor="hand2", padx=15, command=self.apply_filters)
        filter_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = tk.Button(filter_frame, text="Clear", font=FONT_BOLD, bg="#95A5A6", fg="white", bd=0, cursor="hand2", padx=15, command=self.clear_filters)
        clear_btn.pack(side=tk.LEFT)

        # 3. History Table (Treeview)
        table_frame = tk.Frame(self, bg=BG_COLOR)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(10, 30))

        columns = ("date", "product", "shop", "total", "qty", "unit_price")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("date", text="Date")
        self.tree.heading("product", text="Product Name")
        self.tree.heading("shop", text="Shop")
        self.tree.heading("total", text="Total Price")
        self.tree.heading("qty", text="Quantity & Unit")
        self.tree.heading("unit_price", text="Normalized Unit Price")

        self.tree.column("date", width=100, anchor="center")
        self.tree.column("product", width=200, anchor="w")
        self.tree.column("shop", width=150, anchor="w")
        self.tree.column("total", width=100, anchor="center")
        self.tree.column("qty", width=120, anchor="center")
        self.tree.column("unit_price", width=150, anchor="center")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load Real Data from SQLite
        self.load_history()

    def load_history(self, prod_query="", shop_query=""):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        rows = get_purchase_history(prod_query, shop_query)
        for row in rows:
            p_date, p_name, shop, total, qty, unit, norm_price, base_unit = row
            formatted_row = (
                p_date,
                p_name,
                shop,
                f"₹{total:.2f}",
                f"{qty:g} {unit}",
                f"₹{norm_price:.2f} / {base_unit}"
            )
            self.tree.insert("", tk.END, values=formatted_row)

    def apply_filters(self):
        prod_query = self.filter_product.get().strip()
        shop_query = self.filter_shop.get().strip()
        self.load_history(prod_query, shop_query)
        
    def clear_filters(self):
        self.filter_product.delete(0, tk.END)
        self.filter_shop.delete(0, tk.END)
        self.load_history()