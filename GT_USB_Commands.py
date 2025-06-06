'''---------------------------------------------------------------------
    
    Company:    EATON COROPORATION
            
                Proprietary Information
                (C) Copyright 2016
                All rights reserved
                
                PXR MCCB Automation - Protection  
    
-------------------------------------------------------------------------------
    
    Authors:    David Arisumi                (412) 893-3213
                Eaton Corporation
                1000 Cherrington Parkway
                Moon Twp, PA 15108-4312
                (412) 893-3300
                
-------------------------------------------------------------------------------
    
    Product:    Automated test system to test the PXR10, PXR20, PXR2D, PXR25, 
                and PXR35 protection algorithms for the SR, NZM, and NRX 
                breaker frames.   
                
    Module:     GT_USB_Commands.py
                
    Mechanics:  Lists all the commands USB

                init()
                    Function:
                        Creates command dictionary. dictionary{key: [packet_array, data]}
                            key: string name of the command
                            packet_array: int array that contains the first few bytes for the usb message.
                            data: string name of what is data needs to be appended to the the message before it is sent. 
                                "No Input" - No Data Will Be Added
                                "Dictionary and Keys" The User needs to provide a dictionary as well as the a set of keys that will be used to get info from the dictionary
                                "Uint08" The message will take as many integers as given and convert them into Uint08 and append them to the message
                                "Uint16" The message will take as many integers as given and convert them into Uint16 and append them to the message
                                "Uint32" The message will take as many integers as given and convert them into Uint32 and append them to the message
                                "Char" The message will take as many integers as given and convert them into Chars and append them to the message
                                "Float"  The message will take as many Floats as given and convert them into hex and append them to the message

                set_family(self,family)
                    Function: command dictionary is inialized using MCCB messages. When using an ACB, the family must be changed so that certain messages can be changed.
                    Input:
                        family(string): what family (ACB/MCCB) the trip unit needs to set messages for.
                    Output:
                        None
                    Changes:
                        command_dictionary(dictionary)-changes command_dictionary. 
                
                get_message(self, def_name, *argv)
                    Function: Given a string command, it figures out what the byte message, adds in any additional info and creates a checksum. 
                    Input:
                        def_name(string) - name of the commmand that needs to be sent
                        *argv(unkown) - Whatever data/info that needs to be added to the command, such as setpoints in a write command
                    Output:
                        tx(String)    - Byte array that will be sent to the trip unit
                        packet(array) - int array of the bytes to be sent. Useful for printing and logging
                    Changes:
                        None

                
                
    Reference:  USB specification for PXR MCCB 3.35
----------------------------------------------------------------------------'''
from __future__ import division
from struct import *
import math


