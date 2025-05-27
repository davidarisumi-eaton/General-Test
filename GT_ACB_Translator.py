
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

status_list = {0: "Unkown",
               1: "Normal",
               3: "Instantaneous",
               11: "Over Voltage",
               12: "Under Voltage",
               14: "Aux Power Under Power",
               15: "Over Frequency",
               16: "Under Frequency",
               17: "Current Unbalance",
               18: "Voltage Unbalacne",
               19: "Apparent Power Factor",
               26: "Power Demand",
               27: "VA Demand",
               30: "THD",
               31: "Operations Count",
               33: "Control Via Communicatons",
               37: "Coil Supervision",
               38: "Coil Supervision",
               39: "Diagnostics Warning #1",
               41: "Low Battery",
               61: "Long Delay",
               62: "Short Delay",
               64: "Bad Rating Plug",
               65: "Reverse Power",
               68: "Reverse Sequence",
               69: "Phase Current Loss",
               73: "High Load 1",
               161: "High Load 2",
               159: "Thermal Memory Alarm",
               162: "Ground Fault Pre-alarm",
               163: "High Temperature Alarm",
               75: "Making Current Release",
               76: "Fixed Hardware Inst",
               78: "Setpoints Error",
               80: "Long Delay Neutral Over Current",
               158: "Short Delay Neutral Over Current",
               5: "Inst Neutral Over Current",
               84: "Ground Fault",
               85: "Earth Fault",
               113: "Calibration",
               136: "Real Time Clock",
               153: "MM Mode",
               154: "Breaker Mech Fault",
               155: "Frame Board Version Fault",
               2: "Real Power",
               4: "Reactive Power",
               6: "Reactive Power",
               7: "Apparent Power",
               8: "Under Power Factor",
               9: "Reverse Reactive Power",
               10: "Real Power Demand",
               20: "Apaparent Power Demand",
               21: "Neutral",
               22: "Electric Alarm",
               23: "Current THD",
               24: "Voltage THD",
               999: "Display Over Temperature",
               25: "Time To Trip",
               28: "Thermal Capacity"}

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
        if data_type == "int16":
            val = GT_Conversions.int_sixteen_to_dec(msg, byte_num)
            byte_num = byte_num + 6
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
            print("Q4")
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
            data_amount = data_amount + 6
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
Specialized Methods/Legacy Methods
=================================================================================

    Info:
    When given a specific message, this tranlates the data and returns a packet. This is needed for more complex information, such as strings.

    More info to be written later. 

    
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



def translate_breaker_frame(msg):

    frame = GT_Conversions.uint_sixteen_to_dec(msg, 24)

    return frame

def translate_breaker_rating(msg):

    rating = GT_Conversions.uint_sixteen_to_dec(msg, 24)

    return rating
def translate_style(msg):

    sty_hex_one = msg[24] + msg[25]
    sty_hex_two = msg[27] + msg[28]

    if sty_hex_one == "00":
        pxr = 20
        other = "V000L00C"
        val = 0 
    elif sty_hex_one == "01":
        pxr = 20
        other = "V000L00M"
        val = 1
    elif sty_hex_one == "02":
        pxr = 20
        other = "V000LG0C"
        val = 2
    elif sty_hex_one == "03":
        pxr = 20
        other = "V000LG0M"
        val = 3
    elif sty_hex_one == "04":
        pxr = 20
        other = "V000LGAC"
        val = 4
    elif sty_hex_one == "05":
        pxr = 20
        other = "V000LGAM"
        val = 5
    elif sty_hex_one == "06":
        pxr = 25
        other = "V000L00M"
        val = 6
    elif sty_hex_one =="07":
        pxr = 25
        other = "V000LG0M"
        val = 7
    elif sty_hex_one == "08":
        pxr = 25
        other = "V000L0AM"
        val = 8 
    elif sty_hex_one == "09":
        pxr = 25
        other = "V000LGAM"
        val = 9
    elif sty_hex_one == "0a":
        pxr = 20
        other = "V000L0AM"
        val = 10
    elif sty_hex_one == "0b":
        pxr = 20
        other = "V000L0AC"
        val = 11



    return [pxr, other, val]

