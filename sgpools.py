

import numpy as np 
# import pandas as pd
import time
import datetime
import json
import logging 
import re
import asyncio
import threading

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome

from functools import cache,cached_property

from utils_sgpools.sgpools_regex_utils import regex_bettype_filter,event_filter

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
        
        self._BetTypes=[
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
        self._LogDir=None
        self._ScrapeDir=None
        self._toJson=None
        self._JsonDict=None # Declared at SgPoolsScraper class (Constructor class)
        self._lock = threading.Lock()  # Initialize a lock for thread safety
        
    def SetDir(self,directory:str="",dirtype:str="")->None:
        
        match dirtype:
            case "Log":
                self._LogDir = directory 
            case "Scrape":
                self._ScrapeDir=directory
            case "Json":
                self._toJson=directory
            # case _ :
            #     print(f"Invalid Directory Type Set. Aborting
            #           Writing Directory Setter Operations")
        
        return None
    
    def GetDir(self,dirtype:str="")->str:
        match dirtype:
            case "Log":
                return self._LogDir
            case "Scrape":
                return self._ScrapeDir
            case "Json":
                return self._toJson
            # case __ :
            #     print(f"Invalid Directory Type Set. Aborting
            #           Writing Directory Setter Operations")
    
    def GetJsonDict(self):
        return self._JsonDict
    
    def Clear(self):
        with open(self._toJson,"w") as json_file:
            json_file.write("")

    def Save(self):
        with self._lock:  # Acquire the lock before writing to the file
            with open(self._toJson, "a") as json_file:
                json_file.write(json.dumps(self._JsonDict))
    
    async def WriteBet(self,ParsedData:list[str],BetType:str):
        pass 


    
class SgPoolsScraper(SgPools):
    """A Generic Class to Scrape defined terms
    """
    def __init__(self) -> None:
        super().__init__()
        self._Writer = None
        self._regex_matching_implementated=[
            '1/2 Goal',
            "1X2",
            "Halftime 1x2"
        ]
        self._regex_matching_WIP=[ 
            "Asian Handicap/HT Asian Handicap",
            "Halftime Total Goals"
        ]

    def SetBetType(self,BetType:str)->None:
        if BetType not in self.__BetTypes:
            print(f"BetType: {BetType} not found. Please Try Again!")
            logging.warning(f"BetType: {BetType} not found. Please Try Again!")
            return None
    
    def SetWriter(self, Writer:SgPoolsWriter=None):
        self._Writer=Writer
        # self._Writer.Clear() #Clears the Json Data from previous runs of file. #MOVED TO MAIN()
        self._Writer._JsonDict={"Date":[],
                                "EventID":[],
                                "Events":{}}
        return None
    
    def GetWriter(self):
        if self._Writer==None:
            logging.critical(f"No Writer Set. Aborting GET Operation")
            return None
        return self._Writer
    
    # def BetTypeSelector(self):
    
    async def DriverInit(self,options):
        #TODO: implement options here
        self._options = webdriver.ChromeOptions()
        self._options.add_argument("--headless")
        self._driver = webdriver.Chrome(options=self._options)

        self._driver.get(self.URL)
        time.sleep(15)

        return self._driver

    async def ScrapeBet(self,
                        EventText:str,
                        BetType:str='match_details_pattern')->None:
        
        RegexParse = regex_bettype_filter(searchitem=BetType)
        BetDetails = None

        #TODO 06/08/2024: driver selemnium webelement must be set as attribute of class.ither here or parent
        
        # Finds the dropdown option for different bet type
        bet_type_selector = self._driver.find_element(
            By.XPATH, "//select[@class='form-control event-list__filter__market-sort']")
        # #TODO: Evaluate if this is needed at all
        # bet_type_list=bet_type_specific.text.split('\n')
        
        # Selector selects the bet type based on Bet Category (1X2, Total Goals, etc)      
        select_bet = Select(bet_type_selector).select_by_visible_text(
            EventText
        )

        try:
        # Load More Button
            load_button = self._driver.find_element(By.CLASS_NAME,"event-list__load-all-events")
            load_button.click()
        except: 
            pass

        
        # Clicks on the display bet button to load the bet details
        display_bet=self._driver.find_element(
            By.XPATH, "//button[@class='btn-block button button--orange btn btn-default']")
        display_bet.click()

        #wait for elements to appear
        time.sleep(15.0) 

        # Gets all group of events 
        events = self._driver.find_elements(
            By.XPATH,"//div[@class='event-list']//div[@class='event-list__group']")
        for event in events:
            # Gets individual events

            # TODO: Assess if Live Events need to be parsed 
            # Finds Live Matches and Ignore them
            isLiveGroup=re.findall(regex_bettype_filter('isLiveMatch',False),
                                   event.text,re.MULTILINE)
            if len(isLiveGroup)==True:
                print("Ignored Matches")
                continue

            # Parsing of HTML element proper
            eventdate_groups=re.findall(regex_bettype_filter('date_pattern1',False),
                                        event.text,re.MULTILINE)
            if len(eventdate_groups)>1:
                logging.warning(f"Parsed info contains more than 1 event date. {eventdate_groups}. Only first event date is taken.")
            
            evdate = eventdate_groups[0]
            if evdate not in self._Writer._JsonDict["Date"]:
                self._Writer._JsonDict["Date"].append(evdate)

            await self.ScrapeSpecificBet(event,evdate,BetType)


    async def ScrapeSpecificBet(
            self,
            event,
            eventdate, #Variable : evdate
            BetType:str='match_details_pattern'):


        #TODO: Check if this section should be here or ScrapeBet
        details_regex_group = re.findall(
            regex_bettype_filter(
                'match_details_pattern',
                False),
            event.text)
        if len(details_regex_group) == 0:
            return None
        for event_detail_grouped in details_regex_group:
            eventtime,eventid,hometeam,awayteam = event_detail_grouped
        
            if eventid not in self._Writer._JsonDict["EventID"]:
                self._Writer._JsonDict["EventID"].append(eventid)
                self._Writer._JsonDict["Events"][eventid] = {}
                logging.info(f"Added Event {eventid} into toJson")
                            
            if "Date" not in self._Writer._JsonDict["Events"][eventid].keys():
                self._Writer._JsonDict["Events"][eventid]["Date"] = eventdate
                self._Writer._JsonDict["Events"][eventid]["Time"] = eventtime
                self._Writer._JsonDict["Events"][eventid]["Matchup"] = f"{hometeam} vs {awayteam}"



        match BetType:
            case "1/2 Goal":
                betdetails = re.findall(regex_bettype_filter('1/2 Goal',False),
                                        event.text,
                                        re.MULTILINE)
                for eventid,homeodds,awayodds in betdetails:
                    
                    try:
                        self._Writer._JsonDict["Events"][eventid]["1/2 Goal"] = {}
                        self._Writer._JsonDict["Events"][eventid]["1/2 Goal"]["HomeOdds"] = homeodds
                        self._Writer._JsonDict["Events"][eventid]["1/2 Goal"]["AwayOdds"] = awayodds 
                    except:
                        logging.warning(f"Fail to insert Odds ({homeodds},{awayodds}) for {eventid}")
            
            # TODO: Figure out which one is the correct one
            case "1X2"|"Halftime 1x2":
                betdetails = re.findall(regex_bettype_filter('1X2'),event.text,re.MULTILINE)
                for eventid,homeodds,drawodds,awayodds in betdetails:
                    try: 
                        self._Writer._JsonDict["Events"][eventid][BetType] = {}
                        self._Writer._JsonDict["Events"][eventid][BetType]["HomeOdds"] = homeodds
                        self._Writer._JsonDict["Events"][eventid][BetType]["DrawOdds"] = drawodds
                        self._Writer._JsonDict["Events"][eventid][BetType]["AwayOdds"] = awayodds
                    except:
                        logging.warning(f"Fail to insert Odds ({homeodds},{drawodds},{awayodds}) for {eventid} for {BetType}")

            # case "1X2"|"Halftime 1x2":
            #     betdetails = re.findall(regex_bettype_filter('1X2'),event.text,re.MULTILINE)
            #     for eventid,homeodds,drawodds,awayodds in betdetails:
            #         try: 
            #             self._Writer["Events"][eventid][BetType] = {}
            #             self._Writer["Events"][eventid][BetType]["HomeOdds"] = homeodds
            #             self._Writer["Events"][eventid][BetType]["DrawOdds"] = drawodds
            #             self._Writer["Events"][eventid][BetType]["AwayOdds"] = awayodds
            #         except:
            #             logging.warning(f"Fail to insert Odds ({homeodds},{drawodds},{awayodds}) for {eventid} for {bet_type}")
            # case "Asian Handicap/HT Asian Handicap":
            #     print("Logging Details for Asian Handicap Matches")
            #     betdetails=re.findall(regex_bettype_filter('Asian Handicap'),event.text,re.MULTILINE)
            #     if len(betdetails)==0:
            #         logging.warning(f"Betdetails for {bet_type} not found.")
                
            #     print(betdetails)
            #     for eventid, homeodds, homehandicap, awayodds, awayhandicap in betdetails:
            #         try:
            #             toJson["Events"][eventid][bet_type] = {}
            #             toJson["Events"][eventid][bet_type]["HomeOdds"] = homeodds
            #             toJson["Events"][eventid][bet_type]["HomeHandicap"] = homehandicap
            #             toJson["Events"][eventid][bet_type]["AwayOdds"] = awayodds
            #             toJson["Events"][eventid][bet_type]["AwayHandicap"] = awayhandicap
            #         except:
            #             logging.warning(f"Fail to insert Odds ({homeodds},{homehandicap},{awayodds},{awayhandicap}) for {eventid} for {bet_type}")
                    
                
            #     # print("Asian Handicap/HT Asian Handicap")
            #     # print(event.text)

            #     # print("1X2")
            #     # print(betdetails)


            case _:
                print(f"Error. {BetType} Not Implemented")
                return None
        
        return None
    
    def ScrapeBetRun(self):



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

        # 10/6/24: Is this really necessary? pls fix
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
        regex_matching_WIP = ["Asian Handicap/HT Asian Handicap","Halftime Total Goals"]
        for bet_type in bet_type_list:

            if (bet_type not in regex_matching_implemented) and (bet_type not in regex_matching_WIP):
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
                            continue
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
                            print("Logging Details for Asian Handicap Matches")
                            betdetails=re.findall(regex_bettype_filter('Asian Handicap'),event.text,re.MULTILINE)
                            if len(betdetails)==0:
                                logging.warning(f"Betdetails for {bet_type} not found.")
                            
                            print(betdetails)
                            for eventid, homeodds, homehandicap, awayodds, awayhandicap in betdetails:
                                try:
                                    toJson["Events"][eventid][bet_type] = {}
                                    toJson["Events"][eventid][bet_type]["HomeOdds"] = homeodds
                                    toJson["Events"][eventid][bet_type]["HomeHandicap"] = homehandicap
                                    toJson["Events"][eventid][bet_type]["AwayOdds"] = awayodds
                                    toJson["Events"][eventid][bet_type]["AwayHandicap"] = awayhandicap
                                except:
                                    logging.warning(f"Fail to insert Odds ({homeodds},{homehandicap},{awayodds},{awayhandicap}) for {eventid} for {bet_type}")
                                
                            
                            # print("Asian Handicap/HT Asian Handicap")
                            # print(event.text)

                            # print("1X2")
                            # print(betdetails)


                events_text = {bet_type : event.text.split('\n')}
                # events_text = {bet_type : event.json()}
                with open("sg_pools2.json",'a') as json_file:
                    json_file.write(json.dumps(events_text))

        with open("sgpools3.json",'w') as json_file:
            json_file.write(json.dumps(toJson))

        driver.close()

    
        return None
    


def main():
    Writer = SgPoolsWriter()
    Writer.SetDir(directory="sgpools_datacleaning.log",dirtype="Log")
    Writer.SetDir(directory="sg_pools.json",dirtype="Json")
    Writer.Clear()

    Implemented_BetTypes = [
        "1X2",
        "Asian Handicap/HT Asian Handicap",
        "Halftime 1x2",
        "1/2 Goal"
    ]

    async def AsyncSgPools(BetType:str,Writer:SgPoolsWriter):
        Scraper = SgPoolsScraper()
        Scraper.SetWriter(Writer=Writer)
        await Scraper.DriverInit(options=None)
        starttime = time.time()
        print(f"Started Scraping: {BetType}, Start Time: {starttime}")
        await Scraper.ScrapeBet(BetType)
        await asyncio.to_thread(Scraper._Writer.Save)
        print(f"Finished Scraping: {BetType}, Start Time: {starttime}, "
              f"End Time: {time.time()}, Total Elapsed Time: {time.time()-starttime}")

    async def AsyncSgPoolsTask():
        tasks = []
        for bet_type in Implemented_BetTypes:
            tasks.append(asyncio.create_task(AsyncSgPools(bet_type, Writer)))
        await asyncio.gather(*tasks)

        await asyncio.to_thread(Writer.Save)

    asyncio.run(AsyncSgPoolsTask())
    print("Job Done")

    return None 
    
if __name__ == "__main__":

    main()

    # Scraper = SgPoolsScraper()
    # Writer = SgPoolsWriter()
    # Writer.SetDir(directory="sgpools_datacleaning.log",dirtype="Log")
    # # Writer.SetDir(directory="sgpools_datacleaning.log",dirtype="Scrape")
    # Writer.SetDir(directory="sg_pools.json",dirtype="Json")
    
    # # input("Initate successful. Press any key to continue")
    # Scraper.SetWriter(Writer=Writer)
    # Writer._Writer.Clear()
    # Scraper.DriverInit(options=None)
    # Scraper.Scrape()
    # asyncio.run(Scraper.ScrapeBet("1X2"))
    # asyncio.run(Scraper.ScrapeBet("Asian Handicap/HT Asian Handicap"))
    # asyncio.run(Scraper.ScrapeBet("Halftime 1x2"))
    # asyncio.run(Scraper.ScrapeBet("1/2 Goal"))
    
    # Scraper._Writer.Save()

    