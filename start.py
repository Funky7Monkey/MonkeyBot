from time import sleep
import subprocess as sub
p = sub.Popen('sudo','python3.5','bot.py',stdout=sub.PIPE,stderr=sub.PIPE)
while True:
	if p.poll == False:
		print('TEST')
	if p.poll == True:
		print('TEST2')
		p = os.popen('sudo python3.5 bot.py',"r")
	sleep(1)