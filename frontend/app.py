import customtkinter as ctk
import tkinter as tk
import random
import os
from PIL import Image

from constants import (
    BG_APP, BG_PANEL, BG_CARD, BG_INPUT,
    ACCENT_BLUE, ACCENT_BRIGHT, BORDER_COLOR, BORDER_BRIGHT,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    COLOR_PIVOT, COLOR_COMPARE, COLOR_SWAP, COLOR_SORTED, COLOR_UNSORTED,
    FONT_TITLE, FONT_LABEL, FONT_SMALL, FONT_MONO, FONT_HEADER, FONT_CTRL,
    card_frame
)
from ui.panels import LeftPanel, CenterPanel, RightPanel, section_title, start_row


class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("QuickSort Application")
        self.geometry("1500x850")
        self.minsize(1200, 700)
        self.configure(fg_color=BG_APP)
        self.resizable(False, False)
        
        # Build layout and panels
        self.build_layout()
        self.header()      
        self.build_left_panel()
        self.build_center_panel()
        self.build_right_panel()
    
    def build_layout(self):
        self.grid_columnconfigure(0, weight=0, minsize=260)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0, minsize=280)
        self.grid_rowconfigure(1, weight=1) 
        
    def header(self):
        header_frame = ctk.CTkFrame(self, height=52, fg_color=BG_PANEL, corner_radius=0, border_width=1, border_color=BORDER_COLOR)
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)
        
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo1.png")
        try:
            logo_img = ctk.CTkImage(Image.open(logo_path), size=(36, 26))
            ctk.CTkLabel(header_frame, image=logo_img, text="").grid(row=0, column=0, padx=(14, 4), pady=12)
        except Exception:
            pass
        
        ctk.CTkLabel(header_frame, text="QUICKSORT APPLICATION", font=FONT_HEADER, text_color=TEXT_PRIMARY).grid(row=0, column=1, sticky="w", padx=8)
        
        btn_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=2, padx=12, sticky="e")
        
        for label, cmd in [("Help", self.open_help), ("About", self.open_about)]:
            ctk.CTkButton(btn_frame, text=label, width=70, height=28, font=FONT_SMALL, fg_color=ACCENT_BLUE, hover_color=ACCENT_BRIGHT, text_color=TEXT_PRIMARY, corner_radius=6, command=cmd).pack(side="left", padx=4)
    
    def open_help(self):
        help_section = self.dialog("Help", "500x420")
        self.dialog_header(help_section, "QuickSort Help")
        
        body = ctk.CTkFrame(help_section, fg_color=BG_PANEL, corner_radius=10)
        body.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        
        sections = [
            ("How to use",
             "1. Enter numbers manually, or click Random.\n"
             "2. Choose a pivot strategy.\n"
             "3. Press Start — or use Step to go one step at a time.\n"
             "4. Watch the Explanation Log for step-by-step reasoning."),
            ("Tips for better visualization",
             "• Use 5–15 elements for clear animations.\n"
             "• Try different pivots on the same array to compare.\n"
             "• Slow the speed down to follow the recursion tree."),
        ]
        
        for heading, text in sections:
            ctk.CTkLabel(body, text=heading, font=FONT_LABEL, text_color=ACCENT_BRIGHT).pack(anchor="w", padx=16, pady=(12, 4))
            ctk.CTkLabel(body, text=text, justify="left", font=FONT_SMALL, text_color=TEXT_PRIMARY, wraplength=440).pack(anchor="w", padx=24)
            
        ctk.CTkButton(help_section, text="Close", fg_color=ACCENT_BLUE, hover_color=ACCENT_BRIGHT, corner_radius=6, command=help_section.destroy).pack(pady=12)
    
    def open_about(self):
        about_section = self.dialog("About", "400x300")
        self.dialog_header(about_section, "About this app")
        
        body = ctk.CTkFrame(about_section, fg_color=BG_PANEL, corner_radius=10)
        body.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        
        about_text = (
            "QuickSort Visualizer\n\n"
            "Visualizes the QuickSort algorithm step-by-step,\n"
            "including pivot selection, comparisons, swaps,\n"
            "and the recursion tree."
        )
        
        ctk.CTkLabel(body, text=about_text, justify="center", font=FONT_SMALL, text_color=TEXT_PRIMARY).pack(expand=True, pady=20)
        
        ctk.CTkButton(about_section, text="Close", fg_color=ACCENT_BLUE, hover_color=ACCENT_BLUE, corner_radius=6, command=about_section.destroy).pack(pady=12)
    
    def build_left_panel(self):
        self.left = ctk.CTkScrollableFrame(self, fg_color="transparent", scrollbar_button_color=BORDER_COLOR)
        self.left.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=10)
        
        LeftPanel(self).build()
    
    def build_center_panel(self):
        self.center = ctk.CTkFrame(self, fg_color="transparent")
        self.center.grid(row=1, column=1, sticky="nsew", padx=5, pady=10)
        self.center.grid_rowconfigure(1, weight=1)
        self.center.grid_rowconfigure(2, weight=0)
        self.center.grid_rowconfigure(3, weight=0)
        self.center.grid_columnconfigure(0, weight=1)
        
        CenterPanel(self).build()
    
    def build_right_panel(self):
        self.right = ctk.CTkFrame(self, fg_color="transparent")
        self.right.grid(row=1, column=2, sticky="nsew", padx=(5, 10), pady=10)
        self.right.grid_rowconfigure(0, weight=1)
        self.right.grid_rowconfigure(1, weight=0)
        self.right.grid_rowconfigure(2, weight=0)
        self.right.grid_columnconfigure(0, weight=1)
        
        RightPanel(self).build()
    
    # Action methods
    def random_input(self):
        nums = random.sample(range(1, 100), random.randint(6, 10))
        self.array_entry.delete("1.0", "end")
        self.array_entry.insert("end", ", ".join(map(str, nums)))
        
    def generate_array(self):
        pass
    
    def start_sort(self):
        pass
    
    def pause_sort(self):
        pass
    
    def step_sort(self):
        pass
    
    def reset_sort(self):
        pass
    
    def show_pivot_help(self):
        window = self.dialog("Pivot Selection Help", "400x250")
        self.dialog_header(window, "Pivot Selection Strategies")
        
        body = ctk.CTkFrame(window, fg_color=BG_PANEL, corner_radius=10)
        body.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        text = (
            "First element:  Always picks arr[lo] as pivot.\n"
            "  → Worst case O(n²) on sorted arrays.\n\n"
            "Last element:   Always picks arr[hi] as pivot.\n"
            "  → Same worst-case risk as First.\n\n"
            "Random element: Picks a random index each time.\n"
            "  → Avoids worst-case on nearly-sorted data.\n"
            "  → Expected O(n log n) performance."
        )
        ctk.CTkLabel(body, text=text, justify="left", font=FONT_SMALL, text_color=TEXT_PRIMARY, wraplength=370).pack(padx=16, pady=12)
        ctk.CTkButton(window, text="Close", fg_color=ACCENT_BLUE, hover_color=ACCENT_BRIGHT, corner_radius=6, command=window.destroy).pack(pady=12)
    
    # Status and logging
    def update_status(self, text, color=TEXT_PRIMARY):
        self.status_var.set(text)
        self.status_label.configure(text_color=color)
    
    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
    
    def clear_log(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")
    
    def focus_entry(self):
        self.array_entry.delete("1.0", "end")
        self.array_entry.focus_set()
        
    def on_speed_change(self, val):
        label = f"{float(val):.2f}"
        self.speed_val_label.configure(text=label)
    
    # Dialog helpers
    def dialog(self, title, geometry):
        window = ctk.CTkToplevel(self)
        window.title(title)
        window.geometry(geometry)
        window.configure(fg_color=BG_APP)
        window.resizable(False, False)
        window.after(100, lambda: (window.lift(), window.focus_force(), window.grab_set()))
        return window
    
    def dialog_header(self, parent, text):
        frame = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=10)
        frame.pack(fill="x", padx=14, pady=14)
        ctk.CTkLabel(frame, text=text, font=FONT_HEADER, text_color=TEXT_PRIMARY).pack(pady=12)