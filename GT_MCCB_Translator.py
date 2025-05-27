'''---------------------------------------------------------------------
    
    Company:    EATON COROPORATION
            
                Proprietary Information
                (C) Copyright 2016
                All rights reserved
                
                PXR MCCB Automation - Protection  
    
-------------------------------------------------------------------------------
    
    Authors:    David Arisumi
                Eaton Corporation
                1000 Cherrington Parkway
                Moon Twp, PA 15108-4312
                (412) 893-3300
                
-------------------------------------------------------------------------------
    
    Product:    Automated test system to test the PXR10, PXR20, PXR2D, PXR25, 
                and PXR35 protection algorithms for the SR, NZM, and NRX 
                breaker frames.   
                
    Module:     MCCB_Translator.py
                
    Mechanics:  Trnalstes USB Commands to MCCB Setpoints

----------------------------------------------------------------------------'''

from struct import *
from GT import GT_Conversions


'''
The purpose of this program is to translate messages from the ACB into usable information.

GT_Conversions contains the methods of actually translating the bytes into useful types
'''



'''
Generic Methods
=================================================================================

    Info:
    ACB messages are recieved in this format aa aa aa dd dd dd dd dd xx xx xx
    aa: message information - This designates what message is being sent
    dd: data infrormation - This desginates that bytes that make up the data in the message such as rating or setpoints. 
    xx: ending designators - This is the checksum as well as an fd byte to mark the end of the message

    translate generic(with and without write) uses a dictionary the contains the following array [value, data_type] and an array to
    itterate through the dictionary. 
    

    Limitations: 
    Generic Translate can handle the Data Types Uint08/16/32, int32/64, Q4/8/10, Flat and Date. For strings and other data types, more
    specialized translate data. 


    translate_generic(msg, key_array, dictionary):
        Input:
            msg(string) - USB message recieved from the ACB unit.
            key_array(array) - array of keys used to itterate through the dictionary
            dictionary(dictionary{key:[int/float, string]}) - Dictionary that contains the value we are looking for and the data type of that value

        Output:
            None
        Changes:
            Index 0 of dictionary.

    translate_generic_no_write(msg, key_array, dictionary):
        Input:
            msg(string) - USB message recieved from the ACB unit.
            key_array(array) - array of keys used to itterate through the dictionary
            dictionary(dictionary{key:[int/float, string]}) - Dictionary that contains the value we are looking for and the data type of that value

        Output:
            None
        Changes:
            val_array(array): array containing the data part of the trip unit.

    calc_data_amount(key_array, dictionary):
        Input:
            key_array(array) - array of keys used to itterate through the dictionary
            dictionary(dictionary{key:[int/float, string]}) - Dictionary that contains the value we are looking for and the data type of that value

        Output:
            data_amount(int): the amount of data needed to run it. 
        Changes:
            None   

    
'''


def translate_generic(msg, key_array, dictionary):

    val_array = translate_generic_no_write(msg, key_array, dictionary)

    i = 0
    for key in key_array:   
        dictionary[key][0] = val_array[i]
        i = i + 1


def translate_generic_no_write(msg, key_array, dictionary):

    val_array = []
    message_length = (len(msg)+1)

    da = calc_data_amount(key_array, dictionary)
    byte_num = message_length - da - 9 #Subtracts length of the message from the data amount and 9(3 bytes of checksum and endbyte)

    
    for key in key_array:
        data_type = dictionary[key][1]
        if data_type == "Uint08":
            val = GT_Conversions.uint_eight_to_dec(msg, byte_num) #Rating
            byte_num = byte_num + 3
        if data_type == "Uint16":
            val = GT_Conversions.uint_sixteen_to_dec(msg, byte_num) #Rating
            byte_num = byte_num + 6
        if data_type == "Uint32":
            val = GT_Conversions.uint_thirtytwo_to_dec(msg, byte_num)
            byte_num = byte_num + 12
        if data_type == "Uint64":
            val = GT_Conversions.uint_sixtyfour_to_dec(msg, byte_num)
            byte_num = byte_num + 15
        if data_type == "int32":
            val = GT_Conversions.int_thirtytwo_to_dec(msg, byte_num)
            byte_num = byte_num + 12
        if data_type == "int64":
            val = GT_Conversions.int_sixtyfour_to_dec(msg, byte_num)
            byte_num = byte_num + 15
        if data_type == "Q4":
            val = GT_Conversions.q_four_to_float(msg, byte_num)
            byte_num = byte_num + 12
        if data_type == "Q10Padded":
            val = GT_Conversions.q_ten_to_float_padded(msg, byte_num)
            byte_num = byte_num + 6
        if data_type == "Q4Padded":
            val = GT_Conversions.q_four_to_float_padded(msg,byte_num)
            byte_num = byte_num + 6
        if data_type == "Q8Padded":
            val = GT_Conversions.q_eight_to_float_padded(msg, byte_num)
            byte_num = byte_num + 6
        if data_type == "Float":
            val = GT_Conversions.hex_to_float(msg,byte_num)
            byte_num = byte_num + 12
        if data_type == "Date":
            val = GT_Conversions.convert_to_date(msg, byte_num)
            byte_num = byte_num + 24

        val_array.append(val)

        

        
    return val_array

def calc_data_amount(key_array, dictionary):

    data_amount = 0 
    for key in key_array:
        data_type = dictionary[key][1]
        if data_type == "Uint08":
            data_amount = data_amount + 3
        if data_type == "Uint16":
            data_amount = data_amount + 6
        if data_type == "Uint32":
            data_amount = data_amount + 12
        if data_type == "Uint64":
            data_amount = data_amount + 15
        if data_type == "int32":
            data_amount = data_amount + 12
        if data_type == "int64":
            data_amount = data_amount + 15
        if data_type == "Q4":
            data_amount = data_amount + 12
        if data_type == "Q10Padded":
            data_amount = data_amount + 6
        if data_type == "Q4Padded":
            data_amount = data_amount + 6
        if data_type == "Q8Padded":
            data_amount = data_amount + 6
        if data_type == "Float":
            data_amount = data_amount + 12
        if data_type == "Date":
            data_amount = data_amount + 24

    return data_amount

