from time import sleep
import subprocess as sub
de = ['sudo','rm','nohup.out']
update = ['sudo','git','pull']
bot = ['sudo','nohup','python3.5','bot.py']
de = sub.Popen(de)
de.wait()
up = sub.Popen(update)
up.wait()
p = sub.Popen(bot,universal_newlines=True)
while True:
	try:
		p.wait()
		p = sub.Popen(bot,universal_newlines=True)
	except KeyboardInterrupt:
		pass
