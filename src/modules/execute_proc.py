#!/usr/bin/python

"""
Creates and executes jobs in scheduler.

MAY HAVE TO DELETE THIS

"""

import os
import time

from modules.backend.process.scraper_proc import web_scraping_proc
from modules.backend.utility_ops.utility import write_to_log


def execute_proc():

    # runs every 3 hours
    web_scraping_proc()

    time.sleep(120)
