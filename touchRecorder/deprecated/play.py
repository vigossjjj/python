import subprocess
import time

INTERVAL_BETWEEN_EVENTS = 0.007
INTERVAL_BETWEEN_ACTIONS = 0.5

def parseFileToEvent(name):
	fp = open(name, 'r')
	eventDic = {}
	index = 0
	for line in fp.readlines():
		index += 1
		eventDic[index] = line.split()
	return eventDic
def splitEventToAction(eventDic):
	start = 0
	end = 0
	TRACKING_ID = int("39", 16)
	FLAG_END = int("ffffffff", 16)
	GET_A_PAIR = False
	actionDir = {}
	index = 0
	for x, y in eventDic.items():	
		if int(y[1], 16) == TRACKING_ID and int(y[2], 16) != FLAG_END:
			start = x
		if int(y[1], 16) == TRACKING_ID and int(y[2], 16) == FLAG_END:
			end = x + 1
			GET_A_PAIR = True		
		if GET_A_PAIR == True:
			GET_A_PAIR = False
			index += 1
			actionDir[index] = [start, end]
	actionDic = {}
	index = 0
	for x, y in actionDir.items():
		index += 1
		action = {}
		subIndex = 0
		for x in range(y[0], y[1] + 1):
			subIndex += 1
			action[subIndex] = eventDic[x]
		print action
		actionDic[index] = action
	return actionDic
		

def playAction(actionDic):
	for x, y in actionDic.items():
		for m, n in y.items():
			cmd = "adb shell sendevent /dev/input/event1 %s %s %s" % (int(n[0], 16), int(n[1], 16), int(n[2], 16))
			subprocess.Popen(cmd, shell = True)
			time.sleep(INTERVAL_BETWEEN_EVENTS)
		time.sleep(INTERVAL_BETWEEN_ACTIONS)

def main():
	eventDic = parseFileToEvent("tmp")
	actionDic = splitEventToAction(eventDic)
	playAction(actionDic)

if __name__ == '__main__':
	main()
