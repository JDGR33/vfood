import tweepy
from dotenv import load_dotenv
import os
import re
from datetime import datetime



def create_tw_client():
    """Create a tweepy.Client object
    
    Returns :
    ---------
    tweepy.Clinet 
    """
    load_dotenv()

    # Variables that contains the credentials to access Twitter API
    BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

    client = tweepy.Client(BEARER_TOKEN)
    return(client)

def get_recent_tweets(user:str,num_tw=10)->tweepy.Response :
    """Get the last tweets from a user
    
    Parameters :
    ------------
    user : str
        Name of the user
    
    num_tw : int
        Limit of Tweets

    Returns :
    ---------
    tweepy.Response 
        The fields in responses from Twitter’s API.
    
    """
    client = create_tw_client()
    query = f'from:{user}'

    tweets = client.search_recent_tweets(query=query, tweet_fields=['text', 'created_at'], max_results=num_tw)
    # print(type(tweets))
    # for tweet in tweets.data:
    #      print(tweet.text)
    #      print("date")
    #      print(tweet.created_at)
    #      print("\n")

    return tweets

def check_monitor_data(tweet_txt:str)->bool:
    """Filter out tweets that don't show exchange rate information
    Parameters :
    ------------
    tweet_txt : str
        The Raw tweet to evaluate

    Return :
    --------
    bool :
        True if has exchange information, false otherwise

    """
    text_1 = "🗓" in tweet_txt
    text_2 = "💵" in tweet_txt
    
    return text_1 and text_2

def get_monitor_data(tweet_txt:str)->float:
    """Gets the exchange rate float from a Tweet from monitor
    
    Parameters :
    ------------
    tweet_txt : str
        Raw text data from a Tweet
    
    Returns :
    ---------
    float
        The exchange rate from the tweet
    """


    data={}

    expression ="💵\s*Bs\.?\s*(\d+[,.]\d+)" #💵, zero or more  of white Spaces, "Bs", a possible dot,zero or more of white Spaces,one or more numbers, either the comma or dot characters, and one or more numbers ////
   
    rate = re.search(expression,tweet_txt).group(1)#Find the regular expression and get the group with the rate rate float
    rate = rate.replace(",",".")#Replace the comma for a dot 
    rate = float(rate) #Convert to float
    print(rate)
    data['exchange']=rate
    
    return data
    
def last_exchange_monitor(tweets:tweepy.Response)->str:
    """Get the first tweet with exchange Rate Information
    
    Parameters :
    ------------
    tweets : tweepy.Response
        API response with tweets you want to check
    
    Return :
    --------
    tweepy.tweet.Tweet :
        Tweet object with the latest exchange rate information
    """

    r = ""

    for tweet in tweets.data:
        if check_monitor_data(tweet.text): #Check if the tweet has exchange rate information
            print(tweet.text)
            print(type(tweet))
            r = tweet
            break
    return r

def exchange_from_tw_user(user:str)->dict:
    """Get the latest exchange rate from a user

    Parameters :
    ------------
    user : str
        Twitter username for scraping
    
    Returns :
    ---------
    dict :
        Data with the exchange rate, date time, name of the user, and the tweet text
    """

    tweets  = get_recent_tweets(user) #Get latest tweets
    
    data = {}
    if user == "monitordolarvla":
        last_tw =(last_exchange_monitor(tweets)) #Get latest exchange rate tweet
        data['rate'] = get_monitor_data(last_tw.text) #Get the exchange rate from the tweet

    data['date'] = last_tw.created_at #Datetime of the tweet 
    data['name'] = user #Username
    data['tweet'] = last_tw.text #Raw text from the tweet

    return data

print(exchange_from_tw_user("monitordolarvla"))
