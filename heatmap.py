import pandas as pd
import plotly.graph_objects as go
from pytz import timezone
import numpy as np

# Read the CSV data
df = pd.read_csv('swimmers.csv')

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
    title='Average Number of Swimmers by Day and Hour',
    xaxis_title='Hour of Day',
    yaxis_title='Day of Week',
    xaxis=dict(tickmode='linear', tick0=0, dtick=1),
)

# Save the plot as a PNG file
try:
    fig.write_image("swimmers.png")
    print("Heatmap has been saved as 'swimmers.png'")
except Exception as e:
    print(f"An error occurred while saving the image: {e}")
    print("Attempting to display the plot instead...")
    fig.show()

# Print the pivot table for debugging
print("\nPivot Table Data:")
print(pivot_table)