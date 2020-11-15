import pandas
import requests
from bs4 import BeautifulSoup
import re

from sqlalchemy import create_engine, Table, MetaData
from functools import reduce

# update to threading
from multiprocessing.dummy import Pool  # This is a thread-based Pool
from multiprocessing import cpu_count, freeze_support

# URL constants for scraping
BASE_URL = 'https://www.pro-football-reference.com{0}'
PLAYER_LIST_URL = 'https://www.pro-football-reference.com/players/{0}'

# Headers for consistent data loading
HEADERS = {
    'user-agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36')
}

# get page for url
def get_page(url):
    try:
        return requests.get(url, headers=HEADERS)
    except (KeyboardInterrupt, SystemExit):
        raise

# Get all players for letter pass through
def get_players_for_letter(letter):
    """Get a list of player links for a letter of the alphabet.
            Site organizes players by first letter of last name.
            Args:
                - letter (str): letter of the alphabet uppercased
            Returns:
                - player_links (str[]): the URLs to get player profiles
    """
    response = get_page(PLAYER_LIST_URL.format(letter))
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(PLAYER_LIST_URL.format(letter))
    players = soup.find('div', {'id': 'div_players'}).find_all('a')
    return [BASE_URL.format(player['href']) for player in players]

# Finds table in pro-football-reference
def findTables(url):
    res = requests.get(url)
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("", res.text), 'lxml')
    divs = soup.findAll('div', id="content")
    divs = divs[0].findAll("div", id=re.compile("^all"))
    ids = []
    for div in divs:
        searchme = str(div.findAll("table"))
        x = searchme[searchme.find("id=") + 3: searchme.find(">")]
        x = x.replace("\"", "")
        if len(x) > 0:
            ids.append(x)
    return(ids)

# Pulls table from url
def pullTable(url, tableID, header=True):
    res = requests.get(url)

    # Work around comments
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("", res.text), 'lxml')
    tables = soup.findAll('table', id=tableID)
    if len(tables) == 0:
        return
    data_rows = tables[0].findAll('tr')
    game_data = [[td.getText() for td in data_rows[i].findAll(['th', 'td'])]
                    for i in range(len(data_rows))
                ]
    game_headers = []
    for th in data_rows[1].find_all('th'):
        game_headers.append(th['data-stat'])
    data = pandas.DataFrame(game_data)
    data = data.reset_index(drop=True)
    data.columns = game_headers
    return(data)

# Find gamelog table
def gamelogFinder(url):
    gamelogUrl = url + "/gamelog/"
    dat = pullTable(gamelogUrl, "stats", header=False)
    if dat is not None:
        dat = dat.reset_index(drop=True)
        return(dat)
    return None

# clean up scraped gamelog
def cleanGamelog(gamelogs, player):
    if len(gamelogs) > 0:
        # drop headers
        gamelogs = gamelogs.drop(gamelogs.index[:1])
        # drop last row
        gamelogs = gamelogs.drop(gamelogs.tail(1).index)
        # drop mid headers
        gamelogs = gamelogs[~gamelogs['ranker'].isin(["Rk"])]
        # generate gamelog_ids
        player_id = player[-8:]
        gamelogs.insert(loc=1, column='gamelog_id', value=player_id + '_' + gamelogs['ranker'])
        # drop first 2 columns
        gamelogs = gamelogs.drop(gamelogs.columns[[0]], axis=1)
        # add player_ids
        gamelogs.insert(loc=1, column='player_id', value=player_id)
        # gamelogs.columns = ['Year',	'Date',	'G#', 'Week', 'Age', 'Tm', 'Away', 'Opp', 'Result',	'GS']
        return(gamelogs)

# convert stats to numeric types
def cleanDataFrame(df):
    for col in  df.columns[13:]:
        df.replace(r'^\s*$', 0, regex=True)
        df[col] = pandas.to_numeric(df[col], errors='coerce')
    return(df)

# Print progress bars
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

# alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
#             'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
alphabet = ['A']
playerUrls, results = [], []

def fetchPlayerGamelogs(player):
    playerGamelogs = gamelogFinder(player)
    if playerGamelogs is not None:
        return cleanGamelog(playerGamelogs, player)
    return None

if __name__ == "__main__":
    freeze_support()
    printProgressBar(0, len(alphabet), prefix='Fetch Player URLS:', suffix='Complete 0/' + str(len(alphabet)), length=50)
    for iter, character in enumerate(alphabet):
        playerUrls.extend(get_players_for_letter(character))
        printProgressBar(iter + 1, len(alphabet), prefix='Fetch Player URLS:', suffix='Complete ' + str(iter + 1) + '/' + str(len(alphabet)), length=50)
    playerUrls = ['https://www.pro-football-reference.com/players/N/NewtCa00', 'https://www.pro-football-reference.com/players/K/KuecLu00', 'https://www.pro-football-reference.com/players/B/BrowAn04', 'https://www.pro-football-reference.com/players/G/GanoGr44', 'https://www.pro-football-reference.com/players/H/HekkJo00']
    playerUrlsLen = len(playerUrls)
    strPlayerUrlsLen = str(playerUrlsLen)

    FILE_LINES = playerUrlsLen
    NUM_WORKERS = cpu_count() * 2
    chunksize = FILE_LINES // NUM_WORKERS * 4   # Try to get a good chunksize. You're probably going to have to tweak this, though. Try smaller and lower values and see how performance changes.
    pool = Pool(NUM_WORKERS)

    printProgressBar(0, playerUrlsLen, prefix='Scrape Gamelogs:',
                 suffix='Complete 0/' + strPlayerUrlsLen, length=50)
    for iter, player in enumerate(playerUrls):
        # results.append(fetchPlayerGamelogs(player))
        for item in pool.imap_unordered(fetchPlayerGamelogs, (player,)):
            results.append(item)
        df_results = pandas.concat(results, axis=0, ignore_index=True)
        df_results = cleanDataFrame(df_results)
        printProgressBar(iter + 1, playerUrlsLen,
            prefix='Scrape Gamelogs:', suffix='Complete ' + str(iter + 1) + '/' + strPlayerUrlsLen, length=50)
    print(df_results)
    # Drop old data table
    printProgressBar(0, 1, prefix='Update Database:',
                 suffix='Complete 0/1', length=50)
    engine = create_engine('mysql+mysqldb://dbadmin:12345@localhost/fantasy_football', echo=False)
    meta = MetaData(engine)
    table_to_drop = Table('sleeperapp_gamelogs', meta, autoload=True, autoload_with=engine)
    table_to_drop.drop(engine)
    df_results.to_sql('sleeperapp_gamelogs',method='multi',index=False, con=engine, if_exists='replace')
    engine.dispose()
    printProgressBar(1, 1, prefix='Update Database:',
                 suffix='Complete 1/1', length=50)