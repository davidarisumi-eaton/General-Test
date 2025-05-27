import math 

def trip_result(repos):

    t_max = repos.expected['Max Time']
    t_min = repos.expected['Min Time']
    t_adj = repos.results['Trip Time + Mech']
    trip_time = repos.results['Trip Time']
    
    
    if repos.no_trip_case == True:
        t_max = -1
        repos.expected['Max Time'] = -1

                      
    '''  Analyze trip results - return Pass/Fail '''
    if (t_max == -1 and trip_time == -1):
        result = 'Pass'

    elif (t_max == -1 and t_min == -1 and t_adj != -1):
        result = 'Fail'
        
    elif (t_max == -1 and t_adj> t_min and t_min != -1):
        result = 'Pass'
        
    elif (t_min < t_adj and t_adj < t_max):
        result = 'Pass'
    else:
        result = 'Fail'

    return result

def metering_result(results, expected, UI):

    if expected['I_test_A'] != 0:
        A_error = (results['phase_A'] - expected['I_test_A'])/expected['I_test_A']
    else:
        A_error = 0
    if expected['I_test_B'] != 0:
        B_error = (results['phase_B'] - expected['I_test_B'])/expected['I_test_B']
    else:
        B_error = 0
    if expected['I_test_C'] != 0:
        C_error = (results['phase_C'] - expected['I_test_C'])/expected['I_test_C']
    else:
        C_error = 0

    msg = ("A Error " + str(A_error)
           + "\nB Error " + str(B_error)
           + "\nC Error " + str(C_error))
    UI.write_results(msg)

    if abs(A_error) > 0.05 or abs(B_error) > 0.05 or abs(C_error) > 0.05:
        result = "Fail"
    else:
        result = "Pass"

    return result



