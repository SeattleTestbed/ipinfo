
# The purpose of this is to give a breakdown of 'types' of nodes.   This
# is things like university machines, home nodes, phones, etc.

outfd = file('summary.nodetypes','w')

# search bots to remove
botnamelist = ['msnbot', 'googlebot']

testbednamelist = ['planet', 'lab']

phonenamelist = ['android', 'phone', 'tablet', 'ipad', 'mobile', 'tmodns.net', 
      'cingular', 'vodafone', 'myvzw', 'tele']


edunamelist = ['edu', 'uni', 'uvic.ca', 'tuwien.ac.at', 'umich', 'kth.se', 
      'chalmers.se', 'ubc.ca', 'utoronto.ca', 'ethz.ch', 'ust.hk', 'mpi-sws',
      'ualberta.ca']

homenamelist = ['dsl', 'dial', 'dyn', 'cable', 'comcast', 'qwest', 'pool',
      'cust', 'broad', 'cox.net', 'netvigator', 'telering', 'rr.com', 
      'triband', 'surfer', 'wayport', 'highway.a1', 'charter', 'verizon',
      'singnet', 'kabel', 'pacenet-india']

cloudnamelist = ['amazonaws', 'gae.googleusercontent', 'cloud']

researchlablist = ['research', ]

# sbcglobal and t-ipconnect.de (Deutsche Telekom) seem ambiguous home nodes.

domainnamedata = []


for line in file('domainnamedata'):
  domainnamedata.append(line.strip().lower().split()[-1])

print >> outfd, 'Started with',len(domainnamedata),'entries'


searchbots = []
for dnsname in domainnamedata[:]:
  for botname in botnamelist:
    if botname in dnsname:
      try:
        domainnamedata.remove(dnsname)
      except ValueError:
        # duplicate entry...
	pass
      else:
        searchbots.append(dnsname)
    
print >> outfd, len(searchbots),'searchbots (not nodes).'


testbednodes = []
for dnsname in domainnamedata[:]:
  for testbedname in testbednamelist:
    if testbedname in dnsname:
      try:
        domainnamedata.remove(dnsname)
      except ValueError:
        # duplicate entry...
	pass
      else:
        testbednodes.append(dnsname)
    
print >> outfd, len(testbednodes),'nodes in testbeds.'

phonenodes = []
for dnsname in domainnamedata[:]:
  for phonename in phonenamelist:
    if phonename in dnsname:
      try:
        domainnamedata.remove(dnsname)
      except ValueError:
        # duplicate entry...
	pass
      else:
        phonenodes.append(dnsname)
    
print >> outfd, len(phonenodes),'phones.'

edunodes = []
for dnsname in domainnamedata[:]:
  for eduname in edunamelist:
    if eduname in dnsname:
      try:
        domainnamedata.remove(dnsname)
      except ValueError:
        # duplicate entry...
	pass
      else:
        edunodes.append(dnsname)

print >> outfd, len(edunodes),'nodes in university networks.'
    
homenodes = []
for dnsname in domainnamedata[:]:
  for homename in homenamelist:
    if homename in dnsname:
      try:
        domainnamedata.remove(dnsname)
      except ValueError:
        # duplicate entry...
	pass
      else:
        homenodes.append(dnsname)
    

print >> outfd, len(homenodes),'definite home nodes.'


cloudnodes = []
for dnsname in domainnamedata[:]:
  for cloudname in cloudnamelist:
    if cloudname in dnsname:
      try:
        domainnamedata.remove(dnsname)
      except ValueError:
        # duplicate entry...
	pass
      else:
        cloudnodes.append(dnsname)
    

print >> outfd, len(cloudnodes),'cloud nodes.'


researchnodes = []
for dnsname in domainnamedata[:]:
  for researchname in researchlablist:
    if researchname in dnsname:
      try:
        domainnamedata.remove(dnsname)
      except ValueError:
        # duplicate entry...
	pass
      else:
        researchnodes.append(dnsname)
    

print >> outfd, len(researchnodes),'research lab nodes.'




print >> outfd, len(domainnamedata),'remaining entries.'

print 'unknown nodes:'
print domainnamedata

print 'summary data written to "summary.nodetypes"'
