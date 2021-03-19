import tweepy
from textblob import TextBlob
import re

# Helper class for gathering tweets in a stream
class StreamListener(tweepy.StreamListener):
  MAX_TWEETS = 1
  tweet_count = 0
  count_pos_tweet = 0
  count_neg_tweet = 0
  subjectivity = 0
  polarity = 0

  def on_status(self, status):
    # Perform sentiment analysis on the tweet
    analysis = TextBlob(status.text)
    curr_polarity = analysis.sentiment.polarity
    curr_subjectivity = analysis.sentiment.subjectivity

    # Ignore tweets that meet one of the following conditions:
    # 1) They are too subjective (could be editied, depending on need)
    # 2) They are a retweet
    # 3) The tweet has no polarity
    if ((curr_subjectivity > 0.5) or 
    re.search('^(RT @).*', status.text) != None or
    curr_polarity == 0.0):
      return

    # Print the tweet out
    print("-"*50 + "\n" + status.text)

    # Print the polarity and subjectivity of the tweet
    # Store the total polarity and subjectivity for later analysis
    print("Polarity: " + str(curr_polarity))
    self.polarity += curr_polarity
    print("Subjectivity: " + str(curr_subjectivity))
    self.subjectivity += curr_subjectivity

    self.tweet_count += 1

    # Log the polarity of the tweet
    if curr_polarity > 0:
      self.count_pos_tweet += 1
    elif curr_polarity < 0:
      self.count_neg_tweet += 1

    # Once you reach a max number of tweets, end the stream
    if (self.tweet_count >= self.MAX_TWEETS):
      return False

  # End the stream if bad status code
  def on_error(self, status_code):
    if status_code == 420:
      return False