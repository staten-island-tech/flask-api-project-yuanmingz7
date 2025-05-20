from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    profile = None
    if request.method == "POST":
        username = request.form["username"]
        profile = fetch_player_profile(username)
    return render_template("index.html", profile=profile)

def fetch_player_profile(username):
    url = f"https://api.chess.com/pub/player/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

if __name__ == "__main__":
    app.run(debug=True)