def translate_configuration(msg, *argv):

    pol = GT_Conversions.uint_sixteen_to_dec(msg, 24) #Poles
    std = GT_Conversions.uint_sixteen_to_dec(msg, 30) #Standard
    dtp = GT_Conversions.uint_sixteen_to_dec(msg, 36) #Device Type
    rat = GT_Conversions.uint_sixteen_to_dec(msg, 42) #DC Rating Capability
    vol = GT_Conversions.uint_sixteen_to_dec(msg, 48) #Voltage Metering
    iec = GT_Conversions.uint_sixteen_to_dec(msg, 54) #Max IEC  Amps
    ul = GT_Conversions.uint_sixteen_to_dec(msg, 60)  #Max UL489 Amps
    ans = GT_Conversions.uint_sixteen_to_dec(msg, 66) #MAX ANSI Amps
    frm = GT_Conversions.uint_sixteen_to_dec(msg, 72)  #Frame Amps
    mn = GT_Conversions.uint_sixteen_to_dec(msg, 78)  #Min In
    wit = GT_Conversions.uint_sixteen_to_dec(msg, 84) #Max Withstand
    ovr = GT_Conversions.uint_sixteen_to_dec(msg, 90) #Override Circuit
    mcr = GT_Conversions.uint_sixteen_to_dec(msg, 96) #MCR Multiplier
    gf = GT_Conversions.uint_sixteen_to_dec(msg, 102) #GF Current Max
    phy = GT_Conversions.uint_sixteen_to_dec(msg, 108) #Max Physical Interrupting
    irp = GT_Conversions.uint_sixteen_to_dec(msg, 114) #Interrupting Max 
    ins = GT_Conversions.uint_sixteen_to_dec(msg, 120) #Max Instantaneous

    return [pol, std, dtp, rat, vol, iec, ul, ans, frm, mn, wit, ovr, mcr, gf, phy, irp, ins]    

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
            primary_status = "Open"
        elif temp_prim == 2:
            primary_status = "Closed"
        elif temp_prim == 3:
            primary_status = "Tripped" 
        elif temp_prim == 4:
            primary_status = "Alarmed"
        else:
            primary_status = "Picked-Up"

        if temp_sec == 1:
            second_status = "N/A"
        elif temp_sec == 3:
            second_status = "Test Mode"
        elif temp_sec == 7:
            second_status = "Powered_Up Sine Last Trip/Alarm Reset" 
        else:
            second_status = "Alarm"



        global status_list
        if temp_cause in status_list:
            breaker_status = status_list[temp_cause]
        else:
            breaker_status = "Unknown"

            
        int_bin = [int(x) for x in list('{0:0b}'.format(temp_bin))]


        tu_bin = []
        temp_tu_bin = []
        for y in range(0, 15 - len(int_bin)):
            temp_tu_bin.append(0)


        my_len = len(int_bin)
        for val in int_bin:
            temp_tu_bin.append(val)

        #Reverse the order of the bits for correct read
        for k in range(0, len(temp_tu_bin)):
            rev_index = len(temp_tu_bin)-k-1
            val = temp_tu_bin[rev_index]
            tu_bin.append(val)
      

        if tu_bin[0] == 1:
            open_status = "Close"
        else:
            open_status = "Open"

        if tu_bin[1] == 1:
            trip_condition = "Un-acknowledged"
        else:
            trip_condition = "Acknowledged"

        if tu_bin[2] == 1:
            alarm_condition = "Un-acknowledged"
        else:
            alarm_condition = "Acknowledged"

        if tu_bin[4] == 1:
            MM_status = "Enabled"
        else:
            MM_status = "Disabled"


        if tu_bin[5] == 1:
            testing_active = "Active"
        else:
            testing_active = "Inactive"


        if tu_bin[6] == 1:
            testing_forbid = "True"
        else:
            testing_forbid = "False"


        if tu_bin[9] == 1:
            ld_pickup_status = "Active"
        else:
            ld_pickup_status = "Inactive"

        if tu_bin[10] == 1:
            ZIN_status = "Active"
        else:
            ZIN_status = "Inactive"

        if tu_bin[11] == 1:
            Aux_status = "Connected"
        else:
            Aux_status = "Not Connected"

        if tu_bin[12] == 1:
            GF_condition = "Source Ground"
        else:
            GF_condition = "Inactive"

        if tu_bin[13] == 1:
            breaker_position = "Connected"
        else:
            breaker_position = "Not Connected"

        if tu_bin[14] == 1:
            spring_status = "Charged"
        else:
            spring_status = "Not_Charged"

            
        return_buffer = [primary_status,
                      second_status,
                      breaker_status,
                      open_status,
                      trip_condition,
                      alarm_condition,
                      MM_status,
                      testing_active,
                      testing_forbid,
                      ld_pickup_status,
                      ZIN_status,
                      Aux_status,
                      GF_condition,
                      breaker_position,
                      spring_status]

        return return_buffer