def calc_max_min_time(repos):

    if repos.expected['Max Time'] != 0:
        return repos.expected['Max Time'], repos.expected['Min Time'], False
        

    no_trip_case = False


    '''
    =======================
    Lays out Variables Needed For Calculations
    =======================
    '''
    
    setpoints = repos.etu_dictionary
    expected = repos.expected
    family       = repos.family
    style_2      =  setpoints['Style2'][0]

    rating    = int(setpoints['Rating'][0])
    frame     = int(setpoints['Frame'][0])

    #Line Settings
    ldpu      = setpoints['LD PU'][0]
    t_ld      = setpoints['LD Time'][0]
    lds       = setpoints['LD Slope'][0]
    sdpu      = setpoints['SD PU'][0]
    sds       = setpoints['SD Slope'][0]
    t_sd      = setpoints['SD Time'][0]
    ipu       = setpoints['Inst PU'][0]
    gfpu      = setpoints['GF PU'][0]
    t_gf      = setpoints['GF Time'][0]
    gfs       = setpoints['GF Slope'][0]
    gf_mode   = setpoints['GF Mode'][0]
    gf_type   = setpoints['GF Type'][0]
    gf_sensor = setpoints['Source Ground Sensor'][0]
    neutral_level = setpoints['Neutral Ratio'][0]

    #High Current Settings
    try:
        override  = setpoints['Override'] [0] * 1000
    except:
        override  = setpoints['withstand'] [0]
    usb_mm_mode   = setpoints['MM Mode'][0]
    mm_level  = setpoints['MM Level'][0]

    #Motor Protection Settings
    ov_action = int(setpoints['Over V Action'][0])
    ov_pu = setpoints['Over V PU'][0]
    ov_t = setpoints['Over V Time'][0]
    uv_action = int(setpoints['Under V Action'][0])
    uv_pu = setpoints['Under V PU'][0]
    uv_t = setpoints['Under V Time'][0]
    vu_action = int(setpoints['V Unbalance Action'][0])
    vu_pu = setpoints['V Unbalance PU'][0]
    vu_t = setpoints['V Unbalance Time'][0]
    cu_action = int(setpoints['I Unbalance Action'][0])
    cu_pu = setpoints['I Unbalance PU'][0]
    cu_t = int(setpoints['I Unbalance Time'][0])
    pr_action = setpoints['Power Rev Action'][0]
    pl_action = int(setpoints['Phase Loss Action'][0])
    pl_t = setpoints['Phase Loss Time'][0]
    expected_freq = setpoints['Line Frequency'][0]





    if family == "35":
        rp_action = setpoints['Reverse Forward Power Action'][0]
        rp_pu = setpoints['Reverse Forward Power Pickup'][0] * -1000
        rp_t = setpoints['Reverse Forward Power Time'][0]/100
        pr_sense = setpoints['Power Rev Sense'][0]
        sys_volt = setpoints['System Voltage'][0]
        rr_pu     = setpoints['Reverse Reactive Power Pickup'][0] * -1000
        rr_t      = setpoints['Reverse Reactive Power Time'][0]/100
        rr_action = setpoints['Reverse Reactive Power Action'][0]
        pwr_en = setpoints['Power Protection Enable/Disable'][0]
        mtr_en = setpoints['Extended Protection Enable/Disable'][0]
        freq_proc = setpoints['Frequency Protection Enable'][0]
        ofreq_action = setpoints['Over Frequency Action'][0]
        ofreq_pu = setpoints['Over Frequency Pickup'][0]/1000
        ofreq_t = setpoints['Over Frequency Time'][0]/100
        ufreq_action = setpoints['Under Frequency Action'][0]
        ufreq_pu = setpoints['Under Frequency Pickup'][0]/1000
        ufreq_t = setpoints['Under Frequency Time'][0]/100

        #Demand Protection
        pow_int = setpoints['Power Interval'][0] *60
        rpd_action = setpoints['Real Demand Power Action'][0]
        rpd_pu = setpoints['Real Demand Power Pickup'][0]
        rpd_t = setpoints['Real Demand Power Time'][0] * pow_int #demand time is demand time * pow_int
        apd_action = setpoints['Apparent Demand Power Action'][0]
        apd_pu = setpoints['Apparent Demand Power Pickup'][0] * 1000
        apd_t = setpoints['Apparent Demand Power Time'][0] * pow_int 
        rpd_action = 2

        ov_pu = (ov_pu/1000)*sys_volt
        ov_t = ov_t/100

        uv_pu = (uv_pu/1000) * sys_volt
        uv_t = uv_t/100

        vu_pu = vu_pu
        vu_t = vu_t/100

        cu_pu = cu_pu
        cu_t = cu_t/100

        if ov_action == 0:
            ov_action = 1
        else:
            ov_action = 0
            
        if uv_action == 0:
            uv_action= 1
        else:
            uv_action = 0
        uv_action= 1
            
        if vu_action == 0:
            vu_action = 1
        else:
            vu_action = 0

        if cu_action == 0:
            cu_action = 1
        else:
            cu_action = 0


    else:
        pwr_en = 0
        mtr_en = 0
        freq_proc = 0
        rp_action = 2
        rp_pu = 100
        rp_t = 300
        pr_sense = 0
        sys_volt = 240
        rr_pu     = 100
        rr_t      = 300
        rr_action = 2
        ofreq_action = 2
        ofreq_pu = 60
        ofreq_t = 300
        ufreq_action = 2
        ufreq_pu = 60
        ufreq_t = 300

    if pwr_en != 0:
        
        fw_action = setpoints['Forward Real Power Action'][0]
        fw_pu = setpoints['Forward Real Power Pickup'][0]*1000
        fw_t = setpoints['Forward Real Power Time'][0]
        fvar_action = setpoints['Forward Reactive Power Action'][0]
        fvar_pu = setpoints['Forward Reactvie Power Pickup'][0]*1000
        fvar_t = setpoints['Forward Reactive Power Time'][0]
        va_action = setpoints['Apparent Power Action'][0]
        va_pu = setpoints['Apparent Power Pickup'][0]*1000
        va_t = setpoints['Apparent Power Time'][0]
        up_action = setpoints['Under Power Factor Action'][0]
        up_pu = setpoints['Under Power Factor Pickup'][0]
        up_t = setpoints['Under Power Factor Time'][0]


    #Other Important Inputs
    neutral      = repos.neutral


    all_max_times = []
    all_min_times = []


    
    '''
    =========================================================
    Inputs Current/Voltage/Power
    ============================================================
    '''        
    #Inputs
    I_test_A = expected['I A (Amps)']
    I_test_B = expected['I B (Amps)']
    I_test_C = expected['I C (Amps)']

    max_I = max(I_test_A, I_test_B, I_test_C)

    
    #Motor Protection Inputs
    Va = repos.expected['V A']
    Vb = repos.expected['V B']
    Vc = repos.expected['V C']

    #Phase Angles
    freq = setpoints["Source_Freq"][0]
    ra_ang = math.radians(int(setpoints["Ra_Phase_Angle"][0]))
    rb_ang = math.radians(int(setpoints["Rb_Phase_Angle"][0]))
    rc_ang = math.radians(int(setpoints["Rc_Phase_Angle"][0]))
    va_ang = math.radians(int(setpoints["Va_Phase_Angle"][0]))
    vb_ang = math.radians(int(setpoints["Vb_Phase_Angle"][0]))
    vc_ang = math.radians(int(setpoints["Vc_Phase_Angle"][0]))

    pf = (ra_ang -va_ang)
    unit_pf = math.cos(pf)

    a_real_power = I_test_A * Va * math.cos(pf + math.radians(90))#90 Degree Shift For Omicron 
    b_real_power = I_test_B * Vb * math.cos(pf + math.radians(90))#90 Degree Shift For Omicron 
    c_real_power = I_test_C * Vc * math.cos(pf + math.radians(90))#90 Degree Shift For Omicron 
    
    a_reactive_power = I_test_A * Va * math.sin(pf - math.radians(90))#90 Degree Shift For Omicron 
    b_reactive_power = I_test_B * Vb * math.sin(pf - math.radians(90))#90 Degree Shift For Omicron 
    c_reactive_power = I_test_C * Vc * math.sin(pf - math.radians(90))#90 Degree Shift For Omicron 
    
    a_apparent_power = I_test_A * Va
    b_apparent_power = I_test_B * Vb 
    c_apparent_power = I_test_C * Vc
    
    real_power     = max(a_real_power, b_real_power, c_real_power)
    reactive_power = max(a_reactive_power, b_reactive_power, c_reactive_power)
    apparent_power = max(a_apparent_power, b_apparent_power, c_apparent_power)
    
    rev_real_power     = min(a_real_power, b_real_power, c_real_power)
    rev_reactive_power = min(a_reactive_power, b_reactive_power, c_reactive_power)


    #Calculates Line To Line Voltage
    VAB = math.sqrt(((Va + Vb/2)*(Va + Vb/2))+((Vb*math.sqrt(3)/2)*(Vb*math.sqrt(3)/2)))
    VBC = math.sqrt(((Vb + Vc/2)*(Vb + Vc/2))+((Vc*math.sqrt(3)/2)*(Vc*math.sqrt(3)/2)))
    VCA = math.sqrt(((Vc + Va/2)*(Vc + Va/2))+((Va*math.sqrt(3)/2)*(Va*math.sqrt(3)/2)))
    max_V = max(VAB, VBC, VCA)
    min_V = min(VAB, VBC, VCA)

    if max_V == 0: #Avoids Divide By 0 Erros
        max_V =1

    #Calculates Unbalanced %
    try: 
        V_unbal_per = ((max_V - min(VAB, VBC, VCA))/max_V)*100
    except: 
        V_unbal_per = 0
        
    try: 
        I_unbal_per = ((max_I - min(I_test_A, I_test_B, I_test_C))/max_I)*100
    except:
        I_unbal_per = 0



    '''
    =========================================================
    Translating some of the variables
    ============================================================
    '''
        
    if sds == 1:
        sds = 2
    if gfs == 1:
        gfs = 2

    if gfpu == 0: #Not going to be used anyway. Stops divide by 0 error
        gfpu = 1


    ground_I_x = I_test_A * math.cos(0) + I_test_B * math.cos(2.0945) + I_test_C * math.cos(-2.0945)
    ground_I_y = I_test_A * math.sin(0) + I_test_B * math.sin(2.0945) + I_test_C * math.sin(-2.0945)
    ground_I   = math.sqrt((ground_I_x*ground_I_x)+(ground_I_y*ground_I_y)) #Calculation of Residual GF Current Based on a 0, 120, -120 phase configuration

    if max_I == 0:
        max_I = .01 #avoids divide by 0 error
    if ground_I == 0:
        ground_I = .01 #avoids divide by 0 error



    if family == "ACB" or family == "35":
        ldpu = ldpu*rating/100



    '''
    ==================================================================================
    Checks to see if the max trip time needs to be calculated.
    If -1 is set in the excel sheet, then the program will calculate max trip time
    If it is a value other than 1, it will use that as the max time
    ===================================================================================
    '''

    #a neutral level of 60 increases causes the pu to be 60% less
    if neutral == 1:
        if neutral_level == 60:
            sdpu = sdpu*.6
            ldpu = ldpu*.6
            ipu = ipu*.6
        elif neutral_level == 200:
            sdpu = sdpu*2
            ldpu = ldpu*2
            ipu = ipu*2
        elif neutral_level == 0: #Works well enough to check Pickups. Improve in Future.
            sdpu = sdpu*2
            ldpu = ldpu*2
            ipu = ipu*2


    '''
    ===========================================================================================
    Calculates Protection Time Tolerances
    ===========================================================================================
    '''

    'Line Protection Calculations'
    #Calculates Max Long Delay Time, Min Long Delay Time, and the Expectd Long Delay Time
    max_ld, min_ld, long_delay    = calc_long_delay(max_I, ldpu, lds, t_ld)
    
    #Calculates Max Short Delay Time, Min Short Delay Time, and the Expectd Short Delay Time
    max_sd, min_sd, short_delay   = calc_short_delay(max_I, ldpu, sdpu, sds, t_sd)
    
    #Adjusts Long Delay Times Based On Special Rules
    max_ld, min_ld                = calc_long_delay_special_rules(max_I, max_ld, min_ld, short_delay, sdpu, t_sd, frame) #Adjusts Long Delay Times Based On Special Rules

    #Calculates Max Ground Fault Time and Min Ground Fault Time
    max_gf, min_gf                = calc_gf_delay(max_I, rating, gf_type, gf_sensor, gfpu, t_gf, gfs, gf_mode, frame, style_2)

    #Calculates Max Instaneous Time and Min Instantaneous Time
    max_inst, min_inst            = calc_inst(max_I, rating, ipu)

    #Calculates Max Maintenance Mode Time and Min Maintenance Mode Time
    max_mm, min_mm                = calc_mm_mode(max_I, rating, usb_mm_mode, mm_level)

    #Calculates Max Maintenance Mode Time and Min Maintenance Mode Time
    max_override, min_override    = calc_override(max_I, override)

    #Appends the specified trip time to an index of all the max times and all the min times [Trip Time, Trip Name]
    all_max_times, all_min_times  = append_max_and_mins(max_ld, min_ld, "Long Delay", all_max_times, all_min_times) 
    all_max_times, all_min_times  = append_max_and_mins(max_sd, min_sd, "Short Delay", all_max_times, all_min_times) 
    all_max_times, all_min_times  = append_max_and_mins(max_gf, min_gf, "Ground Fault", all_max_times, all_min_times) 
    all_max_times, all_min_times  = append_max_and_mins(max_inst, min_inst, "Instantaneous", all_max_times, all_min_times)
    all_max_times, all_min_times  = append_max_and_mins(max_mm, min_mm, "MM Mode", all_max_times, all_min_times) 
    all_max_times, all_min_times  = append_max_and_mins(max_override, min_override, "Override", all_max_times, all_min_times)


    'Motor Protection Calculations'  
    if mtr_en != 0: #If Motor Protection Is Enabled

        #Calculates Max and Min Under Voltage Trip Times
        max_vu                       = calc_time_generic(V_unbal_per, vu_action, vu_pu, vu_t, 2, .3, 3)
        min_vu                       = calc_time_generic(V_unbal_per, vu_action, vu_pu, vu_t, -2, -.3, 3)

        #Calculates Max and Min Current Unbalance Trip Times
        max_cu                       = calc_time_generic(I_unbal_per, cu_action, cu_pu, cu_t, 2, .3, 3)
        min_cu                       = calc_time_generic(I_unbal_per, cu_action, cu_pu, cu_t, -2, -.3, 3)

        #Calculates Max and Min Current Phase Loss Trip Times
        max_pl                       = calc_time_generic(I_unbal_per, pl_action, 75, pl_t, 2, .3, 3)
        min_pl                       = calc_time_generic(I_unbal_per, pl_action, 75, pl_t, -2, -.3, 3)

        #Calculates Max and Min Current Over Voltage Trip Times
        max_ov                       = calc_time_generic(max_V, ov_action, ov_pu, ov_t,  1.02, .3, 1)
        min_ov                       = calc_time_generic(max_V, ov_action, ov_pu, ov_t,  .98, -.3, 1)

        #Calculates Max and Min Current Under Voltage Trip Times
        max_uv                       = calc_time_generic(max_V, uv_action, uv_pu, uv_t, 1.02, .3, 5)
        min_uv                       = calc_time_generic(max_V, uv_action, uv_pu, uv_t, .98, -.3, 5)

        #Appends Motor Protection Times To An Index Of All The MaxTimes And All The Min Times [Trip Time, Trip Name]
        all_max_times, all_min_times = append_max_and_mins(max_vu, min_vu, "Voltage Unbalanced", all_max_times, all_min_times)
        all_max_times, all_min_times = append_max_and_mins(max_cu, min_cu, "Current Unbalanced", all_max_times, all_min_times)
        all_max_times, all_min_times = append_max_and_mins(max_pl, min_pl, "Phase Loss", all_max_times, all_min_times) 
        all_max_times, all_min_times = append_max_and_mins(max_ov, min_ov, "Over Voltage", all_max_times, all_min_times)
        all_max_times, all_min_times = append_max_and_mins(max_uv, min_uv, "Under Voltage", all_max_times, all_min_times) 

        
    'Power Protection Calculations'
    if pwr_en != 0:
        
        min_fw_power                 = calc_time_generic(real_power, fw_action, fw_pu, fw_t, .98, -.3, 1)
        max_fw_power                 = calc_time_generic(real_power, fw_action, fw_pu, fw_t, 1.02, +.3, 1)
        all_max_times, all_min_times = append_max_and_mins(max_fw_power, min_fw_power, "Forward Real Power", all_max_times, all_min_times)
        
        min_fvar_power               = calc_time_generic(reactive_power, fvar_action, fvar_pu, fvar_t, .98, -.3, 1)
        max_fvar_power               = calc_time_generic(reactive_power, fvar_action, fvar_pu, fvar_t, 1.02, +.3, 1)
        all_max_times, all_min_times = append_max_and_mins(max_fvar_power, min_fvar_power, "Forward Reactive Power", all_max_times, all_min_times)
                
        min_va_power                 = calc_time_generic(apparent_power, va_action, va_pu, va_t, .98, -.3, 1)
        max_va_power                 = calc_time_generic(apparent_power, va_action, va_pu, va_t, 1.02, +.3, 1)
        all_max_times, all_min_times = append_max_and_mins(max_va_power, min_va_power, "Forward Apparent Power", all_max_times, all_min_times)

        min_rp_power                 = calc_time_generic(rev_real_power, rp_action, rp_pu, rp_t, .98, -.3, 5)
        max_rp_power                 = calc_time_generic(rev_real_power, rp_action, rp_pu, rp_t, 1.02, +.3, 5)
        all_max_times, all_min_times = append_max_and_mins(max_rp_power, min_rp_power, "Reverse Forward Power", all_max_times, all_min_times)

        min_rr_power                 = calc_time_generic(rev_reactive_power, rr_action, rr_pu, rr_t, .98, -.3, 5)
        max_rr_power                 = calc_time_generic(rev_reactive_power, rr_action, rr_pu, rr_t, 1.02, +.3, 5)
        all_max_times, all_min_times = append_max_and_mins(max_rr_power, min_rr_power, "Reverse Reactive Power", all_max_times, all_min_times)

        min_upf_power                 = calc_time_generic(unit_pf, up_action, up_pu, up_t, .98, -.3, 5)
        max_upf_power                 = calc_time_generic(unit_pf, up_action, up_pu, up_t, 1.02, +.3, 5)
        all_max_times, all_min_times = append_max_and_mins(max_upf_power, min_upf_power, "Under Power Factor", all_max_times, all_min_times)

        min_r_demand_power                 = calc_time_generic(real_power, rpd_action, rpd_pu, rpd_t, .95, .95, 0)
        max_r_demand_power                 = calc_time_generic(real_power, rpd_action, rpd_pu, rpd_t, 1.05, 1.05, 0)
        all_max_times, all_min_times = append_max_and_mins(max_r_demand_power, min_r_demand_power, "Real Demand Power", all_max_times, all_min_times)

        min_a_demand_power                 = calc_time_generic(apparent_power, apd_action, apd_pu, apd_t, .95, .95, 0)
        max_a_demand_power                 = calc_time_generic(apparent_power, apd_action, apd_pu, apd_t, 1.05, 1.05, 0) 
        all_max_times, all_min_times = append_max_and_mins(max_a_demand_power, min_a_demand_power, "Apparent Demand Power", all_max_times, all_min_times)

        
    if freq_proc != 0:

        freq_level = freq/expected_freq

        #Needs to be flip flopped due to calc time checks actions
        if ofreq_action == 0:
            ofreq_action = 1
        else:
            ofreq_action = 0

        if ufreq_action == 0:
            ufreq_action = 1
        else:
            ufreq_action = 0
            
        min_ofreq                 = calc_time_generic(freq_level, ofreq_action, ofreq_pu, ofreq_t, .98, -.3, 1)
        max_ofreq                 = calc_time_generic(freq_level, ofreq_action, ofreq_pu, ofreq_t, 1.02, +.3, 1)
        all_max_times, all_min_times = append_max_and_mins(max_ofreq, min_ofreq, "Over Frequency", all_max_times, all_min_times)

        min_ufreq                 = calc_time_generic(freq_level, ufreq_action, ufreq_pu, ufreq_t, 1.02, -.3, 5)
        max_ufreq                 = calc_time_generic(freq_level, ufreq_action, ufreq_pu, ufreq_t, .98, +.3, 5)
        all_max_times, all_min_times = append_max_and_mins(max_ufreq, min_ufreq, "Under Frequency", all_max_times, all_min_times)
        
        
    '''
    ===========================================================================================
    Finds the Max and Minimum Times Used For The Test
    ===========================================================================================
    '''
    
    max_trip_times = []
    min_trip_times = [] 
    array_len = len(all_max_times)

    
    for j in range(0, array_len, 2):
        if all_max_times[j] != -1:
            max_trip_times.append(all_max_times[j])
            print(all_max_times[j+1])
            print(all_max_times[j])

        if all_min_times[j] != -1:
            min_trip_times.append(all_min_times[j])

        j = j + 1


    if len(max_trip_times) != 0:
        max_time = min(max_trip_times)
    else:
        j = j + 1
        no_trip_case = True
        max_time = -1
        

    if len(min_trip_times) != 0:
        min_time = min(min_trip_times)
    else:
        no_trip_case = True
        min_time = -1

        
    
    if no_trip_case == True:
        if gf_mode == 0: 
            max_time = 2
        elif ov_action == 0:
            max_time = ov_t
        elif uv_action == 0:
            max_time = uv_t
        elif vu_action == 0:
            max_time = vu_t
        elif cu_action == 0:
            max_time = cu_t + 1
        elif rp_action == 0 and pwr_en != 0:
            max_time = rp_t
        elif pl_action == 0:
            max_time = pl_t
        elif pwr_en != 0:
            max_time = 600
        elif freq_proc != 0:
            max_time = 300
        else:
            max_time = long_delay

            
    return max_time, min_time, no_trip_case


