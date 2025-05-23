from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Home route - search form and basic profile info
@app.route("/", methods=["GET", "POST"])
def index():
    player_data = None
    error = None

    if request.method == "POST":
        username = request.form.get("username").lower()  # Ensure lowercase for API
        response = requests.get(f"https://api.chess.com/pub/player/{username}", headers={"User-Agent": "Mozilla"})
        print(response)
        player_data = response.json()
      

    return render_template("index.html", player=player_data, error=error)

# Detailed stats route
@app.route("/player/<username>")
def player_detail(username):
    response = requests.get(f"https://api.chess.com/pub/player/{username}/stats")

    if response.status_code != 200:
        return render_template("error.html", error = f"Stats for '{username}' not available")
    else:
        data = response.json()

        stats = {
            'chess_rapid': data.get('chess_rapid', {}).get('last', {}),
            'chess_blitz': data.get('chess_blitz', {}).get('last', {}),
            'chess_bullet': data.get('chess_bullet', {}).get('last', {}),
            'chess_daily': data.get('chess_daily', {}).get('last', {})
        }

        return render_template("player.html", username=username, stats=stats)

if __name__ == '__main__':
    app.run(debug=True)
