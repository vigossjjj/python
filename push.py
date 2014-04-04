#!/usr/bin/env python
import os
import sys
import time
import stat
import subprocess
from argparse import ArgumentParser

FORE_RED = 31
FORE_GREEN = 32
FORE_YELLOW = 33

p = ArgumentParser(usage='push -t n -r [True, False] -d [True, False]', description='Author wxl')
p.add_argument('-t', default=300, type=int, dest='time', help='the time that files are modified within')
p.add_argument('-r', default=1, type=int, choices=[0, 1], dest='reboot', help='reboot the phone')
p.add_argument('-d', default=0, type=int, dest='debug', help='enable debug flag')

args = p.parse_known_args(sys.argv)

debug = args[0].debug 
reboot = args[0].reboot
duration = args[0].time


pushList = []
scanList = ["/system/app", "/system/framework", "/system/bin", "/system/lib", "/system/priv-app", "/system/containers", "/data/app"]
def colorPrint(msg, color):
	fore = 37
	if (color == "red"):
		fore = FORE_RED
	elif (color == "green"):
		fore = FORE_GREEN
	elif (color == "yellow"):
		fore = FORE_YELLOW
	else:
		print "Don't supprrot %s, use white as default" % color				
	type = "\x1B[%d;%dm" % (0, fore)
	orig = "\x1B[0m"
	print "%s%s%s" % (type, msg, orig)
def searchFile(path=None):
	if not path:
		print "path is empty"
		return
	if debug == 1:
		print path
	if os.path.isdir(path):
		folderList = os.listdir(path)
		for x in folderList:
			if debug == 1:
				print x
			searchFile(path + "/" + x)
	elif os.path.isfile(path):
		delta = time.time() - os.stat(path)[stat.ST_MTIME]
		if debug == 1:
			print delta
		if delta < duration:
			if debug == 1:
				print path
			pushList.append(path)
def pushToRight(dst):
	for i in range(len(pushList)):
		colorPrint ("pushing " + pushList[i] + " to " + dst, "green")
		subprocess.call("adb push " + pushList[i] + " " + dst, shell=True)
	pushList[:] = []
def findPrj(prj):
	if "ljp" in os.getcwd():
		return "ljp/kk"
	else:
		return prj
def main():
	if "Workspace" in os.getcwd():
		target_product = os.environ.get("TARGET_PRODUCT")
		if target_product != None:
			if debug == 1:
				print target_product
			index = os.getcwd().split("/").index("Workspace")
			workspace = "/".join(os.getcwd().split("/")[:index + 1])
			if debug == 1:
				print workspace
			prj = os.getcwd().split("/")[index + 1: index + 2][0]
			prj = findPrj(prj)
			if debug == 1:
				print prj
			out = workspace + "/" + prj+ "/out/target/product/" + target_product
			if debug == 1:
				print out
			res = subprocess.call("adb remount", shell=True)
			if res != 0:
				print "Please check your connection"
			else:
				for i in range(len(scanList)):
					searchFile(out + scanList[i])
					pushToRight(scanList[i])
				if reboot == 1:
					print "reboot phone"
					subprocess.call("adb reboot", shell=True)
		else:
			print "No product specified"
	else:
		print "It won't work out of Workspace"
if __name__ == '__main__':
	main()
