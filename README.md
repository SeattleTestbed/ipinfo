ipinfo
======

The purpose of this project is to generates useful stats / maps from logs (often apache logs)

## UNDERSTANDING IP COUNT / DISTRIBUTION

This details how to gather IP statistics from apache logs.   We use this
in Seattle, but it is general and could potentially be used in other projects.

To use some utilities below, you will need to install PIL and pygeoip.   
You can use pip to install these libraries.

You are expected to have a directory with access.log* in it.   These files
should be *uncompressed* to start with.   

If needed, do: 
````
gunzip access.log*.gz 
````

Change into the directory with your access.log files.

Now run: 
````
initialparse *STRINGTOSEARCHFOR*
````

For example, for Seattle if we want to see software updates, we run: 
````
scripts/initalparse metainfo
````

To see all lines, use '.' as the argument.

This will (eventually) produce a file called ipdate.filtered.log that
has lines like this:
````
130.237.50.124 31/Jul/2014:12:26:07
192.41.136.219 31/Jul/2014:12:26:14
128.208.4.199 31/Jul/2014:12:26:16
````

## FIGURING OUT WHEN SYSTEMS FIRST CONTACTED YOUR SERVER

Run:
````
python scripts/findfirstentry.py
````

This creates a file 'firstseen' that contains the very first entry for
each IP address.   (A word count of this file will list the number of IPs.)

To see how many new nodes joined each day, use:
````
scripts/adoptionovertime
````

This creates a file datefirstseen which contains this information in the
following format:
````
30/Jul/2014 3
31/Jul/2014 5
1/Aug/2014 2
````


## GUESSING THE TYPE OF USER USING DNS REVERSE LOOKUP ON THE IP

First you need to generate a file called iplist.   To do this, type:
````
awk '{print $1}' firstseen | sort -u > iplist
````
NOTE: If this does not work because you do not have datefirstseen, try this:
````
awk '{print $1}' ipdate.filtered.log | sort -u > iplist
````

To look up the host names (VERY TIME CONSUMING, USE A SERVER AND LET IT RUN
OVERNIGHT), do:
````
scripts/dnslookup
````

This creates a file domainnamedata.   Note, if you need to stop and start
this due to your network being disconnected, etc., you can look for the
last valid line number (grep -n) and then use tail -n +lineno to find out
where to resume from.

**Before you do the above, remember to backup the iplist file**

For example:
````
tail domainnamedata
mv iplist fulliplist
grep -n 1.2.3.4 fulliplist  # use your last IP instead of 1.2.3.4. Reverse 
                            # DNS lookups have the octet order reversed!!!
tail -n +1234 fulliplist > iplist  # use the line number from grep above
                                   # instead of 1234
````
now resume...
````
scripts/dnslookup
````

Once this is complete, you will want to categorize those nodes.   To do so,
type:
````
python domaintypes.py
````

This will create a file summary.nodetypes.   It will also print out all of
the 'unknown' DNS names.   If possible, categorize popular but unique
strings in the script by editing the lists at the top.   This will improve
categorization of nodes for future runs.




## GETTING THE NODE LOCATIONS

To look up the geoip locations, you can run:
````
python scripts/geolookup.py
````

This will produce two files: geo.info and country.info.   The geo.info
file contains lines which have IP address, lat, lon, country code, and city.
Unknown lines are listed with ??

````
116.59.173.13 25.0392 121.525 TW Taipei
106.39.255.227 ?? ?? ?? ??
59.92.154.97 12.9832 77.5833 IN Bangalore
````

The country.info file will be sorted by country name and lists the number
of nodes in each country.   Unknown nodes are listed with ??.
For example:
````
?? has 4777 nodes.
A2 has 1 nodes.
AE has 19 nodes.
AL has 1 nodes.
AR has 10 nodes.
AT has 7133 nodes.
...
````

To get a list sorted by number of nodes, use:
````
sort -k3 -n country.info
````


This will also produce files that contain latitude, longitude, and count
information.   For example, latlong.info just contains the rounded lat
and long values w/ a count.   splatter is similar, but makes surrounding values
larger as well so the points aren't so missible when graphed.

## DRAWING LOCATION GRAPHS

NOTE: You need to have PIL installed to run this script!   Use pip / 
virtualenv to install it.

To plot latitude and longitude information use the drawmap.py script with
an argument for the latlong file to use.   For example use one of these:
````
python scripts/drawmap.py latlong.info  # fine points
````
or
````
python scripts/drawmap.py splatter.latlong.info  # large points
````

This script plots the location of points in two different ways.
First, it produces an ASCII map called 'map.ascii' where points are assigned
different values based upon the number of nodes:

  if value == 0: ' '
  if value <= 10: '.'
  if value <= 50: 'o'
  if value <= 250: 'O'
  if value <= 1250: '@'
  else: '*'

Each line has 360 characters (longitude) and there are 180 lines (latitude).
Example output can be found in scripts/examples/map.ascii.

It also produces a map.png file that contains the relevant points (plotted) and
transparent pixels for the remainder.   If you open this in a drawing program
(e.g. Preview on the Mac) and copy it over a world map (e.g. 
scripts/worldmap.jpg), this will plot the pixels in the right place.
The bar at the bottom indicates the meaning of the colors, with 1, 10, 100,
and 1000 signaling color transitions.   Example output can be found in
scripts/examples/map.png and scripts/examples/finishedmap.pdf

