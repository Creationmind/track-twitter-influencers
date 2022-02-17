import tweepy
import json
import telegram


# ----- Configuring api --------------------------------------------------------

consumer_key = ""
consumer_secret = ""
Bearer_token = ""
access_token = ""
access_token_secret = ""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# -----------------------------------------------------------------------------
# Initialising telegram bot

bot = telegram.Bot(token='')

# -----------------------------------------------------------------------------
trackeeList = []



def loadJsonFile():
    with open('twitter_account.json') as f:
        jsonData = json.load(f)
        f.close()
    return jsonData


def writeJsonData(writeData):
    with open('twitter_account.json', 'w') as f:
        json.dump(writeData, f)
        print('writing data')
        f.close()
    return


def hardReset():
    oldJsonData = loadJsonFile()
    for user in trackeeList:
        print(f'Screening {user} ...')
        try:
            oldJsonData[user] = getFriendList(user)
        except:
            print(
                f'API could not fetch {user} details, please check if ID and messageList.')
            trackeeList.remove(user)
    writeJsonData(oldJsonData)
    print('Hard reset done')
    return


def getFriendList(user):
    friendList = api.friends_ids(user)
    return friendList


def seperateNewfromOld(newList, oldList):
    difference = list(set(newList) - set(oldList))
    return difference


def compare():
#-------------------- Defining function scope variables -
    messageList = []
    oldJsonData = loadJsonFile()
#-------------------- Helper functions ------------------
    def appendMessageList(trackee, listOfNewFollowers):
        for newUsers in listOfNewFollowers:
            getNewUserInfo = api.get_user(str(newUsers))._json
            temp_message = '@' + trackee + '  just followed https://twitter.com/' + \
                getNewUserInfo['screen_name'] + \
                f'\nFollower : {getNewUserInfo["followers_count"]} '
            try:
                followerCount = int(getNewUserInfo["followers_count"])
                if followerCount < 500:
                    temp_message += '🔴'
                elif followerCount < 3000:
                    temp_message += '🟡'
                else:
                    temp_message += '🟢'
                temp_message += f'\Website: {getNewUserInfo["url"]}'
            except:
                print('Error in sending telegram message')
            messageList.append(temp_message)
        return

    def appendNewTrackee(trackee, newTrackeeData):  # added new user to track
        print('new user: ', trackee)
        oldJsonData[trackee] = newTrackeeData
        messageToSendTelegram = f'Bot is following new user :@{trackee}'
        bot.send_message(chat_id='', text=messageToSendTelegram)
        return
#----------------------------- Logic ----------------------------
    for trackee in trackeeList:
        print(f'Screning {trackee}')
        
        try:
            friendListFromApi = getFriendList(trackee)
        except:
            print(f'API could not fetch {trackee} details, please check if ID and messageList.')
            trackeeList.remove(trackee)
            continue
        
        try:
            newFriendList = seperateNewfromOld(friendListFromApi, oldJsonData[trackee])
        except:  # oldData[trackee] might not exist because of new trackee added into the list of trackeeList
            appendNewTrackee(trackee, friendListFromApi)
            
        oldJsonData[trackee] = friendListFromApi # Update json file data
        appendMessageList(trackee, newFriendList)
        
    writeJsonData(oldJsonData)
    for sendMessage in messageList:
        bot.send_message(chat_id='', text=sendMessage)


def _main():
    try:
        while True:
            compare()
    except:
        print('error')
        return _main()

_main()
# hardReset()

# compare()
