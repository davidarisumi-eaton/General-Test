import time, math
from GT import GT_Omicron

def calibrate(master):

        if master.pxr != "PXR10":
            pxr_20_and_25_cal(master)
        else:
            pxr_10_cal(master)
            
'''
=========================================================================================================================================================================================
PXR 20/25 Calibration 
=========================================================================================================================================================================================
'''

def pxr_20_and_25_cal(repos, usb, omi):    #  frame calibration routine
    
    check0 = enter_into_manufactory_mode(repos, usb)
    time.sleep(1)

    check1 = reset_internal_calibration(repos, usb)
    time.sleep(1)
    
    check2 = internal_calibration(repos, usb, omi)
    time.sleep(1)

    
    if repos.pxr != "PXR10" and repos.pxr != "PXR20":
        check3 = reset_external_calibration(repos, usb)
        time.sleep(1)
                          
        check4 = external_calibration(repos, usb, omi)      
        time.sleep(1)

    else:
        msg = "External Cal Skipped"
        check3 = 1
        check4 = 1
        
    check5 = exit_out_of_manufactory_mode(repos, usb)

    time.sleep(1)
    check = check0 & check1 & check2 & check3 & check4 & check5
    
'''
=========================================================================================================================================================================================
PXR 20/25 Calibration Functions
=========================================================================================================================================================================================
'''
def reset_internal_calibration(repos, usb):

    #Clears internal scale facotrs for phase a, b, c and n    
    rsp = usb.communicate('clear_internal_I_four_pole_current_scale_factor_request')
    
    rsp = usb.communicate('clear_internal_I_four_pole_current_scale_factor_check')
    
    cor = usb.get_correctness(rsp)
    
    if cor == "successful":
        check1 = 1
    else:
        check1 = 0
        
    time.sleep(1)
    
    #Clears internal I offset
    rsp = usb.communicate('clear_internal_I_offset_request')
    
    rsp = usb.communicate('clear_internal_I_offset_check')
    
    cor = usb.get_correctness(rsp)
    
    if cor == "successful":
        check2 = 1
    else:
        check2 = 0 

    time.sleep(1)
    if repos.pxr != "PXR10" and repos.frame != 25 and repos.frame !=26:
        
    #Clears Internal Ig scale factor
        rsp = usb.communicate('clear_internal_Ig_scale_request')
        
        rsp = usb.communicate('clear_internal_Ig_scale_result_check')
        
        cor = usb.get_correctness(rsp)
        
        if cor == "successful":
            check3 = 1
        else:
            check3 = 0 
        
    else:
        check4 = 1
        check5 = 1

    check = check1 & check2 & check3 
    return check

def internal_calibration(repos, usb, omi):
    
    
    time.sleep(5)
    #Creates new offset for internal current
    rsp = usb.communicate('internal_I_offset_calibration_request')
    
    rsp = usb.communicate('internal_I_offset_calibration_check')
    
    cor = usb.get_correctness(rsp)
    
    time.sleep(1)
    not_finished = True
    
    while not_finished:
        rsp = usb.communicate('internal_I_offset_calibration_check')
        
        cor = usb.get_correctness(rsp)
        
        if cor == 'successful':
            check1 = 1
            break
        elif cor == 'failure':
            check1 = 0
            break
        elif cor == "busy":
            time.sleep(1)
        else:
            check1 = 0
            break
        
        
    cal_point =  repos.setpoints['rating'] * 1.1 

    repos.expected['I_test_A']= cal_point
    repos.expected['I_test_B']= cal_point
    repos.expected['I_test_C']= cal_point


    #Calibration For A B and C

    #Scales internal current scale factor for phase a, b and c.
    cal_request = "interal_Ia_scale_calibration_request"
    cal_check   = "interal_Ia_scale_calibration_check"
    phase = "A"
    check_a = calibrate_phase(repos, usb, omi, cal_point, cal_request, cal_check, phase)
    
    cal_request = "interal_Ib_scale_calibration_request"
    cal_check   = "interal_Ib_scale_calibration_check"
    phase = "B"
    check_b = calibrate_phase(repos, usb, omi, cal_point, cal_request, cal_check, phase)
    
    cal_request = "interal_Ic_scale_calibration_request"
    cal_check   = "interal_Ic_scale_calibration_check"
    phase = "C"
    check_c = calibrate_phase(repos, usb, omi, cal_point, cal_request, cal_check, phase)


    time.sleep(5)
    if repos.pxr != "PXR10" and repos.frame != 25 and repos.frame !=26:
        cal_request = "interal_Ig_scale_calibration_request"
        cal_check   = "interal_Ig_scale_calibration_check"
        phase = "ground"
        check_g = calibrate_phase(repos, usb, omi, cal_point, cal_request, cal_check, phase)
    else:
        check_g = 1
    


    check = check_a & check_b & check_c & check_g
    return check

