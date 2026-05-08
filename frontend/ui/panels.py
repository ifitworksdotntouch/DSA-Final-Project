import customtkinter as ctk
import tkinter as tk
import random

from constants import (
    BG_APP,
    BG_PANEL,
    BG_CARD,
    BG_INPUT,
    ACCENT_BLUE,
    ACCENT_BRIGHT,
    BORDER_COLOR,
    BORDER_BRIGHT,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    COLOR_PIVOT,
    COLOR_COMPARE,
    COLOR_SWAP,
    COLOR_SORTED,
    COLOR_UNSORTED,
    FONT_TITLE,
    FONT_LABEL,
    FONT_SMALL,
    FONT_MONO,
    FONT_HEADER,
    FONT_CTRL,
    card_frame,
)

def section_title(parent, text, grid=False, row=0):
    lbl = ctk.CTkLabel(parent, text=text, font=FONT_TITLE, text_color=TEXT_SECONDARY)
    if grid:
        lbl.grid(row=row, column=0, sticky="w", padx=12, pady=(10, 4))
    else:
        lbl.pack(anchor="w", padx=12, pady=(10, 6))


def start_row(parent, label_text, var, color):
    row = ctk.CTkFrame(parent, fg_color="transparent"); row.pack(fill="x", padx=12, pady=2)
    ctk.CTkLabel(row, text=label_text, font=FONT_SMALL, text_color=TEXT_SECONDARY).pack(side="left")
    ctk.CTkLabel(row, textvariable=var, font=FONT_LABEL, text_color=color).pack(side="right")