def translate_buffer_one(msg, *argv):

        Ia   = GT_Conversions.q_four_to_float(msg, 36)
        Ib   = GT_Conversions.q_four_to_float(msg, 48)
        Ic   = GT_Conversions.q_four_to_float(msg, 60)
        In   = GT_Conversions.q_four_to_float(msg, 72)
        Ig   = GT_Conversions.q_four_to_float(msg, 84)
        
        Van  = GT_Conversions.q_four_to_float_padded(msg, 96) 
        Vbn  = GT_Conversions.q_four_to_float_padded(msg, 102)
        Vcn  = GT_Conversions.q_four_to_float_padded(msg, 108)
        Vab  = GT_Conversions.q_four_to_float_padded(msg, 114)
        Vbc  = GT_Conversions.q_four_to_float_padded(msg, 120)
        Vca  = GT_Conversions.q_four_to_float_padded(msg, 126)
        freq = GT_Conversions.q_four_to_float_padded(msg, 132)

        w    = GT_Conversions.int_thirtytwo_to_dec(msg, 138)
        var  = GT_Conversions.int_thirtytwo_to_dec(msg, 150)
        va   = GT_Conversions.int_thirtytwo_to_dec(msg, 162)
        
        pf   = GT_Conversions.q_ten_to_float_padded(msg, 174)
        temp = GT_Conversions.q_four_to_float_padded(msg, 180)
        bat  = GT_Conversions.q_eight_to_float_padded(msg, 186)
        
        return_array = [Ia, Ib, Ic, In, Ig, Van, Vbn, Vcn, Vab, Vbc, Vca, freq, w, var, va, pf, temp, bat]

        return return_array

        
def translate_buffer_two(msg, *argv):


        fw  = GT_Conversions.uint_sixtyfour_to_dec(msg, 30)
        rvs = GT_Conversions.uint_sixtyfour_to_dec(msg, 54)
        ttl = GT_Conversions.uint_sixtyfour_to_dec(msg, 78)
        net = GT_Conversions.int_sixtyfour_to_dec(msg, 102)
        
        led = GT_Conversions.uint_sixtyfour_to_dec(msg, 126)
        lag = GT_Conversions.uint_sixtyfour_to_dec(msg, 150)
        tre = GT_Conversions.uint_sixtyfour_to_dec(msg, 174)
        nre = GT_Conversions.int_sixtyfour_to_dec(msg, 198)
        
        ape = GT_Conversions.uint_sixtyfour_to_dec(msg, 222)
        lre_date = GT_Conversions.convert_to_date(msg, 246)    

        return_array = [fw, rvs, ttl, net, led, lag, nre, tre, ape, lre_date]

        return return_array

