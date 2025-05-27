import sys
import serial
##sys.path.insert(1, 'Z:\Arisumi\Programs\General Test 3.5')
import time
from struct import *





# fun fact, you can just write a bitmask in place of this to command custom channel combos in 1 write instruction
def get_bit_mask(channels : list):
    print("WHAT IS GOING ON?")
    mask = 0x00
    for value in channels:
        mask |= value
    return bytearray(mask)


# how to use python for this
# documentation is a bit misleading for this. This is how I got it to work.
usbrelay = [
            [bytearray([0xff, 0x01, 0x00]), bytearray([0xff, 0x01, 0x01])], # channel-0
            [bytearray([0xff, 0x02, 0x00]), bytearray([0xff, 0x02, 0x02])], # channel-1
            [bytearray([0xff, 0x03, 0x00]), bytearray([0xff, 0x03, 0x03])], # channel-2
            [bytearray([0xff, 0x04, 0x00]), bytearray([0xff, 0x04, 0x04])], # channel-3
            [bytearray([0xff, 0x05, 0x00]), bytearray([0xff, 0x05, 0x05])], # channel-4
            [bytearray([0xff, 0x06, 0x00]), bytearray([0xff, 0x06, 0x06])], # channel-5
            [bytearray([0xff, 0x07, 0x00]), bytearray([0xff, 0x07, 0x07])], # channel-6
            [bytearray([0xff, 0x08, 0x00]), bytearray([0xff, 0x08, 0x08])], # channel-7
            [bytearray([0x00]), bytearray([0xff])], # all channels 
            ]




get_bit_mask([0,1,2])

serial_port = serial.Serial(
                            'COM96',
                            baudrate=9600,
                            bytesize =8,
                            timeout=5,
                            stopbits =serial.STOPBITS_ONE)



serial_port.write(usbrelay[0][1])
time.sleep(2)
serial_port.write(usbrelay[0][0])
time.sleep(2)
serial_port.write(usbrelay[1][1])
time.sleep(2)
serial_port.write(usbrelay[1][0])
time.sleep(2)
serial_port.write(usbrelay[2][1])
time.sleep(2)
serial_port.write(usbrelay[2][0])
time.sleep(2)
serial_port.write(usbrelay[3][1])
time.sleep(2)
serial_port.write(usbrelay[3][0])
time.sleep(2)
serial_port.write(usbrelay[4][1])
time.sleep(2)
serial_port.write(usbrelay[4][0])
time.sleep(2)
serial_port.write(usbrelay[5][0])
time.sleep(2)
serial_port.write(usbrelay[5][1])
time.sleep(2)
serial_port.write(usbrelay[6][1])
time.sleep(2)
serial_port.write(usbrelay[6][0])
time.sleep(2)


time.sleep(10)

### first index is channel, 2nd is on/off (0 or 1
##channel=0
##global_channel=8
##off_on=1
##
##
##packet = [58, 70, 69, 48, 53, 48, 48, 48, 48, 70, 70, 48, 48, 70, 69, 13, 10]
##print(packet)
##data = str(len(packet))+'B'
##tx = pack(data, *packet)
##print(tx)
##result = serial_port.write(tx)
##print(result)
##
##time.sleep(10)
##
##packet = [58, 70, 69, 48, 70, 48, 48, 48, 48, 48, 48, 49, 48, 48, 50,70, 70, 70, 70, 69, 51, 13, 10]
##
##print(packet)
##data = str(len(packet))+'B'
##tx = pack(data, *packet)
##print(tx)
##result = serial_port.write(tx)
##print(result)
##
##time.sleep(10)
##
##
##print("CLOSING")
##packet = [255, 1, 1]
##data = str(len(packet))+'B'
##tx = pack(data, *packet)
##print(tx)
##result = serial_port.write(tx)
##print(result)
##
##
###result = serial_port.write(b':FE050000FF00FE\r\n')
##print(usbrelay[channel][off_on])
##result = serial_port.write(usbrelay[channel][off_on])
##
##
##
##ack = ' '
##time.sleep(2)
##while serial_port.in_waiting:
##    inp = ''
##    try:
##        inp = serial_port.read(size=1) #read one byte
##    except:
##        print("read error")
##     
##
##    if len(inp) == 0:
##        print("No message recived")
##        break
##        
##    
##    check = inp.hex() #gives the correct bytes, each on a newline
##    ack = ack + ' ' + check
##    print(ack)
##         
##
##
##
##    
###result = serial_port.write(close_relay_cmd)
##result = serial_port.write([255,1,1]) # command all
##time.sleep(5)
##print(usbrelay[channel][off_on])
##time.sleep(5)
####print(result)
##
##[58, 70, 69, 48, 53, 48, 48, 48, 48, 70, 70, 48, 48, 70, 69, 13, 10]
##result = serial_port.write(b':FE0100200000FF\r\n')
##time.sleep(2)
##print(result)
##result = serial_port.write(b':FE0100000010F1\r\n')
##print(result)
##time.sleep(5)
##serial_port.write(get_bit_mask([ 1, 3, 5, 7])) # turn on all odds
##
##
##time.sleep(5) # wait before closing serial port
##
##
##serial_port.write(usbrelay[global_channel][0])
##print("Openinng")
##result = serial_port.write(usbrelay[channel][0])
##print(result)

time.sleep(5)
serial_port.close()
