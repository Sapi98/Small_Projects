import os
import subprocess

class MACChanger:
    def __init__(self):
        self.cmd = ""
        self.device = ""
        self.new_mac = []
        self.old_mac = []
        self.pswd = ""

    def process_exec(self, console_print=False, return_report=False):
        proc = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = proc.communicate()
        if err != None:
            print(err)
        elif console_print:
            print(out)
            if return_report:
                return out.splitlines()

    def set_command(self, command_string):
        self.cmd = command_string.strip().split()
    
    def check_device(self, out):
        index = -1
        for i in range(len(out)):
            exp = out[i]
            if self.device in exp:
                index = i+1
                break
        
        if index == -1:
            return (False, -1)
        else:
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
        pass

    def exit_app(self):
        print('!!!APPLICATION IS CLOSED!!!')
        exit(0)
    
    def main(self):
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

        flag = False

        self.set_command("ip link show")
        out = self.process_exec(console_print=True, return_report=True)

        while not flag:
            self.device = input("Enter the name of the device (eg eth0) : ")
            flag, i = self.check_device(out)
            if not flag:
                print("The Device Name entered is Invalid")
                i = input("Enter Yes/No : ")
                i = i.lower()
                if 'no' or 'n':
                    self.exit_app()
        
        self.find_save_mac(out, i)

        self.set_command('ip link set dev ' + self.device + ' down')
        self.process_exec()

        self.set_command("ip link set dev " + self.device + " address " + ':'.join(self.new_mac))
        self.process_exec()

        self.set_command('ip link set dev ' + self.device + ' up')
        self.process_exec()

        print("MAC ID SUCCESSFULLY CHANGED")
