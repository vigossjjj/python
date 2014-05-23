#!/usr/bin/env python
import subprocess
import os
import threading
import re
import time
from playInput import playInput
DBG = False
traceOption = "gfx view wm am input load freq sched res dalvik"
class LogThread(threading.Thread):
    finish = False
    LogList = []
    def run(self):
        self.LogList = []
        os.system("adb logcat -c")
        p = subprocess.Popen("adb logcat -v time", shell = True, stdout = subprocess.PIPE)
        while self.finish != True:
            self.LogList.append(p.stdout.readline())

    def finish(self):
        self.finish = True

    def getLog(self):
        return self.LogList

class EventThread(threading.Thread):
    inputEventFileName = ""
    def run(self):
        time.sleep(1)
        playInput(self.inputEventFileName)

    def setFileName(self, fileName):
        self.inputEventFileName = fileName



def main():
    time = raw_input("time(s): ")
    time = int(time)
    #repeatCount = int(raw_input("repeatTime: "))
    if DBG:
        print ("time: %d" % time)

    mainKey = raw_input("mainKey: ")
    if DBG:
        print ("mainKey: %s" % mainKey)


    tagKey = raw_input("Please enter tag: ")
    inputEventFileName = raw_input("Please enter event file name: ")
    #packageName = raw_input("Please enter packageName: ")



    cmd = raw_input("Press Enter to Start")
    mainKeyIndex = 0
    outputList = ""
    psList = ""
    #while repeatCount > 0:
    while cmd != "f":
        #init output name and cmd
        mainKeyIndex += 1
        HTMLoutputName = "%s%d%s.html" % (mainKey, mainKeyIndex, tagKey)
        LogOutputName = "%s%d%s.log" % (mainKey, mainKeyIndex, tagKey)
        outputList = outputList + " " + HTMLoutputName
        systraceCmd = "systrace.py %s -t %d -o %s" % (traceOption, time, HTMLoutputName)
        #stopCmd = "adb shell am force-stop %s" % packageName

        #start Capture Log and systrace
        event = EventThread()
        event.setFileName(inputEventFileName)
        log = LogThread()
        log.setDaemon(True)
        log.start()
        event.start()
        os.system(systraceCmd)

        #stop capturing log and get ps list
        log.finish()
        pidList = []
        for item in log.getLog():
            pid = getPidFromLog(item)
            if pid != "" and (pid not in pidList) :
                pidList.append(pid)
        psCmd = "adb shell ps | grep -E '%s'"  % ("|".join(pidList))

        psList = subprocess.Popen(psCmd, shell = True, stdout = subprocess.PIPE).stdout.readlines()
        memInfo = subprocess.Popen("adb shell dumpsys meminfo system_server", shell = True, stdout = subprocess.PIPE).stdout.readlines()
        #os.system(stopCmd)

        #write log to file
        logOutput = open(LogOutputName, "w")
        for item in psList:
            logOutput.write(item)
        for item in memInfo:
            logOutput.write(item)
        for item in log.getLog():
            logOutput.write(item)
        logOutput.flush()
        logOutput.close()
        #repeatCount -= 1
        cmd = raw_input("Enter f to stop or any key to continue")
    cmd = "google-chrome %s" % outputList
    subprocess.Popen(cmd, shell = True)



def getPidFromLog(sample):
    res = re.findall('\(\s{0,3}\d*\)', sample)
    if len(res) != 0:
        return str(int(res[0][1:-1]))
    else:
        return ""


if __name__ == '__main__':
    main()





