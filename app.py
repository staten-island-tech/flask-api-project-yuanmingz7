from flask import Flask, render_template, request
import requests

app = Flask(__name__)

searched_players = []

@app.route("/", methods=["GET", "POST"])
def index():
    player_data = None
    error = None

    if request.method == "POST":
        username = request.form.get("username").lower()
        response = requests.get(
            f"https://api.chess.com/pub/player/{username}",
            headers={"User-Agent": "Mozilla"}
        )

        if response.status_code == 200:
            player_data = response.json()

            if player_data and username not in [p['username'] for p in searched_players]:
                searched_players.append({
                    'username': player_data.get('username'),
                    'avatar': player_data.get('avatar'),
                    'name': player_data.get('name'),
                    'title': player_data.get('title'),
                    'status': player_data.get('status'),
                    'country': player_data.get('country'),
                    'followers': player_data.get('followers')
                })
        else:
            error = f"User '{username}' not found."

    return render_template("index.html", player=player_data, players=searched_players, error=error)

@app.route("/player/<username>")
def player_detail(username):
    response = requests.get(
        f"https://api.chess.com/pub/player/{username}/stats",
        headers={"User-Agent": "Mozilla"}
    )

    if response.status_code != 200:
        return render_template("error.html", error=f"Stats for '{username}' not available")

    data = response.json()

    stats = {
        'chess_rapid': data.get('chess_rapid', {}).get('last', {}),
        'chess_blitz': data.get('chess_blitz', {}).get('last', {}),
        'chess_bullet': data.get('chess_bullet', {}).get('last', {}),
        'chess_daily': data.get('chess_daily', {}).get('last', {})
    }

    return render_template("player.html", username=username, stats=stats)

if __name__ == "__main__":
    app.run(debug=True)
