from time import sleep
import subprocess as sub
update = ['sudo','git','pull']
bot = ['sudo','python3.5','bot.py']
up = sub.Popen(update,stdout=sub.PIPE,stderr=sub.PIPE)
up.wait()
p = sub.Popen(bot,stdout=sub.PIPE,stderr=sub.PIPE,universal_newlines=True)
while True:
	if p.returncode == None:
		print(p.stdout.readline())
	elif p.returncode != None:
		p = sub.Popen(bot,stdout=sub.PIPE,stderr=sub.PIPE)