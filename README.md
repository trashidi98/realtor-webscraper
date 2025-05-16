# This Project 

This project is a webscraper that scrapes the data from a realtor website. The motivation being that I came across this realtor website and thought that the data could be useful (to some businesses in or adjacent to the real estate market), can I scrape it?

I have no intention to sell the data or this scraper it just seemed like an interesting project to work on and was my introduction to webscraping.

I have redacted the website, stored on a local env file, to ensure that this scraper is not utilized on that particular webpage.

Worked on making sure the code was as clean as possible and testable.

There are also end-to-end tests that I wrote because it's easy to get "lost in the sauce" in unit testing and forget if the app is still functioning with each commit.

# How to run 

This is meant to be run as a command line script with two arguments 

```
python scraper.py 3 realtor_data 
```

Where 3 indicates the number of webpages of data you want to scrape, and realtor_data is the name of the file you would like to save it to, will be saved as realtor_data.csv, in the directory where this script is called. 

You can also call it with no arguments

```
python scraper.py
```

In this case, the script will default back to the values here: https://github.com/trashidi98/realtor-webscraper/blob/09aef9d3a2f64f56522955192fc82e0a2a3ccfab/src/final_scraper.py#L18-L19


## Things left todo 

I still have a few things I want to do on this project, but for now until I have some free time it will stay this way.

Add What I learned section

Code Review

Can you run headless and enable JS?


## FORMATTING COMMANDS 

This is for myself, I used the ruff linter, it was perfect. I also added a pre-commit hook for the ruff linter which worked extremely well. Checkout the commands and resources below if you want that on your repo.

```
Build requirements.txt
pipreqs . --ignore ./.venv/ --force 

Check and Format
ruff check src/scraper.py

ruff check tests/test_scraper.py

ruff format src/scraper.py

ruff format tests/test_scraper.py
```

Create a .pre-commit-config.yaml file from the README below
https://github.com/astral-sh/ruff-pre-commit?tab=readme-ov-file

How to add pre commit hook
https://pre-commit.com/




