import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ss

df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')
df=preprocessor.preprocess(df,region_df)
df1=df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Season', 'City', 'Event', 'Medal'])


st.sidebar.title("Olympic Analysis")
st.sidebar.image('oic.jpeg')

user_menu=st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis')
)


if user_menu=='Medal Tally':
    st.sidebar.header("Medal Tally")
    country,years=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select year",years)
    selected_country = st.sidebar.selectbox("Select country", country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        medal_tally=helper.medal_tally(df)
        st.title("Country's Performances Over Years")
        st.table(medal_tally)

    elif selected_year != 'Overall' and selected_country != 'Overall':
        x,y=helper.fetch_medal_tally(df,selected_year,selected_country)
        col1, col2 = st.columns(2)
        with col1:
            st.title("Total Number of Medals:-")
            st.table(x)
        with col2:
            st.title("Player Performances:-")
            st.table(y)

    else:
        z=helper.fetch_medal_tally(df1, selected_year, selected_country)
        st.title("Performance:-")
        st.table(z)


if user_menu=='Overall Analysis':
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]


    st.title("Top Statistics")
    col1,col2,col3=st.columns(3)

    with col1:
        st.title("Editions")
        st.title(editions)
    with col2:
        st.title("Hosts")
        st.title(cities)
    with col3:
        st.title("Sports")
        st.title(sports)

    with col1:
        st.title("Events")
        st.title(events)
    with col2:
        st.title("Nations")
        st.title(nations)
    with col3:
        st.title("Athletes")
        st.title(athletes)

    st.title("Participating Nations Over the Years")
    nations_over_time=helper.participating_nations_over_time(df)
    fig = px.line(nations_over_time, x="Edition", y="No of Countries",color_discrete_sequence=["yellow"])
    st.plotly_chart(fig)

    st.title("No of events over the years")
    no_of_events=helper.no_of_events_over_time(df)
    no_of_events=no_of_events.sort_values('Edition')
    fig2 = px.line(no_of_events, x="Edition", y="No of Events",color_discrete_sequence=["orange"])
    st.plotly_chart(fig2)

    st.title("Athlete Participation Over The Years")
    athlete_over_time=helper.no_of_athletes_over_time(df)
    fig3 = px.line(athlete_over_time, x="Edition", y="No of Athletes", color_discrete_sequence=["green"])
    st.plotly_chart(fig3)


    st.title("No. of Events over time(Every Sport)")
    fig4,ax=plt.subplots(figsize=(20,20))
    ax = sns.heatmap(helper.heatmap(df),annot=True)
    st.pyplot(fig4)

    df['Gold'] = pd.to_numeric(df['Gold'], errors='coerce')
    df['Silver'] = pd.to_numeric(df['Silver'], errors='coerce')
    df['Bronze'] = pd.to_numeric(df['Bronze'], errors='coerce')


    st.title("Most Successful Athletes")
    all_unique_sports=helper.unique_sports(df)
    selected_sport=st.selectbox("Select a Sport",all_unique_sports)
    successful_athletes=helper.top_performers(selected_sport,df,region_df)
    st.table(successful_athletes)



if user_menu=='Country-wise Analysis':
    st.sidebar.header("Select Country")
    country,years=helper.country_year_list(df)
    if country[0] == 'Overall':
        country.pop(0)
    selected_country = st.sidebar.selectbox("Select Country", country)
    country_performance=helper.country_performance(df1,selected_country)

    st.title("No of Gold Medals:-")
    fig5=px.line(country_performance,x="Year",y="Gold",color_discrete_sequence=["yellow"])
    st.plotly_chart(fig5)

    st.title("No of Silver Medals:-")
    fig5 = px.line(country_performance, x="Year", y="Silver",color_discrete_sequence=["orange"])
    st.plotly_chart(fig5)

    st.title("No of Bronze Medals")
    fig5 = px.line(country_performance, x="Year", y="Bronze",color_discrete_sequence=["green"])
    st.plotly_chart(fig5)

    st.title("Total Medals:-")
    fig5 = px.line(country_performance, x="Year", y="Total",color_discrete_sequence=["pink"])
    st.plotly_chart(fig5)

    st.title("Sports Counntries Good At")
    pivot_table=helper.heatmap2(selected_country,df)
    if pivot_table.empty or pivot_table.isnull().all().all():
        st.write("Country haven't won any medal till date.")
    else:
        fig6, ax = plt.subplots(figsize=(25, 25))
        ax = sns.heatmap(pivot_table, annot=True)
        st.pyplot(fig6)


    st.title("Top 20 Athletes")
    top_25_players=helper.country_top_athletes(selected_country,df)
    if top_25_players.empty:
        st.write("No athlete have won a medal till date.")
    else:
        st.table(top_25_players)



