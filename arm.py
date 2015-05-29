
import kinovapy
import sys
import time


# TODO: rename to "arms" 
# TODO: Add cartesian (plus hand orientation), force and velocity position modes.
# TODO: rework to allow chunked sequences of trajectories.  Wait for each chunk
# to complete, but queue all trajectories within chunk.
# TODO: add protection zone for mounting column etc.
# TODO: get force sensing info

# Initial values, changed later to map arm index to left/right based on
# Laterality field .
armID = { 'left': 0, 'right': 1 }
armName = {0: 'left', 1: 'right' }

oldoldparkstate = {
  'left': [ 244.5, 309.0, 134.3, 7.4, 152.3, 96.3 ],  
  'right': [294.3, 315.2, 134.3, 170.4, 202.2, 76.8 ] 
}

openfingerstate = [10, 10, 10]
closedfingerstate = [5000, 5000, 5000]

oldparkstate = {
    'right': [271.378693, 312.187500, 136.985291, 219.204559, 2.863636, 77.795456],
    'left': [264.926483, 309.609375, 130.643387, 351.068207, 7.227273, 96.068184]
}

parkstate = {

#  'left':  [80.551468, 54.790625, 235.753677, 202.840912, 6.409091, 285.886383] ,
#  'right':  [280.661774, 293.531250, 118.400734, 151.772736, 358.840912, 290.250000] 

  'left':  [92.426468, 45.609375, 235.147064, 204.272736, 6.409091, 286.159088] ,
  'right':  [280.863983, 312.281250, 119.558823, 150.545456, 357.204559, 290.454559] 
}


preparkstate = { 
  'left': [56.360294, 54.796875, 227.607315, 207.613647, 28.722046, 286.295471], 
  'right': [317.715881, 293.638519, 122.578148, 122.033569, 349.920776, 289.153442]
}


deviceCount = 0
initialized = False

def init():
  global initialized
  global deviceCount
    
  if initialized:
    return True
  print 'arm.py: Initializing Arms...'

  if kinovapy.InitAPI() != kinovapy.NO_ERROR_KINOVA:
    print 'arm.py: Error initializing Kinova API'
    return False

  deviceCount = kinovapy.GetNumDevices()

  if deviceCount < 0:
    print 'arm.py: Error getting device count'
    return False

  print 'arm.py: Found %d devices' % (deviceCount)

  
  for i in xrange(0, deviceCount):
    kinovapy.SetActiveDeviceNum(i)
    clientconfig = kinovapy.ClientConfigurations()
    kinovapy.GetClientConfigurations(clientconfig)
    print 'clientid=%s. laterality is %d. LEFTHAND=%d RIGHTHAND=%d' % (clientconfig.ClientID, clientconfig.Laterality, kinovapy.LEFTHAND, kinovapy.RIGHTHAND)
    # Laterality affects home position.  It does not invert an y of the joint position
    # coordinates. Not sure yet if it changes cartesian coordinate system or
    # anything else.
    if clientconfig.Laterality == kinovapy.LEFTHAND:
      s = 'left'
    else:
      s = 'right'
    print 'arm.py: Laterality of %d is %s ' % (i, s)
    armID[s] = i
    armName[i] = s

  initialized = True
  return True

def home(armid = None):
  if armid == None:
    for i in xrange(0, deviceCount):
      print 'arm.py: Homing arm #%d' % (i)
      home(i)
      time.sleep(2)
      if armName[i] == 'left':
        print 'moving left out of the way'
        movejoints(i, [42.022060, 149.859375, 285.330872, 125.045456, 245.568192, 285.681824])
      else:
        print 'moving right out of the way'
        movejoints(i, [308.713226, 207.890625, 67.996323, 174.818192, 245.522736, 288.477295] )
      time.sleep(3)
  else:
      kinovapy.SetActiveDeviceNum(armid)
      kinovapy.MoveHome()

def init_fingers(armid = None):
  if armid == None:
    for i in xrange(0, deviceCount):
      init_fingers(i)
  else:
    print 'arm.py: Initializing fingers on arm #%d' % (armid)
    kinovapy.SetActiveDeviceNum(armid)
    kinovapy.InitFingers()


def movearms(jointstate):
  if not init():
    return False
  global deviceCount
  for i in xrange(0, deviceCount):
    armname = armName[i]
    print 'arm.py: movearms: Moving %s arm #%d' % (armname, i)
    j = jointstate[armname]
    fingername = armname+'fingers'
    fingerstate = None
    if fingername in jointstate.keys():
      fingerstate = jointstate[fingername]
    movejoints(i, j, fingerstate)

