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
        id = _id[-1]  
        

        image_url = f""
        
        disneys.append({
            'name': disney['name'].capitalize(),
            'id': id,
            'image': image_url
        })
    
    return render_template("index.html", disneys=disneys)

@app.route("/disney/<int:id>")
def disney_detail(id):
    response = requests.get(f"https://api.disneyapi.dev/character/{id}")
    data = response.json()
    
    types = [t['type']['name'] for t in data['types']]
    height = data.get('height')
    name = data.get('name').capitalize()
    image_url = f""
    

    return render_template("disney.html", disney={
        'name': name,
        'id': id,
        'image': image_url,
        'types': types,
        'height': height,
    })

if __name__ == '__main__':
    app.run(debug=True)
