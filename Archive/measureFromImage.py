from math import sqrt, pow
from PIL import Image, ImageDraw, ImageFont
<<<<<<< Updated upstream
# This function will be used to define the calibration value to convert between pixels and units.
# Acceptable units are SI (um, mm, cm, m, km) and English (in, ft, mi)
# Internally all units will be handled in mm and converted?

# def calibrateImage( startPoint, endPoint, calibUnit, calibValue ):
#    # Add both the parameters and return them."
#
#    total = arg1 + arg2
#    print("Inside the function : ", total)
#    return total;

def calculateDistance(startPoint, endPoint, calibValue):
    x = 0
    y = 1
    distancePixels = sqrt( pow(endPoint[x] - startPoint[x],2) + pow(endPoint[y] - startPoint[y],2) )
    distanceUnit = distancePixels * calibValue
    return distanceUnit;

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

calibUnit = 'mm'
calibUnitValue = calibUnitChoices.get(calibUnit)
p1 = [1,2]
p2 = [2,5]
dist = calculateDistance(p1, p2, calibUnitValue)
print('calulate distance' , dist, 'and the calibration unit is ', calibUnit, '. The conversion value is', calibUnitValue)
from os import sys
#from imutils import perspective
#from __future__ import print_function

# get an image
base = Image.open("car.png").convert('RGBA')
base# = Image.open('Pillow/Tests/images/lena.png').convert('RGBA')
print(base.format, base.size, base.mode)

#draw = ImageDraw.Draw(im)
#draw.line((0, 0) + im.size, fill=128)
#draw.line((0, im.size[1], im.size[0], 0), fill=128)
#del draw

#Draw lines
line = ImageDraw.Draw.line(10,10,75,75)


# make a blank image for the text, initialized to transparent text color
txt = Image.new('RGBA', base.size, (255,255,255,0))

# get a font
fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
# get a drawing context
d = ImageDraw.Draw(txt)

# draw text, half opacity
d.text((10,10), "Hello", font=fnt, fill=(255,255,255,128))
# draw text, full opacity
d.text((10,60), "World", font=fnt, fill=(255,255,255,255))

out = Image.alpha_composite(base, txt)
out = Image.alpha_composite(out, line)

out.show()

# write to stdout
#im.save(sys.stdout, "PNG")
