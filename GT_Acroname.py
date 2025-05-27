import brainstem
from brainstem.result import Result
import math
import time

class BrainstemObject:
    def __init__(self):
        self.stem   = None
        self.result = None
        #self.TextDisplay = TextDisplay

    def CheckPort(self, port):
        powerResult = self.stem.usb.getPortState(port)      

        success = True
        if powerResult.error == Result.NO_ERROR:
            if powerResult.value == 0:
                on = False
            else:
                on = True
        else:
            success = False
            on = False


        return success, on

    def PowerOnPort(self, portID):
        powerResult = self.stem.usb.setPortEnable(portID)
        if powerResult == Result.NO_ERROR:
            success = True
        else:
            success = False

        return success

    def PowerOffPort(self, portID):
        powerResult = self.stem.usb.setPortDisable(portID)
        if powerResult == Result.NO_ERROR:
            success = True
        else:
            success = False

        return success

    def Connect(self):
        self.stem = brainstem.stem.USBHub3p()
        self.result = self.stem.discoverAndConnect(brainstem.link.Spec.USB)

        if self.result == Result.NO_ERROR:
            success = True
            #connectionSuccesful.set()
            print('Connection Succesful')
        else:
            #connectionSuccesful.clear()
            print('Connection Failed')
            success = False

        return success

    def Disconnect(self):
        self.stem.disconnect()
        #connectionSuccesful.clear()

        self.stem   = None
        self.result = None

        return True

def main():
        bs =BrainstemObject
        bs.Connect(bs)

main()
