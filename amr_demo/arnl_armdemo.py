#!/usr/bin/python
from AriaPy import *
from ArNetworkingPy import *
import sys
import arm
#import armdemo
import time
import ptu

# Change these if neccesary
demogoal = 'Arm Demo'
hostname = '192.168.0.32'

# Initialize both arms. See arm.py.
arm.init()
#arm.home()
arm.closefingers()
time.sleep(5)
arm.park()

Aria.init()

# Initialize PTU, see armdemo.py and ptu.py.
armdemo.initptu()

arnlServerConn = ArClientBase()
arrived = False

def statusChanged(status):
  print 'new status: ', status
  if status == 'Touring to '+demogoal:
    print 'arnl_armdemo Forcing gotoGoal'
    arnlServerConn.requestOnceWithString('gotoGoal', demogoal)
    return
  elif(status == 'Arrived at '+demogoal):
    print 'arrived'
    arrived = True
    arnlServerConn.requestOnce('stop')

    # do arm demo here:
    print '------- Arm Demo --------'
    #armdemo.demo()

    closed = [8200, 4600, 4000]
    arm.movejoints('right', 
	#     [282.352936, 316.359375, 281.636017, 248.386368, 13.431819, 356.045471] ,
 [282.297791, 316.312500, 242.647064, 198.886368, 39.613636, 40.840912],
	     closed
	)
    time.sleep(13)
    arm.openfingers()
    time.sleep(10)
    arm.setfingers(closed)
    arm.movejoints('right',
        [280.863983, 312.281250, 119.558823, 150.545456, 357.204559, 290.454559] ,
	     closed
	)
    time.sleep(5)


    print '-------------------------'

    # Resume tour:
    #time.sleep(3)
    #arm.park()
    time.sleep(3)
    #arm.closefingers()
    arnlServerConn.requestOnce('tourGoals')
    return
  elif(status == 'Failed to get home'):
    # just keep trying
    arnlServerConn.requestOnce('home')
  elif(status[0:6] == 'Failed'):
    # will tour to next goal, skip this one
    arnlServerConn.requestOnce('tourGoals')
  else:
    arrived = False

if not arnlServerConn.blockingConnect(hostname, 7272):
  print "Could not connect to server at %s port 7272, exiting" % (hostname)
  Aria.exit(1);
print 'connected to goo.local. will do arm demo when we reach a goal named ' + demogoal

# Monitor changes in ARNL server status
clientupdate = ArClientHandlerRobotUpdate(arnlServerConn)
clientupdate.addStatusChangedCB(statusChanged)
clientupdate.requestUpdates(300)
arnlServerConn.run()

arm.close()
