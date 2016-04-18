import sys
import re
import random
import discord
from settings import email,password,botname,owner,Allowed_Channels,Allowed_Channels_MB,prefix,voice_channel,opusloc
import datetime
import time
import asyncio
import youtube_dl
import functools
import json
import importlib
import logging
import subprocess

log = logging.getLogger('discord')
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
log.addHandler(handler)

client = discord.Client()
loop = asyncio.get_event_loop()
try:
	with open('save.json', 'r') as q:
		queue = json.loads(q.read())
	open('save.json', 'w')
except json.decoder.JSONDecodeError:
	print('Empty JSON')
	queue = []
	pass
print(queue)

class Skip:
	skip = 0
	attemped = []
	current = []

async def music_queue():
	await client.wait_until_ready()
	channel = discord.Object(id=voice_channel)
	global player
	while not client.is_closed:
		try:
			if player.is_done():
				Skip.current = []
			if queue and player.is_done():
				await asyncio.sleep(5)
				log.info('Starting song')
				Skip.current = queue[0]
				song = Skip.current[0]
				url = Skip.current[3]
				title = Skip.current[1]
				t = Skip.current[2]
				queue.pop(0)
				opt = '-async 1'
				player = client.voice.create_ffmpeg_player(url, options=opt)
				await client.send_message(client.get_channel('144963553475035137'), 'Now playing: *"' + title + '"* ' + t)
				player.start()
				Skip.started = datetime.datetime.now()
				Skip.skip = 0
				Skip.attemped = []
		except NameError:
			if queue:
				log.info('Starting song')
				Skip.current = queue[0]
				song = Skip.current[0]
				url = Skip.current[3]
				title = Skip.current[1]
				t = Skip.current[2]
				queue.pop(0)
				opt = '-async 1'
				before = ''
				try:
					opt += ' -ss ' + str(Skip.current[5])
					Skip.current.pop(5)
				except IndexError as e:
					print(str(datetime.datetime.now()) + ': IndexError: ' + str(e))
					pass
				player = client.voice.create_ffmpeg_player(url, options=opt, before_options=before)
				await client.send_message(client.get_channel('144963553475035137'), 'Now playing: *"' + title + '"* - ' + t)
				player.start()
				Skip.started = datetime.datetime.now()
		await asyncio.sleep(1)

@client.event
async def on_ready():
	await client.edit_profile(password, username = botname)
	print(str(datetime.datetime.now()) + '\nLogged in as ' + client.user.name + '\nUser ID: ' + client.user.id + '\n------')
	discord.opus.load_opus(opusloc)
	global voice
	voice = await client.join_voice_channel(client.get_channel(voice_channel))
	global queue
	global player
	loop.create_task(music_queue())
	global owners
	owners = []
	for member in client.get_all_members():
		if int(member.id) in owner and member not in owners:
			owners.append(member)

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if message.content == '(╯°□°）╯︵ ┻━┻':
		await client.send_message(message.channel, '┬─┬﻿ ノ( ゜-゜ノ)')
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
					\n__**MusicBot**__\n`{1}play` - Play audio from a YouTube video or a number of other sources.\
					\n`{1}status` - Get the current track and any tracks in queue.\
					\n`{1}skip` - Vote to skip current track. Requires at least half of the members in the Music channel to succeed.\
					\nWhen calling commands in PM, do not use the prefix `{1}`'.format(botname, prefix))
		elif command == 'join':
			if message.author.id in owner or message.author.id == client.user.id:
				if not arg:
					await client.send_message(message.channel, 'Error no invite')
				else:
					await client.accept_invite(arg)
		elif command == 'restart' or command == 'kill':
			if int(message.author.id) in owner or message.author.id == client.user.id:
				try:
					if player.is_playing():
						Skip.current.append(int((datetime.datetime.now() - Skip.started).total_seconds()))
						queue.insert(0, Skip.current)
					with open('save.json', 'w') as q:
						json.dump(queue, q)
				except NameError:
					pass
				except Exception:
					for o in owners:
						await client.send_message(o, 'Something went wrong.\n```' + tb + '```')
					await client.send_message(message.channel, 'Something went wrong.\nClosing...')
				finally:
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
		elif command == 'playing':
			if not arg:
				await client.change_status(game = discord.Game(name = None))
				print(str(datetime.datetime.now()) + ': ' + message.author.name + ' set status to None')
			else:
				await client.change_status(game = discord.Game(name = arg))
				print(str(datetime.datetime.now()) + ': ' + message.author.name + ' set status to {}'.format(arg))
		elif command == 'slap':
			global slap
			try:
				if int((datetime.datetime.now() - slap).total_seconds()) < 2:
					return
			except NameError:
				pass
			randmem = list(message.server.members)[(random.randrange(0, len(message.server.members)))]
			send = message.author.mention + ' slapped '
			if arg:
				IDs = arg.replace('@', '').replace('<', '').replace('>', '').split()
				for member in message.server.members:
					if str(member.id) in IDs:
						if member.id != client.user.id:
							send = send + member.mention + ' and '
						elif arg.replace('@', '').replace('<', '').replace('>', '') == client.user.id:
							send = message.author.mention + ", don't you dare slap me     "
							break
				if arg.startswith('@everyone'):
					send = message.author.mention + ", you can't slap *everyone,* dumbass     "
				send = send[:-5]
			else:
				send = send + randmem.name
			if send == message.author.mention + ' slapped ':
				send = send + randmem.name
			await client.send_message(message.channel, send + '!')
			slap = datetime.datetime.now()
		elif command == 'milkshake':
			await client.send_message(message.channel, 'https://www.youtube.com/watch?v=pGL2rytTraA')
		elif command == 'compensation':
			comp = ['https://hipiseverything.files.wordpress.com/2013/03/compensation.jpg','https://s-media-cache-ak0.pinimg.com/736x/13/82/03/138203eb61d3ba6faa09a1e44960413d.jpg',
				'http://img.photobucket.com/albums/v394/xdoctor/l_1ed8c6e94411092f4b3e97f21a8bdb59.jpg','http://s2.quickmeme.com/img/e6/e61ac53e2e3cc669600d1161509d4f5456e33c65a57761ad3d4fc5d5c91c5c21.jpg',
				'https://updatesfromthefield.files.wordpress.com/2010/10/windowslivewriter496747266b98-5752overcompensation-2.jpg','http://www.toptenz.net/wp-content/uploads/2010/10/big-truck-photo.jpeg']
			await client.send_message(message.channel, random.choice(comp))
		elif command == 'e' or command == 'i':
			if int(message.author.id) in owner:
				sent = await client.send_message(message.server.default_channel, arg[0])
				for i in range(len(arg)-1):
					sent = await client.edit_message(sent, sent.content + arg[i+1])
					if command == 'e':
						await asyncio.sleep(1)

