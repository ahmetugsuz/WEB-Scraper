# HTML reader

The Program is a data analysis program that allows you to analyze and compare the performance of top NBA players.
It reads player data from Wikipedia and selects the top three players based on their points, assists, and rebounds from each team in the regular season. 
Allowing for comparison of performance within each team and across the league. The program provides a user-friendly plot for visualizing and analyzing player performance.

## Requirements

## Dependencies
* [Pip](https://pypi.org/project/pip/)
* [tabulate](https://pypi.org/project/tabulate/)
* [pandas](https://pandas.pydata.org/docs/getting_started/install.html)
* [numpy](https://numpy.org/)
* [Matplotlib](https://matplotlib.org)
* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)


## Installation
Simply clone the git repository containing the sourcecode:
* `git clone https://github.com/ahmetugsuz/HTML-Reader` 


## Running

### Running Tests

#### Unit Tests
* navigate to the root:
* `python3 -m pytest` / `pytest`
!Note: There might be some data changes during the season, may not all test pass because of that.

#### Ski Sports (Alpine ski World cup)
To extract the information 
* `Date`  
* `Venue`   
* `Type`  
From the calender on wikipedia, 
with the url = 
 `https://en.wikipedia.org/wiki/20{year}–{year+1}_FIS_Alpine_Ski_World_Cup`
Simple run the code with   
* `python3 time_planner.py`.

#### Statistics of the NBA players
There is already images of the plots on the directory: `NBA_player_statistics` wheras you can check out
* `points`  
* `assists`  
* `rebounds`    
of the players from the last season. It is also possible to run the program    
* `python3 fetch_player_statistics.py`   
to fetch the latest data about the regular season, who finds the top 3 best players for each team.
etc. Top assists for the season is given by statistics like on the image down below  
  
![alt text](https://github.com/ahmetugsuz/HTML-Reader/blob/master/NBA_player_statistics/assists.png)



#### Wiki Race
Run: `python3 wiki_race_challenge.py`  
, to run from the given start link: `"https://en.wikipedia.org/wiki/Python_(programming_language)"` and finish link: `"https://en.wikipedia.org/wiki/Peace"`  
, finding the shortest path with BFS. Note that this can take some time, it may be useful to change the urls.


