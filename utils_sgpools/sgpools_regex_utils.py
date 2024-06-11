
# Provide Regex Pattern Matching for SgPools Scraping


import re
from functools import cache

@cache
def regex_bettype_filter(searchitem:str, complex_pattern:bool=False):

    """Returns regex pattern to search for

    Args:
        bettype (str): _description_
    """
    
    #Betting Types
    if searchitem=='match_info'and complex_pattern==True:
        return re.compile(r'^(\d+\.\d{2}\w{2})\s(\d{4})\n([\w|\s]+?)\svs\s([\w|\s]+?)\s',re.MULTILINE)
    
    if searchitem=='1/2 Goal' and complex_pattern==True:

        # Group 1: Event Time
        # Group 2: Event ID
        # Group 3: Team1 name
        # Group 4: Team2 name
        # Group 5: Team1 odds
        # Group 6: Team1 handicap
        # Group 7: Team2 odds
        # Group 8: Team2 handicap
    # match_info_pattern=r'(\d\.\d{2}\w{2})\n(\d{4})\n([\w|\s]+)\svs\s([\w|\s]+)*'
    # odds_pattern=r'\s\n(\d{2})\n(\d+\.\d+)\n([\w\s]+ [-+]\d+\.\d+)'

        return re.compile(r'(\d\.\d{2}\w{2})\n(\d{4})\n([\w|\s]+)\svs\s([\w|\s]+)*\n.{23}(.{4}).{2}(?:[\w|\s]+)(.{4}).{7}(.{4})\n(?:[\w|\s]+)(.{4})',re.MULTILINE)
    
    
    #Event Types
    # match searchitem:
    #     case 'date_pattern':
    #         return re.compile(r'^(\w{3}, \d{2} \w{3} \d{4})$',re.MULTILINE)
    #     case 'time_pattern':
    #         return re.compile(r'(\d\.\d+\w{2})',re.MULTILINE)
    #     case _:
    #         return re.compile(r'^(\w{3}, \d{2} \w{3} \d{4})$',re.MULTILINE)
        
    # return pattern_to_return
    
                  
    match searchitem:
        case 'date_pattern':
            return re.compile(r'^(\w{3}, \d{2} \w{3} \d{4})$',re.MULTILINE)
        case 'time_pattern':
            return re.compile(r'(\d\.\d+\w{2})',re.MULTILINE)
        case 'match_pattern':
            return re.compile(r'(\d{4})\\',re.MULTILINE)
        case 'teams_pattern':
            return re.compile(r'^([\w\s]+) vs ([\w\s]+)$',re.MULTILINE)
        case 'odds_pattern':
            return re.compile(r'^(\d{2})\n(\d+\.\d+)\n([\w\s]+ [-+]\d+\.\d+)\s\n(\d{2})\n(\d+\.\d+)\n([\w\s]+ [-+]\d+\.\d+)$',re.MULTILINE)
        
        case 'isLiveMatch': return r'\(Live\)'
        
        case '1X2': return r'(\d{4})\n.*?\n01\n([\d.]*)\n02\n([\d.]*)\n03\n([\d.]*)'
        # case '1/2 Goal3': return r'\n01\n([\d|\.]*).*?\n02\n([\d|\.]*)'
        # case '1/2 Goal3': return r'\n01\n([\d.]*).*?\n.*?\n.*?\n([\d.]*)'
        # # case '1/2 Goal2': return r'\n(\d{4})\n.*?Goal\n01\n([\d.]+)'
        # This is the working one (i think)
        case '1/2 Goal': return r'(\d{4})\n.*?\n.*?\n.*?(?:1/2 Goal\n01\n([\d.]*)).*?\n.*?\n.*?\n([\d.]*)'
        # # case '1/2 Goal2': return r'\n01\n([\d|\.]*)'
        # case '1/2 Goal1':
        #     return r'\n01\n([\d|\.]*).+?\n02\n([\d|\.]*)'
        # case '1/2 Goal':
        #     # Returns groups of (matchID,home_odds, away_odds)
        #     # return r'm\n(\d{4}).+?\n01\n([\d|\.]*)'
        #     return r'm(?:\n|\s)(\d{4}).+?\n01\n([\d|\.]*).+?\n02\n([\d|\.]*)'
        #     # return re.compile(r'^0[1|2]\n(\d*\.\d*)\n[\w\s]* ([\+|\-][\d|\.]*)*',re.MULTILINE)
        case 'Asian Handicap': return r'\n(\d{4})\n.*?(?:Asian Handicap)'
        
        case 'date_pattern1':
            return r'(\w*, \d* \w* \d{4})'
        case 'match_details_pattern':
            # Returns List[ Set(Time, Event ID, Home Team, Away Team) ]
            return r'(\d*\.\d{2}\w{2})[\n\s](\d{4})[\n\s]([\w\s]*) vs ([\w\s]*)\n'
        case _ :
            print("False")
            return
    
    # if searchitem=='date_pattern':
    #     return re.compile(r'^(\w{3}, \d{2} \w{3} \d{4})$',re.MULTILINE)
    # if searchitem=='time_pattern':
    #     return re.compile(r'(\d\.\d+\w{2})',re.MULTILINE)
    # if searchitem=='match_pattern':
    #     return re.compile(r'(\d{4})\\',re.MULTILINE)
    # if searchitem=='teams_pattern':
    #     return re.compile(r'^([\w\s]+) vs ([\w\s]+)$',re.MULTILINE)
    # if searchitem=='odds_pattern':
    #     return re.compile(r'^(\d{2})\n(\d+\.\d+)\n([\w\s]+ [-+]\d+\.\d+)\s\n(\d{2})\n(\d+\.\d+)\n([\w\s]+ [-+]\d+\.\d+)$',re.MULTILINE)
    
    # if searchitem=='1/2 Goal':
    #     return re.compile(r'^0[1|2]\n(\d*\.\d*)\n[\w\s]* ([\+|\-][\d|\.]*)*',re.MULTILINE)
    
    # if searchitem=='match_details_pattern':
    #     return r'(\d*\.\d{2}\w{2}) (\d{4})\n([\w\s]*) vs ([\w\s]*)'
    
    
    
    
    # if searchitem=='time_pattern':
    #     return r'^(\d{1,2}.\d{2}(am|pm))$'
    
