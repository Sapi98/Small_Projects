import os
import subprocess
import time

class MACChanger:
    def __init__(self):
        self.cmd = ""
        self.device = ""
        self.new_mac = []
        self.old_mac = []
        self.pswd = ""
        self.printChoice()
        self.main()

    def process_exec(self, console_print=False, return_report=False):
        proc = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = proc.communicate()
        out = out.splitlines()

        for i in range(len(out)):
            out[i] = str(out[i])[2:-1]
            if console_print:
                print(out[i])

        if err != None:
            print(err)
        if return_report:
            return out

    def set_command(self, command_string):
        self.cmd = command_string.strip().split()
    
    def check_device(self, out):
        index = -1
        for i in range(len(out)):
            if self.device == out[i][0]:
                index = i+1
                break
        
        if index == -1:
            return (False, -1)
        else:
            i = 3
            self.device = ''
            while out[index-1][i] != ':':
                self.device += out[index-1][i]
                i += 1
            return (True, index)
    
    def check_mac(self):
        l = len(self.new_mac)
        if l != 6:
            return False
        else:
            for i in self.new_mac:
                if len(i) != 2:
                    return False
        return True

    def find_save_mac(self, out, index):
        self.old_mac = out[index].split()[1]
        print("Old MAC : ", self.old_mac)
        print("Please wait while the Old MAC is being saved....")
        save_file = open('old_mac', 'w')
        save_file.write(self.device+'@'+self.old_mac)
        save_file.close()
        time.sleep(3)
        print('Old MAC Id is saved in file : \'', os.path.join(os.getcwd(), 'old_mac'), "\'")
    
    def reset_MAC(self):
        try:
            read_file = open('old_mac', 'r')
            file_content = read_file.read().split('@')
        except FileNotFoundError:
            print('ERROR : The \'old_mac\' file does not exist in this Directory.')
            print('Please make sure that the file and the program is kept in the same Directory')
            return
        
        self.device, self.new_mac = file_content
        
        self.set_command('ip link set dev ' + self.device + ' down')
        self.process_exec()

        self.set_command("ip link set dev " + self.device + " address " + self.new_mac)
        self.process_exec()

        self.set_command('ip link set dev ' + self.device + ' up')
        self.process_exec()

        print("MAC ID SUCCESSFULLY RESET")
        print('Device :', self.device)
        print('MAC ID :', self.new_mac)

    def exit_app(self):
        print('!!!APPLICATION IS CLOSED!!!')
        exit(0)

    def check_MAC(self):
        self.set_command("ip link show")
        out = self.process_exec(console_print=True, return_report=True)
    
    def changeMac_control(self):
        flag = False
        i = None
        out = ""

        while not flag:
            self.new_mac = input("Enter the New MAC that you want to set (in form xx:xx:xx:xx:xx:xx): ").strip().split(':')
            flag = self.check_mac()
            if not flag:
                print("The MAC ID entered is Invalid")
                i = input("Enter Yes/No : ")
                i = i.lower()
                if 'no' or 'n':
                    self.exit_app()

        self.check_MAC()

        flag = False

        while not flag:
            self.device = input("Enter the device index (eg 1): ")
            flag, i = self.check_device(out)
            if not flag:
                print("The Device Name entered is Invalid")
                i = input("Do you want to continue ? Enter Yes/No : ")
                i = i.lower()
                if 'no' or 'n':
                    self.exit_app()
        
        print('====================================')
        print("Your Chosen Device Is :", self.device.upper())
        print('====================================')
        self.find_save_mac(out, i)

        self.set_command('ip link set dev ' + self.device + ' down')
        self.process_exec()

        self.set_command("ip link set dev " + self.device + " address " + ':'.join(self.new_mac))
        self.process_exec()

        self.set_command('ip link set dev ' + self.device + ' up')
        self.process_exec()

        print("MAC ID SUCCESSFULLY CHANGED")
        print('Device :', self.device)
        print('MAC ID :', self.new_mac)

    def printChoice(self):
        print('Enter :')
        print('1 for Changing the MAC Id')
        print('2 for reset the MAC Id')
        print('3 to check the MAC Id')
        print('0 to exit')
    
    def main(self):
        
        while True:
            try:
                choice = int(input('Enter Option : '))
            except ValueError:
                print("Input should be a numeric value ranging from 0-2")
                continue
            if choice == 0:
                self.exit_app()
            elif choice == 1:
                self.changeMac_control()
            elif choice == 2:
                self.reset_MAC()
            else:
                print('Wrong Input')


obj = MACChanger()