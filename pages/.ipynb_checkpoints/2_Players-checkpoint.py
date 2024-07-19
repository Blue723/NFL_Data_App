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

def position_df (year, team, position):

    file = f'Weekly Stats/{position}_Player_Weekly_Stats'

    df = pd.read_csv(file, index_col=0)

    query = f'''
        select * 
        from df
        where (Year = {year}) 
        and (Team = '{team}') 
    '''

    df = duckdb.sql(query).df()
    
    return df
    

# position = position_abbrev
#for bar chart
def get_player (year, week, team, position, player):

    file = f'Weekly Stats/{position}_Player_Weekly_Stats'

    df = pd.read_csv(file, index_col=0)

    query = f'''
        select * 
        from df
        where (Year = {year}) 
        and (Player = '{player}')
        and (Team = '{team}')
        order by Week
    '''

    df = duckdb.sql(query).df()
    
    return df


#bar chart
def px_bar_charts(df: pd, column: str):
    player = df['Player'].iloc[0]
    
    fig1 = px.bar(
        df, 
        x=df['Week'],
        y=df[column], 
        barmode='group',
        color=df['Player'],
        labels=df['Player'].iloc[:],
        title=f'{player}'
    )
    return st.plotly_chart(fig1)


#piechart
def px_pie_charts(df, team, column):
    fig1 = px.pie(data_frame=df, values=df[column], names=df['Player'], title=team)

    return st.plotly_chart(fig1)


################### Players main st area

st.set_page_config(page_title='Players', layout='wide', initial_sidebar_state='expanded')

st.title('Player Results')

#side bar selecitons
year_select = st.sidebar.selectbox('Select Year', options=years)
team_select = st.sidebar.selectbox('Select Team', options=team_names)
position_select = st.sidebar.selectbox('Select Position', options=position_choices)

#selected posisition to import position df
position = positions_dict[position_select]

# position dataframe
# get player list
#get week list
pos_df =  position_df(year_select, team_select, position)

#week select list
week_min = int(pos_df['Week'].min())
week_max = int(pos_df['Week'].max()+1)
week_li = range(week_min, week_max)
#user input dropdown boxes for year team and table
week_select = st.sidebar.selectbox('Select Week', options=week_li)

#filter for players playing that week
player_li = list(pos_df[pos_df['Week']==week_select]['Player'].unique())
player_select = st.sidebar.selectbox('Select Player', options=player_li)

#select column
column_select = st.sidebar.selectbox('Select Column', options=list(pos_df.columns))


#player dataframe
player_df = get_player(year_select, week_select, team_select, position, player_select)

st.write(player_df)

with st.expander(f'{year_select} Week: {week_select} Player: {player_select} Position: {position_select} Stats'):

    c1, c2 = st.columns((5,5))
    with c1:
        px_bar_charts(player_df, column_select)
    with c2:
        #filter pos df for that week
        week_filter_pos_df = pos_df[pos_df['Week']==week_select]
        px_pie_charts(week_filter_pos_df, team_select, column_select)

with st.expander(f'{year_select} {team_select} {position_select}'):

    c1, c2 = st.columns((5,5))
    with c1:
        px_bar_charts(pos_df, column_select)
    with c2:
        px_pie_charts(pos_df, team_select, column_select)