'''
Specific Translations
=============================================
'''

def translate(def_name, msg, *argv):

    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(def_name)

    
    if not method:
        print(def_name, " is not a method")
        return False
    else:
        if len(argv) == 0:
            array = method(msg)
        elif len(argv) == 1:
            array = method(msg, argv[0])

        

    return array

        
def translate_style(msg):

    sto_hex_one =  (msg[24])+(msg[25])
    sto_hex_two =  (msg[27])+(msg[28])
    
    hex_sto    = '0x' + sto_hex_two + sto_hex_one
    sto_bin    = (int(hex_sto, 0))
    print("HEX")
    print(hex_sto)



    int_bin = [int(x) for x in list('{0:0b}'.format(sto_bin))]

    style_one_bin = []
    if len(int_bin) < 14:
        for y in range(0, 14 - len(int_bin)):
            style_one_bin.append(0)
    for val in int_bin:
        style_one_bin.append(val)
        
  
    stt_hex_one =  (msg[30])+(msg[31])
    stt_hex_two =  (msg[33])+(msg[34])
    
    hex_stt    = '0x' + stt_hex_two + stt_hex_one
    stt_bin    = (int(hex_stt, 0))  


    int_bin = [int(x) for x in list('{0:0b}'.format(stt_bin))]

    style_two_bin = []
    if len(int_bin) < 6:
        for y in range(0, 6 - len(int_bin)):
            style_two_bin.append(0)
    for val in int_bin:
        style_two_bin.append(val)


    print(style_one_bin)
    print(style_two_bin)
    return_array = [style_one_bin, style_two_bin]
    return return_array

def translate_setpoint_zero(msg, *argv):

    rtg = GT_Conversions.uint_sixteen_to_dec(msg, 36) #Rating
    frm = GT_Conversions.uint_sixteen_to_dec(msg, 42) #Breaker Frame
    sto = GT_Conversions.uint_sixteen_to_dec(msg, 48) #Style 1
    stt = GT_Conversions.uint_sixteen_to_dec(msg, 54) #Style 2
    mm = GT_Conversions.uint_sixteen_to_dec(msg, 60)  #MM Enable
    mml = GT_Conversions.uint_sixteen_to_dec(msg, 66) #MM Level
    lf = GT_Conversions.uint_sixteen_to_dec(msg, 72)  #Line Frequency
    rf = GT_Conversions.uint_sixteen_to_dec(msg, 78)  # Reverse Feed 
    sin = GT_Conversions.uint_sixteen_to_dec(msg, 84) # Sign Convention
    pwn = GT_Conversions.uint_sixteen_to_dec(msg, 90) # Power Demand Window
    pin = GT_Conversions.uint_sixteen_to_dec(msg, 96) # Power Deman Interval
    lan = GT_Conversions.uint_sixteen_to_dec(msg, 102) #Laguage Setting
    lcd = GT_Conversions.uint_sixteen_to_dec(msg, 108) #LCD Rotation
    ron = GT_Conversions.uint_sixteen_to_dec(msg, 114) #Relay 1 Configuration
    rtw = GT_Conversions.uint_sixteen_to_dec(msg, 120) #Relay 2 Configuration
    rth = GT_Conversions.uint_sixteen_to_dec(msg, 126) #Relay 3 Configuration
    pol = GT_Conversions.uint_sixteen_to_dec(msg, 132) #Pole A Location
    cwi = GT_Conversions.uint_sixteen_to_dec(msg, 138) #Current Window
    cin = GT_Conversions.uint_sixteen_to_dec(msg, 144) #Current Interval
    hth = GT_Conversions.uint_sixteen_to_dec(msg, 150) #Breaker Health Alarm Level
        
    return_array = [rtg, frm, sto, stt, mm, mml, lf, rf, sin, pwn, pin, lan, lcd, ron,
                    rtw, rth, pol, cwi, cin, hth]

    return return_array                                

 
def translate_setpoint_one(msg, *argv):
    
    ri = GT_Conversions.uint_sixteen_to_dec(msg, 36) #Rating Information
    bf = GT_Conversions.uint_sixteen_to_dec(msg, 42) #Breaker Frame
    tu = GT_Conversions.uint_sixteen_to_dec(msg, 48) #Trip Unit Style 1
    tut= GT_Conversions.uint_sixteen_to_dec(msg, 54) #Trip Unit Style 2
    tmm = GT_Conversions.uint_sixteen_to_dec(msg, 60) #Thermal Memory 
    zsi = GT_Conversions.uint_sixteen_to_dec(msg, 66) #ZSI
    lds = GT_Conversions.uint_sixteen_to_dec(msg, 72) #Long Delay Slope
    ldpu = GT_Conversions.uint_sixteen_to_dec(msg, 78) #Long Delay Pickup
    ldt = GT_Conversions.uint_sixteen_to_dec(msg, 84) #Long Delay Time
    hla = GT_Conversions.uint_sixteen_to_dec(msg, 90) #High Load 1
    sds = GT_Conversions.uint_sixteen_to_dec(msg, 96) #Short Delay Slope
    sdpu = GT_Conversions.uint_sixteen_to_dec(msg, 102) #Short Delay Pickup
    sdt = GT_Conversions.uint_sixteen_to_dec(msg, 108) #Short Delay Time
    ipu = GT_Conversions.uint_sixteen_to_dec(msg, 114) #Instantaneous Pickup
    gsen = GT_Conversions.uint_sixteen_to_dec(msg, 120) #Ground Sensing Type
    gfy = GT_Conversions.uint_sixteen_to_dec(msg, 126) #Ground Fault Protectio Type
    gfs = GT_Conversions.uint_sixteen_to_dec(msg, 132) #Ground Fault SLope
    gfpu = GT_Conversions.uint_sixteen_to_dec(msg, 138) #Ground Fault Pickup
    gft = GT_Conversions.uint_sixteen_to_dec(msg, 144) #Ground Fault Time
    gthm = GT_Conversions.uint_sixteen_to_dec(msg, 150) #Ground Thermal 
    npr = GT_Conversions.uint_sixteen_to_dec(msg, 156) #Neutral Protection Ratio
    hlat = GT_Conversions.uint_sixteen_to_dec(msg, 162) #High Load 2
    gfa = GT_Conversions.uint_sixteen_to_dec(msg, 168) #Ground Fault Alarm


    return_array = [ri, bf, tu, tut, tmm, zsi, lds, ldpu, ldt, hla, sds, sdpu, sdt,
                    ipu, gsen, gfy, gfs, gfpu, gft, gthm, npr, hlat, gfa]

    
    return return_array

