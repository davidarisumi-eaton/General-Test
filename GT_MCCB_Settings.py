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

    Last Edited: 10/9/2019



-------------------------------------------------------------------------------
    
    Product:    Automated test system to test the PXR10, PXR20, PXR2D, PXR25, 
                and PXR35 protection algorithms for the SR
                breaker frames.   
                
    Module:     Settings.py
                
    Mechanics:   Most of functions are different profiles of the configurations of PXR units. Scrolling
                 down you'll notice that the profiles are divided into different sections. As of now the
                 contents look as so


----------------------------------------------------------------------------'''


'''
    ====================================================================================================================
====Keys =======================================================================================================
    =================
'''

def add_dictionary_values(repos, keys):

    for val in keys:
        repos.etu_dictionary.update({val:[0, "Uint16"]})

def add_setpoint_group_zero(repos):

    repos.sp_zero_keys =    ['Rating',
                                'Frame',
                                'Style1',
                                'Style2',
                                'MM Mode',
                                'MM Level',
                                'Line Frequency',
                                'Reverse Feed',
                                'Sign',
                                'Power Window',
                                'Power Interval',
                                'Language',
                                'LCD Rotatation',
                                'Relay 1',
                                'Relay 2',
                                'Relay 3',
                                'Pole Location',
                                'I Window',
                                'I Interval',
                                'Health Level'
                            ]


    add_dictionary_values(repos, repos.sp_zero_keys)
        
def add_setpoint_group_one(repos):

            
    repos.sp_one_keys =     ['Rating',
                            'Frame',
                            'Style1',
                            'Style2',
                            'LD Thermal',
                            'ZSI',
                            'LD Slope',
                            'LD PU',
                            'LD Time',
                            'HL Alarm 1', 
                            'SD Slope',
                            'SD PU',
                            'SD Time',
                            'Inst PU',
                            'GF Type',
                            'GF Mode',
                            'GF Slope',
                            'GF PU', 
                            'GF Time',
                            'GF Thermal',
                            'Neutral Ratio',
                            'HL Alarm 2',
                            'GF Alarm',
                             'Reserved16'
                            ]
    
    repos.sp_etu_keys =     ['Etu Rating',
                                'Etu Frame',
                                'Etu Style1',
                                'Etu Style2',
                                'Etu LD Thermal',
                                'Etu ZSI',
                                'Etu LD Slope',
                                'Etu LD PU',
                                'Etu LD Time',
                                'Etu HL Alarm 1', 
                                'Etu SD Slope',
                                'Etu SD PU',
                                'Etu SD Time',
                                'Etu Inst PU',
                                'Etu GF Type',
                                'Etu GF Mode',
                                'Etu GF Slope',
                                'Etu GF PU', 
                                'Etu GF Time',
                                'Etu GF Thermal',
                                'Etu Neutral Ratio',
                                'Etu HL Alarm 2',
                                'Etu GF Alarm',
                                'Etu Reserved16'
                             
                            ]


    add_dictionary_values(repos, repos.sp_one_keys)
    add_dictionary_values(repos, repos.sp_etu_keys)


def add_setpoint_group_two(repos):

    repos.sp_two_keys   =   ['MBus Address',
                             'MBus Baud',
                             'MBus Parity',
                             'MBus Stop Bit']
    
    add_dictionary_values(repos, repos.sp_two_keys)


def add_setpoint_group_three(repos):
    
    repos.sp_three_keys   =   [ 'MCam Address',
                            'MCam Baud',
                            'MCam Parity',
                            'MCam Stop Bit', 
                            'Incom Address',
                            'Incom Baud',
                            'ECam DHCP',
                            'ECam IP 0',
                            'ECam IP 1',
                            'ECam IP 2',
                            'ECam IP 3',
                            'ECam IP 4',
                            'ECam Subnet',
                            'ECam Default 1',
                            'EeCam Default 1',
                            'eCam Reset',
                            'pCam Address']

    add_dictionary_values(repos, repos.sp_three_keys)


def add_setpoint_group_five(repos):

    repos.sp_five_keys =   ['Over V Action',
                            'Over V PU',
                            'Over V Time',
                            'Under V Action',
                            'Under V PU', 
                            'Under V Time',
                            'V Unbalance PU',
                            'V Unbalance Action',
                            'V Unbalance Time',
                            'I Unbalance Action',
                            'I Unbalance PU',
                            'I Unbalance Time',
                            'Rev Power Action',
                            'Rev Power PU',
                            'Rev Power Time',
                            'Power Rev Sense',
                            'Power Rev Action',
                            'Phase Loss Action',
                            'Phase Loss Time']
    
    
    add_dictionary_values(repos, repos.sp_five_keys)

def add_configuration(repos):

    
    repos.breaker_protection_capacity_keys = ['frame_ap',
                                        'Poles',
                                        'Standard', 
                                        'Ct Version', 
                                        'Override',
                                        'MCR',              
                                        'Max Interrupt Label', 
                                        'Frame Construction']
    repos.etu_dictionary["Frame Ap"]                =  [0,"Uint16"]
    repos.etu_dictionary["Poles"]                   =  [0,"Uint16"]
    repos.etu_dictionary["Standard"]                =  [0,"Uint16"]
    repos.etu_dictionary["Ct Version"]              =  [0,"Uint16"]
    repos.etu_dictionary["Override"]                =  [1100 ,"Uint32"]
    repos.etu_dictionary["MCR"]                     =  [0,"Uint32"]             
    repos.etu_dictionary['Max Interrupt Label']     =  [0,"Uint32"]
    repos.etu_dictionary["Frame Construction"]      =  [0,"Uint32"]
                            
    add_dictionary_values(repos, repos.breaker_protection_capacity_keys)

def add_buffer_zero(repos):
    
    repos.buffer_zero_keys = ['Primary Status',
                            'Second Status',
                            'Cause Of Status',
                            'Breaker Status',
                            'Trip Condition',
                            'Alarm Condition',
                            'MM Status',
                            'Test Mode Status',
                            'Testing Forbid',
                            'LD Pickup Status',
                            'ZIN Status',
                            'Aux Power Connected',
                            'Source Ground Active']
    
    repos.etu_dictionary['Primary Status']       = ["Unkown", "Byte"]
    repos.etu_dictionary['Second Status']        = ["Unkown", "Byte"]
    repos.etu_dictionary['Cause Of Status']      = ["Unkown", "Byte"]
    repos.etu_dictionary['Breaker Status']       = ["Unkown", "2Byte"]
    repos.etu_dictionary['Trip Condition']       = ["Unkown", "Bin"]
    repos.etu_dictionary['Alarm Condition']      = ["Unkown", "Bin"]
    repos.etu_dictionary['MM Status']            = ["Unkown", "Bin"]
    repos.etu_dictionary['Test Mode Status']     = ["Unkown", "Bin"]
    repos.etu_dictionary['Testing Forbid']       = ["Unkown", "Bin"]
    repos.etu_dictionary['LD Pickup Status']     = ["Unkown", "Bin"]
    repos.etu_dictionary['ZIN Status']           = ["Unkown", "Bin"]
    repos.etu_dictionary['Aux Power Connected']  = ["Uknown", "Bin"]
    repos.etu_dictionary['Source Ground Active'] = ["Uknown", "Bin"]


def add_buffer_one(repos):

    repos.buffer_one_keys         = ['External Ia',
                                    'External Ib',
                                    'External Ic',
                                    'External In',
                                    'External Ig',
                                    'External Va',
                                    'External Vb',
                                    'External Vc',
                                    'External Vab',
                                    'External Vbc',
                                    'External Vca',
                                    'Freq',
                                    'Real Power',
                                    'React Power',
                                    'App Power',
                                    'PF',
                                    'Temp',
                                    'Batt Val']
    
    repos.etu_dictionary['External Ia']       = [0, "Float"]
    repos.etu_dictionary['External Ib']       = [0, "Float"]
    repos.etu_dictionary['External Ic']       = [0, "Float"]
    repos.etu_dictionary['External In']       = [0, "Float"]
    repos.etu_dictionary['External Ig']       = [0, "Float"]
    repos.etu_dictionary['External Va']       = [0, "Float"]
    repos.etu_dictionary['External Vb']       = [0, "Float"]
    repos.etu_dictionary['External Vc']       = [0, "Float"]
    repos.etu_dictionary['External Vab']      = [0, "Float"]
    repos.etu_dictionary['External Vbc']      = [0, "Float"]
    repos.etu_dictionary['External Vca']      = [0,"Float"]
    repos.etu_dictionary['Freq']              = [0, "Q4Padded"]
    repos.etu_dictionary['Real Power']        = [0, "Float"]
    repos.etu_dictionary['React Power']       = [0,"Float"]
    repos.etu_dictionary['App Power']         = [0, "Float"]
    repos.etu_dictionary['PF']                = [0, "Q10Padded"]
    repos.etu_dictionary['Temp']              = [0, "Q4Padded"]
    repos.etu_dictionary['Batt Val']          = [0, "Q8Padded"]


    if repos.pxr == "PXR20" or repos.pxr == "PXR10":
        repos.etu_dictionary['External Ia'][1]    = "Q4"
        repos.etu_dictionary['External Ib'][1]   = "Q4"
        repos.etu_dictionary['External Ic'][1]   = "Q4"
        repos.etu_dictionary['External In'][1]   = "Q4"
        repos.etu_dictionary['External Ig'][1]   = "Q4"
        repos.etu_dictionary['Freq']             = "Uint32"


def add_buffer_ten(repos): 

    repos.buffer_ten_keys = ['Internal Ia',
                            'Internal Ib',
                            'Internal Ic',
                            'Internal In',
                            'Internal Ig']
    
    repos.etu_dictionary['Internal Ia']          = [0, "Q4"]
    repos.etu_dictionary['Internal Ib']          = [0, "Q4"]
    repos.etu_dictionary['Internal Ic']          = [0, "Q4"]
    repos.etu_dictionary['Internal In']          = [0, "Q4"]
    repos.etu_dictionary['Internal Ig']          = [0, "Q4"]

def get_dictionary(repos):

    #Setpoint {Name: [Value, Data_Type]}

   

    repos.etu_dictionary =  {'MCU1 Version'             : [0, "Uint16"],
                            'MCU1 Revision'            : [0, "Uint16"],
                            'MCU1 Debugger'            : [0, "Uint16"],
                            'MCU2 Version'             : [0, "Uint08"],
                            'MCU2 Revision'            : [0, "Uint08"],
                            'MCU2 Debugger'            : [0, "Uint16"],
                            'MCU Com Ver'              : [0, "Uint08"],
                            'MCU Com Rev'              : [0, "Uint08"],
                            'MCU Com Debug'            : [0, "Uint16"],
                            'USB PC Tool Ver'          : [0, "Uint16"],
                            'USB PC Tool Rev'          : [0, "Uint16"],
                            'MCU2 Flash Firmware Version'  : [0, "Uint08"],
                            'MCU2 Flash Firmware Revision' : [0, "Uint08"],
                            'MCU2 Flash Firmware Debugger' : [0, "Uint08"],
                            'primary_status'  : ["Unkown", "Byte"],
                            'second_status'   : ["Unkown", "Byte"],
                            'cause_of_status' : ["Unkown", "Byte"],
                            'breaker_status'  : ["Unkown", "2Byte"],
                            'trip_condition'  : ["Unkown", "Bin"],
                            'alarm_condition' : ["Unkown", "Bin"],
                            'MM_status'       : ["Unkown", "Bin"],
                            'test_mode_status': ["Unkown", "Bin"],
                            'testing_forbid'  : ["Unkown", "Bin"],
                            'ld_pickup_status': ["Unkown", "Bin"],
                            'ZIN_status'      : ["Unkown", "Bin"],
                            'GF_condition'    : ["Unkown", "Bin"] ,
                             'external_Ia'     : [0, "Q4"],
                            'external_Ib'     : [0, "Q4"],
                            'external_Ic'     : [0, "Q4"],
                            'external_In'     : [0, "Q4"],
                            'external_Ig'     : [0, "Q4"],
                            'external_Va'     : [0, "Q4Padded"],
                            'external_Vb'     : [0, "Q4Padded"],
                            'external_Vc'     : [0, "Q4Padded"],
                            'external_Vab'    : [0, "Q4Padded"],
                            'external_Vbc'    : [0, "Q4Padded"],
                            'external_Vca'    : [0, "Q4Padded"],
                            'freq'            : [0, "Q4Padded"],
                            'real_power'      : [0, "int32"],
                            'react_power'     : [0, "int32"],
                            'app_power'       : [0, "Uint32"],
                            'pf'              : [0, "Q10Padded"],
                            'temp'            : [0, "Q4Padded"],
                            'batt_val'        : [0, "Q8Padded"],
                            'forward energy'  : [0, "Uint64"],
                            'reverse energy'  : [0, "Uint64"],
                            'total energy'    : [0, "Uint64"],
                            'net energy'      : [0, "int64"],
                            'leading reactive energy' : [0, "Uint64"],
                            'lagging reactive energy' : [0, "Uint64"],
                            'total reactive energy'   : [0, "Uint64"],
                            'net reactive energy'     : [0, "int64"],
                            'apparent energy'         : [0, "Uint64"],
                            'last energy reset time'  : [0, "Date"],
                            'power demand interval'   : [0, "Uint16"],
                            'real power demand'       : [0, "int32"],
                            'reactive power demand'   : [0, "int32"],
                            'apparent power demand'   : [0, "Uint32"],
                            'Max Real Power Demand'   : [0, "Uint32"],
                            'Time Of Max Pn Demand Occurrence': [0, "Date"],
                            'Max Reactive Power Demand': [0, "Uint32"],
                            'Time Of Max Pr Demand Occurrence': [0, "Date"],
                            'Max Apparent Power Demand': [0, "Uint32"],
                            'Time Of Max Pa Demand Occurrence': [0, "Date"],
                            'Last Time Of Resetting Power Demand': [0, "Date"],
                            'ex_Ia_max': [0, "Q4"],
                            'ex_Ia_max_time': [0, "Date"],
                            'ex_Ib_max': [0, "Q4"],
                            'ex_Ib_max_time': [0, "Date"],
                            'ex_Ic_max': [0, "Q4"],
                            'ex_Ic_max_time': [0, "Date"],
                            'ex_In_max': [0, "Q4"],
                            'ex_In_max_time': [0, "Date"],
                            'ex_Ig_max': [0, "Q4"],
                            'ex_Ig_max_time': [0, "Date"],
                            'ex_Ia_min': [0, "Q4"],
                            'ex_Ia_min_time': [0, "Date"],
                            'ex_Ib_min': [0, "Q4"],
                            'ex_Ib_min_time': [0, "Date"],
                            'ex_Ic_min': [0, "Q4"],
                            'ex_Ic_min_time': [0, "Date"],
                            'ex_In_min': [0, "Q4"],
                            'ex_In_min_time': [0, "Date"],
                            'ex_Ig_min': [0, "Q4"],
                            'ex_Ig_min_time': [0, "Date"],
                            'Last_Reset': [0, "Date"],
                            'total_short_circuit_counter': [0, "Uint16"],
                            'short_delay_trip_counter': [0, "Uint16"],
                            'instantaneous_trip_counter': [0, "Uint16"],
                            'high_current_trip_counter': [0, "Uint16"],
                            'total_overload_trip_counter': [0, "Uint16"],
                            'trip_operations_counter': [0, "Uint16"],
                            'test_operations_counter': [0, "Uint16"],
                            'long_delay_trip_counter': [0, "Uint16"],
                            'ground_fault_trip_counter': [0, "Uint16"],
                            'total_operations_counter': [0, "Uint16"],
                            'trip_operations_counter': [0, "Uint16"],
                            'test_operations_counter': [0, "Uint16"],
                            'opens_operations_counter' : [0, "Uint16"],
                            'manual_operations_counter' : [0, "Uint16"],
                            'manual_operations_counter': [0, "Uint16"],
                            'time_of_last_operations': [0, "Date"],
                            'max_temp'                : [0, "Uint16"],
                            'time_of_max_temp'        : [0, "Uint16"],
                            'running_minute'          : [0, "Uint16"],
                            'running_hour'            : [0, "Uint16"],
                            'running_day'             : [0, "Uint16"],
                            'life_points'             : [0, "Uint16"],
                            'max_Vab'                 : [0, "Q4Padded"],
                            'time_max_Vab'            : [0, "Date"],
                            'max_Vbc'                 : [0, "Q4Padded"],
                            'time_max_Vbc'            : [0, "Date"],
                            'max_Vca'                 : [0, "Q4Padded"],
                            'time_max_Vca'            : [0, "Date"],
                            'min_Vab'                 : [0, "Q4Padded"],
                            'time_min_Vab'            : [0, "Date"],
                            'min_Vbc'                 : [0, "Q4Padded"],
                            'time_min_Vbc'            : [0, "Date"],
                            'min_Vca'                 : [0, "Q4Padded"],
                            'time_min_Vca'            : [0, "Date"],
                            'time_reset'              : [0, "Date"],
                            'max_Van'                 : [0, "Q4Padded"],
                            'time_max_Van'            : [0, "Date"],
                            'max_Vbn'                 : [0, "Q4Padded"],
                            'time_max_Vbn'            : [0, "Date"],
                            'max_Vcn'                 : [0, "Q4Padded"],
                            'time_max_Vcn'            : [0, "Date"],
                            'min_Van'                 : [0, "Q4Padded"],
                            'time_min_Van'            : [0, "Date"],
                            'min_Vbn'                 : [0, "Q4Padded"],
                            'time_min_Vbn'            : [0, "Date"],
                            'min_Vcn'                 : [0, "Q4Padded"],
                            'time_min_Vcn'            : [0, "Date"],
                            'time_reset'              : [0, "Date"],
                            'internal_Ia'             : [0, "Q4"],
                            'internal_Ib'             : [0, "Q4"],
                            'internal_Ic'             : [0, "Q4"],
                            'internal_In'             :  [0, "Q4"],
                            'internal_Ig'             :  [0, "Q4"],
                            'int_short_circuit_count' :  [0, "Uint16"],
                            'int_short_delay_count'   :  [0, "Uint16"],
                            'int_instant_count'       :  [0, "Uint16"],
                            'int_high_current_count'  :  [0, "Uint16"],
                            'int_total_overload_count':  [0, "Uint16"],
                            'int_long_delay_count'    :  [0, "Uint16"],
                            'int_ground_fault_count'  :  [0, "Uint16"],
                            'int_total_op_count'      :  [0, "Uint16"],
                            'int_trip_op_count'       :  [0, "Uint16"],
                            'int_test_op_count'       :  [0, "Uint16"],
                            'int_opens_op_count'      :  [0, "Uint16"],
                            'int_manual_op_count'     :  [0, "Uint16"],
                            'int_time_of_last_op'     :  [0, "Uint16"],
                            'int_max_temp'            :  [0, "Uint16"],
                            'int_time_max_temp'       :  [0, "Uint16"],
                            'int_run_miniute'         :  [0, "Uint16"],
                            'int_run_hour'            :  [0, "Uint16"],
                            'int_run_day'             :  [0, "Uint16"],
                            'int_life_points'         :  [0, "Uint32"],
                            'date_raw_op'             :  [0, "Date"],
                            'date_raw_temp'           :  [0, "Date"],
                            "I Op Counter"            :  [0, "Uint16"],
                            "I Contact Wear Reset"    :  [0, "Uint16"],
                            "I Mech Wear Reset"       :  [0, "Uint16"],
                            "I TimeTemp Wear Reset"   :  [0, "Uint16"], 
                            "I Contact Wear"          :  [0, "Uint16"],
                            "I Mech Wear"             :  [0, "Uint16"],
                            "I TimeTemp Wear"         :  [0, "Uint16"],
                            "I Num LP Resets"         :  [0, "Uint16"],
                            "E Op Counter"            :  [0, "Uint16"],
                            "E Contact Wear Reset"    :  [0, "Uint16"],
                            "E Mech Wear Reset"       :  [0, "Uint16"],
                            "E TimeTemp Wear Reset"   :  [0, "Uint16"],
                            "E Contact Wear"          :  [0, "Uint16"],
                            "E Mech Wear"             :  [0, "Uint16"],
                            "E TimeTemp Wear"         :  [0, "Uint16"],
                            "E Num LP Resets"         :  [0, "Uint16"],                      
                            'Setpoints Group Sensor'  :  [0,"Uint16"],
                            'Active Setpoints Group'  :  [0,"Uint16"],
                            'ScondPT/VDB Module Present'      :  [0,"Uint16"],
                            'Phase Labeling'                  :  [0,"Uint16"],
                            'Trip Waveform Capture Precycles' :  [0,"Uint16"],
                            'Extended Capture Triggers'       :  [0,"Uint16"],
                            'IEC61860 Configuration'          :  [0,"Uint16"],
                            'Demand Logging Interval'         :  [0,"Uint16"],
                            'Reserved16'                      :  [0,"Uint16"],
                            'Reserved16_5-1'                 :  [0,"Uint16"],
                            'Reserved16_5-2'                 :  [0,"Uint16"],
                            'Reserved16_5-3'                 :  [0,"Uint16"],
                            'Reserved16_5-4'                 :  [0,"Uint16"],
                            'Reserved16_5-5'                 :  [0,"Uint16"],
                            'Reserved16_5-6'                 :  [0,"Uint16"],
                            'Reserved16_5-7'                 :  [0,"Uint16"], 
                            'High Load Time'                  :  [0,"Uint16"],
                            'GF ZSI'                          :  [0,"Uint16"],
                            'Netural Alarm Pickup'            :  [0,"Uint16"],
                            'Netural Aalarm Time'             :  [0,"Uint16"],
                            'Over V Alarm Action'                  :  [0,"Uint16"],
                            'Over V Alarm PU'                    :  [0,"Uint16"],
                            'Over V Alarm Time'                  :  [0,"Uint16"],
                            'Extended Protection Enable/Disable' :  [0,"Uint16"],
                            'Reverse Reactive Power Action'      :  [2,"Uint16"],
                            'Reverse Reactive Power Pickup'      :  [0,"Uint16"],
                            'Reverse Reactive Power Time'        :  [0,"Uint16"],
                            'Phase Rotation Time'                :  [0,"Uint16"],
                            'Over Voltage Number Of Phases'      :  [0,"Uint16"],
                            'Under Voltage Number Of Phases'     :  [0,"Uint16"],
                            'Power Protection Enable/Diable' :  [0,"Uint16"],
                            'Forward Real Power Action':  [2,"Uint16"],
                            'Forward Real Power Pickup':  [0,"Uint16"],
                            'Forwared Real Power Time':  [0,"Uint16"],
                            'Forward Reactive Power Action':  [2,"Uint16"],
                            'Forward Reactvie Power Pickup':  [0,"Uint16"],
                            'Forward Reactive Power Time':  [0,"Uint16"],
                            'Apparent Power Action':  [0,"Uint16"],
                            'Apparent Power Pickup':  [2,"Uint16"],
                            'Apparent Power Time':  [0,"Uint16"],
                            'Over Power Factor Action':  [0,"Uint16"],
                            'Over Power Factor Pickup':  [2,"Uint16"],
                            'Over Power Factor Time':  [0,"Uint16"],
                            'Under Power Factor Action':  [2,"Uint16"],
                            'Under Power Factor Pickup':  [0,"Uint16"],
                            'Under Power Factor Time':  [0,"Uint16"],
                            'Real Demand Power Action':  [2,"Uint16"],
                            'Real Demand Power Pickup':  [0,"Uint16"],
                            'Real Demand Power Time':  [0,"Uint16"],
                            'Reactive Demand Power Action':  [2,"Uint16"],
                            'Reactive Demand Power Pickup':  [0,"Uint16"],
                            'Reactive Demand Power Time':  [0,"Uint16"],
                            'Apparent Demand Power Action':  [2,"Uint16"],
                            'Apparent Demand Power Pickup':  [0,"Uint16"],
                            'Apparent Demand Power Time':  [0,"Uint16"],
                            'Sync Check Action' :[0,"Uint16"],
                            'Sync Check Min Linve Voltage 1' :[0,"Uint16"],
                            'Sync Check Max Dead Voltage 1':[0,"Uint16"],
                            'Sync Check Min Live Voltage 2':[0,"Uint16"],
                            'Sync Check Max Live Voltage 2':[0,"Uint16"],
                            'Sync Check Max Voltage Difference':[0,"Uint16"],
                            'Sync Check Max Slip Frequency' :[0,"Uint16"],
                            'Sync Check Max Angle Difference' :[0,"Uint16"],
                            'Sync Check Dead V1 - Dead V2 Enable':[0,"Uint16"],
                            'Sync Check Dead V1 - Live V2 Enable':[0,"Uint16"],
                            'Sync Check Live V1 - Dead V2 Enable':[0,"Uint16"],
                            'Sync Check Live V1 - Dead V2 Enable':[0,"Uint16"],
                            'Sync Cheeck Dead Time':[0,"Uint16"],
                            'ATS Function Enable/Disable':[0,"Uint16"],
                            'Number of Gnerators':[0,"Uint16"],
                            'Preferred Source':[0,"Uint16"],
                            'DTS Auto Adjust':[0,"Uint16"],
                            'Phase Reversal':[0,"Uint16"],
                            'Manutal Retranser/Commit To Transfer':[0,"Uint16"],
                            'Closed Transition':[0,"Uint16"],
                            'Closed Voltage Difference':[0,"Uint16"],
                            'Closed Frequency Difference':[0,"Uint16"],
                            'In-Phase Transition':[0,"Uint16"],
                            'In-Phase Freqnecy Difference':[0,"Uint16"],
                            'Sync Timer':[0,"Uint16"],
                            'Load Voltage Decay':[0,"Uint16"],
                            'Neutral Open Transistion':[0,"Uint16"],
                            'Time Delay Normal to Emergency':[0,"Uint16"],
                            'Time Delay Pretransfer':[0,"Uint16"],
                            'Time Delay Posttransfer':[0,"Uint16"],
                            'Time Delay Engine Start(Source2)':[0,"Uint16"],
                            'Time Delay Engine Start(Source1)':[0,"Uint16"],
                            'Time Dleay Engine Cooldown':[0,"Uint16"],
                            'Time Delay Emergcey Fail':[0,"Uint16"],
                            'Source 1 Overvoltage Dropout':[0,"Uint16"],
                            'Source 1 Overvotage Pickup':[0,"Uint16"],
                            'Source 1 Udervoltage Dropout':[0,"Uint16"],
                            'Source 1 Undervoltage Pickup':[0,"Uint16"],
                            'Source 1 Overfrequency Dropout':[0,"Uint16"],
                            'Source 1 Overfrequency Pickup':[0,"Uint16"],
                            'Source 1 Underfrequency Dropout':[0,"Uint16"],
                            'Source 1 Underfrequency Pickup':[0,"Uint16"],
                            'Source 2 Overvoltage Dropout':[0,"Uint16"],
                            'Source 2 Overvotage Pickup':[0,"Uint16"],
                            'Source 2 Udervoltage Dropout':[0,"Uint16"],
                            'Source 2 Undervoltage Pickup':[0,"Uint16"],
                            'Source 2 Overfrequency Dropout':[0,"Uint16"],
                            'Source 2 Overfrequency Pickup':[0,"Uint16"],
                            'Source 2 Underfrequency Dropout':[0,"Uint16"],
                            'Source 2 Underfrequency Pickup':[0,"Uint16"],
                            'Source 1 Voltage Unbalance Pickup':[0,"Uint16"],
                            'Source 1 Voltage Unbalance Droupout':[0,"Uint16"],
                            'Source 2 Voltage Unbalance Pickup':[0,"Uint16"],
                            'Source 2 Voltage Unbalance Droupout':[0,"Uint16"],
                            'Voltage Unbalance TIme Delay':[0,"Uint16"],
                            'Time Delay Normal Fail':[0,"Uint16"],
                            'Time Delay Emergecy Disconnect':[0,"Uint16"],
                            'Time Delay Emergency Reconnect':[0,"Uint16"],
                            'Time Delay Normal Dissconet':[0,"Uint16"],
                            'Time Delay Normal Reconnect':[0,"Uint16"],
                            'Engine (ATS) Test Duration':[0,"Uint16"],
                            'Overtemperature Action':[0,"Uint16"],
                            'Overtemperature Pickup':[0,"Uint16"],
                            'Current THD Alarm Pickup':[0,"Uint16"],
                            'Current THD Alarm Time':[0,"Uint16"],
                            'Voltage THD Alarm Pikcup':[0,"Uint16"],
                            'Voltage THD Alarm Time':[0,"Uint16"],
                            'Operations Count':[0,"Uint16"],
                            'Health Maintenace Alarm':[0,"Uint16"],
                            'Sneakers Alarm':[0,"Uint16"],
                            'Internal Error':[0,"Uint16"],
                            "THD Van" :[0,"Uint32"],
                            "THD Vbn":[0,"Uint32"],
                            "THD Vcn" :[0,"Uint32"],
                            "THD Vab" :[0,"Uint32"],
                            "THD Vbc" :[0,"Uint32"],
                            "THD Vca" :[0,"Uint32"],
                            "THD Ia" :[0,"Uint32"],
                            "THD Ib" :[0,"Uint32"],
                            "THD Ic" :[0,"Uint32"],
                            "THD In" :[0,"Uint32"],
                            'Current Unbalance':[0,"Q9"],
                            'Voltage Unbalance':[0, "Q9"],
                            'Ia Current Crest Factor':[0, "Q9"],
                            'Ib Current Crest Factor':[0, "Q9"],
                            'Ic Current Crest Factor':[0, "Q9"],
                            'In Current Crest Factor':[0, "Q9"],
                            'Max Power Factor':[0, "Q10"],
                            'Time of Max Power Factor':[0, "Date"],
                            'Min Power Factor':[0, "Q10"],
                            'Time Of Min Power Factor':[0, "Date"],
                            'Time of Max/Min Power Factor Reset':[0, "Date"],
                            'Max Freq':[0, "Q4"],
                            'Time of Max Freq':[0, "Date"],
                            'Min Freq':[0, "Q4"],
                            'TIme of Min Freq':[0, "Date"],
                            'Time of Max/Min Freq Reset':[0, "Date"],
                            "Source_Freq"       :  [0,"None"], 
                            "Ra_Phase_Angle"    :  [0,"None"],
                            "Rb_Phase_Angle"    :  [0,"None"],
                            "Rc_Phase_Angle"    :  [0,"None"],
                            "Ia_Phase_Angle"    :  [0,"None"],
                            "Ib_Phase_Angle"    :  [0,"None"],
                            "Ic_Phase_Angle"    :  [0,"None"],
                            "Va_Phase_Angle"    :  [0,"None"],
                            "Vb_Phase_Angle"    :  [0,"None"],
                            "Vc_Phase_Angle"    :  [0,"None"],
                            "I_Average"         :  [0,"Float"],
                            "V_LN_Average"      :  [0,"Float"],
                            "external_Vab_two"  :  [0,"Float"],
                            "external_Vbc_two"  :  [0,"Float"],
                            "external_Vca_two"  :  [0,"Float"],
                            "V_LL_Average"      :  [0,"Float"],
                            "VLL_Average_two"   :  [0,"Float"],
                            "freq_two"          :  [0,"Float"],
                            'external_Va_two'   :  [0,"Float"],
                            'external_Vb_two'   :  [0,"Float"],
                            'external_Vc_two'   :  [0,"Float"],
                            'V_LN_Average_two'  :  [0,"Float"],
                             "Withstand"  :  [0,"Float"],
                            'Frequency Protection Enable' : [0,"Uint16"],
                            'Overfrequency Action'        : [0,"Uint16"],
                            'Overfrequency Pickup'        : [0,"Uint16"],
                            'OverFrequency Time'          : [0,"Uint16"],
                            'UnderFrequency Action'       : [0,"Uint16"],
                            'UnderFrequency Pickup'       : [0,"Uint16"],
                            'UnderFrequency Time'         : [0,"Uint16"],
                             'Alarm Waveform Capture Precycles'  : [0,"Uint16"],
                            'Zero_R_Zero': [0,"Uint16"],
                            'Zero_R_One': [0,"Uint16"],
                            'Zero_R_Two': [0,"Uint16"],
                            'Overfrequency Alarm Action' : [0,"Uint16"],
                            'Overfrequency Alarm Pickup' : [0,"Uint16"],
                            'OverFrequency Alarm Time' : [0,"Uint16"],
                            'UnderFrequency Alarm Action' : [0,"Uint16"],
                            'UnderFrequency Alarm Pickup' : [0,"Uint16"],
                            'UnderFrequency Alarm Time' : [0,"Uint16"],
                            'Source Ground Sensor' :     [0,"Uint16"]} #Double Check Data Action
    
    add_setpoint_group_zero(repos)
    add_setpoint_group_one(repos)
    add_setpoint_group_two(repos)
    add_setpoint_group_three(repos)
    add_setpoint_group_five(repos)
    add_buffer_zero(repos)
    add_buffer_one(repos)
    add_buffer_ten(repos)
    add_configuration(repos)




                            
'''
    ====================================================================================================================
