import customtkinter as ctk

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

FONT_TITLE = ("Consolas", 14, "bold")
FONT_LABEL = ("Consolas", 12, "bold")
FONT_SMALL = ("Consolas", 15)
FONT_MONO = ("Consolas", 12)
FONT_HEADER = ("Consolas", 16, "bold")
FONT_CTRL = ("Consolas", 13, "bold")

def card_frame(parent, corner_radius=8, border_width=1, border_color=BORDER_COLOR, fg_color=BG_CARD):
    return ctk.CTkFrame(parent, corner_radius=corner_radius, border_width=border_width,
                       border_color=border_color, fg_color=fg_color)