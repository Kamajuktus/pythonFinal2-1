from datetime import datetime, timedelta
from flask import Flask
from flask.helpers import make_response, url_for
from flask import request
from flask.templating import render_template
import jwt
from werkzeug.utils import redirect
from settings import insertResults
from flask_sqlalchemy import SQLAlchemy
from models import News
import re
from bs4 import BeautifulSoup
from transformers import pipeline
import requests

from settings import GetResults

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisismyflasksecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:333btybfRA@127.0.0.1:5433/News'    
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    token = db.Column(db.String(120), unique=True, nullable=False)
    def __repr__(self):
        return '<Users %r>' % self.login



def get_url(cryptoname):
    rawURL = db.session.query(News.link).filter_by(title = cryptoname).order_by(News.id.desc()).first()
    URL = re.sub("[(),']", "", str(rawURL), 0, 0)
    print(str(URL))
    return str(URL)

def summarize(cryptoname):
    summarizer = pipeline("summarization")
    r = requests.get(get_url(cryptoname))

    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all(['h1', 'p'])
    text = [result.text for result in results]
    ARTICLE = ' '.join(text)

    max_chunk = 500

    ARTICLE = ARTICLE.replace('.', '.<eos>')
    ARTICLE = ARTICLE.replace('?', '?<eos>')
    ARTICLE = ARTICLE.replace('!', '!<eos>')

    sentences = ARTICLE.split('<eos>')
    current_chunk = 0 
    chunks = []
    for sentence in sentences:
        if len(chunks) == current_chunk + 1: 
            if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(' '))
            else:
                current_chunk += 1
                chunks.append(sentence.split(' '))
        else:
            print(current_chunk)
            chunks.append(sentence.split(' '))

    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = ' '.join(chunks[chunk_id])

    res = summarizer(chunks, max_length=120, min_length=30, do_sample=False)

    ' '.join([summ['summary_text'] for summ in res])

    text = ' '.join([summ['summary_text'] for summ in res])

    return text

@app.route('/')
def login():
    auth = request.authorization

    if auth and (Users.query.filter_by(login=auth.username).first()!=None):
        if (Users.query.filter_by(login=auth.username).first().password == auth.password):
            newToken = jwt.encode({'user':auth.username, 'exp':datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
            Users.query.filter_by(login=auth.username).update({"token":newToken})
            return redirect(url_for("coin", token=newToken))

    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


@app.route('/coin', methods=['POST', 'GET'])
def coin():
    if request.method == "POST":
         result = request.form["cryptoname"]
         return redirect(url_for("result", cryptoname=result))
    else:
        return render_template('index.html')

@app.route('/<cryptoname>')
def result(cryptoname):
    insertResults(cryptoname)
    result = summarize(cryptoname)
    for news in GetResults():
        paged = news.link
        paged1 = news.paragraphs
    return render_template('result_page.html', content = result, blog = paged, para = paged1)
    

if __name__ == '__main__':
    app.run(debug=True)


    