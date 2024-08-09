

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

# class RegexParser:
    
#     @cached_property
#     def getDate():
#         return re.compile(r'(\d*\.\d{2}\w{2})\s(\d{4})\\n([\w|\s]*)\svs\s([\w|\s]*)\s',re.MULTILINE)

#     @cached_property
#     def getMatchInfo():
#         return re.compile(r'^(\d\.\d{2}\w{2})\\n(\d{4})\\n([\w|\s]+)\svs\s([\w|\s]+)*')
    
#     @cached_property
#     def halfgoal():
#         return re.compile(r'0[1|2]\n(\d*\.\d*)\n[\w\s]* ([\+|\-][\d|\.]*)*',re.MULTILINE)

class SgPools:
    def __init__(self) -> None:
        self.URL="https://online.singaporepools.com/en/sports/category/1/football"
        self.__BetTypes=[
            "1/2 Goal",
            # "1st Goal Scorer",
            "1X2",
            "Halftime 1x2"
        ]
        # self.__BetTypes=[
        #     "1/2 Goal",
        #     "1st Goal Scorer",
        #     "1X2",
        #     "Asian Handicap/HT Asian Handicap",
        #     "Halftime 1x2",
        #     "Halftime Total Goals",
        #     "Halftime-Fulltime",
        #     "Handicap 1X2",
        #     "Last Goal Scorer",
        #     "Pick the Score",
        #     "Team to Score 1st Goal",
        #     "Total Goals",
        #     "Total Goals Odd/Even",
        #     "Total Goals Over/Under",
        #     "Will Both Teams Score"]
        
        self.__BetTypes=[
            "Halftime Total Goals"
        ]
    def SetURL(self,URL=""):
        self.URL=URL 
        return None
    def GetURL(self):
        return self.URL


class SgPoolsWriter(SgPools):
    """A Class to write and store data
    """
    def __init__(self):
        super().__init__()
        self.__LogDir=None
        self.__ScrapeDir=None
        self.__toJson=None
        
    def SetDir(self,directory:str="",dirtype:str="")->None:
        
        match dirtype:
            case "Log":
                self.__LogDir = directory 
            case "Scrape":
                self.__ScrapeDir=directory
            case "Json":
                self.__toJson=directory
            # case _ :
            #     print(f"Invalid Directory Type Set. Aborting
            #           Writing Directory Setter Operations")
        
        return None
    
    def GetDir(self,dirtype:str="")->str:
        match dirtype:
            case "Log":
                return self.__LogDir
            case "Scrape":
                return self.__ScrapeDir
            case "Json":
                return self.__toJson
            # case __ :
            #     print(f"Invalid Directory Type Set. Aborting
            #           Writing Directory Setter Operations")
        
        


class SgPoolsScraper(SgPools):
    """A Generic Class to Scrape defined terms
    """
    def __init__(self) -> None:
        super().__init__()
        self.Writer = None
        
    def SetBetType(self,BetType:str)->None:
        if BetType not in self.__BetTypes:
            print(f"BetType: {BetType} not found. Please Try Again!")
            logging.warning(f"BetType: {BetType} not found. Please Try Again!")
            return None
    
class SgPoolsWriter(SgPools):
    """A Class to write and store data
    """
    def __init__(self) -> None:
        super().__init__()
        self.LogWriteLoc = None 
        self.DataWriteLoc = None
    
    def setLog(self,LogWriteLog=None)->bool:
        if LogWriteLog == None:
            print(f"Invalid Logging Location")
            return False
    def setWriteLocation(self,Location = None) -> bool:
        if Location == None:
            print(f"Invalid Location")
            return False
        else:
            self.LogWriteLoc = Location
            return True
        
        