if user_menu=='Athlete-wise Analysis':


    st.title("Age-wise Medal Distribution")
    age_wise_medal = df.dropna(subset=['Medal'])
    age_wise_medal = age_wise_medal.drop_duplicates(subset=['Name', 'Year', 'region'])
    age_wise_medal = age_wise_medal.dropna(subset=['Age'])
    x1 = age_wise_medal[age_wise_medal['Medal'] == 'Gold']['Age']
    x2 = age_wise_medal[age_wise_medal['Medal'] == 'Silver']['Age']
    x3 = age_wise_medal[age_wise_medal['Medal'] == 'Bronze']['Age']
    x4 = age_wise_medal['Age']
    fig7 = ss.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig7.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig7)


    st.title("Age-wise Gold Medal Distribution in each Sport")
    sports=helper.get_sports(df)
    selected_sport=st.selectbox("select the sport",sports)

    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['Sport'] == selected_sport]
    age_counts = temp_df['Age'].value_counts().sort_index()
    age_probabilities = age_counts / age_counts.sum()
    prob_df = age_probabilities.reset_index()
    prob_df.columns = ['Age', 'Probability']
    fig8 = px.line(prob_df, x='Age', y='Probability', title='Probability vs Age',color_discrete_sequence=["yellow"])
    st.plotly_chart(fig8)


    st.title("Height Vs Weight")
    Sports = df['Sport'].unique().tolist()
    Sports.sort()
    sport=st.selectbox("select a sport",Sports)
    temp_df=helper.weight_v_height(df,sport)
    fig9,ax=plt.subplots()
    ax=sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=100)
    st.pyplot(fig9)


    st.title("Man and Women Participation over the years")
    final=helper.men_vs_women(df)
    fig10=px.line(final,x="Year",y=["Male","Female"])
    fig10.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig10)



