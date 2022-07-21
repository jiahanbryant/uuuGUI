import subprocess
import os, sys
import platform

# From StackOverFlow
# https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def usb_check():
    uuu_WIN = resource_path("tools\win")
    uuu_MAC = resource_path("tools/mac")
    uuu_LINUX = resource_path("tools/linux")
    try:
        print("Checking for USB devices...")
        running_OS = platform.system()
        print("Now in " + running_OS)
        if running_OS == "Windows":
            os.chdir(uuu_WIN)
            command = subprocess.run(["uuu.exe", "-lsusb"], stdout=subprocess.PIPE, universal_newlines=True)
            print(command.stdout)
            if "MX8MM" in command.stdout:
                print("MX8MM SoC found.")
            else:
                print("No USB device found!")
            return True
        elif running_OS == "macOS" or running_OS=="Darwin":
            os.chdir(uuu_MAC)
            command = subprocess.run(["./uuu", "-lsusb"], stdout=subprocess.PIPE, universal_newlines=True)
            print(command.stdout)
            return True
        elif running_OS == "Linux":
            os.chdir(uuu_LINUX)
            command = subprocess.run(["./uuu", "-lsusb"], stdout=subprocess.PIPE, universal_newlines=True)
            print(command.stdout)
            return True
        else:
            print("Error: Not supported OS")
            return False
        
    except subprocess.SubprocessError:
        print("Error in running uuu tool.")
        return False

def main() -> None:

    usb_check()
    input("\nFor staying only. press ENTER to close.\n")

if __name__ == "__main__":
    main()
    