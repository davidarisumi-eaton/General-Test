'''---------------------------------------------------------------------
    
    Company:    EATON COROPORATION
            
                Proprietary Information
                (C) Copyright 2016
                All rights reserved
                
                PXR MCCB Automation - Protection  
    
-------------------------------------------------------------------------------
    
    Authors:    David Arisumi                (412) 893-3213
                Eaton Corporation
                1000 Cherrington Parkway
                Moon Twp, PA 15108-4312
                (412) 893-3300
                
-------------------------------------------------------------------------------
    
    Product:    Automated test system to test the PXR10, PXR20, PXR2D, PXR25, 
                and PXR35 protection algorithms for the SR, NZM, and NRX 
                breaker frames.   
                
    Module:     USB_commands.py
                
    Mechanics:  program module containing the functions related to USB 
                functionality including:
                
                1.  Setpoint override 
                2.  calibration routines
    
                Module Functions:
                    command - init, normalize, compare, carryout hex serial comms
                    calc_checksum - calculate checksum module
                    format_packet - format tx and rx packets
                    write_group1 - write group1 setpoints
                    read_group1 - read group1 setpoints
                    enter_into_manufactory - enter manufactory mode
                    exit_out_of_manufactory - exit manufactory mode
                    update_setpoints - update/verify group1 setpoints
                    calibration - run calibration from profile calibration
                
    Reference:  USB specification for PXR MCCB 3.35
----------------------------------------------------------------------------'''

from __future__ import division
from struct import *
import GT_Conversions, serial, time, math

def get_message(def_name, *argv):

    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(def_name)

    
    if not method:
        print(def_name, " is not a method")
        return False
    else:
        if len(argv) == 0:
            tx, msg_len, tag = method()
        elif len(argv) == 1:
            tx, msg_len, tag = method(argv[0])
        else:
            keys = argv[0]
            setpoints = argv[1]
            tx, msg_len, tag = method(keys, setpoints)
        

    return tx, msg_len, tag

def calc_checksum(Packet):
    

    # compress packet
    packet = []
    for i in range (0, len(Packet)):
        if Packet[i] != '':
            packet.append(Packet[i])
       
    # Hexadecimal to integer conversion
    
    if type(Packet[0]) == hex:
        for i in range(0, len(packet)):
            packet[i] = int(packet[i], 16)
   
        
    # Compute Checksum
    LSB_sum, MSB_sum = 0, 0  
    for i in range(0, len(packet)-3):    
        if i%2 == 0: 
            LSB_sum += packet[i]
        elif i%2 == 1: 
            MSB_sum += packet[i]
        
    CheckLSB = LSB_sum % 256 
    CheckMSB = (MSB_sum + int(LSB_sum/256)) % 256

    packet[-3], packet[-2] = CheckLSB, CheckMSB

    return packet
    
def format_packet(packet):
    
    rx_arr = []
    rx_str = ''
    
    for i in range(0, len(packet)):
        packet[i] = int(packet[i])
        rx_arr.append(hex(packet[i])[2:])
        if i == 0:
            rx_str = rx_str + format(packet[i], '02x') 
        else:
            rx_str = rx_str + ' ' + format(packet[i], '02x') 
    data = str(len(packet))+'B'
    tx = pack(data, *packet)
    
    return tx, rx_str


def get_correctness(msg):
    correctness_byte = msg[12]+msg[13]
    if correctness_byte == '00':
        correctness = "successful"
    elif correctness_byte == '01':
        correctness = "wrong checksum"
    elif correctness_byte == '03':
        correctness = "wrong data type"
    elif correctness_byte == '04':
        correctness = "command is wrong"
    elif correctness_byte == '07':
        correctness = "out of range"
    elif correctness_byte == '0d':
        correctness = "Rotary Switch Wrong"
    elif correctness_byte == '20':
        correctness = "busy"
    elif correctness_byte == '30':
        correctness = "in manufacturing mode"
    elif correctness_byte == '31':
        correctness = "not in manufacturing mode"
    elif correctness_byte == '32':
        correctness = "in auto test mode"
    elif correctness_byte == '33':
        correctness = "not in auto test mode"    
    elif correctness_byte =='50':
        correctness = "pending"
    elif correctness_byte == 'a2':
        correctness = "request recieved"
    elif correctness_byte == 'a5':
        correctness = "request time out"
    elif correctness_byte == 'a6':
        correctness = "FRAM write fail"
    elif correctness_byte == 'a7':
        correctness = "condition fail"
    elif correctness_byte == 'a8':
        correctness = "Action feature not supported at style"
    elif correctness_byte =='a9':
        correctness = "password fail"
    elif correctness_byte == 'aa':
        correctness = "setpoint blocked"
    elif correctness_byte == 'ab':
        correctness = "input password"
    elif correctness_byte == 'ff':
        correctness = "Failure"
    elif correctness_byte == 'c0':
        correctness = "no erasable language"
    elif correctness_byte == 'c1':
        correctness = "no memory for language"
    elif correctness_byte == 'c2':
        correctness = "no memory for language"
    elif correctness_byte == 'c3':
        correctness = "error during write"
    elif correctness_byte == 'c4':
        correctness = "code conflict"
    elif correctness_byte == 'c5':
        correctness = "download language error"
    elif correctness_byte == 'c6':
        correctness = "language cant change"
    elif correctness_byte == 'c7':
        correctness = "language frame conflict"
    elif correctness_byte == 'c8':
        correctness = "langauge file conflict" 
    else:
        correctness = "unknown"
        
    return correctness
''' Master Dependent Functions '''
  

    
def read_setpoint_zero(): #Table 16/17

    #Read Group0 request
    tx = bytes.fromhex('80 00 00 00 80 00 fd')
    tag = "Read Setpoint 0"
    msg_len = 26

    return tx, msg_len, tag

def read_setpoint_one(): #Table 20/21

    tx = bytes.fromhex('80 00 00 01 80 01 fd')
    rx = ''
    msg_len = 63
    tag = "Read Setpoint One"

    return tx, msg_len, tag

def read_setpoint_two(): #Table 20/21

    tx = bytes.fromhex('80 00 00 02 80 02 fd')
    rx = ''
    msg_len = 20
    tag = "Read Setpoint Two"

    return tx, msg_len, tag

