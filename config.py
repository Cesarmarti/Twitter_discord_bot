import tweepy
import os

# Authenticate to Twitter
def create_api():
	consumer_key = os.environ['con_key']
	consumer_secret = os.environ['con_sec']
	access_token = os.environ['acc_tok']
	access_token_secret = os.environ['acc_sec']

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	try:
		api.verify_credentials()
		print("Twitter authentication OK")
	except Exception as e:
		print("Error during authentication")
	print("Twitter API created")
	return api

