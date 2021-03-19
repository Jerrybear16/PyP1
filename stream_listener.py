import tweepy
from textblob import TextBlob
import re

class StreamListener(tweepy.StreamListener):
  MAX_TWEETS = 10
  tweet_count = 0
  count_pos_tweet = 0
  count_neg_tweet = 0
  count_neut_tweet = 0
  subjectivity = 0
  polarity = 0

  def on_status(self, status):
    analysis = TextBlob(status.text)
    curr_polarity = analysis.sentiment.polarity
    curr_subjectivity = analysis.sentiment.subjectivity

    if ((curr_subjectivity > 0.5) or 
    re.search('^(RT @).*', status.text) != None or
    curr_polarity == 0.0):
      return

    print("-"*50 + "\n" + status.text)

    print("Polarity: " + str(curr_polarity))
    self.polarity += curr_polarity
    print("Subjectivity: " + str(curr_subjectivity))
    self.subjectivity += curr_subjectivity

    self.tweet_count += 1

    if curr_polarity > 0:
      self.count_pos_tweet += 1
    elif curr_polarity < 0:
      self.count_neg_tweet += 1
    else:
      self.count_neut_tweet += 1

    if (self.tweet_count >= self.MAX_TWEETS):
      return False

  def on_error(self, status_code):
    if status_code == 420:
      return False