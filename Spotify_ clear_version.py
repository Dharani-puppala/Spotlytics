import requests
import pandas as pd

# Function to get Spotify access token
def fetch_spotify_token(api_key, api_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, data={
        'grant_type': 'client_credentials',
        'client_id': api_key,
        'client_secret': api_secret,
    })
    auth_data = auth_response.json()
    return auth_data['access_token']

# Function to search for a track and get its ID
def find_track_id(track_title, artist_name, token):
    search_query = f"{track_title} artist:{artist_name}"
    search_url = f"https://api.spotify.com/v1/search?q={search_query}&type=track"
    search_response = requests.get(search_url, headers={
        'Authorization': f'Bearer {token}'
    })
    response_data = search_response.json()
    try:
        top_result = response_data['tracks']['items'][0]
        track_identifier = top_result['id']
        return track_identifier
    except (KeyError, IndexError):
        return None

# Function to get track details
def fetch_track_details(track_identifier, token):
    track_url = f"https://api.spotify.com/v1/tracks/{track_identifier}"
    track_response = requests.get(track_url, headers={
        'Authorization': f'Bearer {token}'
    })
    track_data = track_response.json()
    cover_image_url = track_data['album']['images'][0]['url']
    return cover_image_url

# Spotify API Credentials
api_key = 'client_id'  
api_secret = 'client_secret'  

# Get Access Token
access_token = fetch_spotify_token(api_key, api_secret)

# Read your DataFrame (replace 'your_file.csv' with the path to your CSV file)
spotify_data = pd.read_csv('your_file.csv', encoding='ISO-8859-1')

# Loop through each row to get track details and add to DataFrame
for idx, track_info in spotify_data.iterrows():
    track_identifier = find_track_id(track_info['track_name'], track_info['artist_name'], access_token)
    if track_identifier:
        cover_image_url = fetch_track_details(track_identifier, access_token)
        spotify_data.at[idx, 'cover_image_url'] = cover_image_url

# Save the updated DataFrame (replace 'updated_file.csv' with your desired output file name)
spotify_data.to_csv('updated_file.csv', index=False)
