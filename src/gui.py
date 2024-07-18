from customtkinter import *

class GraphicalUserInterface:
    def __init__(self) -> None:
        self.app = CTk()
        self.app.geometry("700x500")

    
    def run(self):
        self.app.mainloop()


app = GraphicalUserInterface()
app.run()