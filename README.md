# Web-Scraper for Multi-Sport Analytics

The HTML Reader for Multi-Sport Analytics is a comprehensive data analysis program designed specifically for analyzing and comparing the performance of top NBA players. It offers a robust platform for extracting player data from Wikipedia and identifying the top three players based on crucial performance metrics such as points, assists, and rebounds during the regular NBA season. This functionality enables users to conduct in-depth comparisons of player performance both within individual teams and across the league.   

## Features:  

- Data extraction from Wikipedia for NBA player statistics.  
- Identification of top players based on points, assists, and rebounds.  
- User-friendly visualization of player performance through plots.  
- Integration with external sports data sources for comprehensive analysis.  

## Requirements

## Dependencies
* [Pip](https://pypi.org/project/pip/)
* [tabulate](https://pypi.org/project/tabulate/)
* [pandas](https://pandas.pydata.org/docs/getting_started/install.html)
* [numpy](https://numpy.org/)
* [Matplotlib](https://matplotlib.org)
* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)


## Installation

### Installing Requirements

To run this project, you'll need to install the required Python packages listed in the `requirements.txt` file.

#### Locally

If you're not using a virtual environment, you can install the project dependencies directly using pip:

```bash
pip install -r requirements.txt
```

This command will install all the necessary packages globally on your system.

#### Using a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies and isolate them from other projects. 
If you haven't already, you can create a virtual environment using venv:  

    python -m venv myenv   

* On macOS/Linux:
```bash
source myenv/bin/activate
```

* On Windows:  
```bash
myenv\Scripts\activate
```

Once the virtual environment is activated, you can install the project dependencies using pip:  
```bash
pip install -r requirements.txt
```

This will install the required packages only within the virtual environment, keeping your system's Python installation clean.   

### Cloning 

To install the HTML Reader for Multi-Sport Analytics, simply clone the Git repository containing the source code:    

    git clone https://github.com/ahmetugsuz/HTML-Reader    

### Running  

Once installed, navigate to the root directory:  

    cd HTML-Reader   

and execute the following command to run `NBA_player_statistics` program:   

    python3 fetch_player_statistics.py  


#### Statistics of the NBA players
There is already images of the plots on the directory: `NBA_player_statistics` wheras you can check out
* `points`  
* `assists`  
* `rebounds`    
of the players from the last season. It is also possible to run the program    
* `python3 fetch_player_statistics.py`   
to fetch the latest data about the regular season, who finds the top 3 best players for each team.  
etc. Top assists for the season is given by statistics like on the image down below    
  
![alt text](https://github.com/ahmetugsuz/HTML-Reader/blob/master/NBA_player_statistics/points.png)  


### Running Tests

#### Unit Tests
To run unit tests, navigate to the root directory and execute the following command:  

    python3 -m pytest / pytest   
   

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



#### Wiki Race
Run:  

    python3 wiki_race_challenge.py   

to run from the given start link: `"https://en.wikipedia.org/wiki/Python_(programming_language)"` and finish link: `"https://en.wikipedia.org/wiki/Peace"`, finding the shortest path with BFS. Note that this can take some time, it may be useful to change the urls.  

Please note that this process may take some time, and users may opt to modify the URLs for their specific requirements.

## Contributing:
Contributions to the project are welcome! Please contact me on my website: [ahmettu.com](https://ahmettu.com)  

## License:
This project is licensed under the MIT License. See the LICENSE file for more details.
