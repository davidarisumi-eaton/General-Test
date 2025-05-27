'''---------------------------------------------------------------------
    
    Company:        EATON COROPORATION
            
                    Proprietary Information
                    (C) Copyright 2016
                    All rights reserved
                
                    PXR MCCB Automation - Protection  
    
------------------------------------------------------------------------
    
    Authors:        David Arisumi                (
                    Eaton Corporation
                    1000 Cherrington Parkway
                    Moon Twp, PA 15108-4312
                    (412) 893-3300
                
-------------------------------------------------------------------
-----
        
    Product:        Automated test system to test the PXR10, PXR20, 
                    PXR2D, PXR25, and PXR35 protection algorithms for 
                    the SR, NZM, and NRX breaker frames.   
                
    Module:         Main.py
                
    Mechanics:      main program module containing the primary foreground 
                    execution routines:
                    
                    defines test groups
                    builds master/data objects
                    executes test routine 
                    generates test report
            
---------------------------------------------------------------------'''

from __future__ import division
import traceback, math, os



import os

import os.path
from os import path

from queue import *

import threading

from GT import GT_Test, GT_USB, GT_Calibration, GT_Conversions
from GT import GT_Excel_Interface, GT_Repository, GT_System_Control

import time #for testing purposes


'''
Functions when using General Test with an UI. 
'''




def run_from_bamboo(repos, save_dir, test_group, omicron, usb):


    repos.phases          = "A"
    repos.power           = "All Power"
    repos.etu_dictionary["Ia_Phase_Angle"][0]         = 0
    repos.etu_dictionary["Ib_Phase_Angle"][0]         = 120
    repos.etu_dictionary["Ic_Phase_Angle"][0]         = -120
    repos.etu_dictionary["Ra_Phase_Angle"][0]         = 90
    repos.etu_dictionary["Rb_Phase_Angle"][0]         = 90
    repos.etu_dictionary["Rc_Phase_Angle"][0]         = 90
    repos.etu_dictionary["Va_Phase_Angle"][0]         = 0
    repos.etu_dictionary["Vb_Phase_Angle"][0]         = 120
    repos.etu_dictionary["Vc_Phase_Angle"][0]         = -120
    repos.cmc_in_use      = False
    repos.neutral         = "No Neutral" 
    repos.UI_test_type    = "Firmware" #["Trip", "Firmware Test", "Hardware Test", "Excel"]
    repos.num_runs        = 1
    repos.frequency       = 60    

    get_breaker_inputs(repos, usb) #Gets default values from breaker

    j = 0
    for i in range(0, len(test_group)):    #  program loop

        in_file, part_file = create_test_file(test_group[i])

        
        update_frame_and_rating(repos, usb, in_file, omicron)
        update_config(repos, in_file, usb)
        
        report = create_report_file(part_file, save_dir, j)
        get_headings(repos, in_file)    
        write_headings(repos, report)
        
        update_omicron_ratios(repos, omicron)
        GT_System_Control.power_cycle(omicron, usb)
        
        try:
            GT_Test.main(repos, in_file, report, usb, omicron)  #  run test routine
        except Exception as err:
            traceback.print_exc()
            x = input('Press Enter to Continue...')
            cleanup(repos, usb, omicron, in_file)
            quit()

        i += 1
        reset_excel_file_info(repos) 
        
    cleanup(repos, usb, omicron, in_file)
    
    
def run_from_ui(UI, repos, save_dir, test_group, omicron, usb):         

    'Setup Methods'
    get_UI_inputs(repos, UI, omicron) 

    
    '1st foor loop is to repeat tests as specified by user'
    for j in range(0, repos.num_runs):      
        '2nd for loop is to read through all input files' 
        for i in range(0, len(test_group)):    

            in_file, part_file = create_test_file(test_group[i])

            
            update_frame_and_rating(repos, usb, in_file, omicron)
            update_config(repos, in_file, usb)
            

            report = create_report_file(part_file, save_dir, j)
            get_headings(repos, in_file)    
            write_headings(repos, report)
            
            update_omicron_ratios(repos, omicron)
            GT_System_Control.power_cycle(omicron, usb)
            get_breaker_inputs(repos, usb) 
            
            try:
                GT_Test.main(repos, in_file, report, usb, omicron)  #  run test routine
            except Exception as err:
                traceback.print_exc()
                x = input('Press Enter to Continue...')
                cleanup(repos, usb, omicron, in_file)
                quit()

            i += 1
            reset_excel_file_info(repos)
            UI.print_msgs(repos, part_file)


    cleanup(repos, usb, omicron, in_file)
    UI.test_running = False
    repos.append_output_msg("All Tests Completed")
    



