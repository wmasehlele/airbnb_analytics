import requests
import traceback
import pandas as pd
from sqlalchemy import create_engine, text

pd.set_option('future.no_silent_downcasting', True)

def db_connection ():
    try:
        engine = create_engine(f'mssql+pyodbc://ZAJNBCONMAMOELA/airbnb_analytics?trusted_connection=yes&driver=ODBC Driver 17 for SQL Server')
        return engine
    except:
        print('Error connecting to sql server')

def city_lat_and_lon (postal_code = 8000, country_code = 'ZA'):
    # get the longitude and latitude for the city
    end_point = BASE_URL + '/geo/1.0/zip?zip='+str(postal_code)+','+country_code+'&appid='+API_KEY
    return requests.get(end_point).json()

def load_airbnb_listingsdata ():
    db_conn = db_connection()
    columns_listings = ['id','name','host_id','neighbourhood','neighbourhood_cleansed','latitude','longitude','property_type','room_type','accommodates','bathrooms','bedrooms','beds','price','minimum_nights','maximum_nights','minimum_minimum_nights','maximum_minimum_nights','minimum_maximum_nights','maximum_maximum_nights','minimum_nights_avg_ntm','maximum_nights_avg_ntm','number_of_reviews','number_of_reviews_ltm','number_of_reviews_l30d','first_review','last_review','review_scores_rating','review_scores_accuracy','review_scores_cleanliness','review_scores_checkin','review_scores_communication','review_scores_location','review_scores_value','instant_bookable','reviews_per_month']
    columns_hosts = ['host_id','host_name','host_since','host_location','host_response_time','host_response_rate','host_acceptance_rate','host_is_superhost','host_has_profile_pic','host_identity_verified']
    try:
        data_load = pd.read_csv('data/listings.csv', encoding='utf8', dtype='object', low_memory=False)

        listings = pd.DataFrame(data_load[columns_listings])
        listings['first_review'] = pd.to_datetime(listings['first_review'])
        listings['last_review'] = pd.to_datetime(listings['last_review'])    
        listings['instant_bookable'] = listings['instant_bookable'].replace(['t','f'],[True,False])
        listings['price'] = listings['price'].replace({'\\$': '', ',': ''}, regex=True)
        listings['price'] = pd.to_numeric(listings['price'])
        listings['latitude'] = pd.to_numeric(listings['latitude'])
        listings['longitude'] = pd.to_numeric(listings['longitude'])
        listings['latitude'] = pd.to_numeric(listings['latitude'])
        listings['longitude'] = pd.to_numeric(listings['longitude'])

        # clean the table before loading new data
        if len(listings) > 0:
            with db_conn.connect() as conn:
                conn.execute(text('TRUNCATE TABLE _tb_dim_listings'))   

        # dump the data into the sql table        
        listings.to_sql('_tb_dim_listings', db_conn, if_exists='append', index=False) 
        print('Done: 1. listings data to sql server')              

        hosts = pd.DataFrame(data_load[columns_hosts])
        hosts['host_since'] = pd.to_datetime(hosts['host_since'])
        hosts['host_is_superhost'] = hosts['host_is_superhost'].replace(['t','f'],[True,False])
        hosts['host_has_profile_pic'] = hosts['host_has_profile_pic'].replace(['t','f'],[True,False])
        hosts['host_identity_verified'] = hosts['host_identity_verified'].replace(['t','f'],[True,False])
        hosts['host_response_time'] = hosts['host_response_time'].replace({'N/A':'NULL'}, regex=True)
        hosts['host_response_rate'] = hosts['host_response_rate'].replace({'%':'', 'N/A':'NULL'}, regex=True)
        hosts['host_acceptance_rate'] = hosts['host_acceptance_rate'].replace({'%':'', 'N/A':'NULL'}, regex=True)
        hosts['host_response_rate'] = pd.to_numeric(hosts['host_response_rate'])
        hosts['host_acceptance_rate'] = pd.to_numeric(hosts['host_acceptance_rate'])    

        # clean the table before loading new data
        if len(hosts) > 0:
            with db_conn.connect() as conn:
                conn.execute(text('TRUNCATE TABLE _tb_ref_hosts'))

        # dump the data into the sql table        
        hosts.to_sql('_tb_ref_hosts', db_conn, if_exists='append', index=False)
        print('Done: 2. hosts data to sql server')  
    except:
        traceback.print_exc()
        print('Error occured while loading airbnb listings data to sql server')

