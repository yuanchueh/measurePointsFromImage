from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk#import Image, ImageTk

def __init__(self,master):
    master.minsize(width=1024, height=800)

if __name__ == "__main__":
    root = Tk()

    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)

    #adding the image
    # File = askopenfilename(parent=root, initialdir="~/Documents/git/measureFromImage/",title='Choose an image.')
    file = '/home/yuanchueh/Documents/git/measureFromImage/car.png'

    # Load File into Pillow for Picture Dimension Sizes
    img = Image.open(file)
    img = img.convert('RGBA')
    height = img.height
    width = img.width
    mode = img.mode
    print (width, height, mode)
    # img.show()

    # Load Image into TKinter Interface
    image = ImageTk.PhotoImage(Image.open(file))
    ht = image.height()
    wd = image.width()
    print(ht, wd)
    canvas.create_image(0,0,image=image,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    #function to be called when mouse is clicked
    def printcoords(event):
        #outputting x and y coords to console
        print (event.x,event.y)
    #mouseclick event
    canvas.bind("<Button 1>",printcoords)

    root.minsize(width=1024,height=600);
    root.mainloop()
