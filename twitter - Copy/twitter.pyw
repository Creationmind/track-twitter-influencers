import tweepy
import webbrowser
import time
import json
import asyncio
import telegram
import winsound

#----- Configuring api --------------------------------------------------------

consumer_key = ""
consumer_secret =  ""
Bearer_token =  ""
access_token = ""
access_token_secret	= ""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
api = tweepy.API(auth, wait_on_rate_limit= True)

#-----------------------------------------------------------------------------
# Initialising telegram bot

bot = telegram.Bot(token='')

#-----------------------------------------------------------------------------
kol = ['jack','elonmusk'] #key opinion leader that you want to track


temp = ''
data ={}
message = []
api_counter =0
def compare():
    print('test')
    temp = ''
    data ={}
    message = []
    with open('twitter_account.json') as f:
        data = json.load(f)
        for user in kol:
            user_friend = api.friends_ids(user)
            difference = list(set(user_friend) - set(data[user]))
            data[user] = user_friend
            for i in difference:
                temp_message = '@'+user+'  just followed https://twitter.com/'+api.get_user(str(i))._json['screen_name']
                message.append(temp_message)
    api_counter =1
    f.close()
    reset_database()
    for i in message:
        bot.send_message(chat_id ='',text=i)

def reset_database():
    with open('twitter_account.json','r+') as f:
        if api_counter == 0:
            for user in kol:
                data[user] = api.friends_ids(user)
        json.dump(data,f)
        f.close()

        
while True:
    compare()