def reset_external_calibration(repos, usb):

    time.sleep(2)
    #Clears extneral I and V offset

    rsp = usb.communicate('clear_external_I_V_offset_request') 
    rsp = usb.communicate('clear_external_I_V_offset_check')
    
    cor = usb.get_correctness(rsp)
    if cor == "successful":
        check1 = 1
    else:
        check1 = 0

    rsp = usb.communicate('clear_external_current_scale_request')
    rsp = usb.communicate('clear_external_current_scale_check')
    
    cor = usb.get_correctness(rsp)
    
    if cor == "successful":
        check2 = 1
    else:
        check2 = 0
        
    check = check1 & check2
    return check

def external_calibration(repos, usb, omi):

    time.sleep(5)
    #Calibrates extrnal current and voltage offset
    rsp = usb.communicate('external_I_V_offset_calibration_check')
    

    time.sleep(1)
    not_finished = True
    while not_finished:
        
        rsp = usb.communicate('external_I_V_offset_calibration_result')
        
        cor = usb.get_correctness(rsp)
        if cor == 'successful':
            check1 = 1
            break
        elif cor == 'failure':
            check1 = 0
            break
        elif cor == "busy":
            time.sleep(1)
        else:
            check1 = 0
            break
                
            
    cal_point =  repos.setpoints['rating'] * 1.1

    repos.expected['I_test_A']= cal_point
    repos.expected['I_test_B']= cal_point
    repos.expected['I_test_C']= cal_point

    

    #Scales internal current scale factor for phase a, b and c.
    cal_request = "external_Ia_scale_factor_calibration_request"
    cal_check   = "external_Ia_scale_calibration_check"
    phase = "A"
    check_a = calibrate_phase(repos, usb, omi, cal_point, cal_request, cal_check, phase)
    
    cal_request = "external_Ib_scale_factor_calibration_request"
    cal_check   = "external_Ib_scale_calibration_check"
    phase = "B"
    check_b = calibrate_phase(repos, usb, omi, cal_point, cal_request, cal_check, phase)
    
    cal_request = "external_Ic_scale_factor_calibration_request"
    cal_check   = "external_Ic_scale_calibration_check"
    phase = "C"
    check_c = calibrate_phase(repos, usb, omi, cal_point, cal_request, cal_check, phase)
                          
    
    check = check1 & check_a & check_b & check_c
    return check


def calibrate_phase(repos, usb, omi, cal_point, cal_request, cal_check, phase):
    time.sleep(5)
    omi.calibration_start(repos, phase, cal_point)

    rsp = usb.communicate(cal_request, cal_point)
    

    not_finished = True
    while not_finished:
        rsp = usb.communicate(cal_check)
        
        cor = usb.get_correctness(rsp)
        
        if cor == "successful":
            check =1
            break
        elif cor == "failure":
            check = 0
            break
        elif cor == "busy":
            pass
        else:
            check = 0
            break
                
        time.sleep(1)   
        
    omi.calibration_end()
    return check
    




'''
=========================================================================================================================================================================================
PXR10 Calibration
=========================================================================================================================================================================================
'''