class LeftPanel:
    def __init__(self, app):
        self.app = app

    def build(self):
        self.input_section()
        self.pivot_section()
        self.speed_section()
        self.legend_section()
        self.status_section()
    
    def input_section(self):
        input_frame = card_frame(self.app.left)
        input_frame.pack(fill="x", pady=(0, 8))
        section_title(input_frame, "INPUT ARRAY")
        btn_row = ctk.CTkFrame(input_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=10, pady=(0, 6))
        ctk.CTkButton(btn_row, text="Manual", width=108, height=30, font=FONT_SMALL, fg_color=ACCENT_BLUE, hover_color=ACCENT_BRIGHT, corner_radius=6, command=self.app.focus_entry).pack(side="left", padx=(0, 6))
        ctk.CTkButton(btn_row, text="Random", width=108, height=30, font=FONT_SMALL, fg_color=ACCENT_BLUE, hover_color=ACCENT_BRIGHT, corner_radius=6, command=self.app.random_input).pack(side="left")
        self.app.array_entry = ctk.CTkTextbox(input_frame, height=48, fg_color=BG_INPUT, text_color=TEXT_PRIMARY, border_color=BORDER_BRIGHT, border_width=1, corner_radius=6, font=FONT_MONO, wrap="word")
        self.app.array_entry.pack(fill="x", padx=10, pady=(0, 6))
        ctk.CTkButton(input_frame, text="Generate Array", height=32, font=FONT_LABEL, fg_color=ACCENT_BLUE, hover_color=ACCENT_BRIGHT, corner_radius=6, border_width=1, border_color=BORDER_BRIGHT, command=self.app.generate_array).pack(fill="x", padx=10, pady=(0, 10))
    
    def pivot_section(self):
        pivot_frame = card_frame(self.app.left); pivot_frame.pack(fill="x", pady=(0, 8))
        header = ctk.CTkFrame(pivot_frame, fg_color="transparent"); header.pack(fill="x", padx=10, pady=(10, 4))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="PIVOT SELECTION", font=FONT_TITLE, text_color=TEXT_PRIMARY).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(header, text="?", width=22, height=22, font=FONT_SMALL, fg_color=ACCENT_BLUE, hover_color=ACCENT_BRIGHT, corner_radius=11, command=self.app.show_pivot_help).grid(row=0, column=1, sticky="e")
        self.app.pivot_var = ctk.StringVar(value="last")
        for value, label in [("first", "First element"), ("last", "Last element"), ("random", "Random element")]:
            ctk.CTkRadioButton(pivot_frame, text=label, value=value, variable=self.app.pivot_var, font=FONT_SMALL, text_color=TEXT_PRIMARY, fg_color=ACCENT_BRIGHT, hover_color=ACCENT_BLUE).pack(anchor="w", padx=14, pady=3)
        ctk.CTkFrame(pivot_frame, height=10, fg_color="transparent").pack()
    
    def speed_section(self):
        speed_frame = card_frame(self.app.left); speed_frame.pack(fill="x", pady=(0, 8))
        section_title(speed_frame, "ANIMATION SPEED")
        self.app.speed_var = ctk.DoubleVar(value=1.0)
        self.app.speed_val_label = ctk.CTkLabel(speed_frame, text="1.0×", font=FONT_LABEL, text_color=ACCENT_BRIGHT); self.app.speed_val_label.pack()
        slider = ctk.CTkSlider(speed_frame, from_=0.25, to=3.0, variable=self.app.speed_var, number_of_steps=11, progress_color=ACCENT_BLUE, button_color=ACCENT_BRIGHT, command=self.app.on_speed_change); slider.pack(fill="x", padx=16, pady=(2, 4))
        row = ctk.CTkFrame(speed_frame, fg_color="transparent"); row.pack(fill="x", padx=16, pady=(0, 10))
        for txt, side in [("Slow", "left"), ("Fast", "right")]:
            ctk.CTkLabel(row, text=txt, font=FONT_SMALL, text_color=TEXT_SECONDARY).pack(side=side)
    
    def legend_section(self):
        legend_frame = card_frame(self.app.left)
        legend_frame.pack(fill="x", pady=(0, 8))
        section_title(legend_frame, "LEGEND")
        colors = [(COLOR_PIVOT, "Pivot"), (COLOR_COMPARE, "Comparing"), (COLOR_SWAP, "Swapping"), (COLOR_SORTED, "Sorted"), (COLOR_UNSORTED, "Unsorted")]
        for color, label in colors:
            row = ctk.CTkFrame(legend_frame, fg_color="transparent"); row.pack(fill="x", padx=14, pady=3)
            ctk.CTkLabel(row, text="", width=18, height=18, fg_color=color, corner_radius=3).pack(side="left")
            ctk.CTkLabel(row, text=label, font=FONT_SMALL, text_color=TEXT_PRIMARY).pack(side="left", padx=10)
        ctk.CTkFrame(legend_frame, height=6, fg_color="transparent").pack()
    
    def status_section(self):
        status_frame = card_frame(self.app.left); status_frame.pack(fill="x", pady=(0, 8))
        row = ctk.CTkFrame(status_frame, fg_color="transparent"); row.pack(fill="x", padx=14, pady=10)
        ctk.CTkLabel(row, text="STATUS", font=FONT_LABEL, text_color=TEXT_SECONDARY).pack(side="left")
        self.app.status_var = ctk.StringVar(value="Idle")
        self.app.status_label = ctk.CTkLabel(row, textvariable=self.app.status_var, font=FONT_LABEL, text_color=COLOR_PIVOT); self.app.status_label.pack(side="right", padx=6)

