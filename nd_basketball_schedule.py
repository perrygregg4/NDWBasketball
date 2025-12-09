import csv
from datetime import datetime
import math

# Notre Dame location (South Bend, IN)
ND_LOCATION = (41.7033, -86.2390)
ND_TIMEZONE = -6  # Central Time

# Game schedule data extracted from the webpage
games = [
    # Exhibition
    {"date": "2025-10-30", "opponent": "Purdue Northwest", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2025-11-05", "opponent": "FDU", "location": "South Bend, IN", "home_away": "Home"},
    # Regular season
    {"date": "2025-11-09", "opponent": "Chicago State", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2025-11-12", "opponent": "Akron", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2025-11-15", "opponent": "Michigan", "location": "Detroit, MI", "home_away": "Neutral"},
    {"date": "2025-11-21", "opponent": "Southern Cal", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2025-11-24", "opponent": "Central Michigan", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2025-12-04", "opponent": "Ole Miss", "location": "Oxford, MS", "home_away": "Away"},
    {"date": "2025-12-07", "opponent": "Florida State", "location": "Tallahassee, FL", "home_away": "Away"},
    {"date": "2025-12-11", "opponent": "Morehead State", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2025-12-14", "opponent": "James Madison", "location": "Harrisonburg, VA", "home_away": "Away"},
    {"date": "2025-12-21", "opponent": "Bellarmine", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2025-12-29", "opponent": "Pittsburgh", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2026-01-01", "opponent": "Georgia Tech", "location": "Atlanta, GA", "home_away": "Away"},
    {"date": "2026-01-04", "opponent": "Duke", "location": "Durham, NC", "home_away": "Away"},
    {"date": "2026-01-08", "opponent": "Boston College", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2026-01-11", "opponent": "North Carolina", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2026-01-15", "opponent": "Louisville", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2026-01-19", "opponent": "UConn", "location": "Storrs, CT", "home_away": "Away"},
    {"date": "2026-01-22", "opponent": "Miami", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2026-01-25", "opponent": "Clemson", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2026-01-29", "opponent": "California", "location": "Berkeley, CA", "home_away": "Away"},
    {"date": "2026-02-01", "opponent": "Stanford", "location": "Palo Alto, CA", "home_away": "Away"},
    {"date": "2026-02-05", "opponent": "Virginia Tech", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2026-02-08", "opponent": "Virginia", "location": "Charlottesville, VA", "home_away": "Away"},
    {"date": "2026-02-15", "opponent": "NC State", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2026-02-19", "opponent": "Wake Forest", "location": "Winston-Salem, NC", "home_away": "Away"},
    {"date": "2026-02-22", "opponent": "SMU", "location": "Dallas, TX", "home_away": "Away"},
    {"date": "2026-02-26", "opponent": "Syracuse", "location": "South Bend, IN", "home_away": "Home"},
    {"date": "2026-03-01", "opponent": "Louisville", "location": "Louisville, KY", "home_away": "Away"},
]

# City coordinates (approximate major cities)
city_coords = {
    "South Bend, IN": (41.7033, -86.2390),
    "Detroit, MI": (42.3314, -83.0458),
    "Oxford, MS": (34.3644, -89.5186),
    "Tallahassee, FL": (30.4383, -84.2807),
    "Harrisonburg, VA": (38.4495, -79.2393),
    "Atlanta, GA": (33.7490, -84.3880),
    "Durham, NC": (35.9940, -78.8986),
    "Storrs, CT": (41.8086, -72.2470),
    "Clemson, SC": (34.6834, -82.8374),
    "Berkeley, CA": (37.8722, -122.2597),
    "Palo Alto, CA": (37.4419, -122.1430),
    "Charlottesville, VA": (38.0293, -78.4767),
    "Winston-Salem, NC": (36.0999, -80.2442),
    "Dallas, TX": (32.7767, -96.7970),
    "Louisville, KY": (38.2527, -85.7585),
}

# Timezone offsets from UTC (Eastern Standard Time = -5, Central = -6, Mountain = -7, Pacific = -8)
timezone_offsets = {
    "South Bend, IN": -6,  # Central
    "Detroit, MI": -5,     # Eastern
    "Oxford, MS": -6,      # Central
    "Tallahassee, FL": -5, # Eastern
    "Harrisonburg, VA": -5, # Eastern
    "Atlanta, GA": -5,     # Eastern
    "Durham, NC": -5,      # Eastern
    "Storrs, CT": -5,      # Eastern
    "Clemson, SC": -5,     # Eastern
    "Berkeley, CA": -8,    # Pacific
    "Palo Alto, CA": -8,   # Pacific
    "Charlottesville, VA": -5, # Eastern
    "Winston-Salem, NC": -5,   # Eastern
    "Dallas, TX": -6,      # Central
    "Louisville, KY": -6,  # Central
}

def calculate_distance(coord1, coord2):
    """Calculate distance between two coordinates using Haversine formula (returns miles)"""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    R = 3959  # Earth's radius in miles
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def calculate_travel_metrics(origin, destination):
    """Calculate travel distance and duration between two cities"""
    if origin not in city_coords or destination not in city_coords:
        return None, None
    
    origin_coords = city_coords[origin]
    dest_coords = city_coords[destination]
    
    # Calculate distance in miles
    distance = calculate_distance(origin_coords, dest_coords)
    
    # Estimate travel time (assuming average speed of 55 mph for driving, 500 mph for flying)
    # For simplicity, we'll use a rough driving estimate
    if distance < 500:
        # Driving estimate
        travel_time = distance / 55
    else:
        # Flying estimate (including airport time, flight, and ground transportation)
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
previous_location = "South Bend, IN"
game_number = 1

for i, game in enumerate(games):
    sport = "Women's Basketball"
    opponent = game["opponent"]
    game_date = game["date"]
    location = game["location"]
    home_away = game["home_away"]
    
    # Calculate travel metrics from previous location
    distance, travel_time = calculate_travel_metrics(previous_location, location)
    travel_direction = get_travel_direction(previous_location, location)
    timezones = count_timezones_crossed(previous_location, location)
    
    # For home games, we assume travel from South Bend
    if home_away == "Home":
        distance = 0
        travel_time = 0
        travel_direction = "Home"
        timezones = 0
    
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
    
    previous_location = location if home_away != "Home" else previous_location
    game_number += 1

# Calculate travel frequency/density
total_games = len(csv_data)
away_games = sum(1 for g in csv_data if g["Home_Away"] == "Away")
travel_games = total_games - sum(1 for g in csv_data if g["Home_Away"] == "Home")

# Write CSV file
output_file = "/tmp/nd_womens_basketball_2025_2026.csv"
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

print(f"✓ CSV file created: {output_file}")
print(f"\nSchedule Summary:")
print(f"Total Games: {total_games}")
print(f"Home Games: {sum(1 for g in csv_data if g['Home_Away'] == 'Home')}")
print(f"Away Games: {away_games}")
print(f"Neutral Games: {sum(1 for g in csv_data if g['Home_Away'] == 'Neutral')}")
print(f"Total Travel Distance: {sum(g['Travel_Distance_Miles'] for g in csv_data):.1f} miles")
print(f"Total Travel Time: {sum(g['Travel_Duration_Hours'] for g in csv_data):.1f} hours")
print(f"Travel Frequency: {away_games}/{total_games} games ({100*away_games/total_games:.1f}%)")
