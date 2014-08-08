# Author: Justin Cappos

# The purpose of this is to give a breakdown of 'types' of nodes.   This
# is things like university machines, home nodes, phones, etc.

# place where the output will go
outfd = file('summary.nodetypes','w')


# These will be processed in order, so the order is relevant.   If 'foo' is
# in the first one and 'bar' the second, 'foobar' will only be counted in the
# first.


dnsnamefilters = (
     {'message':'searchbots (not nodes).', 
            'patterns':['msnbot', 'googlebot']}, 
     {'message':'nodes in testbeds.',
            'patterns':['planet', 'lab']},
     {'message':'phones.',
            'patterns':['android', 'phone', 'tablet', 'ipad', 'mobile', 
                  'tmodns.net', 'cingular', 'vodafone', 'myvzw', 'tele']},
     {'message':'nodes in university networks.',
            'patterns': ['edu', 'uni', 'uvic.ca', 'tuwien.ac.at', 'umich', 
                  'kth.se', 'chalmers.se', 'ubc.ca', 'utoronto.ca', 'ethz.ch', 
                  'ust.hk', 'mpi-sws', 'ualberta.ca']},
     {'message':'definite home nodes.',
            'patterns': ['dsl', 'dial', 'dyn', 'cable', 'comcast', 'qwest', 
                  'pool', 'cust', 'broad', 'cox.net', 'netvigator', 'telering',
                  'rr.com', 'triband', 'surfer', 'wayport', 'highway.a1', 
                  'charter', 'verizon', 'singnet', 'kabel', 'pacenet-india']},
     {'message':'cloud nodes.',
            'patterns': ['amazonaws', 'gae.googleusercontent', 'cloud']},
     {'message':'research lab notes.',
            'patterns': ['research',]}
# sbcglobal and t-ipconnect.de (Deutsche Telekom) seem ambiguous home nodes.
)



domainnamedata = []


for line in file('domainnamedata'):
  domainnamedata.append(line.strip().lower().split()[-1])

print >> outfd, 'Started with',len(domainnamedata),'entries'


# Go through the filters and remove items we match
for dnsfilter in dnsnamefilters:
  thesematchingitems = []

  for dnsname in domainnamedata[:]:

    for thisfilter in dnsfilter['patterns']:
      if thisfilter in dnsname:
        try:
          domainnamedata.remove(dnsname)
        except ValueError:
          # duplicate entry...
          pass
        else:
          thesematchingitems.append(dnsname)
    

  print >> outfd, len(thesematchingitems),dnsfilter['message']


print >> outfd, len(domainnamedata),'remaining entries.'

print 'unknown nodes:'
print domainnamedata

print 'summary data written to "summary.nodetypes"'
