import math


'''
=========================================================================================================================================================================================
Bytes to Number 
=========================================================================================================================================================================================

'''

def uint_eight_to_dec(msg, start):

    s = start
    
    hex_one     =  (msg[s])   + (msg[s+1])

    hex_final = "0x" + hex_one 


    dec_val = int(hex_final, 0)

    return dec_val

def uint_sixteen_to_dec(msg, start):

    s = start
    
    hex_two     =  (msg[s])   + (msg[s+1])
    hex_one     =  (msg[s+3]) + (msg[s+4])


    hex_final = "0x" + hex_one + hex_two 


    dec_val = int(hex_final, 0)

    return dec_val

def uint_thirtytwo_to_dec(msg, start):

    s = start
    
    hex_four   =  (msg[s])   + (msg[s+1])
    hex_three  =  (msg[s+3]) + (msg[s+4])
    hex_two    =  (msg[s+6]) + (msg[s+7])
    hex_one    =  (msg[s+9]) + (msg[s+10])

    hex_final = "0x" + hex_one + hex_two + hex_three + hex_four 


    dec_val = int(hex_final, 0)

    return dec_val

def uint_sixtyfour_to_dec(msg, start):

    s = start
    hex_egt     =  (msg[s])    +(msg[s+1])
    hex_svn    =  (msg[s+3])  +(msg[s+4])
    hex_six     =  (msg[s+6])  +(msg[s+7])
    hex_five    =  (msg[s+9])  +(msg[s+10])
    hex_four    =  (msg[s+12]) +(msg[s+13])
    hex_three   =  (msg[s+15]) +(msg[s+16])
    hex_two     =  (msg[s+18]) +(msg[s+19])
    hex_one     =  (msg[s+21]) +(msg[s+22])

    hex_final = "0x" + hex_one + hex_two + hex_three + hex_four + hex_four + hex_five + hex_six + hex_svn + hex_egt
    dec_val = int(hex_final, 0)

    return dec_val

    
def q_four_to_float(msg, start):

    s = start
    hex_one      = msg[s]
    hex_two      = msg[s+3]
    hex_three    = msg[s+4]
    hex_four     = msg[s+6]
    hex_five     = msg[s+7]
    dec_hex   = msg[s+1]
        
    qfour    = int(dec_hex, 16)
    mantissa = qfour/float(16)

    myByte = hex_two + hex_three + hex_one
    addition_byte = hex_four+hex_five

    addition_num = int(addition_byte, 16)
    whole_num = int(myByte, 16)
    
    final_val = whole_num + mantissa + (addition_num*4096)

    return final_val

def q_four_to_float_padded(msg, start):

    s = start
    hex_one      = msg[s]
    hex_two      = msg[s+3]
    hex_three    = msg[s+4]
    hex_four     = "00"
    hex_five     = "00"
    dec_hex   = msg[s+1]
    
    qfour    = int(dec_hex, 16)
    mantissa = qfour/float(16)

    myByte = hex_two + hex_three + hex_one
    addition_byte = hex_four+hex_five

    addition_num = int(addition_byte, 16)
    whole_num = int(myByte, 16)
    
    final_val = whole_num + mantissa + (addition_num*4096)

    return final_val


def q_eight_to_float_padded(msg, start):

    s = start
    hex_one    = msg[s]
    hex_two    = msg[s+3]
    hex_three  = msg[s+4]
    hex_four   = "00"
    hex_five    = "00"
    dec_hex    = msg[s+1]


    qeight    = int(dec_hex, 16)
    mantissa = qeight/float(256)

    myByte = hex_two + hex_three + hex_one
    addition_byte = hex_four+hex_five

    addition_num = int(addition_byte, 16)
    whole_num = float(int(myByte, 16)/16)

    print(str(mantissa))
    print(str(whole_num))
    print(str(addition_num))
    final_val = whole_num + mantissa + (addition_num*4096)

    return final_val