'''
======================================================================================================================
Methods used to calculate the trip times
=======================================================================================================================

Calculates the Max and Min Expected Long Delay Times
calc_long_delay(I, ldpu, lds_setpoint, t_ld) 
    Inputs
        I (Float) - The current is used to calculate the trip time
        ldpu(Int) - The Pickup Level the current needs to be above in order for a Long Delay Trip to occur
        lds_setpoint(Int) - Choses the Slope used in the Long Delay Slope Calculation 
        t_ld (Float) - The Trip Time used in the Long Delay Calculation 
    Outputs
        long_delay_max (Float) - The max time of the Long Delay Time
        long_delay_min (Float) - The min time of the Long Delay Time
        long_delay (Float)     - The expected time of the Long Delay Time 


There are some rules that change Long Delay times, such as not tripping faster than Short Delay, Faster Trip times for the PD2
calc_long_delay_special_rules(I, long_delay_max, long_delay_min, short_delay, sd_pu, sd_t, frame)
    Inputs
        I (Float) - The current is used to calculate the trip time
        long_delay_max (Float) - The max time of the Long Delay Time
        long_delay_min (Float) - The min time of the Long Delay Time
        short_delay - The calculated Short Delay Time
        sd_pu - The Pickup Level the current needs to be above for Short Delay To Pickup
        sd_t - The time setting of the Short Delay Time
        frame - The breaker being tested (PD2, PD6, Standard, Double Narrow, ect)
    Outputs
        long_delay_max (Float) - The max time of the Long Delay Time
        long_delay_min (Float) - The min time of the Long Delay Time


Calculates the Max and Min Expected Short Delay Times   
calc_short_delay(I, ldpu, sdpu, sds, t_sd)
    Inputs
        I (Float) - The current is used to calculate the trip time
        ldpu(Int) - The Pickup Level the current needs to be above in order for a Long Delay Trip to occur
        short_delay - The calculated Short Delay Time
        sd_pu - The Pickup Level the current needs to be above for Short Delay To Pickup
        sd_t - The time setting of the Short Delay Time
        frame - The breaker being tested (PD2, PD6, Standard, Double Narrow, ect)
    Outputs
        short_delay_max - The max time of the Short Delay Trip time
        short_delay_min - The min time of the Short Delay Trip time
        short_delay - The expected Short Delay Trip Time


Calculates the Max and Min expected Ground Fault Times
calc_gf_delay(I, rating, gf_type, gf_sensor, gfpu, t_gf, gfs, gf_mode, frame, style_2)
    Inputs
        I (Float) - The current is used to calculate the trip time
        rating(Int) - The non-adjustable rating of the breaker
        gt_type(Int) - ground fault measurment system. residual = 0, source = 1
        gf_sensor(Int) - The CT ratio used for source ground. Ratio = (gf_sensor-1)/2
        gfpu(Int) - The Pickup Level the current needs to be above for Ground Fault to trip
        t_gf(Int) - The time setting of the Ground Fault
        gf_s - The slope of the ground fault trip time. flat = 0, i2t = 1
        gf_mode - The action ground fault will take. Trip = 0, Alarm = 1, Diabled = 2
        frame - The breaker being tested (PD2, PD6, Standard, Double Narrow, ect)
        style_2 = the style on the 35 used to check if GF can exceed 1200. 
    Outputs
        ground_fault_max - The max time of the ground fault trip time
        ground_fault_min - The min time of the ground fault trip time 
    

Calculates the Max and Min expected Instantaneous Time   
def calc_inst(I, rating, ipu):
    Inputs
        I (Float) - The current is used to calculate the trip time
        rating(Int) - The non-adjustable rating of the breaker
        ipu(Int) - The pickup level the current needs to be above for the Instantaneous trip
    Outputs
        max_inst - The max time of the instantaneous trip
        min_inst - The max time of the instantaneous trip

Calculates the Max and Min expected Maintenance Mode Time   
calc_mm_mode(I, rating, usb_mm_mode, mm_level)
    Inputs
        I (Float) - The current is used to calculate the trip time
        rating(Int) - The non-adjustable rating of the breaker
        usb_mm_mode(Int) - The level 
        usb_mm_level - the pickup level for maintenance mode 1.5pu = 0, 2pu = 1, 4pu = 2, 6pu = 3, 8pu = 4, 10pu =5
    Outputs
        max_inst - The max time of the instantaneous trip
        min_inst - The max time of the instantaneous trip

calc_override(I, override)
    Inputs
        I (Float) - The current is used to calculate the trip time
        override(Int) - The pickup level the current needs to be above for the overrirde to trip
    Outputs
        max_override - The max time of the override trip
        min_override - The imtime of the override trip


'''