'''
=============================================================================================================
Shared functions that any main could use.
===========================================================================================================

def create_report_file(full_file) Sets the file name as an object and creates a name
    Inputs:
        full_file(String) - name of the file being tested (path/name.ext)
    Changes:
        N/A
    Outputs:
        in_file(object) - excel file object that the program reads from 
        part_file(String) - String of the name of the fiel
        
def create_test_file(full_file) Sets the file name as an object and creates a name
    Inputs:
        full_file(String) - name of the file being tested (path/name.ext)
    Changes:
        N/A
    Outputs:
        in_file(object) - excel file object that the program reads from 
        part_file(String) - String of the name of the fiel



def get_headings(repos, in_file): Reads tabs, setpoints and main info and saves it to be used when creating the output file 
    Inputs:
        repos(object) - repository that holds setpoints/data/info
        in_file(object) - excel file object that the program reads from 
    Changes:
        repos.excel_file_tab_names(array) - array of all tab names in the read excel sheet
        repos.main_keys(array) - array of keys that will be used on the main tab of the output excel file
    Outputs:
        N/A

        
def write_headings(repos, report): using info from "def get_headings" creates new tabs and labels them
    Inputs:
        reps(object) - repository that holds setpoints/data/info
        report - excel file object that results will be written to
    Changes:
        output_file(object) - Excel file that records info
    Outputs:
        N/A


def update_omicron_ratios(repos, omicron) writes roogowski/ct ratio that omicron uses in calculation to output current
    Inputs:
        repos(object) - repository that holds setpoints/data/info
        omicron(object) - power source object that outputs current/voltage/detects trips
    Changes:
        row_ratio(int) - ratio in which the omicron converts the input current to the output llo voltage
        ct_ratio(int) - ratio in which the omicorn converts the input current to the output current
        ph(int) - whether or not the current output should be adjusted as power harvesting current
        ph_type(int) - choice for which current power harvesting equation should be used
    Outputs:
        N/A
        
def get_breaker_inputs(repos, usb)
    Inputs:
        repos(object) - repository that holds setpoints/data/info
        usb(object) - usb object that communicates with the trip unit
    Changes:
        repos.static_style_1(int) - style 1 of the trip unit. Used to overwrite the test file style 1 since it may be inaccurate
        repos.static_style_2(int) - style 2 of the trip unit. Used to overwrite the test file style 2 since it may be inaccurat
    Outputs:
        N/A
        
def update_frame_and_rating(repos, usb, in_file, omicron) Reads the frame and rating from the test file and writes it to the trip unit
    Inputs:
        repos(object) - repository that holds setpoints/data/info
        usb(object) - usb object that communicates with the trip unit
    Changes:
        repos.etu_dictionary['Frame'][0](int)  = trip unit frame 
        repos.etu_dictionary['Rating'][0](int) = trip unit rating
        trip unit frame(external) - frame on the firmware of the trip unit
        trip unit rating(external) - rating on the firmware of the trip unit
    Outputs:
        N/A
        
def cleanup(repos, usb, omicron, in_file) closes test file, exits out of "Test Mode" for pxr10s and 20s and unlocks omicron. 
    Inputs:
        repos(object) - repository that holds setpoints/data/info
        usb(object) - usb object that communicates with the trip unit
    Changes:
        in_file.close_file()
        testmode(external) - Trip units test mode option
        omicron_locked(external) - Blocks the omicron from being used by two different programs
    Outputs:
        N/A
        
def reset_excel_file_info(repos):
    Inputs:
        N/A
    Changes:
        repos.excel_file_tab_names(array) - array of all tab names in the read excel sheet
        repos.main_keys(array) - array of keys that will be used on the main tab of the output excel file
        repos.main_dict(dictionary) - dictionary with all the values displayed on the main tab of the output file


    Outputs:
        N/A

'''


