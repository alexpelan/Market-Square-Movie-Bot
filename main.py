import urllib
import tweepy

#twitter API 
consumer_key = "qwep0aJuygFMPJtcZKpoCQ"
consumer_secret = "imnotreallygoingtopostthistogithub" #LOL
access_token = "537816100-Z66b3qzeueaZugVsZWxWLu0pw7NuQp6iXKg0at36"
access_token_secret = "CWg12ArgCreCsP6FhEtSGJaq8krMdEhJb6ZtilAT4"

#oauth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

file = urllib.urlopen("http://www.marketsquareodanaroad.com/movies.html")
contents=file.read()
index=contents.find("<tr") #just ignore the first and second rows - it's all headers
index=contents.find("<tr",index+1)  
start_tag=0
end_tag=0
substr=""
movies = []
while(index != -1):
    index=contents.find("<tr",index+1)
    start_tag=contents.find("<td",index)
    end_tag=contents.find("</td>",index)
    if end_tag!=-1 and start_tag!=-1:
        substr=contents[start_tag:end_tag]
        end_td_tag=substr.find(">")
        movies.append(substr[end_td_tag+1:])
    else:
        index = -1
x=movies.pop() #last row is bad too

tweets=[]

#construct the full text we want tweeted
tweet = "Movies this week: "
counter = 0;
for movie in movies:
    if counter != 0:
        tweet += ", "
    tweet += movie
    counter += 1
tweet += ". Times:  http://bit.ly/HigCLv"

#split the tweets. Almost every time we're gonna get all the movie titles in two tweets or less. The median movie title is
# 14 characters, and it would require 6 movies with 40 character titles to take up two tweets. So we're going to split
# before the last movie title so that the last tweet, if it's too long, will at least have a movie title and the link 
#in it. 

last_comma_index=10000
second_tweet = ""

if len(tweet) <=140:
    api.update_status(tweet)
else:
    while True:
        last_comma_index = tweet.rfind(",",0,last_comma_index)
        if last_comma_index <= 137:
            break
    second_tweet = "..." + tweet[last_comma_index+2:]
    tweet = tweet[:last_comma_index] + "..."
    api.update_status(tweet)
    
api.update_status(second_tweet)


file.close()