def translate_buffer_three(msg, *argv):

        pdi = GT_Conversions.uint_sixteen_to_dec(msg, 30)
        rpd = GT_Conversions.int_thirtytwo_to_dec(msg, 36)
        epd = GT_Conversions.int_thirtytwo_to_dec(msg, 48)
        apd = GT_Conversions.uint_thirtytwo_to_dec(msg, 60)

        return_array = [pdi, rpd, epd, apd]

        return return_array

def translate_buffer_four(msg, *argv):


        
        mwd      = GT_Conversions.uint_thirtytwo_to_dec(msg, 30)   
        mwd_date = GT_Conversions.convert_to_date(msg, 42)

        mvd      = GT_Conversions.uint_thirtytwo_to_dec(msg, 66)   
        mvd_date = GT_Conversions.convert_to_date(msg, 78)

        mad      = GT_Conversions.uint_thirtytwo_to_dec(msg, 102)
        mad_date = GT_Conversions.convert_to_date(msg, 114)
        
        ltr_date = GT_Conversions.convert_to_date(msg, 138)
                                                  
        return_array = [mwd, mwd_date, mvd, mvd_date, mad, mad_date, ltr_date]

        return return_array



def translate_buffer_five(msg, *argv):

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


        return_array = [mia, mib, mic, mmin, mig, sia, sib, sic, sin, sig,
                       iat_date, ibt_date, ict_date, int_date, igt_date,
                       sat_date, sbt_date, sct_date, snt_date, sgt_date, rst_date]

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
        vbc = GT_Conversions.q_four_to_float_padded(msg, 60)
        vca = GT_Conversions.q_four_to_float_padded(msg, 90)
        sab = GT_Conversions.q_four_to_float_padded(msg, 120)
        sbc = GT_Conversions.q_four_to_float_padded(msg, 150)
        sca = GT_Conversions.q_four_to_float_padded(msg, 180)

        tma = GT_Conversions.convert_to_date(msg, 36)       
        tmb = GT_Conversions.convert_to_date(msg, 66)  
        tmc = GT_Conversions.convert_to_date(msg, 96)   
        tsa = GT_Conversions.convert_to_date(msg, 126)       
        tsb = GT_Conversions.convert_to_date(msg, 156)     
        tsc = GT_Conversions.convert_to_date(msg, 186)  
        ltr_date = GT_Conversions.convert_to_date(msg, 210)      

        return_array = [vab, tma, vbc, tmb, vca, tmc, sab, tsa, sbc, tsb, sca, tsc, ltr_date]

        return return_array


def translate_buffer_eight(msg, *argv):

        van = GT_Conversions.q_four_to_float_padded(msg, 30)
        vbn = GT_Conversions.q_four_to_float_padded(msg, 60)
        vcn = GT_Conversions.q_four_to_float_padded(msg, 90)
        san = GT_Conversions.q_four_to_float_padded(msg, 120)
        sbn = GT_Conversions.q_four_to_float_padded(msg, 150)
        scn = GT_Conversions.q_four_to_float_padded(msg, 180)

        tma = GT_Conversions.convert_to_date(msg, 36)       
        tmb = GT_Conversions.convert_to_date(msg, 66)  
        tmc = GT_Conversions.convert_to_date(msg, 96)   
        tsa = GT_Conversions.convert_to_date(msg, 126)       
        tsb = GT_Conversions.convert_to_date(msg, 156)     
        tsc = GT_Conversions.convert_to_date(msg, 186)  
        ltr_date = GT_Conversions.convert_to_date(msg, 210)      

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
        #rs = GT_Conversions.uint_thirtytwo_to_dec(msg, 186)

        return_array = [tsc, sdc, itc, htc, tot, ldt, gft, toc,
                        trc, tec, ooc, moc, tlo, mt, tmt, rm, rh, rd, lp]


        return return_array
