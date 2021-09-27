import os
import winreg
def software_disable(value):
    # print(value)
    keyval = "SOFTWARE\Classes\.exe"

    registrykey = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Classes",0,winreg.KEY_WRITE)
   
    if value == True:       
        winreg.SetValue(registrykey,".exe",winreg.REG_SZ,"exefile_1")      
        print("usb disabled")
           
    elif value == False:
        winreg.SetValue(registrykey,".exe",winreg.REG_SZ,"exefile") 
        print("softwareinstall enabled")
    else:
        print("op cancelled")
        winreg.CloseKey(registrykey)
    return True

def block_soft():
    software_disable(True)

def unblock_soft():
    software_disable(False)
