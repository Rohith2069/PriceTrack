import tkinter as tk
from tkinter import ttk
from ui.styles import *
from database.db_operations import get_product_names, get_price_comparison

# Matplotlib imports
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PriceComparisonPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_COLOR)
        self.setup_ui()
        
    def setup_ui(self):
        # 1. Page Title
        title_lbl = tk.Label(self, text="Smart Price Comparison", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR)
        title_lbl.pack(pady=(20, 5), anchor="w", padx=40)
        
        # 2. Product Selection Section
        select_frame = tk.Frame(self, bg=BG_COLOR)
        select_frame.pack(fill=tk.X, padx=40, pady=5)
        
        tk.Label(select_frame, text="Select Product to Compare:", font=FONT_NORMAL, bg=BG_COLOR, fg=TEXT_COLOR).pack(side=tk.LEFT, padx=(0, 10))
        
        # Real products list from SQLite
        products_list = get_product_names()
        self.combo_product = ttk.Combobox(select_frame, values=products_list, state="readonly", font=FONT_NORMAL, width=30)
        if products_list:
            self.combo_product.set(products_list[0])
        self.combo_product.pack(side=tk.LEFT, padx=(0, 15))
        
        compare_btn = tk.Button(select_frame, text="Analyze & Compare", font=FONT_BOLD, bg=ACCENT_COLOR, fg="white", bd=0, cursor="hand2", padx=15, command=self.analyze_prices)
        compare_btn.pack(side=tk.LEFT)

        # 3. Summary Cards Section
        self.cards_frame = tk.Frame(self, bg=BG_COLOR)
        self.cards_frame.pack(fill=tk.X, padx=40, pady=10)
        
        self.best_shop_var = tk.StringVar(value="--")
        self.best_price_var = tk.StringVar(value="--")
        self.worst_shop_var = tk.StringVar(value="--")
        
        self.create_summary_card(self.cards_frame, "Cheapest Shop (Best)", self.best_shop_var, SUCCESS_COLOR, 0)
        self.create_summary_card(self.cards_frame, "Lowest Unit Price", self.best_price_var, ACCENT_COLOR, 1)
        self.create_summary_card(self.cards_frame, "Most Expensive Shop", self.worst_shop_var, DANGER_COLOR, 2)

        # Content Splitter: Table (Top) and Chart (Bottom)
        content_frame = tk.Frame(self, bg=BG_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 20))

        # 4. Comparison Table
        table_lbl = tk.Label(content_frame, text="Shop Rankings (Based on Unit Price)", font=FONT_HEADING, bg=BG_COLOR, fg=TEXT_COLOR)
        table_lbl.pack(pady=(5, 5), anchor="w")

        table_frame = tk.Frame(content_frame, bg=BG_COLOR)
        table_frame.pack(fill=tk.X, pady=(0, 10))

        columns = ("rank", "shop", "qty", "total", "unit_price")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=4) 
        
        self.tree.heading("rank", text="Rank")
        self.tree.heading("shop", text="Shop Name")
        self.tree.heading("qty", text="Quantity Bought")
        self.tree.heading("total", text="Total Price Paid")
        self.tree.heading("unit_price", text="Normalized Unit Price")

        self.tree.column("rank", width=80, anchor="center")
        self.tree.column("shop", width=220, anchor="w")
        self.tree.column("qty", width=120, anchor="center")
        self.tree.column("total", width=120, anchor="center")
        self.tree.column("unit_price", width=200, anchor="center")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 5. Chart Frame
        self.chart_frame = tk.Frame(content_frame, bg=BG_COLOR)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)

        # Load initial comparison if products exist
        if products_list:
            self.analyze_prices()

    def create_summary_card(self, parent, title, text_var, color, col):
        card = tk.Frame(parent, bg=CARD_BG, padx=10, pady=10, highlightbackground="#CBD5E1", highlightthickness=1)
        card.grid(row=0, column=col, padx=(0, 10), sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)

        tk.Label(card, text=title, font=("Segoe UI", 11), bg=CARD_BG, fg=TEXT_MUTED).pack(anchor="center")
        tk.Label(card, textvariable=text_var, font=("Segoe UI", 15, "bold"), bg=CARD_BG, fg=color).pack(anchor="center", pady=(5, 0))

    def analyze_prices(self):
        product = self.combo_product.get().strip()
        
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if not product:
            return

        rows = get_price_comparison(product)
        
        if not rows:
            self.best_shop_var.set("N/A")
            self.best_price_var.set("N/A")
            self.worst_shop_var.set("N/A")
            self.draw_chart([], [])
            return

        # Rows are already sorted ASC by normalized_price
        best = rows[0]
        worst = rows[-1]

        self.best_shop_var.set(best[0])
        self.best_price_var.set(f"₹{best[4]:.2f} / {best[5]}")
        self.worst_shop_var.set(f"{worst[0]} (₹{worst[4]:.2f}/{worst[5]})")

        shop_names = []
        unit_prices = []

        for idx, row in enumerate(rows, start=1):
            shop, qty, unit, total, norm_price, base_unit = row
            
            # Add badges for Best and Worst (if more than 1 entry)
            display_shop = shop
            if idx == 1:
                display_shop = f"{shop}  🏆 (Best)"
            elif idx == len(rows) and len(rows) > 1:
                display_shop = f"{shop}  ⚠️ (Worst)"

            self.tree.insert("", tk.END, values=(
                str(idx),
                display_shop,
                f"{qty:g} {unit}",
                f"₹{total:.2f}",
                f"₹{norm_price:.2f} / {base_unit}"
            ))

            shop_names.append(shop)
            unit_prices.append(norm_price)

        self.draw_chart(shop_names, unit_prices)

    def draw_chart(self, shops, prices):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        if not shops:
            return

        fig = Figure(figsize=(8, 3), dpi=100)
        fig.patch.set_facecolor(BG_COLOR)

        ax = fig.add_subplot(111)
        ax.set_facecolor(CARD_BG)
        
        bars = ax.bar(shops, prices, color=ACCENT_COLOR, width=0.4)

        ax.set_title("Unit Price Trend across Shops (Lower is Better)", fontsize=10, color=TEXT_COLOR)
        ax.set_ylabel("Normalized Price (₹)", fontsize=9, color=TEXT_COLOR)
        
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + (max(prices) * 0.02), f'₹{yval:.2f}', ha='center', va='bottom', fontsize=9, color=TEXT_COLOR, fontweight="bold")

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)