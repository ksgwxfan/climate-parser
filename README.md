# Climate Parser v1.4
A Python Script enabling extensive analysis of climate data for individual cities in the United States

### Introduction
Weather data are faithfully kept, recorded, and preserved everyday. This is primarily done via assistance of weather-stations which are plentiful and scattered-about all over the United States. This script allows the user to analyze downloaded CSV files that contain land-based station data. Within seconds, the user can retrieve daily, weekly, monthly, annual, and even climatological data, including ranking the data.

### Contents
* [Downloading the Scripts](#downloading-the-scripts)
* [Data Retrieval and Required Format](#data-retrieval-and-required-format)
* Opening and Initializing the Script
* Optional Maintenance of city's data
* Overview of Core Functions
  * Stats Search Functions - output specific to particular times
  * Report Search Functions - outputs a climatological report of historical stats and enables basic climatological-tendency analysis of desired time-frame
  * Rank Search Functions - orders the data into ranking, based on particular time-frame of interest
* On-the-fly access/reference to data
* Sample Scripts
* Roadmap
* Licensing

### Downloading the Scripts
test

[&#8679; back to the top](#contents)

### Data Retrieval and Required Format

<i>**Some sample data for select cities are included. See repository for this data**</i>

To retrieve station data, goto [https://www.ncdc.noaa.gov/cdo-web/](https://www.ncdc.noaa.gov/cdo-web/).
* Scroll down a little bit and select "Search Tool"
* Under "Weather Observation Type," select *Daily Summaries*
* Determine desired range of dates. *Feel free to choose the earliest date possible. I don't know if there are any stations that go well beyond the late 1800s, but if so, the included Report functions only partially support data prior to 1811, but no errors should be encountered*
* Search for "Stations" &rarr; Input desired location &rarr; Click "Search"
* Attempt to find stations with data encompassing a long period of time and add them to your cart
* After adding the station(s) to your cart, hover over and click on cart data (on the right)
* Select "Custom GHCN-Daily CSV," double-check your date range (it is amended to fit the range of the stations you selected), and click "Continue" at the bottom

Under "Station Detail" 
* ensure that **"Geographical Location"** and **Include Data Flags** are checked

Under "Select Data Types"
* &#9745; Precipitation (ensure only PRCP, SNOW, and SNWD are selected)
* &#9745; Air Temperature (**<u>ONLY</u>** select TMAX and TMIN. The averages will be handled internally by the script
* Click "Continue"
* Input Email Address &rarr; "Submit Order" &rarr; and wait for a completion email

Download the data into the same folder as the scripts

[&#8679; back to the top](#contents)