# import streamlit as st
# import pandas as pd
# import preprocessor
# import helper
# import plotly.express as px
# import matplotlib.pyplot as plt
# import seaborn as sns
# import plotly.figure_factory as ss
#
# # Load the datasets
# df = pd.read_csv('athlete_events.csv')
# region_df = pd.read_csv('noc_regions.csv')
#
# # Preprocess the data
# df = preprocessor.preprocess(df, region_df)
# df1 = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Season', 'City', 'Event', 'Medal'])
#
# # Sidebar setup
# st.sidebar.title("Olympic Analysis")
# st.sidebar.image('oic.jpeg')
#
# # User menu in the sidebar
# user_menu = st.sidebar.radio(
#     'Select an Option',
#     ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
# )
#
# # Medal Tally section
# if user_menu == 'Medal Tally':
#     st.sidebar.header("Medal Tally")
#     country, years = helper.country_year_list(df)
#     selected_year = st.sidebar.selectbox("Select year", years)
#     selected_country = st.sidebar.selectbox("Select country", country)
#
#     # Display medal tally based on user selection
#     if selected_year == 'Overall' and selected_country == 'Overall':
#         medal_tally = helper.medal_tally(df)
#         st.title("Country's Performances Over Years")
#         st.table(medal_tally)
#
#     elif selected_year != 'Overall' and selected_country != 'Overall':
#         x, y = helper.fetch_medal_tally(df, selected_year, selected_country)
#         col1, col2 = st.columns(2)
#         with col1:
#             st.title("Total Number of Medals:-")
#             st.table(x)
#         with col2:
#             st.title("Player Performances:-")
#             st.table(y)
#
#     else:
#         z = helper.fetch_medal_tally(df1, selected_year, selected_country)
#         st.title("Performance:-")
#         st.table(z)
#
# # Overall Analysis section
# if user_menu == 'Overall Analysis':
#     # Display top statistics
#     editions = df['Year'].unique().shape[0] - 1
#     cities = df['City'].unique().shape[0]
#     sports = df['Sport'].unique().shape[0]
#     events = df['Event'].unique().shape[0]
#     athletes = df['Name'].unique().shape[0]
#     nations = df['region'].unique().shape[0]
#
#     st.title("Top Statistics")
#     col1, col2, col3 = st.columns(3)
#
#     with col1:
#         st.title("Editions")
#         st.title(editions)
#     with col2:
#         st.title("Hosts")
#         st.title(cities)
#     with col3:
#         st.title("Sports")
#         st.title(sports)
#
#     with col1:
#         st.title("Events")
#         st.title(events)
#     with col2:
#         st.title("Nations")
#         st.title(nations)
#     with col3:
#         st.title("Athletes")
#         st.title(athletes)
#
#     # Visualization of participating nations over the years
#     st.title("Participating Nations Over the Years")
#     nations_over_time = helper.participating_nations_over_time(df)
#     fig = px.line(nations_over_time, x="Edition", y="No of Countries", color_discrete_sequence=["yellow"])
#     st.plotly_chart(fig)
#
#     # Visualization of the number of events over the years
#     st.title("No of events over the years")
#     no_of_events = helper.no_of_events_over_time(df)
#     no_of_events = no_of_events.sort_values('Edition')
#     fig2 = px.line(no_of_events, x="Edition", y="No of Events", color_discrete_sequence=["orange"])
#     st.plotly_chart(fig2)
#
#     # Visualization of athlete participation over the years
#     st.title("Athlete Participation Over The Years")
#     athlete_over_time = helper.no_of_athletes_over_time(df)
#     fig3 = px.line(athlete_over_time, x="Edition", y="No of Athletes", color_discrete_sequence=["green"])
#     st.plotly_chart(fig3)
#
#     # Heatmap for the number of events over time in each sport
#     st.title("No. of Events over time(Every Sport)")
#     fig4, ax = plt.subplots(figsize=(20, 20))
#     ax = sns.heatmap(helper.heatmap(df), annot=True)
#     st.pyplot(fig4)
#
#     # Most successful athletes
#     st.title("Most Successful Athletes")
#     all_unique_sports = helper.unique_sports(df)
#     selected_sport = st.selectbox("Select a Sport", all_unique_sports)
#     successful_athletes = helper.top_performers(selected_sport, df, region_df)
#     st.table(successful_athletes)
#
# # Country-wise Analysis section
# if user_menu == 'Country-wise Analysis':
#     st.sidebar.header("Select Country")
#     country, years = helper.country_year_list(df)
#     if country[0] == 'Overall':
#         country.pop(0)
#     selected_country = st.sidebar.selectbox("Select Country", country)
#     country_performance = helper.country_performance(df1, selected_country)
#
#     # Visualization of the country's performance over the years
#     st.title("No of Gold Medals:-")
#     fig5 = px.line(country_performance, x="Year", y="Gold", color_discrete_sequence=["yellow"])
#     st.plotly_chart(fig5)
#
#     st.title("No of Silver Medals:-")
#     fig5 = px.line(country_performance, x="Year", y="Silver", color_discrete_sequence(["orange"]))
#     st.plotly_chart(fig5)
#
#     st.title("No of Bronze Medals")
#     fig5 = px.line(country_performance, x="Year", y="Bronze", color_discrete_sequence=["green"]))
#     st.plotly_chart(fig5)
#
#     st.title("Total Medals:-")
#     fig5 = px.line(country_performance, x="Year", y="Total", color_discrete_sequence=["pink"])
#     st.plotly_chart(fig5)
#
#     # Heatmap of sports the country is good at
#     st.title("Sports Countries Good At")
#     pivot_table = helper.heatmap2(selected_country, df)
#     if pivot_table.empty or pivot_table.isnull().all().all():
#         st.write("Country hasn't won any medal till date.")
#     else:
#         fig6, ax = plt.subplots(figsize=(25, 25))
#         ax = sns.heatmap(pivot_table, annot=True)
#         st.pyplot(fig6)
#
#     # Display the top 20 athletes from the selected country
#     st.title("Top 20 Athletes")
#     top_25_players = helper.country_top_athletes(selected_country, df)
#     if top_25_players.empty:
#         st.write("No athlete has won a medal till date.")
#     else:
#         st.table(top_25_players)
#
# # Athlete-wise Analysis section
# if user_menu == 'Athlete-wise Analysis':
#
#     # Distribution of medals by age
#     st.title("Age-wise Medal Distribution")
#     age_wise_medal = df.dropna(subset=['Medal'])
#     age_wise_medal = age_wise_medal.drop_duplicates(subset=['Name', 'Year', 'region'])
#     age_wise_medal = age_wise_medal.dropna(subset=['Age'])
#     x1 = age_wise_medal[age_wise_medal['Medal'] == 'Gold']['Age']
#     x2 = age_wise_medal[age_wise_medal['Medal'] == 'Silver']['Age']
#     x3 = age_wise_medal[age_wise_medal['Medal'] == 'Bronze']['Age']
#     x4 = age_wise_medal['Age']
#     fig7 = ss.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
#     fig7.update_layout(autosize=False, width=1000, height=600)
#     st.plotly_chart(fig7)
#
#     # Age-wise gold medal distribution for each sport
#     st.title("Age-wise Gold Medal Distribution in each Sport")
#     sports = helper.get_sports(df)
#     selected_sport = st.selectbox("select the sport", sports)
#
#     temp_df = df.dropna(subset=['Medal'])
#     temp_df = temp_df[temp_df['Sport'] == selected_sport]
#     age_counts = temp_df['Age'].value_counts().sort_index()
#     age_probabilities = age_counts / age_counts.sum()
#     prob_df = age_probabilities.reset_index()
#     prob_df.columns = ['Age', 'Probability']
#     fig8 = px.line(prob_df, x='Age', y='Probability', title='Probability vs Age', color_discrete_sequence=["yellow"])
#     st.plotly_chart(fig8)
#
#     # Scatter plot of height vs weight with medals and sex categories
#     st.title("Height Vs Weight")
#     Sports = df['Sport'].unique().tolist()
#     Sports.sort()
#     sport = st.selectbox("select a sport", Sports)
#     temp_df = helper.weight_v_height(df, sport)
#     fig9, ax = plt.subplots()
#     ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=100)
#     st.pyplot(fig9)
#
#     # Line chart for male and female participation over the years
#     st.title("Man and Women Participation over the Years")
#     fig10 = helper.men_women(df)
#     st.plotly_chart(fig10)
