# Import required Libraries 
import requests
import pandas as po
# Initsalize your client ID and client secret from Spotify Developer Dashbooard
CLIENT, ID = 'client_Id '
CLIENT, SECRET = 'client _secret'
# Fetch an access token from Spotify
auth_response = requests.post(
            'https://accounts.spotify.com/api/token',
             * data={'grant_type'; 'client cxedentiale', 'client_id'; CLIENT_ID, 'clie
)
auth,data = auth_response.json()
access_token = auth_data['access_token']

# Prepare headers for API requests
headers = {'Authorization': f'Bearer {access_token}'}

# Load your existing CSV file into a DataFrame
* df = pd.read_csv('D:/xprojects/power bi/VizGpt/spotify-2023.csv')

# Create an empty list to store cover URLS
cover urls = []

# Loop through each row in the DataFrame to search for tracks on Spotify
for _, row in df.iterrows():
  track_name = row['track_name ']
  artist _name = row['artist(s) _name']
  query = f"track:{track_name} artist:{artist_name}"
 * search response = requests.get(f"https://api.spotify.com/v1/search?q=(qu
  search_data = search_response.json()

try:
  *cover url = search_data['tracks']['items'][O]['album']['images'][0][
except (KeyError, IndexError):
  cover_url = 'Not Found'
  cover_urls.append(cover_url)

# Add the list of cover URLs as a new column to the DataFrame
df['cover_url'] = cover_urls
# Save the updated DataFrame as a new CSV file
df.to_csv('updated _spotify_data.csv', index=False)
