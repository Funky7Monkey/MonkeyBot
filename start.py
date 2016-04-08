from time import sleep
import subprocess as sub
update = ['sudo','nohup','git','pull']
bot = ['sudo','nohup','python3.5','bot.py']
up = sub.Popen(update)
up.wait()
p = sub.Popen(bot,universal_newlines=True)
while True:
	try:
		p.wait()
		p = sub.Popen(bot,universal_newlines=True)
	except KeyboardInterrupt:
		pass