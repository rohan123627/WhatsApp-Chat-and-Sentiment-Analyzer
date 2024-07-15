from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji
extract = URLExtract()
def fetch_states(selected_user,df):
    if selected_user!='Overall':
        df=df[df['users']==selected_user]
    num_messages = df.shape[0] 

    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0] 

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return num_messages,len(words),num_media_messages,len(links)  
def most_busy_user(df):
    #The function most_busy_user(df) takes a pandas DataFrame df as input, where each row represents a user and contains a column named users with the name of the user. The function then calculates the count of occurrences of each user in the users column using the pandas value_counts() method and returns the top 5 most frequent users using the head() method.

    x=df['users'].value_counts().head()

    #Additionally, the function calculates the percentage of each user's occurrence in the users column by dividing the count of each user by the total number of rows in the DataFrame df and multiplying by 100. The resulting percentages are rounded to two decimal places using the round() method.

    df=round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns ={'index':'name','users':'percentage'})

    return x,df

def emoji_helper(selected_user,df):
    

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis)))).rename(columns ={0:'EMOJI',1:'COUNTS'})

    return emoji_df
def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()  #-->The function  groups the messages in the DataFrame by year and month, and counts the number of messages in each group. 
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time'] = time #-->The function then creates a new column called 'time', which combines the month and year into a single string in the format "month-year". This is useful for creating a timeline plot of message activity over time.
    return timeline
def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline
def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    return df['day_name'].value_counts()
def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    return df['month'].value_counts()