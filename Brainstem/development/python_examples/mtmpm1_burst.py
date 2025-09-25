# Copyright (c) 2018 Acroname Inc. - All Rights Reserved
#
# This file is part of the BrainStem development package.
# See file LICENSE or go to https://acroname.com/software/brainstem-development-kit for full license details.
import brainstem
#for easy access to error constants
from brainstem.result import Result
import time

MICRO_TO_VOLTS = 1000000.0     #Used to convert microvolts to volts.

print ('--------------------------------------')
print ('This example assumes a simple power swtich (relay or FET) is connected \
to the rail0 output. The switch should connect a 1-3ohm load resistor. \
Kelvin sense can be connected or disconnected to show its effect on the voltage \
respone. The swtich control should be connected to DIO0 of the MTM-PM1 module.')
print ('--------------------------------------')
print ('')

print ('Creating MTM-PM-1 stem and connecting to first module found')
stem = brainstem.stem.MTMPM1()

#Locate and connect to the first object you find on USB
#Easy way: 1=USB, 2=TCPIP
result = stem.discoverAndConnect(brainstem.link.Spec.USB)
#Locate and connect to a specific module (replace you with Your Serial Number (hex))
#result = stem.discoverAndConnect(brainstem.link.Spec.USB, 0x66F4859B)

#Check error
if result == (Result.NO_ERROR):
    result = stem.system.getSerialNumber()
    print ("Connected to USBStem with serial number: 0x%08X" % result.value)

    #Setup Digital Pin:
    stem.digital[0].setConfiguration(1) #0=Input, 1=Output, 2=RCServoInput, 3=RCServoOutput, 4=HighZ
    stem.digital[0].setState(0)     #0=Low, 1=High

    #Setup Rail:
    stem.rail[0].setVoltage(3800000) #In microVolts. 3800000 = 3.8VDC
    stem.rail[0].setKelvinSensingEnable(1) #0=KelvinSense Off, #1=KelvinSense On
    stem.rail[0].setOperationalMode(1) #0=Auto, 1=Linear, 2=Switcher, 4=SwitcherLinear

    #Turn Rail on:
    stem.rail[0].setEnable(1) #0=Rail Off, 1=Rail On
    time.sleep(1) #allow rail to stabalize

    #Get measurments.
    vmeas = stem.rail[0].getVoltage()
    print ("RAIL0 voltage reading %d uV" % vmeas.value)
    imeas = stem.rail[0].getCurrent()
    print ("RAIL0 current reading %d uA" % imeas.value)

    nAttempts = 20
    try:
        while True and nAttempts:
            # toggle the external load on/off
            stem.digital[0].setState( nAttempts % 2 )
            time.sleep(0.1)
            imeas = stem.rail[0].getCurrent()
            vmeas = stem.rail[0].getVoltage()
            print(("RAIL0: %.3fV at %.3fA" % ((vmeas.value/MICRO_TO_VOLTS),
                                             (imeas.value/MICRO_TO_VOLTS))))
            nAttempts = nAttempts - 1 #Loop control

    finally:
        #Shut down:
        stem.rail[0].setEnable(0)   #Turn Rail off
        stem.digital[0].setState(0)
        stem.disconnect()   #disconnect from device

else:
    print ('Could not find a module.\n')
