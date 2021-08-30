#!/usr/bin/python

"""
Creates and executes jobs in scheduler.

"""

from apscheduler.schedulers.background import BackgroundScheduler
import os
import time

from backend.process.dashboard_proc import web_scraping_proc
from backend.utility_ops.utility import write_to_log


if __name__ == '__main__':
    job_id = "Ancira Webscraper"
    scheduler = BackgroundScheduler()

    # runs every 3 hours
    scheduler.add_job(web_scraping_proc, 'interval', name="Ancira Car Web-Scraper", seconds=30, id=str(job_id))

    print(f"New job id [ {str(job_id)} ] added.")
    print("Press [ Ctrl + {0} ] to exit".format("Break" if os.name == "nt" else "C"))

    try:
        scheduler.start()

        while True:
            time.sleep(10)

    except (KeyboardInterrupt, SystemExit) as e:
        write_to_log(msg=f"{e} \n")
        scheduler.shutdown()
