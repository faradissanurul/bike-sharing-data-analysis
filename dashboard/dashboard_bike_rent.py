import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style="white")

def create_monthly_bike_rent_df(df):
    monthly_bike_rent_df = df.resample(rule='ME', on='dteday').cnt_x.sum()

    monthly_bike_rent_df.index = monthly_bike_rent_df.index.strftime('%Y/%m')
    monthly_bike_rent_df = monthly_bike_rent_df.reset_index()
    monthly_bike_rent_df.rename(columns={
        "cnt_x": "total_user"
    }, inplace=True)

    return monthly_bike_rent_df

def create_monthly_casual_bike_rent_df(df):
    monthly_casual_bike_rent_df = df.resample(rule='ME', on='dteday').casual_x.sum()

    monthly_casual_bike_rent_df.index = monthly_casual_bike_rent_df.index.strftime('%Y/%m')
    monthly_casual_bike_rent_df = monthly_casual_bike_rent_df.reset_index()
    monthly_casual_bike_rent_df.rename(columns={
        "casual_x": "total_casual_user"
    }, inplace=True)

    return monthly_casual_bike_rent_df

def create_monthly_registered_bike_rent_df(df):
    monthly_registered_bike_rent_df = df.resample(rule='ME', on='dteday').registered_x.sum()

    monthly_registered_bike_rent_df.index = monthly_registered_bike_rent_df.index.strftime('%Y/%m')
    monthly_registered_bike_rent_df = monthly_registered_bike_rent_df.reset_index()
    monthly_registered_bike_rent_df.rename(columns={
        "registered_x": "total_registered_user"
    }, inplace=True)

    return monthly_registered_bike_rent_df

def create_season_df(df):
    season_df = df.groupby(by='c_season').cnt_x.sum().sort_values(ascending=False).reset_index()
    season_df.rename(columns={
        "cnt_x": "total_user"
    }, inplace=True)

    return season_df

def create_month_df(df):
    month_df = df.groupby(by='month').cnt_x.sum().sort_values(ascending=False).reset_index()
    month_df.rename(columns={
        "cnt_x": "total_user"
    }, inplace=True)

    return month_df

def create_weekday_df(df):
    weekday_df = df.groupby(by='day').cnt_x.sum().sort_values(ascending=False).reset_index()
    weekday_df.rename(columns={
        "cnt_x": "total_user"
    }, inplace=True)

    return weekday_df

def create_year_df(df):
    year_df = df.groupby(by='year').cnt_x.sum().reset_index()
    year_df.rename(columns={
        "cnt_x": "total_user"
    }, inplace=True)

    return year_df

def create_year_type_user_df(df):
    year_type_user_df = df.groupby(by='year').agg({
        "casual_x": "sum",
        "registered_x": "sum"
    }).reset_index()

    year_type_user_df.rename(columns={
        "casual_x": "total_casual_user",
        "registered_x": "total_registered_user"
    }, inplace=True)

    return year_type_user_df

def create_peak_hour_workingday_df(df):
    peak_hour_df = df.groupby(by=['workingday_x', 'hr']).cnt_x.sum().sort_values(ascending=False).reset_index()

    workingday_data = peak_hour_df[peak_hour_df['workingday_x'] == 1]
    grouped_data_df = workingday_data.groupby('hr')['cnt_x'].sum().reset_index()

    top_3_hours = grouped_data_df.nlargest(3, 'cnt_x')['hr'].tolist()

    colors = ['#FF6F61' if hr in top_3_hours else '#72BCD4' for hr in grouped_data_df['hr']]

    return grouped_data_df, colors

def create_peak_hour_nonworkingday_df(df):
    peak_hour_df = df.groupby(by=['workingday_x', 'hr']).cnt_x.sum().sort_values(ascending=False).reset_index()

    nonworkingday_data = peak_hour_df[peak_hour_df['workingday_x'] == 0]
    ngrouped_data_df = nonworkingday_data.groupby('hr')['cnt_x'].sum().reset_index()

    top_3_hours = ngrouped_data_df.nlargest(3, 'cnt_x')['hr'].tolist()

    colors = ['#FF6F61' if hr in top_3_hours else '#4C7C9B' for hr in ngrouped_data_df['hr']]

    return ngrouped_data_df, colors


all_df = pd.read_csv("all_data.csv")