def event_filter (event_string:str,bettype:str="Default") -> tuple():

    """ 
    Cthulhu Below:` 
    ^(\w{3}, \d{2} \w{3} \d{4})\n(\d\.\d{2}\w{2})\n(\d{4})\n([\w|\s]+)\svs\s([\w|\s]+)*\n.{23}(.{4})\n(?:[\w|\s]+)(.{4}).{7}(.{4})\n(?:[\w|\s]+)(.{4})

    Explanation: 
        ^(\w{3}, \d{2} \w{3} \d{4}): {Date}
        (\d\.\d{2}\w{2})\n(\d{4}): {Time} and {Event} ID Matching
        ([\w|\s]+)\svs\s([\w|\s]+)*: {Home} team vs {Away} team
        \n.{23}(.{4}): 
            Home Team 1/2 goal odds generally follow this form:
            \n(+17)\n461/2 Goal\n01\n4.80
            captures {4.80}
            Might need to be more robust
        More to be done later.
        
        
    Cthulhu 2:
    (\d\.\d{2}\w{2})\n(\d{4})\n([\w|\s]+)\svs\s([\w|\s]+)*\n.{23}(.{4}).{2}(?:[\w|\s]+)(.{4}).{7}(.{4})\n(?:[\w|\s]+)(.{4})
    (\d\.\d{2}\w{2})\n(\d{4})\n([\w|\s]+)\svs\s([\w|\s]+)*\n.{23}(.{4}).{2}(?:[\w|\s]+)(.{4}).{7}(.{4})\n(?:[\w|\s]+)(.{4})
    
    (\d*\.\d{2}\w{2})\s(\d{4})\n([\w|\s]*)\svs\s([\w|\s]*)\s : Match Info
    \n.{23}(.{4}).{2}(?:[\w|\s]+)(.{4}).{7}(.{4})\n(?:[\w|\s]+)(.{4}) : Odds Part
    """

    date_pattern = r'^(\w{3}, \d{2} \w{3} \d{4})$'
    time_pattern = r'^(\d{1,2}.\d{2}(am|pm))$'
    match_pattern = r'^(\d+)$'
    teams_pattern = r'^([\w\s]+) vs ([\w\s]+)$'
    # handicap_pattern = r'^\(([-+]?\d+)\)$'
    # score_pattern = r'^(\d+)/(\d+)\s([\w\s]+)$'
    
    match_info_pattern=r'^(\d\.\d{2}\w{2})\n(\d{4})\n([\w|\s]+)\svs\s([\w|\s]+)*'
    odds_pattern=r'^\s\n(\d{2})\n(\d+\.\d+)\n([\w\s]+ [-+]\d+\.\d+)'
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
        
        # logging.info(f"{team1} vs {team2} for {bettype} at {home_odds};{away_odds}")
        return date_of,time_of,match_id,team1,team2, home_handicap, home_odds, away_odds

    elif bettype=="Default":
        return date_of,time_of,match_id,team1,team2, None, None, None
        


