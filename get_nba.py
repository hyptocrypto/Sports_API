from bs4 import BeautifulSoup
import datetime
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import db, NBA
import traceback

# driver_path = '/usr/bin/chromedriver'
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.binary_location = '/usr/bin/chromium-browser'
# driver = webdriver.Chrome(options = chrome_options, executable_path = driver_path)

driver_path = '/usr/local/bin/chromedriver'
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
driver = webdriver.Chrome(options=chrome_options, executable_path=driver_path)

date_regex = r"\w{3,9}?\s\d{1,2}, \d{4}?"


def get_nba():
    base_url = "https://www.espn.com/nba/scoreboard/_/date/"

    # Run for historic data

    # seasons = ["2011", "2012", "2013", "2014", "2015",
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

    # Run daily.
    # today = datetime.datetime.now().strftime("%Y%m%d")
    for url, date in zip(urls, dates):
        try:
            print(url)
            print(date)
            driver.get(url)
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            events = soup.find(id='scoreboard-page')
            evs = events.find(id='events')
            away_win_games = evs.find_all(
                'article', attrs={"class": "scoreboard basketball final away-winner js-show"})
            home_win_games = evs.find_all(
                'article', attrs={"class": "scoreboard basketball final home-winner js-show"})
            # date_container = soup.find("div", attrs={"class": "carousel-day"})
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

        except Exception as e:
            traceback.print_exc()
        if (len(home_win_games) > 0):
            for game in home_win_games:
                try:
                    away_team = game.find('tr', attrs={'class': 'away'})
                    name_block = away_team.find("h2")
                    away_name = name_block.find(
                        'span', attrs={'class': 'sb-team-short'})
                    away_total = away_team.find('td', attrs={'class': 'total'})
                except Exception as e:
                    traceback.print_exc()

                try:
                    home_team = game.find('tr', attrs={'class': 'home'})
                    name_block = home_team.find("h2")
                    home_name = name_block.find(
                        'span', attrs={'class': 'sb-team-short'})
                    home_total = home_team.find('td', attrs={'class': 'total'})
                except Exception as e:
                    traceback.print_exc()

                Game = NBA(
                    date=date,
                    score=f'{away_total.text} - {home_total.text}',
                    teams=f'{away_name.text} vs {home_name.text}'
                )
                exists = db.session.query(NBA.id).filter_by(
                    date=date, teams=f'{away_name.text} vs {home_name.text}'
                ).scalar() is not None
                if not exists:
                    db.session.add(Game)
                    db.session.commit()
                    print("Making entry")
                    print({"date": f'{date}', "score": f'{away_total.text} - {home_total.text}',
                           "teams": f'{away_name.text} vs {home_name.text}'})
        if (len(away_win_games) > 0):
            for game in away_win_games:
                try:
                    away_team = game.find('tr', attrs={'class': 'away'})
                    name_block = away_team.find("h2")
                    away_name = name_block.find(
                        'span', attrs={'class': 'sb-team-short'})
                    away_total = away_team.find('td', attrs={'class': 'total'})
                except Exception as e:
                    traceback.print_exc()

                try:
                    home_team = game.find('tr', attrs={'class': 'home'})
                    name_block = home_team.find("h2")
                    home_name = name_block.find(
                        'span', attrs={'class': 'sb-team-short'})
                    home_total = home_team.find('td', attrs={'class': 'total'})
                except Exception as e:
                    traceback.print_exc()

                Game = NBA(
                    date=date,
                    score=f'{away_total.text} - {home_total.text}',
                    teams=f'{away_name.text} vs {home_name.text}'
                )
                exists = db.session.query(NBA.id).filter_by(
                    date=date, teams=f'{away_name.text} vs {home_name.text}'
                ).scalar() is not None
                if not exists:
                    db.session.add(Game)
                    db.session.commit()
                    print("Making entry")
                    print({"date": f'{date}', "score": f'{away_total.text} - {home_total.text}',
                           "teams": f'{away_name.text} vs {home_name.text}'})


if __name__ == "__main__":
    get_nba()
