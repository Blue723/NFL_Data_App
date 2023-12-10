import os
import re

import pandas as pd

import plotly.express as px
import streamlit as st

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


#selected file path by year and table
def selected_file_path(select_year: int, select_table: str):
    
    select_file_str = select_table+'_team'+'_'+'{}'.format(select_year)
    
    file_path = "NFL_Data_{}/".format(select_year)+select_file_str

    return file_path

#the file path to select the table from local files
file_path = selected_file_path(select_year=select_year, select_table=select_table)


#cache data
@st.cache_data(persist=True)

#select table
def select_table_df(file_path: str, select_team: str):
    #uses assigned index col if df does not have 'Player' column
    try:
        select_file = pd.read_csv(file_path, index_col='Player')
    except:
        select_file = pd.read_csv(file_path, index_col=1)

    select_file = select_file.drop(columns=['Unnamed: 0'], axis=1)
    
    df = select_file[select_file['Team']==select_team]

    return df


#Main area

#title
st.title('NFL Data {} {}'.format(select_team, select_year))

#selected dataframe
select_df = select_table_df(file_path, select_team)

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