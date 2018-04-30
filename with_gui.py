import tkinter as tk

from rooms import room1


class RoomGui(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Laspirateur')
        self.data = room1
        self.height = len(self.data)
        self.width = len(self.data[0])
        self.aspi = 1, 2
        self.active = True
        for i, row in enumerate(self.data):
            for j, cell in enumerate(row):
                if cell == 'M':
                    color = 'blue'
                else:
                    color = 'yellow'
                tk.Frame(self, height=20, width=20, background=color).grid(row=i, column=j)
        tk.Frame(self, height=20, width=20, background='red').grid(row=self.aspi[0], column=self.aspi[1])

    def move_aspi(self, x, y):
        tk.Frame(self, height=20, width=20, background='yellow').grid(row=self.aspi[0], column=self.aspi[1])
        self.aspi = x, y
        tk.Frame(self, height=20, width=20, background='red').grid(row=self.aspi[0], column=self.aspi[1])

    def mainloop(self, n=0):
        while self.active:
            self.update()

    def destroy(self):
        self.active = False


if __name__ == '__main__':
    app = RoomGui()
    app.mainloop()