def translate_setpoint_two(msg, *argv):
    
    mca = GT_Conversions.uint_sixteen_to_dec(msg, 36) #Modbut Communication Address
    mbr = GT_Conversions.uint_sixteen_to_dec(msg, 42) #Modbus Baud Rate
    mbp = GT_Conversions.uint_sixteen_to_dec(msg, 48) #Modbus Parity
    msb= GT_Conversions.uint_sixteen_to_dec(msg, 54) #Modbus Stop Bit

    return_array = [mca, mbr, mbp, msb]
    
    return return_array

def translate_setpoint_three(msg, *argv):

    bit = GT_Conversions.uint_sixteen_to_dec(msg, 36) #Byte Data Object
    cca = GT_Conversions.uint_sixteen_to_dec(msg, 42) #CAM communication address
    cbr = GT_Conversions.uint_sixteen_to_dec(msg, 48) #Cam Baud Rate
    cpr= GT_Conversions.uint_sixteen_to_dec(msg, 54) #CAM Parity
    csb= GT_Conversions.uint_sixteen_to_dec(msg, 60) #CAM Stop Bit
    ica= GT_Conversions.uint_sixteen_to_dec(msg, 66) #INCOM CAM IP Address MSB
    ibr = GT_Conversions.uint_sixteen_to_dec(msg, 72) #INCOM CAM Baud Rate
    ede = GT_Conversions.uint_sixteen_to_dec(msg, 78) #Ethernet CAM DHCP Enable
    emb = GT_Conversions.uint_sixteen_to_dec(msg, 84) #Ethernet CAM IP Address MSB
    eip = GT_Conversions.uint_sixteen_to_dec(msg, 90) #Ethernet CAM IP Address
    eia = GT_Conversions.uint_sixteen_to_dec(msg, 96) #Ethernet CAM IP Address
    eil = GT_Conversions.uint_sixteen_to_dec(msg, 102) #Ethernet CAM IP ADDRESS LSB
    esm = GT_Conversions.uint_sixteen_to_dec(msg, 108) #Ethernet Cam Subnet Mask
    edg = GT_Conversions.uint_sixteen_to_dec(msg, 114) #Ethernet CAM Default Gateway
    eda = GT_Conversions.uint_sixteen_to_dec(msg, 120) #Ethernet CAM Default Gateway
    erp = GT_Conversions.uint_sixteen_to_dec(msg, 126) #Ethernet CAM Reset Pin
    pca = GT_Conversions.uint_sixteen_to_dec(msg, 132) #Profibus CAM Commnication Address



    return_array = [bit, cca, cbr, cpr, csb, ica, ibr, ede, emb, eip, eia, eil, esm,
                    edg, eda, erp, pca]

    
    return return_array

def translate_setpoint_four(msg, *argv):

    fdo = GT_Conversions.uint_sixteen_to_dec(msg, 36) #Functionality of digital output 1
    fda = GT_Conversions.uint_sixteen_to_dec(msg, 42) #Functionatlity of Digital Output 2
    fdb = GT_Conversions.uint_sixteen_to_dec(msg, 48) #Functionatlity of Digital Output 3
    fdc= GT_Conversions.uint_sixteen_to_dec(msg, 54) #Functionality of Digital Output 3
    cao= GT_Conversions.uint_sixteen_to_dec(msg, 60) #Chanel 0 s0 output
    car= GT_Conversions.uint_sixteen_to_dec(msg, 66) #Chanel 0 pulse refrence
    cad = GT_Conversions.uint_sixteen_to_dec(msg, 72) #Channnel 0 Pulse Duration
    cbo = GT_Conversions.uint_sixteen_to_dec(msg, 78) #Channel 1 s0 output
    cbr= GT_Conversions.uint_sixteen_to_dec(msg, 84) #Channel 1 Pulse Refrence
    cbd = GT_Conversions.uint_sixteen_to_dec(msg, 90) #Channel 1 Pulse Duration
    mac = GT_Conversions.uint_sixteen_to_dec(msg, 96) #Modbus Address Fieldbus Channel
    mbc = GT_Conversions.uint_sixteen_to_dec(msg, 102) #Modbus Baudrate Fieldbus Channel
    mpc = GT_Conversions.uint_sixteen_to_dec(msg, 108) #Modbus Pairty Fieldbus Channel
    xa = GT_Conversions.uint_sixteen_to_dec(msg, 114) #Reserved For Future Use
    xb = GT_Conversions.uint_sixteen_to_dec(msg, 120) #Reserved For Future Use
    xc = GT_Conversions.uint_sixteen_to_dec(msg, 126) #Reserved For Future Use
    xd = GT_Conversions.uint_sixteen_to_dec(msg, 132) #Reserved For Future Use
    xe = GT_Conversions.uint_sixteen_to_dec(msg, 132) #Reserved For Future Use
    xf = GT_Conversions.uint_sixteen_to_dec(msg, 132) #Reserved For Future Use
    xg = GT_Conversions.uint_sixteen_to_dec(msg, 132) #Reserved For Future Use
    xh = GT_Conversions.uint_sixteen_to_dec(msg, 132) #Reserved For Future Use
    xi = GT_Conversions.uint_sixteen_to_dec(msg, 132) #Reserved For Future Use
    xj = GT_Conversions.uint_sixteen_to_dec(msg, 132) #Reserved For Future Use
    xk = GT_Conversions.uint_sixteen_to_dec(msg, 132) #Reserved For Future Use



    return_array = [fdo, fda, fdb, fdc, cao, car, cad, cbo, cbr, cbd, mac, mbc, mpc, xa,
                    xb, xc, xd, xe, xf, xg, xh, xi, xj, xk]
    
    return return_array

