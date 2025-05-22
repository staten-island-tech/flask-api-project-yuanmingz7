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
        response = requests.get(f"https://api.chess.com/pub/player/{username}")

        if response.status_code == 200:
            data = response.json()
            player_data = {
                'username': data.get('username'),
                'name': data.get('name', 'N/A'),
                'title': data.get('title', 'N/A'),
                'status': data.get('status', 'N/A'),
                'country': data.get('country').split('/')[-1] if data.get('country') else 'Unknown',
                'followers': data.get('followers', 0),
                'joined': data.get('joined'),
                'last_online': data.get('last_online'),
                'avatar': data.get('avatar', '/static/default-avatar.png')  # fallback avatar
            }
        else:
            error = f"Player '{username}' not found or an error occurred."

    return render_template("index.html", player=player_data, error=error)

# Detailed stats route
@app.route("/player/<username>")
def player_detail(username):
    response = requests.get(f"https://api.chess.com/pub/player/{username}/stats")

    if response.status_code != 200:
        return f"Stats for '{username}' not available", 404

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
