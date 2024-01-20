# ScrapeCVBankasUsingSelenium

DESCRIPTION

This is a web scraping project to scrape cvbankas.lt for job advertisements in Vilnius. 
It uses Selenium driver to open the appropriate web page in Chrome browser, waits for user input on the position to search, 
then paginates through to get all the results found. Output goes to stdout and a csv file 
in "output" directory. CSV file then can be further manipulated using Excel.


INSTALLATION

Project requires Chrome web driver to be installed in .\venv\driver directory.
Version of driver must match the version of Chrome browser in use. Drivers can be found here:
https://googlechromelabs.github.io/chrome-for-testing/
Use "pip install -r requirements.txt" to set up the needed virtual environment.

USE

Start the main.py, wait for driver initialisation, then input the desired position and enjoy!
The best demonstration goes by searching for "Projektų vadovas" as it returns >200 results, 
therefore scraping continues on next pages.  