def get_UI_inputs(repos, UI, omicron):    	    #  Gets values from the user interface 
    

    repos.phases     = UI.get_phase()
    repos.power      = UI.get_power()
    repos.etu_dictionary["Ia_Phase_Angle"][0]     = UI.get_ia_ang()
    repos.etu_dictionary["Ib_Phase_Angle"][0]     = UI.get_ib_ang()
    repos.etu_dictionary["Ic_Phase_Angle"][0]     = UI.get_ic_ang()
    repos.etu_dictionary["Ra_Phase_Angle"][0]     = UI.get_ra_ang()
    repos.etu_dictionary["Rb_Phase_Angle"][0]     = UI.get_rb_ang()
    repos.etu_dictionary["Rc_Phase_Angle"][0]     = UI.get_rc_ang()
    repos.etu_dictionary["Va_Phase_Angle"][0]     = UI.get_ia_ang()
    repos.etu_dictionary["Vb_Phase_Angle"][0]     = UI.get_ib_ang()
    repos.etu_dictionary["Vc_Phase_Angle"][0]     = UI.get_ic_ang()
    repos.neutral    = UI.get_neutral()  
    repos.UI_test_type    = UI.get_test_type()


    'Sets the number of runs based on the UI.'
    'If the value is invalid, it sets it to a default 1'    
    num = UI.get_num_runs()
    try:
        repos.num_runs = int(num)
    except:
        UI.write_results("Invalid number of runs. Resetting to 1")
        repos.num_runs = 1


    'Sets the frequency based on the UI.'
    'If the value is invalid, it sets it to a default 60Hz'
    freq = UI.get_freq()
    try:
        repos.etu_dictionary["Source_Freq"][0] = int(freq)
    except:
        UI.write_results("Invalid frequency. Resetting to 60")
        repos.etu_dictionary["Source_Freq"][0] = 60


def create_report_file(part_file, save_dir, j):

        
        report = GT_Excel_Interface.Test_File("Write")
        try: 
            report.name_file_std_method(part_file, save_dir, j)
        except:
            j = j + 1
            report.name_file_std_method(part_file, save_dir, j)

        return report
    
def create_test_file(full_file):

    file_parts = full_file.split('/')
    k = len(file_parts)
    part_file = file_parts[k-1]
    in_file = GT_Excel_Interface.Test_File("Read", full_file)

    return in_file, part_file



def get_headings(repos, in_file):

    i = 0
    custom_keys_present = False
    
    for val in in_file.sheet_array: #Grab each tab name from the top left corner (1,1)

        
        key_name = in_file.read_string_from_cell(1,1,i)
        print(key_name)
        if key_name in repos.mapping_dictionary:
            keys = repos.mapping_dictionary[key_name][0]

            
        elif key_name == "Custom":
            k = 1 
            while True:
                sp_val = in_file.read_string_from_cell(k,4, i)
                if sp_val != None and sp_val != '' and sp_val != "None":
                    repos.custom_keys.append(sp_val)
                else:
                    custom_keys_present = True
                    keys = None
                    break 
                k = k + 1
                
        else:
            keys = None
            
        if keys != None:
            repos.excel_file_tab_names.append(key_name)
        i = i+1

    j = 3
    while True: #Reads the custom values in the first tab
        val = in_file.read_string_from_cell(5,j, 0)
        if val != None and val != '' and val != "None":
            repos.main_keys.append(val)
        else:
            break
        
        j = j+1

    if custom_keys_present:
        for val in repos.custom_keys:
            
            print(val)
            if val in repos.sp_zero_keys:
                key_name = "Setpoint 0" 
                    
            elif val in repos.sp_one_keys:
                key_name = "Setpoint 1"
                
            elif val in repos.sp_two_keys:
                key_name = "Setpoint 2"
                
            elif val in repos.sp_three_keys:
                key_name = "Setpoint 3"
                
            elif val in repos.sp_four_keys:
                key_name = "Setpoint 4"
                
            elif val in repos.sp_five_keys:
                key_name = "Setpoint 5"
                
            elif val in repos.sp_six_keys:
                key_name = "Setpoint 6"
                
            elif val in repos.configuration_keys:
                key_name = "Configuration"
            else:
                key_name = "Not Found"
            print(key_name)

            if key_name in repos.excel_file_tab_names and key_name != "Not Found":
                pass
            elif key_name == "Not Found":
                pass
            else:
                repos.excel_file_tab_names.append(key_name)


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
    
    
def write_headings(repos, report):
    i = 0
    for name in repos.excel_file_tab_names:


        keys = repos.mapping_dictionary[name][0]

        if name == "Setpoint 1":
            keys = repos.sp_one_keys
            
        if i == 0:
            keys = repos.main_keys
            report.write_cell(1, 4, i, "Index")
            report.write_row_with_array(2, 4, i, keys)
            report.write_row_with_array(len(keys)+2, 4, i, repos.results_keys)
            report.write_cell(5,1,i, name)
            i = i + 1
        elif name == "Inputs":
            pass
        else:
            report.create_tab(name)
            report.write_cell(1, 4, i, "Index")
            report.write_row_with_array(2, 4, i, keys)
            report.write_cell(5,1,i, name)
            i = i + 1

    report.header()

    
