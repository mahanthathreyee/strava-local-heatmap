from login_module import StravaLogin
from fetch_activities import ActivityScraper
from activity_processor import ActivityProcessor
from gpx_downloader import GPXDownloader
from gpx_processor import GPXProcessor
import constants
import time
import datetime
from dotenv import dotenv_values
import logging

config = dotenv_values(".env")
strava_login = StravaLogin(config['EMAIL_ADDRESS'], config['PASSWORD'])
strava_login.login()
strava_login.store_cookies(f"{constants.COOKIE_FILE_NAME}")
driver = strava_login.get_driver()

now = datetime.datetime.now()
year = now.year
week_number = int(now.strftime("%U"))

strava_athlete_url = f"https://www.strava.com/athletes/{constants.ATHLETE_ID}"
delay = 1
total_activity_count = 0
activity_data = []
print("Week number:", week_number)
for i in range(week_number,17,-1):
    scraper = ActivityScraper(driver, strava_athlete_url, delay)
    activity_links = scraper.fetch_activities(year, i)
    print(activity_links,len(activity_links))
    processor = ActivityProcessor(driver,total_activity_count, activity_links,activity_data)
    activity_data, total_activity_count = processor.actitivity_processor(constants.COOKIE_FILE_NAME)
    print(activity_data)
