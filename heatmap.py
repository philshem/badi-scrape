import pandas as pd
import plotly.graph_objects as go
from pytz import timezone
import numpy as np

# Read the CSV data
df = pd.read_csv('data/swimmers.csv')

# Convert ts_utc to datetime and set it as the index
df['ts_utc'] = pd.to_datetime(df['ts_utc'])
df.set_index('ts_utc', inplace=True)

# Convert UTC to Zürich local time
zurich_tz = timezone('Europe/Zurich')
df.index = df.index.tz_localize('UTC').tz_convert(zurich_tz)

# Extract hour and day of week
df['hour'] = df.index.hour
df['day_of_week'] = df.index.dayofweek

# Create a pivot table for the heatmap
pivot_table = df.pivot_table(values='swimmers', index='day_of_week', columns='hour', aggfunc='mean')

# Fill missing values with 0 or another appropriate value
pivot_table = pivot_table.fillna(0)

# Ensure all days and hours are represented
full_index = pd.Index(range(7), name='day_of_week')
full_columns = pd.Index(range(24), name='hour')
pivot_table = pivot_table.reindex(index=full_index, columns=full_columns, fill_value=0)

# Create the heatmap
fig = go.Figure(data=go.Heatmap(
    z=pivot_table.values,
    x=pivot_table.columns,
    y=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    hoverongaps=False,
    colorscale='Viridis'
))

# Update layout
fig.update_layout(
    title='Hallenbad City (Zürich): Average Count of Swimmers by Day and Hour',
    xaxis_title='Hour of Day',
    yaxis_title='Day of Week',
    xaxis=dict(tickmode='linear', tick0=0, dtick=1),
)

# Save the plot as a PNG file
try:
    fig.write_image("data/swimmers_heatmap.png")
    print("Heatmap has been saved as 'swimmers_heatmap.png'")
except Exception as e:
    print(f"An error occurred while saving the image: {e}")
    print("Attempting to display the plot instead...")
    fig.show()

try:
    # Assuming pivot_table is already defined
    # Reset the index to turn the day_of_week into a column
    pivot_table_reset = pivot_table.reset_index()
    
    # Define day names in the desired order (Monday to Sunday)
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Create a mapping dictionary
    day_map = {i: day for i, day in enumerate(day_names)}
    
    # Replace numeric day_of_week with day names
    pivot_table_reset['day_of_week'] = pivot_table_reset['day_of_week'].map(day_map)
    
    # Convert day_of_week to categorical data type with custom order
    pivot_table_reset['day_of_week'] = pd.Categorical(pivot_table_reset['day_of_week'], categories=day_names, ordered=True)
    
    # Sort the DataFrame by the categorical day order
    pivot_table_reset = pivot_table_reset.sort_values('day_of_week')
    
    # Save to CSV
    pivot_table_reset.to_csv('data/swimmers_heatmap_data.csv', index=False)
    print("Heatmap data has been saved as 'swimmers_heatmap_data.csv'")
except Exception as e:
    print(f"An error occurred while saving the CSV file: {e}")