from flask import Flask
from flask import escape
from flask import url_for # to generate URL

app = Flask(__name__)

@app.route("/") # root address
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name) # escape: prevent the "name" contains toxic code

@app.route("/test")
def test_url_for():
    # the following "print" output in the terminal (not webpage)
    print(url_for('hello'))  # /
    print(url_for('user_page', name='greyli'))  # /user/greyli
    print(url_for('user_page', name='peter'))  # /user/peter
    print(url_for('test_url_for'))  # /test
    print(url_for('test_url_for', num=2))  # /test?num=2 (too many input parameters)
    return 'Test page'
