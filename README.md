# LLM Scraper
Simple prototype coded in few hours for an hackathon challenge. Uses the selenium library to scrape any website text content, and then the OpenAI APIs to answer any question about it. 

# Requirements
Selenium library requires a browser driver to be configured:
- For Firefox "geckodriver" must be in the PATH  (download at https://github.com/mozilla/geckodriver/releases)
- For Chrome "chromedriver" must be installed (https://chromedriver.chromium.org/downloads)

An OpenAI API must be configured in the .env file.
The .env should include the variable OPENAI_KEY (e.g. OPENAI_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx)

# Quickstart
see example.py

## TODO
- setup.py
- CLI
- improve exceptions handling
- rate limiting

# Author 
Francesco Corallo (corallofrancesco@hotmail.it) @ 2023