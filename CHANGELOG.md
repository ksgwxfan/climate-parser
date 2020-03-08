# Change Log (since v2.0)

### v2.8
* Fixed `metclmt` initialization for when the final year on record is only partial, having no more than Jan or Feb records.
* Fixed `allDayRank` and `allMonthRank` winter-based records involving a non-existent `metclmt` year key (i think it would have only affected partial years)
* Modified output of `allDayRank` to be fixed digits
* Simplified read-in of `allMonthRank` data where season kwarg was present
* take out 0 requirement on stats function report rankings (month)
* Fixed output of `monthRank`, `yearRank`, `metYearRank`, and `seasonRank` where it was throwing an exception for rank indices exceeding the length of the compiled lists
  * This was the same strategy I had previously used in `customRank` but had not yet implemented it into the above, which I had generated prior
* Overhauled `yearStats` output: Included rankings and monthly statistics. If you're interested in basic statistics from multiple months in the same year, this is a great shortcut compared to running `monthStats` for each one
* Overhauled `metYearStats` the same way as above
* Overhauled `seasonStats` the same way as above
* MAJOR FIX: in v2.71, I modified how multiple stations were held. A significant mistake was found (by accident) where the overlapped-years were being counted twice. In essence, precip and snow totals (and total days of) would become very inflated. To fix it, all I had to do was 1 simple indention. haha.

### v2.72
* Added a new `rank()` function that is used internally to return the passed rank number and correct suffix; on-going transition to use in `<temporalStats>` functions
* Added rank reporting for `monthStats`
  * Fixed it so the reported rankings coincide with `monthRank`
* Modified `dayStats`,`weekStats`, and `monthStats` to report the lowest temperature ranking (instead of warmest AND coolest)

### v2.71
* Patched an error that would occur during compiling of `metclmt` if data was missing for an entire calendar year (empty placeholders; having no variable data recorded, just dates)
* Changed handling for data for multiple stations where days overlapped to allow modifying of data if an empty-set (empty placeholder) of variables existed for a certain day
* `dayStats` now reflects the id/name of the specific weather data was found (primarily useful if multiple stations are in your csv)
* Tweaked `dayStats` code to be more concise
* Fixed output flaw in `weekRank` that would make it seem that it truncated well too-early. It was due to improper placement of string format code
* Added ranking output in `weekStats`; included output for average snow depth

### v2.7
* Fixed `weekStats` output by making a mirror function of `checkDate`. After the 2.6 overhaul, for days where data was missing, it was outputting default messages from the original checkDate function.
  * Fixed output to reflect missing data by printing an `M`; in v2.6 it only would've done this if no entry was found in `clmt`
* Fixed 'clmtmenu()' so it will interpret custom location names with more than 1 comma in it (i.e. "Minneapolis, MN, USA")
* Included `clmt_vars_months`, which is a 'reverse' dictionary for monthly data. It is the monthly parallel of the previously added 'clmt_vars_days'.
* Included `allMonthRank`, the monthly parallel of the `allDayRank` function, to allow comparison of different months to each other
* Included a basic `valueSearch` function. This allows the user to search the record for data based on specific value thresholds

### v2.6
* Eliminated `csvFileList()` (and the need thereof). The script now runs `clmtmenu()` automatically at the execution of the script. It allows the user to enter in a single number from a list of csv files, and an optional city name.
* Added an `output` csv keyword argument to all report functions. This outputs a csv version of the report, allowing the user to open it up in a spreadsheet program to do charts and such.
* Revamped `weekStats` output to show comprehensive layout of data including all daily data from the week inquired

### v2.5
* Included a new function, `allDayRank()` which ranks based solely on individual day records. This enables displaying all time record highs/lows for the entire record
  * Also included some temporal keyword arguments; so you can compare data within a certain month, month in a year, a year, a season, or a season from a specific year

### v2.4
* Included a reverse dictionary, `clmt_vars_days`, which includes subset dictionaries of `"prcp"`, `"snow"`, `"snwd"`, `"tmax"`, `"tmin"`, `"tavg"`; holding values from individual days. The variables are the keys with matching dates being the new values; will be used more in a future update
* Eliminated the `"station"` keyword argument in the `clmtAnalyze` call.
  * Included code to handle the station ID if more than 1 station was used to compile the data
* Fixed `customRank` help docstring
* Altered exclusion threshold rules for `customRank` to be more stringent for periods less than a week 
* Modified `help` docstrings to be in line with PEP standards
* On all `Rank` functions: changed output record qty (based on the threshold) to be inclusive (greater-than or equal to) rather than exclusive (less-than).
* Added two report-related variables, `clmt_len_rpt` and `clmt_inc_rpt`; enables change of climatology period and assessment-frequency
  * These can be changed anytime; no need to re-run `clmtAnalyze`.
  * The idea of adding these was make it easy for the user to assess other climatology-period lengths (like 10, 15, or 20-yr climatologies)
* Adjusted report output to accommodate the new variables and included them in the output too
  * Added a dynamic end-year range for the reports (wouldn't have been a problem until like 2040, but oh well, lol)
  

### v2.3
* Included `customStats`, `customReport`, and `customRank` functions. These allow the user to define the period of time they want to retrieve stats, reports, or rankings for. You are no longer confined to retrieving data based on fixed lengths of time. A great proxy for a Year-to-Date, Month-to-Date, or even a Season-to-Date functions.
  * Included associated `excludecustom` threshold. Instead of a fixed integer, it is a fixed float as a percentage; implemented since time-frames can be of variable lengths. The functions have basic logic to to use other exclusion variables if they meet certain criteria.
* Included daily temperature average in `dayReport`
* Fixed `weekStats`, `weekReport`, and `weekRank` calculations; one of the problems seen was that on weeks that overlapped years, it wasn't using dates from the later or previous year, respectively
* Included `help()` doc-strings for all major functions

### v2.01
* cleaned up some testing artifacts

### v2.0
* Inclusion of Meteorological Season functions. Allows one to compare seasons to other like-seasons.
  * Spring - 3,4,5; Summer - 6,7,8; Fall - 9,10,11; Winter - 12,1,2
* Inclusion of Meteorological Year functions. Meteorological years go from March to February of the following year (Spring to Winter), encompassing 4 complete seasons. Otherwise, the winter months (12,1,2) would include data from seperate winters like found if assessing a calendar year. Any inferred difference would be much less if astronomically-based functions were included, as there would only be a 10 or 11 day shift in the yearly calculations. But meteorological seasons are much simpler to deal with, and they are a standard temporal frame recognized in the weather community
* Added accessible record-threshold variables near the end of the script to allow easy tweaking. These variables control if a year, season, month, or week of interest is included in reports and rankings. Another bonus is these thresholds can be modified after you compile/mount the script
  * I included these record thresholds in rank function output
* Added tweaks that aids legibility of the function output
  * added fixed-digit output to reports and rankings
  * added alignment to rankings