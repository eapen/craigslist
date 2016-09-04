#! /bin/bash

HOST=$1
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
rsync -avz --exclude craigslist.db --exclude __pycache__ ../ $HOST:~/craigslist
ssh $HOST '/bin/bash -s' < setup_scraper.sh
