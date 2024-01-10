import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = { 'january': 1,
           'february': 2,
           'march': 3,
           'april': 4,
           'may': 5,
           'june': 6,
           'all': 'all'}

MONTH_LOOKUP = { 1: 'January',
           2: 'February',
           3: 'March',
           4: 'April',
           5: 'May',
           6: 'June'}

day_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('What city would you like to choose: Chicago, New York City, or Washington? ').lower()
    while city not in CITY_DATA:
        print('I am sorry. Please enter one of the selections listed.')
        city = input('What city would you like to choose: Chicago, New York City, or Washington? ').lower()
    else:
        print('Thank you for your selection.')

    # get user input for month (all, january, february, ... , june)
    month_selection = input('Please select a month between January and June or select all for all months:').lower()
    while month_selection not in MONTHS:
        print('I am sorry. You entered an invalid selection.')
        month_selection = input('Please select a month between January and June or select all for all months:').lower()
    else:
        month = MONTHS.get(month_selection)
        print('Thank you for your selection.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please select a day of the week or select all to get all data: ').lower()
    while day not in day_of_week:
        print('I am sorry. You entered an invalid selection.')
        day = input('Please select a day of the week or select all to get all data: ').lower()
    else:
        print('Thank you for your selection.')

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (int, str) month - number of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #load data file into a dataframe
    df = pd.read_csv(CITY_DATA.get(city), encoding='unicode_escape')

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #extract hour from Start Time to create new columns
    df['hour'] = df['Start Time'].dt.hour
    #filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = MONTH_LOOKUP[df['month'].mode()[0]]

    print("The most common month is {}.".format(common_month))

    # display the most common day of week
    common_dow = df['day_of_week'].mode()[0]
    print("The most common day of the week is {}.".format(common_dow))

    # display the most common start hour
    start_hour = df['hour'].mode()[0]
    if start_hour <= 12:
        common_hour = str(start_hour) + 'AM'
    else:
        start_hour = start_hour - 12
        common_hour = str(start_hour) + 'PM'
    print('The most common start hour is {}.'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('The most common start station is {}.'.format(common_start))

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('The most common end station is {}.'.format(common_end))

    # display most frequent combination of start station and end station trip
    df['combined'] = df['Start Station'] + ' ending at ' + df['End Station']
    trip = df['combined'].mode()[0]
    print('The most common trip started at {}.'.format(trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tt = df['Trip Duration']

    print('The total trip duration is {}.'.format(tt))

    # display mean travel time
    mean = df['Trip Duration'].mean()
    print('The average trip time is {}.'.format(mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_stats = df['User Type'].value_counts()
    print('\nCounts of types of users:')
    print(user_stats.to_string())

    # Display counts of gender
    #add try statement to handle missing data fields
    try:
        gender = df['Gender'].value_counts()
        print('\nCounts of males and females using the service:')
        print(gender.to_string())
    except:
        print('\nNo gender data to display.')

    # Display earliest, most recent, and most common year of birth
    #add try statement to handle missing data fields
    try:
        old = df['Birth Year'].min()
        young = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()
        print('\nThe earliest birth year is {}.'.format(int(old)))
        print('\nThe most recent birth year is {}.'.format(int(young)))
        print('\nThe most common birth year is {}.'.format(int(most_common)))
    except:
        print('\nNo birth data to display.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw(df):
    """Displays raw data for the user 5 lines at a time if requested."""
    #collect user input on if they want to see the raw data
    response = input("\nWould you like to see the raw data? Y/N ").lower()

    #initialize the iterable for the index
    i = 0

    #set the if statement to process the loop if they want to see the data
    if response == 'y':
        while i <= len(df):
            print(df.iloc[0:(i+5)])
            i += 5

            #ask if the user wants to see more data
            more = input("\nWould you like to see more data?").lower()
            if more != 'y':
                print('\nGoodbye!')
                break
    else:
        print("\nGoodbye!")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
