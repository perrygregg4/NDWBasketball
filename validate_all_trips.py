#!/usr/bin/env python3
"""
Comprehensive validation script to audit all travel calculations
and ensure location tracking is accurate for every trip.
"""

import pandas as pd
import math

def calculate_distance(coord1, coord2):
    """Calculate distance between two coordinates using Haversine formula (returns miles)"""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 3959  # Radius of Earth in miles
    return c * r

# City coordinates (university locations)
city_coords = {
    "South Bend, IN": (41.7033, -86.2390),  # Notre Dame
    "Milwaukee, WI": (43.0396, -87.9073),   # Marquette
    "University Park, PA": (40.8135, -77.8601),  # Penn State
    "Norman, OK": (35.2087, -97.4867),      # Oklahoma
    "Columbia, SC": (34.0007, -81.0348),    # South Carolina
    "Boston, MA": (42.3601, -71.0589),      # Boston College
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
    "Charlottesville, VA": (38.0293, -78.4767),  # University of Virginia
    "Storrs, CT": (41.8086, -72.2470),      # UConn
    "Coral Gables, FL": (25.7217, -80.2764),    # University of Miami
}

# Load the schedule
df = pd.read_csv('nd_womens_basketball_2025_2026.csv')
df['Game_Date'] = pd.to_datetime(df['Game_Date'])

print("=" * 100)
print("COMPREHENSIVE TRIP VALIDATION - NOTRE DAME WOMEN'S BASKETBALL 2025-2026")
print("=" * 100)
print()

# Track current location (team starts at South Bend)
current_location = "South Bend, IN"
current_location_coords = city_coords["South Bend, IN"]
issues_found = []
validation_details = []

for idx, row in df.iterrows():
    game_num = idx + 1
    opponent = row['Opponent']
    game_date = row['Game_Date']
    game_location = row['Location']
    home_away = row['Home_Away']
    csv_distance = row['Travel_Distance_Miles']
    csv_duration = row['Travel_Duration_Hours']
    csv_direction = row['Travel_Direction']
    
    # Check if location is valid
    if game_location not in city_coords:
        issues_found.append({
            'game': game_num,
            'opponent': opponent,
            'issue': f"UNKNOWN LOCATION: '{game_location}' not in coordinates database"
        })
        validation_details.append(f"Game {game_num:2d} | {opponent:20s} | ❌ LOCATION NOT FOUND: '{game_location}'")
        continue
    
    game_location_coords = city_coords[game_location]
    
    # Calculate expected distance and duration
    expected_distance = calculate_distance(current_location_coords, game_location_coords)
    
    # Estimate travel time
    if expected_distance < 500:
        expected_duration = expected_distance / 55  # Driving
    else:
        expected_duration = (expected_distance / 500) + 4  # Flying + airports
    
    # For home games, distance should be 0
    if home_away == "Home":
        expected_distance = 0
        expected_duration = 0
    
    # Check if CSV matches expected
    distance_match = abs(csv_distance - expected_distance) < 50  # Allow 50 mile tolerance
    duration_match = abs(csv_duration - expected_duration) < 1.0  # Allow 1 hour tolerance
    
    # Update current location based on game type
    if home_away == "Away":
        next_location = game_location
        next_location_coords = game_location_coords
    else:
        # Home game - team returns to South Bend
        next_location = "South Bend, IN"
        next_location_coords = city_coords["South Bend, IN"]
    
    # Create validation record
    status = "✅" if (home_away == "Home" or (distance_match and duration_match)) else "⚠️ "
    
    if home_away == "Home":
        validation_details.append(
            f"Game {game_num:2d} | {opponent:20s} | {home_away:4s} | {game_location:20s} | "
            f"Distance: {csv_distance:7.1f} mi (expected 0.0) | Duration: {csv_duration:5.2f} hrs (expected 0.0) | {status}"
        )
    else:
        distance_diff = csv_distance - expected_distance
        duration_diff = csv_duration - expected_duration
        
        if not distance_match or not duration_match:
            status = "⚠️ "
            issues_found.append({
                'game': game_num,
                'opponent': opponent,
                'from': current_location,
                'to': game_location,
                'csv_distance': csv_distance,
                'expected_distance': expected_distance,
                'distance_diff': distance_diff,
                'csv_duration': csv_duration,
                'expected_duration': expected_duration,
                'duration_diff': duration_diff,
            })
        
        validation_details.append(
            f"Game {game_num:2d} | {opponent:20s} | {home_away:4s} | {game_location:20s} | "
            f"Distance: {csv_distance:7.1f} mi (expected {expected_distance:7.1f}) | "
            f"Duration: {csv_duration:5.2f} hrs (expected {expected_duration:5.2f}) | {status}"
        )
    
    # Update current location
    current_location = next_location
    current_location_coords = next_location_coords

# Print validation details
print("\nDETAILED TRIP-BY-TRIP VALIDATION:")
print("-" * 100)
for detail in validation_details:
    print(detail)

print()
print("=" * 100)
if issues_found:
    print(f"⚠️  ISSUES FOUND: {len(issues_found)} discrepancies detected")
    print("=" * 100)
    print()
    
    for idx, issue in enumerate(issues_found, 1):
        print(f"{idx}. Game {issue['game']}: {issue['opponent']}")
        
        if 'from' in issue:
            print(f"   From: {issue['from']}")
            print(f"   To: {issue['to']}")
            print(f"   CSV Distance: {issue['csv_distance']:.1f} mi")
            print(f"   Expected: {issue['expected_distance']:.1f} mi")
            print(f"   Difference: {issue['distance_diff']:+.1f} mi ({abs(issue['distance_diff']/issue['expected_distance']*100):.1f}% error)")
            print(f"   CSV Duration: {issue['csv_duration']:.2f} hrs")
            print(f"   Expected: {issue['expected_duration']:.2f} hrs")
            print(f"   Difference: {issue['duration_diff']:+.2f} hrs")
        else:
            print(f"   Issue: {issue['issue']}")
        print()
else:
    print("✅ ALL TRIPS VALIDATED SUCCESSFULLY - No discrepancies found!")
    print("=" * 100)

# Summary statistics
print()
print("SUMMARY STATISTICS:")
print("-" * 100)
away_games = df[df['Home_Away'] == 'Away']
home_games = df[df['Home_Away'] == 'Home']
print(f"Total Games: {len(df)}")
print(f"  Home Games: {len(home_games)}")
print(f"  Away Games: {len(away_games)}")
print()
print(f"Travel Totals:")
print(f"  Total Distance: {away_games['Travel_Distance_Miles'].sum():.1f} miles")
print(f"  Total Duration: {away_games['Travel_Duration_Hours'].sum():.1f} hours")
print(f"  Average per Away Game: {away_games['Travel_Distance_Miles'].mean():.1f} miles / {away_games['Travel_Duration_Hours'].mean():.2f} hours")
print()
print(f"Validation Status:")
print(f"  Issues Found: {len(issues_found)}")
print(f"  Success Rate: {((len(df) - len(issues_found)) / len(df) * 100):.1f}%")
print()
print("=" * 100)
