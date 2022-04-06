from flask import Flask,render_template,redirect,session,request,url_for,g
from twitter_util import get_request_token,get_access_token,get_oauth_verifier,get_oauth_verifier_url
from user import User
from database import Database

app = Flask(__name__)
app.secret_key="1234"
Database.initialise(database="Learning",user="postgres",password="dasnadas",host="localhost")

@app.before_request
def load_user():
    if 'screen_name' in session:
        g.user= User.load_to_db_by_screen_name(session['screen_name'])

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/login/twitter')
def twitter_login():
    if 'screen_name' in session:
        return redirect(url_for('profile'))
    request_token=get_request_token()
    session['request_token']= request_token

    return redirect(get_oauth_verifier_url(request_token))

@app.route("/auth/twitter")
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    access_token=get_access_token(session['request_token'],oauth_verifier)

    user=User.load_to_db_by_screen_name(access_token['screen_name'])
    if not user:
        user=User(access_token['screen_name'],access_token['oauth_token'],
                  access_token['oauth_token_secret'],None)
        user.save_to_database()

    session['screen_name']= user.screen_name
    return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    return render_template("profile.html",user=g.user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))

@app.route('/search')
def search():
    query=request.args.get('q')
    tweets = g.user.twitter_request("https://api.twitter.com/1.1/search/tweets.json?q={}".format(query))
    tweet_text=[tweet['text'] for tweet in tweets ['statuses']]
    return render_template("search.html",content=tweet_text)


app.run(port=4995, debug=True)

