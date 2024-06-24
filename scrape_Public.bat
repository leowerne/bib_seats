@echo off
echo "scraping bib_seats"
cd \
cd C:/Users/my_username/anaconda3/Scripts
call activate base
CALL conda.bat activate bib_seats
cd \
cd "Path/to/folder"

python scrape.py

