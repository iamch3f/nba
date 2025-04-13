import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os
from PIL import Image
import matplotlib.patches as patches

# Create output directory
os.makedirs('output', exist_ok=True)

print("Creating four-quadrant chart visualization...")

# Load the processed player data
df = pd.read_csv('data/processed_players_for_visualization.csv')
print(f"Loaded data for {len(df)} players")

# Set up the figure and axis
plt.figure(figsize=(16, 12))
ax = plt.subplot(111)

# Get the quadrant boundaries
pts_median = df['PTS'].median()
fga_median = df['FGA'].median()

# Set axis limits with some padding
pts_max = df['PTS'].max() * 1.05
pts_min = df['PTS'].min() * 0.95
fga_max = df['FGA'].max() * 1.05
fga_min = df['FGA'].min() * 0.95

# Create the quadrant areas with light colors
# Q1: High Points, High Attempts (top right)
ax.add_patch(patches.Rectangle((fga_median, pts_median), fga_max - fga_median, pts_max - pts_median, 
                              alpha=0.1, facecolor='red', edgecolor='none'))
# Q2: High Points, Low Attempts (top left)
ax.add_patch(patches.Rectangle((fga_min, pts_median), fga_median - fga_min, pts_max - pts_median, 
                              alpha=0.1, facecolor='green', edgecolor='none'))
# Q3: Low Points, Low Attempts (bottom left)
ax.add_patch(patches.Rectangle((fga_min, pts_min), fga_median - fga_min, pts_median - pts_min, 
                              alpha=0.1, facecolor='blue', edgecolor='none'))
# Q4: Low Points, High Attempts (bottom right)
ax.add_patch(patches.Rectangle((fga_median, pts_min), fga_max - fga_median, pts_median - pts_min, 
                              alpha=0.1, facecolor='orange', edgecolor='none'))

# Draw the quadrant dividing lines
plt.axhline(y=pts_median, color='gray', linestyle='--', alpha=0.7)
plt.axvline(x=fga_median, color='gray', linestyle='--', alpha=0.7)

# Plot each player as a point
for idx, player in df.iterrows():
    plt.scatter(player['FGA'], player['PTS'], alpha=0.7, s=100)
    
    # Add player name as text label
    plt.annotate(player['PLAYER_NAME'], 
                 (player['FGA'], player['PTS']),
                 xytext=(5, 5),
                 textcoords='offset points',
                 fontsize=8)

# Add quadrant labels
plt.text(fga_max*0.95, pts_max*0.95, "High Volume Scorers", 
         ha='right', va='top', fontsize=12, weight='bold', color='darkred')
plt.text(fga_min*1.05, pts_max*0.95, "Efficient Scorers", 
         ha='left', va='top', fontsize=12, weight='bold', color='darkgreen')
plt.text(fga_min*1.05, pts_min*1.05, "Low Usage Players", 
         ha='left', va='bottom', fontsize=12, weight='bold', color='darkblue')
plt.text(fga_max*0.95, pts_min*1.05, "Volume Shooters", 
         ha='right', va='bottom', fontsize=12, weight='bold', color='darkorange')

# Set axis labels and title
plt.xlabel('Field Goal Attempts (FGA)', fontsize=14)
plt.ylabel('Points Scored (PTS)', fontsize=14)
plt.title('NBA Players: Scoring Output vs. Shot Attempts', fontsize=16, weight='bold')

# Add a diagonal reference line for points per field goal attempt = 1.0, 1.5, and 2.0
x_ref = np.linspace(fga_min, fga_max, 100)
for ratio, style in zip([1.0, 1.5, 2.0], ['-', '--', ':']):
    y_ref = x_ref * ratio
    plt.plot(x_ref, y_ref, linestyle=style, color='gray', alpha=0.5, 
             label=f'PTS/FGA = {ratio}')

# Add efficiency legend
plt.legend(loc='lower right')

# Add text explaining the quadrants
plt.figtext(0.02, 0.02, 
            "Quadrant Analysis:\n"
            "- Top Right: High volume scorers (high points, high attempts)\n"
            "- Top Left: Efficient scorers (high points, low attempts)\n"
            "- Bottom Left: Low usage players (low points, low attempts)\n"
            "- Bottom Right: Volume shooters (low points, high attempts)",
            fontsize=10)

# Save the basic chart without avatars
plt.tight_layout()
plt.savefig('output/nba_quadrant_chart_basic.png', dpi=300)
print("Basic four-quadrant chart saved to output/nba_quadrant_chart_basic.png")

# Close the figure to free memory
plt.close()

print("Four-quadrant chart framework created successfully.")
