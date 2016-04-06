from time import sleep
import os
p = False
while True:
	while p == False:
		p = os.popen('sudo python3.5 bot.py',"r")
	while p != False:
		line = p.readline()
		if not line: break
		print(line)
	sleep(10)