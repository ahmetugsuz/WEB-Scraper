import os
import re
from operator import itemgetter
from typing import Dict, List
from urllib.parse import urljoin
from filter_urls import find_urls
import numpy as np
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from requesting_urls import get_html
import pandas as pd
from pathlib import Path
import math

## --- Task 8, 9 and 10 --- ##

try:
    import requests_cache
except ImportError:
    print("install requests_cache to improve performance")
    pass
else:
    requests_cache.install_cache()

base_url = "https://en.wikipedia.org"


def find_best_players(url: str) -> None:
    """Find the best players in the semifinals of the nba.

    This is the top 3 scorers from every team in semifinals.
    Displays plot over points, assists, rebounds

    arguments:
        - html (str) : html string from wiki basketball
    returns:
        - None
    """
    # gets the teams
    teams = get_teams(url)
    assert len(teams) == 8

    # Gets the player for every team and stores in dict (get_players) 
    # dict form: {team : [players]}
    all_players = {}
    for i, team in enumerate(teams):
        team_name = team["name"]
        team_url = team["url"]
        team_players = get_players(team_url) # catching up all players for the team by the url for that team
        all_players[team_name] = team_players

    
    # get player statistics for each player,
    # using get_player_stats
    for team, players in all_players.items():
        # Check if players is not None before iterating over it
        if players is not None:
            for index, player in enumerate(players):
                stats = get_player_stats(player['url'], team)
                if stats is not None and 'points' in stats and 'assists' in stats and 'rebounds' in stats:
                    # Check if stats is not None and contains all required keys
                    points = stats['points']
                    assists = stats['assists']
                    rebounds = stats['rebounds']
                    player = {'name': player['name'], 'url': player['url'], 'points': points, 'assists': assists, 'rebounds': rebounds}
                else: 
                    player = {'name': player['name'], 'url': player['url'], 'points': 0, 'assists': 0, 'rebounds': 0}
                players[index] = player
        else:
            # Handle the case when players is None for a specific team
            # For example, you could log a message or skip processing for that team
            ...



    # at this point, we should have a dict of the form:
    # {
    #     "team name": [
    #         {
    #             "name": "player name",
    #             "url": "https://player_url",
    #             # added by get_player_stats
    #             "points": 5,
    #             "assists": 1.2,
    #             # ...,
    #         },
    #     ]
    # }

    # Select top 3 for each team by points:
    best = {}
    top_stat = ...
    for team, players in all_players.items():
        # Check if players is not None before sorting
        if players is not None:
            players_sorted = sorted(players, key=lambda player: player.get('points', 0))
            top_3 = players_sorted[-3:]  # Get the last 3 players (top 3)
            best[team] = top_3
        else:
            print(f"No players found for {team}.")  # Or any other appropriate action


    stats_to_plot = ['points', 'assists', 'rebounds']
    
    for stat in stats_to_plot:
        plot_best(best, stat=stat)



def plot_best(best: Dict[str, List[Dict]], stat: str = "points") -> None:
    """Plots a single stat for the top 3 players from every team.

    Arguments:
        best (dict) : dict with the top 3 players from every team
            has the form:

            {
                "team name": [
                    {
                        "name": "player name",
                        "points": 5,
                        ...
                    },
                ],
            }

            where the _keys_ are the team name,
            and the _values_ are lists of length 3,
            containing dictionaries about each player,
            with their name and stats.

        stat (str) : [points | assists | rebounds] which stat to plot.
            Should be a key in the player info dictionary.
    """
    stats_dir = "NBA_player_statistics"

    X = [teams for teams in best.keys()]
    fig, ax = plt.subplots(figsize=(10.5,10.5)) #deciding size on the plot table to make it clear with the data
    width = 1
    x = np.arange(0, 40, 5) # "forholdet" er 8 her, ved aa folge 8 teams
    i = 0
    highest_y_label = 0
    for team, players in best.items():
        player_points = [player[stat] for player in players]
        player_names = [player['name'] for player in players]
        bar_0 = plt.bar(x[i]-width, player_points[0], width=width, color='r')
        bar_1 = plt.bar(x[i], player_points[1], width=width, color='g')
        bar_2 = plt.bar(x[i]+width, player_points[2], width=width, color='b')
        plt.bar_label(bar_0, fmt=player_names[0], rotation=90, size=8, padding=5)
        plt.bar_label(bar_1, fmt=player_names[1], rotation=90, size=8, padding=5)
        plt.bar_label(bar_2, fmt=player_names[2], rotation=90, size=8, padding=5)
        i += 1
        if player_points[0] > highest_y_label: #getting known to the highest y-axis value 
            highest_y_label = player_points[0]

    plt.xticks(x, X, rotation=60, size=8.5)
    dest_dir = Path(stats_dir)
    if not dest_dir.exists(): #if were on points
        os.mkdir(stats_dir) #just once, creating a directory

    plt.legend(["First", "Second", "Third"])
    plt.xlabel("Teams")
    plt.ylabel(stat)
    ax.yaxis.label.set_size(10.5)
    ax.xaxis.label.set_size(10.5)
    plt.plot(35, highest_y_label+int(highest_y_label/2) + 7) # making the plot bigger to make it more clear, think of it like padding
    plt.title(stats_dir)
    plt.savefig(stats_dir+"/"+stat)
    plt.show()    # u can cmt this out if u dont want plot.


