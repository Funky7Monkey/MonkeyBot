from time import sleep
import subprocess as sub
bot = ['sudo','python3.5','bot.py']
update = ['sudo','git','clone','https://github.com/Funky7Monkey/MonkeyBot']
copy = ['sudo','cp','~/Discord/MonkeyBot/*.*','~/Discord']
remove = ['sudo','rm','-r','MonkeyBot']
up = sub.Popen(update,stdout=sub.PIPE,stderr=sub.PIPE)
while up.returncode == None:
	pass
sub.Popen(copy)
sub.Popen(remove)
p = sub.Popen(bot,stdout=sub.PIPE,stderr=sub.PIPE)
while True:
	if p.returncode == None:
		out, error = p.communicate()
		print(out)
		print(error)
	elif p.returncode != None:
		p = sub.Popen(bot,stdout=sub.PIPE,stderr=sub.PIPE)