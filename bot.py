import tkinter as tk
from PIL import ImageGrab, ImageTk
import mss 
import mss.tools
import time


class GUI(tk.Tk):
    def __init__(self):
        print('Select the borders of the pool table on your screen, be as precise as possible')
        input('Press Enter to continue...')
        super().__init__()
        self.withdraw()
        self.attributes('-fullscreen', True)

        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill='both',expand=True)

        image = ImageGrab.grab()
        self.image = ImageTk.PhotoImage(image)
        self.photo = self.canvas.create_image(0,0,image=self.image,anchor='nw')

        self.x, self.y = 0, 0
        self.rect, self.start_x, self.start_y = None, None, None
        self.deiconify()

        self.canvas.tag_bind(self.photo,'<ButtonPress-1>', self.on_button_press)
        self.canvas.tag_bind(self.photo,'<B1-Motion>', self.on_move_press)
        self.canvas.tag_bind(self.photo,'<ButtonRelease-1>', self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='white')

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        global bbox
        bbox = self.canvas.bbox(self.rect)
        self.attributes('-fullscreen', False)
        self.destroy()
        return bbox

selection_rectangle = GUI()

selection_rectangle.mainloop()
time.sleep(0.2)

class Bot():
    def __init__(self):
        self.table_coords = bbox
        self.region = {'top': self.table_coords[0], 
                       'left': self.table_coords[1], 
                       'width': self.table_coords[2] - self.table_coords[0], 
                       'height': self.table_coords[3] - self.table_coords[1]}
        print('region :', self.region)

    def get_table(self):
        with mss.mss() as sct:
                return sct.grab(self.region)


botte = Bot()
img = botte.get_table()