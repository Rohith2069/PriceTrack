import tkinter as tk
from tkinter import ttk

# ==========================================
# 💎 PREMIUM THEME: Deep Space & Vibrant Rose
# ==========================================

# Global Colors
BG_COLOR = "#F4F7F9"        # Soft pearl white for main background
CARD_BG = "#FFFFFF"         # Pure white for cards to pop
TEXT_COLOR = "#0B1221"      # Deepest navy for text (softer than harsh black)
TEXT_MUTED = "#64748B"      # Premium slate-gray for hints

# Sidebar Colors (The Rich Dark Look)
SIDEBAR_BG = "#0A0F1D"      # Deep Space Blue (Ultra-dark, rich)
SIDEBAR_FG = "#E2E8F0"      # Crisp silver-white text
SIDEBAR_HOVER = "#1A243D"   # Lighter rich blue for mouse hover
SIDEBAR_ACTIVE = "#E11D48"  # Vibrant Rose / Crimson (Stunning highlight)

# Action Colors
ACCENT_COLOR = "#4F46E5"    # Electric Indigo for Main Buttons (Save, Analyze)
SUCCESS_COLOR = "#059669"   # Rich Emerald Green (For Cheapest/Savings)
DANGER_COLOR = "#E11D48"    # Vibrant Rose Red (For Expensive/Delete)

# Modern Professional Fonts
FONT_LOGO = ("Segoe UI", 24, "bold")
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_HEADING = ("Segoe UI", 15, "bold")
FONT_NORMAL = ("Segoe UI", 11)
FONT_BOLD = ("Segoe UI", 11, "bold")
FONT_SMALL = ("Segoe UI", 10)

def setup_global_theme(root):
    """Applies premium rich styling to all ttk widgets in the app"""
    style = ttk.Style(root)
    
    # Use 'clam' as base because it allows deep customization without Windows overriding it
    style.theme_use('clam')
    
    # 1. Premium Table (Treeview) Styling
    style.configure(
        "Treeview", 
        background=CARD_BG, 
        foreground=TEXT_COLOR, 
        rowheight=38,           # More breathing room between rows
        fieldbackground=CARD_BG, 
        font=FONT_NORMAL, 
        borderwidth=0
    )
    # Table Headings
    style.configure(
        "Treeview.Heading", 
        font=FONT_BOLD, 
        background="#E2E8F0",   # Soft silver header
        foreground="#0A0F1D",   # Dark text for header
        padding=10,
        borderwidth=0
    )
    # Selected Row in Table
    style.map(
        "Treeview", 
        background=[("selected", ACCENT_COLOR)], 
        foreground=[("selected", "white")]
    )
    
    # 2. Modern Inputs (Entry & Combobox)
    style.configure(
        "TEntry", 
        padding=8, 
        font=FONT_NORMAL,
        fieldbackground="white",
        bordercolor="#CBD5E1",
        lightcolor="#CBD5E1",
        darkcolor="#CBD5E1"
    )
    
    style.configure(
        "TCombobox", 
        padding=8, 
        font=FONT_NORMAL,
        bordercolor="#CBD5E1"
    )