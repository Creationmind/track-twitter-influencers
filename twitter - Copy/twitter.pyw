import telegram, tweepy, json




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
twitterHandlersToCheck = ['']


temp = ''
dataFromJsonFile ={}
message = []
api_counter =0
def compare():
    print('Working perfectly')
    temp = ''
    global dataFromJsonFile
    message = []
    with open('twitter_account.json') as f:
        dataFromJsonFile = json.load(f)
        for twitterHandler in twitterHandlersToCheck:
            try:
                twitterHandleFriends = api.friends_ids(twitterHandler)
            except:
                continue
            try:
                difference = list(set(twitterHandleFriends) - set(dataFromJsonFile[twitterHandler]))
            except:
                dataFromJsonFile[twitterHandler] = twitterHandleFriends
                print('new user: ',twitterHandler)
                send_message_to_telegram = f'Bot is following new user :@{twitterHandler}'
                bot.send_message(chat_id ='',text=send_message_to_telegram)
                continue
            for i in difference:
                newFriend = api.get_user(str(i))._json
                message_placeholder = '@'+twitterHandler+'  just followed https://twitter.com/'+newFriend['screen_name'] + f'\nFollower : {newFriend["followers_count"]} '
                try:
                    if int(newFriend["followers_count"]) < 500:
                        message_placeholder += '🔴'
                    elif int(newFriend["followers_count"]) < 3000:
                        message_placeholder +='🟡'
                    else:
                        message_placeholder += '🟢'
                    message_placeholder += f'\Website: {newFriend["url"]}'
                except:
                    print('error in try except function')
                message.append(message_placeholder)
    api_counter =1
    f.close()
    reset_database()
    for i in message:
        bot.send_message(chat_id ='',text=i)



def reset_database():
    if api_counter == 0:
        for user in twitterHandlersToCheck:
            dataFromJsonFile[user] = api.friends_ids(user)
            print(user)
    with open('twitter_account.json','w') as f:
        json.dump(dataFromJsonFile,f)
        print('writing data')
        f.close()
   

def _main():
    try:
        while True:
            compare()
    except:
        print('Error')
        return _main()



_main()

