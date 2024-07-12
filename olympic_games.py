import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.title("Olympic Data Dashboard")

# Load data
gender = pd.read_excel('2021_EntriesGender.xlsx')
teams = pd.read_excel('2021_Teams.xlsx')
athletes = pd.read_excel('2021_Athletes.xlsx')
coaches = pd.read_excel('2021_Coaches.xlsx')
medals = pd.read_excel('2021_Medals.xlsx')

# Medals DataFrame
st.subheader("Top 10 Teams by Medal Count")
medals_top10 = medals.head(10).sort_values(by="Rank by Total", ascending=True)
st.dataframe(medals_top10.style.set_properties(**
    {'background-color': '#F0F0F0','color': '#222222','border': '1.5px  solid black'}).bar(
    color='#FFD700',vmin = 100_000,subset=['Gold']).bar(
    color='#C0C0C0',vmin = 100_000,subset=['Silver']).bar(
    color='#CD7F32',vmin=100_000,subset =['Bronze'])
)

# Pie chart of total medals
st.subheader("Pie Chart of Total Medals by Team")
fig, ax = plt.subplots()
ax.pie(medals['Total'], labels=medals['Team/NOC'], autopct='%1.1f%%', radius=2)
st.pyplot(fig)

# Bar plot of top 10 athletes by discipline count
st.subheader("Top 10 NOCs by Athlete Count")
top10_athlete = athletes.groupby('NOC')['Discipline'].describe()
top10_athlete.sort_values(by='count', ascending=False, inplace=True)
fig, ax = plt.subplots(figsize=(14, 6))
sns.barplot(x='count', y=top10_athlete.index[:10], data=top10_athlete[:10], palette='coolwarm', ax=ax)
st.pyplot(fig)

# Bar plot of top 10 NOCs by unique disciplines
st.subheader("Top 10 NOCs by Unique Disciplines")
top10_discpl_country = athletes.groupby('NOC')['Discipline'].describe()
top10_discpl_country.sort_values(by='unique', ascending=False, inplace=True)
fig, ax = plt.subplots(figsize=(14, 6))
sns.barplot(x='unique', y=top10_discpl_country.index[:10], data=top10_discpl_country[:10], palette='coolwarm', ax=ax)
st.pyplot(fig)

# Bar plot of medals by type for top 10 NOCs
st.subheader("Medal Distribution for Top 10 NOCs")
medals_top10 = medals.head(10)
fig, ax = plt.subplots(figsize=(14, 6))
medals_top10.plot(x='Team/NOC', y=['Gold', 'Silver', 'Bronze'], kind='bar', ax=ax, color=['#FFD700', '#C0C0C0', '#cd7f32'], rot=18)
st.pyplot(fig)

# Plotly bar chart
st.subheader("Plotly Bar Chart of Medal Distribution")
plot_medals = medals.sort_values(by='Total', ascending=False).reset_index(drop=True).head(10)
fig = px.bar(plot_medals, x='Team/NOC', y=['Gold', 'Silver', 'Bronze'],
             color_discrete_sequence=['#FFD700', '#C0C0C0', '#cd7f32'],
             title="Distribution of Medals across Countries")
st.plotly_chart(fig)

# Choropleth map
st.subheader("Choropleth Map of Total Medals by Country")
fig = px.choropleth(medals, locations="Team/NOC", locationmode='country names', color="Total",
                    hover_name="Team/NOC", range_color=[1, 100],
                    color_continuous_scale="blues", title='Map: Glide over any country to see their total medals')
st.plotly_chart(fig)
