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

    def __init__(self, root):

        self.my_tk = root
        
        self.my_tk.title('Test UI')
        self.my_tk.resizable(width = FALSE, height = FALSE)
        self.my_tk.geometry('{}x{}'.format(350, 200))

        self.main_frame = Frame(self.my_tk, bg='grey93', width = 350, height = 200).grid(row = 0, rowspan = 20, column = 0, columnspan = 20)
        
        self.tab_screen = ttk.Notebook(self.main_frame,width = 250, height = 150)
        self.tab_screen.grid(row = 2, rowspan = 17, column = 3, columnspan = 17)
        
        self.tab_zero   = ttk.Frame(self.tab_screen)
        
        self.tab_screen.add(self.tab_zero,  text = "Test")

        self.check_start_dir = os.getcwd()

        Label(self.tab_zero, text = "File and Directory Options").grid(row = 1, column = 5, columnspan = 2)

        self.save_dir_button = Button(self.tab_zero, text = "Pick Check Directory", command = lambda: self.check_dir())
        self.save_dir_button.grid(row = 3, column = 5, columnspan = 2)
        
        self.check_dir_entry = Entry(self.tab_zero, width = 40)
        self.check_dir_entry.grid(row = 4, column = 5, columnspan = 2)
        check_file_path = os.getcwd()
        self.check_dir_entry.insert(0,check_file_path)
        blank = "Nothing, just nothing"
        
        self.start_button = Button(self.tab_zero, text = "Start", command = lambda: self.start(blank))
        self.start_button.grid(row = 11, column = 5, columnspan = 2)
        

    def check_dir(self):

        check_file_path = filedialog.askdirectory(parent=self.my_tk, initialdir= self.check_start_dir, title='Please select a directory')

        #print path
        if check_file_path != "":
            self.check_dir_entry.delete(0, END)
            self.check_dir_entry.insert(0,check_file_path)
            self.check_start_dir = check_file_path
            print(self.check_start_dir)

   
    def check_results(self, base_test, file_name):

        col = 1
        row = 5
        print("===============================================================")
        while True: 
            sp = base_test.read_string_from_cell(col, row, 0)
##            print(sp)
##            print("Col = " + str(col))
##            print("Row = " + str(row))
            
            if col == 1:
                col = col + 1
                if sp == "" or sp == None or sp == "None":
                    print("No Problems Found")
                    print(file_name)
                    return 0 
                elif sp == "Fail" or sp == "No Test":
                    print(sp)
                    print(file_name)
            else: 
                if sp == "" or sp == None or sp == "None":
                    row = row + 1
                    col = 1
                elif sp == "Fail" or sp == "No Test":
                    col = col + 1
                    print(sp)
                    print(file_name)
                    break
                else:
                    col = col + 1

        return 1

            

                    


                
            
    def start(self, blank):

        file_path = self.check_dir_entry.get()

        test_group = []
        name_group = []
        for root, dirs, files, in os.walk(file_path, topdown = True):
            for name in files:
                test_group.append(file_path + '/' + str(os.path.join(name)))
                name_group.append(name)

        for name in name_group:
            print(name)

        i = 0
        fail_count = 0
        for check_file_name in test_group:

            config_file = GT_Excel_Interface.Test_File("Read", check_file_name)
            
            f = self.check_results(config_file, name_group[i])
            fail_count = fail_count + f
            i = i + 1

        print("FAIL COUNT " + str(fail_count))



        

        

def main_with_ui():

    root = Tk()    
    My_UI(root)

    root.mainloop()
    
main_with_ui()

