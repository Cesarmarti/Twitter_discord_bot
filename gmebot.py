import discord
import tweepy
from config import create_api
import time
import asyncio
import os

client = discord.Client()

channel_name = "stonks"
default_channel = 0
api = ""
showAll = False

_loop = asyncio.get_event_loop()

#people_list = ["1362349949011247113"]
people_list = []
#word_list = ["short","bitcoin","GME","diamond hands"]
word_list = []

class PeopleListener(tweepy.StreamListener):
	def __init__(self, api):
		self.api = api
		self.me = api.me()

	def on_status(self, tweet):
		#print(f"{tweet.user.name}:{tweet.text}")
		if not showAll:
			if str(tweet.user.id) not in people_list:
				return
		asyncio.run_coroutine_threadsafe(showTweet(tweet),_loop)
		

	def on_error(self, status):
		print("Error detected")

def init():
	#get vip list from files
	f1 = open("keywords.txt", "r")
	f2 = open("vipList.txt", "r")
	global word_list
	word_list = f1.read().split("\n");
	global people_list
	people_list = f2.read().split("\n");
	#people_list = [int(people) for people in people_list]
	f1.close()
	f2.close()
	global api
	api = create_api()
	dc_key = os.environ['dc_key']
	client.run(dc_key)

def command_text(command):
	#channel = client.get_channel(817125319403765880);
	#channel = client.get_channel(default_channel)
	#print(channel)
	#print(type(default_channel))
	#await default_channel.send("test")
	parts = []
	if "\"" in command:
		parts = command.split("\"")
	else:
		parts = command.split(" ")
	comm = parts[0]
	value = ""
	if len(parts)>1:
		value = parts[1]
	else: 
		value = ""
	comm = comm.replace(" ","")
	print("Used command: "+comm+" with value: "+value)
	if comm == "addPerson":
		asyncio.run_coroutine_threadsafe(addVIP(value),_loop)
	elif comm == "addWord":
		asyncio.run_coroutine_threadsafe(addKeyWord(value),_loop)
	elif comm == "help":
		asyncio.run_coroutine_threadsafe(help(),_loop)
	elif comm == "creator":
		asyncio.run_coroutine_threadsafe(creator(),_loop)
	elif comm == "limit":
		global showAll
		showAll = not showAll
	else:
		print("Invalid command used!")

	
def addPersonToFile(person):
	f2 = open("vipList.txt", "a")
	f2.write("\n"+person)
	f2.close()

def addKeywordToFile(word):
	global word_list
	word_list.append(word)
	f1 = open("keywords.txt", "a")
	f1.write("\n"+word)
	f1.close()

async def creator():
	await default_channel.send("Martin");

async def help():
	msg = "```"
	msg = msg+"- $addPerson -> add user to follow. Must be user's twitter ID\n"
	msg = msg+"- $addWord -> add keyword to look for in a tweet\n"
	msg = msg+"- $help -> this message\n"
	msg = msg+"- $creator -> display the creator\n"
	msg = msg+"- $limit -> shows all the tweets (mentions, retweets, EVERYTING). [softly] Don't.\n"
	msg = msg+"```"
	await default_channel.send(msg);

async def addVIP(person):
	print("Added "+person+" to VIP list.")
	addPersonToFile(person)
	await default_channel.send("Added "+person+".\nChanges will take effect on restart.");

async def addKeyWord(keyword):
	print("Added "+keyword+" to keyword list.")
	addKeywordToFile(keyword)
	await default_channel.send("Added "+keyword+".");

async def showTweet(tweet):
	userName = "**"+tweet.user.name+"** tweeted:" 
	text = "```"+tweet.text+"```"
	lowerText = tweet.text.lower()
	msg = userName+"\n"+text
	found_keywords = ""
	print(lowerText)
	for word in word_list:
		word = word.lower()
		if word in lowerText:
			found_keywords = found_keywords+", "+word
	if found_keywords != "":
		msg = msg+"Found keywords:\n"+"```diff\n-"+found_keywords[1:]+"\n"+"```"
	await default_channel.send(msg);

@client.event
async def on_ready():
	print('Bot logged in as {0.user}'.format(client))
	global default_channel
	for guild in client.guilds:
		for channel in guild.channels:
			if channel.name == channel_name:
				default_channel = client.get_channel(channel.id);
	#await default_channel.send('Bot online!')
	#connect to twitter		
	people_listener = PeopleListener(api)
	stream = tweepy.Stream(api.auth, people_listener)
	stream.filter(follow=people_list, is_async=True)

@client.event
async def on_message(message):

	if message.author == client.user:
		return

	#commands
	if message.content.startswith('$'):
		command_text(message.content[1:])





init()

#TODO extended tweet da vse pokaze
#stream follow da tud mentione, maybe bo zjebal rate