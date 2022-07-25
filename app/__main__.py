import subprocess
import os, sys
import platform
from time import sleep

# command list
checkForUsb = "check_usb_device"
loadImage = "boot_image"

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

def cmdCheck(cmd):
    uuu_WIN = resource_path(r"tools\win\uuu.exe")
    uuu_MAC = resource_path("tools/mac/uuu")
    uuu_LINUX = resource_path("tools/linux/uuu")
    autoScript_WIN = resource_path(r"tools\images\uuu.auto")
    autoScript_Linux_Mac = resource_path("tools/images/uuu.auto")

    try:
        if running_OS == "Windows":
            if cmd == "check_usb_device":
                print("Checking for USB devices...")
                command = subprocess.run([uuu_WIN, "-lsusb"], stdout=subprocess.PIPE, universal_newlines=True)
            elif cmd == "boot_image":
                print("loading images...")
                command = subprocess.run([uuu_WIN, autoScript_WIN], stdout=subprocess.PIPE, universal_newlines=True)
            #print(command.stdout)
            #os.chdir(base_path)
            return command.stdout
        elif running_OS == "macOS" or running_OS=="Darwin":
            if cmd == "check_usb_device":
                print("Checking for USB devices...")
                command = subprocess.run([uuu_MAC, "-lsusb"], stdout=subprocess.PIPE, universal_newlines=True)
            elif cmd == "boot_image":
                print("loading images...")
                command = subprocess.run(["sudo", uuu_LINUX, autoScript_Linux_Mac], stdout=subprocess.PIPE, universal_newlines=True)
            return command.stdout
        elif running_OS == "Linux":
            if cmd == "check_usb_device":
                print("Checking for USB devices...")
                command = subprocess.run([uuu_LINUX, "-lsusb"], stdout=subprocess.PIPE, universal_newlines=True)
            elif cmd == "boot_image":
                print("loading images...")
                command = subprocess.run(["sudo", uuu_LINUX, autoScript_Linux_Mac], stdout=subprocess.PIPE, universal_newlines=True)
            return command.stdout
        else:
            print("Error: Not supported OS")
            return False
        
    except subprocess.SubprocessError:
        print("Error in running uuu tool.")
        return False

# To extract device info from output of usb_check
# currently only support one usb device at a time
def retrieveDEVICE(): 
    suportList = ["MX8MM", "MX8MN"]
    usbDevice = cmdCheck(checkForUsb)
    if usbDevice != "False":
        for device in suportList:
            if device in usbDevice:
                print(device + " is found.")
                return True
    else:
        print("Error: no usb device found.")
        return False

# To load u-boot and fit to ram of soc via USB
def factory_boot():
    try:
        cmdCheck(loadImage)
    except:
        print("Error: failed to boot image.")

def main() -> None:

    global running_OS
    timeout = 0
    running_OS = platform.system()
    print("Now in " + running_OS)

    while True:
        if retrieveDEVICE():
            factory_boot()
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
    