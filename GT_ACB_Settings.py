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

def add_dictionary_values(repos, keys):

    for val in keys:
        repos.etu_dictionary.update({val:[0, "Uint16"]})

    
def add_setpoint_group_zero(repos):

    if repos.frame != 0 and repos.frame != 1:
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
                                'Source Ground Sensor']
    else: 
        repos.sp_zero_keys =   ['Rating',
                                'Frame',
                                'Style1',
                                'MM Mode',
                                'MM Level',
                                'Line Frequency',
                                'Reverse Feed',
                                'Language']

        
    add_dictionary_values(repos, repos.sp_zero_keys)
    repos.mapping_dictionary['Setpoint 0']  = [repos.sp_zero_keys,   "write_setpoint_zero_request", "read_setpoint_zero_request"]
        

def add_setpoint_group_one(repos):

    print("THE FRAME IS " + str(repos.frame))
    if repos.frame == 0 or repos.frame == 1:
        repos.sp_one_keys =     ['Rating',
                                'Frame',
                                'Style1',
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
                                'Neutral Ratio'
                                ]

                                #'Style2',
                                #'GF Thermal',
                                #'Neutral Ratio',
                                #'HL Alarm 2',
                                #'GF Alarm', 
                                #'Thermal Alarm'
                                        
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
                                'Etu Thermal Alarm'
                            ]
    else: 

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
                                'Thermal Alarm'
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
                                'Etu Thermal Alarm'
                                ]
    add_dictionary_values(repos, repos.sp_one_keys)
    add_dictionary_values(repos, repos.sp_etu_keys)
    repos.mapping_dictionary['Setpoint 1']    = [repos.sp_one_keys,   "write_setpoint_one_request", "read_setpoint_one_request"]
    repos.mapping_dictionary['Setpoint etu']  = [repos.sp_etu_keys,   "write_setpoint_one_request", "read_setpoint_one_request"]

def add_setpoint_group_two(repos):

    if repos.frame == 0 or repos.frame == 1:
        repos.sp_two_keys   =   ['MBus Address',
                                 'MBus Baud',
                                 'MBus Parity',
                                 'MBus Stop Bit']
        
    else:

        repos.sp_two_keys   =   ['MBus Address',
                                 'MBus Baud',
                                 'MBus Parity',
                                 'MBus Stop Bit'
                                 'RTU Invalid Handeling']
        
        '''
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
        '''
    
    add_dictionary_values(repos, repos.sp_two_keys)
    repos.mapping_dictionary['Setpoint 2']  = [repos.sp_two_keys,   "write_setpoint_two_request", "read_setpoint_two_request"]

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
    repos.mapping_dictionary['Setpoint 3']  = [repos.sp_three_keys,   "write_setpoint_three_request", "read_setpoint_three_request"]


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
                            'Reverse Real Power Action',
                            'Reverse Real Power Pickup',
                            'Reverse Real Power Time',
                            'Power Rev Sense',
                            'Power Rev Action',
                            'Phase Loss Action',
                            'Phase Loss Time',
                            'Reserved16_5-1',
                            'Reserved16_5-2',
                            'Reserved16_5-3',
                            'Reserved16_5-4',
                            'Reserved16_5-5']
    
    add_dictionary_values(repos, repos.sp_five_keys)
    repos.mapping_dictionary['Setpoint 5']  = [repos.sp_five_keys,   "write_setpoint_five_request", "read_setpoint_five_request"]
                            
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

    repos.mapping_dictionary['Buffer 0']    = [repos.buffer_zero_keys,     "N/A" , "read_real_time_data_buffer_zero_request"]

