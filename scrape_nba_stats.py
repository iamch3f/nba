import requests
import pandas as pd
import time
import json
from bs4 import BeautifulSoup
import os

# Create directories for data and images
os.makedirs('data', exist_ok=True)
os.makedirs('images', exist_ok=True)

# NBA Stats URL for player traditional stats
url = "https://www.nba.com/stats/players/traditional?PerMode=Totals&sort=PTS&dir=-1"

# Headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}

print("Attempting to fetch NBA player statistics...")

try:
    # Make the request to the NBA stats page
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Print the title to verify we got the right page
    print(f"Page title: {soup.title.text}")
    
    # Save the HTML for inspection
    with open('data/nba_stats_page.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    print("HTML content saved to data/nba_stats_page.html")
    
    # Try to find the table with player stats
    tables = soup.find_all('table')
    print(f"Found {len(tables)} tables on the page")
    
except Exception as e:
    print(f"Error fetching NBA stats: {e}")
    
# Since direct scraping might be challenging due to JavaScript rendering,
# let's try using the NBA API endpoints

# NBA API endpoint for player stats
api_url = "https://stats.nba.com/stats/leaguedashplayerstats"

# Parameters for the API request
params = {
    'MeasureType': 'Base',
    'PerMode': 'Totals',
    'PlusMinus': 'N',
    'PaceAdjust': 'N',
    'Rank': 'N',
    'LeagueID': '00',
    'Season': '2024-25',
    'SeasonType': 'Regular Season',
    'PORound': '0',
    'Outcome': '',
    'Location': '',
    'Month': '0',
    'SeasonSegment': '',
    'DateFrom': '',
    'DateTo': '',
    'OpponentTeamID': '0',
    'VsConference': '',
    'VsDivision': '',
    'GameSegment': '',
    'Period': '0',
    'LastNGames': '0',
    'PlayerExperience': '',
    'PlayerPosition': '',
    'StarterBench': '',
    'TeamID': '0',
    'GameScope': '',
    'PlayerID': '0'
}

# Headers specifically for the NBA API
api_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://www.nba.com',
    'Connection': 'keep-alive',
    'Referer': 'https://www.nba.com/',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}

print("\nAttempting to fetch data from NBA API...")

try:
    # Make the API request
    api_response = requests.get(api_url, headers=api_headers, params=params)
    api_response.raise_for_status()
    
    # Parse the JSON response
    data = api_response.json()
    
    # Save the raw JSON data
    with open('data/nba_player_stats.json', 'w') as f:
        json.dump(data, f)
    
    print("API data saved to data/nba_player_stats.json")
    
    # Try to extract the headers and rows
    if 'resultSets' in data and len(data['resultSets']) > 0:
        headers = data['resultSets'][0]['headers']
        rows = data['resultSets'][0]['rowSet']
        
        # Create a DataFrame
        df = pd.DataFrame(rows, columns=headers)
        
        # Save to CSV
        df.to_csv('data/nba_player_stats.csv', index=False)
        print("Player statistics saved to data/nba_player_stats.csv")
        
        # Print the first few rows to verify
        print("\nFirst 5 players by points:")
        print(df[['PLAYER_NAME', 'TEAM_ABBREVIATION', 'PTS', 'FGA']].head())
        
    else:
        print("Could not find expected data structure in API response")
        
except Exception as e:
    print(f"Error fetching from NBA API: {e}")

# Now let's try to get player images
print("\nSearching for player avatar images...")

# NBA player headshot URL template
headshot_url_template = "https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"

# Function to download player headshots
def download_player_image(player_id, player_name):
    image_url = headshot_url_template.format(player_id=player_id)
    try:
        img_response = requests.get(image_url, headers=headers)
        img_response.raise_for_status()
        
        # Clean player name for filename
        clean_name = "".join(c if c.isalnum() else "_" for c in player_name)
        
        # Save the image
        image_path = f'images/{clean_name}_{player_id}.png'
        with open(image_path, 'wb') as img_file:
            img_file.write(img_response.content)
        
        return image_path
    except Exception as e:
        print(f"Error downloading image for {player_name}: {e}")
        return None

# Try to download images for top players if we have the data
try:
    if 'df' in locals():
        print("Downloading player headshots for top 30 players...")
        
        # Add a column for image paths
        df['IMAGE_PATH'] = None
        
        # Download images for top 30 players by points
        top_players = df.sort_values('PTS', ascending=False).head(30)
        
        for _, player in top_players.iterrows():
            player_id = player['PLAYER_ID']
            player_name = player['PLAYER_NAME']
            
            print(f"Downloading image for {player_name}...")
            image_path = download_player_image(player_id, player_name)
            
            # Update the dataframe with the image path
            if image_path:
                df.loc[df['PLAYER_ID'] == player_id, 'IMAGE_PATH'] = image_path
                print(f"Downloaded image for {player_name}")
            
            # Sleep to avoid rate limiting
            time.sleep(0.5)
        
        # Save the updated dataframe
        df.to_csv('data/nba_player_stats_with_images.csv', index=False)
        print("Updated player statistics with image paths saved to data/nba_player_stats_with_images.csv")
    else:
        print("DataFrame not available, cannot download player images")
except Exception as e:
    print(f"Error in image download process: {e}")

print("\nData collection process completed.")