def translate_setpoint_five(msg):


        ovf  = GT_Conversions.uint_sixteen_to_dec(msg, 36) #Over Voltage Feature
        ovp  = GT_Conversions.uint_sixteen_to_dec(msg, 42) #Over Voltage Pickup
        ovt  = GT_Conversions.uint_sixteen_to_dec(msg, 48) #Over Voltage Time
        uvf  = GT_Conversions.uint_sixteen_to_dec(msg, 54) #Under Voltage Featuer
        uvp  = GT_Conversions.uint_sixteen_to_dec(msg, 60) #Under Voltage Pickup
        uvt  = GT_Conversions.uint_sixteen_to_dec(msg, 66) #Under Voltage TIme
        vuf  = GT_Conversions.uint_sixteen_to_dec(msg, 72) #Voltage Unbalanced Feature
        vup  = GT_Conversions.uint_sixteen_to_dec(msg, 78) #Voltage Unbalanced Pickup
        vut  = GT_Conversions.uint_sixteen_to_dec(msg, 84) #Voltage Unbalnced Time
        cuf  = GT_Conversions.uint_sixteen_to_dec(msg, 90) #Current Unbalanced Feature
        cup  = GT_Conversions.uint_sixteen_to_dec(msg, 96) #Current Unbalanced Pickup
        cut  = GT_Conversions.uint_sixteen_to_dec(msg, 102) #Current Unbalanced Time
        rpf  = GT_Conversions.uint_sixteen_to_dec(msg, 108) #Reverse Power Feature
        rpp  = GT_Conversions.uint_sixteen_to_dec(msg, 114) #Reverse Power Pickup
        rpt  = GT_Conversions.uint_sixteen_to_dec(msg, 120) #Reverse Power Time
        prs  = GT_Conversions.uint_sixteen_to_dec(msg, 126) #Phase Reverse Sensing
        prf  = GT_Conversions.uint_sixteen_to_dec(msg, 132) #Phase Reverse Feature
        hlf  = GT_Conversions.uint_sixteen_to_dec(msg, 138) #Phase Loss Feature
        hlt  = GT_Conversions.uint_sixteen_to_dec(msg, 144) #Phase Loss Time
        xa   = GT_Conversions.uint_sixteen_to_dec(msg, 150) #Reserved A
        xb   = GT_Conversions.uint_sixteen_to_dec(msg, 156) #Reserved B
        xc   = GT_Conversions.uint_sixteen_to_dec(msg, 162) #Reserved C
        xd   = GT_Conversions.uint_sixteen_to_dec(msg, 168) #Reserved D
        xe   = GT_Conversions.uint_sixteen_to_dec(msg, 174) #Reserved E

        return_array = [ovf, ovp, ovt, uvf, uvp, uvt, vuf, vup, vut, cuf, cup, cut,
                        rpf, rpp, rpt, prs, prf, hlf, hlt, xa, xb, sc, sd, xe]

        return return_array
                                             
def translate_buffer_zero(msg, *argv):

    stat_hex_one     =  (msg[24])+(msg[25])
    stat_hex_two     =  (msg[27])+(msg[28])
    stat_hex_four    =  (msg[30])+(msg[31])
    stat_hex_three   =  (msg[33])+(msg[34])

    bin_hex_two =  (msg[36])+(msg[37])
    bin_hex_one =  (msg[39])+(msg[40])

    hex_prim    = '0x' + stat_hex_one
    hex_sec     = '0x' + stat_hex_two
    hex_cause   = '0x' + stat_hex_three + stat_hex_four
    hex_bin     = '0x' + bin_hex_one + bin_hex_two

    temp_prim        = (int(hex_prim, 0))
    temp_sec         = (int(hex_sec, 0))
    temp_cause       = (int(hex_cause, 0))
    temp_bin         = (int(hex_bin, 0))  


    if temp_prim == 1:
        ps = "Open"
    elif temp_prim == 2:
        ps = "Closed"
    elif temp_prim == 3:
        ps = "Tripped" 
    elif temp_prim == 4:
        ps = "Alarmed"
    else:
        ps = "Picked-Up"

    if temp_sec == 1:
        ss = "N/A"
    elif temp_sec == 3:
        ss = "Test Mode"
    elif temp_sec == 7:
        ss = "Powered_Up Sine Last Trip/Alarm Reset" 
    else:
        ss = "Alarm"


    if temp_cause == 0:
        bs = "Unkown"
    elif temp_cause == 1:
        bs = "Normal"
    elif temp_cause == 3:
        bs = "Instantaneous"
    elif temp_cause ==14:
        bs = "Current Unbalanced"
    elif temp_cause ==15:
        bs = "Voltage Unbalanced"
    elif temp_cause ==31:
        bs = "Operations Count"
    elif temp_cause ==33:
        bs = "Control Via Communications"
    elif temp_cause ==37:
        bs = "Coil Supervision"
    elif temp_cause ==41:
        bs = "Battery Low Voltage Alarm"
    elif temp_cause ==43:
        bs = "Battery Low Voltage"
    elif temp_cause ==61:
        bs = "Long Delay"
    elif temp_cause ==62:
        bs = "Short Delay"
    elif temp_cause ==65:
        bs = "Reverse Power"
    elif temp_cause ==68:
        bs = "Phase Rotation"
    elif temp_cause ==68:
        bs = "Phase Rotation"
    elif temp_cause ==69:
        bs = "Phase Loss"
    elif temp_cause ==69:
        bs = "Phase Loss"
    elif temp_cause ==73:
        bs = "High Load"
    elif temp_cause ==75:
        bs = "Making Current Release"
    elif temp_cause ==76:
        bs = "Fixed Hardware Instantaneous"
    elif temp_cause ==77:
        bs = "Setpoints Error"
    elif temp_cause ==78:
        bs = "Over Temperature"
    elif temp_cause ==80:
        bs = "Long Delay Neutral OVer Current"
    elif temp_cause ==84:
        bs = "Ground Fault"
    elif temp_cause ==85:
        bs = "Earth Fault"
    elif temp_cause==113:
        bs = "Calibration"
    elif temp_cause ==136:
        bs = "Real Time Clock"
    elif temp_cause ==153:
        bs = "MM Mode"
    elif temp_cause ==2458:
        bs = "Breaker Mechanism Fault"
    elif temp_cause ==2044:
        bs = "Digital Bypass"
    elif temp_cause ==2045:
        bs = "NV Memory Failure"
    elif temp_cause ==2046:
        bs = "Watchdog Fault"
    else:
        bs = "Motor Alarm Or Trip"

        
    int_bin = [int(x) for x in list('{0:0b}'.format(temp_bin))]

    tu_bin = []
    for y in range(0, 15 - len(int_bin)):
        tu_bin.append(0)
    for val in int_bin:
        tu_bin.append(val)
        
  

    if tu_bin[0] == 1:
        tu = "Close"
    else:
        tu = "Open"

    if tu_bin[1] == 1:
        tri = "Un-acknowledged"
    else:
        tri = "Acknowledged"

    if tu_bin[2] == 1:
        ac = "Un-acknowledged"
    else:
        ac = "Acknowledged"

    if tu_bin[3] == 1:
        mm = "Enabled"
    else:
        mm = "Disabled"

    if tu_bin[4] == 1:
        tms = "Active"
    else:
        tms = "Inactive"


    if tu_bin[5] == 1:
        tf = "True"
    else:
        tf = "False"


    if tu_bin[6] == 1:
        frb = "True"
    else:
        frb = "False"


    if tu_bin[7] == 1:
        pu = "Active"
    else:
        pu = "Inactive"

    if tu_bin[8] == 1:
        zin = "Active"
    else:
        zin = "Inactive"

    if tu_bin[9] == 1:
        gf = "Source Ground"
    else:
        gf = "Inactive"

    return_array = [ps, ss, bs, tu, tri, ac, mm, tms, tf, frb, pu, zin, gf]
    
    return return_array
                         
