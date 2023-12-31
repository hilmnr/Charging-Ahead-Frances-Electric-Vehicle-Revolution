# Charging Ahead
France's Electric Vehicle Revolution 🔋

![Alt text](https://github.com/hilmnr/Charging-Ahead-Frances-Electric-Vehicle-Revolution/assets/145452309/b0e3068a-fd01-40f9-bbad-22ba92928917)

## Project Description 
Electric vehicles (EVs) are becoming increasingly important as more people look for ways to help the environment and cut down on pollution. They're leading the change by providing a cleaner way to travel that doesn't rely on more polluting energy like gasoline. EVs are here to stay; they're a key element in moving us towards a future where we can breathe easier and the planet is healthier. Additionally, with technological advancements, EVs are becoming more accessible and efficient, offering longer ranges and shorter charging times.

The main goal of this project is to look into two big questions about EVs in France. First, we want to understand how French consumers are reacting to the push for more EVs and what new buying patterns are showing. We'll look at how many people are buying EVs, if companies and governments are using more of them, and how government initiatives are helping this along. Second, we'll see if France’s infrastructure is getting ready for more EVs by enabling the necessary amount of charging points. This will give us a clearer picture of how ready France is for more electric cars on the roads.

## Process
- Scope definition 
- End-to-end project planning using Trello
- Data collection using these following sources (Web Scraping, API, Flat File, Database & Big Data System)
- Exploratory data analysis in Python (data wrangling, data cleaning & data visualization)
- Selection and creation of a database using MySQL
- Added data to database and designed Entity Relationship Diagram
- Explored data with MySQL
- Exposed data via API
- Data visualization of main insights using Tableau
- Process data for time series analysis
- Train and test models


## Exploratory Data Analysis
### Data cleaning/wrangling
Data cleaning for this project was thorough and involved the application of a variety of techniques, such as: handling duplicates, handling null values, handling date formats, filtering values, renaming columns, renaming rows values, creating columns, dropping columns when necessary, dropping rows when necessary, verifying that the datatypes were accurate, if not, handle conversion, string formatting, melting,etc.

### Data visualization
To ensure consistency between visualizations and overall analysis, I chose 2011 through 2021 as the range of available years for the vast majority of the charts.
A total of sixteen visualizations were created from the ‘EV_in_France’ database using Tableau via the MySQL connector. Here's a quick look at them:


https://github.com/hilmnr/Charging-Ahead-Frances-Electric-Vehicle-Revolution/assets/145452309/1f3606c9-36ed-45a6-bc78-851fccc0dfcb


## Data Sources
The topic has been segmented into three distinct categories: EV sales in France (which encompasses registration and fleet data), EV charging points in France, and governmental initiatives related to electric vehicles.

After defining those categories, I moved on to data collection, which was carried out through five distinct methods.

1. Web Scraping
French websites 'Capital Auto' and 'Automobile Propre' were scrapped in compliance with their  respective Terms of Service. The scraping was intended to gather the ‘Top 10 EV selling vehicles’ in France for years 2019, 2020, 2021 and 2022.
[Capital Auto](https://www.capital.fr/auto/les-20-voitures-electriques-les-plus-vendues-en-france-en-2021-1424558)
[Automobile Propre](https://www.automobile-propre.com/voiture-electrique-le-top-10-des-ventes-en-france-en-2020/)

2. API
I accessed France's charging points data, categorized by type and department, through ENEDIS's public API, which oversees the majority of the national electricity distribution network. 
[ENEDIS API](https://data.enedis.fr/api/explore/v2.1/console)

3. Flat File
Two sources of data were used in the form of flat files in CSV format.
a. The International Energy Agency (IEA) has an official website at "https://www.iea.org/"
b. The website "https://www.senat.fr/", which is the official site of the French Senate

 4. Database
I consulted the "Insee" database, which is the official site for the National Institute of Statistics and Economic Studies in France. From this source I was able to retrieve all the information related to vehicle registrations in France, more specifically, number of  EV registrations per month from 2011-2021, and number of registrations by energy type for the same period. 
[INSEE](https://data.enedis.fr/api/explore/v2.1/console](https://www.insee.fr/fr/accueil)https://www.insee.fr/fr/accueil)

5. Big Data System
As a final method for collecting data, I had to use a Big Data System in this project. While there are many big data systems on the market, such as Snowflake, Amazon Redshift, Oracle database, there is no doubt that Google BigQuery stands out due to its scalability, speed, ease of use, and cost effectiveness 

## Exposing API
An API was developed to make a portion of the available data accessible for various applications. The documentation for this API was created directly in the Python file using HTML.

### Here's how it looks in action

https://github.com/hilmnr/Charging-Ahead-Frances-Electric-Vehicle-Revolution/assets/145452309/7d795902-70bf-48a4-b979-0951f5dd2de5

## Time Series

(in progress)



