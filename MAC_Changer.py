import os
import subprocess

cmd = ["ip", "link", "show"]

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
out, err = proc.communicate()
print(out)
out = out.splitlines()

device = input("Enter the name of the device (eg eth0) : ")
new_mac = input("Enter the New MAC that you want to set (in form xx:xx:xx:xx:xx:xx): ").strip().split(':')
l = len(new_mac)
old_mac = None

if l != 6:
    print("Enter a valid MAC Address")
else:
    for i in new_mac:
        if len(i) != 2:
            print("Enter a valid MAC Address")
            break

index = -1
for i in range(len(out)):
    exp = out[i]
    if device in exp:
        index = i+1
        break

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