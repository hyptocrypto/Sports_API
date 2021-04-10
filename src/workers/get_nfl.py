from bs4 import BeautifulSoup
import datetime
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import traceback

## Dirty hack for imports.
import sys
import os
sys.path.append(os.path.abspath('../app'))
from config import db, NFL

# driver_path = '/usr/bin/chromedriver'
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.binary_location = '/usr/bin/chromium-browser'
# driver = webdriver.Chrome(options = chrome_options, executable_path = driver_path)
# driver2 = webdriver.Chrome(options = chrome_options, executable_path = driver_path)

driver_path = '/usr/local/bin/chromedriver'
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
driver = webdriver.Chrome(options=chrome_options, executable_path=driver_path)
driver2 = webdriver.Chrome(options=chrome_options, executable_path=driver_path)

date_regex = r"\w{3,9}?\s\d{1,2}, \d{4}?"


def get_nfl():
    urls = []
    base_url = 'https://www.espn.com/nfl/scoreboard/_'
    # seasons = ["2009",
    #            "2010", "2011", "2012", "2013", "2014", "2015",
    #            "2016", "2017", "2018", "2019", "2020"]

    seasons = ["2021", "2020"]

    for season in seasons:
        for week in range(17):
            for i in range(2):
                urls.append(
                    f"{base_url}/year/{season}/seasontype/{i+2}/week/{week+1}")
    # Run daily.
    # today = = datetime.datetime.now().strftime("%Y%m%d")
    for url in urls:
        print(url)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        events = soup.find(id='events')
        # Define a soup object for away wins and home wins
        away_games = events.find_all(
            'article', attrs={"class": "scoreboard football final away-winner js-show"})
        home_games = events.find_all(
            'article', attrs={"class": "scoreboard football final home-winner js-show"})
        other_games = events.find_all(
            'article', attrs={"class": "scoreboard football fallback-no-recap final home-winner js-show"})
        # if home_games is None and away_games is None:
        #     print("good check")
        other_games = events.find_all(
            'article', attrs={"class": "scoreboard football fallback-no-recap final home-winner js-show"})

        if (len(other_games) > 0):
            for game in other_games:
                try:
                    recap_link = game.find("article", attrs={"recap-link"})
                    link = recap_link.find('a', href=re.compile(
                        r'[/]([a-z]|[A-Z])\w+')).attrs['href']
                    driver2.get(f"https://www.espn.com{link}")
                    article_soup = BeautifulSoup(
                        driver2.page_source, "html.parser")
                    article = article_soup.find(
                        "article", attrs={"class": "article"})
                    timestamp = article.find(
                        "div", attrs={"class": "article-meta"})
                    game_date = re.match(date_regex, timestamp.text).group()
                    try:
                        date_obj = datetime.datetime.strptime(
                            game_date, "%B %d, %Y")
                        date = date_obj.strftime('%Y-%m-%d')
                        print("One date")
                    except:
                        date_obj = datetime.datetime.strptime(
                            game_date, "%b %d, %Y")
                        date = date_obj.strftime('%Y-%m-%d')
                        print("Two date")
                except:
                    traceback.print_exc()
                    date = 'na'
