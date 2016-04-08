from time import sleep
import subprocess as sub
update = ['sudo','git','pull']
bot = ['sudo','python3.5','bot.py']
up = sub.Popen(update)
up.wait()
p = sub.Popen(bot,universal_newlines=True)
while True:
	try:
		p.wait()
		p = sub.Popen(bot,universal_newlines=True)
	except KeyboardInterrupt:
		pass