import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
#from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os
st.title('Sentiment Analysis of Tweeets about US Airlines')
#st.markdown('My first streamlit dashboard')
st.sidebar.title('Sentiment Analysis of Tweeets about US Airlines')
st.markdown('This app is used to analyze sentiment of tweets.🇨🇳')
st.sidebar.markdown('Analyze sentiment of tweets.🇨🇳')

path = os.path.dirname(__file__)
data_url =  os.path.join(path, 'Tweets.csv')       

#data_url = ('/Users/dahaixing/Downloads/archive (2)/Tweets.csv')

@st.cache(persist=True)
def load_data():
    data = pd.read_csv(data_url)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'] ) 
    print(data.head())
    return data


data = load_data()

st.sidebar.subheader('Show random tweet')
random_tweet = st.sidebar.radio('Sentiment Type', 
    ('positive', 'neutral', 'negative'))

#st.sidebar.markdown(data.loc[data['airline_sentiment']== random_tweet][['text']].sample(n=1).iat[0,0])
st.sidebar.markdown(data.query('airline_sentiment== @random_tweet')[['text']].sample(n=1).iat[0,0])

st.sidebar.markdown('### Num of tweets by sentiment')

select = st.sidebar.selectbox('Visualization type', ['Hist', 'Piechart'], key = '1')
sentiments_count = data['airline_sentiment'].value_counts()
sentiments_count = pd.DataFrame({'Sentiment': sentiments_count.index, 'Tweets': sentiments_count.values})

if not st.sidebar.checkbox('Hide', True):
    st.markdown('### Number of tweets by sentiment')
    if select == 'Hist':
        fig = px.bar(sentiments_count, x = 'Sentiment', y = 'Tweets', color  = 'Tweets', height = 500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiments_count, names = 'Sentiment', values = 'Tweets')
        st.plotly_chart(fig)


st.sidebar.subheader('When and where are users tweeting from')
#map_data = pd.read_csv('/Users/dahaixing/Downloads/crimes/2022-05/2022-05-south-wales-street.csv')
map_data = pd.read_csv(os.path.join(path, '2022-05-south-wales-street.csv') ) 
map_data = map_data[(map_data['latitude'].notnull())&(map_data['longitude'].notnull())]
#st.map(map_data)
#st.write(map_data)

hour  = st.sidebar.slider('Month', 1, 12)
hour2  = st.sidebar.number_input('Month', 1, 12)
map_data['Month']=pd.to_datetime(map_data['Month'])
map_data['year'] = pd.DatetimeIndex(map_data['Month']).year
map_data['month_real'] = pd.DatetimeIndex(map_data['Month']).month
map_data_num_tweets = map_data.query('month_real == @hour')['Month'].count()
if not st.sidebar.checkbox('Close', True, key = '1'):
    st.markdown('### Tweet location based on month')
    st.map(map_data.query('month_real == @hour'))
    st.markdown('%i tweeets in month %i' %(map_data_num_tweets,hour))
    if st.sidebar.checkbox('Show raw data', False):
        st.write(map_data.query('month_real == @hour'))

st.sidebar.subheader('Breakdown airline tweets by sentiments')
choice = st.sidebar.multiselect('Pick airlines', ('Virgin America', 'United', 'Southwest', 'Delta', 'US Airways',
       'American'), key ='0')
if len(choice) >0:
    choice_data = data[data['airline'].isin(choice)]
    fig_choice = px.histogram(choice_data, x = 'airline', y = 'airline_sentiment', histfunc='count', 
            color = 'airline_sentiment', facet_col = 'airline_sentiment', labels = {'airline_sentiment':'tweets'}, height = 600, width = 800)
    st.plotly_chart(fig_choice)

st.sidebar.header('Word Cloud')

#st.write(map_data_num_tweets)