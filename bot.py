import random
import discord
from settings import token,botname,owner,Allowed_Channels,prefix
import datetime
import json
import logging
import subprocess

log = logging.getLogger('discord')
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
log.addHandler(handler)

client = discord.Client()

@client.event
async def on_ready():
	await client.edit_profile(username = botname)
	print(str(datetime.datetime.now()) + '\nLogged in as ' + client.user.name + '\nUser ID: ' + client.user.id + '\n------')
	global owners
	owners = []
	for member in client.get_all_members():
		if int(member.id) in owner and member not in owners:
			owners.append(member)

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if '(╯°□°）╯︵ ┻━┻' in message.content or '(╯°□°)╯︵ ┻━┻' in message.content:
		n = message.content.count('(╯°□°）╯︵ ┻━┻')
		send = ''
		for i in range(n):
			send += '┬─┬﻿ ノ( ゜-゜ノ)\n'
		await client.send_message(message.channel, send)
	if message.channel.is_private == False:
		if int(message.channel.id) not in Allowed_Channels or not message.content.startswith(prefix):
			return
		message.content = message.content[1:]
		for role in message.author.roles:
			if role.name == 'Bot':
				return
	try:
		print(str(datetime.datetime.now()) + ': received')
		try:
			command, arg = message.content.split(' ', maxsplit = 1)
			command = command.lower()
		except(ValueError):
			command = message.content
			arg = None
		log.info('Received command: "{}" with argument: "{}" from "{}"'.format(command, arg, message.author.name))

		if command == 'help':
			if not arg:
				await client.send_message(message.channel, '__**{0}**__\n`{1}playing` - Set the bot\'s status.\
					\n`{1}slap` - Slap a random person or mentioned person(s).\
					\nWhen calling commands in PM, do not use the prefix `{1}`'.format(botname, prefix))
		elif command == 'restart' or command == 'kill':
			if int(message.author.id) in owner or message.author.id == client.user.id:
				if command == 'kill':
					subprocess.Popen(['sudo','killall','-15','python3.5'])
				await client.close()
		elif command == 'update':
			if int(message.author.id) in owner or message.author.id == client.user.id:
				update = ['sudo','git','pull']
				up = subprocess.Popen(update,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
				out, err = up.communicate()
				up.wait()
				await client.send_message(message.channel, 'Update succeeded!')
				for o in owners:
					await client.send_message(o, 'Output:\n'+out+'\n'+err)
		elif command == 'clean':
			if int(message.author.id) in owner or message.author.id == client.user.id:
				own = []
				for mes in client.messages:
					if mes.author == client.user and mes.channel == message.channel:
						own.append(mes)
				own.reverse()
				for i in range(int(arg)):
					await client.delete_message(own[i])
		elif command == 'add':
			try:
				sub, arg = arg.split(' ', maxsplit = 1)
				sub = sub.lower()
			except(ValueError):
				await client.send_message(message.channel, 'Need Arguments')
			if sub == 'compensation':
				with open('comp.json', 'r') as c:
					comp = json.loads(c.read())
				comp.append(arg)
				with open('comp.json', 'w') as c:
					json.dump(comp, c)
				await client.send_message(message.channel, 'Added `{}`'.format(arg))
		elif command == 'playing':
			if not arg:
				await client.change_status(game = discord.Game(name = None))
				print(str(datetime.datetime.now()) + ': ' + message.author.name + ' set status to None')
			else:
				await client.change_status(game = discord.Game(name = arg))
				print(str(datetime.datetime.now()) + ': ' + message.author.name + ' set status to {}'.format(arg))
		elif command == 'nickname':
			if int(message.author.id) in owner or message.author.id == client.user.id:
				if not arg:
					await client.change_nickname(message.server.get_member(client.user.id), None)
				else:
					await client.change_nickname(message.server.get_member(client.user.id), arg)
		elif command == 'slap':
			global slap
			try:
				if int((datetime.datetime.now() - slap).total_seconds()) < 2:
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
			slap = datetime.datetime.now()
		elif command == 'milkshake':
			await client.send_message(message.channel, 'https://www.youtube.com/watch?v=pGL2rytTraA')
		elif command == 'compensation':
			with open('comp.json', 'r') as c:
				comp = json.loads(c.read())
			await client.send_message(message.channel, random.choice(comp))
		else:
			print(str(datetime.datetime.now()) + ': **Error:** Not a valid command')

	except Exception as e:
		import traceback
		tb = traceback.format_exc()
		await client.send_message(message.channel, 'Something went wrong.')
		for o in owners:
			await client.send_message(o, 'Something went wrong.\n```' + tb + '```')
			print(o, 'Something went wrong.\n' + tb)
		raise

try:
	client.run(token)
except discord.errors.ClientException as e:
	print(str(datetime.datetime.now()) + ': ClientException')
	print(e)
	pass
