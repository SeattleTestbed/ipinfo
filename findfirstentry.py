# This takes the ipdate.filtered.log (which must exist) and produces
# the first time each entry was observed.

outfo = file('firstseen','w')

seenips = set([])

for line in file('ipdate.filtered.log'):
  ip,date = line.split()
  if ip not in seenips:
    seenips.add(ip)
    print >> outfo, line.strip()