#		--------------
#		---MusicBot---
#		--------------

#			Supported sources: https://github.com/rg3/youtube-dl/tree/master/youtube_dl/extractor

		elif command == 'play':
			if int(message.channel.id) not in Allowed_Channels_MB or message.channel.is_private == True:
				return
			if message.author not in client.get_channel(voice_channel).voice_members and int(message.author.id) not in owner:
				await client.send_message(message.channel, 'You must be in the Music voice channel to call `{}play`.'.format(prefix))
				return
			try:
				func = functools.partial(youtube_dl.YoutubeDL({'ignoreerrors':True, 'noplaylist':True}).extract_info, arg, download=False)
				info = await client.voice.loop.run_in_executor(None, func)
			except youtube_dl.utils.DownloadError:
				await client.send_message(message.channel, 'That is not a valid source.')
				return
			if 'entries' in info:
				random.shuffle(info['entries'])
				for video in info['entries']:
					title = video.get('title')
					duration = video.get('duration')
					webpage = video.get('webpage_url')
					try:
						url = video.get('requested_formats')[1].get('url')
					except TypeError:
						url = video['url']
					try:
						if webpage == Skip.current[0]:
							await client.send_message(message.channel, '*"' + Skip.current[1] + '"* is already playing.')
							return
					except IndexError:
						pass
					m, s = divmod(duration, 60)
					if m >= 60:
						h, m = divmod(m, 60)
						t = '%d:%02d:%02d' % (h, m, s)
					else:
						t = '%d:%02d' % (m, s)
					await client.send_message(message.channel, message.author.mention + ' added *"' + title + '"* - ' + t + ' to queue.')
					queue.append([webpage, title, t, url, duration])
			else:
				title = info.get('title')
				duration = info.get('duration')
				webpage = info.get('webpage_url')
				try:
					url = info.get('requested_formats')[1].get('url')
				except TypeError:
					url = info['url']
				try:
					if webpage == Skip.current[0]:
						await client.send_message(message.channel, '*"' + Skip.current[1] + '"* is already playing.')
						return
				except IndexError:
					pass
				m, s = divmod(duration, 60)
				if m >= 60:
					h, m = divmod(m, 60)
					t = '%d:%02d:%02d' % (h, m, s)
				else:
					t = '%d:%02d' % (m, s)
				await client.send_message(message.channel, message.author.mention + ' added *"' + title + '"* - ' + t + ' to queue.')
				queue.append([webpage, title, t, url, duration])
		elif command == 'status':
			if int(message.channel.id) not in Allowed_Channels_MB:
				return
			if message.author not in client.get_channel(voice_channel).voice_members and int(message.author.id) not in owner:
				await client.send_message(message.channel, 'You must be in the Music voice channel to call `{}status`.'.format(prefix))
				return
			if not player.is_playing():
				await client.send_message(message.channel, 'Nothing playing.')
				return
			m, s = divmod((Skip.current[4] - int((datetime.datetime.now() - Skip.started).total_seconds())), 60)
			if m >= 60:
				h, m = divmod(m, 60)
				left = '(%d:%02d:%02d left)' % (h, m, s)
			else:
				left = '(%d:%02d left)' % (m, s)
			mes = 'Playing *"' + Skip.current[1] + '"* - ' + Skip.current[2] + ' ' + left
			need = (((len(client.get_channel(voice_channel).voice_members)-1) // 2) + 1 - Skip.skip)
			mes += '\n Skip votes: ' + str(Skip.skip) + ' More needed to skip: ' + str(need)
			if queue:
				mes += '\n\n __**Queue**__'
				if len(queue) < 3:
					for i in queue:
						mes += '\n*"' + i[1] + '"* - (' + i[2] +')\n'
				else:
					mes += ' Total songs in queue: ' + str(len(queue))
					for i in range(3):
						mes += '\n*"' + queue[i][1] + '"* - ' + queue[i][2] +'\n'
			await client.send_message(message.channel, mes)
		elif command == 'queue':
			if int(message.channel.id) not in Allowed_Channels_MB:
				return
			if not player.is_playing():
				await client.send_message(message.author, 'Nothing playing.')
				return
			m, s = divmod((Skip.current[4] - int((datetime.datetime.now() - Skip.started).total_seconds())), 60)
			if m >= 60:
				h, m = divmod(m, 60)
				left = '(%d:%02d:%02d left)' % (h, m, s)
			else:
				left = '(%d:%02d left)' % (m, s)
			mes = 'Playing *"' + Skip.current[1] + '"* - ' + Skip.current[2] + ' ' + left
			need = (((len(client.get_channel(voice_channel).voice_members)-1) // 2) + 1 - Skip.skip)
			mes += '\n Skip votes: ' + str(Skip.skip) + ' More needed to skip: ' + str(need)
			if queue:
				mes += '\n\n __**Queue**__'
				mes += ' Total songs in queue: ' + str(len(queue))
				for song in queue:
					mes += '\n*"' + song[1] + '"* - ' + song[2] +'\n'
			await client.send_message(message.author, mes)
		elif command == 'skip':
			if arg == 'admin' and int(message.author.id) in owner:
				await client.send_message(message.channel, message.author.mention + ' admin skipped *"' + Skip.current[1] + '"*')
				player.stop()
				return
			if int(message.channel.id) not in Allowed_Channels_MB or message.channel.is_private == True:
				return
			if message.author not in client.get_channel(voice_channel).voice_members:
				await client.send_message(message.channel, 'You must be in the Music voice channel to call `{}skip`.'.format(prefix))
				return
			if message.author.id in Skip.attemped:
				await client.send_message(message.channel, message.author.mention + ', you have already voted to skip *"' + Skip.current[1] + '"*')
				return
			Skip.attemped.append(message.author.id)
			Skip.skip += 1
			if Skip.skip > ((len(client.get_channel(voice_channel).voice_members)-1) // 2):
				await client.send_message(message.channel, 'Skipping *"' + Skip.current[1] + '"*')
				player.stop()
			else:
				need = (((len(client.get_channel(voice_channel).voice_members)-1) // 2) + 1 - Skip.skip)
				if need == 1:
					s = ''
				else:
					s = 's'
				await client.send_message(message.channel, 'Unable to skip *"' + Skip.current[1] + '."* Not enough votes. Need ' + str(need) + ' more vote' + s)

		else:
			print(str(datetime.datetime.now()) + ': **Error:** Not a valid command')
	except Exception as e:
		import traceback
		tb = traceback.format_exc()
		await client.send_message(message.channel, 'Something went wrong.')
		for o in owners:
			await client.send_message(o, 'Something went wrong.\n```' + tb + '```')
		raise

@client.event
async def on_member_ban(member):
	await client.send_message(member.server.default_channel, 'The banhammer fell on {}. :hammer:'.format(member.name))
	await client.send_message(member, 'The banhammer fell on you in {}. :hammer:'.format(member.server.name))

@client.event
async def on_member_kick(member):
	await client.send_message(member.server.default_channel, '{} got the boot. :boot:'.format(member.name))
	await client.send_message(member, 'You got booted from {}. :boot:'.format(member.server.name))

@client.event
async def on_member_unban(server, user):
	await client.send_message(server.default_channel, '{} got unhammered'.format(user.name))

try:
	client.run(email,password)
except discord.errors.ClientException as e:
	print(str(datetime.datetime.now()) + ': ClientException')
	print(e)
	pass
