from AriaPy import *
from ArNetworkingPy import *
import sys
import arm
import time
import ptu
import math

# TODO add mode for teleop using force or velocity control.
# TODO display force sensing results somehow

pausetime = 5 # wait between sending each trajectory to the arms



demoseq = [
   'armsout',
   'armsforward',
   'lookdown',
   'armsdown',
   'armsout',
   'lookcenter',
   'funky_up',
   'lookup',
   'lookdownright',
   'lookcenter'
]
squareseq = [
   'square1', 'squarepause', 'square2', 'squarepause', 'square3', 'squarepause',
'square4', 'squarepause', 'square5', 'pause3sec', 'handout', 'pause3sec', 'handleft', 'pause3sec', 'handright'
]

# Different options for each state, each state can have some or any of these:
PAUSE = 'pause'
LEFTARM = 'leftarm'
RIGHTARM = 'rightarm'
PANTILT = 'pantilt'
LOOKAT = 'lookat'

# Options for each arm (leftarm/rightarm):
JOINTS = 'joints'
HANDPOS = 'pos' # use either JOINTS or HANDPOSE
HANDORI = 'ori'
FINGERS = 'fingers' # use either OPENED or CLOSED as value for FINGERS:

# Options for FINGERS:
CLOSED = 'closed'
OPENED = 'opened'

# Useful hand orientations:

ORI_DOWN = [0, 0, 0]
ORI_OUT = [math.radians(90), 0, 0]
ORI_LEFT = [math.radians(90), 0, math.radians(90)]
ORI_RIGHT = [math.radians(90), 0, math.radians(-90)]

# defined states with names, use these names in demoseq above:
states = {
  'pause3sec':
    { PAUSE:3.0 },
  'squarepause':
    { PAUSE:4.0 },

  'openfingers':
    { FINGERS: OPENED },

  'closefingers': 
    { FINGERS: CLOSED} ,
    

  'square1':
    { RIGHTARM: { HANDPOS : [-0.2, -0.5, 0.1], HANDORI: ORI_DOWN, FINGERS: CLOSED }
     },

  'square2':
    { RIGHTARM: { HANDPOS : [-0.2, -0.6, 0.1], HANDORI: ORI_DOWN } 
    },

  'square3':
    { RIGHTARM: { HANDPOS : [-0.3, -0.6, 0.1] , HANDORI: ORI_DOWN } 
    },

  'square4':
    { RIGHTARM: { HANDPOS : [-0.3, -0.5, 0.1] , HANDORI: ORI_DOWN }
    },
  
  'square5':
    { RIGHTARM: {HANDPOS: [-0.2, -0.5, 0.1], HANDORI: ORI_DOWN, FINGERS:OPENED}
    },

  'handout':
    { RIGHTARM: {HANDORI: ORI_OUT } },

  'handleft':
    { RIGHTARM: {HANDORI: ORI_LEFT } },
  'handright':
    { RIGHTARM: {HANDORI: ORI_RIGHT } },

  'armsforward':
    { LEFTARM: { JOINTS: [94.025734, 74.765625, 200.018387, 20.386364, 303.000000, 285.954559] },
      RIGHTARM: { JOINTS: [273.419128, 269.062500, 142.003677, 182.113647, 257.045471, 288.477295]  }
    }, 

  'lookdown': 
    { PANTILT: [0, -35] },

  'lookleft': 
    { PANTILT: [35, -3] },

  'lookright': 
    { PANTILT: [-35, -3] },

  'lookcenter': 
    { PANTILT: [0, -3] },

  'lookup': 
    { PANTILT: [0, 25] },

  'lookupleft': 
    { PANTILT: [20, 35] },

  'lookdownright': 
    { PANTILT: [-20, -35] },

  'funky_up':
    { LEFTARM: {JOINTS:[84.705887, 107.625000, 98.382355, 178.909103, 207.954544, 285.954559]},
       RIGHTARM: {JOINTS: [273.419128, 269.062500, 142.003677, 182.113647, 257.045471, 288.477295] }
    }, 

  'armsout':
    { LEFTARM: { JOINTS: [37.224266, 91.406250, 200.018387, 167.590912, 233.522736, 285.818176]},
      RIGHTARM: { JOINTS: [324.705872, 269.578125, 130.147064, 130.977280, 139.295456, 288.409088] }
    }, 

  'park':
    { LEFTARM: { JOINTS :[80.018379, 54.796875, 256.985291, 209.181824, 117.340912, 285.886383]},
      RIGHTARM:{ JOINTS: [280.202209, 315.093750, 140.625000, 160.227280, 295.840912, 288.477295]}
    }, 

  'armsdown':
    { LEFTARM: { JOINTS :[87.003677, 46.828125, 196.985291, 122.659096, 38.045456, 111.409096]},
      RIGHTARM: { JOINTS: [300.000000, 306.656250, 111.231621, 81.136368, 0.204545, 285.750000]}
    } 
}




