import re
from copy import copy
from dataclasses import dataclass
import requests
import bs4
import pandas as pd
from bs4 import BeautifulSoup
from requesting_urls import get_html
import markdown

## --- Task 5, 6, and 7 ---- ##

# Dict over all types of events
event_types = {
    "DH": "Downhill",
    "SL": "Slalom",
    "GS": "Giant Slalom",
    "SG": "Super Giant slalom",
    "AC": "Alpine Combined",
    "PG": "Parallel Giant Slalom",
}




@dataclass
class TableEntry:
    """Data class representing a single entry in a table

    Records text content, rowspan, and colspan attributes
    """

    text: str
    rowspan: int
    colspan: int


def extract_events(table: bs4.element.Tag) -> pd.DataFrame:
    """Gets the events from the table
    arguments:
        table (bs4.element.Tag) : Table containing data
    return:
        df (DataFrame) : DataFrame containing filtered and parsed data
    """
    # Gets the table headers and saves their labels in `keys`
    headings = table.find_all("th")
    labels = [th.text.strip() for th in headings]
    data = []
    # Extracts the data in table, keeping track of colspan and rowspan
    rows = table.find_all("tr") #finding the all table rows in the table
    rows = rows[1:] 

    for tr in rows:
        cells = tr.find_all(["th", "td"]) #let the cells be every cell on the the givin row 
        row = []
        for cell in cells:
            colspan = int(cell.get('colspan', 1)) 
            rowspan = int(cell.get('rowspan', 1)) 
            text = cell.get_text(strip=True) 
            row.append(
                TableEntry(
                    text=text,
                    rowspan=rowspan,
                    colspan=colspan,
                )
            )
        data.append(row)
    # at this point `data` should be a table (list of lists)
    # where each item is a TableEntry with row/colspan properties
    # expand TableEntries into a dense table
    all_data = expand_row_col_span(data)

    # List of desired columns
    
    wanted = ["Date", "Venue", "Type"] # her skal vi ta det vi er ute etter, som oppgaven sier: Data, Venue, discipline

    # Filter data and create pandas dataframe
    filtered_data = filter_data(labels, all_data, wanted) # take out the wanted columns, removing the not wanted columns, filtering text

    df = pd.DataFrame(filtered_data) # setting data frame to the filtered data

    df_wanted = pd.DataFrame({wanted[0]: df[0], # df_wanted is just the columns with the key labels on them. 
                        wanted[1]: df[1],
                        wanted[2]: df[2]}) 


 
    return df_wanted


def find_table_with_heading(document, heading_pat): # A method to find a table with the heading
    heading_element = document.find(class_="mw-headline", string=heading_pat)
    table = heading_element.find_next("table")
    return table

def render_schedule(data: pd.DataFrame) -> str:
    """Render the schedule data to markdown

    arguments:
        data (DataFrame) : DataFrame containing table to write
    return:
        markdown (str): the rendered schedule as markdown
    """
    def expand_event_type(type_key):
        """Expand event type key (SL) to full name (Slalom)

        Useful with pandas Series.apply
        """
        return event_types.get(type_key[:2], type_key)


    
    for data_key in data.get("Type"): # tagetting column 'Type', and 
        data = data.replace(data_key, expand_event_type(data_key)) #passing and changing the keys to expand method who gives us full name of the key

        
    table = data.to_markdown() # turning into markdown
    return table



def strip_text(text: str) -> str:
    """Gets rid of cruft from table cells, footnotes and setting limit to 20 chars

    It is not required to use this function,
    but it may be useful.

    arguments:
        text (str) : string to fix
    return:
        text (str) : the string fixed
    """

    text = text[:20]  # 20 char limit
    text = re.sub(r"\[.*\]", "", text)
    return text


def filter_data(keys: list, data: list, wanted: list):
    """Filters away the columns not specified in wanted argument

    It is not required to use this function,
    but it may be useful.

    arguments:
        keys (list of strings) : list of all column names
        data (list of lists) : data with rows and columns
        wanted (list of strings) : list of wanted columns
    return:
        filtered_data (list of lists) : the filtered data
            This is the subset of data in `data`,
            after discarding the columns not in `wanted`.
    """

    filtered_list = [] # making a sub data list of lists
    for i, d in enumerate(data):
        filtered_celle = [] # A list to hold the wanted cells
        for index, celle in enumerate(d):
            if keys[index] in wanted:
                text = strip_text(celle) # stripping the text, to make it finer and readable
                filtered_celle.append(text)
        filtered_list.append(filtered_celle) # Adding the right cells by wanted to the sub list of lists

    return filtered_list #returning the new filtered list

def expand_row_col_span(data):
    """Applies row/colspan to tabular data

    It is not required to use this function,
    but it may be useful.

    - Copies cells with colspan to columns to the right
    - Copies cells with rowspan to rows below
    - Returns raw data (removing TableEntry wrapper)

    arguments:
        data_table (list) : data with rows and cols
            Table of the form:

            [
                [ # row
                    TableEntry(text='text', rowspan=2, colspan=1),
                ]
            ]
    return:
        new_data_table (list): list of lists of strings
            [
                [
                    "text",
                    "text",
                    ...
                ]
            ]

            This should be a dense matrix (list of lists) of data,
            where all rows have the same length,
            and all values are `str`.
    """

    # first, apply colspan by duplicating across the column(s)
    new_data = []
    for row in data:
        new_row = []
        new_data.append(new_row)
        for entry in row:
            for _ in range(entry.colspan):
                new_entry = copy(entry)
                new_entry.colspan = 1
                new_row.append(new_entry)

    # apply row span by inserting copies in subsequent rows
    # in the same column
    for row_idx, row in enumerate(new_data):
        for col_idx, entry in enumerate(row):
            for offset in range(1, entry.rowspan):
                # copy to row(s) below
                target_row = new_data[row_idx + offset]
                new_entry = copy(entry)
                new_entry.rowspan = 1
                target_row.insert(col_idx, new_entry)
            entry.rowspan = 1

    # now that we've applied col/row span,
    # replace the table with the raw entries,
    # instead of the TableEntry objects
    return [[entry.text for entry in row] for row in new_data]

def time_plan(url: str) -> str:
    """Parses table from html text and extract desired information
    and saves in betting slip markdown file

    arguments:
        url (str) : URL for page with calendar table
    return:
        markdown (str) : string containing the markdown schedule
    """
    # Get the page
    r = requests.get(url)
    html = r.text
    # parse the HTML
    soup = BeautifulSoup(html, "html.parser")
    # locate the table
    calendar = re.compile(r"^Calendar")
    soup_heading = soup.find(id=calendar)
    soup_table = soup_heading.find_next("table", {"class": "wikitable"})
    # extract events into pandas data frame
    df = extract_events(soup_table)

    # Write the schedule markdown
    return render_schedule(df)

if __name__ == "__main__":
    # test the script on the past few years by running it:
    for year in range(20, 23):
        url = (
            f"https://en.wikipedia.org/wiki/20{year}–{year+1}_FIS_Alpine_Ski_World_Cup"
        )
        print(url)
        md = time_plan(url)
        print(md)
