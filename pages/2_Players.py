#pipreqs --force

### 7/10/2024 when internet back on rerun weekly player webscrape inorder to include week column
########################
################################   ^^^^^^^  READ ^^^^^^^
############################################################################################

import pandas as pd

import plotly.express as px

import duckdb

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

positions_dict = {
    'QB': 'Quarter Back',
    'RB': 'Running Back',
    'WR': 'Wide Receiver',
    'TE': 'Tight End',
    'K': 'Kicker',
    'DST': 'Defense and Special Teams',
    'DL': 'Defensive Lineman',
    'LB': 'Line Backer',
    'DB': 'Defensive Back'
}

position_choices = list(positions_dict.values())
position_abbrev = list(positions_dict.keys())

# position = position_abbrev
def player_df (year, week, position, player):

    file = f'Player Weekly Stats/{position}_Player_Weekly_Stats'

    df = pd.read_csv(file, index_col=0)

    query = f'''
        select * 
        from {position}_Player_Weekly_Stats
        where (Week = {week}) 
        and (Year = {year}) 
        and (Player = {player})
    '''

    df = duckdb.sql(query).df()
    
    return df


#bar chart
def px_bar_charts(df: pd):
    try:
        fig1 = px.bar(
            df, 
            x= 
            y=df[column], 
            barmode='group',
            color=df['Player'],
            labels=df['Player'].iloc[:],
            title=f'{team}'
        )
    
    except:
        fig1 = px.bar(
            df, 
            x=df[column].index, 
            y=df[column],
            barmode='group',
            color=df[column].index,
            labels=df['Player'].iloc[:],
            title=team
        )

    return st.plotly_chart(fig1)


#piechart
def px_pie_charts(df, team, column):
    fig1 = px.pie(data_frame=df, values=df[column], names=df['Player'], title=team)

    return st.plotly_chart(fig1)



######### Data Frames





################### Players main st area
st.set_page_config(page_title='Players', layout='wide', initial_sidebar_state='expanded')



st.title('Player Results')

#uer input dropdown boxes for year team and table
year_select = st.sidebar.selectbox('Select Year', options=years)
team_select = st.sidebar.selectbox('Select Team', options=team_names)
table_select = st.sidebar.selectbox('Select Position', options=position_choices)

#get select week
sched_df = team_schedule(year_select, team_select)
week_select = st.sidebar.selectbox('Select Week', sched_df['Week'])