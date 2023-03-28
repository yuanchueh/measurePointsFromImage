from tkinter import *
from tkinter.filedialog import askopenfilename
from math import sqrt, pow
from PIL import Image, ImageDraw, ImageFont, ImageGrab, ImageTk, PngImagePlugin
#from time import sleep
import time
from tk_tools import SmartOptionMenu
import os

# The basic interface is laid out. Not functionality yet.
# Additional Resources
#   https://stackoverflow.com/questions/5501192/how-to-display-picture-and-get-mouse-click-coordinate-on-it
#   https://stackoverflow.com/questions/8590234/capturing-x-y-coordinates-with-python-pil
# v4 - working interface, but functions dont really work.
# v5 - adding full functionality. Reset works. Must run calibration first before capturing points. Capture button set as toggle and only works when calibration has been completed. Calibration equations are not implemented.
# v6 - converted status variables to a single status dictionary. Combined functions further. Moved variables into Reset function
# v7 - Need to add zoom factor.

#The calibration unit selector was originally meant to serve as a conversion factor, but the program has been simplified to only use this as a notation of what the unit currently is. The conversion factor is not currently used.
calibUnitChoices = {
    'um': 1e6,
    'mm': 1e3,
    'cm': 1e2,
    'm':  1,
    'km': 1e-3,
    'in': 39.3701,
    'ft': 3.28084,
    'mi': 0.000621371}

def resetInterface():
    global status
    #Initialize Variable List
    status = {
        'Calibrated': False,
        'CollectPoints': True,
        'ImageLoaded':False,
        'clickCounter':0}
    btnLoadImage.configure(state=ACTIVE)
    btnUndo.configure(state=DISABLED)
    btnRedo.configure(state=DISABLED)
    btnCalibrate.configure(state=ACTIVE)
    btnCapture.configure(state=DISABLED, relief='raised')
    btnSetScale.configure(state=ACTIVE)
    btnExport.configure(state=DISABLED)
    btnReset.configure(state=ACTIVE)
    #strSetScale.configure(state=DISABLED)

    # Set widget defaults for tools frames
    strUnitLength.delete(0, END)
    strUnitLength.insert(0,'1.000')
    strSetScale.delete(0, END)
    strSetScale.insert(0,'100')
    # calibUnitVar.set('m')
    strFilePath.delete(0, END)
    strFilePath.insert(0,'')
    canvas.delete("all")
    lstCollected.delete(0, END)
    lblStatus.configure(text='Interface Reset')

def calibrate():
    global status
    lblStatus.configure(text='Button Pressed - Select 2 calibration points on the image of a known distance.')
    status['Calibrated'] = False
    status['CollectPoints'] = False
    btnCalibrate.configure(state = DISABLED)
    btnExport.configure(state=ACTIVE)
    #   canvas.create_line(0,100,200,0,fill='black', dash=(4,4))

def calculateDistance(startPoint, endPoint, *calibValue):
    # handles.unitConverter = C/Cp; %Use in the form Cp/C = Yp/Y where:
    # Cp is pixel length C
    # Yp is pixel length Y
    # C is known real length
    # Y is unknown real length
    # Y = Yp*(C/Cp) = Yp*unitConvert
    # distancePixels = Yp = calculatePixelDistance([xPrev, yPrev], [event.x, event.y])#, 1.54)
    # distance = Yp*(C/Cp)*convertUnitBase

    #indices
    x = 0
    y = 1
    #calculate distance
    distanceInPixels = sqrt( pow(endPoint[x] - startPoint[x],2) + pow(endPoint[y] - startPoint[y],2) )
    if calibValue: #If the calibration value is sent then convert to known length. Otherwise just send the pixel distance as measured
        distance = distanceInPixels * calibValue[0]
    else:
        distance = distanceInPixels
    return distance

