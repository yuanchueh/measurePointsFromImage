from tkinter import *
from tkinter.filedialog import askopenfilename
from math import sqrt, pow
from PIL import Image, ImageDraw, ImageFont, ImageTk
from time import sleep
# The basic interface is laid out. Not functionality yet.
# Additional Resources
#   https://stackoverflow.com/questions/5501192/how-to-display-picture-and-get-mouse-click-coordinate-on-it
#   https://stackoverflow.com/questions/8590234/capturing-x-y-coordinates-with-python-pil
# v4 - working interface, but functions dont really work.
# v5 - adding full functionality. Reset works. Must run calibration first before capturing points. Capture button set as toggle and only works when calibration has been completed. Calibration equations are not implemented.
# v6 - converted status variables to a single status dictionary. Combined functions further. Moved variables into Reset function
# v7 - Need to add zoom factor.

#To Do: Get calculated numbers to be correct.

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
    calibUnitVar.set('m')
    strFilePath.delete(0, END)
    strFilePath.insert(0,'/home/yuanchueh/Documents/git/measureFromImage/car.png')
    canvas.delete("all")
    lstCollected.delete(0, END)
    lblStatus.configure(text='Interface Reset')

def calibrate():
    global status
    lblStatus.configure(text='Button Pressed - Select 2 calibration points on the image of a known distance.')
    status['Calibrated'] = False
    status['CollectPoints'] = False
    btnCalibrate.configure(state = DISABLED)
    #   canvas.create_line(0,100,200,0,fill='black', dash=(4,4))

def calculatePixelDistance(startPoint, endPoint):
    #indices
    x = 0
    y = 1
    #calculate distance
    distanceInPixels = sqrt( pow(endPoint[x] - startPoint[x],2) + pow(endPoint[y] - startPoint[y],2) )
    return distanceInPixels;

def getCoordinates(event):
    #outputting x and y coords to console
    global xPrev, yPrev, status
    status['clickCounter'] += 1
    # lblStatus.configure(text='Coordinates [x,y]: [{},{}], and you have clicked {} times'.format(event.x,event.y, status['clickCounter']))
    if status['Calibrated'] == False and status['CollectPoints'] == False: #Perform Calibration
        lblStatus.configure(text='In calibration.')
        # sleep(2)
        if status['clickCounter']%2 == 1:#First Click
            xPrev = event.x
            yPrev = event.y
        else:#Second calibration click. Calculate the distance and value.
            calibratedLengthPixels = calculatePixelDistance([xPrev, yPrev], [event.x, event.y])
            # handles.unitConverter = C/Cp; %Use in the form Xp/X = Yp/Y where Xp is pixel length X, Yp is pixel length Y, X is known real length, Y is unknown real length
            # %Y = Yp*(X/Xp) = Yp*unitConvert
            calibratedLengthKnown = 25
            calibrationUnit = 1e3
            calibrationMultiplier = calibratedLengthKnown/calibrationUnit
            lblStatus.configure(text='Calibration Complete.')
            lstCollected.insert(0,'Calibration Done {}'.format(calibrationMultiplier))
            status['Calibrated'] = True
            btnCapture.configure(state=ACTIVE)
    elif status['Calibrated'] == True and status['CollectPoints'] == True: #The calibration is complete so now we can collect points.
        if status['clickCounter']%2 == 1:#First Click
            xPrev = event.x
            yPrev = event.y
        else:#Second Click
            canvas.create_line(xPrev,yPrev, event.x, event.y)

            calibUnit = calibUnitVar.get()
            calibUnitValue = calibUnitChoices.get(calibUnit)

            calibValue = strUnitLength.get()
            distance = calculateDistance([xPrev, yPrev], [event.x, event.y], 1.54)
            iterater = status['clickCounter']/2
            # outputString = '#{0:.0f}-{0:.3f}'.format(iterater, distance)
            outputString = '#{0:.0f} - {1:.3f}'.format(iterater, distance)
            canvas.create_text(xPrev-15,yPrev, text=outputString)
            lstCollected.insert(0,outputString)
            # Need to update history list from here.
    else:
        status['clickCounter'] = 0
        lblStatus.configure(text='No Action!!! --> Click Count={}'.format(status['clickCounter']))
        return
    radius = 2.5
    color='green'
    lblStatus.configure(text='Coordinates [x,y]: [{},{}], and you have clicked {} times'.format(event.x,event.y, status['clickCounter']))
    canvas.create_oval(event.x-radius,event.y-radius,event.x+radius, event.y+radius, fill=color)
    # return

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
    filePath = askopenfilename(parent=root, initialdir='~/Documents/git/measureFromImage/',title='Choose an image.')

    # Load Image into TKinter Interface
    image = ImageTk.PhotoImage(Image.open(filePath))
    canvas.image=image
    height = image.height()
    width = image.width()
    canvas.create_image(0,0,image=canvas.image,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))
    btnLoadImage.configure(state=DISABLED)

def setScale():
    # global filePath
    filePath = '/home/yuanchueh/Documents/git/measureFromImage/car.png'
    imageScaled = Image.open(filePath)
    imageScaled = imageScaled.resize((250,250))
    canvas.image=imageScaled
    # image = ImageTk.PhotoImage(image=imageScaled)
    canvas.create_image(0,0,image=canvas.image,anchor="nw")
    # scaleFactor = strSetScale.get()
    lblStatus.configure(text='Scale Factor: {}'.format(scaleFactor))
    # image =
    # canvas.scale()

def calculateDistance(startPoint, endPoint, calibValue):
    #indices
    x = 0
    y = 1
    #calculate distance
    distanceInPixels = sqrt( pow(endPoint[x] - startPoint[x],2) + pow(endPoint[y] - startPoint[y],2) )
    distanceReal = distanceInPixels * calibValue
    return distanceReal;

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

    #set drop down menu
    calibUnitVar = StringVar()
    # calibUnitVar.set = calibUnitChoices[1].keys()
    # calibUnitVar.set = 'Choose an Option'
    drpUnitSelect = OptionMenu(frmTools, calibUnitVar, *calibUnitChoices.keys())

    btnCapture = Button(frmTools, text='Capture', width=btnWidth, state=DISABLED, relief='raised', command=captureState)
    strSetScale = Entry(frmTools, width=btnWidth)
    lblSetScale = Label(frmTools, text='Set Image Scale Factor (%)')
    btnSetScale = Button(frmTools, text='Apply', width=btnWidth, command=setScale)
    btnExport = Button(frmTools, text='Export Image', width=btnWidth)
    btnReset = Button(frmTools, text='Reset', width=btnWidth, command=resetInterface)
    lstCollected = Listbox(frmTools, width=btnWidth*2, height=50)

    # Layout widgets for tools frames
    strFilePath.grid(row=0, column=0, columnspan=2, sticky='ew')
    # btnFilePath.grid(row=2, column=0)
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