def read_setpoint_three(): #Table 20/21

    tx = bytes.fromhex('80 00 00 03 80 03 fd')
    rx = ''
    msg_len = 44
    tag = "Read Setpoint Three"

    return tx, msg_len, tag

def read_setpoint_five():

    tx = bytes.fromhex('80 00 00 05 80 05 fd')
    msg_len = 63
    tag = "Read Setpoitn Five"

    return tx, msg_len, tag

def read_group_two(): #table 23/24

    tx = bytes.fromhex('80 00 00 02 80 02 fd')
    rx = ''
    msg_len = 21

    return tx, msg_len, tag
    
def read_group_three(): #table 26/27

    tx = bytes.fromhex('80 00 00 03 80 03 fd')
    rx = ''
    msg_len = 45

    return tx, rx, msg_len


def write_setpoint_zero(keys, setpoint_packet): #table 28/30

    style = setpoint_packet["Style1"]

    if style == 0:
        vb_one   = 199
        vb_two   = 232 
        vb_three = 56
    elif style == 1:
        vb_one   = 199
        vb_two   = 232 
        vb_three = 56
    elif style == 2:
        vb_one   = 199
        vb_two   = 232 
        vb_three = 56
    elif style == 3:
        vb_one   = 199
        vb_two   = 232 
        vb_three = 56
    elif style == 4:
        vb_one   = 247
        vb_two   = 232 
        vb_three = 56
    elif style == 5:
        vb_one   = 247
        vb_two   = 232 
        vb_three = 56
    elif style == 6:
        vb_one   = 199
        vb_two   = 233 
        vb_three = 62
    elif style == 7:
        vb_one   = 199
        vb_two   = 233 
        vb_three = 126
    elif style == 8:
        vb_one   = 247
        vb_two   = 233
        vb_three = 62
    elif style == 9:
        vb_one   = 247
        vb_two   = 233
        vb_three = 126
    elif style == 10:
        vb_one   = 247
        vb_two   = 252
        vb_three = 56
    elif style == 11:
        vb_one   = 247
        vb_two   = 252
        vb_three = 56


    if setpoint_packet['MCU1 Version'] == 2:
        data_amount = 43
    else:
        data_amount = 49
        
    packet = [128, 2, 0, 0, 1, 1, data_amount, vb_one, vb_two, vb_three]

    for key in keys:
        packet.append(int(int(setpoint_packet[key])%256))
        packet.append(int(int(setpoint_packet[key])/256))

    packet_end = [0, 0, 253]
    packet = packet + packet_end
    
    packet = calc_checksum(packet)
    tx, rx = format_packet(packet)
    tag = "Write Setpoint Zero"
    msg_len = 9

    return tx, msg_len, tag

def write_setpoint_one(keys, setpoint_packet):#Table 31/33

    v_one = 247
    v_two = 253
    v_three = 255

 
##    if setpoint_packet["MCU1 Version"] == 2:
##        v_one = 255
##        v_two = 255
##        v_three = 176
##        print("Version 2")
        
##    v_one = 255
##    v_two = 255
##    v_three = 7
    packet = [128, 2, 0, 1, 1, 1, 51, v_one, v_two, v_three]


    for key in keys:
        packet.append(int(int(setpoint_packet[key])%256))
        packet.append(int(int(setpoint_packet[key])/256))
        
    
    packet_end = [0, 0, 253]

    packet = packet + packet_end
    
    packet = calc_checksum(packet)
    tx, rx = format_packet(packet)
    rx = '80 0e 00 01 00 00 80 0f fd'
    tag = "Write Setpoint One"
    msg_len = 9

    return tx, msg_len, tag

def write_setpoint_two(keys, setpoint_packet):#Table 34/36

    
    packet = [128, 2, 0, 2, 1, 1, 9, 15]
        
    for key in keys:
        packet.append(int(int(setpoint_packet[key])%256))
        packet.append(int(int(setpoint_packet[key])/256))
        
    
    packet_end = [0, 0, 253]
    packet = packet + packet_end


    packet = calc_checksum(packet)
    tx, rx = format_packet(packet)
    rx = '80 0e 00 02 00 00 80 10 fd'
    msg_len = 9
    tag = "Write Setpoint Two"

    return tx, msg_len, tag

def write_setpoint_three(keys, setpoint_packet):#Table 37/39

    
    packet = [128, 2, 0, 3, 1, 1, 35, 0]

    for key in keys:
        packet.append(int(int(setpoint_packet[key])%256))
        packet.append(int(int(setpoint_packet[key])/256))
        
    
    packet_end = [0, 0, 253]
    packet = packet + packet_end


    packet = calc_checksum(packet)
    tx, rx = format_packet(packet)
    rx = '80 0e 00 03 00 00 80 11 fd'
    tag = "Write Setpoint Three"
    msg_len = 9

    return tx, msg_len, tag

def write_setpoint_five(keys, setpoint_packet):#Table 31/33

    v_one = 247
    v_two = 127
    v_three = 6

##    v_one = 255
##    v_two = 255
##    v_three = 7
    packet = [128, 2, 0, 5, 1, 1, 51, v_one, v_two, v_three]


    for key in keys:
        packet.append(int(int(setpoint_packet[key])%256))
        packet.append(int(int(setpoint_packet[key])/256))
        
    
    packet_end = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 253]

    packet = packet + packet_end
    
    packet = calc_checksum(packet)
    tx, rx = format_packet(packet)
    rx = '80 0e 00 01 00 00 80 0f fd'
    tag = "Write Setpoint Five"
    msg_len = 9

    return tx, msg_len, tag

def read_real_time_data_buffer_zero(): #Table 40/41

    tx = '80 00 01 00 81 00 fd' #Table 54 Package Format of PC Read Rea Time Data Buffer0 Request
    
    tx = bytes.fromhex(tx)
    tag = "Read Real Time Data Buffer Zero"
    msg_len = 17

    return tx, msg_len, tag



def read_real_time_data_buffer_one(): #Table 42/43

    tx = '80 00 01 01 81 01 fd' #Table 55 Package Format of PC Read Rea Time Data Buffer1 Request
    
    tx = bytes.fromhex(tx)
    msg_len = 67
    tag = "Read Real Time Data Buffer One"


    return tx, msg_len, tag

