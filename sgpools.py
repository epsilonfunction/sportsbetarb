

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

from functools import cache,cached_property

from utils_sgpools.sgpools_regex_utils import regex_bettype_filter,event_filter

class RegexParser:
    
    @cached_property
    def getDate():
        return re.compile(r'(\d*\.\d{2}\w{2})\s(\d{4})\\n([\w|\s]*)\svs\s([\w|\s]*)\s',re.MULTILINE)

    @cached_property
    def getMatchInfo():
        return re.compile(r'^(\d\.\d{2}\w{2})\\n(\d{4})\\n([\w|\s]+)\svs\s([\w|\s]+)*')
    
    @cached_property
    def halfgoal():
        return re.compile(r'0[1|2]\n(\d*\.\d*)\n[\w\s]* ([\+|\-][\d|\.]*)*',re.MULTILINE)


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
    time.sleep(30)

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
    toJson = {"Date":[],
              "EventID":[],
              "Events":{}}

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
        
        time.sleep(5)

        more_bets = driver.find_elements(By.CLASS_NAME, "show-all")
        for more in more_bets:
            more.click()
            
        
        time.sleep(5)
                    
        events = driver.find_elements(By.XPATH,"//div[@class='event-list']//div[@class='event-list__group']")
        for event in events:
            
            isLiveGroup=re.findall(regex_bettype_filter('isLiveMatch',False),event.text,re.MULTILINE)
            
            # Ignore Live Matches First
            if len(isLiveGroup)==True:
                print("Ignored Matches")
                continue

            eventdate_groups=re.findall(regex_bettype_filter('date_pattern1',False),event.text,re.MULTILINE)
            if len(eventdate_groups)>1:
                logging.warning(f"Parsed info contains more than 1 event date. {eventdate_groups}. Only first event date is taken.")
            # print("eventdate_groups")
            # print(eventdate_groups)
            evdate = eventdate_groups[0]
            # evdate = "1st Jan 1970"
            if evdate not in toJson["Date"]:
                toJson["Date"].append(evdate)
            
            if bet_type in regex_matching_implemented:
                details_regex_group = re.findall(regex_bettype_filter('match_details_pattern', False),event.text)
                print("details_regex_group")
                print(details_regex_group)
                # eventdate,matchdata,oddsdata=event_filter(event.text,bet_type)

                if len(details_regex_group) == 0:
                    continue 
                    
                for event_detail_grouped in details_regex_group:
                    eventtime,eventid,hometeam,awayteam = event_detail_grouped
                    
                    
                    if eventid not in toJson["EventID"]:
                        toJson["EventID"].append(eventid)
                        toJson["Events"][eventid] = {}
                        print(f"Added Event {eventid} into toJson")
                        
                        # toJson["Date"][evdate]["EventID"] = {eventid}
                    
                    if "Date" not in toJson["Events"][eventid].keys():
                        toJson["Events"][eventid]["Date"] = evdate
                        toJson["Events"][eventid]["Time"] = eventtime
                        toJson["Events"][eventid]["Matchup"] = f"{hometeam} vs {awayteam}"
                
                match bet_type:
                    case "1/2 Goal":
                        
                        betdetails = re.findall(regex_bettype_filter('1/2 Goal2',False),event.text,re.MULTILINE)
                        for eventid,homeodds,awayodds in betdetails:
                            toJson["Events"][eventid]["HomeOdds"] = homeodds
                            toJson["Events"][eventid]["AwayOdds"] = awayodds 
                            
                            
                    
                    # if eventtime not in toJson[evdate]:
                    #     toJson[evdate][eventtime] = {}
                    # if eventid not in toJson[evdate][eventtime]:
                    #     toJson[evdate][eventtime][eventid] = {}
                    # if "Matchup" not in toJson[evdate][eventtime][eventid]:
                    #     toJson[evdate][eventtime][eventid]["Matchup"] = f"{hometeam} vs {awayteam}"
            # if matchdata is None:
            #     continue

            # evdate=eventdate[0]
            # if evdate not in toJson:
            #     toJson[evdate] = {}
            
            # idx=0
            # while idx < len(matchdata[0]):
            #     # event time
            #     if matchdata[0][idx] not in toJson[evdate]:
            #         toJson[evdate][matchdata[0][idx]]={}
            #     #event id
            #     if matchdata[1][idx] not in toJson[evdate][matchdata[0][idx]]:
            #         toJson[evdate][matchdata[0][idx]][matchdata[1][idx]]={}

            #     toJson[evdate][matchdata[0][idx]][matchdata[1][idx]]['Home']=matchdata[2][idx]
            #     toJson[evdate][matchdata[0][idx]][matchdata[1][idx]]['Away']=matchdata[3][idx]

            #     if 'BetType' not in toJson[evdate][matchdata[0][idx]][matchdata[1][idx]]:
            #         toJson[evdate][matchdata[0][idx]][matchdata[1][idx]]['BetType']={}
                
                
            #     if bet_type=="1/2 Goal":
            #         home_odds, home_handicap, away_odds, away_handicap = oddsdata[0][idx],oddsdata[1][idx],oddsdata[2][idx],oddsdata[3][idx]

            #         toJson[evdate][matchdata[0][idx]][matchdata[1][idx]]['BetType'][0]=home_odds
            #         toJson[evdate][matchdata[0][idx]][matchdata[1][idx]]['BetType'][1]=away_odds

            #     idx+=1
                

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
