# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import plotly.express as px

company_list = [
    r'C:\\Users\\rguru\\Desktop\\Certificates & course notes\\Statistics for DS notes\\S&P project\\individual_stocks_5yr\\AAL_data.csv',
    r'C:\\Users\\rguru\\Desktop\\Certificates & course notes\\Statistics for DS notes\\S&P project\\individual_stocks_5yr\\AAPL_data.csv',
    r'C:\\Users\\rguru\\Desktop\\Certificates & course notes\\Statistics for DS notes\\S&P project\\individual_stocks_5yr\\AMAT_data.csv',
    r'C:\\Users\\rguru\\Desktop\\Certificates & course notes\\Statistics for DS notes\\S&P project\\individual_stocks_5yr\\AMD_data.csv'
]

# Read and merge all CSVs
all_df = pd.DataFrame()
for file in company_list:
    current_df = pd.read_csv(file)
    all_df = pd.concat([all_df, current_df], ignore_index=True)

# Convert date column
all_df['date'] = pd.to_datetime(all_df['date'])

# Streamlit dashboard
st.set_page_config(page_title='Stock Analysis Dashboard', layout='wide')
st.title("EDA Dashboard")

tech_list = all_df['Name'].unique()

st.sidebar.title("Choose a company")
selected_company = st.sidebar.selectbox("Select a company", tech_list)

company_df=all_df[all_df['Name'] == selected_company]
company_df.sort_values('date',inplace=True)
##1st plot
st.subheader(f"1. Closing Price of {selected_company} over time")
fig1=px.line(company_df,x='date',y='close',title=selected_company + " closing price over time")
st.plotly_chart(fig1,use_container_width=True)

##2nd plot
st.subheader("2. Moving Averages (10, 20, 50 days)")
ma_day=[10,20,50]
for ma in ma_day:
    company_df['close_'+str(ma)]=company_df['close'].rolling(ma).mean()
fig2=px.line(company_df,x='date',y=['close','close_10','close_20','close_50'],title=selected_company + " closing price with moving average")
st.plotly_chart(fig2,use_container_width=True)

##3rd plot
st.subheader("3. Daily returns for "+selected_company)
company_df['Daily return']=company_df['close'].pct_change()*100
fig3=px.line(company_df,x='date',y='Daily return',title="Daily return")
st.plotly_chart(fig3,use_container_width=True)

##4th plot
st.subheader("4.Resample closing price ")
company_df.set_index('date',inplace=True)
resample_option=st.radio('Select resample frequency', ['Monthly', "Quarterly","Yearly"])
if resample_option=="Monthly":
    resampled= company_df['close'].resample('M').mean()
elif resample_option=="Quarterly":
    resampled=company_df['close'].resample('Q').mean()
else:
    resampled=company_df['close'].resample('Y').mean()
resampled = resampled.reset_index()
resampled.columns = ['date', 'close']

fig4 = px.line(
    resampled,
    x='date',
    y='close',
    title=f"{selected_company} {resample_option} average closing price"
)
st.plotly_chart(fig4, use_container_width=True)

##5th plot
st.subheader("5. Closing price correlation ")
aal=pd.read_csv(company_list[0])
aapl=pd.read_csv(company_list[1])
amat=pd.read_csv(company_list[2])
amd=pd.read_csv(company_list[3])
 
dfs = {
    "aal": aal,
    "aapl": aapl,
    "amat": amat,
    "amd": amd
}

closing_price = pd.DataFrame()

for name, df in dfs.items():
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    closing_price[f"{name}_close"] = df["close"]

fig5, ax = plt.subplots()
sns.heatmap(closing_price.corr(), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig5)


st.markdown('-------')
st.markdown('Done by SURABHI RAO')














