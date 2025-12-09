#!/usr/bin/env python3

import csv
import math
import json

# Hardcoded schedule data (actual 2025-2026 Notre Dame Women's Basketball)
games = [
    {"date": "2025-11-05", "opponent": "Lehigh", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2025-11-09", "opponent": "Marquette", "location": "Milwaukee, WI", "home_away": "Away"},
    {"date": "2025-11-11", "opponent": "Western Michigan", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2025-11-16", "opponent": "Penn State", "location": "University Park, PA", "home_away": "Away"},
    {"date": "2025-11-18", "opponent": "Oklahoma", "location": "Norman, OK", "home_away": "Away"},
    {"date": "2025-11-23", "opponent": "UC Davis", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2025-11-26", "opponent": "South Carolina", "location": "Columbia, SC", "home_away": "Away"},
    {"date": "2025-12-02", "opponent": "Boston College", "location": "Boston, MA", "home_away": "Away"},
    {"date": "2025-12-07", "opponent": "Wake Forest", "location": "Winston-Salem, NC", "home_away": "Away"},
    {"date": "2025-12-14", "opponent": "Marquette", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2025-12-20", "opponent": "Syracuse", "location": "Syracuse, NY", "home_away": "Away"},
    {"date": "2025-12-21", "opponent": "Niagara", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2025-12-29", "opponent": "Temple", "location": "Philadelphia, PA", "home_away": "Away"},
    {"date": "2026-01-02", "opponent": "Georgia Tech", "location": "Atlanta, GA", "home_away": "Away"},
    {"date": "2026-01-05", "opponent": "Pittsburgh", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2026-01-08", "opponent": "Duke", "location": "Durham, NC", "home_away": "Away"},
    {"date": "2026-01-11", "opponent": "Louisville", "location": "Louisville, KY", "home_away": "Away"},
    {"date": "2026-01-15", "opponent": "Florida State", "location": "Tallahassee, FL", "home_away": "Away"},
    {"date": "2026-01-18", "opponent": "Clemson", "location": "Clemson, SC", "home_away": "Away"},
    {"date": "2026-01-22", "opponent": "SMU", "location": "Dallas, TX", "home_away": "Away"},
    {"date": "2026-01-25", "opponent": "Virginia Tech", "location": "Blacksburg, VA", "home_away": "Away"},
    {"date": "2026-01-29", "opponent": "California", "location": "Berkeley, CA", "home_away": "Away"},
    {"date": "2026-02-01", "opponent": "Stanford", "location": "Palo Alto, CA", "home_away": "Away"},
    {"date": "2026-02-05", "opponent": "Virginia Tech", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2026-02-08", "opponent": "Virginia", "location": "Charlottesville, VA", "home_away": "Away"},
    {"date": "2026-02-14", "opponent": "UConn", "location": "Storrs, CT", "home_away": "Away"},
    {"date": "2026-02-18", "opponent": "NC State", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2026-02-22", "opponent": "Michigan State", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2026-03-01", "opponent": "Miami", "location": "Coral Gables, FL", "home_away": "Away"},
    {"date": "2026-03-07", "opponent": "Georgia Tech", "location": "South Bend, IN", "home_away": "Home"},
]

# City coordinates (CORRECTED: University locations, not state centroids)
city_coords = {
    "South Bend, IN": (41.7033, -86.2390),  # Notre Dame
    "Milwaukee, WI": (43.0396, -87.9073),   # Marquette
    "University Park, PA": (40.8135, -77.8601),  # Penn State
    "Norman, OK": (35.2087, -97.4867),      # Oklahoma
    "Columbia, SC": (34.0007, -81.0348),    # South Carolina
    "Boston, MA": (42.3601, -71.0589),      # Boston College area
    "Winston-Salem, NC": (36.0999, -80.2442),  # Wake Forest
    "Syracuse, NY": (43.0481, -76.1474),    # Syracuse University
    "Philadelphia, PA": (39.9526, -75.1652),    # Temple University
    "Atlanta, GA": (33.7490, -84.3880),     # Georgia Tech
    "Durham, NC": (35.9940, -78.8986),      # Duke University
    "Louisville, KY": (38.2527, -85.7585),  # University of Louisville
    "Tallahassee, FL": (30.4383, -84.2807),     # Florida State
    "Clemson, SC": (34.6834, -82.8374),     # Clemson University
    "Dallas, TX": (32.7767, -96.7970),      # SMU
    "Blacksburg, VA": (37.2295, -80.4139),  # Virginia Tech
    "Berkeley, CA": (37.8722, -122.2597),   # UC Berkeley
    "Palo Alto, CA": (37.4419, -122.1430),  # Stanford
    "Charlottesville, VA": (38.0293, -78.4767),  # **FIXED: University of Virginia, not state of Virginia**
    "Storrs, CT": (41.8086, -72.2470),      # UConn
    "Coral Gables, FL": (25.7217, -80.2764),    # University of Miami
}

# Timezone offsets from UTC (Eastern Standard Time = -5, Central = -6, Mountain = -7, Pacific = -8)
timezone_offsets = {
    "South Bend, IN": -6,  # Central
    "Milwaukee, WI": -6,   # Central
    "University Park, PA": -5, # Eastern
    "Norman, OK": -6,      # Central
    "Columbia, SC": -5,    # Eastern
    "Boston, MA": -5,      # Eastern
    "Winston-Salem, NC": -5,   # Eastern
    "Syracuse, NY": -5,    # Eastern
    "Philadelphia, PA": -5,     # Eastern
    "Atlanta, GA": -5,     # Eastern
    "Durham, NC": -5,      # Eastern
    "Louisville, KY": -6,  # Central
    "Tallahassee, FL": -5, # Eastern
    "Clemson, SC": -5,     # Eastern
    "Dallas, TX": -6,      # Central
    "Blacksburg, VA": -5,  # Eastern
    "Berkeley, CA": -8,    # Pacific
    "Palo Alto, CA": -8,   # Pacific
    "Charlottesville, VA": -5, # Eastern (FIXED)
    "Storrs, CT": -5,      # Eastern
    "Coral Gables, FL": -5,    # Eastern
}

def calculate_distance(coord1, coord2):
    """Calculate distance between two coordinates using Haversine formula (returns miles)"""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 3959  # Radius of Earth in miles
    
    return c * r

def calculate_travel_metrics(origin, destination):
    """Calculate travel distance and duration between two cities"""
    if origin not in city_coords or destination not in city_coords:
        return None, None
    
    origin_coords = city_coords[origin]
    dest_coords = city_coords[destination]
    
    # Calculate distance in miles
    distance = calculate_distance(origin_coords, dest_coords)
    
    # Estimate travel time (assuming average speed of 55 mph for driving, 500 mph for flying)
    if distance < 500:
        travel_time = distance / 55
    else:
        travel_time = (distance / 500) + 4  # 4 hours for airport/ground transport
    
    return distance, travel_time

def get_travel_direction(origin, destination):
    """Determine travel direction"""
    if origin == destination:
        return "Home"
    
    origin_coords = city_coords[origin]
    dest_coords = city_coords[destination]
    
    lat_diff = dest_coords[0] - origin_coords[0]
    lon_diff = dest_coords[1] - origin_coords[1]
    
    # Determine primary direction
    if abs(lat_diff) > abs(lon_diff):
        return "North" if lat_diff > 0 else "South"
    else:
        return "Eastbound" if lon_diff > 0 else "Westbound"

def count_timezones_crossed(origin, destination):
    """Count how many timezones are crossed"""
    origin_tz = timezone_offsets.get(origin, -6)
    dest_tz = timezone_offsets.get(destination, -6)
    return abs(origin_tz - dest_tz)

# Prepare data for CSV
csv_data = []
current_location = "South Bend, IN"  # **FIX: Track current location (home games return to South Bend)**
game_number = 1

for i, game in enumerate(games):
    sport = "Women's Basketball"
    opponent = game["opponent"]
    game_date = game["date"]
    location = game["location"]
    home_away = game["home_away"]
    
    # **FIX: Calculate travel from current location to next game**
    # Home games return team to South Bend
    if home_away == "Away":
        distance, travel_time = calculate_travel_metrics(current_location, location)
        travel_direction = get_travel_direction(current_location, location)
        timezones = count_timezones_crossed(current_location, location)
        current_location = location  # Update to away game location
    else:
        # Home games have no travel
        distance = 0
        travel_time = 0
        travel_direction = "Home"
        timezones = 0
        current_location = "South Bend, IN"  # Return to South Bend after home game
    
    csv_data.append({
        "Game_Number": game_number,
        "Sport": sport,
        "Opponent": opponent,
        "Game_Date": game_date,
        "Location": location,
        "Home_Away": home_away,
        "Travel_Distance_Miles": round(distance, 1) if distance else 0,
        "Travel_Duration_Hours": round(travel_time, 2) if travel_time else 0,
        "Timezones_Crossed": timezones,
        "Travel_Direction": travel_direction,
    })
    
    game_number += 1

# Calculate travel frequency/density
total_games = len(csv_data)
away_games = sum(1 for g in csv_data if g["Home_Away"] == "Away")
travel_games = total_games - sum(1 for g in csv_data if g["Home_Away"] == "Home")

# Write CSV file
output_file = "nd_womens_basketball_2025_2026_CORRECTED.csv"
with open(output_file, 'w', newline='') as f:
    fieldnames = [
        "Game_Number",
        "Sport",
        "Opponent",
        "Game_Date",
        "Location",
        "Home_Away",
        "Travel_Distance_Miles",
        "Travel_Duration_Hours",
        "Timezones_Crossed",
        "Travel_Direction",
    ]
    
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(csv_data)

print("✅ CORRECTED CSV FILE GENERATED")
print(f"File: {output_file}")
print(f"\nSummary:")
print(f"  Total Games: {total_games}")
print(f"  Away Games: {away_games}")
print(f"  Total Travel Distance: {sum(g['Travel_Distance_Miles'] for g in csv_data):.1f} miles")
print(f"  Total Travel Hours: {sum(g['Travel_Duration_Hours'] for g in csv_data):.1f} hours")

# Show Virginia game specifically
print(f"\n🔍 VIRGINIA GAME VERIFICATION:")
for game in csv_data:
    if game['Opponent'] == 'Virginia':
        print(f"  Opponent: {game['Opponent']}")
        print(f"  Location: {game['Location']}")
        print(f"  Home/Away: {game['Home_Away']}")
        print(f"  Distance: {game['Travel_Distance_Miles']:.1f} miles")
        print(f"  Duration: {game['Travel_Duration_Hours']:.2f} hours")
        print(f"  Timezones: {game['Timezones_Crossed']}")
        print(f"  Direction: {game['Travel_Direction']}")
