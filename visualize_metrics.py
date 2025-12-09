import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Load data
df = pd.read_csv('nd_womens_basketball_2025_2026_with_fatigue_metrics.csv')

# Rename columns for consistency
df = df.rename(columns={
    'Game_Date': 'Game Date',
    'Home_Away': 'Location',
    'Travel_Distance_Miles': 'Travel Distance (miles)',
    'Travel_Duration_Hours': 'Travel Duration (hrs)',
    'Timezones_Crossed': 'Timezones crossed (#)',
    'Travel_Direction': 'Travel Direction (Home, North/South, Eastbound, Westbound)'
})

# Convert Game Date to datetime
df['Game Date'] = pd.to_datetime(df['Game Date'])

# Create figure with multiple subplots
print("Creating visualizations for Notre Dame Women's Basketball 2025-2026 Season...")

# ==== VISUALIZATION 1: Travel Distance Distribution ====
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Notre Dame Women\'s Basketball - Travel & Fatigue Analysis 2025-2026', 
             fontsize=16, fontweight='bold', y=0.995)

# 1a. Travel Distance by Game Type (Home vs Away)
ax1 = axes[0, 0]
travel_data = df[df['Location'] == 'Away']['Travel Distance (miles)']
ax1.hist(travel_data, bins=15, color='#0C2C56', alpha=0.7, edgecolor='black')
ax1.set_xlabel('Travel Distance (miles)', fontweight='bold')
ax1.set_ylabel('Number of Games', fontweight='bold')
ax1.set_title('Distribution of Away Game Travel Distances', fontweight='bold')
ax1.axvline(travel_data.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {travel_data.mean():.0f} mi')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# 1b. Travel Time Distribution
ax2 = axes[0, 1]
travel_time = df[df['Location'] == 'Away']['Travel Duration (hrs)'].dropna()
ax2.hist(travel_time, bins=12, color='#D4AF37', alpha=0.7, edgecolor='black')
ax2.set_xlabel('Travel Duration (hours)', fontweight='bold')
ax2.set_ylabel('Number of Games', fontweight='bold')
ax2.set_title('Distribution of Travel Times', fontweight='bold')
ax2.axvline(travel_time.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {travel_time.mean():.1f} hrs')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

# 1c. Timezone Crossings Impact
ax3 = axes[1, 0]
tz_data = df[df['Location'] == 'Away']['Timezones crossed (#)'].value_counts().sort_index()
colors_tz = ['#90EE90', '#FFD700', '#FF6347', '#FF1493'][:len(tz_data)]
ax3.bar(tz_data.index, tz_data.values, color=colors_tz, edgecolor='black', linewidth=1.5)
ax3.set_xlabel('Number of Timezones Crossed', fontweight='bold')
ax3.set_ylabel('Number of Away Games', fontweight='bold')
ax3.set_title('Away Games by Timezone Crossings', fontweight='bold')
ax3.set_xticks(tz_data.index)
for i, v in enumerate(tz_data.values):
    ax3.text(tz_data.index[i], v + 0.1, str(v), ha='center', fontweight='bold')
ax3.grid(axis='y', alpha=0.3)

# 1d. Travel Direction Analysis
ax4 = axes[1, 1]
direction_data = df[df['Location'] == 'Away']['Travel Direction (Home, North/South, Eastbound, Westbound)'].value_counts()
colors_dir = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'][:len(direction_data)]
ax4.barh(direction_data.index, direction_data.values, color=colors_dir, edgecolor='black', linewidth=1.5)
ax4.set_xlabel('Number of Away Games', fontweight='bold')
ax4.set_title('Away Games by Travel Direction', fontweight='bold')
for i, v in enumerate(direction_data.values):
    ax4.text(v + 0.1, i, str(v), va='center', fontweight='bold')
ax4.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('01_travel_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 01_travel_analysis.png")
plt.close()

# ==== VISUALIZATION 2: Schedule Timeline & Fatigue ====
fig, axes = plt.subplots(2, 1, figsize=(16, 10))
fig.suptitle('Schedule Timeline & Fatigue Metrics', fontsize=16, fontweight='bold')

# 2a. Games chronologically with travel time color coding
ax1 = axes[0]
df_sorted = df.sort_values('Game Date')
colors_fatigue = []
for idx, row in df_sorted.iterrows():
    if row['Location'] == 'Home':
        colors_fatigue.append('#90EE90')  # Light green for home
    elif pd.isna(row['Travel Duration (hrs)']):
        colors_fatigue.append('#D3D3D3')  # Gray for unknown
    elif row['Travel Duration (hrs)'] < 2:
        colors_fatigue.append('#FFD700')  # Yellow for short travel
    elif row['Travel Duration (hrs)'] < 5:
        colors_fatigue.append('#FFA500')  # Orange for medium travel
    else:
        colors_fatigue.append('#FF4444')  # Red for long travel

ax1.scatter(df_sorted['Game Date'], range(len(df_sorted)), c=colors_fatigue, s=200, alpha=0.7, edgecolor='black', linewidth=1)
ax1.set_ylabel('Game Number', fontweight='bold')
ax1.set_title('2025-2026 Schedule: Travel Intensity by Game Date', fontweight='bold')
ax1.grid(axis='y', alpha=0.3)
ax1.tick_params(axis='x', rotation=45)

# Add legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#90EE90', edgecolor='black', label='Home Game'),
    Patch(facecolor='#FFD700', edgecolor='black', label='Short Travel (<2 hrs)'),
    Patch(facecolor='#FFA500', edgecolor='black', label='Medium Travel (2-5 hrs)'),
    Patch(facecolor='#FF4444', edgecolor='black', label='Long Travel (>5 hrs)')
]
ax1.legend(handles=legend_elements, loc='upper left', fontsize=10)

# 2b. Rest Days Between Games
ax2 = axes[1]
df_sorted['Rest Days'] = df_sorted['Game Date'].diff().dt.days - 1
rest_days_valid = df_sorted['Rest Days'].dropna()
ax2.bar(range(1, len(rest_days_valid)+1), rest_days_valid.values, color='#4ECDC4', alpha=0.7, edgecolor='black')
ax2.axhline(rest_days_valid.mean(), color='red', linestyle='--', linewidth=2, label=f'Average: {rest_days_valid.mean():.1f} days')
ax2.set_xlabel('Game Sequence', fontweight='bold')
ax2.set_ylabel('Rest Days Before Game', fontweight='bold')
ax2.set_title('Rest Period Between Consecutive Games', fontweight='bold')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('02_schedule_timeline.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 02_schedule_timeline.png")
plt.close()

# ==== VISUALIZATION 3: Travel Frequency & Density ====
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Travel Frequency & Density Analysis', fontsize=16, fontweight='bold')

# 3a. Home vs Away Distribution
ax1 = axes[0, 0]
location_counts = df['Location'].value_counts()
colors_loc = ['#90EE90', '#FF6B6B']
wedges, texts, autotexts = ax1.pie(location_counts.values, labels=location_counts.index, autopct='%1.1f%%',
                                     colors=colors_loc, startangle=90, textprops={'fontweight': 'bold', 'fontsize': 11})
ax1.set_title(f'Home vs Away Games\n(Total: {len(df)} games)', fontweight='bold')

# 3b. Travel frequency by month
ax2 = axes[0, 1]
df_sorted['Month'] = df_sorted['Game Date'].dt.to_period('M')
travel_by_month = df_sorted[df_sorted['Location'] == 'Away'].groupby('Month').size()
months = [str(m) for m in travel_by_month.index]
ax2.bar(range(len(travel_by_month)), travel_by_month.values, color='#FF9999', alpha=0.7, edgecolor='black')
ax2.set_xticks(range(len(travel_by_month)))
ax2.set_xticklabels(months, rotation=45, ha='right')
ax2.set_ylabel('Away Games', fontweight='bold')
ax2.set_title('Away Games by Month', fontweight='bold')
for i, v in enumerate(travel_by_month.values):
    ax2.text(i, v + 0.1, str(int(v)), ha='center', fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

# 3c. Consecutive Away Games
ax3 = axes[1, 0]
df_sorted['Is Away'] = (df_sorted['Location'] == 'Away').astype(int)
consecutive_away = []
current_streak = 0
for is_away in df_sorted['Is Away'].values:
    if is_away:
        current_streak += 1
    else:
        if current_streak > 0:
            consecutive_away.append(current_streak)
        current_streak = 0
if current_streak > 0:
    consecutive_away.append(current_streak)

if consecutive_away:
    streak_counts = pd.Series(consecutive_away).value_counts().sort_index()
    ax3.bar(streak_counts.index, streak_counts.values, color='#FFB6C1', alpha=0.7, edgecolor='black')
    ax3.set_xlabel('Consecutive Away Games', fontweight='bold')
    ax3.set_ylabel('Frequency', fontweight='bold')
    ax3.set_title('Consecutive Away Game Streaks', fontweight='bold')
    for i, v in enumerate(streak_counts.values):
        ax3.text(streak_counts.index[i], v + 0.05, str(int(v)), ha='center', fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)

# 3d. Total Travel Distance by Opponent
ax4 = axes[1, 1]
opponent_travel = df[df['Location'] == 'Away'].groupby('Opponent')['Travel Distance (miles)'].sum().sort_values(ascending=False).head(10)
ax4.barh(range(len(opponent_travel)), opponent_travel.values, color='#87CEEB', alpha=0.7, edgecolor='black')
ax4.set_yticks(range(len(opponent_travel)))
ax4.set_yticklabels(opponent_travel.index, fontsize=9)
ax4.set_xlabel('Total Travel Distance (miles)', fontweight='bold')
ax4.set_title('Top 10 Away Opponents by Travel Distance', fontweight='bold')
for i, v in enumerate(opponent_travel.values):
    ax4.text(v + 20, i, f'{int(v)}', va='center', fontweight='bold', fontsize=9)
ax4.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('03_travel_frequency.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 03_travel_frequency.png")
plt.close()

# ==== VISUALIZATION 4: Fatigue Risk Assessment ====
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Fatigue Risk Assessment Matrix', fontsize=16, fontweight='bold')

# 4a. Cumulative Travel Distance Over Season
ax1 = axes[0, 0]
df_sorted_away = df_sorted[df_sorted['Location'] == 'Away'].copy()
df_sorted_away['Cumulative Distance'] = df_sorted_away['Travel Distance (miles)'].fillna(0).cumsum()
ax1.plot(range(len(df_sorted_away)), df_sorted_away['Cumulative Distance'].values, 
         marker='o', linewidth=2, markersize=6, color='#FF6B6B')
ax1.fill_between(range(len(df_sorted_away)), df_sorted_away['Cumulative Distance'].values, alpha=0.3, color='#FF6B6B')
ax1.set_xlabel('Away Game Number', fontweight='bold')
ax1.set_ylabel('Cumulative Travel Distance (miles)', fontweight='bold')
ax1.set_title('Cumulative Travel Distance Throughout Season', fontweight='bold')
ax1.grid(True, alpha=0.3)

# 4b. Travel Hours vs Rest Days Scatter
ax2 = axes[0, 1]
df_plot = df_sorted[df_sorted['Location'] == 'Away'].copy()
df_plot['Rest Days'] = df_plot['Game Date'].shift(-1) - df_plot['Game Date']
df_plot['Rest Days'] = df_plot['Rest Days'].dt.days - 1
scatter = ax2.scatter(df_plot['Travel Duration (hrs)'].fillna(0), 
                     df_plot['Rest Days'].fillna(3), 
                     s=150, alpha=0.6, c=df_plot['Timezones crossed (#)'], 
                     cmap='RdYlGn_r', edgecolor='black', linewidth=1)
ax2.set_xlabel('Travel Duration (hours)', fontweight='bold')
ax2.set_ylabel('Rest Days Before Next Game', fontweight='bold')
ax2.set_title('Travel Duration vs Recovery Time', fontweight='bold')
cbar = plt.colorbar(scatter, ax=ax2)
cbar.set_label('Timezones Crossed', fontweight='bold')
ax2.grid(True, alpha=0.3)

# Add risk zones
ax2.axhline(1, color='red', linestyle='--', alpha=0.5, linewidth=1)
ax2.axvline(3, color='orange', linestyle='--', alpha=0.5, linewidth=1)
ax2.text(0.5, 0.98, 'High Risk Zone', transform=ax2.transAxes, 
         fontsize=9, color='red', fontweight='bold', ha='right', va='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# 4c. High Fatigue Games (Travel + Rest Combined)
ax3 = axes[1, 0]
df_risk = df_sorted.copy()
df_risk['Days to Rest'] = (df_risk['Game Date'].shift(-1) - df_risk['Game Date']).dt.days - 1
df_risk['Fatigue Score'] = 0
df_risk.loc[df_risk['Location'] == 'Away', 'Fatigue Score'] = (
    (df_risk[df_risk['Location'] == 'Away']['Travel Duration (hrs)'].fillna(0) / 10) +
    (df_risk[df_risk['Location'] == 'Away']['Timezones crossed (#)'].fillna(0)) +
    (5 - df_risk[df_risk['Location'] == 'Away']['Days to Rest'].fillna(3).clip(0, 5))
)

high_fatigue = df_risk.nlargest(12, 'Fatigue Score')[['Game Date', 'Opponent', 'Fatigue Score', 'Location']]
ax3.barh(range(len(high_fatigue)), high_fatigue['Fatigue Score'].values, 
         color=['#FF4444' if loc == 'Away' else '#90EE90' for loc in high_fatigue['Location']], 
         alpha=0.7, edgecolor='black')
ax3.set_yticks(range(len(high_fatigue)))
ax3.set_yticklabels([f"{row['Opponent']}\n({row['Game Date'].strftime('%m/%d')})" 
                      for _, row in high_fatigue.iterrows()], fontsize=8)
ax3.set_xlabel('Fatigue Score', fontweight='bold')
ax3.set_title('Top 12 Games by Fatigue Risk', fontweight='bold')
ax3.invert_yaxis()
for i, v in enumerate(high_fatigue['Fatigue Score'].values):
    ax3.text(v + 0.1, i, f'{v:.1f}', va='center', fontweight='bold', fontsize=8)
ax3.grid(axis='x', alpha=0.3)

# 4d. Weekly Fatigue Load
ax4 = axes[1, 1]
df_risk['Week'] = df_risk['Game Date'].dt.isocalendar().week
weekly_load = df_risk.groupby('Week').agg({
    'Travel Duration (hrs)': lambda x: x[df_risk.loc[x.index, 'Location'] == 'Away'].sum(),
    'Game Date': 'count'
}).fillna(0)
weekly_load.columns = ['Travel Hours', 'Games']

x = range(len(weekly_load))
ax4_twin = ax4.twinx()

bars1 = ax4.bar(x, weekly_load['Games'], alpha=0.6, color='#4ECDC4', label='Games/Week', edgecolor='black')
line1 = ax4_twin.plot(x, weekly_load['Travel Hours'], marker='o', color='#FF6B6B', linewidth=2, 
                      markersize=8, label='Travel Hours/Week')

ax4.set_xlabel('Week Number', fontweight='bold')
ax4.set_ylabel('Games Per Week', fontweight='bold', color='#4ECDC4')
ax4_twin.set_ylabel('Travel Hours Per Week', fontweight='bold', color='#FF6B6B')
ax4.set_title('Weekly Schedule Load', fontweight='bold')
ax4.tick_params(axis='y', labelcolor='#4ECDC4')
ax4_twin.tick_params(axis='y', labelcolor='#FF6B6B')
ax4.set_xticks(x)
ax4.grid(axis='y', alpha=0.3)

# Combined legend
lines1, labels1 = ax4.get_legend_handles_labels()
lines2, labels2 = ax4_twin.get_legend_handles_labels()
ax4.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.tight_layout()
plt.savefig('04_fatigue_assessment.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 04_fatigue_assessment.png")
plt.close()

# ==== SUMMARY STATISTICS ====
print("\n" + "="*60)
print("NOTRE DAME WOMEN'S BASKETBALL 2025-2026 SEASON SUMMARY")
print("="*60)

away_games = df[df['Location'] == 'Away']
home_games = df[df['Location'] == 'Home']

print(f"\nGAME STATISTICS:")
print(f"  Total Games: {len(df)}")
print(f"  Home Games: {len(home_games)} ({len(home_games)/len(df)*100:.1f}%)")
print(f"  Away Games: {len(away_games)} ({len(away_games)/len(df)*100:.1f}%)")

print(f"\nTRAVEL METRICS:")
total_distance = away_games['Travel Distance (miles)'].sum()
total_hours = away_games['Travel Duration (hrs)'].sum()
print(f"  Total Travel Distance: {total_distance:,.0f} miles")
print(f"  Total Travel Hours: {total_hours:,.0f} hours")
print(f"  Average Distance per Away Game: {away_games['Travel Distance (miles)'].mean():.0f} miles")
print(f"  Average Time per Away Game: {away_games['Travel Duration (hrs)'].mean():.1f} hours")
print(f"  Longest Away Trip: {away_games['Travel Distance (miles)'].max():.0f} miles ({away_games['Travel Duration (hrs)'].max():.1f} hours)")

print(f"\nTIMEZONE IMPACT:")
tz_summary = away_games['Timezones crossed (#)'].value_counts().sort_index()
for tz, count in tz_summary.items():
    print(f"  {int(tz)} timezone(s) crossed: {int(count)} games")

print(f"\nTRAVEL DIRECTION:")
direction_summary = away_games['Travel Direction (Home, North/South, Eastbound, Westbound)'].value_counts()
for direction, count in direction_summary.items():
    print(f"  {direction}: {count} games")

print(f"\nREST PATTERNS:")
rest_days = df_sorted['Game Date'].diff().dt.days - 1
print(f"  Average Rest Days: {rest_days.mean():.1f} days")
print(f"  Minimum Rest Days: {rest_days[rest_days > 0].min():.0f} days")
print(f"  Maximum Rest Days: {rest_days.max():.0f} days")

back_to_backs = (rest_days == 0).sum()
print(f"  Back-to-Back Games: {back_to_backs}")

print("\n" + "="*60)
print("Visualizations saved successfully!")
print("="*60)
