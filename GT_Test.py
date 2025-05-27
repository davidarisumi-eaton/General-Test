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
                
                
-------------------------------------------------------------------------------
    
    Product:    Automated test system to test the PXR10, PXR20, PXR2D, PXR25, 
                and PXR35 protection algorithms for the SR, NZM, and NRX 
                breaker frames.   
                
    Module:     GT_Test.py
                
    Mechanics:  Has test routines. Uses Excel fies as inputs. 
                                         
----------------------------------------------------------------------------'''

from __future__ import division
import random, time
from GT import GT_Calibration, GT_Secondary_Injection, GT_Calculations, GT_Conversions, GT_System_Control
import math
#from openpyxl import load_workbook



    
'''
=========================================================================================================================================================================================
Run Test Methods
=========================================================================================================================================================================================
'''
def main(repos, in_file, output_file, usb, omicron):             #  test type select  
    
    active_row = 5
    input_start = 1
    next_test = True
        
    repos.reset_to_no_trip_values()

    msg = "Testing  " + str(in_file.filename) + "\n\n\n"
    repos.append_output_msg(msg)

    #rsp = usb.communicate("enter_password_request",0,0,0,0)
    
    for val in repos.default_array:
        if repos.family == "35":
            rsp = usb.communicate("enter_password_request",0,0,0,0,0,1)
        else:
            rsp = usb.communicate("enter_password_request",0,0,0,0)
        time.sleep(.5)
        request = repos.mapping_dictionary[val][1]
        key = repos.mapping_dictionary[val][0]
        write_setpoints_to_trip_unit(usb, request, key, repos.etu_dictionary, repos)
        time.sleep(.5)

    

    
    while(next_test):

        repos.append_debug_msg(repos.index)
        test_type = read_setpoints_from_excel(in_file, repos, active_row)
        time.sleep(2)

        if test_type is None:
            break


        if repos.UI_test_type != "Excel": #Overrides the test type if the user wishes
            test_type = repos.UI_test_type

        #rsp = usb.communicate("reset_trip_unit_request")
        #rsp = usb.communicate_with_check("reset_trip_unit_check")
                            
        test_type = check_setting_correctness(repos, test_type, usb)
        test_type = enter_into_auto_test_mode(repos, usb, test_type)
        test_type = write_setpoints_from_excel(usb, repos, test_type)
        if test_type == 'No Test':
            time.sleep(5)
            print("Second Attempt")
            print(repos.etu_dictionary)
            test_type = write_setpoints_from_excel(usb, repos, test_type)
            


        repos.ready_for_test == True
        ''' run selected test type'''
        if test_type == 'Trip':
            run_trip_test(repos, usb, omicron)

            if repos.results['Result'] == 'Fail':
                print("retry")
                time.sleep(5)
                run_trip_test(repos, usb, omicron)
                
        elif test_type == 'Meter':
            run_meter_test(repos, omicron)
        elif test_type == 'Continuous':
            run_continuous_meter_test(repos, omicron)
        elif test_type == 'Hardware Test':
            run_hardware_trip_test(repos, usb)
        elif test_type == 'Firmware Test':
            run_firmware_trip_test(repos, usb)
        elif test_type == 'Firmware Test Without Trip':
            run_hardware_without_trip_test(repos, usb)
        elif test_type == 'Hardware Test Without Trip':
            run_firmware_without_trip_test(repos, usb)
        elif test_type == 'Hardware Meter':
            run_hardware_meter_test(repos)
        elif test_type == 'Firmware Meter':
            run_firmware_meter_test(repos)
        elif test_type == 'Life Point Test':
            run_life_point_test(repos, omicron)
        elif test_type == 'GF':
            run_source_ground_trip(repos, usb, omicron)
        elif test_type == "U_Voltage":
            run_undervolt_trip_test(repos, usb, omicron)
        elif test_type == "Health":
            run_acb_health_test(repos, usb, omicron)
        elif test_type == 'Custom':
            run_custom_test(repos, usb, omicron)
        elif test_type == 'ZSI':
            run_zsi(repos, usb, omicron, active_row)
        elif test_type == 'No Test':
            run_no_test(repos)
        elif test_type == 'No Test':
            run_no_test(repos)
        elif test_type == 'Manufactory Mode Tests':
            run_hardware_maint_trip_test(repos, usb)
        elif test_type == None:
            repos.failure_mode = "Test Is None"
            run_no_test(repos)
        else:
            repos.ready_for_test == False
            repos.failure_mode = test_type + " Is Not A Valid Test Type"
            run_no_test(repos)
            
        if repos.ready_for_test:   
            check(repos)
        else:
            msg = bad_check(repos)

        repos.expected['Test Type'] = test_type


        rsp = usb.communicate("read_real_time_data_buffer_zero_request")
        cor = usb.get_correctness(rsp)

        if repos.pxr == "PXR10":
            time.sleep(10)
            
        trnslt_op = "translate_buffer_zero"
        buff_zero = repos.translator.translate(trnslt_op, rsp, repos.pxr)
        repos.update_buffers(buff_zero, 0)

        time.sleep(3)
        setup_for_file_write(repos)
        write_results(output_file, in_file, repos)
        active_row = active_row + 1
        repos.index = repos.index+1
        

        usb.communicate("reset_trip_unit_request")
        usb.communicate_with_check("reset_trip_unit_check")


        
    if repos.pxr == "PXR10" or repos.pxr == "PXR20"  or repos.etu_dictionary['MCU1 Version'] == 2:
        usb.communicate("exit_out_of_auto_test_mode_request")
        usb.communicate("exit_out_of_auto_test_mode_check")

    repos.index = 0
        
    in_file.close_file()



        
'''
=========================================================================================================================================================================================
main loop functions
=========================================================================================================================================================================================
'''
def check_setting_correctness(repos, test_type, usb):

    if repos.cmc_in_use == False:
        if test_type == 'Trip':
            test_type = 'No Test'
            msg = "Trip test can't be run without omicroncron. Skipping"
            repos.append_output_msg(msg)
        elif test_type == 'Meter':
            test_type = 'No Test'
            msg ="Meter test can't be run without omicroncron. Skipping"
            repos.append_output_msg(msg)
        elif test_type == 'Continuous':
            test_type = 'No Test'
            msg = "Continuous test can't be run without omicroncron. Skipping"
            repos.append_output_msg(msg)
        elif test_type == 'Life Point Test':
            test_type = 'No Test'
            msg = "Lifepoint test can't be run without omicroncron. Skipping"
            repos.append_output_msg(msg)

            
    if test_type != 'Trip' and test_type != 'Custom' and test_type != 'Trip With Measure':

        if repos.power == 'Cold Start' or repos.power == 'Aux Only':
            repos.ready_for_test = False
            
            msg = "USB must be enabled for Test Type " + test_type
            repos.append_output_msg(msg)
            test_type = 'No Test'

    return test_type

def enter_into_auto_test_mode(repos, usb, test_type):

    
    if repos.pxr == "PXR10" or repos.pxr == "PXR20" or repos.etu_dictionary['MCU1 Version'] == 2:
            
            usb.communicate("exit_out_of_manufactory_mode_request")
            usb.communicate_with_check("exit_out_of_manufactory_mode_check")
            time.sleep(1)
    
            usb.communicate("enter_into_auto_test_mode_request")
            rsp = usb.communicate_with_check("enter_into_auto_test_mode_check")
            time.sleep(.1)
    
    return test_type


def read_setpoints_from_excel(in_file, repos, active_row):
    i = 0
    for val in in_file.sheet_array:
        key_name = in_file.read_string_from_cell(1,1,i)


        try:
            keys = repos.mapping_dictionary[key_name][0]
        except:
            keys = None

        if key_name == "Inputs":
            test_type = in_file.read_cell(1,active_row,i)
            if test_type == None:
               return test_type
            else:
                values = in_file.read_row_for_length(1, active_row, i, len(repos.expected_keys))
                k = 0
                read_len = min(len(values),len(repos.expected_keys)) #Makes sure it doesn't read to many or too few values from excel
                for k in range(read_len):
                    repos.expected[repos.expected_keys[k]] = values[k]
                    k = k+1 

        elif key_name == "Custom":
            k = 1
            while True:
                key = in_file.read_string_from_cell(k,4,i)
                sp_val = in_file.read_cell(k, active_row, i)


                if sp_val != None and sp_val != '' and sp_val != "None":
                    if key in repos.etu_dictionary:
                        repos.etu_dictionary[key][0] = sp_val
                else:
                    break
                k = k + 1
            
        elif keys != None:
            values = in_file.read_row_for_length(1, active_row, i, len(keys))
            k = 0
            read_len = min(len(values),len(keys)) #Makes sure it doesn't read to many or too few values from excel
            for k in range(read_len):
                repos.etu_dictionary[keys[k]][0] = values[k]
                k = k+1 
        i = i+1
    repos.etu_dictionary['Style1'][0] = repos.static_style_1 
    repos.etu_dictionary['Style2'][0] = repos.static_style_2
    repos.etu_dictionary['Etu Style1'][0] = repos.static_style_1 
    repos.etu_dictionary['Etu Style2'][0] = repos.static_style_2
    repos.etu_dictionary['Frame'][0] = repos.static_frame


    return test_type


def write_setpoints_from_excel(usb, repos, test_type):
    keys = repos.excel_file_tab_names


    #Configuration must be written first since it requires manufactury mode, which cant be done in auto test mode
    if 'Configuration' in keys and repos.more_config != False:
        if repos.pxr == "PXR10" or repos.pxr == "PXR20":
            usb.communicate("exit_out_of_auto_test_mode_request")
            usb.communicate("exit_out_of_auto_test_mode_check")
        
        usb.communicate("enter_into_manufactory_mode_request")
        usb.communicate("enter_into_manufactory_mode_check")
        
        request = repos.mapping_dictionary["Configuration"][1]
        success = write_setpoints_to_trip_unit(usb, request, repos.configuration_keys, repos.etu_dictionary, repos)
        
        usb.communicate("exit_out_of_manufactory_mode_request")
        usb.communicate("exit_out_of_manufactory_mode_check")
        
    for key in keys:
        #Setpoint 1 needs to write the scaled etu_values instead of the actual Setpoint 1 Values

        
        if repos.family == "35":
            rsp = usb.communicate("enter_password_request",0,0,0,0,0,1)
        else:
            rsp = usb.communicate("enter_password_request",0,0,0,0)
            
            
        if key == "Setpoint 1":
            GT_Conversions.convert_standard_to_etu(repos)
            request = repos.mapping_dictionary[key][1]
            sp_keys = repos.mapping_dictionary[key][0]
                
            success = write_setpoints_to_trip_unit(usb, request, repos.sp_etu_keys, repos.etu_dictionary, repos)
            if success == 0:
                return 'No Test'
        else:
            if key in repos.mapping_dictionary:
                request = repos.mapping_dictionary[key][1]
                sp_keys = repos.mapping_dictionary[key][0]

                if key != 'Configuration' and request != "N/A":
                    #rsp = usb.communicate("enter_password_request", 0, 0, 0, 0)
                    success = write_setpoints_to_trip_unit(usb, request, sp_keys, repos.etu_dictionary, repos)
                    if success == 0:
                        return 'No Test'

    return test_type
        

def write_setpoints_to_trip_unit(usb, request, key, dictionary, repos):

    rsp = usb.communicate(request, key, dictionary)
        
    cor = usb.get_correctness(rsp)
    if cor != "successful":
        test_type = 'No Test'
        msg = "Failed To Write. Correctness is " + cor
        repos.append_output_msg(msg)
        return 0

    time.sleep(.01)
    return 1
    
        


def setup_for_file_write(repos):


    clone_key = repos.main_keys
    repos.main_keys = []
    for key in clone_key:
        if key in repos.expected:
            repos.main_keys.append(key)
        elif key in repos.results:
            repos.main_keys.append(key)
        elif key in repos.etu_dictionary:
            repos.main_keys.append(key)
        else:
            key = fix_string(key)
            if key in repos.expected:
                repos.main_keys.append(key)
            elif key in repos.results:
                repos.main_keys.append(key)
            else:
                repos.main_keys.append(key)      
    
    for key in repos.main_keys:
        print(key)
        if key in repos.expected:
            repos.main_dict[key] = repos.expected[key]
        elif key in repos.results:
            repos.main_dict[key] = repos.results[key]
        elif key in repos.etu_dictionary:
            repos.main_dict[key] = repos.etu_dictionary[key][0]
        else:
            key = fix_string(key)
            if key in repos.expected:
                repos.main_dict[key] = repos.expected[key]
            elif key in repos.results:
                repos.main_dict[key] = repos.results[key]
            else:
                repos.main_dict[key] = repos.etu_dictionary[key][0]

        

    if repos.results['Trip Time'] == -1:
        repos.results['Trip Time']        = "No Trip" 
        repos.results['Trip Time + Mech'] = "No Trip"


    if repos.expected['Max Time'] == -1:
        repos.main_dict['Max Time'] = "No Trip"
    if repos.expected['Min Time'] == -1:
        repos.main_dict['Min Time'] = "No Trip"


    
    if 'LD PU' in repos.main_keys:
        if repos.family != "MCCB": 
            per_unit = repos.etu_dictionary['LD PU'][0]*repos.etu_dictionary['Rating'][0]/100
        else:
            per_unit = repos.etu_dictionary['LD PU'][0]
    elif 'Source Ground Sensor' in repos.main_keys:
        per_unit = (repos.etu_dictionary['Source Ground Sensor'][0]-1)/2
    else:
        per_unit = repos.etu_dictionary['Rating'][0]
        
    repos.main_dict['I A (PU)'] = repos.expected['I A (Amps)']/per_unit

        
def fix_string(val): #Update old formate word1_word2_word3 to Word1 Word2 Word3

    old_string = val
    space_location = 0
    more = True

    new_string = old_string.capitalize() #Capitalize First Letter
    new_string = new_string.replace("_", " ") #Replace "_" With " "
    
    #Capitalize every letter after " "
    while more: 
        
        space_location = new_string.find(" ", space_location + 1) 
        print(space_location)

        if space_location == -1:
            break
        else:
            new_string = new_string[:space_location+1] + new_string[space_location+1].swapcase() + new_string[space_location+2:]

    print(new_string)   
    return new_string
    
def write_results(output_file, in_file, repos):
    index = repos.index +5
    i = 0 #input tab
    j = 0 #output tab
    output_file.get_tabs
    for val in output_file.sheet_array:
        key_name = output_file.read_string_from_cell(5,1,i)
        try:
            keys = repos.mapping_dictionary[key_name][0]
            if key_name == "Setpoint 1":
                keys = repos.sp_one_keys
        except:
            keys = None
            
        if i == 0:
            output_file.write_cell(1, index, i, index-5)
            print(repos.main_keys)
            output_file.write_row_with_dictionary(2, index, j, repos.main_keys, repos.main_dict)
            output_file.write_row_with_dictionary(len(repos.main_keys)+2, index, j, repos.results_keys, repos.results)
            j = j + 1

        elif keys != None and key_name != "Inputs":
            k = 0
            for k in range(len(keys)):
                output_file.write_cell(1, index, j, index-5)
                output_file.write_cell(k+2, index, j, repos.etu_dictionary[keys[k]][0])

            j = j+1
        i = i+1

    
    output_file.save_file()      
        


    

    
'''
=========================================================================================================================================================================================
Test Functions With Omicron
=========================================================================================================================================================================================
'''

def run_trip_test(repos, usb, omicron):              #   run test
    
    t_wd = setup_trip_times(repos)
    
    trip = False
    current_read = False

    if repos.power == 'Cold Start':
        GT_System_Control.all_off(omicron, usb)
        time.sleep(5)
        

    int_time = time.time()
    t = time.time() - int_time
    
    omicron.setup_for_trip()
    omicron.setup_omicron(repos)
    omicron.omicron_on()


        
        
    while (trip == False and t <= t_wd and t_wd >= 0):    #  trip test loop                                  
        if t>(t_wd/2) and repos.power != 'Cold Start' and current_read == False: 
            read_currents(repos, usb)
            current_read = True

        t = time.time() - int_time
        trip = omicron.check_for_trip()


    omicron.end_trip()
    trip_time =  overflow_calc(t, omicron)
    
    if repos.power == 'Cold Start':
        usb.turn_on_port()
        #GT_System_Control.all_on(omicron, usb)
        time.sleep(1)


    
    store_trip_results(repos, trip_time)

    msg = "Trip Time " + str(trip_time)
    repos.append_output_msg(msg)
    

def run_with_measurment(repos, usb, omicron):


    t_wd = 7
    
    trip = False
    current_read = False

    

    time.sleep(.1)
    print("HI")
    usb.communicate("enter_into_manufactory_mode_request")
    time.sleep(.1)
    print("SPY")
    rsp = usb.communicate("enter_into_manufactory_mode_check")
    time.sleep(.1)
    print("Bye")

            
    int_time = time.time()
    t = time.time() - int_time
    
    omicron.setup_for_trip()
    omicron.setup_omicron(repos)
    omicron.omicron_on()
    
    while t <= t_wd:    #  trip test loop                                  
        if t > 4 and current_read == False: 
            read_currents(repos, usb)
            current_read = True

        t = time.time() - int_time

    
    omicron.end_trip()
    usb.communicate("exit_out_of_manufactory_mode_request")
    time.sleep(.1)
    usb.communicate_with_check("exit_out_of_manufactory_mode_check")
    
 
    run_trip_test(repos, usb, omicron)
    

        
def run_undervolt_trip_test(repos, usb, omicron):              #   run test
    
    test_type = "U_Voltage"

    repos.etu_dictionary['Under V Type'][0] = 0
    t_wd = omicron.setup_omicron(repos)
        
    omicron.write_omicron_voltage(200, 0, 60, 1)
    omicron.write_omicron_voltage(200, 120, 60, 2)
    omicron.write_omicron_voltage(200, -120, 60, 3)

    omicron.omicron_on()


    rsp = usb.communicate("write_setpoint_five_request", repos.sp_five_keys, repos.etu_dictionary)
    run_trip_test(repos, usb, omicron)
    
    repos.etu_dictionary['Under V Type'][0] = 2
    rsp = usb.communicate("write_setpoint_five_request", repos.sp_five_keys, repos.etu_dictionary)

    
def run_meter_test(repos, omicron):
    repos.clr_flags()                  #  clear test flags

    repos.t_max = repos.time_values[0]        #  save t_max into repos test case
    repos.t_min = repos.time_values[1]        #  save t_min into repos test case
    

    GT_omicroncron.meter_test(repos)
    repos.results['result'] = GT_Calculations.metering_result(repos.results, repos.expected, repos.my_UI)

        
def run_continuous_meter_test(repos, omicron):

    if repos.index == 0:
        omicron.omicroncron_on()
    
    repos.t_max = repos.time_values[0]        #  save t_max into repos test case
    repos.t_min = repos.time_values[1]        #  save t_min into repos test case
    
    omicron.continuous_meter_test(repos)

    repos.results['result'] = GT_Calculations.metering_result(repos.results, repos.expected, repos.my_UI)

def run_acb_health_test(repos, usb, omicron):

    omicron.setup_for_trip()
    omicron.setup_omicron(repos)

    
    usb.communicate("reset_all_internal_diagnostics_request")
    rsp = usb.communicate_with_check("reset_all_internal_diagnostics_check")
    usb.communicate("reset_all_diagnostics_request")
    rsp = usb.communicate_with_check("reset_all_diagnostics_check")

    usb.communicate("enter_into_manufactory_mode_request")
    usb.communicate_with_check("enter_into_manufactory_mode_check")

    omicron.omicron_on()
    time.sleep(5)
    read_currents(repos, usb)
    omicron.omicron_off()
    
    usb.communicate("exit_out_of_manufactory_mode_request")
    usb.communicate_with_check("exit_out_of_manufactory_mode_check")

    run_trip_test(repos, usb, omicron)

    time.sleep(10)

    rsp = usb.communicate("read_real_time_data_buffer_six_request")
    rsp = usb.communicate("read_real_time_data_buffer_fourty_two_request")
    rsp = usb.communicate("read_real_time_data_buffer_fourty_three_request")

    repos.translator.translate_generic(rsp, repos.buffer_fourty_two_keys, repos.etu_dictionary)
    repos.translator.translate_generic(rsp, repos.buffer_fourty_two_keys, repos.etu_dictionary)
##    rsp = usb.communicate("read_real_time_internal_breaker_health_request")
##    repos.translator.translate_generic(rsp, buffer_fourty_three, repos.etu_dictionary)


  
def run_life_point_test(repos, omicron):

    repos.life_point_test = 1
    
    t_max, t_min, repos.no_trip_case = GT_Calculations.calc_max_min_time(repos) #Calc max an min time
    repos.t_max = t_max        #  save t_max into repos test case
    repos.t_min = t_min       #  save t_min into repos test case
    repos.expected['Max Time'] = t_max
    repos.expected['Min Time'] = t_min

    repos.t_min = repos.time_values[1]        #  save t_min into repos test case
    

    msg = usb.communication("write_group_one")
    cor = usb.get_correctness(msg)
    if cor == "successful":
        repos.ready_for_test = True

    if repos.ready_for_test: 
        t_trip = omicron.single_phase_trip_test(repos)  
            
        repos.t_trip = t_trip      #  save trip time to repos test case
        repos.t_adj = t_trip + repos.mech_time

        repos.results['result'] = GT_Calculations.trip_result(repos)
        
        store_trip_results(repos, result) 

    else:
        repos.results['result'] = "Invalid"


def run_zsi(repos, usb, omicron, i):

    relay = in_file.read_from_cell(1, i ,2)
    
    if relay == 0:
        write_bin_out_off(self, 1)
    else:
        write_bin_out_on(self, 1)
        
    run_trip_test(repos, usb, omicron)
    

'''
=========================================================================================================================================================================================
Test Functions Secondary Injection
=========================================================================================================================================================================================
run_hardware_meter_test(repos, usb)
run_firmware_meter_test(repos, usb)
run_firmware_trip_test(repos, usb)
run_hardware_trip_test(repos, usb)
run_firmware_without_trip_test(repos, usb)
run_hardware_without_trip_test(repos, usb)
run_life_point_secondary_test(repos, usb)
'''


def run_hardware_meter_test(repos, usb):

    start = "secondary_injection_rms_test_without_trip_request"
    check = "secondary_injection_rms_test_without_trip_check"
    cancel = "cancel_software_test_request"
    
    repos.t_max = repos.time_values[0]        #  save t_max into repos test case
    repos.t_min = repos.time_values[1]        #  save t_min into repos test case
    
    GT_Secondary_Injection.secondary_meter(repos, usb, start, check, cancel)

    repos.results['result'] = GT_Calculations.metering_result(repos.results, repos.expected, repos.my_UI)


def run_firmware_meter_test(repos, usb):

    start = "software_rms_test_without_trip_request"
    check = "software_rms_test_without_trip_check"
    cancel = "cancel_secondary_injection_test_request"
    

    repos.t_max = repos.time_values[0]        #  save t_max into repos test case
    repos.t_min = repos.time_values[1]        #  save t_min into repos test case
    
    GT_Secondary_Injection.secondary_meter(repos, usb, start, check, cancel)

    repos.results['result'] = GT_Calculations.metering_result(repos.results, repos.expected, repos.my_UI)

    
def run_firmware_trip_test(repos, usb):              
    
    setup_secondary(repos, usb)  #calculates min/max times and updates setpoints
    
    
    start = "software_rms_test_with_trip_request"
    check = "software_rms_test_with_trip_check"
    cancel = "cancel_software_test_request"
    cancel_check = "cancel_software_test_check"  

    if repos.family == "35":
        check = "read_simulated_test_results_request"


        
    results = GT_Secondary_Injection.secondary_time(repos, usb, start, check, cancel, cancel_check)
    review_secondary(repos, results)
     

    
def run_hardware_trip_test(repos, usb):             
    
    setup_secondary(repos, usb)  #calculates min/max times and updates setpoints


    start  = "secondary_injection_rms_test_with_trip_request"
    check  = "secondary_injection_rms_test_with_trip_check"
    cancel = "cancel_secondary_injection_test_request"
    cancel_check = "cancel_secondary_injection_test_check"
    
    if repos.family == "35":
        check = "read_simulated_test_results_request"


    
    results = GT_Secondary_Injection.secondary_time(repos, usb, start, check, cancel, cancel_check)
    review_secondary(repos, results)



def run_firmware_without_trip_test(repos, usb):              
    
    setup_secondary(repos, usb)
    
    start  = "software_rms_test_without_trip_request"
    check  = "software_rms_test_without_trip_check"
    cancel = "cancel_software_test_request"
    cancel_check = "cancel_software_test_check"  

    if repos.family == "35":
        check = "read_simulated_test_results_request"

        
    results = GT_Secondary_Injection.secondary_time(repos, usb, start, check, cancel, cancel_check)
    review_secondary(repos, results)

 
    
def run_hardware_without_trip_test(repos, usb):              
    
    setup_secondary(repos, usb) #calculates min/max times and updates setpoints

    start = "secondary_injection_rms_test_without_trip_request"
    check = "secondary_injection_rms_test_without_trip_check"
    cancel = "cancel_secondary_injection_test_request"
    cancel_check = "cancel_secondary_injection_test_check"

    if repos.family == "35":
        check = "read_simulated_test_results_request"
    
    results = GT_Secondary_Injection.secondary_time(repos, usb, start, check, cancel, cancel_check)
    review_secondary(repos, results)
    
 

        
def run_life_point_secondary_test(repos, usb):

    setup_secondary(repos, usb) #calculates min/max times and updates setpoints
    
    if repos.ready_for_test: 
        t_trip = GT_Secondary_Injection.firmware_life_point(repos, usb)    
        repos.t_trip = t_trip      #  save trip time to repos test case
        repos.t_adj = t_trip  #there is no mechanical trip time that needs to be added for secondary injection
        
        repos.results['result'] = GT_Calculations.trip_result(repos) #Calculates pass/fail
        
    else:
        repos.results['result'] = "Invalid"



def run_hardware_maint_trip_test(repos, usb):             
    
    setup_secondary(repos, usb)  #calculates min/max times and updates setpoints
    
    usb.communicate("enter_into_manufactory_mode_request")
    usb.communicate("enter_into_manufactory_mode_check")
    
    repos.expected['Max Time'] = 1
    
    start  = "secondary_injection_rms_test_with_trip_request"
    check  = "secondary_injection_rms_test_with_trip_check"
    cancel = "cancel_secondary_injection_test_request"
    cancel_check = "cancel_secondary_injection_test_check"
    
    if repos.family == "35":
        check = "read_simulated_test_results_request"


    
    results = GT_Secondary_Injection.secondary_time(repos, usb, start, check, cancel, cancel_check)
    review_secondary(repos, results)
        
'''
==============================================================================================================
Test Functions Misc.
==============================================================================================================
'''



def run_custom_test(repos, usb, omicron):


    usb.turn_off_port()
    omicron.setup_for_trip()
    omicron.omicron_on()
    I_progression = [.1, .15, .2, .1, .3, .15, .1, .2, .25, 0, .15, 0, .3, 0, .15, 0, .3, 0, .1, .3, .2, .1, .2, .15, .18, .15, 0, .15, .3]
    j = 0
    trip = False
    while trip == False:    #  trip test loop

        time.sleep(.2)
        I_out = I_progression[j] 
        omicron.write_omicron_current(I_out, 0, 60, 1)
        omicron.write_omicron_current(I_out, 0, 60, 2)
        omicron.write_omicron_current(I_out, 0, 60, 3)
        omicron.omicron_on()
        trip = omicron.check_for_trip()
        j = j + 1
        if j >= len(I_progression):
            j = 0
        
        
    usb.turn_on_port()
    omicron.end_trip()
    trip_time =  overflow_calc(t, omicron)    
    store_trip_results(repos, trip_time)

    msg = "Trip Time " + str(trip_time)
    repos.append_output_msg(msg)
    


def run_source_ground_trip(repos, usb, omicron):

    t_wd = setup_trip_times(repos)  

    omicron.setup_for_trip()
    setup_source_ground(repos, usb, omicron)
    
    trip = False
    current_read = False
    int_time = time.time()
    t = time.time() - int_time

    omicron.omicron_on()

    t_wd = repos.expected['Max Time'] + 1.5
    
    while (trip == False and t <= t_wd and t_wd >= 0):    #  trip test loop                                  
        if t>1 and repos.power != 'Cold Start' and current_read == False: 
            #read_currents(repos, usb)
            current_read = True

        t = time.time() - int_time
        trip = omicron.check_for_trip()
    

    omicron.end_trip()
    trip_time =  overflow_calc(t, omicron)    
    store_trip_results(repos, trip_time)

    time.sleep(2)




    msg = "Trip Time " + str(trip_time)
    repos.append_output_msg(msg)

    
   
def run_source_ground_meter(repos, in_file, report, usb, omicron):


    
    #omicron.setup_omicron(repos)
    test_current = [.025, .05, .075, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1,
                    1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2]
    i = 0

    buf_one_array = []
    buf_ten_array = []
    cur_array = []

    for current in test_current:

        omicron.setup_voltage(repos)
        omicron.set_omicron_currents([current, 60, 0], [0, 60, 0], [0, 60, 0])
        omicron.set_omicron_rowgowskis([0, 60, 0], [0, 60, 0], [0, 60, 0])
        omicron.write_omicron_rowgowski(repos)
        omicron.write_omicron_current(repos)
        omicron.omicron_on()
        time.sleep(4)

        rsp = usb.communicate("read_real_time_data_buffer_one_request")
        array = repos.translator.translate_buffer_one(rsp)
        buf_one_array.append(array[4])

        
        rsp = usb.communicate("read_real_time_data_buffer_ten_request")
        array = repos.translator.translate_buffer_ten(rsp)
        buf_ten_array.append(array[4])

        cur_array.append(current)        
        
        omicron.omicron_off()
        omicron.write_omicron_voltage(0, 0, 60, 1)
        omicron.write_omicron_voltage(0, 0, 60, 2)
        omicron.write_omicron_voltage(0, 0, 60, 3)
        

        

    k = 0
    write_array = [0, 0, 0]
    for val in cur_array:
        write_array[0] = cur_array[k]
        write_array[1] = buf_one_array[k]
        write_array[2] = buf_ten_array[k]
        report.value(k, write_array)
        k = k+1
        
    
def run_no_test(repos):


    repos.results['Trip Time']  = -1
    repos.results['Trip Time + Mech']   = -1
    repos.results['Result'] = "No Test Was Run!!!"
    
    repos.ready_for_test = False


'''
======================================================================================================================
Methods used to assist the "Source Ground"
=======================================================================================================================
'''
def setup_source_ground(repos, usb, omicron):

        a = repos.expected['I A (Amps)']

        if repos.family == "35":
             source_ground_sensor = ((repos.etu_dictionary['SG Sensor'][0]-1)/2)
        else:
            source_ground_sensor = ((repos.etu_dictionary['Source Ground Sensor'][0]-1)/2)

        output_current = a/(source_ground_sensor*10)

        if output_current > .5:
            output_current = .5

        print("Source Ground Sensor" + str(source_ground_sensor))
        print("Current is " + str(a))
        print("Output Current " + str(output_current))
        omicron.write_omicron_current(output_current, 0, 60, 1)
        omicron.write_omicron_current(0, 0, 60, 2)
        omicron.write_omicron_current(0, 0, 60, 3)
        omicron.write_omicron_rowgowski(0, 0, 60, 1)
        omicron.write_omicron_rowgowski(0, 0, 60, 2)
        omicron.write_omicron_rowgowski(0, 0, 60, 3)
        omicron.write_omicron_voltage(0, 0, 60, 1)
        omicron.write_omicron_voltage(0, 0, 60, 2)
        omicron.write_omicron_voltage(0, 0, 60, 3)
        

        gfpu =  repos.etu_dictionary['GF PU'][0]
        t_gf =  repos.etu_dictionary['GF Time'][0]
        gfs =  repos.etu_dictionary['GF Slope'][0]      
        pu = a/(source_ground_sensor)
        
        if gfs == 1:
            gfs = 2
        

        if a > gfpu*source_ground_sensor*1.05:
            repos.expected['Max Time'] = ((.67/pu)**(gfs))*t_gf
        else:
            repos.expected['Max Time'] =  repos.etu_dictionary['GF Time'][0] + 1
            repos.no_trip_case = True
            

        if a > gfpu* source_ground_sensor *.95:
            repos.expected['Min Time'] = ((.67/pu)**(gfs))*t_gf 
            if t_gf >= .2:
                repos.expected['Min Time']  = repos.expected['Min Time'] * .8
            elif t_gf >= .16:
                repos.expected['Min Time']  = repos.expected['Min Time'] * .7
            else:
                repos.expected['Min Time']  = repos.expected['Min Time'] * .6

                
        else:
            repos.expected['Min Time'] = -1
            repos.no_trip_case = True


'''
======================================================================================================================
Methods used to assist the "Run Test" methods
=======================================================================================================================
setup_trip_times(repos) Calculates the Max and Min Expected Trip Times
    Inputs
        repos(Object) - Used for the dictionary and calculations
    Changes
        repos.expected['Max Time'](int) - Max allowed time used to check pass/fail
        repos.expected['Min Time'](int) - Min allowed time used to check pass/fail
        repos.no_trip_case - Case to check if no trip should occur during test
    Outputs
        t_wd(int) - Watchdog Time. Stops the Test once the Watchdog Time is reached

