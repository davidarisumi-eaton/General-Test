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

from tkinter import messagebox
from tkinter import filedialog


from queue import *

import threading

from GT import GT_Test, GT_USB, GT_Omicron, GT_Calibration, GT_Conversions,GT_Secondary_Injection
from GT import GT_MCCB_Translator, GT_ACB_Translator, GT_Main, GT_Repository, GT_Custom

import time #for testing purposes
import sys 



'''Graphical User Inteface Code'''
'''
========================================================================================================================================================
========================================================================================================================================================
========================================================================================================================================================
'''

class General_Test_UI(object):

    def __init__(self, repos, omicron, usb, root):


        self.open_ports = usb.get_open_ports()
        

        self.msg_entry_count = 0 #Counter Number of logs entry count has been used
        self.my_tk = root
        
        self.my_tk.title('Test UI')
        self.my_tk.resizable(width = FALSE, height = FALSE)
        self.my_tk.geometry('{}x{}'.format(1400, 800))
        #self.my_tk.grid(row = 0, rowspan = 10, column = 0, columnspan = 10)
        self.connected = False
        self.test_running = False
        self.q = Queue()

        self.main_frame = Frame(self.my_tk, bg='grey93', width = 1400, height = 800).grid(row = 0, rowspan = 20, column = 0, columnspan = 20)
        
        self.tab_screen = ttk.Notebook(self.main_frame,width = 1000, height = 600)
        self.tab_screen.grid(row = 2, rowspan = 17, column = 3, columnspan = 17)
        
        self.tab_zero   = ttk.Frame(self.tab_screen)
        self.tab_one    = ttk.Frame(self.tab_screen)
        self.tab_two    = ttk.Frame(self.tab_screen)
        self.tab_three  = ttk.Frame(self.tab_screen)
        self.tab_four   = ttk.Frame(self.tab_screen)
        self.tab_five   = ttk.Frame(self.tab_screen)
        self.tab_six    = ttk.Frame(self.tab_screen)
        
        self.tab_screen.add(self.tab_zero,  text = "Test")
        self.tab_screen.add(self.tab_one,   text = "Buffer")
        self.tab_screen.add(self.tab_two,   text = "Setpoints")
        self.tab_screen.add(self.tab_three, text = "Secondary Injection")
        self.tab_screen.add(self.tab_four,  text = "Configuration")
        self.tab_screen.add(self.tab_five,  text = "Health Config")
        self.tab_screen.add(self.tab_six,   text = "Single Test")

        
        Label(self.my_tk, text = 'General Test 3.7', font = 'Courier" 15 bold').grid(row = 0, rowspan = 2, column = 5)


        '''
        ================================================================================================================================================================================
        Static Top Frame
        =================================================================================================================================================================================
        '''
        self.top_frame = self.main_frame

        self.serial_frame = Frame(self.my_tk, bg='grey93', relief = "raised", borderwidth = 1, width = 380, height = 35).grid(row = 0, column = 0, columnspan = 3)
        
        Label(self.top_frame, width = 8, text = 'Serial Port').grid(row = 0, column = 0)
        self.refresh_port= Button(self.top_frame, text = 'Serial Port Refresh', command = lambda: self.check_for_new_ports(usb), height = 1, width = 14)
        self.refresh_port.grid(column = 0, row = 0)
        
        self.USB_cbox = StringVar(self.serial_frame)
        self.USB_cbox.set(usb.portname)
        
        self.USB_Menu = ttk.OptionMenu(self.serial_frame, self.USB_cbox, *self.open_ports)
        self.USB_Menu.config(width = 10)
        self.USB_Menu.grid(row = 0, column = 1)

        self.open_ports = usb.get_open_ports()
        usb.initial_port()
        self.open_usb = Button(self.serial_frame, text = "Open", bg = 'red', command = lambda: self.open_port(repos, usb), height = 1, width = 14)
        self.open_usb.grid(column = 2, row = 0)
        self.close_usb = Button(self.serial_frame, text = "Close", bg = 'cyan', command = lambda: self.close_port(repos, usb), height = 1, width = 14)
        self.close_usb.grid(column =2, row = 0)
        self.close_usb.grid_remove()

        self.reset_button = Button(self.top_frame, text = "Reset", width = 14, height = 2, command = lambda: self.reset(usb))
        self.reset_button.grid(column = 2, row = 1)

        self.enter_auto_button = Button(self.top_frame, text = "Enter Test", bg = 'red', width = 14, height = 2, command = lambda: self.enter_auto_test_mode(repos, usb))
        self.enter_auto_button.grid(row = 1, column = 0)

        self.exit_auto_button = Button(self.top_frame, text = "Exit Test", bg = 'cyan', width = 14, height = 2, command = lambda: self.exit_auto_test_mode(repos, usb))
        self.exit_auto_button.grid(row = 1, column = 0)
        self.exit_auto_button.grid_remove()

        self.enter_manu_button = Button(self.top_frame, text = "Enter Manufactory", bg = 'red', width = 14, height = 2, command = lambda: self.enter_manufactory_mode(repos, usb))
        #self.enter_manu_button.config(font=("Arial", 7))
        self.enter_manu_button.grid(row = 1, column = 1)

        self.exit_manu_button = Button(self.top_frame, text = "Exit Manufactory", bg = 'cyan', width = 14, height = 2, command = lambda: self.exit_manufactory_mode(repos, usb))
        #self.exit_manu_button.config(font=("Arial", 7))
        self.exit_manu_button.grid(row = 1, column = 1)
        self.exit_manu_button.grid_remove()
        

        '''
        ================================================================================================================================================================================
        Static Side Frame
        =================================================================================================================================================================================
        '''
        
        self.debug_scroll = tkst.ScrolledText(master = self.main_frame, width = 40, height = 19)
        self.debug_scroll.grid(row = 10, column = 0, columnspan = 3)
        self.debug_scroll.insert(END, "Debug\n")
        self.debug_index = 0

        self.result_scroll = tkst.ScrolledText(master = self.main_frame, width = 40, height = 19)
        self.result_scroll.grid(row = 15, column = 0, columnspan = 3)
        self.result_scroll.insert(END, "Results\n")
        self.my_tk.update()
        self.result_index = 0


        '''
        ================================================================================================================================================================================
        Tab One Frame (Test)
        =================================================================================================================================================================================
        '''
                
        Label(self.tab_zero, text = 'Options').grid(row = 1, column = 0)
        
        Label(self.tab_six, text = 'ia_amp').grid(row = 2, column = 0)
        self.ia_amp_entry = ttk.Entry(self.tab_six, width = 10)
        self.ia_amp_entry.grid(row = 3, column = 0)
        self.CT_cbox = ttk.Combobox(self.tab_zero, width = 10, values = ["25", "1500", "3750"], state = "readonly")
        self.CT_cbox.current(0)
        self.CT_cbox.grid(row = 3, column = 0)
        
        Label(self.tab_zero, text = 'Neutral').grid(row = 4, column = 0)        
        self.neutral_cbox = ttk.Combobox(self.tab_zero, width = 10, values = ["Neutral", "No Neutral"], state = "readonly")
        self.neutral_cbox.current(1)
        self.neutral_cbox.grid(row = 5, column = 0)

        Label(self.tab_zero, text = 'Power:').grid(row = 6, column = 0)
        self.power_cbox = ttk.Combobox(self.tab_zero, width = 10, values = ["All Power", "Cold Start", "USB Only", "Aux Only"], state = "readonly")
        self.power_cbox.grid(row = 7, column = 0)
        self.power_cbox.current(0)

        Label(self.tab_zero, text = 'Phases').grid(row = 8, column = 0)
        self.phase_cbox = ttk.Combobox(self.tab_zero, width = 10, values = ["A", "B", "C", "AB", "BC", "AC", "ABC"], state = "readonly")
        self.phase_cbox.current(0)
        self.phase_cbox.grid(row = 9, column = 0)

        Label(self.tab_zero, text = 'Test Type').grid(row = 10, column = 0)
        self.test_type_cbox = ttk.Combobox(self.tab_zero, width = 10, values = ["Trip", "Firmware Test", "Hardware Test", "Excel"], state = "readonly")
        self.test_type_cbox.current(3)
        self.test_type_cbox.grid(row = 12, column = 0) 
   

        

        '''
        Column 1
        '''
        
        Label(self.tab_zero, text = 'More Options').grid(row = 1, column = 1)
        Label(self.tab_zero, text = 'Family').grid(row = 2, column = 1)
        self.family_cbox = ttk.Combobox(self.tab_zero, width = 10, values = ["ACB", "MCCB"])
        self.family_cbox.current(1) #Sets inital value to value[1], aka MCCB
        self.family_cbox.grid(row = 3, column = 1)
        
        Label(self.tab_zero, text = 'Number of Runs').grid(row = 4, column = 1)
        self.num_runs = ttk.Combobox(self.tab_zero, width = 10, values = [1,2,3,4,5])
        self.num_runs.current(0) #Sets inital value to value[0], aka 1
        self.num_runs.grid(row = 5, column = 1)

        Label(self.tab_zero, text = 'Frequency').grid(row = 6, column = 1)
        self.freq_choice = ttk.Combobox(self.tab_zero, width = 10, values = [50, 60, 400])
        self.freq_choice.current(1) #Sets inital value to values[1], aka 60
        self.freq_choice.grid(row = 7, column = 1)


        '''
        Column 2
        '''
        
        Label(self.tab_zero, text = 'Phase Angles').grid(row = 1, column = 2)

        Label(self.tab_zero, text = 'Ia').grid(row = 2, column = 2)
        self.ia_ang_choice = ttk.Combobox(self.tab_zero, width = 10, values = [0, 120, -120])
        self.ia_ang_choice.current(0) #Sets inital value to values[0], aka 0
        self.ia_ang_choice.grid(row = 3, column = 2)        

        Label(self.tab_zero, text = 'Ib').grid(row = 4, column = 2)
        self.ib_ang_choice = ttk.Combobox(self.tab_zero, width = 10, values = [0, 120, -120])
        self.ib_ang_choice.current(1) #Sets inital value to values[1], aka 120
        self.ib_ang_choice.grid(row = 5, column = 2)


        Label(self.tab_zero, text = 'Ic').grid(row =6, column = 2)
        self.ic_ang_choice = ttk.Combobox(self.tab_zero, width = 10, values = [0, 120, -120])
        self.ic_ang_choice.current(2) #Sets inital value to values[2], aka -120
        self.ic_ang_choice.grid(row = 7, column = 2)


        Label(self.tab_zero, text = 'Rowgowski Va').grid(row = 8, column = 2)
        self.ra_ang_choice = ttk.Combobox(self.tab_zero, width = 10, values = [90, 270])
        self.ra_ang_choice.current(0) #Sets inital value to values[0], aka 0
        self.ra_ang_choice.grid(row = 9, column = 2)        

        Label(self.tab_zero, text = 'Rowgowski Vb').grid(row = 10, column = 2)
        self.rb_ang_choice = ttk.Combobox(self.tab_zero, width = 10, values = [90, 270])
        self.rb_ang_choice.current(0) #Sets inital value to values[1], aka 120
        self.rb_ang_choice.grid(row = 11, column = 2)

        Label(self.tab_zero, text = 'Rowgowski Vc').grid(row =12, column = 2)
        self.rc_ang_choice = ttk.Combobox(self.tab_zero, width = 10, values = [90, 270])
        self.rc_ang_choice.current(0) #Sets inital value to values[2], aka -120
        self.rc_ang_choice.grid(row = 13, column = 2)


        '''
        Column 3
        '''
        
        Label(self.tab_zero, text = 'USB Options').grid(row = 1, column = 3)
        self.bs_cbox = ttk.Combobox(self.tab_zero, width = 10, values = ["Brainstem", "No Brainstem"], state = "readonly")
        self.bs_cbox.current(0)
        self.bs_cbox.grid(row = 3, column = 3)


        '''
        Column 4
        '''
        
        Label(self.tab_zero, text = 'Omicron Options').grid(row = 1, column = 4)
    
        Label(self.tab_zero, text = 'Connect To Omicron?').grid(row = 2, column = 4)
        self.omi_connect_cbox = ttk.Combobox(self.tab_zero, width = 10, values = ["Yes", "No"], state = "readonly")
        self.omi_connect_cbox.current(0)
        self.omi_connect_cbox.grid(row = 3, column = 4)

        Label(self.tab_zero, text = 'Omicron Configuration').grid(row = 4, column = 4)
        self.omi_config_cbox = ttk.Combobox(self.tab_zero, width = 12, values = ['Output A', 'Output A and B'], state = "readonly")
        self.omi_config_cbox.current(0)
        self.omi_config_cbox.grid(row = 5, column = 4)

        Label(self.tab_zero, text = 'LLO Box').grid(row = 6, column = 4)
        self.omi_llo_cbox = ttk.Combobox(self.tab_zero, width = 12, values = ['1-3', '4-6'], state = "readonly")
        self.omi_llo_cbox.current(0)
        self.omi_llo_cbox.grid(row = 7, column = 4)


        self.save_dir_button = Button(self.tab_zero, text = "Set Password to 0000", command = lambda: self.set_pass(usb))
        self.save_dir_button.grid(row = 8, column = 4)


        self.save_pause_button = Button(self.tab_zero, text = "Pause/Redo", command = lambda: self.pause_test(usb))
        self.save_pause_button.grid(row = 10, column = 4)

        self.save_unpause_button = Button(self.tab_zero, text = "Pause/Redo", command = lambda: self.unpause_test(usb))
        self.save_unpause_button.grid(row = 12, column = 4)

        '''
        Column 5 and 6
        '''
        
        Label(self.tab_zero, text = "File and Directory Options").grid(row = 1, column = 5, columnspan = 2)

        self.save_dir_button = Button(self.tab_zero, text = "Pick Save Directory", command = lambda: self.save_dir())
        self.save_dir_button.grid(row = 3, column = 5, columnspan = 2)
        
        self.save_dir_entry = Entry(self.tab_zero, width = 40)
        self.save_dir_entry.grid(row = 4, column = 5, columnspan = 2)
        save_file_path = os.getcwd()
        self.save_dir_entry.insert(0,save_file_path)

        self.sav_start_dir = os.getcwd()


        Label(self.tab_zero, text = "Run Files or Folder").grid(row = 5, column = 5, columnspan = 2)

        self.fof_cbox = ttk.Combobox(self.tab_zero, width = 10, values = ["Folder", "Files"])
        self.fof_cbox.current(0) #Sets inital value to values[0], aka 0
        self.fof_cbox.grid(row = 6, column = 5, columnspan = 2)
        self.fof_cbox.bind("<<ComboboxSelected>>", lambda e : self.change_open_type())



        self.open_start_dir = os.getcwd()