class LogsWriter(SgPoolsWriter):
    def __init__(self) -> None:
        super().__init__() 
    def setWriteLocation(Location=None) -> bool:
        return super().setWriteLocation()

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
    def SetWriter(self, Writer:SgPoolsWriter=None):
        self.Writer=Writer
        return None
    
    def GetWriter(self):
        if self.Writer==None:
            logging.critical(f"No Writer Set. Aborting GET Operation")
            return None
    
    # async def 
    async def ScrapeBet(self,EventText:str,BetType:str='match_details_pattern')->None:
        
        RegexParse = regex_bettype_filter(searchitem=BetType)
        BetDetails = None
        match BetType:
            case _:
                return None
        
        return None
    
    def Scrape(self) -> None:
        if self.Writer == None:
            logging.critical(f"No Writer Set. Aborting Scrape Operation")
            return 
        
        
        logging.basicConfig(filename=self.Writer.GetDir("Log"),encoding='utf-8', level=logging.DEBUG)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info("Current Time: " + current_time)
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(self.URL)
        # The above code is using Selenium WebDriver in Python to open a Chrome browser in headless
        # mode (without a visible browser window) and navigate to the specified `target_url`.
        
        # WebDriverWait(driver,20)
        time.sleep(15)
        
        
        # 10/6/24: Is this really necessary? pls fix
        # Get all bet types possible
        bet_type_specific = driver.find_element(By.XPATH, "//select[@class='form-control event-list__filter__market-sort']")
        bet_type_list=bet_type_specific.text.split('\n')
        # bet_type_list=bet_type_specific.json()
        # all_bet_list = {'bet_list':bet_type_list}
        # with open("sg_pools.json", "a") as json_file:
        #     json_file.write(json.dumps(all_bet_list))

        # testing_data = {"1/2 Goal": ["Sun, 21 Jan 2024", "12.30am", "1028", "Bordeaux vs Nice", "(+17)", "021/2 Goal", "01", "1.20", "Bordeaux +1.5 ", "02", "3.75", "Nice -1.5 ", "12.30am", "1024", "Valenciennes vs Paris FC", "(+15)", "021/2 Goal", "01", "1.12", "Valenciennes +1.5 ", "02", "4.80", "Paris FC -1.5 ", "1.00am", "1357", "Roma vs Verona", "(+17)", "461/2 Goal", "01", "2.30", "Roma -1.5 ", "02", "1.50", "Verona +1.5 "]}

        # allmonths=set(['Jan','Feb','Mar','Apr','May','Jun',
        #                 'Jul','Aug','Sep','Oct','Nov','Dec'])

    eventdate=None
    eventtime=None
    eventid=None
    AllEventStrings=[]
    toJson = {"Date":[],
              "EventID":[],
              "Events":{}}

    select_bet = Select(bet_type_specific)
    display_bet=driver.find_element(By.XPATH, "//button[@class='btn-block button button--orange btn btn-default']")
   
    regex_matching_implemented = ['1/2 Goal',"1X2","Halftime 1x2"]
    regex_matching_WIP = ["Asian Handicap/HT Asian Handicap","Halftime Total Goals","Handicap 1X2"]
    __regex_matching_ = ["1/2 Goal",
        "1st Goal Scorer",
        "1X2",
        "Asian Handicap/HT Asian Handicap",
        "Halftime 1x2",
        "Halftime Total Goals",
        "Halftime-Fulltime",
        "Handicap 1X2",
        "Last Goal Scorer",
        "Pick the Score",
        "Team to Score 1st Goal",
        "Total Goals",
        "Total Goals Odd/Even",
        "Total Goals Over/Under",
        "Will Both Teams Score"]
    
    
    for bet_type in bet_type_list:

            if (bet_type not in regex_matching_implemented) and (bet_type not in regex_matching_WIP):
                continue

        select_bet.select_by_visible_text(bet_type)
        # WebDriverWait(driver,3).until()
        display_bet.click()
        time.sleep(3) #Wait for elements to load
        
        # This doesnt always work. Try to understand why
        # try:
        #     # Adjust the locator and the timeout as needed
        #     element = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.XPATH, "//div[@class='event-list']//div[@class='event-list__group']"))
        #     )
        #     events = driver.find_elements(By.XPATH,"//div[@class='event-list']//div[@class='event-list__group']")
        # finally:
        #     pass
        # Bet Type may not always be available; Skip to next bet type
        try:
            # Load More Button
            load_button = driver.find_element(By.CLASS_NAME,"event-list__load-all-events")
        except: 
            continue
        load_button.click()

        time.sleep(1)
        more_bets = driver.find_elements(By.CLASS_NAME, "show-all")
        for more in more_bets:
            more.click()        
        time.sleep(5)
        events = driver.find_elements(By.XPATH,"//div[@class='event-list']//div[@class='event-list__group']")
        
            
        for event in events:
            
            # Strictly for testing purposes
            # if bet_type in regex_matching_implemented:
            #     continue
            
            # Also strictly for testing
            # if bet_type not in regex_matching_WIP:
            #     continue
            
            print(f"Starting to search for Bet Type of: {bet_type}")
            print(event.text)
            if bet_type not in regex_matching_implemented:
            
                # Only in production
                # continue 
            
                if bet_type in regex_matching_WIP:
                    pass
                    # print(event.text)
                # with open("sgpools_notimpl.txt","ab") as f:
                #     # text_without_line_breaks = event.text.replace("\\n", "")
                #     f.write(event.text.encode("utf-8"))
                #     # f.write("\n")
                    
                # continue
            isLiveGroup=re.findall(regex_bettype_filter('isLiveMatch',False),event.text,re.MULTILINE)
            
            # Ignore Live Matches First
            if len(isLiveGroup)==True:
                print("Ignored Matches")
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
                
                if bet_type not in regex_matching_implemented:
                    
                    if bet_type in regex_matching_WIP:
                        # print(f"{bet_type}")
                        # print(event.text)
                        pass
                        # print(event.text)
                    # with open("sgpools_notimpl.txt","ab") as f:
                    #     # text_without_line_breaks = event.text.replace("\\n", "")
                    #     f.write(event.text.encode("utf-8"))
                    #     # f.write("\n")
                        
                    # continue
                    
                isLiveGroup=re.findall(regex_bettype_filter('isLiveMatch',False),event.text,re.MULTILINE)
                
                # Ignore Live Matches First
                if len(isLiveGroup)==True:
                    print("Ignored Matches")
                    continue

                eventdate_groups=re.findall(regex_bettype_filter('date_pattern1',False),event.text,re.MULTILINE)
                if len(eventdate_groups)>1:
                    logging.warning(f"Parsed info contains more than 1 event date. {eventdate_groups}. Only first event date is taken.")
                evdate = eventdate_groups[0]
                if evdate not in toJson["Date"]:
                    toJson["Date"].append(evdate)
                
                if (bet_type in regex_matching_implemented) or (bet_type in regex_matching_WIP):
                    details_regex_group = re.findall(regex_bettype_filter('match_details_pattern', False),event.text)
                    # print("details_regex_group")
                    # print(details_regex_group)
                    # eventdate,matchdata,oddsdata=event_filter(event.text,bet_type)

                if len(details_regex_group) == 0:
                    continue 
                    
                for event_detail_grouped in details_regex_group:
                    eventtime,eventid,hometeam,awayteam = event_detail_grouped
                    
                    
                    if eventid not in toJson["EventID"]:
                        toJson["EventID"].append(eventid)
                        toJson["Events"][eventid] = {}
                        logging.info(f"Added Event {eventid} into toJson")
                        
                        # toJson["Date"][evdate]["EventID"] = {eventid}
                    
                    if "Date" not in toJson["Events"][eventid].keys():
                        toJson["Events"][eventid]["Date"] = evdate
                        toJson["Events"][eventid]["Time"] = eventtime
                        toJson["Events"][eventid]["Matchup"] = f"{hometeam} vs {awayteam}"
                
                match bet_type:
                    case "1/2 Goal":
                        # continue
                        betdetails = re.findall(regex_bettype_filter('1/2 Goal',False),event.text,re.MULTILINE)
                        for eventid,homeodds,awayodds in betdetails:
                            
                            try:
                                toJson["Events"][eventid]["1/2 Goal"] = {}
                                
                                toJson["Events"][eventid]["1/2 Goal"]["HomeOdds"] = homeodds
                                toJson["Events"][eventid]["1/2 Goal"]["AwayOdds"] = awayodds 
                            except:
                                logging.warning(f"Fail to insert Odds ({homeodds},{awayodds}) for {eventid}")
                    case "1X2"|"Halftime 1x2":
                        # continue
                        betdetails = re.findall(regex_bettype_filter('1X2'),event.text,re.MULTILINE)
                        for eventid,homeodds,drawodds,awayodds in betdetails:
                            try: 
                                toJson["Events"][eventid][bet_type] = {}
                                toJson["Events"][eventid][bet_type]["HomeOdds"] = homeodds
                                toJson["Events"][eventid][bet_type]["DrawOdds"] = drawodds
                                toJson["Events"][eventid][bet_type]["AwayOdds"] = awayodds
                            except:
                                logging.warning(f"Fail to insert Odds ({homeodds},{drawodds},{awayodds}) for {eventid} for {bet_type}")                               
                    case "Asian Handicap/HT Asian Handicap":
                        # continue
                    
                        # WIP: Not fully implemented
                        
                        betdetails = re.findall(regex_bettype_filter('Asian Handicap/HT Asian Handicap'),event.text,re.MULTILINE)
                        print("Asian Handicap/HT Asian Handicap")
                        print(event.text)
                        print(betdetails)

                        # print("1X2")
                        # print(betdetails)
                    case "Handicap 1X2":
                        continue
                        # betdetails = re.findall(regex_bettype_filter('Handicap 1X2'),event.text,re.MULTILINE)
                        print("Handicap 1X2")
                        print(event.text)
                        
                        # print(betdetails)
                    
            events_text = {bet_type : event.text.split('\n')}
            # events_text = {bet_type : event.json()}
            with open("sg_pools2.json",'a') as json_file:
                json_file.write(json.dumps(events_text))

        with open("sgpools3.json",'w') as json_file:
            json_file.write(json.dumps(toJson))

        driver.close()

    
        return None
    
    
