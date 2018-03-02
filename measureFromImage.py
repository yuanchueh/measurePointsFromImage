from math import sqrt, pow
from PIL import Image, ImageDraw, ImageFont
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
