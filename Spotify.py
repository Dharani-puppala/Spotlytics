import requests
import pandas as pd  # Fixed the import to use `pd` consistently

# Initialize your client ID and client secret from Spotify Developer Dashboard
CLIENT_ID = 'client_Id'  # Corrected variable name to CLIENT_ID
CLIENT_SECRET = 'client_secret'  # Corrected variable name to CLIENT_SECRET

# Fetch an access token from Spotify
auth_response = requests.post(
    'https://accounts.spotify.com/api/token',
    data={
        'grant_type': 'client_credentials',  # Fixed the incorrect syntax `';'` to `':'` and spelling
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
)

auth_data = auth_response.json()  # Fixed variable name typo
access_token = auth_data['access_token']

# Prepare headers for API requests
headers = {'Authorization': f'Bearer {access_token}'}

# Load your existing CSV file into a DataFrame
df = pd.read_csv('D:/xprojects/power bi/VizGpt/spotify-2023.csv')

# Create an empty list to store cover URLs
cover_urls = []  # Fixed variable name typo (was 'cover urls')

# Loop through each row in the DataFrame to search for tracks on Spotify
for _, row in df.iterrows():
    track_name = row['track_name']  # Removed extra space in column name
    artist_name = row['artist(s)_name']  # Fixed variable name typo and column name space
    query = f"track:{track_name} artist:{artist_name}"
    
    # Search for the track on Spotify
    search_response = requests.get(
        f"https://api.spotify.com/v1/search?q={query}&type=track", 
        headers=headers  # Added headers to the request
    )
    search_data = search_response.json()

    # Try to fetch the cover URL, otherwise append 'Not Found'
    try:
        cover_url = search_data['tracks']['items'][0]['album']['images'][0]['url']
    except (KeyError, IndexError):
        cover_url = 'Not Found'
    
    cover_urls.append(cover_url)  # Append the cover URL to the list

# Add the list of cover URLs as a new column to the DataFrame
df['cover_url'] = cover_urls

# Save the updated DataFrame as a new CSV file
df.to_csv('updated_spotify_data.csv', index=False)  # Fixed the file name for saving
