# Veritas Baseball Index — Conference Mappings
# Source: Wikipedia List of NCAA Division I baseball programs (2026)

CONFERENCES = {
    # America East
    "Albany": "America East", "Binghamton": "America East", "Bryant": "America East",
    "Maine": "America East", "NJIT": "America East", "UMass Lowell": "America East",
    "UMBC": "America East",

    # American Athletic (The American)
    "Charlotte": "American", "East Carolina": "American", "FAU": "American",
    "Florida Atlantic": "American", "Memphis": "American", "Rice": "American",
    "South Florida": "American", "USF": "American", "Tulane": "American",
    "UAB": "American", "UTSA": "American", "Wichita St.": "American",
    "Wichita State": "American",

    # ACC
    "Boston College": "ACC", "Cal": "ACC", "California": "ACC",
    "Clemson": "ACC", "Duke": "ACC", "Florida St.": "ACC", "Florida State": "ACC",
    "Georgia Tech": "ACC", "Louisville": "ACC", "Miami (FL)": "ACC", "Miami": "ACC",
    "North Carolina": "ACC", "NC State": "ACC", "Notre Dame": "ACC",
    "Pittsburgh": "ACC", "Pitt": "ACC", "Stanford": "ACC", "Virginia": "ACC",
    "Virginia Tech": "ACC", "Wake Forest": "ACC", "SMU": "ACC", "Syracuse": "ACC",

    # ASUN
    "Austin Peay": "ASUN", "Bellarmine": "ASUN", "Central Arkansas": "ASUN",
    "Eastern Kentucky": "ASUN", "FGCU": "ASUN", "Florida Gulf Coast": "ASUN",
    "Jacksonville": "ASUN", "Lipscomb": "ASUN", "North Alabama": "ASUN",
    "North Florida": "ASUN", "Queens": "ASUN", "Stetson": "ASUN",
    "UNF": "ASUN",

    # Atlantic 10
    "Davidson": "A-10", "Dayton": "A-10", "Fordham": "A-10",
    "George Mason": "A-10", "George Washington": "A-10", "La Salle": "A-10",
    "Rhode Island": "A-10", "Richmond": "A-10", "St. Bonaventure": "A-10",
    "Saint Joseph's": "A-10", "Saint Louis": "A-10", "VCU": "A-10",
    "Massachusetts": "A-10", "UMass": "A-10",

    # Big East
    "Butler": "Big East", "Creighton": "Big East", "Georgetown": "Big East",
    "St. John's": "Big East", "Seton Hall": "Big East", "UConn": "Big East",
    "Connecticut": "Big East", "Villanova": "Big East", "Xavier": "Big East",

    # Big South
    "Charleston Southern": "Big South", "Gardner-Webb": "Big South",
    "High Point": "Big South", "Longwood": "Big South", "Presbyterian": "Big South",
    "Radford": "Big South", "UNC Asheville": "Big South", "USC Upstate": "Big South",
    "Winthrop": "Big South",

    # Big Ten
    "Illinois": "Big Ten", "Indiana": "Big Ten", "Iowa": "Big Ten",
    "Maryland": "Big Ten", "Michigan": "Big Ten", "Michigan St.": "Big Ten",
    "Michigan State": "Big Ten", "Minnesota": "Big Ten", "Nebraska": "Big Ten",
    "Northwestern": "Big Ten", "Ohio St.": "Big Ten", "Ohio State": "Big Ten",
    "Oregon": "Big Ten", "Penn St.": "Big Ten", "Penn State": "Big Ten",
    "Purdue": "Big Ten", "Rutgers": "Big Ten", "UCLA": "Big Ten",
    "Southern California": "Big Ten", "USC": "Big Ten", "Washington": "Big Ten",

    # Big 12
    "Arizona": "Big 12", "Arizona St.": "Big 12", "Arizona State": "Big 12",
    "Baylor": "Big 12", "BYU": "Big 12", "Cincinnati": "Big 12",
    "Houston": "Big 12", "Iowa St.": "Big 12", "Iowa State": "Big 12",
    "Kansas": "Big 12", "Kansas St.": "Big 12", "Kansas State": "Big 12",
    "Oklahoma St.": "Big 12", "Oklahoma State": "Big 12", "TCU": "Big 12",
    "Texas Tech": "Big 12", "UCF": "Big 12", "Utah": "Big 12",
    "West Virginia": "Big 12",

    # Big West
    "Cal Poly": "Big West", "Cal St. Fullerton": "Big West",
    "Cal State Fullerton": "Big West", "CSUN": "Big West",
    "Cal St. Northridge": "Big West", "Cal State Northridge": "Big West",
    "CSU Bakersfield": "Big West", "Hawaii": "Big West",
    "Long Beach St.": "Big West", "Long Beach State": "Big West",
    "UC Davis": "Big West", "UC Irvine": "Big West", "UC Riverside": "Big West",
    "UC San Diego": "Big West", "UC Santa Barbara": "Big West",

    # CAA (Coastal Athletic Association)
    "Campbell": "CAA", "Charleston": "CAA", "Elon": "CAA", "Hofstra": "CAA",
    "Monmouth": "CAA", "North Carolina A&T": "CAA", "Northeastern": "CAA",
    "Stony Brook": "CAA", "Towson": "CAA", "UNC Wilmington": "CAA",
    "William & Mary": "CAA",

    # Conference USA
    "Dallas Baptist": "CUSA", "Delaware": "CUSA", "FIU": "CUSA",
    "Jacksonville St.": "CUSA", "Jacksonville State": "CUSA",
    "Kennesaw St.": "CUSA", "Kennesaw State": "CUSA", "Liberty": "CUSA",
    "Louisiana Tech": "CUSA", "Middle Tennessee": "CUSA",
    "Missouri St.": "CUSA", "Missouri State": "CUSA",
    "New Mexico St.": "CUSA", "New Mexico State": "CUSA",
    "Sam Houston": "CUSA", "Western Kentucky": "CUSA",

    # Horizon League
    "Milwaukee": "Horizon", "Northern Kentucky": "Horizon", "Oakland": "Horizon",
    "Purdue Fort Wayne": "Horizon", "Wright St.": "Horizon", "Wright State": "Horizon",
    "Youngstown St.": "Horizon", "Youngstown State": "Horizon",

    # Independent
    "Oregon St.": "Independent", "Oregon State": "Independent",

    # Ivy League
    "Brown": "Ivy", "Columbia": "Ivy", "Cornell": "Ivy", "Dartmouth": "Ivy",
    "Harvard": "Ivy", "Penn": "Ivy", "Princeton": "Ivy", "Yale": "Ivy",

    # MAAC
    "Canisius": "MAAC", "Fairfield": "MAAC", "Iona": "MAAC",
    "Manhattan": "MAAC", "Marist": "MAAC", "Merrimack": "MAAC",
    "Mount St. Mary's": "MAAC", "Niagara": "MAAC", "Quinnipiac": "MAAC",
    "Rider": "MAAC", "Sacred Heart": "MAAC", "St. Peter's": "MAAC",
    "Siena": "MAAC",

    # MAC
    "Akron": "MAC", "Ball State": "MAC", "Bowling Green": "MAC",
    "Central Michigan": "MAC", "Eastern Michigan": "MAC", "Kent State": "MAC",
    "Massachusetts": "MAC", "Miami (OH)": "MAC", "Northern Illinois": "MAC",
    "Ohio": "MAC", "Toledo": "MAC", "Western Michigan": "MAC",

    # Missouri Valley
    "Belmont": "MVC", "Bradley": "MVC", "Evansville": "MVC",
    "Illinois St.": "MVC", "Illinois State": "MVC", "Indiana St.": "MVC",
    "Indiana State": "MVC", "Murray St.": "MVC", "Murray State": "MVC",
    "Southern Illinois": "MVC", "UIC": "MVC", "Valparaiso": "MVC",

    # Mountain West
    "Air Force": "MWC", "Fresno St.": "MWC", "Fresno State": "MWC",
    "Grand Canyon": "MWC", "Nevada": "MWC", "New Mexico": "MWC",
    "San Diego St.": "MWC", "San Diego State": "MWC",
    "San Jose St.": "MWC", "San Jose State": "MWC",
    "UNLV": "MWC", "Washington St.": "MWC", "Washington State": "MWC",

    # NEC
    "Central Connecticut": "NEC", "Coppin St.": "NEC", "Coppin State": "NEC",
    "Delaware St.": "NEC", "Delaware State": "NEC",
    "Fairleigh Dickinson": "NEC", "LIU": "NEC", "Maryland-Eastern Shore": "NEC",
    "Merrimack": "NEC", "New Haven": "NEC", "Norfolk St.": "NEC",
    "Norfolk State": "NEC", "Sacred Heart": "NEC", "Saint Francis": "NEC",
    "St. Francis (PA)": "NEC", "Wagner": "NEC",

    # Ohio Valley
    "Eastern Illinois": "OVC", "Morehead St.": "OVC", "Morehead State": "OVC",
    "Southeast Missouri St.": "OVC", "Southeast Missouri": "OVC",
    "Southern Indiana": "OVC", "Tennessee St.": "OVC", "Tennessee State": "OVC",
    "Tennessee Tech": "OVC", "UT Martin": "OVC",

    # Pac-12
    "Oregon St.": "Independent", "Washington St.": "MWC",

    # Patriot League
    "Army": "Patriot", "Bucknell": "Patriot", "Holy Cross": "Patriot",
    "Lafayette": "Patriot", "Lehigh": "Patriot", "Navy": "Patriot",

    # SEC
    "Alabama": "SEC", "Arkansas": "SEC", "Auburn": "SEC", "Florida": "SEC",
    "Georgia": "SEC", "Kentucky": "SEC", "LSU": "SEC",
    "Mississippi St.": "SEC", "Mississippi State": "SEC",
    "Missouri": "SEC", "Ole Miss": "SEC", "South Carolina": "SEC",
    "Tennessee": "SEC", "Texas": "SEC", "Texas A&M": "SEC", "Vanderbilt": "SEC",

    # Southern Conference
    "The Citadel": "SoCon", "East Tennessee St.": "SoCon",
    "East Tennessee State": "SoCon", "Furman": "SoCon", "Mercer": "SoCon",
    "Samford": "SoCon", "UNC Greensboro": "SoCon", "VMI": "SoCon",
    "Western Carolina": "SoCon", "Wofford": "SoCon",

    # Southland
    "Abilene Christian": "Southland", "Houston Baptist": "Southland",
    "HBU": "Southland", "Incarnate Word": "Southland", "Lamar": "Southland",
    "McNeese": "Southland", "McNeese St.": "Southland",
    "Nicholls": "Southland", "Nicholls St.": "Southland",
    "Northwestern St.": "Southland", "Northwestern State": "Southland",
    "SE Louisiana": "Southland", "Southeastern Louisiana": "Southland",
    "Stephen F. Austin": "Southland", "SFA": "Southland",
    "Texas A&M-Corpus Christi": "Southland",

    # Summit League
    "Oral Roberts": "Summit", "North Dakota St.": "Summit",
    "North Dakota State": "Summit", "South Dakota St.": "Summit",
    "South Dakota State": "Summit", "St. Thomas": "Summit",
    "Kansas City": "Summit", "UMKC": "Summit", "Denver": "Summit",
    "Western Illinois": "Summit",

    # Sun Belt
    "App State": "Sun Belt", "Appalachian State": "Sun Belt",
    "Arkansas St.": "Sun Belt", "Arkansas State": "Sun Belt",
    "Coastal Carolina": "Sun Belt", "Georgia Southern": "Sun Belt",
    "Georgia St.": "Sun Belt", "Georgia State": "Sun Belt",
    "James Madison": "Sun Belt", "Louisiana": "Sun Belt",
    "Louisiana Monroe": "Sun Belt", "ULM": "Sun Belt",
    "Marshall": "Sun Belt", "Old Dominion": "Sun Belt",
    "South Alabama": "Sun Belt", "Southern Miss": "Sun Belt",
    "Southern Mississippi": "Sun Belt", "Texas St.": "Sun Belt",
    "Texas State": "Sun Belt", "Troy": "Sun Belt",

    # SWAC
    "Alabama A&M": "SWAC", "Alabama St.": "SWAC", "Alabama State": "SWAC",
    "Alcorn St.": "SWAC", "Alcorn State": "SWAC",
    "Arkansas-Pine Bluff": "SWAC", "Bethune-Cookman": "SWAC",
    "Florida A&M": "SWAC", "Grambling": "SWAC", "Grambling St.": "SWAC",
    "Jackson St.": "SWAC", "Jackson State": "SWAC",
    "Mississippi Valley St.": "SWAC", "Prairie View A&M": "SWAC",
    "Southern": "SWAC", "Texas Southern": "SWAC",

    # WAC
    "Cal Baptist": "WAC", "Sacramento St.": "WAC", "Sacramento State": "WAC",
    "Seattle": "WAC", "Southern Utah": "WAC", "Tarleton St.": "WAC",
    "Tarleton State": "WAC", "UT Arlington": "WAC", "Utah Tech": "WAC",
    "Utah Valley": "WAC",

    # WCC
    "Gonzaga": "WCC", "LMU": "WCC", "Pacific": "WCC", "Pepperdine": "WCC",
    "Portland": "WCC", "San Diego": "WCC", "San Francisco": "WCC",
    "Santa Clara": "WCC", "St. Mary's": "WCC",
}