def translate_buffer_one(msg, *argv):

    pxr = argv[0][0]
    print("Translating Buffer ONe")
    if pxr == "PXR25":
        eia  = GT_Conversions.hex_to_float(msg, 36)
        eib  = GT_Conversions.hex_to_float(msg, 48)
        eic  = GT_Conversions.hex_to_float(msg, 60)
        ein  = GT_Conversions.hex_to_float(msg, 72)
        eig  = GT_Conversions.hex_to_float(msg, 84)
        van  = GT_Conversions.hex_to_float(msg, 96)
        vbn  = GT_Conversions.hex_to_float(msg, 108)
        vcn  = GT_Conversions.hex_to_float(msg, 120)
        vab  = GT_Conversions.hex_to_float(msg, 132)
        vbc  = GT_Conversions.hex_to_float(msg, 144)
        vca  = GT_Conversions.hex_to_float(msg, 156)
        fre  = GT_Conversions.hex_to_float(msg, 168)
        wat  = GT_Conversions.hex_to_float(msg, 180)
        var  = GT_Conversions.hex_to_float(msg, 192)
        va   = GT_Conversions.hex_to_float(msg, 204)
        pf   = GT_Conversions.hex_to_float(msg, 216)
        temp = GT_Conversions.q_four_to_float_padded(msg, 228)
        bat  = GT_Conversions.q_four_to_float_padded(msg, 234)

        ##    temp_val = (int(hex_temp, 0))/(2**4)
        ##    batt_val = (int(hex_batt, 0))/(2**8)
        
    else: 
        eia  = GT_Conversions.q_four_to_float(msg, 36)
        eib  = GT_Conversions.q_four_to_float(msg, 48)
        eic  = GT_Conversions.q_four_to_float(msg, 60)
        ein  = GT_Conversions.q_four_to_float(msg, 72)
        eig  = GT_Conversions.q_four_to_float(msg, 84)
        van  = GT_Conversions.hex_to_float(msg, 96)
        vbn  = GT_Conversions.hex_to_float(msg, 108)
        vcn  = GT_Conversions.hex_to_float(msg, 120)
        vab  = GT_Conversions.hex_to_float(msg, 132)
        vbc  = GT_Conversions.hex_to_float(msg, 144)
        vca  = GT_Conversions.hex_to_float(msg, 156)
        fre  = GT_Conversions.hex_to_float(msg, 168)
        wat  = GT_Conversions.hex_to_float(msg, 180)
        var  = GT_Conversions.hex_to_float(msg, 192)
        va   = GT_Conversions.hex_to_float(msg, 204)
        pf   = GT_Conversions.uint_thirtytwo_to_dec(msg, 216)
        temp = GT_Conversions.q_four_to_float_padded(msg, 228)
        bat  = GT_Conversions.q_four_to_float_padded(msg, 234)

        
    return_array = [eia, eib, eic, ein, eig, van, vbn, vcn, vab, vbc, vca, fre, wat, var, va, pf, temp, bat]

    return return_array

    
def translate_buffer_two(msg, *argv):

    fwe =  GT_Conversions.int_thirtytwo_to_dec(msg, 30)
    rve =  GT_Conversions.int_thirtytwo_to_dec(msg, 42)
    tte =  GT_Conversions.int_thirtytwo_to_dec(msg, 54)
    nee =  GT_Conversions.int_thirtytwo_to_dec(msg, 66)
    lde =  GT_Conversions.int_thirtytwo_to_dec(msg, 78)
    lge =  GT_Conversions.int_thirtytwo_to_dec(msg, 90)
    tre =  GT_Conversions.int_thirtytwo_to_dec(msg, 102)
    nre =  GT_Conversions.int_thirtytwo_to_dec(msg, 114)
    ape =  GT_Conversions.int_thirtytwo_to_dec(msg, 126)
    ler =  GT_Conversions.convert_to_date(msg, 138)

    return_array = [fwe, rve, tte, nee, lde, lge, tre, nre, ape, ler]
    return return_array

def translate_buffer_three(msg, *argv):

    pdi  = GT_Conversions.uint_sixteen_to_dec(msg, 30)
    rpd  = GT_Conversions.hex_to_float(msg, 36)
    epd  = GT_Conversions.hex_to_float(msg, 48)
    apd  = GT_Conversions.hex_to_float(msg, 60)
    
    return_array = [pdi, rpd, epd, apd]
    return return_array
    
