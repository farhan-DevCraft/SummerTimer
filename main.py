import customtkinter as ctk
from gui import TimerCard
from reshape import text_to_persian
from variable_file import *
from storage import TimerStore

ctk.set_appearance_mode("dark")


class InputFrame(ctk.CTkFrame):
    def __init__(self, master, cal):
        super().__init__(master)


        ctk.CTkLabel(self, text=text_to_persian("لطفا فیلد ها را پر کنید."), font=(FONT, 30), text_color="#ffbd39"
        ).pack()

        self.start_time_entry = ctk.CTkEntry(self, placeholder_text=text_to_persian("ساعت شروع را وارد کنید."),
        font=(FONT, 30), width=500, justify="center", height=60)
        self.start_time_entry.pack(pady=45, padx=50)

        self.end_time_entry = ctk.CTkEntry(self, placeholder_text=text_to_persian("ساعت پایان را وارد کنید."),
        justify="center", font=(FONT, 30), width=500, height=60)
        self.end_time_entry.pack(pady=45, padx=50)

        self.calculate_button = ctk.CTkButton(self, font=(FONT, 30), text=text_to_persian("محاسبه"), command=cal)
        self.calculate_button.pack(pady=40)

class ResultFrame(ctk.CTkFrame):
    def __init__(self, master, store):
        super().__init__(master)
        self.store = store
        self.cards = []
        ctk.CTkLabel(self, text=text_to_persian("تایمر ها"), font=(FONT, 100), text_color="#00ff2a"
        ).pack(padx=100, pady=30)
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(expand=True)

    def show_times(self):
        for name in self.store.names():
            card = TimerCard(self.cards_frame, name, self.store)
            card.pack(side="left", padx=10, pady=10, expand=True)
            self.cards.append(card)
        self.tick()

    def tick(self):
        self.store.check_finished()
        for card in self.cards:
            card.refresh()
        self.after(500, self.tick)


class SummerTimer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SummerTimer")

        self.store = TimerStore()
        self.input_page = InputFrame(self, self.calculate)
        self.result_frame = ResultFrame(self, self.store)

        if self.store.has_data():      # ادامه از جلسه‌ی قبل
            self.show_results()
        else:
            self.input_page.pack(expand=True, fill="both")

    def calculate(self):
        self.end_time = self.input_page.end_time_entry.get()
        self.start_time = self.input_page.start_time_entry.get()

        self.free_time = int(self.end_time) - int(self.start_time)
        free_seconds = self.free_time * 3600

        self.store.create({
            name: task_percentage * free_seconds / 100
            for name, task_percentage in task_time.items()
        })
        self.show_results()

    def show_results(self):
        self.input_page.pack_forget()
        self.result_frame.show_times()
        self.result_frame.pack(expand=True, fill="both")


if __name__ == "__main__":
    run = SummerTimer()
    run.mainloop()