class CenterPanel:
    def __init__(self, app):
        self.app = app

    def build(self):
        self.controls()
        self.canvas()
        self.decision_canvas()
        self.quote_bar()
    
    def controls(self):
        control_bar = card_frame(self.app.center); control_bar.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        inner = ctk.CTkFrame(control_bar, fg_color="transparent")
        inner.pack(pady=12, padx=12)
        buttons = [("▶  Start", "lime", self.app.start_sort), ("⏸  Pause", "#ffa502", self.app.pause_sort), ("⏭  Step", "#b44fff", self.app.step_sort), ("↺  Reset", COLOR_PIVOT, self.app.reset_sort)]
        for text, color, cmd in buttons:
            ctk.CTkButton(inner, text=text, width=110, height=36, font=FONT_CTRL, text_color=color, fg_color=BG_INPUT, hover_color=BG_PANEL, border_width=1, border_color=BORDER_BRIGHT, corner_radius=6, command=cmd).pack(side="left", padx=5)
        sep = ctk.CTkFrame(inner, width=1, height=30, fg_color=BORDER_COLOR); sep.pack(side="left", padx=12)
        ctk.CTkLabel(inner, text="Speed: ", font=FONT_SMALL, text_color=TEXT_SECONDARY).pack(side="left")
        self.app.speed_display = ctk.CTkLabel(inner, text="1.0", font=FONT_LABEL, text_color=COLOR_SWAP); self.app.speed_display.pack(side="left", padx=6)
    
    def canvas(self):
        canvas_frame = card_frame(self.app.center); canvas_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 8)); canvas_frame.grid_propagate(True)
        ctk.CTkLabel(canvas_frame, text="ARRAY VISUALIZATION", font=FONT_SMALL, text_color=TEXT_MUTED).pack(anchor="w", padx=12, pady=(8, 0))
        self.app.canvas = tk.Canvas(canvas_frame, bg=BG_APP, highlightthickness=0); self.app.canvas.pack(fill="both", expand=True, padx=8, pady=(4, 8))
    
    def decision_canvas(self):
        decision_frame = card_frame(self.app.center); decision_frame.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        ctk.CTkLabel(decision_frame, text="RECURSION TREE", font=FONT_SMALL, text_color=TEXT_MUTED).pack(anchor="w", padx=12, pady=(8, 0))
        self.app.decision_canvas = tk.Canvas(decision_frame, bg=BG_APP, highlightthickness=0, height=160); self.app.decision_canvas.pack(fill="x", padx=8, pady=(4, 8))
    
    def quote_bar(self):
        quote_frame = card_frame(self.app.center, fg_color=BG_PANEL)
        quote_frame.grid(row=3, column=0, sticky="ew")
        choices = ['"Divide and conquer — the essence of QuickSort."']
        self.app.quote_var = ctk.StringVar(value=random.choice(choices))
        ctk.CTkLabel(quote_frame, textvariable=self.app.quote_var, font=FONT_HEADER, text_color=TEXT_MUTED).pack(pady=8)

class RightPanel:
    def __init__(self, app):
        self.app = app

    def build(self):
        self.log()
        self.stats()
        self.subarray()
    
    def log(self):
        log_frame = card_frame(self.app.right); log_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 8)); log_frame.grid_rowconfigure(1, weight=1); log_frame.grid_columnconfigure(0, weight=1)
        section_title(log_frame, "EXPLANATION LOG", grid=True, row=0)
        self.app.log_box = ctk.CTkTextbox(log_frame, fg_color=BG_INPUT, text_color=TEXT_PRIMARY, border_color=BORDER_COLOR, border_width=1, corner_radius=6, font=FONT_MONO, state="disabled")
        self.app.log_box.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        clear_btn = ctk.CTkButton(log_frame, text="Clear log", height=26, font=FONT_SMALL, fg_color=BG_INPUT, hover_color=BG_PANEL, text_color=TEXT_SECONDARY, border_width=1, border_color=BORDER_COLOR, corner_radius=6, command=self.app.clear_log); clear_btn.grid(row=2, column=0, sticky="e", padx=10, pady=(0, 8))
    
    def stats(self):
        stat_frame = card_frame(self.app.right); stat_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        section_title(stat_frame, "STATISTICS")
        self.app.comparison_var = ctk.StringVar(value="0")
        self.app.swap_var = ctk.StringVar(value="0")
        self.app.depth_var = ctk.StringVar(value="0")
        self.app.time_var = ctk.StringVar(value="00:00.000")
        stats = [("Comparisons", self.app.comparison_var, COLOR_COMPARE), ("Swaps", self.app.swap_var, COLOR_SWAP), ("Recursion depth", self.app.depth_var, ACCENT_BRIGHT), ("Elapsed time", self.app.time_var, TEXT_SECONDARY)]
        for label, var, color in stats:
            start_row(stat_frame, label, var, color)
        ctk.CTkFrame(stat_frame, height=6, fg_color="transparent").pack()
    
    def subarray(self):
        sub_array_frame = card_frame(self.app.right); sub_array_frame.grid(row=2, column=0, sticky="ew")
        section_title(sub_array_frame, "CURRENT SUBARRAY")
        self.app.left_idx_var = ctk.StringVar(value="—")
        self.app.right_idx_var = ctk.StringVar(value="—")
        self.app.subarray_var = ctk.StringVar(value="[ ]")
        for label, var, color in [("Left index", self.app.left_idx_var, ACCENT_BRIGHT), ("Right index", self.app.right_idx_var, ACCENT_BRIGHT), ("Subarray", self.app.subarray_var, TEXT_PRIMARY)]:
            start_row(sub_array_frame, label, var, color)
        ctk.CTkFrame(sub_array_frame, height=6, fg_color="transparent").pack()