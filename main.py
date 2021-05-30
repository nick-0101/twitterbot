import os
import sys
import schedule
import time
from dotenv import load_dotenv
import tweepy

load_dotenv()

MAX_TWEETS = 100
keyword = 'cosmetic' or 'beauty' or 'deals' or 'beauty sale'

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

def fetchTweets(twitter_api):
    # Fetch x amount of tweets and loop through them
    for tweet in tweepy.Cursor(
        twitter_api.search,
        q=('cosmetics OR beauty OR beauty sale OR deals OR beauty deals OR Canada OR canadian'),
        rpp=100
    ).items(MAX_TWEETS):
        try:
            # Current tweets poster username & if tweet is liked
            status = twitter_api.get_status(tweet.id)
            favorited = status.favorited

            # Check if tweet liked or not
            if favorited == True:
                pass
            else:
                # Tweet reply
                tweet_reply = 'Compare Canadian cosmetic prices across major retailers at glitzher.com'

                # Like each tweet
                twitter_api.create_favorite(tweet.id)

                # Reply to each tweet
                twitter_api.update_status(
                    status=tweet_reply, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)

                # Confirmation Success
                print('Successfully liked and commented!')

                # Delay program to not get blocked by twitter
                time.sleep(55)

        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break


def direct_message_checker(twitter_api):
    messages = twitter_api.list_direct_messages(count=5)

    for message in messages:
        # Reply
        reply = 'Hello! Thank you for contacting Glitzher. I\'m a bot but to get in contact with the admin of Glitzher please send a direct message to them on instagram: @glitzher_official'

        # Get recent dm & sender id
        text = message.message_create["message_data"]["text"]
        sender_id = message.message_create["sender_id"]

        # Respond to direct messgae
        twitter_api.send_direct_message(sender_id, reply)

        # remove DM
        twitter_api.destroy_direct_message(
            message.id)


if __name__ == '__main__':
    print('Startup successful')
    # Every 10 minutes check for messages
    schedule.every(10).minutes.do(direct_message_checker, twitter_api)

    # Every day at these times run fetchTweets
    schedule.every().day.at("12:30").do(fetchTweets, twitter_api)
    schedule.every().day.at("13:30").do(fetchTweets, twitter_api)
    schedule.every().day.at("16:30").do(fetchTweets, twitter_api)

    while 1:
        schedule.run_pending()
        time.sleep(1)
