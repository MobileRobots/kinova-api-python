
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
  print >> sys.stderr, '\nSelecting arm #%d' % (i)
  kinovapy.SetActiveDeviceNum(i)

  clientconfig = kinovapy.ClientConfigurations()
  kinovapy.GetClientConfigurations(clientconfig)
  print >> sys.stderr,  'ClientID="%s"' % (clientconfig.ClientID)
  if clientconfig.Laterality == kinovapy.LEFTHAND:
    print >> sys.stderr,  'Laterality is LEFTHAND'
  else:
    print >> sys.stderr,  'Laterality is RIGHTHAND'

  print >> sys.stderr, 'Getting quick status...'
  status = kinovapy.QuickStatus()
  kinovapy.GetQuickStatus(status)

#  print >> sys.stderr, 'Init Fingers...'
#  kinovapy.InitFingers()

  print >> sys.stderr, 'Status: ',
  print >> sys.stderr,  status

  print >> sys.stderr, 'Getting angular position...',
  jointPosition = kinovapy.AngularPosition()
  kinovapy.GetAngularPosition(jointPosition)
  #kinovapy.GetAngularCommand(jointPosition)
  print >> sys.stderr,  jointPosition

  print >> sys.stderr, 'Getting cartesian position...',
  position = kinovapy.CartesianPosition()
  kinovapy.GetCartesianPosition(position)
  print >> sys.stderr, position

  print >> sys.stderr, 'Getting force info...',
  forceinfo = kinovapy.ForcesInfo()
  kinovapy.GetForcesInfo(forceinfo)
  print >> sys.stderr, forceinfo

  

  if clientconfig.Laterality == kinovapy.LEFTHAND:
    print '  \'left\': { '
  else:
    print '  \'right\': { '
  
  print '    \'joints\': ',
  print jointPosition.Actuators,
  print ', '
  print '    \'pos\': ',
  print position.Coordinates
  print '  }',
  if i == (deviceCount-1): # last
    print ''
  else:
    print ','
    


kinovapy.CloseAPI()

