from time import sleep
import subprocess as sub
bot = ['sudo','python3.5','bot.py']
update = ['sudo','git','clone','https://github.com/Funky7Monkey/MonkeyBot',
	'&&','sudo','cp','~/Discord/MonkeyBot/*.*','~/Discord',
	'&&','sudo','rm','-r','MonkeyBot']
update = sub.Popen(update,stdout=sub.PIPE,stderr=sub.PIPE)
out, error = update.communicate()
print(out)
print(error)
p = sub.Popen(bot,stdout=sub.PIPE,stderr=sub.PIPE)
while True:
	if p.returncode == None:
		out, error = p.communicate()
		print(out)
		print(error)
	elif p.returncode != None:
		p = sub.Popen(bot,stdout=sub.PIPE,stderr=sub.PIPE)