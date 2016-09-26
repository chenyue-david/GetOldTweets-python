import got
from datetime import date
from datetime import timedelta
from time import strftime

def crawl1DayTweet(f, currentDate):
	
	def printTweet(t):
		#print descr
		print ("Username: %s" % t.username.encode('utf-8'))
		print ("Retweets: %d" % t.retweets)
		print ("Text: %s" % t.text.encode('utf-8'))
		print ("Mentions: %s" % t.mentions.encode('utf-8'))
		print ("Hashtags: %s\n" % t.hashtags.encode('utf-8'))
	
	# Example 1 - Get tweets by username
	#tweetCriteria = got.manager.TweetCriteria().setUsername('barackobama').setMaxTweets(1)
	#tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
	
	#printTweet("### Example 1 - Get tweets by username [barackobama]", tweet)
	
	# Example 2 - Get tweets by query search
	#tweetCriteria = got.manager.TweetCriteria().setQuerySearch('europe refugees').setSince("2015-05-01").setUntil("2015-09-30").setMaxTweets(1)
	#tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
	
	#printTweet("### Example 2 - Get tweets by query search [europe refugees]", tweet)
	
	# Example 3 - Get tweets by username and bound dates
	s = strftime("%Y-%m-%d", currentDate.timetuple())
	e = strftime("%Y-%m-%d", (currentDate + timedelta(1)).timetuple())
	tweetCriteria = got.manager.TweetCriteria().setQuerySearch('$aap').setLang('en').setSince(s).setUntil(e).setMaxTweets(4000)
	tweets = got.manager.TweetManager.getTweets(tweetCriteria)
	
	
	for t in reversed(tweets):
		f.write(t.id.encode('utf-8') + '\t' + t.username.encode('utf-8') + '\t' + str(t.date) + '\t' + 
			t.geo.encode('utf-8') + '\t' + t.text.encode('utf-8') + '\t' + str(t.retweets) + '\t' + str(t.favorites)
			+ '\t' + t.hashtags.encode('utf-8') + '\t' + t.mentions.encode('utf-8') + '\t' + t.permalink.encode('utf-8') + '\n')
	#printTweet("### Example 3 - Get tweets by username and bound dates [barackobama, '2015-12-30', '2015-12-31']", tweet)

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + timedelta(n)

if __name__ == '__main__':
	start_date = date(2015, 12, 1)
	end_date = date(2015, 12, 31)
	f = open('$aah-Dec', 'w')
	for single_date in daterange(start_date, end_date):
		crawl1DayTweet(f, single_date)
	f.close()
	