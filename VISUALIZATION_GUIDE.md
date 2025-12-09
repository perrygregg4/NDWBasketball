# Notre Dame Women's Basketball Visualization Guide

## Overview
This directory contains comprehensive visualizations analyzing travel schedules and fatigue metrics for the Notre Dame Women's Basketball team's 2025-2026 season.

## Visualizations

### 1. Travel Analysis (`01_travel_analysis.png`)
Four-panel analysis of travel characteristics:

- **Travel Distance Distribution**: Histogram showing the spread of away game travel distances. Average away trip is 824 miles, with most games requiring 400-1,200 miles of travel.
  
- **Travel Time Distribution**: Hours spent traveling to away games. Most away games require 5-8 hours of travel time, with a mean of 5.8 hours.
  
- **Timezone Crossings**: Impact analysis showing how many games involve crossing multiple time zones:
  - 7 games with no timezone crossing (regional opponents)
  - 3 games crossing 1 timezone (nearby conferences)
  - 2 games crossing 3 timezones (West Coast opponents)
  
- **Travel Direction**: Geographic distribution of away opponents:
  - 5 games Eastbound (towards Atlantic Coast)
  - 3 games South (ACC Southern schools)
  - 3 games Westbound (Big Ten West)
  - 1 game North

---

### 2. Schedule Timeline (`02_schedule_timeline.png`)
Two-panel view of schedule progression:

- **Game Sequence Timeline**: Each game is plotted chronologically with color coding:
  - 🟢 **Green**: Home games (no travel fatigue)
  - 🟡 **Yellow**: Short travel (<2 hours)
  - 🟠 **Orange**: Medium travel (2-5 hours)
  - 🔴 **Red**: Long travel (>5 hours)
  
  This visualization helps identify clusters of demanding away games and travel-intensive periods.

- **Rest Days Between Games**: Shows the recovery time between consecutive games:
  - Average rest: **3.2 days** between games
  - Minimum: 2 days (occasional tight schedules)
  - Maximum: 9 days (rare extended breaks)
  - **No back-to-back games** in 2025-2026 season
  
  Longer bars indicate better recovery opportunities.

---

### 3. Travel Frequency & Density (`03_travel_frequency.png`)
Four-panel analysis of overall travel patterns:

- **Home vs Away Split**: 56.7% home games (17), 40% away games (12), 3.3% TBD
  
- **Away Games by Month**: Distribution showing which months have the most away games, helping identify travel-intensive periods.
  
- **Consecutive Away Streaks**: Shows longest runs of back-to-back away games:
  - No games longer than 2-3 consecutive away games
  - Good schedule distribution preventing excessive travel clusters
  
- **Top 10 Away Opponents by Distance**: Identifies which opponents require the most travel:
  - West Coast schools (Stanford, Oregon, etc.)
  - Southeastern opponents (Florida State, etc.)
  
  This helps prioritize recovery resources for these high-travel matchups.

---

### 4. Fatigue Risk Assessment (`04_fatigue_assessment.png`)
Four-panel comprehensive fatigue analysis:

- **Cumulative Travel Distance**: Shows the progression of total miles traveled throughout the season. Team will accumulate approximately **9,888 miles** over the season's away games. Steep sections indicate high-travel periods requiring extra support.
  
- **Travel vs Recovery Scatter Plot**: 
  - X-axis: Hours of travel before a game
  - Y-axis: Days of rest available before next game
  - Color intensity: Number of timezones crossed
  
  Points in the **lower-left corner** (high travel + low rest) indicate **HIGH-RISK games** requiring special attention.
  
- **Top 12 Games by Fatigue Risk**: Ranking games by combined travel, timezone, and rest factors:
  - Red bars: Away games with high fatigue risk
  - Green bars: Home games (reference points)
  
  These are the critical matchups where fatigue management is most important.
  
- **Weekly Schedule Load**: Shows both games per week and travel hours per week:
  - Bars: Number of games scheduled
  - Red line: Total travel hours that week
  
  Peaks identify the most demanding weeks requiring enhanced recovery protocols.

---

## Key Findings

### Season Overview
- **Total Games**: 30 (17 home, 12 away, 1 TBD)
- **Total Travel Distance**: 9,888 miles
- **Total Travel Hours**: 70 hours
- **Average Away Trip**: 824 miles / 5.8 hours

### Travel Patterns
- **Geographic Distribution**: Balanced mix of directional opponents (East, South, West, North)
- **Timezone Impact**: Mostly regional conference play with minimal timezone crossing
- **Rest Between Games**: Excellent schedule with no back-to-back games and average 3.2 days rest

### Fatigue Risk Factors
✓ **Low Risk**: No back-to-back games scheduled
✓ **Good Recovery**: Average 3.2 days between games
⚠️ **Attention Needed**: 2 West Coast trips requiring 3+ timezone crossings
⚠️ **High Distance**: 1 trip to 2,630 miles requiring 9.3 hours travel

---

## Recommendations for Team Management

### High-Risk Games
Monitor additional fatigue metrics during these periods:
- Longest away trips (West Coast opponents)
- Games after 3+ timezone crossings
- Any games with <2 days rest (none in this schedule)

### Recovery Strategy
- **Post-Long Travel**: Utilize the 3+ day rest periods strategically for full recovery
- **Timezone Management**: Extra hydration and sleep protocols for 3-timezone games
- **Weekly Load**: Distribute strength/conditioning appropriately based on travel weeks

### Resource Allocation
- **High-Travel Weeks**: Increase athletic trainer availability and recovery resources
- **West Coast Trips**: Consider extended travel itineraries to optimize acclimatization
- **Medical Monitoring**: Flag players with travel sensitivity for individualized protocols

---

## Files in This Repository

- `01_travel_analysis.png` - Travel distance, time, timezone, and direction analysis
- `02_schedule_timeline.png` - Chronological schedule view and rest pattern analysis
- `03_travel_frequency.png` - Home/away split, monthly distribution, and consecutive game analysis
- `04_fatigue_assessment.png` - Risk assessment, cumulative load, and weekly schedule analysis
- `visualize_metrics.py` - Python script to regenerate all visualizations
- `nd_womens_basketball_2025_2026_with_fatigue_metrics.csv` - Full dataset with fatigue scores

---

## How to Use These Visualizations with Your Team

1. **Coaching Staff**: Review 01 & 02 for travel-heavy periods and recovery planning
2. **Athletic Training**: Use 04 for injury prevention protocols during high-fatigue games
3. **Strength & Conditioning**: Reference 03 & 04 for weekly programming intensity
4. **Travel Coordinator**: Use 01 for logistical planning of away trips
5. **Medical Staff**: Utilize high-risk games (04) for preventive medical interventions

---

*Generated: December 9, 2025*  
*Data Source: Notre Dame Fighting Irish Athletics - Women's Basketball Schedule 2025-2026*
