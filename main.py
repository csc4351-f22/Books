import flask
from gbookapi import get_books
import os

app = flask.Flask(__name__)
images_folder = os.path.join('static', 'images')

app.config['upload_folder'] = images_folder

Books = [ "Harry potter", "Kidagaa kimemwozea", "The Silent Patient", "To Kill a Mockingbird", "The River and The Source"]

@app.route("/")
def index():

    imageslist = os.listdir('static/images')
    imageslist = ['static/images/'+ i for i in imageslist]

    form_data = flask.request.args
    query = form_data.get("term", "harry")
    Books = get_books(query)
    imagelist= get_books(query)

    return flask.render_template(
        "index.html",
        Books = Books,
        imagelist = imagelist
    )


app.run(use_reloader= True, debug=True)