if __name__ == "__main__":

    TestString='Sat, 16 Mar 2024\n10.30pm 3589\nDarmstadt vs Bayern Munich (Live)\n01\n-.--\n02\n-.--\n03\n-.--\n10.30pm 3576\nHeidenheim vs Monchengladbach (Live)\n01\n9.50\n02\n3.60\n03\n1.37\n10.30pm 3550\nMainz vs Bochum (Live)\n01\n1.23\n02\n4.30\n03\n12.00\n10.30pm 3548\nWolfsburg vs Augsburg (Live)\n01\n-.--\n02\n-.--\n03\n-.--\n11.00pm 3714\nBurnley vs Brentford (Live)\n01\n1.17\n02\n5.00\n03\n16.00\n11.00pm 3754\nLuton vs Nottingham (Live)\n01\n6.50\n02\n3.75\n03\n1.45\n11.00pm 3695\nWest Bromwich vs Bristol City (Live)\n01\n1.17\n02\n5.00\n03\n16.00\n11.15pm 3551\nOsasuna vs Real Madrid (Live)\n01\n13.00\n02\n5.20\n03\n1.17\n11.15pm 3708\nEibar vs Villarreal (B) (Live)\n01\n1.67\n02\n2.90\n03\n5.20'

    TESTONEXTWO='Tue, 2 Apr 2024\n12.00am\n1348\nLecce vs Roma\n(+17)\n021/2 Goal\n01\n1.23\nLecce +1.5 \n02\n3.50\nRoma -1.5 \n12.30am\n1850\nIpswich vs Southampton\n(+17)\n461/2 Goal\n01\n4.80\nIpswich -1.5 \n02\n1.12\nSouthampton +1.5 \n1.15am\n6244\nViking FK vs Sarpsborg\n(+15)\n461/2 Goal\n01\n2.60\nViking FK -1.5 \n02\n1.40\nSarpsborg +1.5 \n2.45am\n1347\nInter vs Empoli\n(+17)\n461/2 Goal\n01\n1.50\nInter -1.5 \n02\n2.30\nEmpoli +1.5 \n3.00am\n1882\nLeeds vs Hull City\n(+17)\n461/2 Goal\n01\n2.05\nLeeds -1.5 \n02\n1.63\nHull City +1.5 \n3.00am\n1597\nVillarreal vs Atletico Madrid\n(+17)\n021/2 Goal\n01\n1.20\nVillarreal +1.5 \n02\n3.75\nAtletico Madrid -1.5 '


    date_regex_group = re.findall(regex_bettype_filter('date_pattern1', False),TestString,re.MULTILINE)
    print("Collated Date Details")
    print(date_regex_group)
    
    details_regex_group = re.findall(regex_bettype_filter('match_details_pattern', False),TestString,re.MULTILINE)
    print("Collated Match Details")
    print(details_regex_group)

    details_regex_group = re.findall(regex_bettype_filter('1/2 Goal', False),TESTONEXTWO,re.MULTILINE)
    print("Collated Odds Details")
    print(details_regex_group)

    details_regex_group = re.findall(regex_bettype_filter('1/2 Goal1', False),TESTONEXTWO,re.MULTILINE)
    print("Collated Odds Details 1")
    print(details_regex_group)

    details_regex_group = re.findall(regex_bettype_filter('1/2 Goal2', False),TESTONEXTWO,re.MULTILINE)
    print("Collated Odds Details 2")
    print(details_regex_group)
    details_regex_group = re.findall(regex_bettype_filter('1/2 Goal3', False),TESTONEXTWO,re.MULTILINE)
    print("Collated Odds Details 3")
    print(details_regex_group)
    details_regex_group = re.findall(regex_bettype_filter('1/2 Goal3', False),TestString,re.MULTILINE)
    print("Collated Odds Details 3")
    print(details_regex_group)

    asianhandicap_text="Tue, 11 Jun 2024\n6.14pm\n5828\nJapan vs Syria\n(+12)\n-Asian Handicap\n(Account Only)\n-\n1.88\nJapan -2.25 \n-\n1.93\nSyria +2.25 \n7.00pm\n5841\nKorea Republic vs China PR\n(+12)\n-Asian Handicap\n(Account Only)\n-\n1.8(8\nKorea Republic -1.75 \n-\n1.93\nChina PR +1.75 \n9.00pm\n5873\nMalaysia vs Chinese Taipei\n(+16)\n-Asian Handicap\n(Account Only)\n-\n1.85\nMalaysia -2.75 \n-\n1.87\nChinese Taipei +2.75     "

    # Maybe Deprecated
    
    # date_match = regex_bettype_filter(searchitem='date_pattern',complex_pattern=True).search(TestString)
    # print("Test Date Regex")
    # print(date_match) 


    # testregex=regex_bettype_filter('match_info',complex_pattern=False).search(TestString)
    # testoutputs = event_filter(TestString,bettype="1/2 Goal")

    # print("Test Regex")
    # print(testregex) 
    
    # print("Test Outputs")
    # print(testoutputs)

    # print("Bet Odds Test")
    # oddsregex=regex_bettype_filter('1/2 Goal',complex_pattern=True).search(TestString)
    # print(oddsregex)

    # print("Bet Odds Old Pattern")
    # oddsregex=regex_bettype_filter('odds_pattern',complex_pattern=False).search(TestString)
    # print(oddsregex)