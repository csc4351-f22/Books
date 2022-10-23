import flask
import requests

API_KEY="AIzaSyAzQ4m3dQxsPBIOXjh0JFvZwunq3ekfeIU"

querys = ["Harry potter", "To Sleep in a Sea of Stars", "Silent Patient", "To Kill a Mockingbird", "Throne of Glass"]

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

books = ["Harry potter", "To Sleep in a Sea of Stars", "Silent Patient", "To Kill a Mockingbird", "The River and The Source"]

@app.route("/")
def index():

    form_data = flask.request.args

    print ("\n\n\n")
    print(form_data)
    print ("\n\n\n")

    Query = form_data.get("term", "")

    response = requests.get(
    "https://www.googleapis.com/books/v1/volumes", 
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
            ggsubtitles.append(response["items"][i]['volumeInfo']['subtitles'])
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
        


    return flask.render_template(
        "index.html", 
        titles=titles, 
        images=images,
        ggtitles=ggtitles,
        ggauthors = ggauthors,
        ggimages =ggimages,
        ggsubtitles=ggsubtitles
        )

app.run(use_reloader= True,debug=True)