def load_airbnb_reviewsdata ():
    db_conn = db_connection()
    columns_reviews = ['listing_id','id','date','reviewer_id','reviewer_name','comments']
    try:
        data_load = pd.read_csv('data/reviews.csv', encoding='utf8', dtype='object', low_memory=False)
        reviews = pd.DataFrame(data_load[columns_reviews])

        # clean the table before loading new data
        if len(reviews) > 0:
            with db_conn.connect() as conn:
                conn.execute(text('TRUNCATE TABLE _tb_dim_reviews'))

        # dump the data into the sql table        
        reviews.to_sql('_tb_dim_reviews', db_conn, if_exists='append', index=False)
        print('Done: 3. reviews data to sql server')  
    except:
        traceback.print_exc()
        print('Error occured while loading airbnb reviews data to sql server')

def load_airbnb_calendardata ():
    db_conn = db_connection()
    columns_reviews = ['listing_id','date','available', 'price', 'minimum_nights', 'maximum_nights']
    try:
        data_load = pd.read_csv('data/calendar.csv', encoding='utf8', dtype='object', low_memory=False)
        calendar = pd.DataFrame(data_load[columns_reviews])
        calendar['available'] = calendar['available'].replace(['t','f'],[True,False])
        calendar['price'] = calendar['price'].replace({'\\$': '', ',': ''}, regex=True)
        calendar['price'] = pd.to_numeric(calendar['price'])
        calendar['minimum_nights'] = pd.to_numeric(calendar['minimum_nights'])
        calendar['maximum_nights'] = pd.to_numeric(calendar['maximum_nights'])

        # clean the table before loading new data
        if len(calendar) > 0:
            with db_conn.connect() as conn:
                conn.execute(text('TRUNCATE TABLE _tb_dim_calendar'))

        # dump the data into the sql table        
        calendar.to_sql('_tb_dim_calendar', db_conn, if_exists='append', index=False)   
        print('Done: 4. calendar data to sql server')  
    except:
        traceback.print_exc()
        print('Error occured while loading airbnb calendar data to sql server')     

def load_capetown_historic_meteorologicaldata ():
    db_conn = db_connection()
    columns_weather = ['dt','dt_iso','timezone','city_name','temp','visibility','feels_like','temp_min','temp_max','pressure','humidity','wind_speed','wind_deg','clouds_all','weather_id','weather_main','weather_description']
    try:
        data_load = pd.read_csv('data/cape_town.csv', encoding='utf8', dtype='object', low_memory=False)
        weather = pd.DataFrame(data_load[columns_weather])    
        weather['dt_iso'] = weather['dt_iso'].str[:-10]  
        weather['dt_iso'] = pd.to_datetime(weather['dt_iso'])
        # clean the table before loading new data
        if len(weather) > 0:
            with db_conn.connect() as conn:
                conn.execute(text('TRUNCATE TABLE _tb_dim_weather'))

        # dump the data into the sql table        
        weather.to_sql('_tb_dim_weather', db_conn, if_exists='append', index=False)   
        print('Done: 5. weather data to sql server') 
    except:
        traceback.print_exc()
        print('Error occured while loading airbnb weather data to sql server')     

def main():
    load_airbnb_listingsdata ()
    load_airbnb_reviewsdata ()
    load_airbnb_calendardata ()
    load_capetown_historic_meteorologicaldata ()

if __name__ == '__main__':
    main()