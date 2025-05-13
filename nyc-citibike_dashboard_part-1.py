################################################ DIVVY BIKES DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt


########################### Initial settings for the dashboard ##################################################################


st.set_page_config(page_title = 'New York citi Bikes Strategy Dashboard', layout='wide')
st.title("New York citi Bikes Strategy Dashboard")
st.markdown("The dashboard will help the  business strategy department assess the current logistics model of bike distribution across the city and identify expansion opportunities.")
st.markdown("Right now, citi bikes runs into a situation where customers complain about bikes not being avaibale at certain times.This will circumvent availability issues and ensure the company’s position as a leader in eco-friendly transportation solutions in the city.")

########################## Import data ###########################################################################################

df_weather = pd.read_csv('trips_weather.csv')
top20 = pd.read_csv('top20_station.csv', index_col = 0)

# ######################################### DEFINE THE CHARTS #####################################################################

## Bar chart

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Blues'}))
fig.update_layout(
    title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width=True)


## Line chart 
df_weather = pd.read_csv('trips_weather.csv', parse_dates=['date'])
df_weather.sort_values('date', inplace=True)

fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

fig_2.add_trace(
    go.Scatter(
        x=df_weather['date'],
        y=df_weather['trip_count'],
        name='Daily Bike Rides',
        line=dict(color='blue')
    ),
    secondary_y=False
)

fig_2.add_trace(
    go.Scatter(
        x=df_weather['date'],
        y=df_weather['avgTemp'],
        name='Avg Temperature (°C)',
        line=dict(color='red')
    ),
    secondary_y=True
)

fig_2.update_layout(
    title='Bike Rides and Temperature Over Time in NYC',
    xaxis_title='Date',
    yaxis_title='Trip Count',
    yaxis2_title='Avg Temperature (°C)',
    legend=dict(x=0.01, y=0.99),
    plot_bgcolor='white',
    title_x=0.5
)

st.plotly_chart(fig_2, use_container_width=True)


### Add the map ###

path_to_html = "nyc-citibike.html" 

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Aggregated citi Bike Trips in New York")
st.components.v1.html(html_data,height=1000)
