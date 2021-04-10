from bs4 import BeautifulSoup
import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import traceback
import re

## Dirty hack for imports.
import sys
import os
sys.path.append(os.path.abspath('../app'))
from config import db, MLB


driver_path = '/usr/local/bin/chromedriver'
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
driver = webdriver.Chrome(options=chrome_options, executable_path=driver_path)

date_regex = r"\w{3,9}?\s\d{1,2}, \d{4}?"


def get_mlb():
    base_url = "https://www.espn.com/mlb/scoreboard/_/date/"
    # seasons = ["2010", "2011", "2012", "2013", "2014", "2015",
    #            "2016", "2017", "2018", "2019", "2020"]
    seasons = ["2020", "2021"]
    days = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11",
            "12", "13,", "14", "15", "16", "17", "18", "19", "20", "21", "22",
            "23", "24", "25", "26", "27", "28", "29", "30", "31", ]
    months = ["01", "02", "03", "04", "05",
              "06", "07", "08", "09", "10", "11", "12"]
    urls = []
    dates = []
    for season in seasons:
        for month in months:
            for day in days:
                urls.append(f"{base_url}{season}{month}{day}")
                dates.append(f'{season}-{month}-{day}')

    for url, date in zip(urls, dates):
        print(url)
        print(date)
        try:
            driver.get(url)
        except:
            driver.get(url)
            time.sleep(3)
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            events = soup.find(id='scoreboard-page')
            evs = events.find(id='events')
            # date_container = soup.find(
            #     "div", attrs={"class": "carousel-day"})
            # date = date_container.find("span")
            # datereg = re.findall(date_regex, date.text)
            # try:
            #     date_obj = datetime.datetime.strptime(
            #         datereg[0], "%B %d, %Y")
            #     date = date_obj.strftime('%Y-%m-%d')
            # except:
            #     date_obj = datetime.datetime.strptime(
            #         datereg[0], "%b %d, %Y")
            #     date = date_obj.strftime('%Y-%m-%d')

            away_win_games = evs.find_all(
                'article', attrs={"class": "scoreboard baseball final away-winner js-show"})
            home_win_games = evs.find_all(
                'article', attrs={"class": "scoreboard baseball final home-winner js-show"})
            print(len(away_win_games))
            print(len(home_win_games))
        except:
            traceback.print_exc()
            print(len(away_win_games))
        if (len(away_win_games) > 0):
            for game in away_win_games:
                try:
                    away_team = game.find('tr', attrs={'class': 'away'})
                    away_name = away_team.find(
                        'span', attrs={'class': 'sb-team-short'})
                    away_total = away_team.find('td', attrs={'class': 'total'})
                except:
                    traceback.print_exc()
                try:
                    home_team = game.find('tr', attrs={'class': 'home'})
                    home_name = home_team.find(
                        'span', attrs={'class': 'sb-team-short'})
                    home_total = home_team.find('td', attrs={'class': 'total'})
                except:
                    traceback.print_exc()
                print("Making entry")
                print({"date": date, "score": f"{away_total.text} - {home_total.text}",
                       "teams": f"{away_name.text} vs {home_name.text}"})
                Game = MLB(
                    date=date,
                    score=f"{home_total.text} - {away_total.text}",
                    teams=f"{home_name.text} vs {away_name.text}")

                exists = db.session.query(MLB.id).filter_by(
                    date=date, teams=f"{home_name.text} vs {away_name.text}").scalar() is not None
                if not exists:
                    print(
                        f"Making entry: {date}---{home_name.text} vs {away_name.text}")
                    db.session.add(Game)
                    db.session.commit()
        if (len(home_win_games) > 0):
            for game in home_win_games:
                try:
                    away_team = game.find('tr', attrs={'class': 'away'})
                    away_name = away_team.find(
                        'span', attrs={'class': 'sb-team-short'})
                    away_total = away_team.find('td', attrs={'class': 'total'})
                except:
                    traceback.print_exc()
                try:
                    home_team = game.find('tr', attrs={'class': 'home'})
                    home_name = home_team.find(
                        'span', attrs={'class': 'sb-team-short'})
                    home_total = home_team.find('td', attrs={'class': 'total'})
                except:
                    traceback.print_exc()
                Game = MLB(
                    date=date,
                    score=f"{home_total.text} - {away_total.text}",
                    teams=f"{home_name.text} vs {away_name.text}")

                exists = db.session.query(MLB.id).filter_by(
                    date=date, teams=f"{home_name.text} vs {away_name.text}").scalar() is not None
                if not exists:
                    print(
                        f"Making entry: {date}---{home_name.text} vs {away_name.text}")
                    db.session.add(Game)
                    db.session.commit()
                print("Making entry")
                print({"date": date, "score": f"{away_total.text} - {home_total.text}",
                       "teams": f"{away_name.text} vs {home_name.text}"})


if __name__ == "__main__":
    get_mlb()
