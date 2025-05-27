# Copyright (c) 2018 Acroname Inc. - All Rights Reserved
#
# This file is part of the BrainStem development package.
# See file LICENSE or go to https://acroname.com/software/brainstem-development-kit for full license details.
import brainstem
#for easy access to error constants.
from brainstem.result import Result
#for easy acces to I2C constants.
from brainstem.stem import I2C
import time


##########################################################################################
# Devantech CMPSXX sample code
# This reads from different compass registers in a single byte transaction
# as well as a mulitple byte transaction.
# See Devantech's product page for additional register locations and values:
# for CMPS11:
# http://www.robot-electronics.co.uk/htm/cmps11i2c.htm
# for CMPS03
# http://www.robot-electronics.co.uk/htm/cmps3tech.htm
def CMPSXX_Test(stem):
	cmpsxx_addr = 0xC0
	cmpsxx_register = b'\x00'
	bus = 0

	#Set the bus speed setting on the I2C object to 100khz
	err = stem.i2c[bus].setSpeed(I2C.I2C_SPEED_100Khz)

	print ('Communicating with CMPSXX module at default I2C address %d (0x%X)' % (cmpsxx_addr, cmpsxx_addr))
	err = stem.i2c[bus].write(cmpsxx_addr, 1, cmpsxx_register)
	if (err != 0):
		print (' CMPSXX write failed: %d' % err)

	# Get the firmware version
	datain = stem.i2c[bus].read(cmpsxx_addr, 1)
	if (datain.value):
		print (' CMPSXX firmware version: %d' % datain.value[0])
	else:
		print (' CMPSXX firmware version FAILED.')

	# Set the compass to the bearing register
	cmpsxx_register = b'\x01'
	stem.i2c[bus].write(cmpsxx_addr, 1, cmpsxx_register)

	# Read back 3 bytes from compass
	datainmult = stem.i2c[bus].read(cmpsxx_addr, 3)
	if (datainmult.value):
		print (' CMPSXX bearing as byte [0-255] : %d' % datainmult.value[0])
		print (' CMPSXX bearing as short [0-3599] : %d\n' % (datainmult.value[1] << 8 | datainmult.value[2]))

##########################################################################################


##########################################################################################
# Create USB object and connect
# to the first module found
print ('\nCreating USBStem and connecting to first module found')
stem = brainstem.stem.USBStem()

#Locate and connect to the first object you find on USB
#Easy way: 1=USB, 2=TCPIP
result = stem.discoverAndConnect(brainstem.link.Spec.USB)

#Check error
if result == (Result.NO_ERROR):
    result = stem.system.getSerialNumber()
    print ("Connected to USBStem with serial number: 0x%08X" % result.value)
    CMPSXX_Test(stem)
else:
    print ('Could not find a module.\n')

#Disconnect from device.
stem.disconnect()
