from tkinter import *
from tkinter.filedialog import askopenfilename
# from tkinter import ttk
from PIL import Image, ImageTk#import Image, ImageTk

# The basic interface is laid out. Not functionality yet.


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
    calibBtn(root, text='Calibrate', state=DISABLED)

def loadImage():
    filePath = askopenfilename(parent=root, initialdir='~/Documents/git/measureFromImage/',title='Choose an image.')
    canvas.create_image(0,0,image=image,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))


if __name__ == '__main__':
    root = Tk()
    root.title('Measure Distance from Image - by Anatomy3D')
    root.geometry('{}x{}'.format(460, 350))
    # root.geometry('{}x{}'.format(460, 350))
    # Create interface items
    calibVariable = StringVar(root)
    calibVariable.set(calibUnitChoices['m'])

    #Create main frame containers
    frmTools = Frame(root, bg='cyan', width=100, height=200, padx=3, pady=3)
    frmCanvas = Frame(root, bg='magenta', width=200, height=200, padx=3, pady=3)
    frmBottom = Frame(root, bg='yellow', width=200, height=15, padx=3, pady=3)

    # Layout all of the main containers
    root.grid_rowconfigure(0, weight=1) #Elastic top row
    root.grid_rowconfigure(1, weight=0)
    root.grid_columnconfigure(0, weight=0)
    root.grid_columnconfigure(1, weight=1) #Elastic second column

    frmTools.grid(rowspan=2, column=0, sticky='ns')
    frmCanvas.grid(row=0,column=1, sticky='nsew')
    frmBottom.grid(row=1,columnspan=2, sticky='ew')

    # Create widgets for the tools frame
    btnWidth = 8
    strFilePath = Entry(frmTools, background='pink', width=btnWidth*2)
    btnFilePath = Button(frmTools, background='yellow', text='Select File', width=btnWidth)
    btnLoadImage = Button(frmTools, background='yellow', text='Load Image', width=btnWidth, command=loadImage)
    btnUndo = Button(frmTools, background='yellow', text='Undo', width=btnWidth)
    btnRedo = Button(frmTools, background='yellow', text='Redo', width=btnWidth)
    btnCalibrate = Button(frmTools, text='Calibrate', width=btnWidth)
    lblUnit = Label(frmTools, text='Set Unit Length')
    strUnitLength = Entry(frmTools, width=10)

    #set drop down menu
    calibUnitVar = StringVar(root)
    # calibUnitVar.set = calibUnitChoices[1].keys()
    # calibUnitVar.set = 'Choose an Option'
    drpUnitSelect = OptionMenu(frmTools, calibUnitVar, *calibUnitChoices.keys())
    calibUnitVar.set(calibUnitChoices['m'])

    btnCapture = Button(frmTools, text='Capture', width=btnWidth)
    strSetScale = Entry(frmTools, text=100, width=btnWidth)
    btnSetScale = Button(frmTools, text='Apply', width=btnWidth)
    btnExport = Button(frmTools, text='Export Image', width=btnWidth)
    btnReset = Button(frmTools, text='Reset', width=btnWidth)
    lstCollected = Listbox(frmTools, width=btnWidth*2, height=50)

    # Layout widgets for tools frames
    strFilePath.grid(row=0, column=0, columnspan=2, sticky='ew')
    btnFilePath.grid(row=2, column=0)
    btnLoadImage.grid(row=2, column=1)
    btnUndo.grid(row=4, column=0, pady=15)
    btnRedo.grid(row=4, column=1)
    lblUnit.grid(row=6, column=0)
    strUnitLength.grid(row=8, column=0, sticky='e')
    drpUnitSelect.grid(row=8, column=1, sticky='ew')
    btnCalibrate.grid(row=10, column=0, columnspan=2, pady=10)
    btnCapture.grid(row=12, column=0, columnspan=2, pady=25)
    strSetScale.grid(row=14, column=0, sticky='e')
    btnSetScale.grid(row=14, column=1, sticky='w')
    btnExport.grid(row=18, column=0)
    btnReset.grid(row=18, column=1)
    lstCollected.grid(row=20, column=0, columnspan=2, sticky='ew', padx=3, pady=3)

    # Create Widgets for information panel
    btnStatus = Label(frmBottom, text="Temporary, No Data to Show!!!")

    # Layout Widgets for information panel
    btnStatus.grid(row=0,column=0, sticky='w')

    # Create Widgets for canvas
    xscroll = Scrollbar(frmCanvas, orient=HORIZONTAL)
    yscroll = Scrollbar(frmCanvas, orient=VERTICAL)
    canvas = Canvas(frmCanvas, bg='red', bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)#, width=200, height=100)
    canvas.create_line(0,0,200,100)
    canvas.create_line(0,100,200,0,fill='black', dash=(4,4))

    # Layout Widgets for Canvas
    frmCanvas.grid_rowconfigure(0, weight=1)
    frmCanvas.grid_columnconfigure(0, weight=1)

    canvas.grid(row=0, column=0, sticky='nsew')
    xscroll.grid(row=1, column=0, sticky='ew')
    yscroll.grid(row=0, column=1, sticky='ns')

    # Configure Widgets for Canvas
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)

    # Adding the image to the Canvas
    # filePath = askopenfilename(parent=root, initialdir='~/Documents/git/measureFromImage/',title='Choose an image.')
    # filePath = '/home/yuanchueh/Documents/git/measureFromImage/car.png'

    # Load Image into TKinter Interface
    # image = ImageTk.PhotoImage(Image.open(filePath))
    # height = image.height()
    # width = image.width()
    # canvas.create_image(0,0,image=image,anchor="nw")
    # canvas.config(scrollregion=canvas.bbox(ALL))

    # Loop GUI
    root.minsize(width=600,height=400);
    root.mainloop()
