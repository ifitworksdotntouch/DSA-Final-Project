import customtkinter as ctk
import tkinter as tk
import random
import os
import re
from api_client import SortApiClient, SortResult, SortStep


from PIL import Image

from constants import (
    BG_APP, BG_PANEL, BG_CARD,
    ACCENT_BLUE, ACCENT_BRIGHT, BORDER_COLOR, BORDER_BRIGHT,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    COLOR_PIVOT, COLOR_COMPARE, COLOR_SWAP, COLOR_SORTED, COLOR_UNSORTED,
    FONT_LABEL, FONT_SMALL, FONT_HEADER,
)
from ui.panels import LeftPanel, CenterPanel, RightPanel

class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.launch_backend()
        self.title("QuickSort Application")
        self.geometry("1600x920")
        self.minsize(1100, 720)
        self.configure(fg_color=BG_APP)
        self.resizable(True, True)
        
        self.api = SortApiClient()
        self.array = []
        self._steps = []
        self._step_index = 0
        self._playing = False
        self._sort_result = None
        self._playback_after_id = None
        self._resize_after_id = None
        self._last_logged_msg = None
        self.after(300, self.check_connection)
        
        self.build_layout()
        self.header()
        self.build_left_panel()
        self.build_center_panel()
        self.build_right_panel()

        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.decision_canvas.bind("<Configure>", self._on_canvas_configure)
        self.on_speed_change(self.speed_var.get())

    def build_layout(self):
        self.grid_columnconfigure(0, weight=0, minsize=260)
        self.grid_columnconfigure(1, weight=2, minsize=420)
        self.grid_columnconfigure(2, weight=1, minsize=340)
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
        help_section = self.dialog("Help", "600x560", minsize=(480, 400))
        self.dialog_header(help_section, "QuickSort Help")

        body = ctk.CTkScrollableFrame(
            help_section, fg_color=BG_PANEL, corner_radius=10,
            scrollbar_button_color=BORDER_COLOR,
        )
        body.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        sections = [
            ("What this app does",
             "You enter a list of integers (or use Random). The Spring Boot backend runs quicksort with Hoare partitioning and records every comparison, swap, and pivot choice. The desktop client animates those steps so you can see how the array evolves."),
            ("Controls",
             "Start fetches the step trace and plays it. Pause stops auto-play. Step moves one frame forward (useful with Pause). Reset jumps back to the first frame. Adjust Animation Speed to slow down or speed up playback."),
            ("Colors",
             "Pivot highlights the pivot index, Comparing shows indices being compared to the pivot, Swapping shows a pair being exchanged, Sorted marks indices known to be in final position, and Unsorted is everything else in the active window."),
            ("Backend",
             "The API must be running at http://localhost:8080 (see the backend Spring project). If it is offline, Random still works locally, but Start needs the server to compute sort steps."),
        ]

        for heading, text in sections:
            ctk.CTkLabel(body, text=heading, font=FONT_LABEL, text_color=ACCENT_BRIGHT).pack(anchor="w", padx=16, pady=(12, 4))
            lbl = ctk.CTkLabel(
                body, text=text, justify="left", font=FONT_SMALL,
                text_color=TEXT_PRIMARY, anchor="w",
            )
            lbl.pack(anchor="w", padx=24, pady=(0, 4))
            self._bind_wrap_to_parent(body, lbl, inset=48)

        ctk.CTkButton(help_section, text="Close", fg_color=ACCENT_BLUE, hover_color=ACCENT_BRIGHT, corner_radius=6, command=help_section.destroy).pack(pady=12)
    
    def open_about(self):
        about_section = self.dialog("About", "480x360", minsize=(400, 280))
        self.dialog_header(about_section, "About this app")

        body = ctk.CTkFrame(about_section, fg_color=BG_PANEL, corner_radius=10)
        body.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        body.grid_columnconfigure(0, weight=1)

        about_text = (
            "QuickSort Application\n\n"
            "DSA final project: Python (CustomTkinter) frontend with a Java Spring Boot "
            "sorting service. Visualization uses step data returned from the server.\n\n"
            "Median-of-three pivot selection and Hoare partition are implemented on the backend."
        )
        about_lbl = ctk.CTkLabel(
            body, text=about_text, justify="left", font=FONT_SMALL,
            text_color=TEXT_PRIMARY, anchor="w",
        )
        about_lbl.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        self._bind_wrap_to_parent(body, about_lbl, inset=48)
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
    
    def random_input(self):
        self.api.random_array_async(
            on_success=self._apply_random_array,
            on_error=lambda _: self._apply_random_array([random.randint(1, 99) for _ in range(10)]),
            tk_root=self,
        )

    def _apply_random_array(self, arr):
        self._cancel_playback()
        self._steps = []
        self._step_index = 0
        self._sort_result = None
        self.array = list(arr)
        self.array_entry.delete("1.0", "end")
        self.array_entry.insert("1.0", ", ".join(str(x) for x in self.array))
        self._reset_stats()
        self._last_logged_msg = None
        self.clear_log()
        self.log(f"Random array loaded ({len(self.array)} elements).")
        self._draw_bars_from_array(self.array, None)
        self._draw_recursion_panel(None, self.array)
        self.update_status("Ready", TEXT_PRIMARY)

    def generate_array(self):
        arr = self._parse_array_from_entry()
        if arr is None:
            self.update_status("Invalid input — use integers", COLOR_PIVOT)
            self.log("Could not parse the text box. Use comma or space separated integers (e.g. 5, 2, 9, 1).")
            return
        self._cancel_playback()
        self._steps = []
        self._step_index = 0
        self._sort_result = None
        self.array = arr
        self._reset_stats()
        self._last_logged_msg = None
        self.log(f"Array set ({len(self.array)} elements). Press Start to sort.")
        self._draw_bars_from_array(self.array, None)
        self._draw_recursion_panel(None, self.array)
        self.update_status("Ready", TEXT_PRIMARY)

    def start_sort(self):
        arr = self._parse_array_from_entry()
        if arr is None or len(arr) == 0:
            self.update_status("Enter a non-empty array", COLOR_PIVOT)
            return
        self.array = arr
        self._cancel_playback()
        self._playing = True
        self._steps = []
        self._step_index = 0
        self._sort_result = None
        self._last_logged_msg = None
        self.update_status("Requesting sort…", ACCENT_BRIGHT)
        self.log("Requesting sort trace from backend…")

        def on_ok(result: SortResult):
            self._sort_result = result
            self._steps = result.steps
            self._step_index = 0
            self.clear_log()
            self.log(f"Trace loaded: {len(self._steps)} steps.")
            self._render_current_step(log_auto=True)
            self.update_status("Playing", ACCENT_BRIGHT)
            self._schedule_playback_tick()

        def on_err(msg: str):
            self._playing = False
            self.update_status("Sort failed", COLOR_PIVOT)
            self.log(msg)

        self.api.sort_async(arr, on_ok, on_err, self)

    def pause_sort(self):
        self._playing = False
        self._cancel_playback()
        if self._steps:
            self.update_status("Paused", TEXT_SECONDARY)
    
    def prev_step(self):
        self._playing = False
        if self._step_index > 1:
            self._step_index -= 2
            self.update_status("Stepping", COLOR_COMPARE)
            step = self._steps[self._step_index]
            self._step_index += 1
            self._draw_bars_from_step(step)    
            self._draw_recursion_panel(step, step.array)  
            self._update_stats_from_step(step) 
            if step.message:
                self.log(step.message)
        else:
            self.log("Already at the first step.")

    def step_sort(self):
        if not self._steps:
            self.log("Run Start first to load steps.")
            return
        self._playing = False
        self._cancel_playback()
        if self._step_index < len(self._steps) - 1:
            self._step_index += 1
        self._render_current_step(log_auto=False)
        if self._step_index >= len(self._steps) - 1:
            self.update_status("Complete", COLOR_SWAP)
        else:
            self.update_status("Paused (step)", TEXT_SECONDARY)

    def reset_sort(self):
        self._playing = False
        self._cancel_playback()
        self._step_index = 0
        self._last_logged_msg = None
        if self._steps:
            self._render_current_step(log_auto=False)
            self.update_status("Reset", TEXT_PRIMARY)
        else:
            arr = self._parse_array_from_entry()
            if arr:
                self.array = arr
            self._draw_bars_from_array(self.array, None)
            self._draw_recursion_panel(None, self.array)
            self._reset_stats()
            self.update_status("Idle", TEXT_PRIMARY)
    
    def show_pivot_help(self):
        window = self.dialog("Pivot selection (fixed)", "520x300", minsize=(420, 240))
        self.dialog_header(window, "Pivot strategy")

        body = ctk.CTkFrame(window, fg_color=BG_PANEL, corner_radius=10)
        body.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        text = (
            "The backend uses a fixed strategy: median-of-three on the first, middle, and last element "
            "of each subarray, then that median is moved to the high index before Hoare partitioning "
            "(same idea as a typical class quicksort reference). There is no pivot mode to choose."
        )
        lbl = ctk.CTkLabel(
            body, text=text, justify="left", font=FONT_SMALL,
            text_color=TEXT_PRIMARY, anchor="w",
        )
        lbl.pack(fill="x", padx=16, pady=12)
        self._bind_wrap_to_parent(body, lbl, inset=40)
        ctk.CTkButton(window, text="Close", fg_color=ACCENT_BLUE, hover_color=ACCENT_BRIGHT, corner_radius=6, command=window.destroy).pack(pady=12)

    def _bind_wrap_to_parent(self, parent, label, inset=32):
        def _apply(_event=None):
            try:
                w = parent.winfo_width()
                if w > inset + 40:
                    label.configure(wraplength=w - inset)
            except tk.TclError:
                pass
        parent.bind("<Configure>", lambda e: _apply())
        parent.after(50, _apply)
    

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
        self.speed_val_label.configure(text=label + "×")
        if hasattr(self, "speed_display"):
            self.speed_display.configure(text=label)

    def dialog(self, title, geometry, minsize=(480, 360)):
        window = ctk.CTkToplevel(self)
        window.title(title)
        window.geometry(geometry)
        window.minsize(minsize[0], minsize[1])
        window.configure(fg_color=BG_APP)
        window.resizable(True, True)
        window.after(100, lambda: (window.lift(), window.focus_force(), window.grab_set()))
        return window

    def dialog_header(self, parent, text):
        frame = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=10)
        frame.pack(fill="x", padx=14, pady=14)
        ctk.CTkLabel(frame, text=text, font=FONT_HEADER, text_color=TEXT_PRIMARY).pack(pady=12)
        
    def check_connection(self):
        import threading
        def _ping():
            ok = self.api.health()
            def _update():
                if ok:
                    self.backend_var.set("● Connected")
                    self.backend_label.configure(text_color=COLOR_SWAP)
                else:
                    self.backend_var.set("● Offline")
                    self.backend_label.configure(text_color=COLOR_PIVOT)
            self.after(0, _update)
        threading.Thread(target=_ping, daemon=True).start()

    def _parse_array_from_entry(self):
        text = self.array_entry.get("1.0", "end").strip()
        if not text:
            return None
        parts = re.split(r"[\s,;]+", text)
        out = []
        for p in parts:
            if not p:
                continue
            try:
                out.append(int(p))
            except ValueError:
                return None
        return out
    def _cancel_playback(self):
        if self._playback_after_id is not None:
            try:
                self.after_cancel(self._playback_after_id)
            except Exception:
                pass
            self._playback_after_id = None

    def _schedule_playback_tick(self):
        if not self._playing or not self._steps:
            return
        if self._step_index >= len(self._steps) - 1:
            self._playing = False
            self.update_status("Complete", COLOR_SWAP)
            if self._sort_result is not None:
                self._apply_final_stats(self._sort_result)
            return
        speed = float(self.speed_var.get())
        delay = max(25, int(380 / max(speed, 0.05)))
        self._playback_after_id = self.after(delay, self._playback_tick)

    def _playback_tick(self):
        self._playback_after_id = None
        if not self._playing or not self._steps:
            return
        if self._step_index >= len(self._steps) - 1:
            self._playing = False
            self.update_status("Complete", COLOR_SWAP)
            if self._sort_result is not None:
                self._apply_final_stats(self._sort_result)
            return
        self._step_index += 1
        self._render_current_step(log_auto=True)
        self._schedule_playback_tick()

    def _render_current_step(self, log_auto: bool):
        if not self._steps:
            return
        step = self._steps[self._step_index]
        self._draw_bars_from_step(step)
        self._draw_recursion_panel(step, step.array)
        self._update_stats_from_step(step)
        self._maybe_log_step(step, log_auto=log_auto)
        if self._step_index >= len(self._steps) - 1 and self._sort_result is not None:
            self._apply_final_stats(self._sort_result)

    def _maybe_log_step(self, step: SortStep, log_auto: bool):
        msg = step.message or ""
        if not msg:
            return
        if msg == self._last_logged_msg:
            return
        if log_auto:
            if self._should_log_auto(msg):
                self.log(msg)
                self._last_logged_msg = msg
        else:
            self.log(msg)
            self._last_logged_msg = msg

    @staticmethod
    def _should_log_auto(msg: str) -> bool:
        keys = (
            "Pivot selected",
            "Pivot (",
            "Median setup",
            "Swapped",
            "Partitioning complete",
            "final position",
        )
        return any(k in msg for k in keys)

    def _reset_stats(self):
        self.comparison_var.set("0")
        self.swap_var.set("0")
        self.depth_var.set("0")
        self.left_idx_var.set("—")
        self.right_idx_var.set("—")
        self.subarray_var.set("[ ]")

    def _update_stats_from_step(self, step: SortStep):
        self.comparison_var.set(str(step.comparisons))
        self.swap_var.set(str(step.swaps))
        self.depth_var.set(str(step.depth))
        self.left_idx_var.set(str(step.left))
        self.right_idx_var.set(str(step.right))
        arr = step.array
        if step.left <= step.right and arr:
            sub = arr[step.left : step.right + 1]
            self.subarray_var.set("[ " + ", ".join(str(x) for x in sub) + " ]")
        else:
            self.subarray_var.set("[ ]")

    def _apply_final_stats(self, result: SortResult):
        self.comparison_var.set(str(result.total_comparisons))
        self.swap_var.set(str(result.total_swaps))
        self.depth_var.set(str(result.max_depth))

    def _on_canvas_configure(self, _event=None):
        if self._resize_after_id is not None:
            try:
                self.after_cancel(self._resize_after_id)
            except Exception:
                pass
        self._resize_after_id = self.after(120, self._redraw_from_state)

    def _redraw_from_state(self):
        self._resize_after_id = None
        if self._steps and 0 <= self._step_index < len(self._steps):
            self._draw_bars_from_step(self._steps[self._step_index])
            self._draw_recursion_panel(self._steps[self._step_index], self._steps[self._step_index].array)
        elif self.array:
            self._draw_bars_from_array(self.array, None)
            self._draw_recursion_panel(None, self.array)

    def _bar_fill(self, index: int, step: SortStep | None) -> str:
        if step is None:
            return COLOR_UNSORTED
        if index in step.swap_indices:
            return COLOR_SWAP
        if index in step.compare_indices:
            return COLOR_COMPARE
        if step.pivot_index is not None and index == step.pivot_index:
            return COLOR_PIVOT
        if index in step.sorted_indices:
            return COLOR_SORTED
        return COLOR_UNSORTED

    def _draw_bars_from_array(self, arr: list[int], step: SortStep | None):
        self.canvas.delete("all")
        if not arr:
            return
        w = max(self.canvas.winfo_width(), 200)
        h = max(self.canvas.winfo_height(), 120)
        pad_x, pad_y = 16, 20
        n = len(arr)
        max_v = max(arr) if arr else 1
        gap = 4
        bar_w = max(3, (w - 2 * pad_x - gap * (n - 1)) / n)
        base_y = h - pad_y
        for i, val in enumerate(arr):
            x0 = pad_x + i * (bar_w + gap)
            x1 = x0 + bar_w
            bar_h = (val / max_v) * (h - 2 * pad_y)
            y0 = base_y - bar_h
            color = self._bar_fill(i, step)
            self.canvas.create_rectangle(x0, y0, x1, base_y, fill=color, outline="", width=0)

    def _draw_bars_from_step(self, step: SortStep):
        self._draw_bars_from_array(list(step.array), step)

    def _draw_recursion_panel(self, step: SortStep | None, arr: list[int]):
        self.decision_canvas.delete("all")
        n = len(arr)
        if n == 0:
            return
        w = max(self.decision_canvas.winfo_width(), 200)
        h = max(self.decision_canvas.winfo_height(), 100)
        pad = 14
        depth_txt = f"depth {step.depth}" if step else "idle"
        range_txt = f"[{step.left} .. {step.right}]" if step else "full array"
        self.decision_canvas.create_text(
            pad, 18, anchor="w",
            text=f"Recursion frame: {depth_txt}   Subarray: {range_txt}",
            fill=TEXT_MUTED, font=("Consolas", 10),
        )
        y_mid = h // 2 + 10
        usable = w - 2 * pad
        cell = usable / n
        self.decision_canvas.create_line(pad, y_mid, pad + usable, y_mid, fill=BORDER_BRIGHT, width=2)
        for i in range(n + 1):
            x = pad + i * cell
            self.decision_canvas.create_line(x, y_mid - 4, x, y_mid + 4, fill=BORDER_COLOR, width=1)
        if step:
            x0 = pad + step.left * cell
            x1 = pad + (step.right + 1) * cell
            self.decision_canvas.create_rectangle(
                x0, y_mid - 14, x1, y_mid + 14,
                outline=ACCENT_BRIGHT, width=2, fill="",
            )
        for i, val in enumerate(arr):
            cx = pad + (i + 0.5) * cell
            self.decision_canvas.create_text(cx, y_mid + 28, text=str(val), fill=TEXT_SECONDARY, font=("Consolas", 9))
    
    def launch_backend(self):
        import subprocess
        jar_path = os.path.join(os.path.dirname(__file__), "backend.jar")
        try:
            subprocess.Popen(
                ["java", "-jar", jar_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                )
        except FileNotFoundError:
            self.after(500, lambda: self.log("Ayaw gumana haha"))
        except Exception as e:
            self.after(500, lambda: self.log(f"Failed: {e}"))
            