def read_real_time_data_buffer_two(): #Table 44/45

    tx = '80 00 01 02 81 02 fd' #Table 58 Package Format of PC Read Real Time Data Buffer 2 Request
    tx = bytes.fromhex(tx)
    msg_len = 93
    tag = "Read Real Time Data Buffer Two"

    return tx, msg_len, tag
    

def read_real_time_data_buffer_three(): #Table 46/47

    tx ='80 00 01 03 81 03 fd'
    tx = bytes.fromhex(tx)
    msg_len = 26
    tag = "Read Real Time Data Buffer Three"

    return tx, msg_len, tag

def read_real_time_data_buffer_four():  #Table 48/49

    
    tx = '80 00 01 04 81 04 fd'
    tx = bytes.fromhex(tx)
    msg_len = 57
    tag = "Read Real Time Buffer Four"

    return tx, msg_len, tag

def read_real_time_data_buffer_five(): #Table 50/51

    tx = '80 00 01 05 81 05 fd'
    tx = bytes.fromhex(tx)
    msg_len = 143
    tag = "Read Real TIme Buffer Five"

    return tx, msg_len, tag

def read_real_time_data_buffer_six(): #Table 52/53

    tx = '80 00 01 06 81 06 fd'
    tx = bytes.fromhex(tx)
    msg_len = 67
    tag = "Read Real Time Buffer Six"

    return tx, msg_len, tag

def read_real_time_data_buffer_seven(): #Table 54/55

    tx = '80 00 01 07 81 07 fd'
    tx = bytes.fromhex(tx)
    msg_len = 81
    tag = "Read Real Time = Seven"

    return tx, msg_len, tag

def read_real_time_data_buffer_eight():  #Table 56/57

    tx = '80 00 01 08 81 08 fd'
    tx = bytes.fromhex(tx)
    msg_len = 81
    tag = "Read Real Time Buffer Eight"

    return tx, msg_len, tag
    

def read_real_time_data_buffer_ten(): #Table 58/59

    tx = '80 00 01 0a 81 0a fd' #Table 72 Package Format of PC Read Rea Time Data Buffer10 Request
    
    tx = bytes.fromhex(tx)
    msg_len = 33
    tag = "Read Real Time Data Buffer Ten"

    return tx, msg_len, tag
    
def read_real_time_data_buffer_eleven(): #Table 60/61

    tx = '80 00 01 0b 81 0b fd' #Table 72 Package Format of PC Read Rea Time Data Buffer10 Request
    
    tx = bytes.fromhex(tx)
    msg_len = 66
    tag = "Read Real TIme Data Buffer Eleven"

    return tx, msg_len, tag

def read_real_time_data_buffer_twelve(): #Table 76-77'

    tx = '80 00 01 0c 81 0c fd' #Table 72 Package Format of PC Read Rea Time Data Buffer10 Request
    
    tx = bytes.fromhex(tx)
    msg_len = 66
    tag = "Read Real TIme Data Buffer Twelve"

    return tx, msg_len, tag

def read_real_time_data_buffer_thirteen(): #Table 76-77'

    tx = '80 00 01 0d 81 0d fd' #Table 72 Package Format of PC Read Rea Time Data Buffer10 Request
    
    tx = bytes.fromhex(tx)
    msg_len = 15
    tag = "Read Real TIme Data Buffer Thirteen"

    return tx, msg_len, tag

def read_real_time_customer_breaker_health():

    tx = '80 00 01 2a 81 2a fd'

    tx = bytes.fromhex(tx)
    msg_len = 57
    tag = "Read Real Time Customer Breaker Health"

    return tx, msg_len, tag

def read_real_time_internal_breaker_health():

    tx = '80 00 01 2b 81 2b fd'

    tx = bytes.fromhex(tx)
    msg_len = 57
    tag = "Read Real Time Internal Breaker Health"

    return tx, msg_len, tag


def reset_all_external_diagnostics_request():
    
    tx = '80 04 03 1b 83 1f fd'
    tx = bytes.fromhex(tx)
    msg_len = 9
    
    tag = "Reset External Breaker Diagnostics Request"

    return tx, msg_len, tag

def reset_all_external_diagnostics_check():
    
    tx = '80 00 03 1b 83 1b fd'
    tx = bytes.fromhex(tx)
    msg_len = 9
    
    tag = "Reset External Breaker Diagnostics Check"

    return tx, msg_len, tag

def reset_all_internal_diagnostics_request():

    tx = '80 04 03 1c 83 20 fd'
    tx = bytes.fromhex(tx)
    msg_len = 9
    
    tag = "Reset Internal Breaker Diagnostics Request"

    return tx, msg_len, tag

def reset_all_internal_diagnostics_check():

    tx = '80 00 03 1c 83 1c fd'
    tx = bytes.fromhex(tx)
    msg_len = 9
    
    tag = "Reset Internal Breaker Diagnostics Check"

    return tx, msg_len, tag

def read_updated_status(): #Table 63/64

    tx = bytes.fromhex('80 00 01 10 81 10 fd')
    rx = ''
    msg_len = 19

    return tx, rx, msg_len

def read_updated_status_two(): #Table 64/65

    tx = bytes.fromhex('80 00 01 11 81 11 fd')
    rx = ''
    msg_len = 21

def read_event_summary(): #Table 70/71

    tx = bytes.fromhex('80 00 02 00 82 00 fd')
    rx = ''
    msg_len = 0 #This one has a variable return amount...gonna have to look into this.

    return tx, rx, msg_len

def read_trip_event_request(): #Table 78/80

    tx = bytes.fromhex('80 00 02 02 82 02 fd')
    rx = ''
    msg_len = 188
    
def read_firmware_version(): #Table 65/66

    tx = bytes.fromhex('80 00 01 11 81 11 fd')
    msg_len = 21
    
    tag = "Read Firmware Version"

    return tx, msg_len, tag


def reset_trip_unit_request(): #Table 92/93

    tx = bytes.fromhex('80 04 03 01 83 05 fd')
    rx = ''
    tag = "Reset Trip Unit Execute"
    msg_len = 9

    return tx, msg_len, tag

