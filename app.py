import os
import json
from flask_pymongo import PyMongo
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'cse391'
app.config['MONGO_URI'] = 'mongodb://admin:ahihi123@ds014118.mlab.com:14118/cse391'

mongo = PyMongo(app)

@app.route('/')
def home(data=None,post_data=None):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # return "Chào Boss!  <a href='/logout'>Logout</a>"
        posts = mongo.db.posts
        all_posts = posts.find({})
        return render_template('homepage.html', user_data=data, post_data=all_posts)


@app.route('/post', methods=['POST'])
def handle_data():
    posts = mongo.db.posts
    posts.insert({"article" :request.form['post_area']})
    post_article = request.form['post_area']
    all_posts = posts.find({})
    print(post_article)
    return render_template('homepage.html', post_data=all_posts)


@app.route('/login', methods=['POST'])
def do_admin_login():
    users = mongo.db.users
    existing_user = users.find_one({'name' : request.form['username'],
                                    'password' : request.form['password']})
    if existing_user is None:
        return render_template('register.html')
    else:
        session['logged_in'] = True
        return home(data=existing_user)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = request.form['password']
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return home()
        else:
            return 'Tài khoản đã được đăng kí!'
    return render_template('register.html')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()
 

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)
