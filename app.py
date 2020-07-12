from flask import Flask
from flask import render_template
from flask import escape
from flask import url_for # to generate URL
from flask import request
from flask import redirect
from flask import flash

from flask_sqlalchemy import SQLAlchemy

import os
import click

app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'

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

# context_processor: set user in all view function to user
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user) # must return a dictionary, this function returns {'user': user}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页

    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录

@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页

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

@app.errorhandler(404)  # to handle the error code 404
def page_not_found(e):  # 接受异常对象作为参数
    user = User.query.first()
    return render_template('404.html'), 404  # 返回模板和状态码
