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
pivot_table = df.pivot_table(values='swimmers', index='day_of_week', columns='hour', aggfunc='median')

# Fill missing values with 0 or another appropriate value
pivot_table = pivot_table.fillna(0)

# Ensure all days and hours are represented
full_index = pd.Index(range(7), name='day_of_week')
full_columns = pd.Index(range(24), name='hour')
pivot_table = pivot_table.reindex(index=full_index, columns=full_columns, fill_value=0)

# Define day names in the correct order (Monday to Sunday)
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Create the heatmap
fig = go.Figure(data=go.Heatmap(
    z=pivot_table.values,
    x=pivot_table.columns,
    y=day_names,  # Use the day_names list directly here
    hoverongaps=False,
    colorscale='Viridis'
))

# Update layout
fig.update_layout(
    title='Hallenbad City (Zürich): Median Count of Swimmers by Day and Hour',
    xaxis_title='Hour of Day',
    yaxis_title='Day of Week',
    xaxis=dict(tickmode='linear', tick0=0, dtick=1),
    yaxis=dict(autorange='reversed')  # This ensures Monday is at the top
)

# Save the plot as a PNG file
try:
    fig.write_image("data/swimmers_heatmap.png")
    print("Heatmap has been saved as 'swimmers_heatmap.png'")
except Exception as e:
    print(f"An error occurred while saving the image: {e}")
    print("Attempting to display the plot instead...")
    fig.show()

# Save the data to CSV
try:
    # Create a new DataFrame with named days
    pivot_table_reset = pivot_table.reset_index()
    pivot_table_reset['day_of_week'] = pivot_table_reset['day_of_week'].map(dict(enumerate(day_names)))
    
    # Save to CSV
    pivot_table_reset.to_csv('data/swimmers_heatmap_data.csv', index=False)
    print("Heatmap data has been saved as 'swimmers_heatmap_data.csv'")
except Exception as e:
    print(f"An error occurred while saving the CSV file: {e}")