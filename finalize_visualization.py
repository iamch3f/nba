import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os
from PIL import Image
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec

# Create output directory
os.makedirs('output', exist_ok=True)

print("Finalizing four-quadrant chart with enhanced visual elements...")

# Load the processed player data
df = pd.read_csv('data/processed_players_for_visualization.csv')
print(f"Loaded data for {len(df)} players")

# Function to load and resize an image for use in the plot
def get_image(path, zoom=0.15):
    try:
        img = plt.imread(path)
        return OffsetImage(img, zoom=zoom)
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        # Return a colored square as fallback
        fallback = np.ones((100, 100, 4))
        fallback[:, :, 0] = 0.8  # Red
        fallback[:, :, 1] = 0.8  # Green
        fallback[:, :, 2] = 0.8  # Blue
        fallback[:, :, 3] = 1.0  # Alpha
        return OffsetImage(fallback, zoom=zoom)

# Create a figure with a specific size and DPI for high quality
plt.figure(figsize=(24, 18), dpi=150)

# Create a grid for the main plot and the efficiency legend
gs = gridspec.GridSpec(2, 2, height_ratios=[4, 1], width_ratios=[4, 1])
ax_main = plt.subplot(gs[0, 0])  # Main plot
ax_eff = plt.subplot(gs[0, 1])   # Efficiency metrics
ax_info = plt.subplot(gs[1, :])  # Information panel

# Get the quadrant boundaries
pts_median = df['PTS'].median()
fga_median = df['FGA'].median()

# Set axis limits with some padding
pts_max = df['PTS'].max() * 1.05
pts_min = df['PTS'].min() * 0.95
fga_max = df['FGA'].max() * 1.05
fga_min = df['FGA'].min() * 0.95

# Create the quadrant areas with light colors on the main plot
# Q1: High Points, High Attempts (top right)
ax_main.add_patch(patches.Rectangle((fga_median, pts_median), fga_max - fga_median, pts_max - pts_median, 
                              alpha=0.15, facecolor='red', edgecolor='darkred', linewidth=1.5))
# Q2: High Points, Low Attempts (top left)
ax_main.add_patch(patches.Rectangle((fga_min, pts_median), fga_median - fga_min, pts_max - pts_median, 
                              alpha=0.15, facecolor='green', edgecolor='darkgreen', linewidth=1.5))
# Q3: Low Points, Low Attempts (bottom left)
ax_main.add_patch(patches.Rectangle((fga_min, pts_min), fga_median - fga_min, pts_median - pts_min, 
                              alpha=0.15, facecolor='blue', edgecolor='darkblue', linewidth=1.5))
# Q4: Low Points, High Attempts (bottom right)
ax_main.add_patch(patches.Rectangle((fga_median, pts_min), fga_max - fga_median, pts_median - pts_min, 
                              alpha=0.15, facecolor='orange', edgecolor='darkorange', linewidth=1.5))

# Draw the quadrant dividing lines
ax_main.axhline(y=pts_median, color='black', linestyle='--', alpha=0.7, linewidth=1.5)
ax_main.axvline(x=fga_median, color='black', linestyle='--', alpha=0.7, linewidth=1.5)

# Add player avatars to the chart
for idx, player in df.iterrows():
    # Get player avatar
    if 'AVATAR_PATH' in player and os.path.exists(player['AVATAR_PATH']):
        img = get_image(player['AVATAR_PATH'])
        
        # Create an annotation box for the avatar
        ab = AnnotationBbox(img, (player['FGA'], player['PTS']),
                           frameon=True,
                           pad=0.2,
                           bboxprops=dict(boxstyle="round,pad=0.3", 
                                         fc="white", 
                                         ec="black", 
                                         lw=1.5))
        ax_main.add_artist(ab)
        
        # Add player name below the avatar
        ax_main.annotate(player['PLAYER_NAME'], 
                    (player['FGA'], player['PTS']),
                    xytext=(0, -30),
                    textcoords='offset points',
                    ha='center',
                    fontsize=9,
                    weight='bold')
        
        # Add team abbreviation
        ax_main.annotate(player['TEAM_ABBREVIATION'], 
                    (player['FGA'], player['PTS']),
                    xytext=(0, -42),
                    textcoords='offset points',
                    ha='center',
                    fontsize=8)
        
        # Add points per game and efficiency
        pts_per_game = player['PTS'] / player['GP']
        efficiency = player['PTS_per_FGA']
        ax_main.annotate(f"{pts_per_game:.1f} PPG | {efficiency:.2f} PTS/FGA", 
                    (player['FGA'], player['PTS']),
                    xytext=(0, -54),
                    textcoords='offset points',
                    ha='center',
                    fontsize=8)
    else:
        # Fallback if avatar not available
        ax_main.scatter(player['FGA'], player['PTS'], alpha=0.7, s=100)
        ax_main.annotate(f"{player['PLAYER_NAME']} ({player['TEAM_ABBREVIATION']})", 
                    (player['FGA'], player['PTS']),
                    xytext=(5, 5),
                    textcoords='offset points',
                    fontsize=8)

# Add quadrant labels with enhanced styling
ax_main.text(fga_max*0.95, pts_max*0.95, "High Volume Scorers", 
         ha='right', va='top', fontsize=16, weight='bold', color='darkred',
         bbox=dict(facecolor='white', alpha=0.7, edgecolor='darkred', boxstyle='round,pad=0.5'))

ax_main.text(fga_min*1.05, pts_max*0.95, "Efficient Scorers", 
         ha='left', va='top', fontsize=16, weight='bold', color='darkgreen',
         bbox=dict(facecolor='white', alpha=0.7, edgecolor='darkgreen', boxstyle='round,pad=0.5'))