def reset_trip_unit_check(): #Table 94/95

    tx = bytes.fromhex('80 00 03 01 83 01 fd')
    rx = ''
    tag = "Reset Trip Unit Check"
    msg_len = 9

    return tx, msg_len, tag


def capture_waveform_execute(): #Table 96/97

    tx = bytes.fromhex('80 04 03 02 83 06 fd')
    rx = ''
    msg_len = 9

    return tx, rx, msg_len

def capture_waveform_read():

    tx = bytes.fromhex('80 00 03 02 83 02 fd')
    rx = ''
    msg_len = 9

    return tx, rx, msg_len


def capture_waveform_read_one():

    tx = bytes.fromhex('80 00 03 03 83 03 fd')
    rx = ''
    msg_len = 26

    return tx, rx, msg_len


def current_time_execute(): #Table 103/104

    tx = bytes.fromhex('80 04 03 04 83 08 fd')
    rx = ''
    msg_len = 9

    return tx, rx, msg_len

def current_time_read(): #Table 105/106

    tx = bytes.fromhex('80 00 03 04 83 04 fd')
    rx = ''
    msg_len = 19

    return tx, rx, msg_len

def set_new_time_execute(time_set): #Table 107/108


    packet = [128, 14, 3, 5, 1, 1, 8, 0]
    packet.append(time_set)

    packet = calc_checksum(packet)
    tx, rx = format_packet(packet)
                       
    rx = '80 0e 03 05 00 00 83, 13, fd'
    msg_len = 9

    return tx, rx, msg_len


def software_test_with_trip_execute(test_current): #Table 111/112

    packet = [128, 4, 3, 6, 1, 1, 6, 0]
    packet.append(test_current)

    tx, rx = format_packet(packet)
    
    rx = '80 0e 03 06 00 00 83 14 fd'

    msg_len = 9

    return tx, rx, msg_len

def software_test_with_trip_read(test_current): #Table 113/114

    tx = '80 00 03 06 83 06 fd'
    rx = ''

    msg_len = 9

    return tx, rx, msg_len

def read_test_result_read(): #Table 115/116
    
    tx = '80 00 03 09 83 09 fd'
    rx = ''
    msg_len = 23

    return tx, rx, msg_len

def software_test_without_trip_execute(test_current): #Table 118/119

    packet = [128, 4, 3, 7, 1, 1, 6, 0]
    packet.append(test_current)
    
    packet = calc_checksum(packet)
    tx, rx = format_packet(packet)

    msg_len = 9
    
    return tx, rx, msg_len

def software_test_without_trip_read(): #Table 119/120

    
    tx = '80 0e 03 07 00 00 03 15 fd'
    rx = ''

    msg_len = 9

    return tx, rx, msg_len

def cancel_software_test_execute():

    tx = '80 04 03 08 83 0c fd'
    rx = ''

    msg_len = 9

    return tx, rx, msg_len

def cancel_software_test_read():

    tx = '80 00 03 08 83 08 fd'
    rx = ''

    msg_len = 9

    return tx, rx, msg_len

def hardware_test_with_trip_execute(test_current): #128/129

    tx = [128, 4, 3, 11, 1, 1, 6, 0]
    packet.append(test_current)
    
    packet = calc_checksum(packet)
    tx, rx = format_packet(packet)

    msg_len = 9

    return tx, rx, msg_len

def hardware_test_with_trip_read(test_current): #Table 130/131

    tx = '80 00 03 0b 83 0b fd'
    rx = ''
    msg_len = 9

    return tx, rx, msg_len

def hardware_test_without_trip_execute(test_current): #135/136

    packet = [80, 4, 4, 12, 1, 1 ,6, 0]
    packet.append(test_current)

    packet = calc_checksum(packet)
    tx, rx = format_packet(packet)

    msg_len = 9

    return tx, rx, msg_len
    
def hardware_test_without_trip_read(): #Table #137/138

    tx = '80 00 03 0c 83 00 0c fd'
    rx = ''

    msg_len = 9

    return tx, rx, msg_len

def hardware_test_cancel_execute(): #Table 141/142

    tx = '80 04 03 0d 83 11 fd'
    rx = ''

    msg_len = 9

    return tx, rx, msg_len

def hardware_test_cancel_read(): #Table 143/144

    tx = '80 00 03 0d 83 0d fd'
    rx = ''

    msg_len = 9

    return tx, rx, msg_len



def enter_into_auto_test_mode_request(): #Table 211/212

    tx = bytes.fromhex('80 04 04 00 84 04 fd')
    rx = '80 0e 04 00 00 00 84 0e fd'
    msg_len = 9
    tag = "Enter Into Auto Test Mode Request"

    return tx, msg_len, tag

def enter_into_auto_test_mode_check(): #Table 211/212

    tx = bytes.fromhex('80 00 04 00 84 00 fd')
    rx = '80 01 04 00 00 00 84 01 fd'
    msg_len = 9
    tag = "Enter Into Auto Test Mode Check"

    return tx, msg_len, tag

def exit_out_of_auto_test_mode_request(): #Table 211/212

    tx = bytes.fromhex('80 04 04 01 84 05 fd')
    rx = '80 0e 04 01 00 00 84 0f fd'
    msg_len = 9
    tag = "Exit Out Of Auto Test Mode Request"

    return tx, msg_len, tag

def exit_out_of_auto_test_mode_check(): #Table 211/212

    tx = bytes.fromhex('80 00 04 01 84 01 fd')
    rx = '80 01 04 01 00 00 84 02 fd'
    msg_len = 9
    tag = "Exit Out Of Auto Test Mode Check"

    return tx, msg_len, tag



def enter_password_execute(): #Table 145/146

    tx = bytes.fromhex('80 04 03 0a 83 0e fd')
    rx = ''
    msg_len = 9
    tag = "Enter Password Execute"

    return tx, msg_len, tag


def enter_password_read(): #Table 147/148

    tx = bytes.fromhex('80 00 03 0a 83 0a fd')
    rx = ''
    msg_len = 7
    tag = "Enter Password Read"

    return tx, msg_len, tag

def verify_password_execute(password): #Table 158/159

    
    packet = [128, 4, 3, 14, 1, 1, 4, 0, password[0], password[1], password[2], password[3], 0, 0, 253]

    
    packet = calc_checksum(packet)
    tx, rx = format_packet(packet)
    rx = '80 0e 00 01 00 00 80 0f fd'
    tag = "Verify Password Execute"
    msg_len = 9

    return tx, msg_len, tag


    
