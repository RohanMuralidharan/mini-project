import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

root = Path(__file__).resolve().parent.parent
csv_path = root / 'saved_tracks_demo.csv'
if csv_path.exists():
  df = pd.read_csv(csv_path)
else:
  df = pd.read_csv(r'C:\JupyterRoot\Datasets\akshay_spotify.csv')
st.set_page_config(layout="wide")
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.title('Spotify User Dashboard')


col1, col2 = st.beta_columns(2)
#
col1.header("Your Latest added Song")
top_5_songs = df[['name','artists']].head(5)
col1.table(top_5_songs)
#
col2.header("Your Top 10 Artists")
df1 = df['artists'].value_counts()[:11].to_frame()
df1['Name'] = df1.index
df1.rename(columns={'artists':'Songs'},inplace=True)
fig = px.pie(df1, values='Songs', names='Name', hole=0.2)
fig.update_traces(textposition='inside', textinfo='label')
col2.plotly_chart(fig, use_container_width=True)
####

col3, col4, col5 = st.beta_columns(3)
#




ur_favourite_artist = df[['artists']].value_counts().index[0][0]
st.markdown("""
<style>
.big-font {
    font-size:30px !important;
    font-Weight: bold;
}
</style>
""", unsafe_allow_html=True)

col3.header("Your Favourite Artist")
col3.markdown(f'<p class="big-font">{str(ur_favourite_artist)}</p>', unsafe_allow_html=True)
#
col4.header("Total Time of Songs")
time = round(df.duration_s.sum()/3600,2)
col4.markdown(f'<p class="big-font">{round(df.duration_s.sum()/3600,2)} hours</p>', unsafe_allow_html=True)
#
col5.header("Total Number of Songs")
col5.markdown(f'<p class="big-font">{df.count()[1]} songs</p>', unsafe_allow_html=True)
#
####

col6, col7 = st.beta_columns(2)
#
col6.header("Your Recommended Songs")
ur_favourite_artist = df[['artists']].value_counts().index[0][0]
df2 = df[df['artists'] == ur_favourite_artist].sort_values \
                    (by = ['popularity'],ascending = False) \
                    [['name','artists','popularity']].reset_index(drop=True)
col6.table(df2.head(5))
#
col7.header("Features of your Latest Songs")
df3 = df.loc[:4,['name', 'artists', 'acousticness', 'liveness', 'instrumentalness', \
                'energy', 'danceability', 'valence']]
df3 = df3.T.reset_index()
df3.rename(columns={'index':'theta', 0:'zero', 1:'one', 2:'two', \
                   3:'three', 4:'four'},inplace=True)
df3_cols = df3.columns[1:]
len_cols = len(df3_cols)
categories = df3['theta'].tolist()[2:]
fig1 = go.Figure()
for i in range(0,len_cols):
    fig1.add_trace(go.Scatterpolar(
      r= df3[df3_cols[i]][2:].tolist(),
      theta=categories,
      fill='toself',
      name=df3[df3_cols[i]][0]))
fig1.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 1]
    )),
  showlegend=True
)
col7.plotly_chart(fig1, use_container_width=True)

