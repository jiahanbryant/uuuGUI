import subprocess
import os
import platform

def usb_check():
    try:
        print("Checking for USB devices...")
        running_OS = platform.system()
        if running_OS == "Windows":
            os.chdir(os.getcwd() + r"\tools\win")
            print("Current working directory is " + os.getcwd())
            command = subprocess.run(["uuu.exe", "-lsusb"], universal_newlines=True)
            print(command.stdout)
            return True
        elif running_OS == "macOS":
            os.chdir(os.getcwd() + "/tools/mac")
            print("Current working directory is " + os.getcwd())
            command = subprocess.run(["uuu", "-lsusb"], universal_newlines=True)
            print(command.stdout)
            return True
        elif running_OS == "Linux":
            os.chdir(os.getcwd() + "/tools/linux")
            print("Current working directory is " + os.getcwd())
            command = subprocess.run(["uuu", "-lsusb"], universal_newlines=True)
            print(command.stdout)
            return True
        else:
            print("Error: Not supported OS")
        
    except subprocess.SubprocessError:
        print("Error in running uuu tool.")
        return False

def main() -> None:

    usb_check()

if __name__ == "__main__":
    main()
    