if __name__ == "__main__":


    Scraper = SgPoolsScraper()
    Writer = SgPoolsWriter()
    Writer.SetDir(directory="sgpools_datacleaning.log",dirtype="Log")
    # Writer.SetDir(directory="sgpools_datacleaning.log",dirtype="Scrape")
    Writer.SetDir(directory="sg_pools.json",dirtype="Json")
    
    input("Initate successful. Press any key to continue")
    Scraper.SetWriter(Writer=Writer)
    Scraper.Scrape()
    

    # logging.basicConfig(filename="sgpools_datacleaning.log",encoding='utf-8', level=logging.DEBUG)
    # current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # logging.info("Current Time: " + current_time)

    # target_url = "https://online.singaporepools.com/en/sports/category/1/football"

    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # driver = webdriver.Chrome(options=options)  
    # driver.get(target_url)

    # #writes pure bet values
    # with open("sg_pools2.json", "w") as json_file:
    #     json_file.write("")

    # #writes only bet types
    # with open("sg_pools.json", "w") as json_file:
    #     json_file.write("")

    # # WebDriverWait(driver,20)
    # time.sleep(30)

    # # Get all bet types possible
    # bet_type_specific = driver.find_element(By.XPATH, "//select[@class='form-control event-list__filter__market-sort']")
    # bet_type_list=bet_type_specific.text.split('\n')
    # # bet_type_list=bet_type_specific.json()
    # all_bet_list = {'bet_list':bet_type_list}
    # with open("sg_pools.json", "a") as json_file:
    #     json_file.write(json.dumps(all_bet_list))

    # testing_data = {"1/2 Goal": ["Sun, 21 Jan 2024", "12.30am", "1028", "Bordeaux vs Nice", "(+17)", "021/2 Goal", "01", "1.20", "Bordeaux +1.5 ", "02", "3.75", "Nice -1.5 ", "12.30am", "1024", "Valenciennes vs Paris FC", "(+15)", "021/2 Goal", "01", "1.12", "Valenciennes +1.5 ", "02", "4.80", "Paris FC -1.5 ", "1.00am", "1357", "Roma vs Verona", "(+17)", "461/2 Goal", "01", "2.30", "Roma -1.5 ", "02", "1.50", "Verona +1.5 "]}

    # allmonths=set(['Jan','Feb','Mar','Apr','May','Jun',
    #                 'Jul','Aug','Sep','Oct','Nov','Dec'])

    # eventdate=None
    # eventtime=None
    # eventid=None
    # AllEventStrings=[]
    # toJson = {"Date":[],
    #           "EventID":[],
    #           "Events":{}}

    # select_bet = Select(bet_type_specific)
    # display_bet=driver.find_element(By.XPATH, "//button[@class='btn-block button button--orange btn btn-default']")
   
    # regex_matching_implemented = ['1/2 Goal',"1X2","Halftime 1x2"]
    # regex_matching_WIP = ["Asian Handicap/HT Asian Handicap","Halftime Total Goals"]
    # __regex_matching_ = ["1/2 Goal",
    #     "1st Goal Scorer",
    #     "1X2",
    #     "Asian Handicap/HT Asian Handicap",
    #     "Halftime 1x2",
    #     "Halftime Total Goals",
    #     "Halftime-Fulltime",
    #     "Handicap 1X2",
    #     "Last Goal Scorer",
    #     "Pick the Score",
    #     "Team to Score 1st Goal",
    #     "Total Goals",
    #     "Total Goals Odd/Even",
    #     "Total Goals Over/Under",
    #     "Will Both Teams Score"]
    
    
    # for bet_type in bet_type_list:

    #     if (bet_type not in regex_matching_implemented) and (bet_type not in regex_matching_WIP):
    #         continue

    #     select_bet.select_by_visible_text(bet_type)
    #     display_bet.click()
    #     time.sleep(3) #Wait for elements to load
        

    #     # Bet Type may not always be available; Skip to next bet type
    #     try:
    #         # Load More Button
    #         load_button = driver.find_element(By.CLASS_NAME,"event-list__load-all-events")
    #         load_button.click()
    #     except: 
    #         continue
        
            
    #     time.sleep(5)

    #     more_bets = driver.find_elements(By.CLASS_NAME, "show-all")
    #     for more in more_bets:
    #         more.click()
            
        
    #     time.sleep(5)
                    
    #     events = driver.find_elements(By.XPATH,"//div[@class='event-list']//div[@class='event-list__group']")
        
            
    #     for event in events:
            
    #         if bet_type not in regex_matching_implemented:
                
    #             if bet_type in regex_matching_WIP:
    #                 pass
    #                 # print(event.text)
    #             # with open("sgpools_notimpl.txt","ab") as f:
    #             #     # text_without_line_breaks = event.text.replace("\\n", "")
    #             #     f.write(event.text.encode("utf-8"))
    #             #     # f.write("\n")
                    
    #             # continue
                
    #         isLiveGroup=re.findall(regex_bettype_filter('isLiveMatch',False),event.text,re.MULTILINE)
            
    #         # Ignore Live Matches First
    #         if len(isLiveGroup)==True:
    #             print("Ignored Matches")
    #             continue

    #         eventdate_groups=re.findall(regex_bettype_filter('date_pattern1',False),event.text,re.MULTILINE)
    #         if len(eventdate_groups)>1:
    #             logging.warning(f"Parsed info contains more than 1 event date. {eventdate_groups}. Only first event date is taken.")
    #         evdate = eventdate_groups[0]
    #         if evdate not in toJson["Date"]:
    #             toJson["Date"].append(evdate)
            
    #         if (bet_type in regex_matching_implemented) or (bet_type in regex_matching_WIP):
    #             details_regex_group = re.findall(regex_bettype_filter('match_details_pattern', False),event.text)
    #             # print("details_regex_group")
    #             # print(details_regex_group)
    #             # eventdate,matchdata,oddsdata=event_filter(event.text,bet_type)

    #             if len(details_regex_group) == 0:
    #                 continue 
                    
    #             for event_detail_grouped in details_regex_group:
    #                 eventtime,eventid,hometeam,awayteam = event_detail_grouped
                    
                    
    #                 if eventid not in toJson["EventID"]:
    #                     toJson["EventID"].append(eventid)
    #                     toJson["Events"][eventid] = {}
    #                     logging.info(f"Added Event {eventid} into toJson")
                        
    #                     # toJson["Date"][evdate]["EventID"] = {eventid}
                    
    #                 if "Date" not in toJson["Events"][eventid].keys():
    #                     toJson["Events"][eventid]["Date"] = evdate
    #                     toJson["Events"][eventid]["Time"] = eventtime
    #                     toJson["Events"][eventid]["Matchup"] = f"{hometeam} vs {awayteam}"
                
    #             match bet_type:
    #                 case "1/2 Goal":
    #                     continue
    #                     betdetails = re.findall(regex_bettype_filter('1/2 Goal',False),event.text,re.MULTILINE)
    #                     for eventid,homeodds,awayodds in betdetails:
                            
    #                         try:
    #                             toJson["Events"][eventid]["1/2 Goal"] = {}
                                
    #                             toJson["Events"][eventid]["1/2 Goal"]["HomeOdds"] = homeodds
    #                             toJson["Events"][eventid]["1/2 Goal"]["AwayOdds"] = awayodds 
    #                         except:
    #                             logging.warning(f"Fail to insert Odds ({homeodds},{awayodds}) for {eventid}")
    #                 case "1X2"|"Halftime 1x2":
    #                     continue
    #                     betdetails = re.findall(regex_bettype_filter('1X2'),event.text,re.MULTILINE)
    #                     for eventid,homeodds,drawodds,awayodds in betdetails:
    #                         try: 
    #                             toJson["Events"][eventid][bet_type] = {}
    #                             toJson["Events"][eventid][bet_type]["HomeOdds"] = homeodds
    #                             toJson["Events"][eventid][bet_type]["DrawOdds"] = drawodds
    #                             toJson["Events"][eventid][bet_type]["AwayOdds"] = awayodds
    #                         except:
    #                             logging.warning(f"Fail to insert Odds ({homeodds},{drawodds},{awayodds}) for {eventid} for {bet_type}")
                                
    #                 case "Asian Handicap/HT Asian Handicap":
    #                     print("Asian Handicap/HT Asian Handicap")
    #                     print(event.text)

    #                     # print("1X2")
    #                     # print(betdetails)


    #         events_text = {bet_type : event.text.split('\n')}
    #         # events_text = {bet_type : event.json()}
    #         with open("sg_pools2.json",'a') as json_file:
    #             json_file.write(json.dumps(events_text))

    # with open("sgpools3.json",'w') as json_file:
    #     json_file.write(json.dumps(toJson))

    # driver.close()
