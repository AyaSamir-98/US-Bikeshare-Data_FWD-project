import time 
import pandas as pd 
import numpy as np

CITY_DATA={'chicago':'chicago.csv','new york city':'new_york_city.csv','washington':'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
	
    print('Hello! Let\'s explore some US bikeshare data!')
	
    # get user input for city (chicago, new york city, washington). and validate the input
    city = input("Choose a City from (chicago, new york, washington) ").lower()
    while city not in ['chicago', 'new york', 'washington']:
        city = input("kindly choose from (chicago, new york, washington)").lower()

    # get user input for month (all, january, february, ... , june) and validate the input
    month = input("Enter the desired month ").lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input("Kindly enter valid month ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday) and validate input
    day = input("Enter the desired day ").lower()
    while day not in ['all', 'saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
        day = input("Kindly enter a valid day ").lower()

    print('-'*40)
    return city, month, day


def load_data(city,month,day):
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time']=pd.to_datetime(df['Start Time'])
    df['month']=df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.weekday
    df['start hour']=df['Start Time'].dt.hour 
    
    if month!='all':
        months=['january','february','march','april','may','june','all']
        month=months.index(month)+1 #to start as jan is monthn 1
        df=df[df['month']==month]
        
    if day!='all':
        #filter by dayv of week to create the new dataframe
        df=df[df['day_of_week']==day.title()] # to be like the dataset typing 

    return df


def time_stats(df):
    # Display statistics on the most frequent times of travel
    print("\nCalculating the most frequent times of travel...")
    start_time = time.time()

    # Create a dictionary to map day numbers to day names
    day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

    # Calculate and display the most common month
    print('The most common month is: {}'.format(df['month'].mode()[0]))

    # Calculate and display the most common day of week
    most_common_day_number = df['day_of_week'].mode()[0]
    most_common_day_name = day_names[most_common_day_number]
    print('The most common day is: {}'.format(most_common_day_name))

    # Calculate and display the most common start hour
    print('The most common start hour is: {}'.format(df['start hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    #displays statistics on the most popular station and trip
    
    print("\n Calculating the most popular station and trip...\n")
    start_time=time.time()
    
    #display the most common used start station
    print("the most common start station is {}".format(df['Start Station'].mode()[0]))
    
    #display the most commonly used end station 
    print("the most common end station is {}".format(df['End Station'].mode()[0]))
    
    #display the most frequent route is combination of start station and end station
    df['route']=df['Start Station']+","+df['End Station']
    print("the most common route is {}".format(df['route'].mode()[0]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time in hours is: ", round((df['Trip Duration'].sum()) / 3600, 2))

    # display mean= (average) travel time
    print("The mean of travel time in hours is: ", round((df['Trip Duration'].mean()) / 3600, 2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    #display statistics on bikeshare users
    
    print("\n Calculation User Stats..\n")
    start_time=time.time()
    
    #DISPLAY COUNTS OF USERS 
    #use to frame because the col of user type is series so we need to convert it to work on it 
    print(df['User Type'].value_counts().to_frame())

    #display the count of gender 
    #note: wahington doesn't have gender info so we do the following 
    if city!= 'washington':
        print(df['Gender'].value_counts().to_frame())
        
        #display earliest,most recent, and most common year of birth
        print("the most common year of birthday is:",int(df['Birth Year'].mode()[0]))
        print("the most recent year of birthday is:",int(df['Birth Year'].max()))
        print("the earliest year of birthday is:",int(df['Birth Year'].min()))
        
    else:
        print("There is no data for this city ")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw_data(df):
    """ Displays the first 5 rows of selected data """
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?").lower()
    start_loc = 0
    while (view_data =="yes"):
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()
        
        
def main():
        while True:
            city, month, day = get_filters()
            df = load_data(city, month, day)
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df,city)
            raw_data(df)
            
            restart=input("\n Would you like to restart? Enter yes or no. \n")
            if restart.lower()!='yes':
                print("Thank you")
                break
if __name__ == "__main__":
    main()