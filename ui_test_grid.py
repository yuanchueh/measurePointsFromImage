from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk#import Image, ImageTk

root = Tk()

content = ttk.Frame(root, padding=(3,3,12,12))
imageFrame = ttk.Frame(content, borderwidth=5, relief="sunken", width=200, height=100)
imagePILPath = '/home/yuanchueh/Documents/git/measureFromImage/car.png'
imagePIL = Image.open(imagePILPath)
image = ImageTK.PhotoImage(imagePIL)

# canvas = Canvas(imageFrame, height=200, width=200)
# basewidth = 150
# wpercent = (basewidth / float(image.size[0]))
# hsize = int((float(image.size[1]) * float(wpercent)))
# print(hsize)
# image = image.resize((basewidth, hsize), Image.ANTIALIAS)
# photo = ImageTk.PhotoImage(image)

# item4 = canvas.create_image(100, 80, image=photo)

# imagePIL = ImageTk.PhotoImage(Image.open(file))


# canvas.create_image(0,0,image=image,anchor="nw")
# canvas.config(scrollregion=canvas.bbox(ALL))


namelbl = ttk.Label(content, text="Name")
name = ttk.Entry(content)


onevar = BooleanVar()
twovar = BooleanVar()
threevar = BooleanVar()

onevar.set(True)
twovar.set(False)
threevar.set(True)

one = ttk.Checkbutton(content, text="One", variable=onevar, onvalue=True)
two = ttk.Checkbutton(content, text="Two", variable=twovar, onvalue=True)
three = ttk.Checkbutton(content, text="Three", variable=threevar, onvalue=True)
ok = ttk.Button(content, text="Okay")
cancel = ttk.Button(content, text="Cancel")

content.grid(column=0, row=0, sticky=(N, S, E, W))
canvas.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))

# canvas.grid(row=0, column=0, sticky=N+S+E+W)
namelbl.grid(column=3, row=0, columnspan=2, sticky=(N, W), padx=5)
name.grid(column=3, row=1, columnspan=2, sticky=(N, E, W), pady=5, padx=5)
one.grid(column=0, row=3)
two.grid(column=1, row=3)
three.grid(column=2, row=3)
ok.grid(column=3, row=3)
cancel.grid(column=4, row=3)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.rowconfigure(1, weight=1)

root.mainloop()
