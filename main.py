import flask
import requests
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
APIKEY = os.getenv("APIKEY")

app = flask.Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres: // lwyipltpevmqly: ad4c58880a29e1bbf9b193a639e7b4fe7deef31e354d6383c65f0538c71cf5be@ec2-54-208-11-146.compute-1.amazonaws.com: 5432/d3uk7d3m4b58gm"

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
    if flask.request.method == "POST":
        data = flask.request.form
        authors = data.getlist("Author")
        # Join the author names with commas
        author_str = ', '.join(authors)
        new_Books = Booksbase(
            Title=data.get("Title"),
            Subtitle=data.get("Subtitle"),
            Author=author_str,
            Thumbnail=data.get("Thumbnail")
        )
        db.session.add(new_Books)
        db.session.commit()
        return flask.redirect("/library")


@app.route("/delete", methods=["POST"])
def delete():
    Title_to_delete = flask.request.form.get('title_book')
    to_delete = Booksbase.query.filter_by(Title=Title_to_delete).first()
    db.session.delete(to_delete)
    db.session.commit()
    return flask.redirect("/library")


@app.route("/", methods=["GET", "POST"])
def index():
    ggtitles = []
    ggauthors = []
    ggimages = []
    ggsubtitles = []

    form_data = flask.request.args

    print("\n\n\n")
    print(form_data)
    print("\n\n\n")

    Query = form_data.get("term", "")

    response = requests.get(

        "https://www.googleapis.com/books/v1/volumes?",
        params={"q": Query, "key": APIKEY}
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
            ggauthors.append(
                ', '.join(response["items"][i]['volumeInfo']['authors']))

        except:
            print("")
        try:
            ggimages.append(response["items"][i]
                            ['volumeInfo']['imageLinks']['thumbnail'])
        except:
            print("error for image")

    return flask.render_template(
        "index.html",
        ggtitles=ggtitles,
        ggauthors=ggauthors,
        ggimages=ggimages,
        ggsubtitles=ggsubtitles
    )


@app.route("/library/", methods=["GET", "POST"])
def Library():
    ggtitles = []
    ggauthors = []
    ggimages = []
    ggsubtitles = []

    data_titles = Booksbase.query.all()
    fav_books = len(data_titles)
    return flask.render_template(
        "library.html",
        data_titles=data_titles,
        fav_books=fav_books,
        ggtitles=ggtitles,
        ggauthors=ggauthors,
        ggimages=ggimages,
        ggsubtitles=ggsubtitles
    )


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
