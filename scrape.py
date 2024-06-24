#%%
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import re
# URL of the website to scrape
url = 'https://www.bib.uni-mannheim.de/standorte/freie-sitzplaetze/'

# Fetch the webpage content
response = requests.get(url)
html_content = response.content

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table containing the seat information
seat_table = soup.find('div', class_='available-seats-table')

# Extract the "Data from" datetime from the webpage
date_time_pattern = r"\d{2}\.\d{2}\.\d{2}, \d{2}:\d{2}"
stand = seat_table.find_all('p')[-1].text
stand_time = re.findall(date_time_pattern, stand)
data_from = stand_time#[datetime.strptime(t, '%d.%m.%y, %H:%M') for t in stand_time]

# Initialize empty dictionary to store data
data = {}

# Get the current timestamp
timestamp = datetime.now()

# Extract data from each row
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
new_data = pd.DataFrame(data, index=[timestamp])

# Add the "Data from" column
new_data['Data from'] = data_from

# Load existing data from the local file
try:
    existing_data = pd.read_csv('bib_seats.csv', index_col=0)
except FileNotFoundError:
    existing_data = pd.DataFrame()

# Append new data to the existing DataFrame
bib_seats = pd.concat([existing_data, new_data])

# Save the extended DataFrame to the local file
bib_seats.to_csv('bib_seats.csv')

print("saved")
# %%
