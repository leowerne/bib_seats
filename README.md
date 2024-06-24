# Libariy Seats over time
I want to understand the patterns in the occupation of the libary seats of my university

## Method
### Procurement of data
#### Setup of the machine
Since I need something to run code all day long for up to a year, I wanted to use a remote solution.I set up EC2 Linux instance on AWS.
I wanted to avoid Amazon because I personally dislike the company but for some reason I could not use the free tier of Oracle, Microsoft, Heroku and IBM.

The system requirements for this job are almost as low as it gets and there was only one option included in the freee tier anyways: t2.micro

#### Scraping
I wrote a simple python script "scrape.py" that is executed every 15 minutes on the Linux instance.
It downloads the html of the university website and extracts the relevant information from it.
It then extends a csv file "bib_seats.csv" with the relevant information.
To run this scipt every 15 minutes, I created a file "scrape.cron" with the content "*/15 * * * * python3 bib_sears.py".
This file with cron job(s) is activated with "crontab scrape.cron"

So in the end instance we have 3 files on the Linux instance:
 - scrape.py
 - scrape.cron
 - bib_seats.csv

This is nice and all but we also need to download "bib_seats.csv" somehow.
#### Downloading
I Sceduled a job on my local machine that downloads the csv file from the Linux instance using SCP.
For this I wrote the file download.bat which is executed with Windows Tasks ("Aufgabenplanung" in German).
This is done once per day for safety since something can allways go wrong (e.g. I could forget that the free tier runs out). 


#### Domain Knowledge
I regularily checked the blog of the university to know of relevant events that might impact the data.
One exapmle is a water damage which forced the main part of one library to close.
This information is collected in domain_knowledge.txt

### Data Analysis
#### Visualization
First up I plotted a simple graph of the time series.

#### Seasonal Time Series Analysis


## Insights