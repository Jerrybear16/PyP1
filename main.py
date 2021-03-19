"""
***RESEARCH PROBLEM***
Run sentiment analysis on tweets to see if the overall opinion of a company is positive or negative
"""

#libs
import tweepy 
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np
import os
import csv

'''
createCSV(column1, column2):

column1 - contains the sentiment of the tweets
column2 - contains the amount of tweets of the previous columns sentiment
'''
def createCSV(company, column1, column2):
  csvFile = open(company + "sentimentCSV.csv", "a")
  i = 0
  for sentiment in column1:
    csvFile.write("companyCSVFiles/" + sentiment + "," + str(column2[i]) + "\n")
    i += 1

def createPieChart(folder):

  count = []
  companies = []
  i = 0

  fileList = []

  for file in os.listdir("companyCSVFiles"):
          fileList.append(folder + "/" + file)

  for company in fileList:
    
    with open(company, newline='') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=',')
      for row in spamreader:
          companies.append(row[0])
          #print(row[0])
          count.append(row[1])
          i += 1
          if i > 5:
              break
          
          
    fig, ax = plt.subplots()
    ax.pie(count, labels=companies, autopct='%1.1f%%')
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    ax.set_title('Tweet Analysis')

    plt.show()
    

#set up twitter auth
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_KEY")
access_token_secret = os.getenv("ACCESS_SECRET")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#company to research - prompt user
s = input('Enter Company to Observe:')
company = s

#search public tweets w/ certain filter
public_tweets = api.search(company,"en")

#counts of pos/neg tweets in regards to above filter^
count_pos_tweet = 0
count_neg_tweet = 0
count_neut_tweet = 0

#for each tweet pulled in filter, do the following:
#-print the tweet
#-print the polarity (1 is pos, -1 is neg) and subjectivity of tweet
for tweet in public_tweets:
  print("-"*50 + "\n" + tweet.text)
  analysis = TextBlob(tweet.text)
  print(str(analysis.sentiment) + "\n" + "-"*50 + "\n")
  if analysis.sentiment.polarity > 0:
    count_pos_tweet += 1
  elif analysis.sentiment.polarity < 0:
    count_neg_tweet += 1
  else:
    count_neut_tweet += 1

#print pos/neg results
print(f"Count of positive tweets for {company} under criteria: {count_pos_tweet}")
print(f"Count of negative tweets for {company} under criteria: {count_neg_tweet}")

#print conclusions on company as a whole
if count_pos_tweet > count_neg_tweet:
  print(f"The general opinion of {company} is positive.")
elif count_pos_tweet < count_neg_tweet:
  print(f"The general opinion of {company} is negative.")
else:
  print(f"The general opinion of {company} is neutral.")

#CSV file creation
#createCSV(company, ["Positive Tweets", "Negative Tweets", "Neutral/Unclassified Tweets"], [count_pos_tweet, count_neg_tweet, count_neut_tweet])

createPieChart(companyCSVFiles)

#bar graph
'''
tweet_types = ['Positive Tweets', 'Negative Tweets', 'Neutral/Unclassified']
y_pos = np.arange(len(tweet_types))
data = [count_pos_tweet, count_neg_tweet, count_neut_tweet]
plt.bar(y_pos, data, align='center', alpha=0.5,
color=['b','r','y'],
label=['Positive', 'Negative', 'Neut/Unk'])
plt.xticks(y_pos, tweet_types)
plt.ylabel('Count')
plt.xlabel('Type of Tweet')
plt.title(f'Distribution of Tweets for {company}')
plt.show()
'''




