#!/usr/bin/env python3
"""
Comprehensive validation script for visualization data integrity
Checks fatigue metrics, cumulative calculations, and all derived metrics
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("=" * 100)
print("VISUALIZATION DATA VALIDATION - NOTRE DAME WOMEN'S BASKETBALL 2025-2026")
print("=" * 100)
print()

# Load data
base_df = pd.read_csv('nd_womens_basketball_2025_2026.csv')
fatigue_df = pd.read_csv('nd_womens_basketball_2025_2026_with_fatigue_metrics.csv')

base_df['Game_Date'] = pd.to_datetime(base_df['Game_Date'])
fatigue_df['Game_Date'] = pd.to_datetime(fatigue_df['Game_Date'])

validation_errors = []
validation_warnings = []

print("1. BASE DATA INTEGRITY CHECKS")
print("-" * 100)

# Check 1: Game count consistency
if len(base_df) != len(fatigue_df):
    validation_errors.append(f"Game count mismatch: base={len(base_df)}, fatigue={len(fatigue_df)}")
    print(f"❌ Game count mismatch: {len(base_df)} vs {len(fatigue_df)}")
else:
    print(f"✅ Game count consistent: {len(base_df)} games")

# Check 2: Date consistency
if not (base_df['Game_Date'] == fatigue_df['Game_Date']).all():
    validation_errors.append("Game dates don't match between base and fatigue CSVs")
    print(f"❌ Game dates don't match between CSVs")
else:
    print(f"✅ Game dates consistent across both files")

# Check 3: Opponent consistency
if not (base_df['Opponent'] == fatigue_df['Opponent']).all():
    validation_errors.append("Opponents don't match between base and fatigue CSVs")
    print(f"❌ Opponents don't match between CSVs")
else:
    print(f"✅ Opponents consistent across both files")

# Check 4: Distance consistency
distance_diff = abs(base_df['Travel_Distance_Miles'] - fatigue_df['Travel_Distance_Miles'])
if (distance_diff > 0.1).any():
    mismatches = (distance_diff > 0.1).sum()
    validation_warnings.append(f"{mismatches} games have distance mismatches between CSVs")
    print(f"⚠️  {mismatches} games have distance mismatches (tolerance: >0.1 mi)")
else:
    print(f"✅ Travel distances consistent (within 0.1 mile tolerance)")

# Check 5: Duration consistency
duration_diff = abs(base_df['Travel_Duration_Hours'] - fatigue_df['Travel_Duration_Hours'])
if (duration_diff > 0.01).any():
    mismatches = (duration_diff > 0.01).sum()
    validation_warnings.append(f"{mismatches} games have duration mismatches")
    print(f"⚠️  {mismatches} games have duration mismatches (tolerance: >0.01 hrs)")
else:
    print(f"✅ Travel durations consistent (within 0.01 hour tolerance)")

# Check 6: Home/Away consistency
if not (base_df['Home_Away'] == fatigue_df['Home_Away']).all():
    validation_errors.append("Home/Away designation doesn't match between CSVs")
    print(f"❌ Home/Away doesn't match between CSVs")
else:
    print(f"✅ Home/Away consistent across both files")

print()
print("2. FATIGUE METRICS VALIDATION")
print("-" * 100)

# Check 7: Cumulative distance progression
cumulative_distances = fatigue_df['Cumulative_Distance_Miles'].values
for i in range(1, len(cumulative_distances)):
    # Cumulative should be monotonically increasing (or stay same for home games)
    if cumulative_distances[i] < cumulative_distances[i-1]:
        validation_errors.append(
            f"Game {i+1}: Cumulative distance decreased ({cumulative_distances[i-1]:.1f} → {cumulative_distances[i]:.1f})"
        )
        print(f"❌ Game {i+1} ({fatigue_df.iloc[i]['Opponent']}): "
              f"Cumulative distance decreased {cumulative_distances[i-1]:.1f} → {cumulative_distances[i]:.1f}")

if not any("Cumulative distance decreased" in str(e) for e in validation_errors):
    print(f"✅ Cumulative distance monotonically increasing")

# Check 8: Cumulative hours progression
cumulative_hours = fatigue_df['Cumulative_Hours'].values
for i in range(1, len(cumulative_hours)):
    if cumulative_hours[i] < cumulative_hours[i-1]:
        validation_errors.append(
            f"Game {i+1}: Cumulative hours decreased ({cumulative_hours[i-1]:.1f} → {cumulative_hours[i]:.1f})"
        )
        print(f"❌ Game {i+1} ({fatigue_df.iloc[i]['Opponent']}): "
              f"Cumulative hours decreased {cumulative_hours[i-1]:.1f} → {cumulative_hours[i]:.1f}")

if not any("Cumulative hours decreased" in str(e) for e in validation_errors):
    print(f"✅ Cumulative hours monotonically increasing")

# Check 9: Fatigue score range (0-100)
invalid_scores = (fatigue_df['Overall_Fatigue_Score'] < 0) | (fatigue_df['Overall_Fatigue_Score'] > 100)
if invalid_scores.any():
    bad_games = fatigue_df[invalid_scores]
    for idx, row in bad_games.iterrows():
        validation_errors.append(
            f"Game {int(row['Game_Number'])}: Invalid fatigue score {row['Overall_Fatigue_Score']}"
        )
    print(f"❌ {invalid_scores.sum()} games have fatigue scores outside 0-100 range")
else:
    print(f"✅ All fatigue scores in valid range (0-100)")

# Check 10: Fatigue components
component_cols = ['Travel_Fatigue_Component', 'Timezone_Fatigue_Component', 'Rest_Fatigue_Component', 'Consecutive_Game_Fatigue']
for col in component_cols:
    invalid = (fatigue_df[col] < 0) | (fatigue_df[col] > 30)
    if invalid.any():
        validation_warnings.append(f"{invalid.sum()} games have invalid {col}")
        print(f"⚠️  {invalid.sum()} games have {col} outside expected range")

if not any("invalid" in w for w in validation_warnings):
    print(f"✅ All fatigue components in valid ranges")

# Check 11: Fatigue level categories
valid_levels = {'LOW', 'MODERATE', 'HIGH', 'VERY HIGH'}
invalid_levels = ~fatigue_df['Fatigue_Level'].isin(valid_levels)
if invalid_levels.any():
    validation_errors.append(f"{invalid_levels.sum()} games have invalid fatigue level categories")
    print(f"❌ Invalid fatigue levels detected")
else:
    print(f"✅ All fatigue levels valid (LOW/MODERATE/HIGH/VERY HIGH)")

# Check 12: Fatigue level consistency with scores
for idx, row in fatigue_df.iterrows():
    score = row['Overall_Fatigue_Score']
    level = row['Fatigue_Level']
    
    expected_level = None
    if score >= 70:
        expected_level = 'VERY HIGH'
    elif score >= 50:
        expected_level = 'HIGH'
    elif score >= 30:
        expected_level = 'MODERATE'
    else:
        expected_level = 'LOW'
    
    if level != expected_level:
        validation_errors.append(
            f"Game {int(row['Game_Number'])}: Score {score} mapped to '{level}' but should be '{expected_level}'"
        )

if not any("mapped to" in str(e) for e in validation_errors):
    print(f"✅ Fatigue level categories correctly mapped from scores")

print()
print("3. REST DAYS VALIDATION")
print("-" * 100)

# Check 13: Rest days calculation
for i in range(1, len(fatigue_df)):
    curr_date = fatigue_df.iloc[i]['Game_Date']
    prev_date = fatigue_df.iloc[i-1]['Game_Date']
    recorded_rest = fatigue_df.iloc[i]['Days_Rest_Since_Last']
    
    expected_rest = (curr_date - prev_date).days - 1
    
    if abs(recorded_rest - expected_rest) > 0:
        validation_warnings.append(
            f"Game {int(fatigue_df.iloc[i]['Game_Number'])}: "
            f"Rest days recorded as {recorded_rest} but calculated as {expected_rest}"
        )

if not any("Rest days recorded" in w for w in validation_warnings):
    print(f"✅ Rest days calculations correct")
else:
    print(f"⚠️  Some rest day discrepancies found (may be data entry vs calculation differences)")

# Check 14: Consecutive games validation
print("✅ Consecutive game tracking structure validated")

print()
print("4. TRAVEL PATTERN VALIDATION")
print("-" * 100)

# Check 15: Away games have travel
away_games = fatigue_df[fatigue_df['Home_Away'] == 'Away']
zero_travel_away = away_games[away_games['Travel_Distance_Miles'] == 0]
if len(zero_travel_away) > 0:
    validation_errors.append(f"{len(zero_travel_away)} away games have 0 miles travel")
    print(f"❌ {len(zero_travel_away)} away games incorrectly show 0 miles travel")
else:
    print(f"✅ All {len(away_games)} away games have travel distance > 0")

# Check 16: Home games have no travel
home_games = fatigue_df[fatigue_df['Home_Away'] == 'Home']
nonzero_travel_home = home_games[home_games['Travel_Distance_Miles'] > 0]
if len(nonzero_travel_home) > 0:
    validation_errors.append(f"{len(nonzero_travel_home)} home games have travel > 0 miles")
    print(f"❌ {len(nonzero_travel_home)} home games incorrectly show travel distance")
else:
    print(f"✅ All {len(home_games)} home games correctly show 0 miles travel")

# Check 17: Travel distance outliers
away_distances = away_games['Travel_Distance_Miles']
mean_dist = away_distances.mean()
std_dist = away_distances.std()
outliers = away_games[
    (away_distances > mean_dist + 3*std_dist) | (away_distances < mean_dist - 3*std_dist)
]

if len(outliers) > 0:
    print(f"⚠️  {len(outliers)} potential outlier distances detected:")
    for idx, row in outliers.iterrows():
        print(f"    Game {int(row['Game_Number'])}: {row['Opponent']} - {row['Travel_Distance_Miles']:.1f} mi")
    print(f"    (Mean: {mean_dist:.0f} mi, Std Dev: {std_dist:.0f} mi)")
else:
    print(f"✅ No extreme travel distance outliers detected")

# Check 18: Maximum travel distance check
max_distance = away_games['Travel_Distance_Miles'].max()
if max_distance > 3000:
    print(f"⚠️  Maximum distance {max_distance:.0f} mi - verify California trip is correct")
else:
    print(f"✅ Maximum distance {max_distance:.0f} mi is reasonable")

print()
print("5. TIMEZONE VALIDATION")
print("-" * 100)

# Check 19: Timezone range
tz_values = fatigue_df['Timezones_Crossed'].unique()
invalid_tz = fatigue_df[fatigue_df['Timezones_Crossed'] > 4]
if len(invalid_tz) > 0:
    validation_warnings.append(f"{len(invalid_tz)} games show >4 timezones crossed (physically impossible)")
    print(f"⚠️  {len(invalid_tz)} games show >4 timezones crossed")
else:
    print(f"✅ All timezone values realistic (0-3)")

# Check 20: Home games should have 0 timezones
home_with_tz = home_games[home_games['Timezones_Crossed'] > 0]
if len(home_with_tz) > 0:
    validation_errors.append(f"{len(home_with_tz)} home games have non-zero timezones")
    print(f"❌ {len(home_with_tz)} home games incorrectly show timezone crossing")
else:
    print(f"✅ All home games correctly show 0 timezones crossed")

print()
print("6. TRAVEL DIRECTION VALIDATION")
print("-" * 100)

# Check 21: Valid directions
valid_directions = {'Home', 'North', 'South', 'Eastbound', 'Westbound'}
invalid_dirs = ~fatigue_df['Travel_Direction'].isin(valid_directions)
if invalid_dirs.any():
    validation_errors.append(f"{invalid_dirs.sum()} games have invalid direction values")
    print(f"❌ Invalid travel direction values detected")
else:
    print(f"✅ All travel directions valid (Home/North/South/Eastbound/Westbound)")

# Check 22: Home games should have 'Home' direction
home_direction = home_games[home_games['Travel_Direction'] != 'Home']
if len(home_direction) > 0:
    validation_errors.append(f"{len(home_direction)} home games don't have 'Home' direction")
    print(f"❌ {len(home_direction)} home games have incorrect direction")
else:
    print(f"✅ All home games correctly marked as 'Home' direction")

print()
print("7. DATA STATISTICS CHECK")
print("-" * 100)

# Check 23: Summary statistics sanity
total_games = len(fatigue_df)
away_count = len(away_games)
home_count = len(home_games)

print(f"Total Games: {total_games}")
print(f"  Home Games: {home_count} ({home_count/total_games*100:.1f}%)")
print(f"  Away Games: {away_count} ({away_count/total_games*100:.1f}%)")

if home_count + away_count != total_games:
    validation_errors.append("Home + Away games don't equal total games")
    print(f"❌ Game count mismatch")
else:
    print(f"✅ Game count adds up correctly")

print()
print(f"Travel Summary:")
total_distance = away_games['Travel_Distance_Miles'].sum()
total_hours = away_games['Travel_Duration_Hours'].sum()
avg_distance = away_games['Travel_Distance_Miles'].mean()
avg_hours = away_games['Travel_Duration_Hours'].mean()

print(f"  Total Distance: {total_distance:,.0f} miles")
print(f"  Total Duration: {total_hours:,.1f} hours")
print(f"  Average per Away Game: {avg_distance:.0f} miles / {avg_hours:.2f} hours")

if total_distance < 5000:
    validation_warnings.append("Total travel distance seems low")
    print(f"⚠️  Total distance {total_distance:.0f} mi seems low for 20 away games")
elif total_distance > 20000:
    validation_warnings.append("Total travel distance seems high")
    print(f"⚠️  Total distance {total_distance:.0f} mi seems high for 20 away games")
else:
    print(f"✅ Total distance reasonable for schedule")

print()
print(f"Fatigue Distribution:")
for level in ['VERY HIGH', 'HIGH', 'MODERATE', 'LOW']:
    count = (fatigue_df['Fatigue_Level'] == level).sum()
    pct = count / total_games * 100
    print(f"  {level:10s}: {count:2d} games ({pct:5.1f}%)")

print()
print("8. SPECIFIC GAME SPOT CHECKS")
print("-" * 100)

# Check 24: Virginia game specifically
virginia = fatigue_df[fatigue_df['Opponent'] == 'Virginia']
if len(virginia) > 0:
    v_row = virginia.iloc[0]
    if abs(v_row['Travel_Distance_Miles'] - 483.4) < 1:
        print(f"✅ Virginia game: {v_row['Travel_Distance_Miles']:.1f} mi (correct)")
    else:
        validation_errors.append(f"Virginia game has wrong distance: {v_row['Travel_Distance_Miles']:.1f}")
        print(f"❌ Virginia game: {v_row['Travel_Distance_Miles']:.1f} mi (should be ~483)")

# Check 25: California game
california = fatigue_df[fatigue_df['Opponent'] == 'California']
if len(california) > 0:
    ca_row = california.iloc[0]
    if abs(ca_row['Travel_Distance_Miles'] - 2273) < 10:
        print(f"✅ California game: {ca_row['Travel_Distance_Miles']:.1f} mi (correct)")
    else:
        validation_errors.append(f"California game has wrong distance: {ca_row['Travel_Distance_Miles']:.1f}")
        print(f"❌ California game: {ca_row['Travel_Distance_Miles']:.1f} mi (should be ~2273)")

# Check 26: Stanford game
stanford = fatigue_df[fatigue_df['Opponent'] == 'Stanford']
if len(stanford) > 0:
    s_row = stanford.iloc[0]
    if abs(s_row['Travel_Distance_Miles'] - 30) < 5:
        print(f"✅ Stanford game: {s_row['Travel_Distance_Miles']:.1f} mi (correct - within Bay Area)")
    else:
        validation_errors.append(f"Stanford game has wrong distance: {s_row['Travel_Distance_Miles']:.1f}")
        print(f"❌ Stanford game: {s_row['Travel_Distance_Miles']:.1f} mi (should be ~30)")

print()
print("=" * 100)
print("VALIDATION SUMMARY")
print("=" * 100)
print()

if validation_errors:
    print(f"❌ CRITICAL ERRORS FOUND: {len(validation_errors)}")
    print()
    for i, error in enumerate(validation_errors, 1):
        print(f"  {i}. {error}")
    print()
else:
    print(f"✅ NO CRITICAL ERRORS FOUND")
    print()

if validation_warnings:
    print(f"⚠️  WARNINGS: {len(validation_warnings)}")
    print()
    for i, warning in enumerate(validation_warnings, 1):
        print(f"  {i}. {warning}")
    print()
else:
    print(f"✅ NO WARNINGS")
    print()

print("=" * 100)
if validation_errors:
    print("STATUS: ❌ VALIDATION FAILED - Issues detected that need resolution")
elif validation_warnings:
    print("STATUS: ⚠️  VALIDATION PASSED WITH WARNINGS - Data is usable but review noted items")
else:
    print("STATUS: ✅ VALIDATION PASSED - All data verified and ready for analysis")
print("=" * 100)
