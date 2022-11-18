import flask
import requests
from flask_sqlalchemy import SQLAlchemy
import os

API_KEY="AIzaSyAzQ4m3dQxsPBIOXjh0JFvZwunq3ekfeIU"

querys = ["Harry potter deathly", "To Sleep in a Sea of Stars", "Silent Patient", "To Kill a Mockingbird", "Throne of Glass"]

titles = []
images = []

ggtitles=[]
ggauthors=[]
ggimages=[]
ggsubtitles=[]

for query in querys:
    response = requests.get(
        "https://www.googleapis.com/books/v1/volumes", 
        params={"q": query, "key": API_KEY}
    )

    response = response.json()
    titles.append(response["items"][0]['volumeInfo']['title'])
    images.append(response["items"][0]['volumeInfo']["imageLinks"]['thumbnail'])

app = flask.Flask(__name__)

books = ["Harry potter", "To Sleep in a Sea of Stars", "Silent Patient", "To Kill a Mockingbird", "Throne of Glass"]

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.db")

db = SQLAlchemy(app)

class Booksbase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(80))
    Subtitle = db.Column(db.String(80))
    Author = db.Column(db.String(80))
    Thumbnail = db.Column(db.String(80))

with app.app_context():
    db.create_all()

@app.route("/add", methods=["GET", "POST"])
def add():
    if flask.request.method =="POST":
        data = flask.request.form
        new_Books = Booksbase(
            Title = data["Title"],
            Subtitle = data["Subtitle"],
            Author = data["Author"],
            Thumbnail = data["Thumbnail"]
        )
        db.session.add(new_Books)
        db.session.commit()
        return flask.redirect("/")

@app.route("/delete", methods = ["POST"])
def delete(): 
    Title_to_delete = flask.request.form.get('title_book')
    to_delete = Booksbase.query.filter_by(Title = Title_to_delete).first()
    db.session.delete(to_delete)
    db.session.commit()
    return flask.redirect("/")

@app.route("/")
def index():
    ggtitles=[]
    ggauthors=[]
    ggimages=[]
    ggsubtitles=[]

    form_data = flask.request.args

    print ("\n\n\n")
    print(form_data)
    print ("\n\n\n")

    Query = form_data.get("term", "")

    response = requests.get(
    "https://www.googleapis.com/books/v1/volumes?", 
    params={"q": Query, "key": API_KEY}
    )
    response = response.json()

    # https://www.w3schools.com/python/python_try_except.asp
    # https://www.geeksforgeeks.org/python-try-except/

    # i used try and except because it gives me KeyError: 'imageLinks' or 'subtitles'
    # which means that some books do not have those information

    for i in range(5):
        try:
            ggtitles.append(response["items"][i]['volumeInfo']['title'])
        except:
            print("")
        try:
            ggsubtitles.append(response["items"][i]['volumeInfo']['subtitle'])
        except:
            print("error for subtitle")

        try:
            ggauthors.append(response["items"][i]['volumeInfo']['authors'])
        except:
            print("")
        try:
            ggimages.append(response["items"][i]['volumeInfo']['imageLinks']['thumbnail'])
        except:
            print("error for image")
        
    data_titles = Booksbase.query.all()
    fav_books = len(data_titles)
    return flask.render_template(
        "index.html", 
        data_titles=data_titles, 
        fav_books=fav_books,
        ggtitles=ggtitles,
        ggauthors = ggauthors,
        ggimages =ggimages,
        ggsubtitles=ggsubtitles
        )

app.run(use_reloader= True,debug=True)
