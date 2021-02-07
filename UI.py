import tkinter as tk

import Content

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_crafts()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command= self.destroy)
        self.quit.pack(side="bottom")

    def create_crafts(self):
        self.one = CommonCraftElement(self)

    def say_hi(self):
        print("hi there, everyone!")

    def destroy_all(self):
        # self.one.destroy()
        self.master.destroy()

class CommonCraftElement(tk.Frame):
    def __init__(self, master=None, craft=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_craft_UI(craft)


    def create_craft_UI(self, craft=None):

        if craft is None:
            self.text = tk.Label(self, text="EKSDEE")
            self.text.pack()

            photo = tk.Image("ex.png")
            self.aug_button = tk.Button(self, text="LUL", )



            self.aug_button.pack()







root = tk.Tk()
app = Application(master=root)
app.mainloop()