def calc_long_delay(I, ldpu, lds_setpoint, t_ld):
    lds_setpoint = round(lds_setpoint,0)
    
    if lds_setpoint > 3:
        PU = (I/ldpu)
        if PU == 1: #avoids divide by 0 error. 
            PU = 1.01
            
        if lds_setpoint == 4: #Moderate
            lds = 10 #logic to make sure moderate follows +15% tolerance....should improve later
            long_delay = ((.0515/((PU**.02)-1))+.114)*t_ld
        elif lds_setpoint == 5: #Very
            long_delay = ((19.61/((PU**2)-1))+.491)*t_ld
        elif lds_setpoint == 6: #Extreme
            long_delay = ((28.2/((PU**2)-1))+.1217)*t_ld
        elif lds_setpoint == 7:#A
            long_delay = (.14/((PU**.02)-1))*t_ld
        elif lds_setpoint == 8:#B
            long_delay = (13.5/(PU-1))*t_ld
        else: #C
            long_delay = (80/((PU**2)-1))*t_ld


    else:

        if lds_setpoint == 3:
            lds = 4
        elif lds_setpoint == 0:
            lds = .5
        else:
            lds = lds_setpoint

        if I == 0:
            I = 1

        long_delay = ((6/(I/ldpu))**lds)*t_ld

    #LDPU Min Pickup Tolerance is 105%
    if I >= ldpu * 1.05:
        
        if lds_setpoint > 3:
            low_tol = .85
        else:
            low_tol = .7
        long_delay_min = long_delay * low_tol
    else:
        long_delay_min = -1

    #LDPU Max Pickup Tolerance is 110%
    if I >= ldpu *1.15:
        long_delay_max = long_delay
        
        if lds_setpoint > 3:
            if long_delay_max * 0.15 < .09:
                long_delay_max = long_delay_max+.09
            else:
                long_delay_max = long_delay_max*1.15
        else:
           long_delay_max = long_delay_max
    
    else:
        long_delay_max = -1

    
    return long_delay_max, long_delay_min, long_delay



