#pipreqs --force in linux to create requirements.txt file

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

#key = table title
#value = table's file name
tables = {'Team Stats And Ranking': 'team_stats_and_ranking',
          'Schedule And Game Results': 'schedule_and_game_results',
          'Team Conversions': 'team_conversions',
          'Passing': 'passing',
          'Rushing And Receiving': 'rushing_and_receiving',
          'Kick And Punt Returns': 'kick_and_punt_returns',
          'Kicking': 'kicking',
          'Punting': 'punting',
          'Defense And Fumbles': 'defense_and_fumbles',
           'Scoring Summary': 'scoring_summary',
          'Touchdown Log': 'touchdown_log',
          'Opponent Touchdown Log': 'opponent_touchdown_log'
         }

table_title = list(tables.keys())

table_file = list(tables.values())


#sidebar

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

#titles
st.sidebar.write('Select the table you would lke to view')

#sidebar selections
# select years
select_year = st.sidebar.selectbox('Years', years)

#select table
select_table = st.sidebar.selectbox('Tables', table_title)

#select team
select_team = st.sidebar.selectbox('Teams', team_names)




####select dataframe

#get table
def read_table_csv(select_table: str):

    df = pd.read_csv(f'Table Data/{tables[select_table]}', index_col=1).drop(columns=['Unnamed: 0'])

    return df

#full dataframe no filter from csv file
read_csv_df = read_table_csv(select_table)


#filter team and year
def df_team_year (df: None, select_team: str, select_year: int):

    new_df = df[(df['Team'] == select_team) & (df['Year'] == select_year)]

    return new_df

#filter dataframe for team and year
team_year_df = df_team_year(read_csv_df, select_team, select_year)


#filter year

def df_year (df: None, select_year: int):

    new_df = df[df['Year'] == select_year]

    return new_df

#filter datframe for year
year_df = df_year(read_csv_df, select_year)


##################################################################Main area

#title
st.title('NFL Data {} {}'.format(select_team, select_year))

#show dataframe
st.write(team_year_df)

df_col = list(read_csv_df.columns)
try:
    df_col.remove('Team')
except:
    pass
#select column
select_column = st.sidebar.selectbox('Columns', df_col)

#Graph title
st.header(select_column)



with st.expander(f'{select_team} {select_year}'):
    
    #graphs
    team_year_df = team_year_df.sort_values([select_column], ascending=False)
    team_year_df = team_year_df.sort_values(['Team'])

    
    c1, c2 = st.columns((4,6))
    
    #barchart
    with c1:
        try:
            fig1 = px.bar(
                team_year_df, 
                x=team_year_df['Player'], 
                y=team_year_df[select_column], 
                color=team_year_df['Player'])
        
            st.plotly_chart(fig1)
        
        except:
            fig1 = px.bar(
                team_year_df, 
                x=team_year_df[select_column].index, 
                y=team_year_df[select_column], 
                color=team_year_df[select_column].index)
    
            st.plotly_chart(fig1)
    
    #pie chart
    with c2: 
        fig2 = px.pie(data_frame=team_year_df, values=team_year_df[select_column], 
                      names=team_year_df[select_column].index)
    
        st.plotly_chart(fig2)


with st.expander(f'Compare All Teams in {select_year}'):
    
    year_df = year_df.sort_values([select_column], ascending=False)
    year_df = year_df.sort_values(['Team'])

    sort_year_df = year_df.sort_values(select_column, ascending=False)


    
    c3, c4 = st.columns((5,5))

    with c3:
        if select_table == 'Touchdown Log' or select_table == 'Opponent Touchdown Log':
            df_grpby = year_df.groupby(by='Team', as_index=False)[['Team', select_column]].value_counts()

            fig3 = px.line(
                df_grpby,
                x='Date',
                y='count',
                barmode='relative',
                color=select_column
            )
            
            st.plotly_chart(fig3)
        
        else:
            try:
                fig3 = px.bar(
                    year_df,
                    x='Team', 
                    y=select_column,
                    barmode='relative',
                    color=year_df[select_column].index,
                    hover_name='Player',
                )
                
                st.plotly_chart(fig3)

            except:
                fig3 = px.bar(
                    year_df,
                    x='Team', 
                    y=select_column,
                    barmode='relative',
                    color=year_df[select_column].index,
                    hover_name=year_df['Team']
                )
            
                st.plotly_chart(fig3)
    

    with c4:
        fig4 = px.pie(data_frame=year_df, values=year_df[select_column], 
                      names=year_df[select_column].index)
    
        st.plotly_chart(fig4)


        