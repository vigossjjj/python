import subprocess
import threading


class GetThread(threading.Thread):
  Finish = False
  eventsDic = {}
  count = 0
  def run(self):
    handle = subprocess.Popen('adb shell getevent -t /dev/input/event1', stdout = subprocess.PIPE, shell = True)
    while self.Finish != True:
      self.count += 1
      eventsStr = handle.stdout.readline().split()
      self.eventsDic[self.count] = eventsStr
  def finish(self):
    self.Finish = True
  def getOutput(self):
    return self.eventsDic

def proceedRedundant(eventDic):
  out = {}
  index = 0
  lastTimeStamp = 0
  for x, y in eventDic.items():
    event = []
    event.append(y[1][:-1])
    event.append(y[2])
    event.append(y[3])
    event.append(y[4])
    index += 1
    out[index] = event
  return out

def writeEventToFile(eventDic, fileName):
  fd = open(fileName, "w")
  for x, y in eventDic.items():
    for item in y:
      fd.write(item)
      fd.write(" ")
    fd.write('\n')
  fd.flush()
  fd.close()
def main():
  t = GetThread()  
  t.setDaemon(True)
  Flag = True
  while Flag == True:
    arg = str(raw_input("Please enter command: "))
    if arg == 's':
      t.start()
    elif arg == 'f':
      t.finish()
      Flag = False
    else:
      print "wrong arg"
  eventDic = proceedRedundant(t.getOutput())
  writeEventToFile(eventDic, "tmp")

if __name__ == '__main__':
  main()
  