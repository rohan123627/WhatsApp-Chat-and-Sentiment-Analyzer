# Importing modules
import nltk
import streamlit as st
import re
import preprocessor1,helper1,preprocessor,helper
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
selected = option_menu("CHOOSE AN OPTION",
                       ["WHATSAPP CHAT ANALYZER",
                        "WHATSAPP SENTIMENT ANALYZER"],
                        )

if (selected == "WHATSAPP SENTIMENT ANALYZER"):
    
    st.sidebar.title("Whatsapp Chat  Sentiment Analyzer")

    
    nltk.download('vader_lexicon')

    
    uploaded_file = st.sidebar.file_uploader("Choose a file")

    
    st. markdown("<h1 style='text-align: center;'>Whatsapp Chat  Sentiment Analyzer</h1>", unsafe_allow_html=True)

    if uploaded_file is not None:
        
        
        bytes_data = uploaded_file.getvalue()
        d = bytes_data.decode("utf-8")
        
        # Perform preprocessing
        data = preprocessor1.preprocess(d)
        
        # Importing SentimentIntensityAnalyzer class from "nltk.sentiment.vader"
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        
        # Object
        sentiments = SentimentIntensityAnalyzer()
        
        # Creating different columns for (Positive/Negative/Neutral)
        data["po"] = [sentiments.polarity_scores(i)["pos"] for i in data["message"]] # Positive
        data["ne"] = [sentiments.polarity_scores(i)["neg"] for i in data["message"]] # Negative
        data["nu"] = [sentiments.polarity_scores(i)["neu"] for i in data["message"]] # Neutral
        
        # To indentify true sentiment per row in message column
        def sentiment(d):
            if d["po"] >= d["ne"] and d["po"] >= d["nu"]:
                return 1
            if d["ne"] >= d["po"] and d["ne"] >= d["nu"]:
                return -1
            if d["nu"] >= d["po"] and d["nu"] >= d["ne"]:
                return 0

        # Creating new column & Applying function
        data['value'] = data.apply(lambda row: sentiment(row), axis=1)
        
        # User names list
        user_list = data['user'].unique().tolist()
        
        # Sorting
        user_list.sort()
        
        # Insert "Overall" at index 0
        user_list.insert(0, "Overall")
        
        # Selectbox
        selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
        
        if st.sidebar.button("Show Analysis"):
            # Monthly activity map
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("<h3 style='text-align: center;'>Monthly Activity map(Positive)</h3>",unsafe_allow_html=True)
                
                busy_month = helper1.month_activity_map(selected_user, data,1)
                
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.markdown("<h3 style='text-align: center;'>Monthly Activity map(Neutral)</h3>",unsafe_allow_html=True)
                
                busy_month = helper1.month_activity_map(selected_user, data, 0)
                
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='grey')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col3:
                st.markdown("<h3 style='text-align: center; '>Monthly Activity map(Negative)</h3>",unsafe_allow_html=True)
                
                busy_month = helper1.month_activity_map(selected_user, data, -1)
                
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            # Daily activity map
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("<h3 style='text-align: center;'>Daily Activity map(Positive)</h3>",unsafe_allow_html=True)
                
                busy_day = helper1.week_activity_map(selected_user, data,1)
                
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.markdown("<h3 style='text-align: center;'>Daily Activity map(Neutral)</h3>",unsafe_allow_html=True)
                
                busy_day = helper1.week_activity_map(selected_user, data, 0)
                
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='grey')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col3:
                st.markdown("<h3 style='text-align: center;'>Daily Activity map(Negative)</h3>",unsafe_allow_html=True)
                
                busy_day = helper1.week_activity_map(selected_user, data, -1)
                
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            
            # Daily timeline
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("<h3 style='text-align: center; '>Daily Timeline(Positive)</h3>",unsafe_allow_html=True)
                
                daily_timeline = helper1.daily_timeline(selected_user, data, 1)
                
                fig, ax = plt.subplots()
                ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.markdown("<h3 style='text-align: center; '>Daily Timeline(Neutral)</h3>",unsafe_allow_html=True)
                
                daily_timeline = helper1.daily_timeline(selected_user, data, 0)
                
                fig, ax = plt.subplots()
                ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='grey')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col3:
                st.markdown("<h3 style='text-align: center; '>Daily Timeline(Negative)</h3>",unsafe_allow_html=True)
                
                daily_timeline = helper1.daily_timeline(selected_user, data, -1)
                
                fig, ax = plt.subplots()
                ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            # Monthly timeline
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("<h3 style='text-align: center; '>Monthly Timeline(Positive)</h3>",unsafe_allow_html=True)
                
                timeline = helper1.monthly_timeline(selected_user, data,1)
                
                fig, ax = plt.subplots()
                ax.plot(timeline['time'], timeline['message'], color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.markdown("<h3 style='text-align: center; '>Monthly Timeline(Neutral)</h3>",unsafe_allow_html=True)
                
                timeline = helper1.monthly_timeline(selected_user, data,0)
                
                fig, ax = plt.subplots()
                ax.plot(timeline['time'], timeline['message'], color='grey')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col3:
                st.markdown("<h3 style='text-align: center; '>Monthly Timeline(Negative)</h3>",unsafe_allow_html=True)
                
                timeline = helper1.monthly_timeline(selected_user, data,-1)
                
                fig, ax = plt.subplots()
                ax.plot(timeline['time'], timeline['message'], color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            # Percentage contributed
            if selected_user == 'Overall':
                col1,col2,col3 = st.columns(3)
                with col1:
                    st.markdown("<h3 style='text-align: center; '>Most Positive Contribution</h3>",unsafe_allow_html=True)
                    x = helper1.percentage(data, 1)
                    
                    # Displaying
                    st.dataframe(x)
                with col2:
                    st.markdown("<h3 style='text-align: center; '>Most Neutral Contribution</h3>",unsafe_allow_html=True)
                    y = helper1.percentage(data, 0)
                    
                    # Displaying
                    st.dataframe(y)
                with col3:
                    st.markdown("<h3 style='text-align: center; '>Most Negative Contribution</h3>",unsafe_allow_html=True)
                    z = helper1.percentage(data, -1)
                    
                    # Displaying
                    st.dataframe(z)


            # Most Positive,Negative,Neutral User...
            if selected_user == 'Overall':
                
                # Getting names per sentiment
                x = data['user'][data['value'] == 1].value_counts().head(10)
                y = data['user'][data['value'] == -1].value_counts().head(10)
                z = data['user'][data['value'] == 0].value_counts().head(10)

                col1,col2,col3 = st.columns(3)
                with col1:
                    # heading
                    st.markdown("<h3 style='text-align: center; '>Most Positive Users</h3>",unsafe_allow_html=True)
                    
                    # Displaying
                    fig, ax = plt.subplots()
                    ax.bar(x.index, x.values, color='green')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    # heading
                    st.markdown("<h3 style='text-align: center; '>Most Neutral Users</h3>",unsafe_allow_html=True)
                    
                    # Displaying
                    fig, ax = plt.subplots()
                    ax.bar(z.index, z.values, color='grey')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col3:
                    # heading
                    st.markdown("<h3 style='text-align: center; '>Most Negative Users</h3>",unsafe_allow_html=True)
                    
                    # Displaying
                    fig, ax = plt.subplots()
                    ax.bar(y.index, y.values, color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

if(selected =="WHATSAPP CHAT ANALYZER"):
    st. markdown("<h1 style='text-align: center;'>Whatsapp Chat Analyzer</h1>", unsafe_allow_html=True)
    st.sidebar.title("WHATS APP CHAT ANALYZER")
    uploaded_file=st.sidebar.file_uploader("CHOOSE A FILE")


    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        
        df=preprocessor.preprocess(data)
        #st.dataframe(df)
        
        
        
        
        user_list=df['users'].unique().tolist()
        #user_list.remove('group_notification')
        #User names list
        #user_list = data['user'].unique().tolist()

        # Check if 'group_notification' is in the list before removing
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        else:
            print("'group_notification' not found in the list")
        # Try to remove 'group_notification' from the list
        try:
            user_list.remove('group_notification')
        except ValueError:
            print("'group_notification' not found in the list")

        user_list.sort()
        user_list.insert(0,'Overall')
        selected_user = st.sidebar.selectbox("Show analysis with respect to",user_list) 
        if st.sidebar.button("Show analysis"):
            num_messages,words,num_media_messages,links = helper.fetch_states(selected_user,df)
            st.title("TOP STATISTICS")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.header("Total Messages")
                st.header("")
                st.header("")
                st.title(num_messages)
            with col2:
                st.header("Total Words")
                st.header("")
                st.header("")
                st.title(words)
            with col3:
                st.header("No of media shared")
                st.header("")
                st.title(num_media_messages)
            with col4:
                st.header("No of links shared")
                st.header("")
                st.header("")
                
                st.title(links)
            st.title("MONTHLY TIMELINE")
            timeline= helper.monthly_timeline(selected_user,df)
            fig,ax=plt.subplots()
            ax.plot(timeline['time'],timeline['message'],color='green')
            plt.xticks(rotation='vertical')
            plt.xlabel('MONTHS-YEAR',fontdict={'fontsize': 14,'fontweight': 10})
            plt.ylabel('No. of messages',fontdict={'fontsize': 14,'fontweight': 10})
            st.pyplot(fig)
            
            #activity map
            st.title("ACTIVITY MAP")
            col1,col2 = st.columns(2)
            with col1:
                st.header("MOST BUSY DAY")
                busy_day = helper.week_activity_map(selected_user,df)
                fig,ax=plt.subplots()
                ax.bar(busy_day.index,busy_day.values)
                plt.xticks(rotation='vertical')
                plt.xlabel('DAY',fontdict={'fontsize': 14,'fontweight': 10})
                plt.ylabel('NO OF MESSAGEs',fontdict={'fontsize': 14,'fontweight': 10})
                st.pyplot(fig)
            with col2:
                st.header('MOST BUSY MONTH')
                busy_month = helper.month_activity_map(selected_user,df)
                fig ,ax = plt.subplots()
                ax.bar(busy_month.index,busy_month.values,color='orange')
                plt.xticks(rotation='vertical')
                plt.xlabel('MONTHS',fontdict={'fontsize': 14,'fontweight': 10})
                plt.ylabel('NO OF MESSAGES',fontdict={'fontsize': 14,'fontweight': 10})
                st.pyplot(fig)
            
            # finding the busiest user in group in the group
            if selected_user == 'Overall':
                st.title('Most Busy users')
                x,new_df=helper.most_busy_user(df)
                fig,ax = plt.subplots()
                col1,col2 = st.columns(2)
                with col1:
                    ax.bar(x.index,x.values,)
                    plt.xticks(rotation='vertical')
                    plt.xlabel('USER NAME',fontdict={'fontsize': 14,'fontweight': 10})
                    plt.ylabel('NO OF MESSAGES',fontdict={'fontsize': 14,'fontweight': 10})
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df,50,300,use_container_width=True)
            emoji_df=helper.emoji_helper(selected_user,df)
            st.title("Emoji Analysis")
            
            st.dataframe(emoji_df,50,300,use_container_width=True)
            

            

                
