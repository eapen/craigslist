import os


SLEEP_INTERVAL = 20 * 60
MIN_PRICE = 50
MAX_PRICE = 500

CRAIGSLIST_SITE = 'sfbay'

AREAS = ["sby", "eby", "sfc", "nby"]

SECTIONS = ["hab", "spo"]

# import private settings
try:
    from private import *
except Exception:
    pass

SLACK_CHANNEL = '#leads'
try:
    SLACK_TOKEN
except NameError:
    SLACK_TOKEN = os.getenv('SLACK_TOKEN', "")

# import external private settings
try:
    from config.private import *
except Exception:
    pass
