import subprocess
import os, sys
import platform
from time import sleep

# From StackOverFlow, mainly for Windows
# https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    global base_path
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# To extract device info from output of usb_check
# currently only support one usb device at a time
def retrieveDEVICE(): 
    suportList = ["MX8MM", "MX8MN"]
    usbDevice = usb_check()
    if usbDevice != "False":
        for device in suportList:
            if device in usbDevice:
                print(device + " is found.")
                return True
    else:
        print("Error: no usb device found.")
        return False

def usb_check():
    uuu_WIN = resource_path("tools\win")
    uuu_MAC = resource_path("tools/mac")
    uuu_LINUX = resource_path("tools/linux")
    try:
        print("Checking for USB devices...")
        if running_OS == "Windows":
            os.chdir(uuu_WIN)
            command = subprocess.run(["uuu.exe", "-lsusb"], stdout=subprocess.PIPE, universal_newlines=True)
            #print(command.stdout)
            os.chdir(base_path)
            return command.stdout
        elif running_OS == "macOS" or running_OS=="Darwin":
            os.chdir(uuu_MAC)
            command = subprocess.run(["./uuu", "-lsusb"], stdout=subprocess.PIPE, universal_newlines=True)
            print(command.stdout)
            os.chdir(base_path)
            return command.stdout
        elif running_OS == "Linux":
            os.chdir(uuu_LINUX)
            command = subprocess.run(["./uuu", "-lsusb"], stdout=subprocess.PIPE, universal_newlines=True)
            #print(command.stdout)
            os.chdir(base_path)
            return command.stdout
        else:
            print("Error: Not supported OS")
            return False
        
    except subprocess.SubprocessError:
        print("Error in running uuu tool.")
        return False

def main() -> None:

    global running_OS
    timeout = 0
    running_OS = platform.system()
    print("Now in " + running_OS)

    while True:
        if retrieveDEVICE():
            print("now start to program...")
            timeout = 0
            break
        elif timeout <= 9:
            sleep(1)
            timeout += 1
            continue
        else:
            print("Error: waiting for usb timeout !")
            break
    input("\nPress ENTER to close this window.\n")

if __name__ == "__main__":
    main()
    