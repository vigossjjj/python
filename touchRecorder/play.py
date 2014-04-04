import time
import subprocess
def readEventFromFile(fileName):
  eventDic = {}
  index = 0
  fd = open(fileName, "r")
  for line in fd.readlines():
    event = line.split()
    index += 1
    eventDic[index] = event
  return eventDic

def calculateInterval(eventDic):
  lastTimeStamp = float(eventDic[1][0])
  for x, y in eventDic.items():
    currentTimeStamp = float(y[0])
    y[0] = currentTimeStamp - lastTimeStamp
    lastTimeStamp = currentTimeStamp

def main():
  eventDic = readEventFromFile("tmp")
  calculateInterval(eventDic)
  print eventDic
  for x, y in eventDic.items():
    cmd = "adb shell sendevent /dev/input/event1 %s, %s, %s" % (int(y[1], 16), int(y[2], 16), int(y[3], 16))
    print cmd
    subprocess.Popen(cmd, shell = True)
    if y[0] != 0.0:
      print "goint to sleep %f" % y[0]
      time.sleep(y[0])
    else:
      time.sleep(0.005)
  
if __name__ == '__main__':
  main()
    