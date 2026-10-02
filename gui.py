import math
from variable_file import *
from reshape import text_to_persian
import customtkinter as ctk


def format_duration(total_seconds: float) -> str:
    total_seconds = int(total_seconds)
    hours, remaining_seconds = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remaining_seconds, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}"


class TimerCard(ctk.CTkFrame):
    def __init__(self, master, name, store):
        super().__init__(master, width=250, height=250)
        self.pack_propagate(False)
        self.name = name
        self.store = store

        ctk.CTkLabel(self, text=text_to_persian(name), font=(FONT, 32)).pack(padx=25, pady=10)

        self.timer_text = ctk.CTkLabel(self, text="", font=("Arial", 24))
        self.timer_text.pack(pady=10)

        self.btn_select = ctk.CTkButton(
            self, text=text_to_persian("انتخاب"), font=(FONT, 28), command=self.timer
        )
        self.btn_select.pack(pady=10)

        self.refresh()

    def timer(self):
        # کلیک روی تایمر فعال = توقف، کلیک روی بقیه = شروع (و توقف تایمر قبلی)
        if self.store.active == self.name:
            self.store.pause()
        else:
            self.store.select(self.name)

    def refresh(self):
        remaining = self.store.get_remaining(self.name)
        self.timer_text.configure(text=format_duration(math.ceil(remaining)))

        running = self.store.active == self.name
        self.btn_select.configure(
            text=text_to_persian("توقف" if running else "انتخاب"),
            fg_color="#c0392b" if running else ["#3a7ebf", "#1f538d"],
        )