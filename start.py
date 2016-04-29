from time import sleep
import subprocess as sub
updis = ['pip','install','--upgrade','discord.py']
de = ['sudo','rm','nohup.out']
update = ['sudo','git','pull']
bot = ['sudo','nohup','python3.5','bot.py']
dp = sub.Popen(updis)
dp.wait()
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
