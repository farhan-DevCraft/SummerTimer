import customtkinter as ctk


class InputFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(self, text="input frame").pack()
        
class SummerTimer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SummerTimer")

        self.input_page = InputFrame(self)
                
        self.input_page.pack(fill="both", expand=True)



if __name__ == "__main__":
    run = SummerTimer()
    run.mainloop()