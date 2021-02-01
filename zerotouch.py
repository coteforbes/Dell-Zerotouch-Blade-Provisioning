#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import subprocess
import sys
import time
import io  
import re
import os

# create parser
parser = argparse.ArgumentParser()
 
# add arguments to the parser
parser.add_argument("cmc_ip")

# parse the arguments
args = parser.parse_args()
cmc_ip=str(sys.argv[1])
lockfile=str(cmc_ip) + ".cmc"
idrac_username = "root"

idrac_off = []
idrac_ips = []


def check_running_status():
    while os.path.isfile(lockfile):
        print("Script already in progress, waiting...")
        time.sleep(600)
    else:
        print ("Lockfile does not exist, creating...")
        open(lockfile,"w+")
        print("Starting script")


def get_slots_with_no_idrac():
    for i in range(1, 17):
        server= "server-"+str(i)
        print(server)
        output= subprocess.run(["/opt/dell/srvadmin/sbin/racadm", "-r", cmc_ip, "-u", "root", "-p", "calvin", "--nocertwarn", "getniccfg", "-m", server], stdout=subprocess.PIPE).stdout.decode('utf-8')
        if "0.0.0.0" in output:
            idrac_off.append(server)
    print(idrac_off)
    if len(idrac_off) == 0:
        print("No new blades, exiting...")
        os.remove(lockfile)
        quit()
    subprocess.run(["/opt/dell/srvadmin/sbin/racadm", "-r", cmc_ip, "-u", "root", "-p", "calvin", "--nocertwarn", "deploy", "-a", "-d"], stdout=subprocess.PIPE).stdout.decode('utf-8')
    time.sleep(300)


def zerotouch(idrac_off):
    for blade in idrac_off:
        output= subprocess.Popen(["/opt/dell/srvadmin/sbin/racadm", "-r", cmc_ip, "-u", "root", "-p", "calvin", "--nocertwarn", "getniccfg", "-m", blade], stdout=subprocess.PIPE)
        for line in io.TextIOWrapper(output.stdout, encoding="utf-8"):
            if "IP Address" in line:
                find_ip(line)
    for ip in idrac_ips: # These will be new blades so using default credentials
        subprocess.run(["/opt/dell/srvadmin/sbin/racadm", "-r", ip, "-u", "root", "-p", "calvin", "--nocertwarn", "set", "iDRAC.NIC.Autoconfig", "1"], stdout=subprocess.PIPE).stdout.decode('utf-8')
        

def find_ip(str):
    pattern = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    test = pattern.search(str)
    ip= test.group()
    idrac_ips.append(ip)


if __name__ == "__main__":
    time.sleep(1800)
    check_running_status()
    get_slots_with_no_idrac()
    zerotouch(idrac_off)
    os.remove(lockfile)
else:
    print("FAIL")