def pxr_10_cal(master):

    check0 = GT_USB_commands.enter_into_manufactory(master)

    time.sleep(5)
    
    tx = [128, 2, 6, 158, 1, 1, 8, 0, 0, 0,
                                      0, 0,
                                      0, 0, 
                                      0, 0,
                                      0, 0, 253]

    tx = GT_USB_commands.calc_checksum(tx)
    tx, px = GT_USB_commands.format_packet(tx)  
    reset_reply= master.USB.command(tx, 'NULL') #Resets offset cal
    
    if master.rating == 60 or master.rating == 63 or master.rating == 100:
        radian = 15
    elif master.rating == 150 or master.rating == 160:
        radian = 30
    else:
        radian = 50



    #Gets Unmetered data value
    master.ldpu = 1
    master.I_test= radian
    
    GT_Omicron.calibration_start(master, "A")

    time.sleep(25)
    
    tx = [128, 0, 1, 10, 0, 0, 253]
    tx = GT_USB_commands.calc_checksum(tx)
    tx, px = GT_USB_commands.format_packet(tx)  
    phase_A_data = master.USB.command(tx, 'Read_Buffer_1') #Gets real time data from buffer 1

    
    GT_Omicron.calibration_end()

    time.sleep(5)

    GT_Omicron.calibration_start(master, "B")

    time.sleep(25)
    
    tx = [128, 0, 1, 10, 0, 0, 253]
    tx = GT_USB_commands.calc_checksum(tx)
    tx, px = GT_USB_commands.format_packet(tx)  
    phase_B_data = master.USB.command(tx, 'Read_Buffer_1') #Gets real time data from buffer 1
    
    GT_Omicron.calibration_end()

    time.sleep(5)

    GT_Omicron.calibration_start(master, "C")

    time.sleep(25)
    
    tx = [128, 0, 1, 10, 0, 0, 253]
    tx = GT_USB_commands.calc_checksum(tx)
    tx, px = GT_USB_commands.format_packet(tx)  
    phase_C_data = master.USB.command(tx, 'Read_Buffer_1') #Gets real time data from buffer 1
    
    GT_Omicron.calibration_end()


    a_hex_one = phase_A_data[30]
    a_hex_two = phase_A_data[33]
    a_hex_three = phase_A_data[34]
    a_dec_hex = phase_A_data[31]

    a_qfour = int(a_dec_hex, 16)
    a_dec = a_qfour/float(16)

    myByte = a_hex_two + a_hex_three + a_hex_one
    a_int = int(myByte, 16)
    a_measured = a_int + a_dec
 
    b_hex_one = phase_B_data[42]
    b_hex_two = phase_B_data[45]
    b_hex_three = phase_B_data[46]
    b_dec_hex = phase_B_data[43]

    b_qfour = int(b_dec_hex, 16)
    b_dec = a_qfour/float(16)

    myByte = b_hex_two + b_hex_three + b_hex_one
    b_int = int(myByte, 16)
    b_measured = b_int + b_dec
    
    c_hex_one = phase_C_data[54]
    c_hex_two = phase_C_data[57]
    c_hex_three = phase_C_data[58]
    c_dec_hex = phase_C_data[55]

    c_qfour = int(c_dec_hex, 16)
    c_dec = a_qfour/float(16)

    myByte = c_hex_two + c_hex_three + c_hex_one
    c_int = int(myByte, 16)
    c_measured = c_int + c_dec

 
    b = 4*radian*math.sqrt(2)/3.14

    c = (radian-a_measured*a_measured/radian)/(4*math.sqrt(2)/3.14)
    a_result = (-b+math.sqrt(b*b - 4*b*c))/2

    c = (radian-b_measured*b_measured/radian)/(4*math.sqrt(2)/3.14)
    b_result = (-b+math.sqrt(b*b - 4*b*c))/2

    c = (radian-c_measured*c_measured/radian)/(4*math.sqrt(2)/3.14)
    c_result = (-b+math.sqrt(b*b - 4*b*c))/2
    
    if master.rating == 60 or master.rating == 63 or master.rating == 100:
        a_offset = (int((a_result/.44)*16))
        b_offset = (int((b_result/.44)*16))
        c_offset = (int((c_result/.44)*16))
    else:
        a_offset = (int((a_result/1.1)*16))
        b_offset = (int((b_result/1.1)*16))
        c_offset = (int((c_result/1.1)*16))


