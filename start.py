import subprocess as sub
from time import sleep
p = False
while True:
	if p == False:
		p = sub.Popen(['sudo', 'python3.5', 'bot.py'],stdout=sub.PIPE,stderr=sub.PIPE)
	sleep(60)