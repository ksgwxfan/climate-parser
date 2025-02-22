# Climate Parser v2.9x
A Python Script enabling extensive analysis of climate data for individual cities in the United States

### Requirements
* This script was written with Python 3.7x installed; no 3rd-party modules need to be installed

### Introduction
Weather data are faithfully kept, recorded, and preserved everyday. This is primarily done via assistance of weather-stations which are plentiful and scattered-about all over the United States. This script allows the user to analyze downloaded CSV files that contain land-based station data. Within seconds, the user can retrieve daily, weekly, monthly, annual, and even climatological data, including ranking the data.

### Contents
**&bull; Go ahead and download the script** `clmt_parser.py`
* [Fixes / Changes](#fixes-and-changes)
* [Data Retrieval and Required Format](#data-retrieval-and-required-format)<br />
* [Running the Script / Loading the Data](#running-the-script)
* [A Note on Record Thresholds](#a-note-on-record-thresholds)
* [Error Report Overview (skip if you just want to go to analyzing the data)](#error-report)
  * [OPTIONAL: Fixing Errored Data](#fixing-data)
* [Overview of Core Functions](#overview-of-core-functions)
  * [Stats Search Functions](#stats) - output specific to particular times
  * [Report Search Functions](#reports) - outputs a climatological report of historical stats and enables basic climatological-tendency analysis of desired time-frame
  * [Rank Search Functions](#ranking) - orders the data into ranking, based on particular time-frame of interest
  * [Value Searching the Record](#valueSearch) - search the record based on specific value thresholds
* [On-the-fly access/reference to data](#on-the-fly-data-retrieval)
* Sample Scripts (to be added later)
* [Roadmap](#roadmap)
* [Licensing](#license)
* [HELP!!!](#help)

### Recent Fixes and Changes

##### v2.92
* Deprecated (and removed) the `clmt_len_rpt` and `clmt_inc_rpt` variables... I upgraded all Report functions to include default keyword arguments, `climatology=30` and `increment=5` and `output=False`, all of which are accessible and edit-ready upon call of the Report function if one so chooses. Otherwise, the defaults listed above will be used.
* Patched-up (notice I didn't say "fixed") a major problem with `dayReport` where little to no daily average temperatures were being recorded. So the report was printing, but the reported avg temps weren't representative of reality. I had used short-circuiting for error addressing and it inadvertently "hid" the problem.

##### v2.91
* added `custom` kwarg to `allDayRank`. This will allow you to limit the scope of ranking to a specific time-interval. Example: `allDayRank("prcp",20,custom=[9,21,3,20])` would only list the ranking if a day falls between September 21 and March 20

##### v2.9
* fixed output issue in `dayRank` where it was trying to output ranks that weren't asked for; caused by me being lazy about putting in a single logic statement.
* fixed 'dayRank' output issue where if the length of a variable (i.e. `snwd`) was empty, it was throwing an `AttributeError`
* added `snwd` to the standard initialization scheme. Just added yearly/monthly lists of &gt; 0 quantities and total days
* added output to `monthStats`,`yearStats`,'seasonStats', `metYearStats`, and `customStats` to reflect quantity of days snow was reported on the ground (snow-depth;`snwdDAYS`)
* added standardized conditioning to `metclmt` initialization to match `clmt` init
* fixed a problem in `customStats` where ranking wasn't printing in spots. Out of necessity/convenience, I had used a`except` block to print a newline, which once investigated, I had used a wrong variable name in the `try` block.
* added `"prcpDAYS"`, `"snowDAYS"`, and `"snwdDAYS"` to the `clmt_vars_months` dictionary, init scheme, and compatibility to `allMonthRank` as accepted attributes
* modified `customStats` to accept no more than a year's period; may change this back in future versions if I feel like working out a way to rank multi-year scopes

*Please see CHANGELOG.md for a more extensive list of changes

[&#8679; back to Contents](#contents)

### Data Retrieval and Required Format

***Some sample data for select cities are included. See repository for this data. Ensure that they are placed in the same directory as script***

To retrieve station data, goto [https://www.ncdc.noaa.gov/cdo-web/](https://www.ncdc.noaa.gov/cdo-web/).
* Scroll down a little bit and select "Search Tool"
* Under "Weather Observation Type," select *Daily Summaries*
* Determine desired range of dates. *TIP: Choose the earliest date possible(like 1763). I don't know if there are any stations that go back that far but it ensures the maximum duration selection*
* You're given different options of how to search.
  * I'd recommend to search by *City* or *State*. Input a search term, and then search
  * Find the city or state you're wanting, and click on *View Full Details*
  * Then under *Included Stations*, select *See Station List Below*
  * This will allow you to sort the stations in the vicinity by name, start/end date, or coverage.
* You ideally want to find a station whose records are of a long period, still maintained, and has really good coverage of data (&gt;90%). Data from airports are generally very-well maintained, but as planes weren't developed until after 1900, with airports not well-established until deep into the 20th century, The records for these won't go fully back.
  * In a situation like this, it's recommended to seek another station to add to the cart. Overlap of time-period is normal, but you should attempt to keep the overlap small.
* Add the station(s) that you pick out to your cart
* Hover over and click on cart data (on the right)
* Select *Custom GHCN-Daily CSV*, double-check your date range (it is amended to fit the range of the stations you selected), and click *Continue* at the bottom

Under "Station Detail" 
* ensure that **Geographical Location** AND **Include Data Flags** are checked

Under "Select Data Types"
* &#9744; Precipitation 
  * &#9745; Precipitation (PRCP)
  * &#9745; Snow depth (SNWD)
  * &#9745; Snowfall (SNOW)
* &#9744; Air Temperature
  * &#9745; Maximum temperature (TMAX)
  * &#9745; Minimum temperature (TMIN)
* Ensure that only the 5 variables above are selected
* Click "Continue"
* Input Email Address &rarr; "Submit Order" &rarr; and wait for a completion email

Download the data, change the name to something intuitive, and place it into the same folder as the script
* NOTE: Selecting more than one station in one cart session will result in a single combined csv.
  * The script is programmed to do a basic-handle of multiple stations. If there is overlap, it always keeps the data from the date of the first station. This is okay, but may not be fully desired if there is a large overlap.
  * Do separate cart-checkouts for to different cities
  * As CSV's are just text, a notepad program can be used to cut/paste data out of, or manuevered around, the text file. It's recommended to do this outside of a spreadsheet program to ensure preservation of the data inside quotations. This is vital for the script to work correctly.
    * You may feel this to be necessary if you'd rather one station's data to be preferred over another.

[&#8679; back to Contents](#contents)

### Running the Script

When you load the script `clmt_parser.py`, you'll see a list of csv files with a number in front. The prompt will ask you which file you'd like to mount/load. Enter the number. It also supports a custom city name. This is beneficial if using multiple stations from one general location. You can always bring up this prompt again by entering `clmtmenu()` to load a different file. This replaces the deprecated 'csvFileList' function.
```
*** Run this function again by entering clmtmenu() ***
-----------------------------------------------------------
  1. RenoNV_alltime.csv
  2. CHI_IL_1940_2019.csv
  3. clmt-TALLAHASSEE_2stations_1899_2019.csv
-----------------------------------------------------------
Enter Selection: 3, Tallahassee, FL
```

Wait for the script to complete. At the end you'll receive a notice of monthly data missing from the record and the time it took to run the script
```
--- City: City Name, USA ---
*** SKIPPED: Insufficient or erroneous TMAX data - 1893-03
*** SKIPPED: Insufficient or erroneous TMIN data - 1893-03
*** SKIPPED: Insufficient or erroneous TMAX data - 1921-07
*** SCRIPT COMPLETE ***
Runtime: 11.06 seconds
```

Now you're ready to do some analysis or inspect the data.

[&#8679; back to Contents](#contents)

### Changeable Climatology Report-Related Variables

DEPRECATED and REMOVED! Check the [Report Search Functions](#reports) section for better (much more user-friendly) method...

[&#8679; back to Contents](#contents)

### A Note on Record Thresholds

A big part that is played in compiling reports and ranks is the exclusion of data if it is deemed insufficient or incomplete. The idea is to prevent, for example, years with only 50 days of data, all happening to be in the spring and summer months, from bothering yearly-ranks and reports. To handle this, I used exclusion thresholds. In v2.0 or newer, these variables are accessible at the end of the script, to allow you to tinker with if desired. For example, for yearly ranks, the default threshold is 300 days. Change it if you feel it is too lenient or not lenient enough of a standard. Just change the variable, and run your function again. When changing, to ensure the most accurate results, run `clmtAnalyze` again. This potentially would alter the rankings. The following are the default values found at the end of the script:
```
excludeyear = 300       # Exclude years from ranking/reports if year recordqty <= to this threshold
excludeseason = 70      # Exclude season from rankings/reports if season recordqty <= to this threshold
excludemonth = 20       # Exclude months from ranking/reports if month recordqty <= to this threshold
excludeweek = 4         # Exclude weeks from ranking/reports if week recordqty <= to this threshold
```
In general, these thresholds are not used when determining precipitation maximums, but are used when calculating the driest months. So a month may only have 10 days of data, but if it ends up being the rainiest month, it'll show up in the ranks. But it won't if it is one of the driest months.

Temperatures always use the thresholds, but uses the number of days with temperatures recorded, rather than the `recordqty`, as it's possible that temperature data is missing from a present daily-record

[&#8679; back to Contents](#contents)

### Error Report

As is with most things in life, recorded data is not perfect. When you downloaded your station data, included were Data Flags. When compiling the data, various methods were used to investigate likely errors which I guess could've come from bad indexing or illegibility. Instead of manually checking the errors and fixing the numbers (which would be humanly impossible to do), quality flags were recorded. This script includes a function that can list dates and values with Quality Flags

`errorStats()` will do this. The vast quantity of errors are of type 'I', 'Internal Consistency Check' failure. In my limited experience, these may or may not be significant. The default setting is to skip over all values with any kind of quality flag.
* For example, one city I was working with showed day with 0.02 inches of PRCP, but with nearly 50 inches of SNOW (2500-to-1 snow/rain ratio! :anguished: :grimacing:). This raised an 'I' quality flag. I personally think it should've raised a different quality flag, but alas.
* The error report also lists days where the high-temperature (TMAX) is lower than the low-temperature (TMIN). These are also excluded from the stat functions as it's impossible to tell exactly which of the two recorded temperatures are wrong.

It is possible to change the flags which are ignored.
* Enter `qflagcheck()` to get a list of the abbreviations of possible flag-types you'll run across.
* to add a flag to ignore, enter `ignoreflags.append("I")`, where "I" is the example flag we want to include in our calculations
* to remove a flag from the ignore list, (as such to skip over data with the quality flag), enter `ignoreflags.remove("I")
* These flags MUST be capitalized strings for it to work properly

[&#8679; back to Contents](#contents)

### Fixing Data

This is advanced, and frankly, not very fun. Feel free to skip. Just know that by default, no data is included if it has been quality-flagged in any way.

In the giant scope of these climate data records, these errors or flagged data probably contribute a very small amount to statistics/calculations. As such, manually modifying/fixing the data may, in large-part, be somewhat futile. You may feel it is important for ranking purposes. If anything, you may feel it is important to check/verify the data, and report it to the NCDC. In the event you feel it necessary to investigate and change data, there are ways to modify the data manually. This section outlines that process

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

A late addition to the script was the `corrections()` function. Identify the date and attribute you wish to change.

Example of use:
```
CORRECTIONS MODE ACTIVATED - CITY, USA
------------------------------------------------
* Input a comma-separated list of the Year, Month, Date, Attribute, and new reading
* Ex: INPUT CORRECTION: 1899,1,30,"prcp",2.02
* When finished, type DONE and press enter
INPUT CORRECTION: 1940,6,2,"tmax",79
    Amendment for 1940-06-02 TMAX successful: 79
```

After you finish, enter `DONE`. The function will spit out two files:
* An amended version of the data with the changes you made reflected in it. Ex: `AMENDED_city_data.csv`
* A changes csv which records the changes you made. The csv format makes it convenient to load in a spreadsheet Ex: `CHG_20191108_1245_city_data.csv`
  * After completion of each run of `corrections()`, a different changes file will be generated

The data you just changed is active with the shell session you're working in. The changes would reflect in some, but not all, of the stat functions in the script. So it is recommended to run the `clmtAnalyze()` function on the newly amended version of the data

[&#8679; back to Contents](#contents)

### Overview of Core Functions

The "bread-and-butter" of this program is to quickly generate output that would be of most interest to the scientist/researcher/hobbyist. These core functions are generally broken-up into three categories: Stats, Reports, and Ranking

#### Stats

These are a set of functions to get info specific info based on a desired temporal length: `dayStats(y,m,d)`, `weekStats(y,m,d)`, `monthStats(y,m)`, `yearStats(y)`, `metYearStats(y)`, `seasonStats(y,season)`, `customStats(y1,m1,d1,*[y2,m2,d2])`

Simple report retrieved for desired day
```
>>> dayStats(2000,12,25)

Statistics for 2000-12-25
Report Location: USW00001337, CITY USA
-------------------
PRCP: 0.01, Rank: 21st
SNWD: 11.0, Rank: 7th
TMAX: 12, Rank: 13th Coolest
TMIN: -17, Rank: 4th Coolest

```

Delivered stats based on a 7-day week with the submitted date being the center of that period
```
>>> weekStats(2014,2,14)

                 Weekly Statistics for 2014-02-11 thru 2014-02-17
                              USC0001337: CITY, USA
                              Quantity of Records: 7
       '*' Denotes existance of quality flag; not included in average stats
-----------------------------------------------------------------------------------
      |   2014   |   2014   |   2014   |   2014   |   2014   |   2014   |   2014
      |  Feb 11  |  Feb 12  |  Feb 13  |  Feb 14  |  Feb 15  |  Feb 16  |  Feb 17
------|----------|----------|----------|----------|----------|----------|----------
 PRCP |  0.00T   |   0.00   |   1.20   |   0.47   |   0.02   |   0.00   |   0.00
 SNOW |   0.0    |   0.0    |   8.6    |   2.6    |   0.0    |   0.0    |   0.0
 SNWD |   0.0    |   0.0    |   8.0    |   11.0   |   7.0    |   5.0    |   4.0
 TMAX |    40    |    39    |    30    |    41    |    56    |    39    |    52
 TMIN |    27    |    20    |    21    |    30    |    32    |    22    |    22

Total Precipitation: 1.69, Rank: 18
Total Precipitation Days (>= T): 4
Total Snow: 11.2, Rank: 2
Total Snow Days (>= T): 2
Average Snow Depth: 5.0, Rank: 1
Average Temperature: 33.6, Rank: 19th Coolest
Average Max Temperature: 42.4, Rank: 13th Coolest
Average Min Temperature: 24.9, Rank: 28th Coolest
```
Get stats for the specified month
```
>>> monthStats(2005,12)
-------------------------------------
Monthly Statistics for December 2005
USC00001337: CITY, USA
Quantity of Records: 31
* Reported rankings are relative to the month of December
-----
Total Precipitation: 1.96, 24th Driest
Total Precipitation Days (>= T): 8
-- Highest Daily Precip: 1.09 ::: 2000-12-17
Total Snow: 2.0, 31st Snowiest
Total Snow Days (>= T): 1
-- Highest Daily Snow Total: 2.0 ::: 2000-12-20
Average Temperature: 29.8, 2nd Coolest
Average MAX Temperature: 41.2, 2nd Coolest
-- Warmest Daily TMAX: 56 ::: 2000-12-09
-- Coolest Daily TMAX: 27 ::: 2000-12-31
Average MIN Temperature: 18.4, 2nd Coolest
-- Warmest Daily TMIN: 33 ::: 2000-12-17
-- Coolest Daily TMIN: 7 ::: 2000-12-23
-----
```
Return stats for the specified year
```
>>> yearStats(1990)
-------------------------------------
>>> yearStats(1984)

              Yearly Statistics for 1984
                 US00001337: CITY, USA
               Quantity of Records: 365
-------------------------------------------------------
      |  JAN  |  FEB  |  MAR  |  APR  |  MAY  |  JUN  |
-------------------------------------------------------
 PRCP |  0.67 |  1.19 |  3.22 |  3.97 |  6.20 |  5.22 |
 SNOW |   3.2 |  10.8 |  14.3 |  21.8 |   --  |   --  |
 TAVG |  19.6 |  26.9 |  34.2 |  42.2 |  54.6 |  68.0 |
 TMAX |  27.0 |  32.1 |  40.5 |  50.9 |  64.8 |  78.0 |
 TMIN |  12.1 |  21.6 |  27.9 |  33.6 |  44.4 |  57.9 |
-------------------------------------------------------
      |  JUL  |  AUG  |  SEP  |  OCT  |  NOV  |  DEC  |
-------------------------------------------------------
 PRCP |  3.07 |  3.12 |  3.34 |  2.61 |  4.93 |  1.53 |
 SNOW |   --  |   --  |   --  |   0.0 |  30.4 |  21.0 |
 TAVG |  77.2 |  76.7 |  62.6 |  48.4 |  34.0 |   3.7 |
 TMAX |  87.0 |  87.0 |  71.6 |  56.4 |  39.0 |  11.1 |
 TMIN |  67.4 |  66.5 |  53.6 |  40.3 |  29.0 |  -3.8 |
-------------------------------------------------------
 Total Precipitation: 39.07, Rank: 5th Wettest
 Total Precipitation Days (>=T): 210, Rank: 8th Most
 -- Highest Daily Precip: 1.65 ::: 1983-07-03
 Total Snow: 101.5, Rank: 1st Snowiest
 Total Snow Days (>=T): 93, Rank: 10th Most
 Average Temperature: 45.8, Rank: 30th Warmest
 Avg MAX Temperature: 53.9, Rank: 23rd Coolest
 -- Warmest Daily TMAX: 97 ::: 1983-08-07
 -- Coolest Daily TMAX: -17 ::: 1983-12-23
 Avg MIN Temperature: 37.6, Rank: 21st Warmest
 -- Warmest Daily TMIN: 79 ::: 1983-07-21
 -- Coolest Daily TMIN: -29 ::: 1983-12-19
-----
```
Return stats for the specified Meteorological Year (March-February)
```
>>> metYearStats(1993)

                 Statistics for Meteorological Year 1993
                         US000001337: CITY, USA
                        Quantity of Records: 365
-------------------------------------------------------------------------
      | MAR 1993 | APR 1993 | MAY 1993 | JUN 1993 | JUL 1993 | AUG 1993 |
-------------------------------------------------------------------------
 PRCP |    7.26  |    3.15  |    4.34  |    1.41  |    2.97  |    3.79  |
 SNOW |    11.0  |     --   |     --   |     --   |     --   |     --   |
 TAVG |    44.2  |    55.0  |    65.9  |    72.7  |    78.1  |    74.0  |
 TMAX |    54.3  |    68.4  |    78.2  |    85.8  |    91.0  |    86.0  |
 TMIN |    34.7  |    41.7  |    53.6  |    59.6  |    65.3  |    61.8  |
-------------------------------------------------------------------------
      | SEP 1993 | OCT 1993 | NOV 1993 | DEC 1993 | JAN 1994 | FEB 1994 |
-------------------------------------------------------------------------
 PRCP |    5.34  |    1.68  |    4.42  |    4.74  |    6.30  |    4.63  |
 SNOW |     --   |     --   |     --   |     6.3  |     2.5  |     1.5  |
 TAVG |    69.1  |    54.2  |    45.3  |    34.9  |    30.2  |    37.5  |
 TMAX |    80.0  |    69.2  |    57.9  |    45.6  |    40.3  |    49.3  |
 TMIN |    57.5  |    39.4  |    32.6  |    24.6  |    20.7  |    25.7  |
-------------------------------------------------------------------------
 Total Precipitation: 50.03, Rank: 41st Wettest
 Total Precipitation Days (>=T): 134, Rank: 23rd Most
 -- Highest Daily Precip: 3.2 ::: 1993-11-28
 Total Snow: 21.3, Rank: 8th Snowiest
 Total Snow Days (>=T): 6, Rank: 7th Least
 Average Temperature: 56.0, Rank: 18th Coolest
 Avg MAX Temperature: 67.4, Rank: 10th Coolest
 -- Warmest Daily TMAX: 97 ::: 1993-07-10
 -- Coolest Daily TMAX: 15 ::: 1994-01-16
 Avg MIN Temperature: 43.8, Rank: 22nd Coolest
 -- Warmest Daily TMIN: 71 ::: 1993-07-20
 -- Coolest Daily TMIN: -2 ::: 1994-01-19,  1994-01-20
```
Retrieve stats of a certain season (meteorological)
```
>>> seasonStats(1955,"autumn")
----------------------------------------
Seasonal Statistics for Meteorological Fall 1955
         USC00001337: CITY, USA
        Quantity of Records: 91
----------------------------------------
      | SEP 1955 | OCT 1955 | NOV 1955 |
 PRCP |    0.59  |    1.92  |    1.60  |
 SNOW |     --   |     --   |     --   |
 TAVG |    70.4  |    57.1  |    45.4  |
 TMAX |    81.9  |    72.0  |    59.9  |
 TMIN |    58.9  |    43.0  |    31.0  |
----------------------------------------
 Total Precipitation: 4.11, Rank: 9th Driest
 Total Precipitation Days (>=T): 22, Rank: 12th Least
 -- Highest Daily Precip: 0.83 ::: 1955-10-08
 Average Temperature: 57.6, Rank: 27th Coolest
 Avg MAX Temperature: 71.2, Rank: 29th Warmest
 -- Warmest Daily TMAX: 93 ::: 1955-09-19
 -- Coolest Daily TMAX: 35 ::: 1955-11-29
 Avg MIN Temperature: 44.3, Rank: 30th Coolest
 -- Warmest Daily TMIN: 66 ::: 1955-09-23
 -- Coolest Daily TMIN: 14 ::: 1955-11-29
-----
```

Return stats for a custom time-frame; if you don't include an ending date, by default December 31 of that year will be used
```
>>> customStats(1999,12,1,2000,1,15)

Statistics for 1999-12-1 thru 2000-1-15
USW00001337: TOWN, USA
Quantity of Records: 46
-------------------------------------
 Total Precipitation: 0.97
 Total Precipitation Days (>=T): 19, Rank: 7th Least
 -- Highest Daily Precip: 0.3 ::: 2000-01-12
 Total Snow: 19.7, Rank: 22nd Snowiest
 Total Snow Days (>=T): 16
-- Snowiest Day: 8.7 ::: 2000-01-12
 Average Temperature: 24.4, Rank: 9th Warmest
 Avg MAX Temperature: 32.2, Rank: 7th Warmest
 -- Warmest Daily TMAX: 53 ::: 1999-12-29
 -- Coolest Daily TMAX: 6 ::: 1999-12-21
 Avg MIN Temperature: 16.5, Rank: 13th Warmest
 -- Warmest Daily TMIN: 36 ::: 1999-12-02
 -- Coolest Daily TMIN: -8 ::: 1999-12-21
-----
```

[&#8679; back to Contents](#contents)

#### Reports

These functions return robust climatological data, including all-time statistics and for climatological eras. As mentioned before, by default, the calculated values are for 30-year periods incremented by 5 years. This enables, what I refer to as, climatological-tendency analysis. This allows you to see how the averages change over time, as comparisons of a day's, month's, or year's data usually only takes place against one time period. How is the long-term average changing? I believe it simplifies analysis and makes it easier to see trends.

In version 2.9x, each report function was upgraded to accept optional keyword arguments for climatology length, increment, and output. This makes it significantly easier over previous versions to customize your report. The climatology length should always be greater than the increment. The smaller the increment, the finer the details seen when doing climatological tendency analysis.

* So if you wanted a 10-year climatology, incremented every 1 year, you would include `climatology=10, increment=1` in the function call.
* If you wanted to output a CSV report, simply include `output=True` in the call. It will place it in the directory of the script.

`dayReport(m,d, climatology=30, increment=5, output=False)` :: Collects and returns statistics for all specified days in the record
`weekReport(m,d, climatology=30, increment=5, output=False)` :: Gathers and reports for specified week in the entire record
`monthReport(m, climatology=30, increment=5, output=False)` :: Gives a report for a specific month
`yearReport(climatology=30, increment=5, output=False)` :: Analyzes the entire record and returns a report based on years; no passed-data is needed
`metYearReport(climatology=30, increment=5, output=False)` :: Same as above, but does so based on meteorological years (March-February)
`seasonReport(season, climatology=30, increment=5, output=False)` :: Gets a meteorologically-seasoned based statistic report
`customReport(m1,d1,*[m2,d2], climatology=30, increment=5, output=False)` :: Gets a climatolgical report based on the user-defined custom time-frame

```
>>> monthReport(12)
--------------------------------
Climatology Report for December
City: USC00001337, CITY, USA
1893-2019; 5-Year Incremented 30-Year Climatologies
--------------------------------
Part 1: December Precipitation Stats
▒▒Years▒▒ ▒▒▒PRCP▒▒▒▒  ▒▒PRCP▒▒  ▒▒PRCP▒▒ ▒PRCP▒ ▒▒▒▒PRCP▒▒▒▒ ▒▒▒▒PRCP▒▒▒▒ | ▒▒▒SNOW▒▒▒▒  ▒▒SNOW▒▒ ▒SNOW▒ ▒▒▒▒SNOW▒▒▒▒ |
▒▒▒▒▒▒▒▒▒ ▒▒▒DAYS▒▒▒▒  DAYS MAX  DAYS MIN ▒AVG▒▒ ▒▒▒▒MAX▒▒▒▒▒ ▒▒▒▒MIN▒▒▒▒▒ | ▒▒▒DAYS▒▒▒▒  DAYS MAX ▒AVG▒▒ ▒▒▒▒MAX▒▒▒▒▒ |
--------- -----------  --------  -------- ------ ------------ ------------ | -----------  -------- ------ ------------ |
All Time  1249: 33.4%  20, 1972   1, 1896  3.66   8.89, 1901   0.28, 1965  |  144:  3.8%   6, 1945  1.7    14.5, 1917  |
1896-1925  219: 26.4%  14,  2     1, 1896  3.83   8.89, 1901   0.92, 1899  |   31:  3.7%   4,  3    1.8    14.5, 1917  |
1901-1930  238: 28.7%  14,  2     4,  2    4.05   8.89, 1901   0.95, 1928  |   31:  3.7%   4,  3    2.0    14.5, 1917  |
1906-1935  261: 30.1%  14,  3     4,  2    3.73   7.32, 1927   0.95, 1928  |   32:  3.7%   4,  3    2.3    14.5, 1917  |
1911-1940  266: 30.6%  15, 1936   4,  2    3.58   7.32, 1927   0.95, 1928  |   29:  3.3%   4,  2    2.3    14.5, 1917  |
1916-1945  282: 31.4%  19, 1942   4,  2    3.54   7.32, 1927   0.95, 1928  |   36:  4.0%   6, 1945  2.2    14.5, 1917  |
1921-1950  292: 32.5%  19, 1942   4,  2    3.4    7.32, 1927   0.95, 1928  |   36:  4.0%   6, 1945  1.6    10.0, 1945  |
1926-1955  314: 33.8%  19, 1942   4, 1928  3.49   7.32, 1927    0.9, 1955  |   39:  4.2%   6, 1945  1.6    10.0, 1945  |
1931-1960  315: 33.9%  19, 1942   5, 1960  3.45   7.16, 1936    0.9, 1955  |   39:  4.2%   6, 1945  1.6    10.0, 1945  |
1936-1965  305: 34.0%  19, 1942   5, 1960  3.48   7.16, 1936   0.28, 1965  |   40:  4.5%   6, 1945  1.1    10.0, 1945  |
1941-1970  303: 33.7%  19, 1942   5, 1960  3.57   6.22, 1967   0.28, 1965  |   43:  4.8%   6, 1945  1.5    10.0, 1945  |
1946-1975  311: 34.6%  20, 1972   5, 1960  3.56   7.72, 1973   0.28, 1965  |   36:  4.0%   4,  2    1.1     9.5, 1969  |
1951-1980  313: 34.9%  20, 1972   5,  2    3.52   7.72, 1973   0.28, 1965  |   32:  3.6%   4, 1965  1.2     9.5, 1969  |
1956-1985  322: 35.8%  20, 1972   5,  2    3.46   7.72, 1973   0.28, 1965  |   36:  4.0%   4, 1965  1.3     9.5, 1969  |
1961-1990  343: 38.2%  20, 1972   5, 1979  3.42   7.72, 1973   0.28, 1965  |   39:  4.3%   4,  2    1.4     9.5, 1969  |
1966-1995  355: 38.2%  20, 1972   5, 1979  3.38   7.72, 1973   0.68, 1980  |   37:  4.0%   4, 1989  1.6     9.5, 1969  |
1971-2000  359: 38.6%  20, 1972   5, 1979  3.31   7.72, 1973   0.68, 1980  |   33:  3.5%   4, 1989  1.3     8.0, 1997  |
1976-2005  334: 35.9%  19, 1982   5, 1979  3.17   6.16, 1983   0.68, 1980  |   34:  3.7%   4, 1989  1.4     8.0, 1997  |
1981-2010  345: 37.1%  19, 1982   6, 1985  3.55    7.7, 2009    1.0, 1984  |   35:  3.8%   4, 1989  1.8     8.0, 1997  |
1986-2015  348: 37.4%  17, 2008   7, 2010  3.94    7.7, 2009   1.07, 1988  |   30:  3.2%   4, 1989  1.5     8.0, 1997  |

Part 2: December Temperature Stats
▒▒Years▒▒ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒AVG TEMP▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ | ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒TMAX▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ | ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒TMIN▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒▒▒▒▒▒ STDEV ▒AVG▒ ▒▒▒▒MAX▒▒▒▒▒ ▒▒▒▒MIN▒▒▒▒▒ | STDEV ▒AVG▒ ▒▒▒▒MAX▒▒▒▒▒ ▒▒▒▒MIN▒▒▒▒▒ | STDEV ▒AVG▒ ▒▒▒▒MAX▒▒▒▒▒ ▒▒▒▒MIN▒▒▒▒▒
--------- ----- ----- ------------ ------------ | ----- ----- ------------ ------------ | ----- ----- ------------ ------------
All Time   3.5  39.1   48.3, 2015   29.6, 1917  |  9.8  50.4   60.0, 1956   40.2, 1935  |  9.6  27.8   37.4, 2015   17.4, 1917 
1896-1925  3.3  38.3   46.0, 1923   29.6, 1917  |  9.6  49.3   58.4, 1923   41.9, 1917  |  9.6  27.3   33.5, 1923   17.4, 1917 
1901-1930  3.4  38.3   46.0, 1923   29.6, 1917  |  9.8  49.5   58.4, 1923   41.9, 1917  | 10.0  27.1   33.5, 1923   17.4, 1917 
1906-1935  3.9  38.8   46.0, 1931   29.6, 1917  | 10.1  50.0   58.4, 1923   40.2, 1935  | 10.2  27.7   34.4, 1931   17.4, 1917 
1911-1940  3.8  39.3   46.0, 1931   29.6, 1917  |  9.9  50.6   58.4, 1923   40.2, 1935  | 10.3  28.2   34.4, 1931   17.4, 1917 
1916-1945  3.8  39.1   46.0, 1931   29.6, 1917  | 10.2  50.7   58.4, 1923   40.2, 1935  | 10.3  27.6   34.4, 1931   17.4, 1917 
1921-1950  3.5  39.7   46.0, 1931   31.1, 1935  | 10.1  51.4     59, 1946   40.2, 1935  | 10.0  28.0   34.4, 1931     22, 1935 
1926-1955  3.2  39.2   46.0, 1931   31.1, 1935  |  9.9  50.8     59, 1946   40.2, 1935  |  9.9  27.6   34.4, 1931     22, 1935 
1931-1960  3.6  39.5   47.5, 1956   31.1, 1935  |  9.8  51.1   60.0, 1956   40.2, 1935  |  9.8  27.8   35.1, 1956   21.1, 1960 
1936-1965  3.1  39.3   47.5, 1956   34.0, 1960  |  9.6  51.0   60.0, 1956   43.9, 1945  |  9.8  27.6   35.1, 1956   21.1, 1960 
1941-1970  3.2  39.0   47.5, 1956   34.0, 1960  |  9.7  50.6   60.0, 1956   43.9, 1945  |  9.7  27.4   35.1, 1956   21.1, 1960 
1946-1975  3.3  39.7   47.5, 1956   34.0, 1960  |  9.6  51.0   60.0, 1956   44.6, 1969  |  9.8  28.3   35.9, 1971   21.1, 1960 
1951-1980  3.2  39.4   47.5, 1956   34.0, 1960  |  9.4  50.8   60.0, 1956   44.6, 1969  |  9.9  28.1   35.9, 1971   21.1, 1960 
1956-1985  3.6  39.7   47.5, 1956   34.0, 1960  | 10.0  51.0   60.0, 1956   44.6, 1981  | 10.1  28.5   35.9, 1971   21.1, 1960 
1961-1990  3.4  39.6   47.0, 1971   31.9, 1989  |  9.8  50.6   59.9, 1984   42.0, 1989  |  9.9  28.7   35.9, 1971   22.2, 1989 
1966-1995  3.6  39.6   47.0, 1971   31.9, 1989  |  9.8  50.5   59.9, 1984   42.0, 1989  |  9.7  28.8   35.9, 1971   22.2, 1989 
1971-2000  3.8  39.4   47.0, 1971   29.8, 2000  | 10.0  50.6   59.9, 1984   41.2, 2000  |  9.7  28.2   35.9, 1971   18.4, 2000 
1976-2005  3.7  38.6   46.8, 1984   29.8, 2000  | 10.0  50.0   59.9, 1984   41.2, 2000  |  9.4  27.3   34.1, 1990   18.4, 2000 
1981-2010  3.9  38.5   46.8, 1984   29.8, 2000  | 10.2  49.6   59.9, 1984   41.2, 2000  |  9.1  27.4   34.1, 1990   18.4, 2000 
1986-2015  4.0  39.1   48.3, 2015   29.8, 2000  |  9.8  50.3   59.2, 2015   41.2, 2000  |  8.9  27.8   37.4, 2015   18.4, 2000

```

[&#8679; back to Contents](#contents)

#### Ranking

The "fun stuff." These temporal-based functions give quick info of record-setting times for the city. Associated data is not considered if threshold quantities are not met.

`dayRank(m,d,qty)` :: Searches for records based on a specific day. Input the month, day, and how many ranks you want the report to be on (put `10` for the top-10)
`weekRank(m,d,qty)` :: Searches for weekly-based records with the provided day being the center of the week.
`monthRank(m,"rain",qty)` :: Searches for records by the month. You must specifiy `"temp"` for temperature records or `"rain"` for precipitation-based records
`yearRank("temp",qty)` :: Ranks by the year. Like `monthRank`, you must specify which type of ranking you want
`metYearRank("temp",qty)` :: Ranks by the meteorological year (March-Feb). Like `monthRank`, you must specify which type of ranking you want
`seasonRank(season,"temp",qty)` :: Ranks by the meteorological season. Like `monthRank`, you must specify which type of ranking you want
`customRank("attribute",qty,m1,d1,*[m2,d2])` :: Ranks by the meteorological season. Like some others, you must specify which type of ranking you want
`allDayRank("attribute",qty,**{season="season",year=<YEAR>,month=<MONTH>,ascending=False})` :: Ranks based on individual days in the record, in contrast to `dayRank` which only compares records from a specified day. You can use it, for example, to get an all-time daily record high/low; all-time daily record rain/snow, etc. To reverse the order (lowest to highest), include the `ascending=True` kwarg (only valid for temperature attrs)
`allMonthRank("attribute",qty,**{season="season",ascending=False})` :: Ranks individual months, allowing comparison of different months to each other; monthly parallel of `allDayRank`. It does not accept as many optional keyword arguments though. To reverse the order (lowest to highest), include the `ascending=True` kwarg

Example output:

```
>>> monthRank(1,"temp",10)

                                      Ranked January Monthly Temperatures                                      
                                            USC00001337, CITY, USA                                       
---------------------------------------------------------------------------------------------------------------
              AVG TEMP              |                TMAX                 |                TMIN                
------------------------------------|-------------------------------------|------------------------------------
     Warmest     |     Coolest      |     Warmest      |     Coolest      |     Warmest      |     Coolest     
-----------------|------------------|------------------|------------------|------------------|-----------------
 1. 1950   48.1  |  1. 1977   25.6  |  1. 1950   60.2  |  1. 1977   35.2  |  1. 1937   39.5  |  1. 1893   15.7
 2. 1937   47.4  |  2. 1893   27.0  |  2. 1974   57.2  |  2. 1918     37  |  2. 1949   37.1  |  2. 2014   16.3
 3. 1949   47.1  |  3. 1918   27.7  |  3. 1949   57.1  |  3. 1940   37.9  |  3. 1974     37  |  3. 1977   16.5
    1974   47.1  |  4. 1940   28.3  |  4. 1932   56.9  |  4. 1893   38.4  |  4. 1932   36.0  |  4. 1918   18.4
 4. 1932   46.4  |  5. 2014   29.3  |  5. 1907   56.4  |  5. 1978   38.9  |     1950   36.0  |  5. 1940   18.8
 5. 1907   44.6  |  6. 1978     30  |  6. 1933   56.0  |  6. 1994   40.3  |  5. 1947   33.7  |  6. 2018   19.4
 6. 1913   44.4  |  7. 1994   30.2  |  7. 1990   55.4  |  7. 2014   42.3  |  6. 1913   33.6  |  7. 1904   19.8
 7. 1947   44.3  |  8. 1982   31.3  |  8. 1937   55.2  |  8. 1982   42.4  |  7. 1907   32.9  |  8. 1982   20.3
 8. 1933   44.0  |  9. 1904   31.4  |  9. 1913   55.1  |  9. 1970   42.5  |  8. 1993   32.7  |  9. 1912   20.4
 9. 1990   43.5  | 10. 1912   31.5  | 10. 1947   54.9  | 10. 1912   42.7  |  9. 1916   32.1  | 10. 1994   20.7
10. 1952   43.0  |     2018   31.5  |                  |                  | 10. 1933     32  |                
                 |                  |                  |                  |     1990   32.0  |                
```

```
>>> yearRank("rain",10)
                             Ranked Yearly Precipitation Amounts and Days                              
                                       USC00001337, CITY, USA                                  
-------------------------------------------------------------------------------------------------------
                                Rain                                 |              Snow               
---------------------------------------------------------------------|---------------------------------
     Wettest      |      Driest      |   Most Days   |  Least Days   |    Snowiest     |   Most Days   
------------------|------------------|---------------|---------------|-----------------|---------------
  1. 2003   69.96 |  1. 1930   19.76 |  1. 1996  176 |  1. 1900   71 |  1. 1895   28.5 |  1. 1978   16 
  2. 2018    69.0 |  2. 1904   28.05 |  2. 2003  173 |  2. 1899   75 |     1987   28.5 |  2. 1914   15 
  3. 2013    68.3 |  3. 1963   28.36 |  3. 1945  167 |  3. 1903   77 |  2. 1912   27.5 |  3. 1895   14 
  4. 1901   63.89 |  4. 1894   28.79 |  4. 1992  160 |  4. 1894   78 |     1960   27.5 |     1948   14 
  5. 2015   59.01 |  5. 1933   29.92 |  5. 1982  158 |  5. 1893   82 |  3. 2018   24.4 |  4. 1936   13 
  6. 1929   58.45 |  6. 1988    32.7 |  6. 2015  157 |  6. 1901   86 |  4. 2010   23.8 |     1965   13 
  7. 2012   58.22 |  7. 2008   33.43 |  7. 2013  156 |  7. 1896   87 |  5. 1914   23.3 |     1983   13 
  8. 1957   58.02 |  8. 1986   33.62 |  8. 1957  152 |     1941   87 |  6. 1979   23.2 |     1987   13 
     1996   58.02 |  9. 1925   34.36 |     1959  152 |  8. 1897   89 |  7. 1908   21.5 |  5. 1908   12 
  9. 1989   57.89 | 10. 1914   35.14 |     1979  152 |     1921   89 |     1996   21.5 |     1982   12 
 10. 1906   57.32 |                  |     1989  152 |  9. 1904   90 |  8. 1969   20.8 |     1996   12 
                  |                  |  9. 1906  150 | 10. 1914   93 |  9. 1993   20.3 |  6. 1950   11 
                  |                  |     1994  150 |               | 10. 2014   20.2 |     1967   11 
                  |                  | 10. 1910  148 |               |                 |     1968   11 
                  |                  |     1991  148 |               |                 |     1980   11 
                  |                  |     2014  148 |               |                 |     2013   11
```

[&#8679; back to Contents](#contents)

### valueSearch

This function allows the user to get basic stats on data based on a specific value. You can also search monthly-based data.
* `valueSearch("attribute","operator",value,**{sortmonth=False})`
  * The attribute ultimately must be in `["prcp","snow","snwd","tavg","tmax","tmin"]`, but some derivatives are accepted
  * The operator must be in `["<=","<","==","!=",">",">="]`
  * The value must be an `int` or `float`
  * if the **kwarg `sortmonth=True`, monthly data will be searched instead of daily
  * if the results list is >= 50, the user will be notified and asked if they want it output or not

Example 1:
```
>>> valueSearch("tmax",">=",100)
Total days where 'tmax' >= 100: 62
print results? ('y'/'n'): y
100: 1904-07-18
102: 1904-07-19
103: 1904-07-20
102: 1914-06-11
101: 1914-06-21
100: 1914-06-22
100: 1914-06-25
100: 1914-07-12
100: 1914-07-25
101: 1914-07-26 ......
```

Example 2:
```
>>> valueSearch("prcp","<=",0.25,sortmonth=True)
Total months where 'prcp' <= 0.25: 9
  0.00: Oct 1901
  0.11: Nov 1901
  0.00: Sep 1903
  0.13: Oct 1904
  0.00: Sep 1939
  0.00: Apr 1942
  0.05: Oct 1963
  0.19: Sep 1984
  0.00: Oct 2000
```

[&#8679; back to Contents](#contents)

### On-the-fly Data retrieval

This section partly goes over the data-structure and some examples to quickly call upon some data.

##### Day Summaries
The quickest way to look at multi-day data would be the `daySummary` function.
  * Syntax: `daySummary(y1,m1,d1,*[y2,m2,d2])`
  * The 2nd date is optional; if none is entered, Dec 31 for the year given by y1 will be used
  * This lists daily summaries for all dates in the range. Think of it like a raw data dump.
  * Quality flags are listed as well.
```
>>> daySummary(1901,8,1,1901,8,31)

                    Day Summaries from 01 AUG 1901 to 10 AUG 1901
                              USC000001337: City, USA
                    ---------------------------------------------
1901-08-01: PRCP:  0.00   ; SNOW: ----   ; SNWD: ----   ; TMAX:  85   ; TMIN:  61
1901-08-02: PRCP:  0.00   ; SNOW: ----   ; SNWD: ----   ; TMAX:  85   ; TMIN:  58
1901-08-03: PRCP:  0.00   ; SNOW: ----   ; SNWD: ----   ; TMAX:  86   ; TMIN:  67 I
1901-08-04: PRCP:  0.00   ; SNOW: ----   ; SNWD: ----   ; TMAX:  89   ; TMIN:  65
1901-08-05: PRCP:  3.27   ; SNOW: ----   ; SNWD: ----   ; TMAX:  71 I ; TMIN:  66
1901-08-06: PRCP:  0.98   ; SNOW: ----   ; SNWD: ----   ; TMAX:  76   ; TMIN:  63
1901-08-07: PRCP:  0.00   ; SNOW: ----   ; SNWD: ----   ; TMAX:  83   ; TMIN:  64
1901-08-08: PRCP:  0.00   ; SNOW: ----   ; SNWD: ----   ; TMAX:  85   ; TMIN:  57
1901-08-09: PRCP:  0.00   ; SNOW: ----   ; SNWD: ----   ; TMAX:  88   ; TMIN:  58
1901-08-10: PRCP:  0.75   ; SNOW: ----   ; SNWD: ----   ; TMAX:  90   ; TMIN:  62
```

##### Other detailed info
When compiling, everything is thrown into a python-dictionary, `clmt`. The primary keys are integers, making organization into a dictionary to be very useful. Monthly dictionaries and Day objects are nested within the respective year's dictionary.

Tier 1 keys generally are years:
  * `clmt[1982]` :: This would hold keys specific for the year 1982. These will include months

Tier 2 keys generally are the months for a specific year:
  * `clmt[1982][3]` :: This would hold daily data for March 1982.

Year and Month keys have additional keys besides their integer counter-parts. This includes:
```
['recordqty']   :: integer; the number of data entries for the year or month
['prcp'] 		:: list containing the individual prcp values found for a year or month
['prcpDAYS']	:: integer; the number of days in a given year or month with prcp recorded
['prcpPROP']	:: holds day or month maximum and minimum statistics
['snow'] 		:: list containing the individual snow values found for a year or month
['snowDAYS'] 	:: integer; the number of snow days for a given year/month
['snowPROP']	:: daily/monthly max/min stats
['snwd']		:: list containing individual snow-depth amounts for months/years
['snwdDAYS']	:: integer of days (in months/years) where snow-depth amounts &gt; 0 (&gt; T)
['tempAVGlist] 	:: list; contains matching highs and lows for a year or month. Only days with a recorded high AND a recorded low are put into this list
['tmax']		:: list; contains all high-temperature data for a year or month
['tmaxPROP']	:: daily/monthly max/min stats
['tmin']		:: list; contains all low-temperature data for a year or month
['tminPROP']	:: daily/monthly max/min stats
```

* `clmt[2005][4]["prcp"]` would return a list of individual precipitation amounts recorded for April 2005
* `clmt[2009]["snow"]` would return a list of individual snow amounts occurring in the year 2009

The above in lists can easily be worked with using the `sum` function or a `statistics` module method, like `mean`.
* `sum(clmt[1982]["prcp"])` would return the total rain amount for the year 1982
* `mean(clmt[1993][4]["tmax"])` would return the average high-temperature for April 1993
* They eliminate time and lines that would otherwise be needed

Tier 3 keys generally are the specific days. The values are data objects (see below):
  * `clmt[1982][3][29]` :: This is a data-object specific to March 29, 1982.

Day keys contain `object` values. So each day in the record has the following attributes:

```
.stationid 		:: GHNCD Station ID
.station_name 	:: Station Name
.station_lat 	:: Station Latitude
.station_lon	:: Station Longitude
.station_elev	:: Station Elevation
.daystr 		:: The date in string format
.entryday		:: the date in python's datetime format
.prcp 			:: Recorded rain for a date (string format)
.prcp<M,Q,S,T> 	:: Various precipitation data flags (string format)
.snow 			:: Recorded snow for a date (string format)
.snow<M,Q,S,T> 	:: Various snow data flags (string format)
.snwd 			:: Recorded snow-depth for a date (string format)
.snwd<M,Q,S,T> 	:: Various snow-depth data flags (string format)
.tmax 			:: Recorded high-temperature for a date (string format)
.tmax<M,Q,S,T> 	:: Various tmax data flags (string format)
.tmin 			:: Recorded low-temperature for a date (string format)
.tmin<M,Q,S,T> 	:: Various tmin data flags (string format)
```

The above could be accessed via a simple object attribute call
* `clmt[1992][12][29].tmax` would give the high-temperature for December 29, 1992
* This kind of use is extremely, but powerfully, simplified using the [Stats functions](#stats)

Meteorlogical Years/Seasons can also be retrieved in very similar ways as above. Instead of `clmt`, you would type `metclmt` in the commands above. Additionally, metclmt years have 4 additional keys, `"spring","summer","fall","winter"`. So you can get the list of high-temperatures for spring of 2017 like this: `metclmt[2017]["spring"]["tmax"]`. Here, as mentioned above, a lot has been simplified via the stats functions

Two reverse dictionaries are included, `clmt_vars_days` and `clmt_vars_months`. These are exclusively used in the `allDayRank`, `allMonthRank`, and `valueSearch` functions. They have tier 1 keys as `"prcp","snow","snwd","tavg","tmax","tmin"`. These are dictionaries set up with tier-2 keys as the unique values as keys, with lists of dates as values. Both can be called in a very similar fashion, but on-the-fly retrieval is best accomodated using the above functions, because it's cumbersome to use unless you know the exact value, and a KeyError will result if it can't find the exact key.

For example, if you wanted to find days(months) where the rainfall equaled 2 inches, you could command the following:
```
# prints days in the record where rain total equalled exactly 5
for DAY in clmt_vars_days["prcp"][5.00]: print(DAY)
# prints months on record where monthly sum of rain was exactly 10
for MONTH in clmt_vars_months["prcp"][10.00]: print(MONTH.month,MONTH.year)
```

You could do something like this to return a list of days/months based on a certain threshold
```
# prints days in the record where the high temperature >= 100 degrees
for DAY in [day for v in clmt_vars_days["tmax"] if v >= 100 for day in clmt_vars_days["tmax"][v]]: print(DAY)
# prints months in the record where monthly sum of rain exceeded 12 inches
for MONTH in [month for v in clmt_vars_months["prcp"] if v >= 12 for month in clmt_vars_months["prcp"][v]]: print(MONTH.month,"-",MONTH.year)
```

As you can tell, that is quite a keyboard-full to type. So, like mentioned above, some functions are included to help assist the user.
[&#8679; back to Contents](#contents)

### Sample Scripts

`*** COMING SOON ***`

[&#8679; back to Contents](#contents)

### Roadmap

* Include least-snowiest years in `yearRank` and `metYearRank`
* Make an annual Average Temperatures Graph; daily and day-centered weekly; day-centered monthly
* include more kwargs for `valueSearch`
  * consider adding a `sortyear` kwarg
* include error-addressing in `allDayRank, allMonthRank, and valueSearch` functions
* Continue evolution of handling multi-station data where days overlap
  * perhaps make a note of the recorded station for each variable
* days of snow on the ground (snwd > 0); could add it to reports, and rank functions
* it is possible that `snow` isn't constantly recorded, but `snwd` is. How do I account for that/warn the user about that?
* in `errorStats`, account for times when `SNWD` goes up without any `SNOW` in the recent record
* add ranking to `snwdDAYS` in customStats

[&#8679; back to Contents](#contents)

### Licensing

MIT License (see LICENSE.md)

[&#8679; back to Contents](#contents)

### HELP

* Check the roadmap section to see if what you're needing addressed is already there
* Let me know via the issues tab of the github repository
* Place suggestions there too (which can come-about because of issues)

If you want, let me know if this benefits you somehow in your research/project. Thanks.

[&#8679; back to Contents](#contents)
