#!/usr/bin/python

"""
Contains main methods for running each job.

"""
import pandas as pd
from bs4 import BeautifulSoup
import requests

# from timeloop import Timeloop
from datetime import timedelta

import time

from modules.backend.utility_ops.anc_utility import check_pagination, retrieve_vehicles
from modules.backend.utility_ops.utility import check_path, write_to_log

# tl = Timeloop()

# @tl.job(interval=timedelta(seconds=10))
def web_scraping_proc(job_name="Car Web-Scraper",
                      dataset_dir="modules/frontend/",
                      car_csv_file="ancira_mcar_listing.csv",
                      mcar_csv_file="ancira_mcar_listing.csv"):

    """
	Web scraper that pulls data and creates a dataset to track manual transmission and automatic transmission cars.

	PARAMETERS
		job_name : str
			Name of the process or job
		dataset_dir : str
		    directory or name of folder to save the dataset
		all_used_dataset : str
		    name of the csv file to save all used vehicles
		mt_dataset : str
		    name of the csv file to save manual transmission vehicles

	RETURNS
		Nothing
	"""

    write_to_log(msg=f"Now starting {job_name} process")

    domain = 'https://www.ancira.com'
    home_link = '/used-car-truck-suv-for-sale-san-antonio-tx.html?pn=100'  # subquery
    home_url = domain + home_link

    write_to_log(msg=f"Requesting {home_url}")
    res = requests.get(home_url)
    write_to_log(msg=f"Request message - {res}")

    write_to_log(msg=f"Getting content using BeautifulSoup")
    soup = BeautifulSoup(res.content, 'lxml')

    write_to_log(msg=f"Checking pagination links")
    page_list = check_pagination(soup, home_link)

    # all cars no matter the transmission
    write_to_log(msg=f"Retrieving vehicle information")
    veh_df = retrieve_vehicles(page_list, domain)

    veh_df["transmission"] = veh_df["transmission"].str.lower()
    veh_df.loc[veh_df['transmission'].str.contains('manual', case=False), 'transmission'] = 'manual'
    veh_df.loc[veh_df['transmission'] != 'manual', 'transmission'] = 'automatic'

    write_to_log(msg=f"{veh_df.shape[0]} rows retrieved.")
    write_to_log(msg=f"{veh_df.shape[1]} columns retrieved.")
    write_to_log(msg=f"Column names are {veh_df.columns}")

    # check_path(dataset_dir)
    # all car data
    write_to_log(msg=f"saving all car data.")
    dataset_path = dataset_dir + car_csv_file
    veh_df.to_csv(dataset_path, index=False)
    write_to_log(msg=f"{veh_df.shape[0]} rows saved.")
    write_to_log(msg=f"{veh_df.shape[1]} columns saved.")

    # manual transmission data
    write_to_log(msg=f"saving manual_trans data.")
    mveh_df = veh_df.loc[veh_df['transmission'] == "manual"]
    mveh_df.to_csv(dataset_dir + mcar_csv_file, index=False)
    write_to_log(msg=f"{mveh_df.shape[0]} rows saved.")
    write_to_log(msg=f"{mveh_df.shape[1]} columns saved.")

    write_to_log(msg=f"Process finished running! \n")

    # time.sleep(300)
