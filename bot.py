import random
import discord
from settings import token,botname,owner
import datetime
import json
import logging
import subprocess
import types
import importlib
import commands

available = {}
for command in dir(commands):
	if not command.startswith('_'):
		available[getattr(commands, command).__name__] = getattr(commands, command)

log = logging.getLogger('discord')
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
log.addHandler(handler)

client = discord.Client()
discord.Server.comm = {}
discord.Server.allowed = {}
discord.Server.__slots__.append('comm')
discord.Server.__slots__.append('allowed')

class builtin():
	"""Built-in commands"""
	async def help(client, message, *arg):
		"""Displays Help dialog"""
		send = 'List of commands:'
		for name, command in message.server.comm.items():
			send += '\n\n`{1}' + name + '` - ' + command.__doc__
		await client.send_message(message.channel, send.format(botname, message.server.allowed['prefix']))
		
	async def restart(client, message, *arg):
		"""Restarts {0}"""
		comm = {}
		for server in client.servers:
			comm[server.id] = list(server.comm.keys())
		with open('comm.json', 'w') as c:
			json.dump(comm, c)
		allowed = {}
		for server in client.servers:
			allowed[server.id] = server.allowed
		with open('allowed.json', 'w') as c:
			json.dump(allowed, c)
		await client.close()

	async def update(client, message, *arg):
		"""Updates {0}"""
		if int(message.author.id) in owner or message.author.id == client.user.id:
			update = ['sudo','git','pull']
			up = subprocess.Popen(update,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
			out, err = up.communicate()
			up.wait()
			await client.send_message(message.channel, 'Update succeeded!')
			for o in owners:
				await client.send_message(o, 'Output:\n'+out+'\n'+err)

	async def playing(client, message, *arg):
		"""Sets {0}\'s status"""
		if not arg[0]:
			await client.change_status(game = discord.Game(name = None))
			print(str(datetime.datetime.now()) + ': ' + message.author.name + ' set status to None')
		else:
			await client.change_status(game = discord.Game(name = arg[0]))
			print(str(datetime.datetime.now()) + ': ' + message.author.name + ' set status to {}'.format(arg[0]))

	async def allow(client, message, *arg):
		"""Allows {0} to run in a channel\nUsable by server owner"""
		if int(message.author.id) in owner or message.server.owner == message.author:
			if not arg[0]:
				message.server.allowed[message.channel.id] = message.channel.id
				await client.send_message(message.channel, '{0} will now run in {1}.'.format(botname, message.channel.mention))
			else:
				for server in client.servers:
					if message.server.get_channel(arg[0]) != None:
						channel = message.server.get_channel(arg[0])
				message.server.allowed[channel.id] = channel.id
				await client.send_message(message.channel, '{0} will now run in {1}.'.format(botname, channel.mention))

	async def disallow(client, message, *arg):
		"""Disallows {0} to run in a channel\nUsable by server owner"""
		if int(message.author.id) in owner or message.server.owner == message.author:
			if not arg[0]:
				del message.server.allowed[message.channel.id]
				await client.send_message(message.channel, '{0} will no longer run in {1}.'.format(botname, message.channel.mention))
			else:
				for server in client.servers:
					if message.server.get_channel(arg[0]) != None:
						channel = message.server.get_channel(arg[0])
				del message.server.allowed[channel.id]
				await client.send_message(message.channel, '{0} will no longer run in {1}.'.format(botname, channel.mention))

	async def module(client, message, *arg):
		"""Works with commands"""
		if int(message.author.id) in owner or message.author.id == client.user.id:
			if not arg[0]:
				imported = ''
				for name, command in message.server.comm.items():
					imported += '\n**' + name + '** - ' + command.__doc__
				av = ''
				for name, command in available.items():
					av += '\n**' + name + '** - ' + command.__doc__
				await client.send_message(message.channel, '__**Imported Commands:**__' + imported.format(botname) + '\n\n__**Available Commands:**__' + av.format(botname))
			elif arg[0].startswith('import'):
				args = arg[0].split(' ')
				if args[1].lower() in message.server.comm:
					await client.send_message(message.channel, 'The command `' + args[1].lower() + '` has already been imported.')
				elif args[1].lower() in available:
					message.server.comm[args[1].lower()] = available[args[1].lower()]
					await client.send_message(message.channel, 'Imported:\n**' + args[1].lower() + '** - ' + message.server.comm[args[1].lower()].__doc__)
				else:
					await client.send_message(message.channel, 'The command `' + args[1].lower() + '` is not available.')
			elif arg[0].startswith('export'):
				args = arg[0].split(' ')
				if args[1].lower() in message.server.comm and args[1].lower() in available:
					del message.server.comm[args[1].lower()]
					await client.send_message(message.channel, 'Removed:\n**' + args[1].lower() + '** - ' + available[args[1].lower()].__doc__)
			elif arg[0].startswith('reload'):
				importlib.reload(commands)
				available.clear()
				for command in dir(commands):
					if not command.startswith('_'):
						available[getattr(commands, command).__name__] = getattr(commands, command)

@client.event
async def on_ready():
	await client.edit_profile(username = botname)
	print(str(datetime.datetime.now()) + '\nLogged in as ' + client.user.name + '\nUser ID: ' + client.user.id + '\n------')
	global owners
	owners = []
	for member in client.get_all_members():
		if int(member.id) in owner and member not in owners:
			owners.append(member)
	with open('comm.json', 'r') as c:
		comm = json.loads(c.read())
	with open('allowed.json', 'r') as c:
		al = json.loads(c.read())
	for server in client.servers:
		for i in al[server.id]:
			server.allowed[i] = al[server.id][i]
		for command in dir(builtin):
			if not command.startswith('_'):
				server.comm[getattr(builtin, command).__name__] = getattr(builtin, command)
		for name in comm[server.id]:
			if not name in server.comm:
				server.comm[name] = available[name]

@client.event
async def on_message(message):
	if message.author == client.user or not message.content.startswith(message.server.allowed['prefix']):
		return
	if len(message.server.allowed) > 1 and message.channel.id not in message.server.allowed:
		return
	try:
		try:
			command, arg = message.content.split(' ', maxsplit = 1)
			command = command.lower()[1:]
		except(ValueError):
			command = message.content[1:]
			arg = None
		print(str(datetime.datetime.now()) + ': Received command: "{}" with argument(s): "{}" from "{}"'.format(command, arg, message.author.name))
		log.info('Received command: "{}" with argument(s): "{}" from "{}"'.format(command, arg, message.author.name))

		if command in message.server.comm:
			await message.server.comm[command](client, message, arg)
		else:
			print('Command not found')

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
except Exception as e:
	comm = {}
	for server in client.servers:
		comm[server.id] = list(server.comm.keys())
	with open('comm.json', 'w') as c:
		json.dump(comm, c)
	allowed = {}
	for server in client.servers:
		allowed[server.id] = server.allowed
	with open('allowed.json', 'w') as c:
		json.dump(allowed, c)
