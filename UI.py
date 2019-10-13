from tkinter import *
from tkinter import ttk

a = []

class Root(Tk):

    def __init__(self):
        super(Root, self).__init__()
        self.title("Order")
        self.minsize(640, 400)
        #self.configure(background = '#4D4D4D')

        self.initUI()
    
    def clickMe(self):

        a.append(self.name.get())
        
        print(len(a))
        self.label.configure(text = len(a))
        self.label.place(x = 100, y = 300)

        r = 100
        t = 0
        i = len(a) - 1
        while i>=0 and t<11:
            
            self.label = ttk.Label(self, text = a[i])
            self.label.place(x = 350, y = r)
            r += 20
            i = i - 1
            t = t + 1
    
    def initUI(self):

        self.name = StringVar()

        self.label = ttk.Label(self, text = "Enter your order")
        self.label.place(x = 50, y = 50)

        self.textbox = ttk.Entry(self, width = 20, textvariable = self.name)
        self.textbox.place(x = 50, y = 80)


        self.label = ttk.Label(self, text = "Total orders:")
        self.label.place(x = 50, y = 200)

        self.label = ttk.Label(self, text = len(a))
        self.label.place(x = 100, y = 300)


        self.button = ttk.Button(self, text = "Send order", command = self.clickMe)
        self.button.place(x = 50, y = 110)

        self.label1 = ttk.Label(self, text = "Recent orders")
        self.label1.place(x = 350, y = 50)


root = Root()
root.mainloop()