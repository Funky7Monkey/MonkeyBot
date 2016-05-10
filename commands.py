async def slap(client, message, *arg):
	"""Slaps mentioned or random member(s)"""
	import random
	import datetime
	global sl
	try:
		if int((datetime.datetime.now() - sl).total_seconds()) < 2:
			return
	except NameError:
		pass
	randmem = list(message.server.members)[(random.randrange(0, len(message.server.members)))]
	send = message.author.mention + ' slapped '
	if not arg:
		send = send + randmem.name
	elif '@everyone' in arg or '@here' in arg:
		send = message.author.mention + ", you can't slap *everyone,* dumbass"
	elif client.user in message.mentions:
		send = message.author.mention + ", don't you dare slap me"
	elif message.author in message.mentions:
		send = message.author.mention + ", have fun hurting yourself, you dirty masochist"
	elif len(message.mentions) > 0:
		for member in message.mentions:
			send = send + member.mention + ' and '
		send = send[:-5]
	else:
		send = send + randmem.name
	await client.send_message(message.channel, send + '!')
	sl = datetime.datetime.now()
async def milkshake(client, message, *arg):
	"""Milkshake"""
	await client.send_message(message.channel, 'https://www.youtube.com/watch?v=pGL2rytTraA')
async def nickname(client, message, *arg):
	"""Change nickname"""
	if int(message.author.id) in owner or message.author.id == client.user.id:
				if not arg:
					await client.change_nickname(message.server.get_member(client.user.id), None)
				else:
					await client.change_nickname(message.server.get_member(client.user.id), arg)