##        self.input_scroll = tkst.ScrolledText(master = self.tab_zero, width = 28, height = 10)
##        self.input_scroll.grid(row = 8, column = 5, rowspan = 6, columnspan = 2)
##        self.input_scroll.grid_remove()
##        self.input_index = 0
        
        self.open_file_button = Button(self.tab_zero, text = "Pick Choose File", command = lambda: self.open_file())
        self.open_file_button.grid(row = 7, column = 5, columnspan = 2)

        self.file_scroll = tkst.ScrolledText(master = self.tab_zero, width = 28, height = 10)
        self.file_scroll.grid(row = 8, column = 5, rowspan = 6, columnspan = 2)
        self.file_scroll.grid_remove()
        self.file_index = 0

        self.open_dir_button = Button(self.tab_zero, text = "Pick Choose Directory", command = lambda: self.open_dir())
        self.open_dir_button.grid(row = 7, column = 5, columnspan = 2)
        
        self.open_dir_entry = Entry(self.tab_zero, width = 40)
        self.open_dir_entry.grid(row = 8, column = 5, columnspan = 2)
        open_file_path = os.getcwd()
        self.open_dir_entry.insert(0,open_file_path)
        

        self.reset_therm = Button(self.tab_zero, text = "Reset Thermal", command = lambda: self.reset_therm(repos))
        self.reset_therm.grid(column = 8, row = 0)   
        #self.custom_button = Button(self.tab_zero, text = "Custom", command = lambda: self.custom_test(repos, usb))
        #self.custom_button.grid(column = 8, row = 6)
        
        self.save_properties = Button(self.tab_zero, text = "Get Prop", command = lambda: self.get_prop())
        self.save_properties.grid(column = 9, row = 0)                
        self.save_properties = Button(self.tab_zero, text = "Save Prop", command = lambda: self.save_prop())
        self.save_properties.grid(column = 9, row = 2)
        #self.cal_prime_button = Button(self.tab_zero, text = "Calibrate Prime",command = lambda: self.calibrate_primary_setup(repos, usb, omicron)) #Future Additon
        #self.cal_prime_button.grid(column = 9, row = 8)
        #self.cal_sec_button = Button(self.tab_zero, text = "Calibrate Second",command = lambda: self.calibrate_secondary(repos, usb)) #Future Additon 
        #self.cal_sec_button.grid(column = 9, row = 10)
        #self.check_button = Button(self.tab_zero, text = "Check Inputs", command = lambda: self.check_setup(repos, usb, omicron))
        #self.check_button.grid(column = 9, row = 12)
        self.test_button = Button(self.tab_zero, text = "Run Test", bg = 'cyan', width = 14, height = 2, command = lambda: self.start_setup(repos, usb))
        self.test_button.grid(column = 8, row = 8)

        self.test_button = Button(self.tab_zero, text = "Run Custom", bg = 'cyan', width = 14, height = 2, command = lambda: self.run_custom(repos, usb))
        self.test_button.grid(column = 8, row = 10)

        self.get_prop()


        '''
        ================================================================================================================================================================================
        Tab One Frame (Buffer)
        =================================================================================================================================================================================
        '''

        buffers = ["Buffer 0", "Buffer 1", "Buffer 2", "Buffer 3", "Buffer 4", "Buffer 5", "Buffer 6", "Buffer 7", "Buffer 8", "Buffer 10", "Buffer 11", "Buffer 12", "Buffer 13", "Buffer 42", "Buffer 43", "Buffer 48", "Buffer 55"]

        self.label_zero_array = []
        self.entry_zero_array = []
        self.label_one_array = []
        self.entry_one_array = []
        self.label_two_array = []
        self.entry_two_array = []


        self.zero_cbox = ttk.Combobox(self.tab_one, width = 10, values = buffers, state = "readonly")
        self.zero_cbox.current(0)
        self.zero_cbox.grid(row = 1, column = 0)
        self.zero_cbox.bind("<<ComboboxSelected>>", lambda e : self.label_section(repos, 0, self.zero_cbox.get()))
            
        self.zero_read_button = Button(self.tab_one, text = "Read", command = lambda: self.read_command(repos, usb, 0))
        self.zero_read_button.grid(row = 1, column = 1, columnspan = 2)

        self.zero_refresh = BooleanVar()
        self.zero_refresh.set(False)
        self.zero_check = Checkbutton(self.tab_one, text = "1s Refresh", variable = self.zero_refresh, command = lambda: self.change_zero_check(repos, usb))
        self.zero_check.grid(row = 2, column = 2)


        
        self.one_cbox = ttk.Combobox(self.tab_one, width = 10, values = buffers, state = "readonly")
        self.one_cbox.current(0)
        self.one_cbox.grid(row = 1, column = 4)
        self.one_cbox.bind("<<ComboboxSelected>>", lambda e : self.label_section(repos, 1, self.one_cbox.get()))
            
        self.one_read_button = Button(self.tab_one, text = "Read", command = lambda: self.read_command(repos, usb, 1))
        self.one_read_button.grid(row = 1, column = 5, columnspan = 2)

        self.one_refresh = BooleanVar()
        self.one_refresh.set(False)
        self.one_check = Checkbutton(self.tab_one, text = "1s Refresh", variable = self.one_refresh, command = lambda: self.change_one_check(repos, usb))
        self.one_check.grid(row = 2, column = 5)


        
        self.two_cbox = ttk.Combobox(self.tab_one, width = 10, values = buffers, state = "readonly")
        self.two_cbox.current(0)
        self.two_cbox.grid(row = 1, column = 8)
        self.two_cbox.bind("<<ComboboxSelected>>", lambda e: self.label_section(repos, 2, self.two_cbox.get()))
            
        self.two_read_button = Button(self.tab_one, text = "Read", command = lambda: self.read_command(repos, usb, 2))
        self.two_read_button.grid(row = 1, column = 9, columnspan = 2)

        self.two_refresh = BooleanVar()
        self.two_refresh.set(False)
        self.two_check = Checkbutton(self.tab_one, text = "1s Refresh", variable = self.two_refresh, command = lambda: self.change_two_check(repos, usb))
        self.two_check.grid(row = 2, column = 9)
        
        '''
        Section Zero
        '''
        self.sec_zero_zero_label      = Label(self.tab_one)
        self.sec_zero_one_label       = Label(self.tab_one)
        self.sec_zero_two_label       = Label(self.tab_one)
        self.sec_zero_three_label     = Label(self.tab_one)
        self.sec_zero_four_label      = Label(self.tab_one)
        self.sec_zero_five_label      = Label(self.tab_one)
        self.sec_zero_six_label       = Label(self.tab_one)
        self.sec_zero_seven_label     = Label(self.tab_one)
        self.sec_zero_eight_label     = Label(self.tab_one)
        self.sec_zero_nine_label      = Label(self.tab_one)
        self.sec_zero_ten_label       = Label(self.tab_one)
        self.sec_zero_eleven_label    = Label(self.tab_one)
        self.sec_zero_twelve_label    = Label(self.tab_one)
        self.sec_zero_thirteen_label  = Label(self.tab_one)
        self.sec_zero_fourteen_label  = Label(self.tab_one)
        self.sec_zero_fifteen_label   = Label(self.tab_one)
        self.sec_zero_sixteen_label   = Label(self.tab_one)
        self.sec_zero_seventeen_label = Label(self.tab_one)
        self.sec_zero_eighteen_label  = Label(self.tab_one)
        self.sec_zero_nineteen_label  = Label(self.tab_one)
        self.sec_zero_twenty_label    = Label(self.tab_one)
        self.sec_zero_twenty_one_label       = Label(self.tab_one)
        self.sec_zero_twenty_two_label       = Label(self.tab_one)
        self.sec_zero_twenty_three_label     = Label(self.tab_one)
        self.sec_zero_twenty_four_label      = Label(self.tab_one)
        self.sec_zero_twenty_five_label      = Label(self.tab_one)
        self.sec_zero_twenty_six_label       = Label(self.tab_one)
        self.sec_zero_twenty_seven_label     = Label(self.tab_one)
        self.sec_zero_twenty_eight_label     = Label(self.tab_one)
        self.sec_zero_twenty_nine_label      = Label(self.tab_one)
        self.sec_zero_thirty_label       = Label(self.tab_one)
        self.sec_zero_thirty_one_label       = Label(self.tab_one)
        self.sec_zero_thirty_two_label       = Label(self.tab_one)
        self.sec_zero_thirty_three_label     = Label(self.tab_one)
        self.sec_zero_thirty_four_label      = Label(self.tab_one)
        self.sec_zero_thirty_five_label      = Label(self.tab_one)
        self.sec_zero_thirty_six_label       = Label(self.tab_one)
        self.sec_zero_thirty_seven_label     = Label(self.tab_one)
        self.sec_zero_thirty_eight_label     = Label(self.tab_one)
        self.sec_zero_thirty_nine_label      = Label(self.tab_one)

        
        self.sec_zero_zero_entry      = Entry(self.tab_one, width = 20)
        self.sec_zero_one_entry       = Entry(self.tab_one, width = 20)
        self.sec_zero_two_entry       = Entry(self.tab_one, width = 20)
        self.sec_zero_three_entry     = Entry(self.tab_one, width = 20)
        self.sec_zero_four_entry      = Entry(self.tab_one, width = 20)
        self.sec_zero_five_entry      = Entry(self.tab_one, width = 20)
        self.sec_zero_six_entry       = Entry(self.tab_one, width = 20)
        self.sec_zero_seven_entry     = Entry(self.tab_one, width = 20)
        self.sec_zero_eight_entry     = Entry(self.tab_one, width = 20)
        self.sec_zero_nine_entry      = Entry(self.tab_one, width = 20)
        self.sec_zero_ten_entry       = Entry(self.tab_one, width = 20)
        self.sec_zero_eleven_entry    = Entry(self.tab_one, width = 20)
        self.sec_zero_twelve_entry    = Entry(self.tab_one, width = 20)
        self.sec_zero_thirteen_entry  = Entry(self.tab_one, width = 20)
        self.sec_zero_fourteen_entry  = Entry(self.tab_one, width = 20)
        self.sec_zero_fifteen_entry   = Entry(self.tab_one, width = 20)
        self.sec_zero_sixteen_entry   = Entry(self.tab_one, width = 20)
        self.sec_zero_seventeen_entry = Entry(self.tab_one, width = 20)
        self.sec_zero_eighteen_entry  = Entry(self.tab_one, width = 20)
        self.sec_zero_nineteen_entry  = Entry(self.tab_one, width = 20)
        self.sec_zero_twenty_entry    = Entry(self.tab_one, width = 20)
        self.sec_zero_twenty_one_entry       = Entry(self.tab_one, width = 20)
        self.sec_zero_twenty_two_entry       = Entry(self.tab_one, width = 20)
        self.sec_zero_twenty_three_entry     = Entry(self.tab_one, width = 20)
        self.sec_zero_twenty_four_entry      = Entry(self.tab_one, width = 20)
        self.sec_zero_twenty_five_entry      = Entry(self.tab_one, width = 20)
        self.sec_zero_twenty_six_entry       = Entry(self.tab_one, width = 20)
        self.sec_zero_twenty_seven_entry     = Entry(self.tab_one, width = 20)
        self.sec_zero_twenty_eight_entry     = Entry(self.tab_one, width = 20)
        self.sec_zero_twenty_nine_entry      = Entry(self.tab_one, width = 20)
        self.sec_zero_thirty_entry      = Entry(self.tab_one, width = 20)
        self.sec_zero_thirty_one_entry       = Entry(self.tab_one, width = 20)
        self.sec_zero_thirty_two_entry       = Entry(self.tab_one, width = 20)
        self.sec_zero_thirty_three_entry     = Entry(self.tab_one, width = 20)
        self.sec_zero_thirty_four_entry      = Entry(self.tab_one, width = 20)
        self.sec_zero_thirty_five_entry      = Entry(self.tab_one, width = 20)
        self.sec_zero_thirty_six_entry       = Entry(self.tab_one, width = 20)
        self.sec_zero_thirty_seven_entry     = Entry(self.tab_one, width = 20)
        self.sec_zero_thirty_eight_entry     = Entry(self.tab_one, width = 20)
        self.sec_zero_thirty_nine_entry      = Entry(self.tab_one, width = 20)
        

        self.label_zero_array.append(self.sec_zero_zero_label)
        self.label_zero_array.append(self.sec_zero_one_label)
        self.label_zero_array.append(self.sec_zero_two_label)
        self.label_zero_array.append(self.sec_zero_three_label)
        self.label_zero_array.append(self.sec_zero_four_label)
        self.label_zero_array.append(self.sec_zero_five_label)
        self.label_zero_array.append(self.sec_zero_six_label)
        self.label_zero_array.append(self.sec_zero_seven_label)
        self.label_zero_array.append(self.sec_zero_eight_label)
        self.label_zero_array.append(self.sec_zero_nine_label)
        self.label_zero_array.append(self.sec_zero_ten_label)
        self.label_zero_array.append(self.sec_zero_eleven_label)
        self.label_zero_array.append(self.sec_zero_twelve_label)
        self.label_zero_array.append(self.sec_zero_thirteen_label)
        self.label_zero_array.append(self.sec_zero_fourteen_label)
        self.label_zero_array.append(self.sec_zero_fifteen_label)
        self.label_zero_array.append(self.sec_zero_sixteen_label)
        self.label_zero_array.append(self.sec_zero_seventeen_label)
        self.label_zero_array.append(self.sec_zero_eighteen_label)
        self.label_zero_array.append(self.sec_zero_nineteen_label)
        self.label_zero_array.append(self.sec_zero_twenty_label)
        self.label_zero_array.append(self.sec_zero_twenty_one_label)
        self.label_zero_array.append(self.sec_zero_twenty_two_label)
        self.label_zero_array.append(self.sec_zero_twenty_three_label)
        self.label_zero_array.append(self.sec_zero_twenty_four_label)
        self.label_zero_array.append(self.sec_zero_twenty_five_label)
        self.label_zero_array.append(self.sec_zero_twenty_six_label)
        self.label_zero_array.append(self.sec_zero_twenty_seven_label)
        self.label_zero_array.append(self.sec_zero_twenty_eight_label)
        self.label_zero_array.append(self.sec_zero_twenty_nine_label)
        self.label_zero_array.append(self.sec_zero_thirty_label)
        self.label_zero_array.append(self.sec_zero_thirty_one_label)
        self.label_zero_array.append(self.sec_zero_thirty_two_label)
        self.label_zero_array.append(self.sec_zero_thirty_three_label)
        self.label_zero_array.append(self.sec_zero_thirty_four_label)
        self.label_zero_array.append(self.sec_zero_thirty_five_label)
        self.label_zero_array.append(self.sec_zero_thirty_six_label)
        self.label_zero_array.append(self.sec_zero_thirty_seven_label)
        self.label_zero_array.append(self.sec_zero_thirty_eight_label)
        self.label_zero_array.append(self.sec_zero_thirty_nine_label)

        

        self.entry_zero_array.append(self.sec_zero_zero_entry)
        self.entry_zero_array.append(self.sec_zero_one_entry)
        self.entry_zero_array.append(self.sec_zero_two_entry)
        self.entry_zero_array.append(self.sec_zero_three_entry)
        self.entry_zero_array.append(self.sec_zero_four_entry)
        self.entry_zero_array.append(self.sec_zero_five_entry)
        self.entry_zero_array.append(self.sec_zero_six_entry)
        self.entry_zero_array.append(self.sec_zero_seven_entry)
        self.entry_zero_array.append(self.sec_zero_eight_entry)
        self.entry_zero_array.append(self.sec_zero_nine_entry)
        self.entry_zero_array.append(self.sec_zero_ten_entry)
        self.entry_zero_array.append(self.sec_zero_eleven_entry)
        self.entry_zero_array.append(self.sec_zero_twelve_entry)
        self.entry_zero_array.append(self.sec_zero_thirteen_entry)
        self.entry_zero_array.append(self.sec_zero_fourteen_entry)
        self.entry_zero_array.append(self.sec_zero_fifteen_entry)
        self.entry_zero_array.append(self.sec_zero_sixteen_entry)
        self.entry_zero_array.append(self.sec_zero_seventeen_entry)
        self.entry_zero_array.append(self.sec_zero_eighteen_entry)
        self.entry_zero_array.append(self.sec_zero_nineteen_entry)
        self.entry_zero_array.append(self.sec_zero_twenty_entry)
        self.entry_zero_array.append(self.sec_zero_twenty_one_entry)
        self.entry_zero_array.append(self.sec_zero_twenty_two_entry)
        self.entry_zero_array.append(self.sec_zero_twenty_three_entry)
        self.entry_zero_array.append(self.sec_zero_twenty_four_entry)
        self.entry_zero_array.append(self.sec_zero_twenty_five_entry)
        self.entry_zero_array.append(self.sec_zero_twenty_six_entry)
        self.entry_zero_array.append(self.sec_zero_twenty_seven_entry)
        self.entry_zero_array.append(self.sec_zero_twenty_eight_entry)
        self.entry_zero_array.append(self.sec_zero_twenty_nine_entry)
        self.entry_zero_array.append(self.sec_zero_thirty_entry)
        self.entry_zero_array.append(self.sec_zero_thirty_one_entry)
        self.entry_zero_array.append(self.sec_zero_thirty_two_entry)
        self.entry_zero_array.append(self.sec_zero_thirty_three_entry)
        self.entry_zero_array.append(self.sec_zero_thirty_four_entry)
        self.entry_zero_array.append(self.sec_zero_thirty_five_entry)
        self.entry_zero_array.append(self.sec_zero_thirty_six_entry)
        self.entry_zero_array.append(self.sec_zero_thirty_seven_entry)
        self.entry_zero_array.append(self.sec_zero_thirty_eight_entry)
        self.entry_zero_array.append(self.sec_zero_thirty_nine_entry)


        
        '''
        Section One
        '''
        
        self.sec_one_zero_label      = Label(self.tab_one)
        self.sec_one_one_label       = Label(self.tab_one)
        self.sec_one_two_label       = Label(self.tab_one)
        self.sec_one_three_label     = Label(self.tab_one)
        self.sec_one_four_label      = Label(self.tab_one)
        self.sec_one_five_label      = Label(self.tab_one)
        self.sec_one_six_label       = Label(self.tab_one)
        self.sec_one_seven_label     = Label(self.tab_one)
        self.sec_one_eight_label     = Label(self.tab_one)
        self.sec_one_nine_label      = Label(self.tab_one)
        self.sec_one_ten_label       = Label(self.tab_one)
        self.sec_one_eleven_label    = Label(self.tab_one)
        self.sec_one_twelve_label    = Label(self.tab_one)
        self.sec_one_thirteen_label  = Label(self.tab_one)
        self.sec_one_fourteen_label  = Label(self.tab_one)
        self.sec_one_fifteen_label   = Label(self.tab_one)
        self.sec_one_sixteen_label   = Label(self.tab_one)
        self.sec_one_seventeen_label = Label(self.tab_one)
        self.sec_one_eighteen_label  = Label(self.tab_one)
        self.sec_one_nineteen_label  = Label(self.tab_one)
        self.sec_one_twenty_label    = Label(self.tab_one)
        self.sec_one_twenty_one_label       = Label(self.tab_one)
        self.sec_one_twenty_two_label       = Label(self.tab_one)
        self.sec_one_twenty_three_label     = Label(self.tab_one)
        self.sec_one_twenty_four_label      = Label(self.tab_one)
        self.sec_one_twenty_five_label      = Label(self.tab_one)
        self.sec_one_twenty_six_label       = Label(self.tab_one)
        self.sec_one_twenty_seven_label     = Label(self.tab_one)
        self.sec_one_twenty_eight_label     = Label(self.tab_one)
        self.sec_one_twenty_nine_label      = Label(self.tab_one)
        self.sec_one_thirty_label       = Label(self.tab_one)
        self.sec_one_thirty_one_label       = Label(self.tab_one)
        self.sec_one_thirty_two_label       = Label(self.tab_one)
        self.sec_one_thirty_three_label     = Label(self.tab_one)
        self.sec_one_thirty_four_label      = Label(self.tab_one)
        self.sec_one_thirty_five_label      = Label(self.tab_one)
        self.sec_one_thirty_six_label       = Label(self.tab_one)
        self.sec_one_thirty_seven_label     = Label(self.tab_one)
        self.sec_one_thirty_eight_label     = Label(self.tab_one)
        self.sec_one_thirty_nine_label      = Label(self.tab_one)

        
        self.sec_one_zero_entry      = Entry(self.tab_one, width = 20)
        self.sec_one_one_entry       = Entry(self.tab_one, width = 20)
        self.sec_one_two_entry       = Entry(self.tab_one, width = 20)
        self.sec_one_three_entry     = Entry(self.tab_one, width = 20)
        self.sec_one_four_entry      = Entry(self.tab_one, width = 20)
        self.sec_one_five_entry      = Entry(self.tab_one, width = 20)
        self.sec_one_six_entry       = Entry(self.tab_one, width = 20)
        self.sec_one_seven_entry     = Entry(self.tab_one, width = 20)
        self.sec_one_eight_entry     = Entry(self.tab_one, width = 20)
        self.sec_one_nine_entry      = Entry(self.tab_one, width = 20)
        self.sec_one_ten_entry       = Entry(self.tab_one, width = 20)
        self.sec_one_eleven_entry    = Entry(self.tab_one, width = 20)
        self.sec_one_twelve_entry    = Entry(self.tab_one, width = 20)
        self.sec_one_thirteen_entry  = Entry(self.tab_one, width = 20)
        self.sec_one_fourteen_entry  = Entry(self.tab_one, width = 20)
        self.sec_one_fifteen_entry   = Entry(self.tab_one, width = 20)
        self.sec_one_sixteen_entry   = Entry(self.tab_one, width = 20)
        self.sec_one_seventeen_entry = Entry(self.tab_one, width = 20)
        self.sec_one_eighteen_entry  = Entry(self.tab_one, width = 20)
        self.sec_one_nineteen_entry  = Entry(self.tab_one, width = 20)
        self.sec_one_twenty_entry    = Entry(self.tab_one, width = 20)
        self.sec_one_twenty_one_entry       = Entry(self.tab_one, width = 20)
        self.sec_one_twenty_two_entry       = Entry(self.tab_one, width = 20)
        self.sec_one_twenty_three_entry     = Entry(self.tab_one, width = 20)
        self.sec_one_twenty_four_entry      = Entry(self.tab_one, width = 20)
        self.sec_one_twenty_five_entry      = Entry(self.tab_one, width = 20)
        self.sec_one_twenty_six_entry       = Entry(self.tab_one, width = 20)
        self.sec_one_twenty_seven_entry     = Entry(self.tab_one, width = 20)
        self.sec_one_twenty_eight_entry     = Entry(self.tab_one, width = 20)
        self.sec_one_twenty_nine_entry      = Entry(self.tab_one, width = 20)
        self.sec_one_thirty_entry      = Entry(self.tab_one, width = 20)
        self.sec_one_thirty_one_entry       = Entry(self.tab_one, width = 20)
        self.sec_one_thirty_two_entry       = Entry(self.tab_one, width = 20)
        self.sec_one_thirty_three_entry     = Entry(self.tab_one, width = 20)
        self.sec_one_thirty_four_entry      = Entry(self.tab_one, width = 20)
        self.sec_one_thirty_five_entry      = Entry(self.tab_one, width = 20)
        self.sec_one_thirty_six_entry       = Entry(self.tab_one, width = 20)
        self.sec_one_thirty_seven_entry     = Entry(self.tab_one, width = 20)
        self.sec_one_thirty_eight_entry     = Entry(self.tab_one, width = 20)
        self.sec_one_thirty_nine_entry      = Entry(self.tab_one, width = 20)
        

        self.label_one_array.append(self.sec_one_zero_label)
        self.label_one_array.append(self.sec_one_one_label)
        self.label_one_array.append(self.sec_one_two_label)
        self.label_one_array.append(self.sec_one_three_label)
        self.label_one_array.append(self.sec_one_four_label)
        self.label_one_array.append(self.sec_one_five_label)
        self.label_one_array.append(self.sec_one_six_label)
        self.label_one_array.append(self.sec_one_seven_label)
        self.label_one_array.append(self.sec_one_eight_label)
        self.label_one_array.append(self.sec_one_nine_label)
        self.label_one_array.append(self.sec_one_ten_label)
        self.label_one_array.append(self.sec_one_eleven_label)
        self.label_one_array.append(self.sec_one_twelve_label)
        self.label_one_array.append(self.sec_one_thirteen_label)
        self.label_one_array.append(self.sec_one_fourteen_label)
        self.label_one_array.append(self.sec_one_fifteen_label)
        self.label_one_array.append(self.sec_one_sixteen_label)
        self.label_one_array.append(self.sec_one_seventeen_label)
        self.label_one_array.append(self.sec_one_eighteen_label)
        self.label_one_array.append(self.sec_one_nineteen_label)
        self.label_one_array.append(self.sec_one_twenty_label)
        self.label_one_array.append(self.sec_one_twenty_one_label)
        self.label_one_array.append(self.sec_one_twenty_two_label)
        self.label_one_array.append(self.sec_one_twenty_three_label)
        self.label_one_array.append(self.sec_one_twenty_four_label)
        self.label_one_array.append(self.sec_one_twenty_five_label)
        self.label_one_array.append(self.sec_one_twenty_six_label)
        self.label_one_array.append(self.sec_one_twenty_seven_label)
        self.label_one_array.append(self.sec_one_twenty_eight_label)
        self.label_one_array.append(self.sec_one_twenty_nine_label)
        self.label_one_array.append(self.sec_one_thirty_label)
        self.label_one_array.append(self.sec_one_thirty_one_label)
        self.label_one_array.append(self.sec_one_thirty_two_label)
        self.label_one_array.append(self.sec_one_thirty_three_label)
        self.label_one_array.append(self.sec_one_thirty_four_label)
        self.label_one_array.append(self.sec_one_thirty_five_label)
        self.label_one_array.append(self.sec_one_thirty_six_label)
        self.label_one_array.append(self.sec_one_thirty_seven_label)
        self.label_one_array.append(self.sec_one_thirty_eight_label)
        self.label_one_array.append(self.sec_one_thirty_nine_label)

        

        self.entry_one_array.append(self.sec_one_zero_entry)
        self.entry_one_array.append(self.sec_one_one_entry)
        self.entry_one_array.append(self.sec_one_two_entry)
        self.entry_one_array.append(self.sec_one_three_entry)
        self.entry_one_array.append(self.sec_one_four_entry)
        self.entry_one_array.append(self.sec_one_five_entry)
        self.entry_one_array.append(self.sec_one_six_entry)
        self.entry_one_array.append(self.sec_one_seven_entry)
        self.entry_one_array.append(self.sec_one_eight_entry)
        self.entry_one_array.append(self.sec_one_nine_entry)
        self.entry_one_array.append(self.sec_one_ten_entry)
        self.entry_one_array.append(self.sec_one_eleven_entry)
        self.entry_one_array.append(self.sec_one_twelve_entry)
        self.entry_one_array.append(self.sec_one_thirteen_entry)
        self.entry_one_array.append(self.sec_one_fourteen_entry)
        self.entry_one_array.append(self.sec_one_fifteen_entry)
        self.entry_one_array.append(self.sec_one_sixteen_entry)
        self.entry_one_array.append(self.sec_one_seventeen_entry)
        self.entry_one_array.append(self.sec_one_eighteen_entry)
        self.entry_one_array.append(self.sec_one_nineteen_entry)
        self.entry_one_array.append(self.sec_one_twenty_entry)
        self.entry_one_array.append(self.sec_one_twenty_one_entry)
        self.entry_one_array.append(self.sec_one_twenty_two_entry)
        self.entry_one_array.append(self.sec_one_twenty_three_entry)
        self.entry_one_array.append(self.sec_one_twenty_four_entry)
        self.entry_one_array.append(self.sec_one_twenty_five_entry)
        self.entry_one_array.append(self.sec_one_twenty_six_entry)
        self.entry_one_array.append(self.sec_one_twenty_seven_entry)
        self.entry_one_array.append(self.sec_one_twenty_eight_entry)
        self.entry_one_array.append(self.sec_one_twenty_nine_entry)
        self.entry_one_array.append(self.sec_one_thirty_entry)
        self.entry_one_array.append(self.sec_one_thirty_one_entry)
        self.entry_one_array.append(self.sec_one_thirty_two_entry)
        self.entry_one_array.append(self.sec_one_thirty_three_entry)
        self.entry_one_array.append(self.sec_one_thirty_four_entry)
        self.entry_one_array.append(self.sec_one_thirty_five_entry)
        self.entry_one_array.append(self.sec_one_thirty_six_entry)
        self.entry_one_array.append(self.sec_one_thirty_seven_entry)
        self.entry_one_array.append(self.sec_one_thirty_eight_entry)
        self.entry_one_array.append(self.sec_one_thirty_nine_entry)


        

        '''
        Section Two
        '''
        
        self.sec_two_zero_label      = Label(self.tab_one)
        self.sec_two_one_label       = Label(self.tab_one)
        self.sec_two_two_label       = Label(self.tab_one)
        self.sec_two_three_label     = Label(self.tab_one)
        self.sec_two_four_label      = Label(self.tab_one)
        self.sec_two_five_label      = Label(self.tab_one)
        self.sec_two_six_label       = Label(self.tab_one)
        self.sec_two_seven_label     = Label(self.tab_one)
        self.sec_two_eight_label     = Label(self.tab_one)
        self.sec_two_nine_label      = Label(self.tab_one)
        self.sec_two_ten_label       = Label(self.tab_one)
        self.sec_two_eleven_label    = Label(self.tab_one)
        self.sec_two_twelve_label    = Label(self.tab_one)
        self.sec_two_thirteen_label  = Label(self.tab_one)
        self.sec_two_fourteen_label  = Label(self.tab_one)
        self.sec_two_fifteen_label   = Label(self.tab_one)
        self.sec_two_sixteen_label   = Label(self.tab_one)
        self.sec_two_seventeen_label = Label(self.tab_one)
        self.sec_two_eighteen_label  = Label(self.tab_one)
        self.sec_two_nineteen_label  = Label(self.tab_one)
        self.sec_two_twenty_label    = Label(self.tab_one)
        
        self.sec_two_zero_entry      = Entry(self.tab_one, width = 20)
        self.sec_two_one_entry       = Entry(self.tab_one, width = 20)
        self.sec_two_two_entry       = Entry(self.tab_one, width = 20)
        self.sec_two_three_entry     = Entry(self.tab_one, width = 20)
        self.sec_two_four_entry      = Entry(self.tab_one, width = 20)
        self.sec_two_five_entry      = Entry(self.tab_one, width = 20)
        self.sec_two_six_entry       = Entry(self.tab_one, width = 20)
        self.sec_two_seven_entry     = Entry(self.tab_one, width = 20)
        self.sec_two_eight_entry     = Entry(self.tab_one, width = 20)
        self.sec_two_nine_entry      = Entry(self.tab_one, width = 20)
        self.sec_two_ten_entry       = Entry(self.tab_one, width = 20)
        self.sec_two_eleven_entry    = Entry(self.tab_one, width = 20)
        self.sec_two_twelve_entry    = Entry(self.tab_one, width = 20)
        self.sec_two_thirteen_entry  = Entry(self.tab_one, width = 20)
        self.sec_two_fourteen_entry  = Entry(self.tab_one, width = 20)
        self.sec_two_fifteen_entry   = Entry(self.tab_one, width = 20)
        self.sec_two_sixteen_entry   = Entry(self.tab_one, width = 20)
        self.sec_two_seventeen_entry = Entry(self.tab_one, width = 20)
        self.sec_two_eighteen_entry  = Entry(self.tab_one, width = 20)
        self.sec_two_nineteen_entry  = Entry(self.tab_one, width = 20)
        self.sec_two_twenty_entry    = Entry(self.tab_one, width = 20)

        self.label_two_array.append(self.sec_two_zero_label)
        self.label_two_array.append(self.sec_two_one_label)
        self.label_two_array.append(self.sec_two_two_label)
        self.label_two_array.append(self.sec_two_three_label)
        self.label_two_array.append(self.sec_two_four_label)
        self.label_two_array.append(self.sec_two_five_label)
        self.label_two_array.append(self.sec_two_six_label)
        self.label_two_array.append(self.sec_two_seven_label)
        self.label_two_array.append(self.sec_two_eight_label)
        self.label_two_array.append(self.sec_two_nine_label)
        self.label_two_array.append(self.sec_two_ten_label)
        self.label_two_array.append(self.sec_two_eleven_label)
        self.label_two_array.append(self.sec_two_twelve_label)
        self.label_two_array.append(self.sec_two_thirteen_label)
        self.label_two_array.append(self.sec_two_fourteen_label)
        self.label_two_array.append(self.sec_two_fifteen_label)
        self.label_two_array.append(self.sec_two_sixteen_label)
        self.label_two_array.append(self.sec_two_seventeen_label)
        self.label_two_array.append(self.sec_two_eighteen_label)
        self.label_two_array.append(self.sec_two_nineteen_label)
        self.label_two_array.append(self.sec_two_twenty_label)

        self.entry_two_array.append(self.sec_two_zero_entry)
        self.entry_two_array.append(self.sec_two_one_entry)
        self.entry_two_array.append(self.sec_two_two_entry)
        self.entry_two_array.append(self.sec_two_three_entry)
        self.entry_two_array.append(self.sec_two_four_entry)
        self.entry_two_array.append(self.sec_two_five_entry)
        self.entry_two_array.append(self.sec_two_six_entry)
        self.entry_two_array.append(self.sec_two_seven_entry)
        self.entry_two_array.append(self.sec_two_eight_entry)
        self.entry_two_array.append(self.sec_two_nine_entry)
        self.entry_two_array.append(self.sec_two_ten_entry)
        self.entry_two_array.append(self.sec_two_eleven_entry)
        self.entry_two_array.append(self.sec_two_twelve_entry)
        self.entry_two_array.append(self.sec_two_thirteen_entry)
        self.entry_two_array.append(self.sec_two_fourteen_entry)
        self.entry_two_array.append(self.sec_two_fifteen_entry)
        self.entry_two_array.append(self.sec_two_sixteen_entry)
        self.entry_two_array.append(self.sec_two_seventeen_entry)
        self.entry_two_array.append(self.sec_two_eighteen_entry)
        self.entry_two_array.append(self.sec_two_nineteen_entry)
        self.entry_two_array.append(self.sec_two_twenty_entry)



        '''
        ================================================================================================================================================================================
        Tab Two Frame (Setpoints)
        =================================================================================================================================================================================
        '''            
        sp_list = ["Setpoint 0", "Setpoint 1", "Setpoint 2", "Setpoint 3", "Setpoint 4", "Setpoint 5", "Setpoint 6", "Setpoint 7"]


        self.s_label_zero_array = []
        
        self.s_zero_cbox = ttk.Combobox(self.tab_two, width = 10, values = sp_list, state = "readonly")
        self.s_zero_cbox.current(0)
        self.s_zero_cbox.grid(row = 1, column = 0)
        self.s_zero_cbox.bind("<<ComboboxSelected>>", lambda e : self.label_section(repos, 0, self.s_zero_cbox.get()))
  
            
        self.s_read_button_zero = Button(self.tab_two, text = "Read", command = lambda: self.read_command(repos, usb, 0))
        self.s_write_button_zero = Button(self.tab_two, text = "Write", command = lambda: self.write_command(repos, usb, 0))
        self.s_read_button_zero.grid(row = 1, column = 2)
        self.s_write_button_zero.grid(row = 1, column = 3)

        self.sp_zero_refresh = BooleanVar()
        self.sp_zero_refresh.set(False)
        self.sp_zero_check = Checkbutton(self.tab_two, text = "2s Refresh", variable = self.sp_zero_refresh, command = lambda: self.change_sp_zero_check(repos, usb))
        self.sp_zero_check.grid(row = 2, column = 3)
        


        self.s_one_cbox = ttk.Combobox(self.tab_two, width = 10, values = sp_list, state = "readonly")
        self.s_one_cbox.current(0)
        self.s_one_cbox.grid(row = 1, column = 5)
        self.s_one_cbox.bind("<<ComboboxSelected>>", lambda e : self.label_section(repos, 1, self.s_one_cbox.get()))
            
        self.s_read_button_one = Button(self.tab_two, text = "Read", command = lambda: self.read_command(repos, usb, 1))
        self.s_write_button_one = Button(self.tab_two, text = "Write", command = lambda: self.write_command(repos, usb, 1))
        self.s_read_button_one.grid(row = 1, column = 6)
        self.s_write_button_one.grid(row = 1, column = 7)  
        


        
        '''
        Section Zero
        '''

        self.set_zero_zero_label          = Label(self.tab_two)
        self.set_zero_one_label           = Label(self.tab_two)
        self.set_zero_two_label           = Label(self.tab_two)
        self.set_zero_three_label         = Label(self.tab_two)
        self.set_zero_four_label          = Label(self.tab_two)
        self.set_zero_five_label          = Label(self.tab_two)
        self.set_zero_six_label           = Label(self.tab_two)
        self.set_zero_seven_label         = Label(self.tab_two)
        self.set_zero_eight_label         = Label(self.tab_two)
        self.set_zero_nine_label          = Label(self.tab_two)
        self.set_zero_ten_label           = Label(self.tab_two)
        self.set_zero_eleven_label        = Label(self.tab_two)
        self.set_zero_twelve_label        = Label(self.tab_two)
        self.set_zero_thirteen_label      = Label(self.tab_two)
        self.set_zero_fourteen_label      = Label(self.tab_two)
        self.set_zero_fifteen_label       = Label(self.tab_two)
        self.set_zero_sixteen_label       = Label(self.tab_two)
        self.set_zero_seventeen_label     = Label(self.tab_two)
        self.set_zero_eighteen_label      = Label(self.tab_two)
        self.set_zero_nineteen_label      = Label(self.tab_two)
        self.set_zero_twenty_label        = Label(self.tab_two)
        self.set_zero_twentyone_label     = Label(self.tab_two)
        self.set_zero_twentytwo_label     = Label(self.tab_two)
        self.set_zero_twentythree_label   = Label(self.tab_two)
        self.set_zero_twentyfour_label    = Label(self.tab_two)
        self.set_zero_twentyfive_label    = Label(self.tab_two)
        self.set_zero_twentysix_label    = Label(self.tab_two)
        self.set_zero_twentyseven_label    = Label(self.tab_two)
        self.set_zero_twentyeight_label    = Label(self.tab_two)
        self.set_zero_twentynine_label        = Label(self.tab_two)
        self.set_zero_thirty_label     = Label(self.tab_two)
        self.set_zero_thirtyone_label     = Label(self.tab_two)
        self.set_zero_thirtytwo_label   = Label(self.tab_two)
        self.set_zero_thirtythree_label    = Label(self.tab_two)
        self.set_zero_thirtyfour_label    = Label(self.tab_two)
        self.set_zero_thirtyfive_label    = Label(self.tab_two)
        self.set_zero_thirtysix_label    = Label(self.tab_two)
        self.set_zero_thirtyseven_label    = Label(self.tab_two)
        self.set_zero_thirtyeight_label    = Label(self.tab_two)
        self.set_zero_thirtynine_label        = Label(self.tab_two)
        self.set_zero_fourty_label     = Label(self.tab_two)
        self.set_zero_fourtyone_label     = Label(self.tab_two)
        self.set_zero_fourtytwo_label   = Label(self.tab_two)
        self.set_zero_fourtythree_label    = Label(self.tab_two)
        self.set_zero_fourtyfour_label    = Label(self.tab_two)
        self.set_zero_fourtyfive_label    = Label(self.tab_two)
        self.set_zero_fourtysix_label    = Label(self.tab_two)
        self.set_zero_fourtyseven_label    = Label(self.tab_two)
        self.set_zero_fourtyeight_label    = Label(self.tab_two)
        self.set_zero_fourtynine_label        = Label(self.tab_two)
        
        self.set_zero_zero_entry      = Entry(self.tab_two, width = 15)
        self.set_zero_one_entry       = Entry(self.tab_two, width = 15)
        self.set_zero_two_entry       = Entry(self.tab_two, width = 15)
        self.set_zero_three_entry     = Entry(self.tab_two, width = 15)
        self.set_zero_four_entry      = Entry(self.tab_two, width = 15)
        self.set_zero_five_entry      = Entry(self.tab_two, width = 15)
        self.set_zero_six_entry       = Entry(self.tab_two, width = 15)
        self.set_zero_seven_entry     = Entry(self.tab_two, width = 15)
        self.set_zero_eight_entry     = Entry(self.tab_two, width = 15)
        self.set_zero_nine_entry      = Entry(self.tab_two, width = 15)
        self.set_zero_ten_entry       = Entry(self.tab_two, width = 15)
        self.set_zero_eleven_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_twelve_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_thirteen_entry  = Entry(self.tab_two, width = 15)
        self.set_zero_fourteen_entry  = Entry(self.tab_two, width = 15)
        self.set_zero_fifteen_entry   = Entry(self.tab_two, width = 15)
        self.set_zero_sixteen_entry   = Entry(self.tab_two, width = 15)
        self.set_zero_seventeen_entry = Entry(self.tab_two, width = 15)
        self.set_zero_eighteen_entry  = Entry(self.tab_two, width = 15)
        self.set_zero_nineteen_entry  = Entry(self.tab_two, width = 15)
        self.set_zero_twenty_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_twentyone_entry = Entry(self.tab_two, width = 15)
        self.set_zero_twentytwo_entry  = Entry(self.tab_two, width = 15)
        self.set_zero_twentythree_entry  = Entry(self.tab_two, width = 15)
        self.set_zero_twentyfour_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_twentyfive_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_twentysix_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_twentyseven_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_twentyeight_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_twentynine_entry  = Entry(self.tab_two, width = 15)
        self.set_zero_thirty_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_thirtyone_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_thirtytwo_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_thirtythree_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_thirtyfour_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_thirtyfive_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_thirtysix_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_thirtyseven_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_thirtyeight_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_thirtynine_entry  = Entry(self.tab_two, width = 15)
        self.set_zero_fourty_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_fourtyone_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_fourtytwo_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_fourtythree_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_fourtyfour_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_fourtyfive_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_fourtysix_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_fourtyseven_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_fourtyeight_entry    = Entry(self.tab_two, width = 15)
        self.set_zero_fourtynine_entry  = Entry(self.tab_two, width = 15)
        
        self.s_label_zero_array = []
        self.s_label_zero_array.append(self.set_zero_zero_label)
        self.s_label_zero_array.append(self.set_zero_one_label)
        self.s_label_zero_array.append(self.set_zero_two_label)
        self.s_label_zero_array.append(self.set_zero_three_label)
        self.s_label_zero_array.append(self.set_zero_four_label)
        self.s_label_zero_array.append(self.set_zero_five_label)
        self.s_label_zero_array.append(self.set_zero_six_label)
        self.s_label_zero_array.append(self.set_zero_seven_label)
        self.s_label_zero_array.append(self.set_zero_eight_label)
        self.s_label_zero_array.append(self.set_zero_nine_label)
        self.s_label_zero_array.append(self.set_zero_ten_label)
        self.s_label_zero_array.append(self.set_zero_eleven_label)
        self.s_label_zero_array.append(self.set_zero_twelve_label)
        self.s_label_zero_array.append(self.set_zero_thirteen_label)
        self.s_label_zero_array.append(self.set_zero_fourteen_label)
        self.s_label_zero_array.append(self.set_zero_fifteen_label)
        self.s_label_zero_array.append(self.set_zero_sixteen_label)
        self.s_label_zero_array.append(self.set_zero_seventeen_label)
        self.s_label_zero_array.append(self.set_zero_eighteen_label)
        self.s_label_zero_array.append(self.set_zero_nineteen_label)
        self.s_label_zero_array.append(self.set_zero_twenty_label)
        self.s_label_zero_array.append(self.set_zero_twentyone_label)
        self.s_label_zero_array.append(self.set_zero_twentytwo_label)
        self.s_label_zero_array.append(self.set_zero_twentythree_label)
        self.s_label_zero_array.append(self.set_zero_twentyfour_label)
        self.s_label_zero_array.append(self.set_zero_twentyfive_label)
        self.s_label_zero_array.append(self.set_zero_twentysix_label)
        self.s_label_zero_array.append(self.set_zero_twentyseven_label)
        self.s_label_zero_array.append(self.set_zero_twentyeight_label)
        self.s_label_zero_array.append(self.set_zero_twentynine_label)
        self.s_label_zero_array.append(self.set_zero_thirty_label)
        self.s_label_zero_array.append(self.set_zero_thirtyone_label)
        self.s_label_zero_array.append(self.set_zero_thirtytwo_label)
        self.s_label_zero_array.append(self.set_zero_thirtythree_label)
        self.s_label_zero_array.append(self.set_zero_thirtyfour_label)
        self.s_label_zero_array.append(self.set_zero_thirtyfive_label)
        self.s_label_zero_array.append(self.set_zero_thirtysix_label)
        self.s_label_zero_array.append(self.set_zero_thirtyseven_label)
        self.s_label_zero_array.append(self.set_zero_thirtyeight_label)
        self.s_label_zero_array.append(self.set_zero_thirtynine_label)
        self.s_label_zero_array.append(self.set_zero_fourty_label)
        self.s_label_zero_array.append(self.set_zero_fourtyone_label)
        self.s_label_zero_array.append(self.set_zero_fourtytwo_label)
        self.s_label_zero_array.append(self.set_zero_fourtythree_label)
        self.s_label_zero_array.append(self.set_zero_fourtyfour_label)
        self.s_label_zero_array.append(self.set_zero_fourtyfive_label)
        self.s_label_zero_array.append(self.set_zero_fourtysix_label)
        self.s_label_zero_array.append(self.set_zero_fourtyseven_label)
        self.s_label_zero_array.append(self.set_zero_fourtyeight_label)
        self.s_label_zero_array.append(self.set_zero_fourtynine_label)
        
        

        self.s_entry_zero_array = []
        self.s_entry_zero_array.append(self.set_zero_zero_entry)
        self.s_entry_zero_array.append(self.set_zero_one_entry)
        self.s_entry_zero_array.append(self.set_zero_two_entry)
        self.s_entry_zero_array.append(self.set_zero_three_entry)
        self.s_entry_zero_array.append(self.set_zero_four_entry)
        self.s_entry_zero_array.append(self.set_zero_five_entry)
        self.s_entry_zero_array.append(self.set_zero_six_entry)
        self.s_entry_zero_array.append(self.set_zero_seven_entry)
        self.s_entry_zero_array.append(self.set_zero_eight_entry)
        self.s_entry_zero_array.append(self.set_zero_nine_entry)
        self.s_entry_zero_array.append(self.set_zero_ten_entry)
        self.s_entry_zero_array.append(self.set_zero_eleven_entry)
        self.s_entry_zero_array.append(self.set_zero_twelve_entry)
        self.s_entry_zero_array.append(self.set_zero_thirteen_entry)
        self.s_entry_zero_array.append(self.set_zero_fourteen_entry)
        self.s_entry_zero_array.append(self.set_zero_fifteen_entry)
        self.s_entry_zero_array.append(self.set_zero_sixteen_entry)
        self.s_entry_zero_array.append(self.set_zero_seventeen_entry)
        self.s_entry_zero_array.append(self.set_zero_eighteen_entry)
        self.s_entry_zero_array.append(self.set_zero_nineteen_entry)
        self.s_entry_zero_array.append(self.set_zero_twenty_entry)
        self.s_entry_zero_array.append(self.set_zero_twentyone_entry)
        self.s_entry_zero_array.append(self.set_zero_twentytwo_entry)
        self.s_entry_zero_array.append(self.set_zero_twentythree_entry)
        self.s_entry_zero_array.append(self.set_zero_twentyfour_entry)
        self.s_entry_zero_array.append(self.set_zero_twentyfive_entry)
        self.s_entry_zero_array.append(self.set_zero_twentysix_entry)
        self.s_entry_zero_array.append(self.set_zero_twentyseven_entry)
        self.s_entry_zero_array.append(self.set_zero_twentyeight_entry)
        self.s_entry_zero_array.append(self.set_zero_twentynine_entry)
        self.s_entry_zero_array.append(self.set_zero_thirty_entry)
        self.s_entry_zero_array.append(self.set_zero_thirtyone_entry)
        self.s_entry_zero_array.append(self.set_zero_thirtytwo_entry)
        self.s_entry_zero_array.append(self.set_zero_thirtythree_entry)
        self.s_entry_zero_array.append(self.set_zero_thirtyfour_entry)
        self.s_entry_zero_array.append(self.set_zero_thirtyfive_entry)
        self.s_entry_zero_array.append(self.set_zero_thirtysix_entry)
        self.s_entry_zero_array.append(self.set_zero_thirtyseven_entry)
        self.s_entry_zero_array.append(self.set_zero_thirtyeight_entry)
        self.s_entry_zero_array.append(self.set_zero_thirtynine_entry)
        self.s_entry_zero_array.append(self.set_zero_fourty_entry)
        self.s_entry_zero_array.append(self.set_zero_fourtyone_entry)
        self.s_entry_zero_array.append(self.set_zero_fourtytwo_entry)
        self.s_entry_zero_array.append(self.set_zero_fourtythree_entry)
        self.s_entry_zero_array.append(self.set_zero_fourtyfour_entry)
        self.s_entry_zero_array.append(self.set_zero_fourtyfive_entry)
        self.s_entry_zero_array.append(self.set_zero_fourtysix_entry)
        self.s_entry_zero_array.append(self.set_zero_fourtyseven_entry)
        self.s_entry_zero_array.append(self.set_zero_fourtyeight_entry)
        self.s_entry_zero_array.append(self.set_zero_fourtynine_entry)
                
        '''
        settion One
        '''

        self.set_one_zero_label          = Label(self.tab_two)
        self.set_one_one_label           = Label(self.tab_two)
        self.set_one_two_label           = Label(self.tab_two)
        self.set_one_three_label         = Label(self.tab_two)
        self.set_one_four_label          = Label(self.tab_two)
        self.set_one_five_label          = Label(self.tab_two)
        self.set_one_six_label           = Label(self.tab_two)
        self.set_one_seven_label         = Label(self.tab_two)
        self.set_one_eight_label         = Label(self.tab_two)
        self.set_one_nine_label          = Label(self.tab_two)
        self.set_one_ten_label           = Label(self.tab_two)
        self.set_one_eleven_label        = Label(self.tab_two)
        self.set_one_twelve_label        = Label(self.tab_two)
        self.set_one_thirteen_label      = Label(self.tab_two)
        self.set_one_fourteen_label      = Label(self.tab_two)
        self.set_one_fifteen_label       = Label(self.tab_two)
        self.set_one_sixteen_label       = Label(self.tab_two)
        self.set_one_seventeen_label     = Label(self.tab_two)
        self.set_one_eighteen_label      = Label(self.tab_two)
        self.set_one_nineteen_label      = Label(self.tab_two)
        self.set_one_twenty_label        = Label(self.tab_two)
        self.set_one_twentyone_label     = Label(self.tab_two)
        self.set_one_twentytwo_label     = Label(self.tab_two)
        self.set_one_twentythree_label   = Label(self.tab_two)
        self.set_one_twentyfour_label    = Label(self.tab_two)
        
        self.set_one_zero_entry      = Entry(self.tab_two, width = 15)
        self.set_one_one_entry       = Entry(self.tab_two, width = 15)
        self.set_one_two_entry       = Entry(self.tab_two, width = 15)
        self.set_one_three_entry     = Entry(self.tab_two, width = 15)
        self.set_one_four_entry      = Entry(self.tab_two, width = 15)
        self.set_one_five_entry      = Entry(self.tab_two, width = 15)
        self.set_one_six_entry       = Entry(self.tab_two, width = 15)
        self.set_one_seven_entry     = Entry(self.tab_two, width = 15)
        self.set_one_eight_entry     = Entry(self.tab_two, width = 15)
        self.set_one_nine_entry      = Entry(self.tab_two, width = 15)
        self.set_one_ten_entry       = Entry(self.tab_two, width = 15)
        self.set_one_eleven_entry    = Entry(self.tab_two, width = 15)
        self.set_one_twelve_entry    = Entry(self.tab_two, width = 15)
        self.set_one_thirteen_entry  = Entry(self.tab_two, width = 15)
        self.set_one_fourteen_entry  = Entry(self.tab_two, width = 15)
        self.set_one_fifteen_entry   = Entry(self.tab_two, width = 15)
        self.set_one_sixteen_entry   = Entry(self.tab_two, width = 15)
        self.set_one_seventeen_entry = Entry(self.tab_two, width = 15)
        self.set_one_eighteen_entry  = Entry(self.tab_two, width = 15)
        self.set_one_nineteen_entry  = Entry(self.tab_two, width = 15)
        self.set_one_twenty_entry    = Entry(self.tab_two, width = 15)
        self.set_one_twentyone_entry = Entry(self.tab_two, width = 15)
        self.set_one_twentytwo_entry  = Entry(self.tab_two, width = 15)
        self.set_one_twentythree_entry  = Entry(self.tab_two, width = 15)
        self.set_one_twentyfour_entry    = Entry(self.tab_two, width = 15)

        self.s_label_one_array = []
        self.s_label_one_array.append(self.set_one_zero_label)
        self.s_label_one_array.append(self.set_one_one_label)
        self.s_label_one_array.append(self.set_one_two_label)
        self.s_label_one_array.append(self.set_one_three_label)
        self.s_label_one_array.append(self.set_one_four_label)
        self.s_label_one_array.append(self.set_one_five_label)
        self.s_label_one_array.append(self.set_one_six_label)
        self.s_label_one_array.append(self.set_one_seven_label)
        self.s_label_one_array.append(self.set_one_eight_label)
        self.s_label_one_array.append(self.set_one_nine_label)
        self.s_label_one_array.append(self.set_one_ten_label)
        self.s_label_one_array.append(self.set_one_eleven_label)
        self.s_label_one_array.append(self.set_one_twelve_label)
        self.s_label_one_array.append(self.set_one_thirteen_label)
        self.s_label_one_array.append(self.set_one_fourteen_label)
        self.s_label_one_array.append(self.set_one_fifteen_label)
        self.s_label_one_array.append(self.set_one_sixteen_label)
        self.s_label_one_array.append(self.set_one_seventeen_label)
        self.s_label_one_array.append(self.set_one_eighteen_label)
        self.s_label_one_array.append(self.set_one_nineteen_label)
        self.s_label_one_array.append(self.set_one_twenty_label)
        self.s_label_one_array.append(self.set_one_twentyone_label)
        self.s_label_one_array.append(self.set_one_twentytwo_label)
        self.s_label_one_array.append(self.set_one_twentythree_label)
        self.s_label_one_array.append(self.set_one_twentyfour_label)
        

        self.s_entry_one_array = []
        self.s_entry_one_array.append(self.set_one_zero_entry)
        self.s_entry_one_array.append(self.set_one_one_entry)
        self.s_entry_one_array.append(self.set_one_two_entry)
        self.s_entry_one_array.append(self.set_one_three_entry)
        self.s_entry_one_array.append(self.set_one_four_entry)
        self.s_entry_one_array.append(self.set_one_five_entry)
        self.s_entry_one_array.append(self.set_one_six_entry)
        self.s_entry_one_array.append(self.set_one_seven_entry)
        self.s_entry_one_array.append(self.set_one_eight_entry)
        self.s_entry_one_array.append(self.set_one_nine_entry)
        self.s_entry_one_array.append(self.set_one_ten_entry)
        self.s_entry_one_array.append(self.set_one_eleven_entry)
        self.s_entry_one_array.append(self.set_one_twelve_entry)
        self.s_entry_one_array.append(self.set_one_thirteen_entry)
        self.s_entry_one_array.append(self.set_one_fourteen_entry)
        self.s_entry_one_array.append(self.set_one_fifteen_entry)
        self.s_entry_one_array.append(self.set_one_sixteen_entry)
        self.s_entry_one_array.append(self.set_one_seventeen_entry)
        self.s_entry_one_array.append(self.set_one_eighteen_entry)
        self.s_entry_one_array.append(self.set_one_nineteen_entry)
        self.s_entry_one_array.append(self.set_one_twenty_entry)
        self.s_entry_one_array.append(self.set_one_twentyone_entry)
        self.s_entry_one_array.append(self.set_one_twentytwo_entry)
        self.s_entry_one_array.append(self.set_one_twentythree_entry)
        self.s_entry_one_array.append(self.set_one_twentyfour_entry)

        '''
        ============================================================================================================================================================================
        Tab Three Secondary Tab
        ============================================================================================================================================================================
        '''

        self.fill_label_zero = Label(self.tab_three, text = "", width = 15)
        self.fill_label_zero.grid(row = 1, column = 1)

        self.sec_header_label = Label(self.tab_three, text = " Secondary Injection", width = 17, font = 'bold')
        self.sec_header_label.grid(row = 1, column = 2, columnspan = 2)
                                      
        self.label_simhard = Label(self.tab_three, text = "Type", width = 5)
        self.label_simhard.grid(row = 2, column = 2)
        self.simhard_cbox = ttk.Combobox(self.tab_three, width = 13, values = ["Hardware", "Simulated"], state = "readonly")
        self.simhard_cbox.current(0)
        self.simhard_cbox.grid(row = 2, column = 3)

        self.label_sec_phase = Label(self.tab_three, text = "Phase", width = 10)
        self.label_sec_phase.grid(row = 3, column = 2)
        self.sec_phase_cbox = ttk.Combobox(self.tab_three, width = 13, values = ["A", "B", "C", "G"], state = "readonly")
        self.sec_phase_cbox.current(0)
        self.sec_phase_cbox.grid(row = 3, column = 3)

        self.label_sec_current = Label(self.tab_three, text = "Current", width = 5)
        self.label_sec_current.grid(row = 4, column = 2)
        self.sec_cur_entry = Entry(self.tab_three, width = 17)
        self.sec_cur_entry.grid(row = 4, column = 3)

        self.label_sim_type = Label(self.tab_three, text = "Trip/No Trip", width = 10)
        self.label_sim_type.grid(row = 5, column = 2)
        self.sec_type_cbox = ttk.Combobox(self.tab_three, width = 13, values = ["RMS With Trip", "RMS No Trip"], state = "readonly")
        self.sec_type_cbox.current(0)
        self.sec_type_cbox.grid(row = 5, column = 3)

        self.fill_label_one = Label(self.tab_three, text = "")
        self.fill_label_one.grid(row = 6, column = 3)
        
        self.sec_strt_button = Button(self.tab_three, text = "Run", width = 10, command = lambda: self.run_secondary(repos, usb))
        self.sec_strt_button.grid(row = 7, column = 2, columnspan = 2)

        self.sec_clr_button = Button(self.tab_three, text = "Clear Cal", width = 10, command = lambda: self.clear_secondary(repos, usb))
        self.sec_clr_button.grid(row = 10, column = 10, columnspan = 2)

        self.sec_base_button = Button(self.tab_three, text = "Base Cal", width = 10, command = lambda: self.base_secondary(repos, usb))
        self.sec_base_button.grid(row = 10, column = 12, columnspan = 2)

        self.sec_base_button = Button(self.tab_three, text = "Delta Cal", width = 10, command = lambda: self.delta_secondary(repos, usb))
        self.sec_base_button.grid(row = 10, column = 14, columnspan = 2)

        self.sec_gain_button = Button(self.tab_three, text = "35 Gain Cal", width = 10, command = lambda: self.secondary_calibrate_test_injection_gain(repos, usb))
        self.sec_gain_button.grid(row = 12, column = 14, columnspan = 2)
        
        self.sec_off_button = Button(self.tab_three, text = "35 Offset Cal", width = 10, command = lambda: self.secondary_calibrate_test_offset_injection(repos, usb))
        self.sec_off_button.grid(row = 12, column = 10, columnspan = 2)


        self.fill_label_two = Label(self.tab_three, text = "")
        self.fill_label_two.grid(row = 8, column = 3)

        self.label_sim_trip = Label(self.tab_three, text = "Trip Type", width = 10)
        self.label_sim_trip.grid(row = 9, column = 2)
        self.label_sim_time = Label(self.tab_three, text = "Trip Time", width = 10)
        self.label_sim_time.grid(row = 9, column = 3)
        self.sim_type_entry = Entry(self.tab_three, width = 15)
        self.sim_type_entry.grid(row = 10, column = 2)       
        self.sim_time_entry = Entry(self.tab_three, width = 15)
        self.sim_time_entry.grid(row = 10, column = 3)

                
        self.running_secondary = "None"
        self.sec_cancel_button = Button(self.tab_three, text = "Cancel", width = 10, command = lambda: self.cancel_test(repos, usb))
        self.sec_cancel_button.grid(row = 12, column = 2, columnspan = 2)
        
        '''
        ============================================================================================================================================================================
        Tab Four Configuration Tab
        ============================================================================================================================================================================
        '''
        
  
        self.label_frame = Label(self.tab_four, text = "Frame", width = 10)
        self.label_frame.grid(row = 1, column = 0)
        self.read_frame_button  = Button(self.tab_four, text = "Read", width = 10,  command = lambda: self.read_frame(repos, usb))
        self.read_frame_button.grid(row = 1, column = 1)
        self.write_frame_button = Button(self.tab_four, text = "Write", width = 10,  command = lambda: self.write_frame(repos, usb))
        self.write_frame_button.grid(row = 1, column = 2)
        self.frame_entry = Entry(self.tab_four, width = 15)
        self.frame_entry.grid(row = 1, column = 3)

        self.label_frame = Label(self.tab_four, text = "Rating", width = 10)
        self.label_frame.grid(row = 2, column = 0)
        self.read_rating_button  = Button(self.tab_four, text = "Read", width = 10, command = lambda: self.read_rating(repos, usb))
        self.read_rating_button.grid(row = 2, column = 1)
        self.write_rating_button = Button(self.tab_four, text = "Write", width = 10, command = lambda: self.write_rating(repos, usb))
        self.write_rating_button.grid(row = 2, column = 2)
        self.rating_entry = Entry(self.tab_four, width = 15)
        self.rating_entry.grid(row = 2, column = 3)



        self.label_frame = Label(self.tab_four, text = "Style", width = 10)
        self.label_frame.grid(row = 3, column = 0)
        self.read_style_button = Button(self.tab_four, text = "Read", width = 10, command = lambda: self.read_style(repos, usb))
        self.read_style_button.grid(row = 3, column = 1)

        self.write_style_button = Button(self.tab_four, text = "Write", width = 10, command = lambda: self.write_style(repos, usb))
        self.write_style_button.grid(row = 3, column = 2)
        

        styles = ["PXR20V000L00C", "PXR20V00L00M", "PXR20V00LG0C", "PXR20V00LG0M", "PXR20V00LGAC", "PXR20V000LGAM",
                  "PXR25V000L00M", "PXR25V00LG0M", "PXR25V000LGAM", "PXR25V000L0AM", "PXR20V000L0AC"]

        
        self.style_cbox = ttk.Combobox(self.tab_four, width = 15, values = styles)
        self.style_cbox.current(0) #Sets inital value to values[0], aka 0
        self.style_cbox.grid(row = 3, column = 3, columnspan = 2)
        self.style_cbox.bind("<<ComboboxSelected>>", lambda e : self.change_open_type())
        

        self.read_config_button = Button(self.tab_four, text = "Read Configuration", command = lambda: self.read_configuration(repos, usb))
        self.read_config_button.grid(row = 1, column = 5)

        self.write_config_button = Button(self.tab_four, text = "Write Configruation", command = lambda: self.write_configuration(repos, usb))
        self.write_config_button.grid(row = 1, column = 6)
   

        self.config_zero_label          = Label(self.tab_four)
        self.config_one_label           = Label(self.tab_four)
        self.config_two_label           = Label(self.tab_four)
        self.config_three_label         = Label(self.tab_four)
        self.config_four_label          = Label(self.tab_four)
        self.config_five_label          = Label(self.tab_four)
        self.config_six_label           = Label(self.tab_four)
        self.config_seven_label         = Label(self.tab_four)
        self.config_eight_label         = Label(self.tab_four)
        self.config_nine_label          = Label(self.tab_four)
        self.config_ten_label           = Label(self.tab_four)
        self.config_eleven_label        = Label(self.tab_four)
        self.config_twelve_label        = Label(self.tab_four)
        self.config_thirteen_label      = Label(self.tab_four)
        self.config_fourteen_label      = Label(self.tab_four)
        self.config_fifteen_label       = Label(self.tab_four)
        self.config_sixteen_label       = Label(self.tab_four)

        
        self.config_zero_entry      = Entry(self.tab_four, width = 15)
        self.config_one_entry       = Entry(self.tab_four, width = 15)
        self.config_two_entry       = Entry(self.tab_four, width = 15)
        self.config_three_entry     = Entry(self.tab_four, width = 15)
        self.config_four_entry      = Entry(self.tab_four, width = 15)
        self.config_five_entry      = Entry(self.tab_four, width = 15)
        self.config_six_entry       = Entry(self.tab_four, width = 15)
        self.config_seven_entry     = Entry(self.tab_four, width = 15)
        self.config_eight_entry     = Entry(self.tab_four, width = 15)
        self.config_nine_entry      = Entry(self.tab_four, width = 15)
        self.config_ten_entry       = Entry(self.tab_four, width = 15)
        self.config_eleven_entry    = Entry(self.tab_four, width = 15)
        self.config_twelve_entry    = Entry(self.tab_four, width = 15)
        self.config_thirteen_entry  = Entry(self.tab_four, width = 15)
        self.config_fourteen_entry  = Entry(self.tab_four, width = 15)
        self.config_fifteen_entry   = Entry(self.tab_four, width = 15)
        self.config_sixteen_entry   = Entry(self.tab_four, width = 15)

        
        self.config_label_array = []
        self.config_label_array.append(self.config_zero_label)
        self.config_label_array.append(self.config_one_label)
        self.config_label_array.append(self.config_two_label)
        self.config_label_array.append(self.config_three_label)
        self.config_label_array.append(self.config_four_label)
        self.config_label_array.append(self.config_five_label)
        self.config_label_array.append(self.config_six_label)
        self.config_label_array.append(self.config_seven_label)
        self.config_label_array.append(self.config_eight_label)
        self.config_label_array.append(self.config_nine_label)
        self.config_label_array.append(self.config_ten_label)
        self.config_label_array.append(self.config_eleven_label)
        self.config_label_array.append(self.config_twelve_label)
        self.config_label_array.append(self.config_thirteen_label)
        self.config_label_array.append(self.config_fourteen_label)
        self.config_label_array.append(self.config_fifteen_label)
        self.config_label_array.append(self.config_sixteen_label)

        

        self.config_entry_array = []
        self.config_entry_array.append(self.config_zero_entry)
        self.config_entry_array.append(self.config_one_entry)
        self.config_entry_array.append(self.config_two_entry)
        self.config_entry_array.append(self.config_three_entry)
        self.config_entry_array.append(self.config_four_entry)
        self.config_entry_array.append(self.config_five_entry)
        self.config_entry_array.append(self.config_six_entry)
        self.config_entry_array.append(self.config_seven_entry)
        self.config_entry_array.append(self.config_eight_entry)
        self.config_entry_array.append(self.config_nine_entry)
        self.config_entry_array.append(self.config_ten_entry)
        self.config_entry_array.append(self.config_eleven_entry)
        self.config_entry_array.append(self.config_twelve_entry)
        self.config_entry_array.append(self.config_thirteen_entry)
        self.config_entry_array.append(self.config_fourteen_entry)
        self.config_entry_array.append(self.config_fifteen_entry)
        self.config_entry_array.append(self.config_sixteen_entry)


        
        

        '''
        ============================================================================================================================================================================
        Tab Five Configuration Tab
        ============================================================================================================================================================================
        '''
        
  
        self.label_i_health = Label(self.tab_five, text = "Internal Health Config", width = 20)
        self.label_i_health.grid(row = 1, column = 0)
        self.read_i_health_button  = Button(self.tab_five, text = "Read", width = 10,  command = lambda: self.read_i_health(repos, usb))
        self.read_i_health_button.grid(row = 1, column = 1)
        self.write_i_health_button = Button(self.tab_five, text = "Write", width = 10,  command = lambda: self.write_i_health(repos, usb))
        self.write_i_health_button.grid(row = 1, column = 2)

        self.label_e_health = Label(self.tab_five, text = "External Health Config", width = 20)
        self.label_e_health.grid(row = 1, column = 7)
        self.read_e_health_button  = Button(self.tab_five, text = "Read", width = 10,  command = lambda: self.read_e_health(repos, usb))
        self.read_e_health_button.grid(row = 1, column = 8)
        self.write_e_health_button = Button(self.tab_five, text = "Write", width = 10,  command = lambda: self.write_e_health(repos, usb))
        self.write_e_health_button.grid(row = 1, column = 9)


       
   

        self.i_health_zero_label          = Label(self.tab_five, text = "Total Short Circuit Counter", width = 20)
        self.i_health_one_label           = Label(self.tab_five, text = "Short Delay Trip Counter", width = 20)
        self.i_health_two_label           = Label(self.tab_five, text = "Instantaneous Trip Counter", width = 20)
        self.i_health_three_label         = Label(self.tab_five, text = "High Current Trip Counter", width = 20)
        self.i_health_four_label          = Label(self.tab_five, text = "Total Overload Trip Counter", width = 20)
        self.i_health_five_label          = Label(self.tab_five, text = "Long Delay Trip Counter", width = 20)
        self.i_health_six_label           = Label(self.tab_five, text = "Ground Fault Trip Counter", width = 20)
        self.i_health_seven_label         = Label(self.tab_five, text = "Total Operation Counter", width = 20)
        self.i_health_eight_label         = Label(self.tab_five, text = "Trip Operation Counter", width = 20)
        self.i_health_nine_label          = Label(self.tab_five, text = "Test Operations Counter", width = 20)
        self.i_health_ten_label           = Label(self.tab_five, text = "Opens Operations Counter", width = 20)
        self.i_health_eleven_label        = Label(self.tab_five, text = "Manual Operations Counter", width = 20)
        self.i_health_twelve_label        = Label(self.tab_five, text = "Time Of Last Opeartions", width = 20)
        self.i_health_thirteen_label      = Label(self.tab_five, text = "Max Temperature", width = 20)
        self.i_health_fourteen_label      = Label(self.tab_five, text = "Time Of Max Temperature" , width = 20)
        self.i_health_fifteen_label       = Label(self.tab_five, text = "Running Minute", width = 20)
        self.i_health_sixteen_label       = Label(self.tab_five, text = "Running Hour", width = 20)
        self.i_health_seventeen_label     = Label(self.tab_five, text = "Running Day", width = 20)
        self.i_health_eighteen_label      = Label(self.tab_five, text = "Life Points", width = 20)
        self.i_health_nineteen_label      = Label(self.tab_five, text = "Life Points", width = 20)
        
        self.i_health_zero_entry      = Entry(self.tab_five, width = 15)
        self.i_health_one_entry       = Entry(self.tab_five, width = 15)
        self.i_health_two_entry       = Entry(self.tab_five, width = 15)
        self.i_health_three_entry     = Entry(self.tab_five, width = 15)
        self.i_health_four_entry      = Entry(self.tab_five, width = 15)
        self.i_health_five_entry      = Entry(self.tab_five, width = 15)
        self.i_health_six_entry       = Entry(self.tab_five, width = 15)
        self.i_health_seven_entry     = Entry(self.tab_five, width = 15)
        self.i_health_eight_entry     = Entry(self.tab_five, width = 15)
        self.i_health_nine_entry      = Entry(self.tab_five, width = 15)
        self.i_health_ten_entry       = Entry(self.tab_five, width = 15)
        self.i_health_eleven_entry    = Entry(self.tab_five, width = 15)
        self.i_health_twelve_entry    = Entry(self.tab_five, width = 15)
        self.i_health_thirteen_entry  = Entry(self.tab_five, width = 15)
        self.i_health_fourteen_entry  = Entry(self.tab_five, width = 15)
        self.i_health_fifteen_entry   = Entry(self.tab_five, width = 15)
        self.i_health_sixteen_entry   = Entry(self.tab_five, width = 15)
        self.i_health_seventeen_entry = Entry(self.tab_five, width = 15)
        self.i_health_eighteen_entry  = Entry(self.tab_five, width = 15)
        self.i_health_nineteen_entry  = Entry(self.tab_five, width = 15)


        self.i_health_label_array = []
        self.i_health_label_array.append(self.i_health_zero_label)
        self.i_health_label_array.append(self.i_health_one_label)
        self.i_health_label_array.append(self.i_health_two_label)
        self.i_health_label_array.append(self.i_health_three_label)
        self.i_health_label_array.append(self.i_health_four_label)
        self.i_health_label_array.append(self.i_health_five_label)
        self.i_health_label_array.append(self.i_health_six_label)
        self.i_health_label_array.append(self.i_health_seven_label)
        self.i_health_label_array.append(self.i_health_eight_label)
        self.i_health_label_array.append(self.i_health_nine_label)
        self.i_health_label_array.append(self.i_health_ten_label)
        self.i_health_label_array.append(self.i_health_eleven_label)
        self.i_health_label_array.append(self.i_health_twelve_label)
        self.i_health_label_array.append(self.i_health_thirteen_label)
        self.i_health_label_array.append(self.i_health_fourteen_label)
        self.i_health_label_array.append(self.i_health_fifteen_label)
        self.i_health_label_array.append(self.i_health_sixteen_label)
        self.i_health_label_array.append(self.i_health_seventeen_label)
        self.i_health_label_array.append(self.i_health_eighteen_label)
        self.i_health_label_array.append(self.i_health_nineteen_label)


        self.i_health_entry_array = []
        self.i_health_entry_array.append(self.i_health_zero_entry)
        self.i_health_entry_array.append(self.i_health_one_entry)
        self.i_health_entry_array.append(self.i_health_two_entry)
        self.i_health_entry_array.append(self.i_health_three_entry)
        self.i_health_entry_array.append(self.i_health_four_entry)
        self.i_health_entry_array.append(self.i_health_five_entry)
        self.i_health_entry_array.append(self.i_health_six_entry)
        self.i_health_entry_array.append(self.i_health_seven_entry)
        self.i_health_entry_array.append(self.i_health_eight_entry)
        self.i_health_entry_array.append(self.i_health_nine_entry)
        self.i_health_entry_array.append(self.i_health_ten_entry)
        self.i_health_entry_array.append(self.i_health_eleven_entry)
        self.i_health_entry_array.append(self.i_health_twelve_entry)
        self.i_health_entry_array.append(self.i_health_thirteen_entry)
        self.i_health_entry_array.append(self.i_health_fourteen_entry)
        self.i_health_entry_array.append(self.i_health_fifteen_entry)
        self.i_health_entry_array.append(self.i_health_sixteen_entry)
        self.i_health_entry_array.append(self.i_health_seventeen_entry)
        self.i_health_entry_array.append(self.i_health_eighteen_entry)
        self.i_health_entry_array.append(self.i_health_nineteen_entry)
        
        r = 2
        x = 0 
        for label in self.i_health_label_array:

            self.i_health_label_array[x].grid(row = r, column = 1)
            
            self.i_health_entry_array[x].delete(0, END)
            self.i_health_entry_array[x].grid(row = r, column = 2, columnspan =1)
            #data = config[x]
            #self.i_health_entry_array[x].insert(0,data)
            x = x+1
            r = r + 1

        self.e_health_zero_label          = Label(self.tab_five, text = "Total Short Circuit Counter", width = 20)
        self.e_health_one_label           = Label(self.tab_five, text = "Short Delay Trip Counter", width = 20)
        self.e_health_two_label           = Label(self.tab_five, text = "Instantaneous Trip Counter", width = 20)
        self.e_health_three_label         = Label(self.tab_five, text = "High Current Trip Counter", width = 20)
        self.e_health_four_label          = Label(self.tab_five, text = "Total Overload Trip Counter", width = 20)
        self.e_health_five_label          = Label(self.tab_five, text = "Long Delay Trip Counter", width = 20)
        self.e_health_six_label           = Label(self.tab_five, text = "Ground Fault Trip Counter", width = 20)
        self.e_health_seven_label         = Label(self.tab_five, text = "Total Operation Counter", width = 20)
        self.e_health_eight_label         = Label(self.tab_five, text = "Trip Operation Counter", width = 20)
        self.e_health_nine_label          = Label(self.tab_five, text = "Test Operations Counter", width = 20)
        self.e_health_ten_label           = Label(self.tab_five, text = "Opens Operations Counter", width = 20)
        self.e_health_eleven_label        = Label(self.tab_five, text = "Manual Operations Counter", width = 20)
        self.e_health_twelve_label        = Label(self.tab_five, text = "Time Of Last Opeartions", width = 20)
        self.e_health_thirteen_label      = Label(self.tab_five, text = "Max Temperature", width = 20)
        self.e_health_fourteen_label      = Label(self.tab_five, text = "Time Of Max Temperature" , width = 20)
        self.e_health_fifteen_label       = Label(self.tab_five, text = "Running Minute", width = 20)
        self.e_health_sixteen_label       = Label(self.tab_five, text = "Running Hour", width = 20)
        self.e_health_seventeen_label     = Label(self.tab_five, text = "Running Day", width = 20)
        self.e_health_eighteen_label      = Label(self.tab_five, text = "Life Points", width = 20)
        
        self.e_health_zero_entry      = Entry(self.tab_five, width = 15)
        self.e_health_one_entry       = Entry(self.tab_five, width = 15)
        self.e_health_two_entry       = Entry(self.tab_five, width = 15)
        self.e_health_three_entry     = Entry(self.tab_five, width = 15)
        self.e_health_four_entry      = Entry(self.tab_five, width = 15)
        self.e_health_five_entry      = Entry(self.tab_five, width = 15)
        self.e_health_six_entry       = Entry(self.tab_five, width = 15)
        self.e_health_seven_entry     = Entry(self.tab_five, width = 15)
        self.e_health_eight_entry     = Entry(self.tab_five, width = 15)
        self.e_health_nine_entry      = Entry(self.tab_five, width = 15)
        self.e_health_ten_entry       = Entry(self.tab_five, width = 15)
        self.e_health_eleven_entry    = Entry(self.tab_five, width = 15)
        self.e_health_twelve_entry    = Entry(self.tab_five, width = 15)
        self.e_health_thirteen_entry  = Entry(self.tab_five, width = 15)
        self.e_health_fourteen_entry  = Entry(self.tab_five, width = 15)
        self.e_health_fifteen_entry   = Entry(self.tab_five, width = 15)
        self.e_health_sixteen_entry   = Entry(self.tab_five, width = 15)
        self.e_health_seventeen_entry = Entry(self.tab_five, width = 15)
        self.e_health_eighteen_entry  = Entry(self.tab_five, width = 15)

        self.e_health_label_array = []
        self.e_health_label_array.append(self.e_health_zero_label)
        self.e_health_label_array.append(self.e_health_one_label)
        self.e_health_label_array.append(self.e_health_two_label)
        self.e_health_label_array.append(self.e_health_three_label)
        self.e_health_label_array.append(self.e_health_four_label)
        self.e_health_label_array.append(self.e_health_five_label)
        self.e_health_label_array.append(self.e_health_six_label)
        self.e_health_label_array.append(self.e_health_seven_label)
        self.e_health_label_array.append(self.e_health_eight_label)
        self.e_health_label_array.append(self.e_health_nine_label)
        self.e_health_label_array.append(self.e_health_ten_label)
        self.e_health_label_array.append(self.e_health_eleven_label)
        self.e_health_label_array.append(self.e_health_twelve_label)
        self.e_health_label_array.append(self.e_health_thirteen_label)
        self.e_health_label_array.append(self.e_health_fourteen_label)
        self.e_health_label_array.append(self.e_health_fifteen_label)
        self.e_health_label_array.append(self.e_health_sixteen_label)
        self.e_health_label_array.append(self.e_health_seventeen_label)
        self.e_health_label_array.append(self.e_health_eighteen_label)


        self.e_health_entry_array = []
        self.e_health_entry_array.append(self.e_health_zero_entry)
        self.e_health_entry_array.append(self.e_health_one_entry)
        self.e_health_entry_array.append(self.e_health_two_entry)
        self.e_health_entry_array.append(self.e_health_three_entry)
        self.e_health_entry_array.append(self.e_health_four_entry)
        self.e_health_entry_array.append(self.e_health_five_entry)
        self.e_health_entry_array.append(self.e_health_six_entry)
        self.e_health_entry_array.append(self.e_health_seven_entry)
        self.e_health_entry_array.append(self.e_health_eight_entry)
        self.e_health_entry_array.append(self.e_health_nine_entry)
        self.e_health_entry_array.append(self.e_health_ten_entry)
        self.e_health_entry_array.append(self.e_health_eleven_entry)
        self.e_health_entry_array.append(self.e_health_twelve_entry)
        self.e_health_entry_array.append(self.e_health_thirteen_entry)
        self.e_health_entry_array.append(self.e_health_fourteen_entry)
        self.e_health_entry_array.append(self.e_health_fifteen_entry)
        self.e_health_entry_array.append(self.e_health_sixteen_entry)
        self.e_health_entry_array.append(self.e_health_seventeen_entry)
        self.e_health_entry_array.append(self.e_health_eighteen_entry)
        
        r = 2
        x = 0 
        for label in self.e_health_label_array:

            self.e_health_label_array[x].grid(row = r, column = 8)
            
            self.e_health_entry_array[x].delete(0, END)
            self.e_health_entry_array[x].grid(row = r, column = 9, columnspan =1)
            #data = config[x]
            #self.e_health_entry_array[x].insert(0,data)
            x = x+1
            r = r + 1
        

 
        self.exit_manu_button["state"] = "disabled"
        self.enter_manu_button["state"] = "disabled"
        self.reset_button["state"] = "disabled"
        self.exit_auto_button["state"] = "disabled"
        self.enter_auto_button["state"] = "disabled"
        self.reset_therm["state"] = "disabled"

        '''
        ================================================================================================================================================================================
        Tab Six (Single Trip)
        =================================================================================================================================================================================
        '''

        '''
        Column 2
        '''
        
