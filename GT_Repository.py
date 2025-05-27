'''---------------------------------------------------------------------
    
    Company:    EATON COROPORATION
            
                Proprietary Information
                (C) Copyright 2016
                All rights reserved
                
                PXR Automation - Protection  
    
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
                
    Module:     Repository.py
                
    Mechanics: Holds and Updates Variables 
                    
----------------------------------------------------------------------------'''

from __future__ import division
from struct import *
import time

from GT import GT_MCCB_Translator, GT_ACB_Translator, GT_Conversions
from GT import GT_MCCB_Settings, GT_ACB_Settings, GT_ACB35_Settings

class Repository(object):           #  creates object to manage core setpoints
    
    def __init__(self):	        #  initialize setpoints
        

        self.cmc_in_use = False     #  bypass omicron code
        self.re_cal_needed = False #recalibrates secondary injection
        self.UI_test_type = "Excel"      # used to override excel test type
        self.run_test_type = "Excel"
            
        
        self.num_runs   = 0         # Number of runs that will occur
        self.rating     = 0         
        self.ct         = 60
        self.phases     = 'A'       # Determins which phases will be used
        self.power      = 'All Power' # Determins what type of power the trip unit gets 
        self.neutral    = 0
        self.row_ratio  = 0
        self.ct_ratio   = 0
        self.ph         = True
        self.ph_type    = 0
        self.pxr        = 35
        self.more_config = True
        
        self.mech_time  = 0         # This is the mechanical time it takes to trip. Used for t_adj
        self.failure_mode = 'None'  #Stores why a test has failed
        
        self.life_point_test = 0    #  changes behavior of omircon if life point test
        self.ready_for_test  = False #checks if the test is ready to run 
        self.index      = 0         #  test case index
        self.result     = ''        #  test case trip result 

        self.main_info_keys = []
        self.excel_file_tab_names = []
        self.translator = GT_MCCB_Translator
        self.no_trip_case = False

        self.output_msg = ""
        self.debug_msg = ""
        self.starting_life_points = 0
        self.life_point_change = 0

        self.static_style_1 = 0 #only to be changed when reading from the trip unit
        self.static_style_2 = 0 #only to be changed when reading from the trip unit
        self.static_frame  =  0 
        self.msg_entry_count = 0 # Counter number of Entries Logged (Switch to 0 Later)
    
        self.main_dict     =   {}
        self.main_keys     =   []


        
        
        self.expected      =   { 'Test Type'     :"None",
                                 'I A (Amps)'    :0,
                                 'I B (Amps)'    :0,
                                 'I C (Amps)'    :0,
                                 'I A (PU)'      :0,
                                 'I B (PU)'      :0,     
                                 'I C (PU)'      :0,
                                 'V A'           :0,
                                 'V B'           :0,
                                 'V C'           :0,
                                 'Max Time'      :0,
                                 'Min Time'      :0
                               }

        self.expected_keys  =[   'Test Type',
                                 'I A (Amps)',
                                 'I B (Amps)',     
                                 'I C (Amps)',
                                 'I A (PU)',
                                 'I B (PU)',
                                 'I C (PU)',
                                 'V A',
                                 'V B',
                                 'V C',
                                 'Max Time',
                                 'Min Time']
                
        
        self.results_keys  =    ['Trip Time',
                                 'Trip Time + Mech',
                                 'Result'
                                 ]
        
        self.results       =   { 'Trip Time'    :0,
                                 'Trip Time + Mech'     :0,
                                 'Result'    :"N/A"
                               }

        self.custom_setpoints = [] #Used for a tab with only a few setpoints
        self.custom_keys = [] #Used to determine what information to use on main tab of the report. 
        self.excel_file_tab_keys = []



    '''
    ========================================================================================================================================================================================
    Setup Repository Settings
    ========================================================================================================================================================================================
    '''

    def setup(self, choice):
    
        self.set_family(choice)
        self.set_setting_file(choice)
        self.set_translator(choice)
        self.set_keys()
        
    def set_family(self, choice):

        if choice == "ACB":
            self.family = "ACB"
        elif choice == "35":
            self.family = "35" 
        else:
            self.family = "MCCB"

    def set_translator(self, choice):
        
        if choice == "ACB":
            self.translator = GT_ACB_Translator
        elif choice == "35":
            self.translator = GT_ACB_Translator 
        else:
            self.translator = GT_MCCB_Translator
        
    def set_setting_file(self, choice):

        if choice == "ACB":
            self.setting_file = GT_ACB_Settings
        elif choice == "35":
            self.setting_file = GT_ACB35_Settings
        else:
            self.setting_file = GT_MCCB_Settings
            
    def set_setting_parameters(self):

        self.setting_file.get_values(self)
        self.setting_file.get_setpoint_keys(self)
        self.setting_file.get_dictionary(self)

    def set_pxr20(self):
        self.setting_file.change_pxr20_data_types(self)

    def set_pxr10(self):
        self.setting_file.change_pxr10_data_types(self)
        
    def set_keys(self):

        self.setting_file.get_setpoint_keys(self)
        self.setting_file.get_buffer_keys(self)
        self.setting_file.get_dictionary(self)

    def set_row_ratio(self):
        frame = self.etu_dictionary["Frame"][0]
        rating = self.etu_dictionary["Rating"][0]
        self.row_ratio = self.setting_file.get_rog_ratio(frame, rating)

    def set_ct_ratio(self):
        frame = self.etu_dictionary["Frame"][0]
        rating = self.etu_dictionary["Rating"][0]
        self.ct_ratio, self.ph, self.ph_type = self.setting_file.get_ct_ratio(frame, rating)

    def set_mapping_dictionary(self):
        self.setting_file.get_mapping_dictionary(self)

    def reset_to_no_trip_values(self):
        self.setting_file.reset_to_no_trip_values(self)

    '''
    ========================================================================================================================================================================================
    Update Values
    ========================================================================================================================================================================================
    '''

    def update_buffers(self, array, choice):

        if choice == 0:
            keys = self.buffer_zero_keys
        elif choice == 1:
            keys = self.buffer_one_keys
        elif choice == 2:
            keys = self.buffer_two_keys
        elif choice == 3:
            keys = self.buffer_three_keys
        elif choice == 4:
            keys = self.buffer_four_keys
        elif choice == 5:
            keys = self.buffer_five_keys
        elif choice == 6:
            keys = self.buffer_six_keys
        elif choice == 7:
            keys = self.buffer_seven_keys
        elif choice == 8:
            keys = self.buffer_eight_keys
        elif choice == 9:
            keys = self.buffer_nine_keys
        elif choice == 10:
            keys = self.buffer_ten_keys
        elif choice == 11:
            keys = self.buffer_eleven_keys
        elif choice == 12:
            keys = self.buffer_tweleve_keys
        elif choice == 13:
            keys = self.buffer_thirteen_keys
        elif choice == 42:
            keys = self.buffer_fourty_two_keys
        elif choice == 43:
            keys = self.buffer_fourty_three_keys
        elif choice == 48:
            keys = self.buffer_fourty_eight_keys
        elif choice == 55:
            keys = self.buffer_fifty_five_keys
        j = 0
        for key in keys:
            self.etu_dictionary[key][0] = array[j]
            j = j + 1
            
    
    def update_setpoints(self, array, choice):

        if choice == 0:
            keys = self.sp_zero_keys 
        elif choice == 1:
            keys = self.sp_etu_keys 
        elif choice == 2:
            keys = self.sp_two_keys
        elif choice == 3:
            keys = self.sp_two_keys
        elif choice == 4:
            keys = self.sp_two_keys
        else:
            keys = self.sp_five_keys

        j = 0
        for key in keys:
            self.etu_dictionary[key][0] = array[j]
            print(str(key) + "    "  + str(array[j]))
            j = j + 1

        if choice == 1:
            GT_Conversions.convert_etu_to_standard(self)

    def update_firmware(self, array):

        j = 0 
        for key in self.firmware_keys:
            self.etu_dictionary[key][0] = array[j]
            print(str(key) + "    "  + str(array[j]))
            j = j + 1
            
        
    '''
    ========================================================================================================================================================================================
    Frame Choice
    ========================================================================================================================================================================================
    '''
    def get_frame(self, frame): 
        if frame == "PD2" or frame == "SR2":
            frame_num = 21
        elif frame == "PD3A" or frame == "SR3A":
            frame_num  = 22
        elif frame == "PD3B" or frame == "SR3B":
            frame_num  = 23
        elif frame == "PD4" or frame == "SR4":
            frame_num  = 24
        elif frame == "PD5" or frame == "SR5":
            frame_num  = 25
        elif frame == "PD6" or frame == "PD6":
            frame_num  = 26
        elif frame == "N Frame":
            frame_num  = 0
        elif frame == "R Frame" :
            frame_num  = 1
        elif frame == "Standard":
            frame_num  = 2
        elif frame == "Narrow":
            frame_num  = 3
        elif frame == "Double Standard":
            frame_num  = 4
        elif frame == "Double Narrow":
            frame_num  = 5
        else:
            frame_num = -1
        print(frame)
        print(frame_num)
        return frame_num 

    
    '''
    ========================================================================================================================================================================================
    Log Messages
    ========================================================================================================================================================================================
    '''

    def append_usb_msg(self, tag, tx, return_msg):

        msg = "\n" + tag
        self.debug_msg = self.debug_msg + msg 

        msg = "\n" + tx
        self.debug_msg = self.debug_msg + msg 

        msg = "\n" + return_msg
        self.debug_msg = self.debug_msg + msg 

    def append_debug_msg(self, msg):

        msg = "\n" + str(msg)
        self.debug_msg = self.debug_msg + msg 

    def clear_debug_msg(self):

        self.debug_msg = ""
        
    def append_output_msg(self, msg):


        self.msg_entry_count = self.msg_entry_count + 1
        msg = "\n" + str(msg)
        self.output_msg = self.output_msg + msg 
 
    def clear_output_msg(self):

        self.output_msg = ""

    def mark_usb_error(self):

        self.results['t_adj'] = "READ/Write Error"

        
