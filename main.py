import os
import json
import time
from datetime import datetime
import calendar

from mastodon import Mastodon

PROGRESS_BAR_FILLED_CHAR = '|'
PROGRESS_BAR_EMPTY_CHAR = ':'
PROGRESS_BAR_SCALAR = 1

def main():
    CREDS = get_bot_credentials()
    print('Application credentials loaded!')
    
    api = Mastodon(
        CREDS['CLIENT_ID'], 
        CREDS['CLIENT_SECRET'], 
        CREDS['ACCESS_TOKEN'],
        api_base_url='https://botsin.space'
    )
    
    posted = False
    year_percent = calculate_year_percentage()
    bar = generate_progress_bar(year_percent)
    bar += f'  {year_percent}%'
    
    while not posted:
        try:
            api.status_post(bar)
            posted = True
        except Exception:
            time.sleep(10)


def calculate_year_percentage():
    now = datetime.now()
    year_start = datetime(now.year, 1, 1)
    
    time_delta = now - year_start
    return round(time_delta.days / (365 + calendar.isleap(now.year)) * 100)

def generate_progress_bar(progress: int):
    bar: str = ''
    
    bar += PROGRESS_BAR_FILLED_CHAR * int(progress * PROGRESS_BAR_SCALAR)
    bar += PROGRESS_BAR_EMPTY_CHAR * int((100 - progress) * PROGRESS_BAR_SCALAR)
    return bar
    

def get_bot_credentials() -> dict:
    filepath = os.path.join('secrets.json')
    try:
        with open(filepath, 'r') as FILE:
            return json.loads(FILE.read())
    except FileNotFoundError:
        return {}

if __name__ == '__main__':
    main()