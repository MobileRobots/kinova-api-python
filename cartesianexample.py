#!/usr/bin/python
import kinovapy
import sys

if kinovapy.InitAPI() != kinovapy.NO_ERROR_KINOVA:
  print 'Error initializing Kinova API'
  sys.exit(1)

deviceCount = kinovapy.GetNumDevices()

if deviceCount < 0:
  print 'Error getting device count'
  sys.exit(2)

pointToSend = kinovapy.TrajectoryPoint()
pointToSend.InitStruct()
pointToSend.Position.HandMode = kinovapy.POSITION_MODE
pointToSend.Position.Type = kinovapy.CARTESIAN_POSITION
pointToSend.LimitationsActive = 1
pointToSend.Limitations.speedParameter1 = 0.08
pointToSend.Limitations.speedParameter2 = 0.7

# Position wil be set interactively below
#pointToSend.Position.CartesianPosition.X = -0.30
#pointToSend.Position.CartesianPosition.Y = 0.30
#pointToSend.Position.CartesianPosition.Z = 0.30
#pointToSend.Position.CartesianPosition.ThetaX = 1.55
#pointToSend.Position.CartesianPosition.ThetaY = 1.02
#pointToSend.Position.CartesianPosition.ThetaZ = -0.03
pointToSend.Position.Fingers.Finger1 = 45.0
pointToSend.Position.Fingers.Finger2 = 45.0
pointToSend.Position.Fingers.Finger3 = 45.0

print 'Found %d devices' % deviceCount


for i in xrange(0, deviceCount):
  print '\nSelecting arm #%d' % (i)
  kinovapy.SetActiveDeviceNum(i)
  #print 'Homing...'
  #kinovapy.MoveHome()
  #print 'Init Fingers...'
  #kinovapy.InitFingers()
  position = kinovapy.CartesianPosition()
  kinovapy.GetCartesianPosition(position)
  pointToSend.Position.CartesianPosition = position.Coordinates

print ''

def input_position(name, curr, max):
  try:
    x = float(raw_input('move %s (meters), if any? ' % name))
    if abs(x) > max:
      raise ValueError('Position value too large')
    print 'Setting new %s %f' % (name, x)
    return x
    pointToSend.Position.CartesianPosition.X = x
  except ValueError:
    print 'using previous.'
  return curr

while True:
  for i in xrange(0, deviceCount):
    print '\nSelecting arm #%d' % (i)
    kinovapy.SetActiveDeviceNum(i)

    clientconfig = kinovapy.ClientConfigurations()
    kinovapy.GetClientConfigurations(clientconfig)
    print 'ClientID="%s"' % (clientconfig.ClientID)
    if clientconfig.Laterality == kinovapy.LEFTHAND:
      print 'Laterality is LEFTHAND'
    else:
      print 'Laterality is RIGHTHAND'

    status = kinovapy.QuickStatus()
    kinovapy.GetQuickStatus(status)

    print 'Status: ',
    print  status

    print 'Current cartesian position: ',
    position = kinovapy.CartesianPosition()
    kinovapy.GetCartesianPosition(position)
    print position

    pointToSend.Position.CartesianPosition.X = input_position('X', pointToSend.Position.CartesianPosition.X, 2)
    pointToSend.Position.CartesianPosition.Y = input_position('Y', pointToSend.Position.CartesianPosition.Y, 2)
    pointToSend.Position.CartesianPosition.Z = input_position('Z', pointToSend.Position.CartesianPosition.Z, 2)

    print 'Moving to position (%f, %f, %f)...' % ( pointToSend.Position.CartesianPosition.X, pointToSend.Position.CartesianPosition.Y, pointToSend.Position.CartesianPosition.Z )
    #kinovapy.SendAdvanceTrajectory(pointToSend)

    pointToSend.Position.ThetaX = input_position('ThetaX', pointToSend.Position.CartesianPosition.ThetaX, 360)
    pointToSend.Position.ThetaY = input_position('ThetaY', pointToSend.Position.CartesianPosition.ThetaY, 360)
    pointToSend.Position.ThetaZ = input_position('ThetaZ', pointToSend.Position.CartesianPosition.ThetaZ, 360)
    print 'Moving to orientation (%f, %f, %f)...' % ( pointToSend.Position.CartesianPosition.ThetaX, pointToSend.Position.CartesianPosition.ThetaY, pointToSend.Position.CartesianPosition.ThetaZ )
    kinovapy.SendAdvanceTrajectory(pointToSend)

    print '------------'


kinovapy.CloseAPI()

