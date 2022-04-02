# MT Car Dealership Scraper
An application that monitors and pulls used __manual transmission__ and __automatic transmission__ car data from dealerships near me. List refreshes daily.

### The Problem
My motivations for creating this script was due to dealerships not having a functional filter for stick-shift cars. Even if the option is there available to filter, often times the automatic cars are added to the list anyway. This forces more work on the user to click on each listing and make sure the car indeed is a manual **despite** already choosing the manual transmission filter.

## About the Dataset - Ancira Car Dealership
`vin_num`: Vehicle Identification Number

`year`: year the car was manufactured

`make`: car brand or manufacturer (i.e. Ford, Hyundai, Volkswagon, etc)

`model`: category of car for that manufactur (i.e. Chevy Spark, Ford Mustang, Kia Soul, etc)

`trim`: version of the model

`body_style`: Style of the car (i.e. hatchback, 4 Door, etc)

`ext_color`: Outside color of the car

`int_color`: Interior color of the car

`transmission`: transmission of the car (i.e. Manual, Automatic)

`city_mpg`: miles per gallon (mpg) via city

`hwy_mpg`: miles per gallon (mpg) via highway

`mileage`: Overall miles the car has driven in its lifetime

`dealership`: location of which the car could be found

`price`: cost of the car in dollars ($) (Note: -1 means that the dealer does not have a price listed)

`alert_dt` : date that the code was last run

---

### Technologies Used
* Python
* Flask
* Bootstrap

## Instructions for Running via Terminal

* Open terminal
* Activate virtual env: `source venv/bin/activate`
<!-- * Run setup script: `python setup.py install` -->
* start server: `python app.py runserver`

__Note__: When you're done running the code, you're going to want to exit the virtual environment. To deactivate the virtual environment, just type: `deactivate` into the terminal.