def get_teams(url: str) -> list:
    """Extracts all the teams that were in the semi finals in nba

    arguments:
        - url (str) : url of the nba finals wikipedia page
    returns:
        teams (list) : list with all teams
            Each team is a dictionary of {'name': team name, 'url': team page
    """
    # Get the table
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Bracket").find_next("table")

    # find all rows in table
    rows = table.find_all("tr")
    rows = rows[2:]
    # maybe useful: identify cells that look like 'E1' or 'W5', etc.
    seed_pattern = re.compile(r"^[EW][1-8]$")

    # lots of ways to do this,
    # but one way is to build a set of team names in the semifinal
    # and a dict of {team name: team url}

    team_links = {}  # dict of team name: team url
    in_semifinal = set()  # set of teams in the semifinal

    # Loop over every row and extract teams from semi finals
    # also locate the links tot he team pages from the First Round column
    for row in rows:
        cols = row.find_all("td")
        # useful for showing structure
        # print([c.get_text(strip=True) for c in cols])

        # TODO:
        # 1. if First Round column, record team link from `a` tag
        # 2. if semifinal column, record team name

        # quarterfinal, E1/W8 is in column 1
        # team name, link is in column 2
        if len(cols) >= 3 and seed_pattern.match(cols[1].get_text(strip=True)):
            team_col = cols[2]
            a = team_col.find("a")
            team_links[team_col.get_text(strip=True)] = urljoin(base_url, a["href"])

        elif len(cols) >= 4 and seed_pattern.match(cols[2].get_text(strip=True)):
            team_col = cols[3]
            in_semifinal.add(team_col.get_text(strip=True))

        elif len(cols) >= 5 and seed_pattern.match(cols[3].get_text(strip=True)):
            team_col = cols[4]
            in_semifinal.add(team_col.get_text(strip=True))

    # return list of dicts (there will be 8):
    # [
    #     {
    #         "name": "team name",
    #         "url": "https://team url",
    #     }
    # ]

    assert len(in_semifinal) == 8
    return [
        {
            "name": team_name.rstrip("*"),
            "url": team_links[team_name],
        }
        for team_name in in_semifinal
    ]


def get_players(team_url: str) -> list: 
    # her kommer inn et lag, url for det laget som inneholder en tabell over spillerene deres, og vi returneres link til hver spiller sin wiki
    """Gets all the players from a team that were in the roster for semi finals
    arguments:
        team_url (str) : the url for the team
    returns:
        player_infos (list) : list of player info dictionaries
            with form: {'name': player name, 'url': player wikipedia page url}
    """
    print(f"Finding players in {team_url}")

    # Get the table
    html = get_html(team_url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Roster").find_next("table")

    players = []
    # Loop over every row and get the names from roster
    rows = table.find_all("tr")
    rows = rows[2:]
    for row in rows:
        # Get the columns
        cols = row.find_all("td")
        if not cols:
            continue
        kolonne_players = str(cols[2]) #hele html stringen, denne skal vi loope gjennom for aa finne a tag, så href.
        # find name links (a tags)
        player_url = [urls for urls in find_urls(kolonne_players)] #bruker metoden find_urls som finner a tag ved hjelp av regex patterns
        
        values = [td.get_text(strip=True) for td in cols]
        name = values[2]
        # and add to players a dict with
        # {'name':, 'url':}

        players_dict = {'name': name, 'url': player_url[0] if player_url else 'https://en.wikipedia.org/wiki/2021%E2%80%9322_Milwaukee_Bucks_season'}
        players.append(players_dict)
    # return list of players
    return players
#get_players("https://en.wikipedia.org/wiki/2021%E2%80%9322_Golden_State_Warriors_season")

def get_player_stats(player_url: str, team: str) -> dict:
    """Gets the player stats for a player in a given team
    arguments:
        player_url (str) : url for the wiki page of player
        team (str) : the name of the team the player plays for
    returns:
        stats (dict) : dictionary with the keys (at least): points, assists, and rebounds keys
    """
    print(f"Fetching stats for player in {player_url}")

    # Get the table with stats
    html = get_html(player_url)
    soup = BeautifulSoup(html, "html.parser")
    soup_heading = soup.find(id="Regular_season")
    if soup_heading == None: # this is to catch up the players who miss regular season table in their url, so we can ignore them
        return {'points': 0.0, 'assists': 0.0, 'rebounds': 0.0}
    table = soup_heading.find_next("table")

    stats = {}

    rows = table.find_all("tr")
    rows = rows[1:]

    headings = table.find_all("th") #not in use yet
    labels = [th.text.strip() for th in headings]

    # Loop over rows and extract the stats
    for row in rows:
        cols = row.find_all("td")
        values = [td.get_text(strip=True) for td in cols] # setting up values to the values of the row 
        # Check correct team (some players change team within season)
        if len(values) > 1:
            player_team = values[1]
        else:
            # Handle the case when values does not contain enough elements
            player_team = None  # Or any other appropriate action

        if str(player_team) != team:
            continue
        # load stats from columns
        # keys should be 'points', 'assists', etc.
        points = values[12] #picking up points from list of values 
        points = float(re.sub(r"\*$", "", points)) # subbing out the character: * (if its exist)
        assists = float(re.sub(r"\*$", "", values[9])) 
        rebounds = float(values[8])
        stats.update({'points': points, 'assists': assists, 'rebounds': rebounds})
    
    return stats
#get_player_stats("https://en.wikipedia.org/wiki/Stephen_Curry", "Golden State")



# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2022_NBA_playoffs"
    find_best_players(url)
