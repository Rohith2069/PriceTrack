import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from ui.styles import *
from database.db_operations import add_purchase_to_db

class AddPurchasePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_COLOR)
        self.setup_ui()

    def setup_ui(self):
        # Page Title
        title_lbl = tk.Label(self, text="Add New Purchase", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR)
        title_lbl.pack(pady=(30, 15), anchor="w", padx=40)

        # Card Container
        form_card = tk.Frame(self, bg=CARD_BG, padx=35, pady=30, highlightbackground="#CBD5E1", highlightthickness=1)
        form_card.pack(fill=tk.X, padx=40, pady=10)

        # Form Fields
        fields = [
            ("Product Name:", "entry_product"),
            ("Category:", "combo_category"),
            ("Shop Name:", "entry_shop"),
            ("Total Price (₹):", "entry_price"),
            ("Quantity:", "entry_qty"),
            ("Unit:", "combo_unit"),
            ("Purchase Date (YYYY-MM-DD):", "entry_date")
        ]

        for idx, (label_text, attr_name) in enumerate(fields):
            tk.Label(form_card, text=label_text, font=FONT_BOLD, bg=CARD_BG, fg=TEXT_COLOR).grid(
                row=idx, column=0, sticky="w", pady=10, padx=(0, 20)
            )

            if attr_name == "combo_category":
                widget = ttk.Combobox(
                    form_card,
                    values=["Groceries", "Beverages", "Dairy", "Personal Care", "Household", "Other"],
                    state="readonly",
                    font=FONT_NORMAL,
                    width=33
                )
                widget.set("Groceries")
            elif attr_name == "combo_unit":
                widget = ttk.Combobox(
                    form_card,
                    values=["kg", "g", "L", "ml", "piece"],
                    state="readonly",
                    font=FONT_NORMAL,
                    width=33
                )
                widget.set("kg")
            else:
                widget = ttk.Entry(form_card, font=FONT_NORMAL, width=35)
                if attr_name == "entry_date":
                    widget.insert(0, str(date.today()))

            widget.grid(row=idx, column=1, sticky="w", pady=10)
            setattr(self, attr_name, widget)

        # Save Button
        save_btn = tk.Button(
            form_card,
            text="Save Purchase",
            font=FONT_BOLD,
            bg=ACCENT_COLOR,
            fg="white",
            bd=0,
            cursor="hand2",
            padx=25,
            pady=10,
            command=self.save_purchase
        )
        save_btn.grid(row=len(fields), column=1, sticky="w", pady=(20, 0))

    def save_purchase(self):
        product = self.entry_product.get().strip()
        category = self.combo_category.get().strip()
        shop = self.entry_shop.get().strip()
        price_str = self.entry_price.get().strip()
        qty_str = self.entry_qty.get().strip()
        unit = self.combo_unit.get().strip()
        p_date = self.entry_date.get().strip()

        # Validation
        if not all([product, shop, price_str, qty_str, p_date]):
            messagebox.showwarning("Missing Info", "Please fill in all fields!")
            return

        try:
            price = float(price_str)
            qty = float(qty_str)
            if price <= 0 or qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Price and Quantity must be positive numbers!")
            return

        # Save to SQLite Database
        success, msg = add_purchase_to_db(product, category, shop, price, qty, unit, p_date)

        if success:
            messagebox.showinfo("Success", msg)
            # Clear inputs for next entry
            self.entry_product.delete(0, tk.END)
            self.entry_shop.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)
            self.entry_qty.delete(0, tk.END)
        else:
            messagebox.showerror("Error", msg)