##        Label(self.tab_six, text = 'Phase Angles').grid(row = 1, column = 2)
##
##        Label(self.tab_six, text = 'Ia').grid(row = 2, column = 2)
##        self.ia_ang_choice = ttk.Combobox(self.tab_six, width = 10, values = [0, 120, -120])
##        self.ia_ang_choice.current(0) #Sets inital value to values[0], aka 0
##        self.ia_ang_choice.grid(row = 3, column = 2)        
##
##        Label(self.tab_six, text = 'Ib').grid(row = 4, column = 2)
##        self.ib_ang_choice = ttk.Combobox(self.tab_six, width = 10, values = [0, 120, -120])
##        self.ib_ang_choice.current(1) #Sets inital value to values[1], aka 120
##        self.ib_ang_choice.grid(row = 5, column = 2)
##
##
##        Label(self.tab_six, text = 'Ic').grid(row =6, column = 2)
##        self.ic_ang_choice = ttk.Combobox(self.tab_six, width = 10, values = [0, 120, -120])
##        self.ic_ang_choice.current(2) #Sets inital value to values[2], aka -120
##        self.ic_ang_choice.grid(row = 7, column = 2)
##
##
##        Label(self.tab_six, text = 'Rowgowski Va').grid(row = 8, column = 2)
##        self.ra_ang_choice = ttk.Combobox(self.tab_six, width = 10, values = [90, 270])
##        self.ra_ang_choice.current(0) #Sets inital value to values[0], aka 0
##        self.ra_ang_choice.grid(row = 9, column = 2)        
##
##        Label(self.tab_six, text = 'Rowgowski Vb').grid(row = 10, column = 2)
##        self.rb_ang_choice = ttk.Combobox(self.tab_six, width = 10, values = [90, 270])
##        self.rb_ang_choice.current(0) #Sets inital value to values[1], aka 120
##        self.rb_ang_choice.grid(row = 11, column = 2)
##
##        Label(self.tab_six, text = 'Rowgowski Vc').grid(row =12, column = 2)
##        self.rc_ang_choice = ttk.Combobox(self.tab_six, width = 10, values = [90, 270])
##        self.rc_ang_choice.current(0) #Sets inital value to values[2], aka -120
##        self.rc_ang_choice.grid(row = 13, column = 2)
##
        
    '''
    ============================================================================================================================================================================
    Static Tab Functions
    ============================================================================================================================================================================
    '''

    def reset(self, usb):

        usb.communicate("reset_trip_unit_request")
        rsp = usb.communicate("reset_trip_unit_check")

        rsp = usb.communicate("reset_trip_unit_request")
        rsp = usb.communicate("reset_trip_unit_check")
                
        self.update_results(repos)
        self.update_debug(repos)  

        
    '''
    ============================================================================================================================================================================
    Test Tab Functions
    ============================================================================================================================================================================
    '''

    def check_for_new_ports(self, usb):
        print(self.open_ports)
        self.USB_Menu['menu'].delete(0,'end')
        self.open_ports = usb.get_open_ports()
        print(self.open_ports)
        self.USB_cbox.set(usb.portname)
        self.USB_Menu.set_menu(*self.open_ports)

                                              
    def start_setup(self, repos, usb):

        if self.test_running == False:
            self.test_running = True
            self.testing_thread = threading.Thread(target = self.start, daemon = True, kwargs={'repos':repos, 'usb':usb})
            self.q.put(self.testing_thread)
            self.testing_thread.start()
            
    def start(self, repos, usb):

        ready = True
        bs = self.get_bs()
        
        try:
            rsp = usb.communicate("read_setpoint_one_request")
            repos.translator.translate_setpoint_one(rsp)
            
        except:
            ready = False
            msg = "USB Connection Problem."
            self.write_results(repos)

        
        omicron = GT_Omicron.Omicron()
        use_omicron = self.get_omi_connect()


        
        if ready and use_omicron == True:
            omi_config = self.get_omi_config()
            my_config = self.omi_config_cbox.get()
            llo = self.omi_llo_cbox.get()
            repos.cmc_in_use = True

            try:
                msg = omicron.connect_omicron()           #  sets up Omicron Engine.app along with Omicron Amplifiers
                repos.append_output_msg(msg)
                self.write_results(repos)
                omicron.aux_on()
                
                if omi_config == 'Output A and B':
                    print("ROUTING A AND B")
                    omicron.route_a_and_b()

                print("THE LLO IS")
                print(llo)
                if llo == '1-3':
                    omicron.route_llo(3)
                elif llo == '4-6':
                    omicron.route_llo(4)
                    
            except:
                ready = False
                
                msg = "Omicron can't Connect"
                repos.append_output_msg(msg)
    
                msg = sys.exc_info()[0]
                repos.append_output_msg(msg)
                
                self.write_results(repos)

                
        elif use_omicron == False:
            repos.cmc_in_use = False


        if ready and bs == 'Brainstem':
            msg = "Connecting Brainstem"
            repos.append_output_msg(msg)
            try:
                usb.connect_brain_stem()
                msg = "Brainstem Connected"
                repos.append_output_msg(msg)
                 
            except:
                ready = False
                msg = "Brainstem can't Connect"
                repos.append_output_msg(msg)
                
                msg = sys.exc_info()[0]
                repos.append_output_msg(msg)
                
                self.write_results(repos)
        elif ready and bs == 'No Brainstem':
            pwr = self.get_power
            if pwr == 'Cold Start Only' or pwr == 'Aux Only':
                ready = Flase
                msg = "Brainstem is needed for Cold Start or Aux Only power tests"
                self.write_results(msg)

        
        if ready:

            save_dir = self.save_dir_entry.get()
            test_group = self.create_test_group()
            GT_Main.run_from_ui(self, repos, save_dir, test_group, omicron, usb)
            self.update_msgs(repos)
            
        else:
            self.test_running = False
            

    def check_setup(self, repos, usb, omicron):
        
        self.check_thread = threading.Thread(target = self.check_inputs, daemon = True, kwargs={'repos':repos, 'usb':usb, 'omicron':omicron})
        self.q.put(self.check_thread)
        self.check_thread.start()
            
    def check_inputs(self, repos, usb, omicron):

        ready = True
        
        if ready:

            save_dir = self.save_dir_entry.get()
            test_group = self.create_test_group()
            GT_Main.run_check_inputs(self, repos, test_group, usb, omicron)



    def check_queue(self):

        try:
            task = self.q.get(0)
        except Empty:
            self.my_tk.after(100, self.check_queue(repos))
     
    def run_custom(self, repos, usb):

        ready = True
        omicron = GT_Omicron.Omicron()
        use_omicron = self.get_omi_connect()
        
        if ready and use_omicron == True:
            omi_config = self.get_omi_config()
            my_config = self.omi_config_cbox.get()
            llo = self.omi_llo_cbox.get()
            repos.cmc_in_use = True

            try:
                msg = omicron.connect_omicron()           #  sets up Omicron Engine.app along with Omicron Amplifiers
                print(msg)
                omicron.aux_on()
                
                if omi_config == 'Output A and B':
                    print("ROUTING A AND B")
                    omicron.route_a_and_b()

                print("THE LLO IS")
                print(llo)
                if llo == '1-3':
                    omicron.route_llo(3)
                elif llo == '4-6':
                    omicron.route_llo(4)
                    
            except:
                ready = False
                
                msg = "Omicron can't Connect"
                print(msg)
    
                msg = sys.exc_info()[0]
                print(msg)
                
                self.write_results(repos)

        bs = self.get_bs()     
        if ready and bs == 'Brainstem':
            msg = "Connecting Brainstem"
            print(msg)
            try:
                usb.connect_brain_stem()
                msg = "Brainstem Connected"
                print(msg)
                 
            except:
                ready = False
                msg = "Brainstem can't Connect"
                print(msg)
                
                msg = sys.exc_info()[0]
                print(msg)
                
                self.write_results(repos)
                
        elif ready and bs == 'No Brainstem':
            pwr = self.get_power
            if pwr == 'Cold Start Only' or pwr == 'Aux Only':
                ready = Flase
                print(msg)
                
        GT_Custom.custom_run(self, repos, omicron, usb)


    '''
    ============================================================================================================================================================================
    Frame Methods 
    ============================================================================================================================================================================
    '''


    def enter_auto_test_mode(self, repos, usb):            

        self.exit_auto_button.grid(row = 1, column = 0)
        self.enter_auto_button.grid_remove()
        
        usb.communicate("enter_into_auto_test_mode_request")
        rsp = usb.communicate("enter_into_auto_test_mode_check")


    def exit_auto_test_mode(self, repos, usb):            

        self.enter_auto_button.grid(row = 1, column = 0)
        self.exit_auto_button.grid_remove()
        
        usb.communicate("exit_out_of_auto_test_mode_request")
        rsp = usb.communicate("exit_out_of_auto_test_mode_check")



            
            
    def enter_manufactory_mode(self, repos, usb):            

        self.exit_manu_button.grid(row = 1, column = 1)
        self.enter_manu_button.grid_remove()
        
        usb.communicate("enter_into_manufactory_mode_request")
        rsp = usb.communicate("enter_into_manufactory_mode_check")



    def exit_manufactory_mode(self, repos, usb):            

        self.enter_manu_button.grid(row = 1, column = 1)
        self.exit_manu_button.grid_remove()
        
        usb.communicate("exit_out_of_manufactory_mode_request")
        rsp = usb.communicate("exit_out_of_manufactory_mode_check")


    '''
    ============================================================================================================================================================================
    Button Methods (Tab 0)
    ============================================================================================================================================================================
    '''

    def enable_buttons(self):
        
        self.exit_manu_button["state"] = "normal"
        self.enter_manu_button["state"] = "normal"
        self.reset_button["state"] = "normal"
        self.exit_auto_button["state"] = "normal"
        self.enter_auto_button["state"] = "normal"
        self.reset_therm["state"] = "normal"

    def disable_buttons(self):
        self.exit_manu_button["state"] = "disabled"
        self.enter_manu_button["state"] = "disabled"
        self.reset_button["state"] = "disabled"
        self.exit_auto_button["state"] = "disabled"
        self.enter_auto_button["state"] = "disabled"
        self.reset_therm["state"] = "disabled"
        
    def set_pass(self,usb):
        
        usb.communicate("set_password_request", 0,0,0,0)

        
    def create_test_group(self):

            choice = self.fof_cbox.get()
            test_group = []

            if choice == "Folder":

                file_path = self.open_dir_entry.get()

                for root, dirs, files, in os.walk(file_path, topdown = True):
                    for name in files:
                        test_group.append(file_path + '/' + str(os.path.join(name)))
            else:
                temp_group = self.file_scroll.get('1.0', 'end-1c')
                file_group = temp_group.split(',')
                for file in file_group:
                    if len(file) > 5:
                        #Makes sure that the filename is valid.
                        #If it's less than 4 chars, it's not. 
                        test_group.append(file)
                    else:
                        pass
                    
            return test_group
        
    def open_port(self, repos, usb):
        
        name = self.get_port()
        
        usb.set_portname(name)
        disconnected = usb.open_port()

        if disconnected == False:
            self.open_usb.grid_remove()
            self.close_usb.grid(column = 2, row = 0)
            
            self.get_unit_info(repos, usb)
            self.connected = True

            self.update_thread = threading.Thread(target = self.update_msgs, daemon = True, kwargs={'repos':repos})
            self.q.put(self.update_thread)
            self.update_thread.start()
            self.enable_buttons()
            

        else:
            message =  "Issue connecting to " + name 
            repos.append_output_msg(message)

        self.write_results(repos)
        self.write_debug(repos)
         
    def close_port(self, repos, usb):

        name = self.get_port()
        usb.close_port()
        self.open_usb.grid(column = 2, row = 0)
        self.close_usb.grid_remove()
        
        message = "Disconnected from " + name
        repos.append_output_msg(message)
        self.disable_buttons()
        self.connected = False


    def reset_therm(self, repos, usb):

        request = 1
        usb.communicate("thermal_memory_reset_request", request)
        usb.communicate("thermal_memory_reset_check", request)

        
    def open_buffer_com(self, repos, usb):

        run_buffer = GT_Buffer_Screen.Buffer_Screen(repos, usb)

        
    def save_dir(self):

        save_file_path = filedialog.askdirectory(parent=self.my_tk, initialdir= self.sav_start_dir, title='Please select a directory')

        #print path
        if save_file_path != "":
            self.save_dir_entry.delete(0, END)
            self.save_dir_entry.insert(0,save_file_path)
            self.sav_start_dir = save_file_path
            print(self.sav_start_dir)

    def change_open_type(self):


        choice = self.fof_cbox.get()

        if choice == "Folder":

            self.file_scroll.grid_remove()
            self.open_dir_entry.grid(row = 8, column = 5, columnspan = 2)
            self.open_file_button.grid_remove()
            self.open_dir_button.grid(row = 7, column = 5, columnspan = 2)
            
        else:

            self.file_scroll.grid(row = 8, column = 5, rowspan = 6, columnspan = 2)
            self.open_dir_button.grid_remove()
            self.open_file_button.grid(row = 7, column = 5, columnspan = 2)
            self.open_dir_entry.grid_remove()

    def open_dir(self):

        open_folder = filedialog.askdirectory(parent=self.my_tk, initialdir= self.open_start_dir, title='Please select a directory')

        self.open_dir_entry.delete(0, END)
        self.open_dir_entry.insert(0, open_folder)
        self.open_start_dir = open_folder
        
    def open_file(self):

        start_path = os.getcwd()
        open_file = filedialog.askopenfilename(parent=self.my_tk, initialdir= self.open_start_dir, title='Please select a file')
        if len(open_file) > 5:
            self.file_scroll.insert(END, open_file)
            self.file_scroll.insert(END, ",")
            self.file_scroll.see("end")

            self.open_start_dir = ""
            file_parts = open_file.split('/')
            k = len(file_parts)
            for j in range(0, k-1): 
                self.open_start_dir = self.open_start_dir + file_parts[j]
        

      

    def calibrate_primary_setup(self, repos, usb, omicron):

        if self.test_running == False:
            self.test_running = True
            self.calibrate_thread = threading.Thread(target = self.calibrate_primary, daemon = True, kwargs={'repos':repos, 'usb':usb, 'omicron':omicron})
            self.update_thread = threading.Thread(target = self.update_msgs, daemon = True, kwargs={'repos':repos})
            self.q.put(self.calibrate_thread)
            self.q.put(self.update_thread)
            self.update_thread.start()
            self.calibrate_thread.start()
            
    def calibrate_primary(self, repos, usb, omicron):

        ready = True
        repos.ct = self.get_CT()
        
        family = self.get_family()
        repos.choose_translator(family)
        omicron.set_device(family)


            
        try:
            rsp = usb.communicate("read_setpoint_one")
            repos.translator.update_setpoint_one(repos, rsp)
        
        except:
            ready = False
            msg = "USB Connection Problem." + str(sys.exc_info()[0])
            repos.append_output_msg(msg)
            

        connect_to_omicron = self.get_omi_connect()
        if ready and connect_to_omicron == True:
            omicron.connect_omicron()            #  sets up Omicron Engine.app along with Omicron Amplifiers
            omicron.route_llo()
            try:
                #omicron.connect_omicron()            #  sets up Omicron Engine.app along with Omicron Amplifiers
                #omicron.route_llo()
                omicron.turn_on_aux()
                
                omi_config = self.get_omi_config()
                if omi_config == 'Output A and B':
                    omicron.route_a_and_b()
                    

            except:
                ready = False
                msg = "Omicron can't Connect" +str(sys.exc_info()[0])
                repos.append_output_msg(msg)

        elif connect_to_omicron == False:
            msg ="No Omicron detected. No calibration will be done."
            repos.append_output_msg(msg)
            ready = False

        
        if ready:  
            GT_Calibration.pxr_20_and_25_cal(repos, usb, omicron)
            omicron.unlock_omicron()

            
        msg = "Primary Calibration Complete"
        repos.append_output_msg(msg)

        self.update_results(repos)
        self.update_debug(repos)
        self.test_running = False
        
    def calibrate_secondary(self, repos):

        ready = True
        family = self.get_family()
        repos.choose_translator(family)
        
        try:
            rsp = usb.communicate("read_breaker_frame_request")
            
            repos.set_points['frame']  = GT_USB_commands.read_breaker_frame_request(repos)
        except:
            ready = False
            msg = "USB Connection Problem."
            self.write_results(msg)

        if ready:   
            GT_Calibration.calibrate_secondary_inection(repos)
            
        msg = "Secondary Calibration Complete"
        self.write_results(msg)

    def custom_test(self, repos, usb):

        print("nothing now")
        


    def pause_test(self, usb):

        #self.test_running = False
        
        self.testing_thread.pause
        print("Stop")

    def unpause_test(self, usb):
        
        self.test_running = True
        print("RUN")

    '''
    ============================================================================================================================================================================
    Updating Outputs
    ============================================================================================================================================================================
    '''

    def write_results(self, repos):
        #message = "\n"+ str(message)
        message = repos.output_msg
        if message != "":
            self.result_scroll.insert(END, message)
            self.result_scroll.see("end")

        repos.clear_output_msg()
        self.my_tk.update()
        
    def write_debug(self, repos):
        
        message = repos.debug_msg
        self.debug_scroll.insert(END, message)
        self.debug_scroll.see("end")
        
        repos.clear_debug_msg()
        self.my_tk.update()

    def update_results(self, repos):
        #message = "\n"+ str(message)
        message = repos.output_msg
        if message != "":
            self.result_scroll.insert(END, message)
            self.result_scroll.see("end")

        repos.clear_output_msg()
        self.my_tk.update()
        
    def update_debug(self, repos):
        
        message = repos.debug_msg
        if message != "":
            self.debug_scroll.insert(END, message)
            self.debug_scroll.see("end")

        
        repos.clear_debug_msg()
        self.my_tk.update()

    def update_msgs(self, repos):

        while self.connected == True:
            self.update_results(repos)
            self.update_debug(repos)
            if repos.msg_entry_count == 500:
                repos.msg_entry_count = 0
                self.result_scroll.delete('1.0', END)
                self.debug_scroll.delete('1.0', END)
                
                
            time.sleep(2)

    def print_msgs(self, repos , part_file):

        testing_string = self.result_scroll.get('1.0', END)
        print(testing_string)

        file_path = part_file + ".txt"
        with open(file_path, 'w') as file:
            file.write(testing_string)
        
    '''
    ============================================================================================================================================================================
    Buffer/Setpoint Methods (Tab 1/2)
    ============================================================================================================================================================================
    '''


        
    def update_buffset(self, repos, section, choice):

        label_array, entry_array, grid_array = self.get_section_info(section)
        usb_req, trnslt_op, keys             = self.get_buffset_info(repos, choice, "r")

        row = grid_array[0]
        col = grid_array[1]   
        
        j = 0

        tab_sel = self.tab_screen.index(self.tab_screen.select())

        buffset_dic = repos.etu_dictionary

        
        for i in range(0, len(keys)):

            label_array[i].grid(row = row+j, column = col)
            label_array[i].config(text = keys[i])
            
            entry_array[i].delete(0, END)
            entry_array[i].grid(row = row+j, column = col+1, columnspan =1)
            data = buffset_dic[keys[i]][0]
            entry_array[i].insert(0,data)
            j = j+1
            if j>25:
                j = 0
                col = col + 3            

    def label_section(self, repos, section, choice):

        label_array, entry_array, grid_array = self.get_section_info(section)
        usb_req, trnslt_op, keys = self.get_buffset_info(repos, choice, "r")
        
        for i in range(0, len(label_array)):
            label_array[i].grid_forget()
            entry_array[i].grid_forget()

        self.update_buffset(repos, section, choice)

    

        
    def get_section_info(self, section):

        tab_sel = self.tab_screen.index(self.tab_screen.select())
        print(tab_sel)
        
        if tab_sel == 1:
            if section == 0:
                label_array = self.label_zero_array
                entry_array = self.entry_zero_array
                grid_array = [3, 0]
            elif section == 1:
                label_array = self.label_one_array 
                entry_array = self.entry_one_array 
                grid_array = [3, 5]
            elif section == 2:
                label_array = self.label_two_array 
                entry_array = self.entry_two_array 
                grid_array = [3, 10]
        elif tab_sel == 2:
            if section == 0:
                label_array = self.s_label_zero_array 
                entry_array = self.s_entry_zero_array 
                grid_array = [3, 0]
            elif section == 1:
                label_array = self.s_label_one_array 
                entry_array = self.s_entry_one_array 
                grid_array = [3, 5]


        return label_array, entry_array, grid_array
    
    def get_buffset_info(self, repos, choice, rw):

        info_array = repos.mapping_dictionary[choice]

        if rw == "r":
            usb_req = info_array[2]
        else:
            usb_req = info_array[1]
        trnslt_op = "None"     

        if choice == 'Buffer 0':
            trnslt_op = "translate_buffer_zero"

        keys = info_array[0]
        print(usb_req)
        print(keys)
        
        return usb_req, trnslt_op, keys
    
    def read_buffset(self, repos, usb, read_sp, trnslt_op, keys):

        print(read_sp)    
        rsp = usb.communicate(read_sp)
        cor = usb.get_correctness(rsp)
        if cor == "successful":

            buffset_dic = repos.etu_dictionary

            if trnslt_op != "translate_buffer_zero":
                new_setpoints = repos.translator.translate_generic_no_write(rsp, keys, buffset_dic)
            else: 
                new_setpoints = repos.translator.translate(trnslt_op, rsp, repos.pxr)

            j = 0 
            for key in keys:
                buffset_dic[key][0] = new_setpoints[j]
                j = j+1

            if read_sp == "read_setpoint_one":
                GT_Conversions.convert_etu_to_standard(repos)
                keys = repos.sp_one_keys
                
        else:
            msg = "Issue Reading Message From "  + read_sp + "\n" + cor
            repos.append_output_msg(msg)
        
    def read_command(self, repos, usb, section):

        tab_sel = self.tab_screen.index(self.tab_screen.select())
        if tab_sel == 1:
            if section == 0:
                choice = self.zero_cbox.get()
            elif section == 1:
                choice = self.one_cbox.get()
            elif section == 2:
                choice = self.two_cbox.get() 
        else:
            if section == 0:
                choice = self.s_zero_cbox.get()
            elif section == 1:
                choice = self.s_one_cbox.get()

            
        usb_req, trnslt_op, keys = self.get_buffset_info(repos, choice, "r")
        
        self.read_buffset(repos, usb, usb_req, trnslt_op, keys)                         
        self.update_buffset(repos, section, choice)

    def write_command(self, repos, usb, section):

        if section == 0: 
            choice = self.s_zero_cbox.get()
            entry_array = self.s_entry_zero_array
        elif section == 1:
            choice = self.s_one_cbox.get()
            entry_array = self.s_entry_one_array

        keys = repos.mapping_dictionary[choice][0]
        usb_com = repos.mapping_dictionary[choice][1]
        
        for i in range(0, len(keys)):
            data = entry_array[i].get()
            msg = keys[i] + "  " + str(data)
            print(msg)
            repos.etu_dictionary[keys[i]][0] = float(data)

