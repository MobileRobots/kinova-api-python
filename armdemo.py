from AriaPy import *
from ArNetworkingPy import *
import sys
import arm
import time

# TODO add mode for teleop using force or velocity control.
# TODO display force sensing results somehow

ptu_serial = '/dev/ttyUSB0'

demoseq = [
   'out',
    'forward',
    'lookdown',
  'down',
   'out',
    'lookcenter',
   'funky_up',
    'lookup',
    'lookdownright',
  'park',
    'lookcenter'
]

states = {
'forward':
  {'left':[94.025734, 74.765625, 200.018387, 20.386364, 303.000000, 285.954559],
    'right': [273.419128, 269.062500, 142.003677, 182.113647, 257.045471, 288.477295] 
  }, 
  'lookdown': { 'pantilt': [0, -35] },
  'lookleft': { 'pantilt': [35, -3] },
  'lookright': { 'pantilt': [-35, -3] },
  'lookcenter': { 'pantilt': [0, -3] },
  'lookup': { 'pantilt': [0, 25] },
  'lookupleft': { 'pantilt': [20, 35] },
  'lookdownright': { 'pantilt': [-20, -35] },
'funky_up':
  {'left':[84.705887, 107.625000, 98.382355, 178.909103, 207.954544, 285.954559],
    'right': [273.419128, 269.062500, 142.003677, 182.113647, 257.045471, 288.477295] 
  }, 
'out':
  {'left':[37.224266, 91.406250, 200.018387, 167.590912, 233.522736, 285.818176],
    'right': [324.705872, 269.578125, 130.147064, 130.977280, 139.295456, 288.409088] 
  }, 
'park':
  {'left':[80.018379, 54.796875, 256.985291, 209.181824, 117.340912, 285.886383],
    'right': [280.202209, 315.093750, 140.625000, 160.227280, 295.840912, 288.477295]
  }, 
'down':
  {'left':[87.003677, 46.828125, 196.985291, 122.659096, 38.045456, 111.409096],
    'right': [300.000000, 306.656250, 111.231621, 81.136368, 0.204545, 285.750000]
  } 
}



ptu = ArDPPTU(None)
con = ArSerialConnection()
ptuinitialized = False

def initptu():
  global ptu
  global ptuinitialized
  global ptu_serial
  if ptuinitialized:
    return
  print 'opening '+ptu_serial
  print 'serial con status %d: %s' % (con.getStatus(), con.getStatusMessage(con.getStatus()))
  r = con.open(ptu_serial) 
  if(r != 0):
    print 'armdemo: Error opening serial port for ptu'
    return
  print 'serial con status %d: %s' % (con.getStatus(), con.getStatusMessage(con.getStatus()))
  ptu.setDeviceConnection(con)
  ptu.init()
  ptu.reset()
  ptuinitialized = True

def pantilt(pos):
  global ptu
  global ptuinitialized
  initptu()
  if not ptuinitialized:
    return
  ptu.panTilt(pos[0], pos[1])    
  ptu.awaitExec()

def demo():
  for sn in demoseq:
    print 'armdemo: doing pose ' + sn
    try:
      s = states[sn]
      try:
        print s
        arm.movearms(s)
      except:
        print 'armdemo: WARNING error doing state %s: %s' % (sn, states[sn])
    except KeyError:
      print 'armdemo: no state named %s!' % (sn)
    if 'pantilt' in s.keys():
      print 'doing pantilt %s' % s['pantilt']
      pantilt(s['pantilt'])
    time.sleep(4)
  arm.closefingers()


if __name__ == '__main__':
  arm.init()
  arm.home()
#  arm.init_fingers()
  arm.closefingers()

  initptu()
  #pantilt([5, 0])
  #pantilt([-5, 0])
  #pantilt([0, 0])
  #pantilt([0, -5])
  #pantilt([0, 5])
  #pantilt([0, 0])

  while True:
    demo()
    arm.closefingers()
    time.sleep(10)
    ptu.panSlew(ptu.getMaxPanSlew())
    ptu.tiltSlew(ptu.getMaxTiltSlew())

#  try:
#    arm.movearms(states['openfingers'])
#  except:
#    print 'armdemo: no openfingers sttate!'
#  try:
#    arm.movearms(states['closefingers'])
#  except:
#    print 'armdemo: no closefingers sttate!'
  #arm.park()
  arm.close()

