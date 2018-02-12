from PIL import Image, ImageDraw, ImageFont
from os import sys
#from imutils import perspective
#from __future__ import print_function

# get an image
base = Image.open("car.png").convert('RGBA')
base# = Image.open('Pillow/Tests/images/lena.png').convert('RGBA')
print(im.format, im.size, im.mode)

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