def doarmstate(whicharm, state):
  fingers = None
  if FINGERS in state.keys():
    fingers = state[FINGERS]
  if JOINTS in state.keys():
    print 'Doing joint positions'
    arm.movejoints(whicharm, state[JOINTS], fingers)
  elif HANDPOS in state.keys():
    hp = state[HANDPOS]
    print 'Doing hand position'
    ho = None
    if HANDORI in state.keys():
      ho = state[HANDORI]
      print 'got hand orientation'
    else:
      print 'no hand orientation'
    print 'moveto...'
    arm.moveto(whicharm, state[HANDPOS], ho, fingers)
  elif fingers != None:
    print 'Doing fingers only'
    arm.movejoints(whicharm, None, fingers)


def dostate(name):
  print 'armdemo: doing state %s' % name
  try:
    s = states[name]
    print s

    try:
      leftstate = s[LEFTARM]
      try:
        doarmstate(LEFTARM, leftstate)
      except RuntimeError, e:
        print 'warning: error doing left arm state: %s' % e
    except KeyError:
      print 'warning: no left arm state specified'

    try:
      rightstate = s[RIGHTARM]
      try:
        doarmstate(RIGHTARM, rightstate)
      except RuntimeError, e:
        print 'warning: error doing right arm state: %s' % e
    except KeyError:
      print 'warning: no right arm state specified'

    if FINGERS in s.keys():
      f = s[FINGERS]
      if f == 'CLOSED':
        arm.closefingers()
      elif f == 'OPENED':
        arm.openfingers()

    if PANTILT in s.keys():
      print 'doing pantilt %s' % s['pantilt']
      ptu.pantilt(s[PANTILT])
    elif LOOKAT in s.keys():
      armx = s[LOOKAT][0]
      army = s[LOOKAT][1]
      armz = s[LOOKAT][2]
      ptux = -1 * army
      ptuy = -1 * armx
      ptuz = armz
      ptu.lookat([ptux, ptuy, ptuz])

    if PAUSE in s.keys():
      time.sleep(s[PAUSE])

  except KeyError:
    print 'armdemo: no state named %s!' % (sn)

def doseq(seq):
  for si in seq:
    if isinstance(si, list):
      print 'doing subsequence'
      doseq(si)
    else:  
      dostate(si)
    time.sleep(pausetime)

def demo():
  doseq(demoseq)
  # end of demo sequence
  ptu.pantilt([0, 0])
  arm.park()
  arm.closefingers()

def initptu():
  return ptu.initptu()

if __name__ == '__main__':
  arm.init()
  arm.home()
  arm.init_fingers()

  ptu.initptu()
  #ptu.pantilt([5, 0])
  #ptu.pantilt([-5, 0])
  #ptu.pantilt([0, 0])
  #ptu.pantilt([0, -5])
  #ptu.pantilt([0, 5])
  #ptu.pantilt([0, 0])

  while True:
    demo()
    time.sleep(5)

  arm.close()

