import os
import schedule
import time
from dotenv import load_dotenv
import tweepy

load_dotenv()

MAX_TWEETS = 1
# 5000000000000000000000

# Api Keys
twitter_api_key = os.getenv('CONSUMER_KEY')
twitter_api_secret = os.getenv('CONSUMER_SECRET')
twitter_api_token = os.getenv('ACCESS_TOKEN')
twitter_api_secret_token = os.getenv('ACCESS_TOKEN_SECRET')

# Twitter API
auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
auth.set_access_token(twitter_api_token, twitter_api_secret_token)
twitter_api = tweepy.API(auth, wait_on_rate_limit=True,
                         wait_on_rate_limit_notify=True)


# #
#   Check for new tweets
# #

# 1. First check last 100 followers from sephora & other accounts.
# 2. Follow all the accounts
# 3. Filter tweets based on hashtags like #beauty, #cosmetics
# 4. Like every tweet and comment "This look beautiful!"
# Once bot has liked & commented on about 500 tweets


def fetchTweets(twitter_api):
    # Define vars
    twitterUser = ''

    # Fetch x amount of tweets and loop through them
    for tweet in tweepy.Cursor(twitter_api.search, q='#beauty', rpp=100).items(MAX_TWEETS):
        # Current tweets poster username
        twitterUser = tweet.user.screen_name

        # For each follower of twitterUser, follow them
        for follower in twitter_api.followers(twitterUser):
            print(follower.screen_name)

        pass


fetchTweets(twitter_api)
