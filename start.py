from time import sleep
import os
p = os.popen('sudo python3.5 bot.py',"r")
while True:
	if p.poll == False:
		print('TEST')
		line = p.readline()
		if not line: break
		print(line)
	if p.poll == True:
		print('TEST2')
		p = os.popen('sudo python3.5 bot.py',"r")
	sleep(1)