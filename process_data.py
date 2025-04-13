import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os
from PIL import Image, ImageDraw
import requests
from io import BytesIO
import time

# Create output directory
os.makedirs('output', exist_ok=True)

print("Processing NBA player statistics for visualization...")

# Load the player statistics data
df = pd.read_csv('data/nba_player_stats.csv')

# Display basic information about the dataset
print(f"Total number of players: {len(df)}")
print(f"Columns in the dataset: {', '.join(df.columns)}")

# Filter players with minimum games played to ensure meaningful data
min_games = 20
filtered_df = df[df['GP'] >= min_games].copy()
print(f"Players with at least {min_games} games played: {len(filtered_df)}")

# Calculate points per field goal attempt (scoring efficiency)
filtered_df['PTS_per_FGA'] = filtered_df['PTS'] / filtered_df['FGA']
filtered_df['PTS_per_FGA'] = filtered_df['PTS_per_FGA'].replace([np.inf, -np.inf], np.nan)
filtered_df = filtered_df.dropna(subset=['PTS_per_FGA'])

# Sort by total points
filtered_df = filtered_df.sort_values('PTS', ascending=False)

# Select top 50 players by points for visualization
top_players = filtered_df.head(50)
print(f"Selected top {len(top_players)} players by points for visualization")

# Display the top 10 players and their stats
print("\nTop 10 players by points:")
print(top_players[['PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'PTS', 'FGA', 'PTS_per_FGA']].head(10))

# Calculate quartiles for PTS and FGA to determine quadrant boundaries
pts_median = top_players['PTS'].median()
fga_median = top_players['FGA'].median()

print(f"\nMedian values for quadrant boundaries:")
print(f"Points (PTS) median: {pts_median}")
print(f"Field Goal Attempts (FGA) median: {fga_median}")

# Create a function to determine the quadrant for each player
def get_quadrant(row):
    if row['PTS'] >= pts_median and row['FGA'] >= fga_median:
        return "High Points, High Attempts"
    elif row['PTS'] >= pts_median and row['FGA'] < fga_median:
        return "High Points, Low Attempts"
    elif row['PTS'] < pts_median and row['FGA'] >= fga_median:
        return "Low Points, High Attempts"
    else:
        return "Low Points, Low Attempts"

# Add quadrant information to the dataframe
top_players['Quadrant'] = top_players.apply(get_quadrant, axis=1)

# Count players in each quadrant
quadrant_counts = top_players['Quadrant'].value_counts()
print("\nPlayers in each quadrant:")
print(quadrant_counts)

# Create a function to generate placeholder avatars for players
def create_placeholder_avatar(player_name, team_abbr, size=(100, 100)):
    # Create a blank image with a team color background
    img = Image.new('RGB', size, color=(200, 200, 200))
    draw = ImageDraw.Draw(img)
    
    # Add player initials
    initials = ''.join([name[0] for name in player_name.split() if name[0].isupper()])
    if not initials:
        initials = player_name[:2].upper()
    
    # Draw the initials in the center
    draw.text((size[0]//2, size[1]//2), initials, fill=(0, 0, 0))
    
    # Add team abbreviation at the bottom
    draw.text((size[0]//2, size[1]-15), team_abbr, fill=(0, 0, 0))
    
    return img

# Try to get NBA player headshots from NBA.com using a different approach
def get_player_avatar(player_id, player_name, team_abbr):
    # NBA.com headshot URL format
    url = f"https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            print(f"Could not get image for {player_name}, creating placeholder")
            return create_placeholder_avatar(player_name, team_abbr)
    except Exception as e:
        print(f"Error getting image for {player_name}: {e}")
        return create_placeholder_avatar(player_name, team_abbr)

# Create a directory for player avatars if it doesn't exist
os.makedirs('images/avatars', exist_ok=True)

# Get or create avatars for each player in the top players list
print("\nGetting player avatars...")
for idx, player in top_players.iterrows():
    player_id = player['PLAYER_ID']
    player_name = player['PLAYER_NAME']
    team_abbr = player['TEAM_ABBREVIATION']
    
    # Create a clean filename
    clean_name = "".join(c if c.isalnum() else "_" for c in player_name)
    avatar_path = f'images/avatars/{clean_name}_{player_id}.png'
    
    # Check if we already have the avatar
    if not os.path.exists(avatar_path):
        print(f"Getting avatar for {player_name}...")
        avatar = get_player_avatar(player_id, player_name, team_abbr)
        avatar.save(avatar_path)
        # Sleep briefly to avoid rate limiting
        time.sleep(0.2)
    
    # Add the avatar path to the dataframe
    top_players.at[idx, 'AVATAR_PATH'] = avatar_path

# Save the processed data
top_players.to_csv('data/processed_players_for_visualization.csv', index=False)
print("\nProcessed data saved to data/processed_players_for_visualization.csv")

print("\nData processing completed successfully.")