def getCoordinates(event):
    #outputting x and y coords to console
    global xPrev, yPrev, status, calibratedLengthKnown, calibratedLengthPixels
    status['clickCounter'] += 1
    if status['Calibrated'] == False and status['CollectPoints'] == False: #Perform Calibration
        color='red'
        lblStatus.configure(text='In calibration.')
        if status['clickCounter']%2 == 1:#First Click
            xPrev = event.x
            yPrev = event.y
        else:#Second calibration click. Calculate the distance and value.
            canvas.create_line(xPrev,yPrev, event.x, event.y)
            calibratedLengthPixels = calculateDistance([xPrev, yPrev], [event.x, event.y])
            calibratedLengthKnown = float(strUnitLength.get())
            outputString = 'Calibration - {0:.3f}'.format(calibratedLengthKnown)
            canvas.create_text(xPrev-15,yPrev, text=outputString, fill='red', justify = RIGHT)
            lblStatus.configure(text='Calibration Complete.')
            status['Calibrated'] = True
            btnCapture.configure(state=ACTIVE)
    elif status['Calibrated'] == True and status['CollectPoints'] == True: #The calibration is complete so now we can collect points.
        color='green'
        if status['clickCounter']%2 == 1:#First Click
            xPrev = event.x
            yPrev = event.y
        else:#Second Click
            canvas.create_line(xPrev,yPrev, event.x, event.y)
            distance = calculateDistance([xPrev, yPrev], [event.x, event.y], calibratedLengthKnown/calibratedLengthPixels)
            iterater = status['clickCounter']/2
            outputString = '#{0:.0f} - {1:.3f}'.format(iterater, distance)
            canvas.create_text(xPrev-15,yPrev, text=outputString)
            lstCollected.insert(0,outputString)
    else:
        status['clickCounter'] = 0
        lblStatus.configure(text='No Action!!! --> Click Count={}'.format(status['clickCounter']))
        return
    radius = 2.5
    lblStatus.configure(text='Coordinates [x,y]: [{},{}], and you have clicked {} times'.format(event.x,event.y, status['clickCounter']))
    canvas.create_oval(event.x-radius,event.y-radius,event.x+radius, event.y+radius, fill=color)

def captureState():
    # This will run when the capture button is pressed. It uses the capture as a toggle button.
    # When the button is not toggled points clicked will not be captured.
    global status
    if btnCapture.config('relief')[-1] == 'sunken':
        btnCapture.config(relief="raised")
        status['CollectPoints'] = False
    else:
        btnCapture.config(relief="sunken")
        status['CollectPoints'] = True

def loadImage():
    #rootDirectory = '~/Documents/git/measureFromImage/'
    global filePath
    filePath = askopenfilename(parent=root, title='Choose an image.')
    strFilePath.insert(0,filePath)
    # Load Image into TKinter Interface
    image = ImageTk.PhotoImage(Image.open(filePath))
    canvas.image=image
    height = image.height()
    width = image.width()
    canvas.create_image(0,0,image=canvas.image,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))
    btnLoadImage.configure(state=DISABLED)

def setScale():
    #Sets the size of the image. A way to make it bigger or smaller in the viewport.
    #It does not currently move points that have been set with the image.
    
    scaleFactor = int(strSetScale.get())
    imageOriginal = Image.open(filePath)
    imageOriginalPhoto = ImageTk.PhotoImage(imageOriginal)
    origH = imageOriginalPhoto.height()
    origW = imageOriginalPhoto.width()
    scaleHeight = int(origH * scaleFactor / 100)
    scaleWidth = int(origW * scaleFactor / 100)
    imageScaled = imageOriginal.resize((scaleWidth, scaleHeight))
    canvas.image = ImageTk.PhotoImage(imageScaled)
    canvas.create_image(0, 0, image=canvas.image, anchor="nw")
    lblStatus.configure(text='Scale Factor: {}, (H, W): ({}, {})'.format(scaleFactor, origH, origW))
    