def translate_buffer_four(msg, *argv):

        mwd      = GT_Conversions.hex_to_float(msg, 30)   
        mwd_date = GT_Conversions.convert_to_date(msg, 42)

        mvd      = GT_Conversions.hex_to_float(msg, 66)   
        mvd_date = GT_Conversions.convert_to_date(msg, 78)

        mad      = GT_Conversions.hex_to_float(msg, 102)
        mad_date = GT_Conversions.convert_to_date(msg, 114)
        
        ltr_date = GT_Conversions.convert_to_date(msg, 138)
                                                  
        return_array = [mwd, mwd_date, mvd, mvd_date, mad, mad_date, ltr_date]

        return return_array



def translate_buffer_five(msg, *argv):

    pxr = argv[0]
        
    if pxr == "PXR25":
        mia  = GT_Conversions.hex_to_float(msg, 36)
        mib  = GT_Conversions.hex_to_float(msg, 72)
        mic  = GT_Conversions.hex_to_float(msg, 108)
        mmin = GT_Conversions.hex_to_float(msg, 144)
        mig  = GT_Conversions.hex_to_float(msg, 180)
        sia  = GT_Conversions.hex_to_float(msg, 216)
        sib  = GT_Conversions.hex_to_float(msg, 252)
        sic  = GT_Conversions.hex_to_float(msg, 288)
        sin  = GT_Conversions.hex_to_float(msg, 324)
        sig  = GT_Conversions.hex_to_float(msg, 360)
    else:
        mia  = GT_Conversions.q_four_to_float(msg, 36)
        mib  = GT_Conversions.q_four_to_float(msg, 72)
        mic  = GT_Conversions.q_four_to_float(msg, 108)
        mmin = GT_Conversions.q_four_to_float(msg, 144)
        mig  = GT_Conversions.q_four_to_float(msg, 180)
        sia  = GT_Conversions.q_four_to_float(msg, 216)
        sib  = GT_Conversions.q_four_to_float(msg, 252)
        sic  = GT_Conversions.q_four_to_float(msg, 288)
        sin  = GT_Conversions.q_four_to_float(msg, 324)
        sig  = GT_Conversions.q_four_to_float(msg, 360)
            
    iat_date =  GT_Conversions.convert_to_date(msg, 48)
    ibt_date =  GT_Conversions.convert_to_date(msg, 84)
    ict_date =  GT_Conversions.convert_to_date(msg, 120)
    int_date =  GT_Conversions.convert_to_date(msg, 156)
    igt_date =  GT_Conversions.convert_to_date(msg, 192)
    sat_date =  GT_Conversions.convert_to_date(msg, 228)
    sbt_date =  GT_Conversions.convert_to_date(msg, 264)
    sct_date =  GT_Conversions.convert_to_date(msg, 300)
    snt_date =  GT_Conversions.convert_to_date(msg, 336)
    sgt_date =  GT_Conversions.convert_to_date(msg, 372)
    rst_date =  GT_Conversions.convert_to_date(msg, 396)

    return_array = [mia, iat_date, mib, ibt_date, mic, ict_date, mmin, int_date,
                    mig, igt_date, sia, sat_date, sib, sbt_date, sic, sct_date,
                    sin, snt_date, sig, sgt_date, rst_date]

    return return_array

def translate_buffer_six(msg, *argv):

    tsc = GT_Conversions.uint_sixteen_to_dec(msg, 36)
    sdc = GT_Conversions.uint_sixteen_to_dec(msg, 42)
    itc = GT_Conversions.uint_sixteen_to_dec(msg, 48)
    htc = GT_Conversions.uint_sixteen_to_dec(msg, 54)
    tot = GT_Conversions.uint_sixteen_to_dec(msg, 60)
    ldt = GT_Conversions.uint_sixteen_to_dec(msg, 66)
    gft = GT_Conversions.uint_sixteen_to_dec(msg, 72)
    toc = GT_Conversions.uint_sixteen_to_dec(msg, 78)
    trc = GT_Conversions.uint_sixteen_to_dec(msg, 84)
    tec = GT_Conversions.uint_sixteen_to_dec(msg, 90)
    ooc = GT_Conversions.uint_sixteen_to_dec(msg, 96)
    moc = GT_Conversions.uint_sixteen_to_dec(msg, 102)
    tlo = GT_Conversions.convert_to_date(msg, 108)
    mt  = GT_Conversions.q_four_to_float_padded(msg, 132)
    tmt = GT_Conversions.convert_to_date(msg, 138)
    rm  = GT_Conversions.uint_sixteen_to_dec(msg, 162)
    rh  = GT_Conversions.uint_sixteen_to_dec(msg, 168) 
    rd  = GT_Conversions.uint_sixteen_to_dec(msg, 174)
    lp  = GT_Conversions.uint_thirtytwo_to_dec(msg, 180)


    return_array = [tsc, sdc, itc, htc, tot, ldt, gft, toc,
                    trc, tec, ooc, moc, tlo, mt, tmt, rm, rh, rd, lp]

    return return_array
    

def translate_buffer_seven(msg, *argv):

    vab = GT_Conversions.q_four_to_float_padded(msg, 30)
    vbc = GT_Conversions.q_four_to_float_padded(msg, 66)
    vca = GT_Conversions.q_four_to_float_padded(msg, 102)
    sab = GT_Conversions.q_four_to_float_padded(msg, 138)
    sbc = GT_Conversions.q_four_to_float_padded(msg, 168)
    sca = GT_Conversions.q_four_to_float_padded(msg, 210)

    tma = GT_Conversions.convert_to_date(msg, 42)       
    tmb = GT_Conversions.convert_to_date(msg, 78)  
    tmc = GT_Conversions.convert_to_date(msg, 114)   
    tsa = GT_Conversions.convert_to_date(msg, 150)       
    tsb = GT_Conversions.convert_to_date(msg, 186)     
    tsc = GT_Conversions.convert_to_date(msg, 222)  
    ltr_date = GT_Conversions.convert_to_date(msg, 246)      

    return_array = [vab, tma, vbc, tmb, vca, tmc, sab, tsa, sbc, tsb, sca, tsc, ltr_date]

    return return_array

    
    
