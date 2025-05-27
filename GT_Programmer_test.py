'''
Read Me

You need PYOCD installed. https://pypi.org/project/pyocd/

To program stm32h743xx you will need to download an expanded micro
list. 
use the command line command {pyocd pack -f stm32h743xx} to install them
'''



import pyocd
from pyocd.core.helpers import ConnectHelper
from pyocd.flash.file_programmer import FileProgrammer


'''
chip int 0=Dislpay 1=Protection
file = str hex_file name and locatoin. ex. "C\\documents\\example.hex"
'''
def main(chip, file):

    #PXR35 Protection Processor "stm32f407igtx"
    #PXR35 Display Processor "stm32h743xx"
    if chip == 0:
        target = "stm32h743xx"
    else:
        target = "stm32f407igtx"
        
    result = program(target, file)
    result = str(result)


    if result == "All Good":
        print("Finished Programming." )
    elif result== "Memory transfer fault (STLink error (21): DP fault)":
        print("Wrong Target. Your probably trying to program the protection micro with display code or vise versa.")
    elif result == "STLink error (9): Get IDCODE error":
        print("Looks like you're not connected to the board. Check your connection or board power")
    else:
        print("You did something wrong. Not sure what, but you're wrong and bad and you should feel bad.")

def program(target, file):
    try: 
        with ConnectHelper.session_with_chosen_probe(options = {"frequency": 4000000, "target_override": target}) as session:

            board = session.board
            target = board.target
            flash = target.memory_map.get_boot_memory()
            print(board)
            print(target)
            print(flash)

            FileProgrammer(session).program(file)

            
    except Exception as problem:
        return problem

    return "All Good"