def calc_long_delay_special_rules(I, long_delay_max, long_delay_min, short_delay, sd_pu, sd_t, frame):
    #Long Delay Can't Be Faster Than Short Delay

    if frame > 10 and sd_pu != 0: 
        if long_delay_max < short_delay and long_delay_max != -1: 
            long_delay_max = short_delay
            long_delay_min = short_delay* .7


    if frame < 10 and long_delay_max != -1:
        if long_delay_max < short_delay:
            long_delay_max = short_delay
            long_delay_min = short_delay* .7

        
        elif long_delay_max < sd_t:
            long_delay_max = sd_t
            long_delay_min = sd_t * .7
        
    #For SR2 the long delay times are sped up at higher currents to prevent shunt fusing
    if frame == 21 and I > 1500:
        long_delay_max = long_delay_max/1.4
        long_delay_min = long_delay_min/1.4
    elif frame == 21 and I > 1800:
        long_delay_max = long_delay_max/1.8
        long_delay_min = long_delay_min/1.8            
                
    return long_delay_max, long_delay_min




def calc_short_delay(I, ldpu, sdpu, sds, t_sd):

    short_delay = ((8/(I/ldpu))**sds)*t_sd
    
    #Checks to see if the trip is in Short Dealy Pickup
    if I > ldpu * sdpu * 1.05 and sdpu != 0:
        short_delay_max = short_delay

        #Short Dealy flatens out after 8x
        if short_delay_max < t_sd:
            if sdpu == 0:
                short_delay_max = .05
            else:
                short_delay_max = t_sd

        #Short Delay times might get a +% depending on what we see.
        if t_sd < .1 and sds == 0:
           short_delay_max =  short_delay* 1.2
           
    else:
        short_delay_max = -1
        


    #Short delay has a tolrance of +5%/-5%
    if I >= ldpu*sdpu*.95 and sdpu != 0: 
        if sds == 2 and (I/ldpu) < 8: #Tolerances for short delay i2t times
            if t_sd <= .15:
                short_delay_min = short_delay * .6
            else:
                short_delay_min = short_delay * .7
        else:                           #Tolerances for short delay flat times
            if t_sd < .1:
                short_delay_min = short_delay *.5 
            elif t_sd <= .15:
                short_delay_min = short_delay *.6
            elif t_sd <= .2:
                short_delay_min = short_delay *.7                
            else:
                short_delay_min = short_delay *.8
    else:
        short_delay_min = -1

    return short_delay_max, short_delay_min, short_delay
                    

