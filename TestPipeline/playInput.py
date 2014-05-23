#!/usr/bin/env python
'''
Created on May 20, 2014

@author: wxl
'''

import sys
import time
import os
from InputEventCommon import getTouchNode

EVENT_THRESHOLD = 0.005

def getEventsFromFile(eventFileName):
    eventsList = []
    fp = open(eventFileName, "r")
    for item in fp.readlines():
        eventsList.append(item)
    return eventsList

def pickCoordinates(eventsList):
    '''
    [946697616.529345] 0003 0039 00000028    /start
    [946697616.529345] 0003 0035 0000026b    /X
    [946697616.529345] 0003 0036 0000040c    /Y
    [946697616.529345] 0003 003a 00000025    /pressure
    [946697616.529345] 0000 0000 00000000    /sync
    [946697616.584677] 0003 0039 ffffffff    /end
    [946697616.584677] 0000 0000 00000000    /sync
    '''
    simplifiedEventList =[]
    for i in range(4):
        simplifiedEventList.append(eventsList[i])
    simplifiedEventList.append("0000 0000 00000000")
    simplifiedEventList.append("0003 0039 ffffffff")
    simplifiedEventList.append("0000 0000 00000000")
    return simplifiedEventList

def handleTimeStamp(timeStamp):
    print timeStamp
    dotPos = timeStamp.index(".")
    intigerPart = int(timeStamp[1: dotPos])
    lastDigit = intigerPart % 10
    decimalPart = int(timeStamp[dotPos + 1: -1])
    newTimeStamp = lastDigit * 1000000 + decimalPart
    print newTimeStamp
    return newTimeStamp


def convertList(eventsList):
    '''
    convert something like this
    0003 0039 0000001a
    '''
    intEventList = []
    for item in eventsList:
        tmp = item.split()
        for i in range(len(tmp)):
            tmp[i] = str(int(tmp[i], 16))
        intEventList.append(" ".join(tmp))
    return intEventList

def sendEvent(evnetsList):
    touchPos =  getTouchNode()
    for item in evnetsList:
        cmd = "adb shell sendevent %s %s" % (touchPos, item)
        os.system(cmd)


def playInput(inpuEventFileName):
    hexEventsList = getEventsFromFile(inpuEventFileName)
    simplifiedEventList = pickCoordinates(hexEventsList)
    intEventList = convertList(simplifiedEventList)
    sendEvent(intEventList)

def main():
    if len(sys.argv) == 0:
        return

    inpuEventFileName = sys.argv[1]
    playInput(inpuEventFileName)




if __name__ == "__main__":
    main()