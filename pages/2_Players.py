#pipreqs --force for rereiremetns.txt

import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import duckdb

import streamlit as st



#years
years = range(2010,2024)

#team names
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

#positions
positions_dict = {
    'Quarter Back': 'QB',
    'Running Back': 'RB',
    'Wide Receiver': 'WR',
    'Tight End': 'TE',
    'Kicker': 'K',
    'Defense and Special Teams': 'DST',
    'Defensive Lineman': 'DL',
    'Line Backer': 'LB',
    'Defensive Back': 'DB'
}


position_abbrev = list(positions_dict.values())
position_choices = list(positions_dict.keys())

##### get position data and graphs

# position = position_abbrev

def position_df (year, team, position):

    file = f'Weekly Stats/{position}_Player_Weekly_Stats'

    df = pd.read_csv(file, index_col=0)

    sched_game_results_df = pd.read_csv('Football_Data/schedule_and_game_results', index_col=0)
    
    query = f'''
        select df.*, sched_game_results_df."Points Scored" as "Team Points Scored", sched_game_results_df."Win/Loss"
        from df
        join sched_game_results_df 
        on (df.Year = sched_game_results_df.Year)
        and (df.Week = sched_game_results_df.Week)
        and (df.Team = sched_game_results_df.Team)
        where df.Year = {year}
    '''

    df = duckdb.sql(query).df()
    
    return df


#use position dataframe
def get_team (position_df, team: str):

    query = f'''
        select * 
        from position_df
        where Team = '{team}'
        order by Week
    '''

    df = duckdb.sql(query).df()
    
    return df

#use get team df
def get_player (team_df, player: str):

    query = f'''
            select *
            from team_df
            where Player = '{player}'
            order by Week
    '''

    df = duckdb.sql(query).df()
    
    return df


##### get rolling average of data and graph
#get rolling average of selected column
# this is to compare players performance that week to overall average
def col_rolling_average (year, team, position, player, column):
    
    file = f'Weekly Stats/{position}_Player_Weekly_Stats'

    df = pd.read_csv(file, index_col=0)

    query = f'''   
        select 
            Player, Team, Year, Week, Date, "{column}", 
            ROUND(AVG("{column}") 
                OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 2)
                as "{column} Moving Average",
            ("{column}" - "{column} Moving Average") "{column} - Moving Average Difference"

        from df
        where (Year = {year}) 
        and (Player = '{player}')
        and (Team = '{team}') 
        ORDER BY Year, Week
    '''

    df = duckdb.sql(query).df()

    return df



################ GRAPHS

############ Team graphs
#bar chart
# use get_player df
def px_bar_charts(df: pd, column: str, team: str):
    
    fig = px.bar(
        df, 
        x=df['Week'],
        y=df[column], 
        barmode='group',
        color=df['Player'],
        labels=df['Player'].iloc[:],
        title=f'{team}'
    )

    return st.plotly_chart(fig)

# piechart
def px_pie_charts(df, column, team):
    fig = px.pie(data_frame=df, values=df[column], names=df['Player'], title=team)

    return st.plotly_chart(fig)



##### Player graphs
#bar chart
# use get_player df
def player_px_bar_charts(df: pd, column: str, player: str):
    
    fig = px.bar(
        df, 
        x=df['Week'],
        y=df[column], 
        barmode='group',
        color=df['Player'],
        labels=df['Player'].iloc[:],
        title=f'{player}'
    )

    return st.plotly_chart(fig)

# piechart
def player_px_pie_charts(df, column, team):
    fig = px.pie(data_frame=df, values=df[column], names=df['Week'], title=team)

    return st.plotly_chart(fig)


#rolling average line plot
def roll_avg_px_plot (df, team, column):
    
    fig = go.Figure()
    
    fig.add_trace(go.Line(x=df['Date'], y=df.iloc[:,5], name=column))
    fig.add_trace(go.Line(x=df['Date'], y=df.iloc[:,6], name=f"{column} Moving Average"))
    fig.add_trace(go.Line(x=df['Date'], y=df.iloc[:,7], name=f'{column} - Moving Average Difference'))
    
    return st.plotly_chart(fig)





################### Players main st area

st.set_page_config(page_title='Players', layout='wide', initial_sidebar_state='expanded')

st.title('Player Results')


#side bar selecitons

#select year
year_select = st.sidebar.selectbox('Select Year', options=years)

#select team
team_select = st.sidebar.selectbox('Select Team', options=team_names)


#selected posisition to import position df
position_select = st.sidebar.selectbox('Select Position', options=position_choices)
position = positions_dict[position_select]

# position dataframe
# get player list
#get week list
pos_df = position_df(year_select, team_select, position)


#team position dataframe
team_df = get_team(pos_df, team_select)


#week select list
week_min = 0
week_max = int(pos_df['Week'].max()+1)
week_li = range(week_min, week_max)

#user input dropdown boxes for year team and table
week_select = st.sidebar.selectbox('Select Week', options=week_li)


#filter Position dataframe to specific week
if week_select > 0:
    week_pos_df = pos_df[pos_df['Week']==week_select]
else:
    week_pos_df = pos_df

#filter team dataframe to specific week
if week_select > 0:
    week_team_df = team_df[team_df['Week']==week_select]
else:
    week_team_df = team_df


#filter for players playing that week
if week_select > 0:
    player_li = list(team_df[team_df['Week']==week_select]['Player'].unique())
else:
    player_li = list(team_df['Player'].unique())

#select player
player_select = st.sidebar.selectbox('Select Player', options=player_li)

#player dataframe
player_df = get_player(team_df, player_select)


#select column
column_select = st.sidebar.selectbox('Select Column', options=list(pos_df.columns))



##### players streamlit main area#########
st.title(f'{player_select}')

st.write(player_df)

with st.expander(f'Player: {player_select} Position: {position_select} Stats'):

    c1, c2 = st.columns((5,5))

    with c1:
        player_px_bar_charts(player_df, column_select, player_select)
    with c2:
        player_px_pie_charts(player_df, column_select, team_select)


with st.expander(f'Player: {player_select} Position: {position_select} {column_select} Rolling Average'):
    rolling_avg_df = col_rolling_average(year_select, team_select, position, player_select, column_select)
    
    st.write(rolling_avg_df)

    roll_avg_px_plot (rolling_avg_df, team_select, column_select)


with st.expander(f'Team: {team_select} Position: {position_select} Stats'):

    c1, c2 = st.columns((5,5))

    with c1:
        px_bar_charts(week_team_df, column_select, team_select)
    with c2:
        px_pie_charts(week_team_df, column_select, team_select)


with st.expander(f'Position: {position_select} Stats'):

    c1, c2 = st.columns((5,5))

    with c1:
        px_bar_charts(week_pos_df, column_select, team_select)
    with c2:
        px_pie_charts(week_pos_df, column_select, team_select)