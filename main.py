"""
***RESEARCH PROBLEM***
Run sentiment analysis on tweets to see if the overall opinion of a company is positive or negative
"""

#libs
import tweepy 
import stream_listener as sl
import matplotlib.pyplot as plt
import numpy as np
import os

#set up twitter auth
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_KEY")
access_token_secret = os.getenv("ACCESS_SECRET")

company = input("Enter the company you wish to observe:\n> ")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

stream_listener = sl.StreamListener()
stream = tweepy.Stream(auth=api.auth, listener = stream_listener)
stream.filter(track = [f"{company}"], languages=["en"])

print("\n"+"-"*100)

if stream_listener.count_pos_tweet > stream_listener.count_neg_tweet:
  print(f"The general opinion of {company} is positive.")
elif stream_listener.count_pos_tweet < stream_listener.count_neg_tweet:
  print(f"The general opinion of {company} is negative.")
else:
  print(f"The general opinion of {company} is neutral.")

print("-"*100 + "\n")

print("Total Positive Tweets: " + str(stream.listener.count_pos_tweet))
print("Total Negative Tweets: " + str(stream_listener.count_neg_tweet))
print("Total Neutral Tweets: " + str(stream_listener.count_neut_tweet))

print("-"*100 + "\n")

print("Overall Polarity: " + str((stream_listener.polarity / stream_listener.MAX_TWEETS)))
print("Overall Subjectivity: " + str((stream_listener.subjectivity / stream_listener.MAX_TWEETS)))

tweet_types = ['Positive Tweets', 'Negative Tweets', 'Neutral/Unclassified']
y_pos = np.arange(len(tweet_types))
data = [stream_listener.count_pos_tweet, stream_listener.count_neg_tweet, stream_listener.count_neut_tweet]
plt.bar(y_pos, data, align='center', alpha=0.5,
color=['b','r','y'],
label=['Positive', 'Negative', 'Neut/Unk'])
plt.xticks(y_pos, tweet_types)
plt.ylabel('Count')
plt.xlabel('Type of Tweet')
plt.title(f'Distribution of Tweets for {company}')
plt.show()
