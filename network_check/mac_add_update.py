#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2022 gq <gq@gqhp>
#
# Distributed under terms of the MIT license.

"""
Try to update the destination mac address remotely

"""

import os
import sys
sys.path.append('../')
from python_udp_recv.params import dst_mac

# mac for receiving output1 and output2
new_rec_mac = [dst_mac[0], dst_mac[2]]

ssh_cmd = "sshpass -p root ssh  -oHostKeyAlgorithms\=\+ssh-rsa root\@192.168.1.188"


def update_mac(new_mac, pn):
# pn is 0 or 1

    i = pn
    mac_sendin = "0x" + new_mac.replace(":", "")[4:]
    cmd = ssh_cmd +  " \"sed -i '/\\s port" + str(i) \
        + "_dst_mac0/c\\    port" + str(i) + "_dst_mac0=" + mac_sendin \
                + "' py2drv.py\""

    errors= os.system(cmd)
    if errors:
        print("Updating Mac Address: " + new_rec_mac[0] + " part1: " +
                mac_sendin + " failed\n")
        print("Errors: ", errors)
        update_ok = False
    else:
        print(new_rec_mac[0] + " part1: " + mac_sendin +
                " was sucessfully Updated\n")

def update_all_macs():
    update_ok = True
    for i, new_mac in enumerate(new_rec_mac):

        # update dest_mac0
        mac_sendin = "0x" + new_mac.replace(":", "")[4:]
        cmd = ssh_cmd + " \"sed -i '/\\s port" + str(i) \
            + "_dst_mac0/c\\    port" + str(i) + "_dst_mac0=" + mac_sendin \
                    + "' py2drv.py\""


        errors= os.system(cmd)
        if errors:
            print("Updating Mac Address: " + new_rec_mac[0] + " part1: " +
                    mac_sendin + " failed\n")
            print("Errors: ", errors)
            update_ok = False
        else:
            print(new_rec_mac[0] + " part1: " + mac_sendin +
                    " was sucessfully Updated\n")

        # update dest_mac0
        mac_sendin = "0x" + new_mac.replace(":", "")[0:4]
        cmd = ssh_cmd + " \"sed -i '/\\s port" + str(i) \
            + "_dst_mac1/c\\    port" + str(i) + "_dst_mac1=" + mac_sendin \
                    + "' py2drv.py\""
        errors= os.system(cmd)

        if errors:
            print("Updating Mac Address part2 : " + new_rec_mac[0] +  " part1: " +
                   mac_sendin +  " failed\n")
            print("Errors: ", errors)
            update_ok = False
        else:
            print(new_rec_mac[0] + " part2: " + mac_sendin +
                    " was sucessfully Updated\n")

    if update_ok:
        print("Restat Receiver, pleaset wait for a few secs.......")
        cmd = ssh_cmd + " \" python zrf8_init.py\""
        errors= os.system(cmd)
        if errors:
            print("Restart Receiver failed....")
            print("Errors: ", errors)
        else:
            print("Restart Restart sucessfully....")

    else:
        print("Update failed....please check and try again. Exited with failure...")

if __name__ == "__main__":
    update_all_macs()
