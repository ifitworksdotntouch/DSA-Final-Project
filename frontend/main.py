import customtkinter as ctk
import tkinter as tk
import random
import requests # type: ignore
from PIL import Image
import os

BG_APP = "#0a0f1a"
BG_PANEL = "#0f1c2e"
BG_CARD = "#132338"
BG_INPUT = "#0d1a2b"
ACCENT_BLUE = "#1a6fbd"
ACCENT_BRIGHT = "#2196f3"
BORDER_COLOR = "#1e3a5f"
BORDER_BRIGHT = "#2a5080"

TEXT_PRIMARY = "#e8f4ff"
TEXT_SECONDARY = "#7aa8cc"
TEXT_MUTED = "#3d6080"

COLOR_PIVOT = "#ff4757"
COLOR_COMPARE = "#ffa502"
COLOR_SWAP = "#2ed573"
COLOR_SORTED = "#1e90ff"
COLOR_UNSORTED = "#2a4a6b"

FONT_TITLE = ("Consolas", 13, "bold")
FONT_LABEL = ("Consolas", 11, "bold")
FONT_SMALL = ("Consolas", 10)
FONT_MONO = ("Consolas", 11)
FONT_HEADER = ("Consolas", 15, "bold")
FONT_CTRL = ("Consolas", 12, "bold")

