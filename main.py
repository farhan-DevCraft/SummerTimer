import customtkinter as ctk


class SummerTimer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SummerTimer")
        self.geometry("800x600")
        self.resizable(False, False)

if __name__ == "__main__":
    run = SummerTimer()
    run.mainloop()