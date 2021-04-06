from bs4 import BeautifulSoup
import datetime
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

driver_path = '/usr/bin/chromedriver'
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = '/usr/bin/chromium-browser'
driver = webdriver.Chrome(options = chrome_options, executable_path = driver_path)

urls = []
results = {"results":[]}

driver.get("https://www.espn.com/mma/schedule/_/league/ufc")
time.sleep(3)
soup = BeautifulSoup(driver.page_source, 'html.parser')
previous_matches = soup.find_all("div",
                                 text=re.compile("Past Results"), 
                                 attrs={"class": "Table__Title"})[0].previous_element()
matches = previous_matches[1].find_all("tr", attrs={"class": "Table__TR Table__TR--sm Table__even"})

for match in matches:
    url = match.find('a', href = re.compile(r'[/]([a-z]|[A-Z])\w+')).attrs['href']
    urls.append(url)
for url in urls:
    driver.get(f"https://www.espn.com{url}")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    card = soup.find("div", attrs={"class":"MMAFightCard__Gamestrip br-5 mh4 relative MMAFightCard__Gamestrip--open"})
    fighters = card.find_all("div", attrs={"class": "MMACompetitor"})
    data = {"match":"", "winner":""}
    fighter_list = []
    for fighter in fighters:
        details = fighter.find("div", attrs={"class": "MMACompetitor__Detail"})
        name = details.find("span").text
        fighter_list.append(name)
        try:
            arrow = fighter.find('svg', attrs={"class": "MMACompetitor__arrow"})
            if arrow:
                details = fighter.find("div", attrs={"class": "MMACompetitor__Detail"})
                name = details.find("h2")
                winner = name.find("span").text
                data["winner"] = winner
        except Exception as e:
            print(e)
    data["match"] = " vs ".join(fighter_list)
    results["results"].append(data)
print(results)
with open('/home/ubuntu/sports_scores_api/ufc.txt', '+w') as f:
    f.write(str(results))
    f.close()
