# def medal_tally(df):
#     # we have data in such a manner that altough india won only 9-10 gold medals but it will show that india won total of 131 gold medal.
#     # it is due to this data is arranged according to players not by countery so if india wins a gold in hockey that means all 15 palyers of indian hockey team have won gold medals and that would inflate the medall count
#     # this happened with other country also due to team events
#     # so we will dro the duplicated rows on the basis of [team,noc,games,year,season,city,sport,event,medal]
#     medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Season', 'City', 'Event', 'Medal'])
#
#     # now we will grop by on the basis of medal counts
#     medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
#
#     medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
#
#     medal_tally['Gold']=medal_tally['Gold'].astype(int)
#     medal_tally['Silver'] = medal_tally['Silver'].astype(int)
#     medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
#     medal_tally['total'] = medal_tally['total'].astype(int)
#
#
#     return medal_tally
#
#
# def country_year_list(df):
#     # now we will extract all the years when olympic played
#     years = df['Year'].unique().tolist()
#     years.sort()
#     years.insert(0, 'Overall')
#
#     # now we will extract countries
#     country = df['region'].dropna().unique().tolist()
#     country.sort()
#     country.insert(0, 'Overall')
#
#     return country,years
#
#
# def get_sports(df):
#     sports=df['Sport'].unique().tolist()
#     sports.sort()
#     return sports
#
#
#
# def fetch_medal_tally(df, year, country):
#
#     if year != 'Overall' and country == 'Overall':
#         x = df[df['Year'] == year]  ############## year ko bracket me daal ke dekh
#         x = x.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
#         x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
#         return x
#
#     if year == 'Overall' and country != 'Overall':
#         y = df[df['region'] == country]
#         y = y.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
#         y['total'] = y['Gold'] + y['Silver'] + y['Bronze']
#         return y
#
#     if year != 'Overall' and country != 'Overall':
#         z = df[(df['region'] == country) & (df['Year'] == year)]
#         z1 = z[['Name','Sport','Event', 'Gold', 'Silver', 'Bronze','Sex']].sort_values('Sport')
#         z = z.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Season', 'City', 'Event', 'Medal'])
#         z = z.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
#         z['Total']=z['Gold']+z['Silver']+z['Bronze']
#         return z, z1
#
#
# def participating_nations_over_time(df):
#     nations_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('Year').reset_index()
#     nations_over_time=nations_over_time[['index','Year']]
#     nations_over_time.rename(columns={'index': 'Edition', 'Year': 'No of Countries'}, inplace=True)
#     nations_over_time=nations_over_time.sort_values('Edition')
#
#     return nations_over_time
#
# def no_of_events_over_time(df):
#     no_of_events = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values('Year').reset_index()
#     no_of_events = no_of_events[['index', 'Year']]
#     no_of_events.rename(columns={'Year': 'No of Events', 'index': 'Edition'}, inplace=True)
#
#     return no_of_events
#
# def no_of_athletes_over_time(df):
#     athlete_over_time = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values('Year').reset_index()
#     athlete_over_time=athlete_over_time[['index','Year']]
#     athlete_over_time.rename(columns={'index':'Edition','Year':'No of Athletes'},inplace=True)
#     athlete_over_time=athlete_over_time.sort_values('Edition')
#
#     return athlete_over_time
#
# def heatmap(df):
#     x = df.drop_duplicates(['Year', 'Sport', 'Event'])
#     x = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0)
#     x = x.astype(int)
#     return x
#
#
# def unique_sports(df):
#     return df['Sport'].unique().tolist()
#
#
#
#
# def top_performers(selected_sport, df,region_df):
#     dp = df[df['Sport'] == selected_sport]
#     is_all_zero = (dp[['Gold', 'Silver', 'Bronze']] == 0).all(axis=1)
#     dp_cleaned = dp[~is_all_zero]
#     dp_cleaned = dp_cleaned.groupby('Name')[['Gold', 'Silver', 'Bronze']].sum()
#     dp_cleaned['total'] = dp_cleaned['Gold'] + dp_cleaned['Silver'] + dp_cleaned['Bronze']
#     dp_cleaned=dp_cleaned.sort_values('Gold', ascending=False)
#     new_df = df[['Name', 'region']]
#     dp_cleaned=dp_cleaned.merge(new_df, on='Name', how='left').drop_duplicates('Name').head(25).reset_index()
#     dp_cleaned = dp_cleaned[['Name', 'Gold', 'Silver', 'Bronze', 'total', 'region']]
#     return dp_cleaned
#
#
# def country_performance(df,country):
#     performance = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Season', 'City', 'Event', 'Medal'])
#     performance = performance[performance['region'] == country]
#     performance = performance.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum()
#     performance['Total'] = performance['Gold'] + performance['Silver'] + performance['Bronze']
#     performance=performance.reset_index()
#     return performance
#
#
# def heatmap2(country,df):
#     temp_df = df.dropna(subset=['Medal'])
#     temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
#     temp_df = temp_df[temp_df['region'] == country]
#     temp_df = temp_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
#     temp_df = temp_df.astype(int)
#     return temp_df
#
#
# def country_top_athletes(country, df):
#     # Ensure the 'Name' column is of type string
#     df['Name'] = df['Name'].astype(str)
#     df['region'] = df['region'].astype(str)
#
#     temp = df[['Name', 'Sport']]
#     df = df[df['region'] == country]
#     df = df.dropna(subset=['Medal'])
#     df = df['Name'].value_counts().reset_index()
#
#     df.columns = ['Name', 'count']  # Rename the columns for the merge
#     df = df.merge(temp, on='Name').drop_duplicates('Name').reset_index(drop=True)
#     df = df.head(25)
#
#     df = df[['Name', 'count', 'Sport']]
#     df = df.rename(columns={'count': 'Medals'})
#
#     return df
#
# def weight_v_height(df,sport):
#     athlete_df=df.drop_duplicates(subset=['Name','region'])
#     athlete_df['Medal'].fillna('No Medal',inplace=True)
#     temp_df=athlete_df[athlete_df['Sport']==sport]
#     return temp_df
#
#
# def men_vs_women(df):
#     men = df[df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
#     women = df[df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
#     final = men.merge(women, on='Year', how='left')
#     final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
#     final.fillna(0, inplace=True)
#     return final
















