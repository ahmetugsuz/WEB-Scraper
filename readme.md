# HTML reader

This is an program who reads the table of NBA player, from wikipedia urls, and plot a NBA player statistics, taken 3 best player from each team in the regular season.  
It also offers a wikipedia golf program, with the BFS algotithm, finding the shortest way from a wikipedia link to another.    
It also reads a calender to make a markdown for the ski sport of choosen columns.

## Requirements

## Dependencies
* [Pip](https://pypi.org/project/pip/)
* [tabulate](https://pypi.org/project/tabulate/)
* [pandas](https://pandas.pydata.org/docs/getting_started/install.html)
* [numpy](https://numpy.org/)
* [Matplotlib](https://matplotlib.org)
* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)


## Installation

* `git clone https://github.uio.no/IN3110/IN3110-ahmettu/tree/main/assignment4` git repository containing the sourcecode
* from the root simply run
* `python3 -m pip install .`


## Running

### Running Tests

#### Unit Tests
* navigate to the root:
* `python3 -m pytest` / `pytest`

#### Ski Sports (Alpine ski World cup)
To extract the information 
* `Date`  
* `Venue`   
* `Type`  
From the calender on wikipedia, 
with the url = (
 `https://en.wikipedia.org/wiki/20{year}–{year+1}_FIS_Alpine_Ski_World_Cup`)
Simple run the code with  `python3 time_planer.py`.

#### Statistics of the NBA players
There is already images of the plots on the directory: `NBA_player_statistics` wheras tou can check out
* `points`  
* `assists`  
* `rebounds`    
Of the players from the last season.

#### Wiki Race
Run: `python3 wiki_race_challenge.py`  
, to run from the given start link: `"https://en.wikipedia.org/wiki/Python_(programming_language)"` and finish link: `"https://en.wikipedia.org/wiki/Peace"`  
, finding the shortest path with BFS.