class usb_commands():

    def __init__(self):

        print("creating dictionary")
        self.command_dictionary =   {
                                "read_ID_request"                                       : [[128, 0, 0, 16], "No Input"],
                                "write_configured_serial_number_request"                : [[128, 2, 4, 105, 1, 1, 64, 0], "Uint08_Array"],
                                "write_configured_serial_number_check"                  : [[128, 0, 4, 104, 0, 0], "No Input"],
                                "read_configured_serial_number_request"                 : [[128, 4, 4, 104], "No Input"],     
                                "read_configured_serial_number_check"                   : [[128, 0, 4, 104], "No Input"],   
                                "read_pcba_hadware_version_request"                     : [[128, 0, 7, 195], "No Input"],
                                "read_pcba_test_status_request"                         : [[128, 0, 7, 196], "No Input"],
                                "read_pcba_tu_type_request"                             : [[128, 0, 7, 197], "No Input"],
                                "write_external_current_offset_request"                 : [[128, 2, 6, 144, 1, 1, 16, 0], "Uint16"],
                                "write_external_current_offset_check"                   : [[128, 8, 6, 144], "No Input"],
                                "read_external_current_offset_request"                  : [[128, 0, 6, 144], "No Input"],
                                "write_external_current_scale_request"                  : [[128, 2, 6, 146, 1,1, 16, 0], "Uint16"],
                                "write_external_current_scale_check"                    : [[128, 8, 6, 146], "No Input"],
                                "read_external_current_scale_request"                   : [[128, 0, 6, 146], "No Input"],
                                "write_external_voltage_offset_request"                 : [[128, 2, 6, 148, 1, 1, 12], "Uint32"],
                                "write_external_voltage_offset"                         : [[128, 8, 6, 148], "No Input"], 
                                "read_external_voltage_offset_request"                  : [[128, 0, 6, 148], "No Input"],
                                "write_external_voltage_scale_request"                  : [[128, 2, 6, 150, 1, 1, 12, 0], "Float"],
                                "write_external_voltage_scale_check"                    : [[128, 8, 6, 150], "No Input"],
                                "read_external_voltage_scale_request"                   : [[128, 0, 6, 150], "No Input"],
                                "write_external_low_correction_factor_request"          : [[128, 2, 6, 157, 1, 1, 24, 0], "Uint16"],
                                "write_external_low_correction_factor_check"            : [[128, 8, 6, 157], "No Input"],
                                "read_external_low_correction_factor_request"           : [[128, 0, 6, 157], "No Inptu"],
                                "write_internal_low_correction_factor_request"          : [[128, 2, 6, 158, 1, 1, 24, 0], "Low Correction"],
                                "write_internal_low_correction_factor_check"            : [[128, 8, 6, 158], "No Input"],
                                "read_internal_low_correction_factor_request"           : [[128, 0, 6, 158], "No Input"],
                                "write_phase_shift_request"                             : [[128, 2, 6, 152, 1, 1, 24, 0], "Uint16"],
                                "write_phase_shift_check"                               : [[128, 8, 6, 152], "No Input"],
                                "read_phase_shift_request"                              : [[128, 0, 6, 155], "No Input"],
                                "write_internal_current_offset_and_gain_request"        : [[128, 2, 6, 157, 1,1, 48, 0], "Uint16"],
                                "write_internal_current_offset_and_gain_check"          : [[128, 8, 6, 157], "No Input"],
                                "read_internal_current_offset_and_gain_request"         : [[128, 0, 6, 157], "No Input"],
                                "read_coil_open_detection_basis_request"                : [[128, 0, 6, 153], "No Input"],
                                "write_power_correction_factor_request"                 : [[128, 2, 6, 160, 1, 1, 48, 0], "Float"],
                                "write_power_correction_factor_check"                   : [[128, 8, 6, 160], "No Input"], 
                                "read_power_correction_factor_request"                  : [[128, 0, 6, 160], "No Input"],
                                "write_power_correction_current_limit_request"          : [[128, 2, 6, 162, 1,1, 8, 0], "Float"],
                                "write_power_correction_current_limit_check"            : [[128, 8, 6, 162], "No Input"],
                                "read_power_correction_current_limit_request"           : [[128, 0, 6, 162], "No Input"],
                                "read_all_valid_language_description_request"           : [[128, 0, 5, 0], "No Input"],
                                "write_breaker_protection_capacity_request"             : [[128, 2, 7, 210, 1, 1, 16, 0], "write_breaker_protection_capacity"],
                                "write_breaker_plug_request"                            : [[128, 2, 4, 25, 1, 1, 2, 0], "Uint16"],
                                "read_breaker_protection_capacity_request"              : [[128, 0, 7, 210], "No Input"],
                                "write_breaker_plug_check"                              : [[128, 0, 4, 25], "No Input"],
                                "calibrate_current_offset_test_injection_request"       : [[128, 4, 4, 214, 1, 1, 2, 0],  "Uint08"],
                                "calibrate_curent_offset_test_injection_check"          : [[128, 0, 4, 214],  "No Input"],
                                "calibrate_current_gain_test_injection_request"         : [[128, 4, 4, 215, 1, 1, 2, 0],  "Uint08"],
                                "calibrate_curent_gain_test_injection_check"            : [[128, 0, 4, 215],    "No Input"]}


    def populate_commands(self):
        self.add_buffers()
        self.add_setpoints()
        self.add_setpoints()
        self.add_secondary_injection()
        self.add_commands()
        self.add_mccb_commmands()
        
            
    def add_buffers(self):
        
         self.command_dictionary["read_real_time_data_buffer_zero_request"]               = [[128, 0, 1, 0], "No Input"]
         self.command_dictionary["read_real_time_data_buffer_one_request"]                = [[128, 0, 1, 1], "No Input"]
         self.command_dictionary["read_real_time_data_buffer_two_request"]                = [[128, 0, 1, 2], "No Input"]
         self.command_dictionary["read_real_time_data_buffer_three_request"]              = [[128, 0, 1, 3], "No Input"]
         self.command_dictionary["read_real_time_data_buffer_four_request"]               = [[128, 0, 1, 4], "No Input"]
         self.command_dictionary["read_real_time_data_buffer_five_request"]               = [[128, 0, 1, 5], "No Input"]
         self.command_dictionary["read_real_time_data_buffer_six_request"]                = [[128, 0, 1, 6], "No Input"]
         self.command_dictionary["read_real_time_data_buffer_seven_request"]              = [[128, 0, 1, 7], "No Input"]
         self.command_dictionary["read_real_time_data_buffer_eight_request"]              = [[128, 0, 1, 8], "No Input"]
         self.command_dictionary["read_real_time_data_buffer_ten_request"]                = [[128, 0, 1, 10], "No Input"]
         self.command_dictionary["read_real_time_data_buffer_eleven_request"]             = [[128, 0, 1, 11], "No Input"]
         self.command_dictionary["read_real_time_data_buffer_fourteen_request"]           = [[128, 0, 1, 14], "No Input"]
         self.command_dictionary["read_updated_status_of_trip_unit_request"]              = [[128, 0, 1, 16], "No Input"]
         self.command_dictionary["read_updated_status_of_trip_unit_request"]              = [[128, 0, 1, 16], "No Input"]

         self.command_dictionary["read_max_min_current_demand_requeset"]                  = [[128, 0, 1, 19], "No Input"]
         self.command_dictionary["read_firmware_request"]                                 = [[128, 0, 1, 17], "No Input"]
                                 
    def add_setpoints(self):
        
        self.command_dictionary["read_setpoint_zero_request"]   = [[128, 0, 0, 0], "No Input"]
        self.command_dictionary["read_setpoint_one_request"]    = [[128, 0, 0, 1], "No Input"]
        self.command_dictionary["read_setpoint_two_request"]    = [[128, 0, 0, 2], "No Input"]
        self.command_dictionary["read_setpoint_three_request"]  = [[128, 0, 0, 3], "No Input"]
        self.command_dictionary["read_setpoint_four_request"]   = [[128, 0, 0, 4], "No Input"]
        self.command_dictionary["read_setpoint_five_request"]   = [[128, 0, 0, 5], "No Input"]
        
        self.command_dictionary["write_setpoint_zero_request"]  = [[128, 2, 0, 0, 1, 1, 42], "dictionary and Keys"]
        self.command_dictionary["write_setpoint_one_request"]   = [[128, 2, 0, 1, 1, 1, 52], "dictionary and Keys"]
        self.command_dictionary[ "write_setpoint_two_request"]  = [[128, 2, 0, 2, 1 ,1, 9], "dictionary and Keys"]
        self.command_dictionary["write_setpoint_three_request"] = [[128, 2, 0, 3, 1 ,1, 37], "dictionary and Keys"]
        self.command_dictionary["write_setpoint_four_request"]  = [[128, 2, 0, 4, 1, 1, 53], "dictionary and Keys"]
        self.command_dictionary["write_setpoint_five_request"]  = [[128, 2, 0, 5, 1, 1, 51], "dictionary and Keys"]       

    def add_secondary_injection(self):
        
        self.command_dictionary["software_rms_test_with_trip_request"]                   = [[128, 4, 3, 6, 1, 1, 6, 0], "Secondary"]
        self.command_dictionary["software_rms_test_with_trip_check"]                     = [[128, 0, 3, 6], "No Input"]
        self.command_dictionary["software_peak_test_with_trip_request"]                  = [[128, 4, 3, 32, 1, 1, 6, 0], "Secondary"]
        self.command_dictionary["software_peak_test_with_trip_check"]                    = [[128, 0, 3, 32], "No Input"]
        self.command_dictionary["software_rms_test_without_trip_request"]                = [[128, 4, 3, 7, 1, 1, 6, 0], "Secondary"]
        self.command_dictionary["software_rms_test_without_trip_check"]                  = [[128, 0, 3, 7], "No Input"]
        self.command_dictionary["sotfware_peak_test_without_trip_request"]               = [[128, 4, 3, 33, 1, 1, 6, 0], "Secondary"]
        self.command_dictionary["software_peak_test_without_trip_check"]                 = [[128, 0, 3, 33], "No Input"]
        self.command_dictionary["secondary_injection_rms_test_with_trip_request"]        = [[128, 4, 3, 11, 1, 1, 6, 0], "Secondary"]
        self.command_dictionary["secondary_injection_rms_test_with_trip_check"]          = [[128, 0, 3, 11], "No Input"]
        self.command_dictionary["secondary_injection_peak_test_with_trip_request"]       = [[128, 4, 3, 34, 1, 1, 6, 0], "Secondary"]
        self.command_dictionary["secondary_injeciton_peak_test_with_trip_check"]         = [[128, 0, 3, 34], "No Input"]
        self.command_dictionary["secondary_injection_rms_test_without_trip_request"]     = [[128, 4, 3, 12, 1, 1, 6, 0], "Secondary"]
        self.command_dictionary["secondary_injection_rms_test_without_trip_check"]       = [[128, 0, 3, 12], "No Input"]
        self.command_dictionary["secondary_injection_peak_test_without_trip_request"]    = [[128, 4, 3, 35, 1, 1, 6, 0], "Secondary"]
        self.command_dictionary["secondary_injection_peak_test_without_trip_check"]      = [[128, 0, 3, 35], "No Input"]
        self.command_dictionary["read_simulated_test_results_request"]                   = [[128, 0, 3, 9],  "No Input"]
        self.command_dictionary["cancel_software_test_request"]                          = [[128, 4, 3, 8],  "No Input"]
        self.command_dictionary["cancel_software_test_check"]                            = [[128, 0, 3, 8],  "No Input"]
        self.command_dictionary["cancel_secondary_injection_test_request"]               = [[128, 4, 3, 13], "No Input"]
        self.command_dictionary["cancel_secondary_injection_test_check"]                 = [[128, 0, 3, 13], "No Input"]

    def add_commands(self):

        self.command_dictionary["enter_password_request"]                                = [[128, 4, 3, 14, 1, 1, 4, 0], "Uint08"]
        self.command_dictionary["set_password_request"]                                  = [[128, 4, 3, 31, 1, 1, 4, 0], "Uint08"]
        self.command_dictionary["reset_trip_unit_request"]                               = [[128, 4, 3, 1], "No Input"]
        self.command_dictionary["reset_trip_unit_check"]                                 = [[128, 0, 3, 1], "No Input"]

    def add_event_commands(self):

        self.command_dictionary["read_event_summary_request"]                            = [[128, 0, 2, 0], "No Input"]
        self.command_dictionary["read_time_adjustment_request"]                          = [[128, 0, 2, 1], "No Input"]
        self.command_dictionary["read_trip_event_request"]                               = [[128, 0, 2, 2], "No Input"]
        self.command_dictionary["read_alarm_event_request"]                              = [[128, 0, 2, 3], "No Input"]

        
    def add_mccb_commmands(self):
        
        self.command_dictionary["read_firmware_event_summary_request"]                   = [[128, 0, 2, 0],  "No Input"]
        
        self.command_dictionary["read_real_time_data_thd_request"]                       = [[128, 0, 1, 14], "No Input"]
        self.command_dictionary["read_real_time_data_unbalance_reqeust"]                 = [[128, 0, 1, 15], "No Input"]
        self.command_dictionary["read_real_time_data_current_demand_request"]            = [[128, 0, 1, 18], "No Input"]
        self.command_dictionary["read_motor_external_diagnostics"]                       = [[128, 0, 1, 21], "No Input"]
        self.command_dictionary["read_motor_internal_diagnostisc_request"]               = [[128, 0, 1, 22], "No Input"],
        self.command_dictionary["read_real_time_harmonics_reqeuset"]                     = [[128, 0, 1],     "Uint08"], #The One byte is for the choice of harmonics
        self.command_dictionary["read_rotary_switch_position_request"]                   = [[128, 0, 1, 26], "No Input"]
        self.command_dictionary["psc"]                                                   = [[128, 0, 1, 80], "No Input"]
        

        
        self.command_dictionary["enter_into_manufactory_mode_request"]  = [[128, 4, 4, 2], "No Input"]
        self.command_dictionary["enter_into_manufactory_mode_check"]    = [[128, 0, 4, 2], "No Input"]
        self.command_dictionary["exit_out_of_manufactory_mode_request"] = [[128, 4, 4, 3], "No Input"]
        self.command_dictionary["exit_out_of_manufactory_mode_check"]   = [[128, 0, 4, 3], "No Input"]
        self.command_dictionary["write_setpoint_zero_request"]          = [[128, 2, 0, 0, 1, 1, 49], "dictionary and Keys"]
        self.command_dictionary["write_breaker_frame_request"]          = [[128, 2, 4, 29, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["write_breaker_frame_check"]            = [[128, 0, 4, 29], "No Input"]
        self.command_dictionary["read_breaker_frame_request"]           = [[128, 4, 4, 28], "No Input"]
        self.command_dictionary["read_breaker_frame_check"]          = [[128, 0, 4, 28], "No Input"]
        
        self.command_dictionary["capture_waveform_request"]             = [[128, 4, 3, 2], "No Input"]
        self.command_dictionary["capture_waveform_check"]               = [[128, 0, 3, 2], "No Input"]
        self.command_dictionary["read_once_cylce_waveform_request"]     = [[128, 3, 3, 2], "No Input"]
        self.command_dictionary["read_real_time_clock_request"]         = [[128, 4, 3, 4], "No Input"]
        self.command_dictionary["read_real_time_clock_check"]           = [[128, 0, 3, 4], "No Input"]
        self.command_dictionary["set_real_time_clock_request"]          = [[128, 4, 3, 4], "No Input"]
        self.command_dictionary["set_real_time_clock_check"]            = [[128, 0, 3, 4], "No Input"]
        self.command_dictionary["write_new_time_clock_request"]         = [[128, 4, 3, 5, 1, 1, 8, 0], "Uint08"]
        self.command_dictionary["write_new_time_clock_check"]           = [[128, 0, 3, 5], "No Input"]
        self.command_dictionary["enter_password_from_lcd_request"]      = [[128, 4, 3, 10],"No Input"]
        self.command_dictionary["enter_password_from_lcd_check"]        = [[128, 0, 3, 10],"No Input"]

        self.command_dictionary["coil_open_detection_request"]              = [[128, 4, 3, 15], "No Input"]
        self.command_dictionary["coil_open_detection_check"]                = [[128, 0, 3, 15], "No Input"]
        self.command_dictionary["reset_all_min_max_data_request"]           = [[128, 4, 3, 16], "No Input"]
        self.command_dictionary["reset_all_min_max_data_check"]             = [[128, 0, 3, 16], "No Input"]
        self.command_dictionary["reset_min_max_current_request"]            = [[128, 4, 3, 17], "No Input"]
        self.command_dictionary["reset_min_max_current_check"]              = [[128, 0, 3, 17], "No Input"]
        self.command_dictionary["reset_min_max_VLL_request"]                = [[128, 4, 3, 18], "No Input"]
        self.command_dictionary["reset_min_max_VLL_check"]                  = [[128, 0, 3, 18], "No Input"]
        self.command_dictionary["reset_min_max_VLN_request"]                = [[128, 4, 3, 19], "No Input"]
        self.command_dictionary["reset_min_max_VLN_check"]                  = [[128, 0, 3, 19], "No Input"]
        self.command_dictionary["reset_peak_power_demand_request"]          = [[128, 4, 3, 20], "No Input"]
        self.command_dictionary["reset_peak_power_demand_check"]            = [[128, 0, 3, 20], "No Input"]
        self.command_dictionary["reset_accumulated_energy_request"]         = [[128, 4, 3, 21], "No Input"]
        self.command_dictionary["reset_accumulated_energy_check"]           = [[128, 0, 3, 21], "No Input"]

        self.command_dictionary["reset_external_trip_counter_request"]      = [[128, 4, 3, 23], "No Input"]
        self.command_dictionary["reset_external_trip_counter_check"]        = [[128, 0, 3, 23], "No Input"]
        self.command_dictionary["reset_external_operations_request"]        = [[128, 4, 3, 24], "No Input"]
        self.command_dictionary["reset_external_operations_check"]          = [[128, 0, 3, 24], "No Input"]
        self.command_dictionary["reset_external_temperature_request"]       = [[128, 4, 3, 25], "No Input"]
        self.command_dictionary["reset_external_temperature_check"]         = [[128, 0, 3, 25], "No Input"]
        self.command_dictionary["reset_external_runtime_request"]           = [[128, 4, 3, 26], "No Input"]
        self.command_dictionary["reset_external_rutime_check"]              = [[128, 0, 3, 26], "No Input"]
        self.command_dictionary["reset_external_diagnostics_all_request"]   = [[128, 4, 3, 27], "No Input"]
        self.command_dictionary["reset_external_diagnostics_all_check"]     = [[128, 0, 3, 27], "No Input"]

        self.command_dictionary["reset_internal_trip_counter_request"]      = [[128, 4, 3, 23], "No Input"]
        self.command_dictionary["reset_internal_trip_counter_check"]        = [[128, 0, 3, 23], "No Input"]
        self.command_dictionary["reset_internal_operations_request"]        = [[128, 4, 3, 24], "No Input"]
        self.command_dictionary["reset_internal_operations_check"]          = [[128, 0, 3, 24], "No Input"]
        self.command_dictionary["reset_internal_temperature_request"]       = [[128, 4, 3, 25], "No Input"]
        self.command_dictionary["reset_internal_temperature_check"]         = [[128, 0, 3, 25], "No Input"]
        self.command_dictionary["reset_internal_runtime_request"]           = [[128, 4, 3, 26], "No Input"]
        self.command_dictionary["reset_internal_rutime_check"]              = [[128, 0, 3, 26], "No Input"]
        self.command_dictionary["reset_internal_diagnostics_all_request"]   = [[128, 4, 3, 27], "No Input"]
        self.command_dictionary["reset_internal_diagnostics_all_check"]     = [[128, 0, 3, 27], "No Input"]
        
        self.command_dictionary["reset_power_up_flag_request"]   = [[128, 4, 3, 29], "No Input"]
        self.command_dictionary["reset_power_up_flag_check"]     = [[128, 0, 3, 29], "No Input"]
        
        self.command_dictionary["enable_maintenance_mode_request"]   = [[128, 4, 3, 64], "No Input"] #Probably a defunct command
        self.command_dictionary["enable_maintenance_mode_request"]   = [[128, 0, 3, 64], "No Input"] #Probably a defunct command
        self.command_dictionary["disable_maintenance_mode_request"]  = [[128, 4, 3, 65], "No Input"] #Probably a defunct command
        self.command_dictionary["disable_maintenance_mode_request"]  = [[128, 0, 3, 65], "No Input"] #Probably a defunct command

        self.command_dictionary["open_breaker_request"]             = [[128, 4, 3, 66], "No Input"]
        self.command_dictionary["open_breaker_check"]               = [[128, 0, 3, 66], "No Input"]
        self.command_dictionary["relay_output_request"]             = [[128, 4, 3, 67, 1, 1, 2, 0], "Uint08"]
        self.command_dictionary["relay_output_check"]               = [[128, 0, 3, 67], "No Input"]
        self.command_dictionary["thermal_memory_reset_request"]     = [[128, 4, 3, 68, 1, 1, 2, 0], "Uint16"]

        self.command_dictionary["test_led_active_request"]          = [[128, 4, 11, 5, 1, 1, 2, 0], "Uint08"]
        self.command_dictionary["test_led_active_check"]            = [[128, 8, 11, 5], "No Input"]
        self.command_dictionary["test_active_relay_request"]        = [[128, 4, 11, 6, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["test_active_relay_check"]          = [[128, 8, 11, 6], "No Input"]
        self.command_dictionary["trip_TA_request"]                  = [[128, 4, 11, 7], "No Input"]
        self.command_dictionary["trip_TA_check"]                    = [[128, 8, 11, 7], "No Input"]

        self.command_dictionary["set_zsi_output_pin_value_request"] = [[128, 4, 11, 9, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["set_zsi_output_pin_value_check"]   = [[128, 8, 11, 9], "No Input"]
        self.command_dictionary["test_lcd_screen_request"]          = [[128, 4, 11, 12, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["test_lcd_screen_check"]            = [[128, 8, 11, 12], "Two Bytes"]
        self.command_dictionary["set_frequency_request"]            = [[128, 4, 11, 15, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["set_frequency_check"]              = [[128, 8, 11, 15], "No Input"]
        self.command_dictionary["factory_default_reset_request"]    = [[128, 4, 11, 10], "No Input"]
        self.command_dictionary["factory_deault_reset_check"]       = [[128, 8, 11, 10], "No Input"]
        self.command_dictionary["test_thermal_memory_request"]      = [[128, 4, 11, 11], "No Input"]
        self.command_dictionary["test_thermal_memory_check"]        = [[128, 8, 11, 11], "No Input"]


        self.command_dictionary["enter_into_manufactory_mode_request"]                   = [[128, 4, 11, 2], "No Input"]
        self.command_dictionary["enter_into_manufactory_mode_check"]                     = [[128, 8, 11, 2], "No Input"]
        self.command_dictionary["exit_out_of_manufactory_mode_request"]                  = [[128, 4, 11, 3], "No Input"]
        self.command_dictionary["exit_out_of_manufactory_mode_check"]                    = [[128, 8, 11, 3], "No Input"]
        self.command_dictionary["enter_into_auto_test_mode_request"]                     = [[128, 4, 11, 0], "No Input"]
        self.command_dictionary["enter_into_auto_test_mode_check"]                       = [[128, 8, 11, 0], "No Input"]
        self.command_dictionary["exit_out_of_auto_test_mode_request"]                    = [[128, 4, 11, 1], "No Input"]
        self.command_dictionary["exit_out_of_auto_test_mode_check"]                      = [[128, 8, 11, 1], "No Input"]
        
        '''========Calibration Commands=========='''
        self.command_dictionary["external_IV_offset_calibration_request"]                = [[128, 4, 10, 16], "No Input"]
        self.command_dictionary["external_IV_offset_calibration_check"]                  = [[128, 8, 10, 16], "No Input"]
        self.command_dictionary["internal_I_offset_calibration_request"]                 = [[128, 4, 10, 53], "No Input"]
        self.command_dictionary["internal_I_offset_calibration_check"]                   = [[128, 8, 10, 53], "No Input"]
        self.command_dictionary["external_ia_calibration_request"]                       = [[128, 4, 10, 32, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["external_ib_calibration_request"]                       = [[128, 4, 10, 33, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["external_ic_calibration_request"]                       = [[128, 4, 10, 34, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["external_in_calibration_request"]                       = [[128, 4, 10, 35, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["external_ig_calibration_request"]                       = [[128, 4, 10, 36, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["external_three_pole_current_scale_calibration_request"] = [[128, 4, 10, 37, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["external_four_pole_current_scale_calibration_request"]  = [[128, 4, 10, 38, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["secondary_injection_base_counter_calibration_request"]  = [[128, 4, 16, 18], "No Input"]
        self.command_dictionary["external_va_scale_calibraiton_request"]                 = [[128, 4, 10, 42, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["external_vb_scale_calibration_request"]                 = [[128, 4, 10, 43, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["external_vc_scale_calibration_request"]                 = [[128, 4, 10, 44, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["external_three_pole_voltage_scale_calibration_request"] = [[128, 4, 10, 45, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["phase_a_shift_calibration_request"]                     = [[128, 4, 10, 48, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["phase_b_shift_calibration_request"]                     = [[128, 4, 10, 49, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["phase_c_shift_calibration_request"]                     = [[128, 4, 10, 50, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["phase_three_shift_calibration_request"]                 = [[128, 4, 10, 51, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["internal_ia_scale_calibration_request"]                 = [[128, 1, 10, 55, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["internal_ib_scale_calibration_request"]                 = [[128, 1, 10, 56, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["internal_ic_scale_calibration_request"]                 = [[128, 1, 10, 57, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["internal_in_scale_calibration_request"]                 = [[128, 1, 10, 58, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["internal_ig_scale_calibration_request"]                 = [[128, 1, 10, 59, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["internal_three_pole_scale_calibration_request"]         = [[128, 1, 10, 60, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["internal_four_pole_scale_calibration_request"]          = [[128, 1, 10, 61, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["secondary_injection_base_counter_calibration_request"]  = [[128, 4, 10, 18], "No Input"]
        self.command_dictionary["secondary_injection_base_counter_calibration_check"]    = [[128, 8, 10, 18], "No Input"]
        self.command_dictionary["secondary_injection_delta_counter_calibration_request"] = [[128, 4, 10, 19], "No Input"]
        self.command_dictionary["secondary_injection_delta_counter_calibration_check"]   = [[128, 8, 10, 19], "No Input"]
        self.command_dictionary["coil_open_basis_calibration_request"]                   = [[128, 4, 10, 20], "No Input"]
        self.command_dictionary["coil_open_basis_calibration_check"]                     = [[128, 8, 10, 20], "No Input"]
        self.command_dictionary["external_ia_scale_calibration_check"]                   = [[128, 8, 10, 32], "No Input"]
        self.command_dictionary["external_ib_scale_calibration_check"]                   = [[128, 8, 10, 33], "No Input"]
        self.command_dictionary["external_ic_scale_calibration_check"]                   = [[128, 8, 10, 34], "No Input"]
        self.command_dictionary["external_in_scale_calibration_check"]                   = [[128, 8, 10, 35], "No Input"]
        self.command_dictionary["external_ig_scale_calibration_check"]                   = [[128, 8, 10, 36], "No Input"]
        self.command_dictionary["external_three_pole_current_scale_calibration_check"]   = [[128, 8, 10, 37], "No Input"]
        self.command_dictionary["external_four_pole_current_scale_calibration_check"]    = [[128, 8, 10, 38], "No Input"]
        self.command_dictionary["external_va_scale_calibraiton_check"]                   = [[128, 8, 10, 42], "No Input"]
        self.command_dictionary["external_vb_scale_calibration_check"]                   = [[128, 8, 10, 43], "No Input"]
        self.command_dictionary["external_vc_scale_calibration_check"]                   = [[128, 8, 10, 44], "No Input"] 
        self.command_dictionary["external_three_pole_voltage_scale_calibration_check"]   = [[128, 8, 10, 45], "No Input"]
        self.command_dictionary["phase_a_shift_calibration_check"]                       = [[128, 8, 10, 46], "No Input"]
        self.command_dictionary["phase_b_shift_calibration_check"]                       = [[128, 8, 10, 47], "No Input"]
        self.command_dictionary["phase_c_shift_calibration_check"]                       = [[128, 8, 10, 48], "No Input"]
        self.command_dictionary["phase_three_shift_calibration_check"]                   = [[128, 8, 10, 49], "No Input"]
        self.command_dictionary["internal_ia_scale_calibration_check"]                   = [[128, 8, 10, 55], "No Input"]
        self.command_dictionary["internal_ib_scale_calibration_check"]                   = [[128, 8, 10, 56], "No Input"]
        self.command_dictionary["internal_ic_scale_calibraiton_check"]                   = [[128, 8, 10, 57], "No Input"]
        self.command_dictionary["internal_in_scale_calibraiton_check"]                   = [[128, 8, 10, 58], "No Input"]
        self.command_dictionary["internal_ig_scale_calibration_check"]                   = [[128, 8, 10, 59], "No Input"]
        self.command_dictionary["internal_three_pole_scale_calibration_check"]           = [[128, 8, 10, 60], "No Input"]
        self.command_dictionary["internal_four_pole_scale_calibration_check"]            = [[128, 8, 10, 61], "No Input"]                            
        self.command_dictionary["clear_external_IV_offset_request"]                      = [[128, 4, 10, 64], "No Input"]
        self.command_dictionary["clear_external_IV_offset_check"]                        = [[128, 8, 10, 64], "No Input"]
        self.command_dictionary["clear_external_current_scale_request"]                  = [[128, 4, 10, 65], "No Input"]
        self.command_dictionary["clear_external_current_scale_check"]                    = [[128, 8, 10, 65], "No Input"]
        self.command_dictionary["clear_external_voltage_scale_request"]                  = [[128, 4, 10, 66], "No Input"]
        self.command_dictionary["clear_external_voltage_scale_check" ]                   = [[128, 8, 10, 66], "No Input"]
        self.command_dictionary["clear_phase_shift_scale_request"]                       = [[128, 4, 10, 67], "No Input"]
        self.command_dictionary["clear_phase_shift_scale_check"]                         = [[128, 8, 10, 67], "No Input"]
        self.command_dictionary["clear_internal_offset_request"]                         = [[128, 4, 10, 68], "No Input"]
        self.command_dictionary["clear_internal_offset_check"]                           = [[128, 8, 10, 68], "No Input"]
        self.command_dictionary["clear_interal_current_scale_request"]                   = [[128, 4, 10, 69], "No Input"]
        self.command_dictionary["clear_internal_current_scale_check"]                    = [[128, 8, 10, 69], "No Input"]
        self.command_dictionary["clear_internal_ig_scale_request"]                       = [[128, 4, 10, 70], "No Input"]
        self.command_dictionary["clear_internal_ig_scale_check"]                         = [[128, 8, 10, 70], "No Input"]
        self.command_dictionary["clear_all_extneral_calibration_request"]                = [[128, 4, 10, 71], "No Input"]
        self.command_dictionary["clear_all_external_calibration_check"]                  = [[128, 8, 10, 71], "No Input"]
        self.command_dictionary["clear_all_internal_calibration_request"]                = [[128, 4, 10, 72], "No Input"]
        self.command_dictionary["clear_all_internal_calibraiton_check"]                  = [[128, 8, 10, 72], "No Input"]
        self.command_dictionary["clear_secondary_injection_request"]                     = [[128, 4, 10, 73], "No Input"]
        self.command_dictionary[ "clear_secondary_injection_check"]                      = [[128, 8, 10, 73], "No Input"]

        '''========Breaker Manufactory Info=========='''
        self.command_dictionary["write_etu_style_request"]                                : [[128, 2, 7, 176, 1, 1, 4, 0], "Uint16"]
        self.command_dictionary["write_etu_style_check"]                                 : [[128, 8, 7, 176], "No Input"]                                                   
        self.command_dictionary["read_etu_style_request"]                                : [[128, 0, 7, 176], "No Input"]
        self.command_dictionary["write_etu_manufacture_location_request"]                : [[128, 2, 7, 177, 1, 1, 4, 0], "Char"]
        self.command_dictionary["write_etu_manufacture_location_check"]                  : [[128, 8, 7, 177]," No Input"]
        self.command_dictionary["read_etu_manufacture_location_request"]                 : [[128, 0, 7, 177], "No Input"]
        self.command_dictionary["write_etu_manufacture_date_request"]                    : [[128, 2, 7, 178, 1, 1, 6, 0], "Char"]
        self.command_dictionary["write_etu_manufacture_date_check"]                      : [[128, 8, 7, 178], "No Input"]
        self.command_dictionary["read_etu_manufacture_date_request"]                     : [[128, 0, 7, 178], "No Input"]
        self.command_dictionary["write_etu_serial_number_request"]                       : [[128, 2, 7, 179, 1, 1, 40, 0], "Char"]
        self.command_dictionary["write_etu_serial_number_check"]                         : [[128, 8, 7, 179], "No Input"]
        self.command_dictionary["read_etu_serial_number_request"]                        : [[128, 0, 7, 179], "No Input"]
        self.command_dictionary["write_etu_catalog_number_request"]                      : [[128, 2, 7, 181, 1, 1, 40, 0], "Char"]
        self.command_dictionary["write_etu_catalog_number_check"]                        : [[128, 8, 7, 181], "No Input"]
        self.command_dictionary["read_etu_catalog_number_request"]                       : [[128, 0, 7, 181], "No Input"]
        self.command_dictionary["write_etu_style_string_request"]                        : [[128, 2, 7, 182, 1, 1, 40, 0], "Char"]
        self.command_dictionary["write_etu_style_string_check"]                          : [[128, 8, 7, 182], "no Input"]
        self.command_dictionary["read_etu_style_string_request"]                         : [[128, 0, 7, 182], "No Input"]
        self.command_dictionary["write_etu_status_request"]                              : [[128, 2, 7, 180, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["write_etu_status_check"]                                : [[128, 8, 7, 180], "No Input"]      
        self.command_dictionary["write_breaker_rating_request"]                          : [[128, 2, 7, 208, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["write_breaker_rating_check"]                            : [[128, 8, 7, 208], "No Input"]
        self.command_dictionary["read_breaker_rating_request"]                           : [[128, 0, 7, 208], "No Input"]
        self.command_dictionary["write_breaker_frame_request"]                           : [[128, 2, 7, 209, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["write_breaker_frame_check"]                             : [[128, 8, 7, 209], "No Input"]
        self.command_dictionary["read_breaker_frame_request"]                            : [[128, 0, 7, 209], "No Input"]
        self.command_dictionary["write_breaker_protection_request"]                      : [[128, 2, 7, 210, 1, 1, 16, 1], "dictionary and Keys"]
        self.command_dictionary["write_breaker_protection_check"]                        : [[128, 8, 7, 210], "No Input"] 
        self.command_dictionary["read_breaker_protection_request"]                       : [[128, 0, 7, 210], "No Input"]
        self.command_dictionary["write_breaker_manufacture_location_request"]            : [[128, 2, 7, 211, 1, 1, 4, 0], "Char"]
        self.command_dictionary["write_breaker_manufacture_location_check"]              : [[128, 8, 7, 211], "No Input"] 
        self.command_dictionary["read_breaker_manufacture_location_request"]             : [[128, 0, 7, 211], "No Input"]
        self.command_dictionary["write_breaker_manufacture_date_request"]                : [[128, 2, 7, 212, 1, 1, 6, 0,], "Char"]
        self.command_dictionary["write_breaker_manufacture_date_check"]                  : [[128, 8, 7, 212], "No Input"]
        self.command_dictionary["read_breaker_manufacture_date_request"]                 : [[128, 0, 7, 212], "No Input"]
        self.command_dictionary["write_breaker_test_status_request"]                     : [[128, 2, 7, 213, 1,1, 2, 0], "Unit16"]
        self.command_dictionary["write_breaker_test_status_check"]                       : [[128, 8, 7, 213], "No Input"]
        self.command_dictionary["read_breaker_test_status_request"]                      : [[128, 0, 7, 213], "No Input"]
        self.command_dictionary["write_breaker_serial_number_request"]                   : [[128, 2, 7, 214, 1, 1, 40, 0], "Char"]
        self.command_dictionary["write_breaker_serial-number_check"]                     : [[128, 8, 7, 214], "No Input"]
        self.command_dictionary["read_breaker_serial_number_request"]                    : [[128, 0, 7, 214], "No Input"]
        self.command_dictionary["write_breaker_catalog_number_request"]                  : [[128, 2, 7, 215, 1, 1, 40, 0], "Char"]
        self.command_dictionary["write_breaker_catalog_number_check"]                    : [[128, 8, 7, 215], "No Input"]
        self.command_dictionary["read_breaker_catalog_number_request"]                   : [[128, 0, 7, 215], "No Input"]
        self.command_dictionary["write_pcba_manufacture_location_request"]               : [[128, 2, 7, 192, 1, 1, 4, 0], "Char"]
        self.command_dictionary["write_pcba_manufacture_location_check"]                 : [[128, 8, 7, 192], "No Input"]
        self.command_dictionary["read_pcba_manufacture_location_request"]                : [[128, 0, 7, 192], "No Input"]
        self.command_dictionary["write_pcba_manufacture_date_request"]                   : [[128, 2, 7, 193, 1, 1, 6, 0], "Char"]
        self.command_dictionary["write_pcba_manufacture_date_check"]                     : [[128, 8, 7, 193], "No Input"]
        self.command_dictionary["read_pcba_manufacture_date_request"]                    : [[128, 0, 7, 193], "No Input"]
        self.command_dictionary["write_pcab_serial_number_request"]                      : [[128, 2, 7, 194, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["read_pcba_serial_number_request"]                       : [[128, 0, 7, 194], "No Input"]  
                                
    def add_acb_commands(self):
        self.command_dictionary["read_real_time_current_crest_factor"]                   : [[128, 0, 1, 20], "No Input"]
        self.command_dictionary["read_real_power_factor_freqeuncy_min_max"]              : [[128, 0, 1, 22], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_power"]                      : [[128, 0, 1, 23], "No Input"]  
        self.command_dictionary["read_real_time_harmonics"]                              : [[128, 0, 1], "Uint08"]
        '''32 = Ia, 33 = Ib, 34 = Ic, 35 = In, 36 = Van, 37 = Vbn, 38 = Vcn, 39 = Vab, Vbc = 40, Vca = 41'''

        self.command_dictionary["enter_into_auto_test_mode_request"]                     = [[128, 4, 4, 0], "No Input"]
        self.command_dictionary["enter_into_auto_test_mode_check"]                       = [[128, 8, 4, 0], "No Input"]
        self.command_dictionary["exit_out_of_auto_test_mode_request"]                    = [[128, 4, 4, 1], "No Input"]
        self.command_dictionary["exit_out_of_auto_test_mode_check"]                      = [[128, 8, 4, 1], "No Input"]
        self.command_dictionary["enter_into_manufactory_mode_request"]                   = [[128, 4, 4, 2], "No Input"]
        self.command_dictionary["enter_into_manufactory_mode_check"]                     = [[128, 8, 4, 2], "No Input"]
        self.command_dictionary["exit_out_of_manufactory_mode_request"]                  = [[128, 4, 4, 3], "No Input"]
        self.command_dictionary["exit_out_of_manufactory_mode_check"]                    = [[128, 8, 4, 3], "No Input"]

        self.command_dictionary["test_led_active_request"]          = [[128, 4, 4, 5, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["test_led_active_check"]            = [[128, 0, 4, 5], "No Input"]
        self.command_dictionary["test_active_relay_request"]        = [[128, 4, 4, 6, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["test_active_relay_check"]          = [[128, 8, 11, 6], "No Input"]
        self.command_dictionary["trip_TA_request"]                  = [[128, 4, 4, 7], "No Input"]
        self.command_dictionary["trip_TA_check"]                    = [[128, 0, 4, 7], "No Input"]
        self.command_dictionary["test_zsi_input_request"]           = [[128, 4, 4, 8], "No Input"]
        self.command_dictionary["test_zsi_input_check"]             = [[128, 0, 4, 8], "No Input"]
        self.command_dictionary["test_zsi_input_request"]           = [[128, 4, 4, 9], "No Input"]
        self.command_dictionary["test_zsi_input_check"]             = [[128, 0, 4, 9], "No Input"]
        self.command_dictionary["factory_default_request"]          = [[128, 4, 4, 10], "No Input"]
        self.command_dictionary["factory_default_check"]            = [[128, 0, 4, 10], "No Input"]
        self.command_dictionary["test_thermal_memory_request"]      = [[128, 4, 4, 11, 1, 1, 2, 0],  "Uint16"]
        self.command_dictionary["test_thermal_memory_check"]        = [[128, 0, 4, 11], "No Input"]
        self.command_dictionary["clear_etu_request"]                = [[128, 4, 4, 13], "No Input"]
        self.command_dictionary["clear_etu_check"]                  = [[128, 0, 4, 13], "No Input"]
        self.command_dictionary["read_thermal_memory_request"]      = [[128, 4, 4, 14], "No Input"]
        self.command_dictionary["read_thermal_memory_check"]        = [[128, 0, 4, 14], "No Input"]
        self.command_dictionary["wrtie_frequency_request"]          = [[128, 4, 4, 15, 1, 1, 2, 0],  "Uint16"]
        self.command_dictionary["wrtie_frequency_check"]            = [[128, 0, 4, 15], "No Input"]

        self.command_dictionary["temp_cal_high_point_request"]      = [[128, 4, 4, 30, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["temp_cal_high_point_check"]        = [[128, 0, 4, 30], "No Input"]
        self.command_dictionary["temp_cal_high_point_request"]      = [[128, 4, 4, 31, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["temp_cal_high_point_check"]        = [[128, 0, 4, 31], "No Input"]

        self.command_dictionary["temp_cal_high_point_request"]      = [[128, 4, 4, 31, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["temp_cal_high_point_check"]        = [[128, 0, 4, 31], "No Input"]

        self.command_dictionary["cal_phase_ia_etu_scale_request"]   = [[128, 4, 4, 32, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["cal_phase_ia_etu_scale_check"]     = [[128, 0, 4, 32], "No Input"]
        self.command_dictionary["cal_phasei_b_etu_scale_request"]   = [[128, 4, 4, 33, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["cal_phase_ib_etu_scale_check"]     = [[128, 0, 4, 33], "No Input"]
        self.command_dictionary["cal_phase_ic_etu_scale_request"]   = [[128, 4, 4, 34, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["cal_phase_ic_etu_scale_check"]     = [[128, 0, 4, 34], "No Input"]
        self.command_dictionary["cal_phase_in_etu_scale_request"]   = [[128, 4, 4, 35, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["cal_phase_in_etu_scale_check"]     = [[128, 0, 4, 35], "No Input"]
        self.command_dictionary["cal_phase_va_scale_request"]       = [[128, 4, 4, 36, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["cal_phase_va_scale_check"]         = [[128, 0, 4, 36], "No Input"]
        self.command_dictionary["cal_phase_vb_scale_request"]       = [[128, 4, 4, 37, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["cal_phase_vb_scale_check"]         = [[128, 0, 4, 37], "No Input"]
        self.command_dictionary["cal_phase_vc_scale_request"]       = [[128, 4, 4, 38, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["cal_phase_vc_scale_check"]         = [[128, 0, 4, 38], "No Input"]  
        self.command_dictionary["cal_phase_vc_scale_request"]       = [[128, 4, 4, 39, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["cal_phase_vc_scale_check"]         = [[128, 0, 4, 39], "No Input"]
        self.command_dictionary["cal_current_voltage_offset_request"]       = [[128, 4, 4, 41], "Uint32"]
        self.command_dictionary["cal_current_voltage_offset_check"]         = [[128, 0, 4, 41], "No Input"]
        self.command_dictionary["cal_current_offset_request"]       = [[128, 4, 4, 57], "Uint32"]
        self.command_dictionary["cal_current_offset_check"]         = [[128, 0, 4, 57], "No Input"]

        self.command_dictionary["cal_source_ground_scale_request"]    = [[128, 4, 4, 42, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["cal_source_ground_scale_check"]      = [[128, 0, 4, 42], "No Input"]
        self.command_dictionary["cal_source_ground_offset_request"]   = [[128, 4, 4, 44, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["cal_source_ground_offset_check"]     = [[128, 0, 4, 44], "No Input"]

        self.command_dictionary["cal_si_base_counter_request"]   = [[128, 4, 4, 45], "No Input"]
        self.command_dictionary["cal_si_base_counter_check"]     = [[128, 0, 4, 45], "No Input"]
        self.command_dictionary["cal_si_scale_factor_request"]   = [[128, 4, 4, 46], "No Input"]
        self.command_dictionary["cal_si_scale_factor_check"]     = [[128, 0, 4, 46], "No Input"]
        self.command_dictionary["cal_si_coil_open_request"]      = [[128, 4, 4, 47], "No Input"]
        self.command_dictionary["cal_si_coil_open_check"]        = [[128, 0, 4, 47], "No Input"]

        self.command_dictionary["cal_phase_a_phase_shift_request"]       = [[128, 4, 4, 37, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["cal_phase_a_phase_shift_check"]         = [[128, 0, 4, 36], "No Input"]

        self.command_dictionary["cal_phase_a_shift_request"]         = [[128, 4, 4, 48, 1, 1, 4, 0],  "Uint32"]
        self.command_dictionary["cal_phase_a_shift_check"]           = check = [[128, 0, 4, 48], "No Input"]
        self.command_dictionary["cal_phase_b_shift_request"]         = [[128, 4, 4, 49, 1, 1, 4, 0],  "Uint32"]
        self.command_dictionary["cal_phase_b_shift_check"]           = [[128, 0, 4, 49], "No Input"]
        self.command_dictionary["cal_phase_c_shift_request"]         = [[128, 4, 4, 50, 1, 1, 4, 0],  "Uint32"]
        self.command_dictionary["cal_phase_c_shift_check"]           = [[128, 0, 4, 50], "No Input"]

        self.command_dictionary["cal_three_phase_shift_request"]     = [[128, 4, 4, 51, 1, 1, 4, 0],  "Uint32"]
        self.command_dictionary["cal_three_phase_shift_check"]       = [[128, 0, 4, 51], "No Input"]
        self.command_dictionary["cal_three_pole_etu_gain_scale_request"]  = [[128, 4, 4, 52, 1, 1, 4, 0],  "Uint32"]
        self.command_dictionary["cal_three_pole_etu_gain_scale_check"]    = [[128, 0, 4, 52], "No Input"]
        self.command_dictionary["cal_four_pole_etu_gain_scale_request"]   = [[128, 4, 4, 53, 1, 1, 4, 0],  "Uint32"]
        self.command_dictionary["cal_four_pole_etu_gain_scale_check"]     = [[128, 0, 4, 53], "No Input"]
        self.command_dictionary["cal_three_pole_rog_gain_scale_request"]  = [[128, 4, 4, 54, 1, 1, 4, 0],  "Uint32"]
        self.command_dictionary["cal_three_pole_rog_gain_scale_check"]    = [[128, 0, 4, 54], "No Input"]
        self.command_dictionary["cal_four_pole_rog_gain_scale_request"]   = [[128, 4, 4, 55, 1, 1, 4, 0],  "Uint32"]
        self.command_dictionary["cal_four_pole_rog_gain_scale_check"]     = [[128, 0, 4, 55], "No Input"]

        self.command_dictionary["cal_three_pole_rog_gain_scale_request"]   = [[128, 4, 4, 56, 1, 1, 4, 0],  "Uint32"]
        self.command_dictionary["cal_three_pole_rog_gain_scale_check"]     = [[128, 0, 4, 56], "No Input"]
        self.command_dictionary["cal_phase_ia_rog_scale_request"]          = [[128, 4, 4, 58, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["cal_phase_ia_rog_scale_check"]            = [[128, 0, 4, 58], "No Input"]
        self.command_dictionary["cal_phasei_b_rog_scale_request"]          = [[128, 4, 4, 59, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["cal_phase_ib_rog_scale_check"]            = [[128, 0, 4, 59], "No Input"]
        self.command_dictionary["cal_phase_ic_rog_scale_request"]          = [[128, 4, 4, 60, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["cal_phase_ic_rog_scale_check"]            = [[128, 0, 4, 60], "No Input"]
        self.command_dictionary["cal_phase_in_rog_scale_request"]          = [[128, 4, 4, 61, 1, 1, 4, 0], "Uint32"]
        self.command_dictionary["cal_phase_in_rog_scale_check"]            = [[128, 0, 4, 61], "No Input"]

        self.command_dictionary["recover_cal_to_etu_request"]              = [[128, 4, 4, 64], "No Input"]
        self.command_dictionary["recover_cal_to_etu__check"]               = [[128, 0, 4, 64], "No Input"]
        self.command_dictionary["recover_cal_to_rog_request"]              = [[128, 4, 4, 65], "No Input"]
        self.command_dictionary["recover_cal_to_rog__check"]               = [[128, 0, 4, 65], "No Input"]
        self.command_dictionary["recover_cal_to_rog_request"]              = [[128, 4, 4, 66], "No Input"]
        self.command_dictionary["recover_cal_to_rog_check"]                = [[128, 0, 4, 66], "No Input"]
        self.command_dictionary["recover_gf_request"]                      = [[128, 4, 4, 67], "No Input"]
        self.command_dictionary["recover_gf_check"]                        = [[128, 0, 4, 67], "No Input"]
        self.command_dictionary["recover_phase_shift_request"]             = [[128, 4, 4, 68], "No Input"]
        self.command_dictionary["recover_phase_shift_check"]               = [[128, 0, 4, 68], "No Input"]
        self.command_dictionary["recover_all_cal_request"]                 = [[128, 4, 4, 69], "No Input"]
        self.command_dictionary["recover_all_cal_check"]                   = [[128, 0, 4, 69], "No Input"] 
        self.command_dictionary["recover_temp_cal_request"]                 = [[128, 4, 4, 70], "No Input"]
        self.command_dictionary["recover_temp_cal_check"]                   = [[128, 0, 4, 70], "No Input"]
        self.command_dictionary["recover_secondary_injection_request"]                 = [[128, 4, 4, 70], "No Input"]
        self.command_dictionary["recover_secondary_injection_check"]                   = [[128, 0, 4, 70], "No Input"] 

        self.command_dictionary["read_firmware_version_request"]                         =[[128, 0, 1, 11], "No Input"] #ACB Only
        self.command_dictionary["write_firmware_version_request"]                        = [[128, 0, 4, 27], "No Input"]
                
        self.command_dictionary["read_trip_unit_style_request"]                          = [[128, 4, 4, 26], "No Input"] 
        self.command_dictionary["read_trip_unit_style_check"]                         = [[128, 0, 4, 26], "No Input"] 
        self.command_dictionary["write_trip_unit_style_request"]                         = [[128, 2, 4, 27, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["write_trip_unit_style_check"]                         = [[128, 2, 4, 27,], "No Input"]
        
        self.command_dictionary["read_trip_unit_serial_number_request"]                  = [[128, 4, 4, 160], "No Input"] 
        self.command_dictionary["read_trip_unit_serial_number_check"]                 = [[128, 0, 4, 160], "No Input"] 
        self.command_dictionary["write_trip_unit_serial_number_request"]                 = [[128, 2, 4, 161, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["write_trip_unit_serial_number_check"]                = [[128, 2, 4, 161], "No Input"]

        self.command_dictionary["read_trip_unit_hardware_version_request"]                  = [[128, 4, 4, 162], "No Input"] 
        self.command_dictionary["read_trip_unit_hardware_version_check"]                 = [[128, 0, 4, 162], "No Input"] 
        self.command_dictionary["write_trip_unit_hardware_version_request"]                 = [[128, 2, 4, 163, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["write_trip_unit_hardware_version_check"]                = [[128, 2, 4, 163], "No Input"]

        self.command_dictionary["read_frame_module_serial_number_request"]                  = [[128, 4, 4, 176], "No Input"] 
        self.command_dictionary["read_frame_module_serial_number_check"]                 = [[128, 0, 4, 176], "No Input"] 
        self.command_dictionary["write_frame_module_serial_number_request"]                 = [[128, 2, 4, 177, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["write_frame_module_serial_number_check"]                = [[128, 2, 4, 177], "No Input"]

        self.command_dictionary["read_frame_hardware_version_request"]                  = [[128, 4, 4, 178], "No Input"] 
        self.command_dictionary["read_frame_hardware_version_check"]                 = [[128, 0, 4, 178], "No Input"] 
        self.command_dictionary["write_frame_hardware_version_request"]                 = [[128, 2, 4, 179, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["write_frame_hardware_version_check"]                = [[128, 2, 4, 179], "No Input"]

        self.command_dictionary["read_frame_hardware_version_request"]                  = [[128, 4, 4, 178], "No Input"] 
        self.command_dictionary["read_frame_hardware_version_check"]                 = [[128, 0, 4, 178], "No Input"] 
        self.command_dictionary["write_frame_hardware_version_request"]                 = [[128, 2, 4, 179, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["write_frame_hardware_version_check"]                = [[128, 2, 4, 179], "No Input"]

        self.command_dictionary["read_breaker_rating_request"]           = [[128, 4, 4, 24], "No Input"]
        self.command_dictionary["read_breaker_rating_check"]          = [[128, 0, 4, 24], "No Input"]
        self.command_dictionary["write_breaker_rating_request"]          = [[128, 2, 4, 25, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["write_breaker_rating_check"]         = [[128, 0, 4, 25], "No Input"]
        self.command_dictionary["read_breaker_frame_request"]            = [[128, 4, 4, 28], "No Input"]
        self.command_dictionary["read_breaker_frame_check"]              = [[128, 0, 4, 28], "No Input"]   
        self.command_dictionary["write_breaker_frame_request"]           = [[128, 2, 4, 29, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["write_breaker_frame_check"]             = [[128, 0, 4, 29], "No Input"]

        self.command_dictionary["write_breaker_frame_request"]           = [[128, 2, 4, 29, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["write_breaker_frame_check"]             = [[128, 0, 4, 29], "No Input"]

            
    def set_family(self, family):
        self.family = family
        if family == "MCCB":
            self.command_dictionary["clear_secondary_injection_request"]    = [[128, 4, 11, 3], "No Input"]
            self.command_dictionary["clear_secondary_injection_check"]      = [[128, 8, 11, 3], "No Input"]
        if family != "MCCB":
            print("pass")
        if family == "35":
            self.add_pxr_35(family)


    def add_pxr_35(self, frame):

        self.command_dictionary["read_breaker_rating_request"]           = [[128, 4, 4, 24], "No Input"]
        self.command_dictionary["read_breaker_rating_check"]          = [[128, 0, 4, 24], "No Input"]
        self.command_dictionary["write_breaker_rating_request"]          = [[128, 2, 4, 25, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["write_breaker_rating_check"]         = [[128, 0, 4, 25], "No Input"]
        self.command_dictionary["write_breaker_frame_request"]           = [[128, 2, 4, 29, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["write_breaker_frame_check"]             = [[128, 0, 4, 29], "No Input"]
        self.command_dictionary["read_breaker_frame_request"]            = [[128, 4, 4, 28], "No Input"]
        self.command_dictionary["read_breaker_frame_check"]           = [[128, 0, 4, 28], "No Input"]

                            
        
        self.command_dictionary["read_setpoint_zero_request"]           = [[128, 0, 0, 8], "No Input"]
        self.command_dictionary["read_setpoint_one_request"]            = [[128, 0, 0, 16], "No Input"]
        self.command_dictionary["read_setpoint_two_request"]            = [[128, 0, 0, 24], "No Input"]
        self.command_dictionary["read_setpoint_three_request"]          = [[128, 0, 0, 32], "No Input"]
        self.command_dictionary["read_setpoint_four_request"]           = [[128, 0, 0, 40], "No Input"]
        self.command_dictionary["read_setpoint_five_request"]           = [[128, 0, 0, 48], "No Input"]
        self.command_dictionary["read_setpoint_six_request"]            = [[128, 0, 0, 56], "No Input"]
        self.command_dictionary["read_setpoint_seven_request"]          = [[128, 0, 0, 64], "No Input"]
        self.command_dictionary["read_setpoint_eight_request"]          = [[128, 0, 0, 72], "No Input"]
        self.command_dictionary["read_setpoint_nine_request"]           = [[128, 0, 0, 80], "No Input"]
        self.command_dictionary["read_setpoint_ten_request"]            = [[128, 0, 0, 88], "No Input"]
        
        self.command_dictionary["write_setpoint_zero_request"]          = [[128, 2, 0, 8, 1, 1, 75], "dictionary and Keys"]
        self.command_dictionary["write_setpoint_one_request"]           = [[128, 2, 0, 16, 1, 1, 77], "dictionary and Keys"]
        self.command_dictionary["write_setpoint_two_request"]           = [[128, 2, 0, 24, 1, 1, 9], "dictionary and Keys"]
        self.command_dictionary["write_setpoint_three_request"]         = [[128, 2, 0, 32, 1, 1, 35, 0], "dictionary and Keys"]
        self.command_dictionary["write_setpoint_four_request"]          = [[128, 2, 0, 40, 1, 1, 35], "dictionary and Keys"]
        self.command_dictionary["write_setpoint_five_request"]          = [[128, 2, 0, 48, 1, 1, 93], "dictionary and Keys"]
        self.command_dictionary["write_setpoint_six_request"]           = [[128, 2, 0, 56, 1, 1, 61], "dictionary and Keys"]
        self.command_dictionary["write_setpoint_seven_request"]         = [[128, 2, 0, 64, 1, 1, 33], "dictionary and Keys"]
        self.command_dictionary["write_setpoint_eight_request"]         = [[128, 2, 0, 72, 1, 1, 71], "dictionary and Keys"]
        self.command_dictionary["write_setpoint_nine_request"]          = [[128, 2, 0, 80, 1, 1, 33], "dictionary and Keys"]
        self.command_dictionary["write_setpoint_nine_request"]          = [[128, 2, 0, 88, 1, 1, 182, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255], "dictionary and Keys"]



        self.command_dictionary["read_real_time_data_buffer_fifteen_request"]           = [[128, 0, 1, 15], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_eighteen_request"]          = [[128, 0, 1, 18], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_nineteen_request"]          = [[128, 0, 1, 19], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_twenty_request"]            = [[128, 0, 1, 20], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_twenty_two_request"]        = [[128, 0, 1, 22], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_twenty_three_request"]      = [[128, 0, 1, 23], "No Input"]
        
        self.command_dictionary["read_real_time_data_buffer_fourty_two_request"]        = [[128, 0, 1, 42], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_fourty_three_request"]      = [[128, 0, 1, 43], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_fourty_eight_request"]      = [[128, 0, 1, 48], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_fourty_nine_request"]       = [[128, 0, 1, 49], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_fifty_request"]             = [[128, 0, 1, 50], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_fifty_one_request"]         = [[128, 0, 1, 51], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_fifty_two_request"]         = [[128, 0, 1, 52], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_fifty_three_request"]       = [[128, 0, 1, 53], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_fifty_four_request"]        = [[128, 0, 1, 54], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_fifty_five_request"]        = [[128, 0, 1, 55], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_fifty_seven_request"]       = [[128, 0, 1, 57], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_fifty_eight_request"]       = [[128, 0, 1, 58], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_fifty_nine_request"]        = [[128, 0, 1, 59], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_sixty_request"]             = [[128, 0, 1, 60], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_sixty_one_request"]         = [[128, 0, 1, 61], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_sixty_two_request"]         = [[128, 0, 1, 62], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_sixty_three_request"]       = [[128, 0, 1, 63], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_sixty_four_request"]        = [[128, 0, 1, 64], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_sixty_five_request"]        = [[128, 0, 1, 65], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_sixty_six_request"]         = [[128, 0, 1, 66], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_sixty_seven_request"]       = [[128, 0, 1, 67], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_sixty_nine_request"]        = [[128, 0, 1, 69], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_seventy_request"]           = [[128, 0, 1, 70], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_seventy_one_request"]       = [[128, 0, 1, 71], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_seventy_two_request"]       = [[128, 0, 1, 72], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_seventy_three_request"]     = [[128, 0, 1, 73], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_seventy_four_request"]      = [[128, 0, 1, 74], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_seventy_five_request"]      = [[128, 0, 1, 75], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_seventy_six_request"]       = [[128, 0, 1, 76], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_seventy_seven_request"]     = [[128, 0, 1, 77], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_seventy_eight_request"]     = [[128, 0, 1, 78], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_seventy_nine_request"]      = [[128, 0, 1, 79], "No Input"]
        self.command_dictionary["read_real_time_data_buffer_eighty_request"]            = [[128, 0, 1, 80], "No Input"]
        self.command_dictionary["read_simulated_test_results_request"]                  = [[128, 0, 3, 32],  "No Input"]

                            
        self.command_dictionary["test_led_active_request"]          = [[128, 4, 11, 5, 1, 1, 2, 0], "Uint08"]
        self.command_dictionary["test_led_active_check"]            = [[128, 8, 11, 5], "No Input"]
        self.command_dictionary["test_active_relay_request"]        = [[128, 4, 11, 6, 1, 1, 2, 0], "Uint16"]
        self.command_dictionary["test_active_relay_check"]          = [[128, 8, 11, 6], "No Input"]
        self.command_dictionary["trip_TA_request"]                  = [[128, 4, 11, 7], "No Input"]
        self.command_dictionary["trip_TA_check"]                    = [[128, 8, 11, 7], "No Input"]
        self.command_dictionary["cancel_secondary_injection_test_request"]               = [[128, 4, 3, 13],  "No Input"]
        self.command_dictionary["cancel_secondary_injection_test_check" ]                = [[128, 0, 3, 13],  "No Input"]

        self.command_dictionary["calibrate_current_gain_test_injection_request"]         = [[128, 4, 4, 215, 1, 1, 2, 0],  "Uint08"]
        self.command_dictionary["calibrate_curent_gain_test_injection_check"]            = [[128, 0, 4, 215],    "No Input"]
        
        self.command_dictionary["calibrate_current_offset_test_injection_request"]       = [[128, 4, 4, 214, 1, 1, 2, 0],  "Uint08"]
        self.command_dictionary["calibrate_curent_offset_test_injection_check"]          = [[128, 0, 4, 214],  "No Input"]

        self.command_dictionary["write_breaker_configuraiton"]                           = [[128, 2, 4, 111, 1, 1, 34], "dictionary and Keys"]
        self.command_dictionary["read_breaker_configuraiton_request"]                    = [[128, 0, 4, 111], "No Input"]
        self.command_dictionary["enter_password_request"]                                = [[128, 4, 3, 14, 1, 1, 6, 0], "Uint08"]


   
            
    def get_message(self, def_name, *argv):
  
        info_array = self.command_dictionary[def_name]
##        try: 
##            info_array = self.command_dictionary[def_name]
##        except Exception as e:
##            print(e)
##            print("{} is not a method".format(def_name))
##            add_data = ""
##            return False

        packet_start  = info_array[0]
        add_data = info_array[1]

        if add_data == "No Input":
            tx, packet = self.add_no_input(packet_start)
        elif add_data == "Uint08":
            tx, packet = self.add_uint_eight(packet_start, *argv)
        elif add_data == "Uint16":
            tx, packet = self.add_uint_sixteen(packet_start, *argv)
        elif add_data == "Uint32":
            tx, packet = self.add_uint_thirty_two(packet_start, *argv)
        elif add_data == "Float":
            tx, packet = self.add_uint_float(packet_start, *argv)
        elif add_data == "dictionary and Keys":
            tx, packet = self.dictionary_and_keys(packet_start, argv[0], argv[1])
        elif add_data == "Secondary":
            tx, packet = self.secondary(packet_start, argv[0], argv[1])
        elif add_data == "char":
            tx, packet = self.add_char(packet_start, *argv)
        elif add_data == "Uint08_Array":
            tx, packet = self.add_uint_eight_array(packet_start, argv[0])
        elif add_data == "write_breaker_protection_capacity":
            tx, packet = self.write_breaker_protection_capacity(packet_start, argv[0], argv[1])

            
        else:
            print(def_name, " is not a known command")
            return False
            

        return tx, packet



    ''' Packet Manipulation Functions'''

    def calc_checksum(self, Packet):
        

        # compress packet
        packet = []
        for i in range (0, len(Packet)):
            if Packet[i] != '':
                packet.append(Packet[i])
           
        # Hexadecimal to integer conversion
        
        if type(Packet[0]) == hex:
            for i in range(0, len(packet)):
                packet[i] = int(packet[i], 16)
       
            
        # Compute Checksum
        
        LSB_sum, MSB_sum = 0, 0  
        for i in range(0, len(packet)-3):    
            if i%2 == 0: 
                LSB_sum += packet[i]
            elif i%2 == 1: 
                MSB_sum += packet[i]
            
        CheckLSB = LSB_sum % 256 
        CheckMSB = (MSB_sum + int(LSB_sum/256)) % 256

        packet[-3], packet[-2] = CheckLSB, CheckMSB

        return packet
        
    def format_packet(self, packet):
        
        data = str(len(packet))+'B'
        tx = pack(data, *packet)
        
        return tx


    def get_correctness(self, msg):
        
        correctness_byte = msg[12]+msg[13]
        if correctness_byte == '00':
            correctness = "successful"
        elif correctness_byte == '01':
            correctness = "wrong checksum"
        elif correctness_byte == '03':
            correctness = "wrong data type"
        elif correctness_byte == '04':
            correctness = "command is wrong"
        elif correctness_byte == '07':
            correctness = "out of range"
        elif correctness_byte == '20':
            correctness = "busy"
        elif correctness_byte == '30':
            correctness = "in manufacturing mode"
        elif correctness_byte == '31':
            correctness = "not in manufacturing mode"
        elif correctness_byte == '32':
            correctness = "in auto test mode"
        elif correctness_byte == '33':
            correctness = "not in auto test mode"    
        elif correctness_byte =='50':
            correctness = "pending"
        elif correctness_byte == 'a2':
            correctness = "request recieved"
        elif correctness_byte == 'a5':
            correctness = "request time out"
        elif correctness_byte == 'a6':
            correctness = "FRAM write fail"
        elif correctness_byte == 'a7':
            correctness = "condition fail"
        elif correctness_byte == 'a8':
            correctness = "Action feature not supported at style"
        elif correctness_byte =='a9':
            correctness = "password fail"
        elif correctness_byte == 'aa':
            correctness = "setpoint blocked"
        elif correctness_byte == 'ab':
            correctness = "input password"
        elif correctness_byte == 'ff':
            correctness = "Failure"
        elif correctness_byte == 'c0':
            correctness = "no erasable language"
        elif correctness_byte == 'c1':
            correctness = "no memory for language"
        elif correctness_byte == 'c2':
            correctness = "no memory for language"
        elif correctness_byte == 'c3':
            correctness = "error during write"
        elif correctness_byte == 'c4':
            correctness = "code conflict"
        elif correctness_byte == 'c5':
            correctness = "download language error"
        elif correctness_byte == 'c6':
            correctness = "language cant change"
        elif correctness_byte == 'c7':
            correctness = "language frame conflict"
        elif correctness_byte == 'c8':
            correctness = "langauge file conflict" 
        else:
            correctness = "unknown"
  
        return correctness

    '''    
    Insert Data
    '''

    
    def add_no_input(self, packet_start):
        packet_end = [0, 0, 253]

        packet = packet_start + packet_end
      
        packet = self.calc_checksum(packet)
        tx = self.format_packet(packet)

        return tx, packet

    def add_uint_eight_array(self, packet_start, my_array):

        data_packet = []
        
        for val in my_array:
            data_packet.append(val%256)

        packet_end = [0, 0, 253]

        packet = packet_start + data_packet + packet_end
      
        packet = self.calc_checksum(packet)
        tx = self.format_packet(packet)

        return tx, packet
            
    
    def add_uint_eight(self, packet_start, *argv):

        data_packet = []
        
        for val in argv:
            data_packet.append(val%256)

        packet_end = [0, 0, 253]

        packet = packet_start + data_packet + packet_end
      
        packet = self.calc_checksum(packet)
        tx = self.format_packet(packet)

        return tx, packet
        
    
    def add_uint_sixteen(self, packet_start, *argv):


        data_packet = []

        
        for val in argv:
            data_packet.append(val%256)
            data_packet.append(math.floor(val/256))

            

        packet_end = [0, 0, 253]

        packet = packet_start + data_packet + packet_end
      
        packet = self.calc_checksum(packet)
        tx = self.format_packet(packet)

        return tx, packet         



    def add_uint_thirtytwo(self, packet_start, *argv):

        data_packet = []
        
        for val in argv:
            data_packet.append(val%256)
            data_packet.append(math.floor(val/256))
            data_packet.append(math.floor(val/(256*256)))
            data_packet.append(math.floor(val/(256*256*256)))
            

        packet_end = [0, 0, 253]

        packet = packet_start + data_packet + packet_end
      
        packet = self.calc_checksum(packet)
        tx = self.format_packet(packet)

        return tx, packet

    
    def add_float(self, packet_start, *argv):

        data_packet = []
        
        for val in argv:
            data_packet.append(val%256)
            data_packet.append(math.floor(val/256))
            data_packet.append(math.floor(val/(256*256)))
            data_packet.append(math.floor(val/(256*256*256)))
            

        packet_end = [0, 0, 253]

        packet = packet_start + data_packet + packet_end
      
        packet = self.calc_checksum(packet)
        tx = self.format_packet(packet)

        return tx, packet

    def add_char(self, packet_start, argv):

        data_string = str[argv[0]]

        for char in data_string:
            data_packet = int(char)

        packet_end = [0, 0, 253]

        packet = packet_start + data_packet + packet_end
      
        packet = self.calc_checksum(packet)
        tx = self.format_packet(packet)

        return tx, packet       

    def dictionary_and_keys(self, packet_start, keys, dictionary):


        data_packet = []

        
        if  packet_start[3] == 0 or packet_start[3] == 1 or packet_start[3] == 5 or packet_start[3] > 7:


            if self.family == "MCCB":
                vb1 = 255
                vb2 = 255

                if packet_start[3] == 0:
                    vb3 = 7
                elif packet_start[3] == 1:
                    vb3 = 127
                elif packet_start[3] == 2:
                    vb3 = 127
                elif packet_start[3] == 3:
                    vb3 = 127
                elif packet_start[3] == 4:
                    vb3 = 1   
                elif packet_start[3] == 5:
                    vb3 = 31

                data_packet.append(vb1)
                data_packet.append(vb2)
                data_packet.append(vb3)


            elif self.family == "35":
                vb1 = 255
                vb2 = 255
                vb3 = 255
                vb4 = 255
                vb5 = 0
                vb6 = 255


                if packet_start[4] == 16: #Setpoing Group 1 
                    vb1 = 255
                    vb2 = 255
                    vb3 = 255
                    vb4 = 255
                    vb5 = 255

                
                    data_packet.append(vb1)
                    data_packet.append(vb2)
                    data_packet.append(vb3)
                    data_packet.append(vb4)
                    data_packet.append(vb5)

                    

                    
                elif packet_start[3] == 56: #Setpoint Group 6
                    data_packet.append(vb1)
                    data_packet.append(vb2)
                    data_packet.append(vb3)

                elif packet_start[3] == 48: #Setpoint Group 5
                    data_packet.append(vb1)
                    data_packet.append(vb2)
                    data_packet.append(vb3)
                    data_packet.append(vb4)
                    data_packet.append(255)
                    data_packet.append(vb6)
                    data_packet.append(0)
                    

                    
                elif packet_start[3] == 40:  #Setpoint Group 4
                    data_packet.append(vb1)
                    data_packet.append(vb2)
                    data_packet.append(0)
                    
                
                
                elif packet_start[3] == 8: #Setpoint Group 0
                    data_packet.append(vb1)
                    data_packet.append(vb2)
                    data_packet.append(vb3)
                    data_packet.append(vb4)
                    data_packet.append(255)
                elif packet_start[3] == 111: #Configuration
                    data_packet.append(0)
              
                else:
                    data_packet.append(vb1)
                    data_packet.append(vb2)
                    data_packet.append(vb3)
                    data_packet.append(vb4)
                    data_packet.append(vb5)



                
            else:

                if packet_start[3] == 0:
                    style = dictionary["Style1"][0]
                    vb1, vb2, vb3 = self.acb_setpoint_zero_validity_bits(style)
                    
                elif packet_start[3] == 1:
                    vb1 = 247
                    vb2 = 253
                    vb3 = 255

                elif packet_start[3] == 2:
                    vb3 = 127
                elif packet_start[3] == 3:
                    vb3 = 127
                elif packet_start[3] == 4:
                    vb3 = 1   
                elif packet_start[3] == 5:
                    vb1 = 247
                    vb2 = 127
                    vb3 = 6

                data_packet.append(vb1)
                data_packet.append(vb2)
                data_packet.append(vb3)

        
        for key in keys:

##            a = int(dictionary[key][0]%256)
##            b = int(dictionary[key][0]/256)
##            print("a  " + str(a))
##            print("b  " + str(b)) 
            data_packet.append(int(dictionary[key][0]%256))
            data_packet.append(int(dictionary[key][0]/256))

        if packet_start[3] == 5:
            for k in range(10):
                data_packet.append(0)

        packet_end = [0, 0, 253]


        if packet_start[6] == 93:
            data_packet = data_packet[:-4]


        packet = packet_start + data_packet + packet_end
      
        packet = self.calc_checksum(packet)
        tx  = self.format_packet(packet)

        return tx, packet

    def secondary(self, msg, phase, current): #Table 149-150

        I_byte_four  = (math.floor(current/(256*256*256)))%256
        I_byte_three = (math.floor(current/(256*256)))%256
        I_byte_two   = (math.floor(current/(256)))%256
        I_byte_one   = current%256

        packet = msg +  [phase, 0, I_byte_one, I_byte_two, I_byte_three, I_byte_four, 0, 0, 253] #Table 149 software RMS test with trip request from PC 
        
        packet = self.calc_checksum(packet)
        tx = self.format_packet(packet)


        return tx, packet


    

    def write_breaker_protection_capacity(self, packet_start, keys, breaker_protection_capacity): #Table 544-545

       
        
        fa  = breaker_protection_capacity['frame_ap'][0]
        pol = breaker_protection_capacity['poles'][0]
        std = breaker_protection_capacity['standard'][0]
        ct  = breaker_protection_capacity['ct_version'][0]
        wst = breaker_protection_capacity['withstand'][0]
        mcr = breaker_protection_capacity['MCR'][0]
        mil = breaker_protection_capacity['max_interupt_label'][0]
        fc  = breaker_protection_capacity['frame_construction'][0]


        
        fa_byte_two   = math.floor(fa/(256))
        fa_byte_one   = fa%256

        pol_byte_two   = math.floor(pol/(256))
        pol_byte_one   = pol%256

        std_byte_two   = math.floor(std/(256))
        std_byte_one   = std%256

        ct_byte_two   = math.floor(ct/(256))
        ct_byte_one   = ct%256

        wst_byte_four  = math.floor(wst/(256*256*256))
        wst_byte_three = math.floor(wst/(256*256))
        wst_byte_two   = math.floor(wst/(256))
        wst_byte_one   = wst%256

        mcr_byte_four  = math.floor(mcr/(256*256*256))
        mcr_byte_three = math.floor(mcr/(256*256))
        mcr_byte_two   = math.floor(mcr/(256))
        mcr_byte_one   = mcr%256

        mil_byte_four  = math.floor(mil/(256*256*256))
        mil_byte_three = math.floor(mil/(256*256))
        mil_byte_two   = math.floor(mil/(256))
        mil_byte_one   = mil%256

        fc_byte_four  = math.floor(fc/(256*256*256))
        fc_byte_three = math.floor(fc/(256*256))
        fc_byte_two   = math.floor(fc/(256))
        fc_byte_one   = fc%256
        
        packet = [128, 2, 7, 210, 1, 1, 24, 0, fa_byte_one, fa_byte_two, pol_byte_one, pol_byte_two,
            std_byte_one, std_byte_two, wst_byte_four, wst_byte_three, wst_byte_two, wst_byte_one,
            mcr_byte_four, mcr_byte_three, mcr_byte_two, mcr_byte_one,
            mil_byte_four, mil_byte_three, mil_byte_two, mil_byte_one,
            fc_byte_four, fc_byte_three, fc_byte_two, fc_byte_one,
            0, 0, 253]

        
        tx = self.calc_checksum(packet)
        tx = self.format_packet(tx)

        return tx, packet



    def acb_setpoint_zero_validity_bits(self, style):
        

        if style == 0 or style == 1 or style == 2 or style == 3 or style == 6 or style == 7:
            vb_one = 199
        else:
            vb_one = 247

        if style == 6 or style == 7 or style == 8 or style == 9:
            vb_two = 233
        else:
            vb_two = 232

        if style == 0 or style == 1 or style == 6 or style == 10 or style == 11:
            vb_three = 56
        elif style == 2 or style == 3 or style == 4 or style == 5:
            vb_three = 120
        elif style == 6 or style == 8:
            vb_three = 62
        else:
            vb_three = 126
        return vb_one, vb_two, vb_three

    
    def acb_setpoint_one_validity_bits(self, style):
        

        vb_one = 247

        if style == 0 or style == 1 or style == 6 or style == 8 or style == 10 or style == 11:
            vb_two = 63
        else:
            vb_two = 253

        if style == 0 or style == 1 or style == 6 or style == 8 or style == 10 or style == 11:
            vb_three = 176
        else:
            vb_three == 255

        return vb_one, vb_two, vb_three

    

    def acb_setpoints_two_validity_bits(self, style):
        if style == 0 or style == 2 or style == 4 or style == 11:
            vb_one = 0

        else:
            vb_one = 15

        return vb_one





















                                        
