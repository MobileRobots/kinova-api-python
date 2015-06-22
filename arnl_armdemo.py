from AriaPy import *
from ArNetworkingPy import *
import sys
import arm
import armdemo
import time
import ptu

demogoal = 'Arm Demo'


arm.init()
arm.home()
arm.closefingers()
time.sleep(5)
arm.park()

Aria.init()

armdemo.initptu()

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
    armdemo.demo()
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

clientupdate = ArClientHandlerRobotUpdate(clientbase)
clientupdate.addStatusChangedCB(statusChanged)
clientupdate.requestUpdates(300)
clientbase.run()

arm.close()
