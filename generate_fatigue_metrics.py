import csv
import pandas as pd
from datetime import datetime, timedelta

# Read the main schedule
df = pd.read_csv('/tmp/nd_womens_basketball_2025_2026.csv')
df['Game_Date'] = pd.to_datetime(df['Game_Date'])

# Create derived metrics CSV
derived_data = []

for idx, row in df.iterrows():
    # Travel Frequency: Games within 7 days with travel
    days_since_last = (row['Game_Date'] - df[df.index < idx]['Game_Date'].max()).days if idx > 0 else 0
    
    # Cumulative travel at this point in season
    cumulative_miles = df[df.index <= idx]['Travel_Distance_Miles'].sum()
    cumulative_hours = df[df.index <= idx]['Travel_Duration_Hours'].sum()
    
    # Days rest since previous game
    if idx > 0:
        prev_date = df.iloc[idx-1]['Game_Date']
        days_rest = (row['Game_Date'] - prev_date).days
    else:
        days_rest = 0
    
    # Fatigue Score (0-100): higher = more fatigue
    # Based on: travel miles, travel hours, days rest, consecutive away games, timezone changes
    fatigue_score = 0
    
    # Component 1: Travel intensity (0-30 points)
    if row['Travel_Distance_Miles'] == 0:
        travel_fatigue = 0
    elif row['Travel_Distance_Miles'] < 500:
        travel_fatigue = 5
    elif row['Travel_Distance_Miles'] < 1000:
        travel_fatigue = 15
    elif row['Travel_Distance_Miles'] < 2500:
        travel_fatigue = 25
    else:
        travel_fatigue = 30
    
    # Component 2: Timezone impact (0-20 points)
    timezone_fatigue = row['Timezones_Crossed'] * 5
    
    # Component 3: Rest days (0-20 points) - fewer days = more fatigue
    if days_rest <= 1:
        rest_fatigue = 20
    elif days_rest == 2:
        rest_fatigue = 10
    elif days_rest <= 3:
        rest_fatigue = 5
    else:
        rest_fatigue = 0
    
    # Component 4: Consecutive away games (0-30 points)
    consecutive_away = 0
    for j in range(max(0, idx-2), idx):
        if df.iloc[j]['Home_Away'] == 'Away':
            consecutive_away += 1
    
    if consecutive_away >= 2:
        consecutive_fatigue = 30
    elif consecutive_away == 1 and row['Home_Away'] == 'Away':
        consecutive_fatigue = 15
    else:
        consecutive_fatigue = 0
    
    fatigue_score = min(100, travel_fatigue + timezone_fatigue + rest_fatigue + consecutive_fatigue)
    
    # Determine fatigue level category
    if fatigue_score >= 70:
        fatigue_level = "VERY HIGH"
    elif fatigue_score >= 50:
        fatigue_level = "HIGH"
    elif fatigue_score >= 30:
        fatigue_level = "MODERATE"
    else:
        fatigue_level = "LOW"
    
    derived_data.append({
        'Game_Number': row['Game_Number'],
        'Game_Date': row['Game_Date'].date(),
        'Opponent': row['Opponent'],
        'Home_Away': row['Home_Away'],
        'Days_Rest_Since_Last': days_rest,
        'Travel_Distance_Miles': row['Travel_Distance_Miles'],
        'Travel_Duration_Hours': row['Travel_Duration_Hours'],
        'Timezones_Crossed': row['Timezones_Crossed'],
        'Travel_Direction': row['Travel_Direction'],
        'Cumulative_Distance_Miles': round(cumulative_miles, 1),
        'Cumulative_Hours': round(cumulative_hours, 1),
        'Travel_Fatigue_Component': travel_fatigue,
        'Timezone_Fatigue_Component': timezone_fatigue,
        'Rest_Fatigue_Component': rest_fatigue,
        'Consecutive_Game_Fatigue': consecutive_fatigue,
        'Overall_Fatigue_Score': fatigue_score,
        'Fatigue_Level': fatigue_level,
    })