##    ###########################
##    a_offset_byte_one = a_offset % 256
##    a_offset_byte_two = int(math.floor(a_offset / 256))
##    while a_offset_byte_two > 256:
##        a_offset_byte_two = a_offset_byte_two -256
##        
##    a_offset_byte_three = int(math.floor(a_offset / (256**2)))
##    while a_offset_byte_three > 256:
##        a_offset_byte_three = a_offset_byte_three -256
##        
##    a_offset_byte_four = int(math.floor(a_offset / (256**3)))
##
##    #######################################
##        
##    b_offset_byte_one = b_offset % 256
##    b_offset_byte_two = int(math.floor(b_offset / 256))
##    while b_offset_byte_two > 256:
##        b_offset_byte_two = b_offset_byte_two -256
##        
##    b_offset_byte_three = int(math.floor(b_offset / (256**2)))
##    while b_offset_byte_three > 256:
##        b_offset_byte_three = b_offset_byte_three -256
##        
##    b_offset_byte_four = int(math.floor(b_offset / (256**3)))
##
##    ###################################
##    c_offset_byte_one = c_offset % 256
##    c_offset_byte_two = int(math.floor(c_offset / 256))
##    while c_offset_byte_two > 256:
##        c_offset_byte_two = c_offset_byte_two -256
##        
##    c_offset_byte_three = int(math.floor(c_offset / (256**2)))
##    while c_offset_byte_three > 256:
##        c_offset_byte_three = c_offset_byte_three -256
##        
##    c_offset_byte_four = int(math.floor(c_offset / (256**3)))

    if a_offset < 0:
        counter = 0 
        while True:
            counter = counter + 1
            a_offset_byte_one = int(256 * counter + a_offset)
            a_offset_byte_two = 256 - counter
            if a_offset_byte_one >= 0:
                break
    else:
        a_offset_byte_one = int(a_offset % 256)
        a_offset_byte_two = int(a_offset / 256)
    if b_offset < 0:
        counter = 0 
        while True:
            counter = counter + 1
            b_offset_byte_one = int(256 * counter + b_offset)
            b_offset_byte_two = 256 - counter
            if b_offset_byte_one >= 0:
                break
    else:
        b_offset_byte_one = int(b_offset % 256)
        b_offset_byte_two = int(b_offset / 256)
    if c_offset < 0:
        counter = 0 
        while True:
            counter = counter + 1
            c_offset_byte_one = int(256 * counter + c_offset)
            c_offset_byte_two = 256 - counter
            if c_offset_byte_one >= 0:
                break
    else:
        c_offset_byte_one = int(c_offset % 256)
        c_offset_byte_two = int(c_offset / 256)
    
    tx = [128, 2, 6, 158, 1, 1, 8, 0, a_offset_byte_one, a_offset_byte_two,
                                    b_offset_byte_one, b_offset_byte_two,
                                    c_offset_byte_one, c_offset_byte_two, 
                                    0, 0,
                                    0, 0, 253]


    tx = GT_USB_commands.calc_checksum(tx)
    tx, px = GT_USB_commands.format_packet(tx)  
    response = master.USB.command(tx, 'NULL') #Gets real time data from buffer 1


    time.sleep(10)
    check5 = GT_USB_commands.exit_out_of_manufactory(master)
    
    

'''
=========================================================================================================================================================================================
Calibrate Secondary Injection 
=========================================================================================================================================================================================
'''

def calibrate_secondary_injection(repos, usb):

        enter_into_manufactory_mode(repos, usb)
                
        clear_secondary_injection(repos, usb)
        time.sleep(1)

        secondary_injection_base_counter_calibration(repos, usb) 
        time.sleep(1)

        secondary_injection_delta_counter_calibration(repos, usb)
        time.sleep(1)

        exit_out_of_manufactory_mode(repos, usb)


'''
=========================================================================================================================================================================================
Calibrate Secondary Injection Functions
=========================================================================================================================================================================================
'''


def clear_secondary_injection(repos, usb):
    
    rsp = usb.communicate('clear_secondary_injection_request')
    #rsp = usb.communicate('clear_secondary_injection_check')
    


    finished = False
    while finished == False:

        rsp = usb.communicate('clear_secondary_injection_check')
        
        cor = usb.get_correctness(rsp)

        
        if cor == "successful":
            finished = True
            msg = "Clear Secondary Calibration Finished "
            repos.append_output_msg(msg)
                                    
        elif cor == "busy":
            pass
                                    
        elif cor == "failure":
            finished = True
            msg = "Failed Clear Secondary. Correctness is " + cor
            repos.append_output_msg(msg)
                                    
        else:
            finished = True
            msg = "Other Clear Secondary Problem. Correctness is " + cor
            repos.append_output_msg(msg)

        time.sleep(1)

    
