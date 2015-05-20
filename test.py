
import kinovapy
import sys

if kinovapy.InitAPI() != kinovapy.NO_ERROR_KINOVA:
  print 'Error initializing Kinova API'
  sys.exit(1)

result = 0
result,deviceCount = kinovapy.GetDeviceCount()

print deviceCount
print result
print kinovapy.NO_ERROR_KINOVA
if result != kinovapy.NO_ERROR_KINOVA:
  print 'Error getting device count'
  sys.exit(2)

print 'Found %d devices' % (deviceCount)

for i in xrange(0, deviceCount):
  print 'Selecting arm #%d' % (i)
  kinovapy.SetActiveDeviceNum(i)

  status = kinovapy.QuickStatus()
  kinovapy.GetQuickStatus(status)

  kinovapy.MoveHome()
  kinovapy.InitFingers()

  actualPosition = kinovapy.AngularPosition()
  kinovapy.GetAngularCommand(actualPosition)
  pointToSend =  kinovapy.TrajectoryPoint()
  pointToSend.InitStruct()
  pointToSend.Position.Type = kinovapy.ANGULAR_POSITION
  pointToSend.LimitationsActive = 1

  # Set velocity limitation to 20 degrees per second for joint 1, 2 and 3.
  pointToSend.Limitations.speedParameter1 = 20.0

  # Set velocity limitation to 20 degrees per second for joint 4, 5 and 6
  pointToSend.Limitations.speedParameter2 = 20.0

  pointToSend.Position.Actuators.Actuator1 = actualPosition.Actuators.Actuator1 + 50
  pointToSend.Position.Actuators.Actuator2 = actualPosition.Actuators.Actuator2
  pointToSend.Position.Actuators.Actuator3 = actualPosition.Actuators.Actuator3
  pointToSend.Position.Actuators.Actuator4 = actualPosition.Actuators.Actuator4
  pointToSend.Position.Actuators.Actuator5 = actualPosition.Actuators.Actuator5
  pointToSend.Position.Actuators.Actuator6 = actualPosition.Actuators.Actuator6

  if status.RobotType == 0 or status.RobotType == 3:
    # If the robotic arm is a JACO or JACO2, we use those value for the fingers.
    pointToSend.Position.Fingers.Finger1 = 45.0
    pointToSend.Position.Fingers.Finger2 = 45.0
    pointToSend.Position.Fingers.Finger3 = 45.0
  elif status.RobotType == 1:
    # If the robotic arm is a MICO, we use those value for the fingers.
    pointToSend.Position.Fingers.Finger1 = 4500.0
    pointToSend.Position.Fingers.Finger2 = 4500.0
    pointToSend.Position.Fingers.Finger3 = 4500.0
  else:
    pointToSend.Position.Fingers.Finger1 = 0.0
    pointToSend.Position.Fingers.Finger2 = 0.0
    pointToSend.Position.Fingers.Finger3 = 0.0

  print "Sending trajectory" 

  # Add the point to the robot's FIFO
  kinovapy.SendAdvanceTrajectory(pointToSend)

  # Modify the position of the actuator #3
  pointToSend.Position.Actuators.Actuator1 = actualPosition.Actuators.Actuator1 - 100.0

  # Add the point to the robot's FIFO
  kinovapy.SendAdvanceTrajectory(pointToSend)

  # Modify the position of the actuator #1
  pointToSend.Position.Actuators.Actuator1 = actualPosition.Actuators.Actuator1 + 100.0

  # Add the point to the robot's FIFO
  kinovapy.SendAdvanceTrajectory(pointToSend)

  # Modify again the position of the actuator #3
  pointToSend.Position.Actuators.Actuator1 = actualPosition.Actuators.Actuator1 - 50

  # Add the point to the robot's FIFO
  kinovapy.SendAdvanceTrajectory(pointToSend)


print 'End of example'

kinovapy.CloseAPI()

