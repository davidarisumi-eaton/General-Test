from __future__ import division
import time

from openpyxl import Workbook
from openpyxl.styles import Alignment
from openpyxl import load_workbook

from openpyxl.styles.borders import Border, Side

import win32com
from win32com.client import Dispatch

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

import time

import GT_Excel_Interface
import GT_ACB_Settings, GT_ACB35_Settings, GT_MCCB_Settings
import GT_Excel_Interface

import tkinter
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as tkst
from tkinter.filedialog import askopenfilename



class Repository(object):
    def __init__(self):
        print("Starting")
        


class My_UI(object):

    def __init__(self, repos, root):

        self.my_tk = root
        
        self.my_tk.title('Test UI')
        self.my_tk.resizable(width = FALSE, height = FALSE)
        self.my_tk.geometry('{}x{}'.format(350, 200))

        self.main_frame = Frame(self.my_tk, bg='grey93', width = 350, height = 200).grid(row = 0, rowspan = 20, column = 0, columnspan = 20)
        
        self.tab_screen = ttk.Notebook(self.main_frame,width = 250, height = 150)
        self.tab_screen.grid(row = 2, rowspan = 17, column = 3, columnspan = 17)
        
        self.tab_zero   = ttk.Frame(self.tab_screen)
        
        self.tab_screen.add(self.tab_zero,  text = "Test")

        self.open_start_dir = os.getcwd()
        self.sav_start_dir = os.getcwd()

        Label(self.tab_zero, text = "File and Directory Options").grid(row = 1, column = 5, columnspan = 2)

        self.save_dir_button = Button(self.tab_zero, text = "Pick Save Directory", command = lambda: self.save_dir())
        self.save_dir_button.grid(row = 3, column = 5, columnspan = 2)

        self.save_dir_entry = Entry(self.tab_zero, width = 40)
        self.save_dir_entry.grid(row = 4, column = 5, columnspan = 2)
        save_file_path = os.getcwd()
        self.save_dir_entry.insert(0,save_file_path)
        
        self.open_file_button = Button(self.tab_zero, text = "Pick Choose File", command = lambda: self.open_file())
        self.open_file_button.grid(row = 7, column = 5, columnspan = 2)

