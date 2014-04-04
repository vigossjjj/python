import os
import subprocess
import platform

version = platform.python_version()[0]
fp = open('dumpInfo', 'w')
handle = subprocess.Popen('adb shell pm list package', stdout = subprocess.PIPE, shell = True)
packageList = handle.stdout.read().split()
for i in range(len(packageList)):
  packageList[i] = packageList[i][8:]
  
for i in range(len(packageList)):
  cmd = 'adb shell pm dump %s' % packageList[i]
  handle = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell = True)
  if version == '2':
    print '%d / %d' % (i, len(packageList))
  elif version == '3':
    print (i, "/", len(packageList))
  fp.write(handle.stdout.read())
print "done"
fp.close()
