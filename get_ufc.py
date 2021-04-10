from bs4 import BeautifulSoup
import datetime
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import db, UFC
import traceback

driver_path = '/usr/local/bin/chromedriver'
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
driver = webdriver.Chrome(options=chrome_options, executable_path=driver_path)

seasons = ["2020", "2021"]

# Run daily.
# today = = datetime.datetime.now().strftime("%Y%m%d")


def get_ufc():
    for season in seasons:
        driver.get(
            f"https://www.espn.com/mma/schedule/_/year/{season}/league/ufc")
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        previous_matches = soup.find_all("div",
                                         text=re.compile("Past Results"),
                                         attrs={"class": "Table__Title"})[0].previous_element()
        matches = previous_matches[1].find_all(
            "tr", attrs={"class": "Table__TR Table__TR--sm Table__even"})
        urls = []
        for match in matches:
            url = match.find('a', href=re.compile(
                r'[/]([a-z]|[A-Z])\w+')).attrs['href']
            urls.append(url)
        for url in urls:
            driver.get(f"https://www.espn.com{url}")
            soup = BeautifulSoup(driver.page_source, "html.parser")
            cards = soup.find_all("div", attrs={"class": "AccordionPanel mb4"})
            date_raw = soup.find("div", attrs={"class": "n6 mb2"})
            try:
                date_obj = datetime.datetime.strptime(
                    date_raw.text, "%B %d, %Y")
                date = date_obj.strftime('%Y-%m-%d')
            except:
                date_obj = datetime.datetime.strptime(
                    date_raw.text, "%b %d, %Y")
                date = date_obj.strftime('%Y-%m-%d')
            print(date)
            try:
                for card in cards:
                    res = card.find("div", attrs={"class": "h8"})
                    data = {"date": date, "result": res.text,
                            "fighters": "", "winner": ""}
                    fighters = card.find_all(
                        "div", attrs={"class": "MMACompetitor"})
                    fighter_list = []
                    for fighter in fighters:
                        details = fighter.find(
                            "div", attrs={"class": "MMACompetitor__Detail"})
                        name = details.find("span").text
                        fighter_list.append(name)
                        try:
                            arrow = fighter.find(
                                'svg', attrs={"class": "MMACompetitor__arrow"})
                            if arrow:
                                details = fighter.find(
                                    "div", attrs={"class": "MMACompetitor__Detail"})
                                name = details.find("h2")
                                winner = name.find("span").text
                                data["winner"] = winner
                        except Exception as e:
                            print(e)
                        data["fighters"] = " vs ".join(fighter_list)
                    Fight = UFC(
                        date=data["date"],
                        result=data["result"],
                        fighters=data["fighters"],
                        winner=data["winner"])
                    exists = db.session.query(UFC.id).filter_by(
                        date=data["date"], fighters=data["fighters"]).scalar() is not None
                    if not exists:
                        print(Fight)
                        db.session.add(Fight)
                        db.session.commit()
            except:
                traceback.print_exc()
                pass


if __name__ == '__main__':
    get_ufc()
