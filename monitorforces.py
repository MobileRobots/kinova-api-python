
import kinovapy
import sys
import time

if kinovapy.InitAPI() != kinovapy.NO_ERROR_KINOVA:
  print 'Error initializing Kinova API'
  sys.exit(1)

deviceCount = kinovapy.GetNumDevices()

if deviceCount < 0:
  print 'Error getting device count'
  sys.exit(2)

print 'Found %d devices' % deviceCount


print 'Homing each arm...'
for i in xrange(0, deviceCount):
	kinovapy.SetActiveDeviceNum(0)
	kinovapy.MoveHome()
	kinovapy.InitFingers()

cmd = kinovapy.TrajectoryPoint()
cmd.InitStruct
cmd.Position.Type = kinovapy.CARTESIAN_POSITION
cmd.Position.CartesianPosition.X = 0.50
cmd.Position.CartesianPosition.Y = 0.50

print 'Moving each arm 50 cm out (X) and 50 cm forward (Y)...'
for i in xrange(0, deviceCount):
	kinovapy.SetActiveDeviceNum(i)
	kinovapy.SendAdvanceTrajectory(cmd)

while True:
	for i in xrange(0, deviceCount):
	  kinovapy.SetActiveDeviceNum(i)
	  clientconfig = kinovapy.ClientConfigurations()
	  kinovapy.GetClientConfigurations(clientconfig)
	  forceinfo = kinovapy.ForcesInfo()
	  kinovapy.GetForcesInfo(forceinfo)

          print 'arm #%d' % (i),
	  if clientconfig.Laterality == kinovapy.LEFTHAND:
	    print ' (left): ',
	  else:
	    print ' (right): ',
	  print forceinfo
	time.sleep(0.25)
	  

kinovapy.CloseAPI()