====Keys =======================================================================================================
    =================
'''

def get_setpoint_keys(repos):

    repos.mech_time = .008

                            


    repos.sp_four_keys = []                       
    repos.sp_six_keys = []
    repos.sp_seven_keys = []
    repos.angle_keys          =   ["Ra_Phase_Angle",
                                    "Rb_Phase_Angle",
                                    "Rc_Phase_Angle",
                                    "Ia_Phase_Angle",
                                    "Ib_Phase_Angle",
                                    "Ic_Phase_Angle",
                                    "Va_Phase_Angle",
                                    "Vb_Phase_Angle",
                                    "Vc_Phase_Angle"]
    

    repos.pf_and_freq_keys =[]

    
def get_buffer_keys(repos):



            

            
    repos.buffer_two_keys = ['forward energy',
                            'reverse energy',
                            'total energy',
                            'net energy',
                            'leading reactive energy',
                            'lagging reactive energy',
                            'total reactive energy',
                            'net reactive energy',
                            'apparent energy',
                            'last energy reset time']

    repos.buffer_three_keys = ["power demand interval",
                              "real power demand",
                              "reactive power demand",
                              "apparent power demand"]
    
    repos.buffer_four_keys = ["Max Real Power Demand",
                            "Time Of Max Pn Demand Occurrence",
                            "Max Reactive Power Demand",
                            "Time Of Max Pr Demand Occurrence",
                            "Max Apparent Power Demand",
                            "Time Of Max Pa Demand Occurrence",
                            "Last Time Of Resetting Power Demand"]

    repos.buffer_five_keys = ["ex_Ia_max",
                             "ex_Ia_max_time",
                             "ex_Ib_max",
                             "ex_Ib_max_time",
                             "ex_Ic_max",
                             "ex_Ic_max_time",
                             "ex_In_max",
                             "ex_In_max_time",
                             "ex_Ig_max",
                             "ex_Ig_max_time",
                             "ex_Ia_min",
                             "ex_Ia_min_time",
                             "ex_Ib_min",
                             "ex_Ib_min_time",
                             "ex_Ic_min",
                             "ex_Ic_min_time",
                             "ex_In_min",
                             "ex_In_min_time",
                             "ex_Ig_min",
                             "ex_Ig_min_time",
                             "Last_Reset"]

            
    repos.buffer_six_keys = ["total_short_circuit_counter",
                            "short_delay_trip_counter",
                            "instantaneous_trip_counter",
                            "high_current_trip_counter",
                            "total_overload_trip_counter",
                            "long_delay_trip_counter",
                            "ground_fault_trip_counter",
                            "total_operations_counter",
                            "trip_operations_counter",
                            "test_operations_counter",
                            "opens_operations_counter",
                            "manual_operations_counter",
                            "time_of_last_operations",
                            "max_temp",
                            "time_of_max_temp",
                            "running_minute",
                            "running_hour",
                            "running_day",
                            "life_points"]
    
    repos.buffer_seven_keys = ["max_Vab",
                            "time_max_Vab",
                            "max_Vbc",
                            "time_max_Vbc",
                            "max_Vca",
                            "time_max_Vca",
                            "min_Vab",
                            "time_min_Vab",
                            "min_Vbc",
                            "time_min_Vbc",
                            "min_Vca",
                            "time_min_Vca",
                            "time_reset"]
    
    repos.buffer_eight_keys = ["max_Van",
                            "time_max_Van",
                            "max_Vbn",
                            "time_max_Vbn",
                            "max_Vcn",
                            "time_max_Vcn",
                             "min_Van",
                            "time_min_Van",
                            "min_Vbn",
                            "time_min_Vbn",
                            "min_Vcn",
                            "time_min_Vcn",
                            "time_reset"]

            
    repos.buffer_eleven_keys = ['short_circuit_count',
                              'short_delay_count',
                              'instant_count',
                              'high_current_count',
                              'total_overload_count',
                              'long_delay_count',
                              'ground_fault_count',
                              'total_op_count',
                              'trip_op_count',
                              'opens_op_count',
                              'manual_op_count',
                              'time_of_last_op',
                              'max_temp',
                              'time_max_temp',
                              'run_miniute',
                              'run_hour',
                              'run_day',
                              'life_points']
    


            
    repos.buffer_eleven_keys = ['short_circuit_count',
                               'short_delay_count',
                               'instant_count',
                               'high_current_count',
                               'total_overload_count',
                               'long_delay_count',
                               'ground_fault_count',
                               'total_op_count',
                               'trip_op_count',
                               'opens_op_count',
                               'manual_op_count',
                               'time_of_last_op',
                               'max_temp',
                               'time_max_temp',
                               'run_miniute',
                               'run_hour',
                               'run_day',
                               'life_points'
                              ]

    repos.buffer_twelve_keys = ['phase_a_real_power',
                               'phase_b_real_power',
                               'phase_c_real_power',
                               'total_real_power',
                               'phase_a_reac_power',
                               'phase_b_reac_power',
                               'phase_c_reac_power',
                               'total_reac_power',
                               'phase_a_app_power',
                               'phase_b_app_power',
                               'phase_c_app_power',
                               'total_app_power']




    repos.buffer_thirteen_keys = ["USB Cable Connected State",
                                 "BSM1 State",
                                 "BSM2 State",
                                 "ARMS Switch State",
                                 "ARMS Communication State",
                                 "ARMS Secondary Pin State",
                                 "ARMS Active State",
                                 "1st Full Scan To All Rotary Switch State",
                                 "Setpoints Changed State",
                                 "Reset Button States",
                                 "Reset Trip Unit From Push Bottom State",
                                 "Reset Trip Unit From Comm Channels State",
                                 "Up Button State",
                                 "Down Button State",
                                 "Enter Button State",
                                 "Control Relay 0 From Comm State",
                                 "Control Relay 1 From Comm State",
                                 "Control Relay 2 From Comm State"]

    repos.buffer_fourteen_keys = []


def get_mapping_dictionary(repos):

    #Dictionary {Name: [keys, type, usb_read, usb_write]}

    
##    repos.mapping_dictionary = {'Setpoint 0'      : [repos.sp_zero_keys,   "write_setpoint_zero_request", "read_setpoint_zero_request"],
##                                'Setpoint 1'      : [repos.sp_one_keys,    "write_setpoint_one_request", "read_setpoint_one_request"],
##                                'Setpoint etu'    : [repos.sp_etu_keys,   "write_setpoint_one_request", "read_setpoint_one_request"],
##                                'Setpoint 2'      : [repos.sp_two_keys,          "write_setpoint_two_request", "read_setpoint_two_request"],
##                                'Setpoint 3'      : [repos.sp_three_keys,        "write_setpoint_three_request", "read_setpoint_three_request"],
##                                'Setpoint 5'      : [repos.sp_five_keys,      "write_setpoint_five_request", "read_setpoint_five_request"],
##                                'Setpoint 6'      : [repos.sp_six_keys,      "write_setpoint_six_request", "read_setpoint_six_request"],
##                                'Setpoint 7'      : [repos.sp_seven_keys,      "write_setpoint_seven_request", "read_setpoint_seven_request"],
##                                'Buffer 0'        : [repos.buffer_zero_keys,     "N/A" , "read_real_time_data_buffer_zero_request"],
##                                'Buffer 1'        : [repos.buffer_one_keys,      "N/A" , "read_real_time_data_buffer_one_request"],
##                                'Buffer 2'        : [repos.buffer_two_keys,     "N/A" , "read_real_time_data_buffer_two_request"],
##                                'Buffer 3'        : [repos.buffer_three_keys,      "N/A" , "read_real_time_data_buffer_three_request"],
##                                'Buffer 4'        : [repos.buffer_four_keys,     "N/A" , "read_real_time_data_buffer_four_request"],
##                                'Buffer 5'        : [repos.buffer_five_keys,      "N/A" , "read_real_time_data_buffer_five_request"],
##                                'Buffer 6'        : [repos.buffer_six_keys,  "N/A" , "read_real_time_data_buffer_six_request"],
##                                'Buffer 7'        : [repos.buffer_seven_keys,    "N/A" , "read_real_time_data_buffer_seven_request"],
##                                'Buffer 8'        : [repos.buffer_eight_keys,     "N/A" , "read_real_time_data_buffer_eight_request"],
##                                'Buffer 10'       : [repos.buffer_ten_keys,   "N/A" , "read_real_time_data_buffer_ten_request"],
##                                'Buffer 11'       : [repos.buffer_eleven_keys,  "N/A" , "read_real_time_data_buffer_eleven_request"],
##                                'Configuration'   : [repos.breaker_protection_capacity_keys,  "N/A" , "read_real_time_data_buffer_zero_request"],
##                                'angle_keys'      : [repos.angle_keys, "N/A", "N/A"],
##                                'Main'            : [repos.main_keys, "N/A", "N/A"],
##                                'Inputs'          : [repos.expected_keys, "N/A", "N/A"]}


   repos.mapping_dictionary = {'Setpoint 0'      : [repos.sp_zero_keys,   "write_setpoint_zero_request", "read_setpoint_zero_request"],
                                'Setpoint 1'      : [repos.sp_one_keys,    "write_setpoint_one_request", "read_setpoint_one_request"],
                                'Setpoint etu'    : [repos.sp_etu_keys,   "write_setpoint_one_request", "read_setpoint_one_request"],
                                'Setpoint 2'      : [repos.sp_two_keys,          "write_setpoint_two_request", "read_setpoint_two_request"],
                                'Setpoint 3'      : [repos.sp_three_keys,        "write_setpoint_three_request", "read_setpoint_three_request"],
                                'Setpoint 5'      : [repos.sp_five_keys,      "write_setpoint_five_request", "read_setpoint_five_request"],
                                'Setpoint 6'      : [repos.sp_six_keys,      "write_setpoint_six_request", "read_setpoint_six_request"],
                                'Setpoint 7'      : [repos.sp_seven_keys,      "write_setpoint_seven_request", "read_setpoint_seven_request"],
                                'Buffer 0'        : [repos.buffer_zero_keys,     "N/A" , "read_real_time_data_buffer_zero_request"],
                                'Buffer 1'        : [repos.buffer_one_keys,      "N/A" , "read_real_time_data_buffer_one_request"],
                                'Buffer 2'        : [repos.buffer_two_keys,     "N/A" , "read_real_time_data_buffer_two_request"],
                                'Buffer 3'        : [repos.buffer_three_keys,      "N/A" , "read_real_time_data_buffer_three_request"],
                                'Buffer 4'        : [repos.buffer_four_keys,     "N/A" , "read_real_time_data_buffer_four_request"],
                                'Buffer 5'        : [repos.buffer_five_keys,      "N/A" , "read_real_time_data_buffer_five_request"],
                                'Buffer 6'        : [repos.buffer_six_keys,  "N/A" , "read_real_time_data_buffer_six_request"],
                                'Buffer 7'        : [repos.buffer_seven_keys,    "N/A" , "read_real_time_data_buffer_seven_request"],
                                'Buffer 8'        : [repos.buffer_eight_keys,     "N/A" , "read_real_time_data_buffer_eight_request"],
                                'Buffer 10'       : [repos.buffer_ten_keys,   "N/A" , "read_real_time_data_buffer_ten_request"],
                                'Buffer 11'       : [repos.buffer_eleven_keys,  "N/A" , "read_real_time_data_buffer_eleven_request"],
                                'Configuration'   : [repos.breaker_protection_capacity_keys,  "N/A" , "read_real_time_data_buffer_zero_request"],
                                'angle_keys'      : [repos.angle_keys, "N/A", "N/A"],
                                'Main'            : [repos.main_keys, "N/A", "N/A"],
                                'Inputs'          : [repos.expected_keys, "N/A", "N/A"],
                                'pf_and_freq'     : [repos.pf_and_freq_keys, "N/A", "N/A"]}
   
   repos.default_array       =  ['Setpoint etu', 
                                 'Setpoint 0']

def get_rog_ratio(frame, rating):

    print("Rog Ratio")
    print(frame)
    if frame == 21: #PD2
        row_ratio = 0
    elif frame == 22 or frame == 23 or frame == 24: #PD3A/3B/4
        row_ratio = 1/3276.8
    
    elif frame == 25: #PD5
        row_ratio = 335/1000000

    elif frame == 26: #PD6
        row_ratio = 364/1000000

    else:
        row_ratio = .0000000001 #PD2 Or Invalid

    
    return row_ratio

def get_ct_ratio(frame, rating):
    if frame == 21: #PD2

        ph = False
        ph_type = 0 
        
        if rating > 100:
            ct_ratio = 3750
        else:
            ct_ratio = 1500
    else:
        ct_ratio = 0
        ph = True
        ph_type = 1

    return ct_ratio, ph, ph_type

def get_mech_time(frame):

    if frame == 21: #PD2
        mech_time = .004
    elif frame == 22 or frame == 23 or frame == 24: #PD5
        mech_time = .004
    elif frame == 25: #PD5
        mech_time = .014
    else: #PD6
        mech_time = .016

    return mech_time 
        
def change_pxr20_data_types(repos): #Some PXR25 and PXR20 have different data types

    print("Changing Types")
    repos.etu_dictionary['ex_Ia_max'][1]   = "Q4"
    repos.etu_dictionary['ex_Ib_max'][1]   = "Q4"
    repos.etu_dictionary['ex_Ic_max'][1]   = "Q4"
    repos.etu_dictionary['ex_In_max'][1]   = "Q4"
    repos.etu_dictionary['ex_Ig_max'][1]   = "Q4"
    repos.etu_dictionary['ex_Ia_min'][1]   = "Q4"
    repos.etu_dictionary['ex_Ib_min'][1]   = "Q4"
    repos.etu_dictionary['ex_Ic_min'][1]   = "Q4"
    repos.etu_dictionary['ex_In_min'][1]   = "Q4"
    repos.etu_dictionary['ex_Ig_min'][1]   = "Q4"
    repos.etu_dictionary['external_Ia'][1] = "Q4"
    repos.etu_dictionary['external_Ib'][1] = "Q4"
    repos.etu_dictionary['external_Ic'][1] = "Q4"
    repos.etu_dictionary['external_In'][1] = "Q4"
    repos.etu_dictionary['external_Ig'][1] = "Q4"
    repos.etu_dictionary['freq'][1]        = "Uint32"
    repos.etu_dictionary['pf'][1]          = "Uint32"

def change_pxr10_data_types(repos): #Some PXR25 and PXR20 have different data types

    print("Changing Types")
    repos.etu_dictionary['ex_Ia_max'][1]   = "Q4"
    repos.etu_dictionary['ex_Ib_max'][1]   = "Q4"
    repos.etu_dictionary['ex_Ic_max'][1]   = "Q4"
    repos.etu_dictionary['ex_In_max'][1]   = "Q4"
    repos.etu_dictionary['ex_Ig_max'][1]   = "Q4"
    repos.etu_dictionary['ex_Ia_min'][1]   = "Q4"
    repos.etu_dictionary['ex_Ib_min'][1]   = "Q4"
    repos.etu_dictionary['ex_Ic_min'][1]   = "Q4"
    repos.etu_dictionary['ex_In_min'][1]   = "Q4"
    repos.etu_dictionary['ex_Ig_min'][1]   = "Q4"
    repos.etu_dictionary['external_Ia'][1] = "Q4"
    repos.etu_dictionary['external_Ib'][1] = "Q4"
    repos.etu_dictionary['external_Ic'][1] = "Q4"
    repos.etu_dictionary['external_In'][1] = "Q4"
    repos.etu_dictionary['external_Ig'][1] = "Q4"
    repos.etu_dictionary['freq'][1]        = "Uint32"
    repos.etu_dictionary['pf'][1]          = "Uint32"

def reset_to_no_trip_values(repos):
    #Group 0 Values
    repos.etu_dictionary['MM Mode'][0] = 0
    repos.etu_dictionary['MM Level'][0] = 5
    repos.etu_dictionary['Line Frequency'][0] = 60
    repos.etu_dictionary['Reverse Feed'][0] = 0
    repos.etu_dictionary['Sign'][0] = 0
    repos.etu_dictionary['Power Window'][0] = 0
    repos.etu_dictionary['Power Interval'][0] = 5
    repos.etu_dictionary['Language'][0] = 0
    repos.etu_dictionary['I Window'][0] = 0
    repos.etu_dictionary['I Interval'][0] = 5
    repos.etu_dictionary['Health Level'][0] = 100

    


    #Group 1 Values                        
    repos.etu_dictionary['LD Slope'][0] = 2
    repos.etu_dictionary['LD PU'][0] = repos.etu_dictionary['Rating'][0]
    repos.etu_dictionary['LD Time'][0] = 24
    repos.etu_dictionary['SD PU'][0] = 0
    repos.etu_dictionary['SD Slope'][0] = 0
    repos.etu_dictionary['GF Mode'][0] = 2
    repos.etu_dictionary['ZSI'][0] = 0
    repos.etu_dictionary['LD Thermal'][0] = 0
    repos.etu_dictionary['GF Thermal'][0] = 0
    repos.etu_dictionary['SD Time'][0] = .5


        

    
    repos.etu_dictionary['Etu LD Slope'][0] = 2
    repos.etu_dictionary['Etu LD PU'][0] = repos.etu_dictionary['Rating'][0]
    repos.etu_dictionary['Etu LD Time'][0] = 240
    repos.etu_dictionary['Etu SD PU'][0] = 0
    repos.etu_dictionary['Etu SD Slope'][0] = 0
    repos.etu_dictionary['Etu SD Time'][0] = 500
    repos.etu_dictionary['Etu GF Mode'][0] = 2
    repos.etu_dictionary['Etu ZSI'][0] = 0
    repos.etu_dictionary['Etu LD Thermal'][0] = 0
    repos.etu_dictionary['Etu GF Thermal'][0] = 0

    if repos.pxr == "PXR10":
        repos.etu_dictionary['SD PU'][0] = 0
        repos.etu_dictionary['Etu SD PU'][0] = 0
        repos.etu_dictionary['SD Time'][0] = 0
        repos.etu_dictionary['Etu SD Time'][0] = 0
        repos.etu_dictionary['LD Time'][0] = 10
        repos.etu_dictionary['Etu LD Time'][0] = 100

        
    frame = repos.etu_dictionary['Frame'][0]
    
    if frame == 21: #PD2
        if repos.etu_dictionary['Rating'][0] == 60:
            repos.etu_dictionary['Etu Inst PU' ][0] = 183
            repos.etu_dictionary['Inst PU'][0] = 18.3
        elif repos.etu_dictionary['Rating'][0] == 63:
            repos.etu_dictionary['Etu Inst PU' ][0] = 174
            repos.etu_dictionary['Inst PU'][0] = 17.4
        elif repos.etu_dictionary['Rating'][0] ==100:
            repos.etu_dictionary['Etu Inst PU' ][0] = 110
            repos.etu_dictionary['Inst PU'][0] = 11
        elif repos.etu_dictionary['Rating'][0] == 150:
            repos.etu_dictionary['Etu Inst PU' ][0] = 140
            repos.etu_dictionary['Inst PU'][0] = 14
        elif repos.etu_dictionary['Rating'][0] == 160:
            repos.etu_dictionary['Etu Inst PU' ][0] = 131
            repos.etu_dictionary['Inst PU'][0] = 13.1
        elif repos.etu_dictionary['Rating'][0] == 200:
            repos.etu_dictionary['Etu Inst PU' ][0] = 105
            repos.etu_dictionary['Inst PU'][0] = 10.5
        elif repos.etu_dictionary['Rating'][0] == 225:
            repos.etu_dictionary['Etu Inst PU' ][0] = 93
            repos.etu_dictionary['Inst PU'][0] = 9.3
        elif repos.etu_dictionary['Rating'][0] == 250:
            repos.etu_dictionary['Etu Inst PU' ][0] = 84
            repos.etu_dictionary['Inst PU'][0] = 8.4
        
    elif frame == 22: #PD3A
        if repos.etu_dictionary['Rating'][0] == 125:
            repos.etu_dictionary['Etu Inst PU' ][0] = 240
            repos.etu_dictionary['Inst PU'][0] = 24
        elif repos.etu_dictionary['Rating'][0] == 250:
            repos.etu_dictionary['Etu Inst PU' ][0] = 176
            repos.etu_dictionary['Inst PU'][0] = 17.6
        elif repos.etu_dictionary['Rating'][0] == 400:
            repos.etu_dictionary['Etu Inst PU' ][0] = 110
            repos.etu_dictionary['Inst PU'][0] = 11

    elif frame == 23: #PD3B
        if repos.etu_dictionary['Rating'][0] == 250:
            repos.etu_dictionary['Etu Inst PU' ][0] = 288
            repos.etu_dictionary['Inst PU'][0] = 28.8
        elif repos.etu_dictionary['Rating'][0] == 400:
            repos.etu_dictionary['Etu Inst PU' ][0] = 180
            repos.etu_dictionary['Inst PU'][0] = 18
        elif repos.etu_dictionary['Rating'][0] == 600:
            repos.etu_dictionary['Etu Inst PU' ][0] = 120
            repos.etu_dictionary['Inst PU'][0] = 12
        elif repos.etu_dictionary['Rating'][0] == 630:
            repos.etu_dictionary['Etu Inst PU' ][0] = 114
            repos.etu_dictionary['Inst PU'][0] = 11.4
            
    elif frame == 24: #PD4
        repos.etu_dictionary['Etu Inst PU' ][0] = 80
        repos.etu_dictionary['Inst PU'][0] = 8

    elif frame == 25: #PD5
        repos.etu_dictionary['Etu Inst PU' ][0] = 90
        if repos.etu_dictionary['Rating'][0] == 800:
            repos.etu_dictionary['LD Time'][0] = 14
            repos.etu_dictionary['Inst PU'][0] = 15
            repos.etu_dictionary['Etu Inst PU' ][0] = 150
        elif repos.etu_dictionary['Rating'][0] == 1600:
            repos.etu_dictionary['LD Time'][0] = 20
            repos.etu_dictionary['Inst PU'][0] = 9
            repos.etu_dictionary['Etu Inst PU' ][0] = 90
            
    else: #PD6
        if repos.etu_dictionary['Rating'][0] == 1600:
            repos.etu_dictionary['Etu Inst PU' ][0] = 100
            repos.etu_dictionary['Inst PU'][0] = 10
        else:
            repos.etu_dictionary['Etu Inst PU' ][0] = 70
            repos.etu_dictionary['Inst PU'][0] = 7


    


    #Group 5 Values  
    repos.etu_dictionary['Over V Action'][0]      = 0
    repos.etu_dictionary['Over V PU'][0]        = 180
    repos.etu_dictionary['Over V Time'][0]      = 300
    repos.etu_dictionary['Under V Action'][0]     = 2
    repos.etu_dictionary['Under V PU'][0]       = 60
    repos.etu_dictionary['Under V Time'][0]     = 300
    repos.etu_dictionary['V Unbalance Action'][0] = 2
    repos.etu_dictionary['V Unbalance PU'][0]   = 5
    repos.etu_dictionary['V Unbalance Time'][0] = 300
    repos.etu_dictionary['I Unbalance Action'][0] = 2
    repos.etu_dictionary['I Unbalance PU'][0]   = 5
    repos.etu_dictionary['Rev Power Action'][0]   = 2
    repos.etu_dictionary['Rev Power PU'][0]     = 1
    repos.etu_dictionary['Rev Power Time'][0]   = 300
    repos.etu_dictionary['Power Rev Sense'][0]  = 1
    repos.etu_dictionary['Power Rev Action'][0]   = 2
    repos.etu_dictionary['Phase Loss Action'][0]  = 2
    repos.etu_dictionary['Phase Loss Time'][0]  = 1



    

    
    
    


