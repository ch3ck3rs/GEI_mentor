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

st.markdown('## Summary')
st.write('This survey had ', respondents, ' respondents and was administered \
    the week of ', start_date, '.  The average time for completion was 10 min.')

st.write('Of the ', respondents, ' respondents, 24 ',\
    ' would like to have a mentor.  Most respondents do not have a preference for a \
    mentor inside or outside of engineering, but would like to gain a better understanding \
    of Finance and RD&E.  The main topics of interest were Career Development followed by \
    Influencing Others and Building your Brand.')

# Do you have a current mentor?

current_df = survey.groupby(['mentor_current']).size()
current = current_df.plot(kind='pie', y='mentor_current', colormap=cmap, figsize=(5,5))
current.set_title('Do you currently have a mentor?')
current.set_ylabel(None)

st.markdown('### Current Mentor Status')
st.write('We asked respondents if they currently had a mentor.  ', current_df['Yes'], \
' of the respondets replied "Yes" they have a mentor and ', current_df['No'], \
' replied "No" they do not have a current mentor. ')
c1, c2, c3 = st.beta_columns((1,2,1))
c2.pyplot()

# have you ever had a mentor?

ever_df = survey.groupby(['mentor_ever']).size()


st.markdown('### Previous Mentor Status')
st.write('We were also curious if respondents had ever had a mentor.  ', \
    ever_df['Yes'], 'respondents have had a previous mentor and ', ever_df['No'], \
    ' have not had a previous mentor.  The dark blue bars below are those that \
    currently have a mentor and the light blue bar are those that do not have a current mentor.')
c1,c2 = st.beta_columns(2)

ever_df_no = survey[survey['mentor_ever']=='No'].groupby(['mentor_ever', 'mentor_current']).size()
ever_df_yes = survey[survey['mentor_ever']=='Yes'].groupby(['mentor_ever', 'mentor_current']).size()

ever_no = ever_df_no.unstack().plot(kind='bar', colormap=cmap)
ever_no.set_ylim([0,18])
ever_no.set_xlabel("")
ever_no.legend(title='Current mentor')
ever_no.annotate('First time mentees', xy=(0.15,4), xytext=(0.2,8), 
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

# TODO: add df groupby 'mentor_desired' and 'mentor_additional' show in a similar manner to that above. 

desire = survey[survey['mentor_current']=='No'].groupby('mentor_desired').size()
addnl = survey[survey['mentor_current']=='Yes'].groupby('mentor_additional').size()

st.markdown('### Desire for a mentor:')
st.write('Of the ', respondents, ' respondents ', desire['Yes']+addnl['Yes'], 'would like a mentor. \n \
    \n Respondents were asked if they desired a mentor if they did not have one, \
    or an additional mentor if they have current mentor.  Of the ', current_df['No'], \
    ' respondents who do not have a mentor, ', desire['Yes'], ' would like to have a mentor. \
    And of the ', current_df['Yes'], ' respondents who have a current mentor, ', addnl['Yes'], \
    ' would like to have an additional mentor.')



# Interest by topic

# TODO: create pie chart by column

st.header('Topics of Interest')
st.write('To understand what respondents would like to be mentored in, we gave \
    respondents a list of topics to choose from.  They were allowed to select all \
    topics that applied to them.  The below chart shows all options provided to \
    respondents and the corresponding votes.   \n \
    \n Career Development recieved the most votes with 25 of 34 respondents selecting this option.')



topics_total = mentor_topics.iloc[34].copy()
topics_total.drop(['Unnamed: 0','id'], inplace=True)


topics_plot = topics_total.sort_values(ascending=True).plot(kind='barh', colormap=cmap)
topics_plot.set_ylabel('')
plt.show()
st.pyplot()


st.header('What has been learned from mentors in the past?')

st.markdown('summary of responses')

lesson = survey['mentor_benefits_str'].dropna()

if st.checkbox('Show detailed responses for mentoring benefits'):
    for response in lesson:
        st.write(response)

st.header('What function would you like your mentor to come from?')

# TODO: remind desire for current mentor (just number)
# TODO: bag of words / pie chart where people would like mentor to come from

in_out = survey.groupby('mentor_in_out').size()
functions = survey['mentor_function'].dropna()

st.markdown('We asked respondents if they wanted a mentor from within the greater \
    engineering organization or outside of engineering.  Most are open to either \
    inside or outside of engineering.  \n \
    \n For those that wanted a mentor outside of engineering, we asked what function \
    they saught a mentor from. The top requests are **RD&E** and **Finance**, \
    followed closely by Sales and Marketing with Enterprise Excellence and \
    Executive Management getting an honerable mention. ')


in_out_plot = in_out.plot(kind='pie', colormap=cmap)
in_out_plot.set_ylabel('')
c1, c2, c3 = st.beta_columns((1,2,1))
c2.pyplot()



if st.checkbox('Show detailed responses for mentor function'):
    for response in functions:
        st.write(response)
