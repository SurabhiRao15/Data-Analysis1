# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import plotly.express as px

company_list = [
    "data/AAL_data.csv",
    "data/AAPL_data.csv",
    "data/AMAT_data.csv",
    "data/AMD_data.csv"
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
company_df = company_df.sort_values('date')

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

company_df['date'] = pd.to_datetime(company_df['date'])
company_df = company_df.sort_values('date')
company_df_resample = company_df.set_index('date')

resample_option = st.radio('Select resample frequency', ['Monthly', "Quarterly","Yearly"])
if resample_option == "Monthly":
    resampled = company_df_resample['close'].resample('M').mean()
elif resample_option == "Quarterly":
    resampled = company_df_resample['close'].resample('Q').mean()
else:
    resampled = company_df_resample['close'].resample('Y').mean()

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
dfs = {}
for i, name in enumerate(["aal", "aapl", "amat", "amd"]):
    df = pd.read_csv(company_list[i])
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date').sort_index()
    dfs[name] = df

closing_price = pd.DataFrame()
for name, df in dfs.items():
    closing_price[f"{name}_close"] = df["close"]

fig5, ax = plt.subplots()
sns.heatmap(closing_price.corr(), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig5)



st.markdown('-------')
st.markdown('Data Analysis Project 1')















