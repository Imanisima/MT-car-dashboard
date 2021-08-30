#!/usr/bin/python

"""
Runs web scraper in the background and frontend
"""

import threading

from modules.backend.process.scraper_proc import web_scraping_proc
from modules.frontend.app import run_server

if __name__ == "__main__":
    # runs web scrape process every 3 hours
    print("--------------\n")

    # t1 = threading.Thread(target=web_scraping_proc)
    t2 = threading.Thread(target=run_server)

    # t1.start()
    t2.start()

    # t1.join()





