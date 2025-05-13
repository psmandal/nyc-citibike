################################################ CITI BIKES DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from PIL import Image


########################### Initial settings for the dashboard ##################################################################

st.set_page_config(page_title='Citi Bikes Strategy Dashboard', layout='wide')
st.title("Citi Bikes Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
    ["Intro page", "Weather component and bike usage",
     "Most popular stations",
     "Interactive map with aggregated bike trips", "Recommendations"])

########################## Import data ###########################################################################################

df = pd.read_csv('trips_weather.csv')
top20 = pd.read_csv('top20_station.csv', index_col = 0)
def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

df['date'] = pd.to_datetime(df['date'])
df['season'] = df['date'].apply(get_season)

# ######################################### DEFINE THE PAGES #####################################################################

### Intro page

if page == "Intro page":
    st.markdown("#### This dashboard aims at providing helpful insights on the expansion problems Citi Bikes currently faces.")
    st.markdown("Right now, Citi bikes runs into a situation where customers complain about bikes not being available at certain times. This analysis will look at the potential reasons behind this. The dashboard is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis our team looked at.")

    myImage = Image.open("bike_pic.jpg") 
    st.image(myImage, caption="Citi Bike Image")

### Most popular stations page

    # Create the season variable

elif page == 'Most popular stations':
    
    # Create the filter on the side bar
    
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
    default=df['season'].unique())

    df1 = df.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['trip_count'].sum()) 
    st.metric(label='Total Bike Rides', value=f"{int(total_rides):,}")
    
    # Bar chart
    
    fig = go.Figure(go.Bar(
    x=top20['start_station_name'],
    y=top20['value'],
    marker={'color': top20['value'], 'colorscale': 'Blues'}
))

    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color':top20['value'],'colorscale': 'Blues'}))
    fig.update_layout(
    title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("From the bar chart it is clear that there are some start stations that are more popular than others - in the top 3 we can see W 21 St & 6 Ave, Broadway & W 58 St, West St & Chambers St. There is a big jump between the highest and lowest bars of the plot, indicating some clear preferences for the leading stations. This is a finding that we could cross reference with the interactive map that you can access through the side bar select box.")


elif page == 'Weather component and bike usage':

    ### Create the dual axis line chart page ###
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
    st.markdown("There is an obvious correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to October.")


elif page == 'Interactive map with aggregated bike trips': 

    ### Add the map ###
    st.write("Interactive map showing aggregated bike trips over New York")

    path_to_html = "nyc-citibike-mini.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    ## Show in webpage
    st.header("Aggregated citi Bike Trips in New York")
    st.components.v1.html(html_data, height=1000)
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("Busy Zones: Midtown Manhattan, Central Park area, and downtown Manhattan have extremely high trip volumes.")
    st.markdown("Major Corridors: Heavy bike traffic connects Union Square, Times Square, Central Park South, and Brooklyn waterfront areas.")
    st.markdown("Possible Reasons: These are high-density commercial, tourist, and residential areas where bike sharing is heavily used for commuting and recreation. Central Park also attracts a lot of casual users, especially in summer.")
    st.markdown("Interesting Note: Cross-borough trips (e.g., Brooklyn to Manhattan) appear less frequent than intra-borough trips, possibly due to bridge crossing difficulty.")

else:
    st.header("Conclusions and recommendations")

    bikes = Image.open("business_pic.jpg")
    st.image(bikes, caption="Citi Bike Recommendations")

    st.markdown("### Our analysis highlights key factors contributing to bike shortages and uneven usage patterns across Citi Bike stations:")
    st.markdown("""
        1. **Seasonal Variability**: Bike usage peaks during warmer months (May–October) and drops significantly in colder months, driven by temperature variations. This seasonal demand surge likely leads to complaints about bike unavailability.
        2. **High-Demand Stations**: Specific stations in central and lower Manhattan, such as W 21 St & 6 Ave, West St & Chambers St, and Broadway & W 58 St, dominate usage. However, this high concentration of activity creates imbalances in supply and demand.
        3. **Uneven Regional Activity**: Peripheral areas, such as northern Manhattan and some outer boroughs, show lower activity, indicating underutilization of resources.
        4. **Regional Connectivity**: Significant travel links between Manhattan, Jersey City, and Brooklyn emphasize the need for better infrastructure and bike management across these hubs.
        5. **Redistribution Gaps**: Current operational strategies may not sufficiently address the variability in demand, especially during peak seasons and at high-traffic stations.
    """)
