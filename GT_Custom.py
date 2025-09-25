from GT import GT_Test, GT_USB, GT_Calibration, GT_Conversions, GT_System_Control, GT_Secondary_Injection
import time, random



def custom_run(UI, repos, omicron, usb):

    omicron.write_omicron_rowgowski(.4, 120, 60, 1)
            
    file_name = "Tokyo Power Up.txt"
    my_file = open(file_name, "x")
    my_file.close()

    counter = 1 
    while True:
  
        time.sleep(5)
        usb.communicate("enter_into_manufactory_mode_request")
        usb.communicate("enter_into_manufactory_mode_check")

        time.sleep(5)
        start = "secondary_injection_rms_test_with_trip_request"
        check = "secondary_injection_rms_test_with_trip_check"
        cancel = "cancel_software_test_request"
        GT_Secondary_Injection.secondary_generic(usb, 1, 90000, start, check, cancel)
        
        time.sleep(1)

        usb.communicate("Test_TA_action")
        usb.communicate("Test_TA_check")
        #usb.communicate("exit_out_of_manufactory_mode_request")
        #usb.communicate("exit_out_of_manufactory_mode_check")

        usb.communicate("reset_all_min_max_data_request")
        usb.communicate("reset_all_min_max_data_check")

        usb.communicate("reset_all_internal_diagnostics_request")
        usb.communicate("reset_all_internal_diagnostics_check")
        usb.communicate("reset_all_internal_diagnostics_request")
        usb.communicate("reset_all_internal_diagnostics_check")

        
        GT_System_Control.all_off(omicron, usb)
        time.sleep(5)
        GT_System_Control.omicron_on(omicron)
        time.sleep(1)
        GT_System_Control.usb_on(usb)
        time.sleep(10)


        
        rsp = usb.communicate("read_real_time_data_buffer_zero_request")
        cor = usb.get_correctness(rsp)
        trnslt_op = "translate_buffer_zero"
        buff_zero = repos.translator.translate(trnslt_op, rsp, repos.pxr)
        repos.update_buffers(buff_zero, 0)

        status = str(counter) + repos.etu_dictionary['cause_of_status'][0] + "\n"

        print(status)

        my_file = open(file_name, "a")
        my_file.write(status)
        my_file.close()

        GT_System_Control.omicron_off(omicron)

        counter = counter + 1

        GT_System_Control.all_off(omicron, usb)
        time.sleep(5)
        GT_System_Control.omicron_on(omicron)
        GT_System_Control.usb_on(usb)
        time.sleep(1)
        
        
        
        
