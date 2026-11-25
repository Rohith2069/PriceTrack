import tkinter as tk
from ui.styles import *

# Modules
from modules.dashboard import DashboardPage
from modules.add_purchase import AddPurchasePage
from modules.products import ProductsPage
from modules.comparison import PriceComparisonPage
from modules.history import HistoryPage
from database.db_connection import initialize_database

class PriceTrackApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Window Setup
        self.title("PriceTrack - Smart Price Comparison System")
        self.geometry("1150x700")
        self.minsize(1000, 600)
        self.configure(bg=BG_COLOR)
        
        # Apply the global theme from styles.py
        setup_global_theme(self)
        
        # Sidebar state memory
        self.sidebar_btns = {}
        self.current_page = None

        self.setup_ui()

    def setup_ui(self):
        # 1. Main Container
        self.main_container = tk.Frame(self, bg=BG_COLOR)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # 2. Sidebar Frame
        self.sidebar_frame = tk.Frame(self.main_container, bg=SIDEBAR_BG, width=220)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False) 

        # Logo
        title_lbl = tk.Label(self.sidebar_frame, text="PriceTrack", font=FONT_LOGO, bg=SIDEBAR_BG, fg=SIDEBAR_FG, pady=30)
        title_lbl.pack(fill=tk.X)

        # 3. Content Area
        self.content_frame = tk.Frame(self.main_container, bg=BG_COLOR)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_sidebar_buttons()
        self.show_page("Dashboard") # Load default

    def create_sidebar_buttons(self):
        menu_items = ["Dashboard", "Add Purchase", "Products", "Price Comparison", "History"]
        
        for item in menu_items:
            btn = tk.Button(
                self.sidebar_frame, 
                text=item,
                font=FONT_NORMAL,
                bg=SIDEBAR_BG,
                fg=SIDEBAR_FG,
                bd=0,
                activebackground=SIDEBAR_ACTIVE,
                activeforeground=SIDEBAR_FG,
                cursor="hand2",
                pady=10,
                command=lambda p=item: self.show_page(p)
            )
            btn.pack(fill=tk.X, pady=2, padx=10)
            
            # Hover Animations bindings
            btn.bind("<Enter>", lambda e, b=btn, p=item: self.on_hover(b, p))
            btn.bind("<Leave>", lambda e, b=btn, p=item: self.on_leave(b, p))
            
            self.sidebar_btns[item] = btn

    def on_hover(self, btn, page_name):
        # Don't change color if it's the currently active page
        if self.current_page != page_name:
            btn.configure(bg=SIDEBAR_HOVER)

    def on_leave(self, btn, page_name):
        # Don't change color if it's the currently active page
        if self.current_page != page_name:
            btn.configure(bg=SIDEBAR_BG)

    def highlight_active_button(self, page_name):
        self.current_page = page_name
        for name, btn in self.sidebar_btns.items():
            if name == page_name:
                btn.configure(bg=SIDEBAR_ACTIVE, font=FONT_BOLD) # Active style
            else:
                btn.configure(bg=SIDEBAR_BG, font=FONT_NORMAL)   # Normal style

    def show_page(self, page_name):
        # Highlight sidebar button
        self.highlight_active_button(page_name)

        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Route to proper module
        if page_name == "Dashboard":
            page = DashboardPage(self.content_frame)
        elif page_name == "Add Purchase":
            page = AddPurchasePage(self.content_frame)
        elif page_name == "Products":
            page = ProductsPage(self.content_frame)
        elif page_name == "Price Comparison":
            page = PriceComparisonPage(self.content_frame)
        elif page_name == "History":
            page = HistoryPage(self.content_frame)
        else:
            return
            
        page.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = PriceTrackApp()
    app.mainloop()