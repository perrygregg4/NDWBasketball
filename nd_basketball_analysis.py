import csv
import pandas as pd
from datetime import datetime, timedelta

# Read the schedule
df = pd.read_csv('/tmp/nd_womens_basketball_2025_2026.csv')

print("=" * 80)
print("NOTRE DAME WOMEN'S BASKETBALL 2025-2026 SEASON - TRAVEL & FATIGUE ANALYSIS")
print("=" * 80)

# Basic Statistics
print("\n📊 SCHEDULE OVERVIEW")
print(f"Total Games: {len(df)}")
print(f"Home Games: {(df['Home_Away'] == 'Home').sum()}")
print(f"Away Games: {(df['Home_Away'] == 'Away').sum()}")
print(f"Neutral Games: {(df['Home_Away'] == 'Neutral').sum()}")

# Travel Statistics
print("\n✈️  TRAVEL STATISTICS")
print(f"Total Travel Distance: {df['Travel_Distance_Miles'].sum():.1f} miles")
print(f"Average Travel per Away Game: {df[df['Home_Away'] == 'Away']['Travel_Distance_Miles'].mean():.1f} miles")
print(f"Total Travel Time: {df['Travel_Duration_Hours'].sum():.1f} hours")
print(f"Average Travel Time per Away Game: {df[df['Home_Away'] == 'Away']['Travel_Duration_Hours'].mean():.2f} hours")

# Timezone Analysis
print("\n🌍 TIMEZONE ANALYSIS")
tz_data = df[df['Timezones_Crossed'] > 0]
print(f"Games with Timezone Changes: {len(tz_data)}")
print(f"Total Timezones Crossed: {df['Timezones_Crossed'].sum()}")
print(f"Maximum Timezones in Single Trip: {df['Timezones_Crossed'].max()}")

# Travel Direction Distribution
print("\n🧭 TRAVEL DIRECTION DISTRIBUTION")
direction_counts = df[df['Home_Away'] != 'Home']['Travel_Direction'].value_counts()
for direction, count in direction_counts.items():
    print(f"  {direction}: {count} games")

# High Travel Intensity Periods (3+ away games in calendar month)
print("\n⚠️  HIGH TRAVEL INTENSITY PERIODS")
df['Game_Date'] = pd.to_datetime(df['Game_Date'])
df['Month'] = df['Game_Date'].dt.to_period('M')

for month, group in df.groupby('Month'):
    away_count = (group['Home_Away'] == 'Away').sum()
    if away_count >= 2:
        travel_miles = group[group['Home_Away'] == 'Away']['Travel_Distance_Miles'].sum()
        travel_hours = group[group['Home_Away'] == 'Away']['Travel_Duration_Hours'].sum()
        print(f"  {month}: {away_count} away games, {travel_miles:.0f} miles, {travel_hours:.1f} hours")

# Consecutive Game Fatigue Analysis
print("\n💪 CONSECUTIVE GAME FATIGUE INDICATORS")
consecutive_away = 0
max_consecutive = 0
max_consecutive_location = ""
current_away_games = []

for idx, row in df.iterrows():
    if row['Home_Away'] == 'Away':
        consecutive_away += 1
        current_away_games.append({
            'opponent': row['Opponent'],
            'location': row['Location'],
            'date': row['Game_Date']
        })
        if consecutive_away > max_consecutive:
            max_consecutive = consecutive_away
            max_consecutive_location = row['Opponent']
    else:
        if consecutive_away >= 2:
            print(f"  {consecutive_away} consecutive away games before {row['Opponent']} (home) on {row['Game_Date'].date()}")
            for game in current_away_games:
                print(f"    - {game['opponent']} @ {game['location']} ({game['date'].date()})")
        consecutive_away = 0
        current_away_games = []

# Longest Road Trip
print("\n🛫 LONGEST ROAD TRIPS")
df['Cum_Travel'] = df['Travel_Distance_Miles'].cumsum()
in_road_trip = False
road_trip_start = 0
road_trip_games = []

for idx, row in df.iterrows():
    if row['Home_Away'] == 'Away':
        if not in_road_trip:
            in_road_trip = True
            road_trip_start = idx
            road_trip_games = []
        road_trip_games.append(row)
    else:
        if in_road_trip and len(road_trip_games) > 0:
            trip_distance = sum(g['Travel_Distance_Miles'] for g in road_trip_games)
            trip_hours = sum(g['Travel_Duration_Hours'] for g in road_trip_games)
            if len(road_trip_games) >= 2 or trip_distance >= 1000:
                print(f"  {len(road_trip_games)} games: {trip_distance:.0f} miles, {trip_hours:.1f} hours")
                for game in road_trip_games:
                    print(f"    - {game['Opponent']} @ {game['Location']} ({game['Game_Date'].date()})")
        in_road_trip = False
        road_trip_games = []

# Final road trip
if in_road_trip and len(road_trip_games) > 0:
    trip_distance = sum(g['Travel_Distance_Miles'] for g in road_trip_games)
    trip_hours = sum(g['Travel_Duration_Hours'] for g in road_trip_games)
    if len(road_trip_games) >= 2 or trip_distance >= 1000:
        print(f"  {len(road_trip_games)} games: {trip_distance:.0f} miles, {trip_hours:.1f} hours (final road trip)")
        for game in road_trip_games:
            print(f"    - {game['Opponent']} @ {game['Location']} ({game['Game_Date'].date()})")

print("\n" + "=" * 80)
