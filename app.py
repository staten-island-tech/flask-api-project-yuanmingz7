from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    response = requests.get("https://api.disneyapi.dev/character")
    data = response.json()
    disney_list = data['results']
    
    disneys = []
    
    for disney in disney_list:
        url = disney['url']
        parts = url.strip("/").split("/")
        id = parts[-1]  
        

        image_url = disney.get('image_url', '')
        
        disneys.append({
            'name': disney['name'].capitalize(),
            'id': id,
            'image': image_url
        })
        # Fetching Disney films
    film_response = requests.get("https://api.disneyapi.dev/films")
    film_data = film_response.json()
    films = film_data['results'] if 'results' in film_data else []

    return render_template("index.html", disneys=disneys)

@app.route("/disney/<int:id>")
def film_detail(id):
    response = requests.get(f"https://api.disneyapi.dev/films/{id}")
    data = response.json()

    title = data.get('title', 'Unknown Film')
    release_date = data.get('release_date', 'Unknown')
    description = data.get('description', 'No description available')
    image_url = data.get('image_url', '')

    return render_template("film_detail.html", film={
        'title': title,
        'release_date': release_date,
        'description': description,
        'image': image_url,
    })

if __name__ == '__main__':
    app.run(debug=True)
