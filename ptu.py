#!/usr/bin/python
from AriaPy import *
import sys
import time
import math

ptu_serial = '/dev/ttyS1'

ptu = ArDPPTU(None)
con = ArSerialConnection()
ptuinitialized = False

def initptu():
  global ptu
  global ptuinitialized
  global ptu_serial
  if ptuinitialized:
    return True
  print 'ptu.py: opening '+ptu_serial
  print 'ptu.py: serial con status %d: %s' % (con.getStatus(), con.getStatusMessage(con.getStatus()))
  r = con.open(ptu_serial) 
  if(r != 0):
    print 'ptu.py: Error opening serial port for ptu'
    return False
  print 'ptu.py: serial con status %d: %s' % (con.getStatus(), con.getStatusMessage(con.getStatus()))
  ptu.setDeviceConnection(con)
  ptu.init()
  time.sleep(2)
#  recalib()
#  time.sleep(10)
  ptu.panSlew(ptu.getMaxPanSlew() - 20)
  ptu.tiltSlew(ptu.getMaxTiltSlew() - 20)
  ptuinitialized = True
  return True

def pantilt(angles):
  if not initptu():
    return False
  global ptu
  print 'ptu.py: moving to angles %f, %f' % (angles[0], angles[1])
  if(angles[1] <= -45): 
    angles[1] = -45
  ptu.panTilt(angles[0], angles[1])    
  return True

# pos is a point in space [x, y, z] relative to the base of the PTU. +x is to the right. +y is in front. +z is up.
def lookat(pos):
  if not initptu():
    return False
  panoffset = 0   # offset of rotation point of pan joint on X axis (left/right)
  tiltoffset = 0  # offset of rotation point of tilt joint on Z axis (up/down)
  # todo also include vertical offset of ptu stage from middle of tilt joint
  global ptu
  x = pos[0]
  y = pos[1]
  z = pos[2]
  if y == 0:
    p = 0
  else:
    p = math.degrees( math.atan( -x / (y + panoffset) ) ) 
  if z == 0:
    t = 0
  else:
    t = math.degrees( math.atan( x / (z + tiltoffset) ) ) 
  print 'ptu lookat: pos [%f, %f, %f] -> angles [%f, %f].' % (x, y, z, p, t)
  if p > ptu.getMaxPosPan():
    p = ptu.getMaxPosPan() - 10
  elif p < ptu.getMaxNegPan():
    p = ptu.getMaxNegPan() + 10
  if t > ptu.getMaxPosTilt():
    t = ptu.getMaxPosTilt() - 10
  elif t < ptu.getMaxNegTilt():
    t = ptu.getMaxNegTilt() + 10
  print 'ptu lookat: moving to [%f, %f]' % (p, t)
  ptu.panTilt( p , t )
  return True

def wait():
  global ptu
  print 'ptu.py: waiting for ptu to finish moving...'
  ptu.awaitExec()

def recalib():
  global ptu
  print 'ptu.py: recalib...'
  ptu.resetCalib()

if __name__ == '__main__':
  initptu()

  print 'left'
  pantilt([20, 0])
  time.sleep(2)
  print 'right'
  pantilt([-20, 0])
  time.sleep(2)
  print 'center'
  pantilt([0, 0])
  time.sleep(2)
  print 'down'
  pantilt([0, -20])
  time.sleep(2)
  print 'up'
  pantilt([0, 20])
  time.sleep(2)
  print 'center'
  pantilt([0, 0])
  time.sleep(2)

  #recalib()

  print 'lookat 0.5, 0.3, -0.1, should be to the right and down a bit'
  lookat([0.5, 0.3, -0.2])
  time.sleep(4)

  print 'lookat 0.5, 0.1, 0.1, should be to the right a bit less, and up a bit'  
  lookat([0.5, 0.1, 0.1])
  time.sleep(4)

  print 'lookat 2.0, -0.25, 0.5, should be a little bit up and to the left (looking far away)'  
  lookat([2.0, -0.2, 0.1])
  time.sleep(4)

  print 'lookat 0.1, 0, -0.7, should be down as far as it can'
  lookat([0.1, 0, -0.7])
  time.sleep(4)

  print 'lookat 1000, 0, 0, should be straight ahead'
  lookat([1000, 0, 0])
  time.sleep(4)

  print 'center'
  pantilt([0, 0])
  time.sleep(2)

  print 'relaib'
  recalib()
  time.sleep(4)