all_df.sort_values(by='dteday', inplace=True)
all_df.reset_index(inplace=True)
all_df['dteday'] = pd.to_datetime(all_df['dteday'])


min_date = all_df['dteday'].min()
max_date = all_df['dteday'].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df['dteday'] >= str(start_date)) &
                  (all_df['dteday'] <= str(end_date))]

monthly_bike_rent_df = create_monthly_bike_rent_df(main_df)
monthly_casual_bike_rent_df = create_monthly_casual_bike_rent_df(main_df)
monthly_registered_bike_rent_df = create_monthly_registered_bike_rent_df(main_df)
season_df = create_season_df(main_df)
month_df= create_month_df(main_df)
weekday_df = create_weekday_df(main_df)
year_df = create_year_df(main_df)
year_type_user_df = create_year_type_user_df(main_df)
peak_hour_workingday_df, colors_w = create_peak_hour_workingday_df(main_df)
peak_hour_nonworkingday_df, colors_n = create_peak_hour_nonworkingday_df(main_df)

st.header('Analisis Bike Sharing Dataset :bike:')
st.write('By Faradissa Nurul')

st.subheader('Monthly Bike Rent')
col1, col2, col3 = st.columns(3)

with col1:
    total_user = monthly_bike_rent_df.total_user.sum()
    st.metric("Total Bike Rent User", value=total_user)

with col2:
    total_casual_user = monthly_casual_bike_rent_df.total_casual_user.sum()
    st.metric("Total Casual User", value=total_casual_user)

with col3:
    total_registered_user = monthly_registered_bike_rent_df.total_registered_user.sum()
    st.metric("Total Registered User", value=total_registered_user)

fig, ax = plt.subplots(figsize=(30, 10))
ax.plot(monthly_bike_rent_df['dteday'],
        monthly_bike_rent_df['total_user'],
        marker='o',
        linewidth=2,
        color="#72BCD4")
ax.set_title("Total Bike Rent User per Month", loc="center", fontsize=30)
ax.tick_params('x', labelsize=15)
ax.tick_params('y', labelsize=15)

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(30, 10))
ax.plot(monthly_casual_bike_rent_df['dteday'],
        monthly_casual_bike_rent_df['total_casual_user'],
        marker='o', 
        linewidth=2, 
        color="#72BCD4",
        label="Casual")
ax.plot(monthly_registered_bike_rent_df['dteday'], 
        monthly_registered_bike_rent_df['total_registered_user'],
        marker='o', 
        linewidth=2, 
        color="#4C7C9B",
        label="Registered")
ax.set_title("Total Casual & Registered User per Month", loc="center", fontsize=30)
ax.tick_params('x', labelsize=15)
ax.tick_params('y', labelsize=15)
ax.legend()

st.pyplot(fig)

st.subheader("High and Low on Demand based on Season")

fig, ax = plt.subplots(figsize=(15, 7))

colors = ["#005B96", "#ffd092", "#ffd092", "#005B96"]

sns.barplot(x=season_df['c_season'],
            y= season_df['total_user'],
            data=season_df,
            palette=colors)
ax.set_title("Total Bike Rent Based on Season", loc="center", fontsize=30)
ax.set_xlabel("Season", fontsize=15)
ax.set_ylabel("Total User (Million)", fontsize=15)
ax.tick_params('x', labelsize=15)
ax.tick_params('y', labelsize=15)

st.pyplot(fig)

st.subheader("High and Low on Demand based on Month")

fig, ax = plt.subplots(figsize=(15, 7))
colors = ["#005B96", "#ffd092", "#ffd092", "#ffd092", "#ffd092", "#ffd092", "#ffd092", "#ffd092", "#ffd092", "#ffd092", "#ffd092", "#005B96"]

sns.barplot(y=month_df['month'],
            x= month_df['total_user'],
            data=month_df,
            palette=colors)