def calc_gf_delay(I, rating, gf_type, gf_sensor, gfpu, t_gf, gfs, gf_mode, frame, style_2):

    
    if gf_mode == 0: 

        constant = 1
        gf_rating = rating #The GF rating is used as the basis for the PU. It is usually 
        
        if frame == 26: #If PD6
            rating = 1200 #The 
        if frame < 6: #If the unit is an ACB
            constant = .625 #The constant for the ground fault equation is .625
            
            if rating > 1200: 
                if style_2 != 3:
                    rating = 1200
        

        if gf_type == 1: #If the unit is source ground
            rating = (gf_sensor - 1)/2 #Use the grount fault sensor ratio (ex. a 800:1 is 1601 in group 1 setpoints)
            
        if gfpu * rating * 1.05 < I:#Calc GF Time Max
            ground_fault_max  = ((constant/(I/rating))**gfs)*t_gf

            if ground_fault_max < t_gf:
                ground_fault_max = t_gf
        else:
            ground_fault_max = -1



        
            
        if gfpu * rating * .95 < I: #Calc GF Time Min            
            ground_fault_min = ((constant/(I/rating))**gfs)*t_gf

            if ground_fault_min < t_gf:
                ground_fault_min = t_gf
            
            if gfs == 2 and (I/rating) < 1 and frame > 6:
                if t_gf < .1:
                    ground_fault_min = ground_fault_min * .5
                else:
                    ground_fault_min = ground_fault_min * .7
            else:
                if t_gf < .1:
                    ground_fault_min = ground_fault_min *.5
                elif t_gf <= .15:
                    ground_fault_min = ground_fault_min *.6
                elif t_gf <= .2:
                    ground_fault_min = ground_fault_min *.7
                else:
                    ground_fault_min = ground_fault_min *.8
        else:
            ground_fault_min = -1

        if t_gf < .1 and ground_fault_max != -1:
            ground_fault_max = ground_fault_max *1.5
           
    else:
        ground_fault_max = -1
        ground_fault_min = -1

    return ground_fault_max, ground_fault_min


