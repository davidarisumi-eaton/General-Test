from GT import GT_USB
from GT import GT_Repository
from GT import GT_Conversions
import time
import random

def main(): 
    repos = GT_Repository.Repository()   #  create master object
    usb = GT_USB.USB_Communication()
    usb.set_repository(repos)
    usb.initial_port()
    usb.open_port()
    get_unit_info(repos, usb)

    my_array = [0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0]
    counter = 0 


        
    while(True):

        i = 0
        for val in my_array:
            my_array[i] = random.randint(48, 57)
            i = i+1
            
        print(counter)
        usb.communicate("enter_into_manufactory_mode_request")
        usb.communicate_with_check("enter_into_manufactory_mode_check")
        
        rsp = usb.communicate("write_configured_serial_number_request", my_array)
        rsp = usb.communicate("write_configured_serial_number_check")
        time.sleep(1)
        
        rsp = usb.communicate_with_check("read_configured_serial_number_request")  
        rsp = usb.communicate("read_configured_serial_number_check")
        print(rsp)
        
        for i in range(0,63):
            m = 24 + (i*3)
            a = GT_Conversions.uint_eight_to_dec(rsp, m)
            if my_array[i] != a:
                print("fail")
                print(my_array[i])
                print(a)
                return
    

        usb.communicate("exit_out_of_manufactory_mode_request")
        usb.communicate_with_check("exit_out_of_manufactory_mode_check")

        counter = counter+ 1



def get_unit_info(repos, usb):

        remove_var = 0
        connected = True

                

        try:
            tx = '80 00 07 d1 87 d1 fd'
            tx = bytes.fromhex(tx)

            tag = "Read Breaker Frame Request"
            rsp = usb.communicate_manual(tx, tag)
            print(tag)
            print(rsp)
            repos.frame = GT_Conversions.uint_sixteen_to_dec(rsp, 24)
            print("Frame is")
            print(repos.frame)
        except:
            print("ACB?")
            msg = "MCCB Message Failed, Trying ACB"
            repos.append_output_msg(msg)
            
            try:
                tx = '80 04 04 1c 84 20 fd'
                tx = bytes.fromhex(tx)
                tag = "Read Breaker Frame Request"
                rsp = usb.communicate_manual(tx, tag)

                tx = '80 00 04 1c 84 1c fd'
                tx = bytes.fromhex(tx)
                tag = "Read Breaker Frame Response"
                rsp = usb.communicate_manual(tx, tag)
                
                repos.frame = GT_Conversions.uint_sixteen_to_dec(rsp, 24)
                print("ACB FRAME IS")
                print(repos.frame)
                if repos.frame>20:
                    repos.frame = 3
                    remove_var = 35

                repos.frame = 3
                remove_var = 35      
            except:
                msg = "ACB Message Failed."
                repos.append_output_msg(msg)
                #connected = False
                print("35?")
                msg = "PXR35?????"
                repos.frame = 3
                remove_var = 35

        if connected:
            if repos.frame > 20:
                print("Family is MCCB?")
                repos.setup("MCCB")
                usb.set_command_list("MCCB")
            elif remove_var == 35:
                print("Family is 35?")
                repos.setup("35")
                usb.set_command_list("35")
            else:
                print("Family is ACB?")
                repos.setup("ACB")
                usb.set_command_list("ACB")
            

            if repos.family == "ACB":
                rsp = usb.communicate("read_trip_unit_style_request")
                rsp = usb.communicate("read_trip_unit_style_response")
                style_array = repos.translator.translate("translate_style", rsp)

                if style_array[0] == 25:
                    repos.pxr = "PXR25"
                else:
                    repos.pxr = "PXR20"

                rsp = usb.communicate("read_firmware_version_request")
                firmware_array = repos.translator.translate(rsp, repos.firmware_keys, repos.etu_dictionary)
                if repos.etu_dictionary['MCU1 Version'][0] == 2:
                    repos.setting_file.version_two_keys(repos)
                    
                    
            elif repos.family == "MCCB":
                rsp = usb.communicate("read_etu_style_request")
                print(rsp)
                style_array = repos.translator.translate("translate_style", rsp)
                
                style_two_array = style_array[1]
                print(style_two_array)
                

                if style_two_array[5] == 1:
                    repos.pxr = "PXR25"
                else:
                    repos.pxr = "PXR20"
                    repos.set_pxr20()
                    print("PXR20")
            repos.set_mapping_dictionary()
            
        return connected
    

    
    
main()

 