def update_omicron_ratios(repos, omicron):

    if repos.cmc_in_use == True:
        repos.set_row_ratio()
        repos.set_ct_ratio()     
        omicron.set_rowgowski_ratio(repos.row_ratio)
        omicron.set_ct_ratio(repos.ct_ratio)
        omicron.set_power_harvesting(repos.ph, repos.ph_type)

    
def get_breaker_inputs(repos, usb):

    i = 0
    while i < 4: 
        try: 
            rsp = usb.communicate("read_setpoint_zero_request")
            setpoints = repos.translator.translate_generic(rsp, repos.sp_zero_keys, repos.etu_dictionary)
            i = 5
        except:
            print("Issue, retrying")
            time.sleep(2)
            i = i + 1
            

        
    time.sleep(1)
    
    rsp = usb.communicate("read_setpoint_one_request")
    repos.translator.translate_generic(rsp, repos.sp_etu_keys, repos.etu_dictionary)
    GT_Conversions.convert_etu_to_standard(repos)


    if repos.family == "35":
##        rsp = usb.communicate("read_setpoint_two_request")
##        setpoints = repos.translator.translate_generic(rsp, repos.sp_two_keys, repos.etu_dictionary)
##        time.sleep(2)
##        rsp = usb.communicate("read_setpoint_three_request")
##        setpoints = repos.translator.translate_generic(rsp, repos.sp_three_keys, repos.etu_dictionary)
##        time.sleep(2)
##        rsp = usb.communicate("read_setpoint_four_request")
        setpoints = repos.translator.translate_generic(rsp, repos.sp_four_keys, repos.etu_dictionary)
        rsp = usb.communicate("read_setpoint_five_request")
        setpoints = repos.translator.translate_generic(rsp, repos.sp_five_keys, repos.etu_dictionary)
        rsp = usb.communicate("read_setpoint_six_request")
        setpoints = repos.translator.translate_generic(rsp, repos.sp_six_keys, repos.etu_dictionary)
    elif repos.family == "MCCB":
        rsp = usb.communicate("read_breaker_protection_capacity_request")
        setpoints = repos.translator.translate_generic(rsp, repos.breaker_protection_capacity_keys, repos.etu_dictionary)
        for val in repos.breaker_protection_capacity_keys:
            print(val)
            print(repos.etu_dictionary[val])
    
    repos.static_style_1 = repos.etu_dictionary['Style1'][0]  
    repos.static_style_2 = repos.etu_dictionary['Style2'][0] 



    