##        if choice == "Setpoint 0":
##            usb_com = "write_setpoint_zero_request"
##            
##        elif choice == "Setpoint 1":
##            GT_Conversions.convert_standard_to_etu(repos)
##            usb_com = "write_setpoint_one_request"
##            
##        elif choice == "Setpoint 2":
##            usb_com = "write_setpoint_two_request"
##
##        elif choice == "Setpoint 3":
##            usb_com = "write_setpoint_three_request"
##
##        elif choice == "Setpoint 4":
##            usb_com = "write_setpoint_four_request"
##            
##        elif choice == "Setpoint 5":
##            usb_com = "write_setpoint_five_request"
##
##        elif choice == "Setpoint 6":
##            usb_com = "write_setpoint_six_request"
            
        GT_Conversions.convert_standard_to_etu(repos)
        rsp = usb.communicate("enter_password_request", 0, 0, 0,0, 0, 0)
        cor = usb.get_correctness(rsp)
        rsp = usb.communicate(usb_com, keys,  repos.etu_dictionary)
        cor = usb.get_correctness(rsp)
                             
    def change_zero_check(self, repos, usb):

        zero = self.zero_refresh.get()

        if zero == False:
            self.zero_refresh.set(False)
            
        else:
            self.zero_refresh.set(True)
            self.section_zero_refresh(repos, usb)
            
    def change_one_check(self, repos, usb):

        one = self.one_refresh.get()

        if one == False:
            self.one_refresh.set(False)
            
        else:
            self.one_refresh.set(True)
            self.section_one_refresh(repos, usb)

    def change_two_check(self, repos, usb):

        two = self.two_refresh.get()

        if two == False:
            self.two_refresh.set(False)
            
        else:
            self.two_refresh.set(True)
            self.section_two_refresh(repos, usb)


    def change_sp_zero_check(self, repos, usb):

        zero = self.sp_zero_refresh.get()

        if zero == False:
            self.sp_zero_refresh.set(False)
            
        else:
            self.sp_zero_refresh.set(True)
            self.section_sp_zero_refresh(repos, usb)
            

    def section_sp_zero_refresh(self, repos, usb):

        zero = self.sp_zero_refresh.get()
        print(zero)
        if zero == True:

            choice = self.s_zero_cbox.get() 
            usb_req, trnslt_op, keys = self.get_buffset_info(repos, choice, "r")            
            self.read_buffset(repos, usb, usb_req, trnslt_op, keys)                         

            self.update_buffset(repos, 0, choice)
                             
            self.tab_one.after(1000, lambda: self.section_sp_zero_refresh(repos, usb))
            
    def section_zero_refresh(self, repos, usb):

        zero = self.zero_refresh.get()
        if zero == True:

            choice = self.zero_cbox.get() 
            usb_req, trnslt_op, keys = self.get_buffset_info(repos, choice, "r")            
            self.read_buffset(repos, usb, usb_req, trnslt_op, keys)                         

            self.update_buffset(repos, 0, choice)
                             
            self.tab_one.after(1000, lambda: self.section_zero_refresh(repos, usb))

    def section_one_refresh(self, repos, usb):

       
        one = self.one_refresh.get()
        if one == True:

            choice = self.one_cbox.get() 
            usb_req, trnslt_op, keys = self.get_buffset_info(repos, choice, "r")            
            self.read_buffset(repos, usb, usb_req, trnslt_op, keys)                         

            self.update_buffset(repos, 1, choice)
                             
            self.tab_one.after(1000, lambda: self.section_one_refresh(repos, usb))

    def section_two_refresh(self, repos, usb):
        
        two = self.two_refresh.get()
        if two == True:


            choice = self.two_cbox.get() 
            usb_req, trnslt_op, keys = self.get_buffset_info(repos, choice, "r")            
            self.read_buffset(repos, usb, usb_req, trnslt_op, keys)                         

            self.update_buffset(repos, 2, choice)
                             
            self.tab_one.after(1000, lambda: self.section_two_refresh(repos, usb))
            

    '''
    ============================================================================================================================================================================
    Secondary Method (Tab 3)
    ============================================================================================================================================================================
    '''

    def run_secondary(self, repos, usb):

        if self.test_running == False:
            self.test_running = True
            self.testing_thread = threading.Thread(target = self.secondary_injection_thread, daemon = True, kwargs={'repos':repos, 'usb':usb})
            self.q.put(self.testing_thread)
            self.testing_thread.start()

    def secondary_injection_thread(self, repos, usb):           
        simhard = self.simhard_cbox.get()
        sec_type = self.sec_type_cbox.get()
        my_phase = self.sec_phase_cbox.get()
        I =  int(self.sec_cur_entry.get())
        
        #next_space = "Next  " + str(master.index)
        repos.t_max = 10000

        print(my_phase)
        
        if my_phase == "A":
            repos.expected['I A (Amps)'] = I
            repos.expected['I B (Amps)'] = 0
            repos.expected['I C (Amps)'] = 0
            
        elif my_phase == "B":
            repos.expected['I A (Amps)'] = 0
            repos.expected['I B (Amps)'] = I
            repos.expected['I C (Amps)'] = 0
 
        elif my_phase == "C":
            repos.expected['I A (Amps)'] = 0
            repos.expected['I B (Amps)'] = 0
            repos.expected['I C (Amps)'] = I

        if simhard == "Simulated":
            self.running_secondary = "Simulated"
            
            if sec_type == "RMS With Trip":
                start = "software_rms_test_with_trip_request"
                check = "software_rms_test_with_trip_check"
                cancel = "cancel_software_test_request"
                cancel_check = "cancel_software_test_request"
                if repos.family == "35":
                    check = "read_simulated_test_results_request"
                
            elif sec_type == "RMS No Trip":
                start = "secondary_injection_rms_test_without_trip_request"
                check = "secondary_injection_rms_test_without_trip_check"
                cancel = "cancel_secondary_injection_test_request"
                cancel_check = "cancel_secondary_injection_test_check"
                if repos.family == "35":
                    check = "read_simulated_test_results_request"
            
        elif simhard == "Hardware":
            self.running_secondary = "Hardware"
            
            if sec_type == "RMS With Trip":
                start  = "secondary_injection_rms_test_with_trip_request"
                check  = "secondary_injection_rms_test_with_trip_check"
                cancel = "cancel_secondary_injection_test_request"
                cancel_check = "cancel_secondary_injection_test_request"
                if repos.family == "35":
                    check = "read_simulated_test_results_request"
                
            elif sec_type == "RMS No Trip":
                start  = "software_rms_test_without_trip_request"
                check  = "software_rms_test_without_trip_check"
                cancel = "cancel_software_test_request"
                cancel_check = "cancel_software_test_request"
                if repos.family == "35":
                    check = "read_simulated_test_results_request"
            
    
        trip_time = GT_Secondary_Injection.secondary_time(repos, usb, start, check, cancel, cancel_check)
        self.running_secondary = "None"
        self.test_running = False

    def cancel_test(self, repos, usb):

        if self.running_secondary == "Simulated":
            rsp = usb.communicate("cancel_software_test_request")
            rsp = usb.communicate("cancel_software_test_check")
            
        elif self.running_secondary == "Hardware":
            rsp = usb.communicate("cancel_secondary_injection_test_request")
            rsp = usb.communicate("cancel_secondary_injection_test_check")
            
        else:
            pass

    def clear_secondary(self, repos, usb):  
        rsp = usb.communicate("clear_secondary_injection_request")


        cor = "busy"
        while cor == "busy":
            time.sleep(.05)
            cor = usb.communicate_with_check("clear_secondary_injection_check")

    def base_secondary(self, repos, usb):

        rsp = usb.communicate("secondary_injection_base_counter_calibration_request")
        cor = "busy"
        while cor == "busy":
            time.sleep(.05)
            cor = usb.communicate_with_check("secondary_injection_base_counter_calibration_check")
            
                                
    def delta_secondary(self, repos, usb):

                                
        rsp = usb.communicate("secondary_injection_delta_counter_calibration_request")
        cor = "busy"
        while cor == "busy":
            time.sleep(.05)
            cor = usb.communicate_with_check("secondary_injection_delta_counter_calibration_check")

            
    def secondary_calibrate_test_injection_gain(self, repos, usb):
        my_phase = self.sec_phase_cbox.get()
        if my_phase == "A":
            my_phase = 0 
        elif my_phase == "B":
             my_phase = 1
        elif my_phase == "C":
            my_phase = 2

        rsp = usb.communicate("calibrate_current_gain_test_injection_request", my_phase, 0)
        cor = "busy"
        while cor == "busy":
            cor = usb.communicate_with_check("calibrate_curent_gain_test_injection_check")
            print(cor)

    def secondary_calibrate_test_offset_injection(self, repos, usb):
        my_phase = self.sec_phase_cbox.get()

        if my_phase == "A":
            my_phase = 0 
        elif my_phase == "B":
             my_phase = 1
        elif my_phase == "C":
            my_phase = 2
            
        rsp = usb.communicate("calibrate_current_offset_test_injection_request", my_phase, 0)
        cor = "busy"
        while cor == "busy":
            cor = usb.communicate_with_check("calibrate_curent_offset_test_injection_check")
            print(cor)
            
    '''
    ============================================================================================================================================================================
    Configuration Tab Methods (Tab 4)
    ============================================================================================================================================================================
    '''

    def read_frame(self, repos, usb):
        

        if repos.family == "ACB" or repos.family == "35":
            rsp = usb.communicate("read_breaker_frame_request")
            rsp = usb.communicate("read_breaker_frame_check")
        elif repos.family == "MCCB":
            rsp = usb.communicate("read_breaker_frame_request")


        frame = repos.translator.translate("translate_breaker_frame", rsp)
        self.frame_entry.delete(0, END)
        self.frame_entry.insert(0, frame)
        repos.frame = frame
        

            
    def write_frame(self, repos, usb):


        frame = int(self.frame_entry.get())
        print(frame)
        
        rsp = usb.communicate("write_breaker_frame_request", frame)
        rsp = usb.communicate("write_breaker_frame_check")

        cor = usb.get_correctness(rsp)

        if cor == "successful":
            repos.frame = frame


    def read_rating(self, repos, usb):
        
        if repos.family == "ACB" or repos.family == "35":
            rsp = usb.communicate("read_breaker_rating_request")
            rsp = usb.communicate("read_breaker_rating_check")
        elif repos.family == "MCCB":
            rsp = usb.communicate("read_breaker_rating_request")


        frame = repos.translator.translate("translate_breaker_rating", rsp)
        self.rating_entry.delete(0, END)
        self.rating_entry.insert(0, frame)
  
        
    def write_rating(self, repos, usb):
        rating = int(self.rating_entry.get())
        
        rsp = usb.communicate("write_breaker_rating_request", rating)
        rsp = usb.communicate("write_breaker_rating_check")

        cor = usb.get_correctness(rsp)

        if cor == "successful":
            repos.rating = rating

    def read_style(self, repos, usb):

        rsp = usb.communicate("read_trip_unit_style_request")
        rsp = usb.communicate("read_trip_unit_style_check")
        
        style = repos.translator.translate_style(rsp)
        val = style[2]
        self.style_cbox.current(val)
        
    def write_style(self, repos, usb):

        style = self.style_cbox.current()
        rsp = usb.communicate("write_trip_unit_style_request", style)
        rsp = usb.communicate("read_trip_unit_style_check")


        
    def read_configuration(self, repos, usb):
        label_array  = self.config_label_array
        entry_array = self.config_entry_array

        acb_labels = ["Poles", "Standard", "Device Type",
                      "Voltage Metering", "Max IEC Amps", "Max UL Amps",
                      "Max ANSI/UL Amps", "Frame Amps", "Min In",
                      "Withstand Limit", "MCR Multiplier", "Ground Fault Max",
                      "Max Physical Limit", "Max Label", "Max Instantaneous"]


        usb.communicate("read_breaker_configuration_request")
        msg = usb.communicate("read_breaker_configuration_check")
        config = repos.translator.translate_configuration(msg)


        j = 0 
        for key in repos.configuration_keys:
            repos.configuration[key] = config[j]
            j = j + 1
            
        r = 2
        x = 0 
        for label in acb_labels:

            label_array[x].grid(row = r, column = 5)
            label_array[x].config(text = label)
            
            entry_array[x].delete(0, END)
            entry_array[x].grid(row = r, column = 6, columnspan =1)
            data = config[x]
            entry_array[x].insert(0,data)
            x = x+1
            r = r + 1
   
        
    def write_configuration(self, repos, usb):


        entry_array = self.config_entry_array

        fail_array = []
        fail_index = []
        
        config = []
        for j in range(0, len(repos.configuration_keys)):
            val = entry_array[j].get()

            if val == '':
                val = 0 
                fail_array.append(1)
                fail_index.append(repos.configuration_keys[j])
                
            try:
                data = int(val)
            except:
                data = 0 
                fail_array.append(2)
                fail_index.append(repos.configuration_keys[j])

                config.append(data)

        if len(fail_array) > 0:

            for i in range(0, len(fail_array)):
                if fail_array[i] == 1:
                    msg = "No Value"
                elif fail_array[i] == 2:
                    msg = "Not An Int"
 

                fail_setpoint = fail_index[i]

                full_msg = fail_setpoint + " Has Error " + msg
        else:
            rsp = usb.communicate("write_breaker_configuation_request", repos.configuration_keys, repos.configuration)
            rsp = usb.communicate("write_breaker_configuation_check")
            cor = usb.get_correctness(rsp)
            print(cor)
            

        print(config)



    '''
    ============================================================================================================================================================================
    Configuration Tab Methods (Tab 5)
    ============================================================================================================================================================================
    '''

    def read_i_health(self, repos, usb):

        rsp = usb.communicate("read_real_time_data_buffer_eleven")

        repos.etu_dictionary_vals['date_raw_op'][0]   = GT_Conversions.uint_sixteen_to_dec(rsp, 108)
        repos.etu_dictionary_vals['date_raw_temp'][0] = GT_Conversions.uint_sixteen_to_dec(rsp, 138)

        repos.translator.translate_generic(rsp, repos.buffer_eleven_keys, repos.etu_dictionary)
