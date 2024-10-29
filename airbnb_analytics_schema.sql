IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = 'airbnb_analytics')
BEGIN
	CREATE DATABASE airbnb_analytics;
END
GO

USE airbnb_analytics;
GO

DROP TABLE IF EXISTS _tb_ref_hosts;
GO

CREATE TABLE _tb_ref_hosts (
	 id									INT IDENTITY(1,1) NOT NULL
	,refresh_date						DATETIME DEFAULT GETDATE()
	,host_id							BIGINT NOT NULL
	,host_name							NVARCHAR(200)
	,host_since							DATE
	,host_location						NVARCHAR(200)
	,host_response_time					NVARCHAR(50)
	,host_response_rate					NVARCHAR(4)
	,host_acceptance_rate				NVARCHAR(4)
	,host_is_superhost					NVARCHAR(1)
	,host_has_profile_pic				NVARCHAR(1)
	,host_identity_verified				NVARCHAR(1)
)
GO 

DROP TABLE IF EXISTS _tb_dim_listings;
GO
CREATE TABLE _tb_dim_listings (
	 listing_id							BIGINT IDENTITY(1,1)
	,refresh_date						DATETIME DEFAULT GETDATE()
	,id									BIGINT UNIQUE NOT NULL
	,name								NVARCHAR(500)
	,host_id							BIGINT
	,neighbourhood						NVARCHAR(200)	
	,neighbourhood_cleansed				NVARCHAR(30)
	,latitude							DECIMAL(16,6)
	,longitude							DECIMAL(16,6)
	,property_type						NVARCHAR(200)
	,room_type							NVARCHAR(200)
	,accommodates						DECIMAL(16,6)
	,bathrooms							DECIMAL(16,6)
	,bedrooms							DECIMAL(16,6)
	,beds								DECIMAL(16,6)
	,price								DECIMAL(16,6)
	,minimum_nights						DECIMAL(16,6)
	,maximum_nights						DECIMAL(16,6)
	,minimum_minimum_nights				DECIMAL(16,6)
	,maximum_minimum_nights				DECIMAL(16,6)
	,minimum_maximum_nights				DECIMAL(16,6)
	,maximum_maximum_nights				DECIMAL(16,6)
	,minimum_nights_avg_ntm				DECIMAL(16,6)
	,maximum_nights_avg_ntm				DECIMAL(16,6)
	,number_of_reviews					DECIMAL(16,6)
	,number_of_reviews_ltm				DECIMAL(16,6)
	,number_of_reviews_l30d				DECIMAL(16,6)
	,first_review						DATE
	,last_review						DATE
	,review_scores_rating				DECIMAL(16,6)
	,review_scores_accuracy				DECIMAL(16,6)
	,review_scores_cleanliness			DECIMAL(16,6)
	,review_scores_checkin				DECIMAL(16,6)
	,review_scores_communication		DECIMAL(16,6)
	,review_scores_location				DECIMAL(16,6)
	,review_scores_value				DECIMAL(16,6)
	,instant_bookable					NVARCHAR(1)
	,reviews_per_month					DECIMAL(16,6)
)
GO

DROP TABLE IF EXISTS _tb_dim_reviews;
GO

CREATE TABLE _tb_dim_reviews (
	 reviews_id							BIGINT IDENTITY(1,1)
	,refresh_date						DATETIME DEFAULT GETDATE()
	,id									BIGINT UNIQUE
	,reviewer_id						BIGINT
	,listing_id							BIGINT
	,date								DATE
	,reviewer_name						NVARCHAR(100)
	,comments							NVARCHAR(MAX)
)
GO

DROP TABLE IF EXISTS _tb_dim_calendar;
GO
CREATE TABLE _tb_dim_calendar (
	 calendar_id						BIGINT IDENTITY(1,1) PRIMARY KEY
	,refresh_date						DATETIME DEFAULT GETDATE()
	,listing_id							BIGINT
	,date								DATE
	,available							BIT
	,price								DECIMAL(16,6)
	,minimum_nights						INT
	,maximum_nights						INT
)
GO

DROP TABLE IF EXISTS _tb_dim_weather;
GO

CREATE TABLE _tb_dim_weather (
	 id									BIGINT IDENTITY(1,1)
	,refresh_date						DATETIME DEFAULT GETDATE()
	,dt									NVARCHAR(50)
	,dt_iso								DATETIME
	,timezone							NVARCHAR(50)
	,city_name							NVARCHAR(200)
	,temp 								DECIMAL(16,6)
	,visibility							DECIMAL(16,6)
	,feels_like							DECIMAL(16,6)
	,temp_min							DECIMAL(16,6)
	,temp_max							DECIMAL(16,6)
	,pressure							DECIMAL(16,6)
	,humidity							DECIMAL(16,6)
	,wind_speed							DECIMAL(16,6)
	,wind_deg							DECIMAL(16,6)
	,clouds_all							DECIMAL(16,6)
	,weather_id							DECIMAL(16,6)
	,weather_main						NVARCHAR(50)
	,weather_description				NVARCHAR(50)
)
GO
