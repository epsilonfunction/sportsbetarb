

import numpy as np 
# import pandas as pd
import time
import datetime
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

from functools import cache

@cache
def regex_bettype_filter(searchitem:str, complex_pattern:bool=False):

    """Returns regex pattern to search for

    Args:
        bettype (str): _description_
    """
    
    #Betting Types
    if searchitem=='match_info'and complex_pattern==True:
        return re.compile(r'(\d*\.\d{2}\w{2})\s(\d{4})\\n([\w|\s]*)\svs\s([\w|\s]*)\s',re.MULTILINE)
    
    if searchitem=='1/2 Goal' and complex_pattern==True:

        # Group 1: Event Time
        # Group 2: Event ID
        # Group 3: Team1 name
        # Group 4: Team2 name
        # Group 5: Team1 odds
        # Group 6: Team1 handicap
        # Group 7: Team2 odds
        # Group 8: Team2 handicap
    # match_info_pattern=r'(\d\.\d{2}\w{2})\\n(\d{4})\\n([\w|\s]+)\svs\s([\w|\s]+)*'
    # odds_pattern=r'\s\n(\d{2})\n(\d+\.\d+)\n([\w\s]+ [-+]\d+\.\d+)'

        return re.compile(r'(\d\.\d{2}\w{2})\\n(\d{4})\\n([\w|\s]+)\svs\s([\w|\s]+)*\\n.{23}(.{4}).{2}(?:[\w|\s]+)(.{4}).{7}(.{4})\\n(?:[\w|\s]+)(.{4})',re.MULTILINE)
    
    
    #Event Types
    if searchitem=='date_pattern':
        return re.compile(r'^(\w{3}, \d{2} \w{3} \d{4})$',re.MULTILINE)
    if searchitem=='time_pattern':
        return re.compile(r'(\d\.\d+\w{2})',re.MULTILINE)
    if searchitem=='match_pattern':
        return re.compile(r'(\d{4})\\',re.MULTILINE)
    if searchitem=='teams_pattern':
        return re.compile(r'^([\w\s]+) vs ([\w\s]+)$',re.MULTILINE)
    if searchitem=='odds_pattern':
        return re.compile(r'^(\d{2})\n(\d+\.\d+)\n([\w\s]+ [-+]\d+\.\d+)\s\n(\d{2})\n(\d+\.\d+)\n([\w\s]+ [-+]\d+\.\d+)$',re.MULTILINE)
    
    if searchitem=='1/2 Goal':
        return re.compile(r'0[1|2]\n(\d*\.\d*)\n[\w\s]* ([\+|\-][\d|\.]*)*',re.MULTILINE)
    
    # if searchitem=='time_pattern':
    #     return r'^(\d{1,2}.\d{2}(am|pm))$'
    

