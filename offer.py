#!/usr/bin/python
import arm
import time

#arm.init()
#time.sleep(10)

#arm.init_fingers()

closed = [8200, 4600, 4000]



while(True):
	arm.movejoints('right', 
	#     [282.352936, 316.359375, 281.636017, 248.386368, 13.431819, 356.045471] ,
 [282.297791, 316.312500, 242.647064, 198.886368, 39.613636, 40.840912],
	     closed
	)
	time.sleep(13)
	arm.openfingers()
	time.sleep(20)
	arm.setfingers(closed)
	arm.movejoints('right',
	    [280.863983, 312.281250, 119.558823, 150.545456, 357.204559, 290.454559] ,
	     closed
	)
	time.sleep(20)



	#arm.close()