def q_ten_to_float_padded(msg, start):

    s = start
    hex_one    = msg[s]
    hex_two    = msg[s+3]
    hex_three  = msg[s+4]
    hex_four   = "00"
    hex_five    = "00"
    dec_hex    = msg[s+1]

        
    qeight    = int(dec_hex, 16)
    mantissa = qeight/float(1024)

    myByte = hex_two + hex_three + hex_one
    addition_byte = hex_four+hex_five

    addition_num = int(addition_byte, 16)
    whole_num = int(myByte, 16)
    
    final_val = whole_num + mantissa + (addition_num*4096)

    return final_val


def int_sixteen_to_dec(msg, start):

    s = start
    
    hex_two     =  (msg[s])   + (msg[s+1])
    hex_one     =  (msg[s+3]) + (msg[s+4])


    hex_final = "0x" + hex_one + hex_two 

    dec_val = hex_to_two_compliment(hex_final, 64)

    return dec_val

def int_thirtytwo_to_dec(msg, start):

    s = start
    
    hex_four   =  (msg[s])   + (msg[s+1])
    hex_three  =  (msg[s+3]) + (msg[s+4])
    hex_two    =  (msg[s+6]) + (msg[s+7])
    hex_one    =  (msg[s+9]) + (msg[s+10])

    hex_final = "0x" + hex_one + hex_two + hex_three + hex_four 

    dec_val = hex_to_two_compliment(hex_final, 32)

    return dec_val

def int_sixtyfour_to_dec(msg, start):

    s = start

    hex_egt     =  (msg[s])    +(msg[s+1])
    hex_svn    =  (msg[s+3])  +(msg[s+4])
    hex_six     =  (msg[s+6])  +(msg[s+7])
    hex_five    =  (msg[s+9])  +(msg[s+10])
    hex_four    =  (msg[s+12]) +(msg[s+13])
    hex_three   =  (msg[s+15]) +(msg[s+16])
    hex_two     =  (msg[s+18]) +(msg[s+19])
    hex_one     =  (msg[s+21]) +(msg[s+22])

    hex_final = "0x" + hex_one + hex_two + hex_three + hex_four + hex_four + hex_five + hex_six + hex_svn + hex_egt

    dec_val = hex_to_two_compliment(hex_final, 64)

    return dec_val

def hex_to_two_compliment(hex_final, bits):

    uval = int(hex_final,16)

    if uval & (1 << (bits -1)) !=0:
        uval = uval - (1 << bits)

    return uval
    

def hex_to_float(msg, start):


    s = start
    
    hex_one     =  (msg[s])   + (msg[s+1])
    hex_two     =  (msg[s+3]) + (msg[s+4])
    hex_three   =  (msg[s+6]) + (msg[s+7])
    hex_four    =  (msg[s+9]) + (msg[s+10])

    hex_final = "0x" + hex_four + hex_three + hex_two + hex_one

    
    
    bin_array = [None]*32
    
    int_val = int(hex_final, 16)
    bin_val = "{0:04b}".format(int_val)
    
    pad_num = 32 - len(bin_val)
    for x in range(0, pad_num):
        bin_val = '0' + bin_val
    
    x = 0 
    for char in bin_val:
        bin_array[x] = int(char)
        x= x+1
   
    sign = 1
    exponent = 0
    significand = 1.0
    addition = 0.00
    
    if bin_array[0] == '1':
        sign = -1
    for val in range(1,9):
        exponent = exponent + bin_array[val] * (2 ** (8 - val))
        
    x = 1
    for val in range(9,31):
        addition = int(bin_array[val]) * 1.000/(2**x)
        significand = significand + addition
        x = x+1

    float_val = sign * 2**(exponent-127) * significand

    float_val = round(float_val,4)
    
    if float_val < .01:
        float_val = 0


    return float_val


def convert_to_date(msg, start):

    s = start
    hex_egt      =  (msg[s])    +(msg[s+1])
    hex_svn      =  (msg[s+3])  +(msg[s+4])
    hex_six      =  (msg[s+6])  +(msg[s+7])
    hex_five     =  (msg[s+9])  +(msg[s+10])
    hex_four     =  (msg[s+12]) +(msg[s+13])
    hex_three    =  (msg[s+15]) +(msg[s+16])
    hex_two      =  (msg[s+18]) +(msg[s+19])
    hex_one      =  (msg[s+21]) +(msg[s+22])
    
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
    