import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def medal_tally(df: pd.DataFrame) -> pd.DataFrame:
    # Calculate the medal tally
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Gold', ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally

def fetch_medal_tally(df: pd.DataFrame, year: str, country: str):
    # Fetch medal tally for a specific year and country
    if year == 'Overall' and country == 'Overall':
        temp_df = df
    elif year == 'Overall' and country != 'Overall':
        temp_df = df[df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = df[df['Year'] == year]
    else:
        temp_df = df[(df['Year'] == year) & (df['region'] == country)]
    x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    y = temp_df.groupby('Name').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    return x, y

def country_year_list(df: pd.DataFrame):
    # Get the list of countries and years
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return country, years

def participating_nations_over_time(df: pd.DataFrame) -> pd.DataFrame:
    # Calculate the number of participating nations over time
    nations_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_time.columns = ['Edition', 'No of Countries']
    return nations_over_time

def no_of_events_over_time(df: pd.DataFrame) -> pd.DataFrame:
    # Calculate the number of events over time
    events_over_time = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values('index')
    events_over_time.columns = ['Edition', 'No of Events']
    return events_over_time

def no_of_athletes_over_time(df: pd.DataFrame) -> pd.DataFrame:
    # Calculate the number of athletes over time
    athletes_over_time = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values('index')
    athletes_over_time.columns = ['Edition', 'No of Athletes']
    return athletes_over_time

def heatmap(df: pd.DataFrame) -> pd.DataFrame:
    # Create a heatmap of the number of events over time for each sport
    pt = df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
    return pt

def unique_sports(df: pd.DataFrame) -> list:
    # Get a list of unique sports
    all_unique_sports = np.unique(df['Sport'].dropna().values).tolist()
    all_unique_sports.insert(0, 'Overall')
    return all_unique_sports

def top_performers(selected_sport: str, df: pd.DataFrame, region_df: pd.DataFrame) -> pd.DataFrame:
    # Calculate the top performers in a selected sport
    temp_df = df.dropna(subset=['Medal'])
    if selected_sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == selected_sport]

    top_athletes = temp_df.groupby('Name').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    top_athletes = top_athletes.merge(region_df, on='NOC', how='left')
    return top_athletes.head(10)

def country_performance(df: pd.DataFrame, selected_country: str) -> pd.DataFrame:
    # Calculate the performance of a country over time
    temp_df = df[df['region'] == selected_country]
    country_performance = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze', 'Total']].sort_values('Year').reset_index()
    return country_performance

def heatmap2(selected_country: str, df: pd.DataFrame) -> pd.DataFrame:
    # Create a heatmap for the sports a country is good at
    temp_df = df[df['region'] == selected_country]
    pivot_table = temp_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(int)
    return pivot_table

def country_top_athletes(selected_country: str, df: pd.DataFrame) -> pd.DataFrame:
    # Calculate the top 20 athletes from a selected country
    temp_df = df[df['region'] == selected_country]
    top_athletes = temp_df.groupby('Name').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    return top_athletes.head(20)

def get_sports(df: pd.DataFrame) -> list:
    # Get a list of sports
    sports = df['Sport'].unique().tolist()
    sports.sort()
    sports.insert(0, 'Overall')
    return sports

def weight_v_height(df: pd.DataFrame, sport: str) -> pd.DataFrame:
    # Generate data for the height vs weight scatter plot
    temp_df = df.dropna(subset=['Weight', 'Height'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    return temp_df

def men_women(df: pd.DataFrame) -> pd.DataFrame:
    # Calculate the participation of men and women over time
    men_women_over_time = df.groupby(['Year', 'Sex']).size().unstack().fillna(0)
    men_women_over_time = men_women_over_time.reset_index()
    return px.line(men_women_over_time, x='Year', y=['M', 'F'])
