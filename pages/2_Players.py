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

def position_df (year, position):

    file = f'Weekly Stats/{position}_Player_Weekly_Stats'

    df = pd.read_csv(file, index_col=0)

    query = f'''
        select * 
        from df
        where Year = {year}
    '''

    df = duckdb.sql(query).df()
    
    return df


# position = position_abbrev
def player_df (year, week, position, player):

    file = f'Weekly Stats/{position}_Player_Weekly_Stats'

    df = pd.read_csv(file, index_col=0)

    query = f'''
        select * 
        from df
        where (Week = {week}) 
        and (Year = {year}) 
        and (Player = '{player}')
    '''

    df = duckdb.sql(query).df()
    
    return df


#bar chart
def px_bar_charts(df: pd, column: str):
    try:
        fig1 = px.bar(
            df, 
            x=df[column],
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


################### Players main st area

st.set_page_config(page_title='Players', layout='wide', initial_sidebar_state='expanded')

st.title('Player Results')


year_select = st.sidebar.selectbox('Select Year', options=years)
position_select = st.sidebar.selectbox('Select Position', options=position_choices)
position = positions_dict[position_select]

# position dataframe
# get player list
#get week list
pos_df =  position_df(year_select, position)

#week select list
week_li = range(pos_df['Week'].min(), pos_df['Week'].max()+1)

#user input dropdown boxes for year team and table
week_select = st.sidebar.selectbox('Select Week', options=week_li)

#filter for players playing that week
player_li = list(pos_df[pos_df['Week']==week_select]['Player'].unique())
player_select = st.sidebar.selectbox('Select Player', options=player_li)


######### Data Frames

player = player_df(year_select, week_select, position, player_select)