# Create dataframe and save
derived_df = pd.DataFrame(derived_data)
derived_df.to_csv('/tmp/nd_womens_basketball_2025_2026_with_fatigue_metrics.csv', index=False)

print("=" * 100)
print("DERIVED FATIGUE METRICS - NOTRE DAME WOMEN'S BASKETBALL 2025-2026")
print("=" * 100)

# Display games ranked by fatigue score
print("\n🔴 HIGHEST FATIGUE GAMES (Top 10)")
print("-" * 100)
high_fatigue = derived_df.nlargest(10, 'Overall_Fatigue_Score')[
    ['Game_Number', 'Game_Date', 'Opponent', 'Home_Away', 'Overall_Fatigue_Score', 'Fatigue_Level']
]
for idx, row in high_fatigue.iterrows():
    print(f"Game {row['Game_Number']:2.0f} | {row['Game_Date']} | {row['Opponent']:20s} | "
          f"{row['Home_Away']:6s} | Score: {row['Overall_Fatigue_Score']:3.0f} | {row['Fatigue_Level']}")

# Breakdown of fatigue by level
print("\n📊 FATIGUE DISTRIBUTION")
print("-" * 100)
fatigue_counts = derived_df['Fatigue_Level'].value_counts().sort_index(ascending=False)
for level, count in fatigue_counts.items():
    pct = 100 * count / len(derived_df)
    print(f"{level:12s}: {count:2.0f} games ({pct:5.1f}%)")

# Critical concern games
print("\n⚠️  CRITICAL CONCERN GAMES (Fatigue Score >= 70)")
print("-" * 100)
critical = derived_df[derived_df['Overall_Fatigue_Score'] >= 70]
if len(critical) > 0:
    for idx, row in critical.iterrows():
        print(f"Game {row['Game_Number']:2.0f} | {row['Game_Date']} | {row['Opponent']:20s} @ {row['Home_Away']:6s}")
        print(f"  → Rest: {row['Days_Rest_Since_Last']} days | Travel: {row['Travel_Distance_Miles']:.0f}mi "
              f"({row['Travel_Duration_Hours']:.1f}hrs) | Timezones: {row['Timezones_Crossed']} | "
              f"Direction: {row['Travel_Direction']}")
        print(f"  → Fatigue Breakdown: Travel({row['Travel_Fatigue_Component']}), "
              f"Timezone({row['Timezone_Fatigue_Component']}), "
              f"Rest({row['Rest_Fatigue_Component']}), "
              f"Consecutive({row['Consecutive_Game_Fatigue']})")
else:
    print("None identified")

# Identify recovery windows
print("\n✅ BEST RECOVERY WINDOWS (4+ days rest before next game)")
print("-" * 100)
recovery_windows = derived_df[derived_df['Days_Rest_Since_Last'] >= 4][['Game_Number', 'Game_Date', 'Opponent']]
if len(recovery_windows) > 0:
    for idx, row in recovery_windows.iterrows():
        print(f"Before Game {row['Game_Number']:2.0f} ({row['Game_Date']} vs {row['Opponent']})")
else:
    print("Limited recovery windows identified - schedule is relatively condensed")

# Month-by-month analysis
print("\n📅 FATIGUE BY MONTH")
print("-" * 100)
derived_df['Month'] = pd.to_datetime(derived_df['Game_Date']).dt.to_period('M')
for month, group in derived_df.groupby('Month'):
    avg_fatigue = group['Overall_Fatigue_Score'].mean()
    max_fatigue = group['Overall_Fatigue_Score'].max()
    games_count = len(group)
    away_count = (group['Home_Away'] == 'Away').sum()
    travel_miles = group['Travel_Distance_Miles'].sum()
    
    print(f"\n{month}:")
    print(f"  Games: {games_count} (Away: {away_count}) | Travel: {travel_miles:.0f} miles | "
          f"Avg Fatigue: {avg_fatigue:.1f} | Max Fatigue: {max_fatigue:.0f}")

print("\n" + "=" * 100)
print(f"✓ Extended metrics saved to: nd_womens_basketball_2025_2026_with_fatigue_metrics.csv")
print("=" * 100)
