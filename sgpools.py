

import numpy as np 
# import pandas as pd
import time
import json
import logging 
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome

def event_filter (event_string:str):

    date_pattern = r'^(\w{3}, \d{2} \w{3} \d{4})$'
    time_pattern = r'^(\d{1,2}.\d{2}(am|pm))$'
    match_pattern = r'^(\d+)$'
    teams_pattern = r'^([\w\s]+) vs ([\w\s]+)$'
    handicap_pattern = r'^\(([-+]?\d+)\)$'
    score_pattern = r'^(\d+)/(\d+)\s([\w\s]+)$'
    odds_pattern = r'^(\d{2})\n(\d+\.\d+)\n([\w\s]+ [-+]\d+\.\d+)\s\n(\d{2})\n(\d+\.\d+)\n([\w\s]+ [-+]\d+\.\d+)$'

    # Find matches for each pattern
    date_match = re.search(date_pattern, event_string, re.MULTILINE)
    time_match = re.search(time_pattern, event_string, re.MULTILINE)
    match_id_match = re.search(match_pattern, event_string, re.MULTILINE)
    teams_match = re.search(teams_pattern, event_string, re.MULTILINE)
    handicap_match = re.search(handicap_pattern, event_string, re.MULTILINE)
    score_match = re.search(score_pattern, event_string, re.MULTILINE)
    odds_match = re.search(odds_pattern, event_string, re.MULTILINE)

    # Extract matched components
    date_of = date_match.group(1) if date_match else None
    time_of = time_match.group(1) if time_match else None
    match_id = match_id_match.group(1) if match_id_match else None
    team1, team2 = teams_match.groups(1) if teams_match else (None, None)
    handicap = handicap_match.group(1) if handicap_match else None
    # home_score, away_score, goal = score_match.groups() if score_match else (None, None, None)
    # home_odds, away_odds = odds_match.group(2), odds_match.group(5) if odds_match else (None, None)

    # Output the extracted components
    # print("Date:", date_of)
    # print("Time:", time_of)
    # print("Match ID:", match_id)
    # print("Teams:", team1, "vs", team2)
    # print("Handicap:", handicap)
    # print("Score:", home_score, "/", away_score, goal)
    # print("Home Odds:", home_odds)
    # print("Away Odds:", away_odds)

    return date_of,time_of,match_id,team1,team2, handicap


def isEventDate(inp:str) -> bool:
    tempsplit = inp.split()
    for component in tempsplit:
        if component in allmonths:
            logging.info(f"Input String ({inp}) appears to be valid event date.")
            return True
    return False

def isEventTime(inp:str) -> bool:
    validtimeregexp = re.compile(r'\.[0-9]{2}[a,p]m')#allows .30am and .62pm #special case of 'Ham' (hamburg) or 'Jamshedpur' is declined.
    tempsplit = inp.split()
    for component in tempsplit:
        if validtimeregexp.search(component):
            logging.info(f"Input String ({inp}) appears to be valid event time.")
            return True
        # if "am" in component or "pm" in component:
        #     return True
    return False

def isEventId(inp:str) -> bool:
    try: 
        if eval(inp) == 2024 or 999> eval(inp) or eval(inp)>9999:
            return False
        logging.info(f"Input String ({inp}) appears to be valid event ID.")
        return True
    except:
        return False


if __name__ == "__main__":
    target_url = "https://online.singaporepools.com/en/sports/category/1/football"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(target_url)

    #writes pure bet values
    with open("sg_pools2.json", "w") as json_file:
        json_file.write("")

    #writes only bet types
    with open("sg_pools.json", "w") as json_file:
        json_file.write("")

    # WebDriverWait(driver,20)
    time.sleep(3)

    # Get all bet types possible
    bet_type_specific = driver.find_element(By.XPATH, "//select[@class='form-control event-list__filter__market-sort']")
    bet_type_list=bet_type_specific.text.split('\n')
    # bet_type_list=bet_type_specific.json()
    all_bet_list = {'bet_list':bet_type_list}
    with open("sg_pools.json", "a") as json_file:
        json_file.write(json.dumps(all_bet_list))

    testing_data = {"1/2 Goal": ["Sun, 21 Jan 2024", "12.30am", "1028", "Bordeaux vs Nice", "(+17)", "021/2 Goal", "01", "1.20", "Bordeaux +1.5 ", "02", "3.75", "Nice -1.5 ", "12.30am", "1024", "Valenciennes vs Paris FC", "(+15)", "021/2 Goal", "01", "1.12", "Valenciennes +1.5 ", "02", "4.80", "Paris FC -1.5 ", "1.00am", "1357", "Roma vs Verona", "(+17)", "461/2 Goal", "01", "2.30", "Roma -1.5 ", "02", "1.50", "Verona +1.5 "]}

    allmonths=set(['Jan','Feb','Mar','Apr','May','Jun',
                    'Jul','Aug','Sep','Oct','Nov','Dec'])



    # import re
    # word = 'fubar'
    # regexp = re.compile(r'ba[rzd]')
    # if regexp.search(word):
    #   print('matched')




    eventdate=None
    eventtime=None
    eventid=None
    AllEventStrings=[]
    toJson = {}

    select_bet = Select(bet_type_specific)
    display_bet=driver.find_element(By.XPATH, "//button[@class='btn-block button button--orange btn btn-default']")
    for bet_type in bet_type_list:
        select_bet.select_by_visible_text(bet_type)
        display_bet.click()
        time.sleep(3) #Wait for elements to load
        

        # Bet Type may not always be available; Skip to next bet type
        try:
            # Load More Button
            load_button = driver.find_element(By.CLASS_NAME,"event-list__load-all-events")
            load_button.click()
        except:
            continue

        events = driver.find_elements(By.XPATH,"//div[@class='event-list']//div[@class='event-list__group']")
        more_bets = driver.find_elements(By.CLASS_NAME, "show-all")
        for more in more_bets:
            more.click()
        for event in events:

            eventdate,eventtime,eventid,hometeam,awayteam,handicap=None,None,None,None,None,None
            
            eventdate,eventtime,eventid,hometeam,awayteam,handicap=event_filter(event.text)
            
            if eventtime is None:
                continue

            if eventdate not in toJson:
                toJson[eventdate] = {}
            if eventtime not in toJson[eventdate]:
                toJson[eventdate][eventtime]={}
            if eventid not in toJson[eventdate][eventtime]:
                toJson[eventdate][eventtime][eventid]={}


            toJson[eventdate][eventtime][eventid]['Home']=hometeam
            toJson[eventdate][eventtime][eventid]['Away']=awayteam
            
            if 'BetType' not in toJson[eventdate][eventtime][eventid]:
                toJson[eventdate][eventtime][eventid]['BetType']={}
            
            toJson[eventdate][eventtime][eventid]['BetType'][bet_type] = handicap

            events_text = {bet_type : event.text.split('\n')}
            # events_text = {bet_type : event.json()}
            with open("sg_pools2.json",'a') as json_file:
                json_file.write(json.dumps(events_text))

    with open("sgpools3.json",'w') as json_file:
        json_file.write(json.dumps(toJson))

    driver.close()
