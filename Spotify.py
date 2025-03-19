import requests
import pandas as pd  

# Initialize your client ID and client secret from Spotify Developer Dashboard
spotify_client_id = 'client_Id'  
spotify_client_secret = 'client_secret'  

# Fetch an access token from Spotify
token_response = requests.post(
    'https://accounts.spotify.com/api/token',
    data={
        'grant_type': 'client_credentials',  
        'client_id': spotify_client_id,  
        'client_secret': spotify_client_secret  
    }
)

token_data = token_response.json() 
access_token = token_data['access_token']

# Prepare headers for API requests
api_headers = {'Authorization': f'Bearer {access_token}'} 

# Load your existing CSV file into a DataFrame
spotify_data = pd.read_csv('D:/xprojects/power bi/VizGpt/spotify-2023.csv') 

# Create an empty list to store cover URLs
album_cover_urls = []

# Loop through each row in the DataFrame to search for tracks on Spotify
for _, track_info in spotify_data.iterrows():
    song_name = track_info['track_name']  
    artist_name = track_info['artist(s)_name'] 
    search_query = f"track:{song_name} artist:{artist_name}" 
    
    # Search for the track on Spotify
    search_request = requests.get(
        f"https://api.spotify.com/v1/search?q={search_query}&type=track", 
        headers=api_headers 
    )
    search_results = search_request.json()  

    # Try to fetch the cover URL, otherwise append 'Not Found'
    try:
        album_cover_url = search_results['tracks']['items'][0]['album']['images'][0]['url']  
    except (KeyError, IndexError):
        album_cover_url = 'Not Found'
    
    album_cover_urls.append(album_cover_url)  

# Add the list of cover URLs as a new column to the DataFrame
spotify_data['cover_url'] = album_cover_urls  

# Save the updated DataFrame as a new CSV file
spotify_data.to_csv('updated_spotify_data.csv', index=False)  
