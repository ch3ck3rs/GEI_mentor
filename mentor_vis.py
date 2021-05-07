""" This doc will use streamlit to visualize the mentor data """

import streamlit as st
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# streamlit options
st.set_option('deprecation.showPyplotGlobalUse', False)

# data import
mentor_topics = pd.read_csv('./NA Mentor Topics.csv')
survey_bin = pd.read_csv('./NA Mentor Cleaned binary.csv')
survey = pd.read_csv('./NA Mentor Cleaned.csv')

# set up colors
Ecolab_blu = '#007AC9'
lt_blu = '#5EB6E4'
dk_blu = '#005172'
gry = '#616265'
lt_gry = '#ADAFAF'
red = '#E00034'
aqua = '#2AD2C9'
blk = '#000000'
white = '#ffffff'
cmap = ListedColormap([Ecolab_blu, gry, dk_blu, lt_gry, lt_blu, aqua, blk, Ecolab_blu, gry, dk_blu, lt_gry, lt_blu])



st.title('Exploring Mentor Survey Results')

st.write('Below is a copy of the dataset after it has been cleaned and some basic stats.')
if st.checkbox('Show Dataframe'):
    survey_bin

respondents = len(survey_bin['id'])
start_date = survey_bin.iloc[0]['start_time'].split(' ',1)[0]

st.write('This survey had ', respondents, ' respondents and was administered the week of ', start_date, '.')

# Do you have a current mentor?

current_df = survey.groupby(['mentor_current']).size()
current = current_df.plot(kind='pie', y='mentor_current', colormap=cmap, figsize=(5,5))
current.set_title('Do you currently have a mentor?')
current.set_ylabel(None)

st.write('We asked respondents if they currently had a mentor.  ', current_df['Yes'], ' of the respondets replied "Yes" they have a mentor and ', current_df['No'], ' replied "No" they do not have a mentor currently.')
c1, c2, c3 = st.beta_columns((1,2,1))
c2.pyplot()

# have you ever had a mentor?

ever_df = survey.groupby(['mentor_ever']).size()

st.write('We were also curious if respondents had ever had a mentor.  ', ever_df['Yes'], 'respondents have had a previous mentor and ', ever_df['No'], ' have not had a previous mentor.')
c1,c2 = st.beta_columns(2)

ever_df_no = survey[survey['mentor_ever']=='No'].groupby(['mentor_ever', 'mentor_current']).size()
ever_df_yes = survey[survey['mentor_ever']=='Yes'].groupby(['mentor_ever', 'mentor_current']).size()

ever_no = ever_df_no.unstack().plot(kind='bar', colormap=cmap)
ever_no.set_ylim([0,18])
ever_no.set_xlabel("")
ever_no.legend(title='Current mentor')
ever_no.annotate('confusion', xy=(0.15,4), xytext=(0.25,8), 
        arrowprops=dict(facecolor='black', shrink=0.05))

c1.header("Previous Mentor = Never")
c1.pyplot()

ever_yes = ever_df_yes.unstack().plot(kind='bar', colormap=cmap)
ever_yes.set_ylim([0,18])
ever_yes.set_xlabel("")
ever_yes.legend(title='Current mentor')

c2.header("Previous Mentor = Yes")
c2.pyplot()
ever_df = survey.groupby(['mentor_ever', 'mentor_current']).size()
# ever_df
# st.write(ever_df_yes)

# interenst in having a mentor or having a second mentor

st.header('Desire for a mentor')
# TODO: add df groupby 'mentor_desired' and 'mentor_additional' show in a similar manner to that above. 

# Interest by topic

# TODO: create pie chart by column

st.header('Topics of Interest')
st.write('We gave respondents a list of topics to choose from.  They were allowed to select as many topics as they liked.  Below you see those topics that recieved more than one vote. ')
topics_total = mentor_topics.iloc[34].copy()
topics_total.drop(['Unnamed: 0','id'], inplace=True)

topics_plot = topics_total.where(topics_total >1).plot(kind='pie', colormap=cmap)
topics_plot.set_title(label='')
plt.show()
st.pyplot()

topics_total

st.header('What has been learned from mentors in the past?')


st.header('What function would you like your mentor to come from?')