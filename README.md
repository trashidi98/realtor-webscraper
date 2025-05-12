# This Project 

This is a project I worked on recently, covering a lot of things that I learned as I become a more involved engineer. It's definitely one of the most in-depth **personal projects** I've done because it is fully tested. 

I spent a good amount of time thinking about how this could possibly scale. I also worked on making sure the code was as clean as possible, maintanable and most importantly testable.

Every function I wrote is unit tested with the expected output as well as their respective error handling cases. There are also end-to-end tests that I wrote because it's easy to get "lost in the sauce" in unit testing and forget if the entire app is functioning the way it should.


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
ruff check src/final_scraper.py

ruff check tests/test_scraper.py

ruff format src/final_scraper.py

ruff format tests/test_scraper.py
```

Create a .pre-commit-config.yaml file from the README below
https://github.com/astral-sh/ruff-pre-commit?tab=readme-ov-file

How to add pre commit hook
https://pre-commit.com/