def secondary_injection_base_counter_calibration(repos, usb):
 
    
    rsp = usb.communicate('secondary_injection_base_counter_calibration_request')
    
        
    finished = False

    num_fails = 0 
    while finished == False:

        rsp = usb.communicate('secondary_injection_base_counter_calibration_check')
        
        cor = usb.get_correctness(rsp)

        
        if cor == "successful":
            finished = True
            msg = "Delta Counter Calibration Finished "
            repos.append_output_msg(msg)
                                    
        elif cor == "busy":
            pass
                                    
        elif cor == "failure":
            finished = True
            msg = "Failed Delta Calibration. Correctness is " + cor
            repos.append_output_msg(msg)
                                    
        else:
            msg = "Other Delta Calibration Problem. Correctness is " + cor
            repos.append_output_msg(msg)
            num_fails = num_fails + 1
            if num_fails > 10:
                    finished = True

        time.sleep(1)


def secondary_injection_delta_counter_calibration(repos, usb):


    time.sleep(1)

    rsp = usb.communicate('secondary_injection_delta_counter_calibration_request')
    num_fails = 0
        
    finished = False
    while finished == False:

        rsp = usb.communicate('secondary_injection_delta_counter_calibration_check')
        
        cor = usb.get_correctness(rsp)

        
        if cor == "successful":
            finished = True
            msg = "Delta Counter Calibration Finished "
            repos.append_output_msg(msg)
                                    
        elif cor == "busy":
            pass
                                    
        elif cor == "failure":
            finished = True
            msg = "Failed Delta Calibration. Correctness is " + cor
            repos.append_output_msg(msg)
                                    
        else:
            msg = "Other Delta Calibration Problem. Correctness is " + cor
            repos.append_output_msg(msg)
            num_fails = num_fails + 1
            if num_fails > 10:
                    finished = True

        time.sleep(1)
                                    
    time.sleep(3)

'''
=========================================================================================================================================================================================
ACB Calibration
=========================================================================================================================================================================================
'''

def acb_calibration(repos, usb):

        enter_into_manufactory_mode(repos, usb)

   
        rsp = usb.communicate("write_breaker_plug_request", 630)
        correctness = usb.get_correctness(rsp)
        repos.append_output_msg(correctness)

        not_finished = True
        while not_finished:
            rsp = usb.communicate("write_breaker_plug_check")
            correctness = usb.get_correctness(rsp)
            repos.append_output_msg(correctness)

            if correctness == "busy":
                pass
            else:
                not_finished = False
                

        rsp = usb.communicate("write_breaker_frame_request", 1)
        correctness = usb.get_correctness(rsp)
        repos.append_output_msg(correctness)
        
        not_finished = True
        while not_finished:
            rsp = usb.communicate("write_breaker_frame_check")
            correctness = usb.get_correctness(rsp)
            repos.append_output_msg(correctness)

            if correctness == "busy":
                pass
            else:
                not_finished = False
                
     

        exit_out_of_manufactory_mode(repos, usb)


def acb_current_offset_routine(repos, usb):

        acb_set_rating(repos, usb, 630, 0)
        acb_current_offset(repos, usb)

        acb_set_rating(repos, usb, 320, 1)
        acb_current_offset(repos, usb)

        acb_set_rating(repos, usb, 630, 1)
        acb_current_offset(repos, usb)

        acb_set_rating(repos, usb, 1250, 1)
        acb_current_offset(repos, usb)

        acb_set_rating(repos, usb, 1600, 1)
        acb_current_offset(repos, usb)
        
def acb_current_offset(repos, usb):

        rsp = usb.communicate("recover_current_calibration_etu_request")
        correctness = usb.get_correctness(rsp)
        repos.append_output_msg(correctness)
        
        not_finished = True
        while not_finished:
            rsp = usb.communicate("recover_current_calibtration_etu_check")
            correctness = usb.get_correctness(rsp)
            repos.append_output_msg(correctness)

            if correctness == "busy":
                pass
            else:
                not_finished = False


