import customtkinter as ctk
import sys 
import os
from reshap import text_to_persian

ctk.set_appearance_mode("dark")

def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


FONT = resource_path("Vazir.ttf")


class InputFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


        ctk.CTkLabel(self, text=text_to_persian("لطفا فیلد ها را پر کنید."), font=(FONT, 100), text_color="#00c8ff"
        ).pack(padx=120, pady=50)

        self.start_time_entry = ctk.CTkEntry(self, placeholder_text=text_to_persian("ساعت شروع را وارد کنید."),
        font=(FONT, 30), width=500, justify="center", height=60)
        self.start_time_entry.pack(pady=45)

        self.end_time_entry = ctk.CTkEntry(self, placeholder_text=text_to_persian("ساعت پایان را وارد کنید."),
        justify="center", font=(FONT, 30), width=500, height=60)
        self.end_time_entry.pack(pady=45)

        self.calculate_button = ctk.CTkButton(self, font=(FONT, 30), text=text_to_persian("محاسبه"))
        self.calculate_button.pack(pady=40)

class ResultFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text=text_to_persian("تایمر ها"), font=(FONT,100))


class SummerTimer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SummerTimer")

        self.input_page = InputFrame(self)
                
        self.input_page.pack(fill="both", expand=True)



if __name__ == "__main__":
    run = SummerTimer()
    run.mainloop()