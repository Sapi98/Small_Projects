import os
import subprocess

class MACChanger:
    def __init__(self):
        self.cmd = None
        self.device = None
        self.new_mac = None
        self.old_mac = None
        self.pswd = None

    def process_exec(self, cmd, console_print=False, return_report=False):
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
            if device in exp:
                index = i+1
                break
        
        if index == -1:
            return False
        else:
            return True
    
    def check_mac(self):
        l = len(self.new_mac)
        if l != 6:
            return False
        else:
            for i in self.new_mac:
                if len(i) != 2:
                    return False
        return True
    
    def main(self):
        pass

cmd = ["ip", "link", "show"]

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
out, err = proc.communicate()
print(out)
out = out.splitlines()

device = input("Enter the name of the device (eg eth0) : ")
new_mac = input("Enter the New MAC that you want to set (in form xx:xx:xx:xx:xx:xx): ").strip().split(':')

old_mac = None

if index == -1:
    print("The device you have entered does not exists")
else:
    #Find out the old MAC Address and save it into disk for retrieval
    cmd = ['ip', 'link', 'set', 'dev'] + [device] + ['down']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = proc.communicate()
    if err != None:
        print(err)
    else:
        cmd = ['ip', 'link', 'set', 'dev'] + [device] + ['address'] + [':'.join(new_mac)]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = proc.communicate()