def translate_buffer_eight(msg, *argv):
    
   
    van = GT_Conversions.q_four_to_float_padded(msg, 30)
    vbn = GT_Conversions.q_four_to_float_padded(msg, 66)
    vcn = GT_Conversions.q_four_to_float_padded(msg, 102)
    san = GT_Conversions.q_four_to_float_padded(msg, 138)
    sbn = GT_Conversions.q_four_to_float_padded(msg, 168)
    scn = GT_Conversions.q_four_to_float_padded(msg, 210)

    tma = GT_Conversions.convert_to_date(msg, 42)       
    tmb = GT_Conversions.convert_to_date(msg, 78)  
    tmc = GT_Conversions.convert_to_date(msg, 114)   
    tsa = GT_Conversions.convert_to_date(msg, 150)       
    tsb = GT_Conversions.convert_to_date(msg, 186)     
    tsc = GT_Conversions.convert_to_date(msg, 222)  
    ltr_date = GT_Conversions.convert_to_date(msg, 246)      

    return_array = [van, tma, vbn, tmb, vcn, tmc, san, tsa, sbn, tsb, scn, tsc, ltr_date]


    return return_array
    
def translate_buffer_ten(msg, *argv):


    ia   = GT_Conversions.q_four_to_float(msg, 30)
    ib   = GT_Conversions.q_four_to_float(msg, 42)
    ic   = GT_Conversions.q_four_to_float(msg, 54)
    in_  = GT_Conversions.q_four_to_float(msg, 66)
    ig   = GT_Conversions.q_four_to_float(msg, 78)

    return_array = [ia, ib, ic, in_, ig]

    return return_array

    
def translate_buffer_eleven(msg, *argv):
    tsc = GT_Conversions.uint_sixteen_to_dec(msg, 36)
    sdc = GT_Conversions.uint_sixteen_to_dec(msg, 42)
    itc = GT_Conversions.uint_sixteen_to_dec(msg, 48)
    htc = GT_Conversions.uint_sixteen_to_dec(msg, 54)
    tot = GT_Conversions.uint_sixteen_to_dec(msg, 60)
    ldt = GT_Conversions.uint_sixteen_to_dec(msg, 66)
    gft = GT_Conversions.uint_sixteen_to_dec(msg, 72)
    toc = GT_Conversions.uint_sixteen_to_dec(msg, 78)
    trc = GT_Conversions.uint_sixteen_to_dec(msg, 84)
    tec = GT_Conversions.uint_sixteen_to_dec(msg, 90)
    ooc = GT_Conversions.uint_sixteen_to_dec(msg, 96)
    moc = GT_Conversions.uint_sixteen_to_dec(msg, 102)
    tlo = GT_Conversions.convert_to_date(msg, 108)
    mt  = GT_Conversions.q_four_to_float_padded(msg, 132)
    tmt = GT_Conversions.convert_to_date(msg, 138)
    rm  = GT_Conversions.uint_sixteen_to_dec(msg, 162)
    rh  = GT_Conversions.uint_sixteen_to_dec(msg, 168) 
    rd  = GT_Conversions.uint_sixteen_to_dec(msg, 174)
    lp  = GT_Conversions.uint_thirtytwo_to_dec(msg, 180)


    return_array = [tsc, sdc, itc, htc, tot, ldt, gft, toc,
                    trc, tec, ooc, moc, tlo, mt, tmt, rm, rh, rd, lp]


    return return_array


def translate_buffer_twelve(msg, *argv):

    awa   = GT_Conversions.hex_to_float(msg, 30)
    bwa   = GT_Conversions.hex_to_float(msg, 42)
    cwa   = GT_Conversions.hex_to_float(msg, 54)
    twa   = GT_Conversions.hex_to_float(msg, 66)
    avr   = GT_Conversions.hex_to_float(msg, 78)
    bvr   = GT_Conversions.hex_to_float(msg, 90)
    cvr   = GT_Conversions.hex_to_float(msg, 102)
    tvr   = GT_Conversions.hex_to_float(msg, 114)
    ava   = GT_Conversions.hex_to_float(msg, 126)
    bva   = GT_Conversions.hex_to_float(msg, 138)
    cva   = GT_Conversions.hex_to_float(msg, 150)
    tva   = GT_Conversions.hex_to_float(msg, 162)

    return_array = [awa, bwa, cwa, twa, avr, bvr, cvr, tvr, ava, bva, cva, tva]

    return return_array


    
def translate_buffer_thirteen(msg, *argv):

    hex_eo_two   = msg[24] + msg[25]
    hex_eo_one   = msg[27] + msg[28]
    
    hex_et_one  = msg[30] + msg[31]
    hex_et_two  = msg[33] + msg[34]

    hex_eo = '0x' + hex_eo_two  + hex_eo_one
    hex_et = '0x' + hex_et_two  + hex_et_one

    
    temp_eo = (int(hex_eo, 0))
    my_eo = [int(x) for x in list('{0:0b}'.format(temp_eo))]

    eo_bin = []
    for y in range(0, 15 - len(my_eo)):
        eo_bin.append(0)
    for val in my_eo:
        eo_bin.append(val)
        

    temp_et = (int(hex_et, 0))
    my_et = [int(x) for x in list('{0:0b}'.format(temp_et))]

    et_bin = []
    for y in range(0, 15 - len(my_et)):
        et_bin.append(0)
    for val in my_eo:
        et_bin.append(val)
                      
    if eo_bin[0] == 1:   #USB Connected
        uccs = "Connected"
    else:
        uccs = "Disconnected"


    if eo_bin[1] == 1: #BSM1 State
        bsmo = "Close"
    else:
        bsmo = "Open"

    if eo_bin[2] == 1: #BSM2 State
        bsmt = "Trip"
    else:
        bsmt = "Non-Trip"

    if eo_bin[3] == 1: #Arms Switch State
        ast = "Enabled"
    else:
        ast = "Disabled"

    if eo_bin[4] == 1: #Arms Communication State
        acs = "Enabled"
    else:
        acs = "Disabled"

    if eo_bin[5] == 1: #Arms Secondary State
        aps = "Enabled"
    else:
        aps = "Disabled"

    if eo_bin[6] == 1:#Arms Artical State
        aas = "Enabled"
    else:
        aas = "Disabled"


    if et_bin[0] == 1: #1st Full Scan
        ffs= "Enabled"
    else:
        ffs = "Disabled"
                      
    if et_bin[1] == 1: #Setpoints Changed States
        scs = "Changed"
    else:
        scs = "Not Changed"

    if et_bin[2] == 1: #Reset Button State
        rbs = "Pressed"
    else:
        rbs = "Not Pressed"

    if et_bin[3] == 1: #Reset Trip Unit From Push Buton
        rtu= "Pressed"
    else:
        rtu = "Not Pressed"
        
    if et_bin[4] == 1: #Reset From Comms
        rfc= "Pressed"
    else:
        rfc = "Not Pressed"
                      
    if et_bin[5] == 1: #Up Button Pressed
        ubs = "Pressed"
    else:
        ubs = "Not Pressed"

    if et_bin[6] == 1: #Down Button 
        dbs = "Pressed"
    else:
        dbs = "Not Pressed"
                             
    if et_bin[7] == 1: #Enter Button
        ebs = "Pressed"
    else:
        ebs = "Not Pressed"

    if et_bin[8] == 1: #Control Relay One
        crs = "Closed"
    else:
        crs = "Open"

    if et_bin[9] == 1: #Control Relay Two
        crt = "Closed"
    else:
        crt = "Open"

    if et_bin[10] == 1: #Control Relay Three
        crf = "Closed"
    else:
        crf = "Open"


    return_array = [uccs, bsmo, bsmt, ast, acs, aps, aas, ffs, scs, rbs, rtu, rfc, ubs, dbs, ebs, crs, crt, crf]

    return return_array