##        vals = repos.translator.translate_buffer_eleven(rsp)
##        repos.update_buffers(vals, 11)
        
        x = 0 
        for key in repos.etu_dictionary_eleven_keys:

            self.i_health_entry_array[x].delete(0, END)
            data = repos.etu_dictionary_vals[key]
            self.i_health_entry_array[x].insert(0,data)
            x = x+1
            
            
      

    def write_i_health(self, repos, usb):


        repos.etu_dictionary_vals['int_time_of_last_op'][0] = repos.etu_dictionary_vals['date_raw_op'][0]
        repos.etu_dictionary_vals['int_time_max_temp'][0]   = repos.etu_dictionary_vals['date_raw_temp'][0]

        print(repos.etu_dictionary_vals['int_time_of_last_op'][0])
        print(repos.etu_dictionary_vals['int_time_max_temp'][0])
        rsp = usb.communicate("write_internal_diagnostics", repos.etu_dictionary_eleven_keys, repos.etu_dictionary_vals)
        
    def read_e_health(self, repos, usb):
        rsp = usb.communicate("read_real_time_data_buffer_six")
        repos.translator.translate_generic(rsp, repos.buffer_seven_keys, repos.etu_dictionary)
        
        x = 0 
        for key in repos.etu_dictionary_six_keys:

            self.e_health_entry_array[x].delete(0, END)
            data = repos.etu_dictionary_vals[key]
            self.e_health_entry_array[x].insert(0,data)
            x = x+1
            
    def write_health(self, repos, usb):
        print("HI")
    
        
    '''
    ============================================================================================================================================================================
    Getters
    ============================================================================================================================================================================
    '''

    def get_CT(self):

        my_CT = self.CT_cbox.get()
        return my_CT
    

    def get_family(self):

        my_family = self.family_cbox.get()
        return my_family
    
    def get_neutral(self):

        my_neutral = self.neutral_cbox.get()

        if my_neutral == "Neutral":
            return 1
        else:
            return 0

    def get_num_runs(self):

        num_runs = self.num_runs.get()
        return num_runs

    def get_freq(self):
        my_freq = self.freq_choice.get()
        return my_freq

    def get_ia_ang(self):
        my_ia = self.ia_ang_choice.get()
        return my_ia
    
    def get_ib_ang(self):
        my_ib = self.ib_ang_choice.get()
        return my_ib
    
    def get_ic_ang(self):
        my_ic = self.ic_ang_choice.get()
        return my_ic
    
    def get_ra_ang(self):
        my_ra = self.ra_ang_choice.get()
        return my_ra
    
    def get_rb_ang(self):
        my_rb = self.rb_ang_choice.get()
        return my_rb
    
    def get_rc_ang(self):
        my_rc = self.rc_ang_choice.get()
        return my_rc
    
    def get_port(self):
        my_port = self.USB_cbox.get()
        return my_port
    
    def get_phase(self):
        my_phase = self.phase_cbox.get()
        return my_phase
    
    def get_power(self):
        my_power = self.power_cbox.get()
        return my_power

    def get_test_type(self):
        my_test_type = self.test_type_cbox.get()
        return my_test_type
    
    def get_omi_connect(self):
        my_connect = self.omi_connect_cbox.get()
        if my_connect == 'Yes':
            return True
        else:
            return False
    
    def get_omi_config(self):
        my_config = self.omi_config_cbox.get()
        return my_config

    def get_bs(self):
        my_bs = self.bs_cbox.get()
        return my_bs
    '''
    ============================================================================================================================================================================
    USB Check 
    ============================================================================================================================================================================
    '''

    def get_unit_info(self, repos, usb):

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
                rsp = usb.communicate("read_trip_unit_style_check")
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

                style_one_array = style_array[0]
                style_two_array = style_array[1]
                print(style_two_array)
                

                if style_two_array[0] == 1:
                    repos.pxr = "PXR25"
                else:
                    if style_two_array[4] == 0: #b4 is ZSI. PXR10 Shouldn't have it
                        repos.pxr = "PXR10"
                        repos.set_pxr10()
                    else:
                        repos.pxr = "PXR20"
                        repos.set_pxr20()

                print(repos.pxr)

            repos.set_mapping_dictionary()

            self.ui_buffer_keys = []
            self.ui_setpoint_keys = []
            for val in repos.mapping_keys:
                if "Buffer" in val:
                    self.ui_buffer_keys.append(val)
                    
            for val in repos.mapping_keys:
                if "Setpoint" in val:
                    self.ui_setpoint_keys.append(val)
                    
            
            self.zero_cbox['values'] = self.ui_buffer_keys
            self.s_zero_cbox['values'] = self.ui_setpoint_keys
            
        return connected


    '''
    ============================================================================================================================================================================
    Save/Load UI configuration
    ============================================================================================================================================================================
    '''

    def save_prop(self):

        f = open("startup.txt", "w+")
        print("Saving props")
        CT = self.CT_cbox.get()
        PXR = "0"
        power = self.power_cbox.get()
        phase = self.phase_cbox.get()
        runs = self.num_runs.get()
        freq = self.freq_choice.get()
        ia_ang = self.ia_ang_choice.get()
        ib_ang = self.ib_ang_choice.get()
        ic_ang = self.ic_ang_choice.get()
        ra_ang = self.ra_ang_choice.get()
        rb_ang = self.rb_ang_choice.get()
        rc_ang = self.rc_ang_choice.get()
        bs = self.bs_cbox.get()
        omi_connect = self.omi_connect_cbox.get()
        omi_config = self.omi_config_cbox.get()
        save_dir = self.sav_start_dir
        fof = self.fof_cbox.get()
        open_choice = self.fof_cbox.get()
        open_dir = self.open_start_dir
        open_group = self.file_scroll.get('1.0', 'end-1c')

        f.write(str(CT)+",")
        f.write(str(PXR)+",")
        f.write(str(power)+",")
        f.write(str(phase)+",")
        f.write(str(runs)+",")
        f.write(str(freq)+",")
        f.write(str(ia_ang)+",")
        f.write(str(ib_ang)+",")
        f.write(str(ic_ang)+",")
        f.write(str(ra_ang)+",")
        f.write(str(rb_ang)+",")
        f.write(str(rc_ang)+",")
        f.write(str(bs)+",")
        f.write(str(omi_connect)+",")
        f.write(str(omi_config)+",")
        f.write(str(save_dir)+",")
        f.write(str(fof+","))
        f.write(str(open_choice+","))
        f.write(str(open_dir+","))
        f.write(str(open_group))
        
        f.close()

    def get_prop(self):

        if path.isfile("startup.txt"):
            
            f = open("startup.txt", "r")
            
            f_line = f.readline()

            file_array = f_line.split(",")
            print(file_array)
            CT = str(file_array[0])
            PXR = file_array[1]
            power = file_array[2]
            phase = file_array[3]
            runs = int(file_array[4])
            freq = int(file_array[5])
            ia_ang = int(file_array[6])
            ib_ang = int(file_array[7])
            ic_ang = int(file_array[8])
            ra_ang = int(file_array[9])
            rb_ang = int(file_array[10])
            rc_ang = int(file_array[11])
            bs = file_array[12]
            omi_connect = file_array[13]
            omi_config = file_array[14]
            save_dir = file_array[15]
            fof = file_array[16]
            open_choice = file_array[17] 
            open_dir = file_array[18]
            
            total_len = len(file_array)
            open_group = ""
            if total_len - 19 != 0:
                for num in range(19, total_len):
                    open_group = open_group + file_array[num] + ","
            
            
            temp = self.CT_cbox['values']
            i = temp.index(CT)
            self.CT_cbox.current(i)
            

            i = self.power_cbox['values'].index(power)
            self.power_cbox.current(0)

            i = self.phase_cbox['values'].index(phase)
            self.phase_cbox.current(i)

            self.num_runs.set(runs)
            self.freq_choice.set(freq)         
            self.ia_ang_choice.set(ia_ang)
            self.ib_ang_choice.set(ib_ang)
            self.ic_ang_choice.set(ic_ang)
            self.ra_ang_choice.set(ra_ang)
            self.rb_ang_choice.set(rb_ang)
            self.rc_ang_choice.set(rc_ang)

            i = self.bs_cbox['values'].index(bs)
            self.bs_cbox.current(i)


            i = self.omi_connect_cbox['values'].index(omi_connect)
            self.omi_connect_cbox.current(i)


            i = self.omi_config_cbox['values'].index(omi_config)
            self.omi_config_cbox.current(i)
                
            i = self.fof_cbox['values'].index(fof)
            self.fof_cbox.current(0)

                

            self.save_dir_entry.delete(0, END)
            self.save_dir_entry.insert(0,save_dir)

            if open_choice == "Folder":

                self.file_scroll.grid_remove()
                self.open_dir_entry.grid(row = 8, column = 5, columnspan = 2)
                self.open_file_button.grid_remove()
                self.open_dir_button.grid(row = 7, column = 5, columnspan = 2)
                self.open_dir_entry.delete(0, END)
                self.open_dir_entry.insert(0,open_dir)
                
            else:

                self.file_scroll.grid(row = 8, column = 5, rowspan = 6, columnspan = 2)
                self.open_dir_button.grid_remove()
                self.open_file_button.grid(row = 7, column = 5, columnspan = 2)
                self.open_dir_entry.grid_remove()
                self.file_scroll.delete('1.0', END)
                self.file_scroll.insert(END, open_group)
                self.file_scroll.delete("end-2c", END) #Gets rid of extra comma at the end
            

        else:
            msg = "No Startup File"
 
        

        
def main_with_ui():

    repos, usb, omicron = init()               #  run init routine

    root = Tk()    
    General_Test_UI(repos, omicron, usb, root)

    root.mainloop()

def init():                  #  initialization routine
    repos = GT_Repository.Repository()   #  create master object
    usb = GT_USB.USB_Communication()
    usb.set_repository(repos)
    omicron = GT_Omicron.Omicron()
    
    return repos, usb, omicron

main_with_ui()
