# Trip Validation Report - Notre Dame Women's Basketball 2025-2026

## Executive Summary

✅ **VALIDATION STATUS: PASSED**

All 30 games in the 2025-2026 schedule have been validated for geographical accuracy and proper location tracking. **100% success rate with zero discrepancies found.**

---

## Validation Details

### What Was Checked

For each game in the schedule, the validation script verified:

1. **Location Accuracy**: Is the game location a recognized university/arena in our coordinate database?
2. **Travel Distance Calculation**: Does the CSV distance match the calculated distance (within 50-mile tolerance)?
3. **Travel Duration Estimation**: Does the CSV duration match estimated travel time (within 1-hour tolerance)?
4. **Location Tracking**: Does the team's current location track correctly from game to game?
   - **Home games**: Team returns to South Bend, IN
   - **Away games**: Team location updates to away city for next game calculation

### Methodology

The script:
- Tracks the team's current location through the entire season
- Calculates expected distances using the Haversine formula between actual university coordinates
- Estimates travel times based on:
  - <500 miles: Driving (55 mph average)
  - ≥500 miles: Flying (500 mph) + 4 hours for airports/ground transportation
- Compares CSV values against calculated values with reasonable tolerance for rounding

### Critical Fix Validation

The Virginia game fix was verified to be correct:
- **Previous game**: Stanford (Palo Alto, CA) - Away
- **Home game**: Virginia Tech (South Bend, IN) - Home ✓ (Team returns)
- **Current game**: Virginia (Charlottesville, VA) - Away
  - **Calculated from**: South Bend, IN (not Palo Alto)
  - **Distance**: 483.4 miles ✓
  - **Duration**: 8.79 hours ✓

---

## Game-by-Game Results

### All Games (30 Total)

| Game | Opponent | Type | Location | Dist (mi) | Duration (h) | Status |
|------|----------|------|----------|-----------|--------------|--------|
| 1 | Lehigh | Home | South Bend, IN | 0.0 | 0.00 | ✅ |
| 2 | Marquette | Away | Milwaukee, WI | 125.6 | 2.28 | ✅ |
| 3 | Western Michigan | Home | South Bend, IN | 0.0 | 0.00 | ✅ |
| 4 | Penn State | Away | University Park, PA | 439.4 | 7.99 | ✅ |
| 5 | Oklahoma | Away | Norman, OK | 1133.5 | 6.27 | ✅ |
| 6 | UC Davis | Home | South Bend, IN | 0.0 | 0.00 | ✅ |
| 7 | South Carolina | Away | Columbia, SC | 602.9 | 5.21 | ✅ |
| 8 | Boston College | Away | Boston, MA | 790.9 | 5.58 | ✅ |
| 9 | Wake Forest | Away | Winston-Salem, NC | 654.1 | 5.31 | ✅ |
| 10 | Marquette | Home | South Bend, IN | 0.0 | 0.00 | ✅ |
| 11 | Syracuse | Away | Syracuse, NY | 523.1 | 5.05 | ✅ |
| 12 | Niagara | Home | South Bend, IN | 0.0 | 0.00 | ✅ |
| 13 | Temple | Away | Philadelphia, PA | 591.0 | 5.18 | ✅ |
| 14 | Georgia Tech | Away | Atlanta, GA | 665.5 | 5.33 | ✅ |
| 15 | Pittsburgh | Home | South Bend, IN | 0.0 | 0.00 | ✅ |
| 16 | Duke | Away | Durham, NC | 557.9 | 5.12 | ✅ |
| 17 | Louisville | Away | Louisville, KY | 408.8 | 7.43 | ✅ |
| 18 | Florida State | Away | Tallahassee, FL | 546.5 | 5.09 | ✅ |
| 19 | Clemson | Away | Clemson, SC | 305.1 | 5.55 | ✅ |
| 20 | SMU | Away | Dallas, TX | 812.3 | 5.62 | ✅ |
| 21 | Virginia Tech | Away | Blacksburg, VA | 975.4 | 5.95 | ✅ |
| 22 | California | Away | Berkeley, CA | 2273.2 | 8.55 | ✅ |
| 23 | Stanford | Away | Palo Alto, CA | 30.4 | 0.55 | ✅ |
| 24 | Virginia Tech | Home | South Bend, IN | 0.0 | 0.00 | ✅ |
| 25 | Virginia | Away | Charlottesville, VA | 483.4 | 8.79 | ✅ |
| 26 | UConn | Away | Storrs, CT | 420.7 | 7.65 | ✅ |
| 27 | NC State | Home | South Bend, IN | 0.0 | 0.00 | ✅ |
| 28 | Michigan State | Home | South Bend, IN | 0.0 | 0.00 | ✅ |
| 29 | Miami | Away | Coral Gables, FL | 1155.5 | 6.31 | ✅ |
| 30 | Georgia Tech | Home | South Bend, IN | 0.0 | 0.00 | ✅ |

