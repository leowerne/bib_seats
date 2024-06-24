#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import re

#set name of storagte file 
filename = 'bib_seats2.csv'

# URL of the websites to scrape
urls = ['https://www.bib.uni-mannheim.de/standorte/freie-sitzplaetze/','https://www.ub.uni-heidelberg.de/raumres/?building=Altstadt']

# Fetch the webpages content
responses = [requests.get(url) for url in urls]

# Get the current timestamp
timestamp = datetime.now()


# Parse the HTML content
html_contents = [response.content for response in responses]
soups = [BeautifulSoup(html_content, 'html.parser') for html_content in html_contents]

#%% Mannheim
# Find the table containing the seat information
seat_table = soups[0].find('div', class_='available-seats-table')

# Extract the "Data from" datetime from the webpage
date_time_pattern = r"\d{2}\.\d{2}\.\d{2}, \d{2}:\d{2}"
stand = seat_table.find_all('p')[-1].text
stand_time = re.findall(date_time_pattern, stand)
data_from = stand_time#[datetime.strptime(t, '%d.%m.%y, %H:%M') for t in stand_time]

# Initialize empty dictionary to store data
data = {}

#Extract data from each row
rows = seat_table.find_all('tr')
for row in rows:
    # Find all cells in the row
    cells = row.find_all('td')
    if len(cells) == 3:
        # Extract the library name from the first cell
        library_name = cells[1].find('h4').find('a').text.strip()
        
        # Extract the available seats information from the second cell
        available_seats_cell = cells[0].find('div', class_='available-seats-table-status')
        available_seats_string = available_seats_cell.find('span').text.strip() if available_seats_cell.find('span') else available_seats_cell.find('p').text.strip()
        
        # Store data in dictionary
        data[library_name] = available_seats_string

# Create a DataFrame
new_data_ma = pd.DataFrame(data, index=[timestamp])

# Add the "Data from" column
new_data_ma['Data from'] = data_from

#%% Heidelberg
soups[1]


#%% save
# Load existing data from the local file
try:
    existing_data = pd.read_csv(filename, index_col=0)
except FileNotFoundError:
    existing_data = pd.DataFrame()

# Append new data to the existing DataFrame
bib_seats = pd.concat([existing_data, new_data])

# Save the extended DataFrame to the local file
bib_seats.to_csv(filename)

print("saved")
# %%