def update_frame_and_rating(repos, usb, in_file, omicron):     #  updates the breaker based on the file

    tab = 0
    old_frame = repos.etu_dictionary['Frame']
    old_rating = repos.etu_dictionary['Rating']

    frame_name = in_file.read_string_from_cell(3,4, tab)
    frame = repos.get_frame(frame_name)
    repos.static_frame = frame

    repos.etu_dictionary['Frame'][0] = frame
    repos.etu_dictionary['Rating'][0]= in_file.read_cell(3,5, tab)

    if old_frame != frame or old_rating != repos.etu_dictionary['Rating'][0]:
        repos.re_cal_needed = True
    else:
        repos.re_cal_needed = False
        

    usb.communicate("enter_into_manufactory_mode_request")
    usb.communicate_with_check("enter_into_manufactory_mode_check")


    print(str(frame))
    if frame != -1: 
        usb.communicate("write_breaker_frame_request", frame)
        cor = usb.communicate_with_check("write_breaker_frame_check")
        if cor != "successful":
            repos.etu_dictionary['Frame'][0] = old_frame
    else:
        print("Invalid Frame Name")
      
    if repos.family == "ACB" or repos.family == "35":
        print("Rating " + str(repos.etu_dictionary['Rating'][0]))
        usb.communicate("write_breaker_plug_request", repos.etu_dictionary['Rating'][0])
        cor = usb.communicate_with_check("write_breaker_plug_check")
    else:
        usb.communicate("write_breaker_rating_request", repos.etu_dictionary['Rating'][0])
        cor = usb.communicate_with_check("write_breaker_rating_check")

    if cor != "successful":
        repos.etu_dictionary['Rating'][0] = old_rating

    time.sleep(1)
    usb.communicate("exit_out_of_manufactory_mode_request")
    time.sleep(.5)
    usb.communicate_with_check("exit_out_of_manufactory_mode_check")
  
  
    #GT_System_Control.power_cycle(omicron, usb)
   

def update_config(repos, in_file, usb):

    i = 0 
    for val in in_file.sheet_array:
        key_name = in_file.read_string_from_cell(1,1,i)

        try:
            keys = repos.mapping_dictionary[key_name][0]
        except:
            keys = None

        if key_name == 'Configuration':
            print("Configuration Being Changed")
            key_name = in_file.read_string_from_cell(1,1,i)

            try:
                keys = repos.mapping_dictionary[key_name][0]
            except:
                keys = None
                
            values = in_file.read_row_for_length(1, 5, i, len(keys))
            k = 0
            read_len = min(len(values),len(keys)) #Makes sure it doesn't read to many or too few values from excel
            for k in range(read_len):
                repos.etu_dictionary[keys[k]][0] = values[k]
                k = k+1

            usb.communicate("enter_into_manufactory_mode_request")
            usb.communicate("enter_into_manufactory_mode_check")
            
            request = repos.mapping_dictionary[key_name][1]
            success = write_setpoints_to_trip_unit(usb, request, keys, repos.etu_dictionary, repos)

            usb.communicate("exit_out_of_manufactory_mode_request")
            usb.communicate("exit_out_of_manufactory_mode_check")

            more = in_file.read_string_from_cell(1,6,i)

            if more == None:
                repos.more_config = False
            break

        i = i + 1 


    if repos.family == "MCCB" and repos.pxr == "PXR25":
        usb.communicate("enter_into_manufactory_mode_request")
        usb.communicate("enter_into_manufactory_mode_check")

        if "Setpoint 5" in in_file.sheet_array:
            print("Writing_Motor")
            usb.communicate("write_etu_style_request", 14255, 59)
            usb.communicate("write_etu_style_check")
        else:
            print("No Motor")
            usb.communicate("write_etu_style_request", 14143, 59)
            usb.communicate("write_etu_style_check")
        get_breaker_inputs(repos, usb)

        usb.communicate("exit_out_of_manufactory_mode_request")
        usb.communicate("exit_out_of_manufactory_mode_check")
        
        

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

def cleanup(repos, usb, omicron, in_file):
    in_file.close_file()
    if repos.pxr == "PXR10" or repos.pxr == "PXR20":
        usb.communicate("exit_out_of_auto_test_mode_request")
        usb.communicate_with_check("exit_out_of_auto_test_mode_check")

    else:
        pass
    
    if repos.cmc_in_use:
        omicron.unlock_omicron()
        

def reset_excel_file_info(repos):

    print(repos.main_keys)


    for key in repos.main_keys:
        del repos.main_dict[key]

    for key in repos.custom_setpoints:
        del repos.custom_setpoints[key]


    repos.main_keys = []
    repos.excel_file_tab_names = []
    repos.custom_setpoings = []
    print(repos.main_keys)