def enter_into_manufactory_mode_request(): #Table 219/220

    tx = bytes.fromhex('80 04 04 02 84 06 fd')
    rx = '80 0e 04 02 00 00 84 10 fd'
    msg_len = 9
    tag = "Enter Into Manufactory Mode Request"

    return tx, msg_len, tag

def enter_into_manufactory_mode_check(): #Table 221/222

    tx = bytes.fromhex('80 00 04 02 84 02 fd')
    rx = '80 01 04 02 00 00 84 03 fd'
    msg_len = 9
    tag = "Enter Into Manufactory Mode Request"

    return tx, msg_len, tag

def exit_out_of_manufactory_mode_request(): #Table 223/224

    tx = bytes.fromhex('80 04 04 03 84 07 fd')
    rx = '80 0e 04 03 00 00 84 11 fd'
    msg_len = 9
    tag = "Exit Out Of Manufactory Mode Request"
    
    return tx, msg_len, tag

def exit_out_of_manufactory_mode_check(): #Table 225/226

    tx = bytes.fromhex('80 00 04 03 84 03 fd')
    rx = '80 01 04 03 00 00 84 04 fd'
    msg_len = 9
    tag = "Exit Out Of Manufactory Mode Check"

    return tx, msg_len, tag

def calibration_to_current_offset_request(): #Table 309

    tx = bytes.fromhex('80 04 04 39 84 3d fd')
    rx = '80 0e 04 39 00 00 84 47 fd'

    msg_len = 9
    tag = "Calibration To Current Offset Request"

    return tx, msg_len, tag

def calibration_to_current_offset_check(): #Table 309

    tx = bytes.fromhex('80 00 04 39 84 39 fd')
    rx = '80 01 04 39 00 00 84 3a fd'

    msg_len = 9
    tag = "Calibration To Current Offset Request"

    return tx, msg_len, tag


def calibration_to_sg_gain_scale_factor_request(current): #Table 317/318

    cal_point = current
    
    cal_byte_a = int(cal_point % 256)
    
    cal_byte_b = int(math.floor(cal_point / 256))
    while cal_byte_b > 256:
        cal_byte_b = cal_byte_b -256
        
    cal_byte_c = int(math.floor(cal_point / (256**2)))
    while cal_byte_c > 256:
        cal_byte_c = cal_byte_c -256
        
    cal_byte_d = int(math.floor(cal_point / (256**3)))

    tx = [128, 4, 4, 43, 1, 1, 4, 0, cal_byte_a, cal_byte_b, cal_byte_c, cal_byte_d, 0, 0, 253] #Table 342 External Ia scale factor calibration request from PC
    tx = calc_checksum(tx)
    tx, unused = format_packet(tx)
        
    rx = '80 0e 04 2b 00 00 84 39 fd'   #Table 343 external Ia scale factor calibration request feedback to PC

    msg_len = 9
    tag = "Calibration To Source Ground Gain Scale Factor"

    return tx, msg_len, tag


def calibration_to_sg_gain_scale_factor_check(): #Table 319/310

    tx = bytes.fromhex('80 00 04 2b 84 2b fd')
    rx = '80 01 04 2b 00 00 84 2c'
    msg_len = 9
    tag = "Calibration To SG Gain Scale Factor Check"

    return tx, msg_len, tag
    
def calibration_to_current_four_pole_gain_scale_factor_to_etu_request(current): #Table 357/358

    q_four_current = current*2**4

    cal_byte_a = int(q_four_current % 256)
    
    cal_byte_b = int(math.floor(q_four_current / 256))
    while cal_byte_b > 256:
        cal_byte_b = cal_byte_b -256
        
    cal_byte_c = int(math.floor(q_four_current / (256**2)))
    while cal_byte_c > 256:
        cal_byte_c = cal_byte_c -256
        
    cal_byte_d = int(math.floor(q_four_current / (256**3)))

    tx = [256, 4, 4, 53, 1, 1, 4, cal_byte_a, cal_byte_b, cal_byte_c, calbyte_c, 0, 0, 253]
    tx = calc_checksum(tx)
    tx, unused = format_packet(tx)
                     
    rx = '80 0e 04 35 00 00 43 84 fd'

    msg_len = 9
    tag = "calibration to current 4 pole gain scale factor to etu request"

    return tx, msg_len, tag

def calibration_to_current_four_pole_gain_scale_factor_to_etu_check(current): #Table 359/360

    tx = bytes.fromhex('80 00 04 35 84 35 fd')
    rx = ('80 01 04 35 00 00 84 36 fd')

    msg_len = 9
    tag = "calibration to current 4 pole gain scale factor to etu check"

    return tx, msg_len, tag
                     
                     
def recover_current_calibration_request(): #Table 389/390

    tx = bytex.fromhex('80 04 04 40 84 44 fd')
    rx = '80 0e 04 40 00 00 84 4e fd'
    msg_len = 9
    tag = "Recover Current Calibration"

    return tx, msg_len, tag


def recover_current_calibration_check(): #Table 391/392

    tx = bytes.fromhex('80 00 04 40 84 40 fd')
    rx = '80 01 04 40 00 00 84 41 fd'
    msg_len = 9
    tag = "Recover Current Calibration"

    return tx, msg_len, tag


def set_gain_of_pga_request(gain): #Table 313/314


    packet = [128, 4, 4, 42, 1, 1, 2, 0, gain, 0, 0, fd]
    packet = calc_checksum(packet)
    tx, rx = format_packet(packet)

    rx = '80 0e 04 2a 0 0 84 38 fd'

    msg_len = 9
    tag = "Set Gain Of PGA Request"
    return tx, msg_len, tag

def set_gain_of_pga_check(gain): #Table 315/316

    tx = bytes.fromhex('80 00 04 2a 84 2a fd')
    rx = '80 01 04 2a 00 00 84 2b fd' 

    msg_len = 9
    tag = "Set Gain Of PGA Request"
    
    return tx, msg_len, tag