def save_widget_as_image(widget, file_name):
    ImageGrab.grab(bbox=(
        widget.winfo_rootx(),
        widget.winfo_rooty(),
        widget.winfo_rootx() + widget.winfo_width(),
        widget.winfo_rooty() + widget.winfo_height()
    )).save(file_name)
    
def exportImage():
    # global canvas
    # PIL image can be saved as .png .jpg .gif or .bmp file (among others)
    outputFolder = os.path.dirname(filePath)
    outputFilename = time.strftime('%Y%m%d%H%M%S_outputimage.png')
    x=root.winfo_rootx()
    y=root.winfo_rooty()
    x1=x+canvas.winfo_width()
    y1=y+canvas.winfo_height()
    # filename = filedialog.asksaveasfilename(initialdir = "C:/Users/desktop.ini",
                                              # title = "Select file",
                                              # filetypes = (("PNG files","*.png"),("All files","*.*")))
    #ImageGrab.grab().crop((x,y,x1,y1)).save(outputFilename, format="PNG")
    #ImageGrab.grab((x,y,x1,y1)).save(outputFilename)
    save_widget_as_image(canvas,outputFilename)

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
    #btnFilePath = Button(frmTools, background='yellow', text='Select File', width=btnWidth)
    btnLoadImage = Button(frmTools, text='Load Image', width=btnWidth, command=loadImage)
    btnUndo = Button(frmTools, text='Undo', width=btnWidth, state=DISABLED)
    btnRedo = Button(frmTools, text='Redo', width=btnWidth, state=DISABLED)
    btnCalibrate = Button(frmTools, text='Calibrate', width=btnWidth, state=ACTIVE, command=calibrate)
    lblUnit = Label(frmTools, text='Set Unit Length')
    strUnitLength = Entry(frmTools, width=10)
    drpUnitSelect = SmartOptionMenu(frmTools, list(calibUnitChoices.keys()),'m')
    btnCapture = Button(frmTools, text='Capture', width=btnWidth, state=DISABLED, relief='raised', command=captureState)
    strSetScale = Entry(frmTools, width=btnWidth)
    lblSetScale = Label(frmTools, text='Set Image Scale Factor (%)')
    btnSetScale = Button(frmTools, text='Apply', width=btnWidth, command=setScale)
    btnExport = Button(frmTools, text='Export Image', width=btnWidth, command=exportImage)
    btnReset = Button(frmTools, text='Reset', width=btnWidth, command=resetInterface)
    lstCollected = Listbox(frmTools, width=btnWidth*2, height=50)

    # Layout widgets for tools frames
    strFilePath.grid(row=0, column=0, columnspan=2, sticky='ew')
    btnLoadImage.grid(row=2, column=1)
    btnUndo.grid(row=4, column=0, pady=15)
    btnRedo.grid(row=4, column=1)
    lblUnit.grid(row=6, column=0)
    strUnitLength.grid(row=8, column=0, sticky='e')
    drpUnitSelect.grid(row=8, column=1, sticky='ew')
    btnCalibrate.grid(row=10, column=0, columnspan=2, pady=10)
    btnCapture.grid(row=12, column=0, columnspan=2, pady=25)
    lblSetScale.grid(row=13, column=0, columnspan=2)
    strSetScale.grid(row=14, column=0, sticky='e')
    btnSetScale.grid(row=14, column=1, sticky='w')
    btnExport.grid(row=18, column=0)
    btnReset.grid(row=18, column=1)
    lstCollected.grid(row=20, column=0, columnspan=2, sticky='ew', padx=3, pady=3)

    # Create Widgets for information panel
    lblStatus = Label(frmBottom, text="Temporary, No Data to Show!!!")

    # Layout Widgets for information panel
    lblStatus.grid(row=0,column=0, sticky='w')

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

    # Set widget defaults for tools frames
    resetInterface()

    #mouseclick event
    canvas.bind("<Button 1>",getCoordinates)
    xPrev = 0
    yPrev = 0

    # Loop GUI
    root.minsize(width=600,height=400);
    root.mainloop()