def translate_breaker_capacity(repos, msg):        


    fa_hex_two       =   msg[24] + msg[25]
    fa_hex_one       =   msg[27] + msg[28]

    pol_hex_two      =   msg[30] + msg[31]
    pol_hex_one      =   msg[33] + msg[34]

    std_hex_two      =   msg[36] + msg[37]
    std_hex_one      =   msg[39] + msg[40]

    ct_hex_two       =   msg[42] + msg[43]
    ct_hex_one       =   msg[45] + msg[46]

    wth_hex_four     =   msg[48] + msg[49]
    wth_hex_three    =   msg[51] + msg[52]
    wth_hex_two      =   msg[54] + msg[55]
    wth_hex_one      =   msg[57] + msg[58]

    mcr_hex_four     =   msg[60] + msg[61]
    mcr_hex_three    =   msg[63] + msg[64]
    mcr_hex_two      =   msg[66] + msg[67]
    mcr_hex_one      =   msg[69] + msg[70]

    inp_hex_four     =   msg[72] + msg[73]
    inp_hex_three    =   msg[75] + msg[76]
    inp_hex_two      =   msg[78] + msg[79]
    inp_hex_one      =   msg[81] + msg[82]

    ctn_hex_four     =   msg[84] + msg[85]
    ctn_hex_three    =   msg[87] + msg[88]
    ctn_hex_two      =   msg[90] + msg[91]
    ctn_hex_one      =   msg[93] + msg[94]

    hex_fa  = '0x' + fa_hex_one + fa_hex_two
    hex_pol = '0x' + pol_hex_one + pol_hex_two
    hex_std = '0x' + std_hex_one + std_hex_two
    hex_ct  = '0x' + ct_hex_one + ct_hex_two
    hex_wth = '0x' + wth_hex_one + wth_hex_two + wth_hex_three + wth_hex_four
    hex_mcr = '0x' + mcr_hex_one + mcr_hex_two + mcr_hex_three + mcr_hex_four
    hex_inp = '0x' + inp_hex_one + inp_hex_two + inp_hex_three + inp_hex_four
    hex_ctn = '0x' + ctn_hex_one + ctn_hex_two + ctn_hex_three + ctn_hex_four

    repos.breaker_protection_capacity['frame_ap'][0]             = (int(hex_fa, 0))
    repos.breaker_protection_capacity['poles'] [0]               = (int(hex_pol, 0))
    repos.breaker_protection_capacity['standard'][0]             = (int(hex_std, 0))
    repos.breaker_protection_capacity['ct_version'][0]           = (int(hex_ct, 0))
    repos.breaker_protection_capacity['withstand'][0]            = (int(hex_wth, 0))
    repos.breaker_protection_capacity['MCR'][0]                 = (int(hex_mcr, 0))
    repos.breaker_protection_capacity['max_interupt_label'][0]  = (int(hex_inp, 0))
    repos.breaker_protection_capacity['frame_construction'][0]   = (int(hex_ctn, 0))

def translate_breaker_frame(msg):

    frm_hex_two   = (msg[24])+(msg[25])
    frm_hex_one   = (msg[27])+(msg[28])
    frm_hex       = '0x' + frm_hex_one + frm_hex_two
    frame         = (int(frm_hex, 0))
    
    return frame 

def translate_breaker_rating(msg):

    rtg_hex_two   = (msg[24])+(msg[25])
    rtg_hex_one   = (msg[27])+(msg[28])
    rtg_hex = '0x' + rtg_hex_one + rtg_hex_two
    rating = (int(rtg_hex, 0))
    
    return rating

def translate_real_time_clock(rsp):

    date = GT_Conversions.convert_to_date(rsp, 24)

    return date
def convert_to_date(repos, hex_one, hex_two, hex_three, hex_four, hex_five, hex_six, hex_svn, hex_egt):

    hex_year   = '0x' + hex_svn + hex_egt
    hex_month  = '0x' + hex_six
    hex_day    = '0x' + hex_five
    hex_hour   = '0x' + hex_four
    hex_min    = '0x' + hex_three
    hex_sec    = '0x' + hex_two
    
    year   =  int(hex_year,  0) 
    month  = int(hex_month, 0)
    day    = int(hex_day, 0)
    hour   = int(hex_hour, 0)
    minute = int(hex_min, 0)
    sec    = int(hex_sec, 0)

    date = '{:0>2}/{:0>2}/{:0>4} {:0>2}:{:0>2}:{:0>2}'.format(month, day, year, hour, minute, sec)
    return date



