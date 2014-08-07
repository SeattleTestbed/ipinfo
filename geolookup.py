#!/usr/bin/env python

# looks up the geoip data by iplist.   Both must be in the current dir 
# (unfortunately)
import sys
import os.path

scriptdir = os.path.dirname(sys.argv[0])

sys.path.append(scriptdir)

import pygeoip

geooutfd = file('geo.info','w')
countryoutfd = file('country.info','w')
latlongoutfd = file('latlong.info','w')

# This trickles the data out to surrounding areas.  We add the observed point
# in each neighboring area.
splatteroutfd = file('splatter.latlong.info','w')


def wraplat(latval):
  while latval<= -90:
    latval+= 180
  while latval> 90:
    latval-= 180
  return latval

def wraplong(longval):
  while longval<= -180:
    longval+= 360
  while longval> 180:
    longval-= 360
  return longval


geoipdb = pygeoip.GeoIP(scriptdir+"/GeoLiteCity.dat")

country_count = {}
latlongdict = {}
splatterdict = {}

for line in file('iplist'):
  ip = line.strip()
  record = geoipdb.record_by_addr(ip)

  if not record:
    record = {}

  if 'country_code' not in record or record['country_code'] is None:
    record['country_code'] = '??'

  if 'city' not in record or record['city'] is None:
    record['city'] = '??'

  if 'latitude' not in record:
    record['latitude'] = '??'

  if 'longitude' not in record:
    record['longitude'] = '??'

  print >> geooutfd, ip,record['latitude'],record['longitude'],record['country_code'].encode('utf-8'),record['city'].encode('utf-8')

  if record['country_code'] not in country_count:
    country_count[record['country_code']] = 0

  country_count[record['country_code']] += 1

  # skip if these aren't set...
  if record['latitude'] == '??' or record['longitude'] == '??':
    continue

  latitude = int(round(record['latitude']))
  longitude = int(round(record['longitude']))

  # in some rare cases, the values are set to 0 instead and should be skipped
  if latitude == 0 and longitude == 0:
    continue

  # populate lat/long map...
  if (latitude, longitude) not in latlongdict:
    latlongdict[(latitude,longitude)] = 0

  latlongdict[(latitude,longitude)] += 1

  # 60% in the corners, 100% in the center / mid edges
  for latoffset, longoffset in [(-1,-1),(-1,1),(1,-1),(1,1)]:
    thislat = latitude + latoffset
    thislong = longitude + longoffset
    if (thislat, thislong) not in splatterdict:
      splatterdict[(thislat,thislong)] = 0.0

    splatterdict[(thislat,thislong)] += .6 

  # Do the center, up, down, left, right
  for latoffset, longoffset in [(-1,0),(0,-1),(0,1),(1,0),(0,0)]:
    thislat = latitude + latoffset
    thislong = longitude + longoffset
    if (thislat, thislong) not in splatterdict:
      splatterdict[(thislat,thislong)] = 0.0

    splatterdict[(thislat,thislong)] += 1.0


sortedcountries = country_count.keys()[:]
sortedcountries.sort()

for countrycode in sortedcountries:
  print >> countryoutfd, countrycode, 'has',country_count[countrycode],'nodes.'


for latlong in latlongdict:
  print >> latlongoutfd, latlong[0], latlong[1], latlongdict[(latlong[0],latlong[1])]

for latlong in splatterdict:
  print >> splatteroutfd, latlong[0], latlong[1], int(round(splatterdict[(latlong[0],latlong[1])]))
