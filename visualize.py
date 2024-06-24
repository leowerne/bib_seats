#%%
import pandas as pd
import matplotlib.pyplot as plt
import re
import os

def get_newest_csv_file():
    files = [file for file in os.listdir('.') if file.startswith('bib_seats') and file.endswith('.csv')]
    if not files:
        return None
    newest_file = max(files, key=os.path.getctime)
    return newest_file

# Read the CSV file into a DataFrame, skipping the first two columns
new_file = get_newest_csv_file()
df = pd.read_csv(new_file)

#%%
# Set the index to the timestamps from the last column
df.index = pd.to_datetime(df.iloc[:, -1], format='%d.%m.%y, %H:%M')
 

# Drop the last column after setting it as index
df = df.iloc[:, 2:-1]

def extract_percents(cell):
    match = re.search(r'(\d+) %', cell)
    if match:
        return int(match.group(1))
    return None

# Apply the function to each cell in the DataFrame
df = df.applymap(extract_percents)
#%%
# Plot all time series as lines in one plot
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
for col in df.columns:
    plt.plot(df.index, df[col], label=col)

plt.xlabel('Time')
plt.ylabel('Unavailable Seats')
plt.title('Occupied seats per library over time')
plt.legend()
plt.grid(True)
plt.savefig("bib_seats.png")
#plt.show()
# %%
