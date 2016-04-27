 
# Example of cartesian velocity control.
# This program uses a pygame window to get keyboard events. click on the small
# window that opens and use arrow keys, page up/down, to move, and number keys to select
# multiple arms.

import kinovapy
import sys
#import pygame


if kinovapy.InitAPI() != kinovapy.NO_ERROR_KINOVA:
  print 'Error initializing Kinova API'
  sys.exit(1)

deviceCount = kinovapy.GetNumDevices()
print 'deviceCount', deviceCount
if deviceCount < 0:
  print 'Error getting device count'
  sys.exit(2)

for i in xrange(0, deviceCount):
  print 'Selecting arm #%d' % (i)
  kinovapy.SetActiveDeviceNum(i)
  kinovapy.MoveHome()
  kinovapy.InitFingers()
  status = kinovapy.QuickStatus()
  kinovapy.GetQuickStatus(status)
  print status



# TODO set up exclusion zone

#pygame.init()
#screen = pygame.display.set_mode((320, 240))
#pygame.key.set_repeat() # disable repeat


pointToSend = kinovapy.TrajectoryPoint()
pointToSend.InitStruct()
pointToSend.Position.Type = kinovapy.CARTESIAN_VELOCITY

while True:
  #evts = pygame.event.get()
  #if pygame.QUIT in evts:
  #  sys.exit(0)
  #keys = pygame.key.get_pressed()

  if keys[pygame.K_0]:
    kinovapy.SetActiveDeviceNum(0)
    print 'selected arm 0'
  elif keys[pygame.K_1]:
    kinovapy.SetActiveDeviceNum(1)
    print 'selected arm 1'
  

  if keys[pygame.K_UP]:
    pointToSend.Position.CartesianPosition.Y = 0.08
  elif keys[pygame.K_DOWN]:
    pointToSend.Position.CartesianPosition.Y = -0.08
  else:
    pointToSend.Position.CartesianPosition.Y = 0.0

  if keys[pygame.K_LEFT]:
    pointToSend.Position.CartesianPosition.X = 0.08
  elif keys[pygame.K_RIGHT]:
    pointToSend.Position.CartesianPosition.X = -0.08
  else:
    pointToSend.Position.CartesianPosition.X = 0.0

  if keys[pygame.K_PAGEUP]:
    pointToSend.Position.CartesianPosition.Z = 0.08
  elif keys[pygame.K_PAGEDOWN]:
    pointToSend.Position.CartesianPosition.Z = -0.08
  else:
    pointToSend.Position.CartesianPosition.Z = 0.0

  kinovapy.SendBasicTrajectory(pointToSend)

print 'End of example'


kinovapy.CloseAPI()

