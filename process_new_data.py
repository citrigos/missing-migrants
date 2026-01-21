#!/usr/bin/env python3
"""
Process the new Missing Migrants data to match the format of the existing dataset.
"""
import pandas as pd
import re

def extract_coordinates(coord_string):
    """Extract X and Y coordinates from coordinate string (lat, lon format)."""
    if pd.isna(coord_string):
        return None, None

    # Try POINT format first (old format)
    match = re.search(r'POINT\s*\(([0-9.-]+)\s+([0-9.-]+)\)', str(coord_string))
    if match:
        return float(match.group(1)), float(match.group(2))

    # Try "lat, lon" format (new format)
    try:
        parts = str(coord_string).split(',')
        if len(parts) == 2:
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
            return lon, lat  # Return as (X=lon, Y=lat)
    except (ValueError, AttributeError):
        pass

    return None, None

def get_season(month):
    """Determine season based on month."""
    if pd.isna(month):
        return None

    month = str(month).strip().lower()

    # Winter: December, January, February
    if month in ['december', 'january', 'february', '12', '1', '2']:
        return 'Winter'
    # Spring: March, April, May
    elif month in ['march', 'april', 'may', '3', '4', '5']:
        return 'Spring'
    # Summer: June, July, August
    elif month in ['june', 'july', 'august', '6', '7', '8']:
        return 'Summer'
    # Fall: September, October, November
    elif month in ['september', 'october', 'november', '9', '10', '11']:
        return 'Fall'
    else:
        return None

def get_cause_abbreviation(cause):
    """Get abbreviated cause of death."""
    if pd.isna(cause):
        return 'Unknown'

    cause = str(cause).lower()

    if 'drown' in cause:
        return 'Drowning'
    elif 'harsh' in cause or 'environmental' in cause:
        return 'Harsh conditions'
    elif 'vehicle' in cause or 'accident' in cause:
        return 'Vehicle accident'
    elif 'violence' in cause:
        return 'Violence'
    elif 'sickness' in cause or 'medical' in cause or 'illness' in cause:
        return 'Sickness'
    elif 'mixed' in cause or 'unknown' in cause:
        return 'Mixed or unknown'
    else:
        return cause.title()

# Load the new data
print("Loading new data...")
df = pd.read_csv('data/Missing_Migrants_Global_Figures_allData_NEW.csv')
print(f"Loaded {len(df)} rows from 2014 to {df['Incident Year'].max()}")

# Extract X and Y coordinates
print("Extracting coordinates...")
coords = df['Coordinates'].apply(extract_coordinates)
df['X'] = coords.apply(lambda x: x[0])
df['Y'] = coords.apply(lambda x: x[1])

# Add Season column
print("Adding season...")
df['Season'] = df['Month'].apply(get_season)

# Add Cause of Death Abbreviation
print("Adding cause of death abbreviations...")
df['Cause of Death Abbreviation'] = df['Cause of Death'].apply(get_cause_abbreviation)

# Rename columns to match old format
print("Renaming columns...")
df = df.rename(columns={
    'Incident Year': 'Incident year',
    'Month': 'Reported Month',
    'Migration Route': 'Migration route',
    'Location of Incident': 'Location of death'
})

# Reorder columns to match old format
columns_order = [
    'Main ID', 'Incident ID', 'Incident Type', 'Region of Incident',
    'Incident year', 'Reported Month', 'Number of Dead',
    'Minimum Estimated Number of Missing', 'Total Number of Dead and Missing',
    'Number of Survivors', 'Number of Females', 'Number of Males',
    'Number of Children', 'Country of Origin', 'Region of Origin',
    'Cause of Death', 'Migration route', 'Location of death',
    'Information Source', 'Coordinates', 'UNSD Geographical Grouping',
    'X', 'Y', 'Season', 'Cause of Death Abbreviation'
]

# Only include columns that exist
columns_to_keep = [col for col in columns_order if col in df.columns]
df = df[columns_to_keep]

# Remove rows with missing coordinates
print(f"Removing rows with missing coordinates...")
initial_count = len(df)
df = df.dropna(subset=['X', 'Y'])
print(f"Removed {initial_count - len(df)} rows with missing coordinates")

# Save the processed data
output_file = 'data/Missing_Migrants_Global_Figures_filtered.csv'
print(f"\nSaving processed data to {output_file}...")
df.to_csv(output_file, index=False)

print(f"\nProcessing complete!")
print(f"Final dataset: {len(df)} rows")
print(f"Year range: {df['Incident year'].min()} to {df['Incident year'].max()}")
print(f"\nRows by year:")
print(df['Incident year'].value_counts().sort_index())