def calibration_to_sg_scale_factor_request(gain): #Table 317/318


    packet = [128, 4, 4, 43, 1, 1, 4, 0, gain, 0, 0, fd]
    packet = calc_checksum(packet)
    tx, rx = format_packet(packet)

    rx = '80 0e 04 2b 00 00 84 39 fd' 

    msg_len = 9
    tag = "Set Gain Of PGA Request"

    return tx, msg_len, tag

def calibration_to_sg_scale_factor_check(): #Table 319/320

    tx = bytes.fromhex('80 00 04 2b 84 30 fd')
    rx = '80 0e 04 2c 00 00 84 3a fd'
    msg_len = 9
    tag = "Recover Ground Fault Calibration Check"

    return tx, msg_len, tag

def calibration_to_sg_offset_request():#Table 321/322

    tx = bytes.fromhex('80 04 04 2b 84 2b fd')
    rx = '80 01 04 2b 00 00 84 2c fd'
    msg_len = 9
    tag = "Calibration To SG Offset Request"

    return tx, msg_len, tag

def calbiration_to_sg_offset_check(): #Table 323/324

    tx = bytes.fromhex('80 00 03 2c 83 2c fd')
    rx = '80 01 04 2c 00 00 84 2d fd'

    msg_len = 9
    tag = "Calibration To SG Offset Check"

    return tx, msg_len, tag

    
def recover_ground_fault_calibration_request(): #Table 401/402

    tx = bytes.fromhex('80 04 04 43 84 47 fd')
    rx = '80 0e 04 43 00 00 84 51 fd'

    msg_len = 9
    tag = "Recover Ground Fault Calibration Request"

    return tx, msg_len, tag

def recover_ground_fault_calibration_check(): #Table 403/404

    tx = bytes.fromhex('80 00 04 43  84 43 fd')
    rx = '80 01 04 43 00 00 84 44 fd'


    msg_len = 9
    tag = "Recover Ground Fault Calibration Test"

    return tx, msg_len, tag

def read_trip_unit_style_request(): #Table 450/541

    tx = bytes.fromhex('80 04 04 1a 84 1e fd')
    msg_len = 9
    tag = "Read Trip Unit Style Request"
    
    return tx, msg_len, tag

def read_trip_unit_style_response(): #Table 452/453

    tx = bytes.fromhex('80 00 04 1a 84 1a fd')
    msg_len = 12
    tag = "Read Trip Unit Style Check"
    
    return tx, msg_len, tag


def write_trip_unit_style_request(style):#Table 454/455

    packet = [128, 2, 4, 27, 1, 1, 2, 0, style, 0, 0, 0, 253]
    packet = calc_checksum(packet)
    tx, rx = format_packet(packet)

    rx = '80 0e 04 2b 00 00 84 39 fd' 

    msg_len = 9
    tag = "Write Trip Unit Style"

    return tx, msg_len, tag

    
def read_breaker_rating_request():#Table 490

    tx = bytes.fromhex('80 04 04 18 84 1c fd')

    msg_len = 9
    tag = "Read Breaker Rating Request"

    return tx, msg_len, tag

def read_breaker_rating_response(): #Table 491

    tx = bytes.fromhex('80 00 04 18 84 18 fd')

    msg_len = 9
    tag = "Read Breaker Rating Response"

    return tx, msg_len, tag

def read_breaker_plug_request():#Table 461/462

    tx = bytes.fromhex('80 04 04 18 84 1c fd')
    rx = '80 0e 04 18 00 00 84 26 fd'

    msg_len = 9
    tag = "Read Breaker Plug Request"
    return tx, msg_len, tag

def read_breaker_plug_response():#Table 463/464

    tx = bytes.fromhex('80 00 04 18 84 18 fd')
    rx = '80 00 04 18 00 00 01 01 02 00 87 19 fd'

    msg_len = 13
    tag = "Read Breaker Plug Response"
    return tx, msg_len, tag

def write_breaker_plug_request(plug_id): #Table 465/466

    ida = plug_id%256
    idb = plug_id/256
    packet = [128, 2, 4, 25, 1, 1, 2, 0, ida, idb, 0, 0, 253]
    rx = '80 0e 04 19 00 00 84 27 fd'

    packet = calc_checksum(packet)
    tx, rx = format_packet(packet)
    
    msg_len = 9
    tag = "write breaker plug"

    return tx, msg_len, tag


def write_breaker_plug_check(): #Table 467/468

    tx = bytes.fromhex('80 00 04 19 84 19 fd')
    rx = '80 01 04 19 00 00 84 1a fd'

    msg_len = 9
    tag = "write breaker plug response"
    return tx, msg_len, tag
    
def write_breaker_frame_request(frame): #Table 473/474

    fa = int(frame%256)
    fb = int(frame/256)
    packet = [128, 2, 4, 29, 1, 1, 2, 0, fa, fb, 0, 0, 253]
    rx = '80 0e 04 1d 00 00 84 2b fd'

    packet = calc_checksum(packet)
    tx, rx = format_packet(packet)
    
    msg_len = 9
    tag = "write breaker frame"

    return tx, msg_len, tag

def write_breaker_frame_response(): #Table 475/476

    #NF = 0 RF = 1
    tx = bytes.fromhex('80 00 04 1d 84 1d fd')
    rx = '80 01 04 1d 00 00 84 1e fd'

    msg_len = 9
    tag = "write Breaker Frame Response"
    return tx, msg_len, tag


def read_breaker_frame_request(): #Table 469

    tx = bytes.fromhex('80 04 04 1c 84 20 fd')
    rx = '80 0e 04 1c 00 00 84 1e fd'

    msg_len = 9
    tag = "Read Breaker Frame Request"
    return tx, msg_len, tag

def read_breaker_frame_response(): #Table 471

    tx = bytes.fromhex('80 00 04 1c 84 1c fd')
    

    msg_len = 13
    tag = "Read Breaker Frame Response"
    return tx, msg_len, tag

def write_breaker_rating_request(rating):


    rat_two   = math.floor(rating/(256))
    rat_one   = rating%256
    
    tx = [128, 2, 4, 25, 1, 1, 2, 0, rat_one, rat_two, 0, 0, 253] #Table 149 software RMS test with trip request from PC 

    tx = calc_checksum(tx)
    tx, px = format_packet(tx)
    tag = "Write Breaker Rating Request"
    msg_len = 9

    return tx, msg_len, tag

