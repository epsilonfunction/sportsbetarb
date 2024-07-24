# sportsbetarb
Sports Betting Arbitrage

This is a test of webscraping and data analytics.

The objective here is to find out if there is any betting arbitrage opportunity between betting sites.

Key Steps:
1) Webscraping from betting sites
    Targets:
        - Singapore Pools
        - 1xbet
        
2) Use Apache Airflow to orchestrate the different python webscraping files
3) Warehouse it on local PostgreSQL/NoSQL database. 
4) Find ways to arbitrage it

Focus on Football ONLY for now


Official Steps
Step 1: 
activate venv

Step 2:
pip install -r requirements.txt

    2a. Dev Note: requirements.txt generated with: 
    
    pipreqs ./ --ignore .venv
 
Step 3: 
    a. Start MongoDB server
        net start mongodb
    b. stop MongoDB server
        net stop mongodb
    Default Port: localhost:27017



Requirements:
- Python 3.9

Dependencies Used:
- Selenium
- PyMongo

Unofficial Requirements:
- You can connect to the following sites:
    - www.singaporepools.com.sg
    - sg.1xbet.com/en/line/football
        - Access is based on connecting to Google Public DNS Service
        - https://developers.google.com/speed/public-dns
        - Use at own's risk

Issues:
1) Chromedriver Path not defined. Always downloaded and unzipped. May want to work on this


## Branches
1. Main 
    Production Branch
2. Testing/Prototyping
    - Docker Deployment of sgpools (might merge into sgpools once sgpools is ready)
    - PyMongo (Not created Yet)
        Dumping of data into mongodb datalake
3. sgpools
    Conversionof sgpools notebook into functional environment.
    TODO:
    1) "1/2 Goal" Pattern Matching -done-
    2) "1st Goal Scorer" Pattern Matching 
    3) "1X2" Pattern Matching 
    4) "Asian Handicap/HT Asian Handicap" Regex Matching
    9) Testcase Writing/Saving
        a) Event stream
        b) HTML scrape

Misc 1: Accessing .venv for admin purposes
# cd .venv/Scripts
# . activate
# cd ../..




Proposed Schema:
{
    Event_Date: {
        Event_Time: {
            Event_ID: {
                Matchup: X vs Y
                BetType: {
                    "1/2 Goal"
                }
            }
        } 
    }
}

