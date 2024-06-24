#pipreqs --force
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

#key = table title
#value = table's file name
tables = {
    'Team Stats And Ranking': 'team_stats_and_ranking',
    'Team Conversions': 'team_conversions',
    'Passing': 'passing',
    'Rushing And Receiving': 'rushing_and_receiving',
    'Kick And Punt Returns': 'kick_and_punt_returns',
    'Kicking': 'kicking',
    'Punting': 'punting',
    'Defense And Fumbles': 'defense_and_fumbles',
    'Scoring Summary': 'scoring_summary',
    'Schedule And Game Results': 'schedule_and_game_results',
    'Touchdown Log': 'touchdown_log',
    'Opponent Touchdown Log': 'opponent_touchdown_log'
}

table_title = list(tables.keys())

table_file = list(tables.values())

#get dataframe
#filter team and year

# get opponent for that select team's week
#get week and opponent
#for select week
def team_schedule (year:int, team:str):

    file = 'Football_Data/schedule_and_game_results'
    
    schedule_and_game_results = pd.read_csv(file, index_col=0)
    
    query = f'''
    select Week, Opponent, Team, Year
    from schedule_and_game_results
    where Team='{team}' and Year={year}
    order by Week
    '''

    df = duckdb.sql(query).df()

    return df

#get opponent table
def query_df(schedule_df, year:int, team:str, table:str, week:int):
    
    opp_filter = schedule_df[schedule_df['Week'] == week]
    
    str_opp_team = opp_filter['Opponent'].iloc[0]

    file = f'Football_Data/{table}'
    table_df = pd.read_csv(file, index_col=0)

    table_query = f'''
    select *
    from table_df
    where (Team='{team}' or Team='{str_opp_team}') and Year={year}
    '''

    df = duckdb.sql(table_query).df()

    return df, str_opp_team


#filter year
def df_year (year: int, table):

    file = f'Football_Data/{table}'
    table_df = pd.read_csv(file, index_col=0)
    
    query = f'''select * from table_df where Year = {year}'''
    
    df = duckdb.sql(query).df()

    return df

#bar chart
def px_bar_charts(df: pd, team, column):
    try:
        fig1 = px.bar(
            df, 
            x=df['Team'], 
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


############ streamlit
#set up multipage link
st.set_page_config(page_title='Team', layout='wide', initial_sidebar_state='expanded')

#Title
st.title('Team Results')

#uer input dropdown boxes for year team and table
year_select = st.sidebar.selectbox('Select Year', options=years)
team_select = st.sidebar.selectbox('Select Team 1', options=team_names)
table_select = st.sidebar.selectbox('Select Table', options= table_title[:-3])

#get select week
sched_df = team_schedule(year_select, team_select)
week_select = st.sidebar.selectbox('Select Week', sched_df['Week'])


#filter dataframe for team and year
#oppoennt dataframe
df, opponent = query_df(sched_df, year_select, team_select, tables[table_select], week_select)


#filter datframe for year
year_df = df_year(year_select, tables[table_select])


##################################################################      Main area

#title
st.title(f'NFL Data {year_select} {team_select} vs. {opponent}')

#show dataframe
st.write(team_select)
st.dataframe(df[df['Team']==team_select], column_config={'index':None, 'Team':None, 'Year':None})
st.write(opponent)
st.dataframe(df[df['Team']==opponent], column_config={'index':None, 'Team':None, 'Year':None})


df_col = list(df.columns)
try:
    df_col.remove('Team')
except:
    pass


#expanders/ drop downs
with st.expander(f'{year_select}: {team_select} vs. {opponent}'):
    #select column
    column_select = st.selectbox('Columns', df_col[2:])

    #Graph title
    st.header(column_select.title())
    
    df = df.sort_values(['Player'])
    #df = df.sort_values([column_select], ascending=False)

    team_filter = df[df['Team'] == team_select]
    opp_team_filter = df[df['Team'] == opponent]

    
    #barchart  
    px_bar_charts(df, team_select, column_select)

    
    c1, c2 = st.columns((5,5))
    with c1:
        px_pie_charts(team_filter, team_select, column_select)

    #opponent bar chart
    with c2:
        px_pie_charts(opp_team_filter, opponent, column_select)    

        