ax.set_title("Total Bike Rent Based on Month", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel("Total User", fontsize=15)
ax.tick_params('x', labelsize=15)
ax.tick_params('y', labelsize=15)

st.pyplot(fig)

st.subheader("High and Low on Demand based on Weekday")

fig, ax = plt.subplots(figsize=(15, 7))
colors = ["#005B96", "#ffd092", "#ffd092", "#ffd092", "#ffd092", "#ffd092", "#005B96"]

sns.barplot(y=weekday_df['day'],
            x= weekday_df['total_user'],
            data=weekday_df,
            palette=colors)
ax.set_title("Total Bike Rent Based on Weekday", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel("Total User", fontsize=15)
ax.tick_params('x', labelsize=15)
ax.tick_params('y', labelsize=15)

st.pyplot(fig)

st.subheader("Total Bike Rent per Year")

fig, ax = plt.subplots(figsize=(15, 7))

sns.barplot(x=year_df['year'],
            y= year_df['total_user'],
            data=year_df,
            color="#72BCD4")
ax.bar_label(ax.containers[0], fmt='%.0f')
ax.set_title("Total Bike Rent per Year", loc="center", fontsize=30)
ax.set_xlabel("Year", fontsize=15)
ax.set_ylabel("Total User (Million)", fontsize=15)
ax.tick_params('x', labelsize=15)
ax.tick_params('y', labelsize=15)

st.pyplot(fig)

st.subheader("Total Casual & Registered User per Year")

x =  np.arange(len(year_type_user_df['year']))
width = 0.35

fig, ax = plt.subplots(figsize=(15, 7))

casual_bar = ax.bar(x + width/2, year_type_user_df['total_casual_user'], width, label="Casual", color="#72BCD4")
registered_bar = ax.bar(x - width/2, year_type_user_df['total_registered_user'], width, label="Registered", color="#4C7C9B")
ax.bar_label(casual_bar, fmt='%.0f')
ax.bar_label(registered_bar, fmt='%.0f')
ax.set_title("Total Casual & Registered User per Year", loc="center", fontsize=30)
ax.set_xlabel("Year", fontsize=15)
ax.set_ylabel("Total User (Million)", fontsize=15)
ax.tick_params('x', labelsize=15)
ax.tick_params('y', labelsize=15)
ax.set_xticks(x)
ax.set_xticklabels(year_type_user_df['year'])
ax.legend()

st.pyplot(fig)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(30, 10))

sns.barplot(x=year_type_user_df['year'],
            y=year_type_user_df['total_casual_user'],
            data=year_type_user_df,
            color="#72BCD4",
            ax=ax[0]
            )
ax[0].bar_label(ax[0].containers[0], fmt='%.0f')
ax[0].set_title("Total Casual User per Year", loc="center", fontsize=30)
ax[0].set_xlabel("Year", fontsize=15)
ax[0].set_ylabel("Total User (Million)", fontsize=15)
ax[0].tick_params('x', labelsize=15)
ax[0].tick_params('y', labelsize=15)

sns.barplot(x=year_type_user_df['year'],
            y=year_type_user_df['total_registered_user'],
            data=year_type_user_df,
            color="#4C7C9B",
            ax=ax[1]
            )
ax[1].bar_label(ax[1].containers[0], fmt='%.0f')
ax[1].set_title("Total Registered User per Year", loc="center", fontsize=30)
ax[1].set_xlabel("Year", fontsize=15)
ax[1].set_ylabel("Total User (Million)", fontsize=15)
ax[1].tick_params('x', labelsize=15)
ax[1].tick_params('y', labelsize=15)

st.pyplot(fig)

st.subheader("Peak Hours Based on Workingday & Non-Workingday")
st.write("on Working Day")

fig, ax = plt.subplots(figsize=(30, 15))

sns.barplot(x=peak_hour_workingday_df['hr'],
            y=peak_hour_workingday_df['cnt_x'],
            palette= colors_w
            )
ax.set_title("Bike Rental by Hour on Working Day", loc="center", fontsize=30)
ax.tick_params('x', labelsize=15)
ax.tick_params('y', labelsize=15)
ax.set_ylabel("Total User", fontsize=15)
ax.set_xlabel("Hour of The Day")

st.pyplot(fig)

st.write("on Non-Working Day")

fig, ax = plt.subplots(figsize=(30, 15))

sns.barplot(x=peak_hour_nonworkingday_df['hr'],
            y=peak_hour_nonworkingday_df['cnt_x'],
            palette= colors_n
            )
ax.set_title("Bike Rental by Hour on Non-Working Day", loc="center", fontsize=30)
ax.tick_params('x', labelsize=15)
ax.tick_params('y', labelsize=15)
ax.set_ylabel("Total User", fontsize=15)
ax.set_xlabel("Hour of The Day")

st.pyplot(fig)