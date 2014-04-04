import subprocess
import threading


class GetThread(threading.Thread):
	Finish = False
	eventsDic = {}
	count = 0
	def run(self):
		handle = subprocess.Popen('adb shell getevent /dev/input/event1', stdout = subprocess.PIPE, shell = True)
		while self.Finish != True:
			self.count += 1
			eventsStr = handle.stdout.readline().split()
			self.eventsDic[self.count] = eventsStr
	def finish(self):
		self.Finish = True
	def getOutput(self):
		return self.eventsDic

Flag = True
t = GetThread()
t.setDaemon(True)
while Flag == True:
	arg = str(raw_input("Please enter command: "))
	print arg
	if arg == 's':
		t.start()
	elif arg == 'f':
		t.finish()
		Flag = False
	else:
		print "wrong arg"
fp = open('tmp', 'w')
res = t.getOutput()
for x, y in res.items():
	print x, y
	fp.write(y[0])
	fp.write(' ')
	fp.write(y[1])
	fp.write(' ')
	fp.write(y[2])
	fp.write('\n')
fp.flush()
fp.close()
