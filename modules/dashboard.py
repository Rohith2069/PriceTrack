import tkinter as tk
from tkinter import ttk
from ui.styles import *
from database.db_operations import get_dashboard_stats, get_recent_purchases

class DashboardPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_COLOR)
        self.setup_ui()
        self.load_dashboard_data()

    def setup_ui(self):
        # 1. Page Title
        title_lbl = tk.Label(self, text="Dashboard Overview", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR)
        title_lbl.pack(pady=(30, 15), anchor="w", padx=40)

        # 2. Summary Cards Frame (4 Cards)
        cards_frame = tk.Frame(self, bg=BG_COLOR)
        cards_frame.pack(fill=tk.X, padx=40, pady=(0, 25))

        self.total_products_var = tk.StringVar(value="0")
        self.total_purchases_var = tk.StringVar(value="0")
        self.monthly_spent_var = tk.StringVar(value="₹0.00")
        self.total_spent_var = tk.StringVar(value="₹0.00")

        self.create_stat_card(cards_frame, "Products Tracked", self.total_products_var, ACCENT_COLOR, 0)
        self.create_stat_card(cards_frame, "Total Purchases", self.total_purchases_var, SUCCESS_COLOR, 1)
        self.create_stat_card(cards_frame, "This Month's Spend", self.monthly_spent_var, "#D97706", 2)
        self.create_stat_card(cards_frame, "Total Spent", self.total_spent_var, DANGER_COLOR, 3)

        # 3. Recent Purchases Table
        recent_lbl = tk.Label(self, text="Recent Purchases", font=FONT_HEADING, bg=BG_COLOR, fg=TEXT_COLOR)
        recent_lbl.pack(pady=(5, 10), anchor="w", padx=40)

        table_frame = tk.Frame(self, bg=BG_COLOR)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 30))

        columns = ("date", "product", "shop", "total", "qty", "unit_price")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        self.tree.heading("date", text="Date")
        self.tree.heading("product", text="Product Name")
        self.tree.heading("shop", text="Shop")
        self.tree.heading("total", text="Total Price")
        self.tree.heading("qty", text="Quantity")
        self.tree.heading("unit_price", text="Normalized Price")

        self.tree.column("date", width=100, anchor="center")
        self.tree.column("product", width=200, anchor="w")
        self.tree.column("shop", width=150, anchor="w")
        self.tree.column("total", width=100, anchor="center")
        self.tree.column("qty", width=110, anchor="center")
        self.tree.column("unit_price", width=150, anchor="center")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_stat_card(self, parent, title, text_var, color, col):
        card = tk.Frame(parent, bg=CARD_BG, padx=16, pady=16, highlightbackground="#CBD5E1", highlightthickness=1)
        # Last card ki right padding avasaram ledu
        pad_right = 0 if col == 3 else 12
        card.grid(row=0, column=col, padx=(0, pad_right), sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)

        tk.Label(card, text=title, font=FONT_SMALL, bg=CARD_BG, fg=TEXT_MUTED).pack(anchor="w")
        tk.Label(card, textvariable=text_var, font=("Segoe UI", 18, "bold"), bg=CARD_BG, fg=color).pack(anchor="w", pady=(6, 0))

    def load_dashboard_data(self):
        # Update Cards
        total_products, total_purchases, total_spent, monthly_spent = get_dashboard_stats()
        self.total_products_var.set(str(total_products))
        self.total_purchases_var.set(str(total_purchases))
        self.monthly_spent_var.set(f"₹{monthly_spent:.2f}")
        self.total_spent_var.set(f"₹{total_spent:.2f}")

        # Update Recent Purchases Table
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = get_recent_purchases()
        for row in rows:
            p_date, p_name, shop, total, qty, unit, norm_price, base_unit = row
            self.tree.insert("", tk.END, values=(
                p_date,
                p_name,
                shop,
                f"₹{total:.2f}",
                f"{qty:g} {unit}",
                f"₹{norm_price:.2f} / {base_unit}"
            ))