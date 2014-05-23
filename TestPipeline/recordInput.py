#!/usr/bin/env python
'''
Created on May 20, 2014

@author: wxl
'''
import subprocess
import threading
from InputEventCommon import getTouchNode

class CollectInputEventThread(threading.Thread):
    finish = False
    eventsList = []
    cmd = ""
    def run(self):
        p = subprocess.Popen(self.cmd, shell = True, stdout = subprocess.PIPE)
        while self.finish != True:
            self.eventsList.append(p.stdout.readline())
    def setCmd(self, cmd):
        self.cmd = cmd
    def stop(self):
        self.finish = True
    def getEvent(self):
        return self.eventsList

def generateCmd():
    pos = getTouchNode()
    if pos == None:
        return None
    return ("adb shell getevent %s" % pos)

def main():
    cmd = generateCmd()
    if (cmd == None):
        return
    #init collect thread
    collectThread = CollectInputEventThread()
    collectThread.setDaemon(True)
    collectThread.setCmd(cmd)
    collectThread.start()
    flag = raw_input("Press any key to stop")
    if flag != None:
        collectThread.stop()
    outputName = raw_input("Enter outputName: ")
    fp = open(outputName, "w")
    for item in collectThread.getEvent():
        fp.write(item)
    fp.flush()
    fp.close()
    return


if __name__ == "__main__":
    main()