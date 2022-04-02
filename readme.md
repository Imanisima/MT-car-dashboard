# MT Car Dealership Scraper
An application that monitors and pulls used __manual transmission__ and __automatic transmission__ car data from a chain of local dealerships in San Antonio, TX. List refreshes daily.

### The Problem
Dealerships do not always have a functional filter for stick-shift cars. Even when the transmission filtering option is available, it is quitee common that automatic cars are added to the results. This forces the user to double check that the car they are viewing is indeed a manual **despite** using the filter or entering the kywords `manual transmission cars` into the searchbar.

### Technologies Used
* Python
* Flask
* Bootstrap
* Plotly Express

### Instructions for Running via Terminal

* Open terminal
* Activate virtual env: `source venv/bin/activate`
* start server: `python app.py runserver`

__Note__: When you're done running the code, you're going to want to exit the virtual environment. To deactivate the virtual environment, just type: `deactivate` into the terminal.

### How to Use
Once you have found a car listing that interests you, go to the ![ancira](ancira.com) website and paste the VIN number into the search bar!

---

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

