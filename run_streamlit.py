import os
import re

import pandas as pd

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

file_path = selected_file_path(select_year= select_year, select_table=select_table)


#cache data
@st.cache_data(persist=True)

#select table
def select_table(file_path: str, select_team: str):

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
select_df = select_table(file_path, select_team)

#show dataframe
st.write(select_df)

#select column
select_column = st.sidebar.selectbox('Columns', select_df.columns[1:])

#Graph title
st.header(select_column)

#barchart
st.bar_chart(select_df[select_column])


























