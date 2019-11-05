# Climate Parser v1.4
A Python Script enabling extensive analysis of climate data for individual cities in the United States

### Introduction
Weather data are faithfully kept, recorded, and preserved everyday. This is primarily done via assistance of weather-stations which are plentiful and scattered-about all over the United States. This script allows the user to analyze downloaded CSV files that contain land-based station data. Within seconds, the user can retrieve daily, weekly, monthly, annual, and even climatological data, including ranking the data.

### Contents
** &bull; Go ahead and download the script `clmt_parser.py` **
* [Data Retrieval and Required Format](#data-retrieval-and-required-format)
* [Running the Script (including 'mounting' the Data)](#running-the-script)
* [Error Report Overview](#error-report)
  * [OPTIONAL: Fixing Errored Data](#fixing-data)
* Overview of Core Functions
  * Stats Search Functions - output specific to particular times
  * Report Search Functions - outputs a climatological report of historical stats and enables basic climatological-tendency analysis of desired time-frame
  * Rank Search Functions - orders the data into ranking, based on particular time-frame of interest
* On-the-fly access/reference to data
* Sample Scripts
* Roadmap
* Licensing

### Data Retrieval and Required Format

** *Some sample data for select cities are included. See repository for this data* **

To retrieve station data, goto [https://www.ncdc.noaa.gov/cdo-web/](https://www.ncdc.noaa.gov/cdo-web/).
* Scroll down a little bit and select "Search Tool"
* Under "Weather Observation Type," select *Daily Summaries*
* Determine desired range of dates. *Feel free to choose the earliest date possible. I don't know if there are any stations that go well beyond the late 1800s, but if so, the included Report functions only partially support data prior to 1811, but no errors should be encountered*
* Search for "Stations" &rarr; Input desired location &rarr; Click "Search"
* Attempt to find the major stations with data encompassing a long period of time and add them to your cart (Airports are good candidates)
* After adding the station(s) to your cart, hover over and click on cart data (on the right)
* Select "Custom GHCN-Daily CSV," double-check your date range (it is amended to fit the range of the stations you selected), and click "Continue" at the bottom

Under "Station Detail" 
* ensure that **"Geographical Location"** and **Include Data Flags** are checked

Under "Select Data Types"
* &#9745; Precipitation (ensure only PRCP, SNOW, and SNWD are selected)
* &#9745; Air Temperature (** _ONLY_ ** select TMAX and TMIN. The averages will be handled internally by the script
* Click "Continue"
* Input Email Address &rarr; "Submit Order" &rarr; and wait for a completion email

Download the data, change the name to something intuitive, and place it into the same folder as the script

* NOTE: Selecting more than one station in one cart session will result in a single combined csv.
  * If there is overlap in the records, the program will only keep the first record of a date encountered.
  * Do separate cart-checkouts for to different cities

[&#8679; back to Contents](#contents)

### Running the Script

When you load the script `clmt_parser.py`, you should see a welcome message.

Loading data is done through the `clmtAnalyze()` function.
* Find the filename of interest
  * running `csvFileList()` will return a list of CSV files in the current directory (helps if your directory is cluttered)

run `clmtAnalyze("city-data.csv")`
  * OPTIONAL: `clmtAnalyze` accepts 2 optional keyword arguments: `city="cityname.csv"` or `station="station_text"`
  * Example: `clmtAnalyze("city-name.csv",city="City Name",station="Multiple")`
  * This would be helpful if you're working with a csv that has data from multiple stations
  * The default setting would be using the [GHCND Station ID](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt) and Station Name (which typically includes the cityname)
  * You wouldn't want to represent all of the data as originating from one place if you used multiple stations

Wait for the script to complete. At the end you'll receive a notice of data missing from the record and the time it took to run the script
```
--- City: City Name, USA ---
*** SKIPPED: TMAX data missing - 1921-07
*** SKIPPED: TMIN data missing - 1921-07
*** SKIPPED: TMAX data missing - 1922-08
*** SKIPPED: TMIN data missing - 1922-08
*** SCRIPT COMPLETE ***
Runtime: 10.81 seconds
```

Now you're ready to do some analysis or inspect the data.

[&#8679; back to Contents](#contents)

### Error Report

As is with most things in life, recorded data is not perfect. When you downloaded your station data, we included Data Flags. When compiling the data, various methods were used to investigate likely errors which could've come from bad indexing or illegibility). Instead of manually checking the errors and fixing the numbers (which would be humanly impossible to do), quality flags were recorded. This script includes a function that can list dates and values with Quality Flags

`errorStats()` will do this. The vast quantity of errors are of type 'I', 'Internal Consistency Check' failure. In my limited experience, these may or may not be significant. As such, they are ignored when compiling statistics (as of this release). Hinting at something I'm going to be investigating, PRCP and SNOW errors with 'I' quality flags, may be legit. They are included in the error report but ARE included in statistics too. This may change. 
  * For example, one city I was working with showed day with 0.02 inches of PRCP, but with nearly 50 inches of SNOW (2500-to-1 snow/rain ratio! :anguished: :grimmacing:). This raised an 'I' quality flag. I personally think it should've raised a different quality flag, but alas. So in future releases, I'll be considering skipping these data points for prcp and snow values.

There's a decent chance that other non-'I' quality flags are legit errors and thus are NOT included in calculations.

One other hiccup is that days where the recorded hi (TMAX) temperature is lower than the low (TMIN) temperature typically only raises an 'I' quality flag. As of this release these values are included in statistics but I'll be looking to change this and other related items in the future.

One final note: In the giant scope of these climate data records, these likely amount to very little contribution of statistics/calculations. As such, manually modifying/fixing the data may, in large-part, be somewhat futile.

[&#8679; back to Contents](#contents)

### Fixing Data

In the event you feel it necessary to investigate and change data, there are ways to modify the data manually. This brief section outlines that processs. Loot at the list. The easiest to check are errors that occur in large groups for a single month.

##### *Verification*

If you desire to go ahead and check/verify data, 
  * Run `errorStats()`
    * Tip: Some dates may have multiple errors (for different values) associated with them. Once you've picked a date, enter dayStats(yyyy,m,d) ...this will return a basic report for that specific day with listed errors if any. This is a good way to save time
  * goto the [NCDC Image Publications System Co-Op](https://www.ncdc.noaa.gov/IPS/coop/coop.html)
  * Select the State
  * Find the station of interest (If your city had a lot of stations to choose from, use the "order summary" link located in your download email to try to match the numbers of the station).
      * If not listed, that particular data may not be available in the image archive or may be split up. Feel free to check similar stations that match the time frame you're looking for. I'd bet the most major of stations are the ones that are in the co-op
     * Determine date of interest based on the error report. The dropdown list is separated by month and year; select and continue.
	 * A temporary PDF link will appear. Go ahead and click on it

These records are scanned. Zoom in if you need to. Try to determine if an error was made with the variable in question. If you'd like, you can open a spreadsheet to document them this way. Even if it's correct in the record, make note of it so it the record may be amended.
  * I'd recommend to focus on precipitation errors first
  * Use sound judgement. But be cautious about assumptions. Yes, it didn't snow in July when the high got up to 85, but that doesn't necessarily mean the recorder meant to place the value in the rain column.
  * Records that are correct could've been flagged because the scanner or whoever oversaw it missed a decimal in the recording due to lightness of the pen/pencil.
  * Upon looking at the errors, it's likely normal to come across data where you'll be perplexed why it threw a data-quality flag. If it looks good, keep track of the right ones too.

##### *Changing Data*

A late addition to the script was the `corrections()` function. Once loading, follow the instructions that appear to make your corrections. Upon finishing it will output a new CSV file. Enter `DONE` when finished. Then you can run the `clmtAnalyze()` function on the new csv.
  * The data you just changed is active with the shell session you're working in. The changes would reflect in some, but not all, of the stat functions in the script. So it is recommended to run the `clmtAnalyze()` function on the newly amended output
  * If you forgot to make note of the dates you were checking, no worries. This function prints a little report after you're done, documenting your changes
  * You may find it thorough enough to skip the spreadsheet and rely on the output of the function.

[&#8679; back to Contents](#contents)



















