'''---------------------------------------------------------------------
    
    Company:    EATON COROPORATION
            
                Proprietary Information
                (C) Copyright 2016
                All rights reserved
                
                PXR MCCB Automation - Protection  
    
-------------------------------------------------------------------------------
    
    Authors:    David Arisumi                (412) 893-3213
                Eaton Corporation
                1000 Cherrington Parkway
                Moon Twp, PA 15108-4312
                (412) 893-3300
                
-------------------------------------------------------------------------------
    
    Product:    Automated test system to test the PXR10, PXR20, PXR2D, PXR25, 
                and PXR35 protection algorithms for the SR, NZM, and NRX 
                breaker frames.   
                
    Module:     USB_commands.py
                
    Mechanics:  
                
    Reference: 
----------------------------------------------------------------------------'''

from __future__ import division
from struct import *
import  serial, time, serial.tools.list_ports, math
from GT import GT_USB_Commands
from GT import GT_Acroname
import traceback


class USB_Communication(object):
    
    def __init__(self):

        self.password= ''
        self.ser = serial.Serial()
        self.portname = ''
        self.connected_bs = False
        self.commands = GT_USB_Commands.usb_commands()
        self.commands.populate_commands()
        self.repos = None



    '''
    =======================================================================================================================
    Setup Methods For USB

    open_port():
    Function:
        Opens the port to allow usb communication. The port that is chosen is self.portname, so portname must be set before
        running this function. 
    Input:
        None
    Output:
        None
    Changes:
        self.ser(serial object) - This is the object that will communicate with the trip unit. 

    get_open_ports():
    Input:
        None
    Output:
        list_ports(string array) - the list of all the portnames that the computer currently sees.
    Changes:
        Nothing
        
    inital_port():
    Function:
        Automatically looks through the list of ports for a name with the name Eaton. 
    Input:
        None
    Output:
        None
    Changes:
        self.portname(string) - portname becomes whatever the eaton portname was
    ========================================================================================================================
    '''
    def set_portname(self, name):
        self.portname = name
        
    def open_port(self):    
        disconnected = True
        fail_count = 0
        while disconnected:
            try:
                self.ser = serial.Serial(     
                    port = self.portname, 
                    baudrate = 9600,
                    bytesize = serial.EIGHTBITS,
                    parity = serial.PARITY_NONE,
                    stopbits = serial.STOPBITS_ONE,
                    timeout = 100)
                break
            except Exception as err:
                self.ser.close()

                if self.connected_bs == True: #If brainstem connected, tries a powercyle
                    self.bs.PowerOffPort(0)
                    time.sleep(2)
                    self.bs.PowerOnPort(0)
                    time.sleep(2)
                    
                fail_count = fail_count + 1
                if fail_count > 5:
                    break

        if fail_count < 5:
            disconnected = False
            
        return disconnected
     
    def get_open_ports(self):

        list_ports = []
        for val in serial.tools.list_ports.comports():

            final_name = ''
            full_name = str(val)
        
            for char in full_name:
                if char == ' ':
                    break
                else:
                    final_name = final_name + char
                    
            list_ports.append(final_name)
            
        return list_ports



    
    def initial_port(self):
        eaton_found = False
        for val in serial.tools.list_ports.comports():
            name = str(val)
            print(name)
            if name.find("Eaton") != -1:
                eaton_found = True
                break

        if eaton_found == False:
            for val in serial.tools.list_ports.comports():
                name = str(val)
                print(name)
                if name.find("USB") != -1:
                    eaton_found = True
                    break          
            
        self.portname = ''
        for char in name:
            if char == ' ':
                break
            else:
                self.portname = self.portname + char
                
    '''
    ============================================================================================================================
    Setup Methods For Brainstem
    ==========================================================================================================================
    '''
    
    def connect_brain_stem(self):

        
        self.bs = GT_Acroname.BrainstemObject()
        result = self.bs.Connect()
        
        if result == True:
            self.connected_bs = True
            msg = "Successful connection to the brainstem"
        else:
            msg = "Something went wrong connecting the brainstem"

        return msg



          
    def disconnct_brain_stem(self):

        result = self.bs.Disconnect()
        if result == True:
            msg = "successful Disconnect."
        else:
            msg = ("Well something went wrong disconnecting the brainstem.")

        return msg

    


    '''
    ========================================================================================
    Set globals
    ==========================================================================================
    '''

    def set_repository(self, repos):
        self.repos = repos

    def set_command_list(self, family):
        self.commands.set_family(family)

    '''
    ===========================================================================================
    Commands 
    ===========================================================================================
    '''
    
    def turn_off_port(self):
        self.bs.PowerOffPort(0)
        self.bs.PowerOffPort(1)
        self.bs.PowerOffPort(2)
        self.bs.PowerOffPort(3)

        
        
    def turn_on_port(self):
        self.bs.PowerOnPort(0)
        self.bs.PowerOnPort(1)
        self.bs.PowerOnPort(2)
        self.bs.PowerOnPort(3)

        
    def close_port(self):
        self.ser.close()
        

    '''
    ===========================================================================================
    Helper Methods

    busy_check(self, tx, command, msg)
    Function:
        Some messages take a while to process. This methods checks to see if the trip unit sends a busy command back to the program. If a busy
        response is recieved, it will try to send the same command back to the trip unit. This will repeat until a non-busy response is given. 
    input:
        tx(string) - the byte message to be set to the trip unit
        command(string) - the string name of the message being sent
        msg(string) - the byte message recieved from the the trip unit
    output:
        cor(string) - the correctness message. 
        
    ===========================================================================================
    '''

    def busy_check(self, tx, command, msg):

        not_finished = True
        while not_finished:
            time.sleep(.4)
            
            cor = self.get_correctness(msg)
            
            if cor == "busy": #If the correctness is busy, we send another command until it responds with not busy.
                pass
            else:
                if self.repos != None:
                    self.repos.append_usb_msg(command, str(tx), str(msg))
                return cor
                
            if self.repos != None:
                self.repos.append_usb_msg(command, str(tx), str(msg))
            else:
                print(command)
                print(tx)
                print(str(msg))

            msg = self.usb_transaction(tx) #Sends usb message(tx)

            
            
    

    '''
    ===========================================================================================
    Communication

    def communicate(self, command, *argv)
    Function:
        Takes the users command, put it into bytes and send it to the trip unit. It the returns
        the trip units resposne.
    Input:
        command(string) - message to be sent to the trip unit.
        *argv(??????) - data that needs to be appended to the usb message
    Output:
        msg(string) - the usb message in bytes that the trip unit sends back
    Changes:
        Nothing 

    def communicate(self, command, *argv)
    Function:
        Takes the users command, put it into bytes and send it to the trip unit. When it recieves the message
        it interperts the correctness byte and returns it to the user. 
    Input:
        command(string) - message to be sent to the trip unit.
        *argv(??????) - data that needs to be appended to the usb message
    Output:
        corr(string) - the message of the correctness byte. 
    Changes:
        Nothing

    def communicate_manual(self, tx, tag)
    Function:
        Sends a byte message provided by the user. Returns the trip units byte response.

    Input:
        tx(string) - byte message to be sent to the trip unit.
    Output:
         msg(string) - the usb message in bytes that the trip unit sends back
    Changes:
        Nothing
    
    ===========================================================================================
    '''
    
            
    def communicate(self, command, *argv):

        tx, packet = self.commands.get_message(command, *argv) #Gets the message in bytes and as an index

        if tx == False: #If no valid message was found, quits out of the method
            return False
        
        time.sleep(.01)

        try:
            msg = self.usb_transaction(tx) #Sends usb message(tx)
        except Exception as err:
            traceback.print_exc()
            x = input('Press Enter to Continue...')
            cleanup(repos, usb, omicron)
            quit()

        
            

        if self.repos != None:
            self.repos.append_usb_msg(command, str(packet), str(msg))
        else:
            print(command)
            print(tx)
            print(str(msg))            
          
        return msg

    def communicate_with_check(self, command, *argv):

        tx, packet = self.commands.get_message(command, *argv) #Gets the message in bytes and as an index
        print(tx)
        print(packet)
        if tx == False: #If no valid message was found, quits out of the method
            return False
        
        time.sleep(.05)
        
        try:
            msg = self.usb_transaction(tx) #Sends usb message(tx)
        except Exception as err:
            traceback.print_exc()
            x = input('Press Enter to Continue...')
            cleanup(repos, usb, omicron)
            quit()

        
            

        if self.repos != None:
            self.repos.append_usb_msg(command, str(packet), str(msg))
        else:
            print(command)
            print(tx)
            print(str(msg))



        cor = self.busy_check(tx, command, msg)
            
          
        return cor
    

    def communicate_manual(self, tx, tag):
        msg = self.usb_transaction(tx)


        tx = "" 
        for b in tx:
            temp = str(hex(b))
            print(b)
            val = temp.replace("0x","")
            if len(val) == 1:
                val = "0" + val
            
            tx = tx + val + " "

        print(tx)
        if self.repos != None:
            self.repos.append_usb_msg(tag, str(tx), str(msg))
            
        return msg

    def send_recieve(self, tx):
        msg = self.usb_transaction(tx)
        return msg

    '''
    ===========================================================================================
    Communication

    def usb_transaction(self, tx)
    Function:
        Sends the usb message to the trip unit and then recieves the trip units reponse. 
    Input:
        tx(string) - byte message to be sent to the trip unit.
    Output:
       msg(string) - the usb message in bytes that the trip unit sends back 
    Changes:
        Nothing


    
    ===========================================================================================
    '''
    
    def usb_transaction_simple(self, tx):

        fail_count = 0
        
        #This part sends the actual message to the unit
        is_valid = False
        while is_valid == False: 
            try:
                self.ser.write(tx)  #Sends the command
            except:
                print("write error 1")
                self.ser.close()

            ack = self.read_specific() #Reads the response message

            is_valid = self.check_if_valid(ack)

            if is_valid == False:
                fail_count = fail_count + 1
                print(fail_count)
                if fail_count > 15:
                    return "USB error"
        

        if ack == "NULL":
            ack = "USB error"
        else:
            ack = self.normalize_buffer_read(ack, (len(ack)*3)+1)
            
            self.ser.flushOutput()
            self.ser.flushInput()



        return ack



    def usb_transaction(self, tx):

        self.ser.flushInput()
        self.ser.flushOutput()
        
        #This part sends the actual message to the unit
        is_valid = False
        fail_count = 0
        while is_valid == False:
            if fail_count == 0 or fail_count > 5: 
                try:
                    good_write = True
                    self.ser.write(tx)  #Sends the command
                    time.sleep(.1)
                except:
                    print("write error " + str(fail_count))
                    print(tx)
                    if self.repos != None:
                        self.repos.mark_usb_error()
                    good_write = False
                    self.ser.close()
                    time.sleep(5)
                    self.open_port()
                    
                    

                #self.ser.flushInput()
                #self.ser.flushOutput()

            fail_count = fail_count + 1
            if fail_count > 15:
                break

            if good_write:            
                ack = self.read_specific() #Reads the response message
                is_valid = self.check_if_valid(ack)

        if ack == "NULL":
            ack = "USB error"
        else:
            ack = self.normalize_buffer_read(ack, len(ack)+1)


        time.sleep(.05)    
        self.ser.flushOutput()
        self.ser.flushInput()
            
        return ack


    def read_specific(self):

        ack = ' '
         
        while self.ser.in_waiting:
            inp = ''
            try:
                inp = self.ser.read(size=1) #read one byte
            except:
                print("read error")
                if self.repos != None:
                    self.repos.mark_usb_error()
                
                

            if len(inp) == 0:
                print("No message recived")
                break
                
            
            check = inp.hex() #gives the correct bytes, each on a newline
            ack = ack + ' ' + check
             

        return ack
    
    '''
    ===========================================================================================
    Quality Of Life Methods
    ===========================================================================================
    '''
    
    def check_if_valid(self, pass_ack):

        is_valid = True

        if pass_ack == "NULL" or len(pass_ack) < 10:   #If no message is recieved it will try to send the command one more time.

            is_valid = False
            
            #self.ser.close()
            time.sleep(1)
            #self.open_port()
            
        return is_valid

    

    def normalize_buffer_read(self, msg, num):

        'normalize message - lower case + delete free space'
    
        msg = msg.lower()   # lower case
    
        i = 0                           
        while i < len(msg): 
            if msg[i] == '8':
                break
            else: 
                i += 1   


        msg = msg[i:num]
   
        return msg


 

    def get_correctness(self, msg):
        correctness = self.commands.get_correctness(msg)

        if self.repos != None:
            self.repos.append_debug_msg(correctness)
            
        return correctness