def calc_inst(I, rating, ipu):


    '''
    Inst Pickup Check
    ''' 
    if I >= ipu * rating * 1.095: #If applied current is greater than the inst pikcup * rating * upper tolerance
       max_inst = .06 #Becomes maximum value
    else:
        max_inst = -1 #No trip

    #If applied current is greater than the inst pikcup * rating * upper tolerance
    if I > ipu * rating *.9: 
       min_inst = .005 #Becomes minimum value 
    else:
        min_inst = -1 #No trip

    return max_inst, min_inst

def calc_mm_mode(I, rating, usb_mm_mode, mm_level):


    '''
    Maintenance Mode Pickup Check
    '''  
    if usb_mm_mode != 0: #0 is off, all other values are some version of on.
        if mm_level == 0:
            mm_pu = 1.5 * rating
        elif mm_level == 1:
            mm_pu = 2.5 * rating
        elif mm_level == 2:
            mm_pu = 4 * rating
        elif mm_level == 3:
            mm_pu = 6 * rating
        elif mm_level == 4:
            mm_pu = 8 * rating
        else:
            mm_pu = 10 * rating
            
        if I > mm_pu *1.15:
            max_mm = .025
        else:
            max_mm = -1 
            
        if I > mm_pu *.85:
            min_mm= 0
        else:
            min_mm = -1

    else:
        max_mm = -1
        min_mm = -1 


    return max_mm, min_mm
        

