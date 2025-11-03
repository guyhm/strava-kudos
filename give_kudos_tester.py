import os
import time

from playwright.sync_api import sync_playwright

BASE_URL = "https://www.strava.com/"


EMAIL = os.environ.get('STRAVA_EMAIL')
PASSWORD = os.environ.get('STRAVA_PASSWORD')

if EMAIL is None or PASSWORD is None:
    raise Exception("Must set environ variables EMAIL AND PASSWORD. \
        e.g. run export STRAVA_EMAIL=YOUR_EMAIL")
print(EMAIL)
print(PASSWORD)

