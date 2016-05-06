#!/usr/bin/python
import arm
import ptu
import time

if __name__ == '__main__':
  ptu.initptu()
  arm.init()
  print arm.status()
  while(True):
    time.sleep(0.1)
    print arm.status()
    #ptu.lookat([x y z])


