#!/usr/bin/python
from AriaPy import *
from ArNetworkingPy import *
import sys
import arm
#import armdemo
import time
import ptu


demogoal = 'kinovademo'

arm.init()
#arm.home()
arm.closefingers()
time.sleep(5)
arm.park()

Aria.init()

#armdemo.initptu()

clientbase = ArClientBase()
arrived = False

def statusChanged(status):
  print 'new status: ', status
  if status == 'Touring to '+demogoal:
    print 'arnl_armdemo Forcing gotoGoal'
    clientbase.requestOnceWithString('gotoGoal', demogoal)
    return
  elif(status == 'Arrived at '+demogoal):
    print 'arrived'
    arrived = True
    clientbase.requestOnce('stop')

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
    clientbase.requestOnce('tourGoals')
    return
  elif(status == 'Failed to get home'):
    # just keep trying
    clientbase.requestOnce('home')
  elif(status[0:6] == 'Failed'):
    # will tour to next goal, skip this one
    clientbase.requestOnce('tourGoals')
  else:
    arrived = False

if not clientbase.blockingConnect("goo.local", 7272):
  print "Could not connect to server at goo.local port 7272, exiting"
  Aria.exit(1);
print 'connected to goo.local. will do arm demo when we reach a goal named ' + demogoal

clientupdate = ArClientHandlerRobotUpdate(clientbase)
clientupdate.addStatusChangedCB(statusChanged)
clientupdate.requestUpdates(300)
clientbase.run()

arm.close()