##        self.file_scroll = tkst.ScrolledText(master = self.tab_zero, width = 28, height = 10)
##        self.file_scroll.grid(row = 8, column = 5, rowspan = 6, columnspan = 2)
##        self.file_scroll.grid_remove()
##        self.file_index = 0

        self.open_file_entry = Entry(self.tab_zero, width = 40)
        self.open_file_entry.grid(row = 9, column = 5, columnspan = 2)
        save_open_file_path = os.getcwd()
        self.open_file_entry.insert(0,save_file_path)

        self.start_button = Button(self.tab_zero, text = "Start", command = lambda: self.start(repos))
        self.start_button.grid(row = 11, column = 5, columnspan = 2)
        


    def save_dir(self):

        save_file_path = filedialog.askdirectory(parent=self.my_tk, initialdir= self.sav_start_dir, title='Please select a directory')

        #print path
        if save_file_path != "":
            self.save_dir_entry.delete(0, END)
            self.save_dir_entry.insert(0,save_file_path)
            self.sav_start_dir = save_file_path
            print(self.sav_start_dir)
            

    def open_file(self):

        start_path = os.getcwd()
        open_file_path = filedialog.askopenfilename(parent=self.my_tk, initialdir= self.open_start_dir, title='Please select a file')
        if open_file_path != "":
            self.open_file_entry.delete(0, END)
            self.open_file_entry.insert(0,open_file_path)
            self.open_file = open_file_path

            

                
    def setup_repos(self, config_file, active_row, my_repository):
        my_repository.main_keys = []
        my_repository.expected_keys = []
        my_repository.custom_setpoints = []
        #my_repository.main_keys = []
        
        frame = config_file.read_string_from_cell(3, active_row, 0)
        PXR   = config_file.read_cell(2, active_row, 0)
        my_repository.pxr   = config_file.read_cell(2, active_row, 0)
        my_repository.expected_runs = config_file.read_cell(5, active_row, 0)
        print(PXR)

        if PXR == "35" or PXR == 35:
            print(35)
            GT_ACB35_Settings.get_dictionary(my_repository)
            GT_ACB35_Settings.get_setpoint_keys(my_repository)
            GT_ACB35_Settings.get_buffer_keys(my_repository)
            GT_ACB35_Settings.get_mapping_dictionary(my_repository)
        elif frame == "Standard" or frame == "Narrow" or frame == "Double Standard" or frame == "Double Narrow":
            GT_ACB_Settings.get_dictionary(my_repository)
            GT_ACB_Settings.get_setpoint_keys(my_repository)
            GT_ACB_Settings.get_buffer_keys(my_repository)
            GT_ACB_Settings.get_mapping_dictionary(my_repository)
        else:
            GT_MCCB_Settings.get_dictionary(my_repository)
            GT_MCCB_Settings.get_setpoint_keys(my_repository)
            GT_MCCB_Settings.get_buffer_keys(my_repository)
            GT_MCCB_Settings.get_mapping_dictionary(my_repository)
            
        input_keys        = ['Test Type',
                             'I A (Amps)',
                             'I B (Amps)',
                             'I C (Amps)',
                             'I A (PU)',
                             'I B (PU)',     
                             'I C (PU)',
                             'V A',
                             'V B',
                             'V C',
                             'Max Time',
                             'Min Time']

        my_repository.mapping_dictionary["Inputs"] = [input_keys,"", ""]

        expected      =     {'Test Type'     :["Trip","Placeholder"],
                             'I A (Amps)'    :[0,"Placeholder"],
                             'I B (Amps)'    :[0,"Placeholder"],
                             'I C (Amps)'    :[0,"Placeholder"],
                             'I A (PU)'      :[0,"Placeholder"],
                             'I B (PU)'      :[0,"Placeholder"],    
                             'I C (PU)'      :[0,"Placeholder"],
                             'V A'           :[0,"Placeholder"],
                             'V B'           :[0,"Placeholder"],
                             'V C'           :[0,"Placeholder"],
                             'Max Time'      :[0,"Placeholder"],
                             'Min Time'      :[0,"Placeholder"]}

        
        my_repository.etu_dictionary = {**my_repository.etu_dictionary, **expected}



   
    def get_default_vals(self, base_test, my_repository):


        
        tabs = base_test.sheet_array
        i = 0
        
         
        for tab in tabs:
            sp = base_test.read_string_from_cell(1, 1, i)
            
            if i == 0:
                my_repository.old_rating = base_test.read_cell(3, 5, 0)
                
            elif i == 1:
                pass
            
            elif sp == "Custom":
                k = 1 
                while True:
                    sp_val = base_test.read_string_from_cell(k,4, i)
                    if sp_val != None and sp_val != '' and sp_val != "None":
                        my_repository.custom_setpoints.append(sp_val)
                    else:
                        break 
                    k = k + 1

                col = 1
                for key in  my_repository.custom_setpoints:
                    value = base_test.read_cell(col, 5, i)
                    print(key)
                    print(value)
                    my_repository.etu_dictionary[key][0] = value
                    col = col + 1
                    
            else:
                sp = base_test.read_string_from_cell(1, 1, i)
                #print(str(sp))
                keys = my_repository.mapping_dictionary[sp][0]

                col = 1
                for key in keys:
                    value = base_test.read_cell(col, 5, i)
                    my_repository.etu_dictionary[key][0] = value 
                    col = col + 1
            i = i+1

                

        
    def get_new_vars(self, config_file, active_row):

        col = 6
        new_vars = []
        rating = config_file.read_cell(4, active_row, 0)
        frame  = config_file.read_cell(3, active_row, 0)

        while True:
            k = config_file.read_string_from_cell(col, active_row, 0)
            if k == None or k == "" or k == "None":
                break
            
            new_vars.append(k)
            col = col + 1

        return new_vars, frame, rating

    def set_new_vars(self, new_vars, my_repository, rating):

        sets = int(len(new_vars)/4)

        for k in range(0, sets):
           key = new_vars[(k*4)]
           my_repository.etu_dictionary[key][0] = new_vars[(k*4)+2]


        my_repository.etu_dictionary["Rating"][0] = rating
        
    def calc_number_of_runs(self, config_file, new_test_file, row):

        
        max_runs = 0
        while True:
            check = new_test_file.read_cell(1, max_runs+5, 1)
            if check == None:
                break 
            max_runs = max_runs + 1

        config_runs = int(config_file.read_cell(5, row, 0))
        print("RUNS")
        print(config_runs)
        #config_runs = int(round(config_runs,0))
        #config_runs = int(round(max_runs,0))
        
        print(config_runs)
        print(max_runs)

        if config_runs > max_runs:
            max_runs = config_runs 

        return max_runs 



    def write_new_settings(self, max_runs, new_vars, new_test_file, my_repository, frame, rating):

        j = 0
        ex_runs = my_repository.expected_runs

        #Read Tab Loop
        num_tabs = len(new_test_file.sheet_array)

        if int(ex_runs) == -1: #only Change Rating on Main Tab
            print("Only Main Tab Change")
            new_test_file.write_cell(3, 4, 0, frame)
            new_test_file.write_cell(3, 5, 0, rating)

            new_test_file.save_file()

            return
        
        if int(ex_runs) == 1 or int(ex_runs) == 0: #Pickup Tests Just Need The Rating Changed

            print("PICKUP OBVIOUSLY")
            new_test_file.write_cell(3, 4, 0, frame)
            new_test_file.write_cell(3, 5, 0, rating)
            my_repository.old_rating = int(my_repository.old_rating)
            my_repository.etu_dictionary["Rating"][0] = int(my_repository.etu_dictionary["Rating"][0])

            print(my_repository.etu_dictionary["Rating"][0])
            print(my_repository.old_rating)
            for run in range(0, max_runs):

                write_val = new_test_file.read_cell(2, run+5, 1)
                print(write_val)
                amps = write_val * my_repository.etu_dictionary["Rating"][0] / my_repository.old_rating
                new_test_file.write_cell(2, run+5, 1, amps)

                write_val = new_test_file.read_cell(3, run+5, 1)
                amps = write_val * my_repository.etu_dictionary["Rating"][0] / my_repository.old_rating
                new_test_file.write_cell(3, run+5, 1, amps)

                write_val = new_test_file.read_cell(4, run+5, 1)
                amps = write_val * my_repository.etu_dictionary["Rating"][0] / my_repository.old_rating
                new_test_file.write_cell(4, run+5, 1, amps)

            for k in range (0, num_tabs):
                sp = new_test_file.read_string_from_cell(1, 1, k)
                if sp == "Setpoint 0" or sp == "Setpoint 1":

                    for run in range(0, max_runs):

                        value_present = new_test_file.read_cell(3, run+5, k)
                        if value_present != "" and value_present != None: 
                            new_test_file.write_cell(1, run+5, k,  my_repository.etu_dictionary["Rating"][0])
                        else:
                            break
                            
                
            new_test_file.save_file()
            
            return

        


        for k in range(0, num_tabs): #Runs through each tab
            if k == 0: #Skips First Tab Since There's No Setpoints
                new_test_file.write_cell(3, 4, k, frame)
                new_test_file.write_cell(3, 5, k, rating)
            else:
                sp = new_test_file.read_string_from_cell(1, 1, k)
                if sp == "Custom":
                    keys = my_repository.custom_setpoints
                else: 
                    keys = my_repository.mapping_dictionary[sp][0]

                for run in range(0, max_runs+1): 
                    col = 1


                    for key in keys:
                        if key in new_vars:
                            key_num = new_vars.index(key)
                            max_val = float(new_vars[key_num+1])
                            interval = float(new_vars[key_num+3])
                            
                            if run == 0:
                                write_val = float(my_repository.etu_dictionary[key][0])
                            else:
                                write_val = float(my_repository.etu_dictionary[key][0]) + interval 

                            if write_val > max_val:
                                write_val = max_val

                            my_repository.etu_dictionary[key][0] = write_val


                            if frame == "PD2" or frame == "PD3A" or frame == "PD3B" or frame == "PD4" or frame == "PD5" or frame == "PD6":

                                print("MCCB")
                                if int(my_repository.etu_dictionary["LD PU"][0]) == 0:
                                    my_repository.etu_dictionary["LD PU"][0] = my_repository.etu_dictionary["Rating"][0]
                                else: 
                                    my_repository.etu_dictionary["LD PU"][0] = int(my_repository.etu_dictionary["LD PU"][0])
                                    
                                if key == "I A (PU)":
                                    amps = write_val * my_repository.etu_dictionary["LD PU"][0]
                                    new_test_file.write_cell(2, run+5, k, amps)
                                elif key == "I B (PU)":
                                    amps = write_val * my_repository.etu_dictionary["LD PU"][0]
                                    new_test_file.write_cell(3, run+5, k, amps)
                                elif key =="I C (PU)":
                                    amps = write_val * my_repository.etu_dictionary["LD PU"][0]
                                    new_test_file.write_cell(4, run+5, k, amps)
                            else:
                                rating = int(my_repository.etu_dictionary["Rating"][0])
                                LDPU = int(my_repository.etu_dictionary["LD PU"][0])/100

                                if LDPU == 0:
                                    LDPU = 1
                                    
                                if key == "I A (PU)":
                                    amps = write_val * LDPU * rating
                                    new_test_file.write_cell(2, run+5, k, amps)
                                elif key == "I B (PU)":
                                    amps = write_val * LDPU * rating
                                    new_test_file.write_cell(3, run+5, k, amps)
                                elif key =="I C (PU)":
                                    amps = write_val * LDPU * rating
                                    new_test_file.write_cell(4, run+5, k, amps)

                                
                        new_test_file.write_cell(col, run+5, k, my_repository.etu_dictionary[key][0])
                        col = col + 1
                    

                k = k + 1
        
        new_test_file.save_file()    


    def rename_file(self, base_test_name, base_test, new_vars, frame, rating):

        str_tag = " " + str(frame) + " " + str(rating) + " " 
        
        num_runs = int(len(new_vars)/4)

        for i in range(0, num_runs):

            var_name = new_vars[i*4]
            max_val = new_vars[(i*4)+1]
            min_val = new_vars[(i*4)+2]

            if max_val == min_val:
                file_name_val = str(max_val)
            else:
                file_name_val = str(max_val) + "-" + str(min_val)

            if i == 0:
                str_tag = str_tag + "__" + str(var_name) + "=" + file_name_val
            else: 
                str_tag = str_tag + "__" + str(var_name) + "=" + file_name_val 
            

        

        base_test_name = base_test_name.replace(".xlsx","")
        base_test_name = base_test_name + str_tag + ".xlsx"

        base_test.name_file(base_test_name)
            
    def start(self, my_repository):

        open_file_name = self.open_file
        config_file = GT_Excel_Interface.Test_File("Read", open_file_name)
        save_file_dir = self.sav_start_dir
        
        active_row = 4

        while True :
            base_test_name = config_file.read_string_from_cell(1, active_row, 0)
            
            if base_test_name == "" or base_test_name == None or base_test_name == "None":
                break

            new_test_name =  save_file_dir + "\\" + base_test_name            
            base_test_name = "Z:\\Arisumi\\Programs\\General Test 3.7\\Tests\\Default Tests\\Generic\\" + base_test_name
            
            print(base_test_name)

            new_test_file = GT_Excel_Interface.Test_File("Modify", base_test_name)
            
            self.setup_repos(config_file, active_row, my_repository)
            
            self.get_default_vals(new_test_file, my_repository)
            new_vars, frame, rating  = self.get_new_vars(config_file, active_row)
            self.set_new_vars(new_vars, my_repository, rating)
            max_runs                 = self.calc_number_of_runs(config_file, new_test_file, active_row)

            self.rename_file(new_test_name, new_test_file, new_vars, frame, rating)
            self.write_new_settings(max_runs, new_vars, new_test_file, my_repository, frame, rating)

            for key in my_repository.custom_setpoints:
                my_repository.custom_setpoints.pop(0)
        
            active_row = active_row + 1
    

        

def main_with_ui():

    my_repository = Repository

    root = Tk()    
    My_UI(my_repository, root)

    root.mainloop()
    
main_with_ui()

