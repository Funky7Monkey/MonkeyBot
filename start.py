from time import sleep
import subprocess as sub
updiscord = ["sudo","pip","install","--upgrade","git+https://github.com/Rapptz/discord.py@async"]
update = ['sudo','git','pull']
bot = ['sudo','nohup','python3.5','bot.py']
up = sub.Popen(updiscord)
up.wait()
up = sub.Popen(update)
up.wait()
p = sub.Popen(bot,universal_newlines=True)
while True:
	try:
		p.wait()
		p = sub.Popen(bot,universal_newlines=True)
	except KeyboardInterrupt:
		pass
