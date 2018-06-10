# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 14:01:17 2018

@author: Sriram
"""

import pandas as pd
import numpy as np 

#read social interaction data
df = pd.read_csv('doc_social_interaction.csv',header=0)

#change str to int
df.social_interaction_id.apply(pd.to_numeric)
#get total of each interaction
a = df.groupby('doc_id')['social_interaction_id'].value_counts().reset_index(name="Total_Count").sort_values(by='doc_id')
#make rows to column
b = a.pivot(index = 'doc_id' , columns='social_interaction_id',values='Total_Count').reset_index()
#renaming column
total_count = b.rename(index=str,columns={1:'TOTAL_LIKE',2:'TOTAL_COMMENT',3:'TOTAL_SHARE',4:'TOTAL_VIEW'})
#sort the main df by date and drop duplicates and keep the latest date, to know last activity date
sorted = df.sort_values('last_modified_date')
latest_date = sorted.drop_duplicates('doc_id',keep='last').sort_values(by='doc_id')

#merge first result and second result
new_df = pd.merge(total_count,latest_date,how='inner',on='doc_id',copy=True)
#renaming certain columns
new_df = new_df.rename(index=str, columns={'last_activity':'last_activity_date','feed_id':'last_feed_activity'})
#dropping social interaction column which came to the new df from second result
new_df = new_df.drop(['social_interaction_id'],axis = 1)
#creating no of days inactive column
new_df['last_activity_date'] = new_df['last_activity_date'].apply(pd.to_datetime)
new_df['present_date']= pd.Timestamp.today()

new_df['no_of_days_inactive'] = new_df['present_date'].subtract(new_df['last_activity_date'])
new_df['no_of_days_inactive'] = new_df['no_of_days_inactive'].apply(lambda x: float(x.days))
new_df = new_df.fillna(0)

new_df['is_churn'] = new_df['no_of_days_inactive'] > 30
 
new_df.info()
