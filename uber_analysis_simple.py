"""
Comprehensive Uber Data Analysis - Simplified Version
Objective: Extract actionable insights around demand patterns
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("="*80)
print("UBER DATA ANALYSIS - COMPREHENSIVE INSIGHTS")
print("="*80)

# Load data
print("\n1. LOADING DATA...")
try:
    df = pd.read_csv('Uber.csv')
    df['pickup_dt'] = pd.to_datetime(df['pickup_dt'])
    print(f"✓ Data loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns")
except Exception as e:
    print(f"Error loading data: {e}")
    exit(1)

# Data preparation
print("\n2. DATA PREPARATION...")
df['hour'] = df['pickup_dt'].dt.hour
df['day_of_week'] = df['pickup_dt'].dt.day_name()
df['month'] = df['pickup_dt'].dt.month
df['month_name'] = df['pickup_dt'].dt.month_name()
df['is_weekend'] = df['pickup_dt'].dt.dayofweek >= 5
df['is_holiday'] = df['hday'] == 'Y'
df['borough'] = df['borough'].fillna('Unknown')

print(f"✓ Date range: {df['pickup_dt'].min()} to {df['pickup_dt'].max()}")

# Basic statistics
print("\n3. BASIC STATISTICS...")
print(f"\nPickups Statistics:")
print(f"  Mean: {df['pickups'].mean():.2f}")
print(f"  Median: {df['pickups'].median():.2f}")
print(f"  Std: {df['pickups'].std():.2f}")
print(f"  Min: {df['pickups'].min()}")
print(f"  Max: {df['pickups'].max()}")

# Univariate analysis - Pickups distribution
print("\n4. CREATING VISUALIZATIONS...")
try:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df['pickups'], bins=50, edgecolor='black', alpha=0.7)
    ax.axvline(df['pickups'].mean(), color='r', linestyle='--', label=f'Mean: {df["pickups"].mean():.0f}')
    ax.set_title('Distribution of Pickups')
    ax.set_xlabel('Number of Pickups')
    ax.set_ylabel('Frequency')
    ax.legend()
    plt.tight_layout()
    plt.savefig('1_univariate_pickups.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 1_univariate_pickups.png")
except Exception as e:
    print(f"Error creating pickups histogram: {e}")

# Temporal patterns - Hourly
try:
    hourly_pickups = df.groupby('hour')['pickups'].mean()
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(hourly_pickups.index, hourly_pickups.values, marker='o', linewidth=2, markersize=6)
    ax.set_title('Average Pickups by Hour of Day')
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Average Pickups')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(range(0, 24, 2))
    plt.tight_layout()
    plt.savefig('2_hourly_pattern.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 2_hourly_pattern.png")
    print(f"  Peak hour: {hourly_pickups.idxmax()}:00 ({hourly_pickups.max():.0f} avg)")
except Exception as e:
    print(f"Error creating hourly plot: {e}")

# Day of week pattern
try:
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_pickups = df.groupby('day_of_week')['pickups'].mean().reindex(day_order)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(range(len(day_pickups)), day_pickups.values, color='steelblue')
    ax.set_title('Average Pickups by Day of Week')
    ax.set_xlabel('Day of Week')
    ax.set_ylabel('Average Pickups')
    ax.set_xticks(range(len(day_pickups)))
    ax.set_xticklabels(day_pickups.index, rotation=45, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('3_daily_pattern.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 3_daily_pattern.png")
    print(f"  Peak day: {day_pickups.idxmax()} ({day_pickups.max():.0f} avg)")
except Exception as e:
    print(f"Error creating daily plot: {e}")

# Monthly pattern
try:
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    month_pickups = df.groupby('month_name')['pickups'].mean().reindex(month_order)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(range(len(month_pickups)), month_pickups.values, color='coral')
    ax.set_title('Average Pickups by Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Average Pickups')
    ax.set_xticks(range(len(month_pickups)))
    ax.set_xticklabels(month_pickups.index, rotation=45, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('4_monthly_pattern.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 4_monthly_pattern.png")
except Exception as e:
    print(f"Error creating monthly plot: {e}")

# Borough analysis
try:
    borough_total = df.groupby('borough')['pickups'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(borough_total.index, borough_total.values, color='steelblue')
    ax.set_title('Total Pickups by Borough')
    ax.set_xlabel('Borough')
    ax.set_ylabel('Total Pickups')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('5_borough_total.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 5_borough_total.png")
except Exception as e:
    print(f"Error creating borough plot: {e}")

# Weather correlation
try:
    numeric_cols = ['pickups', 'spd', 'vsb', 'temp', 'dewp', 'slp', 'pcp01', 'pcp06', 'pcp24', 'sd']
    correlation_matrix = df[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
                square=True, ax=ax, cbar_kws={'shrink': 0.8})
    ax.set_title('Correlation Matrix: Pickups vs Weather Variables')
    plt.tight_layout()
    plt.savefig('6_correlation_matrix.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 6_correlation_matrix.png")
    
    # Print correlations
    print("\n--- Weather Correlation with Pickups ---")
    pickup_corr = correlation_matrix['pickups'].sort_values(ascending=False)
    for var, corr in pickup_corr.items():
        if var != 'pickups':
            print(f"  {var:10s}: {corr:6.3f}")
except Exception as e:
    print(f"Error creating correlation plot: {e}")

# Temperature impact
try:
    df['temp_bin'] = pd.cut(df['temp'], bins=10)
    temp_pickups = df.groupby('temp_bin')['pickups'].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(range(len(temp_pickups)), temp_pickups.values, marker='o', linewidth=2, markersize=8, color='orange')
    ax.set_title('Average Pickups by Temperature')
    ax.set_xlabel('Temperature Bin')
    ax.set_ylabel('Average Pickups')
    ax.set_xticks(range(len(temp_pickups)))
    ax.set_xticklabels([f"{t.left:.0f}°F" for t in temp_pickups.index], rotation=45, ha='right')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('7_temperature_impact.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 7_temperature_impact.png")
except Exception as e:
    print(f"Error creating temperature plot: {e}")

# Precipitation impact
try:
    precip_comparison = df.groupby(df['pcp01'] > 0)['pickups'].mean()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(['No Precipitation', 'With Precipitation'], precip_comparison.values, 
           color=['lightblue', 'darkblue'])
    ax.set_title('Average Pickups: With vs Without Precipitation')
    ax.set_ylabel('Average Pickups')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('8_precipitation_impact.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 8_precipitation_impact.png")
    print(f"  No precip: {precip_comparison[False]:.0f} avg, With precip: {precip_comparison[True]:.0f} avg")
except Exception as e:
    print(f"Error creating precipitation plot: {e}")

# Holiday impact
try:
    holiday_pickups = df.groupby('is_holiday')['pickups'].mean()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(['Non-Holiday', 'Holiday'], holiday_pickups.values, color=['steelblue', 'gold'])
    ax.set_title('Average Pickups: Holiday vs Non-Holiday')
    ax.set_ylabel('Average Pickups')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('9_holiday_impact.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 9_holiday_impact.png")
    print(f"  Non-holiday: {holiday_pickups[False]:.0f} avg, Holiday: {holiday_pickups[True]:.0f} avg")
except Exception as e:
    print(f"Error creating holiday plot: {e}")

# Weekend vs Weekday
try:
    weekend_pickups = df.groupby('is_weekend')['pickups'].mean()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(['Weekday', 'Weekend'], weekend_pickups.values, color=['skyblue', 'orange'])
    ax.set_title('Average Pickups: Weekday vs Weekend')
    ax.set_ylabel('Average Pickups')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('10_weekend_impact.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 10_weekend_impact.png")
except Exception as e:
    print(f"Error creating weekend plot: {e}")

# Borough hourly pattern (top 3)
try:
    borough_total = df.groupby('borough')['pickups'].sum().sort_values(ascending=False)
    top_boroughs = borough_total.head(3).index
    fig, ax = plt.subplots(figsize=(12, 6))
    for borough in top_boroughs:
        borough_hourly = df[df['borough'] == borough].groupby('hour')['pickups'].mean()
        ax.plot(borough_hourly.index, borough_hourly.values, marker='o', label=borough, linewidth=2)
    ax.set_title('Hourly Pickup Pattern by Borough (Top 3)')
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Average Pickups')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xticks(range(0, 24, 2))
    plt.tight_layout()
    plt.savefig('11_borough_hourly.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Saved: 11_borough_hourly.png")
except Exception as e:
    print(f"Error creating borough hourly plot: {e}")

# Generate summary report
print("\n" + "="*80)
print("SUMMARY REPORT")
print("="*80)

# Key insights
print("\n--- KEY INSIGHTS ---")

# Temporal
hourly_pickups = df.groupby('hour')['pickups'].mean()
day_pickups = df.groupby('day_of_week')['pickups'].mean().reindex(day_order)
month_pickups = df.groupby('month_name')['pickups'].mean().reindex(month_order)
weekend_pickups = df.groupby('is_weekend')['pickups'].mean()

print(f"\n1. TEMPORAL PATTERNS:")
print(f"   - Peak hour: {hourly_pickups.idxmax()}:00 ({hourly_pickups.max():.0f} avg pickups)")
print(f"   - Lowest hour: {hourly_pickups.idxmin()}:00 ({hourly_pickups.min():.0f} avg pickups)")
print(f"   - Peak day: {day_pickups.idxmax()} ({day_pickups.max():.0f} avg pickups)")
print(f"   - Weekend vs Weekday: {weekend_pickups[True]:.0f} vs {weekend_pickups[False]:.0f} pickups")

# Borough
borough_total = df.groupby('borough')['pickups'].sum().sort_values(ascending=False)
borough_avg = df.groupby('borough')['pickups'].mean().sort_values(ascending=False)
print(f"\n2. BOROUGH PATTERNS:")
for borough in borough_total.head(3).index:
    print(f"   - {borough}: {borough_total[borough]:,.0f} total, {borough_avg[borough]:.1f} avg per record")

# Weather
numeric_cols = ['pickups', 'spd', 'vsb', 'temp', 'dewp', 'slp', 'pcp01', 'pcp06', 'pcp24', 'sd']
correlation_matrix = df[numeric_cols].corr()
pickup_corr = abs(correlation_matrix['pickups']).sort_values(ascending=False)
pickup_corr = pickup_corr[pickup_corr.index != 'pickups']

print(f"\n3. WEATHER IMPACT (Top 3 by absolute correlation):")
for i, (var, corr) in enumerate(pickup_corr.head(3).items(), 1):
    direction = "positive" if correlation_matrix.loc[var, 'pickups'] > 0 else "negative"
    print(f"   {i}. {var}: {abs(corr):.3f} ({direction})")

# Holiday
holiday_pickups = df.groupby('is_holiday')['pickups'].mean()
print(f"\n4. HOLIDAY IMPACT:")
print(f"   - Holiday: {holiday_pickups[True]:.0f} avg pickups")
print(f"   - Non-holiday: {holiday_pickups[False]:.0f} avg pickups")
print(f"   - Difference: {holiday_pickups[True] - holiday_pickups[False]:.0f} ({100*(holiday_pickups[True]/holiday_pickups[False]-1):+.1f}%)")

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)