def get_conference(team_name):
    return CONFERENCES.get(team_name, "Other")
# D1 Baseball Conference Mappings
# Used by rate.py to tag teams with their conference

CONFERENCES = {
    # SEC
    "Alabama": "SEC", "Arkansas": "SEC", "Auburn": "SEC", "Florida": "SEC",
    "Georgia": "SEC", "Kentucky": "SEC", "LSU": "SEC", "Mississippi St.": "SEC",
    "Missouri": "SEC", "Ole Miss": "SEC", "South Carolina": "SEC", "Tennessee": "SEC",
    "Texas": "SEC", "Texas A&M": "SEC", "Vanderbilt": "SEC",

    # ACC
    "Boston College": "ACC", "Clemson": "ACC", "Duke": "ACC", "Florida St.": "ACC",
    "Georgia Tech": "ACC", "Louisville": "ACC", "Miami (FL)": "ACC", "NC State": "ACC",
    "North Carolina": "ACC", "Notre Dame": "ACC", "Pittsburgh": "ACC", "Stanford": "ACC",
    "Syracuse": "ACC", "Virginia": "ACC", "Virginia Tech": "ACC", "Wake Forest": "ACC",
    "Cal": "ACC", "SMU": "ACC",

    # Big 12
    "Arizona": "Big 12", "Arizona St.": "Big 12", "Baylor": "Big 12",
    "BYU": "Big 12", "Cincinnati": "Big 12", "Houston": "Big 12",
    "Iowa St.": "Big 12", "Kansas": "Big 12", "Kansas St.": "Big 12",
    "Oklahoma St.": "Big 12", "Oregon": "Big Ten", "TCU": "Big 12",
    "Texas Tech": "Big 12", "UCF": "Big 12", "Utah": "Big 12",
    "West Virginia": "Big 12",

    # Big Ten
    "Illinois": "Big Ten", "Indiana": "Big Ten", "Iowa": "Big Ten",
    "Maryland": "Big Ten", "Michigan": "Big Ten", "Michigan St.": "Big Ten",
    "Minnesota": "Big Ten", "Nebraska": "Big Ten", "Northwestern": "Big Ten",
    "Ohio St.": "Big Ten", "Penn St.": "Big Ten", "Purdue": "Big Ten",
    "Rutgers": "Big Ten",

    # Pac-12 (remaining members)
    "Oregon St.": "Ind", "Washington St.": "MWC",

    # American Athletic
    "Charlotte": "AAC", "East Carolina": "AAC", "Florida Atlantic": "AAC",
    "Memphis": "AAC", "Navy": "AAC", "Rice": "AAC", "South Florida": "AAC",
    "Temple": "AAC", "Tulane": "AAC", "Tulsa": "AAC", "UAB": "AAC",
    "UTSA": "AAC", "Wichita St.": "AAC",

    # Sun Belt
    "App State": "Sun Belt", "Arkansas St.": "Sun Belt", "Coastal Carolina": "Sun Belt",
    "Georgia Southern": "Sun Belt", "Georgia St.": "Sun Belt", "James Madison": "Sun Belt",
    "Louisiana": "Sun Belt", "Louisiana Monroe": "Sun Belt", "Marshall": "Sun Belt",
    "Old Dominion": "Sun Belt", "South Alabama": "Sun Belt", "Southern Miss": "Sun Belt",
    "Texas St.": "Sun Belt", "Troy": "Sun Belt",

    # Mountain West
    "Air Force": "MWC", "Fresno St.": "MWC", "Nevada": "MWC",
    "New Mexico": "MWC", "San Diego St.": "MWC", "San Jose St.": "MWC",
    "UNLV": "MWC",

    # Conference USA
    "FIU": "CUSA", "Jacksonville St.": "CUSA", "Kennesaw St.": "CUSA",
    "Liberty": "CUSA", "Middle Tennessee": "CUSA", "New Mexico St.": "CUSA",
    "North Texas": "CUSA", "Sam Houston": "CUSA", "UTEP": "CUSA",
    "Western Kentucky": "CUSA",

    # WCC
    "Gonzaga": "WCC", "LMU": "WCC", "Pacific": "WCC", "Pepperdine": "WCC",
    "Portland": "WCC", "San Diego": "WCC", "San Francisco": "WCC",
    "Santa Clara": "WCC", "St. Mary's": "WCC",

    # Big West
    "Cal Poly": "Big West", "Cal St. Fullerton": "Big West", "Cal St. Northridge": "Big West",
    "Hawaii": "Big West", "Long Beach St.": "Big West", "UC Davis": "Big West",
    "UC Irvine": "Big West", "UC Riverside": "Big West", "UC San Diego": "Big West",
    "UC Santa Barbara": "Big West",

    # Southern Conference
    "The Citadel": "SoCon", "East Tennessee St.": "SoCon", "Furman": "SoCon",
    "Mercer": "SoCon", "Samford": "SoCon", "UNC Greensboro": "SoCon",
    "VMI": "SoCon", "Western Carolina": "SoCon", "Wofford": "SoCon",

    # SEC-adjacent independents / others
    "Southern California": "Big Ten", "UCLA": "Big Ten",

    # Atlantic 10
    "Davidson": "A-10", "Dayton": "A-10", "Fordham": "A-10",
    "George Mason": "A-10", "George Washington": "A-10", "La Salle": "A-10",
    "Massachusetts": "A-10", "Rhode Island": "A-10", "Richmond": "A-10",
    "Saint Louis": "A-10", "St. Bonaventure": "A-10", "VCU": "A-10",

    # Big South
    "Campbell": "Big South", "Charleston Southern": "Big South",
    "Gardner-Webb": "Big South", "High Point": "Big South",
    "Longwood": "Big South", "Presbyterian": "Big South",
    "Radford": "Big South", "UNC Asheville": "Big South",
    "Winthrop": "Big South",

    # CAA
    "Delaware": "CAA", "Elon": "CAA", "Hofstra": "CAA",
    "Monmouth": "CAA", "Northeastern": "CAA", "Stony Brook": "CAA",
    "Towson": "CAA", "UNC Wilmington": "CAA", "William & Mary": "CAA",

    # Missouri Valley
    "Bradley": "MVC", "Dallas Baptist": "MVC", "Illinois St.": "MVC",
    "Indiana St.": "MVC", "Mississippi Valley St.": "MVC", "Missouri St.": "MVC",
    "Southern Illinois": "MVC",

    # Southland
    "Abilene Christian": "Southland", "Houston Baptist": "Southland",
    "Incarnate Word": "Southland", "Lamar": "Southland",
    "McNeese": "Southland", "Nicholls": "Southland",
    "Northwestern St.": "Southland", "SE Louisiana": "Southland",
    "Stephen F. Austin": "Southland", "Texas A&M-Corpus Christi": "Southland",

    # MEAC
    "Bethune-Cookman": "MEAC", "Coppin St.": "MEAC", "Delaware St.": "MEAC",
    "Florida A&M": "MEAC", "Howard": "MEAC", "Maryland-Eastern Shore": "MEAC",
    "Morgan St.": "MEAC", "Norfolk St.": "MEAC", "North Carolina A&T": "MEAC",
    "North Carolina Central": "MEAC", "Savannah St.": "MEAC", "South Carolina St.": "MEAC",

    # SWAC
    "Alabama A&M": "SWAC", "Alabama St.": "SWAC", "Alcorn St.": "SWAC",
    "Arkansas-Pine Bluff": "SWAC", "Grambling": "SWAC", "Jackson St.": "SWAC",
    "Mississippi Valley St.": "SWAC", "Prairie View A&M": "SWAC",
    "Southern": "SWAC", "Texas Southern": "SWAC",

    # Ivy League
    "Brown": "Ivy", "Columbia": "Ivy", "Cornell": "Ivy", "Dartmouth": "Ivy",
    "Harvard": "Ivy", "Penn": "Ivy", "Princeton": "Ivy", "Yale": "Ivy",

    # Patriot League
    "Army": "Patriot", "Bucknell": "Patriot", "Holy Cross": "Patriot",
    "Lafayette": "Patriot", "Lehigh": "Patriot",

    # Ohio Valley
    "Bellarmine": "OVC", "Eastern Illinois": "OVC", "Eastern Kentucky": "OVC",
    "Morehead St.": "OVC", "Murray St.": "OVC", "Southern Indiana": "OVC",
    "Tennessee Tech": "OVC", "UT Martin": "OVC",

    # Horizon League
    "Illinois-Chicago": "Horizon", "Milwaukee": "Horizon", "Northern Kentucky": "Horizon",
    "Oakland": "Horizon", "Wright St.": "Horizon", "Youngstown St.": "Horizon",

    # Northeast Conference
    "Bryant": "NEC", "Central Connecticut": "NEC", "Fairleigh Dickinson": "NEC",
    "LIU": "NEC", "Merrimack": "NEC", "Sacred Heart": "NEC",
    "Saint Francis": "NEC", "Wagner": "NEC",

    # MAAC
    "Canisius": "MAAC", "Fairfield": "MAAC", "Manhattan": "MAAC",
    "Marist": "MAAC", "Niagara": "MAAC", "Quinnipiac": "MAAC",
    "Rider": "MAAC", "Siena": "MAAC", "St. Peter's": "MAAC",

    # WAC
    "Cal Baptist": "WAC", "Grand Canyon": "WAC", "Seattle": "WAC",
    "Southern Utah": "WAC", "Tarleton St.": "WAC", "Utah Tech": "WAC",
    "Utah Valley": "WAC",

    # Independent / misc
    "Belmont": "MVC", "Evansville": "MVC",
}

def get_conference(team_name):
    return CONFERENCES.get(team_name, "Other")
