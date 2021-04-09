import time
import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': '../files/chicago.csv',
              'New York': '../files/new_york_city.csv',
              'Washington': '../files/washington.csv' }

def get_filters(): # done
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze 
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=''
    month=''
    day=''
    
    # user is asked to type the first letter of the city. This will be checked if valid. If yes the variable city will be filled. 
    # a while loop is going to insure that the correct letters are entered
    while city=='':
        city_in= input("Which of the cities would you like to explore? Please type c for Chicago, n for New York City or w for Washington!\n")
       
        if city_in=='c':
            city= 'Chicago'
        elif city_in== 'n':
            city= 'New York'
        elif city_in== 'w':
            city= 'Washington'
            
        if city!='': # if a correct value was entered the loop can be left
            break
            
   
    # get user input for month (all, january, february, ... , june)
    #valid input for month names
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'all'] 
    while month=='':
        month_in= input("We have data from January to June. Which month would you like to see? You can also enter 'all' for the complete dataset\n")
        if month_in in months:
            month= month_in
            break
        else:
            print('Sorry, this is not a valid month input\n')


    # get user input for day of week (all, monday, tuesday, ... sunday)
    #valid input for days
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'all'] 
    while day=='':
        day_in= input("Are you interested in a special weekday? If yes, choose Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday. Print 'all' for the complete week\n")
        if day_in in days:
            day= day_in
            break
        else:
            print('Sorry, this is not a valid day input\n')

    print('-'*40)
    return city, month, day
    

def load_data(city, month, day): #done
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze, first character needs to be upper case
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #read data of parameter city
    #df = pd.read_csv(CITY_DATA[city], nrows=1000)
    df = pd.read_csv(CITY_DATA[city])
        
    #print(df.shape) 
    
    # Überarbeiten der Datei:
    # Start Time und End Time werden ins Format Datetime überführt
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # New columns for month, day and hour of Start time 
    df['month'] = df['Start Time'].dt.month
    df['month_name'] = df['Start Time'].dt.month_name()
    df['dayofweek'] = df['Start Time'].dt.dayofweek
    df['day_name'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    
    # now column line to calculate common connections
    df['line']= df['Start Station']+ ' to ' + df['End Station']
    
    
    # check if filtering of data concerning month and day are needed
    month_check= month!= 'all'
    day_check= day!= 'all'
        
    
    if month_check: # filter by month to create the new dataframe
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June'] 
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    
    if day_check:
        # filter by day to create the new dataframe      
        df = df[df['day_name'] == day]       

    return df




def time_stats(df): #done
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
 
    # display the most common month
    common_month = df['month_name'].mode()[0]
    print('Most common month:', common_month)


    # display the most common day of week
    common_day = df['day_name'].mode()[0]
    print('Most common day:', common_day)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most common hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df): #done
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most common start station:', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most common end station:', common_end_station)

    # display most frequent combination of start station and end station trip
    common_line = df['line'].mode()[0]
    print('Most common line:', common_line)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df): # done
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # transform travel time to minutes, as seconds are to huge for working with function timedelta
    total_travel_mins= (df['Trip Duration'].sum())/60
    total_travel_time= str(dt.timedelta(minutes=total_travel_mins))
    
    print('Total travel time:', total_travel_time)
    
    # total travel time in seconds
    # print('Total travel time: {} seconds'.format(df['Trip Duration'].sum()))

    # display mean travel time 
    mean_travel_time= df['Trip Duration'].mean()
    # convert time from seconds to better readable format
    mean_travel_time= str(dt.timedelta(seconds=mean_travel_time))
    print('Mean travel time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df): #done
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types= df['User Type'].value_counts()
    print('Rentals per user types:\n', user_types)


    # Display counts of gender
    # check first if gender is provided in the file
    if 'Gender' not in df:
        print('Gender not available in data source!')
    else:
        # get the count of rentals per gender
        gender= df['Gender'].value_counts()
        print('Rentals per gender:\n', gender)


    # Display earliest, most recent, and most common year of birth
    # check first if year of birth is provided in the file
    if 'Birth Year' not in df:
        print('Birth year not available in data source!')
    else:
        # earliest birth of year
        year_first= df['Birth Year'].min()
        print('Earliest birth year', year_first)
        
        # Most recent birth of year
        year_recent= df['Birth Year'].max()
        print('Most recent birth year', year_recent)
        
        # Most common birth of year
        year_common= df['Birth Year'].value_counts().idxmax()
        print('Most common birth year', year_common)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
                
        # print the summary of the user input        
        print('Perfect, let\'s explore the bike data of {}!'.format(city))
        if month!= 'all':            
                print('Month filter on {}!'.format(month))
        if day!= 'all':        
                print('Day filter on {}s!'.format(day))
        
        
        df = load_data(city, month, day)
        
        #print(df.head())
        #print(df.describe())

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
