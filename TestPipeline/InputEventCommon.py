'''
Created on May 20, 2014

@author: wxl
'''
import subprocess
import re

def getTouchNode():
    devices_info_cmd = "adb shell cat /proc/bus/input/devices"
    p = subprocess.Popen(devices_info_cmd, shell = True, stdout = subprocess.PIPE)
    devices_info_list = p.stdout.readlines()
    '''
    something like this
    I: Bus=0018 Vendor=0000 Product=0000 Version=0000
    N: Name="r69001-touchscreen"
    P: Phys=
    S: Sysfs=/devices/pci0000:00/0000:00:09.2/i2c-7/7-0055/input/input0
    U: Uniq=

    B: PROP=0
    B: EV=9
    B: ABS=6608000 0
    '''
    index_offset_from_name_to_handlers = 4
    handler_info_position = 0

    for item in devices_info_list:
        if "touch" in item:
            index = devices_info_list.index(item)
            handler_info_position = index + index_offset_from_name_to_handlers
            break

    '''
    parse the below string to get the event0
    H: Handlers=event0
    '''
    if handler_info_position != 0:
        handler_info = devices_info_list[handler_info_position]
        touch_event_position = re.findall('event\d', handler_info)
        touch_postion = "/dev/input/%s" % touch_event_position[0]
        return touch_postion
    else:
        print "Error: counldn't find touch pos!"
        return None






