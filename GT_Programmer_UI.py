
import tkinter
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as tkst
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import filedialog


import os
import os.path
from os import path

import programmer_test



class My_UI(object):

    def __init__(self, root):

        self.my_tk = root
        
        self.my_tk.title('Programmer UI')
        self.my_tk.resizable(width = FALSE, height = FALSE)
        self.my_tk.geometry('{}x{}'.format(350, 200))

        self.main_frame = Frame(self.my_tk, bg='grey93', width = 350, height = 200).grid(row = 0, rowspan = 20, column = 0, columnspan = 20)
        
        self.tab_screen = ttk.Notebook(self.main_frame,width = 250, height = 150)
        self.tab_screen.grid(row = 2, rowspan = 17, column = 3, columnspan = 17)
        
        self.tab_zero   = ttk.Frame(self.tab_screen)
        
        self.tab_screen.add(self.tab_zero,  text = "Test")

        Label(self.tab_zero, text = "Processer To Program").grid(row = 4, column = 5, columnspan = 2)

        chip_choice_list = ["Display", "Protection"]
        
        self.chip_cbox = ttk.Combobox(self.tab_zero, width = 10, values = chip_choice_list, state = "readonly")
        self.chip_cbox.current(0)
        self.chip_cbox.grid(row = 5, column = 5, columnspan = 2)

        
        self.open_start_dir = os.getcwd()

        Label(self.tab_zero, text = "File and Directory Options").grid(row = 6, column = 5, columnspan = 2)
        
        self.open_file_button = Button(self.tab_zero, text = "Pick Choose File", command = lambda: self.open_file())
        self.open_file_button.grid(row = 7, column = 5, columnspan = 2)

        self.open_file_entry = Entry(self.tab_zero, width = 40)
        self.open_file_entry.grid(row = 9, column = 5, columnspan = 2)
        save_open_file_path = os.getcwd()
        self.open_file_entry.insert(0,self.open_start_dir)

        self.start_button = Button(self.tab_zero, text = "Program", command = lambda: self.start())
        self.start_button.grid(row = 11, column = 5, columnspan = 2)


    def open_file(self):

        start_path = os.getcwd()
        open_file_path = filedialog.askopenfilename(parent=self.my_tk, initialdir= self.open_start_dir, title='Please select a file')
        if open_file_path != "":
            self.open_file_entry.delete(0, END)
            self.open_file_entry.insert(0,open_file_path)
            self.open_file = open_file_path

    def start(self):
        choice = self.chip_cbox.get()

        if choice == "Display":
            chip = 0 
        else:
            chip = 1

        programmer_test.main(chip, self.open_file)

        

      

def main_with_ui():


    root = Tk()    
    My_UI(root)

    root.mainloop()
    
main_with_ui()
