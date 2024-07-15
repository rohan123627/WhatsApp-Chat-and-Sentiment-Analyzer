# Importing modules
import streamlit as st
from urlextract import URLExtract

import pandas as pd
from collections import Counter

# Object
extract = URLExtract()

# -1 => Negative
# 0 => Neutral
# 1 => Positive

# Will return count of messages of selected user per day having k(0/1/-1) sentiment
def week_activity_map(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value'] == k]
    return df['day_name'].value_counts()


# Will return count of messages of selected user per month having k(0/1/-1) sentiment
def month_activity_map(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value'] == k]
    return df['month'].value_counts()



# Will return count of messages of selected user per date having k(0/1/-1) sentiment
def daily_timeline(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value']==k]
    # count of message on a specific date
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline


# Will return count of messages of selected user per {year + month number + month} having k(0/1/-1) sentiment
def monthly_timeline(selected_user,df,k):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df = df[df['value']==-k]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

# Will return percentage of message contributed having k(0/1/-1) sentiment
def percentage(df,k):
    df = round((df['user'][df['value']==k].value_counts() / df[df['value']==k].shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return df