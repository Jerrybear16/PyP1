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
import csv

# Variables for twitter authentication
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_KEY")
access_token_secret = os.getenv("ACCESS_SECRET")

# User input for company or person they want to review tweets for
company = input("Enter the company or person on twitter you wish to observe:\n> ")

# Set up twitter authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Create stream listener, and begin receiving tweets
stream_listener = sl.StreamListener()
stream = tweepy.Stream(auth=api.auth, listener = stream_listener)
# Filter tweets for company, and english-only tweets
stream.filter(track = [f"{company}"], languages=["en"])

# Begin printing results:
print("\n"+"-"*100)
# Print overall opinion of subject
if stream_listener.count_pos_tweet > stream_listener.count_neg_tweet:
  print(f"The general opinion of {company} is positive.")
elif stream_listener.count_pos_tweet < stream_listener.count_neg_tweet:
  print(f"The general opinion of {company} is negative.")

print("-"*100)
# Print total positive or negative tweets
print("Total Positive Tweets: " + str(stream.listener.count_pos_tweet))
print("Total Negative Tweets: " + str(stream_listener.count_neg_tweet))

print("-"*100)
# Print overall polarity and subjectivity of tweets
print("Overall Polarity: " + str((stream_listener.polarity / stream_listener.MAX_TWEETS)))
print("Overall Subjectivity: " + str((stream_listener.subjectivity / stream_listener.MAX_TWEETS)))

# Create bar chart of results
tweet_types = ['Positive Tweets', 'Negative Tweets']
y_pos = np.arange(len(tweet_types))
data = [stream_listener.count_pos_tweet, stream_listener.count_neg_tweet]
plt.bar(y_pos, data, align='center', alpha=0.5,
color=['b','r'],
label=['Positive', 'Negative'])
plt.xticks(y_pos, tweet_types)
plt.ylabel('Count')
plt.xlabel('Type of Tweet')
plt.title(f'Distribution of Tweets for {company}')

plt.show()


'''
createCSV(company, column1, column2):

Input:
company - the company name that is being looked at
column1 - contains the sentiment of the tweets in a list format
column2 - contains the amount of tweets of the previous columns sentiment in a list format

Returns:
None

Creates a CSV file from a company name and creates columns based on the two lists provided
'''
def createCSV(company, column1, column2):
  if not os.path.isdir("companyCSVFiles"):
    os.mkdir("companyCSVFiles")

  csvFile = open("companyCSVFiles/" + company + "sentimentCSV.csv", "a")
  i = 0
  for sentiment in column1:
    csvFile.write(sentiment + "," + str(column2[i]) + "\n")
    i += 1

'''
createPieChart(folder):

Input:
folder - the name of the folder containing csv files to make into piecharts

Returns:
None

Creates a Pie chart from a folder containing all of the csv files
'''
def createPieChart(folder):
  i = 0
  fileList = []

  for file in os.listdir("companyCSVFiles"):
          fileList.append(folder + "/" + file)

  for company in fileList:
    count = []
    companies = []

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
    ax.set_title(company + ' Tweet Analysis')

    plt.show()

# CSV file creation
createCSV(company, ["Positive Tweets", "Negative Tweets"], [stream_listener.count_pos_tweet, stream_listener.count_neg_tweet])
# Pie chart creation
createPieChart("companyCSVFiles")