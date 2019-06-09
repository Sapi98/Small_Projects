import os
import subprocess

#pwd = input("Enter the password : ")
#new_mac = input("Enter the New MAC that you want to set : ").strip().split(':')

proc = subprocess.Popen(["ip", "link", "show"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
out, err = proc.communicate()
out = out.splitlines()
print(proc.pid)
for i in out:
    print()
    print(i)
    print()
