from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from PIL import Image, ImageTk#import Image, ImageTk

calibUnitChoices = {
    'um': 1e6,
    'mm': 1e3,
    'cm': 1e2,
    'm':  1,
    'km': 1e-3,
    'in': 39.3701,
    'ft': 3.28084,
    'mi': 0.000621371,
    }

def calibrateBtn():
    print('Button Pressed')
    calibBtn(gui, text='Calibrate', state=DISABLED)

if __name__ == "__main__":
    gui = Tk()
    gui.title('Measure Distance from Image - by Anatomy3D')
    # Create interface items
    calibVariable = StringVar(gui)
    calibVariable.set(calibUnitChoices['m'])

    #setting up a tkinter canvas with scrollbars
    # frame = Frame(gui, bd=2, relief=SUNKEN)
    # frame.grid_rowconfigure(0, weight=1)
    # frame.grid_columnconfigure(0, weight=1)
    # xscroll = Scrollbar(frame, orient=HORIZONTAL)
    # xscroll.grid(row=1, column=0, sticky=E+W)
    # yscroll = Scrollbar(frame)
    # yscroll.grid(row=0, column=1, sticky=N+S)
    # canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    # canvas.grid(row=0, column=0, sticky=N+S+E+W)
    # xscroll.config(command=canvas.xview)
    # yscroll.config(command=canvas.yview)

    content = ttk.Frame(gui, padding=(3,3,12,12))
    frame = ttk.Frame(content, borderWidth=5, relief='sunken', width=200, height=100)
    nameLbl = ttk.Label(content, text='Name')
    name = ttk.Entry(content)

    # calibMenu = OptionMenu(gui, calibVariable, *calibUnitChoices.keys()).grid(row=0)
    # calibLbl = Label(gui, text='TEST').grid(row=1)
    # calibBtn = Button(gui, text='Calibrate', command=calibrateBtn).grid(row=2)
    # frame.pack(fill=BOTH,expand=1)
    gui.mainloop()
    #adding the image
    # File = askopenfilename(parent=gui, initialdir="~/Documents/git/measureFromImage/",title='Choose an image.')
    file = '/home/yuanchueh/Documents/git/measureFromImage/car.png'
    #
    # # Load File into Pillow for Picture Dimension Sizes
    # # img = Image.open(file)
    # # img = img.convert('RGBA')
    # # height = img.height
    # # width = img.width
    # # mode = img.mode
    # # print (width, height, mode)
    # # img.show()
    # #
    # # Load Image into TKinter Interface
    # image = ImageTk.PhotoImage(Image.open(file))
    # height = image.height()
    # width = image.width()
    # # print(ht, wd)
    # canvas.create_image(0,0,image=image,anchor="nw")
    # canvas.config(scrollregion=canvas.bbox(ALL))
    # #
    # #
    # #
    # #
    # #
    # # #function to be called when mouse is clicked
    # # def printcoords(event):
    # #     #outputting x and y coords to console
    # #     print (event.x,event.y)
    # # #mouseclick event
    # # canvas.bind("<Button 1>",printcoords)
    # #
    # # gui.minsize(width=1024,height=600);
