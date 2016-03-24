import sys
import random
from os import system
from settings import Allowed_Channels_MB,botname

class trivia:
	def __init__(self, bServer, bChannel, client):
		global t
		t = int('-1')

	def question(self, arg, client):
		from questions import Questions
		global question
		global answers
		global correct
		global t
		question = random.choice(Questions)
		answers = question[2:]
		t = len(answers) - 1
		correct = answers[int(question[1]) - 1]
		random.shuffle(answers)
		client.send_message(message.channel, 'Respond with\n`@{} answer` followed by the answer.'.format(botname))
		p = '**{}**'.format(question[0])
		for i in range(len(answers)):
			p += '\n{}) {}'.format(i + 1, answers[i])
		client.send_message(message.channel, p)
	
	def answer(self, author, arg, client):
		ans = arg.replace(' ', '')
		global t
		if int(t) < 0:
			client.send_message(message.channel, 'Please use `@{} trivia` to request a trivia question.'.format(botname))
		elif ans.isdigit() == False:
			client.send_message(message.channel, '{} did not send a valid answer'.format(message.author.mention()))
		else:
			t = int(t) - 1
			m = answers[int(ans) - 1]
			if m == correct:
				client.send_message(message.channel, '{} answered correctly.'.format(message.author.mention()))
				t = '-1'
			elif t == 0:
				client.send_message(message.channel, '{} answered incorrectly. The correct answer is {}.'.format(message.author.mention(), correct))
				t = '-1'
			else:
				client.send_message(message.channel, '{} answered incorrectly. {} guesses left.'.format(message.author.mention(), t))