def event_filter (event_string:str,bettype:str="Default") -> tuple():

    """ 
    Cthulhu Below:` 
    ^(\w{3}, \d{2} \w{3} \d{4})\\n(\d\.\d{2}\w{2})\\n(\d{4})\\n([\w|\s]+)\svs\s([\w|\s]+)*\\n.{23}(.{4})\\n(?:[\w|\s]+)(.{4}).{7}(.{4})\\n(?:[\w|\s]+)(.{4})

    Explanation: 
        ^(\w{3}, \d{2} \w{3} \d{4}): {Date}
        (\d\.\d{2}\w{2})\\n(\d{4}): {Time} and {Event} ID Matching
        ([\w|\s]+)\svs\s([\w|\s]+)*: {Home} team vs {Away} team
        \\n.{23}(.{4}): 
            Home Team 1/2 goal odds generally follow this form:
            \n(+17)\n461/2 Goal\n01\n4.80
            captures {4.80}
            Might need to be more robust
        More to be done later.
        
        
    Cthulhu 2:
    (\d\.\d{2}\w{2})\\n(\d{4})\\n([\w|\s]+)\svs\s([\w|\s]+)*\\n.{23}(.{4}).{2}(?:[\w|\s]+)(.{4}).{7}(.{4})\\n(?:[\w|\s]+)(.{4})
    (\d\.\d{2}\w{2})\\n(\d{4})\\n([\w|\s]+)\svs\s([\w|\s]+)*\\n.{23}(.{4}).{2}(?:[\w|\s]+)(.{4}).{7}(.{4})\\n(?:[\w|\s]+)(.{4})
    
    (\d*\.\d{2}\w{2})\s(\d{4})\\n([\w|\s]*)\svs\s([\w|\s]*)\s : Match Info
    \\n.{23}(.{4}).{2}(?:[\w|\s]+)(.{4}).{7}(.{4})\\n(?:[\w|\s]+)(.{4}) : Odds Part
    """

    date_pattern = r'^(\w{3}, \d{2} \w{3} \d{4})$'
    time_pattern = r'^(\d{1,2}.\d{2}(am|pm))$'
    match_pattern = r'^(\d+)$'
    teams_pattern = r'^([\w\s]+) vs ([\w\s]+)$'
    # handicap_pattern = r'^\(([-+]?\d+)\)$'
    # score_pattern = r'^(\d+)/(\d+)\s([\w\s]+)$'
    
    match_info_pattern=r'(\d\.\d{2}\w{2})\\n(\d{4})\\n([\w|\s]+)\svs\s([\w|\s]+)*'
    odds_pattern=r'\s\n(\d{2})\n(\d+\.\d+)\n([\w\s]+ [-+]\d+\.\d+)'
    # odds_pattern = r'^(\d{2})\n(\d+\.\d+)\n([\w\s]+ [-+]\d+\.\d+)\s\n(\d{2})\n(\d+\.\d+)\n([\w\s]+ [-+]\d+\.\d+)$'



    # Find matches for each pattern
    date_match = regex_bettype_filter(searchitem='date_pattern').search(event_string)

    if bettype=="1/2 Goal":

        # Group 1: Event Time
        # Group 2: Event ID
        # Group 3: Team1 name
        # Group 4: Team2 name
        # Group 5: Team1 odds
        # Group 6: Team1 handicap
        # Group 7: Team2 odds
        # Group 8: Team2 handicap
        
        matchdata=regex_bettype_filter(searchitem='match_info',complex_pattern=True).search(event_string)
        oddsdata=regex_bettype_filter(searchitem=bettype,complex_pattern=True).search(event_string)

        dateOf=date_match.group() if date_match else None
        matchdataresults = matchdata.group() if matchdata else None
        oddsdata = oddsdata.group() if oddsdata else None

        return date_match,matchdataresults,oddsdata


    # Find matches for each pattern
    date_match = regex_bettype_filter(searchitem='date_pattern').search(event_string)
    
    try:
        time_match = regex_bettype_filter(searchitem='time_pattern').search(event_string)
        match_id_match = regex_bettype_filter(searchitem='match_pattern').search(event_string)
        teams_match = regex_bettype_filter(searchitem='teams_pattern').search(event_string)
        odds_pattern = regex_bettype_filter(searchitem='odds_pattern').search(event_string)
        # date_match = re.search(date_pattern, event_string, re.MULTILINE)
        # time_match = re.search(time_pattern, event_string, re.MULTILINE)
        # match_id_match = re.search(match_pattern, event_string, re.MULTILINE)
        # teams_match = re.search(teams_pattern, event_string, re.MULTILINE)
        # handicap_match = re.search(handicap_pattern, event_string, re.MULTILINE)
        # score_match = re.search(score_pattern, event_string, re.MULTILINE)
        # odds_match = re.search(odds_pattern, event_string, re.MULTILINE)

    except:
        time_match,match_id_match,teams_match,odds_pattern = None,None,None,None
    # Extract matched components
    date_of = date_match.group(1) if date_match else None
    time_of = time_match.group(1) if time_match else None
    match_id = match_id_match.group(1) if match_id_match else None
    team1, team2 = teams_match.groups(1) if teams_match else (None, None)
    # handicap = handicap_match.group(1) if handicap_match else None
    
    if match_id is None:
        return date_of,time_of,match_id,team1,team2, None, None, None
    
    if bettype=="1/2 Goal":
  
        odds_pattern=r'0[1|2]\n(\d*\.\d*)\n[\w\s]* ([\+|\-][\d|\.]*)*'
        odds_match = re.findall(odds_pattern,event_string,re.MULTILINE)
        home_odds, home_handicap, = odds_match[0] if odds_match else None,None
        away_odds,away_handicap = odds_match[1] if odds_match else None,None
        
        logging.info(f"{team1} vs {team2} for {bettype} at {home_odds};{away_odds}")
        return date_of,time_of,match_id,team1,team2, home_handicap, home_odds, away_odds

    elif bettype=="Default":
        return date_of,time_of,match_id,team1,team2, None, None, None
        
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



# def isEventDate(inp:str) -> bool:
#     tempsplit = inp.split()
#     for component in tempsplit:
#         if component in allmonths:
#             logging.info(f"Input String ({inp}) appears to be valid event date.")
#             return True
#     return False

