import tweepy

class MentionsStreamListener(tweepy.StreamListener):

	def __init__(self, models, api):
		self.models = models;
		self.api = api;

	def on_status(self, status):
		from creative_ai.generate import generateMusicForPhrase

		user_handle = status.user.screen_name
		tweet_id = status.id
		first_word = status.text.replace("@CountryBot1", "").split()[0]
    	
		if (first_word == "RT"):
			return;

		if (user_handle == "CountryBot1"):
			return;

		print(user_handle + " " + first_word)

		phrase = self.models.generatePhrase(first_word)
		verseOne = generateMusicForPhrase(self.models, first_word, phrase);

		status = ""
		for line in verseOne:
			status += (' '.join(line)).capitalize() + "\n"

		print(status)
		print()

		self.api.update_status("@" + user_handle + "\n" + status, in_reply_to_status_id = tweet_id)

class TwitterManager():

	def __init__(self, consumer_key, consumer_secret, access_token, accesss_token_secret, models):
		"""
		Requires: Valid & registered Twitter consumer/access keys
		Modifies: self (this instance of the TwitterManager object)
		Effects: Authenticates and instantiates a tweepy object. Begins the stream listener.
		"""
	    
		self.models = models;

	    # OAuth process, using the keys and tokens
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)

		# Creation of the actual interface, using authentication
		self.api = tweepy.API(auth)
		 
		mentionsStreamListener = MentionsStreamListener(self.models, self.api)
		self.streamListener = tweepy.Stream(auth = auth, listener=mentionsStreamListener)

		self.streamListener.filter(track=['@CountryBot1'])

if __name__ == '__main__':
    """
    Requires: Nothing
    Modifies: Nothing
    Effects:  This is the main function.
    """

    tm = TwitterManager("xyrR5WQJO5v1ZhKicBOJGrlKj", "KrqzS5VWkpM3rmAmQmVZbpRnHRCOMuTgtetCU7ZSzIk1GxKD4c", "1070065717796634631-YYrAWPS8TJoDVSrvcj2HVyNqaBesmE", "JOJiIuGZRtv27nE5oZLXsISOFTqdjbsLZq7VDlCqcMn14")

