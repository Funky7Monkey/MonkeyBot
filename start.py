from time import sleep
import subprocess as sub
p = sub.Popen(['sudo','python3.5','bot.py'],stdout=sub.PIPE,stderr=sub.PIPE)
while True:
	if p.returncode == None:
		out, error = p.communicate()
		print(out)
		print(error)
	elif p.returncode != None:
		print('TEST2')
		p = sub.Popen(['sudo','python3.5','bot.py'],stdout=sub.PIPE,stderr=sub.PIPE)