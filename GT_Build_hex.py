import subprocess

def main():

    iar_dir = "\"C:\\Program Files (x86)\\IAR Systems\\Embedded Workbench 8.4_3\\common\\bin\""
    ewp = "\C:\\bamboo-files\\ACB-PXR-35-MainMicro-master (1)\\ACB-PXR-35-MainMicro-master\\PXR35_ProtProc.ewp\""
    #ewp = "\C:\\Users\\E0422169\\UsersE0422169DocumentsRepo_Test\\ACB-PXR-35-MainMicro-master\\ACB-PXR-35-MainMicro-master\\PXR35_ProtProc.ewp\""
    create_hex(iar_dir, ewp)

def create_hex(iar_dir, ewp):
    
    output = subprocess.run(iar_dir + "\iarbuild " + ewp + " -build Debug -log all", shell = True)
    print(output)


main()
