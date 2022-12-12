import re
from typing import Tuple
from requesting_urls import get_html
## -- Task 3 (IN3110 optional, IN4110 required) -- ##

# create array with all names of months
month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def get_date_patterns() -> Tuple[str, str, str]:
    """Return strings containing regex pattern for year, month, day
    arguments:
        None
    return:
        year, month, day (tuple): Containing regular expression patterns for each field
    """
    # Regex to capture days, months and years with numbers
    # year should accept a 4-digit number between at least 1000-2029
    year = r"(?P<year>18[0-9]\d|19[0-9]\d|20[01]\d|20[0-9]\d)" #?((19[7-9]\d|20\d{2})
    # month should accept month names or month numbers
    month = r"(?P<month>(?:Jan(?:uary)?|Feb(?:ruary)?|Marc(?:h)?|Apr(?:il)?|May(?:)|Jun(?:e)?|July(?:)?|Aug(?:ust)?|Sept(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?))"
    # day should be a number, which may or may not be zero-padded
    day = r"(?P<day>(?:[1-9]\d|[0-12]|3[01]))"

    return year, month, day

def zero_pad(n: str):
    """zero-pad a number string

    turns '2' into '02'
    """
    ny_str = n
    if len(n) < 2:
        ny_str = "0"
        ny_str = ny_str + n
    return ny_str



def convert_month(s: str) -> str:
    """Converts a string month to number (e.g. 'September' -> '09'.

    arguments:
        month_name (str) : month name
    returns:
        month_number (str) : month number as zero-padded string
    """
    num_month = 0

    # If already digit do nothing
    if s.isdigit():
        return s
    
    for i, month in enumerate(month_names):
        if s == month:
            num_month = i
    num_month += 1
    num_month = str(num_month)
    num_month = zero_pad(num_month) #checking for if its a valid type, when its a digit between 0-9, we put a zero ahead


    # Convert to number as string
    return num_month

def find_dates(text: str, output: str = None) -> list:
    """Finds all dates in a text using reg ex

    arguments:
        text (string): A string containing html text from a website
    return:
        results (list): A list with all the dates found
    """
    year, month, day = get_date_patterns()

    # Date on format YYYY/MM/DD - ISO
    ISO = rf"{year}(?:-)\b(?:(0\d|1[0-3]\d))\b(?:-)(0[1-9]|[12]\d|3[01])"

    # Date on format DD/MM/YYYY
    DMY = rf"\b(?:([1-9]|[12]\d|3[01]))\b\s{month}\s{year}"

    # Date on format MM/DD/YYYY  
    MDY = rf"{month}\s\b(?:([1-9]|[12]\d|3[01]))(?:,)\s{year}"

    # Date on format YYYY/MM/DD
    YMD = rf"{year}\s{month}\s{day}" 

    # list with all supported formats
    format_patterns = [ISO, DMY, MDY, YMD]
    dates = [] #skal være i format år/måned/dag

    for formats in format_patterns:
        date_element = re.findall(formats, text)
        dag_indeks = -2
        maaned_indeks = -2
        aar_indeks = -2

        if formats == ISO:
            dag_indeks = 2
            maaned_indeks = 1
            aar_indeks = 0
        elif formats == DMY:
            dag_indeks = 0
            maaned_indeks = 1
            aar_indeks = 2
        elif formats == MDY:
            dag_indeks = 1
            maaned_indeks = 0
            aar_indeks = 2
        elif formats == YMD:
            aar_indeks = 0
            maaned_indeks = 1
            dag_indeks = 2

        for element in date_element:
            dag = zero_pad(element[dag_indeks])
            maaned = convert_month(element[maaned_indeks])
            aar = element[aar_indeks]
            dato = aar+"/"+maaned+"/"+dag
            dates.append(dato)

    # Write to file if wanted
    if output:
        text_file = open(f"{output}", "w")
        print(f"Writing to: {output}")
        for dato in dates:
            print(dato, file=text_file)

    return dates

