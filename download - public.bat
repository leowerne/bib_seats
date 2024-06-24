@echo off
cd \
cd Users/leon_
echo "current wd:" 
echo %cd%
echo "downloading scraped bib seats"

scp -i "Path/to/foler/bib-seats-keys.pem" ubuntu@ip.adress:~/bib_seats.csv "Path/to/folder/"

echo "renaming bib_seats.csv to bib_seats_%DATE:~6,4%%DATE:~3,2%%DATE:~0,2%.csv in wd:"

cd "Path/to/folder"
echo %cd%

rename "bib_seats.csv" "bib_seats_%DATE:~6,4%%DATE:~3,2%%DATE:~0,2%.csv"

echo "creating plot"
cd \
cd C:/Users/my_username/anaconda3/Scripts
call activate base
CALL conda.bat activate bib_seats
cd \
cd "Path/to/folder"
python visualize.py

pause