def translate_read_customer_breaker_health(msg, *argv):
    oc = GT_Conversions.uint_sixteen_to_dec(msg, 36)
    tcr = GT_Conversions.uint_thirtytwo_to_dec(msg, 72)
    tmr = GT_Conversions.uint_thirtytwo_to_dec(msg, 42)
    ttr = GT_Conversions.uint_thirtytwo_to_dec(msg, 54)
    cw = GT_Conversions.uint_sixteen_to_dec(msg, 78)
    mw = GT_Conversions.uint_sixteen_to_dec(msg, 84)
    tw = GT_Conversions.uint_sixteen_to_dec(msg, 90)
    lpr = GT_Conversions.uint_sixteen_to_dec(msg, 96)

    return_array = [oc, tcr, tmr, ttr, cw, mw, tw, lpr]

    return return_array
    
def translate_read_internal_breaker_health(msg, *argv):
    oc = GT_Conversions.uint_sixteen_to_dec(msg, 36)
    tcr = GT_Conversions.uint_thirtytwo_to_dec(msg, 72)
    tmr = GT_Conversions.uint_thirtytwo_to_dec(msg, 42)
    ttr = GT_Conversions.uint_thirtytwo_to_dec(msg, 54)
    cw = GT_Conversions.uint_sixteen_to_dec(msg, 78)
    mw = GT_Conversions.uint_sixteen_to_dec(msg, 84)
    tw = GT_Conversions.uint_sixteen_to_dec(msg, 90)
    lpr = GT_Conversions.uint_sixteen_to_dec(msg, 96)
    
    return_array = [oc, tcr, tmr, ttr, cw, mw, tw, lpr]

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

        
        data_amount = msg[21] + msg[22]
        print(data_amount)
        if data_amount != "2c":
            syv = GT_Conversions.uint_sixteen_to_dec(msg, 156) # System Voltage
            neu = GT_Conversions.uint_sixteen_to_dec(msg, 162) #Neutral Sensor
            sgs = GT_Conversions.uint_sixteen_to_dec(msg, 168) #Source Ground Sensor
        else:
            syv = 0
            neu = 0
            sgs = 0 
        

        return_array = [rtg, frm, sto, stt, mm, mml, lf, rf, sin, pwn, pin, lan, lcd, ron,
                        rtw, rth, pol, cwi, cin, hth, syv, neu, sgs]

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
        thma = GT_Conversions.uint_sixteen_to_dec(msg, 174) #Thermal Alarm

        return_array = [ri, bf, tu, tut, tmm, zsi, lds, ldpu, ldt, hla, sds, sdpu, sdt,
                        ipu, gsen, gfy, gfs, gfpu, gft, gthm, npr, hlat, gfa, thma]

        
        return return_array

def translate_setpoint_two(msg, *argv):

        mca = GT_Conversions.uint_sixteen_to_dec(msg, 30) #Modbus Communication Address
        mbr = GT_Conversions.uint_sixteen_to_dec(msg, 36) #Modbus Baude Rate
        mp  = GT_Conversions.uint_sixteen_to_dec(msg, 42) #Modbus Pairty
        msb = GT_Conversions.uint_sixteen_to_dec(msg, 48) #Modbus Stop Bit

        return_array = [mca, mbr, mp, msb]

        return return_array

