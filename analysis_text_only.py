"""
Uber Data Analysis - Text Output Only
This script performs comprehensive analysis without plotting
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("UBER DATA ANALYSIS - COMPREHENSIVE INSIGHTS")
print("="*80)

# Load data
print("\n1. LOADING DATA...")
df = pd.read_csv('Uber.csv')
df['pickup_dt'] = pd.to_datetime(df['pickup_dt'])

print(f"Dataset shape: {df.shape}")
print(f"Date range: {df['pickup_dt'].min()} to {df['pickup_dt'].max()}")

# Data preparation
df['hour'] = df['pickup_dt'].dt.hour
df['day_of_week'] = df['pickup_dt'].dt.day_name()
df['month'] = df['pickup_dt'].dt.month
df['month_name'] = df['pickup_dt'].dt.month_name()
df['is_weekend'] = df['pickup_dt'].dt.dayofweek >= 5
df['is_holiday'] = df['hday'] == 'Y'
df['borough'] = df['borough'].fillna('Unknown')

# UNIVARIATE ANALYSIS
print("\n" + "="*80)
print("2. UNIVARIATE ANALYSIS")
print("="*80)

print("\n--- Pickups Statistics ---")
print(df['pickups'].describe())

print("\n--- Weather Variables Statistics ---")
weather_vars = ['spd', 'vsb', 'temp', 'dewp', 'slp', 'pcp01', 'pcp06', 'pcp24', 'sd']
for var in weather_vars:
    print(f"\n{var}:")
    print(f"  Mean: {df[var].mean():.2f}")
    print(f"  Min: {df[var].min():.2f}, Max: {df[var].max():.2f}")
    if var in ['pcp01', 'pcp06', 'pcp24', 'sd']:
        non_zero = (df[var] > 0).sum()
        print(f"  Non-zero records: {non_zero} ({100*non_zero/len(df):.1f}%)")

print("\n--- Borough Distribution ---")
print(df['borough'].value_counts())

print("\n--- Holiday Distribution ---")
print(df['is_holiday'].value_counts())

# BIVARIATE ANALYSIS - TEMPORAL
print("\n" + "="*80)
print("3. BIVARIATE ANALYSIS - TEMPORAL PATTERNS")
print("="*80)

hourly = df.groupby('hour')['pickups'].agg(['mean', 'sum', 'count'])
print("\n--- Hourly Pattern ---")
print(f"Peak hour: {hourly['mean'].idxmax()}:00 ({hourly['mean'].max():.0f} avg pickups)")
print(f"Lowest hour: {hourly['mean'].idxmin()}:00 ({hourly['mean'].min():.0f} avg pickups)")
print("\nTop 5 hours by average pickups:")
print(hourly.nlargest(5, 'mean')[['mean']])

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily = df.groupby('day_of_week')['pickups'].agg(['mean', 'sum']).reindex(day_order)
print("\n--- Day of Week Pattern ---")
print(f"Peak day: {daily['mean'].idxmax()} ({daily['mean'].max():.0f} avg pickups)")
print(f"Lowest day: {daily['mean'].idxmin()} ({daily['mean'].min():.0f} avg pickups)")
print("\nAverage pickups by day:")
print(daily[['mean']])

month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
monthly = df.groupby('month_name')['pickups'].agg(['mean', 'sum']).reindex(month_order)
print("\n--- Monthly Pattern ---")
print(f"Peak month: {monthly['mean'].idxmax()} ({monthly['mean'].max():.0f} avg pickups)")
print("\nAverage pickups by month:")
print(monthly[['mean']])

weekend = df.groupby('is_weekend')['pickups'].agg(['mean', 'sum'])
print("\n--- Weekend vs Weekday ---")
print(f"Weekday: {weekend.loc[False, 'mean']:.0f} avg pickups")
print(f"Weekend: {weekend.loc[True, 'mean']:.0f} avg pickups")
print(f"Ratio: {weekend.loc[True, 'mean']/weekend.loc[False, 'mean']:.2f}")

# BIVARIATE ANALYSIS - BOROUGH
print("\n" + "="*80)
print("4. BIVARIATE ANALYSIS - BOROUGH PATTERNS")
print("="*80)

borough_stats = df.groupby('borough')['pickups'].agg(['sum', 'mean', 'count']).sort_values('sum', ascending=False)
print("\n--- Borough Statistics ---")
print(borough_stats)

# Top borough by hour
print("\n--- Peak Hours by Borough (Top 3) ---")
top_boroughs = borough_stats.head(3).index
for borough in top_boroughs:
    borough_hourly = df[df['borough'] == borough].groupby('hour')['pickups'].mean()
    peak_hour = borough_hourly.idxmax()
    print(f"{borough}: Peak at {peak_hour}:00 ({borough_hourly.max():.0f} avg pickups)")

# BIVARIATE ANALYSIS - WEATHER
print("\n" + "="*80)
print("5. BIVARIATE ANALYSIS - WEATHER IMPACT")
print("="*80)

numeric_cols = ['pickups', 'spd', 'vsb', 'temp', 'dewp', 'slp', 'pcp01', 'pcp06', 'pcp24', 'sd']
corr_matrix = df[numeric_cols].corr()
pickup_corr = corr_matrix['pickups'].sort_values(ascending=False)

print("\n--- Correlation with Pickups ---")
for var, corr in pickup_corr.items():
    if var != 'pickups':
        direction = "positive" if corr > 0 else "negative"
        print(f"{var:10s}: {corr:7.3f} ({direction})")

# Temperature bins
print("\n--- Temperature Impact ---")
df['temp_bin'] = pd.cut(df['temp'], bins=5)
temp_impact = df.groupby('temp_bin')['pickups'].agg(['mean', 'count'])
print(temp_impact)

# Precipitation impact
print("\n--- Precipitation Impact ---")
precip_impact = df.groupby(df['pcp01'] > 0)['pickups'].agg(['mean', 'count'])
print(precip_impact)
print(f"Difference: {precip_impact.loc[True, 'mean'] - precip_impact.loc[False, 'mean']:.0f} pickups")

# Snow impact
print("\n--- Snow Impact ---")
snow_impact = df.groupby(df['sd'] > 0)['pickups'].agg(['mean', 'count'])
print(snow_impact)
if True in snow_impact.index:
    print(f"Difference: {snow_impact.loc[True, 'mean'] - snow_impact.loc[False, 'mean']:.0f} pickups")

# BIVARIATE ANALYSIS - HOLIDAY
print("\n" + "="*80)
print("6. BIVARIATE ANALYSIS - HOLIDAY IMPACT")
print("="*80)

holiday_stats = df.groupby('is_holiday')['pickups'].agg(['mean', 'sum', 'count'])
print(holiday_stats)
print(f"\nDifference: {holiday_stats.loc[True, 'mean'] - holiday_stats.loc[False, 'mean']:.0f} pickups")
print(f"Percentage change: {100*(holiday_stats.loc[True, 'mean']/holiday_stats.loc[False, 'mean']-1):+.1f}%")

# Holiday hourly pattern
print("\n--- Holiday Hourly Pattern (Peak Hours) ---")
holiday_hourly = df[df['is_holiday']].groupby('hour')['pickups'].mean()
nonholiday_hourly = df[~df['is_holiday']].groupby('hour')['pickups'].mean()
print(f"Holiday peak: {holiday_hourly.idxmax()}:00 ({holiday_hourly.max():.0f} avg)")
print(f"Non-holiday peak: {nonholiday_hourly.idxmax()}:00 ({nonholiday_hourly.max():.0f} avg)")

# SUMMARY AND RECOMMENDATIONS
print("\n" + "="*80)
print("7. KEY INSIGHTS & RECOMMENDATIONS")
print("="*80)

print("\n--- Variables Influencing Pickups ---")
print("Based on correlation analysis, the following factors influence pickups:")
feature_importance = abs(pickup_corr).sort_values(ascending=False)
feature_importance = feature_importance[feature_importance.index != 'pickups']
for i, (var, importance) in enumerate(feature_importance.head(5).items(), 1):
    direction = "increases" if corr_matrix.loc[var, 'pickups'] > 0 else "decreases"
    print(f"{i}. {var}: {importance:.3f} correlation ({direction} pickups)")

print("\n--- Most Influential Factor ---")
top_factor = feature_importance.index[0]
top_corr = corr_matrix.loc[top_factor, 'pickups']
print(f"Factor: {top_factor}")
print(f"Correlation: {top_corr:.3f}")
if top_corr > 0:
    print("Impact: Higher values of this factor are associated with more pickups")
else:
    print("Impact: Higher values of this factor are associated with fewer pickups")

print("\n--- Recommendations to Uber Management ---")
print("\n1. TEMPORAL OPTIMIZATION:")
print(f"   - Increase driver availability during peak hours ({hourly['mean'].idxmax()}:00)")
print(f"   - Focus on {daily['mean'].idxmax()} for maximum demand")
print(f"   - Weekend demand is {100*(weekend.loc[True, 'mean']/weekend.loc[False, 'mean']-1):+.1f}% {'higher' if weekend.loc[True, 'mean'] > weekend.loc[False, 'mean'] else 'lower'} than weekdays")

print("\n2. GEOGRAPHIC OPTIMIZATION:")
top_borough = borough_stats.index[0]
print(f"   - {top_borough} accounts for {100*borough_stats.loc[top_borough, 'sum']/borough_stats['sum'].sum():.1f}% of total pickups")
print(f"   - Allocate more drivers to high-demand boroughs during peak times")

print("\n3. WEATHER-BASED STRATEGIES:")
if abs(corr_matrix.loc['temp', 'pickups']) > 0.1:
    print(f"   - Temperature shows {abs(corr_matrix.loc['temp', 'pickups']):.3f} correlation with pickups")
    print("   - Adjust pricing/driver allocation based on temperature forecasts")
if (df['pcp01'] > 0).sum() > 0:
    precip_diff = precip_impact.loc[True, 'mean'] - precip_impact.loc[False, 'mean']
    print(f"   - Precipitation affects demand: {precip_diff:+.0f} pickups difference")
    print("   - Increase surge pricing and driver incentives during precipitation")

print("\n4. HOLIDAY STRATEGIES:")
holiday_diff = holiday_stats.loc[True, 'mean'] - holiday_stats.loc[False, 'mean']
if holiday_diff > 0:
    print(f"   - Holidays show {holiday_diff:.0f} more average pickups")
    print("   - Increase driver capacity and adjust pricing for holidays")
else:
    print(f"   - Holidays show {abs(holiday_diff):.0f} fewer average pickups")
    print("   - Consider special promotions to boost holiday demand")

print("\n5. DATA-DRIVEN PRICING:")
print("   - Implement dynamic pricing based on:")
print("     * Time of day (peak vs off-peak)")
print("     * Day of week (weekend vs weekday)")
print("     * Weather conditions (precipitation, temperature)")
print("     * Borough-specific demand patterns")

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)

