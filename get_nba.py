from bs4 import BeautifulSoup
import datetime
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


def get_nba():
    results = {'nba_results': []}
    dates = []
    for i in range(7):
        start_date = datetime.timedelta(i)
        today = datetime.date.today()
        date = today - start_date
        str_date = date.strftime('%Y%m%d')
        dates.append(str_date)
        
    for date in dates:
        driver.get(f'https://www.espn.com/nba/scoreboard/_/date/{date}')
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        events = soup.find(id='scoreboard-page')
        evs = events.find(id='events')
        games = evs.find_all('article')

        
        for x in games:
            soup = BeautifulSoup(str(x), 'html.parser')
            try:
                away_team = soup.find('tr', attrs={'class': 'away'})
                away_name = away_team.find('span', attrs={'class': 'sb-team-short'})
                away_total = away_team.find('td', attrs={'class': 'total'})
            except:
                pass
            try:
                home_team = soup.find('tr', attrs={'class': 'home'})
                home_name = home_team.find('span', attrs={'class': 'sb-team-short'})
                home_total = home_team.find('td', attrs={'class': 'total'})
            except:
                pass


            try:
                results['nba_results'].append({f'{away_name.text} vs {home_name.text}': [f'{date[0:4]}-{date[4:6]}-{date[6:9]}' ,f'{away_total.text} - {home_total.text}']})
            except:
                pass

    res = {'nba_results':[]}
    for x in results['nba_results']:
        if x not in res['nba_results']:
            res['nba_results'].append(x)
            
    with open('/home/ubuntu/sports_scores_api/nba.txt', 'w+') as f:
        f.write(str(res))
        f.close()

if __name__ == '__main__':
    get_nba()

