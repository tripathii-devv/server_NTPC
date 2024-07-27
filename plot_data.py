import pandas as pd
import plotly.express as px
from datetime import datetime

# Load the downtime log
log_df = pd.read_csv('downtime_log.csv')

# Convert timestamp to datetime
log_df['timestamp'] = pd.to_datetime(log_df['timestamp'])

# Extract month and year for grouping
log_df['month'] = log_df['timestamp'].dt.to_period('M')

# Calculate uptime and downtime
availability = log_df.groupby(['month', 'device', 'status']).size().unstack(fill_value=0)

# Plot the chart
fig = px.bar(availability, x=availability.index, y=['up', 'down'],
             labels={'value': 'Count', 'month': 'Month'},
             title='Monthly Uptime/DownTime')

fig.show()