def movejoints(i, j, fingerstate = None):
  if not init():
    return False
  else:
    if i == 'left':
      i = armID['left']
    elif i == 'right':
      i = armID['right']
    kinovapy.SetActiveDeviceNum(i)

    pointToSend =  kinovapy.TrajectoryPoint()
    pointToSend.InitStruct()
    pointToSend.Position.Type = kinovapy.ANGULAR_POSITION
    pointToSend.LimitationsActive = 1

    # Set velocity limitation to 20 degrees per second for joint 1, 2 and 3.
    pointToSend.Limitations.speedParameter1 = 20.0

    # Set velocity limitation to 30 degrees per second for joint 4, 5 and 6
    pointToSend.Limitations.speedParameter2 = 30.0

    pointToSend.Position.Actuators.Actuator1 = j[0]
    pointToSend.Position.Actuators.Actuator2 = j[1]
    pointToSend.Position.Actuators.Actuator3 = j[2]
    pointToSend.Position.Actuators.Actuator4 = j[3]
    pointToSend.Position.Actuators.Actuator5 = j[4]
    pointToSend.Position.Actuators.Actuator6 = j[5]

    if fingerstate != None:
      if fingerstate == 'open':
        pointToSend.Position.Fingers.Finger1 = openfingerstate[0]
        pointToSend.Position.Fingers.Finger2 = openfingerstate[1]
        pointToSend.Position.Fingers.Finger3 = openfingerstate[2]
      elif fingerstate == 'close':
        pointToSend.Position.Fingers.Finger1 = closedfingerstate[0]
        pointToSend.Position.Fingers.Finger2 = closedfingerstate[1]
        pointToSend.Position.Fingers.Finger3 = closedfingerstate[2]
      else:
        pointToSend.Position.Fingers.Finger1 = fingerstate[0]
        pointToSend.Position.Fingers.Finger2 = fingerstate[1]
        pointToSend.Position.Fingers.Finger3 = fingerstate[2]

    # Add the point to the robot's FIFO
    print 'arm.py: Sending trajectory' 
    kinovapy.SendAdvanceTrajectory(pointToSend)
    #kinovapy.SendBasicTrajectory(pointToSend)


def setfingers(f):
  global deviceCount
  for i in xrange(0, deviceCount):
    print 'fingers: Selecting arm #%d' % (i)
    kinovapy.SetActiveDeviceNum(i)
    kinovapy.InitFingers()
    actualPosition = kinovapy.AngularPosition()
    kinovapy.GetAngularCommand(actualPosition)
    pointToSend =  kinovapy.TrajectoryPoint()
    pointToSend.InitStruct()
    pointToSend.Position.Type = kinovapy.ANGULAR_POSITION
    pointToSend.Position.Actuators.Actuator1 = actualPosition.Actuators.Actuator1 
    pointToSend.Position.Actuators.Actuator2 = actualPosition.Actuators.Actuator2
    pointToSend.Position.Actuators.Actuator3 = actualPosition.Actuators.Actuator3
    pointToSend.Position.Actuators.Actuator4 = actualPosition.Actuators.Actuator4
    pointToSend.Position.Actuators.Actuator5 = actualPosition.Actuators.Actuator5
    pointToSend.Position.Actuators.Actuator6 = actualPosition.Actuators.Actuator6

    pointToSend.Position.Fingers.Finger1 = f[0]
    pointToSend.Position.Fingers.Finger2 = f[1]
    pointToSend.Position.Fingers.Finger3 = f[2]

    # Add the point to the robot's FIFO
    kinovapy.SendAdvanceTrajectory(pointToSend)

def openfingers():
  setfingers(openfingerstate)

def closefingers():
  setfingers(closedfingerstate)


def close():
  global initialized
  print 'arm.py: End of example'
  kinovapy.CloseAPI()
  initialized = False

def park():
  print 'arm.py: prepark'
  movearms(preparkstate)
  time.sleep(5)
  print 'arm.py: park'
  movearms(parkstate)
  print 'arm.py: closefingers'
  time.sleep(6)
  closefingers()

if __name__ == '__main__':
  init()
  status = kinovapy.QuickStatus()
  kinovapy.GetQuickStatus(status)
  print status
  close()

