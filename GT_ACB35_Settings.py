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

'''


'''
================================================================================================================================
Add Setpoint Groups

add_dictionary_values(repos,keys)
add_setpoint_group_zero(repos)
add_setpoint_group_one(repos)
add_setpoint_group_two(repos)
add_setpoint_group_three(repos)
add_setpoint_group_four(repos)
add_setpoint_group_five(repos)
add_setpoint_group_six(repos)
add_setpoint_group_seven(repos)
add_setpoint_group_eight(repos)
add_setpoint_group_ten(repos)

===============================================================================================================================
'''

def add_dictionary_values(repos, keys):

    for val in keys:
        repos.etu_dictionary.update({val:[0, "Uint16"]})

    
def add_setpoint_group_zero(repos):

    repos.sp_zero_keys =   ['Rating',
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
                            'Health Level',
                            'System Voltage',
                            'Neutral Sensor',
                            'Source Ground Sensor',
                            'Setpoints Group Sensor',
                            'Active Setpoints Group',
                            'ScondPT/VDB Module Present',
                            'Phase Labeling',
                            'Trip Waveform Capture Precycles',
                            'Alarm Waveform Capture Precycles',
                            'Extended Capture Triggers',
                            'IEC61860 Configuration',
                            'Demand Logging Interval',
                            'Zero_R_Zero',
                            'Zero_R_One',
                            'Zero_R_Two']

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
                            'Thermal Alarm',
                            'HL Alarm 1 Time',
                            'GF ZSI',
                            'Neutral Alarm Pickup',
                            'Neutral Alarm Time',
                            'HL Alarm 2 Time',
                            'HL Alarm 1 Action',
                            'HL Alarm 2 Action', 
                            'LDPU Disturb Capture',
                            'SG Sensor',
                            'LD Event Action',
                            'Reserved16',
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
                            'Etu Thermal Alarm',
                            'Etu HL Alarm 1 Time',
                            'Etu GF ZSI', 
                            'Etu Neutral Alarm Pickup',
                            'Etu Neutral Alarm Time',
                            'Etu HL Alarm 2 Time',
                            'Etu HL Alarm 1 Action',
                            'Etu HL Alarm 2 Action', 
                            'Etu LDPU Disturb Capture',
                            'Etu SG Sensor',
                            'Etu LD Event Action',
                            'Etu Reserved16',
                            'Etu Reserved16'
                            ]
    
    add_dictionary_values(repos, repos.sp_one_keys)
    add_dictionary_values(repos, repos.sp_etu_keys)

def add_setpoint_group_two(repos):

    repos.sp_two_keys   =   ['MBus Address',
                             'MBus Baud',
                             'MBus Parity',
                             'MBus Stop Bit'
                             'RTU Invalid Handeling',
                             'RTU Routing Word Order',
                             'RTU Fixed Word Order',
                             'RTU Permissions',
                             'TCP Invalid Handeling',
                             'TCP Routing Word Order',
                             'TCP Fixed Word Order',
                             'Timout',
                             'TCP IP Filter Enable',
                             'TCP Permissions']
    
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

def add_setpoint_group_four(repos):
    
    repos.sp_four_keys =   ['Frequency Protection Enable',
                            'Over Frequency Action',
                            'Over Frequency Pickup',
                            'Over Frequency Time',
                            'Under Frequency Action',
                            'Under Frequency Pickup',
                            'Under Frequency Time',
                            'Over Frequency Alarm Action',
                            'Over Frequency Alarm Pickup',
                            'Over Frequency Alarm Time',
                            'Under Frequency Alarm Action',
                            'Under Frequency Alarm Pickup',
                            'Under Frequency Alarm Time',
                            'Reserved16',
                            'Reserved16',
                            'Reserved16']
    
    add_dictionary_values(repos, repos.sp_four_keys)
    
def add_setpoint_group_five(repos):
    
    repos.sp_five_keys =   ['Over V Action',
                            'Over V PU',
                            'Over V Time',
                            'Under V Action',
                            'Under V PU', 
                            'Under V Time',
                            'V Unbalance Action',
                            'V Unbalance PU',
                            'V Unbalance Time',
                            'I Unbalance Action',
                            'I Unbalance PU',
                            'I Unbalance Time',
                            'Reverse Forward Power Action',
                            'Reverse Forward Power Pickup',
                            'Reverse Forward Power Time',
                            'Power Rev Sense',
                            'Power Rev Action',
                            'Phase Loss Action',
                            'Phase Loss Time',
                            'Reserved16_5-1',
                            'Reserved16_5-2',
                            'Reserved16_5-3',
                            'Reserved16_5-4',
                            'Reserved16_5-5',
                            'Over V Alarm Action',
                            'Over V Alarm PU',
                            'Over V Alarm Time',
                            'Extended Protection Enable/Disable',
                            'Reverse Reactive Power Action',
                            'Reverse Reactive Power Pickup',
                            'Reverse Reactive Power Time',
                            'Phase Rotation Time',
                            'Over V Number Of Phases',
                            'Under V Number Of Phases',
                            'Under V Alarm Action',
                            'Under V Alarm PU',
                            'Under V Alarm Time',
                            'V Unbalance Alarm Action',
                            'V Unbalance Alarm PU',
                            'V Unbalance Alarm Time',
                            'I Unbalance Alarm Action',
                            'I Unbalance Alarm PU',
                            'I Unbalance Alarm Time',
                            'Reserved16_5-6',
                            'Reserved16_5-7']
    
    add_dictionary_values(repos, repos.sp_five_keys)
                            
def add_setpoint_group_six(repos):

    repos.sp_six_keys = ['Power Protection Enable/Disable',
                               'Forward Real Power Action',
                               'Forward Real Power Pickup',
                               'Forward Real Power Time',
                               'Forward Reactive Power Action',
                               'Forward Reactvie Power Pickup',
                               'Forward Reactive Power Time',
                               'Apparent Power Action',
                               'Apparent Power Pickup',
                               'Apparent Power Time',
                               'Under Power Factor Action',
                               'Under Power Factor Pickup',
                               'Under Power Factor Time',
                               'Real Demand Power Action',
                               'Real Demand Power Pickup',
                               'Real Demand Power Time',
                               'Apparent Demand Power Time',
                               'Apparent Demand Power Action',
                               'Apparent Demand Power Pickup',
                               'Demand Mode Precision',
                               'Reserved16',
                               'Reserved16_3']
    
    add_dictionary_values(repos, repos.sp_six_keys)


def add_setpoint_group_seven(repos):

    repos.sp_seven_keys =       ['Sync Check Action',
                                 'Sync Check Min Linve Voltage 1',
                                 'Sync Check Max Dead Voltage 1',
                                 'Sync Check Min Live Voltage 2',
                                 'Sync Check Max Live Voltage 2',
                                 'Sync Check Max Voltage Difference',
                                 'Sync Check Max Slip Frequency',
                                 'Sync Check Max Angle Difference',
                                 'Sync Check Dead V1 - Dead V2 Enable',
                                 'Sync Check Dead V1 - Live V2 Enable',
                                 'Sync Check Live V1 - Dead V2 Enable',
                                 'Sync Check Live V1 - Dead V2 Enable',
                                 'Sync Cheeck Dead Time',
                                 'Reserved16',
                                 'Reserved16',
                                 'Reserved16']
    
    add_dictionary_values(repos, repos.sp_six_keys)
    
def add_setpoint_group_eight(repos):

    repos.setpoint_eight_keys = ['ATS Function Enable/Disable'
                                 'Number of Generators',
                                 'Phase Seq',
                                 'Manual Retransfer',
                                 'Commit To Transfer',
                                 'Closed Enable',
                                 'Closed Voltage Difference',
                                 'Closed Frequency Difference',
                                 'In-Phase Enable',
                                 'In-Phase Freqnecy Difference',
                                 'Sync Timer',
                                 'Load Voltage Decay',
                                 'Time Delay Neutral',
                                 'Time Delay Normal to Emergency',
                                 'Time Delay Emergency to Normal',
                                 'Time Delay Pretransfer',
                                 'Time Delay Posttransfer',
                                 'Time Delay Engine Start(Source2)',
                                 'Time Delay Engine Start(Source1)',
                                 'Time Dleay Engine Cooldown',
                                 'Time Delay Emergcey Fail',
                                 'Time Delay Emergecy Disconnect',
                                 'Time Delay Emergency Reconnect',
                                 'Time Delay Normal Fail',
                                 'Time Delay Normal Disconnect',
                                 'Time Delay Normal Reconnect',
                                 'Engine (ATS) Test Duration',
                                 'Source 1 Overvoltage Dropout',
                                 'Source 1 Overvotage Pickup',
                                 'Source 1 Udervoltage Dropout',
                                 'Source 1 Undervoltage Pickup',
                                 'Source 1 Overfrequency Dropout',
                                 'Source 1 Overfrequency Pickup',
                                 'Source 1 Underfrequency Dropout',
                                 'Source 1 Underfrequency Pickup',
                                 'Source 1 Voltage Unbalance Dropout',
                                 'Source 1 Voltage Unbalance Pickup',
                                 'Source 1 Voltage Unbalance Time Delay',
                                 'Spare 1',
                                 'Spare 2',
                                 'Spare 3',
                                 'Spare 4',
                                 'Spare 5',
                                 'Spare 6',
                                 'Spare 7',
                                 'Spare 8',
                                 'Spare 9',
                                 'Spare 10',
                                 'Spare 11',
                                 'Spare 12',
                                 'Spare 13',
                                 'Spare 14',
                                 'Spare 15']
                                 
    add_dictionary_values(repos, repos.setpoint_eight_keys)
    
def add_setpoint_group_nine(repos):
    
    repos.setpoint_nine_keys = ['Overtemperature Action',
                                'Overtemperature Pickup',
                                'Current THD Alarm Pickup',
                                'Current THD Alarm Time',
                                'Voltage THD Alarm Pickup',
                                'Voltage THD Alarm Time',
                                'Operations Count',
                                'Health Maintenace Alarm',
                                'Sneakers Alarm',
                                'Internal Error']
                                
    add_dictionary_values(repos, repos.setpoint_nine_keys)
    
def add_setpoint_group_ten(repos):


    repos.setpoint_ten_keys = ['Device Name',
                               'Downstream Breaker 1',
                               'Downstream Breaker 2',
                               'Downstream Breaker 3',
                               'Downstream Breaker 4',
                               'Downstream Breaker 5',
                               'Downstream Breaker 6',
                               'Downstream Breaker 7',
                               'Downstream Breaker 8',
                               'Downstream Breaker 9',
                               'Downstream Breaker 10',
                               'Downstream Breaker 11',
                               'Downstream Breaker 12',
                               'Downstream Breaker 13',
                               'Downstream Breaker 14',
                               'Downstream Breaker 15',
                               'Downstream Breaker 16',
                               'Downstream Breaker 17',
                               'Downstream Breaker 18',
                               'Downstream Breaker 19',
                               'Downstream Breaker 20',
                               'Downstream Breaker 21',
                               'Downstream Breaker 22',
                               'Downstream Breaker 23',
                               'Downstream Breaker 24',
                               'Downstream Breaker 25',
                               'Downstream Breaker 26',
                               'Downstream Breaker 27',
                               'Downstream Breaker 28',
                               'Downstream Breaker 29',
                               'Downstream Breaker 30',
                               'Downstream Breaker 31',
                               'Trip Fail Protection Action',
                               'Trip Fail Downstream Breaker 1',
                               'Trip Fail Downstream Breaker 2',
                               'Trip Fail Downstream Breaker 3',
                               'Trip Fail Downstream Breaker 4',
                               'Trip Fail Downstream Breaker 5',
                               'Trip Fail Downstream Breaker 6',
                               'Trip Fail Downstream Breaker 7',
                               'Trip Fail Downstream Breaker 8',
                               'Trip Fail Downstream Breaker 9',
                               'Trip Fail Downstream Breaker 10',
                               'Trip Fail Downstream Breaker 11',
                               'Trip Fail Downstream Breaker 12',
                               'Trip Fail Downstream Breaker 13',
                               'Trip Fail Downstream Breaker 14',
                               'Trip Fail Downstream Breaker 15',
                               'Trip Fail Downstream Breaker 16',
                               'Trip Fail Downstream Breaker 17',
                               'Trip Fail Downstream Breaker 18',
                               'Trip Fail Downstream Breaker 19',
                               'Trip Fail Downstream Breaker 20',
                               'Trip Fail Downstream Breaker 21',
                               'Trip Fail Downstream Breaker 22',
                               'Trip Fail Downstream Breaker 23',
                               'Trip Fail Downstream Breaker 24',
                               'Trip Fail Downstream Breaker 25',
                               'Trip Fail Downstream Breaker 26',
                               'Trip Fail Downstream Breaker 27',
                               'Trip Fail Downstream Breaker 28',
                               'Trip Fail Downstream Breaker 29',
                               'Trip Fail Downstream Breaker 30',
                               'Trip Fail Downstream Breaker 31',
                               'Setpoint Set Selector',
                               'Setpoint Set Selector Device 1',
                               'Setpoint Set Selector Device 2',
                               'Setpoint Set Selector Device 3',
                               'Setpoint Set Selector Device 4',
                               'Setpoint Set Selector Device 5',
                               'Setpoint Set Selector Device 6',
                               'Setpoint Set Selector Device 7',
                               'Metered Value Action',
                               'Current Deadband',
                               'Voltage Deadband',
                               'Active Power Deadband',
                               'Reactive Power Deadband',
                               'Apparent Power Deadband',
                               'Frequency Deadband',
                               'Power factor Deadband',
                               'Reserved',
                               'Reserved',
                               'Reserved',
                               'Reserved',
                               'Reserved']
                               
    add_dictionary_values(repos, repos.setpoint_ten_keys)

    
def add_setpoint_group_eleven(repos):


    repos.setpoint_eleven_keys = ['MBus Address',
                                  'MBus Baud',
                                  'MBus Parity',
                                  'MBus Stop Bit',
                                  'eCam DHCP',
                                  'eCam IP Zero',
                                  'eCam IP One',
                                  'eCam IP Two',
                                  'eCam IP Three',
                                  'eCam Subnet',
                                  'eCam Default Two',
                                  'eCam Default One',
                                  'eCam Reset']
                                  
    add_dictionary_values(repos, repos.setpoint_eleven_keys)


'''
================================================================================================================================
Add Setpoint Groups