def read_breaker_configuration_request(): #Table 578-579

    tx = bytes.fromhex('80 04 04 6e 84 72 fd')
    msg_len = 9
    tag = "Read Breaker Configuration"
    return tx, msg_len, tag

    
def read_breaker_configuration_response(): #Table 580-581
    
    tx = bytes.fromhex('80 00 04 6e 84 6e fd')
    msg_len = 44
    tag = "Read Breaker Configuration"
    return tx, msg_len, tag

def write_breaker_configuration_request(keys, configuration):

    packet = [128, 2, 4, 111, 1, 1, 34, 0]

    for key in keys:
        packet.append(int(int(configuration[key])%256))
        packet.append(int(int(configuration[key])/256))

    
    
    packet_end = [0, 0, 253]
    packet = packet + packet_end
    
    packet = calc_checksum(packet)
    tx, rx = format_packet(packet)

    msg_len = 9
    tag = "Write Breaker Configuration Request"

    return tx, msg_len, tag
    
def write_breaker_configuation_response():

    tx = bytes.fromhex('80 00 04 6f 84 6f fd')
    msg_len = 9
    tag = "Write Breaker Configuration Response"

    return tx, msg_len, tag

    
def write_breaker_rating_response():

    tx = bytes.fromhex('80 00 04 19 84 19 fd')
    

    msg_len = 9
    tag = "Write Breaker Frame Response"
    return tx, msg_len, tag
    
    
def read_sg_offset_request(): #Table 621/622

    tx = bytes.fromhex('80 04 04 9a 84 9e fd')
    rx = '80 0e 04 9a 00 00 84 a8 fd'

    msg_len = 9
    tag = "Read SG Offset Request"
    return tx, msg_len, tag

def read_sg_offset_check(): #Table 632/624

    tx = bytes.fromhex('80 00 04 9a 84 9a fd')
    rx = '80 0e 04 9a 00 00 84 a8 fd'

    msg_len = 27
    tag = "Read SG Offset Check"
    return tx, msg_len, tag

def software_RMS_test_with_trip_request(phase, current): #Table 149-150

    I_byte_four  = math.floor(current/(256*256*256))
    I_byte_three = math.floor(current/(256*256))
    I_byte_two   = math.floor(current/(256))
    I_byte_one   = math.floor(current%256)

    tx = [128, 4, 3, 6, 1, 1, 6, 0, phase, 0, I_byte_one, I_byte_two, I_byte_three, I_byte_four, 0, 0, 253] #Table 149 software RMS test with trip request from PC 

    rx = ' 80 0e 03 06 00 00 83 14 fd' #Table 150 software RMS test with trip request feedback to PC
    
    tx = calc_checksum(tx)
    tx, px = format_packet(tx)
    tag = "Software RMS Test With Trip Request"
    msg_len = 9

    return tx, msg_len, tag

    
def software_RMS_test_with_trip_check(): #Table 151-152


    tx = '80 00 03 06 83 06 fd'         #Table 151 software RMS test with trip result check from PC (success)
    rx = '80 01 03 06 00 00 83 07 fd'   #Table 152 software RMS test with trip result feedback to PC (success)


    tx = bytes.fromhex(tx)
    msg_len = 9
    tag = "Software RMS Test With Trip Check"

    return tx, msg_len, tag

def software_RMS_test_without_trip_request(phase, current): #Table 157-158
    

    I_byte_four  = math.floor(current/(256*256*256))
    I_byte_three = math.floor(current/(256*256))
    I_byte_two   = math.floor(current/(256))
    I_byte_one   = current%256

    tx = [128, 4, 3, 7, 1, 1, 6, 0, phase, 0, I_byte_one, I_byte_two, I_byte_three, I_byte_four, 0, 0, 253] #Table 157 software RMS test without trip request from PC 

    rx = ' 80 0e 03 07 00 00 83 15 fd' #Table 158 software RMS test without trip request feedback to PC
    
    tx = calc_checksum(tx)
    tx, px = format_packet(tx)
    tag = "Software RMS Test Without Trip Request"
    msg_len = 9 

    return tx, msg_len, tag
    
def software_RMS_test_without_trip_check(): #Table 159-160

    tx ='80 00 03 07 83 07 fd' #Table 159 software RMS test without trip result check from PC 
    rx = '80 01 03 07 00 00 83 08 fd'   #Table 160 software RMS test without trip result feedback to PC (success)

    
    tx = bytes.fromhex(tx)
    msg_len = 9
    tag = "Software RMS Test Without Trip Check"

    return tx, msg_len, tag

def cancel_software_test_request(): #Table 165-166

    tx = '80 04 03 08 83 0c fd' #Table 165 cancel software test request from PC 
    rx = '80 0e 03 08 00 00 83 16 fd' #Table 166 cancel software test request feedback to PC

    tx = bytes.fromhex(tx)
    msg_len = 9
    tag = "Cancel Software Request"

    return tx, msg_len, tag

def cancel_software_test_check(): #Table 167-168

    tx ='80 00 03 08 83 08 fd' #Table 167 cancel software test result check from PC    
    rx = '80 01 03 08 00 00 83 09 fd'   #Table 168 cancel software test result feedback to PC (success)

    
    tx = bytes.fromhex(tx)
    msg_len = 9
    tag = "Cancel Software Test Check"

    
    return tx, msg_len, tag

def secondary_injection_RMS_test_with_trip_request(phase, current): #Table 137-138
    

    I_byte_four  = math.floor(current/(256*256*256))
    I_byte_three = math.floor(current/(256*256))
    I_byte_two   = math.floor(current/(256))
    I_byte_one   = current%256

    tx = [128, 4, 3, 11, 1, 1, 6, 0, phase, 0, I_byte_one, I_byte_two, I_byte_three, I_byte_four, 0, 0, 253] #Table 169 secondary injection RMS test with trip request from PC 

    rx = '80 0e 03 0b 00 00 83 19 fd' #Table 170 secondary injection RMS test with trip request feedback to PC

    tx = calc_checksum(tx)
    tx, px = format_packet(tx)
    
    msg_len = 9
    tag = "Secondary Injectin RMS Test With Trip Request"
    return tx, msg_len, tag