# def isEventTime(inp:str) -> bool:
#     validtimeregexp = re.compile(r'\.[0-9]{2}[a,p]m')#allows .30am and .62pm #special case of 'Ham' (hamburg) or 'Jamshedpur' is declined.
#     tempsplit = inp.split()
#     for component in tempsplit:
#         if validtimeregexp.search(component):
#             logging.info(f"Input String ({inp}) appears to be valid event time.")
#             return True
#         # if "am" in component or "pm" in component:
#         #     return True
#     return False

# def isEventId(inp:str) -> bool:
#     try: 
#         if eval(inp) == 2024 or 999> eval(inp) or eval(inp)>9999:
#             return False
#         logging.info(f"Input String ({inp}) appears to be valid event ID.")
#         return True
#     except:
#         return False


if __name__ == "__main__":
    

    logging.basicConfig(filename="sgpools_datacleaning.log",encoding='utf-8', level=logging.DEBUG)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info("Current Time: " + current_time)

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

    eventdate=None
    eventtime=None
    eventid=None
    AllEventStrings=[]
    toJson = {}

    select_bet = Select(bet_type_specific)
    display_bet=driver.find_element(By.XPATH, "//button[@class='btn-block button button--orange btn btn-default']")
   
    regex_matching_implemented = ['1/2 Goal']
    for bet_type in bet_type_list:

        if bet_type not in regex_matching_implemented:
            continue
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
            
        
        fst_val,sec_val = None,None
        
        for event in events:

            eventdate,matchdata,oddsdata=None,None,None
            
            if bet_type in regex_matching_implemented:
                eventdate,matchdata,oddsdata=event_filter(event.text,bet_type)
            
            if matchdata is None:
                continue

            evdate=eventdate[0]
            if len(eventdate)>1:
                logging.warning(f"Parsed info contains more than 1 event date. {eventdate}. Only first event date is taken.")
            if evdate not in toJson:
                toJson[evdate] = {}
            
            idx=0
            while idx < len(matchdata[0]):
                # event time
                if matchdata[0][idx] not in toJson[evdate]:
                    toJson[evdate][matchdata[0][idx]]={}
                #event id
                if matchdata[1][idx] not in toJson[evdate][matchdata[0][idx]]:
                    toJson[evdate][matchdata[0][idx]][matchdata[1][idx]]={}

                toJson[evdate][matchdata[0][idx]][matchdata[1][idx]]['Home']=matchdata[2][idx]
                toJson[evdate][matchdata[0][idx]][matchdata[1][idx]]['Away']=matchdata[3][idx]

                if 'BetType' not in toJson[evdate][matchdata[0][idx]][matchdata[1][idx]]:
                    toJson[evdate][matchdata[0][idx]][matchdata[1][idx]]['BetType']={}
                
                
                if bet_type=="1/2 Goal":
                    home_odds, home_handicap, away_odds, away_handicap = oddsdata[0][idx],oddsdata[1][idx],oddsdata[2][idx],oddsdata[3][idx]

                    toJson[evdate][matchdata[0][idx]][matchdata[1][idx]]['BetType'][0]=home_odds
                    toJson[evdate][matchdata[0][idx]][matchdata[1][idx]]['BetType'][1]=away_odds

                idx+=1
                

            # if eventtime not in toJson[eventdate]:
            #     toJson[eventdate][eventtime]={}
            # if eventid not in toJson[eventdate][eventtime]:
            #     toJson[eventdate][eventtime][eventid]={}


            # toJson[eventdate][eventtime][eventid]['Home']=hometeam
            # toJson[eventdate][eventtime][eventid]['Away']=awayteam
            
            # if 'BetType' not in toJson[eventdate][eventtime][eventid]:
            #     toJson[eventdate][eventtime][eventid]['BetType']={}
            
            # if bet_type not in toJson[eventdate][eventtime][eventid]['BetType']:
            #     toJson[eventdate][eventtime][eventid]['BetType'][bet_type] = {}
            
            # if home_odds is None:
            #     toJson[eventdate][eventtime][eventid]['BetType'][bet_type] = None
            # else:
            #     toJson[eventdate][eventtime][eventid]['BetType'][bet_type]['HomeOdds']=home_odds
            #     toJson[eventdate][eventtime][eventid]['BetType'][bet_type]['AwayOdds']=away_odds

            events_text = {bet_type : event.text.split('\n')}
            # events_text = {bet_type : event.json()}
            with open("sg_pools2.json",'a') as json_file:
                json_file.write(json.dumps(events_text))

    with open("sgpools3.json",'w') as json_file:
        json_file.write(json.dumps(toJson))

    driver.close()
