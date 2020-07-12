from flask import Flask
from flask import render_template
from flask import escape
from flask import url_for # to generate URL

from flask_sqlalchemy import SQLAlchemy

import os
import click

app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')

# inherit db.Model
class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    # attribute is instance of db.Column
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份

# function to add data to database
@app.cli.command()
def data_init():
    db.drop_all()
    db.create_all()

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

    user = User(name=name)
    db.session.add(user)
    for item in movies:
        mv = Movie(title=item['title'], year=item['year'])
        db.session.add(mv)
    db.session.commit()
    # click.echo('Done.')

@app.route("/")
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)

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
