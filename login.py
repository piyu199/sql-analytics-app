
from user import User
from database import Database
from twitter_util import consumer,get_request_token,get_oauth_verifier,get_access_token


Database.initialise(database="Learning",user="postgres",password="dasnadas",host="localhost")
user_email=input("Enter your email address:")
user=User.load_to_db_by_email(user_email)

if not user:

    request_token = get_request_token()

    oauth_verifier = get_oauth_verifier(request_token)

    access_token=get_access_token(request_token,oauth_verifier)

    first_name=input("Enter your first_name")

    last_name=input("Enter your last_name")

    user=User(user_email,first_name,last_name,access_token['oauth_token'],access_token['oauth_token_secret'],None)

    user.save_to_database()

tweets= user.twitter_request("https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images",'GET')

for tweet in tweets['statuses']:
    print(tweet['text'])