'''
=========================================================================================================================================================================================
Internal Conversions
=========================================================================================================================================================================================

'''

def convert_standard_to_etu(repos):   #  convert master setpoints        


    for key in repos.sp_one_keys:
        etu_key = "Etu " + key
        repos.etu_dictionary[etu_key][0] = repos.etu_dictionary[key][0]
        repos.etu_dictionary[etu_key][0] = round(repos.etu_dictionary[etu_key][0],0)

    if repos.family == "35":
        repos.etu_dictionary['Etu LD Time'][0] = repos.etu_dictionary['LD Time'][0]*100
        repos.etu_dictionary['Etu LD Time'][0] = round(repos.etu_dictionary['Etu LD Time'][0],0)
    else:
        repos.etu_dictionary['Etu LD Time'][0] = repos.etu_dictionary['LD Time'][0]*10
        repos.etu_dictionary['Etu LD Time'][0] = round(repos.etu_dictionary['Etu LD Time'][0],0)
        
    repos.etu_dictionary['Etu SD PU'][0] = round(repos.etu_dictionary['SD PU'][0]*10,0)
    
    if repos.family == "ACB":
        repos.etu_dictionary['Etu SD Time'][0] = repos.etu_dictionary['SD Time'][0]*100
        repos.etu_dictionary['Etu GF Time'][0] = repos.etu_dictionary['GF Time'][0]*100
    elif repos.family == "35":
        repos.etu_dictionary['Etu SD Time'][0] = round(repos.etu_dictionary['SD Time'][0]*100,0)
        repos.etu_dictionary['Etu GF Time'][0] = round(repos.etu_dictionary['GF Time'][0]*100,0)
    else:
        repos.etu_dictionary['Etu SD Time'][0] = round(repos.etu_dictionary['SD Time'][0],3)*1000
        repos.etu_dictionary['Etu GF Time'][0] = round(repos.etu_dictionary['GF Time'][0],3)*1000
        
    repos.etu_dictionary['Etu Inst PU'][0]  = repos.etu_dictionary['Inst PU'][0]*10                   
    repos.etu_dictionary['Etu GF PU'][0] = repos.etu_dictionary['GF PU'][0]*100            
            

    
def convert_etu_to_standard(repos):

    
    for key in repos.sp_one_keys:
        etu_key = "Etu " + key
        repos.etu_dictionary[key][0] = repos.etu_dictionary[etu_key][0]

    if repos.family == "35":
        repos.etu_dictionary['LD Time'][0] = repos.etu_dictionary['Etu LD Time'][0]/100
    else:
        repos.etu_dictionary['LD Time'][0] = repos.etu_dictionary['Etu LD Time'][0]/10
        
    repos.etu_dictionary['SD PU'][0] = repos.etu_dictionary['Etu SD PU'][0]/10          
    repos.etu_dictionary['SD Time'][0] = repos.etu_dictionary['Etu SD Time'][0]/1000
    
    if repos.family == "ACB":
        repos.etu_dictionary['SD Time'][0] = repos.etu_dictionary['Etu SD Time'][0]/100
        repos.etu_dictionary['GF Time'][0] = repos.etu_dictionary['Etu GF Time'][0]/100
    elif repos.family == "35":
        repos.etu_dictionary['SD Time'][0] = repos.etu_dictionary['Etu SD Time'][0]/100
        repos.etu_dictionary['GF Time'][0] = repos.etu_dictionary['Etu GF Time'][0]/100

    else:
        repos.etu_dictionary['SD Time'][0] = repos.etu_dictionary['Etu SD Time'][0]/1000
        repos.etu_dictionary['GF Time'][0] = repos.etu_dictionary['Etu GF Time'][0]/1000
        
    repos.etu_dictionary['Inst PU'][0]  = repos.etu_dictionary['Etu Inst PU'][0]/10                   
    repos.etu_dictionary['GF PU'][0] = repos.etu_dictionary['Etu GF PU'][0]/100            
    
