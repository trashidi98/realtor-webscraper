# This project 


# Specifications 

Get bs4 running ✅

Get selenium running with chromium ✅

scrape first page using selenium ✅

See how to move to second pages ✅

Get into CSV ✅

Implement batching ✅

Add logging to ensure visibility ✅

Handle Error from Script and add logging ✅

Error happens on page 19 ✅

Cleanup Code TODOS ✅

Implement failsafe if internet drops during a loop 

Write tests 

Code Review 



## FORMATTING COMMANDS 

```
Build requirements.txt
pipreqs . --ignore ./.venv/ --force 

Check and Format
ruff check src/final_scraper.py

ruff check tests/test_scraper.py

ruff format src/final_scraper.py

ruff format tests/test_scraper.py
```


# TODO 

Is it more effecient to store in CSV as you go? Or at the end? Probably at the end

Write a test that takes in the data html and checks for the right values

Can you write tests to make sure its cleaning the right information?

Write unit tests, integration tests, and e2e tests

Add logging 

Add error handling

Can you run headless and enable JS?

Add a function to recieve pages, and location and it should search

Check how you can make it more lightweight using the requests_html 

pip install requests-html

Can render html and JS - a dynamic webapge: https://www.youtube.com/watch?v=MeBU-4Xs2RU

#
# Features to add 

Paginations
Email a list to me every morning?
API Wrapper on top to specify how many articles and maybe search params?
limit, keywords, is there any way to search the backlog?
