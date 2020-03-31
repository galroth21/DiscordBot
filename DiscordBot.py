import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from itertools import cycle
import random
import trello
import asyncio

async def oncall(message):
	channel = client.get_channel(#################)
	print(message)
	await channel.send(message)

async def trellopy():

	api_key = ''
	api_secret = ''
	token = ''
	board_id = ''
	list_id = ''
	discord = []
	
	lists = []
	get_list = trello.Boards(api_key, token = token).get_list(board_id)

	for get in get_list:
		lists.append(get["id"])
		
	cards = []
	for l in lists:
		acts = trello.Lists(api_key, token = token).get_action(l)
		
		for act in acts:
			if act["type"] == "createCard":
				card = act["data"]
				card_info = card["card"]
				card_id = card_info["id"]
				cards.append(card_id)
				
	cards.sort(reverse = True)

	# with open('action.txt', 'w') as output:
	#	output.writelines("%s\n" % card for card in cards)

	tickets = []
	with open('action.txt', 'r') as input:
		data = input.readlines()
		
		for line in data:
			current_place = line[:-1]
			tickets.append(current_place)
			
	for card in cards:
		if card not in tickets:
			ticket = trello.Cards(api_key, token = token).get(card)
			message = f'@OnCall, new ticket in Trello. {ticket["shortUrl"]}'
			asyncio.run(oncall(message))
			
			with open('action.txt', 'a') as output:
				output.write('%s\n' % card)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix  = '.')

status = cycle(['with the API', 'with your MIND', 'with reality',
	'The Purge: COVID-19', 'Heads Up, 7-Up'])

### Event for when bot is ready ###
@client.event
async def on_ready():
	change_status.start()
	print(f'{client.user} is ready.')
	for guild in client.guilds:
		print(f'Connected to {guild.name}')
	
### Command to perform a ping ###	
@client.command()
async def ping(ctx):
	await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

### Magic 8 ball command ###	
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
	responses = [
		 "As I see it, yes.",
		 "Ask again later.",
		 "Better not tell you now.",
		 "Cannot predict now.",
		 "Concentrate and ask again.",
		 "Don’t count on it.",
		 "It is certain.",
		 "It is decidedly so.",
		 "Most likely.",
		 "My reply is no.",
		 "My sources say no.",
		 "Outlook not so good.",
		 "Outlook good.",
		 "Reply hazy, try again.",
		 "Signs point to yes.",
		 "Very doubtful.",
		 "Without a doubt.",
		 "Yes.",
		 "Yes – definitely.",
		 "You may rely on it.",
	]
	
	answer = f'Question: {question}\n'
	answer += f'Answer: {random.choice(responses)}'
	await ctx.send(answer)
	
### Greeting command ###
@client.command()
async def greeting(ctx, *, name):
	await ctx.send(f'Howdy, {name}!')

@tasks.loop(seconds=60)
async def change_status():
	await client.change_presence(activity=discord.Game(next(status)))
	await trellopy()

client.run(TOKEN)
