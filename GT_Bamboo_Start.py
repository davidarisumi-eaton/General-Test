import os

import os.path
from os import path

from datetime import date
import time


import GT_Test, GT_Report, GT_USB, GT_Omicron, GT_Settings, GT_Calibration, GT_Conversions
import GT_Excel_Creator, GT_Excel_Creator2, GT_Buffer_Screen, GT_Secondary_Injection
import GT_MCCB_Translator, GT_ACB_Translator, GT_Main, GT_Repository


def main():

    repos, usb, omicron = init()               #  run init routine

    usb.set_command_list("ACB")
    usb.initial_port()
    usb.open_port()
    usb.set_repository(None)

    get_unit_info(repos, usb)
    
    start(repos, usb)
    
def init():                  #  initialization routine
    repos = GT_Repository.Repository()   #  create master object
    usb = GT_USB.USB_Communication()
    usb.set_repository(repos)
    omicron = GT_Omicron.Omicron()
    
    return repos, usb, omicron

def create_test_group():

    test_group = []
    file_path = "C:\\Users\\HP6125047\\AppData\\Local\\Programs\\Python\\Python39\\Scripts\\General Test3.2\\Tests\\V32 Tests"

    for root, dirs, files, in os.walk(file_path, topdown = True):
        for name in files:
            test_group.append(file_path + '/' + str(os.path.join(name)))

    print(test_group)        
    return test_group

def get_unit_info(repos, usb):

    connected = True
    try:
        tx = '80 00 07 d1 87 d1 fd'
        tx = bytes.fromhex(tx)

        tag = "Read Breaker Frame Request"
        rsp = usb.communicate_manual(tx, tag)
        repos.frame = GT_Conversions.uint_sixteen_to_dec(rsp, 24)
    except:
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
        except:
            msg = "ACB Message Failed."
            repos.append_output_msg(msg)
            connected = False

    if connected:
        if repos.frame > 20:
            repos.setup("MCCB")
            usb.set_command_list("MCCB")
        else:
            repos.setup("ACB")
            usb.set_command_list("ACB")

        if repos.family == "ACB":
            rsp = usb.communicate("read_trip_unit_style_request")
            

            not_finished = True
            while not_finished:

                rsp = usb.communicate("read_trip_unit_style_response")
                cor = usb.get_correctness(rsp)
                
                if cor == "successful":
                    break
                elif cor == "failure":
                    break
                elif cor == "busy":
                    pass
                else:
                    break
            
            style_array = repos.translator.translate("translate_style", rsp)

            if style_array[0] == 25:
                repos.pxr = "PXR25"
            else:
                repos.pxr = "PXR20"
                
        elif repos.family == "MCCB":
            rsp = usb.communicate("read_trip_unit_style_request")
            style_array = repos.translator.translate("translate_style", rsp)
            style_one_array = style_array[0]
            

            if style_one_array[13] == 1:
                repos.pxr = "PXR25"
            else:
                repos.pxr = "PXR20"
        

    return connected

def start(repos, usb):

    ready = True
    use_omicron = False
    repos.cmc_in_use = False
    bs = 'Brainstem'
    
    try:
        rsp = usb.communicate("read_setpoint_one")
        repos.translator.translate_setpoint_one(rsp)
        
    except:
        ready = False
        msg = "USB Connection Problem."
        print(msg)

    
    omicron = GT_Omicron.Omicron()
    
    if ready and use_omicron == True:
        omi_config = 'Output A and B'

        try:
            msg = omicron.connect_omicron()           #  sets up Omicron Engine.app along with Omicron Amplifiers
            
            omicron.route_llo()
            omicron.turn_on_aux()
            
            if omi_config == 'Output A and B':
                omicron.route_a_and_b()
        except:
            ready = False
            
            msg = "Omicron can't Connect"

            msg = sys.exc_info()[0]
            
            #self.write_results(repos)

            
    elif use_omicron == False:
        repos.cmc_in_use = False
        
    if ready and bs == 'Brainstem':
        try:
             usb.connect_brain_stem()
        except:
            ready = False
            msg = "Brainstem can't Connect"
            msg = sys.exc_info()[0]
            

    elif ready and bs == 'No Brainstem':
        if pwr == 'Cold Start Only' or pwr == 'Aux Only':
            ready = Flase
            msg = "Brainstem is needed for Cold Start or Aux Only power tests"

    
    if ready:

        localtime = time.localtime()
        formatted_time = time.strftime("%I-%M-%S", localtime)

        today = date.today()
        formatted_date = today.strftime("%b-%d-%Y")

        new_dir_name = "\\\\pitpasfile02\\swap\\Arisumi\\Bamboo Tests\\" + "Bamboo Test " + formatted_date + " " + formatted_time
        os.mkdir(new_dir_name)
        save_dir = new_dir_name
        test_group = create_test_group()
        GT_Main.run_from_bamboo(repos, save_dir, test_group, omicron, usb)
        
    else:
        test_running = False


main()


            