def add_buffer_one(repos):

    repos.buffer_one_keys = ['External Ia',
                                    'External Ib',
                                    'External Ic',
                                    'External In',
                                    'External Ig',
                                    'I Average', 
                                    'External Va',
                                    'External Vb',
                                    'External Vc',
                                    'V LN Average',
                                    'External Vab',
                                    'External Vbc',
                                    'External Vca',
                                    'V LL Average',
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

    repos.etu_dictionary['External Ia']       = [0, "Q4"]
    repos.etu_dictionary['External Ib']       = [0, "Q4"]
    repos.etu_dictionary['External Ic']       = [0, "Q4"]
    repos.etu_dictionary['External In']       = [0, "Q4"]
    repos.etu_dictionary['External Ig']       = [0, "Q4"]
    repos.etu_dictionary['External Va']       = [0, "Float"]
    repos.etu_dictionary['External Vb']       = [0, "Q4Padded"]
    repos.etu_dictionary['External Vc']       = [0, "Q4Padded"]
    repos.etu_dictionary['External Vab']      = [0, "Q4Padded"]
    repos.etu_dictionary['External Vbc']      = [0, "Q4Padded"]
    repos.etu_dictionary['External Vca']      = [0, "Q4Padded"]
    repos.etu_dictionary["Freq"]              =  [0,"Q4Padded"]
    repos.etu_dictionary['Real Power']        = [0, "int32"]
    repos.etu_dictionary['React Power']       = [0, "int32"]
    repos.etu_dictionary['App Power']         = [0, "Uint32"]
    repos.etu_dictionary['PF']                = [0, "Q10Padded"]
    repos.etu_dictionary['Temp']              = [0, "Q4Padded"]
    repos.etu_dictionary['Batt Val']          = [0, "Q8Padded"]
    
    repos.mapping_dictionary['Buffer 1']    = [repos.buffer_one_keys,     "N/A" , "read_real_time_data_buffer_one"]


def add_buffer_two(repos):

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

    repos.mapping_dictionary['Buffer 2']    = [repos.buffer_two_keys,     "N/A" , "read_real_time_data_buffer_two_request"]

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

    repos.mapping_dictionary['Buffer 4']    = [repos.buffer_four_keys,     "N/A" , "read_real_time_data_buffer_four_request"]
    
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

    repos.mapping_dictionary['Buffer 5']    = [repos.buffer_five_keys,     "N/A" , "read_real_time_data_buffer_five_request"]

    
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

    repos.mapping_dictionary['Buffer 6']    = [repos.buffer_six_keys,     "N/A" , "read_real_time_data_buffer_six_request"]

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

    repos.mapping_dictionary['Buffer 11']    = [repos.buffer_eleven_keys,     "N/A" , "read_real_time_data_buffer_eleven_request"]

def add_buffer_fifteen(repos):

    repos.buffer_fifteen_keys = ['Current Unbalance',
                                 'Voltage Unbalance']

    repos.etu_dictionary['Current Unbalance']   =  [0, "Int32"]
    repos.etu_dictionary['Voltage Unbalance']   =  [0, "Int32"]

    repos.mapping_dictionary['Buffer 15']    = [repos.buffer_fifteen_keys,     "N/A" , "read_real_time_data_buffer_fifteen_request"]

def add_buffer_twenty(repos):

    repos.crest_seventy_keys = ['Ia Current Crest Factor',
                                'Ib Current Crest Factor',
                                'Ic Current Crest Factor',
                                'In Current Crest Factor']
    
    repos.etu_dictionary['Ia Current Crest Factor']=[0, "Q9"]
    repos.etu_dictionary['Ib Current Crest Factor']=[0, "Q9"]
    repos.etu_dictionary['Ic Current Crest Factor']=[0, "Q9"]
    repos.etu_dictionary['In Current Crest Factor']=[0, "Q9"]

    repos.mapping_dictionary['Buffer 20']    = [repos.buffer_twenty_keys,     "N/A" , "read_real_time_data_buffer_twenty_request"]

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
    repos.etu_dictionary["Override"][0] = 150
    repos.mapping_dictionary['Configuration']   = [repos.configuration_keys,  "write_breaker_configuraiton", "read_breaker_configuraiton_request"]


    
def get_dictionary(repos):

    repos.mapping_dictionary = {'angle_keys'      : [repos.angle_keys, "N/A", "N/A"],
                                'Main'            : [repos.main_keys, "N/A", "N/A"],
                                'Inputs'          : [repos.expected_keys, "N/A", "N/A"],
                                'Power Harvester Keys': [repos.power_harvester_keys, "N/A", "N/A"]}
    
    repos.etu_dictionary =  {'Rating'        : [0, "Uint16"],
                            'Frame'          : [0, "Uint16"],
                            'Style1'         : [0, "Uint16"],
                            'Style2'         : [0, "Uint16"],
                            'MM Mode'        : [0, "Uint16"],
                            'MM Level'       : [0, "Uint16"],
                            'Line Frequency' : [0, "Uint16"],
                            'Reverse Feed'   : [0, "Uint16"],
                            'Sign'           : [0, "Uint16"],
                            'Power Window'   : [0, "Uint16"],
                            'Power Interval' : [0, "Uint16"],
                            'Language'       : [0, "Uint16"],
                            'LCD Rotatation' : [0, "Uint16"],
                            'Relay 1'        : [0, "Uint16"],
                            'Relay 2'        : [0, "Uint16"],
                            'Relay 3'        : [0, "Uint16"],
                            'Pole Location'  : [0, "Uint16"],
                            'I Window'       : [0, "Uint16"],
                            'I Interval'     : [0, "Uint16"],
                            'Health Level'   : [0, "Uint16"],
                            'System Voltage' : [0, "Uint16"],
                            'Neutral Sensor' : [0, "Uint16"],
                            'Source Ground Sensor' : [0, "Uint16"], 
                            'LD Thermal'           : [0, "Uint16"],
                            'ZSI'                  : [0, "Uint16"],
                            'LD Slope'             : [0, "Uint16"],
                            'LD PU'                : [0, "Uint16"],
                            'LD Time'              : [0, "Uint16"],
                            'HL Alarm 1'           : [0, "Uint16"],
                            'SD Slope'             : [0, "Uint16"],
                            'SD PU'                : [0, "Uint16"],
                            'SD Time'              : [0, "Uint16"],
                            'Inst PU'              : [0, "Uint16"],
                            'GF Type'              : [0, "Uint16"],
                            'GF Mode'              : [0, "Uint16"],
                            'GF Slope'             : [0, "Uint16"],
                            'GF PU'                : [0, "Uint16"],
                            'GF Time'              : [0, "Uint16"],
                            'GF Thermal'           : [0, "Uint16"],
                            'Neutral Ratio'         : [0, "Uint16"],
                            'HL Alarm 2'           : [0, "Uint16"],
                            'GF Alarm'             : [0, "Uint16"],
                            'Thermal Alarm'        : [0, "Uint16"],
                            'Etu Rating'               : [0, "Uint16"],
                            'Etu Frame'                : [0, "Uint16"],
                            'Etu Style1'               : [0, "Uint16"],
                            'Etu Style2'               : [0, "Uint16"],
                            'Etu LD Thermal'           : [0, "Uint16"],
                            'Etu ZSI'                  : [0, "Uint16"],
                            'Etu LD Slope'             : [0, "Uint16"],
                            'Etu LD PU'                : [0, "Uint16"],
                            'Etu LD Time'              : [0, "Uint16"],
                            'Etu HL Alarm 1'           : [0, "Uint16"],
                            'Etu SD Slope'             : [0, "Uint16"],
                            'Etu SD PU'                : [0, "Uint16"],
                            'Etu SD Time'              : [0, "Uint16"],
                            'Etu Inst PU'              : [0, "Uint16"],
                            'Etu GF Type'              : [0, "Uint16"],
                            'Etu GF Mode'              : [0, "Uint16"],
                            'Etu GF Slope'             : [0, "Uint16"],
                            'Etu GF PU'                : [0, "Uint16"],
                            'Etu GF Time'              : [0, "Uint16"],
                            'Etu GF Thermal'           : [0, "Uint16"],
                            'Etu Neutral Ratio'         : [0, "Uint16"],
                            'Etu HL Alarm 2'           : [0, "Uint16"],
                            'Etu GF Alarm'             : [0, "Uint16"],
                            'Etu Thermal Alarm'        : [0, "Uint16"],
                            'MBus Address'             : [0, "Uint16"],
                            'MBus Baud'                : [0, "Uint16"],
                            'MBus Parity'              : [0, "Uint16"],
                            'MBus Stop Bit'            : [0, "Uint16"],
                            'Cam Satus'                : [0, "Uint16"],
                            'mCam Address'             : [0, "Uint16"],
                            'mCam Baud'                : [0, "Uint16"],
                            'mCam Parity'              : [0, "Uint16"],
                            'mCam Stop Bit'            : [0, "Uint16"],
                            'Incom Address'            : [0, "Uint16"],
                            'Incom Baud'               : [0, "Uint16"],
                            'eCam DHCP'                : [0, "Uint16"],
                            'eCam IP Zero'             : [0, "Uint16"],
                            'eCam IP One'              : [0, "Uint16"],
                            'eCam IP Two'              : [0, "Uint16"],
                            'eCam IP Three'            : [0, "Uint16"],
                            'eCam Subnet'              : [0, "Uint16"],
                            'eCam Default Two'         : [0, "Uint16"],
                            'eCam Default One'         : [0, "Uint16"],
                            'eCam Reset'               : [0, "Uint16"],
                            'pCam Address'             : [0, "Uint16"],
                            'Over V Action'              : [2, "Uint16"],
                            'Over V PU'                : [0, "Uint16"],
                            'Over V Time'              : [0, "Uint16"],
                            'Under V Action'             : [2, "Uint16"],
                            'Under V PU'               : [0, "Uint16"],
                            'Under V Time'             : [0, "Uint16"],
                            'V Unbalance PU'           : [0, "Uint16"],
                            'V Unbalance Action'         : [2, "Uint16"],
                            'V Unbalance Time'         : [0, "Uint16"],
                            'I Unbalance Action'         : [2, "Uint16"],
                            'I Unbalance PU'           : [0, "Uint16"],
                            'I Unbalance Time'         : [0, "Uint16"],
                            'Reverse Forward Power Action'           : [2, "Uint16"],
                            'Reverse Forward Power Pickup'             : [0, "Uint16"],
                            'Reverse Forward Power Time'           : [0, "Uint16"],
                            'Power Rev Sense'          : [0, "Uint16"],
                            'Power Rev Type'           : [2, "Uint16"],
                            'Phase Loss Action'          : [0, "Uint16"],
                            'Phase Loss Time'          : [0, "Uint16"],
                            'MCU1 Version'             : [0, "Uint16"],
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
                            "frame_ap"                :  [0,"Uint16"],
                            "poles"                   :  [0,"Uint16"],
                            "standard"                :  [0,"Uint16"],
                            "ct_version"              :  [0,"Uint16"],
                            "Override"                :  [120000,"Uint32"],
                            "MCR"                     :  [0,"Uint32"],             
                            "max_interupt_label"      :  [0,"Uint32"], 
                            "frame_construction"      :  [0,"Uint32"],
                            'Setpoints Group Sensor'  :  [0,"Uint16"],
                            'Active Setpoints Group'  :  [0,"Uint16"],
                            'ScondPT/VDB Module Present'      :  [0,"Uint16"],
                            'Phase Labeling'                  :  [0,"Uint16"],
                            'Trip Waveform Capture Precycles' :  [0,"Uint16"],
                            'Extended Capture Triggers'       :  [0,"Uint16"],
                            'IEC61860 Configuration'          :  [0,"Uint16"],
                            'Demand Logging Interval'         :  [0,"Uint16"],
                            'Reserved16'                      :  [0,"Uint16"],
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
                            'Power Protection Enable/Disable' :  [0,"Uint16"],
                            'Forward Real Power Action':  [2,"Uint16"],
                            'Forward Real Power Pickup':  [0,"Uint16"],
                            'Forward Real Power Time':  [0,"Uint16"],
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
                            'Over Frequency Action'        : [0,"Uint16"],
                            'Over Frequency Pickup'        : [0,"Uint16"],
                            'Over Frequency Time'          : [0,"Uint16"],
                            'Under Frequency Action'       : [0,"Uint16"],
                            'Under Frequency Pickup'       : [0,"Uint16"],
                            'Under Frequency Time'         : [0,"Uint16"],
                            'Alarm Waveform Capture Precycles'  : [0,"Uint16"],
                            'Zero_R_Zero': [0,"Uint16"],
                            'Zero_R_One': [0,"Uint16"],
                            'Zero_R_Two': [0,"Uint16"],
                            'Over Frequency Alarm Action' : [0,"Uint16"],
                            'Over Frequency Alarm Pickup' : [0,"Uint16"],
                            'Over Frequency Alarm Time' : [0,"Uint16"],
                            'Under Frequency Alarm Action' : [0,"Uint16"],
                            'Under Frequency Alarm Pickup' : [0,"Uint16"],
                            'Under Frequency Alarm Time' : [0,"Uint16"],
                            'Demand Mode Precision' : [16, "Uint16"],
                            'Power Harvester A'       : [2, "Uint16"],
                            'Power Harvester B'       : [2, "Uint16"],
                            'Power Harvester C'       : [2, "Uint16"],
                            'Reserved16_2' : [192, "Uint16"],
                             'Reserved16_3' : [193, "Uint16"]}


    add_setpoint_group_zero(repos)
    add_setpoint_group_one(repos)
    add_setpoint_group_two(repos)
    add_setpoint_group_three(repos)
    add_setpoint_group_five(repos)
    add_buffer_zero(repos)
    add_buffer_one(repos)
    add_configuration(repos)
    mapping_keys = []
    repos.mapping_keys = list(repos.mapping_dictionary.keys())
    repos.power_harvester_keys = ['Power Harvester A',
                                  'Power Harvester B',
                                  'Power Harvester C']



'''
    ====================================================================================================================
====Keys =======================================================================================================
    =================
'''

def get_setpoint_keys(repos):

    repos.mech_time = .019
  

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
    
    repos.breaker_protection_capacity_keys = ['frame_ap',
                                        'poles',
                                        'standard', 
                                        'ct_version', 
                                        'withstand',
                                        'MCR',              
                                        'max_interupt_label', 
                                        'frame_construction']

    repos.configuration_keys =   ["Poles",
                                  "Standard",
                                  "Device Type",
                                  "DC Rating",
                                  "Voltage Metering",
                                  "Max IEC Amps",
                                  "Max UL Amps",
                                  "Max ANSI/UL Amps",
                                  "Purchased",
                                  "Min In",
                                  "Withstand Limit",
                                  "Override",
                                  "MCR Multiplier",
                                  "Ground Fault Max",
                                  "Max Physical Limit",
                                  "Max Label",
                                  "Max Instantaneous"]

    repos.source_keys =     ["Source_Freq", 
                            "Ra_Phase_Angle",
                            "Rb_Phase_Angle",
                            "Rc_Phase_Angle",
                            "Ia_Phase_Angle",
                            "Ib_Phase_Angle",
                            "Ic_Phase_Angle",
                            "Va_Phase_Angle",
                            "Vb_Phase_Angle",
                            "Vc_Phase_Angle"]

    repos.power_harvester_keys = ['Power Harvester A',
                                  'Power Harvester B',
                                  'Power Harvester C']

    
def get_buffer_keys(repos):


    '''
    repos.buffer_zero_keys = ['primary_status',
                            'second_status',
                            'cause_of_status',
                            'breaker_status',
                            'trip_condition',
                            'alarm_condition',
                            'MM_status',
                            'test_mode_status',
                            'testing_forbid',
                            'ld_pickup_status',
                            'ZIN_status',
                            'GF_condition']

            
    repos.buffer_one_keys = ['external_Ia',
                            'external_Ib',
                            'external_Ic',
                            'external_In',
                            'external_Ig',
                            'external_Va',
                            'external_Vb',
                            'external_Vc',
                            'external_Vab',
                            'external_Vbc',
                            'external_Vca',
                            'freq',
                            'real_power',
                            'react_power',
                            'app_power',
                            'pf',
                            'temp',
                            'batt_val']
    '''
    
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
        
    repos.internal_diagnostic_keys = ["I Short Circuit",
                            "I Short Delay",
                            "I Inst",
                            "I Hi Current Trip",
                            "I Total Overload", 
                            "I Long Delay",
                            "I Ground Fault",
                            "I Total Ops",
                            "I Trip Ops",
                            "I Open Ops" ,
                            "I Manual Ops",
                            "I Time Of Last Op",
                            "I Max Temp",
                            "I Time Temp",
                            "I Run Min",
                            "I Run Hour",
                            "I Run Day",
                            "I LP"]
    repos.external_diagnostic_keys = ["E Short Circuit",
                            "E Short Delay",
                            "E Inst",
                            "E Hi Current Trip",
                            "E Total Overload", 
                            "E Long Delay",
                            "E Ground Fault",
                            "E Total Ops",
                            "E Trip Ops",
                            "E Open Ops",
                            "E Manual Ops",
                            "E Time Of Last Op",
                            "E Max Temp",
                            "E Time Temp",
                            "E Run Min",
                            "E Run Hour",
                            "E Run Day",
                            "E LP"]

    repos.buffer_fourty_two_keys = ["I Op Counter",
                               "I Contact Wear Reset",
                               "I Mech Wear Reset",
                               "I TimeTemp Wear Reset",
                               "I Contact Wear",
                               "I Mech Wear",
                               "I TimeTemp Wear",
                               "I Num LP Resets"]

    repos.buffer_fourty_three_keys = ["E Op Counter",
                                 "E Contact Wear Reset",
                                 "E Mech Wear Reset",
                                 "E TimeTemp Wear Reset",
                                 "E Contact Wear",
                                 "E Mech Wear",
                                 "E TimeTemp Wear",
                                 "E Num LP Resets"]
        
    repos.firmware_keys =     [ 'MCU1 Version',
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
def get_mapping_dictionary(repos):

    '''
    repos.mapping_dictionary = {'Setpoint 0'      : [repos.sp_zero_keys,   "read_setpoint_zero_request", "write_setpoint_zero_request"],
                                'Setpoint 1'      : [repos.sp_one_keys,    "read_setpoint_one_request", "write_setpoint_one_request"],
                                'Setpoint etu'    : [repos.sp_etu_keys,   "read_setpoint_one_request", "write_setpoint_one_request"],
                                'Setpoint 2'      : [repos.sp_two_keys,          "read_setpoint_two_request", "write_setpoint_two_request"],
                                'Setpoint 3'      : [repos.sp_three_keys,        "read_setpoint_three_request", "write_setpoint_three_request"],
                                'Setpoint 5'      : [repos.sp_five_keys,      "read_setpoint_five_request", "write_setpoint_five_request"],
                                'Setpoint 6'      : [repos.sp_six_keys,      "read_setpoint_six_request", "write_setpoint_six_request"],
                                'Setpoint 7'      : [repos.sp_seven_keys,      "read_setpoint_seven_request", "write_setpoint_seven_request"],
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
                                'Configuration'   : [repos.breaker_protection_capacity_keys,  "N/A" , "write_breaker_configuraiton"],
                                'angle_keys'      : [repos.angle_keys, "N/A", "N/A"],
                                'Main'            : [repos.main_keys, "N/A", "N/A"],
                                'Inputs'          : [repos.expected_keys, "N/A", "N/A"]}
    '''


    repos.default_array =  ['Setpoint etu']
def get_rog_ratio(frame, rating):

    print("GET ROG RATIO")
    print(str(frame))
    if frame == 0:
        row_ratio = .000345
        #row_ratio = .0003315
        print("NF")
        
    elif frame == 1:
        #row_ratio = 0.000335
        #row_ratio = 0.0000875
        row_ratio = 0.000083
        
    elif frame == 2 or frame == 4:
        row_ratio =.166/1000
    else:
        row_ratio =.208/1000

    return row_ratio

def get_ct_ratio(frame, rating):

    ct_ratio = 0
    ph = True
    ph_type = 1
        
    return ct_ratio, ph, ph_type
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
    repos.etu_dictionary['I Interval'][0] = 5
    repos.etu_dictionary['Health Level'][0] = 25


                                    
 
    #Group 1 Values
    repos.etu_dictionary['LD Thermal'][0] = 0
    repos.etu_dictionary['LD Slope'][0] = 2
    repos.etu_dictionary['LD PU'][0] = 100
    repos.etu_dictionary['LD Time'][0] = 24
    
    repos.etu_dictionary['SD Time' ][0] = .5
    repos.etu_dictionary['SD Slope' ][0] = 0
    repos.etu_dictionary['SD PU' ][0] = 10

    repos.etu_dictionary['Inst PU'][0] = 15
    repos.etu_dictionary['GF Slope'][0] = 0
    repos.etu_dictionary['GF Time'][0] = 1
    repos.etu_dictionary['GF PU'][0] = .2
    repos.etu_dictionary['GF Mode'][0] = 2
    
    repos.etu_dictionary['Etu LD Slope'][0] = 2
    repos.etu_dictionary['Etu LD PU' ][0] = 100
    repos.etu_dictionary['Etu LD Time'][0] = 240
    repos.etu_dictionary['Etu SD Time' ][0] = 50
    repos.etu_dictionary['Etu SD Slope' ][0] = 0
    repos.etu_dictionary['Etu SD PU' ][0] = 100
    repos.etu_dictionary['Etu Inst PU' ][0] =150
    repos.etu_dictionary['Etu GF Slope'][0] = 0
    repos.etu_dictionary['Etu GF Time'][0] = 100
    repos.etu_dictionary['Etu GF PU'][0] = 20
    repos.etu_dictionary['Etu GF Mode'][0] = 2
    repos.etu_dictionary['ZSI'][0] = 0


    #Group 5 Values  
    
    repos.etu_dictionary['Over V Action'][0]      = 2
    repos.etu_dictionary['Over V PU'][0]        = 180
    repos.etu_dictionary['Over V Time'][0]      = 300
    repos.etu_dictionary['Under V Action'][0]     = 2
    repos.etu_dictionary['Under V PU'][0]       = 60
    repos.etu_dictionary['Under V Time'][0]     = 300
    repos.etu_dictionary['V Unbalance Action'][0] = 2
    repos.etu_dictionary['V Unbalance PU'][0]   = 10
    repos.etu_dictionary['V Unbalance Time'][0] = 300
    repos.etu_dictionary['I Unbalance Action'][0] = 2
    repos.etu_dictionary['I Unbalance PU'][0]   = 10
    repos.etu_dictionary['I Unbalance Time'][0]   = 300
    repos.etu_dictionary['Reverse Real Power Action'][0]   = 2
    repos.etu_dictionary['Reverse Real Power Pickup'][0]     = 1
    repos.etu_dictionary['Reverse Real Power Time'][0]   = 300
    repos.etu_dictionary['Power Rev Sense'][0]  = 0
    repos.etu_dictionary['Power Rev Action'][0]   = 2
    repos.etu_dictionary['Phase Loss Action'][0]  = 2
    repos.etu_dictionary['Phase Loss Time'][0]  = 1




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
