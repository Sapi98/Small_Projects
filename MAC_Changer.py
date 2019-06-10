import os
import subprocess

#pwd = input("Enter the password : ")

proc = subprocess.Popen(["ip", "link", "show"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
out, err = proc.communicate()
print(out)
out = out.splitlines()

device = input("Enter the name of the device (eg eth0) : ")
new_mac = input("Enter the New MAC that you want to set (in form xx:xx:xx:xx:xx:xx): ").strip().split(':')
l = len(new_mac)

if l != 6:
    print("Enter a valid MAC Address")
else:
    for i in new_mac:
        if len(i) != 2:
            print("Enter a valid MAC Address")
            break

flag = False
index = -1
for i in range(len(out)):
    exp = out[i]
    if device in exp:
        index = i+1
        break

if index != -1:
    