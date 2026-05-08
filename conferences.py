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
    "Oklahoma St.": "Big 12", "Oregon": "Big 12", "TCU": "Big 12",
    "Texas Tech": "Big 12", "UCF": "Big 12", "Utah": "Big 12",
    "West Virginia": "Big 12",

    # Big Ten
    "Illinois": "Big Ten", "Indiana": "Big Ten", "Iowa": "Big Ten",
    "Maryland": "Big Ten", "Michigan": "Big Ten", "Michigan St.": "Big Ten",
    "Minnesota": "Big Ten", "Nebraska": "Big Ten", "Northwestern": "Big Ten",
    "Ohio St.": "Big Ten", "Penn St.": "Big Ten", "Purdue": "Big Ten",
    "Rutgers": "Big Ten",

    # Pac-12 (remaining members)
    "Oregon St.": "Pac-12", "Washington St.": "Pac-12",

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
    "Southern California": "Ind", "UCLA": "Ind",

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