setup_secondary(repos, usb) Calculates the Max/Min Times and Recalibrates if needed
    Inputs
        repos(Object) - Used for the dictionary and calculations
    Changes
        Calibration Values - Calls Calibration Routine
    Outputs
        N/A
        
review_secondary(repos, results)

overflow_calc(t, omicron)
def bad_check(repos)
phase_choices(repos)
'''


def setup_trip_times(repos):

    t_max, t_min, repos.no_trip_case = GT_Calculations.calc_max_min_time(repos) #Calc max an min time
    repos.expected['Max Time'] = t_max
    repos.expected['Min Time'] = t_min
        
    if repos.no_trip_case == True:
        repos.expected['Max Time'] = -1
        
    msg = "Max Time Should Be " + str(t_max)
    repos.append_output_msg(msg)
    msg = "Min Time Should Be " + str(t_min)
    repos.append_output_msg(msg)

    phase_choices(repos)
    
    if repos.expected['Max Time'] == -1 and t_min != -1:
        t_wd = (repos.expected['Min Time']+2)*1.2
    else:
        t_wd = (t_max+2)*1.2
        
    return t_wd

def setup_secondary(repos, usb):

    setup_trip_times(repos)

    if repos.re_cal_needed:
        repos.re_cal_needed = False
        
        if repos.pxr == "PXR10" or repos.pxr == "PXR20"  or repos.etu_dictionary['MCU1 Version'] == 2:
            usb.communicate("exit_out_of_auto_test_mode_request")
            usb.communicate("exit_out_of_auto_test_mode_check")
            
        #GT_Calibration.calibrate_secondary_injection(repos, usb)

        if repos.pxr == "PXR10" or repos.pxr == "PXR20"  or repos.etu_dictionary['MCU1 Version'] == 2:
            enter_into_auto_test_mode(repos, usb, "SECONDARY")
            write_setpoints_from_excel(usb, repos, "SECONDARY")

        
        time.sleep(15)




def review_secondary(repos, results):

    I = max(repos.expected['I A (Amps)'], repos.expected['I B (Amps)'], repos.expected['I C (Amps)'])
    
    if results != None:
        trip_time, current, cause_of_trip =  GT_Secondary_Injection.translate_secondary_results(results)

        repos.results['Trip Time']  = trip_time
        repos.results['Trip Time + Mech']   = trip_time
        cur_val = current
        

    else:
        
        
        repos.results['Trip Time']  = -1
        repos.results['Trip Time + Mech']   = -1
        cur_val = I
        

    repos.results['Result'] = GT_Calculations.trip_result(repos)


    
    
    if I == repos.expected['I A (Amps)']:
        repos.etu_dictionary['external_Ia'][0] = cur_val
        repos.etu_dictionary['external_Ib'][0] = 0
        repos.etu_dictionary['external_Ic'][0] = 0
    elif I == repos.expected['I B (Amps)']:
        repos.etu_dictionary['external_Ia'][0] = 0
        repos.etu_dictionary['external_Ib'][0] = cur_val
        repos.etu_dictionary['external_Ic'][0] = 0
    else:
        repos.etu_dictionary['external_Ia'][0] = 0
        repos.etu_dictionary['external_Ib'][0] = 0
        repos.etu_dictionary['external_Ic'][0] = cur_val

    

def overflow_calc(t, omicron):
    
    seconds = 28 * 60
    overflow_count = math.floor(t/seconds)
    additional_time = 28 * 60 * overflow_count
    print("Additional Time")
    print(additional_time)
    trip_time = omicron.input_buffer()
    print("Trip Time")
    print(trip_time)
    trip_time = trip_time + additional_time

    return trip_time
    
def store_trip_results(repos, trip_time):

    repos.results['Trip Time']  = trip_time
    repos.results['Trip Time + Mech']   = trip_time + repos.mech_time
    repos.results['Result'] = GT_Calculations.trip_result(repos)


def store_meter_results(repos):

    repos.results['t_trip']  = -1
    repos.results['t_adj']   = -1


    if repos.no_trip_case == True:
        repos.expected['Max Time'] = -1

def change_power(repos, usb, omicron):

    if repos.power == 'USB Only' or repos.power == 'Cold Start':
        omicron.omi_aux_off()
        time.sleep(1)
    if repos.power == 'Aux Only' or repos.power == 'Cold Start':
        usb.close_port()
        time.sleep(1)
        usb.turn_off_port()
        time.sleep(2)
        
def return_power(repos, usb, omicron):

        if repos.power == 'USB Only' or repos.power == 'Cold Start':
            omicron.omi_aux_on()
            time.sleep(1)

        if repos.power == 'Aux Only' or repos.power == 'Cold Start':
            usb.turn_on_port()
            time.sleep(2)
            usb.open_port()
            time.sleep(1)

def read_currents(repos, usb): 

    if repos.family == "35":
        rsp = usb.communicate("read_real_time_data_buffer_fourty_eight_request")
        array = repos.translator.translate_generic(rsp, repos.buffer_fourty_eight_keys, repos.etu_dictionary)
        #repos.update_buffers(array, 48)
        rsp = usb.communicate("read_real_time_data_buffer_fifty_five_request")
        array = repos.translator.translate_generic(rsp, repos.buffer_fifty_five_keys, repos.etu_dictionary)
        #repos.update_buffers(array, 55)
        
    else: 
        rsp = usb.communicate("read_real_time_data_buffer_one_request")
        array = repos.translator.translate_generic(rsp, repos.buffer_one_keys, repos.etu_dictionary)
    #repos.update_buffers(array, 1)
    
##    rsp = usb.communicate("read_real_time_data_buffer_ten_request")
##    array = repos.translator.translate_buffer_ten(rsp)
##    repos.update_buffers(array, 10)
            
def check(repos):                  #  print mid test report check

    
    msg = ("\n\nIndex:" + str(repos.index)
          + "\n  t_max = " + str(repos.expected['Max Time'])
          + "\n  t_min = "  + str(repos.expected['Min Time'])
          + "\n  t_trip = " + str(repos.results['Trip Time + Mech'])
          + "\n" + str(repos.results['Result']))
    
    repos.append_output_msg(msg)

def bad_check(repos):                  #  print mid test report check

    msg = ("\n\nIndex:" + str(repos.index)
          +"\n" + repos.failure_mode)

    
    repos.append_output_msg(msg)


def phase_choices(repos):
        A_phase = repos.phases.find('A')
        B_phase = repos.phases.find('B')
        C_phase = repos.phases.find('C')
        
        if A_phase == -1:
            repos.expected['I A (Amps)'] = 0
            repos.expected['I A (PU)'] = 0


        if B_phase == -1:
            repos.expected['I B (Amps)'] = 0
            repos.expected['I B (PU)'] = 0


        if C_phase == -1:
            repos.expected['I C (Amps)'] = 0
            repos.expected['I C (PU)'] = 0

    
