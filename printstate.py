
import kinovapy
import sys

if kinovapy.InitAPI() != kinovapy.NO_ERROR_KINOVA:
  print 'Error initializing Kinova API'
  sys.exit(1)

deviceCount = kinovapy.GetNumDevices()

if deviceCount < 0:
  print 'Error getting device count'
  sys.exit(2)

print >> sys.stderr, 'Found %d devices' % deviceCount

for i in xrange(0, deviceCount):
  print >> sys.stderr, 'Selecting arm #%d' % (i)
  kinovapy.SetActiveDeviceNum(i)

  clientconfig = kinovapy.ClientConfigurations()
  kinovapy.GetClientConfigurations(clientconfig)
  print >> sys.stderr,  clientconfig.ClientID
  if clientconfig.Laterality == kinovapy.LEFTHAND:
    print >> sys.stderr,  'LEFTHAND'
  else:
    print >> sys.stderr,  'RIGHTHAND'

  status = kinovapy.QuickStatus()
  kinovapy.GetQuickStatus(status)
  kinovapy.InitFingers()

  print >> sys.stderr,  status

  actualPosition = kinovapy.AngularPosition()
  kinovapy.GetAngularCommand(actualPosition)


  print >> sys.stderr,  actualPosition

  if clientconfig.Laterality == kinovapy.LEFTHAND:
    print '  \'left\': ',
  else:
    print '  \'right\': ',
  print actualPosition.Actuators,
  if i == (deviceCount-1): # last
    print ''
  else:
    print ','
    


kinovapy.CloseAPI()

