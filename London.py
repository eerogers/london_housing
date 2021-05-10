# Let's import the pandas, numpy libraries as pd, and np respectively. 
import pandas as pd
import numpy as np
# Load the pyplot collection of functions from matplotlib, as plt 
import matplotlib as plt
# First, make a variable called url_LondonHousePrices, and assign it the following link, enclosed in quotation-marks as a string:
# https://data.london.gov.uk/download/uk-house-price-index/70ac0766-8902-4eb5-aab5-01951aaed773/UK%20House%20price%20index.xls

url_LondonHousePrices = "https://data.london.gov.uk/download/uk-house-price-index/70ac0766-8902-4eb5-aab5-01951aaed773/UK%20House%20price%20index.xls"

# The dataset we're interested in contains the Average prices of the houses, and is actually on a particular sheet of the Excel file. 
# As a result, we need to specify the sheet name in the read_excel() method.
# Put this data into a variable called properties.  
properties = pd.read_excel(url_LondonHousePrices, sheet_name='Average price', index_col= None)
#print(properties.columns.sort_values())

#List of London borough to check for correct rows.
#(note: 'City of London' technically, administratively not a borough, but included)
london_boroughs = ['City of London', 'Westminster', 'Kensington and Chelsea', 'Hammersmith and Fulham', 'Wandsworth',
'Lambeth', 'Southwark', 'Tower Hamlets', 'Hackney', 'Islington', 'Camden', 'Brent', 'Ealing', 'Hounslow', 'Richmond upon Thames',
'Kingston upon Thames', 'Merton', 'Sutton', 'Croydon', 'Bromley', 'Lewisham', 'Greenwich', 'Bexley', 'Havering', 'Barking and Dagenham',
'Redbridge', 'Newham', 'Waltham Forest', 'Haringey', 'Enfield', 'Barnet', 'Harrow', 'Hillingdon']

#Removal of the header value from the created 'properties' dataframe
headless_london = properties.iloc[1:315]

#A brief check of the unnamed columns to be sure of what they contain (all nan values - probably from excel format)
unnamed = ['Unnamed: 34', 'Unnamed: 37', 'Unnamed: 47']
value_check = headless_london.loc[:,unnamed]

#For ease of sorting through borough names, the dataframe is transposed and the unnamed three dropped
transposed_london = headless_london.transpose()
transposed_london.drop(unnamed, axis=0, inplace=True)

#Grabs the upper-most row's values, which contains dates. Iterates through them to create a list of cleaned strings.
date_row= transposed_london.iloc[0]
cleaned_dates = []
for i in date_row:
    x = str(i).replace(' 00:00:00', '')
    cleaned_dates.append(x)

#Now that the dates are saved, the row is dropped.
transposed_london.drop('Unnamed: 0', axis=0, inplace=True)

#Sets cleaned_dates list as column names
transposed_london.columns = cleaned_dates

#Removes regions of England, london regions, and "England", assigns rows to own dataframes
regions_london = transposed_london.loc['Inner London':'Outer London']
transposed_london.drop(['Inner London','Outer London'], axis=0, inplace=True)
regions_england = transposed_london.loc['NORTH EAST':'SOUTH WEST']
transposed_london.drop(transposed_london.loc['NORTH EAST':'SOUTH WEST'].index, axis=0, inplace=True)
england_series = transposed_london.loc['England']
transposed_london.drop('England', axis=0, inplace=True)

#Now that only the desired rows remain in transposed_london, create a new dataframe that only compares
#the first and last values, from which to determine growth
borough_growth = transposed_london.loc[:,['1995-01-01', '2021-02-01']]

borough_growth['Growth'] = borough_growth['2021-02-01'] - borough_growth['1995-01-01']
borough_growth = borough_growth.sort_values(by='Growth', ascending=False)

#This is one calculation. I'll see if a calculated average of 1995 and 2021 changes things.
average_1995 = []
average_2021 = []
for i in transposed_london.columns:
    if '1995' in i:
        average_1995.append(i)
    if '2021' in i:
        average_2021.append(i)
london_1995 = transposed_london[average_1995]
london_2021 = transposed_london[average_2021]

#Calculating averages for 1995 and 2021 respectively
london_1995['Yearly_Average_1995'] = london_1995.sum(axis=1)/12
london_2021['Yearly_Average_2021'] = london_2021.sum(axis=1)/2

#Creating average growth column showing the differences between 2021 and 1995 averages
borough_growth['Average Growth'] = london_2021['Yearly_Average_2021'] - london_1995['Yearly_Average_1995']
sorted_by_average_growth = borough_growth.sort_values(by='Average Growth', ascending=False)
sorted_by_latest_data = borough_growth.sort_values(by='2021-02-01', ascending=False)
sorted_by_oldest_data = borough_growth.sort_values(by='1995-01-01', ascending=False)
print(sorted_by_average_growth)
