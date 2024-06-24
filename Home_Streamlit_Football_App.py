# This is the main streamlit app with mulitpage 
# and connect to sql
# other pages located in the 'pages' folder

#pipreqs --force in linux to create requirements.txt file

import pandas as pd

import plotly.express as px

import duckdb

import streamlit as st

#years
years = range(2010,2025)

team_names=[
     '49ers',
     'Bears',
     'Bengals',
     'Broncos',
     'Browns',
     'Buccaneers',
     'Bills',
     'Cardinals',
     'Chargers',
     'Chiefs',
     'Colts',
     'Commanders',
     'Cowboys',
     'Dolphins',
     'Eagles',
     'Falcons',
     'Giants',
     'Jaguars',
     'Jets',
     'Lions',
     'Packers',
     'Panthers',
     'Patriots',
     'Raiders',
     'Rams',
     'Ravens',
     'Saints',
     'Seahawks',
     'Steelers',
     'Texans',
     'Titans',
     'Vikings'
]


#@cache_resource
def schedule_sql (team:str):

    file = 'NFL_Data_2024/All_Team_Schedule_2024'

    schedule_2024 = pd.read_csv(file, index_col=0)
    
    query = f'''select * from schedule_2024 where Team = '{team}' '''

    df = duckdb.sql(query).df()

    return df

#set page link
st.set_page_config(page_title='Home', layout='wide', initial_sidebar_state='expanded')

st.title('Welcome to the Football Data App')

#sidebar
team = st.sidebar.selectbox('Select a Team',team_names)


#dataframe
df = schedule_sql(team)

#header
st.header(team + ' Schedule')

#dataframe
#st.dataframe(df, height=800)
st.dataframe(
    df, 
    column_config={
        'Year': st.column_config.DateColumn(format='2024')})
