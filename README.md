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

Requirements:
- Python 3.9
- Selenium

Unofficial Requirements:
- You can connect to the following sites:
    - www.singaporepools.com.sg
    - sg.1xbet.com/en/line/football
        - Access is based on connecting to Google Public DNS Service
        - https://developers.google.com/speed/public-dns
        - Use at own's risk


## Branches
1. Main 
    Production Branch
2. Testing/Prototyping
    - Docker Deployment of sgpools (might merge into sgpools once sgpools is ready)
    - PyMongo (Not created Yet)
        Dumping of data into mongodb datalake
3. sgpools
    Conversionof sgpools notebook into functional environment.



Misc 1: Accessing .venv for admin purposes
# cd .venv/Scripts
# . activate
# cd ../..


Proposed Schema:
Sgpools:
{'Timestamp'
    competition: {
        'name': 'UEFA Champions League',
        'federation':'UEFA',
        'date': '2023-01-28',
        'matches': {

        }
    }

}