add_buffer_zero(repos)
add_buffer_two(repos)
add_buffer_four(repos)
add_buffer_five(repos)
add_buffer_six(repos)
add_buffer_eleven(repos)
add_buffer_fourty_two(repos)
add_buffer_fourty_three(repos)
add_buffer_fourty_four(repos)
add_buffer_fourty_five(repos)
add_buffer_fourty_six(repos)
add_buffer_fourty_seven(repos)
add_buffer_fourty_eight(repos)
add_buffer_fourty_nine(repos)
add_buffer_fifty(repos)
add_buffer_fifty_one(repos)
add_buffer_fifty_two(repos)
add_buffer_fifty_three(repos)
add_buffer_fifty_four(repos)
add_buffer_fifty_five(repos)
add_buffer_sixty_nine(repos)


===============================================================================================================================
'''    
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
                            'Source Ground Active',
                            'Spring_Charged']
    
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
    repos.etu_dictionary['Spring_Charged']       = ["Uknown", "Bin"]

def add_buffer_two(repos):

    repos.buffer_fourty_two_keys = ['Forward Energy',
                                     'Reverse Energy',
                                     'Total Energy',
                                     'Net Energy',
                                     'Leading Reactive Energy',
                                     'Lagging Reactive Energy',
                                     'Total Reactive Energy',
                                     'Net Reactive Energy',
                                     'Apparent Energy',
                                     'Last Energy Reset Time']
    
    repos.etu_dictionary['Forward Energy']          = [0, "Uint64"]
    repos.etu_dictionary['Reverse Energy']          = [0, "Uint64"]
    repos.etu_dictionary['Total Energy']            = [0, "int64"]
    repos.etu_dictionary['Net Energy']              = [0, "int64"]
    repos.etu_dictionary['Leading Reactive Energy'] = [0, "Uint64"]
    repos.etu_dictionary['Lagging Reactive Energy'] = [0, "Uint64"]
    repos.etu_dictionary['Total Reactive Energy']   = [0, "int64"]
    repos.etu_dictionary['Net Reactive Energy']     = [0, "int64"]
    repos.etu_dictionary['Apparent Energy']         = [0, "Uint64"]
    repos.etu_dictionary['Last Energy Reset Time']  = [0, "Date"]
    

def add_buffer_four(repos):

    repos.buffer_four_keys =   ['Max Real Power Demand',
                                 'Max Real Power Demand TS',
                                 'Max Reactive Power Demand',
                                 'Max Reactive Power Demand TS',
                                 'Max Apparent Power Demand',
                                 'Max Apparent Power Demand TS',
                                 'Last PD Reset TS']
    
    repos.etu_dictionary['Max Real Power Demand']           = [0, "Uint32"]
    repos.etu_dictionary['Max Real Power Demand TS']        = [0, "Date"],
    repos.etu_dictionary['Max Reactive Power Demand']       = [0, "Uint32"]
    repos.etu_dictionary['Max Reactive Power Demand TS']    = [0, "Date"]
    repos.etu_dictionary['Max Apparent Power Demand']       = [0, "Uint32"]
    repos.etu_dictionary['Max Apparent Power Demand TS']    = [0, "Date"]
    repos.etu_dictionary['Last PD Reset TS']                = [0, "Date"]


def add_buffer_five(repos):

    repos.buffer_five =        ['Max IA',
                               'Max IA TS',
                               'Max IB',
                               'Max IB TS',
                               'Max IC',
                               'Max IC TS',
                               'Max IN',
                               'Max IN TS',
                               'Max IG',
                               'Max IG TS',
                               'Min IA',
                               'Min IA TS',
                               'Min IB',
                               'Min IB TS',
                               'Min IC',
                               'Min IC TS',
                               'Min IN',
                               'Min IN TS',
                               'Min IG',
                               'Min IG TS',
                               'Last I Max-Min Reset TS']
    
    repos.etu_dictionary['Max IA']              = [0, "Q4"]
    repos.etu_dictionary['Max IA TS']           = [0, "Date"]
    repos.etu_dictionary['Max IB']              = [0, "Q4"]
    repos.etu_dictionary['Max IB TS']           = [0, "Date"]
    repos.etu_dictionary['Max IC']              = [0, "Q4"]
    repos.etu_dictionary['Max IC TS']           = [0, "Date"]   
    repos.etu_dictionary['Max IN']              = [0, "Q4"]
    repos.etu_dictionary['Max IN TS']           = [0, "Date"]
    repos.etu_dictionary['Max IG']              = [0, "Q4"]
    repos.etu_dictionary['Max IG TS']           = [0, "Date"]      
    repos.etu_dictionary['Min IA']              = [0, "Q4"]
    repos.etu_dictionary['Min IA TS']           = [0, "Date"]
    repos.etu_dictionary['Min IB']              = [0, "Q4"]
    repos.etu_dictionary['Min IB TS']           = [0, "Date"]
    repos.etu_dictionary['Min IC']              = [0, "Q4"]
    repos.etu_dictionary['Min IC TS']           = [0, "Date"]
    repos.etu_dictionary['Min IN']              = [0, "Q4"]
    repos.etu_dictionary['Min IN TS']           = [0, "Date"]
    repos.etu_dictionary['Min IG']              = [0, "Q4"]
    repos.etu_dictionary['Min IG TS']           = [0, "Date"]
    repos.etu_dictionary['Last I Max-Min Reset TS']                = [0, "Date"]

def add_buffer_six(repos):

    repos.buffer_six_keys = ['Ext Total Short Circuit Counter',
                            'Ext Short Delay Trip Counter',
                            'Ext Instantaneous Trip Counter',
                            'Ext High Current Trip Counter',
                            'Ext Total Overload Trip Counter',
                            'Ext Long Delay Trip Counter',
                            'Ext Ground Fault Trip Counter',
                            'Ext Total Operations Counter',
                            'Ext Trip Operations Counter',
                            'Ext Test Operations Counter',
                            'Ext Opens Operations Counter',
                            'Ext Manual Operations Counter',
                            'Ext Time Of Last Operations',
                            'Ext Max Temp',
                            'Ext Time Of Max Temp',
                            'Ext Running Minute',
                            'Ext Running Hour',
                            'Ext Running Day',
                            'Ext Life Points']
    
    repos.etu_dictionary['Ext Total Short Circuit Counter']     = [0, "Uint16"]
    repos.etu_dictionary['Ext Short Delay Trip Counter']        = [0, "Uint16"]
    repos.etu_dictionary['Ext Instantaneous Trip Counter']      = [0, "Uint16"]
    repos.etu_dictionary['Ext High Current Trip Counter']       = [0, "Uint16"]
    repos.etu_dictionary['Ext Total Overload Trip Counter']     = [0, "Uint16"]
    repos.etu_dictionary['Ext Long Delay Trip Counter']         = [0, "Uint16"]
    repos.etu_dictionary['Ext Ground Fault Trip Counter']       = [0, "Uint16"]
    repos.etu_dictionary['Ext Total Operations Counter']        = [0, "Uint16"]
    repos.etu_dictionary['Ext Trip Operations Counter']         = [0, "Uint16"]
    repos.etu_dictionary['Ext Test Operations Counter']         = [0, "Uint16"]
    repos.etu_dictionary['Ext Opens Operations Counter']        = [0, "Uint16"]
    repos.etu_dictionary['Ext Manual Operations Counter']       = [0, "Uint16"]
    repos.etu_dictionary['Ext Total Short Circuit Counter']     = [0, "Uint16"]
    repos.etu_dictionary['Ext Time Of Last Operations']         = [0, "Date"]
    repos.etu_dictionary['Ext Max Temp']                        = [0, "Q4Padded"]
    repos.etu_dictionary['Ext Time Of Max Temp']                = [0, "Date"]
    repos.etu_dictionary['Ext Running Minute']                  = [0, "Uint16"]
    repos.etu_dictionary['Ext Running Hour']                    = [0, "Uint16"]
    repos.etu_dictionary['Ext Running Day']                     = [0, "Uint16"]
    repos.etu_dictionary['Ext Life Points']                     = [0, "Uint32"]

def add_buffer_eleven(repos):
    
    repos.buffer_eleven_keys =  ['Int Short Circuit Count',
                                'Int Short Delay Count',
                                'Int Instant Count',
                                'Int High Current Count',
                                'Int Total Overload Count',
                                'Int Long Delay Count',
                                'Int Ground Fault Count',
                                'Int Total Op Count',
                                'Int Trip Op Count',
                                'Int Test Op Count',
                                'Int Opens Op Count',
                                'Int Manual Op Count',
                                'Int Time Of Last Op',
                                'Int Max Temp',
                                'Int Time Max Temp',
                                'Int Run Miniute',
                                'Int Run Hour',
                                'Int Run Day',
                                'Int Life Points']

    repos.etu_dictionary['Int Short Circuit Count'] =  [0, "Uint16"]
    repos.etu_dictionary['Int Short Delay Count']   =  [0, "Uint16"]
    repos.etu_dictionary['Int Instant Count']       =  [0, "Uint16"]
    repos.etu_dictionary['Int High Current Count']  =  [0, "Uint16"]
    repos.etu_dictionary['Int Total Overload Count']=  [0, "Uint16"]
    repos.etu_dictionary['Int Long Delay Count']    =  [0, "Uint16"]
    repos.etu_dictionary['Int Ground Fault Count']  =  [0, "Uint16"]
    repos.etu_dictionary['Int Total Op Count']      =  [0, "Uint16"]
    repos.etu_dictionary['Int Trip Op Count']       =  [0, "Uint16"]
    repos.etu_dictionary['Int Test Op Count']       =  [0, "Uint16"]
    repos.etu_dictionary['Int Opens Op Count']      =  [0, "Uint16"]
    repos.etu_dictionary['Int Manual Op Count']     =  [0, "Uint16"]
    repos.etu_dictionary['Int Time Of Last Op']     =  [0, "Uint16"]
    repos.etu_dictionary['Int Max Temp']            =  [0, "Uint16"]
    repos.etu_dictionary['Int Time Max Temp']       =  [0, "Uint16"]
    repos.etu_dictionary['Int Run Miniute']         =  [0, "Uint16"]
    repos.etu_dictionary['Int Run Hour']            =  [0, "Uint16"]
    repos.etu_dictionary['Int Run Day']             =  [0, "Uint16"]
    repos.etu_dictionary['Int Life Points']         =  [0, "Uint32"]


def add_buffer_fourty_two(repos):

    repos.buffer_fourty_two_keys = ["E Op Counter",
                                   "E Contact Wear Reset",
                                   "E Mech Wear Reset",
                                   "E TimeTemp Wear Reset",
                                   "E Contact Wear",
                                   "E Mech Wear",
                                   "E TimeTemp Wear",
                                   "E Num LP Resets",
                                   "Reserved16",
                                   "Reserved16",
                                    "Reserved16",
                                    "Reserved16",
                                    "Reserved16",
                                    "Reserved16",
                                    "Reserved16",
                                    "Reserved16",
                                    "Reserved16",
                                    "Reserved16"]


    repos.etu_dictionary["E Op Counter" ]           =  [0, "Uint16"]
    repos.etu_dictionary["E Contact Wear Reset"]    =  [0, "Uint16"]
    repos.etu_dictionary["E Mech Wear Reset"]       =  [0, "Uint16"]
    repos.etu_dictionary["E TimeTemp Wear Reset"]   =  [0, "Uint16"]
    repos.etu_dictionary["E Contact Wear"]          =  [0, "Uint16"]
    repos.etu_dictionary["E Mech Wear"]             =  [0, "Uint16"]
    repos.etu_dictionary["E TimeTemp Wear"]         =  [0, "Uint16"]
    repos.etu_dictionary["E Num LP Resets"]         =  [0, "Uint16"]        

def add_buffer_fourty_three(repos):
    
    repos.buffer_fourty_three_keys = ["I Op Counter",
                                 "I Contact Wear Reset",
                                 "I Mech Wear Reset",
                                 "I TimeTemp Wear Reset",
                                 "I Contact Wear",
                                 "I Mech Wear",
                                 "I TimeTemp Wear",
                                 "I Num LP Resets",
                                 "Reserved16",
                                 "Reserved16",
                                 "Reserved16",
                                 "Reserved16",
                                 "Reserved16",
                                 "Reserved16",
                                 "Reserved16",
                                 "Reserved16",
                                 "Reserved16",
                                 "Reserved16"]

    repos.etu_dictionary["I Op Counter" ]           =  [0, "Uint16"]
    repos.etu_dictionary["I Contact Wear Reset"]    =  [0, "Uint16"]
    repos.etu_dictionary["I Mech Wear Reset"]       =  [0, "Uint16"]
    repos.etu_dictionary["I TimeTemp Wear Reset"]   =  [0, "Uint16"]
    repos.etu_dictionary["I Contact Wear"]          =  [0, "Uint16"]
    repos.etu_dictionary["I Mech Wear"]             =  [0, "Uint16"]
    repos.etu_dictionary["I TimeTemp Wear"]         =  [0, "Uint16"]
    repos.etu_dictionary["I Num LP Resets"]         =  [0, "Uint16"]

    
def add_buffer_fourty_eight(repos):

    repos.buffer_fourty_eight_keys = ['External Ia',
                                    'External Ib',
                                    'External Ic',
                                    'External In',
                                    'External Ig',
                                    'I Average', 
                                    'External Va',
                                    'External Vb',
                                    'External Vc',
                                    'V LN_Average',
                                    'External Vab',
                                    'External Vbc',
                                    'External Vca',
                                    'V LL_Average',
                                    'External Va Two',
                                    'External Vb Two',
                                    'External Vc Two',
                                    'V LN Average Two',
                                    'External Vab Two',
                                    'External Vbc Two',
                                    'External Vca Two',
                                    'VLL Average Two',
                                    'Freq',
                                    'Freq Two',
                                    'Real Power',
                                    'React Power',
                                    'App Power',
                                    'PF',
                                    'Temp',
                                    'Humidity',
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
    repos.etu_dictionary['External Vca']      = [0, "Float"]
    repos.etu_dictionary["I Average"]         =  [0,"Float"]
    repos.etu_dictionary["V LN Average"]      =  [0,"Float"]
    repos.etu_dictionary["External Vab Two"]  =  [0,"Float"]
    repos.etu_dictionary["External Vbc Two"]  =  [0,"Float"]
    repos.etu_dictionary["External Vca Two"]  =  [0,"Float"]
    repos.etu_dictionary["V LL_ verage"]      =  [0,"Float"]
    repos.etu_dictionary["VLL Average Two"]   =  [0,"Float"]
    repos.etu_dictionary["Freq Two"]          =  [0,"Float"]
    repos.etu_dictionary['External Va Two']   =  [0,"Float"]
    repos.etu_dictionary['External Vb Two']   =  [0,"Float"]
    repos.etu_dictionary['External Vc Two']   =  [0,"Float"]
    repos.etu_dictionary['V LN Average Two']  =  [0,"Float"]
    repos.etu_dictionary['Freq']              = [0, "Float"]
    repos.etu_dictionary['Real Power']        = [0, "Float"]
    repos.etu_dictionary['React Power']       = [0, "Float"]
    repos.etu_dictionary['App Power']         = [0, "Float"]
    repos.etu_dictionary['PF']                = [0, "Float"]
    repos.etu_dictionary['Temp']              = [0, "Float"]
    repos.etu_dictionary['Humidity']          = [0, "Float"]
    repos.etu_dictionary['Batt Val']          = [0, "Float"]


def add_buffer_fourty_nine(repos):

    repos.buffer_fourty_nine_keys = ['Forward Energy',
                                     'Reverse Energy',
                                     'Total Energy',
                                     'Net Energy',
                                     'Leading Reactive Energy',
                                     'Lagging Reactive Energy',
                                     'Total Reactive Energy',
                                     'Net Reactive Energy',
                                     'Apparent Energy',
                                     'Last Energy Reset Time']
    
    repos.etu_dictionary['Forward Energy']          = [0, "Uint64"]
    repos.etu_dictionary['Reverse Energy']          = [0, "Uint64"]
    repos.etu_dictionary['Total Energy']            = [0, "int64"]
    repos.etu_dictionary['Net Energy']              = [0, "int64"]
    repos.etu_dictionary['Leading Reactive Energy'] = [0, "Uint64"]
    repos.etu_dictionary['Lagging Reactive Energy'] = [0, "Uint64"]
    repos.etu_dictionary['Total Reactive Energy']   = [0, "int64"]
    repos.etu_dictionary['Net Reactive Energy']     = [0, "int64"]
    repos.etu_dictionary['Apparent Energy']         = [0, "Uint64"]
    repos.etu_dictionary['Last Energy Reset Time']  = [0, "Date"]
    
def add_buffer_fifty(repos):

    repos.buffer_fifty_keys =   ['RTD PD Window',
                                 'RTD PD Interval',
                                 'Last PD Reset TS',
                                 'Real Power Demand',
                                 'Reactive Power Demand',
                                 'Apparent Power Demand',
                                 'Max Real Power Demand',
                                 'Max Real Power Demand TS',
                                 'Max Reactive Power Demand',
                                 'Max Reactive Power Demand TS',
                                 'Max Apparent Power Demand',
                                 'Max Apparent Power Demand TS',
                                 'Demand Window Status',
                                 'Demand Window Time']
                                 
                                 
                                 
        
    repos.etu_dictionary['RTD PD Window']                   = [0, "Uint08"]    
    repos.etu_dictionary['RTD PD Interval']                 = [0, "Uint08"] #Real Time Data Power Demand Interval
    repos.etu_dictionary['Last PD Reset TS']                = [0, "Date"]
    repos.etu_dictionary['Real Power Demand']               = [0, "Float"]
    repos.etu_dictionary['Reactive Power Demand']           = [0, "Float"]
    repos.etu_dictionary['Apparent Power Demand']           = [0, "Float"]
    repos.etu_dictionary['Max Real Power Demand']           = [0, "Float"]
    repos.etu_dictionary['Max Real Power Demand TS']        = [0, "Date"],
    repos.etu_dictionary['Max Reactive Power Demand']       = [0, "Float"]
    repos.etu_dictionary['Max Reactive Power Demand TS']    = [0, "Date"]
    repos.etu_dictionary['Max Apparent Power Demand']       = [0, "Float"]
    repos.etu_dictionary['Max Apparent Power Demand TS']    = [0, "Date"]
    repos.etu_dictionary['Demand Window Status']            = [0, "Uint16"]
    repos.etu_dictionary['Demand Window Time']              = [0, "Uint16"]


def add_buffer_fifty_one(repos):

    repos.buffer_fifty_keys =   ['Real Power A',
                                 'Real Power B',
                                 'Real Power C',
                                 'Real Power Total',
                                 'Reactive Power A',
                                 'Reactive Power B',
                                 'Reactive Power C',
                                 'Reactive Power Total',
                                 'Apparent Power A',
                                 'Apparent Power B',
                                 'Apparent Power C',
                                 'Apparent Power Total']
                                 
 
    repos.etu_dictionary['Real Power A']         = [0, "Float"] 
    repos.etu_dictionary['Real Power B']         = [0, "Float"]
    repos.etu_dictionary['Real Power C']         = [0, "Float"]
    repos.etu_dictionary['Real Power Total']     = [0, "Float"]
    repos.etu_dictionary['Reactive Power A']     = [0, "Float"]
    repos.etu_dictionary['Reactive Power B']     = [0, "Float"]
    repos.etu_dictionary['Reactive Power C']     = [0, "Float"]
    repos.etu_dictionary['Reactive Power Total'] = [0, "Float"]
    repos.etu_dictionary['Apparent Power A']     = [0, "Float"]
    repos.etu_dictionary['Apparent Power B']     = [0, "Float"]
    repos.etu_dictionary['Apparent Power C']     = [0, "Float"]
    repos.etu_dictionary['Apparent Power Total'] = [0, "Float"]

    
def add_buffer_fifty_two(repos):
    
    repos.buffer_fifty_two_keys = ['Max IA',
                                   'Max IA TS',
                                   'Max IB',
                                   'Max IB TS',
                                   'Max IC',
                                   'Max IC TS',
                                   'Max IN',
                                   'Max IN TS',
                                   'Max IG',
                                   'Max IG TS',
                                   'Min IA',
                                   'Min IA TS',
                                   'Min IB',
                                   'Min IB TS',
                                   'Min IC',
                                   'Min IC TS',
                                   'Min IN',
                                   'Min IN TS',
                                   'Min IG',
                                   'Min IG TS',
                                   'Last I Max-Min Reset TS']
    
    repos.etu_dictionary['Max IA']              = [0, "Q4"]
    repos.etu_dictionary['Max IA TS']           = [0, "Date"]
    repos.etu_dictionary['Max IB']              = [0, "Q4"]
    repos.etu_dictionary['Max IB TS']           = [0, "Date"]
    repos.etu_dictionary['Max IC']              = [0, "Q4"]
    repos.etu_dictionary['Max IC TS']           = [0, "Date"]   
    repos.etu_dictionary['Max IN']              = [0, "Q4"]
    repos.etu_dictionary['Max IN TS']           = [0, "Date"]
    repos.etu_dictionary['Max IG']              = [0, "Q4"]
    repos.etu_dictionary['Max IG TS']           = [0, "Date"]      
    repos.etu_dictionary['Min IA']              = [0, "Q4"]
    repos.etu_dictionary['Min IA TS']           = [0, "Date"]
    repos.etu_dictionary['Min IB']              = [0, "Q4"]
    repos.etu_dictionary['Min IB TS']           = [0, "Date"]
    repos.etu_dictionary['Min IC']              = [0, "Q4"]
    repos.etu_dictionary['Min IC TS']           = [0, "Date"]
    repos.etu_dictionary['Min IN']              = [0, "Q4"]
    repos.etu_dictionary['Min IN TS']           = [0, "Date"]
    repos.etu_dictionary['Min IG']              = [0, "Q4"]
    repos.etu_dictionary['Min IG TS']           = [0, "Date"]
    repos.etu_dictionary['Last I Max-Min Reset TS']                = [0, "Date"]



     
def add_buffer_fifty_three(repos):

     repos.buffer_fifty_three = ['Max Vab1',
                                'Max Vab1 TS',
                                'Max Vbc1',
                                'Max Vbc1 TS',
                                'Max Vca1',
                                'Max Vca1 TS',
                                'Min Vab1',
                                'Min Vab1 TS',
                                'Min Vbc1',
                                'Min Vbc1 TS',
                                'Min Vca1',
                                'Min Vca1 TS',
                                'Max Vab2',
                                'Max Vab2 TS',
                                'Max Vbc2',
                                'Max Vbc2 TS',
                                'Max Vca2',
                                'Max Vca2 TS',
                                'Min Vab2',
                                'Min Vab2 TS',
                                'Min Vbc2',
                                'Min Vbc2 TS',
                                'Min Vca2',
                                'Min Vca2 TS']
     
     repos.etu_dictionary['Max Vab1']                 = [0, "Q4Padded"]
     repos.etu_dictionary['Max Vab1 TS']              = [0, "Date"]
     repos.etu_dictionary['Max Vbc1']                 = [0, "Q4Padded"]
     repos.etu_dictionary['Max Vbc1 TS']              = [0, "Date"]
     repos.etu_dictionary['Max Vca1']                 = [0, "Q4Padded"]
     repos.etu_dictionary['Max Vca1 TS']              = [0, "Date"]
     repos.etu_dictionary['Min Vab1']                 = [0, "Q4Padded"]
     repos.etu_dictionary['Min Vab1 TS']              = [0, "Date"]
     repos.etu_dictionary['Min Vbc1']                 = [0, "Q4Padded"]
     repos.etu_dictionary['Min Vbc1 TS']              = [0, "Date"]
     repos.etu_dictionary['Min Vca1']                 = [0, "Q4Padded"]
     repos.etu_dictionary['Min Vca1 TS']              = [0, "Date"]
     repos.etu_dictionary['Max Vab2']                 = [0, "Q4Padded"]
     repos.etu_dictionary['Max Vab2 TS']              = [0, "Date"]
     repos.etu_dictionary['Max Vbc2']                 = [0, "Q4Padded"]
     repos.etu_dictionary['Max Vbc2 TS']              = [0, "Date"]
     repos.etu_dictionary['Max Vca2']                 = [0, "Q4Padded"]
     repos.etu_dictionary['Max Vca2 TS']              = [0, "Date"]
     repos.etu_dictionary['Min Vab2']                 = [0, "Q4Padded"]
     repos.etu_dictionary['Min Vab2 TS']              = [0, "Date"]
     repos.etu_dictionary['Min Vbc2']                 = [0, "Q4Padded"]
     repos.etu_dictionary['Min Vbc2 TS']              = [0, "Date"]
     repos.etu_dictionary['Min Vca2']                 = [0, "Q4Padded"]
     repos.etu_dictionary['Min Vca2 TS']              = [0, "Date"]
     

def add_buffer_fifty_four(repos):

     repos.buffer_fifty_four = ['Max Van1',
                                'Max Van1 TS',
                                'Max Vbn1',
                                'Max Vbn1 TS',
                                'Max Vcn1',
                                'Max Vcn1 TS',
                                'Min Van1',
                                'Min Van1 TS',
                                'Min Vbn1',
                                'Min Vbn1 TS',
                                'Min Vcn1',
                                'Min Vcn1 TS',
                                'Max Van2',
                                'Max Van2 TS',
                                'Max Vbn2',
                                'Max Vbn2 TS',
                                'Max Vcn2',
                                'Max Vcn2 TS',
                                'Min Van2',
                                'Min Van2 TS',
                                'Min Vbn2',
                                'Min Vbn2 TS',
                                'Min Vcn2',
                                'Min Vcn2 TS']
     
     repos.etu_dictionary['Max Van1']                 = [0, "Float"]
     repos.etu_dictionary['Max Van1 TS']              = [0, "Date"]
     repos.etu_dictionary['Max Vbn1']                 = [0, "Float"]
     repos.etu_dictionary['Max Vbn1 TS']              = [0, "Date"]
     repos.etu_dictionary['Max Vcn1']                 = [0, "Float"]
     repos.etu_dictionary['Max Vcn1 TS']              = [0, "Date"]
     repos.etu_dictionary['Min Van1']                 = [0, "Float"]
     repos.etu_dictionary['Min Van1 TS']              = [0, "Date"]
     repos.etu_dictionary['Min Vbn1']                 = [0, "Float"]
     repos.etu_dictionary['Min Vbn1 TS']              = [0, "Date"]
     repos.etu_dictionary['Min Vcn1']                 = [0, "Float"]
     repos.etu_dictionary['Min Vcn1 TS']              = [0, "Date"]
     repos.etu_dictionary['Max Van2']                 = [0, "Float"]
     repos.etu_dictionary['Max Van2 TS']              = [0, "Date"]
     repos.etu_dictionary['Max Vbn2']                 = [0, "Float"]
     repos.etu_dictionary['Max Vbn2 TS']              = [0, "Date"]
     repos.etu_dictionary['Max Vcn2']                 = [0, "Float"]
     repos.etu_dictionary['Max Vcn2 TS']              = [0, "Date"]
     repos.etu_dictionary['Min Van2']                 = [0, "Float"]
     repos.etu_dictionary['Min Van2 TS']              = [0, "Date"]
     repos.etu_dictionary['Min Vbn2']                 = [0, "Float"]
     repos.etu_dictionary['Min Vbn2 TS']              = [0, "Date"]
     repos.etu_dictionary['Min Vcn2']                 = [0, "Float"]
     repos.etu_dictionary['Min Vcn2 TS']              = [0, "Date"]
     
def add_buffer_fifty_five(repos):

    
    repos.buffer_fifty_five_keys = ['Internal Ia',
                                    'Internal Ib',
                                    'Internal Ic',
                                    'Internal In',
                                    'Internal Ig']

    repos.etu_dictionary['Internal Ia'] = [0, "Float"] #Q4 For PXR25
    repos.etu_dictionary['Internal Ib'] = [0, "Float"]
    repos.etu_dictionary['Internal Ic'] = [0, "Float"]
    repos.etu_dictionary['Internal In'] = [0, "Float"]
    repos.etu_dictionary['Internal Ig'] = [0, "Float"]

def add_buffer_sixty_nine(repos):

    repos.buffer_sixty_nine_keys = ['IA Unbalance Max',
                                    'IA Unbalance Max TS',
                                    'IB Unbalance Max',
                                    'IB Unbalance Max TS',
                                    'IC Unbalance Max',
                                    'IC Unbalance Max TS',
                                    'IAll Unbalance Max',
                                    'IAll Unbalance Max TS',
                                    'VAllN Unbalance Max',
                                    'VAllN Unbalance Max TS',
                                    'VAN Unbalance Max',
                                    'VAN Unbalance Max TS',
                                    'VBN Unbalance Max',
                                    'VBN Unbalance Max TS',
                                    'VCN Unbalance Max',
                                    'VCN Unbalance Max TS',
                                    'VAll LL Unbalance Max',
                                    'VAll LL Unbalance Max TS',
                                    'VAB Unbalance Max',
                                    'VAB Unbalance Max TS',
                                    'VBC Unbalance Max',
                                    'VBC Unbalance Max TS',
                                    'VCA Unbalance Max',
                                    'VCA Unbalance Max TS',
                                    'I Total Unbalance Max',
                                    'I Total Unbalance Max TS',
                                    'V Total Unbalance Max',
                                    'V Total Unbalance Max TS']

    
    repos.etu_dictionary['IA Unbalance Max']       = [0, "Float"]
    repos.etu_dictionary['IA Unbalance Max TS']    = [0, "Date"]
    repos.etu_dictionary['IB Unbalance Max']       = [0, "Float"]
    repos.etu_dictionary['IB Unbalance Max TS']    = [0, "Date"]
    repos.etu_dictionary['IC Unbalance Max']       = [0, "Float"]
    repos.etu_dictionary['IC Unbalance Max TS']    = [0, "Date"]
    repos.etu_dictionary['IAll Unbalance Max']     = [0, "Float"]
    repos.etu_dictionary['IAll Unbalance Max TS']  = [0, "Date"]
    repos.etu_dictionary['VAllN Unbalance Max']    = [0, "Float"]
    repos.etu_dictionary['VAllN Unbalance Max TS'] = [0, "Date"]
    repos.etu_dictionary['VAN Unbalance Max']      = [0, "Float"]
    repos.etu_dictionary['VAN Unbalance Max TS']   = [0, "Date"]
    repos.etu_dictionary['VBN Unbalance Max']      = [0, "Float"]
    repos.etu_dictionary['VBN Unbalance Max TS']   = [0, "Date"]
    repos.etu_dictionary['VCN Unbalance Max']      = [0, "Float"]
    repos.etu_dictionary['VCN Unbalance Max TS']   = [0, "Date"]
    repos.etu_dictionary['VAll LL Unbalance Max']    = [0, "Float"]
    repos.etu_dictionary['VAll LL Unbalance Max TS'] = [0, "Date"]
    repos.etu_dictionary['VAB Unbalance Max']        = [0, "Float"]
    repos.etu_dictionary['VAB Unbalance Max TS']     = [0, "Date"]
    repos.etu_dictionary['VBC Unbalance Max']        = [0, "Float"]
    repos.etu_dictionary['VBC Unbalance Max TS']     = [0, "Date"]
    repos.etu_dictionary['VCA Unbalance Max']        = [0, "Float"]
    repos.etu_dictionary['VCA Unbalance Max TS']     = [0, "Date"]
    repos.etu_dictionary['I Total Unbalance Max']    = [0, "Float"]
    repos.etu_dictionary['I Total Unbalance Max TS'] = [0, "Date"]
    repos.etu_dictionary['V Total Unbalance Max']    = [0, "Float"]
    repos.etu_dictionary['V Total Unbalance Max TS'] = [0, "Date"]

def add_buffer_seventy(repos):

    repos.crest_seventy_keys = ['Ia Current Crest Factor',
                                'Ib Current Crest Factor',
                                'Ic Current Crest Factor',
                                'In Current Crest Factor']
    
    repos.etu_dictionary['Ia Current Crest Factor']=[0, "Q9"]
    repos.etu_dictionary['Ib Current Crest Factor']=[0, "Q9"]
    repos.etu_dictionary['Ic Current Crest Factor']=[0, "Q9"]
    repos.etu_dictionary['In Current Crest Factor']=[0, "Q9"]
        
def add_buffer_seventy_one(repos):

    repos.buffer_seventy_one_keys = ["Min Apparent PF",
                                      "Min Apparent PF TS",
                                      "Max Apparent PF",
                                      "Max Apaprent PF TS",
                                      "Min Disp PF",
                                      "Min Disp PF TS",
                                      "Max Disp PF",
                                      "Max Disp PF TS",
                                      "Min Apparent A PF",
                                      "Min Apparent A PF TS",
                                      "Max Apparent A  PF",
                                      "Max Apaprent A PF TS",
                                      "Min Apparent B PF",
                                      "Min Apparent B PF TS",
                                      "Max Apparent B  PF",
                                      "Max Apaprent B PF TS",
                                      "Min Apparent C PF",
                                      "Min Apparent C PF TS",
                                      "Max Apparent C  PF",
                                      "Max Apaprent C PF TS",
                                      "Min Disp A PF",
                                      "Min Disp A PF TS",
                                      "Max Disp A PF",
                                      "Max Disp A PF TS",
                                      "Min Disp B PF",
                                      "Min Disp B PF TS",
                                      "Max Disp B PF",
                                      "Max Disp B PF TS",
                                      "Min Disp C PF",
                                      "Min Disp C PF TS",
                                      "Max Disp C PF",
                                      "Max Disp C PF TS",
                                      "Min Apparent Total PF",
                                      "Min Apparent Total PF TS",
                                      "Max Apparent Total  PF",
                                      "Max Apaprent Total PF TS",
                                      "Min Disp Total PF TS",
                                      "Min Disp Total PF",
                                      "Max Disp Total PF",
                                      "Max Disp Total PF TS"]

                                      
    repos.etu_dictionary["Min Apparent PF"]    = [0, "Float"]
    repos.etu_dictionary["Min Apparent PF TS"] = [0, "Date"]
    repos.etu_dictionary["Max Apparent PF"]    = [0, "Float"]
    repos.etu_dictionary["Max Apaprent PF TS"] = [0, "Date"]
    repos.etu_dictionary["Min Disp PF"]    = [0, "Float"]
    repos.etu_dictionary["Min Disp PF TS"] = [0, "Date"]
    repos.etu_dictionary["Max Disp PF"]    = [0, "Float"]
    repos.etu_dictionary["Max Disp PF TS"]    = [0, "Date"]
    repos.etu_dictionary["Min Apparent A PF"]    = [0, "Float"]
    repos.etu_dictionary["Min Apparent A PF TS"] = [0, "Date"]
    repos.etu_dictionary["Max Apparent A PF"]    = [0, "Float"]
    repos.etu_dictionary["Max Apaprent A PF TS"] = [0, "Date"]                                      
    repos.etu_dictionary["Min Apparent B PF"]    = [0, "Float"]
    repos.etu_dictionary["Min Apparent B PF TS"] = [0, "Date"]
    repos.etu_dictionary["Max Apparent B PF"]    = [0, "Float"]
    repos.etu_dictionary["Max Apaprent B PF TS"] = [0, "Date"]
    repos.etu_dictionary["Min Apparent C PF"]    = [0, "Float"]
    repos.etu_dictionary["Min Apparent C PF TS"] = [0, "Date"]
    repos.etu_dictionary["Max Apparent C PF"]    = [0, "Float"]
    repos.etu_dictionary["Max Apaprent C PF TS"] = [0, "Date"]
    repos.etu_dictionary["Min Disp A PF"]    = [0, "Float"]
    repos.etu_dictionary["Min Disp A PF TS"] = [0, "Date"]
    repos.etu_dictionary["Max Disp A PF"]    = [0, "Float"]
    repos.etu_dictionary["Max Disp A PF TS"]    = [0, "Date"]
    repos.etu_dictionary["Min Disp B PF"]    = [0, "Float"]
    repos.etu_dictionary["Min Disp B PF TS"] = [0, "Date"]
    repos.etu_dictionary["Max Disp B PF"]    = [0, "Float"]
    repos.etu_dictionary["Max Disp B PF TS"]    = [0, "Date"]
    repos.etu_dictionary["Min Disp C PF"]    = [0, "Float"]
    repos.etu_dictionary["Min Disp C PF TS"] = [0, "Date"]
    repos.etu_dictionary["Max Disp C PF"]    = [0, "Float"]
    repos.etu_dictionary["Max Disp C PF TS"]    = [0, "Date"]
    repos.etu_dictionary["Min Apparent Total PF"]    = [0, "Float"]
    repos.etu_dictionary["Min Apparent Total PF TS"] = [0, "Date"]
    repos.etu_dictionary["Max Apparent Total PF"]    = [0, "Float"]
    repos.etu_dictionary["Max Apaprent Total PF TS"] = [0, "Date"]
    repos.etu_dictionary["Min Disp Total PF"]    = [0, "Float"]
    repos.etu_dictionary["Min Disp Total PF TS"] = [0, "Date"]
    repos.etu_dictionary["Max Disp Total PF"]    = [0, "Float"]
    repos.etu_dictionary["Max Disp Total PF TS"]    = [0, "Date"]
    
    
def add_bufer_seventy_four(repos):

    repos.buffer_seventy_four_keys = ["Min Real Power A",
                                      "Min Real Power A TS",
                                      "Max Real Power A",
                                      "Max Real Power A TS",
                                      "Min Real Power B",
                                      "Min Real Power B TS",
                                      "Max Real Power B",
                                      "Max Real Power B TS",
                                      "Min Real Power C",
                                      "Min Real Power C TS",
                                      "Max Real Power C",
                                      "Max Real Power C TS"]
                                      
    repos.etu_dictionary["Min Real Power A"]    = [0, "Float"]
    repos.etu_dictionary["Min Real Power A TS"] = [0, "Date"]
    repos.etu_dictionary["Max Real Power A"]    = [0, "Float"]
    repos.etu_dictionary["Max Real Power A TS"] = [0, "Date"]
    repos.etu_dictionary["Min Real Power B"]    = [0, "Float"]
    repos.etu_dictionary["Min Real Power B TS"] = [0, "Date"]
    repos.etu_dictionary["Max Real Power B"]    = [0, "Float"]
    repos.etu_dictionary["Max Real Power C TS"] = [0, "Date"]
    repos.etu_dictionary["Min Real Power C"]    = [0, "Float"]
    repos.etu_dictionary["Min Real Power C TS"] = [0, "Date"]
    repos.etu_dictionary["Max Real Power C"]    = [0, "Float"]
    repos.etu_dictionary["Max Real Power C TS"] = [0, "Date"]
    
def add_buffer_seventy_seven(repos):


    repos.buffer_seventy_seven_keys = ['RTD Demand Window Type',
                                       'RTD Window Interval',
                                       'Demand Reset TS',
                                       'Ia Demand',
                                       'Ib Demand',
                                       'Ic Demand',
                                       'In Demand',
                                       'Max Ia Demand',
                                       'Max Ia Demand TS',
                                       'Max Ib Demand',
                                       'Max Ib Demand TS',
                                       'Max Ic Demand',
                                       'Max Ic Demand TS',
                                       'Max In Demand',
                                       'Max In Demand TS',
                                       'Min Ia Demand',
                                       'Min Ia Demand TS',
                                       'Min Ib Demand',
                                       'Min Ib Demand TS',
                                       'Min Ic Demand',
                                       'Min Ic Demand TS',
                                       'Min In Demand',
                                       'Min In Demand TS',
                                       'Window Status',
                                       'Measurment Time'] 

    repos.etu_dictionary['RTD Demand Window Type'] = [0, "Uint08"]
    repos.etu_dictionary['RTD Window Interval'] = [0, "Uint08"]
    repos.etu_dictionary['Demand Reset TS'] = [0, "Date"]
    repos.etu_dictionary['Ia Demand'] = [0, "Float"]
    repos.etu_dictionary['Ib Demand'] = [0, "Float"]
    repos.etu_dictionary['Ic Demand'] = [0, "Float"]
    repos.etu_dictionary['In Demand'] = [0, "Float"]
    repos.etu_dictionary['Max Ia Demand'] = [0, "Float"]
    repos.etu_dictionary['Max Ia Demand TS'] = [0, "Date"]
    repos.etu_dictionary['Max Ib Demand'] = [0, "Float"]
    repos.etu_dictionary['Max Ib Demand TS'] = [0, "Date"]
    repos.etu_dictionary['Max Ic Demand'] = [0, "Float"]
    repos.etu_dictionary['Max Ic Demand TS'] = [0, "Date"]
    repos.etu_dictionary['Max In Demand'] = [0, "Float"]
    repos.etu_dictionary['Max In Demand TS'] = [0, "Date"]
    repos.etu_dictionary['Min Ia Demand'] = [0, "Float"]
    repos.etu_dictionary['Min Ia Demand TS'] = [0, "Date"]
    repos.etu_dictionary['Min Ib Demand'] = [0, "Float"]
    repos.etu_dictionary['Min Ib Demand TS'] = [0, "Date"]
    repos.etu_dictionary['Min Ic Demand'] = [0, "Float"]
    repos.etu_dictionary['Min Ic Demand TS'] = [0, "Date"]
    repos.etu_dictionary['Min In Demand'] = [0, "Float"]
    repos.etu_dictionary['Min In Demand TS'] = [0, "Date"]                                               
    repos.etu_dictionary['Window Status'] = [0, "Uint16"]
    repos.etu_dictionary['Measurment Time'] = [0, "Uint16"]


def add_buffer_seventy_nine(repos):

    repos.buffer_seventy_nine_keys = ["THD Van",
                                      "THD Vbn",
                                      "THD Vcn",
                                      "THD Vab",
                                      "THD Vbc",
                                      "THD Vca",
                                      "THD Ia",
                                      "THD Ib",
                                      "THD Ic",
                                      "THD In"]

    
    repos.etu_dictionary["THD Van"]   = [0,"Uint32"]
    repos.etu_dictionary["THD Vbn"]   = [0,"Uint32"]
    repos.etu_dictionary["THD Vcn"]   = [0,"Uint32"]
    repos.etu_dictionary["THD Vab"]   = [0,"Uint32"]
    repos.etu_dictionary["THD Vbc"]   = [0,"Uint32"]
    repos.etu_dictionary["THD Vca"]   = [0,"Uint32"]
    repos.etu_dictionary["THD Ia"]    = [0,"Uint32"]
    repos.etu_dictionary["THD Ib"]    = [0,"Uint32"]
    repos.etu_dictionary["THD Ic"]    = [0,"Uint32"]
    repos.etu_dictionary["THD In"]    = [0,"Uint32"]

def add_buffer_eighty(repos):


    repos.buffer_eighty_keys = ['Current Unbalance',
                                'Voltage Unbalance',
                                'Current Unbalance A',
                                'Current Unbalance B',
                                'Current Unbalance C',
                                'Current Unbalance Max',
                                'Voltage Unbalance AN',
                                'Voltage Unbalance BN',
                                'Voltage Unbalance CN',
                                'Voltage Unbalance N Max',
                                'Voltage Unbalance AB',
                                'Voltage Unbalance BC',
                                'Voltage Unbalance CA',
                                'Voltage Unbalance LL Max']

        
                            #'Current Unbalance':[0,"Q9"], #PXR25?
                            #'Voltage Unbalance':[0, "Q9"],
    repos.etu_dictionary['Current Unbalance']        = [0,"Float"]
    repos.etu_dictionary['Voltage Unbalance']        = [0,"Float"]
    repos.etu_dictionary['Current Unbalance A']      = [0,"Float"]
    repos.etu_dictionary['Current Unbalance B']      = [0,"Float"]
    repos.etu_dictionary['Current Unbalance C']      = [0,"Float"]
    repos.etu_dictionary['Current Unbalance N']      = [0,"Float"]
    repos.etu_dictionary['Current Unbalance Max']    = [0,"Float"]
    repos.etu_dictionary['Voltage Unbalance AN']     = [0,"Float"]
    repos.etu_dictionary['Voltage Unbalance BN']     = [0,"Float"]
    repos.etu_dictionary['Voltage Unbalance CN']     = [0,"Float"]
    repos.etu_dictionary['Voltage Unbalance N Max']  = [0,"Float"]
    repos.etu_dictionary['Voltage Unbalance AB']     = [0,"Float"]
    repos.etu_dictionary['Voltage Unbalance BC']     = [0,"Float"]
    repos.etu_dictionary['Voltage Unbalance CA']     = [0,"Float"]
    repos.etu_dictionary['Voltage Unbalance LL Max'] = [0,"Float"]
    
def add_firmware(repos):

   repos.firmware_keys = ['MCU1 Version',
                                'MCU1 Revision',
                                'MCU1 Debugger',
                                'MCU Version',
                                'MCU2 Revision',
                                'MCU2 Debugger',
                                'MCU Com Ver',
                                'MCU Com Rev',
                                'MCU Com Debug',
                                'USB PC Tool Ver',
                                'USB PC Tool Rev',
                                'MCU2 Flash Firmware Version',
                                'MCU2 Flash Firmware Revision',
                                'MCU2 Flash Firmware Debugger']
   repos.etu_dictionary['MCU1 Version']                    = [0, "Uint16"]
   repos.etu_dictionary['MCU1 Revision']                   = [0, "Uint16"]
   repos.etu_dictionary['MCU1 Debugger']                   = [0, "Uint16"]
   repos.etu_dictionary['MCU2 Version']                    = [0, "Uint08"]
   repos.etu_dictionary['MCU2 Revision']                   = [0, "Uint08"]
   repos.etu_dictionary['MCU2 Debugger']                   = [0, "Uint16"]
   repos.etu_dictionary['MCU Com Ver']                     = [0, "Uint08"]
   repos.etu_dictionary['MCU Com Rev']                     = [0, "Uint08"]
   repos.etu_dictionary['MCU Com Debug']                   = [0, "Uint16"]
   repos.etu_dictionary['USB PC Tool Ver']                 = [0, "Uint16"]
   repos.etu_dictionary['USB PC Tool Rev']                 = [0, "Uint16"]
   repos.etu_dictionary['MCU2 Flash Firmware Version']     = [0, "Uint16"]
   repos.etu_dictionary['MCU2 Flash Firmware Revision']    = [0, "Uint16"]
   repos.etu_dictionary['MCU2 Flash Firmware Debugger']    = [0, "Uint16"]
    
def add_configuration(repos):

    repos.configuration_keys =      ["Poles",
                                    "Standard",
                                    "Device Type",
                                    "DC Rating",
                                    "Config Voltage",
                                    "Max IEC Amps",
                                    "Max UL Amps",
                                    "Max ANSI/UL Amps",
                                    "Purchased",
                                    "Min In",
                                    "Withstand", 
                                    "Override",
                                    "MCR",
                                    "Config Ground",
                                    "Max Interrupt Label",
                                    "Label Interrupt",
                                    "Config Inst"]

    add_dictionary_values(repos, repos.configuration_keys)
    repos.etu_dictionary["Override"][0] = 36
    

    
def get_dictionary(repos):


    repos.etu_dictionary =  {'time_reset'              : [0, "Date"],
                            'date_raw_op'             :  [0, "Date"],
                            'date_raw_temp'           :  [0, "Date"],                   
                            'Setpoints Group Sensor'  :  [0,"Uint16"],
                            'Active Setpoints Group'  :  [0,"Uint16"],
                            'ScondPT/VDB Module Present'      :  [0,"Uint16"],
                            'Phase Labeling'                  :  [0,"Uint16"],
                            'Trip Waveform Capture Precycles' :  [0,"Uint16"],
                            'Extended Capture Triggers'       :  [0,"Uint16"],
                            'IEC61860 Configuration'          :  [0,"Uint16"],
                            'Demand Logging Interval'         :  [0,"Uint16"],
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
                            'Alarm Waveform Capture Precycles'  : [0,"Uint16"],
                            'Demand Mode Precision' : [16, "Uint16"]
                            } #Double Check Data Type


    repos.etu_dictionary['date_raw_op']             =  [0, "Date"]
    repos.etu_dictionary['date_raw_temp']           =  [0, "Date"]
    repos.etu_dictionary['MCU1 Version']            =  [0, "Date"]
    
    add_setpoint_group_zero(repos)
    add_setpoint_group_one(repos)
    add_setpoint_group_two(repos)
    add_setpoint_group_three(repos)
    add_setpoint_group_four(repos)
    add_setpoint_group_five(repos)
    add_setpoint_group_six(repos)
    add_setpoint_group_seven(repos)
    add_setpoint_group_eight(repos)
    add_setpoint_group_nine(repos)
    add_setpoint_group_ten(repos)
    add_setpoint_group_eleven(repos)
    add_buffer_zero(repos)
    add_buffer_six(repos)
    add_buffer_eleven(repos)
    add_buffer_fourty_two(repos)
    add_buffer_fourty_three(repos)
    add_buffer_fourty_eight(repos)
    add_buffer_fourty_nine(repos)
    add_buffer_fifty(repos)
    add_buffer_fifty_two(repos)
    add_buffer_fifty_five(repos)
    add_buffer_sixty_nine(repos)
    add_buffer_seventy(repos)
    add_buffer_seventy_one(repos)
    add_bufer_seventy_four(repos)
    add_buffer_seventy_seven(repos)
    add_configuration(repos)



def get_setpoint_keys(repos):

    repos.mech_time = .019

    repos.breaker_protection_capacity_keys = ['frame_ap',
                                        'poles',
                                        'standard', 
                                        'ct_version', 
                                        'Withstand',
                                        'MCR',              
                                        'max_interupt_label', 
                                        'frame_construction']
                                 

    
    repos.angle_keys          =   ["Ra_Phase_Angle",
                                    "Rb_Phase_Angle",
                                    "Rc_Phase_Angle",
                                    "Ia_Phase_Angle",
                                    "Ib_Phase_Angle",
                                    "Ic_Phase_Angle",
                                    "Va_Phase_Angle",
                                    "Vb_Phase_Angle",
                                    "Vc_Phase_Angle"]
    
def get_buffer_keys(repos):

   
    repos.buffer_one_keys = ['External Ia',
                                    'External Ib',
                                    'External Ic',
                                    'External In',
                                    'External Ig',
                                    'I Average', 
                                    'External Va',
                                    'External Vb',
                                    'External Vc',
                                    'V LN_Average',
                                    'External Vab',
                                    'External Vbc',
                                    'External Vca',
                                    'V LL_Average',
                                    'External Va Two',
                                    'External Vb Two',
                                    'External Vc Two',
                                    'V LN Average Two',
                                    'External Vab Two',
                                    'External Vbc Two',
                                    'External Vca Two',
                                    'VLL Average Two',
                                    'Freq',
                                    'Freq Two',
                                    'Real Power',
                                    'React Power',
                                    'App Power',
                                    'PF',
                                    'Temp',
                                    'Humidity',
                                    'Batt Val']
            
    repos.buffer_two_keys = ['Forward Energy',
                            'Reverse Energy',
                            'Total Energy',
                            'Net Energy',
                            'Leading Reactive Energy',
                            'Lagging Reactive Energy',
                            'Total Reactive Energy',
                            'Net Reactive Energy',
                            'Apparent Energy',
                            'Last Energy Reset Time']

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

    repos.buffer_ten_keys = ['internal_Ia',
                           'internal_Ib',
                           'internal_Ic',
                           'internal_In',
                           'internal_Ig']

            
    repos.buffer_eleven_keys =  ['int_short_circuit_count',
                            'int_short_delay_count',
                            'int_instant_count',
                            'int_high_current_count',
                            'int_total_overload_count',
                            'int_long_delay_count',
                            'int_ground_fault_count',
                            'int_total_op_count',
                            'int_trip_op_count',
                            'int_test_op_count',
                            'int_opens_op_count',
                            'int_manual_op_count',
                            'int_time_of_last_op',
                            'int_max_temp',
                            'int_time_max_temp',
                            'int_run_miniute',
                            'int_run_hour',
                            'int_run_day',
                            'int_life_points']
    


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
                                 "ARMS Actice State",
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

    repos.buffer_fourteen_keys = ["THD Van",
                                  "THD Vbn",
                                  "THD Vcn",
                                  "THD Vab",
                                  "THD Vbc",
                                  "THD Vca",
                                  "THD Ia",
                                  "THD Ib",
                                  "THD Ic",
                                  "THD In"] 

    repos.buffer_fifteen_keys = ['Current Unbalance',
                                 'Voltage Unbalance']

    repos.pf_and_freq_keys    = ['Max Power Factor',
                                 'Time of Max Power Factor',
                                 'Min Power Factor',
                                 'Time Of Min Power Factor',
                                 'Time of Max/Min Power Factor Reset'
                                 'Max Freq',
                                 'Time of Max Freq',
                                 'Min Freq',
                                 'TIme of Min Freq',
                                 'Time of Max/Min Freq Reset']

  

def get_mapping_dictionary(repos):

    repos.mapping_dictionary = {'Setpoint 0'      : [repos.sp_zero_keys,   "write_setpoint_zero_request", "read_setpoint_zero_request"],
                                'Setpoint 1'      : [repos.sp_one_keys,    "write_setpoint_one_request", "read_setpoint_one_request"],
                                'Setpoint etu'    : [repos.sp_etu_keys,   "write_setpoint_one_request", "read_setpoint_one_request"],
                                'Setpoint 2'      : [repos.sp_two_keys,          "write_setpoint_two_request", "read_setpoint_two_request"],
                                'Setpoint 3'      : [repos.sp_three_keys,        "write_setpoint_three_request", "read_setpoint_three_request"],
                                'Setpoint 4'      : [repos.sp_four_keys,      "write_setpoint_four_request", "read_setpoint_four_request"],
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
                                'Buffer 42'       : [repos.buffer_fourty_two_keys, "N/A", "read_real_time_data_buffer_fourty_two_request"],
                                'Buffer 43'       : [repos.buffer_fourty_three_keys, "N/A", "read_real_time_data_buffer_fourty_three_request"],
                                'Buffer 48'       : [repos.buffer_fourty_eight_keys,  "N/A" , "read_real_time_data_buffer_fourty_eight_request"],
                                'Buffer 55'       : [repos.buffer_fifty_five_keys ,  "N/A" , "read_real_time_data_buffer_fifty_five_request"],   
                                'Configuration'   : [repos.configuration_keys,  "write_breaker_configuraiton", "read_breaker_configuraiton_request"],
                                'angle_keys'      : [repos.angle_keys, "N/A", "N/A"],
                                'Main'            : [repos.main_keys, "N/A", "N/A"],
                                'Inputs'          : [repos.expected_keys, "N/A", "N/A"],
                                'pf_and_freq'     : [repos.pf_and_freq_keys, "N/A", "N/A"]}
  
    repos.default_array =  ['Setpoint etu',
                             'Setpoint 0',
                             'Setpoint 5',
                             'Setpoint 6']


def get_rog_ratio(frame, rating):


    if frame == 0:
        #row_ratio = .000335
        row_ratio = .0003315
        
    elif frame == 1:
        #row_ratio = 0.000335
        #row_ratio = 0.0000875
        row_ratio = 0.000083
        
    elif frame == 2 or frame == 4:
        #row_ratio =.166/1000 Termp Removed
        row_ratio =.169/1000 
        
    else:
        row_ratio =.208/1000 
        #row_ratio =.169/1000 

    print(row_ratio)

    return row_ratio

def get_ct_ratio(frame, rating):

    ct_ratio = 0
    ph = True
    ph_type = 1
        
    return ct_ratio, ph, ph_type

def version_two_keys(repos): 
    repos.sp_zero_keys =   ['Rating',
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
                            'Health Level']

def reset_to_no_trip_values(repos):

    #Group 0 Values
    repos.etu_dictionary['MM Mode'][0] = 0
    repos.etu_dictionary['MM Level'][0] = 2
    repos.etu_dictionary['Line Frequency'][0] = 60
    repos.etu_dictionary['Reverse Feed'][0] = 0
    repos.etu_dictionary['Sign'][0] = 0
    repos.etu_dictionary['Power Window'][0] = 0
    repos.etu_dictionary['Power Interval'][0] = 5
    repos.etu_dictionary['Language'][0] = 0
    repos.etu_dictionary['I Window'][0] = 0
    repos.etu_dictionary['I Interval'][0] = 2
    repos.etu_dictionary['Health Level'][0] = 25
    repos.etu_dictionary['System Voltage'][0] = 240
    repos.etu_dictionary['Neutral Sensor'][0] = 1
    repos.etu_dictionary['Active Setpoints Group'][0] = 1
    repos.etu_dictionary['GF ZSI'][0] = 0
    repos.etu_dictionary['LD Thermal'][0] = 0

    #Group 1 Values                        
    repos.etu_dictionary['LD Slope'][0] = 2
    repos.etu_dictionary['LD PU'][0] = 100
    repos.etu_dictionary['LD Time'][0] = 24
    repos.etu_dictionary['SD PU' ][0] = 14
    repos.etu_dictionary['SD PU' ][0] = 14
    repos.etu_dictionary['Inst PU'][0] = 15
    repos.etu_dictionary['GF Mode'][0] = 2
    repos.etu_dictionary['GF Type'][0] = 0
    repos.etu_dictionary['Etu LD Slope'][0] = 2
    repos.etu_dictionary['Etu LD PU' ][0] = 100
    repos.etu_dictionary['Etu LD Time'][0] = 2400
    repos.etu_dictionary['Etu SD Slope'][0] = 0
    repos.etu_dictionary['Etu SD PU' ][0] = 140
    repos.etu_dictionary['Etu SD Time'][0] = 50
    repos.etu_dictionary['Etu Inst PU' ][0] =150
    repos.etu_dictionary['Etu GF Mode'][0] = 2
    repos.etu_dictionary['ZSI'][0] = 0
    repos.etu_dictionary['Etu GF Type'][0] = 0
    repos.etu_dictionary['Etu GF ZSI'][0] = 0
    repos.etu_dictionary['Etu LD Thermal'][0] = 0

    #Group 4 Values                        
    repos.etu_dictionary['Frequency Protection Enable'][0] = 0
    repos.etu_dictionary['Over Frequency Action'][0] = 0
    repos.etu_dictionary['Over Frequency Pickup'][0] = 1050
    repos.etu_dictionary['Over Frequency Time'][0] = 30000
    repos.etu_dictionary['Under Frequency Action'][0] = 0
    repos.etu_dictionary['Under Frequency Pickup'][0] = 950
    repos.etu_dictionary['Under Frequency Time'][0] = 30000
    repos.etu_dictionary['Over Frequency Alarm Action'][0] = 0
    repos.etu_dictionary['Over Frequency Alarm Pickup'][0] = 1050
    repos.etu_dictionary['Over Frequency Alarm Time'][0] = 30000
    repos.etu_dictionary['Under Frequency Alarm Action'][0] = 0
    repos.etu_dictionary['Under Frequency Alarm Pickup'][0] = 950
    repos.etu_dictionary['Under Frequency Alarm Time'][0] = 30000

    #Group 5 Values  
    
    repos.etu_dictionary['Over V Action'][0]      = 0
    repos.etu_dictionary['Over V PU'][0]        = 1050
    repos.etu_dictionary['Over V Time'][0]      = 30000
    repos.etu_dictionary['Under V Action'][0]     = 0
    repos.etu_dictionary['Under V PU'][0]       = 500
    repos.etu_dictionary['Under V Time'][0]     = 30000
    repos.etu_dictionary['V Unbalance Action'][0] = 0
    repos.etu_dictionary['V Unbalance PU'][0]   = 90
    repos.etu_dictionary['V Unbalance Time'][0] = 30000
    repos.etu_dictionary['I Unbalance Action'][0] = 0
    repos.etu_dictionary['I Unbalance PU'][0]   = 90
    repos.etu_dictionary['Reverse Forward Power Action'][0]   = 2
    repos.etu_dictionary['Reverse Forward Power Pickup'][0]     = 1
    repos.etu_dictionary['Reverse Forward Power Time'][0]   = 30000
    repos.etu_dictionary['Power Rev Sense'][0]  = 0
    repos.etu_dictionary['Power Rev Action'][0]   = 2
    repos.etu_dictionary['Phase Loss Action'][0]  = 2
    repos.etu_dictionary['Phase Loss Time'][0]  = 1
    repos.etu_dictionary['Over V Alarm Action'][0] = 0
    repos.etu_dictionary['Over V Alarm PU'][0]  = 1050
    repos.etu_dictionary['Over V Alarm Time'][0]  = 30000
    repos.etu_dictionary['Extended Protection Enable/Disable'][0] = 0
    repos.etu_dictionary['Reverse Reactive Power Action'][0] = 2
    repos.etu_dictionary['Reverse Reactive Power Pickup'][0] = 1
    repos.etu_dictionary['Reverse Reactive Power Time'][0] = 30000
    repos.etu_dictionary['Phase Rotation Time'][0] = 30000
    repos.etu_dictionary['Over V Number Of Phases'][0] = 1
    repos.etu_dictionary['Under V Number Of Phases'][0] = 1
    repos.etu_dictionary['Under V Alarm Action'][0] = 2
    repos.etu_dictionary['Under V Alarm PU'][0] = 500
    repos.etu_dictionary['Under V Alarm Time'][0] = 30000
    repos.etu_dictionary['V Unbalance Alarm Action'][0] = 0
    repos.etu_dictionary['V Unbalance Alarm PU'][0] = 90
    repos.etu_dictionary['V Unbalance Alarm Time'][0] = 30000
    repos.etu_dictionary['I Unbalance Alarm Action'][0] = 0
    repos.etu_dictionary['I Unbalance Alarm PU'][0] = 90
    repos.etu_dictionary['I Unbalance Alarm Time'][0] = 30000

                            
    #Group 6 Values                        
    repos.etu_dictionary['Power Protection Enable/Disable'][0] = 0
    repos.etu_dictionary['Forward Real Power Action'][0] = 2
    repos.etu_dictionary['Forward Real Power Pickup'][0] = 1
    repos.etu_dictionary['Forward Real Power Time'][0] = 300
    repos.etu_dictionary['Forward Reactive Power Action'][0] = 2
    repos.etu_dictionary['Forward Reactvie Power Pickup'][0] = 1
    repos.etu_dictionary['Forward Reactive Power Time'][0] = 300
    repos.etu_dictionary['Apparent Power Action'][0] = 2
    repos.etu_dictionary['Apparent Power Pickup'][0] = 1
    repos.etu_dictionary['Apparent Power Time'][0] = 300
    repos.etu_dictionary['Under Power Factor Action'][0] = 2
    repos.etu_dictionary['Under Power Factor Pickup'][0] = 95
    repos.etu_dictionary['Under Power Factor Time'][0] = 300
    repos.etu_dictionary['Real Demand Power Action'][0] = 2
    repos.etu_dictionary['Real Demand Power Pickup'][0] = 1000
    repos.etu_dictionary['Real Demand Power Time'][0] = 2
    repos.etu_dictionary['Apparent Demand Power Action'][0] = 2
    repos.etu_dictionary['Apparent Demand Power Pickup'][0] = 1000
    repos.etu_dictionary['Apparent Demand Power Time'][0] = 2
    repos.etu_dictionary['Demand Mode Precision'][0] = 16




    

   

