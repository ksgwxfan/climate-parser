# Climate Parser v1.4
A Python Script enabling extensive analysis of climate data for individual cities in the United States

### Introduction
Weather data are faithfully kept, recorded, and preserved everyday. This is primarily done via assistance of weather-stations which are plentiful and scattered about all over the United States. This script allows the user to analyze downloaded CSV files that contain land-based station data. Within seconds, the user can retrieve daily, weekly, monthly, annual, and even climatological data, including ranking the data.

### Contents
* [Data Retrieval and Required Format](#data-retrieval-and-required-format)
* Opening the Script
* Optional Maintenance of city's data
* Overview of Core Functions
  * Stats Search Functions - output specific to particular times
  * Report Search Functions - outputs a climatological report of historical stats and enables basic climatological-tendency analysis of desired time-frame
  * Rank Search Functions - orders the data into ranking, based on particular time-frame of interest
* On-the-fly access/reference to data
* Sample Scripts
* Roadmap
* Licensing

### Data Retrieval and Required Format

* To retrieve station data, goto [https://www.ncdc.noaa.gov/cdo-web/](https://www.ncdc.noaa.gov/cdo-web/).
* Scroll down a little bit and select "Search Tool"
* Under "Weather Observation Type," select *Daily Summaries*
* Determine desired range of dates. <font style="font-size: .7em;">*Feel free to choose the earliest date possible. I don't know if there are any stations that go well beyond the late 1800s, but if so, the included Report functions only partially support data prior to 1811, but no errors should be encountered*</font>
* Search for "Stations" &rarr; Input desired location &rarr; Click "Search"
* Attempt to find stations with data encompassing a long period of time and add them to your cart
* After adding the station(s) to your cart, hover over and click on cart data (on the right)
* Select "Custom GHCN-Daily CSV," double-check your date range (it is amended to fit the range of the stations you selected), and click "Continue" at the bottom 

