import flask
import os

app = flask.Flask(__name__)
images_folder = os.path.join('static', 'images')

app.config['upload_folder'] = images_folder

Books = [ "Harry potter", "Kidagaa kimemwozea", "The Silent Patient", "To Kill a Mockingbird", "The River and The Source"]
@app.route("/")
def index():
    images_list = os.listdir('static/images')
    images_list = ['static/images/'+ i for i in images_list]
    return flask.render_template(
        "index.html",
        imagelist=images_list,
        len = len(Books), 
        Books = Books,
        
        )

app.run(use_reloader= True, debug=True)