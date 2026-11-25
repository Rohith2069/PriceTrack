import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ui.styles import *
from database.db_operations import get_all_products, delete_product_from_db

class ProductsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_COLOR)
        self.setup_ui()
        
    def setup_ui(self):
        # 1. Page Title
        title_lbl = tk.Label(self, text="Product Management", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR)
        title_lbl.pack(pady=(30, 10), anchor="w", padx=40)
        
        # 2. Search & Action Bar Section
        action_frame = tk.Frame(self, bg=BG_COLOR)
        action_frame.pack(fill=tk.X, padx=40, pady=5)
        
        # --- Left Side: Search ---
        tk.Label(action_frame, text="Search Product:", font=FONT_NORMAL, bg=BG_COLOR, fg=TEXT_COLOR).pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_entry = ttk.Entry(action_frame, font=FONT_NORMAL, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 15))
        
        search_btn = tk.Button(action_frame, text="Search", font=FONT_BOLD, bg=ACCENT_COLOR, fg="white", bd=0, cursor="hand2", padx=15, command=self.search_product)
        search_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = tk.Button(action_frame, text="Clear", font=FONT_BOLD, bg="#95A5A6", fg="white", bd=0, cursor="hand2", padx=15, command=self.clear_search)
        clear_btn.pack(side=tk.LEFT)

        # --- Right Side: Delete Button ---
        delete_btn = tk.Button(action_frame, text="Delete Selected", font=FONT_BOLD, bg=DANGER_COLOR, fg="white", bd=0, cursor="hand2", padx=15, command=self.delete_product)
        delete_btn.pack(side=tk.RIGHT)

        # Instruction/Hint Label
        hint_lbl = tk.Label(self, text="💡 Hint: Select a product from the table below, then click 'Delete Selected'", font=("Segoe UI", 10, "italic"), bg=BG_COLOR, fg=TEXT_MUTED)
        hint_lbl.pack(anchor="e", padx=40, pady=(0, 10))

        # 3. Products Table (Treeview)
        table_frame = tk.Frame(self, bg=BG_COLOR)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 30))

        columns = ("id", "name", "category", "base_unit", "total_purchases")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Product Name")
        self.tree.heading("category", text="Category")
        self.tree.heading("base_unit", text="Base Unit")
        self.tree.heading("total_purchases", text="Times Purchased")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=250, anchor="w")
        self.tree.column("category", width=150, anchor="w")
        self.tree.column("base_unit", width=100, anchor="center")
        self.tree.column("total_purchases", width=120, anchor="center")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load Real Data from SQLite
        self.load_products()

    def load_products(self, query=""):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        rows = get_all_products(query)
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def search_product(self):
        query = self.search_entry.get().strip()
        self.load_products(query)

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.load_products()
        
    def delete_product(self):
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a product from the table to delete!")
            return
            
        confirm = messagebox.askyesno(
            "Confirm Delete", 
            "Are you sure you want to delete this product?\n\nWARNING: This will also delete all purchase history related to this product!"
        )
        
        if confirm:
            for item in selected_item:
                product_data = self.tree.item(item, "values")
                product_id = product_data[0]
                
                success, msg = delete_product_from_db(product_id)
                if success:
                    self.tree.delete(item)
                    messagebox.showinfo("Success", msg)
                else:
                    messagebox.showerror("Error", msg)