def secondary_injection_RMS_test_with_trip_check(): #Table 139-140
    

    tx ='80 00 03 0b 83 0b fd'       #Table 171 secondary injection RMS test with trip result check from PC    
    rx = '80 01 03 0b 00 00 83 0c fd'   #Table 172 secondary injection RMS test with trip result feedback to PC (success)

    
    tx = bytes.fromhex(tx)
    msg_len = 9
    tag = "Secondary Injection RMS Test With Trip Check"
    
    return tx, msg_len, tag


def secondary_injection_RMS_test_without_trip_request(phase, current): #Table 144-145
    

    I_byte_four  = math.floor(current/(256*256*256))
    I_byte_three = math.floor(current/(256*256))
    I_byte_two   = math.floor(current/(256))
    I_byte_one   = current%256

    tx = [128, 4, 3, 12, 1, 1, 6, 0, phase, 0, I_byte_one, I_byte_two, I_byte_three, I_byte_four, 0, 0, 253] #Table 177 secondary injection RMS test without trip request from PC 

    rx = ' 80 0e 03 0c 00 00 83 1a fd' #Table 178 secondary injection RMS test without trip request feedback to PC
    
    tx = calc_checksum(tx)
    tx, px = format_packet(tx)
    msg_len = 9
    tag = "Secondary Injection RMS Test Without Trip Request"

    return tx, msg_len, tag
    
def secondary_injection_RMS_test_without_trip_check(): #Table 146-147

    tx = '80 00 03 0c 83 0c fd' #Table 179 Secondary Injection RMS test with trip without trip result check from the PC    
    rx = '80 01 03 0c 00 00 83 0d fd'   #Table 180 secondary injection RMS test without trip result feedback to PC (success)

    
    tx = bytes.fromhex(tx)

    msg_len = 9
    tag = "Secondary Injetion RMS Test Without Trip Check"

    return tx, msg_len, tag


def cancel_secondary_injection_test_request(): #Table 150-151

    tx = '80 04 03 0d 83 11 fd'         #Table 185 cancel secondary injection test request from PC 
    rx = '80 0e 03 0d 00 00 83 13 fd'  #Table 186 cancel secondary injection test request feedback to PC

    
    tx = bytes.fromhex(tx)
    msg_len = 9
    tag = "Cancel Secondary Injection Test Request"

    return tx, msg_len, tag

def cancel_secondary_injection_test_check(): #Table 152-153

    tx = '80 04 03 0d 83 0b fd'      #Table 187 cancel secondary injection test result check from PC
    rx = '80 01 03 0d 00 00 83 0e fd'   #Table 188 cancel secondary injection test result feedback to PC (success)

    
    tx = bytes.fromhex(tx)
    
    msg_len = 9
    tag = "Cancel Secondary Injection Test Check"

    return tx, msg_len, tag

def read_simulated_test_results(): #Table 189

    tx = '80 00 03 09 83 09 fd' #Table 189 Package Format of PC Read the Test Result
    tx = bytes.fromhex(tx)
    tag = "Read Simulated Test Results"
    msg_len = 23

    return tx, msg_len, tag

def clear_secondary_injection_request(): #Table 482-483
    
    tx = '80 04 04 2e 84 32 fd' #clear secondary injection factor request from PC    
    rx = '80 0e 0a 49 a2 00 2c 58 fd'
    tx = bytes.fromhex(tx)
    msg_len = 9
    
    tag = "clear secondary injection_request"

    return tx, msg_len, tag
    
def clear_secondary_injection_check(): #Table 482-483
    
    tx = '80 00 04 2e 84 2e fd' #clear secondary injection factor request from PC    
    rx = '80 01 0a 49 00 00 8a 50 fd'
    tx = bytes.fromhex(tx)
    msg_len = 9
    
    tag = "clear secondary injection_check"

    return tx, msg_len, tag

def secondary_injection_base_counter_calibration_request(): #Table 434 - Table 435

    tx = bytes.fromhex('80 04 04 2d 84 31 fd') #Table 434 secondary injection base counter calibration request from PC
    rx = '80 0e 0a 12 0a 00 94 20 fd'   #Table 435 secondary injection base counter calibration request feedback to PC
    msg_len = 9
    tag = "Secondary Injection Base Counter Calibration Request"

    return tx, msg_len, tag

def secondary_injection_base_counter_calibration_check(): #Table 436 - Table 437

    tx = bytes.fromhex('80 00 04 2d 84 2d fd')  #Table 435 secondary injection base counter calibration request from PC
    rx = '80 01 0a 12 00 00 8a 13 fd'   #Table 436 secondary injection base counter calibration request feedback to PC (success)

    msg_len = 9
    tag = "Secondary Injection Base Counter Calibration Check"

    return tx, msg_len, tag

def secondary_injection_delta_counter_request():

    tx = bytes.fromhex('80 04 04 2f 84 33 fd') #Table 438 secondary injection delta counter calibration request from PC
    rx = '80 0e 0a 13 a2 00 8a b0 fd'   #Table 439 secondary injection delta counter calibration request feedback to PC

    msg_len = 9
    tag = "Secondary Injection Delta Counter Request"

    return tx, msg_len, tag

def secondary_injection_delta_counter_check():

    tx = bytes.fromhex('80 00 04 2f 84 2f fd') #Table 440 secondary injection delta counter calibration result check from PC (success)
    rx = '80 01 0a 13 00 00 8a 14 fd'   #Table 441 secondary injection delta counter calibration result feedback to PC (success)

    msg_len = 9
    tag = "Secondary Injection Delta Counter Check"

    return tx, msg_len, tag

def write_internal_diagnostics(keys, setpoint_packet):#Table 31/33


    packet = [128, 2, 4, 195, 1, 1, 53, 0]


    for key in keys:
        packet.append(int(int(setpoint_packet[key])%256))
        packet.append(int(int(setpoint_packet[key])/256))
        
    
    packet_end = [0, 0, 0, 0, 253]

    packet = packet + packet_end
    
    packet = calc_checksum(packet)
    tx, rx = format_packet(packet)
    rx = '80 0e 00 01 00 00 80 0f fd'
    tag = "Write Internal Setpoints"
    msg_len = 9

    return tx, msg_len, tag
