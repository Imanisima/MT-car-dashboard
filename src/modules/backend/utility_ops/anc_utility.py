#!/usr/bin/python

"""
Contains methods for retrieving car data.

"""

from bs4 import BeautifulSoup
from datetime import date

import pandas as pd

import re
import requests


def check_pagination(soup, home_link):
    """
	Get all the page links from pagination

	PARAMETERS
		soup : Beautifulsoup obj
			soup = BeautifulSoup(res.content, 'lxml')
		home_link : str
			subquery after the domain url

	RETURNS
		list
	"""

    pagination = soup.find('ul', class_="pagination-sm")
    page_list = pagination.find_all_next('li')

    page_link_arr = [home_link]

    for page in page_list:
        new_page = page.find("a", class_="stat-icon-link")

        if new_page is not None and new_page.get('href') is not None and new_page.get('href') not in page_link_arr:
            page_link_arr.append(new_page.get('href'))

    return page_link_arr


def ret_car_price(veh):
    """
	Get the car price listed by the dealer.

	PARAMETERS
		veh : soup div object from veh_list
			veh_list = soup.find_all("div", class_="srpVehicle")

	RETURNS
		str
	"""

    if veh.get('data-price') == "0":
        return "-1"
    else:
        return veh.get('data-price').strip()


def ret_dealership(veh):
    """
	Return the dealership that has the car

	PARAMETERS
		veh : soup div object from veh_list
			veh_list = soup.find_all("div", class_="srpVehicle")

	RETURNS
		str
	"""

    if veh.find("li", class_="dealershipDisplay") is not None:
        deal_display = veh.find("li", class_="dealershipDisplay").getText()
        dealer = deal_display.split(":", 1)[1]
        return dealer.strip()
    else:
        return "-1"


def ret_ext_color(veh):
    """
	Return the exterior color of the car

	PARAMETERS
		veh : soup div object from veh_list
			veh_list = soup.find_all("div", class_="srpVehicle")

	RETURNS
		str
	"""

    if veh.find("li", class_="extColor") is not None:
        ext_color = veh.find("li", class_="extColor").getText()
        ext_color = ext_color.split(":", 1)[1]
        return ext_color.strip()
    else:
        return "-1"


def ret_int_color(veh):
    """
	Return the interior color of the car.

	PARAMETERS
		veh : soup div object from veh_list
			veh_list = soup.find_all("div", class_="srpVehicle")

	RETURNS
		str
	"""

    if veh.find("li", class_="intColor") is not None:
        int_color = veh.find("li", class_="intColor").getText()
        int_color = int_color.split(":", 1)[1]
        return int_color.strip()
    else:
        return "-1"


def ret_mileage(veh):
    """
	Return the overall mileage of the car.

	PARAMETERS
		veh : soup div object from veh_list
			veh_list = soup.find_all("div", class_="srpVehicle")

	RETURNS
		str
	"""

    if veh.find("li", class_="mileageDisplay") is not None:
        mile_display = veh.find("li", class_="mileageDisplay").getText()
        miles = re.sub('[^0-9]', '', mile_display)
        return miles.strip()
    else:
        return "-1"


def retrieve_vehicles(page_list, domain):
    """
	Retrieve all vehicles listed in each page of the used car site and save to a dataframe to be exported later.

	PARAMETERS
		page_list : list
			a list of urls to track pagination pages

		domain : str
			domain name of a website (i.e. www.google.com, www.github.com)

	RETURNS
		dataframe
	"""

    vin = []
    make = []
    model = []
    year = []
    body_style = []
    trim = []
    interior = []
    exterior = []

    trans_type = []
    city_mpg = []
    hwy_mpg = []

    mileage = []
    price = []

    dealership = []
    alert_dt = []

    # From the list of pagination links, iterate through each link
    for page in page_list:
        url = domain + page
        veh_res = requests.get(url)

        # Save all the vehicles displayed on this one page in a list
        soup = BeautifulSoup(veh_res.content, 'lxml')
        veh_list = soup.find_all("div", class_="srpVehicle")

        # For each vehicle listed on this page, save its exterior and interior details into lists
        for veh in veh_list:
            vin_num = ret_vin_num(veh)
            vin.append(vin_num)

            year.append(veh.get('data-year').strip())
            make.append(veh.get('data-make').strip())
            model.append(veh.get('data-model').strip())
            trim.append(veh.get('data-trim').strip())
            body_style.append(veh.get('data-bodystyle').strip())

            # Get interior color of the car
            int_color = ret_int_color(veh)
            interior.append(int_color)

            # Get exterior color of the car
            ext_color = ret_ext_color(veh)
            exterior.append(ext_color)

            # Get car transmission
            trans_type.append(veh.get('data-trans').strip())

            # Get car gas mileage
            city_mpg.append(veh.get('data-mpgcity').strip())
            hwy_mpg.append(veh.get('data-mpghwy').strip())

            # Get the overall mileage of the car
            miles = ret_mileage(veh)
            mileage.append(miles)

            # Get the price of the car
            car_price = ret_car_price(veh)
            price.append(car_price)

            # Get the dealership of which the car is at
            dealer = ret_dealership(veh)
            dealership.append(dealer)

            # Record the date that this code was last run
            alert_dt.append(date.today())

    # Save lists about the vehicles into a dataframe to be exported later.
    df = pd.DataFrame(vin, columns=["vin_num"])
    df['year'] = year
    df['make'] = make
    df['model'] = model
    df['trim'] = trim
    df['body_style'] = body_style
    df['ext_color'] = exterior
    df['int_color'] = interior

    df['transmission'] = trans_type

    df['city_mpg'] = city_mpg
    df['hwy_mpg'] = hwy_mpg

    df['mileage'] = mileage
    df['price'] = price

    df['dealership'] = dealership
    df['alert_dt'] = alert_dt

    return df


def ret_vin_num(veh):
    """
	Return the VIN number of the car.

	PARAMETERS
		veh : soup div object from veh_list
			veh_list = soup.find_all("div", class_="srpVehicle")

	RETURNS
		str
	"""

    if veh.find("li", class_="vinDisplay") is not None:
        vin_display = veh.find("li", class_="vinDisplay").getText()
        vin_num = vin_display.split(":", 1)[1]
        return vin_num.strip()
    else:
        return "-1"