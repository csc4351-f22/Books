import requests


API_KEY="AIzaSyAzQ4m3dQxsPBIOXjh0JFvZwunq3ekfeIU"

def get_books(query):

    response = requests.get(
        "https://www.googleapis.com/books/v1/volumes",
        params = {"q":query, "api-key": API_KEY},
        )

    response_json = response.json()
    titles = []
    images = []
  
    titles = response_json['items'][0]['volumeInfo']['title']
    images = response_json['items'][0]['volumeInfo']['imageLinks']['thumbnail']

    return [titles, images]