---

## Summary Statistics

### Schedule Composition
- **Total Games**: 30
- **Home Games**: 10 (33.3%)
- **Away Games**: 20 (66.7%)

### Travel Metrics
- **Total Distance**: 13,495.2 miles (all away games combined)
- **Total Duration**: 114.8 hours (all away games combined)
- **Average per Away Game**: 674.8 miles / 5.74 hours

### Longest Away Trips
1. **California (Berkeley, CA)**: 2,273.2 miles / 8.55 hours
2. **Oklahoma (Norman, OK)**: 1,133.5 miles / 6.27 hours
3. **Miami (Coral Gables, FL)**: 1,155.5 miles / 6.31 hours
4. **Virginia Tech (Blacksburg, VA)**: 975.4 miles / 5.95 hours
5. **SMU (Dallas, TX)**: 812.3 miles / 5.62 hours

### Shortest Away Trips
1. **Stanford (Palo Alto, CA)**: 30.4 miles / 0.55 hours *(consecutive game within Bay Area)*
2. **Clemson (Clemson, SC)**: 305.1 miles / 5.55 hours
3. **Marquette (Milwaukee, WI)**: 125.6 miles / 2.28 hours
4. **Louisville (Louisville, KY)**: 408.8 miles / 7.43 hours
5. **UConn (Storrs, CT)**: 420.7 miles / 7.65 hours

---

## Known Data Quality Notes

### Coordinate Database

All 21 away game locations have been verified and use university/arena coordinates:

| Location | Coordinates | University |
|----------|-------------|-----------|
| South Bend, IN | 41.7033°N, 86.2390°W | Notre Dame |
| Milwaukee, WI | 43.0396°N, 87.9073°W | Marquette |
| University Park, PA | 40.8135°N, 77.8601°W | Penn State |
| Norman, OK | 35.2087°N, 97.4867°W | Oklahoma |
| Columbia, SC | 34.0007°N, 81.0348°W | South Carolina |
| Boston, MA | 42.3601°N, 71.0589°W | Boston College |
| Winston-Salem, NC | 36.0999°N, 80.2442°W | Wake Forest |
| Syracuse, NY | 43.0481°N, 76.1474°W | Syracuse |
| Philadelphia, PA | 39.9526°N, 75.1652°W | Temple |
| Atlanta, GA | 33.7490°N, 84.3880°W | Georgia Tech |
| Durham, NC | 35.9940°N, 78.8986°W | Duke |
| Louisville, KY | 38.2527°N, 85.7585°W | Louisville |
| Tallahassee, FL | 30.4383°N, 84.2807°W | Florida State |
| Clemson, SC | 34.6834°N, 82.8374°W | Clemson |
| Dallas, TX | 32.7767°N, 96.7970°W | SMU |
| Blacksburg, VA | 37.2295°N, 80.4139°W | Virginia Tech |
| Berkeley, CA | 37.8722°N, 122.2597°W | UC Berkeley |
| Palo Alto, CA | 37.4419°N, 122.1430°W | Stanford |
| Charlottesville, VA | 38.0293°N, 78.4767°W | University of Virginia |
| Storrs, CT | 41.8086°N, 72.2470°W | UConn |
| Coral Gables, FL | 25.7217°N, 80.2764°W | Miami |

---

## Validation Tolerances

To account for rounding and estimation variations:

- **Distance Tolerance**: ±50 miles (captures rounding and route variation)
- **Duration Tolerance**: ±1 hour (accounts for different speed assumptions, weather, traffic)

*Note: All 30 games fell within these tolerances.*

---

## Conclusion

The comprehensive validation audit confirms that:

1. ✅ **All location tracking is accurate** - No instances of incorrectly tracking team location
2. ✅ **All distance calculations are correct** - Matches expected haversine distances
3. ✅ **All duration estimates are reasonable** - Fits typical travel patterns
4. ✅ **The Virginia game fix is verified** - Proper location returned to South Bend
5. ✅ **No other trips were affected** by the geocoding issue

**The schedule data is reliable and ready for fatigue and travel analysis.**

---

**Validation Run Date**: December 9, 2025  
**Validation Script**: `validate_all_trips.py`  
**Data Source**: `nd_womens_basketball_2025_2026.csv`
