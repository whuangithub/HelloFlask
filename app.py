from flask import Flask
from flask import render_template
from flask import escape
from flask import url_for # to generate URL

app = Flask(__name__)

name = 'H W'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

@app.route("/")
def index():
    return render_template('index.html', name=name, movies=movies)

@app.route("/hello") # root address
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name) # escape: prevent the "name" contains toxic code

@app.route("/test")
def test_url_for():
    # the following "print" output in the terminal (not webpage)
    print(url_for('index'))  # /
    print(url_for('user_page', name='greyli'))  # /user/greyli
    print(url_for('user_page', name='peter'))  # /user/peter
    print(url_for('test_url_for'))  # /test
    print(url_for('test_url_for', num=2))  # /test?num=2 (too many input parameters)
    return 'Test page'