def calc_override(I, override):            
    '''
    Override Pickup Check
    '''

    peak_I = I * math.sqrt(2)
    
    if peak_I > override *1.15:
        max_override = .025
    else:
        max_override = -1
        
    if peak_I > override *.85:
        min_override = 0
    else:
        min_override = -1
        

    return max_override, min_override




def calc_time_generic(input_level, action, pu_level, trip_time, pu_tol, time_tol, calc_type):
    '''
    is_active - check is the type of protection is active 
    metereted level (measured value being protected such as current, voltage, power)
    pu_level (pickup level)
    time_tol(time tolerance) 
    tol_type (tolerance type) is either percentage(0) or straight value(1)
    '''


    if action != 0: #If action does not equal zero then the feature is disabled and has no trip. 
        return -1 # -1 means no trip

    
    if calc_type == 0: #Percentage Pickup Tolerance, Percentage Time Tolerance
        if (pu_level * pu_tol) < input_level:
                result_time = trip_time * time_tol
        else:
            result_time = -1
            
    elif calc_type == 1:#Percentage Pickup Tolerance, Addition Time Tolerance
        if (pu_level * pu_tol) < input_level:
            result_time = trip_time + time_tol
        else:
            result_time = -1

    elif calc_type == 2: #Addition Pickup Tolerance, Percentage Time Tolerance
        if pu_level + pu_tol < input_level:
            result_time = trip_time * time_tol
        else:
            result_time = -1

    elif calc_type == 3:#Addition Pickup Tolerance, Addition Time Tolerance
        lvl = pu_level + pu_tol
        if pu_level + pu_tol < input_level:
            result_time = trip_time + time_tol
        else:
            result_time = -1
            
    elif calc_type == 4: #Under Percentage Tolerance, Percentage time Tolerance
        if pu_level * pu_tol > input_level:
            result_time = trip_time * time_tol
        else: 
            result_time = -1

    elif calc_type == 5: #Under Percentage Tolerance, Addition Time Tolerance 
        if pu_level * pu_tol > input_level:
            result_time = trip_time + time_tol
        else: 
            result_time = -1
        
            
    else:
        result_time = -1


    return result_time
            
def append_max_and_mins(max_time, min_time, tag, max_array, min_array):

    max_array.append(max_time)
    max_array.append(tag)
    min_array.append(min_time)
    min_array.append(tag)

    return max_array, min_array
