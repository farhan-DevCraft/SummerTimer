import sys
import customtkinter as ctk
from gui import TimerCard
from reshape import text_to_persian
from variable_file import *
from storage import TimerStore

ctk.set_appearance_mode("dark")


class InputFrame(ctk.CTkFrame):
    def __init__(self, master, cal):
        super().__init__(master)

        ctk.CTkLabel(self, text=text_to_persian("لطفا فیلد ها را پر کنید."),
                     font=(FONT, 30), text_color="#ffbd39").pack()

        self.start_time_entry = ctk.CTkEntry(
            self, placeholder_text=text_to_persian("ساعت شروع را وارد کنید."),
            font=(FONT, 30), width=500, justify="center", height=60)
        self.start_time_entry.pack(pady=45, padx=50)

        self.end_time_entry = ctk.CTkEntry(
            self, placeholder_text=text_to_persian("ساعت پایان را وارد کنید."),
            justify="center", font=(FONT, 30), width=500, height=60)
        self.end_time_entry.pack(pady=45, padx=50)

        self.calculate_button = ctk.CTkButton(
            self, font=(FONT, 30), text=text_to_persian("محاسبه"), command=cal)
        self.calculate_button.pack(pady=40)


class PasswordDialog(ctk.CTkToplevel):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.on_success = on_success
        self.typed = ""
        self.title(text_to_persian("ریست"))
        self.geometry("340x480")
        self.resizable(False, False)
        self.transient(master)
        self.after(150, self.grab_set)

        ctk.CTkLabel(self, text=text_to_persian("رمز عبور را وارد کنید"),
                     font=(FONT, 22)).pack(pady=(20, 10))

        self.display = ctk.CTkLabel(self, text="", font=("Arial", 30), height=45)
        self.display.pack(pady=5)

        self.error_label = ctk.CTkLabel(self, text="", font=(FONT, 18),
                                        text_color="#ff4d4d", height=25)
        self.error_label.pack()

        pad = ctk.CTkFrame(self, fg_color="transparent")
        pad.pack(pady=10)
        keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "⌫", "0", "✔"]
        for i, key in enumerate(keys):
            ctk.CTkButton(
                pad, text=key, width=80, height=60, font=("Arial", 24),
                command=lambda k=key: self.press(k),
            ).grid(row=i // 3, column=i % 3, padx=5, pady=5)

    def press(self, key):
        self.error_label.configure(text="")
        if key == "⌫":
            self.typed = self.typed[:-1]
        elif key == "✔":
            self.check()
            return
        elif len(self.typed) < 12:
            self.typed += key
        self.display.configure(text="●" * len(self.typed))

    def check(self):
        if self.typed == RESET_PASSWORD:
            self.destroy()
            self.on_success()
        else:
            self.typed = ""
            self.display.configure(text="")
            self.error_label.configure(text=text_to_persian("رمز اشتباه است"))


class ResultFrame(ctk.CTkFrame):
    def __init__(self, master, store, on_reset):
        super().__init__(master)
        self.store = store
        self.cards = []
        self._ticking = False

        ctk.CTkLabel(self, text=text_to_persian("تایمر ها"), font=(FONT, 100),
                     text_color="#00ff2a").pack(padx=100, pady=30)
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(expand=True)

        ctk.CTkButton(
            self, text=text_to_persian("ریست"), font=(FONT, 20), width=120,
            fg_color="#555555", hover_color="#c0392b",
            command=lambda: PasswordDialog(self, on_reset),
        ).pack(side="bottom", pady=20)

    def show_times(self):
        self.clear_cards()
        for name in self.store.names():
            card = TimerCard(self.cards_frame, name, self.store)
            card.pack(side="left", padx=10, pady=10, expand=True)
            self.cards.append(card)
        if not self._ticking:
            self._ticking = True
            self.tick()

    def clear_cards(self):
        for card in self.cards:
            card.destroy()
        self.cards = []

    def tick(self):
        for card in self.cards:
            card.refresh()
        self.after(500, self.tick)


class SummerTimer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"SummerTimer v{VERSION}")

        self.store = TimerStore()
        self.input_page = InputFrame(self, self.calculate)
        self.result_frame = ResultFrame(self, self.store, self.reset_all)

        ctk.CTkLabel(self, text=f"v{VERSION}", font=("Arial", 14),
                     text_color="gray").pack(side="bottom", anchor="e", padx=10, pady=5)

        if self.store.has_data():
            self.show_results()
        else:
            self.input_page.pack(expand=True, fill="both")

    def calculate(self):
        try:
            start = int(self.input_page.start_time_entry.get())
            end = int(self.input_page.end_time_entry.get())
        except ValueError:
            return  # ورودی عدد نیست

        free_seconds = (end - start) * 3600
        if free_seconds <= 0:
            return

        fixed: dict[str, float] = {
            name: float(minutes * 60) for name, minutes in FIXED_MINUTES.items()
        }
        flexible = max(0, free_seconds - sum(fixed.values()))

        times: dict[str, float] = {}
        for name, percent in task_time.items():
            times[name] = percent * flexible / 100
        times.update(fixed)  # «سایر» آخر لیست قرار می‌گیرد

        self.store.create(times)
        self.show_results()

    def show_results(self):
        self.input_page.pack_forget()
        self.result_frame.show_times()
        self.result_frame.pack(expand=True, fill="both")

    def reset_all(self):
        self.store.reset()
        self.result_frame.clear_cards()
        self.result_frame.pack_forget()
        self.input_page.start_time_entry.delete(0, "end")
        self.input_page.end_time_entry.delete(0, "end")
        self.input_page.pack(expand=True, fill="both")


if __name__ == "__main__":
    if "--version" in sys.argv:
        print(f"SummerTimer {VERSION}")
        sys.exit()
    run = SummerTimer()
    run.mainloop()