ax_main.text(fga_min*1.05, pts_min*1.05, "Low Usage Players", 
         ha='left', va='bottom', fontsize=16, weight='bold', color='darkblue',
         bbox=dict(facecolor='white', alpha=0.7, edgecolor='darkblue', boxstyle='round,pad=0.5'))

ax_main.text(fga_max*0.95, pts_min*1.05, "Volume Shooters", 
         ha='right', va='bottom', fontsize=16, weight='bold', color='darkorange',
         bbox=dict(facecolor='white', alpha=0.7, edgecolor='darkorange', boxstyle='round,pad=0.5'))

# Set axis labels and title for main plot
ax_main.set_xlabel('Field Goal Attempts (FGA)', fontsize=16, weight='bold')
ax_main.set_ylabel('Points Scored (PTS)', fontsize=16, weight='bold')
ax_main.set_title('NBA Players: Scoring Output vs. Shot Attempts', fontsize=22, weight='bold')

# Add grid lines for better readability
ax_main.grid(True, linestyle=':', alpha=0.3)

# Add a diagonal reference line for points per field goal attempt = 1.0, 1.5, and 2.0
x_ref = np.linspace(fga_min, fga_max, 100)
for ratio, style, width, label in zip([1.0, 1.5, 2.0], ['-', '--', ':'], [2, 2, 2], 
                                     ['1.0 PTS/FGA', '1.5 PTS/FGA', '2.0 PTS/FGA']):
    y_ref = x_ref * ratio
    ax_main.plot(x_ref, y_ref, linestyle=style, color='black', alpha=0.5, 
             linewidth=width, label=label)

# Add legend to main plot
ax_main.legend(loc='lower right', fontsize=12, framealpha=0.8)

# Create efficiency metrics panel
ax_eff.axis('off')  # Turn off axis
ax_eff.set_title('Scoring Efficiency Leaders', fontsize=16, weight='bold')

# Get top 10 players by efficiency (PTS/FGA)
top_efficient = df.sort_values('PTS_per_FGA', ascending=False).head(10)

# Create a table of top efficient players
efficiency_text = "Top 10 by PTS/FGA:\n\n"
for i, (_, player) in enumerate(top_efficient.iterrows(), 1):
    efficiency_text += f"{i}. {player['PLAYER_NAME']} ({player['TEAM_ABBREVIATION']})\n"
    efficiency_text += f"   {player['PTS_per_FGA']:.2f} PTS/FGA\n"
    efficiency_text += f"   {player['PTS']} PTS / {player['FGA']} FGA\n\n"

ax_eff.text(0.05, 0.95, efficiency_text, va='top', fontsize=12, 
           bbox=dict(facecolor='lightgray', alpha=0.3, boxstyle='round,pad=1.0'))

# Create information panel
ax_info.axis('off')  # Turn off axis

# Add explanatory text
quadrant_info = """
Quadrant Analysis:
• Top Right (Red): High Volume Scorers - Players who score a lot of points but also take many shot attempts
• Top Left (Green): Efficient Scorers - Players who score a lot of points with relatively fewer shot attempts
• Bottom Left (Blue): Low Usage Players - Players who score fewer points and take fewer shot attempts
• Bottom Right (Orange): Volume Shooters - Players who take many shot attempts but score fewer points

Diagonal Lines:
The diagonal reference lines show points per field goal attempt (PTS/FGA) ratios.
Higher values indicate more efficient scoring (more points per shot attempt).
"""

methodology = """
Methodology:
• Data source: NBA.com/stats API
• Players included: Top 50 NBA players by total points scored in the 2024-25 regular season
• Minimum games played: 20
• Quadrant boundaries: Median values for points scored and field goal attempts
• Efficiency metric: Points per Field Goal Attempt (PTS/FGA)
"""

data_info = f"""
Data Summary:
• Total players analyzed: {len(df)}
• Points scored range: {df['PTS'].min():.0f} to {df['PTS'].max():.0f}
• Field goal attempts range: {df['FGA'].min():.0f} to {df['FGA'].max():.0f}
• Median points: {pts_median:.0f}
• Median field goal attempts: {fga_median:.0f}
• Date created: {pd.Timestamp.now().strftime('%Y-%m-%d')}
"""

# Add the text to the information panel
ax_info.text(0.01, 0.99, quadrant_info, va='top', fontsize=12, transform=ax_info.transAxes)
ax_info.text(0.34, 0.99, methodology, va='top', fontsize=12, transform=ax_info.transAxes)
ax_info.text(0.67, 0.99, data_info, va='top', fontsize=12, transform=ax_info.transAxes)

# Add a footer with attribution
plt.figtext(0.5, 0.01, "Created with NBA Stats API data | © 2025", 
           ha='center', fontsize=10, style='italic')

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(hspace=0.1, wspace=0.1)

# Save the final chart with all enhancements
plt.savefig('output/nba_scoring_efficiency_quadrant_chart_final.png', dpi=300, bbox_inches='tight')
print("Final enhanced four-quadrant chart saved to output/nba_scoring_efficiency_quadrant_chart_final.png")

# Create a smaller version for preview
plt.savefig('output/nba_scoring_efficiency_quadrant_chart_preview.jpg', dpi=150, bbox_inches='tight', format='jpg')
print("Preview version saved to output/nba_scoring_efficiency_quadrant_chart_preview.jpg")

# Close the figure to free memory
plt.close()

print("Visualization finalized with enhanced labels and visual elements.")
