# sportsbetarb
Sports Betting Arbitrage

This is a test of webscraping and data analytics.

The objective here is to find out if there is any betting arbitrage opportunity between betting sites.

Key Steps:
1) Webscraping from betting sites
    Targets:
        - Singapore Pools
	- 
2) Use Apache Airflow to orchestrate the different python webscraping files
3) Warehouse it on local PostgreSQL/NoSQL database. 
4) Find ways to arbitrage it

Focus on Football ONLY for now


Official Steps
Step 1: 
activate venv

Step 2:
pip install -r requirements.txt




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