#             teams = game.find("tbdoy", attrs={"class": "teams"})
            try:
                # Parse the soup for the name and total score of the away team
                away_team = game.find('tr', attrs={'class': 'away'})
                away_name = away_team.find(
                    'span', attrs={'class': 'sb-team-short'})
                away_total = away_team.find('td', attrs={'class': 'total'})

                # Parse the soup for the name and total score of the home team
                home_team = game.find('tr', attrs={'class': 'home'})
                home_name = home_team.find(
                    'span', attrs={'class': 'sb-team-short'})
                home_total = home_team.find('td', attrs={'class': 'total'})

                # Append the results to DB
                Game = NFL(
                    date=date,
                    score=f"{home_total.text} - {away_total.text}",
                    teams=f"{home_name.text} vs {away_name.text}")

                exists = db.session.query(NFL.id).filter_by(
                    date=date, teams=f"{home_name.text} vs {away_name.text}").scalar() is not None
                if not exists:
                    print(
                        f"Making entry: {date}---{home_name.text} vs {away_name.text}")
                    db.session.add(Game)
                    db.session.commit()
            except:
                traceback.print_exc()
        if (len(away_name) > 0):
            for game in away_games:
                try:
                    recap_link = game.find("article", attrs={"recap-link"})
                    link = recap_link.find('a', href=re.compile(
                        r'[/]([a-z]|[A-Z])\w+')).attrs['href']
                    driver2.get(f"https://www.espn.com{link}")
                    article_soup = BeautifulSoup(
                        driver2.page_source, "html.parser")
                    article = article_soup.find(
                        "article", attrs={"class": "article"})
                    timestamp = article.find(
                        "div", attrs={"class": "article-meta"})
                    game_date = re.match(date_regex, timestamp.text).group()
                    try:
                        date_obj = datetime.datetime.strptime(
                            game_date, "%B %d, %Y")
                        date = date_obj.strftime('%Y-%m-%d')
                        print("One date")
                    except:
                        date_obj = datetime.datetime.strptime(
                            game_date, "%b %d, %Y")
                        date = date_obj.strftime('%Y-%m-%d')
                        print("Two date")

                except:
                    traceback.print_exc()
                    date = 'NA'
    #             teams = game.find("tbdoy", attrs={"class": "teams"})
                try:
                    # Parse the soup for the name and total score of the away team
                    away_team = game.find('tr', attrs={'class': 'away'})
                    away_name = away_team.find(
                        'span', attrs={'class': 'sb-team-short'})
                    away_total = away_team.find('td', attrs={'class': 'total'})

                    # Parse the soup for the name and total score of the home team
                    home_team = game.find('tr', attrs={'class': 'home'})
                    home_name = home_team.find(
                        'span', attrs={'class': 'sb-team-short'})
                    home_total = home_team.find('td', attrs={'class': 'total'})

                    # Append the results to DB
                    Game = NFL(
                        date=date,
                        score=f"{home_total.text} - {away_total.text}",
                        teams=f"{home_name.text} vs {away_name.text}")

                    exists = db.session.query(NFL.id).filter_by(
                        date=date, teams=f"{home_name.text} vs {away_name.text}").scalar() is not None
                    if not exists:
                        print(
                            f"Making entry: {date}---{home_name.text} vs {away_name.text}")
                        db.session.add(Game)
                        db.session.commit()
                except:
                    traceback.print_exc()
        if (len(home_games) > 0):
            for game in home_games:
                try:
                    recap_link = game.find("article", attrs={"recap-link"})
                    link = recap_link.find('a', href=re.compile(
                        r'[/]([a-z]|[A-Z])\w+')).attrs['href']
                    driver2.get(f"https://www.espn.com{link}")
                    article_soup = BeautifulSoup(
                        driver2.page_source, "html.parser")
                    article = article_soup.find(
                        "article", attrs={"class": "article"})
                    timestamp = article.find(
                        "div", attrs={"class": "article-meta"})
                    game_date = re.match(date_regex, timestamp.text).group()
                    try:
                        date_obj = datetime.datetime.strptime(
                            game_date, "%B %d, %Y")
                        date = date_obj.strftime('%Y-%m-%d')
                    except:
                        date_obj = datetime.datetime.strptime(
                            game_date, "%b %d, %Y")
                        date = date_obj.strftime('%Y-%m-%d')
                except Exception as e:
                    print(e)
                    date = 'NA'
                # teams = game.find("tbody", attrs={"class": "teams"})
                try:
                    # Parse the soup for the name and total score of the away team
                    away_team = game.find('tr', attrs={'class': 'away'})
                    away_name = away_team.find(
                        'span', attrs={'class': 'sb-team-short'})
                    away_total = away_team.find('td', attrs={'class': 'total'})

                    # Parse the soup for the name and total score of the home team
                    home_team = game.find('tr', attrs={'class': 'home'})
                    home_name = home_team.find(
                        'span', attrs={'class': 'sb-team-short'})
                    home_total = home_team.find('td', attrs={'class': 'total'})

                    # Append the results to DB
                    Game = NFL(
                        date=date,
                        score=f"{home_total.text} - {away_total.text}",
                        teams=f"{home_name.text} vs {away_name.text}")

                    exists = db.session.query(NFL.id).filter_by(
                        date=date, teams=f"{home_name.text} vs {away_name.text}").scalar() is not None
                    if not exists:
                        print(
                            f"Making entry: {date}---{home_name.text} vs {away_name.text}")
                        db.session.add(Game)
                        db.session.commit()
                except:
                    traceback.print_exc()


if __name__ == "__main__":
    get_nfl()
