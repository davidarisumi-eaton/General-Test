
import time

def power_cycle(omicron, usb):

        time.sleep(1)

        if omicron.in_use == False and usb.connected_bs == False:
                return

        disconnected = False

        print("BS")
        print(usb.connected_bs)
        if omicron.in_use == True:         
            omicron.aux_off()
        if usb.connected_bs == True:
            usb.turn_off_port()
            disconnected = True
            print("Powering Down")

        print(omicron.in_use)
        time.sleep(10)

        if omicron.in_use == True:
            omicron.aux_on()
        if usb.connected_bs == True:
            usb.turn_on_port()
            
            
        time.sleep(1)


        fail_count = 0
        while disconnected:
            print("Disconnected and Reconnecting")
            time.sleep(2)
            disconnected = usb.open_port()
            
            if disconnected:
                print("Still Disconnected")
                fail_count = fail_count + 1

                usb.turn_off_port()
                time.sleep(5)
                usb.turn_on_port()
                
                if fail_count > 5:
                    break
        
        
        time.sleep(1)


def all_off(omicron, usb):

        if omicron.in_use == False and usb.connected_bs == False:
                return

        disconnected = False

        print("BS")
        print(usb.connected_bs)
        if omicron.in_use == True:         
            omicron.aux_off()
        if usb.connected_bs == True:
            usb.turn_off_port()
            disconnected = True
            print("Powering Down")



def all_on(omicron, usb):

        disconnected = True
        
        if omicron.in_use == True:
            omicron.aux_on()
        if usb.connected_bs == True:
            usb.turn_on_port()
            
            
        time.sleep(5)


        fail_count = 0
        while disconnected:
            print("Disconnected and Reconnecting") 
            disconnected = usb.open_port()
            
            if disconnected:
                fail_count = fail_count + 1
                
                if fail_count > 5:
                    break


def omicron_off(omicron):
        if omicron.in_use == False and usb.connected_bs == False:
                return

        if omicron.in_use == True:         
            omicron.aux_off()



def omicron_on(omicron):
        if omicron.in_use == True:
            omicron.aux_on()


def usb_off(usb):

        if usb.connected_bs == True:
            usb.turn_off_port()
            disconnected = True
            print("Powering Down")
            
def usb_on(usb):


        disconnected = True
        if usb.connected_bs == True:
            usb.turn_on_port()
            
            
        time.sleep(5)


        fail_count = 0
        while disconnected:
            print("Disconnected and Reconnecting") 
            disconnected = usb.open_port()
            
            if disconnected:
                fail_count = fail_count + 1
                
                if fail_count > 5:
                    break
                
