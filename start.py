from time import sleep
import os
p = False
while True:
	p = os.popen('sudo python3.5 bot.py',"r")
	while 1:
		line = p.readline()
		if not line: break
		print(line)
	sleep(10)