from tkinter import *
from tkinter.filedialog import askopenfilename
# from tkinter import ttk
from PIL import Image, ImageTk#import Image, ImageTk

if __name__ == "__main__":
    # https://stackoverflow.com/questions/34276663/tkinter-gui-layout-using-frames-and-grid

    root = Tk()
    root.title('Model Definition')
    #root.geometry('{}x{}'.format(460, 350))

    imgDisplay = Frame(root,bg='green')
    left = Frame(root, bg='blue', width=75)

    left.pack(side='left', fill='y', expand=False)
    imgDisplay.pack(side='right', fill='both', expand=True)

    imgCanvas = Canvas(imgDisplay)
    button = Button(left, text="Calibrate")

    file = '/home/yuanchueh/Documents/git/measureFromImage/car.png'
    image2show = ImageTk.PhotoImage(Image.open(file))
    height = image2show.height()
    width = image2show.width()
    imgCanvas.create_image(0,0,image=image2show,anchor="nw")

    left.grid_rowconfigure(0, weight=1)
    left.grid_columnconfigure(0, weight=1)
    imgCanvas.grid(row=0, column=0)
    button.grid(row=0, column=0, sticky='n')

    root.mainloop()
