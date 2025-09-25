import GT_Omicron
import time

def power_cycle():

        time.sleep(1)
        omicron = GT_Omicron.Omicron()
        
        msg = omicron.connect_omicron()           #  sets up Omicron Engine.app along with Omicron Amplifiers

        while True:
                time.sleep(5)
                print("On")
                omicron.aux_on()
                time.sleep(5)
                print("Off")
                omicron.aux_off()
        
                

power_cycle()