def card_frame(parent, **kwargs):
    defaults = dict(corner_radius=8, border_width=1, border_color=BORDER_COLOR, fg_color=BG_CARD)
    defaults.update(kwargs)
    return ctk.CTkFrame(parent, **defaults)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("QuickSort Application")
        self.geometry("1500x850")
        self.minsize(1200, 700)
        self.configure(fg_color=BG_APP)
        self.resizable(False, False)
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
            ctk.CTkLabel(header_frame, image=logo_img, text="").grid(row = 0, column= 0, padx=(14, 4), pady=12)
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
        
        self.input_section()
        self.build_pivot_section()
        self.build_speed_section()
        self.build_legend_section()
        self.build_status_section()
        
    def input_section(self):
        input_frame = card_frame(self.left)
        input_frame.pack(fill="x", pady=(0, 8)) 
        
        self.section_title(input_frame, "INPUT ARRAY")
        
        btn_row = ctk.CTkFrame(input_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=10, pady=(0, 6))
        
        ctk.CTkButton(btn_row, text="Manual", width=108, height=30, font=FONT_SMALL, fg_color=ACCENT_BLUE, hover_color=ACCENT_BRIGHT, corner_radius=6, command=self.focus_entry).pack(side="left", padx=(0, 6))
        ctk.CTkButton(btn_row, text="Random", width=108, height=30, font=FONT_SMALL, fg_color=ACCENT_BLUE, hover_color=ACCENT_BRIGHT, corner_radius=6, command=self.random_input).pack(side="left")
        
        self.array_entry = ctk.CTkTextbox(input_frame, height=48, fg_color=BG_INPUT, text_color=TEXT_PRIMARY, border_color=BORDER_BRIGHT, border_width=1, corner_radius=6, font=FONT_MONO, wrap="word")
        self.array_entry.pack(fill="x", padx=10, pady=(0, 6))
        
        ctk.CTkButton(input_frame, text="Generate Array", height=32, font=FONT_LABEL, fg_color=ACCENT_BLUE, hover_color=ACCENT_BRIGHT, corner_radius=6, border_width=1, border_color=BORDER_BRIGHT, command=self.generate_array).pack(fill="x", padx=10, pady=(0, 10))
    def build_pivot_section(self):
        pivot_frame = card_frame(self.left)
        pivot_frame.pack(fill="x", pady=(0, 8))
        
        header = ctk.CTkFrame(pivot_frame, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(10, 4))
        header.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(header, text="PIVOT SELECTION", font=FONT_TITLE, text_color=TEXT_PRIMARY).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(header, text="?", width=22, height=22, font=FONT_SMALL, fg_color=ACCENT_BLUE, hover_color=ACCENT_BRIGHT, corner_radius=11, command=self.show_pivot_help).grid(row=0, column=1, sticky="e")
        
        self.pivot_var = ctk.StringVar(value="last")
        
        for value, label in [("first", "First element"),
                             ("last", "Last element"),
                             ("random", "Random element")]:
            ctk.CTkRadioButton(pivot_frame, text=label, value=value, variable=self.pivot_var, font=FONT_SMALL, text_color=TEXT_PRIMARY, fg_color=ACCENT_BRIGHT, hover_color=ACCENT_BLUE).pack(anchor="w", padx=14, pady=3)
        ctk.CTkFrame(pivot_frame, height=10, fg_color="transparent").pack()
        
    def build_speed_section(self):
        speed_frame = card_frame(self.left)
        speed_frame.pack(fill="x", pady=(0, 8))
        
        self.section_title(speed_frame, "ANIMATION SPEED")
        
        self.speed_var = ctk.DoubleVar(value=1.0)
        
        self.speed_val_label = ctk.CTkLabel(speed_frame, text="1.0×", font=FONT_LABEL, text_color=ACCENT_BRIGHT)
        self.speed_val_label.pack()
        
        slider = ctk.CTkSlider(speed_frame, from_=0.25, to=3.0, variable=self.speed_var, number_of_steps=11, progress_color=ACCENT_BLUE, button_color=ACCENT_BRIGHT, command=self.on_speed_change)
        slider.pack(fill="x", padx=16, pady=(2, 4))
        
        row = ctk.CTkFrame(speed_frame, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=(0, 10))
        for txt, side in [("Slow", "left"), ("Fast", "right")]:
            ctk.CTkLabel(row, text=txt, font=FONT_SMALL, text_color=TEXT_SECONDARY).pack(side=side)
              
    def build_legend_section(self):
        legend_frame = card_frame(self.left)
        legend_frame.pack(fill="x", pady=(0, 8))
        
        self.section_title(legend_frame, "LEGEND")
        
        for color, label in [
            (COLOR_PIVOT,    "Pivot"),
            (COLOR_COMPARE,  "Comparing"),
            (COLOR_SWAP,     "Swapping"),
            (COLOR_SORTED,   "Sorted"),
            (COLOR_UNSORTED, "Unsorted"),
        ]:
            row=  ctk.CTkFrame(legend_frame, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=3)
            
            ctk.CTkLabel(row, text="", width=18, height=18, fg_color=color, corner_radius=3).pack(side="left")
            ctk.CTkLabel(row, text=label, font=FONT_SMALL, text_color=TEXT_PRIMARY).pack(side="left", padx=10)
        
        ctk.CTkFrame(legend_frame, height=6, fg_color="transparent").pack()
    
    def build_status_section(self):
        status_frame = card_frame(self.left)
        status_frame.pack(fill="x", pady=(0, 8))
        
        row = ctk.CTkFrame(status_frame, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=10)
        
        ctk.CTkLabel(row, text="STATUS", font=FONT_LABEL, text_color=TEXT_SECONDARY).pack(side="left")
        
        self.status_var = ctk.StringVar(value="Idle")
        self.status_label = ctk.CTkLabel(row, textvariable=self.status_var, font=FONT_LABEL, text_color=COLOR_PIVOT)
        self.status_label.pack(side="right", padx=6)
    
    def build_center_panel(self):
        self.center = ctk.CTkFrame(self, fg_color="transparent")
        self.center.grid(row=1, column=1, sticky="nsew", padx=5, pady=10)
        self.center.grid_rowconfigure(1, weight=1)
        self.center.grid_rowconfigure(2, weight=0)
        self.center.grid_rowconfigure(3, weight=0)
        self.center.grid_columnconfigure(0, weight=1)
        
        self.build_controls()
        self.build_canvas()
        self.build_decision_canvas()
        self.build_quote_bar()
    
    def build_controls(self):
        control_bar = card_frame(self.center)
        control_bar.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        
        inner = ctk.CTkFrame(control_bar, fg_color="transparent")
        inner.pack(pady=12, padx=12)
        
        buttons = [
            ("▶  Start",  "lime",   self.start_sort),
            ("⏸  Pause",  "#ffa502", self.pause_sort),
            ("⏭  Step",   "#b44fff", self.step_sort),
            ("↺  Reset",  COLOR_PIVOT, self.reset_sort),
        ] 
        for text, color, cmd in buttons:
            ctk.CTkButton(inner, text=text, width=110, height=36, font=FONT_CTRL, text_color=color, fg_color=BG_INPUT, hover_color=BG_PANEL, border_width=1, border_color=BORDER_BRIGHT, corner_radius=6, command=cmd).pack(side="left", padx=5)
        
        sep = ctk.CTkFrame(inner, width=1, height=30, fg_color=BORDER_COLOR)
        sep.pack(side="left", padx=12)
        
        ctk.CTkLabel(inner, text="Speed: ", font=FONT_SMALL, text_color=TEXT_SECONDARY).pack(side="left")
        self.speed_display = ctk.CTkLabel(inner, text="1.0", font=FONT_LABEL, text_color=COLOR_SWAP)
        self.speed_display.pack(side="left", padx=6)
    
    def build_canvas(self):
        canvas_frame = card_frame(self.center)
        canvas_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 8))
        canvas_frame.grid_propagate(True)
        
        ctk.CTkLabel(canvas_frame, text="ARRAY VISUALIZATION", font=FONT_SMALL, text_color=TEXT_MUTED).pack(anchor="w", padx=12, pady=(8, 0))
        
        self.canvas = tk.Canvas(canvas_frame, bg=BG_APP, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=8, pady=(4, 8))
    
    def build_decision_canvas(self):
        decision_frame = card_frame(self.center)
        decision_frame.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        
        ctk.CTkLabel(decision_frame, text="RECURSION TREE", font=FONT_SMALL, text_color=TEXT_MUTED).pack(anchor="w", padx=12, pady=(8, 0))
        
        self.decision_canvas = tk.Canvas(decision_frame, bg=BG_APP, highlightthickness=0, height=160)
        self.decision_canvas.pack(fill="x", padx=8, pady=(4, 8))
        
    def build_quote_bar(self):
        quote_frame = card_frame(self.center, fg_color=BG_PANEL)
        quote_frame.grid(row=3, column=0, sticky="ew")
        
        choices = ['"Divide and conquer — the essence of QuickSort."', "Dean Galdiano The Coach of The Dream Team", "The Paul Method", "DIK A 💪 DIK A 💪 DIK A 💪"]
        self.quote_var = ctk.StringVar(
            value=random.choice(choices))
        ctk.CTkLabel(quote_frame, textvariable=self.quote_var, font=FONT_HEADER,
                     text_color=TEXT_MUTED).pack(pady=8)
    
    def build_right_panel(self):
        self.right = ctk.CTkFrame(self, fg_color="transparent")
        self.right.grid(row=1, column=2, sticky="nsew", padx=(5, 10), pady=10)
        self.right.grid_rowconfigure(0, weight=1)
        self.right.grid_rowconfigure(1, weight=0)
        self.right.grid_rowconfigure(2, weight=0)
        self.right.grid_columnconfigure(0, weight=1)
        
        self.build_log()
        self.build_stats()
        self.build_subarray()
    
    def build_log(self):
        build_log_frame = card_frame(self.right)
        build_log_frame.grid(row= 0, column=0, sticky="nsew", pady=(0, 8))
        build_log_frame.grid_rowconfigure(1, weight=1)
        build_log_frame.grid_columnconfigure(0, weight=1)
        
        self.section_title(build_log_frame, "EXPLANATION LOG", grid=True, row=0)
        
        self.log_box = ctk.CTkTextbox(build_log_frame, fg_color=BG_INPUT, text_color=TEXT_PRIMARY,
                                      border_color=BORDER_COLOR, border_width=1, corner_radius=6, font=FONT_MONO, state="disabled")
        self.log_box.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10))
        
        clear_btn = ctk.CTkButton(build_log_frame, text="Clear log", height=26, font=FONT_SMALL, fg_color=BG_INPUT, hover_color=BG_PANEL, text_color=TEXT_SECONDARY, border_width=1, border_color=BORDER_COLOR, corner_radius=6, command=self.clear_log)
        clear_btn.grid(row=2, column=0, sticky="e", padx=10, pady=(0, 8))
    
    def build_stats(self):
        stat_frame = card_frame(self.right)
        stat_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        self.section_title(stat_frame, "STATISTICS")

        self.comparison_var = ctk.StringVar(value="0")
        self.swap_var       = ctk.StringVar(value="0")
        self.depth_var      = ctk.StringVar(value="0")
        self.time_var       = ctk.StringVar(value="00:00.000")

        stats = [
            ("Comparisons", self.comparison_var, COLOR_COMPARE),
            ("Swaps", self.swap_var, COLOR_SWAP),
            ("Recursion depth", self.depth_var, ACCENT_BRIGHT),
            ("Elapsed time", self.time_var, TEXT_SECONDARY),
        ]
        for label, var, color in stats:
            self.start_row(stat_frame, label, var, color)

        ctk.CTkFrame(stat_frame, height=6, fg_color="transparent").pack()
    
    def build_subarray(self):
        sub_array_frame = card_frame(self.right)
        sub_array_frame.grid(row=2, column=0, sticky="ew")

        self.section_title(sub_array_frame, "CURRENT SUBARRAY")

        self.left_idx_var   = ctk.StringVar(value="—")
        self.right_idx_var  = ctk.StringVar(value="—")
        self.subarray_var   = ctk.StringVar(value="[ ]")

        for label, var, color in [
            ("Left index",  self.left_idx_var,  ACCENT_BRIGHT),
            ("Right index", self.right_idx_var, ACCENT_BRIGHT),
            ("Subarray",    self.subarray_var,  TEXT_PRIMARY),
        ]:
            self.start_row(sub_array_frame, label, var, color)

        ctk.CTkFrame(sub_array_frame, height=6, fg_color="transparent").pack()
    
    def section_title(self, parent, text, grid=False, row=0):
        lbl = ctk.CTkLabel(parent, text=text, font=FONT_TITLE, text_color=TEXT_SECONDARY)
        
        if grid:
            lbl.grid(row=row, column=0, sticky="w", padx=12, pady=(10, 4))
        else:
            lbl.pack(anchor="w", padx=12, pady=(10, 6))
    
    def start_row(self, parent, label_text, var, color):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=2)
        ctk.CTkLabel(row, text=label_text, font=FONT_SMALL,
                     text_color=TEXT_SECONDARY).pack(side="left")
        ctk.CTkLabel(row, textvariable=var, font=FONT_LABEL,
                     text_color=color).pack(side="right")
    
    def random_input(self):
        nums = random.sample(range(1, 100), random.randint(6, 14))
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
        text= (
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
        self.array_entry.focus_set()
        
    def on_speed_change(self, val):
        label = f"{float(val):.2f}"
        self.speed_val_label.configure(text=label)
        self.speed_val_label.configure(text=label)
    
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
    
if __name__ == "__main__":
    app = MyApp()
    app.mainloop()