#pipreq in linux to create requirements.txt file
import os
import re

import pandas as pd

import plotly.express as px

import streamlit as st

import pyodbc

import sqlalchemy as sal
from sqlalchemy import create_engine
from sqlalchemy.sql import text

#sql connection
# connection link varaibles
servername = '*****'
dbname = 'NFL_Data'
trusted_conneciton = '?trusted_conneciton=yes'
driver = '&driver=ODBC+Driver+17+for+SQL+Server'

#create engine url to connect to sql server
engine = create_engine(f'mssql+pyodbc://@{servername}/{dbname}{trusted_conneciton}{driver}')

#years
years = range(2010,2024)

team_names=[
     '49ers',
     'Bears',
     'Bengals',
     'Broncos',
     'Browns',
     'Buccaneers',
     'Buffalos',
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

select_table_name_li = [
    'team_stats_and_ranking',
    'schedule_and_game_results',
    'team_conversions',
    'passing',
    'rushing_and_receiving',
    'kick_and_punt_returns',
    'kicking',
    'punting',
    'defense_and_fumbles',
    'scoring_summary',
    'touchdown_log',
    'opponent_touchdown_log'
]


# table name list with team and year to format
table_name_li = [
    'team_stats_and_ranking*',
    'schedule_and_game_results*',
    'team_conversions*',
    'passing*',
    'rushing_and_receiving*',
    'kick_and_punt_returns*',
    'kicking*',
    'punting*',
    'defense_and_fumbles*',
    'scoring_summary*',
    'touchdown_log*',
    'opponent_touchdown_log*'
]


#sidebar

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

#titles
st.sidebar.write('Select the table you would lke to view')

#sidebar selections
# select years
select_year = st.sidebar.selectbox('Years', years)

#select table
select_table = st.sidebar.selectbox('Tables', select_table_name_li)

#select team
select_team = st.sidebar.selectbox('Teams', team_names)

def query_team_year(select_table: str, year: int, team: str, con: str):

    query = f'select * from {select_table} where Year = {year} and Team = \'{select_team}\';'

    df = pd.read_sql(query, con, index_col='index')

    return df
    
#Main area

#title
st.title('NFL Data {} {}'.format(select_team, select_year))

#select dataframe
select_df = query_team_year(select_table, select_year, select_team, engine)


#show dataframe
st.write(select_df)

#select column
select_column = st.sidebar.selectbox('Columns', select_df.columns[1:])

#Graph title
st.header(select_column)

#graphs

c1, c2 = st.columns((5,5))

#barchart
with c1:
    fig1 = px.bar(select_df, x=select_df[select_column], y=select_df[select_column].index)

    st.plotly_chart(fig1)

#pie chart
with c2: 
    fig2 = px.pie(data_frame=select_df, values=select_df[select_column], names=select_df[select_column].index)

    st.plotly_chart(fig2)

    
    
    
c3, c4 = st.columns((5,5))

if select_table == 'schedule_and_game_results' or select_table == 'touchdown_log' or select_table == 'opponent_touchdown_log':
    #line plot
    with c3:
        fig3 = px.line(select_df, x=select_df['Date'], y=select_df[select_column].values)

        st.plotly_chart(fig3)
        
        
        
        
        
        
        