def acb_calibrate_ground(repos, usb, omicron):

        rsp = usb.communicate("recover_ground_fault_calibration_request")
        rsp = usb.communicate("recover_ground_fault_calibration_check")

        pga_settings = [0, 1, 2, 3, 4, 5, 6, 7]

        for pga in pga_settings:
                rsp = usb.communicate("set_gain_of_pga_request", gain)
                rsp = usb.communicate("set_gain_of_pga_check")
                rsp = usb.communicate("calibration_to_sg_offset_request")
                
                while not_finished:
                    rsp = usb.communicate("calbiration_to_sg_offset_check")
                    correctness = usb.get_correctness(rsp)
                    repos.append_output_msg(correctness)

                    if correctness == "busy":
                        pass
                    else:
                        not_finished = False

        
                
        current_inputs = [80, 200, 400, 800, 1600, 3200, 6400, 12800]
        i = 0
        for current in current_inputs:
                rsp = usb.communicate("set_gain_of_pga_request", pga_settings[i])
                i = i + 1
                
                rsp = usb.communicate("set_gain_of_pga_check")
                rsp = usb.communicate("scalibration_to_sg_gain_scale_factor_request", current)
    
                while not_finished:
                    rsp = usb.communicate("scalibration_to_sg_gain_scale_factor_check")
                    correctness = usb.get_correctness(rsp)
                    repos.append_output_msg(correctness)

                    if correctness == "busy":
                        pass
                    else:
                        not_finished = False
                        
                
                
        
def acb_current_four_pole_cal_routine(repos, usb, omicron):

        acb_set_rating(repos, usb, 630, 0)
        acb_current_four_pole_cal(repos, usb, omicron, 693)

        acb_set_rating(repos, usb, 200, 1)
        acb_current_four_pole_cal(repos, usb, omicron, 352)

        acb_set_rating(repos, usb, 630, 1)
        acb_current_four_pole_cal(repos, usb, omicron, 693)

        acb_set_rating(repos, usb, 1250, 1)
        acb_current_four_pole_cal(repos, usb, omicron, 1375)

        acb_set_rating(repos, usb, 1600, 1)
        acb_current_four_pole_cal(repos, usb, omicron, 1760)
        
def acb_current_four_pole_cal(repos, usb, omicron, cal_factor):

        omicron.calibration_start(repos,"ABC", cal_factor)
        
        rsp = usb.communicate("calibration_to_current_four_pole_gain_scale_factor_to_etu_request", )
        correctness = usb.get_correctness(rsp)
        repos.append_output_msg(correctness)
        
        not_finished = True
        while not_finished:
            rsp = usb.communicate("calibration to current 4 pole gain scale factor to etu check")
            correctness = usb.get_correctness(rsp)
            repos.append_output_msg(correctness)

            if correctness == "busy":
                pass
            else:
                not_finished = False

        omicron.calibration_end()
                
def acb_set_rating(repos, usb, plug, frame):
        
        rsp = usb.communicate("write_breaker_plug_request", plug)
        correctness = usb.get_correctness(rsp)
        repos.append_output_msg(correctness)
        
        not_finished = True
        while not_finished:
            rsp = usb.communicate("write_breaker_plug_check")
            correctness = usb.get_correctness(rsp)
            repos.append_output_msg(correctness)

            if correctness == "busy":
                pass
            else:
                not_finished = False
                

        rsp = usb.communicate("write_breaker_frame_request", frame)
        correctness = usb.get_correctness(rsp)
        repos.append_output_msg(correctness)
        
        not_finished = True
        while not_finished:
            rsp = usb.communicate("write_breaker_frame_check")
            correctness = usb.get_correctness(rsp)
            repos.append_output_msg(correctness)

            if correctness == "busy":
                pass
            else:
                not_finished = False

        

'''
=========================================================================================================================================================================================
Shared Functions
=========================================================================================================================================================================================
'''

def enter_into_manufactory_mode(repos, usb):
        
    check = 1 
    rsp = usb.communicate('enter_into_manufactory_mode_request') 
    cor = usb.communicate_with_check('enter_into_manufactory_mode_check')
    if cor != 'successful':
        msg = "Failed To Enter Into Manufactory Mode. Correctness is " + cor
        repos.append_output_msg(msg)
        check = 0 

    return check    

def exit_out_of_manufactory_mode(repos, usb):

    check = 1
    rsp = usb.communicate('exit_out_of_manufactory_mode_request')
    
    cor = usb.communicate_with_check('exit_out_of_manufactory_mode_check')
    if cor != 'successful':
        msg = "Failed To Exit Out Of Manufactory Mode. Correctness is " + cor
        repos.append_output_msg(msg)
        check = 0

    return check
                                    

        