def translate_setpoint_three(msg, *argv):


            
        stat = GT_Conversions.uint_sixteen_to_dec(msg, 24) #CAM Status
        ca   = GT_Conversions.uint_sixteen_to_dec(msg, 30) #CAM communication address
        br   = GT_Conversions.uint_sixteen_to_dec(msg, 36) #Cam Baud Rate
        par  = GT_Conversions.uint_sixteen_to_dec(msg, 42) #CAM Stop Pairity
        sb   = GT_Conversions.uint_sixteen_to_dec(msg, 48)  #CAM Stop Bit
        inca = GT_Conversions.uint_sixteen_to_dec(msg, 54) #INCOM CAM Address
        inbr = GT_Conversions.uint_sixteen_to_dec(msg, 60) #INCOM CAM Baud Rate
        dhcp = GT_Conversions.uint_sixteen_to_dec(msg, 66) #DHCP Enable
        ipm  = GT_Conversions.uint_sixteen_to_dec(msg, 72) #CAM IP Address MSB
        ipca = GT_Conversions.uint_sixteen_to_dec(msg, 78) #CAM IP Address
        ipcb = GT_Conversions.uint_sixteen_to_dec(msg, 84) #CAM IP Address
        iplb = GT_Conversions.uint_sixteen_to_dec(msg, 90) #CAM IP Address LSB
        ipsm = GT_Conversions.uint_sixteen_to_dec(msg, 96) #CAM Subnet Mask
        dg   = GT_Conversions.uint_sixteen_to_dec(msg, 102) #CAM Default Gateway
        dgt  = GT_Conversions.uint_sixteen_to_dec(msg, 108) #CAM Default Gateway
        rp   = GT_Conversions.uint_sixteen_to_dec(msg, 114) #CAM Reset Pin
        pca  = GT_Conversions.uint_sixteen_to_dec(msg, 120) #Profibus CAM Address

        return_array = [stat, ca, br, par, sb, inca, inbr, dhcp, ipm, ipca, ipcb, iplb, ipsm, dg, dgt, rp, pca]

        return return_array

def translate_setpoint_five(msg, *argv):


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
                        rpf, rpp, rpt, prs, prf, hlf, hlt, xa, xb, xc, xd, xe]

        return return_array


def translate_internal_diagnostics(msg, *argv):

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

def translate_external_diagnostics(msg, *argv):

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

def translate_firmware(msg):

    print(str(msg[22]))
    if msg[22] == "A":
        m_one_v = GT_Conversions.uint_eight_to_dec(msg,24)
        m_one_r = GT_Conversions.uint_eight_to_dec(msg,27)
        m_one_d = GT_Conversions.uint_sixteen_to_dec(msg,30)
        m_two_v = GT_Conversions.uint_eight_to_dec(msg,36)
        m_two_r = GT_Conversions.uint_eight_to_dec(msg,39)
        m_two_d = GT_Conversions.uint_sixteen_to_dec(msg,42)
        pc_v = GT_Conversions.uint_eight_to_dec(msg,48)
        pc_r = GT_Conversions.uint_eight_to_dec(msg,51)
        f_v = GT_Conversions.uint_eight_to_dec(msg,54)
        f_r = GT_Conversions.uint_eight_to_dec(msg,57)
        f_d = GT_Conversions.uint_sixteen_to_dec(msg,60)
    else:

        m_one_v = GT_Conversions.uint_eight_to_dec(msg,24)
        m_one_r = GT_Conversions.uint_eight_to_dec(msg,27)
        m_one_d = GT_Conversions.uint_sixteen_to_dec(msg,30)
        m_two_v = GT_Conversions.uint_eight_to_dec(msg,36)
        m_two_r = GT_Conversions.uint_eight_to_dec(msg,39)
        m_two_d = GT_Conversions.uint_sixteen_to_dec(msg,42)
        pc_v = 0
        pc_r = 0
        f_v = GT_Conversions.uint_eight_to_dec(msg,48)
        f_r = GT_Conversions.uint_eight_to_dec(msg,51)
        f_d = GT_Conversions.uint_sixteen_to_dec(msg,54)
        
    return_array = [m_one_v, m_one_r, m_one_d, m_two_v, m_two_r, m_two_d, pc_v, pc_r, f_v, f_r, f_d]


    return return_array


    





    
