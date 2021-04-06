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




def get_nfl():
    results = {'nfl_results': []}
    urls = ['https://www.espn.com/nfl/scoreboard']
    driver.get('https://www.espn.com/nfl/scoreboard')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    events = soup.find(id='scoreboard-page')
    event_soup = BeautifulSoup(str(events), 'html.parser')
    week = event_soup.find('div', attrs={'class': 'dropdown-wrapper width-auto hoverable desktop-dropdown dropdown-ajaxified dropdown-type-week'})
    week_soup = BeautifulSoup(str(week), 'html.parser')
    current_week = week_soup.find('button', attrs={'class': 'button-filter med dropdown-toggle'})
    print(current_week)
    last_week = int(current_week.text.strip()[-1]) - 1
    last_week_url = f'https://www.espn.com/nfl/scoreboard/_/year/2020/seasontype/2/week/{str(last_week)}'
    urls.append(last_week_url)
    for url in urls:  
        # Get page and define the scoreboard events and a bs4 soup object
        try:
            driver.get(url)
        except:
            driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        events = soup.find(id='scoreboard-page')
        event_soup = BeautifulSoup(str(events), 'html.parser')
        evs = event_soup.find(id='events')
        # Define a soup object for away wins and home wins 
        games = evs.find_all('article')
        # Loop through all available games/matches
        for game in games:
            soup = BeautifulSoup(str(game), 'html.parser')
            # Parse the soup for the name and total score of the away team
            away_team = soup.find('tr', attrs={'class': 'away'})
            away_soup = BeautifulSoup(str(away_team), 'html.parser')
            away_name = away_soup.find('span', attrs={'class': 'sb-team-short'})
            away_total = away_soup.find('td', attrs={'class': 'total'})

            # Parse the soup for the name and total score of the home team
            home_team = soup.find('tr', attrs={'class': 'home'})
            home_soup = BeautifulSoup(str(home_team), 'html.parser')
            home_name = home_soup.find('span', attrs={'class': 'sb-team-short'})
            home_total = home_soup.find('td', attrs={'class': 'total'})

            # Append the name and scores to the result json
            try:
                results['nfl_results'].append({f'{away_name.text} vs {home_name.text}':[f'Week {url[-1]}', f'{away_total.text} - {home_total.text}']})
            except:
                pass


    with open('/home/ubuntu/sports_scores_api/nfl.txt', 'w+') as f:
        f.write(str(results))
        f.close()

if __name__ == '__main__':
    get_nfl()
