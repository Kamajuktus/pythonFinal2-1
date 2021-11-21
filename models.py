from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:333btybfRA@127.0.0.1:5433/News'    
db = SQLAlchemy(app)

""" News Model """
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    def __repr__(self):
        return '<Users %r>' % self.login

class News(db.Model):
    __tablename__ = 'News'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String)
    link = db.Column('link', db.String)
    paragraphs = db.Column('paragraphs', db.Text)

    def __init__(self, id, title, link, paragraphs):
        self.id = id
        self.title = title
        self.link = link
        self.paragraphs = paragraphs
    
    
    def find_id():
        news = News.query.all()
        return len(news)
        
def addNews(new_title, new_link, new_paragraphs):
        
        news = News(News.find_id()+1, new_title, new_link, new_paragraphs)
        db.session.add(news)
        db.session.commit()

def getTheNews():
        news = News.query.all()   
        news = news[-1:]
        return news
        

""" Use this command to implement the database 1 time"""
# db.create_all()

