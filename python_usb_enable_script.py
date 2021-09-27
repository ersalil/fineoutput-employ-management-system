
import os
import winreg

def usbenordis(value):
    # print(value)
    
    keyval = r"SYSTEM\CurrentControlSet\Services\UsbStor"
    if not os.path.exists(keyval):
        # print("creating key")
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, keyval)
    registrykey= winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\UsbStor", 0, winreg.KEY_SET_VALUE)
    # print("open key")
    if value == True:
        winreg.SetValueEx(registrykey,"start",0,winreg.REG_DWORD,4)
        print("usb disabled")
    elif value == False:
        winreg.SetValueEx(registrykey,"start",0,winreg.REG_DWORD,3)
        print("usb enabled")
    else:
        print("op cancelled")
        winreg.CloseKey(registrykey)
    return True

def block_usb():
    usbenordis(True)

def unblock_usb():
    usbenordis(False)
