# Notre Dame Women's Basketball 2025-2026 Season Analysis

This repository contains schedule data and travel/fatigue analysis for the Notre Dame Women's Basketball team's 2025-2026 season.

## Files

### Data Files
- **nd_womens_basketball_2025_2026.csv** - Complete schedule with travel metrics
- **nd_womens_basketball_2025_2026_with_fatigue_metrics.csv** - Schedule with additional fatigue analysis metrics

### Python Scripts
- **nd_basketball_schedule.py** - Web scraper for the schedule from fightingirish.com
- **nd_basketball_analysis.py** - Travel distance and time calculations
- **generate_fatigue_metrics.py** - Fatigue and recovery metrics generator

## Key Variables

### Core Schedule Data
- **Sport** - Basketball
- **Opponent** - Team name
- **Game Date** - Date of game
- **Location** - Home/Away designation

### Travel Metrics
- **Travel Duration (hrs)** - Hours traveled
- **Travel Distance (miles)** - Miles traveled
- **Timezones crossed (#)** - Number of timezone boundaries crossed
- **Travel Direction** - Direction relative to home (Home, North/South, Eastbound, Westbound)

### Fatigue Metrics
- **Travel Frequency** - Games per week requiring travel
- **Consecutive Away Games** - Number of consecutive away games
- **Rest Days** - Days between games
- **Back-to-Back Games** - Indicator of consecutive-day games

## Usage

### Extract Schedule
```bash
python3 nd_basketball_schedule.py
```

### Analyze Travel Patterns
```bash
python3 nd_basketball_analysis.py
```

### Generate Fatigue Metrics
```bash
python3 generate_fatigue_metrics.py
```

## Analysis Focus

This dataset enables analysis of:
- Player fatigue based on travel frequency and distance
- Impact of timezone changes on performance
- Rest and recovery patterns
- Geographic clustering of games
- Optimal scheduling for team performance

## Data Source
Schedule scraped from: https://fightingirish.com/sports/wbball/schedule/

## License
MIT
