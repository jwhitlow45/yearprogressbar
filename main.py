import os
import time
from datetime import datetime
import calendar

from dotenv import load_dotenv
from mastodon import Mastodon

load_dotenv()

PROGRESS_BAR_FILLED_CHAR = '|'
PROGRESS_BAR_EMPTY_CHAR = ':'
PROGRESS_BAR_SCALAR = .5

RETRY_FREQUENCY = 10

def main():
    print('Application credentials loaded!')
    
    api = Mastodon(
        os.environ.get('CLIENT_ID'), 
        os.environ.get('CLIENT_SECRET'), 
        os.environ.get('ACCESS_TOKEN'),
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
            print('Toot succeeded!')
        except Exception:
            print(f'Toot failed! Retrying in {RETRY_FREQUENCY} seconds...')
            time.sleep(RETRY_FREQUENCY)
            


def calculate_year_percentage() -> str:
    now = datetime.now()
    year_start = datetime(now.year, 1, 1)
    
    time_delta = now - year_start
    return round(time_delta.days / (365 + calendar.isleap(now.year)) * 100)

def generate_progress_bar(progress: int) -> None:
    bar: str = ''
    
    bar += PROGRESS_BAR_FILLED_CHAR * int(progress * PROGRESS_BAR_SCALAR)
    bar += PROGRESS_BAR_EMPTY_CHAR * int((100 - progress) * PROGRESS_BAR_SCALAR)
    return bar

if __name__ == '__main__':
    main()