# Author: Justin Cappos
#
# This program takes files of the form: lat long count
# and produces a drawing of the resulting information.   It is assumed that
# the lat goes from -90 to 90 and the long from -179 to 180.

import sys

import Image, ImageDraw

def georgbarep(origvalue):
  r,b,g = georgbrep(origvalue)
  return (r,g,b,255)

def georgbrep(origvalue):
  value = origvalue
  if value <= 0:
    raise InternalError('value '+str(value)+' is not allowed for count')
  if value == 1:
    return (192,192,192)

  if value <= 10:
    return (0,0,135+(12*value))
  value = value / 10

  if value <= 10:
    return (0,135+(12*value),0)
  value = value / 10

  if value <= 10:
    return (135+(12*value),0,0)

  value = value / 10
  if value <= 10:
    return (200+(5*value),200+(5*value), 0)

  print 'color overflow!', origvalue
  return (255,255,255)

#  if value <= 300:
#    return (0,250-(value-50),value-50)
#  if value <= 1000:
#    return ((value) / 4, 0, (1000-(value-300))/ 4)
#  if value > 1300:
#    print 'color overflow!', value
#    return (255,255,255)


def geoasciirep(value):
  if value <= 0:
    raise InternalError('value '+str(value)+' is not allowed for count')
  if value <= 10:
    return '.'
  if value <= 50:
    return 'o'
  if value <= 250:
    return 'O'
  if value <= 1250:
    return '@'
  return '*'

asciioutfd = open('map.ascii','w')

geolocfn = sys.argv[1]

imageoutname = 'map.png'
imageobj = Image.new('RGBA',(360,180))
#imageobj = Image.new('RGBA',(360,200))
drawobj = ImageDraw.Draw(imageobj)

geodict = {}
for line in file(geolocfn):
  thislat, thislong, thiscount = line.split()
  thislat = int(thislat)
  thislong = int(thislong)
  thiscount = int(thiscount)

  geodict[(thislat,thislong)] = thiscount



for y in xrange(90,-90,-1):
  for x in xrange(180, -180,-1):
    if (y,x) not in geodict:
      asciioutfd.write(' ')
      drawobj.point((x+180,90-y),(0,0,0,0))
    else:
      asciioutfd.write(geoasciirep(geodict[(y,x)]))
      drawobj.point((x+180,90-y),georgbarep(geodict[(y,x)]))

  asciioutfd.write('\n')


val = 1
# draw the legend...
for x in range(5,355):
  val = val *1.025
  drawobj.point((x,175),georgbarep(int(val)))
  drawobj.point((x,176),georgbarep(int(val)))
  drawobj.point((x,177),georgbarep(int(val)))

drawobj.line((4,174,355,174),(0,0,0,255))
drawobj.line((4,174,4,178),(0,0,0,255))
drawobj.line((4,178,355,178),(0,0,0,255))
drawobj.line((355,174,355,178),(0,0,0,255))

del drawobj

imageobj.save('map.png','PNG')
