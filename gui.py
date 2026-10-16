import math
from variable_file import *
from reshape import text_to_persian
import customtkinter as ctk


def format_duration(total_seconds: float) -> str:
    total_seconds = int(total_seconds)
    sign = "-" if total_seconds < 0 else ""
    hours, remaining_seconds = divmod(abs(total_seconds), 3600)
    minutes, seconds = divmod(remaining_seconds, 60)
    return f"{sign}{hours}:{minutes:02d}:{seconds:02d}"


class TimerCard(ctk.CTkFrame):
    def __init__(self, master, name, store):
        super().__init__(master, width=200, height=200)
        self.pack_propagate(False)
        self.name = name
        self.store = store
        self.is_idle = (name == IDLE_NAME)

        ctk.CTkLabel(self, text=text_to_persian(name), font=(FONT, 24)).pack(padx=25, pady=10)

        self.timer_text = ctk.CTkLabel(self, text="", font=("Arial", 24))
        self.timer_text.pack(pady=10)
        self.default_color = self.timer_text.cget("text_color")

        if not self.is_idle:
            self.btn_select = ctk.CTkButton(
                self, text=text_to_persian("انتخاب"), font=(FONT, 28), command=self.timer
            )
            self.btn_select.pack(pady=10)

        self.refresh()

    def timer(self):
        self.store.select(self.name)

    def refresh(self):
        remaining = self.store.get_remaining(self.name)
        self.timer_text.configure(
            text=format_duration(math.ceil(remaining)),
            text_color="#ff4d4d" if remaining < 0 else self.default_color,
        )

        running = self.store.active == self.name
        self.configure(border_width=2 if running else 0, border_color="#00ff2a")

        if not self.is_idle:
            self.btn_select.configure(
                text=text_to_persian("توقف" if running else "انتخاب"),
                fg_color="#c0392b" if running else ["#3a7ebf", "#1f538d"],
            )
