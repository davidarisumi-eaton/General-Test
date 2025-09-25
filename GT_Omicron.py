'''---------------------------------------------------------------------
    
    Company:    EATON COROPORATselfN
            
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
                
    Module:     Omicron.py
                
    Mechanics:  program module containing the functions related to the control 
                and configuration of the OMICRON CMC unit. 
                
                IO Class: creates object to store amplifier characteristics
                
                Class Functions: 
                    __init__ - initialize amp arrays
                
                Module Functions:
                    trip_test - detect TA trip 
                    input_buffer - read trip time from data buffer
                    init - create omicron object
                    single_phase_trip_test - run signle phase trip test
                    write_amp - write/update all amplifiers
                
                
    Hardware:   OMICRON CMC 356 and 256+:
                                    
----------------------------------------------------------------------------'''

from __future__ import division
import time, random, math


class Omicron():

    def __init__(self):

        self.row_ratio = 1
        self.ph = False
        self.ph_type = 0
        self.ct_ratio = 1
        
        self.aux = 24
        self.in_use = False
        self.external_amp = 3
        self.tf_ratio = 25

        
    def connect_omicron(self):
        import win32com.client
        
        self.engine_app = win32com.client.Dispatch("OMICRON.CMEngAL")
        self.engine_app.DevScanForNew(1)
        
        devices = self.engine_app.DevGetList(1)
        if len(devices) == 0:
            msg = "\n The omicron is either not connected or in use by another program."
            return msg
        
            
        self.dev_num = devices[0]   
        if len(devices) == 14:                             #If the self.dev_num is a two digit number, this will detect it
            dev_num = int(devices[0])*10 + int(devices[1]) #Puts the two digits together
            dev_num = str(dev_num)                         #Returns the self.dev_num to a string
            
        msg = "\nself.dev_num" + str(self.dev_num)
        
        self.engine_app.DevLock(self.dev_num)

        self.engine_app.Exec(self.dev_num,"out:bin:set(0)")           #  Turn off all binary inputs
        self.engine_app.Exec(self.dev_num,"out:aux:def(24)")          #  Set Aux default voltage to 24Vdc

        self.in_use = True
        return msg

    '''
    Set constant variables
    '''
    def set_device(self, device):
        self.device = device
        
    def set_rowgowski_ratio(self, ratio):
        self.row_ratio = ratio

    def set_ct_ratio(self, ratio):
        self.ct_ratio = ratio

    def set_power_harvesting(self, ph, ph_type): #ph power harvesting true/false, ph_type = 0/none 1/acb, 2/mccb
        self.ph = ph
        self.ph_type = ph_type

    def set_tf_ratio(tf_ratio):
        self.tf_ratio = tf_ratio


    '''
    Setup Methods
    '''
    def route_a_and_b(self):
        print("ROUTING A AND B")
        self.engine_app.Exec(self.dev_num, "amp:route(i(1), clr)")
        self.engine_app.Exec(self.dev_num, "amp:def(2, clr)")
        self.engine_app.Exec(self.dev_num, "amp:route(i(1), 17)")

    def route_llo(self, ext):

        self.external_amp = ext
        def_string = self.engine_app.Exec(self.dev_num, "amp:def?")

        setupString     = "amp:def(" + str(ext) + ",ext,v,1.000000E+000,7.070000E+000,0.000000E+000,1.000000E+003,0,0,0)"
        route_string    = "amp:route(v(3)," + str(ext) + ")"
        
        self.engine_app.Exec(self.dev_num, setupString)
        self.engine_app.Exec(self.dev_num, route_string)       #  Route llo amps to v(3)

                

    '''
    =========================================================================================================================================================================================
    Omicron Commands
    =========================================================================================================================================================================================
    '''
   
    def aux_on(self):
        self.engine_app.Exec(self.dev_num,"out:aux:on")               #  Turn off AUX Voltage 

    def aux_off(self):
        self.engine_app.Exec(self.dev_num,"out:aux:off")
        
    def omicron_on(self):
        self.engine_app.Exec(self.dev_num, "out:ana:on")
        
    def omicron_off(self):
        self.engine_app.Exec(self.dev_num, "out:ana:off")

    def omicron_zero_cross_off(self):
        #self.engine_app.Exec(self.dev_num,"out:ana:off(zcross, i(1:1)&i(1:2)&i(1:3)&v(1:1)&v(1:2)&v(1:3)&v(3:1)&v(3:2)&v(3:3)")
        self.engine_app.Exec(self.dev_num,"out:ana:off(zcross, v(3:1))")
        
    def unlock_omicron(self):
        self.engine_app.Exec(self.dev_num,"out:ana:off")
        self.engine_app.DevUnlock(self.dev_num)



    def write_omicron_voltage(self, amplitude, phase_angle, frequency, phase):  
        om_message = "out:ana:v(1:"+str(phase)+"):a("+str(amplitude)+");f("+str(frequency)+");p("+str(phase_angle)+")"
        self.engine_app.Exec(self.dev_num, om_message)
        
    def write_omicron_rowgowski(self, amplitude, phase_angle, frequency, phase):  
        om_message = "out:ana:v(3:" +str(phase)+"):a("+str(amplitude)+");f("+str(frequency)+");p("+str(phase_angle)+")"
        self.engine_app.Exec(self.dev_num, om_message)  

    def write_omicron_current(self, amplitude, phase_angle, frequency, phase):     
        om_message = "out:ana:i(1:"+str(phase)+"):a("+str(amplitude)+");f("+str(frequency)+");p("+str(phase_angle)+")"
        self.engine_app.Exec(self.dev_num, om_message)
        
    def write_omicron_output(self, amplitude, phase_angle, frequency, phase, amplifier, out_type):
        channel = "(" + str(amplifier) + ":" + str(phase) + ")"
        amplifier = str(amplifier)
        current = ":a(" + str(current) + ")"
        frequency = ";f(" + str(frequency) + ")"
        phase = ";p(" + str(phase) + ")"
        
        message = "out:ana:" + out_type + channel + amplitude + frequency + phase_angle
        self.engine_app.Exec(self.dev_num, message)

    def write_bin_out_off(self, num):
        om_message = "out:bin(1):off(" + str(num) + ")"
        self.engine_app.Exec(self.dev_num, om_message)
        
    def write_bin_out_on(self, num):
        om_message = "out:bin(1):on(" + str(num) + ")"
        self.engine_app.Exec(self.dev_num, om_message)

    '''
    =========================================================================================================================================================================================
    Omicron Trip Methods
    =========================================================================================================================================================================================
    '''
    def setup_for_trip(self):
        self.engine_app.Exec(self.dev_num,"inp:buf:clr")            #  clear input buffer
        self.engine_app.Exec(self.dev_num,"inp:buf:sam(bin, on)")   #  turn on input buffe
        
    def check_for_trip(self):
        B = self.engine_app.Exec(self.dev_num,"inp:bin:get?")       #  read binary - break if trip

        if len(B) == 4:                                 #  If the self.dev_number is one digit the binary input will be at index 2 of the message 
            b0 = int(B[2]) & 1                          #  read bin input 1 only
        else:                                           #  If the self.dev_number is two digits the binary input will be at index 3 of the message 
            b0 = int(B[3]) & 1                          #  read bin input 1 only

        if b0 == 1:
            self.end_trip()
            return True
        else:
            return False

    def end_trip(self):
        

        #self.engine_app.Exec(self.dev_num,"out:ana:off(zcross, i(1:2)&v(2:1))")#  turn off analog inputs
        #self.engine_app.Exec(self.dev_num,"out:ana:off(zcross, v(3:2))")
        #self.engine_app.Exec(self.dev_num,"out:ana:off(zcross, v(3:2))")
        #self.engine_app.Exec(self.dev_num,"out:ana:off(zcross, v(3:3))")
        #self.omicron_zero_cross_off()
        self.engine_app.Exec(self.dev_num,"out:ana:off(zcross)")
        self.engine_app.Exec(self.dev_num,"out:ana:clr")
        
        #self.engine_app.Exec(self.dev_num,"out:ana:off")
        #self.engine_app.Exec(self.dev_num,"out:bin:set(0)")             #  turn off bin(0)

    def input_buffer(self):    #  read trip time from input buffer 
                
        BufType = str()          
        BufData = str()                    
        BufIndex = int()        
        BufTime = float()       
        BinaryState = int()     
        
        EndOfBuffer = False
        Trigger = False
        
        ReferenceTime = '0'
        TripTime = '0'
                        
        while (Trigger == False and EndOfBuffer == False): 
        
            result = self.engine_app.Exec(self.dev_num,"inp:buf:get?")        
            Buffer = result.split(',')
        
            BufType  = Buffer[1]
            BufTime  = Buffer[2]
            BufData  = Buffer[3]
            BufIndex = int(Buffer[4]) & 1
                    
            if BufType == 'empty':
                EndOfBuffer = True
                
            elif (BufType == 'bin' and BufIndex == 0):
                ReferenceTime = BufTime
                
            elif (BufType == 'bin' and BufIndex == 1):
                BinaryState = int(BufData) & 1              #lsb = (x & 1)/1
                
                if BinaryState == 1:
                    EndTime = BufTime.encode('ASCII')
                    RefTime = ReferenceTime.encode('ASCII')
                    #print("ENDTIME   ", EndTime)
                    #print("REFTIME   ", RefTime)
                    EventTime = float(EndTime) - float(RefTime)
                    Trigger = True
                                            
        if Trigger == True: 
            TripTime = EventTime        
        else: 
            TripTime = -1       # did not trip
                            
        return TripTime          

    
        

        
    '''
    =========================================================================================================================================================================================
    Configuration Functions
    =========================================================================================================================================================================================
    '''


    def config_rowgowski(self, I, freq):
        freq_comp = freq/60 #Amplitude changes based on frequency
        
        row_output = (I * self.row_ratio * freq/60)  

        if row_output > 7:
            row_output = 7

        return row_output
        
    def config_current(self, I):

        if self.ph == True: #If the current source is being used a power harvester
            if I == 0:
                I = 1
            if self.ph_type == 1:
                output_current = (.0281*math.log(I)-.06)*10 #ACB
            else:
                output_current = (.0281*math.log(I)-.06)*25
                
        else:
            output_current = (I / self.ct_ratio) * self.tf_ratio   #If the current source is being used as a measurment source (PD2 only as of now)
            output_current = round(output_current, 4)    


        if output_current > .3 and self.ph == True: #Saftey method to make sure current doesn't get to high for power harvester
            output_current = .3
        elif output_current > 24 and self.ph == False:
            output_current = 24
        if output_current < 0:
            output_current = 0

        return output_current

    '''
    =========================================================================================================================================================================================
    Omicron Setup Methods
    =========================================================================================================================================================================================
    '''

    def setup_omicron(self, repos):

        a = repos.expected['I A (Amps)']
        b = repos.expected['I B (Amps)']
        c = repos.expected['I C (Amps)']
        va = repos.expected['V A']
        vb = repos.expected['V B']
        vc = repos.expected['V C']

        freq  = repos.etu_dictionary["Source_Freq"][0]
        ia_ang = repos.etu_dictionary["Ia_Phase_Angle"][0]
        ib_ang = repos.etu_dictionary["Ib_Phase_Angle"][0]
        ic_ang = repos.etu_dictionary["Ic_Phase_Angle"][0]
        ia_ang = repos.etu_dictionary["Ia_Phase_Angle"][0]
        ib_ang = repos.etu_dictionary["Ib_Phase_Angle"][0]
        ic_ang = repos.etu_dictionary["Ic_Phase_Angle"][0]
        ra_ang = repos.etu_dictionary["Ra_Phase_Angle"][0]
        rb_ang = repos.etu_dictionary["Rb_Phase_Angle"][0]
        rc_ang = repos.etu_dictionary["Rc_Phase_Angle"][0]
        va_ang = repos.etu_dictionary["Va_Phase_Angle"][0]
        vb_ang = repos.etu_dictionary["Vb_Phase_Angle"][0]
        vc_ang = repos.etu_dictionary["Vc_Phase_Angle"][0]
        

        ia = self.config_current(a)
        ib = self.config_current(b)
        ic = self.config_current(c)

        ra = self.config_rowgowski(a, freq)
        rb = self.config_rowgowski(b, freq)
        rc = self.config_rowgowski(c, freq)

        self.write_omicron_current(ia, ia_ang, freq, 1)
        self.write_omicron_current(ib, ib_ang, freq, 2)
        self.write_omicron_current(ib, ib_ang, freq, 3)

        self.write_omicron_rowgowski(ra, ra_ang, freq, 1)
        self.write_omicron_rowgowski(rb, rb_ang, freq, 2)
        self.write_omicron_rowgowski(rc, rc_ang, freq, 3)

        self.write_omicron_voltage(va, va_ang, freq, 1)
        self.write_omicron_voltage(vb, vb_ang, freq, 2)
        self.write_omicron_voltage(vc, vc_ang, freq, 3)
  
        msg = "ia " + str(ia) + " " + str(ia_ang) + " " + str(freq)
        repos.append_output_msg(msg)
        msg = "ib " + str(ib) + " " + str(ib_ang) + " " + str(freq)
        repos.append_output_msg(msg)
        msg = "ic " + str(ic) + " " + str(ic_ang) + " " + str(freq)
        repos.append_output_msg(msg)
        msg = "ra " + str(ra) + " " + str(ra_ang) + " " + str(freq)
        repos.append_output_msg(msg)
        msg = "rb " + str(rb) + " " + str(rb_ang) + " " + str(freq)
        repos.append_output_msg(msg)
        msg = "rc " + str(rc) + " " + str(rc_ang) + " " + str(freq)
        repos.append_output_msg(msg)
        msg = "va " + str(va) + " " + str(va_ang) + " " + str(freq)
        repos.append_output_msg(msg)
        msg = "vb " + str(vb) + " " + str(vb_ang) + " " + str(freq)
        repos.append_output_msg(msg)
        msg = "vc " + str(vc) + " " + str(vc_ang) + " " + str(freq)
        repos.append_output_msg(msg)


