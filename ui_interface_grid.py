from tkinter import *
from tkinter.filedialog import askopenfilename
# from tkinter import ttk
#Some links to research
#https://stackoverflow.com/questions/40990623/tkinter-and-pillow-operations
#https://stackoverflow.com/questions/42440278/moving-and-resize-image-canvas-object-in-tkinter
#https://stackoverflow.com/questions/29367990/what-is-the-difference-between-image-resize-and-image-thumbnail-in-pillow-python
#https://stackoverflow.com/questions/24745857/python-pillow-how-to-scale-an-image


from PIL import Image, ImageTk#import Image, ImageTk

if __name__ == "__main__":
    # https://stackoverflow.com/questions/34276663/tkinter-gui-layout-using-frames-and-grid

    root = Tk()
    root.title('Model Definition')
    #root.geometry('{}x{}'.format(460, 350))

    # create all of the main containers
    frameImage = Frame(root,bg='green')
    frameLeft = Frame(root, bg='blue', width=75)

    # layout all of the main containers
    frameImage.grid(row=0, column=1, sticky='ns')#, sticky="nsew")
    frameLeft.grid(row=0, column=0)#, weight=1)
    #Layout the toolFrame
    #'frameLeft.pack(side='left', fill='y', expand=False)
    #'frameImage.pack(side='right', fill='both', expand=True)

    imgCanvas = Canvas(frameImage)
    buttonCalibrate = Button(frameLeft, text="Calibrate")

    file = '/home/yuanchueh/Documents/git/measureFromImage/car.png'
    image2show = ImageTk.PhotoImage(Image.open(file))

    # scale to fit
    maxsize = (1028, 1028)
    image2show.resize([256,512],PIL.Image.ANTIALIAS) # resizes to 256x512 exactly
    # imageScaled = image2show.thumbnail(maxsize, PIL.Image.ANTIALIAS)

    height = image2show.height()
    width = image2show.width()
    imgCanvas.create_image(0,0,image=image2show,anchor="center")

    imgCanvas.grid(row=0, column=0)
    buttonCalibrate.grid(row=0, column=0, sticky='n')

    root.mainloop()
