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
                
    Module:     Test.py
                
    Mechanics:  program module containing the functions related the generation 
                of the test report  
                
                Testcase Class: used to create test case object 
                
                Class Functions: 
                    __init__ - initialize test case object from master data
                
                Module Functions:
                    main - generate test report 
                    name   - creates test report name 
                    header - writes header for test report
                    label  - writes labels for test report  
                    value  - writes test case data for test report
                                         
----------------------------------------------------------------------------'''

import math, random, time


def secondary_generic(usb, phase, I, start, check, cancel):


    if phase == "A":
        phase = 1
    elif phase == "B":
        phase = 2
    else:
        phase = 3
        
    rsp = usb.communicate(start, phase, I)
    print(rsp)
    time.sleep(.1)
    not_finished = True
    while not_finished:
        rsp = usb.communicate(check) 
        print(rsp)
        correctness = usb.get_correctness(rsp)

        if correctness == "successful":
            trip_occur = True
            break

        elif correctness == "Failure":
            fail_count = fail_count + 1
            if fail_count > 5:
                trip_occur = False
                break
        elif correctness == "busy":
            print("I am busy")
            pass
            
        else:
            print("something went wrong")
            trip_occur = False
            break
            
    if trip_occur == True:    

        simulated_results = usb.communicate("read_simulated_test_results_request")

    else:
        simulated_results = "NONE"

    return simulated_results

def secondary_time(repos, usb, start, check, cancel, cancel_check):


    t_target = repos.expected['Max Time']
    t_wd = (repos.expected['Max Time']+5)*1.2
    t_wd = round(t_wd, 3)


    time.sleep(2)
    
    I = int(max(repos.expected['I A (Amps)'], repos.expected['I B (Amps)'], repos.expected['I C (Amps)']))
    print("The current is ", I)

    if I == repos.expected['I A (Amps)']:
        phase = 1
    elif I == repos.expected['I B (Amps)']:
        phase = 2
    else:
        phase = 3

    if repos.neutral == 1:
        phase = 4

    phase = 1
    trip_occur = False
    not_finished = True
    no_read = False
    fail_count = 0
    
    rsp = usb.communicate(start, phase, I)
    correctness = usb.get_correctness(rsp)
    start = time.time()


    while not_finished:
        time.sleep(.1)
        current_time = time.time() - start
        current_time = round(current_time, 3)
        
        
        rsp = usb.communicate(check)    
        correctness = usb.get_correctness(rsp)
        
        
        msg = "Max Time " + str(t_wd) + " Current Time " + str(current_time)
        repos.append_output_msg(msg)

        if correctness == "successful":
            trip_occur = True
            break

        if correctness == "Failure":
            fail_count = fail_count + 1
            if fail_count > 5:
                break
            
        elif current_time > t_wd:
            
            if repos.family == "MCCB":
                rsp_one = usb.communicate("read_real_time_data_buffer_one_request")   
                rsp_two = usb.communicate("read_real_time_data_buffer_ten_request")
                repos.translator.translate_generic(rsp_one, repos.buffer_one_keys, repos.etu_dictionary)
                repos.translator.translate_generic(rsp_two, repos.buffer_ten_keys, repos.etu_dictionary)
##                array = repos.translator.translate_buffer_one(rsp_one, "PXR20")
##                repos.update_buffers(array, 1)
##                array = repos.translator.translate_buffer_ten(rsp_two, "PXR20")
##                print(array)
##                repos.update_buffers(array, 10)

            elif repos.family == "ACB" and current_time >.5 and no_read == True:
                rsp = usb.communicate("read_real_time_data_buffer_ten_request")
                array = repos.translator.translate_buffer_ten(rsp)
                repos.update_buffers(array, 10)
                no_read = False
                
            
            break
        
        elif correctness == "busy":
            print("I am busy")
            pass
            
        else:
            print("something went wrong")
            break

        
    if trip_occur == True:
        if repos.family == "35":
            simulated_results = rsp
        else: 
            simulated_results = usb.communicate("read_simulated_test_results_request")

    else:
        rsp = usb.communicate(cancel)
        rsp = usb.communicate(cancel_check)

        if repos.family == "35":
            simulated_results = usb.communicate("read_simulated_test_results_request")
            
        simulated_results = None

    return simulated_results



def secondary_meter(repos, usb, start, check, cancel):


    t_target = repos.expected['Max Time']
    t_wd = 7
    
    I = max(repos.expected['I A (Amps)'], repos.expected['I B (Amps)'], repos.expected['I C (Amps)'])
    print("The current is ", I)

    if I == repos.expected['I A (Amps)']:
        phase = 1
    elif I == repos.expected['I B (Amps)']:
        phase = 2
    else:
        phase = 3

    #phase = 5
    rsp = usb.communicate(start, phase, I)
    #rsp = usb.communicate(cancel)
    
    correctness = usb.get_correctness(rsp)

    
    trip_occur = False
    not_finished = True
    no_read = True
    start = time.time()
    time.sleep(1)
    
    while not_finished:

        current_time = time.time() - start
        
        time.sleep(1)
        rsp = usb.communicate(check)
        
        correctness = usb.get_correctness(rsp)
        
        msg = "Max Time " + str(t_wd) + " Current Time " + str(current_time)
        repos.append_output_msg(msg)

        if correctness == "successful":
            trip_occur = True
            break

        elif correctness == "failure" or current_time > t_wd:

            if repos.family == "MCCB":
                rsp_one = usb.communicate("read_real_time_data_buffer_one_request")   
                rsp_two = usb.communicate("read_real_time_data_buffer_ten_request")
                GT_MCCB_Translator.update_buffer_one_current(repos, rsp_one)
                GT_MCCB_Translator.update_buffer_ten(repos, rsp_two)

            elif repos.family == "ACB" and current_time > 5:
                rsp = usb.communicate("read_real_time_data_buffer_ten_request")
                array = repos.translator.translate_buffer_ten(rsp)
                repos.update_buffers(array, 10)
                no_read = False
                
            rsp = usb.communicate(cancel)
            
            

            
            break
        
        elif correctness == "busy":
            pass
        
        else:
            print("something went wrong")
            break


        
    time.sleep(5)   
    if trip_occur == True:    
        simulated_results = usb.communicate("read_simulated_test_results_request")

    else:
        simulated_results = None

    return simulated_results


def translate_secondary_results(results):

    time_one_hex   = results[24:26] #This is the first byte that trip time
    time_two_hex   = results[27:29] #This is the second  byte that trip time
    time_three_hex = results[30:32] #This is the third  byte that trip time
    time_four_hex  = results[33:35] #This is the fourth  byte that trip time

    trip_time = int(time_one_hex, 16) + int(time_two_hex, 16)*256 + int(time_three_hex, 16)*256*256 +int(time_four_hex, 16)*256*256*256 
    trip_time = float(trip_time)/1000

    cur_one_hex    = results[48:50]
    cur_two_hex    = results[51:53]
    cur_three_hex  = results[54:56]
    cur_four_hex   = results[57:59]

    current = int(cur_one_hex, 16) + int(cur_two_hex, 16)*256 + int(cur_three_hex, 16)*256*256 +int(cur_four_hex, 16)*256*256*256

    cau_one_hex   = results[36:38]
    cau_two_hex   = results[39:41]
    cau_four_hex = results[42:44]
    cau_three_hex  = results[45:47]

    #cause_of_trip = int(cau_one_hex, 16) + int(cau_two_hex, 16)*256 + int(cau_three_hex, 16)*256*256 +int(cau_four_hex, 16)*256*256*256

    cause_of_trip = int(cau_four_hex, 16) + int(cau_three_hex,16)*256

    if cause_of_trip == 3:
        trip_type = "Instantaneous"
    elif cause_of_trip == 61:
        trip_type = "Long Delay"
    elif cause_of_trip == 62:
        trip_type = "Short Delay"
    elif cause_of_trip == 76:
        trip_type = "Fixed Hardware"
    elif cause_of_trip == 84:
        trip_type = "Ground Fault"
    elif cause_of_trip == 85:
        trip_type = "Ground Fault"
    elif cause_of_trip == 153:
        trip_type = "MM Mode"
    else:
        trip_type = "Code is " + str(cause_of_trip)
        

    return trip_time, current, cause_of_trip

