
import requests



def fetch_player_profile(username):
    url = f"        "
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            
    except requests.exception.HTTPError:   
        print ("No")
         
    else:
        print (data)

fetch_player_profile("Hikaru")