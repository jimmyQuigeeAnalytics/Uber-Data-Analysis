"""
Comprehensive Uber Data Analysis
Objective: Extract actionable insights around demand patterns
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Load the data
print("="*80)
print("UBER DATA ANALYSIS - COMPREHENSIVE INSIGHTS")
print("="*80)
print("\n1. LOADING DATA...")
df = pd.read_csv('Uber.csv')

# Convert pickup_dt to datetime
df['pickup_dt'] = pd.to_datetime(df['pickup_dt'])

print(f"Dataset shape: {df.shape}")
print(f"\nFirst few rows:")
print(df.head())
print(f"\nData types:")
print(df.dtypes)
print(f"\nMissing values:")
print(df.isnull().sum())
print(f"\nBasic statistics:")
print(df.describe())

# ============================================================================
# DATA PREPARATION
# ============================================================================
print("\n" + "="*80)
print("2. DATA PREPARATION")
print("="*80)

# Extract temporal features
df['date'] = df['pickup_dt'].dt.date
df['hour'] = df['pickup_dt'].dt.hour
df['day_of_week'] = df['pickup_dt'].dt.day_name()
df['month'] = df['pickup_dt'].dt.month
df['month_name'] = df['pickup_dt'].dt.month_name()
df['day_of_month'] = df['pickup_dt'].dt.day
df['is_weekend'] = df['pickup_dt'].dt.dayofweek >= 5

# Convert hday to boolean
df['is_holiday'] = df['hday'] == 'Y'

# Handle missing borough values
df['borough'] = df['borough'].fillna('Unknown')

print(f"\nDate range: {df['pickup_dt'].min()} to {df['pickup_dt'].max()}")
print(f"Total unique dates: {df['date'].nunique()}")
print(f"Boroughs: {df['borough'].unique()}")

# ============================================================================
# UNIVARIATE ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("3. UNIVARIATE ANALYSIS")
print("="*80)

# Create figure for univariate analysis
fig, axes = plt.subplots(3, 3, figsize=(18, 15))
fig.suptitle('Univariate Analysis - Distribution of Variables', fontsize=16, y=1.02)

# 1. Pickups distribution
axes[0, 0].hist(df['pickups'], bins=50, edgecolor='black', alpha=0.7)
axes[0, 0].set_title('Distribution of Pickups')
axes[0, 0].set_xlabel('Number of Pickups')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].axvline(df['pickups'].mean(), color='r', linestyle='--', label=f'Mean: {df["pickups"].mean():.0f}')
axes[0, 0].legend()

# 2. Wind Speed
axes[0, 1].hist(df['spd'], bins=30, edgecolor='black', alpha=0.7, color='skyblue')
axes[0, 1].set_title('Distribution of Wind Speed (mph)')
axes[0, 1].set_xlabel('Wind Speed')
axes[0, 1].set_ylabel('Frequency')

# 3. Visibility
axes[0, 2].hist(df['vsb'], bins=30, edgecolor='black', alpha=0.7, color='lightgreen')
axes[0, 2].set_title('Distribution of Visibility (miles)')
axes[0, 2].set_xlabel('Visibility')
axes[0, 2].set_ylabel('Frequency')

# 4. Temperature
axes[1, 0].hist(df['temp'], bins=30, edgecolor='black', alpha=0.7, color='orange')
axes[1, 0].set_title('Distribution of Temperature (°F)')
axes[1, 0].set_xlabel('Temperature')
axes[1, 0].set_ylabel('Frequency')

# 5. Dew Point
axes[1, 1].hist(df['dewp'], bins=30, edgecolor='black', alpha=0.7, color='pink')
axes[1, 1].set_title('Distribution of Dew Point (°F)')
axes[1, 1].set_xlabel('Dew Point')
axes[1, 1].set_ylabel('Frequency')

# 6. Sea Level Pressure
axes[1, 2].hist(df['slp'], bins=30, edgecolor='black', alpha=0.7, color='purple')
axes[1, 2].set_title('Distribution of Sea Level Pressure')
axes[1, 2].set_xlabel('Sea Level Pressure')
axes[1, 2].set_ylabel('Frequency')

# 7. Precipitation (1-hour)
axes[2, 0].hist(df[df['pcp01'] > 0]['pcp01'], bins=30, edgecolor='black', alpha=0.7, color='blue')
axes[2, 0].set_title('Distribution of 1-hour Precipitation (non-zero)')
axes[2, 0].set_xlabel('Precipitation')
axes[2, 0].set_ylabel('Frequency')

# 8. Snow Depth
axes[2, 1].hist(df[df['sd'] > 0]['sd'], bins=30, edgecolor='black', alpha=0.7, color='cyan')
axes[2, 1].set_title('Distribution of Snow Depth (non-zero)')
axes[2, 1].set_xlabel('Snow Depth (inches)')
axes[2, 1].set_ylabel('Frequency')

# 9. Borough distribution
borough_counts = df['borough'].value_counts()
axes[2, 2].bar(borough_counts.index, borough_counts.values, color='coral')
axes[2, 2].set_title('Distribution of Records by Borough')
axes[2, 2].set_xlabel('Borough')
axes[2, 2].set_ylabel('Count')
axes[2, 2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('univariate_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Univariate analysis plots saved as 'univariate_analysis.png'")

# Summary statistics
print("\n--- Summary Statistics ---")
print(f"\nPickups:")
print(f"  Mean: {df['pickups'].mean():.2f}")
print(f"  Median: {df['pickups'].median():.2f}")
print(f"  Std Dev: {df['pickups'].std():.2f}")
print(f"  Min: {df['pickups'].min()}")
print(f"  Max: {df['pickups'].max()}")

print(f"\nWeather Variables:")
print(f"  Temperature - Mean: {df['temp'].mean():.1f}°F, Range: {df['temp'].min():.1f} to {df['temp'].max():.1f}°F")
print(f"  Wind Speed - Mean: {df['spd'].mean():.1f} mph, Range: {df['spd'].min():.1f} to {df['spd'].max():.1f} mph")
print(f"  Visibility - Mean: {df['vsb'].mean():.1f} miles, Range: {df['vsb'].min():.1f} to {df['vsb'].max():.1f} miles")
print(f"  Precipitation (1hr) - Non-zero: {(df['pcp01'] > 0).sum()} records ({100*(df['pcp01'] > 0).sum()/len(df):.1f}%)")
print(f"  Snow Depth - Non-zero: {(df['sd'] > 0).sum()} records ({100*(df['sd'] > 0).sum()/len(df):.1f}%)")

# ============================================================================
# BIVARIATE ANALYSIS - TEMPORAL PATTERNS
# ============================================================================
print("\n" + "="*80)
print("4. BIVARIATE ANALYSIS - TEMPORAL PATTERNS")
print("="*80)

# Temporal analysis
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Temporal Patterns in Pickups', fontsize=16, y=1.02)

# Hourly pattern
hourly_pickups = df.groupby('hour')['pickups'].mean()
axes[0, 0].plot(hourly_pickups.index, hourly_pickups.values, marker='o', linewidth=2, markersize=6)
axes[0, 0].set_title('Average Pickups by Hour of Day')
axes[0, 0].set_xlabel('Hour of Day')
axes[0, 0].set_ylabel('Average Pickups')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].set_xticks(range(0, 24, 2))

# Day of week pattern
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_pickups = df.groupby('day_of_week')['pickups'].mean().reindex(day_order)
axes[0, 1].bar(range(len(day_pickups)), day_pickups.values, color='steelblue')
axes[0, 1].set_title('Average Pickups by Day of Week')
axes[0, 1].set_xlabel('Day of Week')
axes[0, 1].set_ylabel('Average Pickups')
axes[0, 1].set_xticks(range(len(day_pickups)))
axes[0, 1].set_xticklabels(day_pickups.index, rotation=45, ha='right')
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Monthly pattern
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
month_pickups = df.groupby('month_name')['pickups'].mean().reindex(month_order)
axes[1, 0].bar(range(len(month_pickups)), month_pickups.values, color='coral')
axes[1, 0].set_title('Average Pickups by Month')
axes[1, 0].set_xlabel('Month')
axes[1, 0].set_ylabel('Average Pickups')
axes[1, 0].set_xticks(range(len(month_pickups)))
axes[1, 0].set_xticklabels(month_pickups.index, rotation=45, ha='right')
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Weekend vs Weekday
weekend_pickups = df.groupby('is_weekend')['pickups'].mean()
axes[1, 1].bar(['Weekday', 'Weekend'], weekend_pickups.values, color=['skyblue', 'orange'])
axes[1, 1].set_title('Average Pickups: Weekday vs Weekend')
axes[1, 1].set_ylabel('Average Pickups')
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('temporal_patterns.png', dpi=300, bbox_inches='tight')
print("\n✓ Temporal patterns plot saved as 'temporal_patterns.png'")

# Print insights
print(f"\n--- Temporal Insights ---")
print(f"Peak hour: {hourly_pickups.idxmax()}:00 ({hourly_pickups.max():.0f} avg pickups)")
print(f"Lowest hour: {hourly_pickups.idxmin()}:00 ({hourly_pickups.min():.0f} avg pickups)")
print(f"Peak day: {day_pickups.idxmax()} ({day_pickups.max():.0f} avg pickups)")
print(f"Lowest day: {day_pickups.idxmin()} ({day_pickups.min():.0f} avg pickups)")
print(f"Weekend avg: {weekend_pickups[True]:.0f} pickups")
print(f"Weekday avg: {weekend_pickups[False]:.0f} pickups")
print(f"Weekend/Weekday ratio: {weekend_pickups[True]/weekend_pickups[False]:.2f}")

# ============================================================================
# BIVARIATE ANALYSIS - BOROUGH PATTERNS
# ============================================================================
print("\n" + "="*80)
print("5. BIVARIATE ANALYSIS - BOROUGH PATTERNS")
print("="*80)

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Pickup Patterns by Borough', fontsize=16, y=1.02)

# Total pickups by borough
borough_total = df.groupby('borough')['pickups'].sum().sort_values(ascending=False)
axes[0, 0].bar(borough_total.index, borough_total.values, color='steelblue')
axes[0, 0].set_title('Total Pickups by Borough')
axes[0, 0].set_xlabel('Borough')
axes[0, 0].set_ylabel('Total Pickups')
axes[0, 0].tick_params(axis='x', rotation=45)
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Average pickups by borough
borough_avg = df.groupby('borough')['pickups'].mean().sort_values(ascending=False)
axes[0, 1].bar(borough_avg.index, borough_avg.values, color='coral')
axes[0, 1].set_title('Average Pickups per Record by Borough')
axes[0, 1].set_xlabel('Borough')
axes[0, 1].set_ylabel('Average Pickups')
axes[0, 1].tick_params(axis='x', rotation=45)
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Hourly pattern by borough (top 3)
top_boroughs = borough_total.head(3).index
for borough in top_boroughs:
    borough_hourly = df[df['borough'] == borough].groupby('hour')['pickups'].mean()
    axes[1, 0].plot(borough_hourly.index, borough_hourly.values, marker='o', label=borough, linewidth=2)
axes[1, 0].set_title('Hourly Pickup Pattern by Borough (Top 3)')
axes[1, 0].set_xlabel('Hour of Day')
axes[1, 0].set_ylabel('Average Pickups')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)
axes[1, 0].set_xticks(range(0, 24, 2))

# Day of week pattern by borough (top 3)
for borough in top_boroughs:
    borough_daily = df[df['borough'] == borough].groupby('day_of_week')['pickups'].mean().reindex(day_order)
    axes[1, 1].plot(range(len(borough_daily)), borough_daily.values, marker='o', label=borough, linewidth=2)
axes[1, 1].set_title('Day of Week Pattern by Borough (Top 3)')
axes[1, 1].set_xlabel('Day of Week')
axes[1, 1].set_ylabel('Average Pickups')
axes[1, 1].set_xticks(range(len(day_order)))
axes[1, 1].set_xticklabels(day_order, rotation=45, ha='right')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('borough_patterns.png', dpi=300, bbox_inches='tight')
print("\n✓ Borough patterns plot saved as 'borough_patterns.png'")

print(f"\n--- Borough Insights ---")
for borough in borough_total.index:
    print(f"{borough}: Total={borough_total[borough]:,.0f}, Avg={borough_avg[borough]:.1f}")

# ============================================================================
# BIVARIATE ANALYSIS - WEATHER IMPACT
# ============================================================================
print("\n" + "="*80)
print("6. BIVARIATE ANALYSIS - WEATHER IMPACT ON PICKUPS")
print("="*80)

# Correlation analysis
numeric_cols = ['pickups', 'spd', 'vsb', 'temp', 'dewp', 'slp', 'pcp01', 'pcp06', 'pcp24', 'sd']
correlation_matrix = df[numeric_cols].corr()

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Weather Impact on Pickups', fontsize=16, y=1.02)

# Correlation heatmap
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
            square=True, ax=axes[0, 0], cbar_kws={'shrink': 0.8})
axes[0, 0].set_title('Correlation Matrix: Pickups vs Weather Variables')

# Temperature vs Pickups
df['temp_bin'] = pd.cut(df['temp'], bins=10)
temp_pickups = df.groupby('temp_bin')['pickups'].mean()
axes[0, 1].plot(range(len(temp_pickups)), temp_pickups.values, marker='o', linewidth=2, markersize=8, color='orange')
axes[0, 1].set_title('Average Pickups by Temperature')
axes[0, 1].set_xlabel('Temperature Bin')
axes[0, 1].set_ylabel('Average Pickups')
axes[0, 1].set_xticks(range(len(temp_pickups)))
axes[0, 1].set_xticklabels([f"{t.left:.0f}°F" for t in temp_pickups.index], rotation=45, ha='right')
axes[0, 1].grid(True, alpha=0.3)

# Wind Speed vs Pickups
df['spd_bin'] = pd.cut(df['spd'], bins=10)
spd_pickups = df.groupby('spd_bin')['pickups'].mean()
axes[0, 2].plot(range(len(spd_pickups)), spd_pickups.values, marker='o', linewidth=2, markersize=8, color='skyblue')
axes[0, 2].set_title('Average Pickups by Wind Speed')
axes[0, 2].set_xlabel('Wind Speed Bin (mph)')
axes[0, 2].set_ylabel('Average Pickups')
axes[0, 2].set_xticks(range(len(spd_pickups)))
axes[0, 2].set_xticklabels([f"{s.left:.0f}" for s in spd_pickups.index], rotation=45, ha='right')
axes[0, 2].grid(True, alpha=0.3)

# Visibility vs Pickups
df['vsb_bin'] = pd.cut(df['vsb'], bins=10)
vsb_pickups = df.groupby('vsb_bin')['pickups'].mean()
axes[1, 0].plot(range(len(vsb_pickups)), vsb_pickups.values, marker='o', linewidth=2, markersize=8, color='lightgreen')
axes[1, 0].set_title('Average Pickups by Visibility')
axes[1, 0].set_xlabel('Visibility Bin (miles)')
axes[1, 0].set_ylabel('Average Pickups')
axes[1, 0].set_xticks(range(len(vsb_pickups)))
axes[1, 0].set_xticklabels([f"{v.left:.1f}" for v in vsb_pickups.index], rotation=45, ha='right')
axes[1, 0].grid(True, alpha=0.3)

# Precipitation impact
precip_comparison = df.groupby(df['pcp01'] > 0)['pickups'].mean()
axes[1, 1].bar(['No Precipitation', 'With Precipitation'], precip_comparison.values, 
               color=['lightblue', 'darkblue'])
axes[1, 1].set_title('Average Pickups: With vs Without Precipitation')
axes[1, 1].set_ylabel('Average Pickups')
axes[1, 1].grid(True, alpha=0.3, axis='y')

# Snow impact
snow_comparison = df.groupby(df['sd'] > 0)['pickups'].mean()
axes[1, 2].bar(['No Snow', 'With Snow'], snow_comparison.values, 
               color=['lightgray', 'darkgray'])
axes[1, 2].set_title('Average Pickups: With vs Without Snow')
axes[1, 2].set_ylabel('Average Pickups')
axes[1, 2].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('weather_impact.png', dpi=300, bbox_inches='tight')
print("\n✓ Weather impact plots saved as 'weather_impact.png'")

# Print correlation insights
print("\n--- Weather Correlation with Pickups ---")
pickup_corr = correlation_matrix['pickups'].sort_values(ascending=False)
for var, corr in pickup_corr.items():
    if var != 'pickups':
        print(f"{var:10s}: {corr:6.3f}")

# ============================================================================
# BIVARIATE ANALYSIS - HOLIDAY IMPACT
# ============================================================================
print("\n" + "="*80)
print("7. BIVARIATE ANALYSIS - HOLIDAY IMPACT")
print("="*80)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Holiday Impact on Pickups', fontsize=16, y=1.02)

# Holiday vs Non-holiday
holiday_pickups = df.groupby('is_holiday')['pickups'].mean()
axes[0].bar(['Non-Holiday', 'Holiday'], holiday_pickups.values, color=['steelblue', 'gold'])
axes[0].set_title('Average Pickups: Holiday vs Non-Holiday')
axes[0].set_ylabel('Average Pickups')
axes[0].grid(True, alpha=0.3, axis='y')

# Holiday hourly pattern
holiday_hourly = df[df['is_holiday']].groupby('hour')['pickups'].mean()
nonholiday_hourly = df[~df['is_holiday']].groupby('hour')['pickups'].mean()
axes[1].plot(holiday_hourly.index, holiday_hourly.values, marker='o', label='Holiday', linewidth=2)
axes[1].plot(nonholiday_hourly.index, nonholiday_hourly.values, marker='s', label='Non-Holiday', linewidth=2)
axes[1].set_title('Hourly Pattern: Holiday vs Non-Holiday')
axes[1].set_xlabel('Hour of Day')
axes[1].set_ylabel('Average Pickups')
axes[1].legend()
axes[1].grid(True, alpha=0.3)
axes[1].set_xticks(range(0, 24, 2))

plt.tight_layout()
plt.savefig('holiday_impact.png', dpi=300, bbox_inches='tight')
print("\n✓ Holiday impact plots saved as 'holiday_impact.png'")

print(f"\n--- Holiday Insights ---")
print(f"Holiday average: {holiday_pickups[True]:.0f} pickups")
print(f"Non-holiday average: {holiday_pickups[False]:.0f} pickups")
print(f"Difference: {holiday_pickups[True] - holiday_pickups[False]:.0f} pickups ({100*(holiday_pickups[True]/holiday_pickups[False]-1):.1f}%)")

# ============================================================================
# ADVANCED ANALYSIS - INTERACTION EFFECTS
# ============================================================================
print("\n" + "="*80)
print("8. ADVANCED ANALYSIS - INTERACTION EFFECTS")
print("="*80)

# Weekend + Hour interaction
weekend_hour = df.groupby(['is_weekend', 'hour'])['pickups'].mean().unstack(0)
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(weekend_hour.index, weekend_hour[False], marker='o', label='Weekday', linewidth=2)
ax.plot(weekend_hour.index, weekend_hour[True], marker='s', label='Weekend', linewidth=2)
ax.set_title('Hourly Pickup Pattern: Weekend vs Weekday', fontsize=14)
ax.set_xlabel('Hour of Day')
ax.set_ylabel('Average Pickups')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_xticks(range(0, 24, 2))
plt.tight_layout()
plt.savefig('weekend_hour_interaction.png', dpi=300, bbox_inches='tight')
print("\n✓ Weekend-hour interaction plot saved as 'weekend_hour_interaction.png'")

# Borough + Hour interaction (heatmap)
borough_hour = df.groupby(['borough', 'hour'])['pickups'].mean().unstack(0)
fig, ax = plt.subplots(figsize=(16, 8))
sns.heatmap(borough_hour.T, annot=False, fmt='.0f', cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Average Pickups'})
ax.set_title('Heatmap: Average Pickups by Borough and Hour', fontsize=14)
ax.set_xlabel('Hour of Day')
ax.set_ylabel('Borough')
plt.tight_layout()
plt.savefig('borough_hour_heatmap.png', dpi=300, bbox_inches='tight')
print("\n✓ Borough-hour heatmap saved as 'borough_hour_heatmap.png'")

# ============================================================================
# STATISTICAL SUMMARY
# ============================================================================
print("\n" + "="*80)
print("9. STATISTICAL SUMMARY & KEY INSIGHTS")
print("="*80)

# Calculate feature importance (correlation with pickups)
feature_importance = abs(correlation_matrix['pickups']).sort_values(ascending=False)
feature_importance = feature_importance[feature_importance.index != 'pickups']

print("\n--- Feature Importance (Absolute Correlation with Pickups) ---")
for feature, importance in feature_importance.items():
    direction = "positive" if correlation_matrix.loc[feature, 'pickups'] > 0 else "negative"
    print(f"{feature:10s}: {importance:6.3f} ({direction})")

# Borough contribution
print("\n--- Borough Contribution to Total Pickups ---")
borough_pct = (borough_total / borough_total.sum() * 100).sort_values(ascending=False)
for borough, pct in borough_pct.items():
    print(f"{borough:15s}: {pct:5.1f}%")

# Peak times
print("\n--- Peak Demand Times ---")
print(f"Peak Hour: {hourly_pickups.idxmax()}:00 ({hourly_pickups.max():.0f} avg pickups)")
print(f"Peak Day: {day_pickups.idxmax()} ({day_pickups.max():.0f} avg pickups)")
print(f"Peak Month: {month_pickups.idxmax()} ({month_pickups.max():.0f} avg pickups)")

# Weather extremes
print("\n--- Weather Impact Summary ---")
print(f"Temperature correlation: {correlation_matrix.loc['temp', 'pickups']:.3f}")
print(f"Precipitation impact: {precip_comparison[True] - precip_comparison[False]:.0f} pickups difference")
print(f"Snow impact: {snow_comparison[True] - snow_comparison[False]:.0f} pickups difference")

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print("\nAll visualizations have been saved as PNG files.")
print("Review the plots and statistical summaries above for actionable insights.")

