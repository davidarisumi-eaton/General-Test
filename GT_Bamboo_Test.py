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
                
    Module:         UI.py
                
    Mechanics:      Starts the program. 
---------------------------------------------------------------------'''

from __future__ import division
import traceback, math, os

import tkinter
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as tkst
from tkinter.filedialog import askopenfilename

import os

import os.path
from os import path


from queue import *

import threading

import GT_Test, GT_Report, GT_USB, GT_Omicron, GT_Settings, GT_Calibration, GT_Conversions
import GT_Excel_Creator, GT_Excel_Creator2, GT_Buffer_Screen, GT_Secondary_Screen, GT_Setting_Screen
import GT_MCCB_Translator, GT_ACB_Translator, GT_Main, GT_Repository

import time #for testing purposes




    








def main_from_bamboo():

    repos, usb, omicron = init()               #  run init routine
    check_one = open_port(repos, usb)
    
    if check_one == 0:
        
        read_sp = "read_setpoint_one"
        trnslt_op = "translate_setpoint_zero"
        keys = repos.sp_one_keys
        read_setpoints(self, repos, usb, read_sp, trnslt_op, keys)

        choice = "Setpoint 1"
        check_two = write_command(self, repos, usb, choice)
        
    else:
        exit(1)

    if check_two == 1:
        exit(1)
    else:
        exit(0)

def init():                  #  initialization routine
    repos = GT_Repository.Repository()   #  create master object
    usb = GT_USB.USB_Communication()
    usb.set_repository(repos)
    omicron = GT_Omicron.Omicron()
    
    return repos, usb, omicron



def open_port(repos, usb):
    
    name = "COM4"
    
    usb.set_portname(name)
    disconnected = usb.open_port()

    if disconnected == False:    
        connected = get_unit_info(repos, usb)

    else:
        message =  "Issue connecting to " + name 
        repos.append_output_msg(message)

    if disconnected == False:
        return 0
    else:
        return 1

def close_port(repos, usb):

    name = "COM4"
    usb.close_port()

    message = "Disconnected from " + name
    repos.append_output_msg(message)

    
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
            rsp = usb.communicate("read_trip_unit_style_check")
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

def exit_auto_test_mode(repos, usb):            

    self.enter_auto_button.grid(row = 0, column = 5, columnspan = 2)
    self.exit_auto_button.grid_remove()
    
    usb.communicate("exit_out_of_auto_test_mode_request")


    not_finished = True
    while not_finished:
        rsp = usb.communicate("exit_out_of_auto_test_mode_check")
        cor = usb.get_correctness(rsp)

        if cor == "successful":
            break
        elif cor == "failure":
            break
        elif cor == "busy":
            pass
        else:
            break
                
        time.sleep(1)
        
def enter_manufactory_mode(repos, usb):            

    usb.communicate("enter_into_manufactory_mode_request")


    not_finished = True
    while not_finished:
        rsp = usb.communicate("enter_into_manufactory_mode_check")
        cor = usb.get_correctness(rsp)

        if cor == "successful":
            break
        elif cor == "failure":
            break
        elif cor == "busy":
            pass
        else:
            break
                
        time.sleep(1)


def exit_manufactory_mode(repos, usb):            

    
    usb.communicate("exit_out_of_manufactory_mode_request")


    not_finished = True
    while not_finished:
        rsp = usb.communicate("exit_out_of_manufactory_mode_check")
        cor = usb.get_correctness(rsp)

        if cor == "successful":
            break
        elif cor == "failure":
            break
        elif cor == "busy":
            pass
        else:
            break
                
        time.sleep(1)

    
def reset_unit(repos, usb):

    rsp = usb.communicate("reset_trip_unit_execute")
    rsp = usb.communicate("reset_trip_unit_check")

    not_finished = True
    while not_finished:
        rsp = usb.communicate("reset_trip_unit_check")
        correctness = usb.get_correctness(rsp)
        repos.append_output_msg(correctness)

        if correctness == "busy":
            pass
        else:
            not_finished = False
            
    self.update_results(repos)
    self.update_debug(repos)   





def read_setpoints(repos, usb, read_sp, trnslt_op, keys):
        
    rsp = usb.communicate(read_sp)
    cor = usb.get_correctness(rsp)
    if cor == "successful":
        
        new_setpoints = repos.translator.translate(trnslt_op, rsp, repos.pxr)
        
        j = 0 
        for key in keys:
            repos.setpoints[key] = new_setpoints[j]
            j = j+1

        if read_sp == "read_setpoint_one":
            GT_Conversions.convert_etu_to_standard(repos)
            keys = repos.sp_one_keys
            
    else:
        msg = "Issue Reading Message From "  + read_sp + "\n" + cor
        repos.append_output_msg(msg)

        
def write_command(repos, usb, choice):

    if choice == "Setpoint 1":
        keys = repos.sp_one_keys
    else:
        keys = repos.get_keys(choice)
    
    for i in range(0, len(keys)):
        data = entry_array[i].get()
        msg = keys[i] + "  " + str(data)
        repos.setpoints[keys[i]] = float(data)

    if choice == "Setpoint 0":
        usb_com = "write_setpoint_zero"
        
    elif choice == "Setpoint 1":
        GT_Conversions.convert_standard_to_etu(repos)
        usb_com = "write_setpoint_one"
        
    elif choice == "Setpoint 2":
        usb_com = "write_setpoint_two"

    elif choice == "Setpoint 3":
        usb_com = "write_setpoint_three"

    elif choice == "Setpoint 4":
        usb_com = "write_setpoint_four"
        
    elif choice == "Setpoint 5":
        usb_com = "write_setpoint_five"


        
    GT_Conversions.convert_standard_to_etu(repos)
    rsp = usb.communicate("verify_password_execute", [0,0,0,0])
    cor = usb.get_correctness(rsp)
    rsp = usb.communicate(usb_com, keys, repos.setpoints)
    cor = usb.get_correctness(rsp)

    if cor == "successful":
        return 0
    else:
        return 1
                         




main_from_bamboo()
