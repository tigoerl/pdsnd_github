# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 20:58:07 2022

@author: TIGOERL
"""

import time
import calendar
import numpy as np
import pandas as pd

# Load Data from similar path as the python file
# Define Data Dictionary, to load Data only, when City is requested

City_Data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def Load_Data():
    """
    Script to load the Data and filter after city, month or day of week.
    Input will be done directly in function

    Parameters
    ----------
    

    Returns
    -------
    df - pandas DataFrame containing city data filtered by month and day of week.

    """
#%%  
    # load data file into a DataFrame and check if input is correct for calculation
    #check if data input (city) is fitting to expected values.
    
    while True: # repeat forever unless it reaches break or return
        print('Which city do you want to analyze? Options are Chicago, New York City and Washington.')
        print('Please write your city here:')
        # customer_city = 'chicago'
        customer_city = input().lower()
        print('-'*40)
        if customer_city in City_Data.keys():
            df = pd.DataFrame(pd.read_csv(City_Data[customer_city]))
            print('You choose: {}'.format(customer_city))
            break
        else:
            print('Sorry, your Input is wrong. Please try again.')
            continue # jumps back to the 'while True' line
    
    print('-'*40)
#%%    
    # convert the Start Time column and the End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    #check which month comes from costumer
    #aviod changing complete database and reduce database directly 
    months = list(calendar.month_name)
    # print(df.head())
  
    
    #check if data input (month) is fitting to the expected value.
    #filter for month
    
    while True: #repeates forever unless it reaches break or return
        print('\n Which month do you want to analyze? Write down the month as name. \n',
              ' If you want to analyze all months, write \'all\'.')
        # customer_month = 'All'
        customer_month = input().title()
        print('-'*40)
        if customer_month in df['month'].unique():
            for i in range(len(months)): #filter after customer month and reduce DataFrame to this month.
                if months[i] == customer_month:
                    # print(i)
                    df = df[df['month'] == customer_month]
                    df['month'] = df['month'].replace([customer_month], i)
            print('You choose: {}'.format(customer_month))
            break
        elif customer_month == 'All':
            print('You choose: {}'.format(customer_month))
            break
        else: 
            print('Sorry, your Input is wrong, or your selected Month is not part of the Databsase.',
                  ' Please try again.')
            continue # jumps back to the 'while True' line
    # print(df)
    print('-'*40)
#%%    
    #filter for day of week
    #check if data input (day of week) is fitting to the expected value.
    
    # print(df['day_of_week'].unique())
    
    while True:
        print('\n Which day of the week, do you want to analyze? Write down the day of week as name. \n',
              'If you want to analyze all months, write down \'all\'.')
        # customer_day = 'All'
        customer_day = input().title()
        print('-'*40)
        if customer_day in list(df['day_of_week'].unique()):
            df = df[df['day_of_week'] == customer_day]
            print('You choose: {}'.format(customer_day))
            break
        elif customer_day == 'All':
            print('You choose: {}'.format(customer_day))
            break
        else:
            print('Sorry, your Input is wrong. Please try again.\n')
            continue # jumps back to the 'while True' line
        #code optimization....
       
    print('-'*40)
#%%            
    return df, customer_city, customer_month, customer_day       
            

def stat_popular_time_travel(df, city, month, day):
    """
    create statistics for the time travel

    Parameters
    ----------
    df : DataFrame
        filtered DataFrane based on customer input
    city : string
        customer input for city filter
    month : string
        customer input for month filter
    day : string
        customer input for day of week filter.

    Returns
    -------
    None.

    """
#%%
    # calculation of most popular hour
    print('Calculating the first statistics...')
    start_time = time.time()
    #create a line in DataFrame for the hour, which is most common
    df['hour'] = df['Start Time'].dt.hour
    
    #create a DataFrame with the hour and counts ordered from Max to Min
    hour_stats = df['hour'].value_counts().rename_axis('hour').reset_index(name='counts')
    most_used_hour = hour_stats.iloc[0,0]
    count_most_used_hour = hour_stats.iloc[0,1]
    start_time = time.time() #timing for the statistics
    
    print(' The most popular hour, where the bike has been rented out',
          ' based on the selection is: {}'.format(most_used_hour))
    print('with a count of {} rentals.'.format(count_most_used_hour))
    
    
    
    #calculating the most common day of week
    
    print('-'*40)
    #create a DataFrame with the day of week and counts ordered from Max to Min
    if day == 'All':
        day_of_week_stats = df['day_of_week'].value_counts().rename_axis('day_of_week').reset_index(name='counts')
        # print(day_of_week_stats)
        most_day_of_week = day_of_week_stats.iloc[0,0]
        count_most_day_of_week = day_of_week_stats.iloc[0,1]
        print('The most popular day of the week, where the bike has been rented out',
              'is: {}'.format(most_day_of_week))
        print('with a count of {} rentals at that day.'.format(count_most_day_of_week))
        print('-'*40)
    
    #create a DataFrame with the month and counts ordered from Max to Min
    if month == 'All':
        month_stats = df['month'].value_counts().rename_axis('month').reset_index(name='counts')
        most_used_month = month_stats.iloc[0,0]
        count_most_used_month = month_stats.iloc[0,1]
        print('The most popular month, where the bike has been rented out',
              'is: {}'.format(most_used_month))
        print('with a count of {} rentals at that month.'.format(count_most_used_month))
        print('-'*40)
        
    #timing for the statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
#%%    
def stats_popular_station_trip(df, city, month, day):
    """
    create statistic for station start end

    Parameters
    ----------
    df : DataFrame
        filtered DataFrane based on customer input
    city : string
        customer input for city filter
    month : string
        customer input for month filter
    day : string
        customer input for day of week filter.

    Returns
    -------
    None.

    """
    
    # print(df.columns)
    start_time = time.time()
    #calculate the most common start station
    start_station_stats = df['Start Station'].value_counts().rename_axis('Start Station').reset_index(name='counts')
    # print(start_station_stats)
    most_start_station = start_station_stats.iloc[0,0]
    count_most_start_station = start_station_stats.iloc[0,1]
    print('The most popular Station, where the bike has been rented out',
          'is: {}'.format(most_start_station))
    print('with a count of {} rentals at that Station.'.format(count_most_start_station))
    print('-'*40)
    
    #calculate the most common End Station
    end_station_stats = df['End Station'].value_counts().rename_axis('End Station').reset_index(name='counts')
    # print(end_station_stats)
    most_end_station = end_station_stats.iloc[0,0]
    count_most_end_station = end_station_stats.iloc[0,1]
    print('The most popular Station, where the bike has been given back',
          'is: {}'.format(most_end_station))
    print('with a count of {} returns at that Station.'.format(count_most_end_station))
    print('-'*40)
    
    #calculate the most frequently used rental combination
    df['trip'] = df['Start Station'] + ' - ' + df['End Station']
    trip_stats = df['trip'].value_counts().rename_axis('trip').reset_index(name='counts')
    most_trips = trip_stats.iloc[0,0]
    count_most_trips = trip_stats.iloc[0,1]
    print('The most popular Trip, where the bike has been rented out',
          'is: {}'.format(most_trips))
    print('with a count of {} trips.'.format(count_most_trips))
    
    
    #timing for the statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#%%
def stats_trip_duration(df, city, month, day):
    """
    create statistic for travel time and average travel time

    Parameters
    ----------
    df : DataFrame
        filtered DataFrane based on customer input
    city : string
        customer input for city filter
    month : string
        customer input for month filter
    day : string
        customer input for day of week filter.

    Returns
    -------
    None.

    """
    # print(df.columns)
    start_time = time.time()
    #calculate total trip duration in seconds
    total_trip_duration = df['Trip Duration'].sum()
    average_trip_duration = df['Trip Duration'].mean()
    print('The total trip duration is {} seconds.'.format(total_trip_duration))
    print('The average trip duration is: {} seconds.'.format(average_trip_duration))
    
    #timing for the statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def stats_user(df, city, month, day):
    """
    calculating User Stats

    Parameters
    ----------
    df : DataFrame
        filtered DataFrane based on customer input
    city : string
        customer input for city filter
    month : string
        customer input for month filter
    day : string
        customer input for day of week filter.

    Returns
    -------
    None.

    """
    
    # print(df.columns)
    start_time = time.time()
    
    # print(df.head())
    # print(df.columns)
    # calculate number of each user type
    user_type_stats = df['User Type'].value_counts().rename_axis('User Type').reset_index(name='counts')
    
    # print(len(user_type_stats.index))
    print('The User Type has the following statistic:')
    for i in range(len(user_type_stats.index)):
        print('User Type: {}, count: {}'.format(user_type_stats.iloc[i,0],user_type_stats.iloc[i,1]))
    
    #count for each gender
    
    # print(df['Gender'])
    
    if 'Gender' in df.columns:
        gender_stats = df['Gender'].value_counts().rename_axis('Gender').reset_index(name='counts')
        print('The Gender Row has the following statistic:')
        for i in range(len(gender_stats.index)):
            print('Gender: {}, count: {}'.format(gender_stats.iloc[i,0], gender_stats.iloc[i,1]))
        
    #timing for the statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#%%
def main():
    """
    main environment to execute. 
    Returns
    -------
    None.

    """
    print('Hello! Welcome to the bikeshop database. Let\'s explore some data. \n', 
          'You you have different options to investigate your data. In the first place you can filter via \n',
          '- city \n',
          '- month \n',
          '- day \n'
          'and have fun with the analysis which will be provided.')
    print('-'*40)
    output_from_LD = Load_Data()
    df = output_from_LD[0]
    customer_city = output_from_LD[1]
    customer_month = output_from_LD[2]
    customer_day = output_from_LD[3]
    stat_popular_time_travel(df, customer_city, customer_month, customer_day)
    stats_popular_station_trip(df, customer_city, customer_month, customer_day)
    stats_trip_duration(df, customer_city, customer_month, customer_day)
    stats_user(df, customer_city, customer_month, customer_day)
    # print('The complete Data-Frame looks like:')
    # print(df.head())
    print('Do you want to restart the program?')
    restart_answer = input().lower()
    if restart_answer == 'yes' or restart_answer == 'y':
        print('-'*40)
        main()
    
    
    
    
main()
