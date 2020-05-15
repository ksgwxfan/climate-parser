#v 2.91

import datetime
from time import time
import calendar
from statistics import mean, pstdev, mode, median, median_grouped
from math import floor
import csv
import os
from textwrap import wrap
from string import Template
import random
import traceback

# assisted on nested list comprehensions: https://www.geeksforgeeks.org/nested-list-comprehensions-in-python/

def quicklist(vrbl,**kw):
    if vrbl not in ["prcp","snow","snwd","tmax","tmin"]: return print("OOPS! Improper variable entered. Try again!")

    vdictionary = {"prcp":"Precipitation Totals","snow":"Snow Totals","snwd":"Snow Depths","tmax":"High Temperatures","tmin":"Low Temperatures"}
    if all(x in kw and len(list(kw.keys())) == 1 for x in ["season"]):              # all yrs; specific season; all months & days
        #if type(kw["season"]) == list:
            #qwkli = []
            #for s in kw["season"]: qwkli.extend(x for y in metclmt if type(y) == int for x in metclmt[y][s][vrbl])
        #else:   # If just one season passed
        qwkli = [x for y in metclmt if type(y) == int for x in metclmt[y][kw["season"]][vrbl]]
        print("* Completed list for all {} occurring in Meteorological {} from the entire record *".format(vdictionary[vrbl],kw["season"]))
    elif all(x in kw and len(list(kw.keys())) == 1 for x in ["metyear"]):           # specific metyear; all months & days
        try:
            qwkli = metclmt[kw["metyear"]][vrbl]
            print("* Completed list for all {} occurring in the Meteorological Year {}. Same as metclmt[{}]['{}'] *".format(vdictionary[vrbl],kw["metyear"],kw["metyear"],vrbl))
        except:
            if kw["metyear"] not in metclmt: print("OOPS! No records are available for the Meteorological Year {}".format(kw["metyear"]))
    elif all(x in kw and len(list(kw.keys())) == 2 for x in ["metyear","season"]):  # specific metyear; specific season; all months & days
        try:
            qwkli = metclmt[kw["metyear"]][kw["season"]][vrbl]
            print("* Completed list for all {} occurring in Meteorological {} of the Year {}. Same as metclmt[{}]['{}']['{}'] *".format(vdictionary[vrbl],kw["season"],kw["metyear"],kw["metyear"],kw["season"],vrbl))
        except:
            if kw["metyear"] not in metclmt: print("OOPS! No records are available for {}".format(kw["year"]))
            elif kw["month"] not in metclmt[kw["metyear"]]: print("OOPS! No records are available for {} {}".format(calendar.month_name[kw["month"]],kw["metyear"]))
    elif all(x in kw and len(list(kw.keys())) == 2 for x in ["year","month"]):      # specific year; specific month; all days
        try:
            qwkli = clmt[kw["year"]][kw["month"]][vrbl]
            print("* Completed list for all {} occurring in {} {}. Same as clmt[{}][{}]['{}'] *".format(vdictionary[vrbl],
                calendar.month_name[kw["month"]],kw["year"],kw["month"],kw["year"],vrbl))
        except:
            if kw["year"] not in clmt: print("OOPS! No records are available for {}".format(kw["year"]))
            elif kw["month"] not in clmt[kw["year"]]: print("OOPS! No records are available for {} {}".format(calendar.month_name[kw["month"]],kw["year"]))
    elif all(x in kw and len(list(kw.keys())) == 1 for x in ["year"]):              # specific year; all months; all days
        try:
            qwkli = clmt[kw["year"]][vrbl]
            print("* Completed list for all {} occurring in {}. Same as clmt[{}]['{}'] *".format(vdictionary[vrbl],kw["year"],kw["year"],vrbl))
        except:
            if kw["year"] not in clmt: print("OOPS! No records are available for {}".format(kw["year"]))
    elif all(x in kw and len(list(kw.keys())) == 1 for x in ["month"]):             # all years; specific month; all days
        qwkli = [x for y in clmt if type(y) == int for m in clmt[y] if type(m) == int and m in clmt[y] and m == kw["month"] for x in clmt[y][kw["month"]][vrbl]]
        print("* Completed list for all {} occurring in the month of {} for all years on record.".format(vdictionary[vrbl],calendar.month_name[kw["month"]]))
    elif all(x in kw and len(list(kw.keys())) == 2 for x in ["month","day"]):       # all years; specific month; specific day
        if vrbl == "prcp": qwkli = [float(clmt[y][kw["month"]][kw["day"]].prcp) for y in clmt if type(y) == int and kw["month"] in clmt[y] and kw["day"] in clmt[y][kw["month"]] and clmt[y][kw["month"]][kw["day"]].prcp not in ["","-9999","9999"] and clmt[y][kw["month"]][kw["day"]].prcpQ in ignoreflags]
        elif vrbl == "snow": qwkli = [float(clmt[y][kw["month"]][kw["day"]].snow) for y in clmt if type(y) == int and kw["month"] in clmt[y] and kw["day"] in clmt[y][kw["month"]] and clmt[y][kw["month"]][kw["day"]].snow not in ["","-9999","9999"] and clmt[y][kw["month"]][kw["day"]].snowQ in ignoreflags]
        elif vrbl == "snwd": qwkli = [float(clmt[y][kw["month"]][kw["day"]].snwd) for y in clmt if type(y) == int and kw["month"] in clmt[y] and kw["day"] in clmt[y][kw["month"]] and clmt[y][kw["month"]][kw["day"]].snwd not in ["","-9999","9999"] and clmt[y][kw["month"]][kw["day"]].snwdQ in ignoreflags]
        elif vrbl == "tmax": qwkli = [int(clmt[y][kw["month"]][kw["day"]].tmax) for y in clmt if type(y) == int and kw["month"] in clmt[y] and kw["day"] in clmt[y][kw["month"]] and clmt[y][kw["month"]][kw["day"]].tmax not in ["","-9999","9999"] and clmt[y][kw["month"]][kw["day"]].tmaxQ in ignoreflags]
        elif vrbl == "tmin": qwkli = [int(clmt[y][kw["month"]][kw["day"]].tmin) for y in clmt if type(y) == int and kw["month"] in clmt[y] and kw["day"] in clmt[y][kw["month"]] and clmt[y][kw["month"]][kw["day"]].tmin not in ["","-9999","9999"] and clmt[y][kw["month"]][kw["day"]].tminQ in ignoreflags]
        print("* Completed list for all {} occurring on {} {} for all years on record *".format(vdictionary[vrbl],calendar.month_name[kw["month"]],kw["day"]))
    return qwkli

def percentiles(li):
    li.sort()   # Sort list from smallest value to largest
    n = len(li)
    percentiles = [x for x in range(5,95+5,5)]   # list of kth percentiles we'll be calculating
    for k in percentiles:
        i = k/100 * (n + 1)
        if i / 1 == int(i):  # if 'i' is an integer...
            print("{}th Percentile: {}".format(k,li[int(i)-1]))
        else:
            i_down = int(i)
            i_up = int(i)+1
            print("{}th Percentile: {:.1f}".format(k,mean([li[i_down-1],li[i_up-1]])))

def percentile(k,li):
    if k <= 0 or k >= 100: return print("OOPS! Invalid percentile. Try again") 
    li.sort()   # Sort list from smallest value to largest
    n = len(li)
    i = k/100 * (n + 1)
    if i / 1 == int(i):  # if 'i' is an integer...
        print("{}th Percentile: {}".format(k,li[int(i)-1]))
    else:
        i_down = int(i)
        i_up = int(i)+1
        print("{}th Percentile: {:.1f}".format(k,mean([li[i_down-1],li[i_up-1]])))

def revperc(v,li):
    if v < min(li) or v > max(li): return print("OOPS! Invalid value. Ensure to select one that is in the range of the data")
    li.sort()
    xli = sorted([x for x in li if x < v])  # Number of data < value
    x = len(xli)                            # " " "
    yli = [y for y in li if y == v]         # Number of times value shows up in the passed list
    y = len(yli)                            # " " "
    n = len(li)                             # lenght of entire list
    
    k = round((x + 0.5*y)/n*100)

    print("{} is the {}th Percentile".format(v,k))

def stats(li):
    # Q1 ~ 25th percentile; Q2 ~ 50th percentile and median; Q3 ~ 75th percentile;
    # sort the list from smallest to largest
    # if len(li) of a quartile == 0, it is the mean of the 2 most-central points
    li.sort()   # orders the values from smallest to largest
    # [52, 68, 73, 77, 82, 89, 91, 96]  --> for list where len == 8, Q2 would be mean(ix3, ix4) --> len(li)/2-1, len(li)/2
    #   0   1   2   3   4   5   6   7
    # [52, 68, 73, 75, 77, 82, 89, 91, 96, 97]  --> for list where len == 8, Q2 would be mean(ix3, ix4) --> len(li)/2-1, len(li)/2
    #   0   1   2   3   4   5   6   7   8   9
    # [52, 68, 73, 75, 77, 82, 91, 96, 97]  --> for list where len == 8, Q2 would be mean(ix3, ix4) --> len(li)/2-1, len(li)/2
    #   0   1   2   3   4   5   6   7   8
    # rli = sorted([random.randint(20,100) for x in range(20)])
    # feb_tmax = [tmax for y in clmt if type(y) == int for m in clmt[y] if m in clmt[y] and m == 2 for tmax in clmt[y][m]["tmax"] if len(clmt[y][m]["tmax"]) > excludemonth]
    L1 = li[:-1 * int(len(li)/2)]
    L3 = li[-1 * int(len(li)/2):]
    if len(li) % 2 == 0 and len(li)/2 % 2 == 0:    # indicates an even number in the set whose mean is also an even number
        Q1 = mean([L1[int(len(L1)/2)-1],L1[int(len(L1)/2)]])
        Q2 = mean([li[int(len(li)/2)-1],li[int(len(li)/2)]])
        Q3 = mean([L3[int(len(L1)/2)-1],L3[int(len(L1)/2)]])
    else:
        if len(li) % 2 == 0: # indicates an even number in the set whose mean is an odd number
            Q2 = mean([li[int(len(li)/2)-1],li[int(len(li)/2)]])
            Q3 = L3[int(len(L3)/2)]
        else: 
            Q2 = li[int(len(li)/2)]   # odd number of items in list
            Q3 = L3[int(len(L3)/2)-1]
        Q1 = L1[int(len(L1)/2)]
    IQR = Q3 - Q1
    M = mean(li)
    PSDV = pstdev(li)
    colwidth = max(len(str(x)) for x in [Q1,Q2,Q3])
    print("Stats")
    print("-----")
    print(" {:^{cwid}} {:^{cwid}} {:^{cwid}}".format("Q1","Q2","Q3",cwid=colwidth))
    print(" {:-^{cwid}} {:-^{cwid}} {:-^{cwid}}".format("","","",cwid=colwidth))
    print(" {:^{cwid}} {:^{cwid}} {:^{cwid}}".format(Q1,Q2,Q3,cwid=colwidth))
    print("-----")
    print("Mean: {:.1f}".format(M),end="")
    print("; PSTDEV: +/- {:.1f}".format(PSDV))
    print("1STDEV Range: [ {:.1f}, {:.1f} ]".format(M-PSDV,M+PSDV),end="")
    print("; Values w/in 1PSTDEV: {:.1f}%".format(len([x for x in li if x >= M-PSDV and x <= M+PSDV])/len(li)*100))
    print("2STDEV Range: [ {:.1f}, {:.1f} ]".format(M-2*PSDV,M+2*PSDV),end="")
    print("; Values between 1 & 2PSTDEV: {:.1f}%".format((len([x for x in li if x >= M-2*PSDV and x <= M+2*PSDV])-len([x for x in li if x >= M-PSDV and x <= M+PSDV]))/len(li)*100))
    #print("Values w/in range (Q1,Q3]: {:.1f}%".format(len([x for x in li if x <= Q3 and x > Q1])/len(li)*100))
    print("IQR (Q3-Q1): {}".format(IQR),end="")
    print("; Range of Potential Outliers: < {}; > {}".format(Q1-1.5*IQR,Q3+1.5*IQR)) if min(li) < Q1-1.5*IQR or max(li) > Q3+1.5*IQR else print("; * No Outliers")
    print("Potential Outliers: QTY {}; {}".format(len([x for x in li if x < Q1-1.5*IQR or x > Q3+1.5*IQR]),[x for x in li if x < Q1-1.5*IQR or x > Q3+1.5*IQR])) if len([x for x in li if x < Q1-1.5*IQR or x > Q3+1.5*IQR]) > 0 else print("")

def histogram(li):
    li.sort()
    li_set = sorted(list(set(li)))
    d = {}
    for x in li:
        if x not in d: d[x] = 1
        else: d[x] += 1
    max_rows = max(amt for amt in d)
    print("Temperature","Frequency",sep=",")
    for x in li_set: print("{}".format(x),"{}".format(d[x]),sep=",")

class DayRecord:
    """Parses each line of date-specific data; not used by user"""
    # int(each[5][0:4])][int(each[5][5:7])][int(each[5][8:10])
    def __init__(self,raw):
        self.stationid = raw[0]
        self.station_name = raw[1]
        self.station_lat = raw[2]
        self.station_lon = raw[3]
        self.station_elev = raw[4]
        ry = int(raw[5][0:4])
        rm = int(raw[5][5:7])
        rd = int(raw[5][8:10])
        self.daystr = raw[5]
        self.entryday = datetime.date(ry,rm,rd)
        # PRCP - Precipitation
        self.prcp = raw[6]
        flags_prcp = raw[7].split(",")
        self.prcpM, self.prcpQ, self.prcpS, self.prcpT = attchk(flags_prcp)
        if self.prcpQ in ignoreflags and self.prcp not in ["9999","-9999",""] and float(self.prcp) > 0:
            if round(float(self.prcp),2) not in clmt_vars_days["prcp"]:
                clmt_vars_days["prcp"][round(float(self.prcp),2)] = []
            clmt_vars_days["prcp"][round(float(self.prcp),2)].append(self.entryday)
        # SNOW - Snow
        self.snow = raw[8]
        flags_snow = raw[9].split(",")
        self.snowM, self.snowQ, self.snowS, self.snowT = attchk(flags_snow)
        if self.snowQ in ignoreflags and self.snow not in ["9999","-9999",""] and float(self.snow) > 0:
            if round(float(self.snow),1) not in clmt_vars_days["snow"]:
                clmt_vars_days["snow"][round(float(self.snow),1)] = []
            clmt_vars_days["snow"][round(float(self.snow),1)].append(self.entryday)
        # SNWD - Snow Depth
        self.snwd = raw[10]
        flags_snwd = raw[11].split(",")
        self.snwdM, self.snwdQ, self.snwdS, self.snwdT = attchk(flags_snwd)
        if self.snwdQ in ignoreflags and self.snwd not in ["9999","-9999",""] and float(self.snwd) > 0:
            if round(float(self.snwd),1) not in clmt_vars_days["snwd"]:
                clmt_vars_days["snwd"][round(float(self.snwd),1)] = []
            clmt_vars_days["snwd"][round(float(self.snwd),1)].append(self.entryday)
        # TMAX - Maximum Temperature
        self.tmax = raw[12]
        flags_tmax = raw[13].split(",")
        self.tmaxM, self.tmaxQ, self.tmaxS, self.tmaxT = attchk(flags_tmax)
        if self.tmaxQ in ignoreflags and self.tmax not in ["9999","-9999",""]:
            if int(self.tmax) not in clmt_vars_days["tmax"]:
                clmt_vars_days["tmax"][int(self.tmax)] = []
            clmt_vars_days["tmax"][int(self.tmax)].append(self.entryday)
        # TMIN - Minimum Temperature
        self.tmin = raw[14]
        flags_tmin = raw[15].split(",")
        self.tminM, self.tminQ, self.tminS, self.tminT = attchk(flags_tmin)
        if self.tminQ in ignoreflags and self.tmin not in ["9999","-9999",""]:
            if int(self.tmin) not in clmt_vars_days["tmin"]:
                clmt_vars_days["tmin"][int(self.tmin)] = []
            clmt_vars_days["tmin"][int(self.tmin)].append(self.entryday)
        # TAVG - Daily Average Temperature
        if self.tmaxQ in ignoreflags and self.tmax not in ["9999","-9999",""] and self.tminQ in ignoreflags and self.tmin not in ["9999","-9999",""]:
            tempavg = round(mean([int(self.tmax),int(self.tmin)]),1)
            if tempavg not in clmt_vars_days["tavg"]:
                clmt_vars_days["tavg"][tempavg] = []
            clmt_vars_days["tavg"][tempavg].append(self.entryday)

def clmtAnalyze(filename,**CITY):
    """Initializes the build of city & session-specific climate dictionaries;
    Required for the successful use of the script.
    
    clmtAnalzye(filename, **{city=str})

    REQUIRED: filename --> str version of the filename (a csv) of interest.
    OPT **kwargs: city=str --> Dictates output of the city-name. This is
                               useful if multiple stations are compiled
                               together to represent the data as it wouldn't
                               be recommended to use a singular station's name
                               if it isn't a complete representation of the
                               data.
    """
    
    if os.path.isfile(filename) == False: return print('"{}" not found! Try again!'.format(filename))
    global clmt
    global metclmt
    global FILE
    global clmt_vars_days
    global clmt_vars_months
    global station_ids
    FILE = filename
    clmt = {}
    metclmt = {}
    clmt_vars_days = {"prcp":{},"snow":{},"snwd":{},"tavg":{},"tmax":{},"tmin":{}}
    clmt_vars_months = {"prcp":{},"prcpDAYS":{},"snow":{},"snowDAYS":{},"snwd":{},"snwdDAYS":{},"tavg":{},"tmax":{},"tmin":{}}
    station_ids = []
    START = time()
    print("*** Script Running. Please Wait ***")

    def statbuild(y,m,d):   # Will run through if clmt[y][m][d] doesn't exist
        # YEAR and MONTH - Additional keys
        if "recordqty" not in clmt[y]: clmt[y]["recordqty"] = 1
        else: clmt[y]["recordqty"] += 1
        if "recordqty" not in clmt[y][m]: clmt[y][m]["recordqty"] = 1
        else: clmt[y][m]["recordqty"] += 1
        if "prcp" not in clmt[y]:
            clmt[y]["prcp"] = []
            clmt[y]["prcpDAYS"] = 0
            clmt[y]["prcpPROP"] = {"day_max":[-1,[]],"month_max":[-1,[]],"month_min":[999,[]]}
        if "prcp" not in clmt[y][m]:
            clmt[y][m]["prcp"] = []
            clmt[y][m]["prcpDAYS"] = 0
            clmt[y][m]["prcpPROP"] = {"day_max":[-1,[]]}
        if clmt[y][m][d].prcpQ in ignoreflags and clmt[y][m][d].prcp not in ["9999","-9999",""]:
            if float(clmt[y][m][d].prcp) > 0:
                clmt[y]["prcp"].append(float(clmt[y][m][d].prcp))
                if round(float(clmt[y][m][d].prcp),2) == clmt[y]["prcpPROP"]["day_max"][0]:
                    clmt[y]["prcpPROP"]["day_max"][1].append(clmt[y][m][d])
                elif round(float(clmt[y][m][d].prcp),2) > clmt[y]["prcpPROP"]["day_max"][0]:
                    clmt[y]["prcpPROP"]["day_max"][0] = round(float(clmt[y][m][d].prcp),2)
                    clmt[y]["prcpPROP"]["day_max"][1] = []
                    clmt[y]["prcpPROP"]["day_max"][1].append(clmt[y][m][d])
                clmt[y][m]["prcp"].append(float(clmt[y][m][d].prcp))
                if round(float(clmt[y][m][d].prcp),2) == clmt[y][m]["prcpPROP"]["day_max"][0]:
                    clmt[y][m]["prcpPROP"]["day_max"][1].append(clmt[y][m][d])
                elif round(float(clmt[y][m][d].prcp),2) > clmt[y][m]["prcpPROP"]["day_max"][0]:
                    clmt[y][m]["prcpPROP"]["day_max"][0] = round(float(clmt[y][m][d].prcp),2)
                    clmt[y][m]["prcpPROP"]["day_max"][1] = []
                    clmt[y][m]["prcpPROP"]["day_max"][1].append(clmt[y][m][d])
            if float(clmt[y][m][d].prcp) > 0 or clmt[y][m][d].prcpM == "T":
                clmt[y]["prcpDAYS"] += 1
                clmt[y][m]["prcpDAYS"] += 1
        if "snow" not in clmt[y]:
            clmt[y]["snow"] = []
            clmt[y]["snowDAYS"] = 0
            clmt[y]["snowPROP"] = {"day_max":[-1,[]],"month_max":[-1,[]]}
        if "snow" not in clmt[y][m]:
            clmt[y][m]["snow"] = []
            clmt[y][m]["snowDAYS"] = 0
            clmt[y][m]["snowPROP"] = {"day_max":[-1,[]]}
        if clmt[y][m][d].snowQ in ignoreflags and clmt[y][m][d].snow not in ["9999","-9999",""]:
            if float(clmt[y][m][d].snow) > 0:
                clmt[y]["snow"].append(float(clmt[y][m][d].snow))
                if round(float(clmt[y][m][d].snow),1) == clmt[y]["snowPROP"]["day_max"][0]:
                    clmt[y]["snowPROP"]["day_max"][1].append(clmt[y][m][d])
                elif round(float(clmt[y][m][d].snow),1) > clmt[y]["snowPROP"]["day_max"][0]:
                    clmt[y]["snowPROP"]["day_max"][0] = round(float(clmt[y][m][d].snow),1)
                    clmt[y]["snowPROP"]["day_max"][1] = []
                    clmt[y]["snowPROP"]["day_max"][1].append(clmt[y][m][d])
                clmt[y][m]["snow"].append(float(clmt[y][m][d].snow))
                if round(float(clmt[y][m][d].snow),1) == clmt[y][m]["snowPROP"]["day_max"][0]:
                    clmt[y][m]["snowPROP"]["day_max"][1].append(clmt[y][m][d])
                elif round(float(clmt[y][m][d].snow),1) > clmt[y][m]["snowPROP"]["day_max"][0]:
                    clmt[y][m]["snowPROP"]["day_max"][0] = round(float(clmt[y][m][d].snow),1)
                    clmt[y][m]["snowPROP"]["day_max"][1] = []
                    clmt[y][m]["snowPROP"]["day_max"][1].append(clmt[y][m][d])
            if float(clmt[y][m][d].snow) > 0 or clmt[y][m][d].snowM == "T":
                clmt[y]["snowDAYS"] += 1
                clmt[y][m]["snowDAYS"] += 1
        if "snwd" not in clmt[y]:
            clmt[y]["snwd"] = []
            clmt[y]["snwdDAYS"] = 0
            clmt[y]["snwdPROP"] = {"day_max":[-1,[]]}
        if "snwd" not in clmt[y][m]:
            clmt[y][m]["snwd"] = []
            clmt[y][m]["snwdDAYS"] = 0
            clmt[y][m]["snwdPROP"] = {"day_max":[-1,[]]}
        if clmt[y][m][d].snwdQ in ignoreflags and clmt[y][m][d].snwd not in ["9999","-9999",""]:
            if float(clmt[y][m][d].snwd) > 0:
                clmt[y]["snwd"].append(float(clmt[y][m][d].snwd))
                if round(float(clmt[y][m][d].snwd),1) == clmt[y]["snwdPROP"]["day_max"][0]:
                    clmt[y]["snwdPROP"]["day_max"][1].append(clmt[y][m][d])
                elif round(float(clmt[y][m][d].snwd),1) > clmt[y]["snwdPROP"]["day_max"][0]:
                    clmt[y]["snwdPROP"]["day_max"][0] = round(float(clmt[y][m][d].snwd),1)
                    clmt[y]["snwdPROP"]["day_max"][1] = []
                    clmt[y]["snwdPROP"]["day_max"][1].append(clmt[y][m][d])
                clmt[y][m]["snwd"].append(float(clmt[y][m][d].snwd))
                if round(float(clmt[y][m][d].snwd),1) == clmt[y][m]["snwdPROP"]["day_max"][0]:
                    clmt[y][m]["snwdPROP"]["day_max"][1].append(clmt[y][m][d])
                elif round(float(clmt[y][m][d].snwd),1) > clmt[y][m]["snwdPROP"]["day_max"][0]:
                    clmt[y][m]["snwdPROP"]["day_max"][0] = round(float(clmt[y][m][d].snwd),1)
                    clmt[y][m]["snwdPROP"]["day_max"][1] = []
                    clmt[y][m]["snwdPROP"]["day_max"][1].append(clmt[y][m][d])
            if float(clmt[y][m][d].snwd) > 0 or clmt[y][m][d].snwdM == "T":
                clmt[y]["snwdDAYS"] += 1
                clmt[y][m]["snwdDAYS"] += 1
        if "tmax" not in clmt[y]:
            clmt[y]["tempAVGlist"] = []
            clmt[y]["tmax"] = []
            clmt[y]["tmaxPROP"] = {"day_max":[-999,[]],"day_min":[999,[]],"month_AVG_max":[-999,[]],"month_AVG_min":[999,[]]}
        if "tmax" not in clmt[y][m]:
            clmt[y][m]["tempAVGlist"] = []
            clmt[y][m]["tmax"] = []
            clmt[y][m]["tmaxPROP"] = {"day_max":[-999,[]],"day_min":[999,[]]}
        if "tmin" not in clmt[y]:
            clmt[y]["tmin"] = []
            clmt[y]["tminPROP"] = {"day_max":[-999,[]],"day_min":[999,[]],"month_AVG_max":[-999,[]],"month_AVG_min":[999,[]]}
        if "tmin" not in clmt[y][m]:
            clmt[y][m]["tmin"] = []
            clmt[y][m]["tminPROP"] = {"day_max":[-999,[]],"day_min":[999,[]]}
        if clmt[y][m][d].tmaxQ in ignoreflags and clmt[y][m][d].tmax not in ["9999","-9999",""]:
            if (clmt[y][m][d].tmin != "" and int(clmt[y][m][d].tmax) >= int(clmt[y][m][d].tmin)) or clmt[y][m][d].tmin == "":
                clmt[y]["tmax"].append(int(clmt[y][m][d].tmax))
                clmt[y][m]["tmax"].append(int(clmt[y][m][d].tmax))
                if int(clmt[y][m][d].tmax) == clmt[y]["tmaxPROP"]["day_max"][0]:
                    clmt[y]["tmaxPROP"]["day_max"][1].append(clmt[y][m][d])
                elif int(clmt[y][m][d].tmax) > clmt[y]["tmaxPROP"]["day_max"][0]:
                    clmt[y]["tmaxPROP"]["day_max"][0] = int(clmt[y][m][d].tmax)
                    clmt[y]["tmaxPROP"]["day_max"][1] = []
                    clmt[y]["tmaxPROP"]["day_max"][1].append(clmt[y][m][d])
                if int(clmt[y][m][d].tmax) == clmt[y]["tmaxPROP"]["day_min"][0]:
                    clmt[y]["tmaxPROP"]["day_min"][1].append(clmt[y][m][d])
                elif int(clmt[y][m][d].tmax) < clmt[y]["tmaxPROP"]["day_min"][0]:
                    clmt[y]["tmaxPROP"]["day_min"][0] = int(clmt[y][m][d].tmax)
                    clmt[y]["tmaxPROP"]["day_min"][1] = []
                    clmt[y]["tmaxPROP"]["day_min"][1].append(clmt[y][m][d])
                if int(clmt[y][m][d].tmax) == clmt[y][m]["tmaxPROP"]["day_max"][0]:
                    clmt[y][m]["tmaxPROP"]["day_max"][1].append(clmt[y][m][d])
                elif int(clmt[y][m][d].tmax) > clmt[y][m]["tmaxPROP"]["day_max"][0]:
                    clmt[y][m]["tmaxPROP"]["day_max"][0] = int(clmt[y][m][d].tmax)
                    clmt[y][m]["tmaxPROP"]["day_max"][1] = []
                    clmt[y][m]["tmaxPROP"]["day_max"][1].append(clmt[y][m][d])
                if int(clmt[y][m][d].tmax) == clmt[y][m]["tmaxPROP"]["day_min"][0]:
                    clmt[y][m]["tmaxPROP"]["day_min"][1].append(clmt[y][m][d])
                elif int(clmt[y][m][d].tmax) < clmt[y][m]["tmaxPROP"]["day_min"][0]:
                    clmt[y][m]["tmaxPROP"]["day_min"][0] = int(clmt[y][m][d].tmax)
                    clmt[y][m]["tmaxPROP"]["day_min"][1] = []
                    clmt[y][m]["tmaxPROP"]["day_min"][1].append(clmt[y][m][d])
        if clmt[y][m][d].tminQ in ignoreflags and clmt[y][m][d].tmin not in ["9999","-9999",""]:
            if (clmt[y][m][d].tmax != "" and int(clmt[y][m][d].tmin) <= int(clmt[y][m][d].tmax)) or clmt[y][m][d].tmax == "":
                clmt[y]["tmin"].append(int(clmt[y][m][d].tmin))
                clmt[y][m]["tmin"].append(int(clmt[y][m][d].tmin))
                if int(clmt[y][m][d].tmin) == clmt[y]["tminPROP"]["day_max"][0]:
                    clmt[y]["tminPROP"]["day_max"][1].append(clmt[y][m][d])
                elif int(clmt[y][m][d].tmin) > clmt[y]["tminPROP"]["day_max"][0]:
                    clmt[y]["tminPROP"]["day_max"][0] = int(clmt[y][m][d].tmin)
                    clmt[y]["tminPROP"]["day_max"][1] = []
                    clmt[y]["tminPROP"]["day_max"][1].append(clmt[y][m][d])
                if int(clmt[y][m][d].tmin) == clmt[y]["tminPROP"]["day_min"][0]:
                    clmt[y]["tminPROP"]["day_min"][1].append(clmt[y][m][d])
                elif int(clmt[y][m][d].tmin) < clmt[y]["tminPROP"]["day_min"][0]:
                    clmt[y]["tminPROP"]["day_min"][0] = int(clmt[y][m][d].tmin)
                    clmt[y]["tminPROP"]["day_min"][1] = []
                    clmt[y]["tminPROP"]["day_min"][1].append(clmt[y][m][d])
                if int(clmt[y][m][d].tmin) == clmt[y][m]["tminPROP"]["day_max"][0]:
                    clmt[y][m]["tminPROP"]["day_max"][1].append(clmt[y][m][d])
                elif int(clmt[y][m][d].tmin) > clmt[y][m]["tminPROP"]["day_max"][0]:
                    clmt[y][m]["tminPROP"]["day_max"][0] = int(clmt[y][m][d].tmin)
                    clmt[y][m]["tminPROP"]["day_max"][1] = []
                    clmt[y][m]["tminPROP"]["day_max"][1].append(clmt[y][m][d])
                if int(clmt[y][m][d].tmin) == clmt[y][m]["tminPROP"]["day_min"][0]:
                    clmt[y][m]["tminPROP"]["day_min"][1].append(clmt[y][m][d])
                elif int(clmt[y][m][d].tmin) < clmt[y][m]["tminPROP"]["day_min"][0]:
                    clmt[y][m]["tminPROP"]["day_min"][0] = int(clmt[y][m][d].tmin)
                    clmt[y][m]["tminPROP"]["day_min"][1] = []
                    clmt[y][m]["tminPROP"]["day_min"][1].append(clmt[y][m][d])
        if clmt[y][m][d].tmaxQ in ignoreflags and clmt[y][m][d].tmax not in ["9999","-9999",""] and clmt[y][m][d].tminQ in ignoreflags and clmt[y][m][d].tmin not in ["9999","-9999",""] and int(clmt[y][m][d].tmax) >= int(clmt[y][m][d].tmin):
            clmt[y]["tempAVGlist"].append(int(clmt[y][m][d].tmax))
            clmt[y]["tempAVGlist"].append(int(clmt[y][m][d].tmin))
            clmt[y][m]["tempAVGlist"].append(int(clmt[y][m][d].tmax))
            clmt[y][m]["tempAVGlist"].append(int(clmt[y][m][d].tmin))

    with open(filename,newline="") as f:
        print("--- COMPILING DICTIONARIES ---")
        csvfile = csv.reader(f, delimiter=',')
        for each in csvfile:
            if each[0] in ["STATION",'"STATION"']:
                pass
            else:
                if each[0] not in station_ids: station_ids.append(each[0])
                if "station" not in clmt:
                    if "city" in CITY: clmt["station_name"] = CITY["city"]
                    else: clmt["station_name"] = each[1]
                    clmt["station"] = each[0]
                    print("--- City: {} ---".format(clmt["station_name"]))
                    clmt["coordinates"] = "{}, {}".format(each[2],each[3])
                    clmt["elevation"] = each[4]
                if "station" not in metclmt:
                    if "city" in CITY: metclmt["station_name"] = CITY["city"]
                    else: metclmt["station_name"] = each[1]
                    metclmt["station"] = each[0]
                    metclmt["coordinates"] = "{}, {}".format(each[2],each[3])
                    metclmt["elevation"] = each[4]
                #if y % 10 == 0: print("{},".format(each[5][0:4]),end=" ")
                y = int(each[5][0:4])
                m = int(each[5][5:7])
                d = int(each[5][8:10])
                if y not in clmt: clmt[y] = {}  # YEAR
                if m not in clmt[y]: clmt[y][m] = {}  # MONTH
                # DAY Record stuff
                if d in clmt[y][m]:     # This will replace the existing DayRecord if the entire entry was blank
                    if all(v == "" for v in [clmt[y][m][d].prcp,clmt[y][m][d].snow,clmt[y][m][d].snwd,clmt[y][m][d].tmax,clmt[y][m][d].tmin]):
                        clmt[y][m][d].stationid = each[0]
                        clmt[y][m][d].station_name = each[1]
                        clmt[y][m][d].station_lat = each[2]
                        clmt[y][m][d].station_lon = each[3]
                        clmt[y][m][d].station_elev = each[4]
                        clmt[y][m][d].prcp = each[6]
                        flags_prcp = each[7].split(",")
                        clmt[y][m][d].prcpM, clmt[y][m][d].prcpQ, clmt[y][m][d].prcpS, clmt[y][m][d].prcpT = attchk(flags_prcp)
                        if clmt[y][m][d].prcp not in ["","-9999","9999"] and clmt[y][m][d].prcpQ in ignoreflags:
                            if float(clmt[y][m][d].prcp) > 0:
                                clmt[y]["prcp"].append(float(clmt[y][m][d].prcp))
                                if round(float(clmt[y][m][d].prcp),2) == clmt[y]["prcpPROP"]["day_max"][0]:
                                    clmt[y]["prcpPROP"]["day_max"][1].append(clmt[y][m][d])
                                elif round(float(clmt[y][m][d].prcp),2) > clmt[y]["prcpPROP"]["day_max"][0]:
                                    clmt[y]["prcpPROP"]["day_max"][0] = round(float(clmt[y][m][d].prcp),2)
                                    clmt[y]["prcpPROP"]["day_max"][1] = []
                                    clmt[y]["prcpPROP"]["day_max"][1].append(clmt[y][m][d])
                                clmt[y][m]["prcp"].append(float(clmt[y][m][d].prcp))
                                if round(float(clmt[y][m][d].prcp),2) == clmt[y][m]["prcpPROP"]["day_max"][0]:
                                    clmt[y][m]["prcpPROP"]["day_max"][1].append(clmt[y][m][d])
                                elif round(float(clmt[y][m][d].prcp),2) > clmt[y][m]["prcpPROP"]["day_max"][0]:
                                    clmt[y][m]["prcpPROP"]["day_max"][0] = round(float(clmt[y][m][d].prcp),2)
                                    clmt[y][m]["prcpPROP"]["day_max"][1] = []
                                    clmt[y][m]["prcpPROP"]["day_max"][1].append(clmt[y][m][d])
                            if float(clmt[y][m][d].prcp) > 0 or clmt[y][m][d].prcpM == "T":
                                clmt[y]["prcpDAYS"] += 1
                                clmt[y][m]["prcpDAYS"] += 1
                        clmt[y][m][d].snow = each[8]
                        flags_snow = each[9].split(",")
                        clmt[y][m][d].snowM, clmt[y][m][d].snowQ, clmt[y][m][d].snowS, clmt[y][m][d].snowT = attchk(flags_snow)
                        if clmt[y][m][d].snowQ in ignoreflags and clmt[y][m][d].snow not in ["9999","-9999",""]:
                            if float(clmt[y][m][d].snow) > 0:
                                clmt[y]["snow"].append(float(clmt[y][m][d].snow))
                                if round(float(clmt[y][m][d].snow),1) == clmt[y]["snowPROP"]["day_max"][0]:
                                    clmt[y]["snowPROP"]["day_max"][1].append(clmt[y][m][d])
                                elif round(float(clmt[y][m][d].snow),1) > clmt[y]["snowPROP"]["day_max"][0]:
                                    clmt[y]["snowPROP"]["day_max"][0] = round(float(clmt[y][m][d].snow),1)
                                    clmt[y]["snowPROP"]["day_max"][1] = []
                                    clmt[y]["snowPROP"]["day_max"][1].append(clmt[y][m][d])
                                clmt[y][m]["snow"].append(float(clmt[y][m][d].snow))
                                if round(float(clmt[y][m][d].snow),1) == clmt[y][m]["snowPROP"]["day_max"][0]:
                                    clmt[y][m]["snowPROP"]["day_max"][1].append(clmt[y][m][d])
                                elif round(float(clmt[y][m][d].snow),1) > clmt[y][m]["snowPROP"]["day_max"][0]:
                                    clmt[y][m]["snowPROP"]["day_max"][0] = round(float(clmt[y][m][d].snow),1)
                                    clmt[y][m]["snowPROP"]["day_max"][1] = []
                                    clmt[y][m]["snowPROP"]["day_max"][1].append(clmt[y][m][d])
                            if float(clmt[y][m][d].snow) > 0 or clmt[y][m][d].snowM == "T":
                                clmt[y]["snowDAYS"] += 1
                                clmt[y][m]["snowDAYS"] += 1
                        clmt[y][m][d].snwd = each[10]
                        flags_snwd = each[11].split(",")
                        clmt[y][m][d].snwdM, clmt[y][m][d].snwdQ, clmt[y][m][d].snwdS, clmt[y][m][d].snwdT = attchk(flags_snwd)
                        if clmt[y][m][d].snwdQ in ignoreflags and clmt[y][m][d].snwd not in ["9999","-9999",""]:
                            if float(clmt[y][m][d].snwd) > 0:
                                clmt[y]["snwd"].append(float(clmt[y][m][d].snwd))
                                if round(float(clmt[y][m][d].snwd),1) == clmt[y]["snwdPROP"]["day_max"][0]:
                                    clmt[y]["snwdPROP"]["day_max"][1].append(clmt[y][m][d])
                                elif round(float(clmt[y][m][d].snwd),1) > clmt[y]["snwdPROP"]["day_max"][0]:
                                    clmt[y]["snwdPROP"]["day_max"][0] = round(float(clmt[y][m][d].snwd),1)
                                    clmt[y]["snwdPROP"]["day_max"][1] = []
                                    clmt[y]["snwdPROP"]["day_max"][1].append(clmt[y][m][d])
                                clmt[y][m]["snwd"].append(float(clmt[y][m][d].snwd))
                                if round(float(clmt[y][m][d].snwd),1) == clmt[y][m]["snwdPROP"]["day_max"][0]:
                                    clmt[y][m]["snwdPROP"]["day_max"][1].append(clmt[y][m][d])
                                elif round(float(clmt[y][m][d].snwd),1) > clmt[y][m]["snwdPROP"]["day_max"][0]:
                                    clmt[y][m]["snwdPROP"]["day_max"][0] = round(float(clmt[y][m][d].snwd),1)
                                    clmt[y][m]["snwdPROP"]["day_max"][1] = []
                                    clmt[y][m]["snwdPROP"]["day_max"][1].append(clmt[y][m][d])
                            if float(clmt[y][m][d].snwd) > 0 or clmt[y][m][d].snwdM == "T":
                                clmt[y]["snwdDAYS"] += 1
                                clmt[y][m]["snwdDAYS"] += 1
                        clmt[y][m][d].tmax = each[12]
                        flags_tmax = each[13].split(",")
                        clmt[y][m][d].tmaxM, clmt[y][m][d].tmaxQ, clmt[y][m][d].tmaxS, clmt[y][m][d].tmaxT = attchk(flags_tmax)
                        clmt[y][m][d].tmin = each[14]
                        flags_tmin = each[15].split(",")
                        clmt[y][m][d].tminM, clmt[y][m][d].tminQ, clmt[y][m][d].tminS, clmt[y][m][d].tminT = attchk(flags_tmin)
                        if clmt[y][m][d].tmaxQ in ignoreflags and clmt[y][m][d].tmax not in ["9999","-9999",""]:
                            if (clmt[y][m][d].tmin != "" and int(clmt[y][m][d].tmax) >= int(clmt[y][m][d].tmin)) or clmt[y][m][d].tmin == "":
                                clmt[y]["tmax"].append(int(clmt[y][m][d].tmax))
                                clmt[y][m]["tmax"].append(int(clmt[y][m][d].tmax))
                                if int(clmt[y][m][d].tmax) == clmt[y]["tmaxPROP"]["day_max"][0]:
                                    clmt[y]["tmaxPROP"]["day_max"][1].append(clmt[y][m][d])
                                elif int(clmt[y][m][d].tmax) > clmt[y]["tmaxPROP"]["day_max"][0]:
                                    clmt[y]["tmaxPROP"]["day_max"][0] = int(clmt[y][m][d].tmax)
                                    clmt[y]["tmaxPROP"]["day_max"][1] = []
                                    clmt[y]["tmaxPROP"]["day_max"][1].append(clmt[y][m][d])
                                if int(clmt[y][m][d].tmax) == clmt[y]["tmaxPROP"]["day_min"][0]:
                                    clmt[y]["tmaxPROP"]["day_min"][1].append(clmt[y][m][d])
                                elif int(clmt[y][m][d].tmax) < clmt[y]["tmaxPROP"]["day_min"][0]:
                                    clmt[y]["tmaxPROP"]["day_min"][0] = int(clmt[y][m][d].tmax)
                                    clmt[y]["tmaxPROP"]["day_min"][1] = []
                                    clmt[y]["tmaxPROP"]["day_min"][1].append(clmt[y][m][d])
                                if int(clmt[y][m][d].tmax) == clmt[y][m]["tmaxPROP"]["day_max"][0]:
                                    clmt[y][m]["tmaxPROP"]["day_max"][1].append(clmt[y][m][d])
                                elif int(clmt[y][m][d].tmax) > clmt[y][m]["tmaxPROP"]["day_max"][0]:
                                    clmt[y][m]["tmaxPROP"]["day_max"][0] = int(clmt[y][m][d].tmax)
                                    clmt[y][m]["tmaxPROP"]["day_max"][1] = []
                                    clmt[y][m]["tmaxPROP"]["day_max"][1].append(clmt[y][m][d])
                                if int(clmt[y][m][d].tmax) == clmt[y][m]["tmaxPROP"]["day_min"][0]:
                                    clmt[y][m]["tmaxPROP"]["day_min"][1].append(clmt[y][m][d])
                                elif int(clmt[y][m][d].tmax) < clmt[y][m]["tmaxPROP"]["day_min"][0]:
                                    clmt[y][m]["tmaxPROP"]["day_min"][0] = int(clmt[y][m][d].tmax)
                                    clmt[y][m]["tmaxPROP"]["day_min"][1] = []
                                    clmt[y][m]["tmaxPROP"]["day_min"][1].append(clmt[y][m][d])
                        if clmt[y][m][d].tminQ in ignoreflags and clmt[y][m][d].tmin not in ["9999","-9999",""]:
                            if (clmt[y][m][d].tmax != "" and int(clmt[y][m][d].tmin) <= int(clmt[y][m][d].tmax)) or clmt[y][m][d].tmax == "":
                                clmt[y]["tmin"].append(int(clmt[y][m][d].tmin))
                                clmt[y][m]["tmin"].append(int(clmt[y][m][d].tmin))
                                if int(clmt[y][m][d].tmin) == clmt[y]["tminPROP"]["day_max"][0]:
                                    clmt[y]["tminPROP"]["day_max"][1].append(clmt[y][m][d])
                                elif int(clmt[y][m][d].tmin) > clmt[y]["tminPROP"]["day_max"][0]:
                                    clmt[y]["tminPROP"]["day_max"][0] = int(clmt[y][m][d].tmin)
                                    clmt[y]["tminPROP"]["day_max"][1] = []
                                    clmt[y]["tminPROP"]["day_max"][1].append(clmt[y][m][d])
                                if int(clmt[y][m][d].tmin) == clmt[y]["tminPROP"]["day_min"][0]:
                                    clmt[y]["tminPROP"]["day_min"][1].append(clmt[y][m][d])
                                elif int(clmt[y][m][d].tmin) < clmt[y]["tminPROP"]["day_min"][0]:
                                    clmt[y]["tminPROP"]["day_min"][0] = int(clmt[y][m][d].tmin)
                                    clmt[y]["tminPROP"]["day_min"][1] = []
                                    clmt[y]["tminPROP"]["day_min"][1].append(clmt[y][m][d])
                                if int(clmt[y][m][d].tmin) == clmt[y][m]["tminPROP"]["day_max"][0]:
                                    clmt[y][m]["tminPROP"]["day_max"][1].append(clmt[y][m][d])
                                elif int(clmt[y][m][d].tmin) > clmt[y][m]["tminPROP"]["day_max"][0]:
                                    clmt[y][m]["tminPROP"]["day_max"][0] = int(clmt[y][m][d].tmin)
                                    clmt[y][m]["tminPROP"]["day_max"][1] = []
                                    clmt[y][m]["tminPROP"]["day_max"][1].append(clmt[y][m][d])
                                if int(clmt[y][m][d].tmin) == clmt[y][m]["tminPROP"]["day_min"][0]:
                                    clmt[y][m]["tminPROP"]["day_min"][1].append(clmt[y][m][d])
                                elif int(clmt[y][m][d].tmin) < clmt[y][m]["tminPROP"]["day_min"][0]:
                                    clmt[y][m]["tminPROP"]["day_min"][0] = int(clmt[y][m][d].tmin)
                                    clmt[y][m]["tminPROP"]["day_min"][1] = []
                                    clmt[y][m]["tminPROP"]["day_min"][1].append(clmt[y][m][d])
                        if clmt[y][m][d].tmaxQ in ignoreflags and clmt[y][m][d].tmax not in ["9999","-9999",""] and clmt[y][m][d].tminQ in ignoreflags and clmt[y][m][d].tmin not in ["9999","-9999",""] and int(clmt[y][m][d].tmax) >= int(clmt[y][m][d].tmin):
                            clmt[y]["tempAVGlist"].append(int(clmt[y][m][d].tmax))
                            clmt[y]["tempAVGlist"].append(int(clmt[y][m][d].tmin))
                            clmt[y][m]["tempAVGlist"].append(int(clmt[y][m][d].tmax))
                            clmt[y][m]["tempAVGlist"].append(int(clmt[y][m][d].tmin))
                else:
                    clmt[y][m][d] = DayRecord(each)
                    statbuild(y,m,d)

    # MONTHLY STATS
    for y in [YR for YR in clmt if type(YR) == int]:
        for m in [MO for MO in clmt[y] if type(MO) == int]:
            # PRCP
            if round(sum(clmt[y][m]["prcp"]),2) not in clmt_vars_months["prcp"]: clmt_vars_months["prcp"][round(sum(clmt[y][m]["prcp"]),2)] = [datetime.date(y,m,1)]
            else: clmt_vars_months["prcp"][round(sum(clmt[y][m]["prcp"]),2)].append(datetime.date(y,m,1))
            if clmt[y][m]["prcpDAYS"] not in clmt_vars_months["prcpDAYS"]: clmt_vars_months["prcpDAYS"][clmt[y][m]["prcpDAYS"]] = [datetime.date(y,m,1)]
            else: clmt_vars_months["prcpDAYS"][clmt[y][m]["prcpDAYS"]].append(datetime.date(y,m,1))
            try:
                if round(sum(clmt[y][m]["prcp"]),2) == clmt[y]["prcpPROP"]["month_max"][0]:
                    clmt[y]["prcpPROP"]["month_max"][1].append(m)
                elif round(sum(clmt[y][m]["prcp"]),2) > clmt[y]["prcpPROP"]["month_max"][0]:
                    clmt[y]["prcpPROP"]["month_max"][0] = round(sum(clmt[y][m]["prcp"]),2)
                    clmt[y]["prcpPROP"]["month_max"][1] = []
                    clmt[y]["prcpPROP"]["month_max"][1].append(m)
                if round(sum(clmt[y][m]["prcp"]),2) == clmt[y]["prcpPROP"]["month_min"][0]:
                    clmt[y]["prcpPROP"]["month_min"][1].append(m)
                elif round(sum(clmt[y][m]["prcp"]),2) < clmt[y]["prcpPROP"]["month_min"][0]:
                    clmt[y]["prcpPROP"]["month_min"][0] = round(sum(clmt[y][m]["prcp"]),2)
                    clmt[y]["prcpPROP"]["month_min"][1] = []
                    clmt[y]["prcpPROP"]["month_min"][1].append(m)
            except:
                print("*** SKIPPED: Insufficient or erroneous PRCP data - {}-{}".format(y,str(m).zfill(2)))
            # SNOW
            if round(sum(clmt[y][m]["snow"]),1) not in clmt_vars_months["snow"]: clmt_vars_months["snow"][round(sum(clmt[y][m]["snow"]),1)] = [datetime.date(y,m,1)]
            else: clmt_vars_months["snow"][round(sum(clmt[y][m]["snow"]),1)].append(datetime.date(y,m,1))
            if clmt[y][m]["snowDAYS"] not in clmt_vars_months["snowDAYS"]: clmt_vars_months["snowDAYS"][clmt[y][m]["snowDAYS"]] = [datetime.date(y,m,1)]
            else: clmt_vars_months["snowDAYS"][clmt[y][m]["snowDAYS"]].append(datetime.date(y,m,1))
            #if sum(clmt[y][m]["snwd"]) not in clmt_vars_months["snwd"]: clmt_vars_months["snwd"][sum(clmt[y][m]["snwd"])] = [datetime.date(y,m,1)]
            #else: clmt_vars_months["snwd"][sum(clmt[y][m]["snwd"])].append(datetime.date(y,m,1))
            try:
                if round(sum(clmt[y][m]["snow"]),1) == clmt[y]["snowPROP"]["month_max"][0]:
                    clmt[y]["snowPROP"]["month_max"][1].append(m)
                elif round(sum(clmt[y][m]["snow"]),1) > clmt[y]["snowPROP"]["month_max"][0]:
                    clmt[y]["snowPROP"]["month_max"][0] = round(sum(clmt[y][m]["snow"]),1)
                    clmt[y]["snowPROP"]["month_max"][1] = []
                    clmt[y]["snowPROP"]["month_max"][1].append(m)
            except:
                print("*** SKIPPED: Insufficient or erroneous SNOW data - {}-{}".format(y,str(m).zfill(2)))
            # SNWD
            if clmt[y][m]["snwdDAYS"] not in clmt_vars_months["snwdDAYS"]: clmt_vars_months["snwdDAYS"][clmt[y][m]["snwdDAYS"]] = [datetime.date(y,m,1)]
            else: clmt_vars_months["snwdDAYS"][clmt[y][m]["snwdDAYS"]].append(datetime.date(y,m,1))
            # TMAX
            if len(clmt[y][m]["tmax"]) > excludemonth:
                if round(mean(clmt[y][m]["tmax"]),1) not in clmt_vars_months["tmax"]: clmt_vars_months["tmax"][round(mean(clmt[y][m]["tmax"]),1)] = [datetime.date(y,m,1)]
                else: clmt_vars_months["tmax"][round(mean(clmt[y][m]["tmax"]),1)].append(datetime.date(y,m,1))
            try:
                if round(mean(clmt[y][m]["tmax"]),1) == clmt[y]["tmaxPROP"]["month_AVG_max"][0]:
                    clmt[y]["tmaxPROP"]["month_AVG_max"][1].append(m)
                elif round(mean(clmt[y][m]["tmax"]),1) > clmt[y]["tmaxPROP"]["month_AVG_max"][0]:
                    clmt[y]["tmaxPROP"]["month_AVG_max"][0] = round(mean(clmt[y][m]["tmax"]),1)
                    clmt[y]["tmaxPROP"]["month_AVG_max"][1] = []
                    clmt[y]["tmaxPROP"]["month_AVG_max"][1].append(m)
                if round(mean(clmt[y][m]["tmax"]),1) == clmt[y]["tmaxPROP"]["month_AVG_min"][0]:
                    clmt[y]["tmaxPROP"]["month_AVG_min"][1].append(m)
                elif round(mean(clmt[y][m]["tmax"]),1) < clmt[y]["tmaxPROP"]["month_AVG_min"][0]:
                    clmt[y]["tmaxPROP"]["month_AVG_min"][0] = round(mean(clmt[y][m]["tmax"]),1)
                    clmt[y]["tmaxPROP"]["month_AVG_min"][1] = []
                    clmt[y]["tmaxPROP"]["month_AVG_min"][1].append(m)
            except:
                print("*** SKIPPED: Insufficient or erroneous TMAX data - {}-{}".format(y,str(m).zfill(2)))
            # TMIN
            if len(clmt[y][m]["tmin"]) > excludemonth:
                if round(mean(clmt[y][m]["tmin"]),1) not in clmt_vars_months["tmin"]: clmt_vars_months["tmin"][round(mean(clmt[y][m]["tmin"]),1)] = [datetime.date(y,m,1)]
                else: clmt_vars_months["tmin"][round(mean(clmt[y][m]["tmin"]),1)].append(datetime.date(y,m,1))
            try:
                if round(mean(clmt[y][m]["tmin"]),1) == clmt[y]["tminPROP"]["month_AVG_max"][0]:
                    clmt[y]["tminPROP"]["month_AVG_max"][1].append(m)
                elif round(mean(clmt[y][m]["tmin"]),1) > clmt[y]["tminPROP"]["month_AVG_max"][0]:
                    clmt[y]["tminPROP"]["month_AVG_max"][0] = round(mean(clmt[y][m]["tmin"]),1)
                    clmt[y]["tminPROP"]["month_AVG_max"][1] = []
                    clmt[y]["tminPROP"]["month_AVG_max"][1].append(m)
                if round(mean(clmt[y][m]["tmin"]),1) == clmt[y]["tminPROP"]["month_AVG_min"][0]:
                    clmt[y]["tminPROP"]["month_AVG_min"][1].append(m)
                elif round(mean(clmt[y][m]["tmin"]),1) < clmt[y]["tminPROP"]["month_AVG_min"][0]:
                    clmt[y]["tminPROP"]["month_AVG_min"][0] = round(mean(clmt[y][m]["tmin"]),1)
                    clmt[y]["tminPROP"]["month_AVG_min"][1] = []
                    clmt[y]["tminPROP"]["month_AVG_min"][1].append(m)
            except:
                print("*** SKIPPED: Insufficient or erroneous TMIN data - {}-{}".format(y,str(m).zfill(2)))
            if len(clmt[y][m]["tempAVGlist"]) > excludemonth * 2:
                if round(mean(clmt[y][m]["tempAVGlist"]),1) not in clmt_vars_months["tavg"]: clmt_vars_months["tavg"][round(mean(clmt[y][m]["tempAVGlist"]),1)] = [datetime.date(y,m,1)]
                else: clmt_vars_months["tavg"][round(mean(clmt[y][m]["tempAVGlist"]),1)].append(datetime.date(y,m,1))

    for YYYY in sorted([Y for Y in clmt if type(Y) == int]): # THIS IS THE CURRENT PROBLEM...NOT READING IN JAN/FEB DATA?
        if YYYY not in metclmt and any(MONTH >= 3 for MONTH in clmt[YYYY] if type(MONTH) == int):
            metclmt[YYYY] = {}
        for MM in sorted([M for M in clmt[YYYY] if type(M) == int]):
            if MM <= 2:
                if YYYY-1 in metclmt: metclmt[YYYY-1][MM] = clmt[YYYY][MM]
            else:
                metclmt[YYYY][MM] = clmt[YYYY][MM]
    for YYYY in [YEAR for YEAR in metclmt if type(YEAR) == int]:
        for s in ["spring","summer","fall","winter"]:
            metclmt[YYYY][s] = {}
            if s == "spring": metclmt[YYYY][s]["valid"] = [3,4,5]
            elif s == "summer": metclmt[YYYY][s]["valid"] = [6,7,8]
            elif s == "fall": metclmt[YYYY][s]["valid"] = [9,10,11]
            elif s == "winter": metclmt[YYYY][s]["valid"] = [12,1,2]
            else: return print("SEASON ERROR! Programmer! Check the seasons!")

    for y in [Y for Y in metclmt if type(Y) == int]:
        # PRCP
        metclmt[y]["recordqty"] = sum(metclmt[y][m]["recordqty"] for m in metclmt[y] if type(m) == int)
        #input("year = {}; recordqty = {}".format(y,metclmt[y]["recordqty"]))
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["recordqty"] = sum(metclmt[y][m]["recordqty"] for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"])
        metclmt[y]["prcp"] = []
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["prcp"] = []
        metclmt[y]["prcp"].extend(r for m in metclmt[y].keys() if type(m) == int for r in metclmt[y][m]["prcp"])
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["prcp"].extend(r for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] for r in metclmt[y][m]["prcp"])
        metclmt[y]["prcpDAYS"] = sum(metclmt[y][m]["prcpDAYS"] for m in metclmt[y] if type(m) == int)
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["prcpDAYS"] = sum(metclmt[y][m]["prcpDAYS"] for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"])
        metclmt[y]["prcpPROP"] = {"day_max":[-1,[]],"month_max":[-1,[]],"month_min":[999,[]]}
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["prcpPROP"] = {"day_max":[-1,[]],"month_max":[-1,[]],"month_min":[999,[]]}
        if len(metclmt[y]["prcp"]) > 0: metclmt[y]["prcpPROP"]["day_max"][0] = round(max(metclmt[y]["prcp"]),2)
        for s in ["spring","summer","fall","winter"]:
            if len(metclmt[y][s]["prcp"]) > 0: metclmt[y][s]["prcpPROP"]["day_max"][0] = round(max(metclmt[y][s]["prcp"]),2)
        metclmt[y]["prcpPROP"]["day_max"][1].extend(metclmt[y][m][d] for m in metclmt[y] if type(m) == int for d in metclmt[y][m] if type(d) == int and metclmt[y][m][d].prcpQ in ignoreflags and metclmt[y][m][d].prcp not in ["","-9999","9999"] and round(float(metclmt[y][m][d].prcp),2) == metclmt[y]["prcpPROP"]["day_max"][0])
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["prcpPROP"]["day_max"][1].extend(metclmt[y][m][d] for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] for d in metclmt[y][m] if type(d) == int and metclmt[y][m][d].prcpQ in ignoreflags and metclmt[y][m][d].prcp not in ["","-9999","9999"] and round(float(metclmt[y][m][d].prcp),2) == metclmt[y][s]["prcpPROP"]["day_max"][0])
        #if y >= 2019: print(y,calendar.month_abbr[m])
        metclmt[y]["prcpPROP"]["month_max"][0] = round(max(sum(metclmt[y][m]["prcp"]) for m in metclmt[y] if type(m) == int),2)
        for s in ["spring","summer","fall","winter"]:
            try: metclmt[y][s]["prcpPROP"]["month_max"][0] = round(max(sum(metclmt[y][m]["prcp"]) for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"]),2)
            except: pass #print(y,s,m,[M for M in metclmt[y] if type(M) == int])
        metclmt[y]["prcpPROP"]["month_max"][1].extend(m for m in metclmt[y] if type(m) == int and round(sum(metclmt[y][m]["prcp"]),2) == metclmt[y]["prcpPROP"]["month_max"][0])
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["prcpPROP"]["month_max"][1].extend(m for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] and round(sum(metclmt[y][m]["prcp"]),2) == metclmt[y][s]["prcpPROP"]["month_max"][0])
        metclmt[y]["prcpPROP"]["month_min"][0] = round(min(sum(metclmt[y][m]["prcp"]) for m in metclmt[y] if type(m) == int),2)
        for s in ["spring","summer","fall","winter"]:
            try: metclmt[y][s]["prcpPROP"]["month_min"][0] = round(min(sum(metclmt[y][m]["prcp"]) for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"]),2)
            except: pass #print(y,s,m,[M for M in metclmt[y] if type(M) == int])
        metclmt[y]["prcpPROP"]["month_min"][1].extend(m for m in metclmt[y] if type(m) == int and round(sum(metclmt[y][m]["prcp"]),2) == metclmt[y]["prcpPROP"]["month_min"][0])
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["prcpPROP"]["month_min"][1].extend(m for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] and round(sum(metclmt[y][m]["prcp"]),2) == metclmt[y][s]["prcpPROP"]["month_min"][0])
        # SNOW
        metclmt[y]["snow"] = []
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["snow"] = []
        metclmt[y]["snow"].extend(r for m in metclmt[y].keys() if type(m) == int for r in metclmt[y][m]["snow"])
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["snow"].extend(r for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] for r in metclmt[y][m]["snow"])
        metclmt[y]["snowDAYS"] = sum(metclmt[y][m]["snowDAYS"] for m in metclmt[y] if type(m) == int)
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["snowDAYS"] = sum(metclmt[y][m]["snowDAYS"] for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"])
        metclmt[y]["snowPROP"] = {"day_max":[-1,[]],"month_max":[-1,[]]}
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["snowPROP"] = {"day_max":[-1,[]],"month_max":[-1,[]]}
        if len(metclmt[y]["snow"]) > 0: metclmt[y]["snowPROP"]["day_max"][0] = round(max(metclmt[y]["snow"]),1)
        for s in ["spring","summer","fall","winter"]:
            if len(metclmt[y][s]["snow"]) > 0: metclmt[y][s]["snowPROP"]["day_max"][0] = round(max(metclmt[y][s]["snow"]),1)
        metclmt[y]["snowPROP"]["day_max"][1].extend(metclmt[y][m][d] for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] for d in metclmt[y][m] if type(d) == int and metclmt[y][m][d].snowQ in ignoreflags and metclmt[y][m][d].snow not in ["","-9999","9999"] and round(float(metclmt[y][m][d].snow),1) == metclmt[y]["snowPROP"]["day_max"][0])
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["snowPROP"]["day_max"][1].extend(metclmt[y][m][d] for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] for d in metclmt[y][m] if type(d) == int and metclmt[y][m][d].snowQ in ignoreflags and metclmt[y][m][d].snow not in ["","-9999","9999"] and round(float(metclmt[y][m][d].snow),1) == metclmt[y][s]["snowPROP"]["day_max"][0])
        metclmt[y]["snowPROP"]["month_max"][0] = round(max(sum(metclmt[y][m]["snow"]) for m in metclmt[y] if type(m) == int),1)
        for s in ["spring","summer","fall","winter"]: 
            try: metclmt[y][s]["snowPROP"]["month_max"][0] = round(max(sum(metclmt[y][m]["snow"]) for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"]),1)
            except: pass #print(y,s,m,[M for M in metclmt[y] if type(M) == int])
        metclmt[y]["snowPROP"]["month_max"][1].extend(m for m in metclmt[y] if type(m) == int and round(sum(metclmt[y][m]["snow"]),1) == metclmt[y]["snowPROP"]["month_max"][0])
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["snowPROP"]["month_max"][1].extend(m for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] and round(sum(metclmt[y][m]["snow"]),1) == metclmt[y][s]["snowPROP"]["month_max"][0])
        # SNWD
        metclmt[y]["snwd"] = []
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["snwd"] = []
        metclmt[y]["snwd"].extend(r for m in metclmt[y].keys() if type(m) == int for r in metclmt[y][m]["snwd"])
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["snwd"].extend(r for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] for r in metclmt[y][m]["snwd"])
        metclmt[y]["snwdDAYS"] = sum(metclmt[y][m]["snwdDAYS"] for m in metclmt[y] if type(m) == int)
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["snwdDAYS"] = sum(metclmt[y][m]["snwdDAYS"] for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"])
        #metclmt[y]["snwdDAYS"] = sum(metclmt[y][m]["snwdDAYS"] for m in metclmt[y] if type(m) == int)
        #for s in ["spring","summer","fall","winter"]: metclmt[y][s]["snwdDAYS"] = sum(metclmt[y][m]["snwdDAYS"] for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"])
        #metclmt[y]["snwdPROP"] = {"day_max":[-1,[]],"month_max":[-1,[]]}
        metclmt[y]["snwdPROP"] = {"day_max":[-1,[]]}
        #for s in ["spring","summer","fall","winter"]: metclmt[y][s]["snwdPROP"] = {"day_max":[-1,[]],"month_max":[-1,[]]}
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["snwdPROP"] = {"day_max":[-1,[]]}
        if len(metclmt[y]["snwd"]) > 0: metclmt[y]["snwdPROP"]["day_max"][0] = round(max(metclmt[y]["snwd"]),1)
        for s in ["spring","summer","fall","winter"]:
            if len(metclmt[y][s]["snwd"]) > 0: metclmt[y][s]["snwdPROP"]["day_max"][0] = round(max(metclmt[y][s]["snwd"]),1)
        metclmt[y]["snwdPROP"]["day_max"][1].extend(metclmt[y][m][d] for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] for d in metclmt[y][m] if type(d) == int and metclmt[y][m][d].snwdQ in ignoreflags and metclmt[y][m][d].snwd not in ["","-9999","9999"] and round(float(metclmt[y][m][d].snwd),1) == metclmt[y]["snwdPROP"]["day_max"][0])
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["snwdPROP"]["day_max"][1].extend(metclmt[y][m][d] for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] for d in metclmt[y][m] if type(d) == int and metclmt[y][m][d].snwdQ in ignoreflags and metclmt[y][m][d].snwd not in ["","-9999","9999"] and round(float(metclmt[y][m][d].snwd),1) == metclmt[y][s]["snwdPROP"]["day_max"][0])
        #metclmt[y]["snwdPROP"]["month_max"][0] = round(max(sum(metclmt[y][m]["snwd"]) for m in metclmt[y] if type(m) == int),1)
        #for s in ["spring","summer","fall","winter"]: 
            #try: metclmt[y][s]["snwdPROP"]["month_max"][0] = round(max(sum(metclmt[y][m]["snwd"]) for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"]),2)
            #except: pass #print(y,s,m,[M for M in metclmt[y] if type(M) == int])
        #metclmt[y]["snwdPROP"]["month_max"][1].extend(m for m in metclmt[y] if type(m) == int and round(sum(metclmt[y][m]["snwd"]),2) == metclmt[y]["snwdPROP"]["month_max"][0])
        #for s in ["spring","summer","fall","winter"]: metclmt[y][s]["snwdPROP"]["month_max"][1].extend(m for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] and round(sum(metclmt[y][m]["snwd"]),2) == metclmt[y][s]["snwdPROP"]["month_max"][0])
        # TAVG
        metclmt[y]["tempAVGlist"] = []
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["tempAVGlist"] = []
        metclmt[y]["tempAVGlist"].extend(ta for m in metclmt[y].keys() if type(m) == int for ta in metclmt[y][m]["tempAVGlist"])
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["tempAVGlist"].extend(ta for m in metclmt[y].keys() if type(m) == int and m in metclmt[y][s]["valid"] for ta in metclmt[y][m]["tempAVGlist"])
        # TMAX
        metclmt[y]["tmax"] = []
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["tmax"] = []
        metclmt[y]["tmax"].extend(tx for m in metclmt[y].keys() if type(m) == int for tx in metclmt[y][m]["tmax"])
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["tmax"].extend(tx for m in metclmt[y].keys() if type(m) == int and m in metclmt[y][s]["valid"] for tx in metclmt[y][m]["tmax"])
        metclmt[y]["tmaxPROP"] = {"day_max":[-999,[]],"day_min":[999,[]],"month_AVG_max":[-999,[]],"month_AVG_min":[999,[]]}
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["tmaxPROP"] = {"day_max":[-999,[]],"day_min":[999,[]],"month_AVG_max":[-999,[]],"month_AVG_min":[999,[]]}
        if len(metclmt[y]["tmax"]) > 0: 
            metclmt[y]["tmaxPROP"]["day_max"][0] = max(metclmt[y]["tmax"])
            for s in ["spring","summer","fall","winter"]: 
                try: metclmt[y][s]["tmaxPROP"]["day_max"][0] = max(metclmt[y][s]["tmax"])
                except: pass #print(y,s,m,[M for M in metclmt[y] if type(M) == int])
            metclmt[y]["tmaxPROP"]["day_max"][1].extend(metclmt[y][m][d] for m in metclmt[y] if type(m) == int for d in metclmt[y][m] if type(d) == int and metclmt[y][m][d].tmaxQ in ignoreflags and metclmt[y][m][d].tmax not in ["","-9999","9999"] and int(metclmt[y][m][d].tmax) == metclmt[y]["tmaxPROP"]["day_max"][0])
            for s in ["spring","summer","fall","winter"]: metclmt[y][s]["tmaxPROP"]["day_max"][1].extend(metclmt[y][m][d] for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] for d in metclmt[y][m] if type(d) == int and metclmt[y][m][d].tmaxQ in ignoreflags and metclmt[y][m][d].tmax not in ["","-9999","9999"] and int(metclmt[y][m][d].tmax) == metclmt[y][s]["tmaxPROP"]["day_max"][0])
            metclmt[y]["tmaxPROP"]["day_min"][0] = min(metclmt[y]["tmax"])
            for s in ["spring","summer","fall","winter"]: 
                try: metclmt[y][s]["tmaxPROP"]["day_min"][0] = min(metclmt[y][s]["tmax"])
                except: pass #print(y,s,m,[M for M in metclmt[y] if type(M) == int])
            metclmt[y]["tmaxPROP"]["day_min"][1].extend(metclmt[y][m][d] for m in metclmt[y] if type(m) == int for d in metclmt[y][m] if type(d) == int and metclmt[y][m][d].tmaxQ in ignoreflags and metclmt[y][m][d].tmax not in ["","-9999","9999"] and int(metclmt[y][m][d].tmax) == metclmt[y]["tmaxPROP"]["day_min"][0])
            for s in ["spring","summer","fall","winter"]: metclmt[y][s]["tmaxPROP"]["day_min"][1].extend(metclmt[y][m][d] for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] for d in metclmt[y][m] if type(d) == int and metclmt[y][m][d].tmaxQ in ignoreflags and metclmt[y][m][d].tmax not in ["","-9999","9999"] and int(metclmt[y][m][d].tmax) == metclmt[y][s]["tmaxPROP"]["day_min"][0])
            if any(len(metclmt[y][M]["tmax"]) > excludemonth for M in metclmt[y] if type(M) == int):
                metclmt[y]["tmaxPROP"]["month_AVG_max"][0] = round(max(mean(metclmt[y][m]["tmax"]) for m in metclmt[y] if type(m) == int and len(metclmt[y][m]["tmax"]) > excludemonth),1)
                metclmt[y]["tmaxPROP"]["month_AVG_max"][1].extend(m for m in metclmt[y] if type(m) == int and len(metclmt[y][m]["tmax"]) > excludemonth and round(mean(metclmt[y][m]["tmax"]),1) == metclmt[y]["tmaxPROP"]["month_AVG_max"][0])
                for s in ["spring","summer","fall","winter"]: metclmt[y][s]["tmaxPROP"]["month_AVG_max"][1].extend(m for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] and len(metclmt[y][m]["tmax"]) > excludemonth and round(mean(metclmt[y][m]["tmax"]),1) == metclmt[y][s]["tmaxPROP"]["month_AVG_max"][0])
                metclmt[y]["tmaxPROP"]["month_AVG_min"][0] = round(min(mean(metclmt[y][m]["tmax"]) for m in metclmt[y] if type(m) == int and len(metclmt[y][m]["tmax"]) > excludemonth),1)
                metclmt[y]["tmaxPROP"]["month_AVG_min"][1].extend(m for m in metclmt[y] if type(m) == int and len(metclmt[y][m]["tmax"]) > excludemonth and round(mean(metclmt[y][m]["tmax"]),1) == metclmt[y]["tmaxPROP"]["month_AVG_min"][0])
                for s in ["spring","summer","fall","winter"]: metclmt[y][s]["tmaxPROP"]["month_AVG_min"][1].extend(m for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] and len(metclmt[y][m]["tmax"]) > excludemonth and round(mean(metclmt[y][m]["tmax"]),1) == metclmt[y][s]["tmaxPROP"]["month_AVG_min"][0])
            for s in ["spring","summer","fall","winter"]: 
                try:metclmt[y][s]["tmaxPROP"]["month_AVG_max"][0] = round(max(mean(metclmt[y][m]["tmax"]) for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] and len(metclmt[y][m]["tmax"]) > excludemonth),1)
                except: pass #print(y,s,m,[M for M in metclmt[y] if type(M) == int])
            for s in ["spring","summer","fall","winter"]: 
                try: metclmt[y][s]["tmaxPROP"]["month_AVG_min"][0] = round(min(mean(metclmt[y][m]["tmax"]) for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] and len(metclmt[y][m]["tmax"]) > excludemonth),1)
                except: pass #print(y,s,m,[M for M in metclmt[y] if type(M) == int])

        # TMIN
        metclmt[y]["tmin"] = []
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["tmin"] = []
        metclmt[y]["tmin"].extend(tx for m in metclmt[y].keys() if type(m) == int for tx in metclmt[y][m]["tmin"])
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["tmin"].extend(tx for m in metclmt[y].keys() if type(m) == int and m in metclmt[y][s]["valid"] for tx in metclmt[y][m]["tmin"])
        metclmt[y]["tminPROP"] = {"day_max":[-999,[]],"day_min":[999,[]],"month_AVG_max":[-999,[]],"month_AVG_min":[999,[]]}
        for s in ["spring","summer","fall","winter"]: metclmt[y][s]["tminPROP"] = {"day_max":[-999,[]],"day_min":[999,[]],"month_AVG_max":[-999,[]],"month_AVG_min":[999,[]]}
        if len(metclmt[y]["tmin"]) > 0:
            metclmt[y]["tminPROP"]["day_max"][0] = max(metclmt[y]["tmin"])
            for s in ["spring","summer","fall","winter"]: 
                try: metclmt[y][s]["tminPROP"]["day_max"][0] = max(metclmt[y][s]["tmin"])
                except: pass #print(y,s,m,[M for M in metclmt[y] if type(M) == int])
            metclmt[y]["tminPROP"]["day_max"][1].extend(metclmt[y][m][d] for m in metclmt[y] if type(m) == int for d in metclmt[y][m] if type(d) == int and metclmt[y][m][d].tminQ in ignoreflags and metclmt[y][m][d].tmin not in ["","-9999","9999"] and int(metclmt[y][m][d].tmin) == metclmt[y]["tminPROP"]["day_max"][0])
            for s in ["spring","summer","fall","winter"]: metclmt[y][s]["tminPROP"]["day_max"][1].extend(metclmt[y][m][d] for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] for d in metclmt[y][m] if type(d) == int and metclmt[y][m][d].tminQ in ignoreflags and metclmt[y][m][d].tmin not in ["","-9999","9999"] and int(metclmt[y][m][d].tmin) == metclmt[y][s]["tminPROP"]["day_max"][0])
            metclmt[y]["tminPROP"]["day_min"][0] = min(metclmt[y]["tmin"])
            for s in ["spring","summer","fall","winter"]: 
                try: metclmt[y][s]["tminPROP"]["day_min"][0] = min(metclmt[y][s]["tmin"])
                except: pass #print(y,s,m,[M for M in metclmt[y] if type(M) == int])
            metclmt[y]["tminPROP"]["day_min"][1].extend(metclmt[y][m][d] for m in metclmt[y] if type(m) == int for d in metclmt[y][m] if type(d) == int and metclmt[y][m][d].tminQ in ignoreflags and metclmt[y][m][d].tmin not in ["","-9999","9999"] and int(metclmt[y][m][d].tmin) == metclmt[y]["tminPROP"]["day_min"][0])
            for s in ["spring","summer","fall","winter"]: metclmt[y][s]["tminPROP"]["day_min"][1].extend(metclmt[y][m][d] for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] for d in metclmt[y][m] if type(d) == int and metclmt[y][m][d].tminQ in ignoreflags and metclmt[y][m][d].tmin not in ["","-9999","9999"] and int(metclmt[y][m][d].tmin) == metclmt[y][s]["tminPROP"]["day_min"][0])
            if any(len(metclmt[y][M]["tmin"]) > excludemonth for M in metclmt[y] if type(M) == int):
                metclmt[y]["tminPROP"]["month_AVG_max"][0] = round(max(mean(metclmt[y][m]["tmin"]) for m in metclmt[y] if type(m) == int and len(metclmt[y][m]["tmin"]) > excludemonth),1)
                metclmt[y]["tminPROP"]["month_AVG_max"][1].extend(m for m in metclmt[y] if type(m) == int and len(metclmt[y][m]["tmin"]) > excludemonth and round(mean(metclmt[y][m]["tmin"]),1) == metclmt[y]["tminPROP"]["month_AVG_max"][0])
                for s in ["spring","summer","fall","winter"]: metclmt[y][s]["tminPROP"]["month_AVG_max"][1].extend(m for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] and len(metclmt[y][m]["tmin"]) > excludemonth and round(mean(metclmt[y][m]["tmin"]),1) == metclmt[y][s]["tminPROP"]["month_AVG_max"][0])
                metclmt[y]["tminPROP"]["month_AVG_min"][0] = round(min(mean(metclmt[y][m]["tmin"]) for m in metclmt[y] if type(m) == int and len(metclmt[y][m]["tmin"]) > excludemonth),1)
                metclmt[y]["tminPROP"]["month_AVG_min"][1].extend(m for m in metclmt[y] if type(m) == int and len(metclmt[y][m]["tmin"]) > excludemonth and round(mean(metclmt[y][m]["tmin"]),1) == metclmt[y]["tminPROP"]["month_AVG_min"][0])
                for s in ["spring","summer","fall","winter"]: metclmt[y][s]["tminPROP"]["month_AVG_min"][1].extend(m for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] and len(metclmt[y][m]["tmin"]) > excludemonth and round(mean(metclmt[y][m]["tmin"]),1) == metclmt[y][s]["tminPROP"]["month_AVG_min"][0])
            for s in ["spring","summer","fall","winter"]: 
                try:metclmt[y][s]["tminPROP"]["month_AVG_max"][0] = round(max(mean(metclmt[y][m]["tmin"]) for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] and len(metclmt[y][m]["tmin"]) > excludemonth),1)
                except: pass #print(y,s,m,[M for M in metclmt[y] if type(M) == int])
            for s in ["spring","summer","fall","winter"]: 
                try: metclmt[y][s]["tminPROP"]["month_AVG_min"][0] = round(min(mean(metclmt[y][m]["tmin"]) for m in metclmt[y] if type(m) == int and m in metclmt[y][s]["valid"] and len(metclmt[y][m]["tmin"]) > excludemonth),1)
                except: pass #print(y,s,m,[M for M in metclmt[y] if type(M) == int])

    END = time()
    if len(station_ids) > 1:
        print("STATION: Multiple Stations")
        clmt["station"] = "{} Stations".format(len(station_ids))
    else: print("STATION: {}".format(clmt["station"]))
    print("*** SCRIPT COMPLETE ***")
    print("Runtime: {} seconds".format(round(END - START,2)))
    print("-------------------------------------------------------------------------------------")
    print(" For more detailed assistance, enter clmthelp() for a breakdown of available functions")
    print("-------------------------------------------------------------------------------------")

def attchk(attstr):
    """Not used by user; program uses it for output and 'filling in' of
    missing data"""
    try:
        M = attstr[0]       # Measurement Flag
    except:
        M = ""
    try:
        Q = attstr[1]       # Quality Flag
    except:
        Q = ""
    try:
        S = attstr[2]       # Source Flag
    except:
        S = ""
    try:
        T = attstr[3]       # Time of Observation
    except:
        T = ""

    return M,Q,S,T

def errorStats():
    """Returns a report on errors that might be worth veryfying the data for.
    
    errorStats()  -> report on possible-to-likely errors in the record; no
                     arguments passeds
    """
    #if "ignore" in ig: ignoreflags.append(ig["ignore"])
    #if "heed" in ig: ignoreflags.remove(ig["heed"])
    if len(clmt) == 0: return print("* OOPS! Run the clmtAnalyze function first.")
    total_records = 0
    errors = []
    nonIerrors = []
    prcp_errors = []
    snow_errors = []
    snwd_errors = []
    tmax_errors = []
    tmin_errors = []
    error_array = [prcp_errors,snow_errors,snwd_errors,tmax_errors,tmin_errors]
    misscounter = 0
    tmax_lt_tmin = []
    snow_gt_0prcp = []
    snwd_gt_snow = []

    for y in [year for year in clmt if type(year) == int]:
        for m in [month for month in clmt[y] if type(month) == int]:
            for d in [day for day in clmt[y][m] if type(day) == int]:
                total_records += 1
                if any(e != "" for e in [clmt[y][m][d].prcpQ,clmt[y][m][d].snowQ,clmt[y][m][d].snwdQ,clmt[y][m][d].tmaxQ,clmt[y][m][d].tminQ]):
                    errors.append(clmt[y][m][d])
                if clmt[y][m][d].prcpQ != "": prcp_errors.append(clmt[y][m][d])
                if clmt[y][m][d].snowQ != "": snow_errors.append(clmt[y][m][d])
                if clmt[y][m][d].snwdQ != "": snwd_errors.append(clmt[y][m][d])
                if clmt[y][m][d].tmaxQ != "": tmax_errors.append(clmt[y][m][d])
                if clmt[y][m][d].tminQ != "": tmin_errors.append(clmt[y][m][d])
                try:
                    if int(clmt[y][m][d].tmax) < int(clmt[y][m][d].tmin):
                        tmax_lt_tmin.append("Day: {}; TMAX: {}; TMIN: {}".format(clmt[y][m][d].daystr,clmt[y][m][d].tmax,clmt[y][m][d].tmin))
                except:
                    misscounter += 1
                try:
                    if float(clmt[y][m][d].snow) > 0 and float(clmt[y][m][d].prcp) == 0 and clmt[y][m][d].prcpM != "T":
                        snow_gt_0prcp.append("Day: {}; PRCP: {} - {} :: SNOW: {} - {}".format(clmt[y][m][d].daystr,clmt[y][m][d].prcp,clmt[y][m][d].prcpQ if clmt[y][m][d].prcpQ != "" else " ",clmt[y][m][d].snow,clmt[y][m][d].snowQ if clmt[y][m][d].snowQ != "" else " "))
                except:
                    continue

    print("Total Dates with at least 1 Quality Flag: {}; % of Total Days: {}%".format(len(errors),round(len(errors)/total_records*100,2)))
    for x in range(len(error_array)):
        if x == 0: print("PRCP ERRORS:")
        if x == 1: print("SNOW ERRORS:")
        if x == 2: print("SNWD ERRORS:")
        if x == 3: print("TMAX ERRORS (Non-I):")
        if x == 4: print("TMIN ERRORS (Non-I):")
        for y in error_array[x]:
            if x == 0:
                if y.prcpQ not in [i for i in ignoreflags if i != "I"] or y.prcp in ["9999","-9999"]:
                    print("Day: {}; PRCP: {}; Quality Flag (prcpQ): {} - {}".format(y.daystr,y.prcp,y.prcpQ,qflagCheck(y.prcpQ)))
            if x == 1:
                if y.snowQ not in [i for i in ignoreflags if i != "I"] or y.snow in ["9999","-9999"]:
                    print("Day: {}; SNOW: {}; Quality Flag (snowQ): {} - {}".format(y.daystr,y.snow,y.snowQ,qflagCheck(y.snowQ)))
            if x == 2:
                if y.snwdQ not in ignoreflags or y.snwd in ["9999","-9999"]:
                    print("Day: {}; SNWD: {}; Quality Flag (snwdQ): {} - {}".format(y.daystr,y.snwd,y.snwdQ,qflagCheck(y.snwdQ)))
            if x == 3:
                if y.tmaxQ not in ignoreflags and y.tmaxQ != "I" or y.tmax in ["9999","-9999"]:
                    print("Day: {}; TMAX: {}; Quality Flag (tmaxQ): {} - {}".format(y.daystr,y.tmax,y.tmaxQ,qflagCheck(y.tmaxQ)))
            if x == 4:
                if y.tminQ not in ignoreflags and y.tminQ != "I" or y.tmax in ["9999","-9999"]:
                    print("Day: {}; TMIN: {}; Quality Flag (tminQ): {} - {}".format(y.daystr,y.tmin,y.tminQ,qflagCheck(y.tminQ)))

    print("---------------------------")
    print("TOTAL DAYS where tmax and/or tmin is missing: {}".format(misscounter))
    if len(tmax_lt_tmin) > 0:
        print("DAYS WHERE TMIN > TMAX:")
        for x in tmax_lt_tmin:
            print(x)
    if len(snow_gt_0prcp) > 0:
        print("----------------------------")
        print("DAYS WHERE PRCP == 0 (with no trace recorded) and SNOW > 0:")
        for x in snow_gt_0prcp:
            print(x)
    print("")

def checkDate(*args):
    """Used only by the program"""
    if len(args) == 3:
        y = args[0]
        m = args[1]
        d = args[2]
        try:
            if clmt[y][m][d]: return True
        except KeyError:
            print("OOPS! An entry for {}-{}-{} was not found. Try again.".format(str(y).zfill(4),str(m).zfill(2)[0:2],str(d).zfill(2)[0:2]))
            if d > y or m > y:
                print("*** Ensure your entry matches the format of dayStats(year,month,day) ***")
            return False
    elif len(args) == 2:
        y = args[0]
        m = args[1]
        try:
            if clmt[y][m]: return True
        except KeyError:
            try:
                print("OOPS! An entry for {} {} was not found. Try again.".format(calendar.month_name[m],y))
                if m > y:
                    print("*** Ensure your entry matches the format of monthStats(year,month) ***")
            except:
                print("OOPS! A likely invalid month entry. Ensure format of monthStats(year,month). Try again.")
            return False
    elif len(args) == 1:
        y = args[0]
        try:
            if clmt[y]: return True
        except KeyError:
            print("OOPS! An entry for {} was not found. Try again.".format(y))
            return False
    else:
        print("OOPS! No date input received! Try again!")

def checkDate2(*args):
    """Used only by the program in functions that check but don't return a true/false message"""
    y = args[0]
    m = args[1]
    d = args[2]
    try:
        if clmt[y][m][d]: return True
    except KeyError:
        return False

def rank(n):
    if n <= 0 or type(n) != int: return ""
    elif n < 10 or int(str(n)[-2:]) not in [11,12,13]:
        if int(str(n)[-1:]) == 1: return str(n) + "st"
        elif int(str(n)[-1:]) == 2: return str(n) + "nd"
        elif int(str(n)[-1:]) == 3: return str(n) + "rd"
        else: return str(n) + "th"
    elif int(str(n)[-2:]) in [11,12,13]: return str(n) + "th"

def qflagCheck(*q):
    """Primarily used internally by the program. Can return definitions of
    Quality Flags. These are used to denote data that may not be reliable.
    
    qflagCheck(*[str]) -> str
    
    OPTIONAL args: "F" -> will return the definition of a flag by that one-
                          letter string
    """
    if len(q) != 0:
        if q[0] == "D": return "Failed (D)uplicate Check"
        if q[0] == "G": return "Failed (G)ap Check"
        if q[0] == "I": return "Failed (I)nternal Consistency Check"
        if q[0] == "K": return "Failed Strea(K)/Frequent-Value Check"
        if q[0] == "L": return "Failed Check on (L)ength of Multi-day period"
        if q[0] == "M": return "Failed (M)ega-Consistency Check"
        if q[0] == "N": return "Failed (N)aught Check"
        if q[0] == "O": return "Failed Climatological (O)utlier Check"
        if q[0] == "R": return "Failed Lagged (R)ange Check"
        if q[0] == "S": return "Failed (S)patial Consistency Check"
        if q[0] == "T": return "Failed (T)emporal Consistency Check"
        if q[0] == "W": return "Temperature Too (W)arm for Snow"
        if q[0] == "X": return "Failed Bounds Check"
        if q[0] == "Z": return "Flagged as a result of an official Datzilla Investigation"
        else: return "None/Not-Documented"
    else:
        print("D - Failed (D)uplicate Check")
        print("G - Failed (G)ap Check")
        print("I - Failed (I)nternal Consistency Check")
        print("K - Failed Strea(K)/Frequent-Value Check")
        print("L - Failed Check on (L)ength of Multi-day period")
        print("M - Failed (M)ega-Consistency Check")
        print("N - Failed (N)aught Check")
        print("O - Failed Climatological (O)utlier Check")
        print("R - Failed Lagged (R)ange Check")
        print("S - Failed (S)patial Consistency Check")
        print("T - Failed (T)emporal Consistency Check")
        print("W - Temperature Too (W)arm for Snow")
        print("X - Failed Bounds Check")
        print("Z - Flagged as a result of an official Datzilla Investigation")

def daySummary(y1,m1,d1,*date2):
    """Quickly list all specific daily data between two dates. The 2nd date
    is optional. If none is provided, December 31 of y1 will be used as the
    stop date.
    
    daySummary(y1,m1,d1,*[y2,m2,d2])
    
    EXAMPLE: daySummary(2016,10,1,2016,10,31) -> Lists daily summaries for
                                                 dates between 1 OCT 2016
                                                 and 31 OCT 2016

    EXAMPLE: daySummary(1980,11,1) -> Lists daily summaries for dates between
                                      1 NOV 1980 and 31 DEC 1980
    """
    if any(type(x) != int for x in [y1,m1,d1]): return print("*** OOPS! Error in Date #1. Ensure that only integers are entered ***")
    #valid1 = checkDate(y1,m1,d1)
    if len(date2) == 0:
        if y1 == max(Y for Y in clmt if type(Y) == int):
            y2 = y1
            m2 = max(M for M in clmt[y2] if type(M) == int)
            d2 = max(D for D in clmt[y2][m2] if type(D) == int)
        else: y2 = y1; m2 = 12; d2 = 31
    elif len(date2) != 3: return print("*** OOPS! For the 2nd (optional) date, ensure a Year, Month and Date are entered ***")
    else:
        if any(type(x) != int for x in [date2[0],date2[1],date2[2]]): return print("*** OOPS! Error in Date #2. Ensure that only integers are entered ***")
        #valid2 = checkDate(date2[0],date2[1],date2[2])
        y2 = date2[0]; m2 = date2[1]; d2 = date2[2]
    
    # Further inspection of Day 1
    if y1 not in clmt: return print("OOPS! Regarding Date #1, no yearly-data found for {}. The earliest year is {}.".format(y1,min(Y for Y in clmt if type(Y) == int)))
    if m1 not in range(1,12+1): return print("OOPS! Regarding Date #1, ensure the month is in the range [1,12]. Try again!")
    daysinmonth = max(D for Y in clmt if type(Y) == int and m1 in clmt[Y] for D in clmt[Y][m1] if type(D) == int)
    if d1 not in range(1,daysinmonth+1): return print("OOPS! Regarding Date #1, ensure the day is in the range [1,{}]. Try again!".format(daysinmonth))
    if m1 == 2 and d1 == 29 and calendar.isleap(y1) == False: print("OOPS! Date #1 does not occur. It's not during a leap year. Try again!")
    # Furthur inspection of Day 2
    if y2 not in clmt: return print("OOPS! Regarding Date #2, no yearly-data found for {}. The earliest year is {}.".format(y2,min(Y for Y in clmt if type(Y) == int)))
    if m2 not in range(1,12+1): return print("OOPS! Regarding Date #2, ensure the month is in the range [1,12]. Try again!")
    daysinmonth = max(D for Y in clmt if type(Y) == int and m2 in clmt[Y] for D in clmt[Y][m2] if type(D) == int)
    if d2 not in range(1,daysinmonth+1): return print("OOPS! Regarding Date #2, ensure the day is in the range [1,{}]. Try again!".format(daysinmonth))
    if m2 == 2 and d2 == 29 and calendar.isleap(y2) == False: print("OOPS! Date #2 does not occur. It's not during a leap year. Try again!")

    startday = datetime.date(y1,m1,d1)
    endday = datetime.date(y2,m2,d2)

    if startday == endday: return print("OOPS! Start and End dates are the exact same; please ensure otherwise! Try again!")
    if endday < startday: return print("OOPS! End date is sooner than the start date. Try again!")

    incrday = startday
    print("")
    #print(f"Day Summaries from {str(d1).zfill(2)} {calendar.month_abbr[m1].upper()} {y1} to {str(d2).zfill(2)} {calendar.month_abbr[m2].upper()} {y2}")
    print("{:^88}".format("Day Summaries from {} {} {} to {} {} {}".format(str(d1).zfill(2),calendar.month_abbr[m1].upper(),y1,str(d2).zfill(2),calendar.month_abbr[m2].upper(),y2)))
    print("{:^88}".format("{}: {}".format(clmt["station"],clmt["station_name"])))
    print("{:^88}".format("{:-^45}".format("")))
    while incrday <= endday:    #        {      
        try: print(" {}: PRCP: {:>5}{:3}; SNOW: {:>4}{:3}; SNWD: {:>4}{:3}; TMAX: {:>3}{:3}; TMIN: {:>3}{:3};".format(
            clmt[incrday.year][incrday.month][incrday.day].daystr,
            "{:>5.2f}".format(float(clmt[incrday.year][incrday.month][incrday.day].prcp)) if clmt[incrday.year][incrday.month][incrday.day].prcp != "" else "",
            "{} {}".format(
                clmt[incrday.year][incrday.month][incrday.day].prcpM if clmt[incrday.year][incrday.month][incrday.day].prcpM == "T" else "",
                clmt[incrday.year][incrday.month][incrday.day].prcpQ if clmt[incrday.year][incrday.month][incrday.day].prcpQ != "" else ""),

            "{:>4.1f}".format(float(clmt[incrday.year][incrday.month][incrday.day].snow)) if (clmt[incrday.year][incrday.month][incrday.day].snow != "" and float(clmt[incrday.year][incrday.month][incrday.day].snow) != 0) or (clmt[incrday.year][incrday.month][incrday.day].snow != "" and clmt[incrday.year][incrday.month][incrday.day].snowM == "T") else "----",
            "{} {} ".format(
                clmt[incrday.year][incrday.month][incrday.day].snowM if clmt[incrday.year][incrday.month][incrday.day].snowM == "T" else "",
                clmt[incrday.year][incrday.month][incrday.day].snowQ if clmt[incrday.year][incrday.month][incrday.day].snowQ != "" else ""),

            "{:>4.1f}".format(float(clmt[incrday.year][incrday.month][incrday.day].snwd)) if (clmt[incrday.year][incrday.month][incrday.day].snwd != "" and float(clmt[incrday.year][incrday.month][incrday.day].snwd) != 0) or (clmt[incrday.year][incrday.month][incrday.day].snwd != "" and clmt[incrday.year][incrday.month][incrday.day].snwdM == "T") else "----",
            "{} {} ".format(
                clmt[incrday.year][incrday.month][incrday.day].snwdM if clmt[incrday.year][incrday.month][incrday.day].snwdM == "T" else "",
                clmt[incrday.year][incrday.month][incrday.day].snwdQ if clmt[incrday.year][incrday.month][incrday.day].snwdQ != "" else ""),

            clmt[incrday.year][incrday.month][incrday.day].tmax,
            " {} ".format(clmt[incrday.year][incrday.month][incrday.day].tmaxQ) if clmt[incrday.year][incrday.month][incrday.day].tmaxQ != "" else "",
            clmt[incrday.year][incrday.month][incrday.day].tmin,
            " {} ".format(clmt[incrday.year][incrday.month][incrday.day].tminQ) if clmt[incrday.year][incrday.month][incrday.day].tminQ != "" else ""
            ))
        except: print(" *** NO ENTRY DATA FOUND FOR {}-{}-{} ***".format(incrday.year,incrday.month,incrday.day))
        incrday += datetime.timedelta(days=1)
    print("")

def dayStats(y,m,d):
    """Report on recorded statistics for the day of interest. Passed arguments
    MUST be integers.
    
    dayStats(year,month,day)   
    
    EXAMPLE: dayStats(1992,12,29) -> Returns a printout of statistics from
                                     December 29, 1992
    """
    ranks = ["th","st","nd","rd","th","th","th","th","th","th"]
    if len(clmt) == 0: return print("* OOPS! Run the clmtAnalyze function first.")
    dayExists = checkDate(y,m,d)
    
    if dayExists:
        print("")
        dayobj = clmt[y][m][d]
        prcphist = sorted(list(set(list(round(float(clmt[Y][m][d].prcp),2) for Y in clmt if type(Y) == int and m in clmt[Y] and d in clmt[Y][m] and clmt[Y][m][d].prcp != "" and float(clmt[Y][m][d].prcp) != 0 and clmt[Y][m][d].prcpQ in ignoreflags))),reverse=True)
        snowhist = sorted(list(set(list(round(float(clmt[Y][m][d].snow),1) for Y in clmt if type(Y) == int and m in clmt[Y] and d in clmt[Y][m] and clmt[Y][m][d].snow != "" and float(clmt[Y][m][d].snow) != 0 and clmt[Y][m][d].snowQ in ignoreflags))),reverse=True)
        snwdhist = sorted(list(set(list(round(float(clmt[Y][m][d].snwd),1) for Y in clmt if type(Y) == int and m in clmt[Y] and d in clmt[Y][m] and clmt[Y][m][d].snwd != "" and float(clmt[Y][m][d].snwd) != 0 and clmt[Y][m][d].snwdQ in ignoreflags))),reverse=True)
        tmaxdeschist = sorted(list(set(list(int(clmt[Y][m][d].tmax) for Y in clmt if type(Y) == int and m in clmt[Y] and d in clmt[Y][m] and clmt[Y][m][d].tmax != "" and clmt[Y][m][d].tmaxQ == ""))),reverse=True)
        tmaxaschist = sorted(list(set(list(int(clmt[Y][m][d].tmax) for Y in clmt if type(Y) == int and m in clmt[Y] and d in clmt[Y][m] and clmt[Y][m][d].tmax != "" and clmt[Y][m][d].tmaxQ == ""))))
        tmindeschist = sorted(list(set(list(int(clmt[Y][m][d].tmin) for Y in clmt if type(Y) == int and m in clmt[Y] and d in clmt[Y][m] and clmt[Y][m][d].tmin != "" and clmt[Y][m][d].tminQ == ""))),reverse=True)
        tminaschist = sorted(list(set(list(int(clmt[Y][m][d].tmin) for Y in clmt if type(Y) == int and m in clmt[Y] and d in clmt[Y][m] and clmt[Y][m][d].tmin != "" and clmt[Y][m][d].tminQ == ""))))

        #clmt_vars_days = {"prcp":{},"snow":{},"snwd":{},"tavg":{},"tmax":{},"tmin":{}}
        tavgdeschist = sorted(list(set(list(V for V in clmt_vars_days["tavg"] for D in clmt_vars_days["tavg"][V] if D.month == m and D.day == d))),reverse=True)
        tavgaschist = sorted(list(set(list(V for V in clmt_vars_days["tavg"] for D in clmt_vars_days["tavg"][V] if D.month == m and D.day == d))))
        #sorted(list(set(list(round(float(clmt[Y][m][d].prcp),2) for Y in clmt if type(Y) == int and m in clmt[Y] and d in clmt[Y][m] and clmt[Y][m][d].prcp != "" and float(clmt[Y][m][d].prcp) != 0 and clmt[Y][m][d].prcpQ == ""))),reverse=True)
        print("Statistics for {}".format(dayobj.entryday))
        print("Report Location: {}, {}".format(dayobj.stationid,dayobj.station_name))
        print("-------------------")
        print("PRCP: {}{}{}".format("T" if dayobj.prcpM == "T" else dayobj.prcp,
                                    ", Flag: {} - {}".format(dayobj.prcpQ,qflagCheck(dayobj.prcpQ)) if dayobj.prcpQ != "" else "",
                                    # rank(tavgaschist.index(round(mean(clmt[y][m]["tempAVGlist"]),1))+1)
                                    ", Rank: {}".format(rank(prcphist.index(round(float(dayobj.prcp),2))+1)) if dayobj.prcp != "" and float(dayobj.prcp) != 0 else ""))
        if dayobj.snow != "" and float(dayobj.snow) > 0 or dayobj.snowM == "T":
            print("SNOW: {}{}{}".format("T" if dayobj.snowM == "T" else dayobj.snow,
                                        ", Flag: {} - {}".format(dayobj.snowQ,qflagCheck(dayobj.snowQ)) if dayobj.snowQ != "" else "",
                                        ", Rank: {}".format(rank(snowhist.index(round(float(dayobj.snow),1))+1)) if dayobj.snowQ in ignoreflags else ""))
        if dayobj.snwd != "" and float(dayobj.snwd) > 0:
            print("SNWD: {}{}{}".format("T" if dayobj.snwdM == "T" else dayobj.snwd,
                                        ", Flag: {} - {}".format(dayobj.snwdQ,qflagCheck(dayobj.snwdQ)) if dayobj.snwdQ != "" else "",
                                        ", Rank: {}".format(rank(snwdhist.index(round(float(dayobj.snwd),1))+1)) if dayobj.snwdQ in ignoreflags else ""))
        print("TAVG: {}{}{}".format(
            "{:4.1f}".format(round(mean([float(dayobj.tmax),float(dayobj.tmin)]),1)) if all(T != "" for T in [dayobj.tmax,dayobj.tmin]) and all(Q in ignoreflags for Q in [dayobj.tmaxQ,dayobj.tminQ]) else "N/A",
            ", Rank: {} Warmest".format(
                rank(tavgdeschist.index(round(mean([float(dayobj.tmax),float(dayobj.tmin)]),1))+1)) if all(T != "" for T in [dayobj.tmax,dayobj.tmin]) and all(Q in ignoreflags for Q in [dayobj.tmaxQ,dayobj.tminQ]) and tavgdeschist.index(round(mean([float(dayobj.tmax),float(dayobj.tmin)]),1)) <= tavgaschist.index(round(mean([float(dayobj.tmax),float(dayobj.tmin)]),1)) else "",
            ", Rank: {} Coolest".format(
                rank(tavgaschist.index(round(mean([float(dayobj.tmax),float(dayobj.tmin)]),1))+1)) if all(T != "" for T in [dayobj.tmax,dayobj.tmin]) and all(Q in ignoreflags for Q in [dayobj.tmaxQ,dayobj.tminQ]) and tavgaschist.index(round(mean([float(dayobj.tmax),float(dayobj.tmin)]),1)) <= tavgdeschist.index(round(mean([float(dayobj.tmax),float(dayobj.tmin)]),1)) else ""
            ))
        print("TMAX: {}{}{}{}".format(
            dayobj.tmax if dayobj.tmax != "" else "N/A",
            ", Flag: {} - {}".format(dayobj.tmaxQ,qflagCheck(dayobj.tmaxQ)) if dayobj.tmaxQ != "" else "",
            ", Rank: {} Warmest".format(rank(tmaxdeschist.index(int(dayobj.tmax))+1)) if dayobj.tmax != "" and dayobj.tmaxQ in ignoreflags and tmaxdeschist.index(int(dayobj.tmax)) <= tmaxaschist.index(int(dayobj.tmax)) else "",
            ", Rank: {} Coolest".format(rank(tmaxaschist.index(int(dayobj.tmax))+1)) if dayobj.tmax != "" and dayobj.tmaxQ in ignoreflags and tmaxaschist.index(int(dayobj.tmax)) <= tmaxdeschist.index(int(dayobj.tmax)) else ""
            ))
        print("TMIN: {}{}{}{}".format(
            dayobj.tmin if dayobj.tmin != "" else "N/A",
            ", Flag: {} - {}".format(dayobj.tminQ,qflagCheck(dayobj.tminQ)) if dayobj.tminQ != "" else "",
            ", Rank: {} Warmest".format(rank(tmindeschist.index(int(dayobj.tmin))+1)) if dayobj.tmin != "" and dayobj.tminQ in ignoreflags and tmindeschist.index(int(dayobj.tmin)) <= tminaschist.index(int(dayobj.tmin)) else "",
            ", Rank: {} Coolest".format(rank(tminaschist.index(int(dayobj.tmin))+1)) if dayobj.tmin != "" and dayobj.tminQ in ignoreflags and tminaschist.index(int(dayobj.tmin)) <= tmindeschist.index(int(dayobj.tmin)) else ""
            ))
        try:
            if int(dayobj.tmax) < int(dayobj.tmin): print("*** CHECK DATA: TMIN > TMAX ***")
        except:
            pass
        print("")

def weekStats(y,m,d):
    """Report on recorded statistics for a week of interest. The week will be
    centered on the day passed as an argument. Passed arguments MUST be
    integers. 

    weekStats(year,month,day)

    EXAMPLE: weekStats(1992,12,29) -> Returns a printout of weekly-based 
                                      statistics centered on December 29, 1992
                                      (The week would be inclusive 3 days
                                      before and after the date
    """
    if len(clmt) == 0: return print("* OOPS! Run the clmtAnalyze function first.")
    ranks = ["th","st","nd","rd","th","th","th","th","th","th"]
    if m == 2 and d == 29:
        m = 2; d = 28
    wkstart = datetime.date(y,m,d) - datetime.timedelta(days=3)
    c = wkstart
    wkend = datetime.date(y,m,d) + datetime.timedelta(days=3)
    #print(st)
    #print(datetime.date(y,m,d))
    #print(en)
    w_prcp = []
    w_prcpDAYS = 0
    w_snow = []
    w_snowDAYS = 0
    w_snwd = []
    w_tmax = []
    w_tmin = []
    w_alltemps = []
    records_in_week = 0
    weekExists = checkDate(y,m,d)
    indvweekdays = []
    if m == 2 and d == 29:
        m = 2; d = 28
    if weekExists:
        print("")
        for x in range(7):
            indvweekdays.append(c)
            try:
                #round(float(clmt[DY.year][DY.month][DY.day].prcp),2) for DY in indvweekdays if checkDate(DY.year,DY.month,DY.day) and clmt[DY.year][DY.month][DY.day].prcp != "" and clmt[DY.year][DY.month][DY.day].prcpQ in ignoreflags
                if clmt[c.year][c.month][c.day]: records_in_week += 1
                if clmt[c.year][c.month][c.day].prcpQ in ignoreflags and clmt[c.year][c.month][c.day].prcp not in ["9999","-9999",""]:
                    w_prcp.append(round(float(clmt[c.year][c.month][c.day].prcp),2))
                    if float(clmt[c.year][c.month][c.day].prcp) > 0 or clmt[c.year][c.month][c.day].prcpM == "T": w_prcpDAYS += 1
                if clmt[c.year][c.month][c.day].snowQ in ignoreflags and clmt[c.year][c.month][c.day].snow not in ["9999","-9999",""]:
                    w_snow.append(round(float(clmt[c.year][c.month][c.day].snow),1))
                    if float(clmt[c.year][c.month][c.day].snow) > 0 or clmt[c.year][c.month][c.day].snowM == "T": w_snowDAYS += 1
                if clmt[c.year][c.month][c.day].snwdQ in ignoreflags and clmt[c.year][c.month][c.day].snwd not in ["9999","-9999",""]:
                    w_snwd.append(round(float(clmt[c.year][c.month][c.day].snwd),1))
                if clmt[c.year][c.month][c.day].tmaxQ in ignoreflags and clmt[c.year][c.month][c.day].tmax not in ["9999","-9999",""]:
                    w_tmax.append(int(clmt[c.year][c.month][c.day].tmax))
                if clmt[c.year][c.month][c.day].tminQ in ignoreflags and clmt[c.year][c.month][c.day].tmin not in ["9999","-9999",""]:
                    w_tmin.append(int(clmt[c.year][c.month][c.day].tmin))
                if clmt[c.year][c.month][c.day].tmaxQ in ignoreflags and clmt[c.year][c.month][c.day].tmax not in ["9999","-9999",""] and clmt[c.year][c.month][c.day].tminQ in ignoreflags and clmt[c.year][c.month][c.day].tmin not in ["9999","-9999",""]:
                    w_alltemps.append(int(clmt[c.year][c.month][c.day].tmax))
                    w_alltemps.append(int(clmt[c.year][c.month][c.day].tmin))
            except KeyError:
                continue
            c += datetime.timedelta(days=1)
        # indvweekdays complete above
        # The following compiles all time data to display ranks in the output
        prcphist = []
        snowhist = []
        snwdhist = []
        tmaxaschist = []
        tmaxdeschist = []
        tminaschist = []
        tmindeschist = []
        tavgaschist = []
        tavgdeschist = []
        for YR in [YYYY for YYYY in clmt if type(YYYY) == int]:
            wc = datetime.date(YR,m,d)
            ws = wc - datetime.timedelta(days=3)
            wd = ws     # current day
            we = wc + datetime.timedelta(days=3)
            tempwkli = []
            # tempwkli = [datetime.date(2009,1,1),datetime.date(2009,1,2),datetime.date(2009,1,3),datetime.date(2009,1,4),datetime.date(2009,1,5),datetime.date(2009,1,6),datetime.date(2009,1,7)]
            while wd <= we:
                tempwkli.append(datetime.date(wd.year,wd.month,wd.day))
                wd = wd + datetime.timedelta(days=1)
            prcpwk = [float(clmt[wkday.year][wkday.month][wkday.day].prcp) for wkday in tempwkli if checkDate2(wkday.year,wkday.month,wkday.day) and clmt[wkday.year][wkday.month][wkday.day].prcp not in ["","-9999","9999","-999","999"] and clmt[wkday.year][wkday.month][wkday.day].prcpQ in ignoreflags]
            prcphist.append(round(sum(prcpwk),2))
            snowwk = [float(clmt[wkday.year][wkday.month][wkday.day].snow) for wkday in tempwkli if checkDate2(wkday.year,wkday.month,wkday.day) and clmt[wkday.year][wkday.month][wkday.day].snow not in ["","-9999","9999","-999","999"] and clmt[wkday.year][wkday.month][wkday.day].snowQ in ignoreflags]
            snowhist.append(round(sum(snowwk),1))
            snwdwk = [float(clmt[wkday.year][wkday.month][wkday.day].snwd) for wkday in tempwkli if checkDate2(wkday.year,wkday.month,wkday.day) and clmt[wkday.year][wkday.month][wkday.day].snwd not in ["","-9999","9999","-999","999"] and clmt[wkday.year][wkday.month][wkday.day].snwdQ in ignoreflags]
            if len(snwdwk) > 0: snwdhist.append(round(sum(snwdwk)/7,1))
            tmaxwk = [int(clmt[wkday.year][wkday.month][wkday.day].tmax) for wkday in tempwkli if checkDate2(wkday.year,wkday.month,wkday.day) and clmt[wkday.year][wkday.month][wkday.day].tmax not in ["","-9999","9999","-999","999"] and clmt[wkday.year][wkday.month][wkday.day].tmaxQ in ignoreflags]
            if len(tmaxwk) > excludeweek:
                tmaxaschist.append(round(mean(tmaxwk),1))
                tmaxdeschist.append(round(mean(tmaxwk),1))
            tminwk = [int(clmt[wkday.year][wkday.month][wkday.day].tmin) for wkday in tempwkli if checkDate2(wkday.year,wkday.month,wkday.day) and clmt[wkday.year][wkday.month][wkday.day].tmin not in ["","-9999","9999","-999","999"] and clmt[wkday.year][wkday.month][wkday.day].tminQ in ignoreflags]
            if len(tminwk) > excludeweek:
                tminaschist.append(round(mean(tminwk),1))
                tmindeschist.append(round(mean(tminwk),1))
            tavgwk = []
            for evd in tempwkli:
                if checkDate2(evd.year,evd.month,evd.day) and clmt[evd.year][evd.month][evd.day].tmax not in ["","-9999","9999","-999","999"] and clmt[evd.year][evd.month][evd.day].tmin not in ["","-9999","9999","-999","999"] and clmt[evd.year][evd.month][evd.day].tmaxQ in ignoreflags and clmt[evd.year][evd.month][evd.day].tminQ in ignoreflags:
                    tavgwk.append(int(clmt[evd.year][evd.month][evd.day].tmax))
                    tavgwk.append(int(clmt[evd.year][evd.month][evd.day].tmin))
            if len(tavgwk) > excludeweek * 2:
                tavgaschist.append(round(mean(tavgwk),1))
                tavgdeschist.append(round(mean(tavgwk),1))

            """
            print("{} - prcp: {} :: snow: {} :: snwd avg: {} :: tavg: {} :: tmax avg: {} :: tmin avg: {}".format(
                            YR,
                            "{:5.2f}".format(round(sum(prcpwk),2)),
                            "{:5.1f}".format(round(sum(snowwk),1)),
                            "{:5.1f}".format(round(mean(snwdwk),1)) if len(snwdwk) > 0 else "--",
                            "{:5.1f}".format(round(mean(tavgwk),1)) if len(tavgwk) > 0 else "--",
                            "{:5.1f}".format(round(mean(tmaxwk),1)) if len(tmaxwk) > 0 else "--",
                            "{:5.1f}".format(round(mean(tminwk),1)) if len(tminwk) > 0 else "--"))
            """

        prcphist = sorted(list(set(prcphist)),reverse=True)
        snowhist = sorted(list(set(snowhist)),reverse=True)
        snwdhist = sorted(list(set(snwdhist)),reverse=True)
        tmaxaschist = sorted(list(set(tmaxaschist)))
        tmaxdeschist = sorted(list(set(tmaxdeschist)),reverse=True)
        tminaschist = sorted(list(set(tminaschist)))
        tmindeschist = sorted(list(set(tmindeschist)),reverse=True)
        tavgaschist = sorted(list(set(tavgaschist)))
        tavgdeschist = sorted(list(set(tavgdeschist)),reverse=True)
        
        #for x in [prcphist,snowhist,snwdhist,tmaxaschist,tmaxdeschist,tminaschist,tmindeschist,tavgaschist,tavgdeschist]: print(x)

        if records_in_week <= excludeweek:
            print("")
            print("{:-^83}".format("*** WEEKLY STATS LIKELY UNDERREPRESENTED ***"))

        print("{:^83}".format("Weekly Statistics for {} thru {}".format(wkstart,wkend)))
        print("{:^83}".format("{}: {}".format(clmt["station"],clmt["station_name"])))
        print("{:^83}".format("Quantity of Records: {}".format(records_in_week)))
        print("{:^83}".format("'*' Denotes existance of quality flag; not included in average stats"))
        print("{:-^83}".format(""))
        
        print("{:^6}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}".format("",indvweekdays[0].year,indvweekdays[1].year,indvweekdays[2].year,indvweekdays[3].year,indvweekdays[4].year,indvweekdays[5].year,indvweekdays[6].year))
        print("{:^6}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}".format("",
                                                                        "{} {}".format(calendar.month_abbr[indvweekdays[0].month],indvweekdays[0].day),
                                                                        "{} {}".format(calendar.month_abbr[indvweekdays[1].month],indvweekdays[1].day),
                                                                        "{} {}".format(calendar.month_abbr[indvweekdays[2].month],indvweekdays[2].day),
                                                                        "{} {}".format(calendar.month_abbr[indvweekdays[3].month],indvweekdays[3].day),
                                                                        "{} {}".format(calendar.month_abbr[indvweekdays[4].month],indvweekdays[4].day),
                                                                        "{} {}".format(calendar.month_abbr[indvweekdays[5].month],indvweekdays[5].day),
                                                                        "{} {}".format(calendar.month_abbr[indvweekdays[6].month],indvweekdays[6].day)))
        print("{:-^6}|{:-^10}|{:-^10}|{:-^10}|{:-^10}|{:-^10}|{:-^10}|{:-^10}".format("","","","","","","",""))
        print("{:^6}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}".format("PRCP",
   "{}{}{}".format(
   clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].prcp if checkDate2(indvweekdays[0].year,indvweekdays[0].month,indvweekdays[0].day) and clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].prcp != "" else "M",
   clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].prcpM if checkDate2(indvweekdays[0].year,indvweekdays[0].month,indvweekdays[0].day) and clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].prcpM == "T" else "",
   "*" if checkDate2(indvweekdays[0].year,indvweekdays[0].month,indvweekdays[0].day) and clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].prcpQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].prcp if checkDate2(indvweekdays[1].year,indvweekdays[1].month,indvweekdays[1].day) and clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].prcp != "" else "M",
   clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].prcpM if checkDate2(indvweekdays[1].year,indvweekdays[1].month,indvweekdays[1].day) and clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].prcpM == "T" else "",
   "*" if checkDate2(indvweekdays[1].year,indvweekdays[1].month,indvweekdays[1].day) and clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].prcpQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].prcp if checkDate2(indvweekdays[2].year,indvweekdays[2].month,indvweekdays[2].day) and clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].prcp != "" else "M",
   clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].prcpM if checkDate2(indvweekdays[2].year,indvweekdays[2].month,indvweekdays[2].day) and clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].prcpM == "T" else "",
   "*" if checkDate2(indvweekdays[2].year,indvweekdays[2].month,indvweekdays[2].day) and clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].prcpQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].prcp if checkDate2(indvweekdays[3].year,indvweekdays[3].month,indvweekdays[3].day) and clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].prcp != "" else "M",
   clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].prcpM if checkDate2(indvweekdays[3].year,indvweekdays[3].month,indvweekdays[3].day) and clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].prcpM == "T" else "",
   "*" if checkDate2(indvweekdays[3].year,indvweekdays[3].month,indvweekdays[3].day) and clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].prcpQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].prcp if checkDate2(indvweekdays[4].year,indvweekdays[4].month,indvweekdays[4].day) and clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].prcp != "" else "M",
   clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].prcpM if checkDate2(indvweekdays[4].year,indvweekdays[4].month,indvweekdays[4].day) and clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].prcpM == "T" else "",
   "*" if checkDate2(indvweekdays[4].year,indvweekdays[4].month,indvweekdays[4].day) and clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].prcpQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].prcp if checkDate2(indvweekdays[5].year,indvweekdays[5].month,indvweekdays[5].day) and clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].prcp != "" else "M",
   clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].prcpM if checkDate2(indvweekdays[5].year,indvweekdays[5].month,indvweekdays[5].day) and clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].prcpM == "T" else "",
   "*" if checkDate2(indvweekdays[5].year,indvweekdays[5].month,indvweekdays[5].day) and clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].prcpQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].prcp if checkDate2(indvweekdays[6].year,indvweekdays[6].month,indvweekdays[6].day)  and clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].prcp != "" else "M",
   clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].prcpM if checkDate2(indvweekdays[6].year,indvweekdays[6].month,indvweekdays[6].day) and clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].prcpM == "T" else "",
   "*" if checkDate2(indvweekdays[6].year,indvweekdays[6].month,indvweekdays[6].day) and clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].prcpQ != "" else "")))
        print("{:^6}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}".format("SNOW",
   "{}{}{}".format(
   clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].snow if checkDate2(indvweekdays[0].year,indvweekdays[0].month,indvweekdays[0].day) else "M",
   clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].snowM if checkDate2(indvweekdays[0].year,indvweekdays[0].month,indvweekdays[0].day) and clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].snowM == "T" else "",
   "*" if checkDate2(indvweekdays[0].year,indvweekdays[0].month,indvweekdays[0].day) and clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].snowQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].snow if checkDate2(indvweekdays[1].year,indvweekdays[1].month,indvweekdays[1].day) else "M",
   clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].snowM if checkDate2(indvweekdays[1].year,indvweekdays[1].month,indvweekdays[1].day) and clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].snowM == "T" else "",
   "*" if checkDate2(indvweekdays[1].year,indvweekdays[1].month,indvweekdays[1].day) and clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].snowQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].snow if checkDate2(indvweekdays[2].year,indvweekdays[2].month,indvweekdays[2].day) else "M",
   clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].snowM if checkDate2(indvweekdays[2].year,indvweekdays[2].month,indvweekdays[2].day) and clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].snowM == "T" else "",
   "*" if checkDate2(indvweekdays[2].year,indvweekdays[2].month,indvweekdays[2].day) and clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].snowQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].snow if checkDate2(indvweekdays[3].year,indvweekdays[3].month,indvweekdays[3].day) else "M",
   clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].snowM if checkDate2(indvweekdays[3].year,indvweekdays[3].month,indvweekdays[3].day) and clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].snowM == "T" else "",
   "*" if checkDate2(indvweekdays[3].year,indvweekdays[3].month,indvweekdays[3].day) and clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].snowQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].snow if checkDate2(indvweekdays[4].year,indvweekdays[4].month,indvweekdays[4].day) else "M",
   clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].snowM if checkDate2(indvweekdays[4].year,indvweekdays[4].month,indvweekdays[4].day) and clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].snowM == "T" else "",
   "*" if checkDate2(indvweekdays[4].year,indvweekdays[4].month,indvweekdays[4].day) and clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].snowQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].snow if checkDate2(indvweekdays[5].year,indvweekdays[5].month,indvweekdays[5].day) else "M",
   clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].snowM if checkDate2(indvweekdays[5].year,indvweekdays[5].month,indvweekdays[5].day) and clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].snowM == "T" else "",
   "*" if checkDate2(indvweekdays[5].year,indvweekdays[5].month,indvweekdays[5].day) and clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].snowQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].snow if checkDate2(indvweekdays[6].year,indvweekdays[6].month,indvweekdays[6].day) else "M",
   clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].snowM if checkDate2(indvweekdays[6].year,indvweekdays[6].month,indvweekdays[6].day) and clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].snowM == "T" else "",
   "*" if checkDate2(indvweekdays[6].year,indvweekdays[6].month,indvweekdays[6].day) and clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].snowQ != "" else "")))
        print("{:^6}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}".format("SNWD",
   "{}{}{}".format(
   clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].snwd if checkDate2(indvweekdays[0].year,indvweekdays[0].month,indvweekdays[0].day) else "M",
   clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].snwdM if checkDate2(indvweekdays[0].year,indvweekdays[0].month,indvweekdays[0].day) and clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].snwdM == "T" else "",
   "*" if checkDate2(indvweekdays[0].year,indvweekdays[0].month,indvweekdays[0].day) and clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].snwdQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].snwd if checkDate2(indvweekdays[1].year,indvweekdays[1].month,indvweekdays[1].day) else "M",
   clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].snwdM if checkDate2(indvweekdays[1].year,indvweekdays[1].month,indvweekdays[1].day) and clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].snwdM == "T" else "",
   "*" if checkDate2(indvweekdays[1].year,indvweekdays[1].month,indvweekdays[1].day) and clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].snwdQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].snwd if checkDate2(indvweekdays[2].year,indvweekdays[2].month,indvweekdays[2].day) else "M",
   clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].snwdM if checkDate2(indvweekdays[2].year,indvweekdays[2].month,indvweekdays[2].day) and clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].snwdM == "T" else "",
   "*" if checkDate2(indvweekdays[2].year,indvweekdays[2].month,indvweekdays[2].day) and clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].snwdQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].snwd if checkDate2(indvweekdays[3].year,indvweekdays[3].month,indvweekdays[3].day) else "M",
   clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].snwdM if checkDate2(indvweekdays[3].year,indvweekdays[3].month,indvweekdays[3].day) and clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].snwdM == "T" else "",
   "*" if checkDate2(indvweekdays[3].year,indvweekdays[3].month,indvweekdays[3].day) and clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].snwdQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].snwd if checkDate2(indvweekdays[4].year,indvweekdays[4].month,indvweekdays[4].day) else "M",
   clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].snwdM if checkDate2(indvweekdays[4].year,indvweekdays[4].month,indvweekdays[4].day) and clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].snwdM == "T" else "",
   "*" if checkDate2(indvweekdays[4].year,indvweekdays[4].month,indvweekdays[4].day) and clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].snwdQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].snwd if checkDate2(indvweekdays[5].year,indvweekdays[5].month,indvweekdays[5].day) else "M",
   clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].snwdM if checkDate2(indvweekdays[5].year,indvweekdays[5].month,indvweekdays[5].day) and clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].snwdM == "T" else "",
   "*" if checkDate2(indvweekdays[5].year,indvweekdays[5].month,indvweekdays[5].day) and clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].snwdQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].snwd if checkDate2(indvweekdays[6].year,indvweekdays[6].month,indvweekdays[6].day) else "M",
   clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].snwdM if checkDate2(indvweekdays[6].year,indvweekdays[6].month,indvweekdays[6].day) and clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].snwdM == "T" else "",
   "*" if checkDate2(indvweekdays[6].year,indvweekdays[6].month,indvweekdays[6].day) and clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].snwdQ != "" else "")))
        print("{:^6}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}".format("TMAX",
   "{}{}{}".format(
   clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].tmax if checkDate2(indvweekdays[0].year,indvweekdays[0].month,indvweekdays[0].day) and clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].tmax != "" else "M",
   clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].tmaxM if checkDate2(indvweekdays[0].year,indvweekdays[0].month,indvweekdays[0].day) and clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].tmaxM == "T" else "",
   "*" if checkDate2(indvweekdays[0].year,indvweekdays[0].month,indvweekdays[0].day) and clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].tmaxQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].tmax if checkDate2(indvweekdays[1].year,indvweekdays[1].month,indvweekdays[1].day) and clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].tmax != "" else "M",
   clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].tmaxM if checkDate2(indvweekdays[1].year,indvweekdays[1].month,indvweekdays[1].day) and clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].tmaxM == "T" else "",
   "*" if checkDate2(indvweekdays[1].year,indvweekdays[1].month,indvweekdays[1].day) and clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].tmaxQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].tmax if checkDate2(indvweekdays[2].year,indvweekdays[2].month,indvweekdays[2].day) and clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].tmax != "" else "M",
   clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].tmaxM if checkDate2(indvweekdays[2].year,indvweekdays[2].month,indvweekdays[2].day) and clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].tmaxM == "T" else "",
   "*" if checkDate2(indvweekdays[2].year,indvweekdays[2].month,indvweekdays[2].day) and clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].tmaxQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].tmax if checkDate2(indvweekdays[3].year,indvweekdays[3].month,indvweekdays[3].day) and clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].tmax != "" else "M",
   clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].tmaxM if checkDate2(indvweekdays[3].year,indvweekdays[3].month,indvweekdays[3].day) and clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].tmaxM == "T" else "",
   "*" if checkDate2(indvweekdays[3].year,indvweekdays[3].month,indvweekdays[3].day) and clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].tmaxQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].tmax if checkDate2(indvweekdays[4].year,indvweekdays[4].month,indvweekdays[4].day) and clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].tmax != "" else "M",
   clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].tmaxM if checkDate2(indvweekdays[4].year,indvweekdays[4].month,indvweekdays[4].day) and clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].tmaxM == "T" else "",
   "*" if checkDate2(indvweekdays[4].year,indvweekdays[4].month,indvweekdays[4].day) and clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].tmaxQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].tmax if checkDate2(indvweekdays[5].year,indvweekdays[5].month,indvweekdays[5].day) and clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].tmax != "" else "M",
   clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].tmaxM if checkDate2(indvweekdays[5].year,indvweekdays[5].month,indvweekdays[5].day) and clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].tmaxM == "T" else "",
   "*" if checkDate2(indvweekdays[5].year,indvweekdays[5].month,indvweekdays[5].day) and clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].tmaxQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].tmax if checkDate2(indvweekdays[6].year,indvweekdays[6].month,indvweekdays[6].day) and clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].tmax != "" else "M",
   clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].tmaxM if checkDate2(indvweekdays[6].year,indvweekdays[6].month,indvweekdays[6].day) and clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].tmaxM == "T" else "",
   "*" if checkDate2(indvweekdays[6].year,indvweekdays[6].month,indvweekdays[6].day) and clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].tmaxQ != "" else "")))
        print("{:^6}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}".format("TMIN",
   "{}{}{}".format(
   clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].tmin if checkDate2(indvweekdays[0].year,indvweekdays[0].month,indvweekdays[0].day) and clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].tmin != "" else "M",
   clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].tminM if checkDate2(indvweekdays[0].year,indvweekdays[0].month,indvweekdays[0].day) and clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].tminM == "T" else "",
   "*" if checkDate2(indvweekdays[0].year,indvweekdays[0].month,indvweekdays[0].day) and clmt[indvweekdays[0].year][indvweekdays[0].month][indvweekdays[0].day].tminQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].tmin if checkDate2(indvweekdays[1].year,indvweekdays[1].month,indvweekdays[1].day) and clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].tmin != "" else "M",
   clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].tminM if checkDate2(indvweekdays[1].year,indvweekdays[1].month,indvweekdays[1].day) and clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].tminM == "T" else "",
   "*" if checkDate2(indvweekdays[1].year,indvweekdays[1].month,indvweekdays[1].day) and clmt[indvweekdays[1].year][indvweekdays[1].month][indvweekdays[1].day].tminQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].tmin if checkDate2(indvweekdays[2].year,indvweekdays[2].month,indvweekdays[2].day) and clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].tmin != "" else "M",
   clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].tminM if checkDate2(indvweekdays[2].year,indvweekdays[2].month,indvweekdays[2].day) and clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].tminM == "T" else "",
   "*" if checkDate2(indvweekdays[2].year,indvweekdays[2].month,indvweekdays[2].day) and clmt[indvweekdays[2].year][indvweekdays[2].month][indvweekdays[2].day].tminQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].tmin if checkDate2(indvweekdays[3].year,indvweekdays[3].month,indvweekdays[3].day) and clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].tmin != "" else "M",
   clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].tminM if checkDate2(indvweekdays[3].year,indvweekdays[3].month,indvweekdays[3].day) and clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].tminM == "T" else "",
   "*" if checkDate2(indvweekdays[3].year,indvweekdays[3].month,indvweekdays[3].day) and clmt[indvweekdays[3].year][indvweekdays[3].month][indvweekdays[3].day].tminQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].tmin if checkDate2(indvweekdays[4].year,indvweekdays[4].month,indvweekdays[4].day) and clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].tmin != "" else "M",
   clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].tminM if checkDate2(indvweekdays[4].year,indvweekdays[4].month,indvweekdays[4].day) and clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].tminM == "T" else "",
   "*" if checkDate2(indvweekdays[4].year,indvweekdays[4].month,indvweekdays[4].day) and clmt[indvweekdays[4].year][indvweekdays[4].month][indvweekdays[4].day].tminQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].tmin if checkDate2(indvweekdays[5].year,indvweekdays[5].month,indvweekdays[5].day) and clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].tmin != "" else "M",
   clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].tminM if checkDate2(indvweekdays[5].year,indvweekdays[5].month,indvweekdays[5].day) and clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].tminM == "T" else "",
   "*" if checkDate2(indvweekdays[5].year,indvweekdays[5].month,indvweekdays[5].day) and clmt[indvweekdays[5].year][indvweekdays[5].month][indvweekdays[5].day].tminQ != "" else ""),
   "{}{}{}".format(
   clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].tmin if checkDate2(indvweekdays[6].year,indvweekdays[6].month,indvweekdays[6].day) and clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].tmin != "" else "M",
   clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].tminM if checkDate2(indvweekdays[6].year,indvweekdays[6].month,indvweekdays[6].day) and clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].tminM == "T" else "",
   "*" if checkDate2(indvweekdays[6].year,indvweekdays[6].month,indvweekdays[6].day) and clmt[indvweekdays[6].year][indvweekdays[6].month][indvweekdays[6].day].tminQ != "" else "")))

        print("")
        print("Total Precipitation: {}{}".format(
                                    round(sum(w_prcp),2),
                                    ", Rank: {}".format(rank(prcphist.index(round(sum(w_prcp),2))+1)) if sum(w_prcp) != 0 else ""
                                    ))
        print("Total Precipitation Days (>= T): {}".format(w_prcpDAYS))
        if w_snowDAYS >= 1:
            print("Total Snow: {}{}".format(
                                        round(sum(w_snow),1),
                                        ", Rank: {}".format(rank(snowhist.index(round(sum(w_snow),1))+1)) if sum(w_snow) != 0 else ""
                                        ))
            print("Total Snow Days (>= T): {}".format(w_snowDAYS))
        if len(w_snwd) > 0 and mean(w_snwd) > 0:
            print("Average Snow Depth: {}{}".format(
                                        round(mean(w_snwd),1),
                                        ", Rank: {}".format(rank(snwdhist.index(round(mean(w_snwd),1))+1)) if mean(w_snwd) != 0 and len(w_snwd) > excludeweek else ""
                                        ))
        if records_in_week > excludeweek and (len(w_tmax) <= excludeweek or len(w_tmin) <= excludeweek): print("*** TEMPERATURE STATS LIKELY UNDERREPRESENTED ***")
        
        print("Average Temperature: {}{}{}".format(
                                        round(mean(w_alltemps),1) if len(w_alltemps) > 0 else "N/A",
                                        ", Rank: {} Warmest".format(rank(tavgdeschist.index(round(mean(w_alltemps),1))+1))
                                                    if len(w_alltemps) > excludeweek*2 and tavgdeschist.index(round(mean(w_alltemps),1)) <= tavgaschist.index(round(mean(w_alltemps),1)) else "",
                                        ", Rank: {} Coolest".format(rank(tavgaschist.index(round(mean(w_alltemps),1))+1))
                                                    if len(w_alltemps) > excludeweek*2 and tavgaschist.index(round(mean(w_alltemps),1)) <= tavgdeschist.index(round(mean(w_alltemps),1)) else ""
                                        ))
        print("Average Max Temperature: {}{}{}".format(
                                        round(mean(w_tmax),1) if len(w_tmax) > 0 else "N/A",
                                        ", Rank: {} Warmest".format(rank(tmaxdeschist.index(round(mean(w_tmax),1))+1))
                                                    if len(w_tmax) > excludeweek and tmaxdeschist.index(round(mean(w_tmax),1)) <= tmaxaschist.index(round(mean(w_tmax),1)) else "",
                                        ", Rank: {} Coolest".format(rank(tmaxaschist.index(round(mean(w_tmax),1))+1))
                                                    if len(w_tmax) > excludeweek and tmaxaschist.index(round(mean(w_tmax),1)) <= tmaxdeschist.index(round(mean(w_tmax),1)) else ""
                                        ))
        #print(tmaxaschist.index(round(mean(w_tmax),1)),tmaxdeschist.index(round(mean(w_tmax),1)))
        print("Average Min Temperature: {}{}{}".format(
                                        round(mean(w_tmin),1) if len(w_tmin) > 0 else "N/A",
                                        ", Rank: {} Warmest".format(rank(tmindeschist.index(round(mean(w_tmin),1))+1))
                                                    if tmindeschist.index(round(mean(w_tmin),1)) <= tminaschist.index(round(mean(w_tmin),1)) else "",
                                        ", Rank: {} Coolest".format(rank(tminaschist.index(round(mean(w_tmin),1))+1))
                                                    if len(w_tmin) > excludeweek and tminaschist.index(round(mean(w_tmin),1)) <= tmindeschist.index(round(mean(w_tmin),1)) else ""
                                        ))
        #print(tminaschist.index(round(mean(w_tmin),1)),tmindeschist.index(round(mean(w_tmin),1)))
        print("")

def monthStats(y,m):
    """Report on recorded statistics for a month of interest. It accepts only
    arguments for the year and month of interest. Passed arguments MUST be
    integers. 
    
    monthStats(year,month)
    
    EXAMPLE: monthStats(2005,7) -> Returns a printout of month-based
                                   statistics from July 2005.
    """
    if len(clmt) == 0: return print("* OOPS! Run the clmtAnalyze function first.")
    monthExists = checkDate(y,m)
    if monthExists:
        ranks = ["th","st","nd","rd","th","th","th","th","th","th"]
        prcpaschist = sorted(list(set(list(var for var in clmt_vars_months["prcp"] for MONTH in clmt_vars_months["prcp"][var] if MONTH.month == m and clmt[MONTH.year][MONTH.month]["recordqty"] > excludemonth))))
        prcpdeschist = sorted(list(set(list(var for var in clmt_vars_months["prcp"] for MONTH in clmt_vars_months["prcp"][var] if MONTH.month == m))),reverse=True)
        #prcpDAYSaschist = sorted(set(list(clmt[Y][m]["prcpDAYS"] for Y in [yr for yr in clmt if type(yr) == int] if m in clmt[Y] and clmt[Y][m]["recordqty"] > excludemonth)))
        #prcpDAYSdeschist = sorted(list(set(list(clmt[Y][m]["prcpDAYS"] for Y in [yr for yr in clmt if type(yr) == int] if m in clmt[Y]))),reverse=True)
        #snowaschist = sorted(list(var for var in clmt_vars_months["snow"] for MONTH in clmt_vars_months["snow"][var] if MONTH.month == m and clmt[MONTH.year][MONTH.month]["recordqty"] > excludemonth))
        snowdeschist = sorted(list(set(list(var for var in clmt_vars_months["snow"] for MONTH in clmt_vars_months["snow"][var] if MONTH.month == m))),reverse=True)
        #snowDAYSdeschist = sorted(list(set(list(clmt[Y][m]["snowDAYS"] for Y in [yr for yr in clmt if type(yr) == int] if m in clmt[Y]))),reverse=True)
        #snwddeschist = sorted(list(set(list(var for var in clmt_vars_months["snwd"] for MONTH in clmt_vars_months["snwd"][var] if MONTH.month == m))),reverse=True)
        #snwdDAYSdeschist = sorted(list(set(list(clmt[Y][m]["snwdDAYS"] for Y in [yr for yr in clmt if type(yr) == int] if m in clmt[Y]))),reverse=True)
        tmaxaschist = sorted(list(set(list(var for var in clmt_vars_months["tmax"] for MONTH in clmt_vars_months["tmax"][var] if MONTH.month == m))))
        tmaxdeschist = sorted(list(set(list(var for var in clmt_vars_months["tmax"] for MONTH in clmt_vars_months["tmax"][var] if MONTH.month == m))),reverse=True)
        tminaschist = sorted(list(set(list(var for var in clmt_vars_months["tmin"] for MONTH in clmt_vars_months["tmin"][var] if MONTH.month == m))))
        tmindeschist = sorted(list(set(list(var for var in clmt_vars_months["tmin"] for MONTH in clmt_vars_months["tmin"][var] if MONTH.month == m))),reverse=True)
        tavgaschist = sorted(list(set(list(var for var in clmt_vars_months["tavg"] for MONTH in clmt_vars_months["tavg"][var] if MONTH.month == m))))
        tavgdeschist = sorted(list(set(list(var for var in clmt_vars_months["tavg"] for MONTH in clmt_vars_months["tavg"][var] if MONTH.month == m))),reverse=True)
        #print(tavgdeschist)
        #for x in [prcphist,snowhist,tmaxaschist,tmaxdeschist,tminaschist,tmindeschist,tavgaschist,tavgdeschist]: print(x)

        if clmt[y][m]["recordqty"] <= excludemonth:
            print("-------------------------------------")
            print("*** MONLTHLY STATS MAY NOT BE COMPLETE FOR RELIANCE ON STATISTICS ***")

        print("-------------------------------------")
        print("Monthly Statistics for {} {}".format(calendar.month_name[m],y))
        print("{}: {}".format(clmt["station"],clmt["station_name"]))
        print("Quantity of Records: {}".format(clmt[y][m]["recordqty"]))
        print("* Reported rankings are relative to the month of {}".format(calendar.month_name[m]))
        print("-----")
        # PRCP related
        print("Total Precipitation: {}{}{}".format(
                    round(sum(clmt[y][m]["prcp"]),2),
                    ", Rank: {} Wettest".format(rank(prcpdeschist.index(round(sum(clmt[y][m]["prcp"]),2))+1)) if sum(clmt[y][m]["prcp"]) > 0 and prcpdeschist.index(round(sum(clmt[y][m]["prcp"]),2)) <= prcpaschist.index(round(sum(clmt[y][m]["prcp"]),2)) else "",
                    ", Rank: {} Driest".format(rank(prcpaschist.index(round(sum(clmt[y][m]["prcp"]),2))+1)) if clmt[y][m]["recordqty"] > excludemonth and prcpaschist.index(round(sum(clmt[y][m]["prcp"]),2)) <= prcpdeschist.index(round(sum(clmt[y][m]["prcp"]),2)) else ""
        ))
        print("Total Precipitation Days (>= T): {}".format(clmt[y][m]["prcpDAYS"]))
        if round(sum(clmt[y][m]["prcp"]),2) > 0:
            print("-- Highest Daily Precip: {}".format(clmt[y][m]["prcpPROP"]["day_max"][0]),end = " ::: ")
            for x in clmt[y][m]["prcpPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end=" ") if x != clmt[y][m]["prcpPROP"]["day_max"][1][len(clmt[y][m]["prcpPROP"]["day_max"][1])-1] else print("{}".format(x.daystr))
        # SNOW related
        if sum(clmt[y][m]["snow"]) > 0 or clmt[y][m]["snowDAYS"] > 0:
            print("Total Snow: {}{}".format(
                        round(sum(clmt[y][m]["snow"]),1),
                        ", Rank: {} Snowiest".format(rank(snowdeschist.index(round(sum(clmt[y][m]["snow"]),2))+1)) if sum(clmt[y][m]["snow"]) > 0 else ", -- ; "
            ))
            print("Total Snow Days (>= T): {}".format(clmt[y][m]["snowDAYS"]))
            if round(sum(clmt[y][m]["snow"]),1) > 0:
                print("-- Highest Daily Snow Total: {}".format(clmt[y][m]["snowPROP"]["day_max"][0]),end = " ::: ")
                for x in clmt[y][m]["snowPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end=" ") if x != clmt[y][m]["snowPROP"]["day_max"][1][len(clmt[y][m]["snowPROP"]["day_max"][1])-1] else print("{}".format(x.daystr))
        # SNWD related
        if clmt[y][m]["snwdDAYS"] > 0:
            print("Total Days with Snow on the Ground ('snwd' >= T): {}".format(clmt[y][m]["snwdDAYS"]))
            if any(v > 0 for v in clmt[y][m]["snwd"]):  # If any of the snwd days are > 0
                print("-- Highest Daily Snow-Depth Total: {}".format(clmt[y][m]["snwdPROP"]["day_max"][0]),end = " ::: ")
                for x in clmt[y][m]["snwdPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end=" ") if x != clmt[y][m]["snwdPROP"]["day_max"][1][len(clmt[y][m]["snwdPROP"]["day_max"][1])-1] else print("{}".format(x.daystr))
        try:
            print("Average Temperature: {}{}{}".format(
                round(mean(clmt[y][m]["tempAVGlist"]),1),
                ", Rank: {} Warmest".format(rank(tavgdeschist.index(round(mean(clmt[y][m]["tempAVGlist"]),1))+1)) if len(clmt[y][m]["tempAVGlist"]) > excludemonth*2 and tavgdeschist.index(round(mean(clmt[y][m]["tempAVGlist"]),1)) <= tavgaschist.index(round(mean(clmt[y][m]["tempAVGlist"]),1)) else "",
                ", Rank: {} Coolest".format(rank(tavgaschist.index(round(mean(clmt[y][m]["tempAVGlist"]),1))+1)) if len(clmt[y][m]["tempAVGlist"]) > excludemonth*2 and tavgaschist.index(round(mean(clmt[y][m]["tempAVGlist"]),1)) <= tavgdeschist.index(round(mean(clmt[y][m]["tempAVGlist"]),1)) else ""
            ))
        except: print("Average Temperature: N/A")
        try:
            print("Average MAX Temperature: {}{}{}".format(
                round(mean(clmt[y][m]["tmax"]),1),
                ", Rank: {} Warmest".format(rank(tmaxdeschist.index(round(mean(clmt[y][m]["tmax"]),1))+1)) if len(clmt[y][m]["tmax"]) > excludemonth and tmaxdeschist.index(round(mean(clmt[y][m]["tmax"]),1)) <= tmaxaschist.index(round(mean(clmt[y][m]["tmax"]),1)) else "",
                ", Rank: {} Coolest".format(rank(tmaxaschist.index(round(mean(clmt[y][m]["tmax"]),1))+1)) if len(clmt[y][m]["tmax"]) > excludemonth and tmaxaschist.index(round(mean(clmt[y][m]["tmax"]),1)) <= tmaxdeschist.index(round(mean(clmt[y][m]["tmax"]),1)) else ""
            ))
            if round(sum(clmt[y][m]["tmax"]),1) > 0:
                print("-- Warmest Daily TMAX: {}".format(clmt[y][m]["tmaxPROP"]["day_max"][0]),end = " ::: ")
                for x in clmt[y][m]["tmaxPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end=" ") if x != clmt[y][m]["tmaxPROP"]["day_max"][1][len(clmt[y][m]["tmaxPROP"]["day_max"][1])-1] else print("{}".format(x.daystr))
            if round(sum(clmt[y][m]["tmax"]),1) > 0:
                print("-- Coolest Daily TMAX: {}".format(clmt[y][m]["tmaxPROP"]["day_min"][0]),end = " ::: ")
                for x in clmt[y][m]["tmaxPROP"]["day_min"][1]: print("{}, ".format(x.daystr), end=" ") if x != clmt[y][m]["tmaxPROP"]["day_min"][1][len(clmt[y][m]["tmaxPROP"]["day_min"][1])-1] else print("{}".format(x.daystr))
        except: print("Average MAX Temperature: N/A")
        try:
            print("Average MIN Temperature: {}{}{}".format(
                round(mean(clmt[y][m]["tmin"]),1),
                ", Rank: {} Warmest".format(rank(tmindeschist.index(round(mean(clmt[y][m]["tmin"]),1))+1)) if len(clmt[y][m]["tmin"]) > excludemonth and tmindeschist.index(round(mean(clmt[y][m]["tmin"]),1)) <= tminaschist.index(round(mean(clmt[y][m]["tmin"]),1)) else "",
                ", Rank: {} Coolest".format(rank(tminaschist.index(round(mean(clmt[y][m]["tmin"]),1))+1)) if len(clmt[y][m]["tmin"]) > excludemonth and tminaschist.index(round(mean(clmt[y][m]["tmin"]),1)) <= tmindeschist.index(round(mean(clmt[y][m]["tmin"]),1)) else ""
            ))
            if round(sum(clmt[y][m]["tmin"]),1) > 0:
                print("-- Warmest Daily TMIN: {}".format(clmt[y][m]["tminPROP"]["day_max"][0]),end = " ::: ")
                for x in clmt[y][m]["tminPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end=" ") if x != clmt[y][m]["tminPROP"]["day_max"][1][len(clmt[y][m]["tminPROP"]["day_max"][1])-1] else print("{}".format(x.daystr))
            if round(sum(clmt[y][m]["tmin"]),1) > 0:
                print("-- Coolest Daily TMIN: {}".format(clmt[y][m]["tminPROP"]["day_min"][0]),end = " ::: ")
                for x in clmt[y][m]["tminPROP"]["day_min"][1]: print("{}, ".format(x.daystr), end=" ") if x != clmt[y][m]["tminPROP"]["day_min"][1][len(clmt[y][m]["tminPROP"]["day_min"][1])-1] else print("{}".format(x.daystr))
        except: print("Average MIN Temperature: N/A")
        if all(len(x) == 0 for x in [clmt[y][m]["tempAVGlist"],clmt[y][m]["tmax"],clmt[y][m]["tmin"]]):
            print("*** No Reliable Temperature Data for {} {}".format(calendar.month_abbr[m],y))
        print("-----")

def yearStats(y):
    """Report on recorded statistics for a year of interest. It accepts only
    an argument for the year. Passed argument MUST be an integer.

    yearStats(year)

    EXAMPLE: yearStats(1945) -> Returns a printout of year-based statistics 
                                from 1945
    """

    if len(clmt) == 0: return print("* OOPS! Run the clmtAnalyze function first.")
    # clmt[int(each[2][0:4])]["prcpPROP"] = {"day_max":[-1,[]],"month_max":[-1,[]],"month_min":[999,[]]}
    # clmt[int(each[2][0:4])]["snowPROP"] = {"day_max":[-1,[]],"month_max":[-1,[]]}
    # clmt[int(each[2][0:4])]["tempAVGlist"] = []
    # clmt[int(each[2][0:4])]["tmax"] = []
    # clmt[int(each[2][0:4])]["tmaxPROP"] = {"day_max":[-999,[]],"day_min":[999,[]],"month_AVG_max":[-999,[]],"month_AVG_min":[999,[]]}
    yearExists = checkDate(y)
    if yearExists:
        prcpaschist, prcpdeschist, prcpDAYSaschist, prcpDAYSdeschist, snowaschist, snowdeschist, snowDAYSaschist, snowDAYSdeschist, tmaxaschist, tmaxdeschist, tminaschist, tmindeschist, tavgaschist, tavgdeschist = yearRank("temps",5,yearStatsRun=True)
        snwdDAYSdeschist = sorted(set(list(clmt[YR]["snwdDAYS"] for YR in [Y for Y in clmt if type(Y) == int] if clmt[YR]["snwdDAYS"] != 0)),reverse=True)
        snwdDAYSaschist = sorted(set(list(clmt[YR]["snwdDAYS"] for YR in [Y for Y in clmt if type(Y) == int] if clmt[YR]["recordqty"] > excludeyear)))
        #for x in [prcpaschist, prcpdeschist, snowaschist, snowdeschist, tmaxaschist, tmaxdeschist, tminaschist, tmindeschist, tavgaschist, tavgdeschist]: print(len(x))
        print("")
        print("{:^55}".format("Yearly Statistics for {}".format(y)))
        print("{:^55}".format("{}: {}".format(clmt["station"],clmt["station_name"])))
        print("{:^55}".format("Quantity of Records: {}".format(clmt[y]["recordqty"])))
        if clmt[y]["recordqty"] <= excludeyear:
            print("{:-^55}".format(""))
            print("*** YEAR STATS MAY NOT BE COMPLETE FOR RELIANCE ON STATISTICS ***")
        print("{:-^55}".format(""))
        print("{:^6}|{:^7}|{:^7}|{:^7}|{:^7}|{:^7}|{:^7}|".format("","JAN","FEB","MAR","APR","MAY","JUN"))
        print("{:-^55}".format(""))
        print("{:^6}|{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |".format(
            "PRCP",
            "{:.2f}".format(round(sum(clmt[y][1]["prcp"]),2)) if 1 in clmt[y] else "",
            "{:.2f}".format(round(sum(clmt[y][2]["prcp"]),2)) if 2 in clmt[y] else "",
            "{:.2f}".format(round(sum(clmt[y][3]["prcp"]),2)) if 3 in clmt[y] else "",
            "{:.2f}".format(round(sum(clmt[y][4]["prcp"]),2)) if 4 in clmt[y] else "",
            "{:.2f}".format(round(sum(clmt[y][5]["prcp"]),2)) if 5 in clmt[y] else "",
            "{:.2f}".format(round(sum(clmt[y][6]["prcp"]),2)) if 6 in clmt[y] else "",
        ))
        print("{:^6}|{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |".format(
            "SNOW",
            "{:.1f}".format(round(sum(clmt[y][1]["snow"]),1)) if 1 in clmt[y] and (sum(clmt[y][1]["snow"]) > 0 or clmt[y][1]["snowDAYS"] > 0) else (" -- " if 1 in clmt[y] and sum(clmt[y][1]["snow"]) == 0 else ""),
            "{:.1f}".format(round(sum(clmt[y][2]["snow"]),1)) if 2 in clmt[y] and (sum(clmt[y][2]["snow"]) > 0 or clmt[y][2]["snowDAYS"] > 0) else (" -- " if 2 in clmt[y] and sum(clmt[y][2]["snow"]) == 0 else ""),
            "{:.1f}".format(round(sum(clmt[y][3]["snow"]),1)) if 3 in clmt[y] and (sum(clmt[y][3]["snow"]) > 0 or clmt[y][3]["snowDAYS"] > 0) else (" -- " if 3 in clmt[y] and sum(clmt[y][3]["snow"]) == 0 else ""),
            "{:.1f}".format(round(sum(clmt[y][4]["snow"]),1)) if 4 in clmt[y] and (sum(clmt[y][4]["snow"]) > 0 or clmt[y][4]["snowDAYS"] > 0) else (" -- " if 4 in clmt[y] and sum(clmt[y][4]["snow"]) == 0 else ""),
            "{:.1f}".format(round(sum(clmt[y][5]["snow"]),1)) if 5 in clmt[y] and (sum(clmt[y][5]["snow"]) > 0 or clmt[y][5]["snowDAYS"] > 0) else (" -- " if 5 in clmt[y] and sum(clmt[y][5]["snow"]) == 0 else ""),
            "{:.1f}".format(round(sum(clmt[y][6]["snow"]),1)) if 6 in clmt[y] and (sum(clmt[y][6]["snow"]) > 0 or clmt[y][6]["snowDAYS"] > 0) else (" -- " if 6 in clmt[y] and sum(clmt[y][6]["snow"]) == 0 else ""),
        ))
        print("{:^6}|{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |".format(
            "TAVG",
            "{:.1f}".format(round(mean(clmt[y][1]["tempAVGlist"]),1)) if 1 in clmt[y] and len(clmt[y][1]["tempAVGlist"]) > 2 else "",
            "{:.1f}".format(round(mean(clmt[y][2]["tempAVGlist"]),1)) if 2 in clmt[y] and len(clmt[y][2]["tempAVGlist"]) > 2 else "",
            "{:.1f}".format(round(mean(clmt[y][3]["tempAVGlist"]),1)) if 3 in clmt[y] and len(clmt[y][3]["tempAVGlist"]) > 2 else "",
            "{:.1f}".format(round(mean(clmt[y][4]["tempAVGlist"]),1)) if 4 in clmt[y] and len(clmt[y][4]["tempAVGlist"]) > 2 else "",
            "{:.1f}".format(round(mean(clmt[y][5]["tempAVGlist"]),1)) if 5 in clmt[y] and len(clmt[y][5]["tempAVGlist"]) > 2 else "",
            "{:.1f}".format(round(mean(clmt[y][6]["tempAVGlist"]),1)) if 6 in clmt[y] and len(clmt[y][6]["tempAVGlist"]) > 2 else "",
        ))
        print("{:^6}|{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |".format(
            "TMAX",
            "{:.1f}".format(round(mean(clmt[y][1]["tmax"]),1)) if 1 in clmt[y] and len(clmt[y][1]["tmax"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][2]["tmax"]),1)) if 2 in clmt[y] and len(clmt[y][2]["tmax"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][3]["tmax"]),1)) if 3 in clmt[y] and len(clmt[y][3]["tmax"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][4]["tmax"]),1)) if 4 in clmt[y] and len(clmt[y][4]["tmax"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][5]["tmax"]),1)) if 5 in clmt[y] and len(clmt[y][5]["tmax"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][6]["tmax"]),1)) if 6 in clmt[y] and len(clmt[y][6]["tmax"]) > 1 else "",
        ))
        print("{:^6}|{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |".format(
            "TMIN",
            "{:.1f}".format(round(mean(clmt[y][1]["tmin"]),1)) if 1 in clmt[y] and len(clmt[y][1]["tmin"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][2]["tmin"]),1)) if 2 in clmt[y] and len(clmt[y][2]["tmin"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][3]["tmin"]),1)) if 3 in clmt[y] and len(clmt[y][3]["tmin"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][4]["tmin"]),1)) if 4 in clmt[y] and len(clmt[y][4]["tmin"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][5]["tmin"]),1)) if 5 in clmt[y] and len(clmt[y][5]["tmin"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][6]["tmin"]),1)) if 6 in clmt[y] and len(clmt[y][6]["tmin"]) > 1 else "",
        ))
        print("{:-^55}".format(""))
        print("{:^6}|{:^7}|{:^7}|{:^7}|{:^7}|{:^7}|{:^7}|".format("","JUL","AUG","SEP","OCT","NOV","DEC"))
        print("{:-^55}".format(""))
        print("{:^6}|{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |".format(
            "PRCP",
            "{:.2f}".format(round(sum(clmt[y][7]["prcp"]),2)) if 7 in clmt[y] else "",
            "{:.2f}".format(round(sum(clmt[y][8]["prcp"]),2)) if 8 in clmt[y] else "",
            "{:.2f}".format(round(sum(clmt[y][9]["prcp"]),2)) if 9 in clmt[y] else "",
            "{:.2f}".format(round(sum(clmt[y][10]["prcp"]),2)) if 10 in clmt[y] else "",
            "{:.2f}".format(round(sum(clmt[y][11]["prcp"]),2)) if 11 in clmt[y] else "",
            "{:.2f}".format(round(sum(clmt[y][12]["prcp"]),2)) if 12 in clmt[y] else "",
        ))
        print("{:^6}|{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |".format(
            "SNOW",
            "{:.1f}".format(round(sum(clmt[y][7]["snow"]),1)) if 7 in clmt[y] and (sum(clmt[y][7]["snow"]) > 0 or clmt[y][7]["snowDAYS"] > 0) else (" -- " if 7 in clmt[y] and sum(clmt[y][7]["snow"]) == 0 else ""),
            "{:.1f}".format(round(sum(clmt[y][8]["snow"]),1)) if 8 in clmt[y] and (sum(clmt[y][8]["snow"]) > 0 or clmt[y][8]["snowDAYS"] > 0) else (" -- " if 8 in clmt[y] and sum(clmt[y][8]["snow"]) == 0 else ""),
            "{:.1f}".format(round(sum(clmt[y][9]["snow"]),1)) if 9 in clmt[y] and (sum(clmt[y][9]["snow"]) > 0 or clmt[y][9]["snowDAYS"] > 0) else (" -- " if 9 in clmt[y] and sum(clmt[y][9]["snow"]) == 0 else ""),
            "{:.1f}".format(round(sum(clmt[y][10]["snow"]),1)) if 10 in clmt[y] and (sum(clmt[y][10]["snow"]) > 0 or clmt[y][10]["snowDAYS"] > 0) else (" -- " if 10 in clmt[y] and sum(clmt[y][10]["snow"]) == 0 else ""),
            "{:.1f}".format(round(sum(clmt[y][11]["snow"]),1)) if 11 in clmt[y] and (sum(clmt[y][11]["snow"]) > 0 or clmt[y][11]["snowDAYS"] > 0) else (" -- " if 11 in clmt[y] and sum(clmt[y][11]["snow"]) == 0 else ""),
            "{:.1f}".format(round(sum(clmt[y][12]["snow"]),1)) if 12 in clmt[y] and (sum(clmt[y][12]["snow"]) > 0 or clmt[y][12]["snowDAYS"] > 0) else (" -- " if 12 in clmt[y] and sum(clmt[y][12]["snow"]) == 0 else ""),
        ))
        print("{:^6}|{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |".format(
            "TAVG",
            "{:.1f}".format(round(mean(clmt[y][7]["tempAVGlist"]),1)) if 7 in clmt[y] and len(clmt[y][7]["tempAVGlist"]) > 2 else "",
            "{:.1f}".format(round(mean(clmt[y][8]["tempAVGlist"]),1)) if 8 in clmt[y] and len(clmt[y][8]["tempAVGlist"]) > 2 else "",
            "{:.1f}".format(round(mean(clmt[y][9]["tempAVGlist"]),1)) if 9 in clmt[y] and len(clmt[y][9]["tempAVGlist"]) > 2 else "",
            "{:.1f}".format(round(mean(clmt[y][10]["tempAVGlist"]),1)) if 10 in clmt[y] and len(clmt[y][10]["tempAVGlist"]) > 2 else "",
            "{:.1f}".format(round(mean(clmt[y][11]["tempAVGlist"]),1)) if 11 in clmt[y] and len(clmt[y][11]["tempAVGlist"]) > 2 else "",
            "{:.1f}".format(round(mean(clmt[y][12]["tempAVGlist"]),1)) if 12 in clmt[y] and len(clmt[y][12]["tempAVGlist"]) > 2 else "",
        ))
        print("{:^6}|{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |".format(
            "TMAX",
            "{:.1f}".format(round(mean(clmt[y][7]["tmax"]),1)) if 7 in clmt[y] and len(clmt[y][7]["tmax"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][8]["tmax"]),1)) if 8 in clmt[y] and len(clmt[y][8]["tmax"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][9]["tmax"]),1)) if 9 in clmt[y] and len(clmt[y][9]["tmax"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][10]["tmax"]),1)) if 10 in clmt[y] and len(clmt[y][10]["tmax"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][11]["tmax"]),1)) if 11 in clmt[y] and len(clmt[y][11]["tmax"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][12]["tmax"]),1)) if 12 in clmt[y] and len(clmt[y][12]["tmax"]) > 1 else "",
        ))
        print("{:^6}|{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |{:>6} |".format(
            "TMIN",
            "{:.1f}".format(round(mean(clmt[y][7]["tmin"]),1)) if 7 in clmt[y] and len(clmt[y][7]["tmin"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][8]["tmin"]),1)) if 8 in clmt[y] and len(clmt[y][8]["tmin"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][9]["tmin"]),1)) if 9 in clmt[y] and len(clmt[y][9]["tmin"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][10]["tmin"]),1)) if 10 in clmt[y] and len(clmt[y][10]["tmin"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][11]["tmin"]),1)) if 11 in clmt[y] and len(clmt[y][11]["tmin"]) > 1 else "",
            "{:.1f}".format(round(mean(clmt[y][12]["tmin"]),1)) if 12 in clmt[y] and len(clmt[y][12]["tmin"]) > 1 else "",
        ))
        print("{:-^55}".format(""))

        print(" Total Precipitation: {}".format(round(sum(clmt[y]["prcp"]),2)),end="")
        try: print(", Rank: {} Wettest".format(rank(prcpdeschist.index(round(sum(clmt[y]["prcp"]),2))+1)),end="") if sum(clmt[y]["prcp"]) > 0 and prcpdeschist.index(round(sum(clmt[y]["prcp"]),2)) <= prcpaschist.index(round(sum(clmt[y]["prcp"]),2)) else print("",end="")
        except: print(", Rank: {} Wettest".format(rank(prcpdeschist.index(round(sum(clmt[y]["prcp"]),2))+1)),end="")
        try: print(", Rank: {} Driest".format(rank(prcpaschist.index(round(sum(clmt[y]["prcp"]),2))+1))) if clmt[y]["recordqty"] > excludeyear and prcpaschist.index(round(sum(clmt[y]["prcp"]),2)) <= prcpdeschist.index(round(sum(clmt[y]["prcp"]),2)) else print("")
        except: print("")

        print(" Total Precipitation Days (>=T): {}".format(clmt[y]["prcpDAYS"]),end="")
        try: print(", Rank: {} Most".format(rank(prcpDAYSdeschist.index(clmt[y]["prcpDAYS"])+1)),end="") if clmt[y]["prcpDAYS"] > 0 and prcpDAYSdeschist.index(clmt[y]["prcpDAYS"]) <= prcpDAYSaschist.index(clmt[y]["prcpDAYS"]) else print("",end="")
        except: print(", Rank: {} Most".format(rank(prcpDAYSdeschist.index(clmt[y]["prcpDAYS"])+1)),end="")
        try: print(", Rank: {} Least".format(rank(prcpDAYSaschist.index(clmt[y]["prcpDAYS"])+1))) if prcpDAYSaschist.index(clmt[y]["prcpDAYS"]) <= prcpDAYSdeschist.index(clmt[y]["prcpDAYS"]) else print("")
        except: print("")
        if round(sum(clmt[y]["prcp"]),2) > 0:
            print(" -- Highest Daily Precip: {}".format(clmt[y]["prcpPROP"]["day_max"][0]),end = " ::: ")
            for x in clmt[y]["prcpPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end=" ") if x != clmt[y]["prcpPROP"]["day_max"][1][len(clmt[y]["prcpPROP"]["day_max"][1])-1] else print("{}".format(x.daystr))

        print(" Total Snow: {}".format(round(sum(clmt[y]["snow"]),1)),end="")
        try: print(", Rank: {} Snowiest".format(rank(snowdeschist.index(round(sum(clmt[y]["snow"]),1))+1)),end="") if sum(clmt[y]["snow"]) > 0 and snowdeschist.index(round(sum(clmt[y]["snow"]),1)) <= snowaschist.index(round(sum(clmt[y]["snow"]),1)) else print("",end="")
        except: print(", Rank: {} Snowiest".format(rank(snowdeschist.index(round(sum(clmt[y]["snow"]),1))+1)),end="")
        try: print(", Rank: {} Least-Snowiest".format(rank(snowaschist.index(round(sum(clmt[y]["snow"]),1))+1))) if clmt[y]["recordqty"] > excludeyear and snowaschist.index(round(sum(clmt[y]["snow"]),1)) <= snowdeschist.index(round(sum(clmt[y]["snow"]),1)) else print("")
        except: print("")
        if round(sum(clmt[y]["snow"]),1) > 0:
            print(" -- Highest Daily Snow: {}".format(clmt[y]["snowPROP"]["day_max"][0]),end = " ::: ")
            for x in clmt[y]["snowPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end=" ") if x != clmt[y]["snowPROP"]["day_max"][1][len(clmt[y]["snowPROP"]["day_max"][1])-1] else print("{}".format(x.daystr))

        print(" Total Snow Days (>=T): {}".format(clmt[y]["snowDAYS"]),end="")
        try: print(", Rank: {} Most".format(rank(snowDAYSdeschist.index(clmt[y]["snowDAYS"])+1)),end="") if clmt[y]["snowDAYS"] > 0 and snowDAYSdeschist.index(clmt[y]["snowDAYS"]) <= snowDAYSaschist.index(clmt[y]["snowDAYS"]) else print("",end="")
        except: print(", Rank: {} Most".format(rank(snowDAYSdeschist.index(clmt[y]["snowDAYS"])+1)),end="")
        try: print(", Rank: {} Least".format(rank(snowDAYSaschist.index(clmt[y]["snowDAYS"])+1))) if clmt[y]["recordqty"] > excludeyear and snowDAYSaschist.index(clmt[y]["snowDAYS"]) <= snowDAYSdeschist.index(clmt[y]["snowDAYS"]) else print("")
        except: print("")
        if clmt[y]["snwdDAYS"] > 0:
            print(" Total Days w/Snow on the Ground (>=T): {}".format(clmt[y]["snwdDAYS"]),end="")
            try: print(", Rank: {} Most".format(rank(snwdDAYSdeschist.index(clmt[y]["snwdDAYS"])+1)),end="") if clmt[y]["snwdDAYS"] > 0 and snwdDAYSdeschist.index(clmt[y]["snwdDAYS"]) <= snwdDAYSaschist.index(clmt[y]["snwdDAYS"]) else print("",end="")
            except: print(", Rank: {} Most".format(rank(snwdDAYSdeschist.index(clmt[y]["snwdDAYS"])+1)),end="")
            try: print(", Rank: {} Least".format(rank(snwdDAYSaschist.index(clmt[y]["snwdDAYS"])+1))) if clmt[y]["recordqty"] > excludeyear and snwdDAYSaschist.index(clmt[y]["snwdDAYS"]) <= snwdDAYSdeschist.index(clmt[y]["snwdDAYS"]) else print("")
            except: print("")
        if round(sum(clmt[y]["snwd"]),1) > 0:
            print(" -- Highest Daily Snow-Depth: {}".format(clmt[y]["snwdPROP"]["day_max"][0]),end = " ::: ")
            for x in clmt[y]["snwdPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end=" ") if x != clmt[y]["snwdPROP"]["day_max"][1][len(clmt[y]["snwdPROP"]["day_max"][1])-1] else print("{}".format(x.daystr))

        try:
            print(" Average Temperature: {}".format(round(mean(clmt[y]["tempAVGlist"]),1)),end="")
            print(", Rank: {} Warmest".format(rank(tavgdeschist.index(round(mean(clmt[y]["tempAVGlist"]),1))+1)),end="") if len(clmt[y]["tempAVGlist"]) > excludeyear*2 and tavgdeschist.index(round(mean(clmt[y]["tempAVGlist"]),1)) <= tavgaschist.index(round(mean(clmt[y]["tempAVGlist"]),1)) else print("",end="")
            print(", Rank: {} Coolest".format(rank(tavgaschist.index(round(mean(clmt[y]["tempAVGlist"]),1))+1))) if len(clmt[y]["tempAVGlist"]) > excludeyear*2 and tavgaschist.index(round(mean(clmt[y]["tempAVGlist"]),1)) <= tavgdeschist.index(round(mean(clmt[y]["tempAVGlist"]),1)) else print("")
        except: print(" Average Temperature: N/A")

        try:
            print(" Avg MAX Temperature: {}".format(round(mean(clmt[y]["tmax"]),1)),end="")
            print(", Rank: {} Warmest".format(rank(tmaxdeschist.index(round(mean(clmt[y]["tmax"]),1))+1)),end="") if len(clmt[y]["tmax"]) > excludeyear and tmaxdeschist.index(round(mean(clmt[y]["tmax"]),1)) <= tmaxaschist.index(round(mean(clmt[y]["tmax"]),1)) else print("",end="")
            print(", Rank: {} Coolest".format(rank(tmaxaschist.index(round(mean(clmt[y]["tmax"]),1))+1))) if len(clmt[y]["tmax"]) > excludeyear and tmaxaschist.index(round(mean(clmt[y]["tmax"]),1)) <= tmaxdeschist.index(round(mean(clmt[y]["tmax"]),1)) else print("")
        except: print(" Avg MAX Temperature: N/A")
        if clmt[y]["tmaxPROP"]["day_max"][0] != -999:
            print(" -- Warmest Daily TMAX: {}".format(clmt[y]["tmaxPROP"]["day_max"][0]),end = " ::: ")
            for x in clmt[y]["tmaxPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end=" ") if x != clmt[y]["tmaxPROP"]["day_max"][1][len(clmt[y]["tmaxPROP"]["day_max"][1])-1] else print("{}".format(x.daystr))
        if clmt[y]["tmaxPROP"]["day_min"][0] != -999:
            print(" -- Coolest Daily TMAX: {}".format(clmt[y]["tmaxPROP"]["day_min"][0]),end = " ::: ")
            for x in clmt[y]["tmaxPROP"]["day_min"][1]: print("{}, ".format(x.daystr), end=" ") if x != clmt[y]["tmaxPROP"]["day_min"][1][len(clmt[y]["tmaxPROP"]["day_min"][1])-1] else print("{}".format(x.daystr))

        try:
            print(" Avg MIN Temperature: {}".format(round(mean(clmt[y]["tmin"]),1)),end="")
            print(", Rank: {} Warmest".format(rank(tmindeschist.index(round(mean(clmt[y]["tmin"]),1))+1)),end="") if len(clmt[y]["tmin"]) > excludeyear and tmindeschist.index(round(mean(clmt[y]["tmin"]),1)) <= tminaschist.index(round(mean(clmt[y]["tmin"]),1)) else print("",end="")
            print(", Rank: {} Coolest".format(rank(tminaschist.index(round(mean(clmt[y]["tmin"]),1))+1))) if len(clmt[y]["tmin"]) > excludeyear and tminaschist.index(round(mean(clmt[y]["tmin"]),1)) <= tmindeschist.index(round(mean(clmt[y]["tmin"]),1)) else print("")
        except: print(" Avg MIN Temperature: N/A")
        if clmt[y]["tminPROP"]["day_max"][0] != -999:
            print(" -- Warmest Daily TMIN: {}".format(clmt[y]["tminPROP"]["day_max"][0]),end = " ::: ")
            for x in clmt[y]["tminPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end=" ") if x != clmt[y]["tminPROP"]["day_max"][1][len(clmt[y]["tminPROP"]["day_max"][1])-1] else print("{}".format(x.daystr))
        if clmt[y]["tminPROP"]["day_min"][0] != -999:
            print(" -- Coolest Daily TMIN: {}".format(clmt[y]["tminPROP"]["day_min"][0]),end = " ::: ")
            for x in clmt[y]["tminPROP"]["day_min"][1]: print("{}, ".format(x.daystr), end=" ") if x != clmt[y]["tminPROP"]["day_min"][1][len(clmt[y]["tminPROP"]["day_min"][1])-1] else print("{}".format(x.daystr))

        if all(len(x) == 0 for x in [clmt[y]["tempAVGlist"],clmt[y]["tmax"],clmt[y]["tmin"]]):
            print("*** No Reliable Temperature Data for {} {}".format(calendar.month_abbr,y))
        print("-----")

def seasonStats(y,season):
    """Report on recorded statistics for a meteorological season of interest
    from a specific year. It accepts only arguments for the inquired year,
    and season. The year must be an integer while the season must be in string
    format.

    seasonStats(YYYY,SEASON)
    
    EXAMPLE: seasonStats(1933,"winter") -> Returns a printout of stats from
                                           the Meteorological Winter of 1933
                                           (inclusive of December 1933 - 
                                           February of 1934)
    """
    if len(clmt) == 0: return print("* OOPS! Run the clmtAnalyze function first.")
    if y not in metclmt: return print("Meteorological Year {} Not Found! Try again!".format(y))
    if season.lower() not in ["spring","summer","fall","autumn","winter"]: return print("'{}' is not a valid season. Try again!".format(season))
    if season.lower() == "autumn": season = "fall"
    season = season.lower()     # Puts season into requisite lower case to match metclmt[y] season dictionaries
    m1 = metclmt[y][season]["valid"][0]
    m2 = metclmt[y][season]["valid"][1]
    m3 = metclmt[y][season]["valid"][2]
    
    prcpaschist, prcpdeschist, prcpDAYSaschist, prcpDAYSdeschist, snowaschist, snowdeschist, snowDAYSaschist, snowDAYSdeschist, tmaxaschist, tmaxdeschist, tminaschist, tmindeschist, tavgaschist, tavgdeschist = seasonRank(season,"temp",5,seasonStatsRun=True)
    #for x in [prcpaschist, prcpdeschist, snowaschist, snowdeschist, tmaxaschist, tmaxdeschist, tminaschist, tmindeschist, tavgaschist, tavgdeschist]: print(len(x))
    #for x in [prcpaschist, prcpdeschist, snowaschist, snowdeschist, tmaxaschist, tmaxdeschist, tminaschist, tmindeschist, tavgaschist, tavgdeschist]: print(x)
    try:
        snwdDAYSdeschist = sorted(set(list(metclmt[YR][season]["snwdDAYS"] for YR in [Y for Y in metclmt if type(Y) == int] if metclmt[YR][season]["snwdDAYS"] != 0)),reverse=True)
        snwdDAYSaschist = sorted(set(list(metclmt[YR][season]["snwdDAYS"] for YR in [Y for Y in metclmt if type(Y) == int] if metclmt[YR][season]["recordqty"] > excludeyear)))
    except Exception as e: print(e)
    
    print("{:-^40}".format(""))
    if season == "winter": print("{:^40}".format("Seasonal Statistics for Meteorological {} {}-{}".format(season.capitalize(),y,str(y+1)[2:])))
    else: print("{:^40}".format("Seasonal Statistics for Meteorological {} {}".format(season.capitalize(),y)))
    print("{:^40}".format("{}: {}".format(metclmt["station"],metclmt["station_name"])))
    print("{:^40}".format("Quantity of Records: {}".format(metclmt[y][season]["recordqty"])))
    if metclmt[y][season]["recordqty"] <= excludeseason:
        print("{:-^40}".format(""))
        print("*** SEASONAL STATS LIKELY NOT COMPLETE FOR RELIANCE ON STATISTICS ***")
    print("{:-^40}".format(""))
    # metclmt[YYYY][s]["valid"] = [3,4,5]
    print("{:^6}|{:^10}|{:^10}|{:^10}|".format(
        "",
        "{} {}".format(calendar.month_abbr[m1].upper(),y) if m1 in [3,4,5,6,7,8,9,10,11,12] else "{} {}".format(calendar.month_abbr[m1].upper(),y+1),
        "{} {}".format(calendar.month_abbr[m2].upper(),y) if m2 in [3,4,5,6,7,8,9,10,11,12] else "{} {}".format(calendar.month_abbr[m2].upper(),y+1),
        "{} {}".format(calendar.month_abbr[m3].upper(),y) if m3 in [3,4,5,6,7,8,9,10,11,12] else "{} {}".format(calendar.month_abbr[m3].upper(),y+1)
    ))
    print("{:^6}|{:>8}  |{:>8}  |{:>8}  |".format(
        "PRCP",
        "{:.2f}".format(round(sum(metclmt[y][m1]["prcp"]),2)) if m1 in metclmt[y] else "",
        "{:.2f}".format(round(sum(metclmt[y][m2]["prcp"]),2)) if m2 in metclmt[y] else "",
        "{:.2f}".format(round(sum(metclmt[y][m3]["prcp"]),2)) if m3 in metclmt[y] else ""
    ))
    print("{:^6}|{:>8}  |{:>8}  |{:>8}  |".format(
        "SNOW",
        "{:.1f}".format(round(sum(metclmt[y][m1]["snow"]),1)) if m1 in metclmt[y] and (sum(metclmt[y][m1]["snow"]) > 0 or metclmt[y][m1]["snowDAYS"] > 0) else (" -- " if m1 in metclmt[y] and sum(metclmt[y][m1]["snow"]) == 0 else ""),
        "{:.1f}".format(round(sum(metclmt[y][m2]["snow"]),1)) if m2 in metclmt[y] and (sum(metclmt[y][m2]["snow"]) > 0 or metclmt[y][m2]["snowDAYS"] > 0) else (" -- " if m2 in metclmt[y] and sum(metclmt[y][m2]["snow"]) == 0 else ""),
        "{:.1f}".format(round(sum(metclmt[y][m3]["snow"]),1)) if m3 in metclmt[y] and (sum(metclmt[y][m3]["snow"]) > 0 or metclmt[y][m3]["snowDAYS"] > 0) else (" -- " if m3 in metclmt[y] and sum(metclmt[y][m3]["snow"]) == 0 else "")
    ))
    print("{:^6}|{:>8}  |{:>8}  |{:>8}  |".format(
        "TAVG",
        "{:.1f}".format(round(mean(metclmt[y][m1]["tempAVGlist"]),1)) if m1 in metclmt[y] and len(metclmt[y][m1]["tempAVGlist"]) > 2 else "",
        "{:.1f}".format(round(mean(metclmt[y][m2]["tempAVGlist"]),1)) if m2 in metclmt[y] and len(metclmt[y][m2]["tempAVGlist"]) > 2 else "",
        "{:.1f}".format(round(mean(metclmt[y][m3]["tempAVGlist"]),1)) if m3 in metclmt[y] and len(metclmt[y][m3]["tempAVGlist"]) > 2 else ""
    ))
    print("{:^6}|{:>8}  |{:>8}  |{:>8}  |".format(
        "TMAX",
        "{:.1f}".format(round(mean(metclmt[y][m1]["tmax"]),1)) if m1 in metclmt[y] and len(metclmt[y][m1]["tmax"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][m2]["tmax"]),1)) if m2 in metclmt[y] and len(metclmt[y][m2]["tmax"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][m3]["tmax"]),1)) if m3 in metclmt[y] and len(metclmt[y][m3]["tmax"]) > 1 else ""
    ))
    print("{:^6}|{:>8}  |{:>8}  |{:>8}  |".format(
        "TMIN",
        "{:.1f}".format(round(mean(metclmt[y][m1]["tmin"]),1)) if m1 in metclmt[y] and len(metclmt[y][m1]["tmin"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][m2]["tmin"]),1)) if m2 in metclmt[y] and len(metclmt[y][m2]["tmin"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][m3]["tmin"]),1)) if m3 in metclmt[y] and len(metclmt[y][m3]["tmin"]) > 1 else ""
    ))
    print("{:-^40}".format(""))

    print(" Total Precipitation: {}".format(round(sum(metclmt[y][season]["prcp"]),2)),end="")
    try: print(", Rank: {} Wettest".format(rank(prcpdeschist.index(round(sum(metclmt[y][season]["prcp"]),2))+1)),end="") if sum(metclmt[y][season]["prcp"]) > 0 and prcpdeschist.index(round(sum(metclmt[y][season]["prcp"]),2)) <= prcpaschist.index(round(sum(metclmt[y][season]["prcp"]),2)) else print("",end="")
    except: print(", Rank: {} Wettest".format(rank(prcpdeschist.index(round(sum(metclmt[y][season]["prcp"]),2))+1)),end="")
    try: print(", Rank: {} Driest".format(rank(prcpaschist.index(round(sum(metclmt[y][season]["prcp"]),2))+1))) if metclmt[y][season]["recordqty"] > excludeseason and prcpaschist.index(round(sum(metclmt[y][season]["prcp"]),2)) <= prcpdeschist.index(round(sum(metclmt[y][season]["prcp"]),2)) else print("")
    except: print("")

    print(" Total Precipitation Days (>=T): {}".format(metclmt[y][season]["prcpDAYS"]),end="")
    try: print(", Rank: {} Most".format(rank(prcpDAYSdeschist.index(metclmt[y][season]["prcpDAYS"])+1)),end="") if metclmt[y][season]["prcpDAYS"] > 0 and prcpDAYSdeschist.index(metclmt[y][season]["prcpDAYS"]) <= prcpDAYSaschist.index(metclmt[y][season]["prcpDAYS"]) else print("",end="")
    except: print(", Rank: {} Most".format(rank(prcpDAYSdeschist.index(metclmt[y][season]["prcpDAYS"])+1)),end="")
    try: print(", Rank: {} Least".format(rank(prcpDAYSaschist.index(metclmt[y][season]["prcpDAYS"])+1))) if prcpDAYSaschist.index(metclmt[y][season]["prcpDAYS"]) <= prcpDAYSdeschist.index(metclmt[y][season]["prcpDAYS"]) else print("")
    except: print("")
    if round(sum(metclmt[y][season]["prcp"]),2) > 0:
        print(" -- Highest Daily Precip: {}".format(metclmt[y][season]["prcpPROP"]["day_max"][0]),end=" ::: ")
        for x in range(len(metclmt[y][season]["prcpPROP"]["day_max"][1])):
            if x != len(metclmt[y][season]["prcpPROP"]["day_max"][1])-1: print("{},".format(metclmt[y][season]["prcpPROP"]["day_max"][1][x].daystr),end=" ")
            else: print("{}".format(metclmt[y][season]["prcpPROP"]["day_max"][1][x].daystr))

    if round(sum(metclmt[y][season]["snow"]),1) > 0 or metclmt[y][season]["snowDAYS"] > 0:
        print(" Total Snow: {}".format(round(sum(metclmt[y][season]["snow"]),1)),end="")
        try: print(", Rank: {} Snowiest".format(rank(snowdeschist.index(round(sum(metclmt[y][season]["snow"]),1))+1)),end="") if sum(metclmt[y][season]["snow"]) > 0 and snowdeschist.index(round(sum(metclmt[y][season]["snow"]),1)) <= snowaschist.index(round(sum(metclmt[y][season]["snow"]),1)) else print("",end="")
        except: print(", Rank: {} Snowiest".format(rank(snowdeschist.index(round(sum(metclmt[y][season]["snow"]),1))+1)),end="")
        try: print(", Rank: {} Least-Snowiest".format(rank(snowaschist.index(round(sum(metclmt[y][season]["snow"]),1))+1))) if metclmt[y][season]["recordqty"] > excludeseason and snowaschist.index(round(sum(metclmt[y][season]["snow"]),1)) <= snowdeschist.index(round(sum(metclmt[y][season]["snow"]),1)) else print("")
        except: print("")

        print(" Total Snow Days (>=T): {}".format(metclmt[y][season]["snowDAYS"]),end="")
        try: print(", Rank: {} Most".format(rank(snowDAYSdeschist.index(metclmt[y][season]["snowDAYS"])+1)),end="") if metclmt[y][season]["snowDAYS"] > 0 and snowDAYSdeschist.index(metclmt[y][season]["snowDAYS"]) <= snowDAYSaschist.index(metclmt[y][season]["snowDAYS"]) else print("",end="")
        except: print(", Rank: {} Most".format(rank(snowDAYSdeschist.index(metclmt[y][season]["snowDAYS"])+1)),end="")
        try: print(", Rank: {} Least".format(rank(snowDAYSaschist.index(metclmt[y][season]["snowDAYS"])+1))) if metclmt[y][season]["recordqty"] > excludeseason and snowDAYSaschist.index(metclmt[y][season]["snowDAYS"]) <= snowDAYSdeschist.index(metclmt[y][season]["snowDAYS"]) else print("")
        except: print("")
        if metclmt[y][season]["snowPROP"]["day_max"][0] > 0:
            print(" -- Highest Daily Snow: {}".format(metclmt[y][season]["snowPROP"]["day_max"][0]),end=" ::: ")
            for x in range(len(metclmt[y][season]["snowPROP"]["day_max"][1])):
                if x != len(metclmt[y][season]["snowPROP"]["day_max"][1])-1: print("{},".format(metclmt[y][season]["snowPROP"]["day_max"][1][x].daystr),end=" ")
                else: print("{}".format(metclmt[y][season]["snowPROP"]["day_max"][1][x].daystr))

    print(" Total Snow Days (>=T): {}".format(metclmt[y][season]["snowDAYS"]),end="")
    try: print(", Rank: {} Most".format(rank(snowDAYSdeschist.index(metclmt[y][season]["snowDAYS"])+1)),end="") if metclmt[y][season]["snowDAYS"] > 0 and snowDAYSdeschist.index(metclmt[y][season]["snowDAYS"]) <= snowDAYSaschist.index(metclmt[y][season]["snowDAYS"]) else print("",end="")
    except: print(", Rank: {} Most".format(rank(snowDAYSdeschist.index(metclmt[y][season]["snowDAYS"])+1)),end="")
    try: print(", Rank: {} Least".format(rank(snowDAYSaschist.index(metclmt[y][season]["snowDAYS"])+1))) if metclmt[y][season]["recordqty"] > excludeyear and snowDAYSaschist.index(metclmt[y][season]["snowDAYS"]) <= snowDAYSdeschist.index(metclmt[y][season]["snowDAYS"]) else print("")
    except: print("")

    if metclmt[y][season]["snwdDAYS"] > 0:
        print(" Total Days w/Snow on the Ground (>=T): {}".format(metclmt[y][season]["snwdDAYS"]),end="")
        try: print(", Rank: {} Most".format(rank(snwdDAYSdeschist.index(metclmt[y][season]["snwdDAYS"])+1)),end="") if metclmt[y][season]["snwdDAYS"] > 0 and snwdDAYSdeschist.index(metclmt[y][season]["snwdDAYS"]) <= snwdDAYSaschist.index(metclmt[y][season]["snwdDAYS"]) else print("",end="")
        except: print(", Rank: {} Most".format(rank(snwdDAYSdeschist.index(metclmt[y][season]["snwdDAYS"])+1)),end="")
        try: print(", Rank: {} Least".format(rank(snwdDAYSaschist.index(metclmt[y][season]["snwdDAYS"])+1))) if metclmt[y][season]["recordqty"] > excludeyear and snwdDAYSaschist.index(metclmt[y][season]["snwdDAYS"]) <= snwdDAYSdeschist.index(metclmt[y][season]["snwdDAYS"]) else print("")
        except: print("")
    if round(sum(metclmt[y][season]["snwd"]),1) > 0:
        print(" -- Highest Daily Snow-Depth: {}".format(metclmt[y][season]["snwdPROP"]["day_max"][0]),end = " ::: ")
        for x in metclmt[y][season]["snwdPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end=" ") if x != metclmt[y][season]["snwdPROP"]["day_max"][1][len(metclmt[y][season]["snwdPROP"]["day_max"][1])-1] else print("{}".format(x.daystr))


    if len(metclmt[y][season]["tempAVGlist"]) <= excludeseason_tavg and metclmt[y][season]["recordqty"] > excludeseason:
        print("{:-^55}".format(""))
        print("*** INSUFFICIENT TEMPERATURE DATA FOR SEASON LIKELY ***")
        print("{:-^55}".format(""))
    try:
        print(" Average Temperature: {}".format(round(mean(metclmt[y][season]["tempAVGlist"]),1)),end="")
        print(", Rank: {} Warmest".format(rank(tavgdeschist.index(round(mean(metclmt[y][season]["tempAVGlist"]),1))+1)),end="") if len(metclmt[y][season]["tempAVGlist"]) > excludeseason*2 and tavgdeschist.index(round(mean(metclmt[y][season]["tempAVGlist"]),1)) <= tavgaschist.index(round(mean(metclmt[y][season]["tempAVGlist"]),1)) else print("",end="")
        print(", Rank: {} Coolest".format(rank(tavgaschist.index(round(mean(metclmt[y][season]["tempAVGlist"]),1))+1))) if len(metclmt[y][season]["tempAVGlist"]) > excludeseason*2 and tavgaschist.index(round(mean(metclmt[y][season]["tempAVGlist"]),1)) <= tavgdeschist.index(round(mean(metclmt[y][season]["tempAVGlist"]),1)) else print("")
    except: print(" Average Temperature: N/A")

    try:
        print(" Avg MAX Temperature: {}".format(round(mean(metclmt[y][season]["tmax"]),1)),end="")
        print(", Rank: {} Warmest".format(rank(tmaxdeschist.index(round(mean(metclmt[y][season]["tmax"]),1))+1)),end="") if len(metclmt[y][season]["tmax"]) > excludeseason and tmaxdeschist.index(round(mean(metclmt[y][season]["tmax"]),1)) <= tmaxaschist.index(round(mean(metclmt[y][season]["tmax"]),1)) else print("",end="")
        print(", Rank: {} Coolest".format(rank(tmaxaschist.index(round(mean(metclmt[y][season]["tmax"]),1))+1))) if len(metclmt[y][season]["tmax"]) > excludeseason and tmaxaschist.index(round(mean(metclmt[y][season]["tmax"]),1)) <= tmaxdeschist.index(round(mean(metclmt[y][season]["tmax"]),1)) else print("")
    except: print(" Avg MAX Temperature: N/A")
    if metclmt[y][season]["tmaxPROP"]["day_max"][0] != -999:
        print(" -- Warmest Daily TMAX: {}".format(metclmt[y][season]["tmaxPROP"]["day_max"][0]),end = " ::: ")
        for x in metclmt[y][season]["tmaxPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end=" ") if x != metclmt[y][season]["tmaxPROP"]["day_max"][1][len(metclmt[y][season]["tmaxPROP"]["day_max"][1])-1] else print("{}".format(x.daystr))
    if metclmt[y][season]["tmaxPROP"]["day_min"][0] != -999:
        print(" -- Coolest Daily TMAX: {}".format(metclmt[y][season]["tmaxPROP"]["day_min"][0]),end = " ::: ")
        for x in metclmt[y][season]["tmaxPROP"]["day_min"][1]: print("{}, ".format(x.daystr), end=" ") if x != metclmt[y][season]["tmaxPROP"]["day_min"][1][len(metclmt[y][season]["tmaxPROP"]["day_min"][1])-1] else print("{}".format(x.daystr))

    try:
        print(" Avg MIN Temperature: {}".format(round(mean(metclmt[y][season]["tmin"]),1)),end="")
        print(", Rank: {} Warmest".format(rank(tmindeschist.index(round(mean(metclmt[y][season]["tmin"]),1))+1)),end="") if len(metclmt[y][season]["tmin"]) > excludeseason and tmindeschist.index(round(mean(metclmt[y][season]["tmin"]),1)) <= tminaschist.index(round(mean(metclmt[y][season]["tmin"]),1)) else print("",end="")
        print(", Rank: {} Coolest".format(rank(tminaschist.index(round(mean(metclmt[y][season]["tmin"]),1))+1))) if len(metclmt[y][season]["tmin"]) > excludeseason and tminaschist.index(round(mean(metclmt[y][season]["tmin"]),1)) <= tmindeschist.index(round(mean(metclmt[y][season]["tmin"]),1)) else print("")
    except: print(" Avg MIN Temperature: N/A")
    if metclmt[y][season]["tminPROP"]["day_max"][0] != -999:
        print(" -- Warmest Daily TMIN: {}".format(metclmt[y][season]["tminPROP"]["day_max"][0]),end = " ::: ")
        for x in metclmt[y][season]["tminPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end=" ") if x != metclmt[y][season]["tminPROP"]["day_max"][1][len(metclmt[y][season]["tminPROP"]["day_max"][1])-1] else print("{}".format(x.daystr))
    if metclmt[y][season]["tminPROP"]["day_min"][0] != -999:
        print(" -- Coolest Daily TMIN: {}".format(metclmt[y][season]["tminPROP"]["day_min"][0]),end = " ::: ")
        for x in metclmt[y][season]["tminPROP"]["day_min"][1]: print("{}, ".format(x.daystr), end=" ") if x != metclmt[y][season]["tminPROP"]["day_min"][1][len(metclmt[y][season]["tminPROP"]["day_min"][1])-1] else print("{}".format(x.daystr))

    print("-----")

def metYearStats(y):
    """Report on recorded statistics for a meteorological year of interest. It
    only accepts an argument for the inquired year. Meteorological years run 
    from March to February of the following year (Spring to Winter).The year
    must be an integer.
    
    metYearStats(YYYY)
    
    EXAMPLE: metYearStats(1985) -> Returns a printout of stats from the
                                           Meteorological Year of 1985 
                                           (inclusive of March 1985 - 
                                           February of 1986)
    """
    if len(metclmt) == 0: return print("* OOPS! Run the clmtAnalyze function first.")
    if y not in metclmt: return print("* A record for {} not found in metclmt *".format(y))

    prcpaschist, prcpdeschist, prcpDAYSaschist, prcpDAYSdeschist, snowaschist, snowdeschist, snowDAYSaschist, snowDAYSdeschist, tmaxaschist, tmaxdeschist, tminaschist, tmindeschist, tavgaschist, tavgdeschist = metYearRank("temps",5,yearStatsRun=True)
    try:
        snwdDAYSdeschist = sorted(set(list(metclmt[YR]["snwdDAYS"] for YR in [Y for Y in metclmt if type(Y) == int] if metclmt[YR]["snwdDAYS"] != 0)),reverse=True)
        snwdDAYSaschist = sorted(set(list(metclmt[YR]["snwdDAYS"] for YR in [Y for Y in metclmt if type(Y) == int] if metclmt[YR]["recordqty"] > excludeyear)))
    except Exception as e: print(e)

    print("")
    print("{:^73}".format("Statistics for Meteorological Year {}".format(y)))
    print("{:^73}".format("{}: {}".format(clmt["station"],clmt["station_name"])))
    print("{:^73}".format("Quantity of Records: {}".format(clmt[y]["recordqty"])))
    if metclmt[y]["recordqty"] <= excludeyear:
        print("{:-^73}".format(""))
        print("*** MET. YEAR STATS MAY NOT BE COMPLETE FOR RELIANCE ON STATISTICS ***")
    print("{:-^73}".format(""))
    print("{:^6}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|".format("","MAR {}".format(y),"APR {}".format(y),"MAY {}".format(y),"JUN {}".format(y),"JUL {}".format(y),"AUG {}".format(y)))
    print("{:-^73}".format(""))
    print("{:^6}|{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |".format(
        "PRCP",
        "{:.2f}".format(round(sum(metclmt[y][3]["prcp"]),2)) if 3 in metclmt[y] else "",
        "{:.2f}".format(round(sum(metclmt[y][4]["prcp"]),2)) if 4 in metclmt[y] else "",
        "{:.2f}".format(round(sum(metclmt[y][5]["prcp"]),2)) if 5 in metclmt[y] else "",
        "{:.2f}".format(round(sum(metclmt[y][6]["prcp"]),2)) if 6 in metclmt[y] else "",
        "{:.2f}".format(round(sum(metclmt[y][7]["prcp"]),2)) if 7 in metclmt[y] else "",
        "{:.2f}".format(round(sum(metclmt[y][8]["prcp"]),2)) if 8 in metclmt[y] else "",
    ))
    print("{:^6}|{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |".format(
        "SNOW",
        "{:.1f}".format(round(sum(metclmt[y][3]["snow"]),1)) if 3 in metclmt[y] and (sum(metclmt[y][3]["snow"]) > 0 or metclmt[y][3]["snowDAYS"] > 0) else (" -- " if 3 in metclmt[y] and sum(metclmt[y][3]["snow"]) == 0 else ""),
        "{:.1f}".format(round(sum(metclmt[y][4]["snow"]),1)) if 4 in metclmt[y] and (sum(metclmt[y][4]["snow"]) > 0 or metclmt[y][4]["snowDAYS"] > 0) else (" -- " if 4 in metclmt[y] and sum(metclmt[y][4]["snow"]) == 0 else ""),
        "{:.1f}".format(round(sum(metclmt[y][5]["snow"]),1)) if 5 in metclmt[y] and (sum(metclmt[y][5]["snow"]) > 0 or metclmt[y][5]["snowDAYS"] > 0) else (" -- " if 5 in metclmt[y] and sum(metclmt[y][5]["snow"]) == 0 else ""),
        "{:.1f}".format(round(sum(metclmt[y][6]["snow"]),1)) if 6 in metclmt[y] and (sum(metclmt[y][6]["snow"]) > 0 or metclmt[y][6]["snowDAYS"] > 0) else (" -- " if 6 in metclmt[y] and sum(metclmt[y][6]["snow"]) == 0 else ""),
        "{:.1f}".format(round(sum(metclmt[y][7]["snow"]),1)) if 7 in metclmt[y] and (sum(metclmt[y][7]["snow"]) > 0 or metclmt[y][7]["snowDAYS"] > 0) else (" -- " if 7 in metclmt[y] and sum(metclmt[y][7]["snow"]) == 0 else ""),
        "{:.1f}".format(round(sum(metclmt[y][8]["snow"]),1)) if 8 in metclmt[y] and (sum(metclmt[y][8]["snow"]) > 0 or metclmt[y][8]["snowDAYS"] > 0) else (" -- " if 8 in metclmt[y] and sum(metclmt[y][8]["snow"]) == 0 else ""),
    ))
    print("{:^6}|{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |".format(
        "TAVG",
        "{:.1f}".format(round(mean(metclmt[y][3]["tempAVGlist"]),1)) if 3 in metclmt[y] and len(metclmt[y][3]["tempAVGlist"]) > 2 else "",
        "{:.1f}".format(round(mean(metclmt[y][4]["tempAVGlist"]),1)) if 4 in metclmt[y] and len(metclmt[y][4]["tempAVGlist"]) > 2 else "",
        "{:.1f}".format(round(mean(metclmt[y][5]["tempAVGlist"]),1)) if 5 in metclmt[y] and len(metclmt[y][5]["tempAVGlist"]) > 2 else "",
        "{:.1f}".format(round(mean(metclmt[y][6]["tempAVGlist"]),1)) if 6 in metclmt[y] and len(metclmt[y][6]["tempAVGlist"]) > 2 else "",
        "{:.1f}".format(round(mean(metclmt[y][7]["tempAVGlist"]),1)) if 7 in metclmt[y] and len(metclmt[y][7]["tempAVGlist"]) > 2 else "",
        "{:.1f}".format(round(mean(metclmt[y][8]["tempAVGlist"]),1)) if 8 in metclmt[y] and len(metclmt[y][8]["tempAVGlist"]) > 2 else "",
    ))
    print("{:^6}|{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |".format(
        "TMAX",
        "{:.1f}".format(round(mean(metclmt[y][3]["tmax"]),1)) if 3 in metclmt[y] and len(metclmt[y][3]["tmax"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][4]["tmax"]),1)) if 4 in metclmt[y] and len(metclmt[y][4]["tmax"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][5]["tmax"]),1)) if 5 in metclmt[y] and len(metclmt[y][5]["tmax"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][6]["tmax"]),1)) if 6 in metclmt[y] and len(metclmt[y][6]["tmax"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][7]["tmax"]),1)) if 7 in metclmt[y] and len(metclmt[y][7]["tmax"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][8]["tmax"]),1)) if 8 in metclmt[y] and len(metclmt[y][8]["tmax"]) > 1 else "",
    ))
    print("{:^6}|{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |".format(
        "TMIN",
        "{:.1f}".format(round(mean(metclmt[y][3]["tmin"]),1)) if 3 in metclmt[y] and len(metclmt[y][3]["tmin"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][4]["tmin"]),1)) if 4 in metclmt[y] and len(metclmt[y][4]["tmin"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][5]["tmin"]),1)) if 5 in metclmt[y] and len(metclmt[y][5]["tmin"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][6]["tmin"]),1)) if 6 in metclmt[y] and len(metclmt[y][6]["tmin"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][7]["tmin"]),1)) if 7 in metclmt[y] and len(metclmt[y][7]["tmin"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][8]["tmin"]),1)) if 8 in metclmt[y] and len(metclmt[y][8]["tmin"]) > 1 else "",
    ))
    print("{:-^73}".format(""))
    print("{:^6}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|".format("","SEP {}".format(y),"OCT {}".format(y),"NOV {}".format(y),"DEC {}".format(y),"JAN {}".format(y+1),"FEB {}".format(y+1)))
    print("{:-^73}".format(""))
    print("{:^6}|{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |".format(
        "PRCP",
        "{:.2f}".format(round(sum(metclmt[y][9]["prcp"]),2)) if 9 in metclmt[y] else "",
        "{:.2f}".format(round(sum(metclmt[y][10]["prcp"]),2)) if 10 in metclmt[y] else "",
        "{:.2f}".format(round(sum(metclmt[y][11]["prcp"]),2)) if 11 in metclmt[y] else "",
        "{:.2f}".format(round(sum(metclmt[y][12]["prcp"]),2)) if 12 in metclmt[y] else "",
        "{:.2f}".format(round(sum(metclmt[y][1]["prcp"]),2)) if 1 in metclmt[y] else "",
        "{:.2f}".format(round(sum(metclmt[y][2]["prcp"]),2)) if 2 in metclmt[y] else "",
    ))
    print("{:^6}|{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |".format(
        "SNOW",
        "{:.1f}".format(round(sum(metclmt[y][9]["snow"]),1)) if 9 in metclmt[y] and (sum(metclmt[y][9]["snow"]) > 0 or metclmt[y][9]["snowDAYS"] > 0) else (" -- " if 9 in metclmt[y] and sum(metclmt[y][9]["snow"]) == 0 else ""),
        "{:.1f}".format(round(sum(metclmt[y][10]["snow"]),1)) if 10 in metclmt[y] and (sum(metclmt[y][10]["snow"]) > 0 or metclmt[y][10]["snowDAYS"] > 0) else (" -- " if 10 in metclmt[y] and sum(metclmt[y][10]["snow"]) == 0 else ""),
        "{:.1f}".format(round(sum(metclmt[y][11]["snow"]),1)) if 11 in metclmt[y] and (sum(metclmt[y][11]["snow"]) > 0 or metclmt[y][11]["snowDAYS"] > 0) else (" -- " if 11 in metclmt[y] and sum(metclmt[y][11]["snow"]) == 0 else ""),
        "{:.1f}".format(round(sum(metclmt[y][12]["snow"]),1)) if 12 in metclmt[y] and (sum(metclmt[y][12]["snow"]) > 0 or metclmt[y][12]["snowDAYS"] > 0) else (" -- " if 12 in metclmt[y] and sum(metclmt[y][12]["snow"]) == 0 else ""),
        "{:.1f}".format(round(sum(metclmt[y][1]["snow"]),1)) if 1 in metclmt[y] and (sum(metclmt[y][1]["snow"]) > 0 or metclmt[y][1]["snowDAYS"] > 0) else (" -- " if 1 in metclmt[y] and sum(metclmt[y][1]["snow"]) == 0 else ""),
        "{:.1f}".format(round(sum(metclmt[y][2]["snow"]),1)) if 2 in metclmt[y] and (sum(metclmt[y][2]["snow"]) > 0 or metclmt[y][2]["snowDAYS"] > 0) else (" -- " if 2 in metclmt[y] and sum(metclmt[y][2]["snow"]) == 0 else ""),
    ))
    print("{:^6}|{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |".format(
        "TAVG",
        "{:.1f}".format(round(mean(metclmt[y][9]["tempAVGlist"]),1)) if 9 in metclmt[y] and len(metclmt[y][9]["tempAVGlist"]) > 2 else "",
        "{:.1f}".format(round(mean(metclmt[y][10]["tempAVGlist"]),1)) if 10 in metclmt[y] and len(metclmt[y][10]["tempAVGlist"]) > 2 else "",
        "{:.1f}".format(round(mean(metclmt[y][11]["tempAVGlist"]),1)) if 11 in metclmt[y] and len(metclmt[y][11]["tempAVGlist"]) > 2 else "",
        "{:.1f}".format(round(mean(metclmt[y][12]["tempAVGlist"]),1)) if 12 in metclmt[y] and len(metclmt[y][12]["tempAVGlist"]) > 2 else "",
        "{:.1f}".format(round(mean(metclmt[y][1]["tempAVGlist"]),1)) if 1 in metclmt[y] and len(metclmt[y][1]["tempAVGlist"]) > 2 else "",
        "{:.1f}".format(round(mean(metclmt[y][2]["tempAVGlist"]),1)) if 2 in metclmt[y] and len(metclmt[y][2]["tempAVGlist"]) > 2 else "",
    ))
    print("{:^6}|{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |".format(
        "TMAX",
        "{:.1f}".format(round(mean(metclmt[y][9]["tmax"]),1)) if 9 in metclmt[y] and len(metclmt[y][9]["tmax"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][10]["tmax"]),1)) if 10 in metclmt[y] and len(metclmt[y][10]["tmax"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][11]["tmax"]),1)) if 11 in metclmt[y] and len(metclmt[y][11]["tmax"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][12]["tmax"]),1)) if 12 in metclmt[y] and len(metclmt[y][12]["tmax"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][1]["tmax"]),1)) if 1 in metclmt[y] and len(metclmt[y][1]["tmax"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][2]["tmax"]),1)) if 2 in metclmt[y] and len(metclmt[y][2]["tmax"]) > 1 else "",
    ))
    print("{:^6}|{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |{:>8}  |".format(
        "TMIN",
        "{:.1f}".format(round(mean(metclmt[y][9]["tmin"]),1)) if 9 in metclmt[y] and len(metclmt[y][9]["tmin"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][10]["tmin"]),1)) if 10 in metclmt[y] and len(metclmt[y][10]["tmin"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][11]["tmin"]),1)) if 11 in metclmt[y] and len(metclmt[y][11]["tmin"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][12]["tmin"]),1)) if 12 in metclmt[y] and len(metclmt[y][12]["tmin"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][1]["tmin"]),1)) if 1 in metclmt[y] and len(metclmt[y][1]["tmin"]) > 1 else "",
        "{:.1f}".format(round(mean(metclmt[y][2]["tmin"]),1)) if 2 in metclmt[y] and len(metclmt[y][2]["tmin"]) > 1 else "",
    ))
    print("{:-^73}".format(""))

    print(" Total Precipitation: {}".format(round(sum(metclmt[y]["prcp"]),2)),end="")
    try: print(", Rank: {} Wettest".format(rank(prcpdeschist.index(round(sum(metclmt[y]["prcp"]),2))+1)),end="") if sum(metclmt[y]["prcp"]) > 0 and prcpdeschist.index(round(sum(metclmt[y]["prcp"]),2)) <= prcpaschist.index(round(sum(metclmt[y]["prcp"]),2)) else print("",end="")
    except: print(", Rank: {} Wettest".format(rank(prcpdeschist.index(round(sum(metclmt[y]["prcp"]),2))+1)),end="")
    try: print(", Rank: {} Driest".format(rank(prcpaschist.index(round(sum(metclmt[y]["prcp"]),2))+1))) if metclmt[y]["recordqty"] > excludeyear and prcpaschist.index(round(sum(metclmt[y]["prcp"]),2)) <= prcpdeschist.index(round(sum(metclmt[y]["prcp"]),2)) else print("")
    except: print("")

    print(" Total Precipitation Days (>=T): {}".format(metclmt[y]["prcpDAYS"]),end="")
    try: print(", Rank: {} Most".format(rank(prcpDAYSdeschist.index(metclmt[y]["prcpDAYS"])+1)),end="") if metclmt[y]["prcpDAYS"] > 0 and prcpDAYSdeschist.index(metclmt[y]["prcpDAYS"]) <= prcpDAYSaschist.index(metclmt[y]["prcpDAYS"]) else print("",end="")
    except: print(", Rank: {} Most".format(rank(prcpDAYSdeschist.index(metclmt[y]["prcpDAYS"])+1)),end="")
    try: print(", Rank: {} Least".format(rank(prcpDAYSaschist.index(metclmt[y]["prcpDAYS"])+1))) if prcpDAYSaschist.index(metclmt[y]["prcpDAYS"]) <= prcpDAYSdeschist.index(metclmt[y]["prcpDAYS"]) else print("")
    except: print("")
    if round(sum(metclmt[y]["prcp"]),2) > 0:
        print(" -- Highest Daily Precip: {}".format(metclmt[y]["prcpPROP"]["day_max"][0]),end = " ::: ")
        for x in metclmt[y]["prcpPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end=" ") if x != metclmt[y]["prcpPROP"]["day_max"][1][len(metclmt[y]["prcpPROP"]["day_max"][1])-1] else print("{}".format(x.daystr))

    print(" Total Snow: {}".format(round(sum(metclmt[y]["snow"]),1)),end="")
    try: print(", Rank: {} Snowiest".format(rank(snowdeschist.index(round(sum(metclmt[y]["snow"]),1))+1)),end="") if sum(metclmt[y]["snow"]) > 0 and snowdeschist.index(round(sum(metclmt[y]["snow"]),1)) <= snowaschist.index(round(sum(metclmt[y]["snow"]),1)) else print("",end="")
    except: print(", Rank: {} Snowiest".format(rank(snowdeschist.index(round(sum(metclmt[y]["snow"]),1))+1)),end="")
    try: print(", Rank: {} Least-Snowiest".format(rank(snowaschist.index(round(sum(metclmt[y]["snow"]),1))+1))) if metclmt[y]["recordqty"] > excludeyear and snowaschist.index(round(sum(metclmt[y]["snow"]),1)) <= snowdeschist.index(round(sum(metclmt[y]["snow"]),1)) else print("")
    except: print("")

    print(" Total Snow Days (>=T): {}".format(metclmt[y]["snowDAYS"]),end="")
    try: print(", Rank: {} Most".format(rank(snowDAYSdeschist.index(metclmt[y]["snowDAYS"])+1)),end="") if metclmt[y]["snowDAYS"] > 0 and snowDAYSdeschist.index(metclmt[y]["snowDAYS"]) <= snowDAYSaschist.index(metclmt[y]["snowDAYS"]) else print("",end="")
    except: print(", Rank: {} Most".format(rank(snowDAYSdeschist.index(metclmt[y]["snowDAYS"])+1)),end="")
    try: print(", Rank: {} Least".format(rank(snowDAYSaschist.index(metclmt[y]["snowDAYS"])+1))) if metclmt[y]["recordqty"] > excludeyear and snowDAYSaschist.index(metclmt[y]["snowDAYS"]) <= snowDAYSdeschist.index(metclmt[y]["snowDAYS"]) else print("")
    except: print("")

    if metclmt[y]["snwdDAYS"] > 0:
        print(" Total Days w/Snow on the Ground (>=T): {}".format(metclmt[y]["snwdDAYS"]),end="")
        try: print(", Rank: {} Most".format(rank(snwdDAYSdeschist.index(metclmt[y]["snwdDAYS"])+1)),end="") if metclmt[y]["snwdDAYS"] > 0 and snwdDAYSdeschist.index(metclmt[y]["snwdDAYS"]) <= snwdDAYSaschist.index(metclmt[y]["snwdDAYS"]) else print("",end="")
        except: print(", Rank: {} Most".format(rank(snwdDAYSdeschist.index(metclmt[y]["snwdDAYS"])+1)),end="")
        try: print(", Rank: {} Least".format(rank(snwdDAYSaschist.index(metclmt[y]["snwdDAYS"])+1))) if metclmt[y]["recordqty"] > excludeyear and snwdDAYSaschist.index(metclmt[y]["snwdDAYS"]) <= snwdDAYSdeschist.index(metclmt[y]["snwdDAYS"]) else print("")
        except: print("")
    if round(sum(metclmt[y]["snwd"]),1) > 0:
        print(" -- Highest Daily Snow-Depth: {}".format(metclmt[y]["snwdPROP"]["day_max"][0]),end = " ::: ")
        for x in metclmt[y]["snwdPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end=" ") if x != metclmt[y]["snwdPROP"]["day_max"][1][len(metclmt[y]["snwdPROP"]["day_max"][1])-1] else print("{}".format(x.daystr))

    try:
        print(" Average Temperature: {}".format(round(mean(metclmt[y]["tempAVGlist"]),1)),end="")
        print(", Rank: {} Warmest".format(rank(tavgdeschist.index(round(mean(metclmt[y]["tempAVGlist"]),1))+1)),end="") if len(metclmt[y]["tempAVGlist"]) > excludeyear*2 and tavgdeschist.index(round(mean(metclmt[y]["tempAVGlist"]),1)) <= tavgaschist.index(round(mean(metclmt[y]["tempAVGlist"]),1)) else print("",end="")
        print(", Rank: {} Coolest".format(rank(tavgaschist.index(round(mean(metclmt[y]["tempAVGlist"]),1))+1))) if len(metclmt[y]["tempAVGlist"]) > excludeyear*2 and tavgaschist.index(round(mean(metclmt[y]["tempAVGlist"]),1)) <= tavgdeschist.index(round(mean(metclmt[y]["tempAVGlist"]),1)) else print("")
    except: print(" Average Temperature: N/A")

    try:
        print(" Avg MAX Temperature: {}".format(round(mean(metclmt[y]["tmax"]),1)),end="")
        print(", Rank: {} Warmest".format(rank(tmaxdeschist.index(round(mean(metclmt[y]["tmax"]),1))+1)),end="") if len(metclmt[y]["tmax"]) > excludeyear and tmaxdeschist.index(round(mean(metclmt[y]["tmax"]),1)) <= tmaxaschist.index(round(mean(metclmt[y]["tmax"]),1)) else print("",end="")
        print(", Rank: {} Coolest".format(rank(tmaxaschist.index(round(mean(metclmt[y]["tmax"]),1))+1))) if len(metclmt[y]["tmax"]) > excludeyear and tmaxaschist.index(round(mean(metclmt[y]["tmax"]),1)) <= tmaxdeschist.index(round(mean(metclmt[y]["tmax"]),1)) else print("")
    except: print(" Avg MAX Temperature: N/A")
    if metclmt[y]["tmaxPROP"]["day_max"][0] != -999:
        print(" -- Warmest Daily TMAX: {}".format(metclmt[y]["tmaxPROP"]["day_max"][0]),end = " ::: ")
        for x in metclmt[y]["tmaxPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end=" ") if x != metclmt[y]["tmaxPROP"]["day_max"][1][len(metclmt[y]["tmaxPROP"]["day_max"][1])-1] else print("{}".format(x.daystr))
    if metclmt[y]["tmaxPROP"]["day_min"][0] != -999:
        print(" -- Coolest Daily TMAX: {}".format(metclmt[y]["tmaxPROP"]["day_min"][0]),end = " ::: ")
        for x in metclmt[y]["tmaxPROP"]["day_min"][1]: print("{}, ".format(x.daystr), end=" ") if x != metclmt[y]["tmaxPROP"]["day_min"][1][len(metclmt[y]["tmaxPROP"]["day_min"][1])-1] else print("{}".format(x.daystr))

    try:
        print(" Avg MIN Temperature: {}".format(round(mean(metclmt[y]["tmin"]),1)),end="")
        print(", Rank: {} Warmest".format(rank(tmindeschist.index(round(mean(metclmt[y]["tmin"]),1))+1)),end="") if len(metclmt[y]["tmin"]) > excludeyear and tmindeschist.index(round(mean(metclmt[y]["tmin"]),1)) <= tminaschist.index(round(mean(metclmt[y]["tmin"]),1)) else print("",end="")
        print(", Rank: {} Coolest".format(rank(tminaschist.index(round(mean(metclmt[y]["tmin"]),1))+1))) if len(metclmt[y]["tmin"]) > excludeyear and tminaschist.index(round(mean(metclmt[y]["tmin"]),1)) <= tmindeschist.index(round(mean(metclmt[y]["tmin"]),1)) else print("")
    except: print(" Avg MIN Temperature: N/A")
    if metclmt[y]["tminPROP"]["day_max"][0] != -999:
        print(" -- Warmest Daily TMIN: {}".format(metclmt[y]["tminPROP"]["day_max"][0]),end = " ::: ")
        for x in metclmt[y]["tminPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end=" ") if x != metclmt[y]["tminPROP"]["day_max"][1][len(metclmt[y]["tminPROP"]["day_max"][1])-1] else print("{}".format(x.daystr))
    if metclmt[y]["tminPROP"]["day_min"][0] != -999:
        print(" -- Coolest Daily TMIN: {}".format(metclmt[y]["tminPROP"]["day_min"][0]),end = " ::: ")
        for x in metclmt[y]["tminPROP"]["day_min"][1]: print("{}, ".format(x.daystr), end=" ") if x != metclmt[y]["tminPROP"]["day_min"][1][len(metclmt[y]["tminPROP"]["day_min"][1])-1] else print("{}".format(x.daystr))

    if all(len(x) == 0 for x in [metclmt[y]["tempAVGlist"],metclmt[y]["tmax"],metclmt[y]["tmin"]]):
        print("*** No Reliable Temperature Data for {} {}".format(calendar.month_abbr,y))
    print("-----")

def customStats(y1,m1,d1,*date2):
    """Report on a custom-length period of recorded statistics. All passed
    arguments MUST be integers. If the optional ending arguments are not
    included, the default ending will be December 31 of the calendar year, 
    given by Y1; does not accept values of greater than a year
    
    customStats(Y1,M1,D1,*[Y2,M2,D2])
    
    REQUIRED: Y1,M1,D1 --> Represent the beginning year, month, and date of
                           the custom period.
    OPT *args: Y2,M2,D2 --> These optional entries represent the ending year,
                            month, and date of the period

    EXAMPLE: customStats(1999,8,12) -> Returns a printout of statistics from
                                       August 12th, 1999 to December 31, 1999.
    """
    if any(type(x) != int for x in [y1,m1,d1]): return print("*** OOPS! Ensure that only integers are entered ***")
    valid1 = checkDate(y1,m1,d1)
    if len(date2) == 0: pass
    elif len(date2) != 3: return print("*** OOPS! For the 2nd (optional) date, ensure a Year, Month and Date are entered ***")
    else:
        if any(type(x) != int for x in [date2[0],date2[1],date2[2]]): return print("*** OOPS! Ensure that only integers are entered ***")
        valid2 = checkDate(date2[0],date2[1],date2[2])

    startday = datetime.date(y1,m1,d1)
    incr_day = startday
    if len(date2) == 3:
        endday = datetime.date(date2[0],date2[1],date2[2])
    else:
        emo = max(M for M in clmt[startday.year] if type(M) == int)
        edy = max(D for D in clmt[startday.year][emo] if type(D) == int)
        endday = datetime.date(startday.year,emo,edy)
        
    if endday <= startday: return print("*** OOPS! Pick an earlier start-day or (if applicable) a later end-day ***")
    # This handles if the passed time is greater than a year
    if endday >= datetime.date(startday.year+1,startday.month,startday.day):
        if endday == datetime.date(startday.year+1,startday.month,startday.day):
            endday = datetime.date(startday.year+1,startday.month,startday.day)-datetime.timedelta(days=1)
        else: return print("*** OOPS! customStats only accepts a temporal scope of a year or less")

    c_prcp = []
    c_prcpDAYS = 0
    c_snow = []
    c_snowDAYS = 0
    c_snwd = []
    c_snwdDAYS = 0
    c_temp = []
    c_tmax = []
    c_tmin = []
    records_in_period = 0
    c_records = {"prcpPROP":{"day_max":[-1,[]]},
                 "snowPROP":{"day_max":[-1,[]]},
                 "snwdPROP":{"day_max":[-1,[]]},
                 "tempPROP":{"day_max":[-999,[]],"day_min":[999,[]]},
                 "tmaxPROP":{"day_max":[-999,[]],"day_min":[999,[]]},
                 "tminPROP":{"day_max":[-999,[]],"day_min":[999,[]]}}

    # Determine total length of period (used for exclusion calculation)
    s = datetime.date(1900,startday.month,startday.day)
    test = datetime.date(1900,endday.month,endday.day)
    if test > s: e = test
    else: e = datetime.date(1901,endday.month,endday.day)
    timelength = (e - s).days + 1
    
    if timelength <= 5: EXCLD = timelength-1
    elif timelength == 6: EXCLD = 4
    elif timelength == 7: EXCLD = excludeweek
    elif timelength == 8: EXCLD = excludeweek
    elif timelength in [28,29,30,31]: EXCLD = excludemonth
    elif timelength >= 350: EXCLD = excludeyear
    else: EXCLD = round(excludecustom * timelength)

    while incr_day <= endday:
        y = incr_day.year; m = incr_day.month; d = incr_day.day
        if y in clmt and m in clmt[y] and d in clmt[y][m]:  # If a record for clmt[y][m][d] exists
            records_in_period += 1
            if clmt[y][m][d].prcpQ in ignoreflags and clmt[y][m][d].prcp not in ["9999","-9999",""]:
                c_prcp.append(float(clmt[y][m][d].prcp))
                if round(float(clmt[y][m][d].prcp),2) == c_records["prcpPROP"]["day_max"][0]:
                    c_records["prcpPROP"]["day_max"][1].append(clmt[y][m][d])
                elif round(float(clmt[y][m][d].prcp),2) > c_records["prcpPROP"]["day_max"][0]:
                    c_records["prcpPROP"]["day_max"][0] = round(float(clmt[y][m][d].prcp),2)
                    c_records["prcpPROP"]["day_max"][1] = []
                    c_records["prcpPROP"]["day_max"][1].append(clmt[y][m][d])
            if clmt[y][m][d].prcpQ in ignoreflags and clmt[y][m][d].prcp not in ["9999","-9999",""] and float(clmt[y][m][d].prcp) != 0 or clmt[y][m][d].prcpM == "T":
                c_prcpDAYS += 1
            if clmt[y][m][d].snowQ in ignoreflags and clmt[y][m][d].snow not in ["9999","-9999",""]:
                c_snow.append(float(clmt[y][m][d].snow))
                if round(float(clmt[y][m][d].snow),2) == c_records["snowPROP"]["day_max"][0]:
                    c_records["snowPROP"]["day_max"][1].append(clmt[y][m][d])
                elif round(float(clmt[y][m][d].snow),2) > c_records["snowPROP"]["day_max"][0]:
                    c_records["snowPROP"]["day_max"][0] = round(float(clmt[y][m][d].snow),2)
                    c_records["snowPROP"]["day_max"][1] = []
                    c_records["snowPROP"]["day_max"][1].append(clmt[y][m][d])
            if clmt[y][m][d].snowQ in ignoreflags and clmt[y][m][d].snow not in ["9999","-9999",""] and float(clmt[y][m][d].snow) != 0 or clmt[y][m][d].snowM == "T":
                c_snowDAYS += 1
            if clmt[y][m][d].snwdQ in ignoreflags and clmt[y][m][d].snwd not in ["9999","-9999",""]:
                if float(clmt[y][m][d].snwd) > 0:
                    c_snwd.append(float(clmt[y][m][d].snwd))
                    if round(float(clmt[y][m][d].snwd),1) == c_records["snwdPROP"]["day_max"][0]:
                        c_records["snwdPROP"]["day_max"][1].append(clmt[y][m][d])
                    if round(float(clmt[y][m][d].snwd),1) > c_records["snwdPROP"]["day_max"][0]:
                        c_records["snwdPROP"]["day_max"][0] = round(float(clmt[y][m][d].snwd),1)
                        c_records["snwdPROP"]["day_max"][1] = [clmt[y][m][d]]
                if float(clmt[y][m][d].snwd) > 0 or clmt[y][m][d].snwdM == "T": c_snwdDAYS += 1
            if clmt[y][m][d].tmaxQ in ignoreflags and clmt[y][m][d].tminQ in ignoreflags and clmt[y][m][d].tmax not in ["9999","-9999",""] and clmt[y][m][d].tmin not in ["9999","-9999",""]:
                c_temp.append(int(clmt[y][m][d].tmax))
                c_temp.append(int(clmt[y][m][d].tmin))
                if round(mean([int(clmt[y][m][d].tmax),int(clmt[y][m][d].tmin)]),1) == c_records["tempPROP"]["day_max"][0]:
                    c_records["tempPROP"]["day_max"][1].append(clmt[y][m][d])
                elif round(mean([int(clmt[y][m][d].tmax),int(clmt[y][m][d].tmin)]),1) > c_records["tempPROP"]["day_max"][0]:
                    c_records["tempPROP"]["day_max"][0] = round(mean([int(clmt[y][m][d].tmax),int(clmt[y][m][d].tmin)]),1)
                    c_records["tempPROP"]["day_max"][1] = []
                    c_records["tempPROP"]["day_max"][1].append(clmt[y][m][d])
                if round(mean([int(clmt[y][m][d].tmax),int(clmt[y][m][d].tmin)]),1) == c_records["tempPROP"]["day_min"][0]:
                    c_records["tempPROP"]["day_min"][1].append(clmt[y][m][d])
                elif round(mean([int(clmt[y][m][d].tmax),int(clmt[y][m][d].tmin)]),1) < c_records["tempPROP"]["day_min"][0]:
                    c_records["tempPROP"]["day_min"][0] = round(mean([int(clmt[y][m][d].tmax),int(clmt[y][m][d].tmin)]),1)
                    c_records["tempPROP"]["day_min"][1] = []
                    c_records["tempPROP"]["day_min"][1].append(clmt[y][m][d])
            if clmt[y][m][d].tmaxQ in ignoreflags and clmt[y][m][d].tmax not in ["9999","-9999",""]:
                c_tmax.append(int(clmt[y][m][d].tmax))
                if int(clmt[y][m][d].tmax) == c_records["tmaxPROP"]["day_max"][0]:
                    c_records["tmaxPROP"]["day_max"][1].append(clmt[y][m][d])
                elif int(clmt[y][m][d].tmax) > c_records["tmaxPROP"]["day_max"][0]:
                    c_records["tmaxPROP"]["day_max"][0] = int(clmt[y][m][d].tmax)
                    c_records["tmaxPROP"]["day_max"][1] = []
                    c_records["tmaxPROP"]["day_max"][1].append(clmt[y][m][d])
                if int(clmt[y][m][d].tmax) == c_records["tmaxPROP"]["day_min"][0]:
                    c_records["tmaxPROP"]["day_min"][1].append(clmt[y][m][d])
                elif int(clmt[y][m][d].tmax) < c_records["tmaxPROP"]["day_min"][0]:
                    c_records["tmaxPROP"]["day_min"][0] = int(clmt[y][m][d].tmax)
                    c_records["tmaxPROP"]["day_min"][1] = []
                    c_records["tmaxPROP"]["day_min"][1].append(clmt[y][m][d])
            if clmt[y][m][d].tminQ in ignoreflags and clmt[y][m][d].tmin not in ["9999","-9999",""]:
                c_tmin.append(int(clmt[y][m][d].tmin))
                if int(clmt[y][m][d].tmin) == c_records["tminPROP"]["day_max"][0]:
                    c_records["tminPROP"]["day_max"][1].append(clmt[y][m][d])
                elif int(clmt[y][m][d].tmin) > c_records["tminPROP"]["day_max"][0]:
                    c_records["tminPROP"]["day_max"][0] = int(clmt[y][m][d].tmin)
                    c_records["tminPROP"]["day_max"][1] = []
                    c_records["tminPROP"]["day_max"][1].append(clmt[y][m][d])
                if int(clmt[y][m][d].tmin) == c_records["tminPROP"]["day_min"][0]:
                    c_records["tminPROP"]["day_min"][1].append(clmt[y][m][d])
                elif int(clmt[y][m][d].tmin) < c_records["tminPROP"]["day_min"][0]:
                    c_records["tminPROP"]["day_min"][0] = int(clmt[y][m][d].tmin)
                    c_records["tminPROP"]["day_min"][1] = []
                    c_records["tminPROP"]["day_min"][1].append(clmt[y][m][d])
        incr_day += datetime.timedelta(days=1)

    # customRank(attribute,quantity,M1,D1,*[M2,D2])
    prcpaschist, prcpdeschist, prcpDAYSaschist, prcpDAYSdeschist, snowaschist, snowdeschist, snowDAYSaschist, snowDAYSdeschist, tmaxaschist, tmaxdeschist, tminaschist, tmindeschist, tavgaschist, tavgdeschist = customRank("temp",5,startday.month,startday.day,endday.month,endday.day,customStatsRun=True)
    #for x in [prcpaschist, prcpdeschist, snowaschist, snowdeschist, tmaxaschist, tmaxdeschist, tminaschist, tmindeschist, tavgaschist, tavgdeschist]: print(len(x))
    #for x in [prcpaschist, prcpdeschist, snowaschist, snowdeschist, tmaxaschist, tmaxdeschist, tminaschist, tmindeschist, tavgaschist, tavgdeschist]: print(x)
    
    print("")
    print("Statistics for {}-{}-{} thru {}-{}-{}".format(startday.year,startday.month,startday.day,
                                                         endday.year,endday.month,endday.day))
    print("{}: {}".format(clmt["station"],clmt["station_name"]))
    print("Quantity of Records: {}".format(records_in_period))
    print("-------------------------------------")
    """
    c_prcp = []
    c_prcpDAYS = 0
    c_snow = []
    c_snowDAYS = 0
    c_snwd = []
    c_temp = []
    c_tmax = []
    c_tmin = []
    records_in_period = 0
    c_records = {"prcpPROP":{"day_max":[-1,[]]},
                 "snowPROP":{"day_max":[-1,[]]},
                 "tempPROP":{"day_max":[-999,[]],"day_min":[999,[]]},
                 "tmaxPROP":{"day_max":[-999,[]],"day_min":[999,[]]},
                 "tminPROP":{"day_max":[-999,[]],"day_min":[999,[]]}}
    """
    print(" Total Precipitation: {}".format(round(sum(c_prcp),2)),end="")
    try: print(", Rank: {} Wettest".format(rank(prcpdeschist.index(round(sum(c_prcp),2))+1)),end="") if sum(c_prcp) > 0 and prcpdeschist.index(round(sum(c_prcp),2)) <= prcpaschist.index(round(sum(c_prcp),2)) else print("",end="")
    except: print(", Rank: {} Wettest".format(rank(prcpdeschist.index(round(sum(c_prcp),2))+1)),end="")
    try: print(", Rank: {} Driest".format(rank(prcpaschist.index(round(sum(c_prcp),2))+1))) if records_in_period > EXCLD and prcpaschist.index(round(sum(c_prcp),2)) <= prcpdeschist.index(round(sum(c_prcp),2)) else print("")
    except: print("")

    print(" Total Precipitation Days (>=T): {}".format(c_prcpDAYS),end="")
    try: print(", Rank: {} Most".format(rank(prcpDAYSdeschist.index(c_prcpDAYS)+1)),end="") if c_prcpDAYS > 0 and prcpDAYSdeschist.index(c_prcpDAYS) <= prcpDAYSaschist.index(c_prcpDAYS) else print("",end="")
    except: print(", Rank: {} Most".format(rank(prcpDAYSdeschist.index(c_prcpDAYS)+1)),end="")
    try: print(", Rank: {} Least".format(rank(prcpDAYSaschist.index(c_prcpDAYS)+1))) if records_in_period > EXCLD and prcpDAYSaschist.index(c_prcpDAYS) <= prcpDAYSdeschist.index(c_prcpDAYS) else print("")
    except: print("")
    if round(sum(c_prcp),2) > 0:
        print(" -- Highest Daily Precip: {}".format(c_records["prcpPROP"]["day_max"][0]),end = " ::: ")
        for x in c_records["prcpPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end="") if x != c_records["prcpPROP"]["day_max"][1][-1] else print("{}".format(x.daystr))

    if c_snowDAYS > 0:
        print(" Total Snow: {}".format(round(sum(c_snow),1)),end="")
        try: print(", Rank: {} Snowiest".format(rank(snowdeschist.index(round(sum(c_snow),1))+1)),end="") if sum(c_snow) > 0 and snowdeschist.index(round(sum(c_snow),1)) <= snowaschist.index(round(sum(c_snow),1)) else print("",end="")
        except: print(", Rank: {} Snowiest".format(rank(snowdeschist.index(round(sum(c_snow),1))+1)),end="")
        try: print(", Rank: {} Least-Snowiest".format(rank(snowaschist.index(round(sum(c_snow),1))+1))) if records_in_period > EXCLD and snowaschist.index(round(sum(c_snow),1)) <= snowdeschist.index(round(sum(c_snow),1)) else print("")
        except: print("")

        print(" Total Snow Days (>=T): {}".format(c_snowDAYS),end="")
        try: print(", Rank: {} Most".format(rank(snowDAYSdeschist.index(c_snowDAYS)+1)),end="") if c_snowDAYS > 0 and snowDAYSdeschist.index(c_snowDAYS) <= snowDAYSaschist.index(c_snowDAYS) else print("",end="")
        except: print(", Rank: {} Most".format(rank(snowDAYSdeschist.index(c_snowDAYS)+1)),end="")
        try: print(", Rank: {} Least".format(rank(snowDAYSaschist.index(c_snowDAYS)+1))) if records_in_period > EXCLD and snowDAYSaschist.index(c_snowDAYS) <= snowDAYSdeschist.index(c_snowDAYS) else print("")
        except: print("")
        if c_records["snowPROP"]["day_max"][0] > 0:
            print("-- Snowiest Day: {}".format(c_records["snowPROP"]["day_max"][0]),end=" ::: ")
            for x in c_records["snowPROP"]["day_max"][1]:
                print("{}, ".format(x.daystr),end=" ") if x!= c_records["snowPROP"]["day_max"][1][-1] else print(x.daystr)
    if len(c_snwd) > 0:
        print(" Total Days w/Snow on the Ground: {}".format(c_snwdDAYS))
        print("-- Highest Snow-Depth: {:.1f}".format(c_records["snwdPROP"]["day_max"][0]),end=" ::: ")
        for x in c_records["snwdPROP"]["day_max"][1]:
            print("{}, ".format(x.daystr),end="") if x != c_records["snwdPROP"]["day_max"][1][-1] else print(x.daystr)
    try:
        print(" Average Temperature: {}".format(round(mean(c_temp),1)),end="")
        print(", Rank: {} Warmest".format(rank(tavgdeschist.index(round(mean(c_temp),1))+1)),end="") if len(c_temp) > EXCLD*2 and tavgdeschist.index(round(mean(c_temp),1)) <= tavgaschist.index(round(mean(c_temp),1)) else print("",end="")
        print(", Rank: {} Coolest".format(rank(tavgaschist.index(round(mean(c_temp),1))+1))) if len(c_temp) > EXCLD*2 and tavgaschist.index(round(mean(c_temp),1)) <= tavgdeschist.index(round(mean(c_temp),1)) else print("")
    except: print(" Average Temperature: N/A")

    try:
        print(" Avg MAX Temperature: {}".format(round(mean(c_tmax),1)),end="")
        print(", Rank: {} Warmest".format(rank(tmaxdeschist.index(round(mean(c_tmax),1))+1)),end="") if len(c_tmax) > EXCLD and tmaxdeschist.index(round(mean(c_tmax),1)) <= tmaxaschist.index(round(mean(c_tmax),1)) else print("",end="")
        print(", Rank: {} Coolest".format(rank(tmaxaschist.index(round(mean(c_tmax),1))+1))) if len(c_tmax) > EXCLD and tmaxaschist.index(round(mean(c_tmax),1)) <= tmaxdeschist.index(round(mean(c_tmax),1)) else print("")
    except: print(" Avg MAX Temperature: N/A")
    if c_records["tmaxPROP"]["day_max"][0] != -999:
        print(" -- Warmest Daily TMAX: {}".format(c_records["tmaxPROP"]["day_max"][0]),end = " ::: ")
        for x in c_records["tmaxPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end="") if x != c_records["tmaxPROP"]["day_max"][1][-1] else print(x.daystr)
    if c_records["tmaxPROP"]["day_min"][0] != -999:
        print(" -- Coolest Daily TMAX: {}".format(c_records["tmaxPROP"]["day_min"][0]),end = " ::: ")
        for x in c_records["tmaxPROP"]["day_min"][1]: print("{}, ".format(x.daystr), end="") if x != c_records["tmaxPROP"]["day_min"][1][-1] else print(x.daystr)

    try:
        print(" Avg MIN Temperature: {}".format(round(mean(c_tmin),1)),end="")
        print(", Rank: {} Warmest".format(rank(tmindeschist.index(round(mean(c_tmin),1))+1)),end="") if len(c_tmin) > EXCLD and tmindeschist.index(round(mean(c_tmin),1)) <= tminaschist.index(round(mean(c_tmin),1)) else print("",end="")
        print(", Rank: {} Coolest".format(rank(tminaschist.index(round(mean(c_tmin),1))+1))) if len(c_tmin) > EXCLD and tminaschist.index(round(mean(c_tmin),1)) <= tmindeschist.index(round(mean(c_tmin),1)) else print("")
    except: print(" Avg MIN Temperature: N/A")
    if c_records["tminPROP"]["day_max"][0] != -999:
        print(" -- Warmest Daily TMIN: {}".format(c_records["tminPROP"]["day_max"][0]),end = " ::: ")
        for x in c_records["tminPROP"]["day_max"][1]: print("{}, ".format(x.daystr), end="") if x != c_records["tminPROP"]["day_max"][1][-1] else print(x.daystr)
    if c_records["tminPROP"]["day_min"][0] != -999:
        print(" -- Coolest Daily TMIN: {}".format(c_records["tminPROP"]["day_min"][0]),end = " ::: ")
        for x in c_records["tminPROP"]["day_min"][1]: print("{}, ".format(x.daystr), end="") if x != c_records["tminPROP"]["day_min"][1][-1] else print(x.daystr)
    print("-----")
    print("")

def dayReport(m,d,**output):
    """Detailed Climatological Report for recorded statistics of a specific
    day. It accepts only arguments for the month and day of interest. Passed
    arguments MUST be integers
    
    dayReport(month,day,**{output=False})
    
    EXAMPLE: dayReport(5,31) -> Returns a climatological report for May 31
    """
    if len(clmt) == 0: return print("* OOPS! Run the clmtAnalyze function first.")
    valid_yrs = [x for x in clmt.keys() if type(x) == int]
    valid_yrs.sort()
    climo30yrs = {}
    for x in range(1811,max(valid_yrs)+1,clmt_inc_rpt):
        if x in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]) and x+clmt_len_rpt-1 in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]+1):
            climo30yrs[(x,x+clmt_len_rpt-1)] = {"years":(x,x+clmt_len_rpt-1),
                                    "prcp": [],"prcpPROP":{"days":0,"day_max":[-1,[]]},
                                    "snow": [],"snowPROP":{"days":0,"day_max":[-1,[]]},
                                    "tempAVGlist": [],"tempAVGlist_ind":[],"tavgPROP":{"day_max":[-999,[]],"day_min":[999,[]]},
                                    "tmax": [],"tmaxPROP":{"day_max":[-999,[]],"day_min":[999,[]]},
                                    "tmin": [],"tminPROP":{"day_max":[-999,[]],"day_min":[999,[]]}}

    alltime = {"years":(valid_yrs[0],valid_yrs[len(valid_yrs)-1]),
               "prcp": [],"prcpPROP":{"days":0,"day_max":[-1,[]]},
               "snow": [],"snowPROP":{"days":0,"day_max":[-1,[]]},
               "tempAVGlist": [],"tempAVGlist_ind":[],"tavgPROP":{"day_max":[-999,[]],"day_min":[999,[]]},
               "tmax": [],"tmaxPROP":{"day_max":[-999,[]],"day_min":[999,[]]},
               "tmin": [],"tminPROP":{"day_max":[-999,[]],"day_min":[999,[]]}}

    # {"day_max":[-1,[]],"month_max":[-1,[]],"month_min":[999,[]]}
    # {"day_max":[-999,[]],"day_min":[999,[]],"month_AVG_max":[-999,[]],"month_AVG_min":[999,[]]}
    # if clmt[int(each[2][0:4])][int(each[2][5:7])][int(each[2][8:10])].prcpQ in ignoreflags and clmt[int(each[2][0:4])][int(each[2][5:7])][int(each[2][8:10])].prcp not in ["9999","-9999",""]:
    # if clmt[int(each[2][0:4])][int(each[2][5:7])][int(each[2][8:10])].tmaxQ in ignoreflags and clmt[int(each[2][0:4])][int(each[2][5:7])][int(each[2][8:10])].tmax not in ["9999","-9999",""]:
    #alltime["prcp"] = [float(clmt[y][m][d].prcp) for y in clmt if type(y) == int and m in clmt[y] and d in clmt[y][m]]
    #alltime["prcpPROP"]["day_max"][0] = max(float(clmt[y][m][d].prcp) for y in clmt if type(y) == int and m in clmt[y] and d in clmt[y][m])
    for y in valid_yrs:
        try:
            if clmt[y][m][d].prcpQ in ignoreflags and clmt[y][m][d].prcp not in ["9999","-9999",""]:
                alltime["prcp"].append(float(clmt[y][m][d].prcp))
                if float(clmt[y][m][d].prcp) > 0 or clmt[y][m][d].prcpM == "T": alltime["prcpPROP"]["days"] += 1
                if float(clmt[y][m][d].prcp) == alltime["prcpPROP"]["day_max"][0]:
                    alltime["prcpPROP"]["day_max"][1].append(clmt[y][m][d])
                elif float(clmt[y][m][d].prcp) > alltime["prcpPROP"]["day_max"][0]:
                    alltime["prcpPROP"]["day_max"][0] = float(clmt[y][m][d].prcp)
                    alltime["prcpPROP"]["day_max"][1] = []
                    alltime["prcpPROP"]["day_max"][1].append(clmt[y][m][d])
                for c in climo30yrs:
                    if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                        climo30yrs[c]["prcp"].append(float(clmt[y][m][d].prcp))
                        if float(clmt[y][m][d].prcp) > 0 or clmt[y][m][d].prcpM == "T": climo30yrs[c]["prcpPROP"]["days"] += 1
                        if float(clmt[y][m][d].prcp) == climo30yrs[c]["prcpPROP"]["day_max"][0]:
                            climo30yrs[c]["prcpPROP"]["day_max"][1].append(clmt[y][m][d])
                        elif float(clmt[y][m][d].prcp) > climo30yrs[c]["prcpPROP"]["day_max"][0]:
                            climo30yrs[c]["prcpPROP"]["day_max"][0] = float(clmt[y][m][d].prcp)
                            climo30yrs[c]["prcpPROP"]["day_max"][1] = []
                            climo30yrs[c]["prcpPROP"]["day_max"][1].append(clmt[y][m][d])
        except:
            pass
        try:
            if clmt[y][m][d].snowQ in ignoreflags and clmt[y][m][d].snow not in ["9999","-9999",""]:
                alltime["snow"].append(float(clmt[y][m][d].snow))
                if float(clmt[y][m][d].snow) > 0 or clmt[y][m][d].snowM == "T": alltime["snowPROP"]["days"] += 1
                if float(clmt[y][m][d].snow) == alltime["snowPROP"]["day_max"][0]:
                    alltime["snowPROP"]["day_max"][1].append(clmt[y][m][d])
                elif float(clmt[y][m][d].snow) > alltime["snowPROP"]["day_max"][0]:
                    alltime["snowPROP"]["day_max"][0] = float(clmt[y][m][d].snow)
                    alltime["snowPROP"]["day_max"][1] = []
                    alltime["snowPROP"]["day_max"][1].append(clmt[y][m][d])
                for c in climo30yrs:
                    if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                        climo30yrs[c]["snow"].append(float(clmt[y][m][d].snow))
                        if float(clmt[y][m][d].snow) > 0 or clmt[y][m][d].snowM == "T": climo30yrs[c]["snowPROP"]["days"] += 1
                        if float(clmt[y][m][d].snow) == climo30yrs[c]["snowPROP"]["day_max"][0]:
                            climo30yrs[c]["snowPROP"]["day_max"][1].append(clmt[y][m][d])
                        elif float(clmt[y][m][d].snow) > climo30yrs[c]["snowPROP"]["day_max"][0]:
                            climo30yrs[c]["snowPROP"]["day_max"][0] = float(clmt[y][m][d].snow)
                            climo30yrs[c]["snowPROP"]["day_max"][1] = []
                            climo30yrs[c]["snowPROP"]["day_max"][1].append(clmt[y][m][d])
        except:
            pass
        try:
            if clmt[y][m][d].tmaxQ in ignoreflags and clmt[y][m][d].tminQ in ignoreflags and clmt[y][m][d].tmax not in ["9999","-9999",""] and clmt[y][m][d].tmin not in ["9999","-9999",""] and int(clmt[y][m][d].tmax) >= int(clmt[y][m][d].tmin):
                alltime["tempAVGlist"].append(int(clmt[y][m][d].tmax))
                alltime["tempAVGlist"].append(int(clmt[y][m][d].tmin))
                if mean([int(clmt[y][m][d].tmax),int(clmt[y][m][d].tmin)]) == alltime["tavgPROP"]["day_max"][0]:
                    alltime["tavgPROP"]["day_max"][1].append(clmt[y][m][d])
                elif mean([int(clmt[y][m][d].tmax),int(clmt[y][m][d].tmin)]) > alltime["tavgPROP"]["day_max"][0]:
                    alltime["tavgPROP"]["day_max"][0] = mean([int(clmt[y][m][d].tmax),int(clmt[y][m][d].tmin)])
                    alltime["tavgPROP"]["day_max"][1] = []
                    alltime["tavgPROP"]["day_max"][1].append(clmt[y][m][d])
                if mean([int(clmt[y][m][d].tmax),int(clmt[y][m][d].tmin)]) == alltime["tavgPROP"]["day_min"][0]:
                    alltime["tavgPROP"]["day_min"][1].append(clmt[y][m][d])
                elif mean([int(clmt[y][m][d].tmax),int(clmt[y][m][d].tmin)]) < alltime["tavgPROP"]["day_min"][0]:
                    alltime["tavgPROP"]["day_min"][0] = mean([int(clmt[y][m][d].tmax),int(clmt[y][m][d].tmin)])
                    alltime["tavgPROP"]["day_min"][1] = []
                    alltime["tavgPROP"]["day_min"][1].append(clmt[y][m][d])
                for c in climo30yrs:
                    if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                        climo30yrs[c]["tempAVGlist"].append(int(clmt[y][m][d].tmax))
                        climo30yrs[c]["tempAVGlist"].append(int(clmt[y][m][d].tmin))
                        if mean([int(clmt[y][m][d].tmax),int(clmt[y][m][d].tmin)]) == climo30yrs["tavgPROP"]["day_max"][0]:
                            climo30yrs["tavgPROP"]["day_max"][1].append(clmt[y][m][d])
                        elif mean([int(clmt[y][m][d].tmax),int(clmt[y][m][d].tmin)]) > climo30yrs["tavgPROP"]["day_max"][0]:
                            climo30yrs["tavgPROP"]["day_max"][0] = mean([int(clmt[y][m][d].tmax),int(clmt[y][m][d].tmin)])
                            climo30yrs["tavgPROP"]["day_max"][1] = []
                            climo30yrs["tavgPROP"]["day_max"][1].append(clmt[y][m][d])
                        if mean([int(clmt[y][m][d].tmax),int(clmt[y][m][d].tmin)]) == climo30yrs["tavgPROP"]["day_min"][0]:
                            climo30yrs["tavgPROP"]["day_min"][1].append(clmt[y][m][d])
                        elif mean([int(clmt[y][m][d].tmax),int(clmt[y][m][d].tmin)]) < climo30yrs["tavgPROP"]["day_min"][0]:
                            climo30yrs["tavgPROP"]["day_min"][0] = mean([int(clmt[y][m][d].tmax),int(clmt[y][m][d].tmin)])
                            climo30yrs["tavgPROP"]["day_min"][1] = []
                            climo30yrs["tavgPROP"]["day_min"][1].append(clmt[y][m][d])
        except:
            pass
        try:
            if clmt[y][m][d].tmaxQ in ignoreflags and clmt[y][m][d].tmax not in ["9999","-9999",""]:
                alltime["tmax"].append(int(clmt[y][m][d].tmax))
                if int(clmt[y][m][d].tmax) == alltime["tmaxPROP"]["day_max"][0]:
                    alltime["tmaxPROP"]["day_max"][1].append(clmt[y][m][d])
                elif int(clmt[y][m][d].tmax) > alltime["tmaxPROP"]["day_max"][0]:
                    alltime["tmaxPROP"]["day_max"][0] = int(clmt[y][m][d].tmax)
                    alltime["tmaxPROP"]["day_max"][1] = []
                    alltime["tmaxPROP"]["day_max"][1].append(clmt[y][m][d])
                if int(clmt[y][m][d].tmax) == alltime["tmaxPROP"]["day_min"][0]:
                    alltime["tmaxPROP"]["day_min"][1].append(clmt[y][m][d])
                elif int(clmt[y][m][d].tmax) < alltime["tmaxPROP"]["day_min"][0]:
                    alltime["tmaxPROP"]["day_min"][0] = int(clmt[y][m][d].tmax)
                    alltime["tmaxPROP"]["day_min"][1] = []
                    alltime["tmaxPROP"]["day_min"][1].append(clmt[y][m][d])
                for c in climo30yrs:
                    if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                        climo30yrs[c]["tmax"].append(int(clmt[y][m][d].tmax))
                        if int(clmt[y][m][d].tmax) == climo30yrs[c]["tmaxPROP"]["day_max"][0]:
                            climo30yrs[c]["tmaxPROP"]["day_max"][1].append(clmt[y][m][d])
                        elif int(clmt[y][m][d].tmax) > climo30yrs[c]["tmaxPROP"]["day_max"][0]:
                            climo30yrs[c]["tmaxPROP"]["day_max"][0] = int(clmt[y][m][d].tmax)
                            climo30yrs[c]["tmaxPROP"]["day_max"][1] = []
                            climo30yrs[c]["tmaxPROP"]["day_max"][1].append(clmt[y][m][d])
                        if int(clmt[y][m][d].tmax) == climo30yrs[c]["tmaxPROP"]["day_min"][0]:
                            climo30yrs[c]["tmaxPROP"]["day_min"][1].append(clmt[y][m][d])
                        elif int(clmt[y][m][d].tmax) < climo30yrs[c]["tmaxPROP"]["day_min"][0]:
                            climo30yrs[c]["tmaxPROP"]["day_min"][0] = int(clmt[y][m][d].tmax)
                            climo30yrs[c]["tmaxPROP"]["day_min"][1] = []
                            climo30yrs[c]["tmaxPROP"]["day_min"][1].append(clmt[y][m][d])
        except:
            pass
        try:
            if clmt[y][m][d].tminQ in ignoreflags and clmt[y][m][d].tmin not in ["9999","-9999",""]:
                alltime["tmin"].append(int(clmt[y][m][d].tmin))
                if int(clmt[y][m][d].tmin) == alltime["tminPROP"]["day_max"][0]:
                    alltime["tminPROP"]["day_max"][1].append(clmt[y][m][d])
                elif int(clmt[y][m][d].tmin) > alltime["tminPROP"]["day_max"][0]:
                    alltime["tminPROP"]["day_max"][0] = int(clmt[y][m][d].tmin)
                    alltime["tminPROP"]["day_max"][1] = []
                    alltime["tminPROP"]["day_max"][1].append(clmt[y][m][d])
                if int(clmt[y][m][d].tmin) == alltime["tminPROP"]["day_min"][0]:
                    alltime["tminPROP"]["day_min"][1].append(clmt[y][m][d])
                elif int(clmt[y][m][d].tmin) < alltime["tminPROP"]["day_min"][0]:
                    alltime["tminPROP"]["day_min"][0] = int(clmt[y][m][d].tmin)
                    alltime["tminPROP"]["day_min"][1] = []
                    alltime["tminPROP"]["day_min"][1].append(clmt[y][m][d])
                for c in climo30yrs:
                    if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                        climo30yrs[c]["tmin"].append(int(clmt[y][m][d].tmin))
                        if int(clmt[y][m][d].tmin) == climo30yrs[c]["tminPROP"]["day_max"][0]:
                            climo30yrs[c]["tminPROP"]["day_max"][1].append(clmt[y][m][d])
                        elif int(clmt[y][m][d].tmin) > climo30yrs[c]["tminPROP"]["day_max"][0]:
                            climo30yrs[c]["tminPROP"]["day_max"][0] = int(clmt[y][m][d].tmin)
                            climo30yrs[c]["tminPROP"]["day_max"][1] = []
                            climo30yrs[c]["tminPROP"]["day_max"][1].append(clmt[y][m][d])
                        if int(clmt[y][m][d].tmin) == climo30yrs[c]["tminPROP"]["day_min"][0]:
                            climo30yrs[c]["tminPROP"]["day_min"][1].append(clmt[y][m][d])
                        elif int(clmt[y][m][d].tmin) < climo30yrs[c]["tminPROP"]["day_min"][0]:
                            climo30yrs[c]["tminPROP"]["day_min"][0] = int(clmt[y][m][d].tmin)
                            climo30yrs[c]["tminPROP"]["day_min"][1] = []
                            climo30yrs[c]["tminPROP"]["day_min"][1].append(clmt[y][m][d])
        except:
            pass

    # PRINT REPORT
    print("---------------------------------------------------")
    print("Climatology Report for {} {}".format(calendar.month_name[m],d))
    print("City: {}, {}".format(clmt["station"],clmt["station_name"]))
    print("{}-{}; {}-Year Incremented {}-Year Climatologies".format(min(valid_yrs),max(valid_yrs),clmt_inc_rpt,clmt_len_rpt))
    print("---------------------------------------------------")
    print("{:▒^9} {:▒^12} {:▒^12} {:▒^8} {:▒^9}  {:▒^9} {:▒^8} {:▒^9}  {:▒^9}".format("YEARS","PRCP","SNOW","TMAX","TMAX","TMAX","TMIN","TMIN","TMIN"))
    print("{:▒^9} {:▒^12} {:▒^12} {:▒^8} {:▒^9}  {:▒^9} {:▒^8} {:▒^9}  {:▒^9}".format(     "","hi","hi","avg","hi","lo","avg","hi","lo"))
    print("{:.^9} {:.^12} {:.^12} {:.^8} {:.^9}  {:.^9} {:.^8} {:.^9}  {:.^9}".format("","","","","","","","",""))
    print("{:^9} {:>6.2f}, {:>4} {:>6.1f}, {:^4} {:^8.1f} {:>3}, {:^4}  {:>3}, {:^4} {:^8.1f} {:>3}, {:^4}  {:>3}, {:^4}".format("All Time",
            alltime["prcpPROP"]["day_max"][0],len(alltime["prcpPROP"]["day_max"][1]) if len(alltime["prcpPROP"]["day_max"][1]) > 1 else alltime["prcpPROP"]["day_max"][1][0].daystr[0:4],
            alltime["snowPROP"]["day_max"][0],len(alltime["snowPROP"]["day_max"][1]) if len(alltime["snowPROP"]["day_max"][1]) > 1 else alltime["snowPROP"]["day_max"][1][0].daystr[0:4],
            round(mean(alltime["tmax"]),1),
            alltime["tmaxPROP"]["day_max"][0],len(alltime["tmaxPROP"]["day_max"][1]) if len(alltime["tmaxPROP"]["day_max"][1]) > 1 else alltime["tmaxPROP"]["day_max"][1][0].daystr[0:4],
            alltime["tmaxPROP"]["day_min"][0],len(alltime["tmaxPROP"]["day_min"][1]) if len(alltime["tmaxPROP"]["day_min"][1]) > 1 else alltime["tmaxPROP"]["day_min"][1][0].daystr[0:4],
            round(mean(alltime["tmin"]),1),
            alltime["tminPROP"]["day_max"][0],len(alltime["tminPROP"]["day_max"][1]) if len(alltime["tminPROP"]["day_max"][1]) > 1 else alltime["tminPROP"]["day_max"][1][0].daystr[0:4],
            alltime["tminPROP"]["day_min"][0],len(alltime["tminPROP"]["day_min"][1]) if len(alltime["tminPROP"]["day_min"][1]) > 1 else alltime["tminPROP"]["day_min"][1][0].daystr[0:4]))

    for c in climo30yrs:
        try:
            print("{:^9} {:>6.2f}, {:>4} {:>6.1f}, {:^4} {:^8.1f} {:>3}, {:^4}  {:>3}, {:^4} {:^8.1f} {:>3}, {:^4}  {:>3}, {:^4}".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
                 climo30yrs[c]["prcpPROP"]["day_max"][0],
                 len(climo30yrs[c]["prcpPROP"]["day_max"][1]) if len(climo30yrs[c]["prcpPROP"]["day_max"][1]) > 1 else climo30yrs[c]["prcpPROP"]["day_max"][1][0].daystr[0:4],
                 climo30yrs[c]["snowPROP"]["day_max"][0],
                 len(climo30yrs[c]["snowPROP"]["day_max"][1]) if len(climo30yrs[c]["snowPROP"]["day_max"][1]) > 1 else climo30yrs[c]["snowPROP"]["day_max"][1][0].daystr[0:4],
                 round(mean(climo30yrs[c]["tmax"]),1),
                 climo30yrs[c]["tmaxPROP"]["day_max"][0],
                 len(climo30yrs[c]["tmaxPROP"]["day_max"][1]) if len(climo30yrs[c]["tmaxPROP"]["day_max"][1]) > 1 else climo30yrs[c]["tmaxPROP"]["day_max"][1][0].daystr[0:4],
                 climo30yrs[c]["tmaxPROP"]["day_min"][0],
                 len(climo30yrs[c]["tmaxPROP"]["day_min"][1]) if len(climo30yrs[c]["tmaxPROP"]["day_min"][1]) > 1 else climo30yrs[c]["tmaxPROP"]["day_min"][1][0].daystr[0:4],
                 round(mean(climo30yrs[c]["tmin"]),1),
                 climo30yrs[c]["tminPROP"]["day_max"][0],
                 len(climo30yrs[c]["tminPROP"]["day_max"][1]) if len(climo30yrs[c]["tminPROP"]["day_max"][1]) > 1 else climo30yrs[c]["tminPROP"]["day_max"][1][0].daystr[0:4],
                 climo30yrs[c]["tminPROP"]["day_min"][0],
                 len(climo30yrs[c]["tminPROP"]["day_min"][1]) if len(climo30yrs[c]["tminPROP"]["day_min"][1]) > 1 else climo30yrs[c]["tminPROP"]["day_min"][1][0].daystr[0:4]))
        except:
            print(c)
    print("")

    if "output" in output and output["output"] == True:
        newfn = "dayReport_" + str(calendar.month_abbr[m]) + str(d) + "_" + str(clmt_len_rpt) + "YRclimo_" + str(clmt_inc_rpt) + "YRincr_" + clmt["station_name"] + ".csv"
        with open(newfn,"w") as w:
            headers = ["Assessed Period ({} {})".format(calendar.month_abbr[m],d),"PRCP Days","PRCP stdev","PRCP AVG","SNOW Days","SNOW stdev","SNOW AVG","TAVG stdev","TAVG","TMAX stdev","TMAX","TMIN stdev","TMIN"]
            # HEADER
            for x in range(len(headers)):
                if x != len(headers) - 1: w.write(headers[x]); w.write(",")
                else: w.write(headers[x]); w.write("\n")
            w.write("{}-{}".format(alltime["years"][0],alltime["years"][1])); w.write(",")
            w.write("{}".format(alltime["prcpPROP"]["days"])); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["prcp"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["prcp"]),1))); w.write(",")
            w.write("{}".format(alltime["snowPROP"]["days"])); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["snow"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["snow"]),1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tempAVGlist"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["tempAVGlist"]),1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tmax"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["tmax"]),1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tmin"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["tmin"]),1))); w.write("\n")
            for x in climo30yrs:
                w.write("{}-{}".format(climo30yrs[x]["years"][0],climo30yrs[x]["years"][1])); w.write(",")
                w.write("{}".format(climo30yrs[x]["prcpPROP"]["days"])); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["prcp"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["prcp"]),1))); w.write(",")
                w.write("{}".format(climo30yrs[x]["snowPROP"]["days"])); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["snow"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["snow"]),1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tempAVGlist"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["tempAVGlist"]),1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tmax"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["tmax"]),1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tmin"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["tmin"]),1))); w.write("\n")
            print("*** csv output successful ***")

def weekReport(m,d,**output):
    """Detailed Climatological Report for recorded statistics of a specific
    week of interest. Passed month and day will represent the center of the
    week. It accepts only arguments for the month and day of interest. Passed
    arguments MUST be integers
    
    weekReport(month,day,**{output=False})
    
    EXAMPLE: weekReport(9,29) -> Returns a climatological report for the week
                                 centered on September 29. So data between
                                 Sept 26 and Oct 2 will be compiled
    """
    if len(clmt) == 0: return print("* OOPS! Run the clmtAnalyze function first.")
    valid_yrs = [x for x in clmt.keys() if type(x) == int]
    valid_yrs.sort()
    climo30yrs = {}
    for x in range(1811,max(valid_yrs)+1,clmt_inc_rpt):
        if x in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]) and x+clmt_len_rpt-1 in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]+1):
            climo30yrs[(x,x+clmt_len_rpt-1)] = {"years":(x,x+clmt_len_rpt-1),"total_days":0,
                                    "prcp": [],"prcpPROP":{"days":0,"week_max":[-1,[]]},
                                    "snow": [],"snowPROP":{"days":0,"week_max":[-1,[]]},
                                    "tempAVGlist": [],"tempAVGlist_ind":[],"tavgPROP":{"week_max":[-999,[]],"week_min":[999,[]]},
                                    "tmax": [],"tmaxPROP":{"week_max":[-999,[]],"week_min":[999,[]]},
                                    "tmin": [],"tminPROP":{"week_max":[-999,[]],"week_min":[999,[]]}}

    alltime = {"years":(valid_yrs[0],valid_yrs[len(valid_yrs)-1]),"total_days":0,
               "prcp": [],"prcpPROP":{"days":0,"week_max":[-1,[]]},
               "snow": [],"snowPROP":{"days":0,"week_max":[-1,[]]},
               "tempAVGlist": [],"tempAVGlist_ind":[],"tavgPROP":{"week_max":[-999,[]],"week_min":[999,[]]},
               "tmax": [],"tmaxPROP":{"week_max":[-999,[]],"week_min":[999,[]]},
               "tmin": [],"tminPROP":{"week_max":[-999,[]],"week_min":[999,[]]}}

    if m == 2 and d == 29: d = 28
    for y in valid_yrs:
        wkstart = datetime.date(y,m,d) - datetime.timedelta(days=3)
        currday = wkstart
        wkend = datetime.date(y,m,d) + datetime.timedelta(days=3)
        wk = []
        wk_prcp = []
        wk_snow = []
        wk_tempAVGlist = []
        wk_tmax = []
        wk_tmin = []
        for DAY in range(7):
            try:
                wk.append(clmt[currday.year][currday.month][currday.day])
                currday += datetime.timedelta(days=1)
            except:
                currday += datetime.timedelta(days=1)
        alltime["total_days"] += len(wk)
        for c in climo30yrs:
            if y >= c[0] and y <= c[1] and c[0] in clmt and c[1] in clmt:
                climo30yrs[c]["total_days"] += len(wk)
        if len(wk) > 0:
            for day in wk:
                try:
                    if day.prcpQ in ignoreflags and day.prcp not in ["9999","-9999",""]:
                        #alltime["prcp"].append(float(day.prcp))
                        if float(day.prcp) > 0 or day.prcpM == "T": alltime["prcpPROP"]["days"] += 1
                        wk_prcp.append(float(day.prcp))
                        for c in climo30yrs:
                            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                                #climo30yrs[c]["prcp"].append(float(day.prcp))
                                if float(day.prcp) > 0 or day.prcpM == "T": climo30yrs[c]["prcpPROP"]["days"] += 1
                except:
                    pass
                try:
                    if day.snowQ in ignoreflags and day.snow not in ["9999","-9999",""]:
                        alltime["snow"].append(float(day.snow))
                        if float(day.snow) > 0 or day.snowM == "T": alltime["snowPROP"]["days"] += 1
                        wk_snow.append(float(day.snow))
                        for c in climo30yrs:
                            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                                #climo30yrs[c]["snow"].append(float(day.snow))
                                if float(day.snow) > 0 or day.snowM == "T": climo30yrs[c]["snowPROP"]["days"] += 1
                except:
                    pass
                # "tempAVGlist": [],"tempAVGlist_ind":[],"tavgPROP":{"week_max":[-999,[]],"week_min":[999,[]]},
                try:
                    if day.tmaxQ in ignoreflags and day.tmax not in ["9999","-9999",""] and day.tminQ in ignoreflags and day.tmin not in ["9999","-9999",""]:
                        alltime["tempAVGlist_ind"].append(int(day.tmax))
                        alltime["tempAVGlist_ind"].append(int(day.tmin))
                        wk_tempAVGlist.append(int(day.tmax))
                        wk_tempAVGlist.append(int(day.tmin))
                        for c in climo30yrs:
                            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                                climo30yrs[c]["tempAVGlist_ind"].append(int(day.tmax))
                                climo30yrs[c]["tempAVGlist_ind"].append(int(day.tmin))
                except:
                    pass
                try:
                    if day.tmaxQ in ignoreflags and day.tmax not in ["9999","-9999",""]:
                        alltime["tmax"].append(int(day.tmax))
                        wk_tmax.append(int(day.tmax))
                        for c in climo30yrs:
                            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                                climo30yrs[c]["tmax"].append(int(day.tmax))
                except:
                    pass
                try:
                    if day.tminQ in ignoreflags and day.tmin not in ["9999","-9999",""]:
                        alltime["tmin"].append(int(day.tmin))
                        wk_tmin.append(int(day.tmin))
                        for c in climo30yrs:
                            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                                climo30yrs[c]["tmin"].append(int(day.tmin))
                except:
                    pass
            alltime["prcp"].append(sum(wk_prcp))
            alltime["snow"].append(sum(wk_snow))
            if len(wk_tempAVGlist) > excludeweek_tavg:
                alltime["tempAVGlist"].append(round(mean(wk_tempAVGlist),1))
            # CLIMO STATS HERE ON THIS LEVEL
            if sum(wk_prcp) == alltime["prcpPROP"]["week_max"][0]: alltime["prcpPROP"]["week_max"][1].append(y)
            elif sum(wk_prcp) > alltime["prcpPROP"]["week_max"][0]:
                alltime["prcpPROP"]["week_max"][0] = sum(wk_prcp)
                alltime["prcpPROP"]["week_max"][1] = []
                alltime["prcpPROP"]["week_max"][1].append(y)
            if sum(wk_snow) == alltime["snowPROP"]["week_max"][0]: alltime["snowPROP"]["week_max"][1].append(y)
            elif sum(wk_snow) > alltime["snowPROP"]["week_max"][0]:
                alltime["snowPROP"]["week_max"][0] = sum(wk_snow)
                alltime["snowPROP"]["week_max"][1] = []
                alltime["snowPROP"]["week_max"][1].append(y)
            # "tempAVGlist": [],"tempAVGlist_ind":[],"tavgPROP":{"week_max":[-999,[]],"week_min":[999,[]]},
            if len(wk_tempAVGlist) > excludeweek_tavg:
                alltime["tempAVGlist"].append(round(mean(wk_tempAVGlist),1))
                if round(mean(wk_tempAVGlist),1) == alltime["tavgPROP"]["week_max"][0]: alltime["tavgPROP"]["week_max"][1].append(y)
                elif round(mean(wk_tempAVGlist),1) > alltime["tavgPROP"]["week_max"][0]:
                    alltime["tavgPROP"]["week_max"][0] = mean(wk_tempAVGlist)
                    alltime["tavgPROP"]["week_max"][1] = []
                    alltime["tavgPROP"]["week_max"][1].append(y)
                if round(mean(wk_tempAVGlist),1) == alltime["tavgPROP"]["week_min"][0]: alltime["tavgPROP"]["week_min"][1].append(y)
                elif round(mean(wk_tempAVGlist),1) < alltime["tavgPROP"]["week_min"][0]:
                    alltime["tavgPROP"]["week_min"][0] = round(mean(wk_tempAVGlist),1)
                    alltime["tavgPROP"]["week_min"][1] = []
                    alltime["tavgPROP"]["week_min"][1].append(y)                                                                   
            if len(wk_tmax) > excludeweek:
                if mean(wk_tmax) == alltime["tmaxPROP"]["week_max"][0]: alltime["tmaxPROP"]["week_max"][1].append(y)
                elif mean(wk_tmax) > alltime["tmaxPROP"]["week_max"][0]:
                    alltime["tmaxPROP"]["week_max"][0] = mean(wk_tmax)
                    alltime["tmaxPROP"]["week_max"][1] = []
                    alltime["tmaxPROP"]["week_max"][1].append(y)
                if mean(wk_tmax) == alltime["tmaxPROP"]["week_min"][0]: alltime["tmaxPROP"]["week_min"][1].append(y)
                elif mean(wk_tmax) < alltime["tmaxPROP"]["week_min"][0]:
                    alltime["tmaxPROP"]["week_min"][0] = mean(wk_tmax)
                    alltime["tmaxPROP"]["week_min"][1] = []
                    alltime["tmaxPROP"]["week_min"][1].append(y)
            if len(wk_tmin) > excludeweek:
                if mean(wk_tmin) == alltime["tminPROP"]["week_max"][0]: alltime["tminPROP"]["week_max"][1].append(y)
                elif mean(wk_tmin) > alltime["tminPROP"]["week_max"][0]:
                    alltime["tminPROP"]["week_max"][0] = mean(wk_tmin)
                    alltime["tminPROP"]["week_max"][1] = []
                    alltime["tminPROP"]["week_max"][1].append(y)
                if mean(wk_tmin) == alltime["tminPROP"]["week_min"][0]: alltime["tminPROP"]["week_min"][1].append(y)
                elif mean(wk_tmin) < alltime["tminPROP"]["week_min"][0]:
                    alltime["tminPROP"]["week_min"][0] = mean(wk_tmin)
                    alltime["tminPROP"]["week_min"][1] = []
                    alltime["tminPROP"]["week_min"][1].append(y)
            for c in climo30yrs:
                if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                    climo30yrs[c]["prcp"].append(sum(wk_prcp))
                    climo30yrs[c]["snow"].append(sum(wk_snow))
                    if sum(wk_prcp) == climo30yrs[c]["prcpPROP"]["week_max"][0]: climo30yrs[c]["prcpPROP"]["week_max"][1].append(y)
                    elif sum(wk_prcp) > climo30yrs[c]["prcpPROP"]["week_max"][0]:
                        climo30yrs[c]["prcpPROP"]["week_max"][0] = sum(wk_prcp)
                        climo30yrs[c]["prcpPROP"]["week_max"][1] = []
                        climo30yrs[c]["prcpPROP"]["week_max"][1].append(y)
                    if sum(wk_snow) == climo30yrs[c]["snowPROP"]["week_max"][0]: climo30yrs[c]["snowPROP"]["week_max"][1].append(y)
                    elif sum(wk_snow) > climo30yrs[c]["snowPROP"]["week_max"][0]:
                        climo30yrs[c]["snowPROP"]["week_max"][0] = sum(wk_snow)
                        climo30yrs[c]["snowPROP"]["week_max"][1] = []
                        climo30yrs[c]["snowPROP"]["week_max"][1].append(y)
                    if len(wk_tempAVGlist) > excludeweek_tavg:
                        climo30yrs[c]["tempAVGlist"].append(round(mean(wk_tempAVGlist),1))
                        if round(mean(wk_tempAVGlist),1) == climo30yrs[c]["tavgPROP"]["week_max"][0]: climo30yrs[c]["tavgPROP"]["week_max"][1].append(y)
                        elif round(mean(wk_tempAVGlist),1) > climo30yrs[c]["tavgPROP"]["week_max"][0]:
                            climo30yrs[c]["tavgPROP"]["week_max"][0] = mean(wk_tempAVGlist)
                            climo30yrs[c]["tavgPROP"]["week_max"][1] = []
                            climo30yrs[c]["tavgPROP"]["week_max"][1].append(y)
                        if round(mean(wk_tempAVGlist),1) == climo30yrs[c]["tavgPROP"]["week_min"][0]: climo30yrs[c]["tavgPROP"]["week_min"][1].append(y)
                        elif round(mean(wk_tempAVGlist),1) < climo30yrs[c]["tavgPROP"]["week_min"][0]:
                            climo30yrs[c]["tavgPROP"]["week_min"][0] = round(mean(wk_tempAVGlist),1)
                            climo30yrs[c]["tavgPROP"]["week_min"][1] = []
                            climo30yrs[c]["tavgPROP"]["week_min"][1].append(y)
                    if len(wk_tmax) > excludeweek:
                        if mean(wk_tmax) == climo30yrs[c]["tmaxPROP"]["week_max"][0]: climo30yrs[c]["tmaxPROP"]["week_max"][1].append(y)
                        elif mean(wk_tmax) > climo30yrs[c]["tmaxPROP"]["week_max"][0]:
                            climo30yrs[c]["tmaxPROP"]["week_max"][0] = mean(wk_tmax)
                            climo30yrs[c]["tmaxPROP"]["week_max"][1] = []
                            climo30yrs[c]["tmaxPROP"]["week_max"][1].append(y)
                        if mean(wk_tmax) == climo30yrs[c]["tmaxPROP"]["week_min"][0]: climo30yrs[c]["tmaxPROP"]["week_min"][1].append(y)
                        elif mean(wk_tmax) < climo30yrs[c]["tmaxPROP"]["week_min"][0]:
                            climo30yrs[c]["tmaxPROP"]["week_min"][0] = mean(wk_tmax)
                            climo30yrs[c]["tmaxPROP"]["week_min"][1] = []
                            climo30yrs[c]["tmaxPROP"]["week_min"][1].append(y)
                    if len(wk_tmin) > excludeweek:
                        if mean(wk_tmin) == climo30yrs[c]["tminPROP"]["week_max"][0]: climo30yrs[c]["tminPROP"]["week_max"][1].append(y)
                        elif mean(wk_tmin) > climo30yrs[c]["tminPROP"]["week_max"][0]:
                            climo30yrs[c]["tminPROP"]["week_max"][0] = mean(wk_tmin)
                            climo30yrs[c]["tminPROP"]["week_max"][1] = []
                            climo30yrs[c]["tminPROP"]["week_max"][1].append(y)
                        if mean(wk_tmin) == climo30yrs[c]["tminPROP"]["week_min"][0]: climo30yrs[c]["tminPROP"]["week_min"][1].append(y)
                        elif mean(wk_tmin) < climo30yrs[c]["tminPROP"]["week_min"][0]:
                            climo30yrs[c]["tminPROP"]["week_min"][0] = mean(wk_tmin)
                            climo30yrs[c]["tminPROP"]["week_min"][1] = []
                            climo30yrs[c]["tminPROP"]["week_min"][1].append(y)
        wkstart = datetime.date(1999,m,d) - datetime.timedelta(days=3)
        currday = wkstart

    # PRINT REPORT
    print("--------------------------------------------------")
    print("Climatology Report for the Week of {:%b} {:%d} - {:%b} {:%d}".format(wkstart,wkstart,wkend,wkend))
    print("City: {}, {}".format(clmt["station"],clmt["station_name"]))
    print("{}-{}; {}-Year Incremented {}-Year Climatologies".format(min(valid_yrs),max(valid_yrs),clmt_inc_rpt,clmt_len_rpt))
    print("--------------------------------------------------")

    print("\nPart 1: Precipitation Stats")
    print("{:▒^9} {:▒^11} {:▒^6} {:▒^12} {:▒^11} {:▒^6} {:▒^12}".format("Years","PRCP","PRCP","PRCP","SNOW","SNOW","SNOW"))
    print("{:▒^9} {:▒^11} {:▒^6} {:▒^12} {:▒^11} {:▒^6} {:▒^12}".format("","DAYS","AVG", "MAX","DAYS","AVG", "MAX"))
    #         Y     PD     PA      PM       SD     SA      SM
    print("{:-^9} {:-^11} {:-^6} {:-^12} {:-^11} {:-^6} {:-^12}".format("","","","","","",""))
    print("{:^9} {:4}:{:>5}% {:^6.2f} {:>5.2f}, {:^5} {:4}:{:>5}% {:^6.1f} {:>5.1f}, {:^5}".format("All Time",
        alltime["prcpPROP"]["days"],
        round(100 * alltime["prcpPROP"]["days"] / alltime["total_days"],1),
        round(mean(alltime["prcp"]),2),
        round(alltime["prcpPROP"]["week_max"][0],2),
        alltime["prcpPROP"]["week_max"][1][0] if len(alltime["prcpPROP"]["week_max"][1]) == 1 else len(alltime["prcpPROP"]["week_max"][1]),
        alltime["snowPROP"]["days"],
        round(100 * alltime["snowPROP"]["days"] / alltime["total_days"],1),
        round(mean(alltime["snow"]),1),
        round(alltime["snowPROP"]["week_max"][0],2),
        alltime["snowPROP"]["week_max"][1][0] if len(alltime["snowPROP"]["week_max"][1]) == 1 else len(alltime["snowPROP"]["week_max"][1])))

    for c in climo30yrs:
        try:
            print("{:^9} {:4}:{:>5}% {:^6.2f} {:>5.2f}, {:^5} {:4}:{:>5}% {:^6.1f} {:>5.1f}, {:^5}".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
            climo30yrs[c]["prcpPROP"]["days"],
            round(100 * climo30yrs[c]["prcpPROP"]["days"] / climo30yrs[c]["total_days"],1),
            round(mean(climo30yrs[c]["prcp"]),2),
            round(climo30yrs[c]["prcpPROP"]["week_max"][0],2),
            climo30yrs[c]["prcpPROP"]["week_max"][1][0] if len(climo30yrs[c]["prcpPROP"]["week_max"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["week_max"][1]),
            climo30yrs[c]["snowPROP"]["days"],
            round(100 * climo30yrs[c]["snowPROP"]["days"] / climo30yrs[c]["total_days"],1),
            round(mean(climo30yrs[c]["snow"]),1),
            round(climo30yrs[c]["snowPROP"]["week_max"][0],2),
            climo30yrs[c]["snowPROP"]["week_max"][1][0] if len(climo30yrs[c]["snowPROP"]["week_max"][1]) == 1 else len(climo30yrs[c]["snowPROP"]["week_max"][1])))
        except:
            pass

    print("\nPart 2: Temperature Stats")
    print("{:▒^9} {:▒^37} | {:▒^37} | {:▒^37}".format("Years","AVG TEMP","TMAX","TMIN"))
    print("{:▒^9} {:▒<5} {:▒^5} {:▒^12} {:▒^12} | {:▒<5} {:▒^5} {:▒^12} {:▒^12} | {:▒<5} {:▒^5} {:▒^12} {:▒^12}".format("","STDEV","AVG","MAX","MIN","STDEV","AVG","MAX","MIN","STDEV","AVG","MAX","MIN"))
    #         Y    TSTDV   TMA     TMX    TMn      TSTDV   TMA     TMX    TMn      TSTDV   TMA     TMX    TMn    
    # "tempAVGlist": [],"tavgPROP":{"week_max":[-999,[]],"week_min":[999,[]]},
    print("{:-^9} {:-^5} {:-^5} {:-^12} {:-^12} | {:-^5} {:-^5} {:-^12} {:-^12} | {:-^5} {:-^5} {:-^12} {:-^12}".format("","","","","","","","","","","","",""))
    print("{:^9} {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5}".format("All Time",
        round(pstdev(alltime["tempAVGlist"]),1),
        round(mean(alltime["tempAVGlist_ind"]),1),
        round(alltime["tavgPROP"]["week_max"][0],1),
        alltime["tavgPROP"]["week_max"][1][0] if len(alltime["tavgPROP"]["week_max"][1]) == 1 else len(alltime["tavgPROP"]["week_max"][1]),
        round(alltime["tavgPROP"]["week_min"][0],1),
        alltime["tavgPROP"]["week_min"][1][0] if len(alltime["tavgPROP"]["week_min"][1]) == 1 else len(alltime["tavgPROP"]["week_min"][1]),
        round(pstdev(alltime["tmax"]),1),
        round(mean(alltime["tmax"]),1),
        round(alltime["tmaxPROP"]["week_max"][0],1),
        alltime["tmaxPROP"]["week_max"][1][0] if len(alltime["tmaxPROP"]["week_max"][1]) == 1 else len(alltime["tmaxPROP"]["week_max"][1]),
        round(alltime["tmaxPROP"]["week_min"][0],1),
        alltime["tmaxPROP"]["week_min"][1][0] if len(alltime["tmaxPROP"]["week_min"][1]) == 1 else len(alltime["tmaxPROP"]["week_min"][1]),
        round(pstdev(alltime["tmin"]),1),
        round(mean(alltime["tmin"]),1),
        round(alltime["tminPROP"]["week_max"][0],1),
        alltime["tminPROP"]["week_max"][1][0] if len(alltime["tminPROP"]["week_max"][1]) == 1 else len(alltime["tminPROP"]["week_max"][1]),
        round(alltime["tminPROP"]["week_min"][0],1),
        alltime["tminPROP"]["week_min"][1][0] if len(alltime["tminPROP"]["week_min"][1]) == 1 else len(alltime["tminPROP"]["week_min"][1])))
    for c in climo30yrs:
        try:
            print("{:^9} {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5}".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
                round(pstdev(climo30yrs[c]["tempAVGlist"]),1),
                round(mean(climo30yrs[c]["tempAVGlist_ind"]),1),
                round(climo30yrs[c]["tavgPROP"]["week_max"][0],1),
                climo30yrs[c]["tavgPROP"]["week_max"][1][0] if len(climo30yrs[c]["tavgPROP"]["week_max"][1]) == 1 else len(climo30yrs[c]["tavgPROP"]["week_max"][1]),
                round(climo30yrs[c]["tavgPROP"]["week_min"][0],1),
                climo30yrs[c]["tavgPROP"]["week_min"][1][0] if len(climo30yrs[c]["tavgPROP"]["week_min"][1]) == 1 else len(climo30yrs[c]["tavgPROP"]["week_min"][1]),
                round(pstdev(climo30yrs[c]["tmax"]),1),
                round(mean(climo30yrs[c]["tmax"]),1),
                round(climo30yrs[c]["tmaxPROP"]["week_max"][0],1),
                climo30yrs[c]["tmaxPROP"]["week_max"][1][0] if len(climo30yrs[c]["tmaxPROP"]["week_max"][1]) == 1 else len(climo30yrs[c]["tmaxPROP"]["week_max"][1]),
                round(climo30yrs[c]["tmaxPROP"]["week_min"][0],1),
                climo30yrs[c]["tmaxPROP"]["week_min"][1][0] if len(climo30yrs[c]["tmaxPROP"]["week_min"][1]) == 1 else len(climo30yrs[c]["tmaxPROP"]["week_min"][1]),
                round(pstdev(climo30yrs[c]["tmin"]),1),
                round(mean(climo30yrs[c]["tmin"]),1),
                round(climo30yrs[c]["tminPROP"]["week_max"][0],1),
                climo30yrs[c]["tminPROP"]["week_max"][1][0] if len(climo30yrs[c]["tminPROP"]["week_max"][1]) == 1 else len(climo30yrs[c]["tminPROP"]["week_max"][1]),
                round(climo30yrs[c]["tminPROP"]["week_min"][0],1),
                climo30yrs[c]["tminPROP"]["week_min"][1][0] if len(climo30yrs[c]["tminPROP"]["week_min"][1]) == 1 else len(climo30yrs[c]["tminPROP"]["week_min"][1])))
        except Exception as e:
            print("ERROR: Era = {}; Exception = {}".format(c,e))
    print("")

    if "output" in output and output["output"] == True:
        newfn = "weekReport_centered_" + str(calendar.month_abbr[m]) + str(d) + "_" + str(clmt_len_rpt) + "YRclimo_" + str(clmt_inc_rpt) + "YRincr_" + clmt["station_name"] + ".csv"
        with open(newfn,"w") as w:
            headers = ["Assessed Period ({}-{} thru {}-{})".format(wkstart.month,wkstart.day,wkend.month,wkend.day),"PRCP Days","PRCP % of days","PRCP stdev","PRCP AVG","SNOW Days","SNOW % of days","SNOW stdev","SNOW AVG","TAVG stdev","TAVG","TMAX stdev","TMAX","TMIN stdev","TMIN"]
            # HEADER
            for x in range(len(headers)):
                if x != len(headers) - 1: w.write(headers[x]); w.write(",")
                else: w.write(headers[x]); w.write("\n")
            w.write("{}-{}".format(alltime["years"][0],alltime["years"][1])); w.write(",")
            w.write("{}".format(alltime["prcpPROP"]["days"])); w.write(",")
            w.write("{:.1f}".format(round(100 * alltime["prcpPROP"]["days"] / alltime["total_days"],1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["prcp"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["prcp"]),1))); w.write(",")
            w.write("{}".format(alltime["snowPROP"]["days"])); w.write(",")
            w.write("{:.1f}".format(round(100 * alltime["snowPROP"]["days"] / alltime["total_days"],1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["snow"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["snow"]),1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tempAVGlist"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["tempAVGlist_ind"]),1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tmax"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["tmax"]),1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tmin"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["tmin"]),1))); w.write("\n")
            for x in climo30yrs:
                w.write("{}-{}".format(climo30yrs[x]["years"][0],climo30yrs[x]["years"][1])); w.write(",")
                w.write("{}".format(climo30yrs[x]["prcpPROP"]["days"])); w.write(",")
                w.write("{:.1f}".format(round(100 * climo30yrs[x]["prcpPROP"]["days"] / climo30yrs[x]["total_days"],1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["prcp"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["prcp"]),1))); w.write(",")
                w.write("{}".format(climo30yrs[x]["snowPROP"]["days"])); w.write(",")
                w.write("{:.1f}".format(round(100 * climo30yrs[x]["snowPROP"]["days"] / climo30yrs[x]["total_days"],1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["snow"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["snow"]),1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tempAVGlist"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["tempAVGlist_ind"]),1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tmax"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["tmax"]),1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tmin"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["tmin"]),1))); w.write("\n")
            print("*** csv output successful ***")

def monthReport(m,**output):
    """Detailed Climatological Report for recorded statistics from a month of
    interest. It only accepts an argument for the month of interest. Passed
    argument MUST be an integer.
    
    monthReport(month,**{output=False})
    
    EXAMPLE: monthReport(11) -> Returns a climatological report for November.
    """
    #print([x for x in clmt.keys()])
    valid_yrs = [x for x in clmt.keys() if type(x) == int]
    valid_yrs.sort()
    climo30yrs = {}
    for x in range(1811,max(valid_yrs)+1,clmt_inc_rpt):
        if x in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]) and x+clmt_len_rpt-1 in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]+1):
            climo30yrs[(x,x+clmt_len_rpt-1)] = {"years":(x,x+clmt_len_rpt-1),"total_days":0,
                                    "prcp": [],"prcpPROP":{"days":0,"month_max_days":[-1,[]],"month_min_days":[999,[]],"month_max":[-1,[]],"month_min":[999,[]]},
                                    "snow": [],"snowPROP":{"days":0,"month_max_days":[-1,[]],"month_max":[-1,[]]},
                                    "tempAVGlist": [],"tempAVGlist_ind":[],"tavgPROP":{"month_max":[-999,[]],"month_min":[999,[]]},
                                    "tmax": [],"tmaxPROP":{"month_max":[-999,[]],"month_min":[999,[]]},
                                    "tmin": [],"tminPROP":{"month_max":[-999,[]],"month_min":[999,[]]}}

    alltime = {"years":(valid_yrs[0],valid_yrs[len(valid_yrs)-1]),"total_days":0,
               "prcp": [],"prcpPROP":{"days":0,"month_max_days":[-1,[]],"month_min_days":[999,[]],"month_max":[-1,[]],"month_min":[999,[]]},
               "snow": [],"snowPROP":{"days":0,"month_max_days":[-1,[]],"month_max":[-1,[]]},
               "tempAVGlist": [],"tempAVGlist_ind":[],"tavgPROP":{"month_max":[-999,[]],"month_min":[999,[]]},
               "tmax": [],"tmaxPROP":{"month_max":[-999,[]],"month_min":[999,[]]},
               "tmin": [],"tminPROP":{"month_max":[-999,[]],"month_min":[999,[]]}}
    # 'recordqty', 'prcp', 'prcpDAYS', 'prcpPROP', 'snow', 'snowDAYS', 'snowPROP', 'tempAVGlist', 'tmax', 'tmaxPROP', 'tmin', 'tminPROP'
    for y in valid_yrs:
        if m in clmt[y]:
            alltime["total_days"] += clmt[y][m]["recordqty"]
            # PRCP
            alltime["prcp"].append(sum(clmt[y][m]["prcp"]))
            alltime["prcpPROP"]["days"] += clmt[y][m]["prcpDAYS"]
            if clmt[y][m]["prcpDAYS"] == alltime["prcpPROP"]["month_max_days"][0]: alltime["prcpPROP"]["month_max_days"][1].append(y)
            elif clmt[y][m]["prcpDAYS"] > alltime["prcpPROP"]["month_max_days"][0]:
                alltime["prcpPROP"]["month_max_days"][0] = clmt[y][m]["prcpDAYS"]
                alltime["prcpPROP"]["month_max_days"][1] = []
                alltime["prcpPROP"]["month_max_days"][1].append(y)
            if sum(clmt[y][m]["prcp"]) == alltime["prcpPROP"]["month_max"][0]: alltime["prcpPROP"]["month_max"][1].append(y)
            elif sum(clmt[y][m]["prcp"]) > alltime["prcpPROP"]["month_max"][0]:
                alltime["prcpPROP"]["month_max"][0] = sum(clmt[y][m]["prcp"])
                alltime["prcpPROP"]["month_max"][1] = []
                alltime["prcpPROP"]["month_max"][1].append(y)
            if clmt[y][m]["recordqty"] > excludemonth:
                if clmt[y][m]["prcpDAYS"] == alltime["prcpPROP"]["month_min_days"][0]: alltime["prcpPROP"]["month_min_days"][1].append(y)
                elif clmt[y][m]["prcpDAYS"] < alltime["prcpPROP"]["month_min_days"][0]:
                    alltime["prcpPROP"]["month_min_days"][0] = clmt[y][m]["prcpDAYS"]
                    alltime["prcpPROP"]["month_min_days"][1] = []
                    alltime["prcpPROP"]["month_min_days"][1].append(y)
                if sum(clmt[y][m]["prcp"]) == alltime["prcpPROP"]["month_min"][0]: alltime["prcpPROP"]["month_min"][1].append(y)
                elif sum(clmt[y][m]["prcp"]) < alltime["prcpPROP"]["month_min"][0]:
                    alltime["prcpPROP"]["month_min"][0] = sum(clmt[y][m]["prcp"])
                    alltime["prcpPROP"]["month_min"][1] = []
                    alltime["prcpPROP"]["month_min"][1].append(y)
            for c in climo30yrs:
                if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                    climo30yrs[c]["prcp"].append(sum(clmt[y][m]["prcp"]))
                    climo30yrs[c]["prcpPROP"]["days"] += clmt[y][m]["prcpDAYS"]
                    climo30yrs[c]["total_days"] += clmt[y][m]["recordqty"]
                    if clmt[y][m]["prcpDAYS"] == climo30yrs[c]["prcpPROP"]["month_max_days"][0]: climo30yrs[c]["prcpPROP"]["month_max_days"][1].append(y)
                    elif clmt[y][m]["prcpDAYS"] > climo30yrs[c]["prcpPROP"]["month_max_days"][0]:
                        climo30yrs[c]["prcpPROP"]["month_max_days"][0] = clmt[y][m]["prcpDAYS"]
                        climo30yrs[c]["prcpPROP"]["month_max_days"][1] = []
                        climo30yrs[c]["prcpPROP"]["month_max_days"][1].append(y)
                    if sum(clmt[y][m]["prcp"]) == climo30yrs[c]["prcpPROP"]["month_max"][0]: climo30yrs[c]["prcpPROP"]["month_max"][1].append(y)
                    elif sum(clmt[y][m]["prcp"]) > climo30yrs[c]["prcpPROP"]["month_max"][0]:
                        climo30yrs[c]["prcpPROP"]["month_max"][0] = sum(clmt[y][m]["prcp"])
                        climo30yrs[c]["prcpPROP"]["month_max"][1] = []
                        climo30yrs[c]["prcpPROP"]["month_max"][1].append(y)
                    if clmt[y][m]["recordqty"] > excludemonth:
                        if clmt[y][m]["prcpDAYS"] == climo30yrs[c]["prcpPROP"]["month_min_days"][0]: climo30yrs[c]["prcpPROP"]["month_min_days"][1].append(y)
                        elif clmt[y][m]["prcpDAYS"] < climo30yrs[c]["prcpPROP"]["month_min_days"][0]:
                            climo30yrs[c]["prcpPROP"]["month_min_days"][0] = clmt[y][m]["prcpDAYS"]
                            climo30yrs[c]["prcpPROP"]["month_min_days"][1] = []
                            climo30yrs[c]["prcpPROP"]["month_min_days"][1].append(y)
                        if sum(clmt[y][m]["prcp"]) == climo30yrs[c]["prcpPROP"]["month_min"][0]: climo30yrs[c]["prcpPROP"]["month_min"][1].append(y)
                        elif sum(clmt[y][m]["prcp"]) < climo30yrs[c]["prcpPROP"]["month_min"][0]:
                            climo30yrs[c]["prcpPROP"]["month_min"][0] = sum(clmt[y][m]["prcp"])
                            climo30yrs[c]["prcpPROP"]["month_min"][1] = []
                            climo30yrs[c]["prcpPROP"]["month_min"][1].append(y)

            # SNOW
            alltime["snow"].append(sum(clmt[y][m]["snow"]))
            alltime["snowPROP"]["days"] += clmt[y][m]["snowDAYS"]
            if clmt[y][m]["snowDAYS"] == alltime["snowPROP"]["month_max_days"][0]: alltime["snowPROP"]["month_max_days"][1].append(y)
            elif clmt[y][m]["snowDAYS"] > alltime["snowPROP"]["month_max_days"][0]:
                alltime["snowPROP"]["month_max_days"][0] = clmt[y][m]["snowDAYS"]
                alltime["snowPROP"]["month_max_days"][1] = []
                alltime["snowPROP"]["month_max_days"][1].append(y)
            if sum(clmt[y][m]["snow"]) == alltime["snowPROP"]["month_max"][0]: alltime["snowPROP"]["month_max"][1].append(y)
            elif sum(clmt[y][m]["snow"]) > alltime["snowPROP"]["month_max"][0]:
                alltime["snowPROP"]["month_max"][0] = sum(clmt[y][m]["snow"])
                alltime["snowPROP"]["month_max"][1] = []
                alltime["snowPROP"]["month_max"][1].append(y)
            for c in climo30yrs:
                if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                    climo30yrs[c]["snow"].append(sum(clmt[y][m]["snow"]))
                    climo30yrs[c]["snowPROP"]["days"] += clmt[y][m]["snowDAYS"]
                    if clmt[y][m]["snowDAYS"] == climo30yrs[c]["snowPROP"]["month_max_days"][0]: climo30yrs[c]["snowPROP"]["month_max_days"][1].append(y)
                    elif clmt[y][m]["snowDAYS"] > climo30yrs[c]["snowPROP"]["month_max_days"][0]:
                        climo30yrs[c]["snowPROP"]["month_max_days"][0] = clmt[y][m]["snowDAYS"]
                        climo30yrs[c]["snowPROP"]["month_max_days"][1] = []
                        climo30yrs[c]["snowPROP"]["month_max_days"][1].append(y)
                    if sum(clmt[y][m]["snow"]) == climo30yrs[c]["snowPROP"]["month_max"][0]: climo30yrs[c]["snowPROP"]["month_max"][1].append(y)
                    elif sum(clmt[y][m]["snow"]) > climo30yrs[c]["snowPROP"]["month_max"][0]:
                        climo30yrs[c]["snowPROP"]["month_max"][0] = sum(clmt[y][m]["snow"])
                        climo30yrs[c]["snowPROP"]["month_max"][1] = []
                        climo30yrs[c]["snowPROP"]["month_max"][1].append(y)
    # 'recordqty', 'prcp', 'prcpDAYS', 'prcpPROP', 'snow', 'snowDAYS', 'snowPROP', 'tempAVGlist', 'tmax', 'tmaxPROP', 'tmin', 'tminPROP'
            # TAVG
            for x in clmt[y][m]["tempAVGlist"]: alltime["tempAVGlist_ind"].append(x)
            if len(clmt[y][m]["tempAVGlist"]) > excludemonth_tavg:
                alltime["tempAVGlist"].append(mean(clmt[y][m]["tempAVGlist"]))
                if mean(clmt[y][m]["tempAVGlist"]) == alltime["tavgPROP"]["month_max"][0]: alltime["tavgPROP"]["month_max"][1].append(y)
                elif mean(clmt[y][m]["tempAVGlist"]) > alltime["tavgPROP"]["month_max"][0]:
                    alltime["tavgPROP"]["month_max"][0] = mean(clmt[y][m]["tempAVGlist"])
                    alltime["tavgPROP"]["month_max"][1] = []
                    alltime["tavgPROP"]["month_max"][1].append(y)
                if mean(clmt[y][m]["tempAVGlist"]) == alltime["tavgPROP"]["month_min"][0]: alltime["tavgPROP"]["month_min"][1].append(y)
                elif mean(clmt[y][m]["tempAVGlist"]) < alltime["tavgPROP"]["month_min"][0]:
                    alltime["tavgPROP"]["month_min"][0] = mean(clmt[y][m]["tempAVGlist"])
                    alltime["tavgPROP"]["month_min"][1] = []
                    alltime["tavgPROP"]["month_min"][1].append(y)
            for c in climo30yrs:
                if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                    for x in clmt[y][m]["tempAVGlist"]:climo30yrs[c]["tempAVGlist_ind"].append(x)
                    if len(clmt[y][m]["tempAVGlist"]) > excludemonth_tavg:
                        climo30yrs[c]["tempAVGlist"].append(mean(clmt[y][m]["tempAVGlist"]))                    
                        if mean(clmt[y][m]["tempAVGlist"]) == climo30yrs[c]["tavgPROP"]["month_max"][0]: climo30yrs[c]["tavgPROP"]["month_max"][1].append(y)
                        elif mean(clmt[y][m]["tempAVGlist"]) > climo30yrs[c]["tavgPROP"]["month_max"][0]:
                            climo30yrs[c]["tavgPROP"]["month_max"][0] = mean(clmt[y][m]["tempAVGlist"])
                            climo30yrs[c]["tavgPROP"]["month_max"][1] = []
                            climo30yrs[c]["tavgPROP"]["month_max"][1].append(y)
                        if mean(clmt[y][m]["tempAVGlist"]) == climo30yrs[c]["tavgPROP"]["month_min"][0]: climo30yrs[c]["tavgPROP"]["month_min"][1].append(y)
                        elif mean(clmt[y][m]["tempAVGlist"]) < climo30yrs[c]["tavgPROP"]["month_min"][0]:
                            climo30yrs[c]["tavgPROP"]["month_min"][0] = mean(clmt[y][m]["tempAVGlist"])
                            climo30yrs[c]["tavgPROP"]["month_min"][1] = []
                            climo30yrs[c]["tavgPROP"]["month_min"][1].append(y)
            # TMAX
            for x in clmt[y][m]["tmax"]: alltime["tmax"].append(x)
            if len(clmt[y][m]["tmax"]) > excludemonth:
                if mean(clmt[y][m]["tmax"]) == alltime["tmaxPROP"]["month_max"][0]: alltime["tmaxPROP"]["month_max"][1].append(y)
                elif mean(clmt[y][m]["tmax"]) > alltime["tmaxPROP"]["month_max"][0]:
                    alltime["tmaxPROP"]["month_max"][0] = mean(clmt[y][m]["tmax"])
                    alltime["tmaxPROP"]["month_max"][1] = []
                    alltime["tmaxPROP"]["month_max"][1].append(y)
                if mean(clmt[y][m]["tmax"]) == alltime["tmaxPROP"]["month_min"][0]: alltime["tmaxPROP"]["month_min"][1].append(y)
                elif mean(clmt[y][m]["tmax"]) < alltime["tmaxPROP"]["month_min"][0]:
                    alltime["tmaxPROP"]["month_min"][0] = mean(clmt[y][m]["tmax"])
                    alltime["tmaxPROP"]["month_min"][1] = []
                    alltime["tmaxPROP"]["month_min"][1].append(y)
            for c in climo30yrs:
                if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                    for x in clmt[y][m]["tmax"]: climo30yrs[c]["tmax"].append(x)
                    if len(clmt[y][m]["tmax"]) > excludemonth:
                        if mean(clmt[y][m]["tmax"]) == climo30yrs[c]["tmaxPROP"]["month_max"][0]: climo30yrs[c]["tmaxPROP"]["month_max"][1].append(y)
                        elif mean(clmt[y][m]["tmax"]) > climo30yrs[c]["tmaxPROP"]["month_max"][0]:
                            climo30yrs[c]["tmaxPROP"]["month_max"][0] = mean(clmt[y][m]["tmax"])
                            climo30yrs[c]["tmaxPROP"]["month_max"][1] = []
                            climo30yrs[c]["tmaxPROP"]["month_max"][1].append(y)
                        if mean(clmt[y][m]["tmax"]) == climo30yrs[c]["tmaxPROP"]["month_min"][0]: climo30yrs[c]["tmaxPROP"]["month_min"][1].append(y)
                        elif mean(clmt[y][m]["tmax"]) < climo30yrs[c]["tmaxPROP"]["month_min"][0]:
                            climo30yrs[c]["tmaxPROP"]["month_min"][0] = mean(clmt[y][m]["tmax"])
                            climo30yrs[c]["tmaxPROP"]["month_min"][1] = []
                            climo30yrs[c]["tmaxPROP"]["month_min"][1].append(y)
            # TMIN
            for x in clmt[y][m]["tmin"]: alltime["tmin"].append(x)
            if len(clmt[y][m]["tmin"]) > excludemonth:
                if mean(clmt[y][m]["tmin"]) == alltime["tminPROP"]["month_max"][0]: alltime["tminPROP"]["month_max"][1].append(y)
                elif mean(clmt[y][m]["tmin"]) > alltime["tminPROP"]["month_max"][0]:
                    alltime["tminPROP"]["month_max"][0] = mean(clmt[y][m]["tmin"])
                    alltime["tminPROP"]["month_max"][1] = []
                    alltime["tminPROP"]["month_max"][1].append(y)
                if mean(clmt[y][m]["tmin"]) == alltime["tminPROP"]["month_min"][0]: alltime["tminPROP"]["month_min"][1].append(y)
                elif mean(clmt[y][m]["tmin"]) < alltime["tminPROP"]["month_min"][0]:
                    alltime["tminPROP"]["month_min"][0] = mean(clmt[y][m]["tmin"])
                    alltime["tminPROP"]["month_min"][1] = []
                    alltime["tminPROP"]["month_min"][1].append(y)
            for c in climo30yrs:
                if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                    for x in clmt[y][m]["tmin"]: climo30yrs[c]["tmin"].append(x)
                    if len(clmt[y][m]["tmin"]) > excludemonth:
                        if mean(clmt[y][m]["tmin"]) == climo30yrs[c]["tminPROP"]["month_max"][0]: climo30yrs[c]["tminPROP"]["month_max"][1].append(y)
                        elif mean(clmt[y][m]["tmin"]) > climo30yrs[c]["tminPROP"]["month_max"][0]:
                            climo30yrs[c]["tminPROP"]["month_max"][0] = mean(clmt[y][m]["tmin"])
                            climo30yrs[c]["tminPROP"]["month_max"][1] = []
                            climo30yrs[c]["tminPROP"]["month_max"][1].append(y)
                        if mean(clmt[y][m]["tmin"]) == climo30yrs[c]["tminPROP"]["month_min"][0]: climo30yrs[c]["tminPROP"]["month_min"][1].append(y)
                        elif mean(clmt[y][m]["tmin"]) < climo30yrs[c]["tminPROP"]["month_min"][0]:
                            climo30yrs[c]["tminPROP"]["month_min"][0] = mean(clmt[y][m]["tmin"])
                            climo30yrs[c]["tminPROP"]["month_min"][1] = []
                            climo30yrs[c]["tminPROP"]["month_min"][1].append(y)
    # PRINT REPORT
    print("--------------------------------")
    print("Climatology Report for {}".format(calendar.month_name[m]))
    print("City: {}, {}".format(clmt["station"],clmt["station_name"]))
    print("{}-{}; {}-Year Incremented {}-Year Climatologies".format(min(valid_yrs),max(valid_yrs),clmt_inc_rpt,clmt_len_rpt))
    print("--------------------------------")
    print("Part 1: {} Precipitation Stats".format(calendar.month_name[m]))
    print("{:▒^9} {:▒^11}  {:▒^8}  {:▒^8} {:▒^6} {:▒^12} {:▒^12} | {:▒^11}  {:▒^8} {:▒^6} {:▒^12} |".format("Years","PRCP","PRCP","PRCP","PRCP","PRCP","PRCP","SNOW","SNOW","SNOW","SNOW"))
    print("{:▒^9} {:▒^11}  {:▒^8}  {:▒^8} {:▒^6} {:▒^12} {:▒^12} | {:▒^11}  {:▒^8} {:▒^6} {:▒^12} |".format("","DAYS","DAYS MAX","DAYS MIN","AVG", "MAX","MIN","DAYS","DAYS MAX","AVG", "MAX"))
    #         Y     PD       PDx    PDn      PA      PM     Pmin      SD     SDx       SA      SM
    print("{:-^9} {:-^11}  {:-^8}  {:-^8} {:-^6} {:-^12} {:-^12} | {:-^11}  {:-^8} {:-^6} {:-^12} |".format("","","","","","","","","","",""))
    print("{:^9} {:4}:{:>5}%  {:>2}, {:^4}  {:>2}, {:^4} {:^6.2f} {:>5.2f}, {:^5} {:>5}, {:^5} | {:4}:{:>5}%  {:>2}, {:^4} {:^6.1f} {:>5.1f}, {:^5} |".format("All Time",
        alltime["prcpPROP"]["days"],
        round(100 * alltime["prcpPROP"]["days"] / alltime["total_days"],1),
        alltime["prcpPROP"]["month_max_days"][0],
        alltime["prcpPROP"]["month_max_days"][1][0] if len(alltime["prcpPROP"]["month_max_days"][1]) == 1 else len(alltime["prcpPROP"]["month_max_days"][1]),
        alltime["prcpPROP"]["month_min_days"][0],
        alltime["prcpPROP"]["month_min_days"][1][0] if len(alltime["prcpPROP"]["month_min_days"][1]) == 1 else len(alltime["prcpPROP"]["month_min_days"][1]),
        round(mean(alltime["prcp"]),2) if len(alltime["prcp"]) > 0 else "--",
        round(alltime["prcpPROP"]["month_max"][0],2),
        alltime["prcpPROP"]["month_max"][1][0] if len(alltime["prcpPROP"]["month_max"][1]) == 1 else len(alltime["prcpPROP"]["month_max"][1]),
        round(alltime["prcpPROP"]["month_min"][0],2),
        alltime["prcpPROP"]["month_min"][1][0] if len(alltime["prcpPROP"]["month_min"][1]) == 1 else len(alltime["prcpPROP"]["month_min"][1]),
        alltime["snowPROP"]["days"] if alltime["snowPROP"]["days"] > 0 else "--",
        round(100 * alltime["snowPROP"]["days"] / alltime["total_days"],1) if alltime["snowPROP"]["days"] > 0 else "--",
        alltime["snowPROP"]["month_max_days"][0],
        alltime["snowPROP"]["month_max_days"][1][0] if len(alltime["snowPROP"]["month_max_days"][1]) == 1 else len(alltime["snowPROP"]["month_max_days"][1]),
        round(mean(alltime["snow"]),1) if len(alltime["snow"]) > 0 else "--",
        round(alltime["snowPROP"]["month_max"][0],2),
        alltime["snowPROP"]["month_max"][1][0] if len(alltime["snowPROP"]["month_max"][1]) == 1 else len(alltime["snowPROP"]["month_max"][1])))
    for c in climo30yrs:
        #print(climo30yrs[c]["prcpPROP"]["days"],climo30yrs[c]["total_days"])
        #print(climo30yrs[c]["snowPROP"]["days"],climo30yrs[c]["total_days"])
        try:
            print("{:^9} {:4}:{:>5}%  {:>2}, {:^4}  {:>2}, {:^4} {:^6.2f} {:>5.2f}, {:^5} {:>5}, {:^5} | {:4}:{:>5}%  {:>2}, {:^4} {:^6.1f} {:>5.1f}, {:^5} |".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
            climo30yrs[c]["prcpPROP"]["days"],
            round(100 * climo30yrs[c]["prcpPROP"]["days"] / climo30yrs[c]["total_days"],1),
            climo30yrs[c]["prcpPROP"]["month_max_days"][0],
            climo30yrs[c]["prcpPROP"]["month_max_days"][1][0] if len(climo30yrs[c]["prcpPROP"]["month_max_days"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["month_max_days"][1]),
            climo30yrs[c]["prcpPROP"]["month_min_days"][0],
            climo30yrs[c]["prcpPROP"]["month_min_days"][1][0] if len(climo30yrs[c]["prcpPROP"]["month_min_days"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["month_min_days"][1]),
            round(mean(climo30yrs[c]["prcp"]),2),
            round(climo30yrs[c]["prcpPROP"]["month_max"][0],2),
            climo30yrs[c]["prcpPROP"]["month_max"][1][0] if len(climo30yrs[c]["prcpPROP"]["month_max"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["month_max"][1]),
            round(climo30yrs[c]["prcpPROP"]["month_min"][0],2),
            climo30yrs[c]["prcpPROP"]["month_min"][1][0] if len(climo30yrs[c]["prcpPROP"]["month_min"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["month_min"][1]),
            climo30yrs[c]["snowPROP"]["days"] if climo30yrs[c]["snowPROP"]["days"] > 0 else "--",
            round(100 * climo30yrs[c]["snowPROP"]["days"] / climo30yrs[c]["total_days"],1) if climo30yrs[c]["snowPROP"]["days"] > 0 else "--",
            climo30yrs[c]["snowPROP"]["month_max_days"][0],
            climo30yrs[c]["snowPROP"]["month_max_days"][1][0] if len(climo30yrs[c]["snowPROP"]["month_max_days"][1]) == 1 else len(climo30yrs[c]["snowPROP"]["month_max_days"][1]),
            round(mean(climo30yrs[c]["snow"]),1) if len(climo30yrs[c]["snow"]) > 0 else "--",
            round(climo30yrs[c]["snowPROP"]["month_max"][0],2),
            climo30yrs[c]["snowPROP"]["month_max"][1][0] if len(climo30yrs[c]["snowPROP"]["month_max"][1]) == 1 else len(climo30yrs[c]["snowPROP"]["month_max"][1])))
        except Exception as e:
            print("ERROR: Era = {}; Exception = {}".format(c,e))

    print("\nPart 2: {} Temperature Stats".format(calendar.month_name[m]))
    print("{:▒^9} {:▒^37} | {:▒^37} | {:▒^37}".format("Years","AVG TEMP","TMAX","TMIN"))
    print("{:▒^9} {:▒<5} {:▒^5} {:▒^12} {:▒^12} | {:▒<5} {:▒^5} {:▒^12} {:▒^12} | {:▒<5} {:▒^5} {:▒^12} {:▒^12}".format("","STDEV","AVG","MAX","MIN","STDEV","AVG","MAX","MIN","STDEV","AVG","MAX","MIN"))
    #         Y    TSTDV   TMA     TMX    TMn      TSTDV   TMA     TMX    TMn      TSTDV   TMA     TMX    TMn    
    # "tempAVGlist": [],"tavgPROP":{"month_max":[-999,[]],"month_min":[999,[]]},
    print("{:-^9} {:-^5} {:-^5} {:-^12} {:-^12} | {:-^5} {:-^5} {:-^12} {:-^12} | {:-^5} {:-^5} {:-^12} {:-^12}".format("","","","","","","","","","","","",""))
    print("{:^9} {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5}".format("All Time",
        round(pstdev(alltime["tempAVGlist"]),1),
        round(mean(alltime["tempAVGlist_ind"]),1),
        round(alltime["tavgPROP"]["month_max"][0],1),
        alltime["tavgPROP"]["month_max"][1][0] if len(alltime["tavgPROP"]["month_max"][1]) == 1 else len(alltime["tavgPROP"]["month_max"][1]),
        round(alltime["tavgPROP"]["month_min"][0],1),
        alltime["tavgPROP"]["month_min"][1][0] if len(alltime["tavgPROP"]["month_min"][1]) == 1 else len(alltime["tavgPROP"]["month_min"][1]),
        round(pstdev(alltime["tmax"]),1),
        round(mean(alltime["tmax"]),1),
        round(alltime["tmaxPROP"]["month_max"][0],1),
        alltime["tmaxPROP"]["month_max"][1][0] if len(alltime["tmaxPROP"]["month_max"][1]) == 1 else len(alltime["tmaxPROP"]["month_max"][1]),
        round(alltime["tmaxPROP"]["month_min"][0],1),
        alltime["tmaxPROP"]["month_min"][1][0] if len(alltime["tmaxPROP"]["month_min"][1]) == 1 else len(alltime["tmaxPROP"]["month_min"][1]),
        round(pstdev(alltime["tmin"]),1),
        round(mean(alltime["tmin"]),1),
        round(alltime["tminPROP"]["month_max"][0],1),
        alltime["tminPROP"]["month_max"][1][0] if len(alltime["tminPROP"]["month_max"][1]) == 1 else len(alltime["tminPROP"]["month_max"][1]),
        round(alltime["tminPROP"]["month_min"][0],1),
        alltime["tminPROP"]["month_min"][1][0] if len(alltime["tminPROP"]["month_min"][1]) == 1 else len(alltime["tminPROP"]["month_min"][1])))
    for c in climo30yrs:
        try:
            print("{:^9} {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5}".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
                round(pstdev(climo30yrs[c]["tempAVGlist"]),1),
                round(mean(climo30yrs[c]["tempAVGlist_ind"]),1),
                round(climo30yrs[c]["tavgPROP"]["month_max"][0],1),
                climo30yrs[c]["tavgPROP"]["month_max"][1][0] if len(climo30yrs[c]["tavgPROP"]["month_max"][1]) == 1 else len(climo30yrs[c]["tavgPROP"]["month_max"][1]),
                round(climo30yrs[c]["tavgPROP"]["month_min"][0],1),
                climo30yrs[c]["tavgPROP"]["month_min"][1][0] if len(climo30yrs[c]["tavgPROP"]["month_min"][1]) == 1 else len(climo30yrs[c]["tavgPROP"]["month_min"][1]),
                round(pstdev(climo30yrs[c]["tmax"]),1),
                round(mean(climo30yrs[c]["tmax"]),1),
                round(climo30yrs[c]["tmaxPROP"]["month_max"][0],1),
                climo30yrs[c]["tmaxPROP"]["month_max"][1][0] if len(climo30yrs[c]["tmaxPROP"]["month_max"][1]) == 1 else len(climo30yrs[c]["tmaxPROP"]["month_max"][1]),
                round(climo30yrs[c]["tmaxPROP"]["month_min"][0],1),
                climo30yrs[c]["tmaxPROP"]["month_min"][1][0] if len(climo30yrs[c]["tmaxPROP"]["month_min"][1]) == 1 else len(climo30yrs[c]["tmaxPROP"]["month_min"][1]),
                round(pstdev(climo30yrs[c]["tmin"]),1),
                round(mean(climo30yrs[c]["tmin"]),1),
                round(climo30yrs[c]["tminPROP"]["month_max"][0],1),
                climo30yrs[c]["tminPROP"]["month_max"][1][0] if len(climo30yrs[c]["tminPROP"]["month_max"][1]) == 1 else len(climo30yrs[c]["tminPROP"]["month_max"][1]),
                round(climo30yrs[c]["tminPROP"]["month_min"][0],1),
                climo30yrs[c]["tminPROP"]["month_min"][1][0] if len(climo30yrs[c]["tminPROP"]["month_min"][1]) == 1 else len(climo30yrs[c]["tminPROP"]["month_min"][1])))
        except Exception as e:
            print("ERROR: Era = {}; Exception = {}".format(c,e))
    print("")
    
    if "output" in output and output["output"] == True:
        newfn = "monthReport_" + str(calendar.month_name[m]) + "_" + str(clmt_len_rpt) + "YRclimo_" + str(clmt_inc_rpt) + "YRincr_" + clmt["station_name"] + ".csv"
        with open(newfn,"w") as w:
            headers = ["Assessed Period ({})".format(str(calendar.month_name[m])),"PRCP Days","PRCP % of days","PRCP stdev","PRCP AVG","SNOW Days","SNOW % of days","SNOW stdev","SNOW AVG","TAVG stdev","TAVG","TMAX stdev","TMAX","TMIN stdev","TMIN"]
            # HEADER
            for x in range(len(headers)):
                if x != len(headers) - 1: w.write(headers[x]); w.write(",")
                else: w.write(headers[x]); w.write("\n")
            w.write("{}-{}".format(alltime["years"][0],alltime["years"][1])); w.write(",")
            w.write("{}".format(alltime["prcpPROP"]["days"])); w.write(",")
            w.write("{:.1f}".format(round(100 * alltime["prcpPROP"]["days"] / alltime["total_days"],1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["prcp"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["prcp"]),1))); w.write(",")
            w.write("{}".format(alltime["snowPROP"]["days"])); w.write(",")
            w.write("{:.1f}".format(round(100 * alltime["snowPROP"]["days"] / alltime["total_days"],1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["snow"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["snow"]),1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tempAVGlist"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["tempAVGlist_ind"]),1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tmax"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["tmax"]),1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tmin"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["tmin"]),1))); w.write("\n")
            for x in climo30yrs:
                w.write("{}-{}".format(climo30yrs[x]["years"][0],climo30yrs[x]["years"][1])); w.write(",")
                w.write("{}".format(climo30yrs[x]["prcpPROP"]["days"])); w.write(",")
                w.write("{:.1f}".format(round(100 * climo30yrs[x]["prcpPROP"]["days"] / climo30yrs[x]["total_days"],1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["prcp"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["prcp"]),1))); w.write(",")
                w.write("{}".format(climo30yrs[x]["snowPROP"]["days"])); w.write(",")
                w.write("{:.1f}".format(round(100 * climo30yrs[x]["snowPROP"]["days"] / climo30yrs[x]["total_days"],1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["snow"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["snow"]),1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tempAVGlist"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["tempAVGlist_ind"]),1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tmax"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["tmax"]),1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tmin"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["tmin"]),1))); w.write("\n")
            print("*** csv output successful ***")

def yearReport(**output):
    """Detailed Climatological Report for recorded statistics from all years
    on record, from January to December.
    
    yearReport(**{output=False})
    
    EXAMPLE: yearReport() -> Returns a climatological report for all years on
                             record.
    """
    valid_yrs = [x for x in clmt.keys() if type(x) == int]
    valid_yrs.sort()
    climo30yrs = {}
    for x in range(1811,max(valid_yrs)+1,clmt_inc_rpt):
        if x in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]) and x+clmt_len_rpt-1 in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]+1):
            climo30yrs[(x,x+clmt_len_rpt-1)] = {"years":(x,x+clmt_len_rpt-1),"total_days":0,
                                    "prcp": [],"prcpPROP":{"days":0,"year_max_days":[-1,[]],"year_min_days":[999,[]],"year_max":[-1,[]],"year_min":[999,[]]},
                                    "snow": [],"snowPROP":{"days":0,"year_max_days":[-1,[]],"year_max":[-1,[]]},
                                    "tempAVGlist": [],"tempAVGlist_ind":[],"tavgPROP":{"year_max":[-999,[]],"year_min":[999,[]]},
                                    "tmax": [],"tmaxPROP":{"year_max":[-999,[]],"year_min":[999,[]]},
                                    "tmin": [],"tminPROP":{"year_max":[-999,[]],"year_min":[999,[]]}}

    alltime = {"years":(valid_yrs[0],valid_yrs[len(valid_yrs)-1]),"total_days":0,
               "prcp": [],"prcpPROP":{"days":0,"year_max_days":[-1,[]],"year_min_days":[999,[]],"year_max":[-1,[]],"year_min":[999,[]]},
               "snow": [],"snowPROP":{"days":0,"year_max_days":[-1,[]],"year_max":[-1,[]]},
               "tempAVGlist": [],"tempAVGlist_ind":[],"tavgPROP":{"year_max":[-999,[]],"year_min":[999,[]]},
               "tmax": [],"tmaxPROP":{"year_max":[-999,[]],"year_min":[999,[]]},
               "tmin": [],"tminPROP":{"year_max":[-999,[]],"year_min":[999,[]]}}

    print("*** PLEASE WAIT. This will take a few moments ***")

    for y in valid_yrs:
        # 'recordqty', 'prcp', 'prcpDAYS', 'prcpPROP', 'snow', 'snowDAYS', 'snowPROP', 'tempAVGlist', 'tmax', 'tmaxPROP', 'tmin', 'tminPROP'
        alltime["total_days"] += clmt[y]["recordqty"]
        # PRCP
        alltime["prcp"].append(sum(clmt[y]["prcp"]))
        alltime["prcpPROP"]["days"] += clmt[y]["prcpDAYS"]
        if clmt[y]["prcpDAYS"] == alltime["prcpPROP"]["year_max_days"][0]: alltime["prcpPROP"]["year_max_days"][1].append(y)
        elif clmt[y]["prcpDAYS"] > alltime["prcpPROP"]["year_max_days"][0]:
            alltime["prcpPROP"]["year_max_days"][0] = clmt[y]["prcpDAYS"]
            alltime["prcpPROP"]["year_max_days"][1] = []
            alltime["prcpPROP"]["year_max_days"][1].append(y)
        if sum(clmt[y]["prcp"]) == alltime["prcpPROP"]["year_max"][0]: alltime["prcpPROP"]["year_max"][1].append(y)
        elif sum(clmt[y]["prcp"]) > alltime["prcpPROP"]["year_max"][0]:
            alltime["prcpPROP"]["year_max"][0] = sum(clmt[y]["prcp"])
            alltime["prcpPROP"]["year_max"][1] = []
            alltime["prcpPROP"]["year_max"][1].append(y)
        if clmt[y]["recordqty"] > excludeyear:
            if clmt[y]["prcpDAYS"] == alltime["prcpPROP"]["year_min_days"][0]: alltime["prcpPROP"]["year_min_days"][1].append(y)
            elif clmt[y]["prcpDAYS"] < alltime["prcpPROP"]["year_min_days"][0]:
                alltime["prcpPROP"]["year_min_days"][0] = clmt[y]["prcpDAYS"]
                alltime["prcpPROP"]["year_min_days"][1] = []
                alltime["prcpPROP"]["year_min_days"][1].append(y)
            if sum(clmt[y]["prcp"]) == alltime["prcpPROP"]["year_min"][0]: alltime["prcpPROP"]["year_min"][1].append(y)
            elif sum(clmt[y]["prcp"]) < alltime["prcpPROP"]["year_min"][0]:
                alltime["prcpPROP"]["year_min"][0] = sum(clmt[y]["prcp"])
                alltime["prcpPROP"]["year_min"][1] = []
                alltime["prcpPROP"]["year_min"][1].append(y)
        for c in climo30yrs:
            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                climo30yrs[c]["prcp"].append(sum(clmt[y]["prcp"]))
                climo30yrs[c]["prcpPROP"]["days"] += clmt[y]["prcpDAYS"]
                climo30yrs[c]["total_days"] += clmt[y]["recordqty"]
                if clmt[y]["recordqty"] > excludeyear:
                    if clmt[y]["prcpDAYS"] == climo30yrs[c]["prcpPROP"]["year_max_days"][0]: climo30yrs[c]["prcpPROP"]["year_max_days"][1].append(y)
                    elif clmt[y]["prcpDAYS"] > climo30yrs[c]["prcpPROP"]["year_max_days"][0]:
                        climo30yrs[c]["prcpPROP"]["year_max_days"][0] = clmt[y]["prcpDAYS"]
                        climo30yrs[c]["prcpPROP"]["year_max_days"][1] = []
                        climo30yrs[c]["prcpPROP"]["year_max_days"][1].append(y)
                    if clmt[y]["prcpDAYS"] == climo30yrs[c]["prcpPROP"]["year_min_days"][0]: climo30yrs[c]["prcpPROP"]["year_min_days"][1].append(y)
                    elif clmt[y]["prcpDAYS"] < climo30yrs[c]["prcpPROP"]["year_min_days"][0]:
                        climo30yrs[c]["prcpPROP"]["year_min_days"][0] = clmt[y]["prcpDAYS"]
                        climo30yrs[c]["prcpPROP"]["year_min_days"][1] = []
                        climo30yrs[c]["prcpPROP"]["year_min_days"][1].append(y)
                    if sum(clmt[y]["prcp"]) == climo30yrs[c]["prcpPROP"]["year_max"][0]: climo30yrs[c]["prcpPROP"]["year_max"][1].append(y)
                    elif sum(clmt[y]["prcp"]) > climo30yrs[c]["prcpPROP"]["year_max"][0]:
                        climo30yrs[c]["prcpPROP"]["year_max"][0] = sum(clmt[y]["prcp"])
                        climo30yrs[c]["prcpPROP"]["year_max"][1] = []
                        climo30yrs[c]["prcpPROP"]["year_max"][1].append(y)
                    if sum(clmt[y]["prcp"]) == climo30yrs[c]["prcpPROP"]["year_min"][0]: climo30yrs[c]["prcpPROP"]["year_min"][1].append(y)
                    elif sum(clmt[y]["prcp"]) < climo30yrs[c]["prcpPROP"]["year_min"][0]:
                        climo30yrs[c]["prcpPROP"]["year_min"][0] = sum(clmt[y]["prcp"])
                        climo30yrs[c]["prcpPROP"]["year_min"][1] = []
                        climo30yrs[c]["prcpPROP"]["year_min"][1].append(y)
        # SNOW
        alltime["snow"].append(sum(clmt[y]["snow"]))
        alltime["snowPROP"]["days"] += clmt[y]["snowDAYS"]
        if clmt[y]["recordqty"] > excludeyear:
            if clmt[y]["snowDAYS"] == alltime["snowPROP"]["year_max_days"][0]: alltime["snowPROP"]["year_max_days"][1].append(y)
            elif clmt[y]["snowDAYS"] > alltime["snowPROP"]["year_max_days"][0]:
                alltime["snowPROP"]["year_max_days"][0] = clmt[y]["snowDAYS"]
                alltime["snowPROP"]["year_max_days"][1] = []
                alltime["snowPROP"]["year_max_days"][1].append(y)
            if sum(clmt[y]["snow"]) == alltime["snowPROP"]["year_max"][0]: alltime["snowPROP"]["year_max"][1].append(y)
            elif sum(clmt[y]["snow"]) > alltime["snowPROP"]["year_max"][0]:
                alltime["snowPROP"]["year_max"][0] = sum(clmt[y]["snow"])
                alltime["snowPROP"]["year_max"][1] = []
                alltime["snowPROP"]["year_max"][1].append(y)
        for c in climo30yrs:
            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                climo30yrs[c]["snow"].append(sum(clmt[y]["snow"]))
                climo30yrs[c]["snowPROP"]["days"] += clmt[y]["snowDAYS"]
                if clmt[y]["recordqty"] > excludeyear:
                    if clmt[y]["snowDAYS"] == climo30yrs[c]["snowPROP"]["year_max_days"][0]: climo30yrs[c]["snowPROP"]["year_max_days"][1].append(y)
                    elif clmt[y]["snowDAYS"] > climo30yrs[c]["snowPROP"]["year_max_days"][0]:
                        climo30yrs[c]["snowPROP"]["year_max_days"][0] = clmt[y]["snowDAYS"]
                        climo30yrs[c]["snowPROP"]["year_max_days"][1] = []
                        climo30yrs[c]["snowPROP"]["year_max_days"][1].append(y)
                    if sum(clmt[y]["snow"]) == climo30yrs[c]["snowPROP"]["year_max"][0]: climo30yrs[c]["snowPROP"]["year_max"][1].append(y)
                    elif sum(clmt[y]["snow"]) > climo30yrs[c]["snowPROP"]["year_max"][0]:
                        climo30yrs[c]["snowPROP"]["year_max"][0] = sum(clmt[y]["snow"])
                        climo30yrs[c]["snowPROP"]["year_max"][1] = []
                        climo30yrs[c]["snowPROP"]["year_max"][1].append(y)
    # 'recordqty', 'prcp', 'prcpDAYS', 'prcpPROP', 'snow', 'snowDAYS', 'snowPROP', 'tempAVGlist', 'tmax', 'tmaxPROP', 'tmin', 'tminPROP'
        # TAVG
        for x in clmt[y]["tempAVGlist"]: alltime["tempAVGlist_ind"].append(x)
        if len(clmt[y]["tempAVGlist"]) > excludeyear_tavg:
            alltime["tempAVGlist"].append(mean(clmt[y]["tempAVGlist"]))
            if mean(clmt[y]["tempAVGlist"]) == alltime["tavgPROP"]["year_max"][0]: alltime["tavgPROP"]["year_max"][1].append(y)
            elif mean(clmt[y]["tempAVGlist"]) > alltime["tavgPROP"]["year_max"][0]:
                alltime["tavgPROP"]["year_max"][0] = mean(clmt[y]["tempAVGlist"])
                alltime["tavgPROP"]["year_max"][1] = []
                alltime["tavgPROP"]["year_max"][1].append(y)
            if mean(clmt[y]["tempAVGlist"]) == alltime["tavgPROP"]["year_min"][0]: alltime["tavgPROP"]["year_min"][1].append(y)
            elif mean(clmt[y]["tempAVGlist"]) < alltime["tavgPROP"]["year_min"][0]:
                alltime["tavgPROP"]["year_min"][0] = mean(clmt[y]["tempAVGlist"])
                alltime["tavgPROP"]["year_min"][1] = []
                alltime["tavgPROP"]["year_min"][1].append(y)
        for c in climo30yrs:
            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                for x in clmt[y]["tempAVGlist"]:climo30yrs[c]["tempAVGlist_ind"].append(x)
                if len(clmt[y]["tempAVGlist"]) > excludeyear_tavg:
                    climo30yrs[c]["tempAVGlist"].append(mean(clmt[y]["tempAVGlist"]))                    
                    if mean(clmt[y]["tempAVGlist"]) == climo30yrs[c]["tavgPROP"]["year_max"][0]: climo30yrs[c]["tavgPROP"]["year_max"][1].append(y)
                    elif mean(clmt[y]["tempAVGlist"]) > climo30yrs[c]["tavgPROP"]["year_max"][0]:
                        climo30yrs[c]["tavgPROP"]["year_max"][0] = mean(clmt[y]["tempAVGlist"])
                        climo30yrs[c]["tavgPROP"]["year_max"][1] = []
                        climo30yrs[c]["tavgPROP"]["year_max"][1].append(y)
                    if mean(clmt[y]["tempAVGlist"]) == climo30yrs[c]["tavgPROP"]["year_min"][0]: climo30yrs[c]["tavgPROP"]["year_min"][1].append(y)
                    elif mean(clmt[y]["tempAVGlist"]) < climo30yrs[c]["tavgPROP"]["year_min"][0]:
                        climo30yrs[c]["tavgPROP"]["year_min"][0] = mean(clmt[y]["tempAVGlist"])
                        climo30yrs[c]["tavgPROP"]["year_min"][1] = []
                        climo30yrs[c]["tavgPROP"]["year_min"][1].append(y)
        # TMAX
        for x in clmt[y]["tmax"]: alltime["tmax"].append(x)
        if len(clmt[y]["tmax"]) > excludeyear:
            if mean(clmt[y]["tmax"]) == alltime["tmaxPROP"]["year_max"][0]: alltime["tmaxPROP"]["year_max"][1].append(y)
            elif mean(clmt[y]["tmax"]) > alltime["tmaxPROP"]["year_max"][0]:
                alltime["tmaxPROP"]["year_max"][0] = mean(clmt[y]["tmax"])
                alltime["tmaxPROP"]["year_max"][1] = []
                alltime["tmaxPROP"]["year_max"][1].append(y)
            if mean(clmt[y]["tmax"]) == alltime["tmaxPROP"]["year_min"][0]: alltime["tmaxPROP"]["year_min"][1].append(y)
            elif mean(clmt[y]["tmax"]) < alltime["tmaxPROP"]["year_min"][0]:
                alltime["tmaxPROP"]["year_min"][0] = mean(clmt[y]["tmax"])
                alltime["tmaxPROP"]["year_min"][1] = []
                alltime["tmaxPROP"]["year_min"][1].append(y)
        for c in climo30yrs:
            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                for x in clmt[y]["tmax"]: climo30yrs[c]["tmax"].append(x)
                if len(clmt[y]["tmax"]) > excludeyear:
                    if mean(clmt[y]["tmax"]) == climo30yrs[c]["tmaxPROP"]["year_max"][0]: climo30yrs[c]["tmaxPROP"]["year_max"][1].append(y)
                    elif mean(clmt[y]["tmax"]) > climo30yrs[c]["tmaxPROP"]["year_max"][0]:
                        climo30yrs[c]["tmaxPROP"]["year_max"][0] = mean(clmt[y]["tmax"])
                        climo30yrs[c]["tmaxPROP"]["year_max"][1] = []
                        climo30yrs[c]["tmaxPROP"]["year_max"][1].append(y)
                    if mean(clmt[y]["tmax"]) == climo30yrs[c]["tmaxPROP"]["year_min"][0]: climo30yrs[c]["tmaxPROP"]["year_min"][1].append(y)
                    elif mean(clmt[y]["tmax"]) < climo30yrs[c]["tmaxPROP"]["year_min"][0]:
                        climo30yrs[c]["tmaxPROP"]["year_min"][0] = mean(clmt[y]["tmax"])
                        climo30yrs[c]["tmaxPROP"]["year_min"][1] = []
                        climo30yrs[c]["tmaxPROP"]["year_min"][1].append(y)
        # TMIN
        for x in clmt[y]["tmin"]: alltime["tmin"].append(x)
        if len(clmt[y]["tmin"]) > excludeyear:
            if mean(clmt[y]["tmin"]) == alltime["tminPROP"]["year_max"][0]: alltime["tminPROP"]["year_max"][1].append(y)
            elif mean(clmt[y]["tmin"]) > alltime["tminPROP"]["year_max"][0]:
                alltime["tminPROP"]["year_max"][0] = mean(clmt[y]["tmin"])
                alltime["tminPROP"]["year_max"][1] = []
                alltime["tminPROP"]["year_max"][1].append(y)
            if mean(clmt[y]["tmin"]) == alltime["tminPROP"]["year_min"][0]: alltime["tminPROP"]["year_min"][1].append(y)
            elif mean(clmt[y]["tmin"]) < alltime["tminPROP"]["year_min"][0]:
                alltime["tminPROP"]["year_min"][0] = mean(clmt[y]["tmin"])
                alltime["tminPROP"]["year_min"][1] = []
                alltime["tminPROP"]["year_min"][1].append(y)
        for c in climo30yrs:
            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                for x in clmt[y]["tmin"]: climo30yrs[c]["tmin"].append(x)
                if len(clmt[y]["tmin"]) > excludeyear:
                    if mean(clmt[y]["tmin"]) == climo30yrs[c]["tminPROP"]["year_max"][0]: climo30yrs[c]["tminPROP"]["year_max"][1].append(y)
                    elif mean(clmt[y]["tmin"]) > climo30yrs[c]["tminPROP"]["year_max"][0]:
                        climo30yrs[c]["tminPROP"]["year_max"][0] = mean(clmt[y]["tmin"])
                        climo30yrs[c]["tminPROP"]["year_max"][1] = []
                        climo30yrs[c]["tminPROP"]["year_max"][1].append(y)
                    if mean(clmt[y]["tmin"]) == climo30yrs[c]["tminPROP"]["year_min"][0]: climo30yrs[c]["tminPROP"]["year_min"][1].append(y)
                    elif mean(clmt[y]["tmin"]) < climo30yrs[c]["tminPROP"]["year_min"][0]:
                        climo30yrs[c]["tminPROP"]["year_min"][0] = mean(clmt[y]["tmin"])
                        climo30yrs[c]["tminPROP"]["year_min"][1] = []
                        climo30yrs[c]["tminPROP"]["year_min"][1].append(y)

    # PRINT REPORT
    print("---------------------------------------------------")
    print("Climatology Report for All Years on Record")
    print("City: {}, {}".format(clmt["station"],clmt["station_name"]))
    print("{}-{}; {}-Year Incremented {}-Year Climatologies".format(min(valid_yrs),max(valid_yrs),clmt_inc_rpt,clmt_len_rpt))
    print("---------------------------------------------------")
    print("Part 1: Precipitation Stats")
    print("{:▒^9} {:▒^12}  {:▒^9}  {:▒^9}  {:▒^6} {:▒^12} {:▒^12} | {:▒^11}  {:▒^9} {:▒^6} {:▒^11} |".format("Years","PRCP","PRCP","PRCP","PRCP","PRCP","PRCP","SNOW","SNOW","SNOW","SNOW"))
    print("{:▒^9} {:▒^12}  {:▒^9}  {:▒^9}  {:▒^6} {:▒^12} {:▒^12} | {:▒^11}  {:▒^9} {:▒^6} {:▒^11} |".format("","DAYS","DAYS MAX","DAYS MIN","AVG", "MAX","MIN","DAYS","DAYS MAX","AVG", "MAX"))
    #         Y     PD       PDx    PDn      PA      PM     Pmin      SD     SDx       SA      SM
    print("{:-^9} {:-^12}  {:-^9}  {:-^9}  {:-^6} {:-^12} {:-^12} | {:-^11}  {:-^9} {:-^6} {:-^11} |".format("","","","","","","","","","",""))
    print("{:^9} {:5}:{:>5}%  {:>3}, {:^4}  {:>3}, {:^4}  {:^6.2f} {:>6.2f}, {:^4} {:>6.2f}, {:^4} | {:4}:{:>5}%  {:>3}, {:^4} {:^6.1f} {:>5.1f}, {:^4} |".format("All Time",
        alltime["prcpPROP"]["days"],
        round(100 * alltime["prcpPROP"]["days"] / alltime["total_days"],1),
        alltime["prcpPROP"]["year_max_days"][0],
        alltime["prcpPROP"]["year_max_days"][1][0] if len(alltime["prcpPROP"]["year_max_days"][1]) == 1 else len(alltime["prcpPROP"]["year_max_days"][1]),
        alltime["prcpPROP"]["year_min_days"][0],
        alltime["prcpPROP"]["year_min_days"][1][0] if len(alltime["prcpPROP"]["year_min_days"][1]) == 1 else len(alltime["prcpPROP"]["year_min_days"][1]),
        round(mean(alltime["prcp"]),2) if len(alltime["prcp"]) > 0 else "--",
        round(alltime["prcpPROP"]["year_max"][0],2),
        alltime["prcpPROP"]["year_max"][1][0] if len(alltime["prcpPROP"]["year_max"][1]) == 1 else len(alltime["prcpPROP"]["year_max"][1]),
        round(alltime["prcpPROP"]["year_min"][0],2),
        alltime["prcpPROP"]["year_min"][1][0] if len(alltime["prcpPROP"]["year_min"][1]) == 1 else len(alltime["prcpPROP"]["year_min"][1]),
        alltime["snowPROP"]["days"] if alltime["snowPROP"]["days"] > 0 else "--",
        round(100 * alltime["snowPROP"]["days"] / alltime["total_days"],1) if alltime["snowPROP"]["days"] > 0 else "--",
        alltime["snowPROP"]["year_max_days"][0],
        alltime["snowPROP"]["year_max_days"][1][0] if len(alltime["snowPROP"]["year_max_days"][1]) == 1 else len(alltime["snowPROP"]["year_max_days"][1]),
        round(mean(alltime["snow"]),1) if len(alltime["snow"]) > 0 else "--",
        round(alltime["snowPROP"]["year_max"][0],2),
        alltime["snowPROP"]["year_max"][1][0] if len(alltime["snowPROP"]["year_max"][1]) == 1 else len(alltime["snowPROP"]["year_max"][1])))
    for c in climo30yrs:
        #print(climo30yrs[c]["prcpPROP"]["days"],climo30yrs[c]["total_days"])
        #print(climo30yrs[c]["snowPROP"]["days"],climo30yrs[c]["total_days"])
        try:
            print("{:^9} {:5}:{:>5}%  {:>3}, {:^4}  {:>3}, {:^4}  {:^6.2f} {:>6.2f}, {:^4} {:>6.2f}, {:^4} | {:4}:{:>5}%  {:>3}, {:^4} {:^6.1f} {:>5.1f}, {:^4} |".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
            climo30yrs[c]["prcpPROP"]["days"],
            round(100 * climo30yrs[c]["prcpPROP"]["days"] / climo30yrs[c]["total_days"],1),
            climo30yrs[c]["prcpPROP"]["year_max_days"][0],
            climo30yrs[c]["prcpPROP"]["year_max_days"][1][0] if len(climo30yrs[c]["prcpPROP"]["year_max_days"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["year_max_days"][1]),
            climo30yrs[c]["prcpPROP"]["year_min_days"][0],
            climo30yrs[c]["prcpPROP"]["year_min_days"][1][0] if len(climo30yrs[c]["prcpPROP"]["year_min_days"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["year_min_days"][1]),
            round(mean(climo30yrs[c]["prcp"]),2),
            round(climo30yrs[c]["prcpPROP"]["year_max"][0],2),
            climo30yrs[c]["prcpPROP"]["year_max"][1][0] if len(climo30yrs[c]["prcpPROP"]["year_max"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["year_max"][1]),
            round(climo30yrs[c]["prcpPROP"]["year_min"][0],2),
            climo30yrs[c]["prcpPROP"]["year_min"][1][0] if len(climo30yrs[c]["prcpPROP"]["year_min"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["year_min"][1]),
            climo30yrs[c]["snowPROP"]["days"] if climo30yrs[c]["snowPROP"]["days"] > 0 else "--",
            round(100 * climo30yrs[c]["snowPROP"]["days"] / climo30yrs[c]["total_days"],1) if climo30yrs[c]["snowPROP"]["days"] > 0 else "--",
            climo30yrs[c]["snowPROP"]["year_max_days"][0],
            climo30yrs[c]["snowPROP"]["year_max_days"][1][0] if len(climo30yrs[c]["snowPROP"]["year_max_days"][1]) == 1 else len(climo30yrs[c]["snowPROP"]["year_max_days"][1]),
            round(mean(climo30yrs[c]["snow"]),1) if len(climo30yrs[c]["snow"]) > 0 else "--",
            round(climo30yrs[c]["snowPROP"]["year_max"][0],2),
            climo30yrs[c]["snowPROP"]["year_max"][1][0] if len(climo30yrs[c]["snowPROP"]["year_max"][1]) == 1 else len(climo30yrs[c]["snowPROP"]["year_max"][1])))
        except Exception as e:
            print("ERROR: Era = {}; Exception = {}".format(c,e))

    print("\nPart 2: Temperature Stats")
    print("{:▒^9} {:▒^37} | {:▒^37} | {:▒^37}".format("Years","AVG TEMP","TMAX","TMIN"))
    print("{:▒^9} {:▒<5} {:▒^5} {:▒^12} {:▒^12} | {:▒<5} {:▒^5} {:▒^12} {:▒^12} | {:▒<5} {:▒^5} {:▒^12} {:▒^12}".format("","STDEV","AVG","MAX","MIN","STDEV","AVG","MAX","MIN","STDEV","AVG","MAX","MIN"))
    #         Y    TSTDV   TMA     TMX    TMn      TSTDV   TMA     TMX    TMn      TSTDV   TMA     TMX    TMn    
    # "tempAVGlist": [],"tavgPROP":{"year_max":[-999,[]],"year_min":[999,[]]},
    print("{:-^9} {:-^5} {:-^5} {:-^12} {:-^12} | {:-^5} {:-^5} {:-^12} {:-^12} | {:-^5} {:-^5} {:-^12} {:-^12}".format("","","","","","","","","","","","",""))
    print("{:^9} {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5}".format("All Time",
        round(pstdev(alltime["tempAVGlist"]),1),
        round(mean(alltime["tempAVGlist_ind"]),1),
        round(alltime["tavgPROP"]["year_max"][0],1),
        alltime["tavgPROP"]["year_max"][1][0] if len(alltime["tavgPROP"]["year_max"][1]) == 1 else len(alltime["tavgPROP"]["year_max"][1]),
        round(alltime["tavgPROP"]["year_min"][0],1),
        alltime["tavgPROP"]["year_min"][1][0] if len(alltime["tavgPROP"]["year_min"][1]) == 1 else len(alltime["tavgPROP"]["year_min"][1]),
        round(pstdev(alltime["tmax"]),1),
        round(mean(alltime["tmax"]),1),
        round(alltime["tmaxPROP"]["year_max"][0],1),
        alltime["tmaxPROP"]["year_max"][1][0] if len(alltime["tmaxPROP"]["year_max"][1]) == 1 else len(alltime["tmaxPROP"]["year_max"][1]),
        round(alltime["tmaxPROP"]["year_min"][0],1),
        alltime["tmaxPROP"]["year_min"][1][0] if len(alltime["tmaxPROP"]["year_min"][1]) == 1 else len(alltime["tmaxPROP"]["year_min"][1]),
        round(pstdev(alltime["tmin"]),1),
        round(mean(alltime["tmin"]),1),
        round(alltime["tminPROP"]["year_max"][0],1),
        alltime["tminPROP"]["year_max"][1][0] if len(alltime["tminPROP"]["year_max"][1]) == 1 else len(alltime["tminPROP"]["year_max"][1]),
        round(alltime["tminPROP"]["year_min"][0],1),
        alltime["tminPROP"]["year_min"][1][0] if len(alltime["tminPROP"]["year_min"][1]) == 1 else len(alltime["tminPROP"]["year_min"][1])))
    for c in climo30yrs:
        try:
            print("{:^9} {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5}".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
                round(pstdev(climo30yrs[c]["tempAVGlist"]),1),
                round(mean(climo30yrs[c]["tempAVGlist_ind"]),1),
                round(climo30yrs[c]["tavgPROP"]["year_max"][0],1),
                climo30yrs[c]["tavgPROP"]["year_max"][1][0] if len(climo30yrs[c]["tavgPROP"]["year_max"][1]) == 1 else len(climo30yrs[c]["tavgPROP"]["year_max"][1]),
                round(climo30yrs[c]["tavgPROP"]["year_min"][0],1),
                climo30yrs[c]["tavgPROP"]["year_min"][1][0] if len(climo30yrs[c]["tavgPROP"]["year_min"][1]) == 1 else len(climo30yrs[c]["tavgPROP"]["year_min"][1]),
                round(pstdev(climo30yrs[c]["tmax"]),1),
                round(mean(climo30yrs[c]["tmax"]),1),
                round(climo30yrs[c]["tmaxPROP"]["year_max"][0],1),
                climo30yrs[c]["tmaxPROP"]["year_max"][1][0] if len(climo30yrs[c]["tmaxPROP"]["year_max"][1]) == 1 else len(climo30yrs[c]["tmaxPROP"]["year_max"][1]),
                round(climo30yrs[c]["tmaxPROP"]["year_min"][0],1),
                climo30yrs[c]["tmaxPROP"]["year_min"][1][0] if len(climo30yrs[c]["tmaxPROP"]["year_min"][1]) == 1 else len(climo30yrs[c]["tmaxPROP"]["year_min"][1]),
                round(pstdev(climo30yrs[c]["tmin"]),1),
                round(mean(climo30yrs[c]["tmin"]),1),
                round(climo30yrs[c]["tminPROP"]["year_max"][0],1),
                climo30yrs[c]["tminPROP"]["year_max"][1][0] if len(climo30yrs[c]["tminPROP"]["year_max"][1]) == 1 else len(climo30yrs[c]["tminPROP"]["year_max"][1]),
                round(climo30yrs[c]["tminPROP"]["year_min"][0],1),
                climo30yrs[c]["tminPROP"]["year_min"][1][0] if len(climo30yrs[c]["tminPROP"]["year_min"][1]) == 1 else len(climo30yrs[c]["tminPROP"]["year_min"][1])))
        except Exception as e:
            print("ERROR: Era = {}; Exception = {}".format(c,e))
    print("")
    
    if "output" in output and output["output"] == True:
        newfn = "yearReport_Jan-Dec_" + str(clmt_len_rpt) + "YRclimo_" + str(clmt_inc_rpt) + "YRincr_" + clmt["station_name"] + ".csv"
        with open(newfn,"w") as w:
            headers = ["Assessed Period (Jan 1-Dec 31)","PRCP Days","PRCP % of days","PRCP stdev","PRCP AVG","SNOW Days","SNOW % of days","SNOW stdev","SNOW AVG","TAVG stdev","TAVG","TMAX stdev","TMAX","TMIN stdev","TMIN"]
            # HEADER
            for x in range(len(headers)):
                if x != len(headers) - 1: w.write(headers[x]); w.write(",")
                else: w.write(headers[x]); w.write("\n")
            w.write("{}-{}".format(alltime["years"][0],alltime["years"][1])); w.write(",")
            w.write("{}".format(alltime["prcpPROP"]["days"])); w.write(",")
            w.write("{:.1f}".format(round(100 * alltime["prcpPROP"]["days"] / alltime["total_days"],1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["prcp"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["prcp"]),1))); w.write(",")
            w.write("{}".format(alltime["snowPROP"]["days"])); w.write(",")
            w.write("{:.1f}".format(round(100 * alltime["snowPROP"]["days"] / alltime["total_days"],1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["snow"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["snow"]),1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tempAVGlist"]),1))); w.write(",")
            w.write("{:.2f}".format(mean(alltime["tempAVGlist_ind"]))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tmax"]),1))); w.write(",")
            w.write("{:.2f}".format(mean(alltime["tmax"]))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tmin"]),1))); w.write(",")
            w.write("{:.2f}".format(mean(alltime["tmin"]))); w.write("\n")
            for x in climo30yrs:
                w.write("{}-{}".format(climo30yrs[x]["years"][0],climo30yrs[x]["years"][1])); w.write(",")
                w.write("{}".format(climo30yrs[x]["prcpPROP"]["days"])); w.write(",")
                w.write("{:.1f}".format(round(100 * climo30yrs[x]["prcpPROP"]["days"] / climo30yrs[x]["total_days"],1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["prcp"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["prcp"]),1))); w.write(",")
                w.write("{}".format(climo30yrs[x]["snowPROP"]["days"])); w.write(",")
                w.write("{:.1f}".format(round(100 * climo30yrs[x]["snowPROP"]["days"] / climo30yrs[x]["total_days"],1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["snow"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["snow"]),1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tempAVGlist"]),1))); w.write(",")
                w.write("{:.2f}".format(mean(climo30yrs[x]["tempAVGlist_ind"]))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tmax"]),1))); w.write(",")
                w.write("{:.2f}".format(mean(climo30yrs[x]["tmax"]))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tmin"]),1))); w.write(",")
                w.write("{:.2f}".format(mean(climo30yrs[x]["tmin"]))); w.write("\n")
            print("*** csv output successful ***")

def seasonReport(season,**output):
    """Detailed Climatological Report for recorded statistics from a season of
    interest. It only accepts an argument for the season of interest which
    must be in string format (accepts "spring", "summer", "fall", or "winter")
    
    seasonReport(SEASON,**{output=False})
    
    EXAMPLE: seasonReport("summer") -> Returns a climatological report for all
                                       met. summers (6,7,8) on record
    """
    if season.lower() not in ["spring","summer","fall","autumn","winter"]: return print("* OOPS! {} is not a valid season. Try again!".format(season.capitalize()))
    if season.lower() == "autumn": season = "fall"
    season = season.lower()
    
    valid_yrs = [x for x in metclmt.keys() if type(x) == int]
    valid_yrs.sort()
    climo30yrs = {}
    for x in range(1811,max(valid_yrs)+1,clmt_inc_rpt):
        if x in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]) and x+clmt_len_rpt-1 in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]+1):
            climo30yrs[(x,x+clmt_len_rpt-1)] = {"years":(x,x+clmt_len_rpt-1),"total_days":0,
                                    "prcp": [],"prcpPROP":{"days":0,"season_max_days":[-1,[]],"season_min_days":[999,[]],"season_max":[-1,[]],"season_min":[999,[]]},
                                    "snow": [],"snowPROP":{"days":0,"season_max_days":[-1,[]],"season_max":[-1,[]]},
                                    "tempAVGlist": [],"tempAVGlist_ind":[],"tavgPROP":{"season_max":[-999,[]],"season_min":[999,[]]},
                                    "tmax": [],"tmaxPROP":{"season_max":[-999,[]],"season_min":[999,[]]},
                                    "tmin": [],"tminPROP":{"season_max":[-999,[]],"season_min":[999,[]]}}

    alltime = {"years":(valid_yrs[0],valid_yrs[len(valid_yrs)-1]),"total_days":0,
               "prcp": [],"prcpPROP":{"days":0,"season_max_days":[-1,[]],"season_min_days":[999,[]],"season_max":[-1,[]],"season_min":[999,[]]},
               "snow": [],"snowPROP":{"days":0,"season_max_days":[-1,[]],"season_max":[-1,[]]},
               "tempAVGlist": [],"tempAVGlist_ind":[],"tavgPROP":{"season_max":[-999,[]],"season_min":[999,[]]},
               "tmax": [],"tmaxPROP":{"season_max":[-999,[]],"season_min":[999,[]]},
               "tmin": [],"tminPROP":{"season_max":[-999,[]],"season_min":[999,[]]}}

    print("*** PLEASE WAIT. This will take a few moments ***")

    for y in valid_yrs:
        # 'recordqty', 'prcp', 'prcpDAYS', 'prcpPROP', 'snow', 'snowDAYS', 'snowPROP', 'tempAVGlist', 'tmax', 'tmaxPROP', 'tmin', 'tminPROP'
        alltime["total_days"] += metclmt[y][season]["recordqty"]
        # PRCP
        alltime["prcp"].append(sum(metclmt[y][season]["prcp"]))
        alltime["prcpPROP"]["days"] += metclmt[y][season]["prcpDAYS"]
        if metclmt[y][season]["prcpDAYS"] == alltime["prcpPROP"]["season_max_days"][0]: alltime["prcpPROP"]["season_max_days"][1].append(y)
        elif metclmt[y][season]["prcpDAYS"] > alltime["prcpPROP"]["season_max_days"][0]:
            alltime["prcpPROP"]["season_max_days"][0] = metclmt[y][season]["prcpDAYS"]
            alltime["prcpPROP"]["season_max_days"][1] = []
            alltime["prcpPROP"]["season_max_days"][1].append(y)
        if sum(metclmt[y][season]["prcp"]) == alltime["prcpPROP"]["season_max"][0]: alltime["prcpPROP"]["season_max"][1].append(y)
        elif sum(metclmt[y][season]["prcp"]) > alltime["prcpPROP"]["season_max"][0]:
            alltime["prcpPROP"]["season_max"][0] = sum(metclmt[y][season]["prcp"])
            alltime["prcpPROP"]["season_max"][1] = []
            alltime["prcpPROP"]["season_max"][1].append(y)
        if metclmt[y][season]["recordqty"] > excludeseason:
            if metclmt[y][season]["prcpDAYS"] == alltime["prcpPROP"]["season_min_days"][0]: alltime["prcpPROP"]["season_min_days"][1].append(y)
            elif metclmt[y][season]["prcpDAYS"] < alltime["prcpPROP"]["season_min_days"][0]:
                alltime["prcpPROP"]["season_min_days"][0] = metclmt[y][season]["prcpDAYS"]
                alltime["prcpPROP"]["season_min_days"][1] = []
                alltime["prcpPROP"]["season_min_days"][1].append(y)
            if sum(metclmt[y][season]["prcp"]) == alltime["prcpPROP"]["season_min"][0]: alltime["prcpPROP"]["season_min"][1].append(y)
            elif sum(metclmt[y][season]["prcp"]) < alltime["prcpPROP"]["season_min"][0]:
                alltime["prcpPROP"]["season_min"][0] = sum(metclmt[y][season]["prcp"])
                alltime["prcpPROP"]["season_min"][1] = []
                alltime["prcpPROP"]["season_min"][1].append(y)
        for c in climo30yrs:
            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in metclmt  if type(YR) == int) and c[1] <= max(YR for YR in metclmt  if type(YR) == int):
                climo30yrs[c]["prcp"].append(sum(metclmt[y][season]["prcp"]))
                climo30yrs[c]["prcpPROP"]["days"] += metclmt[y][season]["prcpDAYS"]
                climo30yrs[c]["total_days"] += metclmt[y][season]["recordqty"]
                if metclmt[y][season]["recordqty"] > excludeseason:
                    if metclmt[y][season]["prcpDAYS"] == climo30yrs[c]["prcpPROP"]["season_max_days"][0]: climo30yrs[c]["prcpPROP"]["season_max_days"][1].append(y)
                    elif metclmt[y][season]["prcpDAYS"] > climo30yrs[c]["prcpPROP"]["season_max_days"][0]:
                        climo30yrs[c]["prcpPROP"]["season_max_days"][0] = metclmt[y][season]["prcpDAYS"]
                        climo30yrs[c]["prcpPROP"]["season_max_days"][1] = []
                        climo30yrs[c]["prcpPROP"]["season_max_days"][1].append(y)
                    if metclmt[y][season]["prcpDAYS"] == climo30yrs[c]["prcpPROP"]["season_min_days"][0]: climo30yrs[c]["prcpPROP"]["season_min_days"][1].append(y)
                    elif metclmt[y][season]["prcpDAYS"] < climo30yrs[c]["prcpPROP"]["season_min_days"][0]:
                        climo30yrs[c]["prcpPROP"]["season_min_days"][0] = metclmt[y][season]["prcpDAYS"]
                        climo30yrs[c]["prcpPROP"]["season_min_days"][1] = []
                        climo30yrs[c]["prcpPROP"]["season_min_days"][1].append(y)
                    if sum(metclmt[y][season]["prcp"]) == climo30yrs[c]["prcpPROP"]["season_max"][0]: climo30yrs[c]["prcpPROP"]["season_max"][1].append(y)
                    elif sum(metclmt[y][season]["prcp"]) > climo30yrs[c]["prcpPROP"]["season_max"][0]:
                        climo30yrs[c]["prcpPROP"]["season_max"][0] = sum(metclmt[y][season]["prcp"])
                        climo30yrs[c]["prcpPROP"]["season_max"][1] = []
                        climo30yrs[c]["prcpPROP"]["season_max"][1].append(y)
                    if sum(metclmt[y][season]["prcp"]) == climo30yrs[c]["prcpPROP"]["season_min"][0]: climo30yrs[c]["prcpPROP"]["season_min"][1].append(y)
                    elif sum(metclmt[y][season]["prcp"]) < climo30yrs[c]["prcpPROP"]["season_min"][0]:
                        climo30yrs[c]["prcpPROP"]["season_min"][0] = sum(metclmt[y][season]["prcp"])
                        climo30yrs[c]["prcpPROP"]["season_min"][1] = []
                        climo30yrs[c]["prcpPROP"]["season_min"][1].append(y)
        # SNOW
        alltime["snow"].append(sum(metclmt[y][season]["snow"]))
        alltime["snowPROP"]["days"] += metclmt[y][season]["snowDAYS"]
        if metclmt[y][season]["recordqty"] > excludeseason:
            if metclmt[y][season]["snowDAYS"] == alltime["snowPROP"]["season_max_days"][0]: alltime["snowPROP"]["season_max_days"][1].append(y)
            elif metclmt[y][season]["snowDAYS"] > alltime["snowPROP"]["season_max_days"][0]:
                alltime["snowPROP"]["season_max_days"][0] = metclmt[y][season]["snowDAYS"]
                alltime["snowPROP"]["season_max_days"][1] = []
                alltime["snowPROP"]["season_max_days"][1].append(y)
            if sum(metclmt[y][season]["snow"]) == alltime["snowPROP"]["season_max"][0]: alltime["snowPROP"]["season_max"][1].append(y)
            elif sum(metclmt[y][season]["snow"]) > alltime["snowPROP"]["season_max"][0]:
                alltime["snowPROP"]["season_max"][0] = sum(metclmt[y][season]["snow"])
                alltime["snowPROP"]["season_max"][1] = []
                alltime["snowPROP"]["season_max"][1].append(y)
        for c in climo30yrs:
            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in metclmt  if type(YR) == int) and c[1] <= max(YR for YR in metclmt  if type(YR) == int):
                climo30yrs[c]["snow"].append(sum(metclmt[y][season]["snow"]))
                climo30yrs[c]["snowPROP"]["days"] += metclmt[y][season]["snowDAYS"]
                if metclmt[y][season]["recordqty"] > excludeseason:
                    if metclmt[y][season]["snowDAYS"] == climo30yrs[c]["snowPROP"]["season_max_days"][0]: climo30yrs[c]["snowPROP"]["season_max_days"][1].append(y)
                    elif metclmt[y][season]["snowDAYS"] > climo30yrs[c]["snowPROP"]["season_max_days"][0]:
                        climo30yrs[c]["snowPROP"]["season_max_days"][0] = metclmt[y][season]["snowDAYS"]
                        climo30yrs[c]["snowPROP"]["season_max_days"][1] = []
                        climo30yrs[c]["snowPROP"]["season_max_days"][1].append(y)
                    if sum(metclmt[y][season]["snow"]) == climo30yrs[c]["snowPROP"]["season_max"][0]: climo30yrs[c]["snowPROP"]["season_max"][1].append(y)
                    elif sum(metclmt[y][season]["snow"]) > climo30yrs[c]["snowPROP"]["season_max"][0]:
                        climo30yrs[c]["snowPROP"]["season_max"][0] = sum(metclmt[y][season]["snow"])
                        climo30yrs[c]["snowPROP"]["season_max"][1] = []
                        climo30yrs[c]["snowPROP"]["season_max"][1].append(y)
    # 'recordqty', 'prcp', 'prcpDAYS', 'prcpPROP', 'snow', 'snowDAYS', 'snowPROP', 'tempAVGlist', 'tmax', 'tmaxPROP', 'tmin', 'tminPROP'
        # TAVG
        for x in metclmt[y][season]["tempAVGlist"]: alltime["tempAVGlist_ind"].append(x)
        if len(metclmt[y][season]["tempAVGlist"]) > excludeseason_tavg:
            alltime["tempAVGlist"].append(mean(metclmt[y][season]["tempAVGlist"]))
            if mean(metclmt[y][season]["tempAVGlist"]) == alltime["tavgPROP"]["season_max"][0]: alltime["tavgPROP"]["season_max"][1].append(y)
            elif mean(metclmt[y][season]["tempAVGlist"]) > alltime["tavgPROP"]["season_max"][0]:
                alltime["tavgPROP"]["season_max"][0] = mean(metclmt[y][season]["tempAVGlist"])
                alltime["tavgPROP"]["season_max"][1] = []
                alltime["tavgPROP"]["season_max"][1].append(y)
            if mean(metclmt[y][season]["tempAVGlist"]) == alltime["tavgPROP"]["season_min"][0]: alltime["tavgPROP"]["season_min"][1].append(y)
            elif mean(metclmt[y][season]["tempAVGlist"]) < alltime["tavgPROP"]["season_min"][0]:
                alltime["tavgPROP"]["season_min"][0] = mean(metclmt[y][season]["tempAVGlist"])
                alltime["tavgPROP"]["season_min"][1] = []
                alltime["tavgPROP"]["season_min"][1].append(y)
        for c in climo30yrs:
            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in metclmt  if type(YR) == int) and c[1] <= max(YR for YR in metclmt  if type(YR) == int):
                for x in metclmt[y][season]["tempAVGlist"]:climo30yrs[c]["tempAVGlist_ind"].append(x)
                if len(metclmt[y][season]["tempAVGlist"]) > excludeseason_tavg:
                    climo30yrs[c]["tempAVGlist"].append(mean(metclmt[y][season]["tempAVGlist"]))                    
                    if mean(metclmt[y][season]["tempAVGlist"]) == climo30yrs[c]["tavgPROP"]["season_max"][0]: climo30yrs[c]["tavgPROP"]["season_max"][1].append(y)
                    elif mean(metclmt[y][season]["tempAVGlist"]) > climo30yrs[c]["tavgPROP"]["season_max"][0]:
                        climo30yrs[c]["tavgPROP"]["season_max"][0] = mean(metclmt[y][season]["tempAVGlist"])
                        climo30yrs[c]["tavgPROP"]["season_max"][1] = []
                        climo30yrs[c]["tavgPROP"]["season_max"][1].append(y)
                    if mean(metclmt[y][season]["tempAVGlist"]) == climo30yrs[c]["tavgPROP"]["season_min"][0]: climo30yrs[c]["tavgPROP"]["season_min"][1].append(y)
                    elif mean(metclmt[y][season]["tempAVGlist"]) < climo30yrs[c]["tavgPROP"]["season_min"][0]:
                        climo30yrs[c]["tavgPROP"]["season_min"][0] = mean(metclmt[y][season]["tempAVGlist"])
                        climo30yrs[c]["tavgPROP"]["season_min"][1] = []
                        climo30yrs[c]["tavgPROP"]["season_min"][1].append(y)
        # TMAX
        for x in metclmt[y][season]["tmax"]: alltime["tmax"].append(x)
        if len(metclmt[y][season]["tmax"]) > excludeseason:
            if mean(metclmt[y][season]["tmax"]) == alltime["tmaxPROP"]["season_max"][0]: alltime["tmaxPROP"]["season_max"][1].append(y)
            elif mean(metclmt[y][season]["tmax"]) > alltime["tmaxPROP"]["season_max"][0]:
                alltime["tmaxPROP"]["season_max"][0] = mean(metclmt[y][season]["tmax"])
                alltime["tmaxPROP"]["season_max"][1] = []
                alltime["tmaxPROP"]["season_max"][1].append(y)
            if mean(metclmt[y][season]["tmax"]) == alltime["tmaxPROP"]["season_min"][0]: alltime["tmaxPROP"]["season_min"][1].append(y)
            elif mean(metclmt[y][season]["tmax"]) < alltime["tmaxPROP"]["season_min"][0]:
                alltime["tmaxPROP"]["season_min"][0] = mean(metclmt[y][season]["tmax"])
                alltime["tmaxPROP"]["season_min"][1] = []
                alltime["tmaxPROP"]["season_min"][1].append(y)
        for c in climo30yrs:
            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in metclmt  if type(YR) == int) and c[1] <= max(YR for YR in metclmt  if type(YR) == int):
                for x in metclmt[y][season]["tmax"]: climo30yrs[c]["tmax"].append(x)
                if len(metclmt[y][season]["tmax"]) > excludeseason:
                    if mean(metclmt[y][season]["tmax"]) == climo30yrs[c]["tmaxPROP"]["season_max"][0]: climo30yrs[c]["tmaxPROP"]["season_max"][1].append(y)
                    elif mean(metclmt[y][season]["tmax"]) > climo30yrs[c]["tmaxPROP"]["season_max"][0]:
                        climo30yrs[c]["tmaxPROP"]["season_max"][0] = mean(metclmt[y][season]["tmax"])
                        climo30yrs[c]["tmaxPROP"]["season_max"][1] = []
                        climo30yrs[c]["tmaxPROP"]["season_max"][1].append(y)
                    if mean(metclmt[y][season]["tmax"]) == climo30yrs[c]["tmaxPROP"]["season_min"][0]: climo30yrs[c]["tmaxPROP"]["season_min"][1].append(y)
                    elif mean(metclmt[y][season]["tmax"]) < climo30yrs[c]["tmaxPROP"]["season_min"][0]:
                        climo30yrs[c]["tmaxPROP"]["season_min"][0] = mean(metclmt[y][season]["tmax"])
                        climo30yrs[c]["tmaxPROP"]["season_min"][1] = []
                        climo30yrs[c]["tmaxPROP"]["season_min"][1].append(y)
        # TMIN
        for x in metclmt[y][season]["tmin"]: alltime["tmin"].append(x)
        if len(metclmt[y][season]["tmin"]) > excludeseason:
            if mean(metclmt[y][season]["tmin"]) == alltime["tminPROP"]["season_max"][0]: alltime["tminPROP"]["season_max"][1].append(y)
            elif mean(metclmt[y][season]["tmin"]) > alltime["tminPROP"]["season_max"][0]:
                alltime["tminPROP"]["season_max"][0] = mean(metclmt[y][season]["tmin"])
                alltime["tminPROP"]["season_max"][1] = []
                alltime["tminPROP"]["season_max"][1].append(y)
            if mean(metclmt[y][season]["tmin"]) == alltime["tminPROP"]["season_min"][0]: alltime["tminPROP"]["season_min"][1].append(y)
            elif mean(metclmt[y][season]["tmin"]) < alltime["tminPROP"]["season_min"][0]:
                alltime["tminPROP"]["season_min"][0] = mean(metclmt[y][season]["tmin"])
                alltime["tminPROP"]["season_min"][1] = []
                alltime["tminPROP"]["season_min"][1].append(y)
        for c in climo30yrs:
            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in metclmt  if type(YR) == int) and c[1] <= max(YR for YR in metclmt  if type(YR) == int):
                for x in metclmt[y][season]["tmin"]: climo30yrs[c]["tmin"].append(x)
                if len(metclmt[y][season]["tmin"]) > excludeseason:
                    if mean(metclmt[y][season]["tmin"]) == climo30yrs[c]["tminPROP"]["season_max"][0]: climo30yrs[c]["tminPROP"]["season_max"][1].append(y)
                    elif mean(metclmt[y][season]["tmin"]) > climo30yrs[c]["tminPROP"]["season_max"][0]:
                        climo30yrs[c]["tminPROP"]["season_max"][0] = mean(metclmt[y][season]["tmin"])
                        climo30yrs[c]["tminPROP"]["season_max"][1] = []
                        climo30yrs[c]["tminPROP"]["season_max"][1].append(y)
                    if mean(metclmt[y][season]["tmin"]) == climo30yrs[c]["tminPROP"]["season_min"][0]: climo30yrs[c]["tminPROP"]["season_min"][1].append(y)
                    elif mean(metclmt[y][season]["tmin"]) < climo30yrs[c]["tminPROP"]["season_min"][0]:
                        climo30yrs[c]["tminPROP"]["season_min"][0] = mean(metclmt[y][season]["tmin"])
                        climo30yrs[c]["tminPROP"]["season_min"][1] = []
                        climo30yrs[c]["tminPROP"]["season_min"][1].append(y)

    # PRINT REPORT
    print("---------------------------------------------------")
    print("Climatology Report for Meteorological {}".format(season.capitalize()))
    print("City: {}, {}".format(metclmt["station"],metclmt["station_name"]))
    print("{}-{}; {}-Year Incremented {}-Year Climatologies".format(min(valid_yrs),max(valid_yrs),clmt_inc_rpt,clmt_len_rpt))
    print("---------------------------------------------------")
    print("Part 1: Precipitation Stats")
    print("{:▒^9} {:▒^12}  {:▒^9}  {:▒^9}  {:▒^6} {:▒^12} {:▒^12} | {:▒^11}  {:▒^9} {:▒^6} {:▒^11} |".format("Years","PRCP","PRCP","PRCP","PRCP","PRCP","PRCP","SNOW","SNOW","SNOW","SNOW"))
    print("{:▒^9} {:▒^12}  {:▒^9}  {:▒^9}  {:▒^6} {:▒^12} {:▒^12} | {:▒^11}  {:▒^9} {:▒^6} {:▒^11} |".format("","DAYS","DAYS MAX","DAYS MIN","AVG", "MAX","MIN","DAYS","DAYS MAX","AVG", "MAX"))
    #         Y     PD       PDx    PDn      PA      PM     Pmin      SD     SDx       SA      SM
    print("{:-^9} {:-^12}  {:-^9}  {:-^9}  {:-^6} {:-^12} {:-^12} | {:-^11}  {:-^9} {:-^6} {:-^11} |".format("","","","","","","","","","",""))
    print("{:^9} {:5}:{:>5}%  {:>3}, {:^4}  {:>3}, {:^4}  {:^6.2f} {:>6.2f}, {:^4} {:>6.2f}, {:^4} | {:4}:{:>5}%  {:>3}, {:^4} {:^6.1f} {:>5.1f}, {:^4} |".format("All Time",
        alltime["prcpPROP"]["days"],
        round(100 * alltime["prcpPROP"]["days"] / alltime["total_days"],1),
        alltime["prcpPROP"]["season_max_days"][0],
        alltime["prcpPROP"]["season_max_days"][1][0] if len(alltime["prcpPROP"]["season_max_days"][1]) == 1 else len(alltime["prcpPROP"]["season_max_days"][1]),
        alltime["prcpPROP"]["season_min_days"][0],
        alltime["prcpPROP"]["season_min_days"][1][0] if len(alltime["prcpPROP"]["season_min_days"][1]) == 1 else len(alltime["prcpPROP"]["season_min_days"][1]),
        round(mean(alltime["prcp"]),2) if len(alltime["prcp"]) > 0 else "--",
        round(alltime["prcpPROP"]["season_max"][0],2),
        alltime["prcpPROP"]["season_max"][1][0] if len(alltime["prcpPROP"]["season_max"][1]) == 1 else len(alltime["prcpPROP"]["season_max"][1]),
        round(alltime["prcpPROP"]["season_min"][0],2),
        alltime["prcpPROP"]["season_min"][1][0] if len(alltime["prcpPROP"]["season_min"][1]) == 1 else len(alltime["prcpPROP"]["season_min"][1]),
        alltime["snowPROP"]["days"] if alltime["snowPROP"]["days"] > 0 else "--",
        round(100 * alltime["snowPROP"]["days"] / alltime["total_days"],1) if alltime["snowPROP"]["days"] > 0 else "--",
        alltime["snowPROP"]["season_max_days"][0],
        alltime["snowPROP"]["season_max_days"][1][0] if len(alltime["snowPROP"]["season_max_days"][1]) == 1 else len(alltime["snowPROP"]["season_max_days"][1]),
        round(mean(alltime["snow"]),1) if len(alltime["snow"]) > 0 else "--",
        round(alltime["snowPROP"]["season_max"][0],2),
        alltime["snowPROP"]["season_max"][1][0] if len(alltime["snowPROP"]["season_max"][1]) == 1 else len(alltime["snowPROP"]["season_max"][1])))
    for c in climo30yrs:
        #print(climo30yrs[c]["prcpPROP"]["days"],climo30yrs[c]["total_days"])
        #print(climo30yrs[c]["snowPROP"]["days"],climo30yrs[c]["total_days"])
        try:
            print("{:^9} {:5}:{:>5}%  {:>3}, {:^4}  {:>3}, {:^4}  {:^6.2f} {:>6.2f}, {:^4} {:>6.2f}, {:^4} | {:4}:{:>5}%  {:>3}, {:^4} {:^6.1f} {:>5.1f}, {:^4} |".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
            climo30yrs[c]["prcpPROP"]["days"],
            round(100 * climo30yrs[c]["prcpPROP"]["days"] / climo30yrs[c]["total_days"],1),
            climo30yrs[c]["prcpPROP"]["season_max_days"][0],
            climo30yrs[c]["prcpPROP"]["season_max_days"][1][0] if len(climo30yrs[c]["prcpPROP"]["season_max_days"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["season_max_days"][1]),
            climo30yrs[c]["prcpPROP"]["season_min_days"][0],
            climo30yrs[c]["prcpPROP"]["season_min_days"][1][0] if len(climo30yrs[c]["prcpPROP"]["season_min_days"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["season_min_days"][1]),
            round(mean(climo30yrs[c]["prcp"]),2),
            round(climo30yrs[c]["prcpPROP"]["season_max"][0],2),
            climo30yrs[c]["prcpPROP"]["season_max"][1][0] if len(climo30yrs[c]["prcpPROP"]["season_max"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["season_max"][1]),
            round(climo30yrs[c]["prcpPROP"]["season_min"][0],2),
            climo30yrs[c]["prcpPROP"]["season_min"][1][0] if len(climo30yrs[c]["prcpPROP"]["season_min"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["season_min"][1]),
            climo30yrs[c]["snowPROP"]["days"] if climo30yrs[c]["snowPROP"]["days"] > 0 else "--",
            round(100 * climo30yrs[c]["snowPROP"]["days"] / climo30yrs[c]["total_days"],1) if climo30yrs[c]["snowPROP"]["days"] > 0 else "--",
            climo30yrs[c]["snowPROP"]["season_max_days"][0],
            climo30yrs[c]["snowPROP"]["season_max_days"][1][0] if len(climo30yrs[c]["snowPROP"]["season_max_days"][1]) == 1 else len(climo30yrs[c]["snowPROP"]["season_max_days"][1]),
            round(mean(climo30yrs[c]["snow"]),1) if len(climo30yrs[c]["snow"]) > 0 else "--",
            round(climo30yrs[c]["snowPROP"]["season_max"][0],2),
            climo30yrs[c]["snowPROP"]["season_max"][1][0] if len(climo30yrs[c]["snowPROP"]["season_max"][1]) == 1 else len(climo30yrs[c]["snowPROP"]["season_max"][1])))
        except Exception as e:
            print("ERROR: Era = {}; Exception = {}".format(c,e))

    print("\nPart 2: Temperature Stats")
    print("{:▒^9} {:▒^37} | {:▒^37} | {:▒^37}".format("Years","AVG TEMP","TMAX","TMIN"))
    print("{:▒^9} {:▒<5} {:▒^5} {:▒^12} {:▒^12} | {:▒<5} {:▒^5} {:▒^12} {:▒^12} | {:▒<5} {:▒^5} {:▒^12} {:▒^12}".format("","STDEV","AVG","MAX","MIN","STDEV","AVG","MAX","MIN","STDEV","AVG","MAX","MIN"))
    #         Y    TSTDV   TMA     TMX    TMn      TSTDV   TMA     TMX    TMn      TSTDV   TMA     TMX    TMn    
    # "tempAVGlist": [],"tavgPROP":{"season_max":[-999,[]],"season_min":[999,[]]},
    print("{:-^9} {:-^5} {:-^5} {:-^12} {:-^12} | {:-^5} {:-^5} {:-^12} {:-^12} | {:-^5} {:-^5} {:-^12} {:-^12}".format("","","","","","","","","","","","",""))
    print("{:^9} {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5}".format("All Time",
        round(pstdev(alltime["tempAVGlist"]),1),
        round(mean(alltime["tempAVGlist_ind"]),1),
        round(alltime["tavgPROP"]["season_max"][0],1),
        alltime["tavgPROP"]["season_max"][1][0] if len(alltime["tavgPROP"]["season_max"][1]) == 1 else len(alltime["tavgPROP"]["season_max"][1]),
        round(alltime["tavgPROP"]["season_min"][0],1),
        alltime["tavgPROP"]["season_min"][1][0] if len(alltime["tavgPROP"]["season_min"][1]) == 1 else len(alltime["tavgPROP"]["season_min"][1]),
        round(pstdev(alltime["tmax"]),1),
        round(mean(alltime["tmax"]),1),
        round(alltime["tmaxPROP"]["season_max"][0],1),
        alltime["tmaxPROP"]["season_max"][1][0] if len(alltime["tmaxPROP"]["season_max"][1]) == 1 else len(alltime["tmaxPROP"]["season_max"][1]),
        round(alltime["tmaxPROP"]["season_min"][0],1),
        alltime["tmaxPROP"]["season_min"][1][0] if len(alltime["tmaxPROP"]["season_min"][1]) == 1 else len(alltime["tmaxPROP"]["season_min"][1]),
        round(pstdev(alltime["tmin"]),1),
        round(mean(alltime["tmin"]),1),
        round(alltime["tminPROP"]["season_max"][0],1),
        alltime["tminPROP"]["season_max"][1][0] if len(alltime["tminPROP"]["season_max"][1]) == 1 else len(alltime["tminPROP"]["season_max"][1]),
        round(alltime["tminPROP"]["season_min"][0],1),
        alltime["tminPROP"]["season_min"][1][0] if len(alltime["tminPROP"]["season_min"][1]) == 1 else len(alltime["tminPROP"]["season_min"][1])))
    for c in climo30yrs:
        try:
            print("{:^9} {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5}".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
                round(pstdev(climo30yrs[c]["tempAVGlist"]),1),
                round(mean(climo30yrs[c]["tempAVGlist_ind"]),1),
                round(climo30yrs[c]["tavgPROP"]["season_max"][0],1),
                climo30yrs[c]["tavgPROP"]["season_max"][1][0] if len(climo30yrs[c]["tavgPROP"]["season_max"][1]) == 1 else len(climo30yrs[c]["tavgPROP"]["season_max"][1]),
                round(climo30yrs[c]["tavgPROP"]["season_min"][0],1),
                climo30yrs[c]["tavgPROP"]["season_min"][1][0] if len(climo30yrs[c]["tavgPROP"]["season_min"][1]) == 1 else len(climo30yrs[c]["tavgPROP"]["season_min"][1]),
                round(pstdev(climo30yrs[c]["tmax"]),1),
                round(mean(climo30yrs[c]["tmax"]),1),
                round(climo30yrs[c]["tmaxPROP"]["season_max"][0],1),
                climo30yrs[c]["tmaxPROP"]["season_max"][1][0] if len(climo30yrs[c]["tmaxPROP"]["season_max"][1]) == 1 else len(climo30yrs[c]["tmaxPROP"]["season_max"][1]),
                round(climo30yrs[c]["tmaxPROP"]["season_min"][0],1),
                climo30yrs[c]["tmaxPROP"]["season_min"][1][0] if len(climo30yrs[c]["tmaxPROP"]["season_min"][1]) == 1 else len(climo30yrs[c]["tmaxPROP"]["season_min"][1]),
                round(pstdev(climo30yrs[c]["tmin"]),1),
                round(mean(climo30yrs[c]["tmin"]),1),
                round(climo30yrs[c]["tminPROP"]["season_max"][0],1),
                climo30yrs[c]["tminPROP"]["season_max"][1][0] if len(climo30yrs[c]["tminPROP"]["season_max"][1]) == 1 else len(climo30yrs[c]["tminPROP"]["season_max"][1]),
                round(climo30yrs[c]["tminPROP"]["season_min"][0],1),
                climo30yrs[c]["tminPROP"]["season_min"][1][0] if len(climo30yrs[c]["tminPROP"]["season_min"][1]) == 1 else len(climo30yrs[c]["tminPROP"]["season_min"][1])))
        except Exception as e:
            print("ERROR: Era = {}; Exception = {}".format(c,e))
    print("")

    if "output" in output and output["output"] == True:
        newfn = "seasonReport_met" + season.lower().capitalize() + "_" + str(clmt_len_rpt) + "YRclimo_" + str(clmt_inc_rpt) + "YRincr_" + clmt["station_name"] + ".csv"
        with open(newfn,"w") as w:
            headers = ["Assessed Period (Meteorological {})".format(season.lower().capitalize()),"PRCP Days","PRCP % of days","PRCP stdev","PRCP AVG","SNOW Days","SNOW % of days","SNOW stdev","SNOW AVG","TAVG stdev","TAVG","TMAX stdev","TMAX","TMIN stdev","TMIN"]
            # HEADER
            for x in range(len(headers)):
                if x != len(headers) - 1: w.write(headers[x]); w.write(",")
                else: w.write(headers[x]); w.write("\n")
            w.write("{}-{}".format(alltime["years"][0],alltime["years"][1])); w.write(",")
            w.write("{}".format(alltime["prcpPROP"]["days"])); w.write(",")
            w.write("{:.1f}".format(round(100 * alltime["prcpPROP"]["days"] / alltime["total_days"],1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["prcp"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["prcp"]),1))); w.write(",")
            w.write("{}".format(alltime["snowPROP"]["days"])); w.write(",")
            w.write("{:.1f}".format(round(100 * alltime["snowPROP"]["days"] / alltime["total_days"],1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["snow"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["snow"]),1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tempAVGlist"]),1))); w.write(",")
            w.write("{:.2f}".format(mean(alltime["tempAVGlist_ind"]))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tmax"]),1))); w.write(",")
            w.write("{:.2f}".format(mean(alltime["tmax"]))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tmin"]),1))); w.write(",")
            w.write("{:.2f}".format(mean(alltime["tmin"]))); w.write("\n")
            for x in climo30yrs:
                w.write("{}-{}".format(climo30yrs[x]["years"][0],climo30yrs[x]["years"][1])); w.write(",")
                w.write("{}".format(climo30yrs[x]["prcpPROP"]["days"])); w.write(",")
                w.write("{:.1f}".format(round(100 * climo30yrs[x]["prcpPROP"]["days"] / climo30yrs[x]["total_days"],1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["prcp"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["prcp"]),1))); w.write(",")
                w.write("{}".format(climo30yrs[x]["snowPROP"]["days"])); w.write(",")
                w.write("{:.1f}".format(round(100 * climo30yrs[x]["snowPROP"]["days"] / climo30yrs[x]["total_days"],1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["snow"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["snow"]),1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tempAVGlist"]),1))); w.write(",")
                w.write("{:.2f}".format(mean(climo30yrs[x]["tempAVGlist_ind"]))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tmax"]),1))); w.write(",")
                w.write("{:.2f}".format(mean(climo30yrs[x]["tmax"]))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tmin"]),1))); w.write(",")
                w.write("{:.2f}".format(mean(climo30yrs[x]["tmin"]))); w.write("\n")
            print("*** csv output successful ***")

def metYearReport(**output):
    """Detailed Climatological Report for recorded statistics from a
    meteorlogical year (March to February) of interest. No arguments are
    needed to be passed.
    
    metYearReport(**{output=False})
    
    EXAMPLE: metYearReport() -> Returns a climatological report for all
                                meteorological years on record.
    """
    valid_yrs = [x for x in metclmt.keys() if type(x) == int]
    valid_yrs.sort()
    climo30yrs = {}
    for x in range(1811,max(valid_yrs)+1,clmt_inc_rpt):
        if x in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]) and x+clmt_len_rpt-1 in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]+1):
            climo30yrs[(x,x+clmt_len_rpt-1)] = {"years":(x,x+clmt_len_rpt-1),"total_days":0,
                                    "prcp": [],"prcpPROP":{"days":0,"year_max_days":[-1,[]],"year_min_days":[999,[]],"year_max":[-1,[]],"year_min":[999,[]]},
                                    "snow": [],"snowPROP":{"days":0,"year_max_days":[-1,[]],"year_max":[-1,[]]},
                                    "tempAVGlist": [],"tempAVGlist_ind":[],"tavgPROP":{"year_max":[-999,[]],"year_min":[999,[]]},
                                    "tmax": [],"tmaxPROP":{"year_max":[-999,[]],"year_min":[999,[]]},
                                    "tmin": [],"tminPROP":{"year_max":[-999,[]],"year_min":[999,[]]}}

    alltime = {"years":(valid_yrs[0],valid_yrs[len(valid_yrs)-1]),"total_days":0,
               "prcp": [],"prcpPROP":{"days":0,"year_max_days":[-1,[]],"year_min_days":[999,[]],"year_max":[-1,[]],"year_min":[999,[]]},
               "snow": [],"snowPROP":{"days":0,"year_max_days":[-1,[]],"year_max":[-1,[]]},
               "tempAVGlist": [],"tempAVGlist_ind":[],"tavgPROP":{"year_max":[-999,[]],"year_min":[999,[]]},
               "tmax": [],"tmaxPROP":{"year_max":[-999,[]],"year_min":[999,[]]},
               "tmin": [],"tminPROP":{"year_max":[-999,[]],"year_min":[999,[]]}}

    print("*** PLEASE WAIT. This will take a few moments ***")

    for y in valid_yrs:
        # 'recordqty', 'prcp', 'prcpDAYS', 'prcpPROP', 'snow', 'snowDAYS', 'snowPROP', 'tempAVGlist', 'tmax', 'tmaxPROP', 'tmin', 'tminPROP'
        alltime["total_days"] += metclmt[y]["recordqty"]
        # PRCP
        alltime["prcp"].append(sum(metclmt[y]["prcp"]))
        alltime["prcpPROP"]["days"] += metclmt[y]["prcpDAYS"]
        if metclmt[y]["prcpDAYS"] == alltime["prcpPROP"]["year_max_days"][0]: alltime["prcpPROP"]["year_max_days"][1].append(y)
        elif metclmt[y]["prcpDAYS"] > alltime["prcpPROP"]["year_max_days"][0]:
            alltime["prcpPROP"]["year_max_days"][0] = metclmt[y]["prcpDAYS"]
            alltime["prcpPROP"]["year_max_days"][1] = []
            alltime["prcpPROP"]["year_max_days"][1].append(y)
        if sum(metclmt[y]["prcp"]) == alltime["prcpPROP"]["year_max"][0]: alltime["prcpPROP"]["year_max"][1].append(y)
        elif sum(metclmt[y]["prcp"]) > alltime["prcpPROP"]["year_max"][0]:
            alltime["prcpPROP"]["year_max"][0] = sum(metclmt[y]["prcp"])
            alltime["prcpPROP"]["year_max"][1] = []
            alltime["prcpPROP"]["year_max"][1].append(y)
        if metclmt[y]["recordqty"] > excludeyear:
            if metclmt[y]["prcpDAYS"] == alltime["prcpPROP"]["year_min_days"][0]: alltime["prcpPROP"]["year_min_days"][1].append(y)
            elif metclmt[y]["prcpDAYS"] < alltime["prcpPROP"]["year_min_days"][0]:
                alltime["prcpPROP"]["year_min_days"][0] = metclmt[y]["prcpDAYS"]
                alltime["prcpPROP"]["year_min_days"][1] = []
                alltime["prcpPROP"]["year_min_days"][1].append(y)
            if sum(metclmt[y]["prcp"]) == alltime["prcpPROP"]["year_min"][0]: alltime["prcpPROP"]["year_min"][1].append(y)
            elif sum(metclmt[y]["prcp"]) < alltime["prcpPROP"]["year_min"][0]:
                alltime["prcpPROP"]["year_min"][0] = sum(metclmt[y]["prcp"])
                alltime["prcpPROP"]["year_min"][1] = []
                alltime["prcpPROP"]["year_min"][1].append(y)
        for c in climo30yrs:
            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in metclmt  if type(YR) == int) and c[1] <= max(YR for YR in metclmt  if type(YR) == int):
                climo30yrs[c]["prcp"].append(sum(metclmt[y]["prcp"]))
                climo30yrs[c]["prcpPROP"]["days"] += metclmt[y]["prcpDAYS"]
                climo30yrs[c]["total_days"] += metclmt[y]["recordqty"]
                if metclmt[y]["recordqty"] > excludeyear:
                    if metclmt[y]["prcpDAYS"] == climo30yrs[c]["prcpPROP"]["year_max_days"][0]: climo30yrs[c]["prcpPROP"]["year_max_days"][1].append(y)
                    elif metclmt[y]["prcpDAYS"] > climo30yrs[c]["prcpPROP"]["year_max_days"][0]:
                        climo30yrs[c]["prcpPROP"]["year_max_days"][0] = metclmt[y]["prcpDAYS"]
                        climo30yrs[c]["prcpPROP"]["year_max_days"][1] = []
                        climo30yrs[c]["prcpPROP"]["year_max_days"][1].append(y)
                    if metclmt[y]["prcpDAYS"] == climo30yrs[c]["prcpPROP"]["year_min_days"][0]: climo30yrs[c]["prcpPROP"]["year_min_days"][1].append(y)
                    elif metclmt[y]["prcpDAYS"] < climo30yrs[c]["prcpPROP"]["year_min_days"][0]:
                        climo30yrs[c]["prcpPROP"]["year_min_days"][0] = metclmt[y]["prcpDAYS"]
                        climo30yrs[c]["prcpPROP"]["year_min_days"][1] = []
                        climo30yrs[c]["prcpPROP"]["year_min_days"][1].append(y)
                    if sum(metclmt[y]["prcp"]) == climo30yrs[c]["prcpPROP"]["year_max"][0]: climo30yrs[c]["prcpPROP"]["year_max"][1].append(y)
                    elif sum(metclmt[y]["prcp"]) > climo30yrs[c]["prcpPROP"]["year_max"][0]:
                        climo30yrs[c]["prcpPROP"]["year_max"][0] = sum(metclmt[y]["prcp"])
                        climo30yrs[c]["prcpPROP"]["year_max"][1] = []
                        climo30yrs[c]["prcpPROP"]["year_max"][1].append(y)
                    if sum(metclmt[y]["prcp"]) == climo30yrs[c]["prcpPROP"]["year_min"][0]: climo30yrs[c]["prcpPROP"]["year_min"][1].append(y)
                    elif sum(metclmt[y]["prcp"]) < climo30yrs[c]["prcpPROP"]["year_min"][0]:
                        climo30yrs[c]["prcpPROP"]["year_min"][0] = sum(metclmt[y]["prcp"])
                        climo30yrs[c]["prcpPROP"]["year_min"][1] = []
                        climo30yrs[c]["prcpPROP"]["year_min"][1].append(y)
        # SNOW
        alltime["snow"].append(sum(metclmt[y]["snow"]))
        alltime["snowPROP"]["days"] += metclmt[y]["snowDAYS"]
        if metclmt[y]["recordqty"] > excludeyear:
            if metclmt[y]["snowDAYS"] == alltime["snowPROP"]["year_max_days"][0]: alltime["snowPROP"]["year_max_days"][1].append(y)
            elif metclmt[y]["snowDAYS"] > alltime["snowPROP"]["year_max_days"][0]:
                alltime["snowPROP"]["year_max_days"][0] = metclmt[y]["snowDAYS"]
                alltime["snowPROP"]["year_max_days"][1] = []
                alltime["snowPROP"]["year_max_days"][1].append(y)
            if sum(metclmt[y]["snow"]) == alltime["snowPROP"]["year_max"][0]: alltime["snowPROP"]["year_max"][1].append(y)
            elif sum(metclmt[y]["snow"]) > alltime["snowPROP"]["year_max"][0]:
                alltime["snowPROP"]["year_max"][0] = sum(metclmt[y]["snow"])
                alltime["snowPROP"]["year_max"][1] = []
                alltime["snowPROP"]["year_max"][1].append(y)
        for c in climo30yrs:
            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in metclmt  if type(YR) == int) and c[1] <= max(YR for YR in metclmt  if type(YR) == int):
                climo30yrs[c]["snow"].append(sum(metclmt[y]["snow"]))
                climo30yrs[c]["snowPROP"]["days"] += metclmt[y]["snowDAYS"]
                if metclmt[y]["recordqty"] > excludeyear:
                    if metclmt[y]["snowDAYS"] == climo30yrs[c]["snowPROP"]["year_max_days"][0]: climo30yrs[c]["snowPROP"]["year_max_days"][1].append(y)
                    elif metclmt[y]["snowDAYS"] > climo30yrs[c]["snowPROP"]["year_max_days"][0]:
                        climo30yrs[c]["snowPROP"]["year_max_days"][0] = metclmt[y]["snowDAYS"]
                        climo30yrs[c]["snowPROP"]["year_max_days"][1] = []
                        climo30yrs[c]["snowPROP"]["year_max_days"][1].append(y)
                    if sum(metclmt[y]["snow"]) == climo30yrs[c]["snowPROP"]["year_max"][0]: climo30yrs[c]["snowPROP"]["year_max"][1].append(y)
                    elif sum(metclmt[y]["snow"]) > climo30yrs[c]["snowPROP"]["year_max"][0]:
                        climo30yrs[c]["snowPROP"]["year_max"][0] = sum(metclmt[y]["snow"])
                        climo30yrs[c]["snowPROP"]["year_max"][1] = []
                        climo30yrs[c]["snowPROP"]["year_max"][1].append(y)
    # 'recordqty', 'prcp', 'prcpDAYS', 'prcpPROP', 'snow', 'snowDAYS', 'snowPROP', 'tempAVGlist', 'tmax', 'tmaxPROP', 'tmin', 'tminPROP'
        # TAVG
        for x in metclmt[y]["tempAVGlist"]: alltime["tempAVGlist_ind"].append(x)
        if len(metclmt[y]["tempAVGlist"]) > excludeyear_tavg:
            alltime["tempAVGlist"].append(mean(metclmt[y]["tempAVGlist"]))
            if mean(metclmt[y]["tempAVGlist"]) == alltime["tavgPROP"]["year_max"][0]: alltime["tavgPROP"]["year_max"][1].append(y)
            elif mean(metclmt[y]["tempAVGlist"]) > alltime["tavgPROP"]["year_max"][0]:
                alltime["tavgPROP"]["year_max"][0] = mean(metclmt[y]["tempAVGlist"])
                alltime["tavgPROP"]["year_max"][1] = []
                alltime["tavgPROP"]["year_max"][1].append(y)
            if mean(metclmt[y]["tempAVGlist"]) == alltime["tavgPROP"]["year_min"][0]: alltime["tavgPROP"]["year_min"][1].append(y)
            elif mean(metclmt[y]["tempAVGlist"]) < alltime["tavgPROP"]["year_min"][0]:
                alltime["tavgPROP"]["year_min"][0] = mean(metclmt[y]["tempAVGlist"])
                alltime["tavgPROP"]["year_min"][1] = []
                alltime["tavgPROP"]["year_min"][1].append(y)
        for c in climo30yrs:
            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in metclmt  if type(YR) == int) and c[1] <= max(YR for YR in metclmt  if type(YR) == int):
                for x in metclmt[y]["tempAVGlist"]:climo30yrs[c]["tempAVGlist_ind"].append(x)
                if len(metclmt[y]["tempAVGlist"]) > excludeyear_tavg:
                    climo30yrs[c]["tempAVGlist"].append(mean(metclmt[y]["tempAVGlist"]))                    
                    if mean(metclmt[y]["tempAVGlist"]) == climo30yrs[c]["tavgPROP"]["year_max"][0]: climo30yrs[c]["tavgPROP"]["year_max"][1].append(y)
                    elif mean(metclmt[y]["tempAVGlist"]) > climo30yrs[c]["tavgPROP"]["year_max"][0]:
                        climo30yrs[c]["tavgPROP"]["year_max"][0] = mean(metclmt[y]["tempAVGlist"])
                        climo30yrs[c]["tavgPROP"]["year_max"][1] = []
                        climo30yrs[c]["tavgPROP"]["year_max"][1].append(y)
                    if mean(metclmt[y]["tempAVGlist"]) == climo30yrs[c]["tavgPROP"]["year_min"][0]: climo30yrs[c]["tavgPROP"]["year_min"][1].append(y)
                    elif mean(metclmt[y]["tempAVGlist"]) < climo30yrs[c]["tavgPROP"]["year_min"][0]:
                        climo30yrs[c]["tavgPROP"]["year_min"][0] = mean(metclmt[y]["tempAVGlist"])
                        climo30yrs[c]["tavgPROP"]["year_min"][1] = []
                        climo30yrs[c]["tavgPROP"]["year_min"][1].append(y)
        # TMAX
        for x in metclmt[y]["tmax"]: alltime["tmax"].append(x)
        if len(metclmt[y]["tmax"]) > excludeyear:
            if mean(metclmt[y]["tmax"]) == alltime["tmaxPROP"]["year_max"][0]: alltime["tmaxPROP"]["year_max"][1].append(y)
            elif mean(metclmt[y]["tmax"]) > alltime["tmaxPROP"]["year_max"][0]:
                alltime["tmaxPROP"]["year_max"][0] = mean(metclmt[y]["tmax"])
                alltime["tmaxPROP"]["year_max"][1] = []
                alltime["tmaxPROP"]["year_max"][1].append(y)
            if mean(metclmt[y]["tmax"]) == alltime["tmaxPROP"]["year_min"][0]: alltime["tmaxPROP"]["year_min"][1].append(y)
            elif mean(metclmt[y]["tmax"]) < alltime["tmaxPROP"]["year_min"][0]:
                alltime["tmaxPROP"]["year_min"][0] = mean(metclmt[y]["tmax"])
                alltime["tmaxPROP"]["year_min"][1] = []
                alltime["tmaxPROP"]["year_min"][1].append(y)
        for c in climo30yrs:
            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in metclmt  if type(YR) == int) and c[1] <= max(YR for YR in metclmt  if type(YR) == int):
                for x in metclmt[y]["tmax"]: climo30yrs[c]["tmax"].append(x)
                if len(metclmt[y]["tmax"]) > excludeyear:
                    if mean(metclmt[y]["tmax"]) == climo30yrs[c]["tmaxPROP"]["year_max"][0]: climo30yrs[c]["tmaxPROP"]["year_max"][1].append(y)
                    elif mean(metclmt[y]["tmax"]) > climo30yrs[c]["tmaxPROP"]["year_max"][0]:
                        climo30yrs[c]["tmaxPROP"]["year_max"][0] = mean(metclmt[y]["tmax"])
                        climo30yrs[c]["tmaxPROP"]["year_max"][1] = []
                        climo30yrs[c]["tmaxPROP"]["year_max"][1].append(y)
                    if mean(metclmt[y]["tmax"]) == climo30yrs[c]["tmaxPROP"]["year_min"][0]: climo30yrs[c]["tmaxPROP"]["year_min"][1].append(y)
                    elif mean(metclmt[y]["tmax"]) < climo30yrs[c]["tmaxPROP"]["year_min"][0]:
                        climo30yrs[c]["tmaxPROP"]["year_min"][0] = mean(metclmt[y]["tmax"])
                        climo30yrs[c]["tmaxPROP"]["year_min"][1] = []
                        climo30yrs[c]["tmaxPROP"]["year_min"][1].append(y)
        # TMIN
        for x in metclmt[y]["tmin"]: alltime["tmin"].append(x)
        if len(metclmt[y]["tmin"]) > excludeyear:
            if mean(metclmt[y]["tmin"]) == alltime["tminPROP"]["year_max"][0]: alltime["tminPROP"]["year_max"][1].append(y)
            elif mean(metclmt[y]["tmin"]) > alltime["tminPROP"]["year_max"][0]:
                alltime["tminPROP"]["year_max"][0] = mean(metclmt[y]["tmin"])
                alltime["tminPROP"]["year_max"][1] = []
                alltime["tminPROP"]["year_max"][1].append(y)
            if mean(metclmt[y]["tmin"]) == alltime["tminPROP"]["year_min"][0]: alltime["tminPROP"]["year_min"][1].append(y)
            elif mean(metclmt[y]["tmin"]) < alltime["tminPROP"]["year_min"][0]:
                alltime["tminPROP"]["year_min"][0] = mean(metclmt[y]["tmin"])
                alltime["tminPROP"]["year_min"][1] = []
                alltime["tminPROP"]["year_min"][1].append(y)
        for c in climo30yrs:
            if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in metclmt  if type(YR) == int) and c[1] <= max(YR for YR in metclmt  if type(YR) == int):
                for x in metclmt[y]["tmin"]: climo30yrs[c]["tmin"].append(x)
                if len(metclmt[y]["tmin"]) > excludeyear:
                    if mean(metclmt[y]["tmin"]) == climo30yrs[c]["tminPROP"]["year_max"][0]: climo30yrs[c]["tminPROP"]["year_max"][1].append(y)
                    elif mean(metclmt[y]["tmin"]) > climo30yrs[c]["tminPROP"]["year_max"][0]:
                        climo30yrs[c]["tminPROP"]["year_max"][0] = mean(metclmt[y]["tmin"])
                        climo30yrs[c]["tminPROP"]["year_max"][1] = []
                        climo30yrs[c]["tminPROP"]["year_max"][1].append(y)
                    if mean(metclmt[y]["tmin"]) == climo30yrs[c]["tminPROP"]["year_min"][0]: climo30yrs[c]["tminPROP"]["year_min"][1].append(y)
                    elif mean(metclmt[y]["tmin"]) < climo30yrs[c]["tminPROP"]["year_min"][0]:
                        climo30yrs[c]["tminPROP"]["year_min"][0] = mean(metclmt[y]["tmin"])
                        climo30yrs[c]["tminPROP"]["year_min"][1] = []
                        climo30yrs[c]["tminPROP"]["year_min"][1].append(y)

    # PRINT REPORT
    print("---------------------------------------------------")
    print("Climatology Report for All Meteorological Years on Record")
    print("City: {}, {}".format(metclmt["station"],metclmt["station_name"]))
    print("{}-{}; {}-Year Incremented {}-Year Climatologies".format(min(valid_yrs),max(valid_yrs),clmt_inc_rpt,clmt_len_rpt))
    print("---------------------------------------------------")
    print("Part 1: Precipitation Stats")
    print("{:▒^9} {:▒^12}  {:▒^9}  {:▒^9}  {:▒^6} {:▒^12} {:▒^12} | {:▒^11}  {:▒^9} {:▒^6} {:▒^11} |".format("Years","PRCP","PRCP","PRCP","PRCP","PRCP","PRCP","SNOW","SNOW","SNOW","SNOW"))
    print("{:▒^9} {:▒^12}  {:▒^9}  {:▒^9}  {:▒^6} {:▒^12} {:▒^12} | {:▒^11}  {:▒^9} {:▒^6} {:▒^11} |".format("","DAYS","DAYS MAX","DAYS MIN","AVG", "MAX","MIN","DAYS","DAYS MAX","AVG", "MAX"))
    #         Y     PD       PDx    PDn      PA      PM     Pmin      SD     SDx       SA      SM
    print("{:-^9} {:-^12}  {:-^9}  {:-^9}  {:-^6} {:-^12} {:-^12} | {:-^11}  {:-^9} {:-^6} {:-^11} |".format("","","","","","","","","","",""))
    print("{:^9} {:5}:{:>5}%  {:>3}, {:^4}  {:>3}, {:^4}  {:^6.2f} {:>6.2f}, {:^4} {:>6.2f}, {:^4} | {:4}:{:>5}%  {:>3}, {:^4} {:^6.1f} {:>5.1f}, {:^4} |".format("All Time",
        alltime["prcpPROP"]["days"],
        round(100 * alltime["prcpPROP"]["days"] / alltime["total_days"],1),
        alltime["prcpPROP"]["year_max_days"][0],
        alltime["prcpPROP"]["year_max_days"][1][0] if len(alltime["prcpPROP"]["year_max_days"][1]) == 1 else len(alltime["prcpPROP"]["year_max_days"][1]),
        alltime["prcpPROP"]["year_min_days"][0],
        alltime["prcpPROP"]["year_min_days"][1][0] if len(alltime["prcpPROP"]["year_min_days"][1]) == 1 else len(alltime["prcpPROP"]["year_min_days"][1]),
        round(mean(alltime["prcp"]),2) if len(alltime["prcp"]) > 0 else "--",
        round(alltime["prcpPROP"]["year_max"][0],2),
        alltime["prcpPROP"]["year_max"][1][0] if len(alltime["prcpPROP"]["year_max"][1]) == 1 else len(alltime["prcpPROP"]["year_max"][1]),
        round(alltime["prcpPROP"]["year_min"][0],2),
        alltime["prcpPROP"]["year_min"][1][0] if len(alltime["prcpPROP"]["year_min"][1]) == 1 else len(alltime["prcpPROP"]["year_min"][1]),
        alltime["snowPROP"]["days"] if alltime["snowPROP"]["days"] > 0 else "--",
        round(100 * alltime["snowPROP"]["days"] / alltime["total_days"],1) if alltime["snowPROP"]["days"] > 0 else "--",
        alltime["snowPROP"]["year_max_days"][0],
        alltime["snowPROP"]["year_max_days"][1][0] if len(alltime["snowPROP"]["year_max_days"][1]) == 1 else len(alltime["snowPROP"]["year_max_days"][1]),
        round(mean(alltime["snow"]),1) if len(alltime["snow"]) > 0 else "--",
        round(alltime["snowPROP"]["year_max"][0],2),
        alltime["snowPROP"]["year_max"][1][0] if len(alltime["snowPROP"]["year_max"][1]) == 1 else len(alltime["snowPROP"]["year_max"][1])))
    for c in climo30yrs:
        #print(climo30yrs[c]["prcpPROP"]["days"],climo30yrs[c]["total_days"])
        #print(climo30yrs[c]["snowPROP"]["days"],climo30yrs[c]["total_days"])
        try:
            print("{:^9} {:5}:{:>5}%  {:>3}, {:^4}  {:>3}, {:^4}  {:^6.2f} {:>6.2f}, {:^4} {:>6.2f}, {:^4} | {:4}:{:>5}%  {:>3}, {:^4} {:^6.1f} {:>5.1f}, {:^4} |".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
            climo30yrs[c]["prcpPROP"]["days"],
            round(100 * climo30yrs[c]["prcpPROP"]["days"] / climo30yrs[c]["total_days"],1),
            climo30yrs[c]["prcpPROP"]["year_max_days"][0],
            climo30yrs[c]["prcpPROP"]["year_max_days"][1][0] if len(climo30yrs[c]["prcpPROP"]["year_max_days"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["year_max_days"][1]),
            climo30yrs[c]["prcpPROP"]["year_min_days"][0],
            climo30yrs[c]["prcpPROP"]["year_min_days"][1][0] if len(climo30yrs[c]["prcpPROP"]["year_min_days"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["year_min_days"][1]),
            round(mean(climo30yrs[c]["prcp"]),2),
            round(climo30yrs[c]["prcpPROP"]["year_max"][0],2),
            climo30yrs[c]["prcpPROP"]["year_max"][1][0] if len(climo30yrs[c]["prcpPROP"]["year_max"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["year_max"][1]),
            round(climo30yrs[c]["prcpPROP"]["year_min"][0],2),
            climo30yrs[c]["prcpPROP"]["year_min"][1][0] if len(climo30yrs[c]["prcpPROP"]["year_min"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["year_min"][1]),
            climo30yrs[c]["snowPROP"]["days"] if climo30yrs[c]["snowPROP"]["days"] > 0 else "--",
            round(100 * climo30yrs[c]["snowPROP"]["days"] / climo30yrs[c]["total_days"],1) if climo30yrs[c]["snowPROP"]["days"] > 0 else "--",
            climo30yrs[c]["snowPROP"]["year_max_days"][0],
            climo30yrs[c]["snowPROP"]["year_max_days"][1][0] if len(climo30yrs[c]["snowPROP"]["year_max_days"][1]) == 1 else len(climo30yrs[c]["snowPROP"]["year_max_days"][1]),
            round(mean(climo30yrs[c]["snow"]),1) if len(climo30yrs[c]["snow"]) > 0 else "--",
            round(climo30yrs[c]["snowPROP"]["year_max"][0],2),
            climo30yrs[c]["snowPROP"]["year_max"][1][0] if len(climo30yrs[c]["snowPROP"]["year_max"][1]) == 1 else len(climo30yrs[c]["snowPROP"]["year_max"][1])))
        except Exception as e:
            print("ERROR: Era = {}; Exception = {}".format(c,e))

    print("\nPart 2: Temperature Stats")
    print("{:▒^9} {:▒^37} | {:▒^37} | {:▒^37}".format("Years","AVG TEMP","TMAX","TMIN"))
    print("{:▒^9} {:▒<5} {:▒^5} {:▒^12} {:▒^12} | {:▒<5} {:▒^5} {:▒^12} {:▒^12} | {:▒<5} {:▒^5} {:▒^12} {:▒^12}".format("","STDEV","AVG","MAX","MIN","STDEV","AVG","MAX","MIN","STDEV","AVG","MAX","MIN"))
    #         Y    TSTDV   TMA     TMX    TMn      TSTDV   TMA     TMX    TMn      TSTDV   TMA     TMX    TMn    
    # "tempAVGlist": [],"tavgPROP":{"year_max":[-999,[]],"year_min":[999,[]]},
    print("{:-^9} {:-^5} {:-^5} {:-^12} {:-^12} | {:-^5} {:-^5} {:-^12} {:-^12} | {:-^5} {:-^5} {:-^12} {:-^12}".format("","","","","","","","","","","","",""))
    print("{:^9} {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5}".format("All Time",
        round(pstdev(alltime["tempAVGlist"]),1),
        round(mean(alltime["tempAVGlist_ind"]),1),
        round(alltime["tavgPROP"]["year_max"][0],1),
        alltime["tavgPROP"]["year_max"][1][0] if len(alltime["tavgPROP"]["year_max"][1]) == 1 else len(alltime["tavgPROP"]["year_max"][1]),
        round(alltime["tavgPROP"]["year_min"][0],1),
        alltime["tavgPROP"]["year_min"][1][0] if len(alltime["tavgPROP"]["year_min"][1]) == 1 else len(alltime["tavgPROP"]["year_min"][1]),
        round(pstdev(alltime["tmax"]),1),
        round(mean(alltime["tmax"]),1),
        round(alltime["tmaxPROP"]["year_max"][0],1),
        alltime["tmaxPROP"]["year_max"][1][0] if len(alltime["tmaxPROP"]["year_max"][1]) == 1 else len(alltime["tmaxPROP"]["year_max"][1]),
        round(alltime["tmaxPROP"]["year_min"][0],1),
        alltime["tmaxPROP"]["year_min"][1][0] if len(alltime["tmaxPROP"]["year_min"][1]) == 1 else len(alltime["tmaxPROP"]["year_min"][1]),
        round(pstdev(alltime["tmin"]),1),
        round(mean(alltime["tmin"]),1),
        round(alltime["tminPROP"]["year_max"][0],1),
        alltime["tminPROP"]["year_max"][1][0] if len(alltime["tminPROP"]["year_max"][1]) == 1 else len(alltime["tminPROP"]["year_max"][1]),
        round(alltime["tminPROP"]["year_min"][0],1),
        alltime["tminPROP"]["year_min"][1][0] if len(alltime["tminPROP"]["year_min"][1]) == 1 else len(alltime["tminPROP"]["year_min"][1])))
    for c in climo30yrs:
        try:
            print("{:^9} {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5}".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
                round(pstdev(climo30yrs[c]["tempAVGlist"]),1),
                round(mean(climo30yrs[c]["tempAVGlist_ind"]),1),
                round(climo30yrs[c]["tavgPROP"]["year_max"][0],1),
                climo30yrs[c]["tavgPROP"]["year_max"][1][0] if len(climo30yrs[c]["tavgPROP"]["year_max"][1]) == 1 else len(climo30yrs[c]["tavgPROP"]["year_max"][1]),
                round(climo30yrs[c]["tavgPROP"]["year_min"][0],1),
                climo30yrs[c]["tavgPROP"]["year_min"][1][0] if len(climo30yrs[c]["tavgPROP"]["year_min"][1]) == 1 else len(climo30yrs[c]["tavgPROP"]["year_min"][1]),
                round(pstdev(climo30yrs[c]["tmax"]),1),
                round(mean(climo30yrs[c]["tmax"]),1),
                round(climo30yrs[c]["tmaxPROP"]["year_max"][0],1),
                climo30yrs[c]["tmaxPROP"]["year_max"][1][0] if len(climo30yrs[c]["tmaxPROP"]["year_max"][1]) == 1 else len(climo30yrs[c]["tmaxPROP"]["year_max"][1]),
                round(climo30yrs[c]["tmaxPROP"]["year_min"][0],1),
                climo30yrs[c]["tmaxPROP"]["year_min"][1][0] if len(climo30yrs[c]["tmaxPROP"]["year_min"][1]) == 1 else len(climo30yrs[c]["tmaxPROP"]["year_min"][1]),
                round(pstdev(climo30yrs[c]["tmin"]),1),
                round(mean(climo30yrs[c]["tmin"]),1),
                round(climo30yrs[c]["tminPROP"]["year_max"][0],1),
                climo30yrs[c]["tminPROP"]["year_max"][1][0] if len(climo30yrs[c]["tminPROP"]["year_max"][1]) == 1 else len(climo30yrs[c]["tminPROP"]["year_max"][1]),
                round(climo30yrs[c]["tminPROP"]["year_min"][0],1),
                climo30yrs[c]["tminPROP"]["year_min"][1][0] if len(climo30yrs[c]["tminPROP"]["year_min"][1]) == 1 else len(climo30yrs[c]["tminPROP"]["year_min"][1])))
        except Exception as e:
            print("ERROR: Era = {}; Exception = {}".format(c,e))
    print("")

    if "output" in output and output["output"] == True:
        newfn = "metYearReport_Mar-Feb_" + str(clmt_len_rpt) + "YRclimo_" + str(clmt_inc_rpt) + "YRincr_" + clmt["station_name"] + ".csv"
        with open(newfn,"w") as w:
            headers = ["Assessed Period (March to February)","PRCP Days","PRCP % of days","PRCP stdev","PRCP AVG","SNOW Days","SNOW % of days","SNOW stdev","SNOW AVG","TAVG stdev","TAVG","TMAX stdev","TMAX","TMIN stdev","TMIN"]
            # HEADER
            for x in range(len(headers)):
                if x != len(headers) - 1: w.write(headers[x]); w.write(",")
                else: w.write(headers[x]); w.write("\n")
            w.write("{}-{}".format(alltime["years"][0],alltime["years"][1])); w.write(",")
            w.write("{}".format(alltime["prcpPROP"]["days"])); w.write(",")
            w.write("{:.1f}".format(round(100 * alltime["prcpPROP"]["days"] / alltime["total_days"],1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["prcp"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["prcp"]),1))); w.write(",")
            w.write("{}".format(alltime["snowPROP"]["days"])); w.write(",")
            w.write("{:.1f}".format(round(100 * alltime["snowPROP"]["days"] / alltime["total_days"],1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["snow"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["snow"]),1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tempAVGlist"]),1))); w.write(",")
            w.write("{:.2f}".format(mean(alltime["tempAVGlist_ind"]))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tmax"]),1))); w.write(",")
            w.write("{:.2f}".format(mean(alltime["tmax"]))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tmin"]),1))); w.write(",")
            w.write("{:.2f}".format(mean(alltime["tmin"]))); w.write("\n")
            for x in climo30yrs:
                w.write("{}-{}".format(climo30yrs[x]["years"][0],climo30yrs[x]["years"][1])); w.write(",")
                w.write("{}".format(climo30yrs[x]["prcpPROP"]["days"])); w.write(",")
                w.write("{:.1f}".format(round(100 * climo30yrs[x]["prcpPROP"]["days"] / climo30yrs[x]["total_days"],1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["prcp"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["prcp"]),1))); w.write(",")
                w.write("{}".format(climo30yrs[x]["snowPROP"]["days"])); w.write(",")
                w.write("{:.1f}".format(round(100 * climo30yrs[x]["snowPROP"]["days"] / climo30yrs[x]["total_days"],1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["snow"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["snow"]),1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tempAVGlist"]),1))); w.write(",")
                w.write("{:.2f}".format(mean(climo30yrs[x]["tempAVGlist_ind"]))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tmax"]),1))); w.write(",")
                w.write("{:.2f}".format(mean(climo30yrs[x]["tmax"]))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tmin"]),1))); w.write(",")
                w.write("{:.2f}".format(mean(climo30yrs[x]["tmin"]))); w.write("\n")
            print("*** csv output successful ***")

def customReport(m1,d1,*date2,**output):
    """Detailed Climatological Report on a custom-length period of statistics.
    All passed arguments MUST be integers. If the optional ending arguments
    are not included, the default ending will be December 31. If the end day
    given occurs before the start day in the calendar year, the end day of the
    following year will be used in compiling stats.
    
    customReport(M1,D1,*[M2,D2],**{output=False})
    
    REQUIRED: M1,D1 --> Represent the beginning month, and day of the custom
                        period.
    OPT *args: M2,D2 --> These optional entries represent the ending month,
                         and day of the period

    EXAMPLE: customReport(10,23) -> Returns a climatological report for the
                                    period between October 23 and December 31
    EXAMPLE: customReport(6,1,11,30) -> Returns a climatological report for
                                        the period between June 1 and Nov 30
    """
    if len(clmt) == 0: return print("* OOPS! Run the clmtAnalyze function first.")
    valid_yrs = [x for x in clmt.keys() if type(x) == int]
    valid_yrs.sort()
    
    if any(type(x) != int for x in [m1,d1]): return print("*** OOPS! Ensure that only integers are entered ***")
    if len(date2) == 0: pass
    elif len(date2) != 2: return print("*** OOPS! For the 2nd (optional) date, ensure only a Month and Date are entered ***")
    elif any(type(x) != int for x in [date2[0],date2[1]]): return print("*** OOPS! Ensure that only integers are entered ***")
    
    if len(date2) == 2:
        m2 = date2[0]
        d2 = date2[1]
    else:
        m2 = 12
        d2 = 31
    
    if m2 == m1:
        if d2 == d1: return print("*** OOPS! Ensure different dates! ***")
    
    if m1 == 2 and d1 == 29: d1 = 28
    if m2 == 2 and d2 == 29: d2 = 28

    # Determine total length of period (used for exclusion calculation)
    s = datetime.date(1900,m1,d1)
    test = datetime.date(1900,m2,d2)
    if test > s: e = test
    else: e = datetime.date(1901,m2,d2)
    timelength = (e - s).days + 1
    if timelength < 7: EXCLD = 1
    elif timelength == 7: EXCLD = excludeweek
    elif timelength in [28,29,30,31]: EXCLD = excludemonth
    elif timelength >= 350: EXCLD = excludeyear
    else: EXCLD = round(excludecustom * timelength)
    
    print("EXCLUDING PERIODS OF <= {} DAYS".format(EXCLD))
    
    climo30yrs = {}
    for x in range(1811,max(valid_yrs)+1,clmt_inc_rpt):
        if x in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]) and x+clmt_len_rpt-1 in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]+1):
            climo30yrs[(x,x+clmt_len_rpt-1)] = {"years":(x,x+clmt_len_rpt-1),"total_days":0,
                                    "prcp": [],"prcpPROP":{"days":0,"e_max_days":[-1,[]],"e_min_days":[999,[]],"e_max":[-1,[]],"e_min":[999,[]]},
                                    "snow": [],"snowPROP":{"days":0,"e_max_days":[-1,[]],"e_max":[-1,[]]},
                                    "tempAVGlist": [],"tempAVGlist_ind":[],"tavgPROP":{"e_max":[-999,[]],"e_min":[999,[]]},
                                    "tmax": [],"tmaxPROP":{"e_max":[-999,[]],"e_min":[999,[]]},
                                    "tmin": [],"tminPROP":{"e_max":[-999,[]],"e_min":[999,[]]}}

    alltime = {"years":(valid_yrs[0],valid_yrs[len(valid_yrs)-1]),"total_days":0,
               "prcp": [],"prcpPROP":{"days":0,"e_max_days":[-1,[]],"e_min_days":[999,[]],"e_max":[-1,[]],"e_min":[999,[]]},
               "snow": [],"snowPROP":{"days":0,"e_max_days":[-1,[]],"e_max":[-1,[]]},
               "tempAVGlist": [],"tempAVGlist_ind":[],"tavgPROP":{"e_max":[-999,[]],"e_min":[999,[]]},
               "tmax": [],"tmaxPROP":{"e_max":[-999,[]],"e_min":[999,[]]},
               "tmin": [],"tminPROP":{"e_max":[-999,[]],"e_min":[999,[]]}}

    e = {}  # Will hold the date-to-date (represented by a parent year) stats

    print("*** Be Patient. This could take a few moments ***")
    


    for YYYY in valid_yrs:
        startday = datetime.date(YYYY,m1,d1)
        incr_day = startday
        if m2 < m1: endday = datetime.date(YYYY+1,m2,d2)   # if end month is less, the results will bleed into the following year
        elif m2 == m1:  # Deals with if the months of the dates are exactly the same
            if d2 < d1: endday = datetime.date(YYYY+1,m2,d2)     # like above, if month is the same, but date is less, results will bleed into following year
            else: endday = datetime.date(YYYY,m2,d2)               # OTHERWISE, it is assumed the same year
        else: endday = datetime.date(YYYY,m2,d2)       # If month2 is > than month 1, the active year will be used
        
        if endday.year > max(valid_yrs): break

        #if YYYY not in e:
        e[YYYY] = {"recordqty":0,
                   "prcp":[],"prcpDAYS":0,"snow":[],"snowDAYS":0,
                   "tempAVGlist":[],"tmax":[],"tmin":[]}
        
        while incr_day <= endday:
            y = incr_day.year; m = incr_day.month; d = incr_day.day
            if y in clmt and m in clmt[y] and d in clmt[y][m]:
                e[YYYY]["recordqty"] += 1
                # PRCP
                if clmt[y][m][d].prcpQ in ignoreflags and clmt[y][m][d].prcp not in ["9999","-9999",""]:
                    if float(clmt[y][m][d].prcp) > 0: e[YYYY]["prcp"].append(round(float(clmt[y][m][d].prcp),2))
                    if float(clmt[y][m][d].prcp) > 0 or clmt[y][m][d].prcpM == "T": e[YYYY]["prcpDAYS"] += 1
                if clmt[y][m][d].prcpQ in ignoreflags and clmt[y][m][d].prcp == "" and clmt[y][m][d].prcpM == "T": e[YYYY]["prcpDAYS"] += 1
                # SNOW
                if clmt[y][m][d].snowQ in ignoreflags and clmt[y][m][d].snow not in ["9999","-9999",""]:
                    if float(clmt[y][m][d].snow) > 0: e[YYYY]["snow"].append(round(float(clmt[y][m][d].snow),2))
                    if float(clmt[y][m][d].snow) > 0 or clmt[y][m][d].snowM == "T": e[YYYY]["snowDAYS"] += 1
                if clmt[y][m][d].snowQ in ignoreflags and clmt[y][m][d].snow == "" and clmt[y][m][d].snowM == "T": e[YYYY]["snowDAYS"] += 1
                # TAVG
                if clmt[y][m][d].tmaxQ in ignoreflags and clmt[y][m][d].tmax not in ["9999","-9999",""] and clmt[y][m][d].tminQ in ignoreflags and clmt[y][m][d].tmin not in ["9999","-9999",""] and int(clmt[y][m][d].tmax) >= int(clmt[y][m][d].tmin):
                    e[YYYY]["tempAVGlist"].append(int(clmt[y][m][d].tmax))
                    e[YYYY]["tempAVGlist"].append(int(clmt[y][m][d].tmin))
                # TMAX
                if clmt[y][m][d].tmaxQ in ignoreflags and clmt[y][m][d].tmax not in ["9999","-9999",""]:
                    if clmt[y][m][d].tmin != "" and int(clmt[y][m][d].tmax) >= int(clmt[y][m][d].tmin):
                        e[YYYY]["tmax"].append(int(clmt[y][m][d].tmax))
                # TMIN
                if clmt[y][m][d].tminQ in ignoreflags and clmt[y][m][d].tmin not in ["9999","-9999",""]:
                    if clmt[y][m][d].tmax != "" and int(clmt[y][m][d].tmin) <= int(clmt[y][m][d].tmax):
                        e[YYYY]["tmin"].append(int(clmt[y][m][d].tmin))
            incr_day += datetime.timedelta(days=1)  # GO ON TO TEST NEXT DAY

    for YYYY in e:
        #print('e[{}]["prcpDAYS"] = {}'.format(YYYY,e[YYYY]["prcpDAYS"]))
        #print('sum(e[{}]["prcp"] = {})'.format(YYYY,sum(e[YYYY]["prcp"])))
        #print("----")
        #print('alltime["prcpPROP"]["e_max_days"][0] = {}'.format(alltime["prcpPROP"]["e_max_days"][0]))
        #print('alltime["prcpPROP"]["e_max_days"][1] = {}'.format(alltime["prcpPROP"]["e_max_days"][1]))
        #print('alltime["prcpPROP"]["e_max"][0] = {}'.format(alltime["prcpPROP"]["e_max"][0]))
        #print('alltime["prcpPROP"]["e_max"][1] = {}'.format(alltime["prcpPROP"]["e_max"][1]))
        #input("----")
        
        alltime["total_days"] += e[YYYY]["recordqty"]
        # PRCP
        alltime["prcp"].append(sum(e[YYYY]["prcp"]))
        alltime["prcpPROP"]["days"] += e[YYYY]["prcpDAYS"]
        if e[YYYY]["prcpDAYS"] == alltime["prcpPROP"]["e_max_days"][0]: alltime["prcpPROP"]["e_max_days"][1].append(YYYY)
        elif e[YYYY]["prcpDAYS"] > alltime["prcpPROP"]["e_max_days"][0]:
            alltime["prcpPROP"]["e_max_days"][0] = e[YYYY]["prcpDAYS"]
            alltime["prcpPROP"]["e_max_days"][1] = []
            alltime["prcpPROP"]["e_max_days"][1].append(YYYY)
        if sum(e[YYYY]["prcp"]) == alltime["prcpPROP"]["e_max"][0]: alltime["prcpPROP"]["e_max"][1].append(YYYY)
        elif sum(e[YYYY]["prcp"]) > alltime["prcpPROP"]["e_max"][0]:
            alltime["prcpPROP"]["e_max"][0] = sum(e[YYYY]["prcp"])
            alltime["prcpPROP"]["e_max"][1] = []
            alltime["prcpPROP"]["e_max"][1].append(YYYY)
        if e[YYYY]["recordqty"] > EXCLD:
            if e[YYYY]["prcpDAYS"] == alltime["prcpPROP"]["e_min_days"][0]: alltime["prcpPROP"]["e_min_days"][1].append(YYYY)
            elif e[YYYY]["prcpDAYS"] < alltime["prcpPROP"]["e_min_days"][0]:
                alltime["prcpPROP"]["e_min_days"][0] = e[YYYY]["prcpDAYS"]
                alltime["prcpPROP"]["e_min_days"][1] = []
                alltime["prcpPROP"]["e_min_days"][1].append(YYYY)
            if sum(e[YYYY]["prcp"]) == alltime["prcpPROP"]["e_min"][0]: alltime["prcpPROP"]["e_min"][1].append(YYYY)
            elif sum(e[YYYY]["prcp"]) < alltime["prcpPROP"]["e_min"][0]:
                alltime["prcpPROP"]["e_min"][0] = sum(e[YYYY]["prcp"])
                alltime["prcpPROP"]["e_min"][1] = []
                alltime["prcpPROP"]["e_min"][1].append(YYYY)
        for c in climo30yrs:
            if YYYY >= c[0] and YYYY <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                climo30yrs[c]["prcp"].append(sum(e[YYYY]["prcp"]))
                climo30yrs[c]["prcpPROP"]["days"] += e[YYYY]["prcpDAYS"]
                climo30yrs[c]["total_days"] += e[YYYY]["recordqty"]
                if e[YYYY]["prcpDAYS"] == climo30yrs[c]["prcpPROP"]["e_max_days"][0]: climo30yrs[c]["prcpPROP"]["e_max_days"][1].append(YYYY)
                elif e[YYYY]["prcpDAYS"] > climo30yrs[c]["prcpPROP"]["e_max_days"][0]:
                    climo30yrs[c]["prcpPROP"]["e_max_days"][0] = e[YYYY]["prcpDAYS"]
                    climo30yrs[c]["prcpPROP"]["e_max_days"][1] = []
                    climo30yrs[c]["prcpPROP"]["e_max_days"][1].append(YYYY)
                if sum(e[YYYY]["prcp"]) == climo30yrs[c]["prcpPROP"]["e_max"][0]: climo30yrs[c]["prcpPROP"]["e_max"][1].append(YYYY)
                elif sum(e[YYYY]["prcp"]) > climo30yrs[c]["prcpPROP"]["e_max"][0]:
                    climo30yrs[c]["prcpPROP"]["e_max"][0] = sum(e[YYYY]["prcp"])
                    climo30yrs[c]["prcpPROP"]["e_max"][1] = []
                    climo30yrs[c]["prcpPROP"]["e_max"][1].append(YYYY)
                if e[YYYY]["recordqty"] > EXCLD:
                    if e[YYYY]["prcpDAYS"] == climo30yrs[c]["prcpPROP"]["e_min_days"][0]: climo30yrs[c]["prcpPROP"]["e_min_days"][1].append(YYYY)
                    elif e[YYYY]["prcpDAYS"] < climo30yrs[c]["prcpPROP"]["e_min_days"][0]:
                        climo30yrs[c]["prcpPROP"]["e_min_days"][0] = e[YYYY]["prcpDAYS"]
                        climo30yrs[c]["prcpPROP"]["e_min_days"][1] = []
                        climo30yrs[c]["prcpPROP"]["e_min_days"][1].append(YYYY)
                    if sum(e[YYYY]["prcp"]) == climo30yrs[c]["prcpPROP"]["e_min"][0]: climo30yrs[c]["prcpPROP"]["e_min"][1].append(YYYY)
                    elif sum(e[YYYY]["prcp"]) < climo30yrs[c]["prcpPROP"]["e_min"][0]:
                        climo30yrs[c]["prcpPROP"]["e_min"][0] = sum(e[YYYY]["prcp"])
                        climo30yrs[c]["prcpPROP"]["e_min"][1] = []
                        climo30yrs[c]["prcpPROP"]["e_min"][1].append(YYYY)

        # SNOW
        alltime["snow"].append(sum(e[YYYY]["snow"]))
        alltime["snowPROP"]["days"] += e[YYYY]["snowDAYS"]
        if e[YYYY]["snowDAYS"] == alltime["snowPROP"]["e_max_days"][0]: alltime["snowPROP"]["e_max_days"][1].append(YYYY)
        elif e[YYYY]["snowDAYS"] > alltime["snowPROP"]["e_max_days"][0]:
            alltime["snowPROP"]["e_max_days"][0] = e[YYYY]["snowDAYS"]
            alltime["snowPROP"]["e_max_days"][1] = []
            alltime["snowPROP"]["e_max_days"][1].append(YYYY)
        if sum(e[YYYY]["snow"]) == alltime["snowPROP"]["e_max"][0]: alltime["snowPROP"]["e_max"][1].append(YYYY)
        elif sum(e[YYYY]["snow"]) > alltime["snowPROP"]["e_max"][0]:
            alltime["snowPROP"]["e_max"][0] = sum(e[YYYY]["snow"])
            alltime["snowPROP"]["e_max"][1] = []
            alltime["snowPROP"]["e_max"][1].append(YYYY)
        for c in climo30yrs:
            if YYYY >= c[0] and YYYY <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                climo30yrs[c]["snow"].append(sum(e[YYYY]["snow"]))
                climo30yrs[c]["snowPROP"]["days"] += e[YYYY]["snowDAYS"]
                if e[YYYY]["snowDAYS"] == climo30yrs[c]["snowPROP"]["e_max_days"][0]: climo30yrs[c]["snowPROP"]["e_max_days"][1].append(YYYY)
                elif e[YYYY]["snowDAYS"] > climo30yrs[c]["snowPROP"]["e_max_days"][0]:
                    climo30yrs[c]["snowPROP"]["e_max_days"][0] = e[YYYY]["snowDAYS"]
                    climo30yrs[c]["snowPROP"]["e_max_days"][1] = []
                    climo30yrs[c]["snowPROP"]["e_max_days"][1].append(YYYY)
                if sum(e[YYYY]["snow"]) == climo30yrs[c]["snowPROP"]["e_max"][0]: climo30yrs[c]["snowPROP"]["e_max"][1].append(YYYY)
                elif sum(e[YYYY]["snow"]) > climo30yrs[c]["snowPROP"]["e_max"][0]:
                    climo30yrs[c]["snowPROP"]["e_max"][0] = sum(e[YYYY]["snow"])
                    climo30yrs[c]["snowPROP"]["e_max"][1] = []
                    climo30yrs[c]["snowPROP"]["e_max"][1].append(YYYY)
# 'recordqty', 'prcp', 'prcpDAYS', 'prcpPROP', 'snow', 'snowDAYS', 'snowPROP', 'tempAVGlist', 'tmax', 'tmaxPROP', 'tmin', 'tminPROP'
        # TAVG
        for x in e[YYYY]["tempAVGlist"]: alltime["tempAVGlist_ind"].append(x)
        if len(e[YYYY]["tempAVGlist"]) > EXCLD * 2:
            alltime["tempAVGlist"].append(mean(e[YYYY]["tempAVGlist"]))
            if mean(e[YYYY]["tempAVGlist"]) == alltime["tavgPROP"]["e_max"][0]: alltime["tavgPROP"]["e_max"][1].append(YYYY)
            elif mean(e[YYYY]["tempAVGlist"]) > alltime["tavgPROP"]["e_max"][0]:
                alltime["tavgPROP"]["e_max"][0] = mean(e[YYYY]["tempAVGlist"])
                alltime["tavgPROP"]["e_max"][1] = []
                alltime["tavgPROP"]["e_max"][1].append(YYYY)
            if mean(e[YYYY]["tempAVGlist"]) == alltime["tavgPROP"]["e_min"][0]: alltime["tavgPROP"]["e_min"][1].append(YYYY)
            elif mean(e[YYYY]["tempAVGlist"]) < alltime["tavgPROP"]["e_min"][0]:
                alltime["tavgPROP"]["e_min"][0] = mean(e[YYYY]["tempAVGlist"])
                alltime["tavgPROP"]["e_min"][1] = []
                alltime["tavgPROP"]["e_min"][1].append(YYYY)
        for c in climo30yrs:
            if YYYY >= c[0] and YYYY <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                for x in e[YYYY]["tempAVGlist"]:climo30yrs[c]["tempAVGlist_ind"].append(x)
                if len(e[YYYY]["tempAVGlist"]) > EXCLD * 2:
                    climo30yrs[c]["tempAVGlist"].append(mean(e[YYYY]["tempAVGlist"]))                    
                    if mean(e[YYYY]["tempAVGlist"]) == climo30yrs[c]["tavgPROP"]["e_max"][0]: climo30yrs[c]["tavgPROP"]["e_max"][1].append(YYYY)
                    elif mean(e[YYYY]["tempAVGlist"]) > climo30yrs[c]["tavgPROP"]["e_max"][0]:
                        climo30yrs[c]["tavgPROP"]["e_max"][0] = mean(e[YYYY]["tempAVGlist"])
                        climo30yrs[c]["tavgPROP"]["e_max"][1] = []
                        climo30yrs[c]["tavgPROP"]["e_max"][1].append(YYYY)
                    if mean(e[YYYY]["tempAVGlist"]) == climo30yrs[c]["tavgPROP"]["e_min"][0]: climo30yrs[c]["tavgPROP"]["e_min"][1].append(YYYY)
                    elif mean(e[YYYY]["tempAVGlist"]) < climo30yrs[c]["tavgPROP"]["e_min"][0]:
                        climo30yrs[c]["tavgPROP"]["e_min"][0] = mean(e[YYYY]["tempAVGlist"])
                        climo30yrs[c]["tavgPROP"]["e_min"][1] = []
                        climo30yrs[c]["tavgPROP"]["e_min"][1].append(YYYY)
        # TMAX
        for x in e[YYYY]["tmax"]: alltime["tmax"].append(x)
        if len(e[YYYY]["tmax"]) > EXCLD:
            if mean(e[YYYY]["tmax"]) == alltime["tmaxPROP"]["e_max"][0]: alltime["tmaxPROP"]["e_max"][1].append(YYYY)
            elif mean(e[YYYY]["tmax"]) > alltime["tmaxPROP"]["e_max"][0]:
                alltime["tmaxPROP"]["e_max"][0] = mean(e[YYYY]["tmax"])
                alltime["tmaxPROP"]["e_max"][1] = []
                alltime["tmaxPROP"]["e_max"][1].append(YYYY)
            if mean(e[YYYY]["tmax"]) == alltime["tmaxPROP"]["e_min"][0]: alltime["tmaxPROP"]["e_min"][1].append(YYYY)
            elif mean(e[YYYY]["tmax"]) < alltime["tmaxPROP"]["e_min"][0]:
                alltime["tmaxPROP"]["e_min"][0] = mean(e[YYYY]["tmax"])
                alltime["tmaxPROP"]["e_min"][1] = []
                alltime["tmaxPROP"]["e_min"][1].append(YYYY)
        for c in climo30yrs:
            if YYYY >= c[0] and YYYY <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                for x in e[YYYY]["tmax"]: climo30yrs[c]["tmax"].append(x)
                if len(e[YYYY]["tmax"]) > EXCLD:
                    if mean(e[YYYY]["tmax"]) == climo30yrs[c]["tmaxPROP"]["e_max"][0]: climo30yrs[c]["tmaxPROP"]["e_max"][1].append(YYYY)
                    elif mean(e[YYYY]["tmax"]) > climo30yrs[c]["tmaxPROP"]["e_max"][0]:
                        climo30yrs[c]["tmaxPROP"]["e_max"][0] = mean(e[YYYY]["tmax"])
                        climo30yrs[c]["tmaxPROP"]["e_max"][1] = []
                        climo30yrs[c]["tmaxPROP"]["e_max"][1].append(YYYY)
                    if mean(e[YYYY]["tmax"]) == climo30yrs[c]["tmaxPROP"]["e_min"][0]: climo30yrs[c]["tmaxPROP"]["e_min"][1].append(YYYY)
                    elif mean(e[YYYY]["tmax"]) < climo30yrs[c]["tmaxPROP"]["e_min"][0]:
                        climo30yrs[c]["tmaxPROP"]["e_min"][0] = mean(e[YYYY]["tmax"])
                        climo30yrs[c]["tmaxPROP"]["e_min"][1] = []
                        climo30yrs[c]["tmaxPROP"]["e_min"][1].append(YYYY)
        # TMIN
        for x in e[YYYY]["tmin"]: alltime["tmin"].append(x)
        if len(e[YYYY]["tmin"]) > EXCLD:
            if mean(e[YYYY]["tmin"]) == alltime["tminPROP"]["e_max"][0]: alltime["tminPROP"]["e_max"][1].append(YYYY)
            elif mean(e[YYYY]["tmin"]) > alltime["tminPROP"]["e_max"][0]:
                alltime["tminPROP"]["e_max"][0] = mean(e[YYYY]["tmin"])
                alltime["tminPROP"]["e_max"][1] = []
                alltime["tminPROP"]["e_max"][1].append(YYYY)
            if mean(e[YYYY]["tmin"]) == alltime["tminPROP"]["e_min"][0]: alltime["tminPROP"]["e_min"][1].append(YYYY)
            elif mean(e[YYYY]["tmin"]) < alltime["tminPROP"]["e_min"][0]:
                alltime["tminPROP"]["e_min"][0] = mean(e[YYYY]["tmin"])
                alltime["tminPROP"]["e_min"][1] = []
                alltime["tminPROP"]["e_min"][1].append(YYYY)
        for c in climo30yrs:
            if YYYY >= c[0] and YYYY <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                for x in e[YYYY]["tmin"]: climo30yrs[c]["tmin"].append(x)
                if len(e[YYYY]["tmin"]) > EXCLD:
                    if mean(e[YYYY]["tmin"]) == climo30yrs[c]["tminPROP"]["e_max"][0]: climo30yrs[c]["tminPROP"]["e_max"][1].append(YYYY)
                    elif mean(e[YYYY]["tmin"]) > climo30yrs[c]["tminPROP"]["e_max"][0]:
                        climo30yrs[c]["tminPROP"]["e_max"][0] = mean(e[YYYY]["tmin"])
                        climo30yrs[c]["tminPROP"]["e_max"][1] = []
                        climo30yrs[c]["tminPROP"]["e_max"][1].append(YYYY)
                    if mean(e[YYYY]["tmin"]) == climo30yrs[c]["tminPROP"]["e_min"][0]: climo30yrs[c]["tminPROP"]["e_min"][1].append(YYYY)
                    elif mean(e[YYYY]["tmin"]) < climo30yrs[c]["tminPROP"]["e_min"][0]:
                        climo30yrs[c]["tminPROP"]["e_min"][0] = mean(e[YYYY]["tmin"])
                        climo30yrs[c]["tminPROP"]["e_min"][1] = []
                        climo30yrs[c]["tminPROP"]["e_min"][1].append(YYYY)

    # PRINT REPORT
    print("---------------------------------------------------")
    print("Climatology Report for {} {} thru {} {}".format(calendar.month_abbr[startday.month],startday.day,calendar.month_abbr[endday.month],endday.day))
    print("City: {}, {}".format(clmt["station"],clmt["station_name"]))
    print("{}-{}; {}-Year Incremented {}-Year Climatologies".format(min(valid_yrs),max(valid_yrs),clmt_inc_rpt,clmt_len_rpt))
    print("---------------------------------------------------")
    print("Part 1: Precipitation Stats")
    print("{:▒^9} {:▒^12}  {:▒^9}  {:▒^9} {:▒^6} {:▒^12} {:▒^12} | {:▒^11}  {:▒^9} {:▒^6} {:▒^12} |".format("Years","PRCP","PRCP","PRCP","PRCP","PRCP","PRCP","SNOW","SNOW","SNOW","SNOW"))
    print("{:▒^9} {:▒^12}  {:▒^9}  {:▒^9} {:▒^6} {:▒^12} {:▒^12} | {:▒^11}  {:▒^9} {:▒^6} {:▒^12} |".format("","DAYS","DAYS MAX","DAYS MIN","AVG", "MAX","MIN","DAYS","DAYS MAX","AVG", "MAX"))
    #         Y     PD       PDx    PDn      PA      PM     Pmin      SD     SDx       SA      SM
    print("{:-^9} {:-^12}  {:-^9}  {:-^9} {:-^6} {:-^12} {:-^12} | {:-^11}  {:-^9} {:-^6} {:-^12} |".format("","","","","","","","","","",""))
    print("{:^9} {:5}:{:>5}%  {:>3}, {:^4}  {:>3}, {:^4} {:^6.2f} {:>5.2f}, {:^5} {:>5}, {:^5} | {:4}:{:>5}%  {:>3}, {:^4} {:^6.1f} {:>5.1f}, {:^5} |".format("All Time",
        alltime["prcpPROP"]["days"],
        round(100 * alltime["prcpPROP"]["days"] / alltime["total_days"],1),
        alltime["prcpPROP"]["e_max_days"][0],
        alltime["prcpPROP"]["e_max_days"][1][0] if len(alltime["prcpPROP"]["e_max_days"][1]) == 1 else len(alltime["prcpPROP"]["e_max_days"][1]),
        alltime["prcpPROP"]["e_min_days"][0],
        alltime["prcpPROP"]["e_min_days"][1][0] if len(alltime["prcpPROP"]["e_min_days"][1]) == 1 else len(alltime["prcpPROP"]["e_min_days"][1]),
        round(mean(alltime["prcp"]),2) if len(alltime["prcp"]) > 0 else "--",
        round(alltime["prcpPROP"]["e_max"][0],2),
        alltime["prcpPROP"]["e_max"][1][0] if len(alltime["prcpPROP"]["e_max"][1]) == 1 else len(alltime["prcpPROP"]["e_max"][1]),
        round(alltime["prcpPROP"]["e_min"][0],2),
        alltime["prcpPROP"]["e_min"][1][0] if len(alltime["prcpPROP"]["e_min"][1]) == 1 else len(alltime["prcpPROP"]["e_min"][1]),
        alltime["snowPROP"]["days"] if alltime["snowPROP"]["days"] > 0 else "--",
        round(100 * alltime["snowPROP"]["days"] / alltime["total_days"],1) if alltime["snowPROP"]["days"] > 0 else "--",
        alltime["snowPROP"]["e_max_days"][0],
        alltime["snowPROP"]["e_max_days"][1][0] if len(alltime["snowPROP"]["e_max_days"][1]) == 1 else len(alltime["snowPROP"]["e_max_days"][1]),
        round(mean(alltime["snow"]),1) if len(alltime["snow"]) > 0 else "--",
        round(alltime["snowPROP"]["e_max"][0],2),
        alltime["snowPROP"]["e_max"][1][0] if len(alltime["snowPROP"]["e_max"][1]) == 1 else len(alltime["snowPROP"]["e_max"][1])))
    for c in climo30yrs:
        try:
            print("{:^9} {:5}:{:>5}%  {:>3}, {:^4}  {:>3}, {:^4} {:^6.2f} {:>5.2f}, {:^5} {:>5}, {:^5} | {:4}:{:>5}%  {:>3}, {:^4} {:^6.1f} {:>5.1f}, {:^5} |".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
            climo30yrs[c]["prcpPROP"]["days"],
            round(100 * climo30yrs[c]["prcpPROP"]["days"] / climo30yrs[c]["total_days"],1),
            climo30yrs[c]["prcpPROP"]["e_max_days"][0],
            climo30yrs[c]["prcpPROP"]["e_max_days"][1][0] if len(climo30yrs[c]["prcpPROP"]["e_max_days"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["e_max_days"][1]),
            climo30yrs[c]["prcpPROP"]["e_min_days"][0],
            climo30yrs[c]["prcpPROP"]["e_min_days"][1][0] if len(climo30yrs[c]["prcpPROP"]["e_min_days"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["e_min_days"][1]),
            round(mean(climo30yrs[c]["prcp"]),2),
            round(climo30yrs[c]["prcpPROP"]["e_max"][0],2),
            climo30yrs[c]["prcpPROP"]["e_max"][1][0] if len(climo30yrs[c]["prcpPROP"]["e_max"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["e_max"][1]),
            round(climo30yrs[c]["prcpPROP"]["e_min"][0],2),
            climo30yrs[c]["prcpPROP"]["e_min"][1][0] if len(climo30yrs[c]["prcpPROP"]["e_min"][1]) == 1 else len(climo30yrs[c]["prcpPROP"]["e_min"][1]),
            climo30yrs[c]["snowPROP"]["days"] if climo30yrs[c]["snowPROP"]["days"] > 0 else "--",
            round(100 * climo30yrs[c]["snowPROP"]["days"] / climo30yrs[c]["total_days"],1) if climo30yrs[c]["snowPROP"]["days"] > 0 else "--",
            climo30yrs[c]["snowPROP"]["e_max_days"][0],
            climo30yrs[c]["snowPROP"]["e_max_days"][1][0] if len(climo30yrs[c]["snowPROP"]["e_max_days"][1]) == 1 else len(climo30yrs[c]["snowPROP"]["e_max_days"][1]),
            round(mean(climo30yrs[c]["snow"]),1) if len(climo30yrs[c]["snow"]) > 0 else "--",
            round(climo30yrs[c]["snowPROP"]["e_max"][0],2),
            climo30yrs[c]["snowPROP"]["e_max"][1][0] if len(climo30yrs[c]["snowPROP"]["e_max"][1]) == 1 else len(climo30yrs[c]["snowPROP"]["e_max"][1])))
        except Exception as e:
            print("ERROR: Era = {}; Exception = {}".format(c,e))

    print("\nPart 2: Temperature Stats")
    print("{:▒^9} {:▒^37} | {:▒^37} | {:▒^37}".format("Years","AVG TEMP","TMAX","TMIN"))
    print("{:▒^9} {:▒<5} {:▒^5} {:▒^12} {:▒^12} | {:▒<5} {:▒^5} {:▒^12} {:▒^12} | {:▒<5} {:▒^5} {:▒^12} {:▒^12}".format("","STDEV","AVG","MAX","MIN","STDEV","AVG","MAX","MIN","STDEV","AVG","MAX","MIN"))
    #         Y    TSTDV   TMA     TMX    TMn      TSTDV   TMA     TMX    TMn      TSTDV   TMA     TMX    TMn    
    # "tempAVGlist": [],"tavgPROP":{"e_max":[-999,[]],"e_min":[999,[]]},
    print("{:-^9} {:-^5} {:-^5} {:-^12} {:-^12} | {:-^5} {:-^5} {:-^12} {:-^12} | {:-^5} {:-^5} {:-^12} {:-^12}".format("","","","","","","","","","","","",""))
    print("{:^9} {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5}".format("All Time",
        round(pstdev(alltime["tempAVGlist"]),1),
        round(mean(alltime["tempAVGlist_ind"]),1),
        round(alltime["tavgPROP"]["e_max"][0],1),
        alltime["tavgPROP"]["e_max"][1][0] if len(alltime["tavgPROP"]["e_max"][1]) == 1 else len(alltime["tavgPROP"]["e_max"][1]),
        round(alltime["tavgPROP"]["e_min"][0],1),
        alltime["tavgPROP"]["e_min"][1][0] if len(alltime["tavgPROP"]["e_min"][1]) == 1 else len(alltime["tavgPROP"]["e_min"][1]),
        round(pstdev(alltime["tmax"]),1),
        round(mean(alltime["tmax"]),1),
        round(alltime["tmaxPROP"]["e_max"][0],1),
        alltime["tmaxPROP"]["e_max"][1][0] if len(alltime["tmaxPROP"]["e_max"][1]) == 1 else len(alltime["tmaxPROP"]["e_max"][1]),
        round(alltime["tmaxPROP"]["e_min"][0],1),
        alltime["tmaxPROP"]["e_min"][1][0] if len(alltime["tmaxPROP"]["e_min"][1]) == 1 else len(alltime["tmaxPROP"]["e_min"][1]),
        round(pstdev(alltime["tmin"]),1),
        round(mean(alltime["tmin"]),1),
        round(alltime["tminPROP"]["e_max"][0],1),
        alltime["tminPROP"]["e_max"][1][0] if len(alltime["tminPROP"]["e_max"][1]) == 1 else len(alltime["tminPROP"]["e_max"][1]),
        round(alltime["tminPROP"]["e_min"][0],1),
        alltime["tminPROP"]["e_min"][1][0] if len(alltime["tminPROP"]["e_min"][1]) == 1 else len(alltime["tminPROP"]["e_min"][1])))
    for c in climo30yrs:
        try:
            print("{:^9} {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5} | {:^5.1f} {:^5.1f} {:>5.1f}, {:^5} {:>5.1f}, {:^5}".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
                round(pstdev(climo30yrs[c]["tempAVGlist"]),1),
                round(mean(climo30yrs[c]["tempAVGlist_ind"]),1),
                round(climo30yrs[c]["tavgPROP"]["e_max"][0],1),
                climo30yrs[c]["tavgPROP"]["e_max"][1][0] if len(climo30yrs[c]["tavgPROP"]["e_max"][1]) == 1 else len(climo30yrs[c]["tavgPROP"]["e_max"][1]),
                round(climo30yrs[c]["tavgPROP"]["e_min"][0],1),
                climo30yrs[c]["tavgPROP"]["e_min"][1][0] if len(climo30yrs[c]["tavgPROP"]["e_min"][1]) == 1 else len(climo30yrs[c]["tavgPROP"]["e_min"][1]),
                round(pstdev(climo30yrs[c]["tmax"]),1),
                round(mean(climo30yrs[c]["tmax"]),1),
                round(climo30yrs[c]["tmaxPROP"]["e_max"][0],1),
                climo30yrs[c]["tmaxPROP"]["e_max"][1][0] if len(climo30yrs[c]["tmaxPROP"]["e_max"][1]) == 1 else len(climo30yrs[c]["tmaxPROP"]["e_max"][1]),
                round(climo30yrs[c]["tmaxPROP"]["e_min"][0],1),
                climo30yrs[c]["tmaxPROP"]["e_min"][1][0] if len(climo30yrs[c]["tmaxPROP"]["e_min"][1]) == 1 else len(climo30yrs[c]["tmaxPROP"]["e_min"][1]),
                round(pstdev(climo30yrs[c]["tmin"]),1),
                round(mean(climo30yrs[c]["tmin"]),1),
                round(climo30yrs[c]["tminPROP"]["e_max"][0],1),
                climo30yrs[c]["tminPROP"]["e_max"][1][0] if len(climo30yrs[c]["tminPROP"]["e_max"][1]) == 1 else len(climo30yrs[c]["tminPROP"]["e_max"][1]),
                round(climo30yrs[c]["tminPROP"]["e_min"][0],1),
                climo30yrs[c]["tminPROP"]["e_min"][1][0] if len(climo30yrs[c]["tminPROP"]["e_min"][1]) == 1 else len(climo30yrs[c]["tminPROP"]["e_min"][1])))
        except Exception as er:
            print("ERROR: Era = {}; Exception = {}".format(c,er))
    print("")

    if "output" in output and output["output"] == True:
        newfn = "customReport_{}{}to{}{}_".format(calendar.month_abbr[m1],d1,calendar.month_abbr[m2],d2) + str(clmt_len_rpt) + "YRclimo_" + str(clmt_inc_rpt) + "YRincr_" + clmt["station_name"] + ".csv"
        with open(newfn,"w") as w:
            headers = ["Assessed Period ({}{} to {}{})".format(calendar.month_abbr[m1],d1,calendar.month_abbr[m2],d2),"PRCP Days","PRCP % of days","PRCP stdev","PRCP AVG","SNOW Days","SNOW % of days","SNOW stdev","SNOW AVG","TAVG stdev","TAVG","TMAX stdev","TMAX","TMIN stdev","TMIN"]
            # HEADER
            for x in range(len(headers)):
                if x != len(headers) - 1: w.write(headers[x]); w.write(",")
                else: w.write(headers[x]); w.write("\n")
            w.write("{}-{}".format(alltime["years"][0],alltime["years"][1])); w.write(",")
            w.write("{}".format(alltime["prcpPROP"]["days"])); w.write(",")
            w.write("{:.1f}".format(round(100 * alltime["prcpPROP"]["days"] / alltime["total_days"],1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["prcp"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["prcp"]),1))); w.write(",")
            w.write("{}".format(alltime["snowPROP"]["days"])); w.write(",")
            w.write("{:.1f}".format(round(100 * alltime["snowPROP"]["days"] / alltime["total_days"],1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["snow"]),1))); w.write(",")
            w.write("{:.1f}".format(round(mean(alltime["snow"]),1))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tempAVGlist"]),1))); w.write(",")
            w.write("{:.2f}".format(mean(alltime["tempAVGlist_ind"]))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tmax"]),1))); w.write(",")
            w.write("{:.2f}".format(mean(alltime["tmax"]))); w.write(",")
            w.write("{:.1f}".format(round(pstdev(alltime["tmin"]),1))); w.write(",")
            w.write("{:.2f}".format(mean(alltime["tmin"]))); w.write("\n")
            for x in climo30yrs:
                w.write("{}-{}".format(climo30yrs[x]["years"][0],climo30yrs[x]["years"][1])); w.write(",")
                w.write("{}".format(climo30yrs[x]["prcpPROP"]["days"])); w.write(",")
                w.write("{:.1f}".format(round(100 * climo30yrs[x]["prcpPROP"]["days"] / climo30yrs[x]["total_days"],1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["prcp"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["prcp"]),1))); w.write(",")
                w.write("{}".format(climo30yrs[x]["snowPROP"]["days"])); w.write(",")
                w.write("{:.1f}".format(round(100 * climo30yrs[x]["snowPROP"]["days"] / climo30yrs[x]["total_days"],1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["snow"]),1))); w.write(",")
                w.write("{:.1f}".format(round(mean(climo30yrs[x]["snow"]),1))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tempAVGlist"]),1))); w.write(",")
                w.write("{:.2f}".format(mean(climo30yrs[x]["tempAVGlist_ind"]))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tmax"]),1))); w.write(",")
                w.write("{:.2f}".format(mean(climo30yrs[x]["tmax"]))); w.write(",")
                w.write("{:.1f}".format(round(pstdev(climo30yrs[x]["tmin"]),1))); w.write(",")
                w.write("{:.2f}".format(mean(climo30yrs[x]["tmin"]))); w.write("\n")
            print("*** csv output successful ***")

def dayRank(m,d,qty):
    """Returns a list of rankings (maxs and mins) based on a specific day of a
    specific month. It only accepts arguments for the month, day, and the how
    many rankings you want to list (ie, top 10; 15; etc). Passed arguments
    MUST be integers.
    
    dayRank(month,day,quantity)
    
    EXAMPLE: dayRank(6,27) -> Returns rankings for June 27
    """
    class day_attr:
        def __init__(self,y,number):
            self.year = y
            self.number = number

    if type(m) != int or type(d) != int or type(qty) != int: return print("* SORRY! Month AND Day need to be submitted as integers")
    if m < 1 or m > 12: return print("* Sorry! Make sure month entry is in the range [1,12]")
    if d < 1 or d > 31: return print("* Sorry! Invalid Day entered.")
    if m in [4,6,9,11] and d == 31: return print("*Sorry! Only months numbered 1,3,5,7,8,10,12 have 31 days")
    if m == 2 and d > 29: return print("* Sorry! February never has 30+ days")
    if type(qty) != int or qty > 50 or qty < 5: return print("* SORRY! Ensure desired quantity is an integer in the range [5,50]")

    DAYS_prcp = []
    DAYS_snow = []
    DAYS_snwd = []
    DAYS_tmax = []
    DAYS_tmin = []
    DAYS_tavg = []

    # YEARS.append(year_attr(y,round(mean(clmt[y][attribute]),1)))
    
    DAYS_prcp = [day_attr(D.year,V) for V in clmt_vars_days["prcp"] for D in clmt_vars_days["prcp"][V] if D.month == m and D.day == d]
    DAYS_snow = [day_attr(D.year,V) for V in clmt_vars_days["snow"] for D in clmt_vars_days["snow"][V] if D.month == m and D.day == d]
    DAYS_snwd = [day_attr(D.year,V) for V in clmt_vars_days["snwd"] for D in clmt_vars_days["snwd"][V] if D.month == m and D.day == d]
    DAYS_tmax = [day_attr(D.year,V) for V in clmt_vars_days["tmax"] for D in clmt_vars_days["tmax"][V] if D.month == m and D.day == d]
    DAYS_tmin = [day_attr(D.year,V) for V in clmt_vars_days["tmin"] for D in clmt_vars_days["tmin"][V] if D.month == m and D.day == d]
    DAYS_tavg = [day_attr(D.year,V) for V in clmt_vars_days["tavg"] for D in clmt_vars_days["tavg"][V] if D.month == m and D.day == d]
    
    DAYS_prcp.sort(key=lambda x:x.number,reverse=True)
    DAYS_snow.sort(key=lambda x:x.number,reverse=True)
    DAYS_snwd.sort(key=lambda x:x.number,reverse=True)
    DAYS_tmax_asc = DAYS_tmax.copy()
    DAYS_tmax.sort(key=lambda x:x.number,reverse=True)
    DAYS_tmax_asc.sort(key=lambda x:x.number)
    DAYS_tmin_asc = DAYS_tmin.copy()
    DAYS_tmin.sort(key=lambda x:x.number,reverse=True)
    DAYS_tmin_asc.sort(key=lambda x:x.number)
    DAYS_tavg_asc = DAYS_tavg.copy()
    DAYS_tavg.sort(key=lambda x:x.number,reverse=True)
    DAYS_tavg_asc.sort(key=lambda x:x.number)

    # This block will control if one of the above lists happen to have a length of zero; it's to avoid error
    if len(DAYS_prcp) == 0: DAYS_prcp = [day_attr(9999,0)]
    if len(DAYS_snow) == 0: DAYS_snow = [day_attr(9999,0)]
    if len(DAYS_snwd) == 0: DAYS_snwd = [day_attr(9999,0)]

    # 15|17|17|15|19|16
    # print("{:2}{} {:4}  {:3}  | {:2}{} {:4}  {:3}  | {:2}{} {:4}  {:3}  | {:2}{} {:4}  {:3}" TMAX and TMIN
    # print("  {:2}{} {:4}  {:5}  |  {:2}{} {:4}  {:4}"     PRCP and SNOW

    print("")
    print("{:^59}".format("Precipitation Records for {} {}".format(calendar.month_name[m],d)))
    print("{:^59}".format("{}, {}".format(clmt["station"],clmt["station_name"])))
    print("{:-^59}".format(""))
    print("{:^19}|{:^19}|{:^19}".format("Rain","Snow","Snow Depth"))
    print("{:-^19}|{:-^19}|{:-^19}".format("","",""))
    i = 0; j = 0; k = 0
    ranked_i = []; ranked_j = []; ranked_k = []
    for x in range(max(len(DAYS_prcp),len(DAYS_snow),len(DAYS_snwd))):
        if x == 0:
            i += 1; j += 1; k += 1
        else:
            try:
                if DAYS_prcp[x].number != DAYS_prcp[x-1].number: i += 1
                if DAYS_prcp[x].number == 0: i = qty + 1
            except: i = qty + 1
            try:
                if DAYS_snow[x].number != DAYS_snow[x-1].number: j += 1
                if DAYS_snow[x].number == 0: j = qty + 1
            except: j = qty + 1
            try:
                if DAYS_snwd[x].number != DAYS_snwd[x-1].number: k += 1
                if DAYS_snwd[x].number == 0: k = qty + 1
            except: k = qty + 1
        #print(i,j,k)
        if all(QTY > qty for QTY in [i,j,k]): break
        else:
            try:
                print("  {}  |  {}  |  {}  ".format(
                    "{:2}{} {:4}  {}".format(
                        i if i not in ranked_i and i <= qty and DAYS_prcp[x].number > 0 else "",
                        "." if i not in ranked_i and i <= qty and DAYS_prcp[x].number > 0 else " ",
                        DAYS_prcp[x].year if i <= qty and x <= len(DAYS_prcp)-1 and DAYS_prcp[x].number > 0 else "",
                        "{:5.2f}".format(DAYS_prcp[x].number) if i <= qty and x <= len(DAYS_prcp)-1 and DAYS_prcp[x].number > 0 else "     "
                    ),
                    "{:2}{} {:4}  {}".format(
                        j if j not in ranked_j and j <= qty and DAYS_snow[x].number > 0 else "",
                        "." if j not in ranked_j and j <= qty and DAYS_snow[x].number > 0 else " ",
                        DAYS_snow[x].year if j <= qty and x <= len(DAYS_snow)-1 and DAYS_snow[x].number > 0 else "",
                        "{:5.1f}".format(DAYS_snow[x].number) if j <= qty and x <= len(DAYS_snow)-1 and DAYS_snow[x].number > 0 else "     "
                    ),
                    "{:2}{} {:4}  {}".format(
                        k if k not in ranked_k and k <= qty and DAYS_snwd[x].number > 0 else "",
                        "." if k not in ranked_k and k <= qty and DAYS_snwd[x].number > 0 else " ",
                        DAYS_snwd[x].year if k <= qty and x <= len(DAYS_snwd)-1 and DAYS_snwd[x].number > 0 else "",
                        "{:5.1f}".format(DAYS_snwd[x].number) if k <= qty and x <= len(DAYS_snwd)-1 and DAYS_snwd[x].number > 0 else "     "
                    )
                ))
            except Exception as e:
                print(x,i,j,k)
                traceback.print_tb(e)
            if i not in ranked_i and i <= qty: ranked_i.append(i)
            if j not in ranked_j and j <= qty: ranked_j.append(j)
            if k not in ranked_k and k <= qty: ranked_k.append(k)

    print("\n{:^102}".format("Temperature Records for {} {}".format(calendar.month_name[m],d)))
    print("{:^102}".format("{}, {}".format(clmt["station"],clmt["station_name"])))
    print("{:-^102}".format(""))
    print("{:^34}|{:^33}|{:^33}".format("TAVG","TMAX","TMIN"))
    print("{:-^34}|{:-^33}|{:-^33}".format("","",""))
    print("{:^16}|{:^17}|{:^16}|{:^16}|{:^16}|{:^16}".format("Warmest","Coolest","Warmest","Coolest","Warmest","Coolest"))
    print("{:-^16}|{:-^17}|{:-^16}|{:-^16}|{:-^16}|{:-^16}".format("","","","","",""))
    i = 0; j = 0; k = 0; l = 0; m = 0; n = 0
    ranked_i = []; ranked_j = []; ranked_k = []; ranked_l = []; ranked_m = []; ranked_n = []
    for x in range(max(len(DAYS_tavg),len(DAYS_tmax),len(DAYS_tmin))):
        if x == 0:
            i += 1; j += 1; k += 1; l += 1; m += 1; n += 1
        else:
            try:
                if DAYS_tavg[x].number != DAYS_tavg[x-1].number: i += 1
            except: i = qty + 1
            try:
                if DAYS_tavg_asc[x].number != DAYS_tavg_asc[x-1].number: j += 1
            except: j = qty + 1
            try:
                if DAYS_tmax[x].number != DAYS_tmax[x-1].number: k += 1
            except: k = qty + 1
            try:
                if DAYS_tmax_asc[x].number != DAYS_tmax_asc[x-1].number: l += 1
            except: l = qty + 1
            try:
                if DAYS_tmin[x].number != DAYS_tmin[x-1].number: m += 1
            except: m = qty + 1
            try:
                if DAYS_tmin_asc[x].number != DAYS_tmin_asc[x-1].number: n += 1
            except: n = qty + 1

        if all(QTY > qty for QTY in [i,j,k,l,m,n]): break
        else:
            print("{} | {} | {} | {} | {} | {} ".format(
                "{:2}{} {:4}  {}".format(
                    i if i not in ranked_i and i <= qty else "",
                    "." if i not in ranked_i and i <= qty else " ",
                    DAYS_tavg[x].year if i <= qty else "",
                    "{:5.1f}".format(DAYS_tavg[x].number) if i <= qty else "     "
                ),
                "{:2}{} {:4}  {}".format(
                    j if j not in ranked_j and j <= qty else "",
                    "." if j not in ranked_j and j <= qty else " ",
                    DAYS_tavg_asc[x].year if j <= qty else "",
                    "{:5.1f}".format(DAYS_tavg_asc[x].number) if j <= qty else "     "
                ),
                "{:2}{} {:4}  {}".format(
                    k if k not in ranked_k and k <= qty else "",
                    "." if k not in ranked_k and k <= qty else " ",
                    DAYS_tmax[x].year if k <= qty else "",
                    "{:4}".format(DAYS_tmax[x].number) if k <= qty else "    "
                ),
                "{:2}{} {:4}  {}".format(
                    l if l not in ranked_l and l <= qty else "",
                    "." if l not in ranked_l and l <= qty else " ",
                    DAYS_tmax_asc[x].year if l <= qty else "",
                    "{:4}".format(DAYS_tmax_asc[x].number) if l <= qty else "    "
                ),
                "{:2}{} {:4}  {}".format(
                    m if m not in ranked_m and m <= qty else "",
                    "." if m not in ranked_m and m <= qty else " ",
                    DAYS_tmin[x].year if m <= qty else "",
                    "{:4}".format(DAYS_tmin[x].number) if m <= qty else "    "
                ),
                "{:2}{} {:4}  {}".format(
                    n if n not in ranked_n and n <= qty else "",
                    "." if n not in ranked_n and n <= qty else " ",
                    DAYS_tmin_asc[x].year if n <= qty else "",
                    "{:4}".format(DAYS_tmin_asc[x].number) if n <= qty else "    "
                )
            ))
            #print("---",i,j,k,l,m,n,"---")
            if i not in ranked_i and i <= qty: ranked_i.append(i)
            if j not in ranked_j and j <= qty: ranked_j.append(j)
            if k not in ranked_k and k <= qty: ranked_k.append(k)
            if l not in ranked_l and l <= qty: ranked_l.append(l)
            if m not in ranked_m and m <= qty: ranked_m.append(m)
            if n not in ranked_n and n <= qty: ranked_n.append(n)
    print("")

def weekRank(mo,d,qty):
    """Returns a list of rankings (maxs and mins) based on a specific week.
    The passed arguments of month and day will be the center of the week. It
    only accepts arguments for the month, day, and the how many rankings you
    want to list (ie, top 10; 15; etc). Passed arguments MUST be integers.
    
    weekRank(month,day,quantity)
    
    EXAMPLE: weekRank(1,30) -> Returns rankings for the week centered on
                               January 30 (from Jan 27 to Feb 2)
    """
    class week_attr:
        def __init__(self,y,number):
            self.year = y
            self.number = number
            
    if type(mo) != int or type(d) != int or type(qty) != int: return print("* SORRY! Month AND Day need to be submitted as integers")
    if mo < 1 or mo > 12: return print("* Sorry! Make sure month entry is in the range [1,12]")
    if d < 1 or d > 31: return print("* Sorry! Invalid Day entered.")
    if mo in [4,6,9,11] and d == 31: return print("*Sorry! Only months numbered 1,3,5,7,8,10,12 have 31 days")
    if mo == 2 and d > 29: return print("* Sorry! February never has 30+ days")
    if type(qty) != int or qty > 50 or qty < 5: return print("* SORRY! Ensure desired quantity is an integer in the range [5,50]")

    WEEKS_prcp = []
    WEEKS_snow = []
    WEEKS_snwd = []
    WEEKS_tavg = []
    WEEKS_tmax = []
    WEEKS_tmin = []
    if mo == 2 and d == 29: d = 28
    wkorig = datetime.date(1999,mo,d) - datetime.timedelta(days=3)
    for y in [YR for YR in clmt if type(YR) == int]:
        wkstart = datetime.date(y,mo,d) - datetime.timedelta(days=3)
        wklist = []
        wk_prcp = []
        wk_snow = []
        wk_snwd = []
        wk_tavg = []
        wk_tmax = []
        wk_tmin = []
        for DAY in range(7):
            wklist.append(wkstart)
            wkstart += datetime.timedelta(days=1)
        for DAY in wklist:
            #input(clmt[y][DAY.month][DAY.day].daystr)
            #if y == 1984:
                #print("HI TEMP: {}; DAY: {}".format(clmt[y][DAY.month][DAY.day].tmax,clmt[y][DAY.month][DAY.day].daystr))
            try:
                #print(clmt[y][DAY.month][DAY.day].prcpQ in ignoreflags)
                if clmt[DAY.year][DAY.month][DAY.day].prcpQ in ignoreflags:
                    wk_prcp.append(float(clmt[DAY.year][DAY.month][DAY.day].prcp))
            except:
                pass
            try:
                if clmt[DAY.year][DAY.month][DAY.day].snowQ in ignoreflags:
                    wk_snow.append(float(clmt[DAY.year][DAY.month][DAY.day].snow))
            except:
                pass
            try:
                if clmt[DAY.year][DAY.month][DAY.day].snwdQ in ignoreflags:
                    wk_snwd.append(float(clmt[DAY.year][DAY.month][DAY.day].snwd))
            except:
                pass
            try:
                if clmt[DAY.year][DAY.month][DAY.day].tmaxQ in ignoreflags and clmt[DAY.year][DAY.month][DAY.day].tmax not in ["9999","-9999",""] and clmt[DAY.year][DAY.month][DAY.day].tminQ in ignoreflags and clmt[DAY.year][DAY.month][DAY.day].tmin not in ["9999","-9999",""]:
                    wk_tavg.append(int(clmt[DAY.year][DAY.month][DAY.day].tmax))
                    wk_tavg.append(int(clmt[DAY.year][DAY.month][DAY.day].tmin))
            except:
                pass
            try:
                if clmt[DAY.year][DAY.month][DAY.day].tmaxQ in ignoreflags:
                    wk_tmax.append(int(clmt[DAY.year][DAY.month][DAY.day].tmax))
            except:
                pass
            try:
                if clmt[DAY.year][DAY.month][DAY.day].tminQ in ignoreflags:
                    wk_tmin.append(int(clmt[DAY.year][DAY.month][DAY.day].tmin))
            except:
                pass
        try:
            WEEKS_prcp.append(week_attr(y,round(sum(wk_prcp),2)))
        except:
            pass
        try:
            WEEKS_snow.append(week_attr(y,round(sum(wk_snow),1)))
        except:
            pass
        if len(wk_snwd) > 0:
            try:
                WEEKS_snwd.append(week_attr(y,round(sum(wk_snwd)/7,1)))
            except:
                pass
        if len(wk_tavg) > excludeweek_tavg:
            try:
                WEEKS_tavg.append(week_attr(y,round(mean(wk_tavg),1)))
            except:
                pass
        if len(wk_tmax) > excludeweek:
            try:
                WEEKS_tmax.append(week_attr(y,round(mean(wk_tmax),1)))
                #if y == 1984: print(round(mean(wk_tmax),1))
            except:
                pass
        if len(wk_tmin) > excludeweek:
            try:
                WEEKS_tmin.append(week_attr(y,round(mean(wk_tmin),1)))
            except:
                pass
    #print(len(WEEKS_tavg),len(WEEKS_tmax),len(WEEKS_tmin),len(WEEKS_prcp),len(WEEKS_snow))
    #input()
    WEEKS_prcp.sort(key=lambda x:x.number,reverse=True)
    WEEKS_snow.sort(key=lambda x:x.number,reverse=True)
    WEEKS_snwd.sort(key=lambda x:x.number,reverse=True)
    WEEKS_tavg_asc = WEEKS_tavg.copy()
    WEEKS_tavg.sort(key=lambda x:x.number,reverse=True)
    WEEKS_tavg_asc.sort(key=lambda x:x.number)
    WEEKS_tmax_asc = WEEKS_tmax.copy()
    WEEKS_tmax.sort(key=lambda x:x.number,reverse=True)
    WEEKS_tmax_asc.sort(key=lambda x:x.number)
    WEEKS_tmin_asc = WEEKS_tmin.copy()
    WEEKS_tmin.sort(key=lambda x:x.number,reverse=True)
    WEEKS_tmin_asc.sort(key=lambda x:x.number)

    #for x in WEEKS_tavg:
        #print(x.year,"-",x.number)
    #input()
    print("")
    print("{:^59}".format("Precipitation Records for the Week of {} {} - {} {}".format(calendar.month_abbr[wkorig.month],wkorig.day,
                                                                                  calendar.month_abbr[(wkorig + datetime.timedelta(days=6)).month],(wkorig + datetime.timedelta(days=6)).day)))
    print("{:^59}".format("{}, {}".format(clmt["station"],clmt["station_name"])))
    print("{:^59}".format("Weeks with >= {} Day(s) of Data".format(excludeweek+1)))
    print("{:-^59}".format(""))
    print("{:^19}|{:^19}|{:^19}".format("Rain","Snow","Avg Snow Depth"))
    print("{:-^19}|{:-^19}|{:-^19}".format("","",""))
    i = 0; j = 0; k = 0
    ranked_i = []; ranked_j = []; ranked_k = []
    for x in range(max(len(WEEKS_prcp),len(WEEKS_snow),len(WEEKS_snwd))):
        if x == 0:
            i += 1; j += 1; k += 1
        else:
            try:
                if WEEKS_prcp[x].number != WEEKS_prcp[x-1].number: i += 1
                if WEEKS_prcp[x].number == 0: i = qty + 1
            except: i = qty + 1
            try:
                if WEEKS_snow[x].number != WEEKS_snow[x-1].number: j += 1
                if WEEKS_snow[x].number == 0: j = qty + 1
            except: j = qty + 1
            try:
                if WEEKS_snwd[x].number != WEEKS_snwd[x-1].number: k += 1
                if WEEKS_snwd[x].number == 0: k = qty + 1
            except: k = qty + 1
        #print(i,j,k)
        if all(QTY > qty for QTY in [i,j,k]): break
        else:
            print("  {}  |  {}  |  {}  ".format(
                "{:2}{} {:4}  {}".format(
                    i if i not in ranked_i and i <= qty and x <= len(WEEKS_prcp)-1 and WEEKS_prcp[x].number > 0 else "",
                    "." if i not in ranked_i and i <= qty and x <= len(WEEKS_prcp)-1 and WEEKS_prcp[x].number > 0 else " ",
                    WEEKS_prcp[x].year if i <= qty and x <= len(WEEKS_prcp)-1 and WEEKS_prcp[x].number > 0 else "",
                    "{:5.2f}".format(WEEKS_prcp[x].number) if i <= qty and x <= len(WEEKS_prcp)-1 and WEEKS_prcp[x].number > 0 else "     "
                ),
                "{:2}{} {:4}  {}".format(
                    j if j not in ranked_j and j <= qty and x <= len(WEEKS_snow)-1 and WEEKS_snow[x].number > 0 else "",
                    "." if j not in ranked_j and j <= qty and x <= len(WEEKS_snow)-1 and WEEKS_snow[x].number > 0 else " ",
                    WEEKS_snow[x].year if j <= qty and x <= len(WEEKS_snow)-1 and WEEKS_snow[x].number > 0 else "",
                    "{:5.1f}".format(WEEKS_snow[x].number) if j <= qty and x <= len(WEEKS_snow)-1 and WEEKS_snow[x].number > 0 else "     "
                ),
                "{:2}{} {:4}  {}".format(
                    k if k not in ranked_k and k <= qty and x <= len(WEEKS_snwd)-1 and WEEKS_snwd[x].number > 0 else "",
                    "." if k not in ranked_k and k <= qty and x <= len(WEEKS_snwd)-1 and WEEKS_snwd[x].number > 0 else " ",
                    WEEKS_snwd[x].year if k <= qty and x <= len(WEEKS_snwd)-1 and WEEKS_snwd[x].number > 0 else "",
                    "{:5.1f}".format(WEEKS_snwd[x].number) if k <= qty and x <= len(WEEKS_snwd)-1 and WEEKS_snwd[x].number > 0 else "     "
                )
            ))
            if i not in ranked_i and i <= qty: ranked_i.append(i)
            if j not in ranked_j and j <= qty: ranked_j.append(j)
            if k not in ranked_k and k <= qty: ranked_k.append(k)

    print("\n{:^106}".format("Temperature Records for the Week of {} {} - {} {}".format(calendar.month_abbr[wkorig.month],wkorig.day,
                                                                                calendar.month_abbr[(wkorig + datetime.timedelta(days=6)).month],(wkorig + datetime.timedelta(days=6)).day)))
    print("{:^106}".format("{}, {}".format(clmt["station"],clmt["station_name"])))
    print("{:^106}".format("Weeks with >= {} Day(s) of Data".format(excludeweek+1)))
    print("{:-^106}".format(""))
    print("{:^34}|{:^35}|{:^35}".format("TAVG","TMAX","TMIN"))
    print("{:-^34}|{:-^35}|{:-^35}".format("","",""))
    print("{:^16}|{:^17}|{:^17}|{:^17}|{:^17}|{:^17}".format("Warmest","Coolest","Warmest","Coolest","Warmest","Coolest"))
    print("{:-^16}|{:-^17}|{:-^17}|{:-^17}|{:-^17}|{:-^17}".format("","","","","",""))
    i = 0; j = 0; k = 0; l = 0; m = 0; n = 0
    ranked_i = []; ranked_j = []; ranked_k = []; ranked_l = []; ranked_m = []; ranked_n = []
    for x in range(max(len(WEEKS_tavg),len(WEEKS_tmax),len(WEEKS_tmin))):
        if x == 0:
            i += 1; j += 1; k += 1; l += 1; m += 1; n += 1
        else:
            try:
                if WEEKS_tavg[x].number != WEEKS_tavg[x-1].number: i += 1
            except: i = qty + 1
            try:
                if WEEKS_tavg_asc[x].number != WEEKS_tavg_asc[x-1].number: j += 1
            except: j = qty + 1
            try:
                if WEEKS_tmax[x].number != WEEKS_tmax[x-1].number: k += 1
            except: k = qty + 1
            try:
                if WEEKS_tmax_asc[x].number != WEEKS_tmax_asc[x-1].number: l += 1
            except: l = qty + 1
            try:
                if WEEKS_tmin[x].number != WEEKS_tmin[x-1].number: m += 1
            except: m = qty + 1
            try:
                if WEEKS_tmin_asc[x].number != WEEKS_tmin_asc[x-1].number: n += 1
            except: n = qty + 1

        if all(QTY > qty for QTY in [i,j,k,l,m,n]): break
        else:
            print("{} | {} | {} | {} | {} | {} ".format(
                "{:2}{} {:4}  {}".format(
                    i if i not in ranked_i and i <= qty else "",
                    "." if i not in ranked_i and i <= qty else " ",
                    WEEKS_tavg[x].year if i <= qty else "",
                    "{:5.1f}".format(WEEKS_tavg[x].number) if i <= qty else "     "
                ),
                "{:2}{} {:4}  {}".format(
                    j if j not in ranked_j and j <= qty else "",
                    "." if j not in ranked_j and j <= qty else " ",
                    WEEKS_tavg_asc[x].year if j <= qty else "",
                    "{:5.1f}".format(WEEKS_tavg_asc[x].number) if j <= qty else "     "
                ),
                "{:2}{} {:4}  {}".format(
                    k if k not in ranked_k and k <= qty else "",
                    "." if k not in ranked_k and k <= qty else " ",
                    WEEKS_tmax[x].year if k <= qty else "",
                    "{:5.1f}".format(WEEKS_tmax[x].number) if k <= qty else "     "
                ),
                "{:2}{} {:4}  {}".format(
                    l if l not in ranked_l and l <= qty else "",
                    "." if l not in ranked_l and l <= qty else " ",
                    WEEKS_tmax_asc[x].year if l <= qty else "",
                    "{:5.1f}".format(WEEKS_tmax_asc[x].number) if l <= qty else "     "
                ),
                "{:2}{} {:4}  {}".format(
                    m if m not in ranked_m and m <= qty else "",
                    "." if m not in ranked_m and m <= qty else " ",
                    WEEKS_tmin[x].year if m <= qty else "",
                    "{:5.1f}".format(WEEKS_tmin[x].number) if m <= qty else "     "
                ),
                "{:2}{} {:4}  {}".format(
                    n if n not in ranked_n and n <= qty else "",
                    "." if n not in ranked_n and n <= qty else " ",
                    WEEKS_tmin_asc[x].year if n <= qty else "",
                    "{:5.1f}".format(WEEKS_tmin_asc[x].number) if n <= qty else "     "
                )
            ))
            #print("---",i,j,k,l,m,n,"---")
            if i not in ranked_i and i <= qty: ranked_i.append(i)
            if j not in ranked_j and j <= qty: ranked_j.append(j)
            if k not in ranked_k and k <= qty: ranked_k.append(k)
            if l not in ranked_l and l <= qty: ranked_l.append(l)
            if m not in ranked_m and m <= qty: ranked_m.append(m)
            if n not in ranked_n and n <= qty: ranked_n.append(n)
    print("")

def monthRank(mo,attribute,qty):
    """Returns a list of rankings (maxs and mins) based on a specific month.
    It only accepts arguments for the month, the kind of stats ("prcp" or
    "temps"), and how many rankings you want to list (ie, top 10; 15; etc).
    The attribute MUST be in string format, while the month and quantity MUST
    be integers.
    
    monthRank(month,attribute,quantity)
    
    EXAMPLE: monthRank(3,"rain",20) -> Returns the "Top 20" Precipitation
                                       Rankings for March
    """
    class month_attr:
        def __init__(self,y,mo,number):
            self.year = y
            self.month = mo
            self.number = number

    if type(mo) != int or mo < 1 or mo > 12: return print("* OOPS! {} is an invalid month. Ensure type(m) == int and is range [1,12]".format(mo))
    if attribute not in ["temp","temps","temperature","temperatures","tmax","tmin","tavg","prcp","precip","rain","snow"]:
        return print("* OOPS! Attribute must be 'temp' or 'prcp'. Try again!")
    if type(qty) != int or qty > 50 or qty < 5: return print("* SORRY! Ensure desired quantity is an integer in the range [5,50]")
    if attribute in ["prcp","precip","rain","snow"]: attribute = "prcp"
    if attribute in ["temp","temps","temperature","temperatures","tmax","tmin","tavg"]: attribute = "temp"
    
    MONTHS_prcp = []
    MONTHS_prcp_asc = []    # Declared here bc it will be compiled with in for-loop
    MONTHS_prcpDAYS = []
    MONTHS_prcpDAYS_asc = []    # Declared here bc it will be compiled with in for-loop
    MONTHS_snow = []
    MONTHS_snowDAYS = []
    MONTHS_tavg = []
    MONTHS_tmax = []
    MONTHS_tmin = []
    
    for y in [YR for YR in clmt if type(YR) == int]:
        try:
            MONTHS_prcp.append(month_attr(y,mo,round(sum(clmt[y][mo]["prcp"]),2)))
            MONTHS_prcpDAYS.append(month_attr(y,mo,clmt[y][mo]["prcpDAYS"]))
            if clmt[y][mo]["recordqty"] > excludemonth:
                MONTHS_prcp_asc.append(month_attr(y,mo,round(sum(clmt[y][mo]["prcp"]),2)))
                MONTHS_prcpDAYS_asc.append(month_attr(y,mo,clmt[y][mo]["prcpDAYS"]))
            MONTHS_snow.append(month_attr(y,mo,round(sum(clmt[y][mo]["snow"]),1)))
            MONTHS_snowDAYS.append(month_attr(y,mo,clmt[y][mo]["snowDAYS"]))
        except:
            pass
        try:
            if len(clmt[y][mo]["tempAVGlist"]) > excludemonth_tavg:
                MONTHS_tavg.append(month_attr(y,mo,round(mean(clmt[y][mo]["tempAVGlist"]),1)))
        except:
            pass
        try:
            if len(clmt[y][mo]["tmax"]) > excludemonth:
                MONTHS_tmax.append(month_attr(y,mo,round(mean(clmt[y][mo]["tmax"]),1)))
        except:
            pass
        try:
            if len(clmt[y][mo]["tmin"]) > excludemonth:
                MONTHS_tmin.append(month_attr(y,mo,round(mean(clmt[y][mo]["tmin"]),1)))
        except:
            pass

    #MONTHS_prcp_asc = MONTHS_prcp.copy()
    MONTHS_prcp.sort(key=lambda x:x.number,reverse=True)
    MONTHS_prcp_asc.sort(key=lambda x:x.number)
    #MONTHS_prcpDAYS_asc = MONTHS_prcpDAYS.copy()
    MONTHS_prcpDAYS.sort(key=lambda x:x.number,reverse=True)
    MONTHS_prcpDAYS_asc.sort(key=lambda x:x.number)
    MONTHS_snow.sort(key=lambda x:x.number,reverse=True)
    MONTHS_snowDAYS.sort(key=lambda x:x.number,reverse=True)
    MONTHS_tavg_asc = MONTHS_tavg.copy()
    MONTHS_tavg.sort(key=lambda x:x.number,reverse=True)
    MONTHS_tavg_asc.sort(key=lambda x:x.number)
    MONTHS_tmax_asc = MONTHS_tmax.copy()
    MONTHS_tmax.sort(key=lambda x:x.number,reverse=True)
    MONTHS_tmax_asc.sort(key=lambda x:x.number)
    MONTHS_tmin_asc = MONTHS_tmin.copy()
    MONTHS_tmin.sort(key=lambda x:x.number,reverse=True)
    MONTHS_tmin_asc.sort(key=lambda x:x.number)
    # print("{:67}|{:32}")
    # print("{:18}|{:18}|{:14}|{:14}|{:17}|{:14}")
    # print(" {:2}{} {:4}  {:6} | {:2}{} {:4}  {:6} | {:2}{} {:4}  {:2} | {:2}{} {:4}  {:2} | {:2}{} {:4}  {:5} | {:2}{} {:4}  {:2} "
    # print("  {:2}{} {:4}  {:2}  |  {:2}{} {:4}  {:2}  "
    print("")
    if attribute == "prcp":
        print("{:^100}".format("Ranked {} Monthly Precipitation Amounts and Days".format(calendar.month_name[mo])))
        print("{:^100}".format("{}, {}".format(clmt["station"],clmt["station_name"])))
        print("{:^100}".format("Months with >= {} Day(s) of Data".format(excludemonth+1)))
        print("{:-^100}".format(""))
        print("{:^67}|{:^32}".format("Rain","Snow"))
        print("{:-^67}|{:-^32}".format("",""))
        print("{:^18}|{:^18}|{:^14}|{:^14}|{:^17}|{:^14}".format("Wettest","Driest","Most Days","Least Days","Snowiest","Most Days"))
        print("{:-^18}|{:-^18}|{:-^14}|{:-^14}|{:-^17}|{:-^14}".format("","","","","",""))
        i = 1;j = 1;k = 1;l = 1;m = 1;n = 1
        ranked_i = [];ranked_j = [];ranked_k = [];ranked_l = [];ranked_m = [];ranked_n = []
        for x in range(min(len(MONTHS_prcp),len(MONTHS_prcp_asc),len(MONTHS_prcpDAYS_asc),len(MONTHS_prcpDAYS),len(MONTHS_snow),len(MONTHS_snowDAYS))):
            if x == 0:
                print(" {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:2} | {:2}{} {:4}  {:2} | {:2}{} {:4}  {:>5} | {:2}{} {:4}  {:>2} ".format(
                    1,".",MONTHS_prcp[x].year,"{:.2f}".format(MONTHS_prcp[x].number),
                    1,".",MONTHS_prcp_asc[x].year,"{:.2f}".format(MONTHS_prcp_asc[x].number),
                    1,".",MONTHS_prcpDAYS[x].year,MONTHS_prcpDAYS[x].number,
                    1,".",MONTHS_prcpDAYS_asc[x].year,MONTHS_prcpDAYS_asc[x].number,
                    1 if MONTHS_snow[x].number else "","." if MONTHS_snow[x].number > 0 else " ",
                    MONTHS_snow[x].year if MONTHS_snow[x].number > 0 else "","{:.1f}".format(MONTHS_snow[x].number) if MONTHS_snow[x].number > 0 else "",
                    1 if MONTHS_snowDAYS[x].number > 0 else "","." if MONTHS_snowDAYS[x].number > 0 else " ",
                    MONTHS_snowDAYS[x].year if MONTHS_snowDAYS[x].number > 0 else "",MONTHS_snowDAYS[x].number if MONTHS_snowDAYS[x].number > 0 else ""))
                ranked_i.append(i);ranked_j.append(j);ranked_k.append(k);ranked_l.append(l);ranked_m.append(m);ranked_n.append(n)
            else:
                if i not in ranked_i and i <= qty: ranked_i.append(i)
                if j not in ranked_j and j <= qty: ranked_j.append(j)
                if k not in ranked_k and k <= qty: ranked_k.append(k)
                if l not in ranked_l and l <= qty: ranked_l.append(l)
                if m not in ranked_m and m <= qty: ranked_m.append(m)
                if n not in ranked_n and n <= qty: ranked_n.append(n)
                if MONTHS_prcp[x].number != MONTHS_prcp[x-1].number: i += 1
                if MONTHS_prcp_asc[x].number != MONTHS_prcp_asc[x-1].number: j += 1
                if MONTHS_prcpDAYS[x].number != MONTHS_prcpDAYS[x-1].number: k += 1
                if MONTHS_prcpDAYS_asc[x].number != MONTHS_prcpDAYS_asc[x-1].number: l += 1
                if MONTHS_snow[x].number != MONTHS_snow[x-1].number: m += 1
                if MONTHS_snowDAYS[x].number != MONTHS_snowDAYS[x-1].number: n += 1
                if MONTHS_prcp[x].number == 0: i = qty + 1
                if MONTHS_prcpDAYS[x].number == 0: k = qty + 1
                if MONTHS_snow[x].number == 0: m = qty + 1
                if MONTHS_snowDAYS[x].number == 0: n = qty + 1
                if i <= qty or j <= qty or k <= qty or l <= qty or m <= qty or n <= qty:
                    print(" {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:2} | {:2}{} {:4}  {:2} | {:2}{} {:4}  {:>5} | {:2}{} {:4}  {:>2} ".format(
                        i if i not in ranked_i and i <= qty else "","." if i not in ranked_i and i <= qty else " ",
                        MONTHS_prcp[x].year if i <= qty else "","{:.2f}".format(MONTHS_prcp[x].number) if i <= qty else "",
                        j if j not in ranked_j and j <= qty else "","." if j not in ranked_j and j <= qty else " ",
                        MONTHS_prcp_asc[x].year if j <= qty else "","{:.2f}".format(MONTHS_prcp_asc[x].number) if j <= qty else "",
                        k if k not in ranked_k and k <= qty else "","." if k not in ranked_k and k <= qty else " ",
                        MONTHS_prcpDAYS[x].year if k <= qty else "",MONTHS_prcpDAYS[x].number if k <= qty else "",
                        l if l not in ranked_l and l <= qty else "","." if l not in ranked_l and l <= qty else " ",
                        MONTHS_prcpDAYS_asc[x].year if l <= qty else "",MONTHS_prcpDAYS_asc[x].number if l <= qty else "",
                        m if m not in ranked_m and m <= qty else "","." if m not in ranked_m and m <= qty else " ",
                        MONTHS_snow[x].year if m <= qty else "","{:.1f}".format(MONTHS_snow[x].number) if m <= qty else "",
                        n if n not in ranked_n and n <= qty else "","." if n not in ranked_n and n <= qty else " ",
                        MONTHS_snowDAYS[x].year if n <= qty else "",MONTHS_snowDAYS[x].number if n <= qty else ""))
            if i > qty and j > qty and k > qty and l > qty and m > qty and n > qty: break
    if attribute == "temp":
        print("{:^111}".format("Ranked {} Monthly Temperatures".format(calendar.month_name[mo])))
        print("{:^111}".format("{}, {}".format(clmt["station"],clmt["station_name"])))
        print("{:^111}".format("Months with >= {} Day(s) of Data".format(excludemonth+1)))
        print("{:-^111}".format(""))
        print("{:^36}|{:^37}|{:^36}".format("AVG TEMP","TMAX","TMIN"))
        print("{:-^36}|{:-^37}|{:-^36}".format("","",""))
        print("{:^17}|{:^18}|{:^18}|{:^18}|{:^18}|{:^17}".format("Warmest","Coolest","Warmest","Coolest","Warmest","Coolest"))
        print("{:-^17}|{:-^18}|{:-^18}|{:-^18}|{:-^18}|{:-^17}".format("","","","","",""))
        i = 1; j = 1; k = 1; l = 1; m = 1; n = 1
        ranked_i = []; ranked_j = []; ranked_k = []; ranked_l = []; ranked_m = []; ranked_n = []
        for x in range(len(MONTHS_tmax)):
            if x == 0:
                print("{:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}".format(
                                                                1,".",MONTHS_tavg[x].year,"{:.1f}".format(MONTHS_tavg[x].number),
                                                                1,".",MONTHS_tavg_asc[x].year,"{:.1f}".format(MONTHS_tavg_asc[x].number),
                                                                1,".",MONTHS_tmax[x].year,"{:.1f}".format(MONTHS_tmax[x].number),
                                                                1,".",MONTHS_tmax_asc[x].year,"{:.1f}".format(MONTHS_tmax_asc[x].number),
                                                                1,".",MONTHS_tmin[x].year,"{:.1f}".format(MONTHS_tmin[x].number),
                                                                1,".",MONTHS_tmin_asc[x].year,"{:.1f}".format(MONTHS_tmin_asc[x].number)))
                ranked_i.append(i); ranked_j.append(j); ranked_k.append(k); ranked_l.append(l); ranked_m.append(m); ranked_n.append(n)
            else:
                if i not in ranked_i and i <= qty: ranked_i.append(i)
                if j not in ranked_j and j <= qty: ranked_j.append(j)
                if k not in ranked_k and k <= qty: ranked_k.append(k)
                if l not in ranked_l and l <= qty: ranked_l.append(l)
                if m not in ranked_m and m <= qty: ranked_m.append(m)
                if n not in ranked_n and n <= qty: ranked_n.append(n)
                if MONTHS_tavg[x].number != MONTHS_tavg[x-1].number: i += 1
                if MONTHS_tavg_asc[x].number != MONTHS_tavg_asc[x-1].number: j += 1
                if MONTHS_tmax[x].number != MONTHS_tmax[x-1].number: k += 1
                if MONTHS_tmax_asc[x].number != MONTHS_tmax_asc[x-1].number: l += 1
                if MONTHS_tmin[x].number != MONTHS_tmin[x-1].number: m += 1
                if MONTHS_tmin_asc[x].number != MONTHS_tmin_asc[x-1].number: n += 1
                if i <= qty or j <= qty or k <= qty or l <= qty or m <= qty or n <= qty:
                    print("{:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}".format(
                            i if i not in ranked_i and i <= qty else "","." if i not in ranked_i and i <= qty else " ",
                            MONTHS_tavg[x].year if i <= qty else "","{:.1f}".format(MONTHS_tavg[x].number) if i <= qty else "",
                            j if j not in ranked_j and j <= qty else "","." if j not in ranked_j and j <= qty else " ",
                            MONTHS_tavg_asc[x].year if j <= qty else "","{:.1f}".format(MONTHS_tavg_asc[x].number) if j <= qty else "",
                            k if k not in ranked_k and k <= qty else "","." if k not in ranked_k and k <= qty else " ",
                            MONTHS_tmax[x].year if k <= qty else "","{:.1f}".format(MONTHS_tmax[x].number) if k <= qty else "",
                            l if l not in ranked_l and l <= qty else "","." if l not in ranked_l and l <= qty else " ",
                            MONTHS_tmax_asc[x].year if l <= qty else "","{:.1f}".format(MONTHS_tmax_asc[x].number) if l <= qty else "",
                            m if m not in ranked_m and m <= qty else "","." if m not in ranked_m and m <= qty else " ",
                            MONTHS_tmin[x].year if m <= qty else "","{:.1f}".format(MONTHS_tmin[x].number) if m <= qty else "",
                            n if n not in ranked_n and n <= qty else "","." if n not in ranked_n and n <= qty else " ",
                            MONTHS_tmin_asc[x].year if n <= qty else "","{:.1f}".format(MONTHS_tmin_asc[x].number) if n <= qty else ""))
            if i > qty and j > qty and k > qty and l > qty and m > qty and n > qty: break
    print("")

def yearRank(attribute,qty,**kwargs):
    """Returns a list of rankings (maxs and mins) for all years on record. It
    only accepts arguments for the kind of stats ("prcp" or "temps") desired,
    and how many rankings you want to list (ie, top 10; 15; etc). The
    attribute MUST be in string format, while the quantity MUST be an integer.
    
    yearRank(attribute,quantity)
   
    EXAMPLE: yearRank("temp",15) -> Returns the "Top 15" Temperature-based
                                    Rankings for all calendar years on record
    * The kwargs option is not available to the user. it is used internally
      by yearStats
    """
    class month_attr:
        def __init__(self,y,number):
            self.year = y
            self.number = number

    if attribute not in ["temp","temps","temperature","temperatures","tmax","tmin","tavg","prcp","precip","rain","snow"]:
        return print("* OOPS! Attribute must be 'temp' or 'prcp'. Try again!")
    if type(qty) != int or qty > 50 or qty < 5: return print("* SORRY! Ensure desired quantity is an integer in the range [5,50]")
    if attribute in ["prcp","precip","rain","snow"]: attribute = "prcp"
    if attribute in ["temp","temps","temperature","temperatures","tmax","tmin","tavg"]: attribute = "temp"
    
    YEARS_prcp = []
    YEARS_prcp_asc = []
    YEARS_prcpDAYS = []
    YEARS_prcpDAYS_asc = []
    YEARS_snow = []
    YEARS_snow_asc = []
    YEARS_snowDAYS = []
    YEARS_snowDAYS_asc = []
    YEARS_tavg = []
    YEARS_tmax = []
    YEARS_tmin = []
    
    for y in [YR for YR in clmt if type(YR) == int]:
        try:
            YEARS_prcp.append(month_attr(y,round(sum(clmt[y]["prcp"]),2)))
            YEARS_prcpDAYS.append(month_attr(y,clmt[y]["prcpDAYS"]))
            if clmt[y]["recordqty"] > excludeyear:
                YEARS_prcp_asc.append(month_attr(y,round(sum(clmt[y]["prcp"]),2)))
                YEARS_prcpDAYS_asc.append(month_attr(y,clmt[y]["prcpDAYS"]))
            YEARS_snow.append(month_attr(y,round(sum(clmt[y]["snow"]),1)))
            if clmt[y]["recordqty"] > excludeyear: YEARS_snow_asc.append(month_attr(y,round(sum(clmt[y]["snow"]),1)))
            YEARS_snowDAYS.append(month_attr(y,clmt[y]["snowDAYS"]))
            if clmt[y]["recordqty"] > excludeyear: YEARS_snowDAYS_asc.append(month_attr(y,clmt[y]["snowDAYS"]))
        except:
            pass
        try:
            if len(clmt[y]["tempAVGlist"]) > excludeyear_tavg:
                YEARS_tavg.append(month_attr(y,round(mean(clmt[y]["tempAVGlist"]),1)))
        except:
            pass
        try:
            if len(clmt[y]["tmax"]) > excludeyear:
                YEARS_tmax.append(month_attr(y,round(mean(clmt[y]["tmax"]),1)))
        except:
            pass
        try:
            if len(clmt[y]["tmin"]) > excludeyear:
                YEARS_tmin.append(month_attr(y,round(mean(clmt[y]["tmin"]),1)))
        except:
            pass

    #YEARS_prcp_asc = YEARS_prcp.copy()
    YEARS_prcp.sort(key=lambda x:x.number,reverse=True)
    YEARS_prcp_asc.sort(key=lambda x:x.number)
    #YEARS_prcpDAYS_asc = YEARS_prcpDAYS.copy()
    YEARS_prcpDAYS.sort(key=lambda x:x.number,reverse=True)
    YEARS_prcpDAYS_asc.sort(key=lambda x:x.number)
    YEARS_snow.sort(key=lambda x:x.number,reverse=True)
    YEARS_snow_asc.sort(key=lambda x:x.number)
    YEARS_snowDAYS.sort(key=lambda x:x.number,reverse=True)
    YEARS_snowDAYS_asc.sort(key=lambda x:x.number)
    YEARS_tavg_asc = YEARS_tavg.copy()
    YEARS_tavg.sort(key=lambda x:x.number,reverse=True)
    YEARS_tavg_asc.sort(key=lambda x:x.number)
    YEARS_tmax_asc = YEARS_tmax.copy()
    YEARS_tmax.sort(key=lambda x:x.number,reverse=True)
    YEARS_tmax_asc.sort(key=lambda x:x.number)
    YEARS_tmin_asc = YEARS_tmin.copy()
    YEARS_tmin.sort(key=lambda x:x.number,reverse=True)
    YEARS_tmin_asc.sort(key=lambda x:x.number)
    if "yearStatsRun" in kwargs and kwargs["yearStatsRun"] == True:
        prcpaschist = sorted(list(set([x.number for x in YEARS_prcp_asc])))
        prcpdeschist = sorted(list(set([x.number for x in YEARS_prcp])),reverse=True)
        prcpDAYSaschist = sorted(list(set([x.number for x in YEARS_prcpDAYS_asc])))
        prcpDAYSdeschist = sorted(list(set([x.number for x in YEARS_prcpDAYS])),reverse=True)
        snowaschist = sorted(list(set([x.number for x in YEARS_snow_asc])))
        snowdeschist = sorted(list(set([x.number for x in YEARS_snow])),reverse=True)
        snowDAYSaschist = sorted(list(set([x.number for x in YEARS_snowDAYS_asc])))
        snowDAYSdeschist = sorted(list(set([x.number for x in YEARS_snowDAYS])),reverse=True)
        tmaxaschist = sorted(list(set([x.number for x in YEARS_tmax_asc])))
        tmaxdeschist = sorted(list(set([x.number for x in YEARS_tmax])),reverse=True)
        tminaschist = sorted(list(set([x.number for x in YEARS_tmin_asc])))
        tmindeschist = sorted(list(set([x.number for x in YEARS_tmin])),reverse=True)
        tavgaschist = sorted(list(set([x.number for x in YEARS_tavg_asc])))
        tavgdeschist = sorted(list(set([x.number for x in YEARS_tavg])),reverse=True)
        return prcpaschist, prcpdeschist, prcpDAYSaschist, prcpDAYSdeschist, snowaschist, snowdeschist, snowDAYSaschist, snowDAYSdeschist, tmaxaschist, tmaxdeschist, tminaschist, tmindeschist, tavgaschist, tavgdeschist
    else:
        print("")
        if attribute == "prcp":
            print("{:^103}".format("Ranked Yearly Precipitation Amounts and Days"))
            print("{:^103}".format("{}, {}".format(clmt["station"],clmt["station_name"])))
            print("{:^103}".format("Years with >= {} day(s) of data".format(excludeyear+1)))
            print("{:-^103}".format(""))
            print("{:^69}|{:^33}".format("Rain","Snow"))
            print("{:-^69}|{:-^33}".format("",""))
            print("{:^18}|{:^18}|{:^15}|{:^15}|{:^17}|{:^15}".format("Wettest","Driest","Most Days","Least Days","Snowiest","Most Days"))
            print("{:-^18}|{:-^18}|{:-^15}|{:-^15}|{:-^17}|{:-^15}".format("","","","","",""))
            i = 1;j = 1;k = 1;l = 1;m = 1;n = 1
            ranked_i = [];ranked_j = [];ranked_k = [];ranked_l = [];ranked_m = [];ranked_n = []
            for x in range(min(len(YEARS_prcp),len(YEARS_prcp_asc),len(YEARS_prcpDAYS_asc),len(YEARS_prcpDAYS),len(YEARS_snow),len(YEARS_snowDAYS))):
                if x == 0:
                    print(" {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:>3} | {:2}{} {:4}  {:>3} | {:2}{} {:4}  {:>5} | {:2}{} {:4}  {:>3} ".format(
                        1,".",YEARS_prcp[x].year,"{:.2f}".format(YEARS_prcp[x].number),
                        1,".",YEARS_prcp_asc[x].year,"{:.2f}".format(YEARS_prcp_asc[x].number),
                        1,".",YEARS_prcpDAYS[x].year,YEARS_prcpDAYS[x].number,
                        1,".",YEARS_prcpDAYS_asc[x].year,YEARS_prcpDAYS_asc[x].number,
                        1 if YEARS_snow[x].number else "","." if YEARS_snow[x].number > 0 else " ",
                        YEARS_snow[x].year if YEARS_snow[x].number > 0 else "","{:.1f}".format(YEARS_snow[x].number) if YEARS_snow[x].number > 0 else "",
                        1 if YEARS_snowDAYS[x].number > 0 else "","." if YEARS_snowDAYS[x].number > 0 else " ",
                        YEARS_snowDAYS[x].year if YEARS_snowDAYS[x].number > 0 else "",YEARS_snowDAYS[x].number if YEARS_snowDAYS[x].number > 0 else ""))
                    ranked_i.append(i);ranked_j.append(j);ranked_k.append(k);ranked_l.append(l);ranked_m.append(m);ranked_n.append(n)
                else:
                    if i not in ranked_i and i <= qty: ranked_i.append(i)
                    if j not in ranked_j and j <= qty: ranked_j.append(j)
                    if k not in ranked_k and k <= qty: ranked_k.append(k)
                    if l not in ranked_l and l <= qty: ranked_l.append(l)
                    if m not in ranked_m and m <= qty: ranked_m.append(m)
                    if n not in ranked_n and n <= qty: ranked_n.append(n)
                    if YEARS_prcp[x].number != YEARS_prcp[x-1].number: i += 1
                    if YEARS_prcp_asc[x].number != YEARS_prcp_asc[x-1].number: j += 1
                    if YEARS_prcpDAYS[x].number != YEARS_prcpDAYS[x-1].number: k += 1
                    if YEARS_prcpDAYS_asc[x].number != YEARS_prcpDAYS_asc[x-1].number: l += 1
                    if YEARS_snow[x].number != YEARS_snow[x-1].number: m += 1
                    if YEARS_snowDAYS[x].number != YEARS_snowDAYS[x-1].number: n += 1
                    if YEARS_prcp[x].number == 0: i = qty + 1
                    if YEARS_prcpDAYS[x].number == 0: k = qty + 1
                    if YEARS_snow[x].number == 0: m = qty + 1
                    if YEARS_snowDAYS[x].number == 0: n = qty + 1
                    if i <= qty or j <= qty or k <= qty or l <= qty or m <= qty or n <= qty:
                        print(" {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:>3} | {:2}{} {:4}  {:>3} | {:2}{} {:4}  {:>5} | {:2}{} {:4}  {:>3} ".format(
                            i if i not in ranked_i and i <= qty else "","." if i not in ranked_i and i <= qty else " ",
                            YEARS_prcp[x].year if i <= qty else "","{:.2f}".format(YEARS_prcp[x].number) if i <= qty else "",
                            j if j not in ranked_j and j <= qty else "","." if j not in ranked_j and j <= qty else " ",
                            YEARS_prcp_asc[x].year if j <= qty else "","{:.2f}".format(YEARS_prcp_asc[x].number) if j <= qty else "",
                            k if k not in ranked_k and k <= qty else "","." if k not in ranked_k and k <= qty else " ",
                            YEARS_prcpDAYS[x].year if k <= qty else "",YEARS_prcpDAYS[x].number if k <= qty else "",
                            l if l not in ranked_l and l <= qty else "","." if l not in ranked_l and l <= qty else " ",
                            YEARS_prcpDAYS_asc[x].year if l <= qty else "",YEARS_prcpDAYS_asc[x].number if l <= qty else "",
                            m if m not in ranked_m and m <= qty else "","." if m not in ranked_m and m <= qty else " ",
                            YEARS_snow[x].year if m <= qty else "","{:.1f}".format(YEARS_snow[x].number) if m <= qty else "",
                            n if n not in ranked_n and n <= qty else "","." if n not in ranked_n and n <= qty else " ",
                            YEARS_snowDAYS[x].year if n <= qty else "",YEARS_snowDAYS[x].number if n <= qty else ""))
                if i > qty and j > qty and k > qty and l > qty and m > qty and n > qty: break
        if attribute == "temp":
            print("{:^111}".format("Ranked Yearly Temperatures"))
            print("{:^111}".format("{}, {}".format(clmt["station"],clmt["station_name"])))
            print("{:^111}".format("Years with >= {} day(s) of data".format(excludeyear+1)))
            print("{:-^111}".format(""))
            print("{:^36}|{:^37}|{:^36}".format("AVG TEMP","TMAX","TMIN"))
            print("{:-^36}|{:-^37}|{:-^36}".format("","",""))
            print("{:^17}|{:^18}|{:^18}|{:^18}|{:^18}|{:^17}".format("Warmest","Coolest","Warmest","Coolest","Warmest","Coolest"))
            print("{:-^17}|{:-^18}|{:-^18}|{:-^18}|{:-^18}|{:-^17}".format("","","","","",""))
            i = 1; j = 1; k = 1; l = 1; m = 1; n = 1
            ranked_i = []; ranked_j = []; ranked_k = []; ranked_l = []; ranked_m = []; ranked_n = []
            for x in range(len(YEARS_tmax)):
                if x == 0:
                    print("{:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}".format(
                                                                    1,".",YEARS_tavg[x].year,"{:.1f}".format(YEARS_tavg[x].number),
                                                                    1,".",YEARS_tavg_asc[x].year,"{:.1f}".format(YEARS_tavg_asc[x].number),
                                                                    1,".",YEARS_tmax[x].year,"{:.1f}".format(YEARS_tmax[x].number),
                                                                    1,".",YEARS_tmax_asc[x].year,"{:.1f}".format(YEARS_tmax_asc[x].number),
                                                                    1,".",YEARS_tmin[x].year,"{:.1f}".format(YEARS_tmin[x].number),
                                                                    1,".",YEARS_tmin_asc[x].year,"{:.1f}".format(YEARS_tmin_asc[x].number)))
                    ranked_i.append(i); ranked_j.append(j); ranked_k.append(k); ranked_l.append(l); ranked_m.append(m); ranked_n.append(n)
                else:
                    if i not in ranked_i and i <= qty: ranked_i.append(i)
                    if j not in ranked_j and j <= qty: ranked_j.append(j)
                    if k not in ranked_k and k <= qty: ranked_k.append(k)
                    if l not in ranked_l and l <= qty: ranked_l.append(l)
                    if m not in ranked_m and m <= qty: ranked_m.append(m)
                    if n not in ranked_n and n <= qty: ranked_n.append(n)
                    if YEARS_tavg[x].number != YEARS_tavg[x-1].number: i += 1
                    if YEARS_tavg_asc[x].number != YEARS_tavg_asc[x-1].number: j += 1
                    if YEARS_tmax[x].number != YEARS_tmax[x-1].number: k += 1
                    if YEARS_tmax_asc[x].number != YEARS_tmax_asc[x-1].number: l += 1
                    if YEARS_tmin[x].number != YEARS_tmin[x-1].number: m += 1
                    if YEARS_tmin_asc[x].number != YEARS_tmin_asc[x-1].number: n += 1
                    if i <= qty or j <= qty or k <= qty or l <= qty or m <= qty or n <= qty:
                        print("{:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}".format(
                                i if i not in ranked_i and i <= qty else "","." if i not in ranked_i and i <= qty else " ",
                                YEARS_tavg[x].year if i <= qty else "","{:.1f}".format(YEARS_tavg[x].number) if i <= qty else "",
                                j if j not in ranked_j and j <= qty else "","." if j not in ranked_j and j <= qty else " ",
                                YEARS_tavg_asc[x].year if j <= qty else "","{:.1f}".format(YEARS_tavg_asc[x].number) if j <= qty else "",
                                k if k not in ranked_k and k <= qty else "","." if k not in ranked_k and k <= qty else " ",
                                YEARS_tmax[x].year if k <= qty else "","{:.1f}".format(YEARS_tmax[x].number) if k <= qty else "",
                                l if l not in ranked_l and l <= qty else "","." if l not in ranked_l and l <= qty else " ",
                                YEARS_tmax_asc[x].year if l <= qty else "","{:.1f}".format(YEARS_tmax_asc[x].number) if l <= qty else "",
                                m if m not in ranked_m and m <= qty else "","." if m not in ranked_m and m <= qty else " ",
                                YEARS_tmin[x].year if m <= qty else "","{:.1f}".format(YEARS_tmin[x].number) if m <= qty else "",
                                n if n not in ranked_n and n <= qty else "","." if n not in ranked_n and n <= qty else " ",
                                YEARS_tmin_asc[x].year if n <= qty else "","{:.1f}".format(YEARS_tmin_asc[x].number) if n <= qty else ""))
                if i > qty and j > qty and k > qty and l > qty and m > qty and n > qty: break
        print("")

def seasonRank(season,attribute,qty,**kwargs):
    """Returns a list of rankings (maxs and mins) for all specified
    meteorological seasons on record. The season ("spring", "summer", "fall",
    "winter") and attribute ("prcp" or "temp") must be in string format. The
    quantity, denoting how many rankings you desire, must be an integer.
    
    seasonRank(season,attribute,quantity)
    
    EXAMPLE: seasonRank("Spring","temp",5) -> Returns the "Top 5" Temperature-
                                              based Rankings for all
                                              Meteorological Springs on record
    """
    class month_attr:
        def __init__(self,y,number):
            self.year = y
            self.number = number

    if attribute not in ["temp","temps","temperature","temperatures","tmax","tmin","tavg","prcp","precip","rain","snow"]:
        return print("* OOPS! Attribute must be 'temp' or 'prcp'. Try again!")
    if type(qty) != int or qty > 50 or qty < 5: return print("* SORRY! Ensure desired quantity is an integer in the range [5,50]")
    if attribute in ["prcp","precip","rain","snow"]: attribute = "prcp"
    if attribute in ["temp","temps","temperature","temperatures","tmax","tmin","tavg"]: attribute = "temp"
    
    SEASON_prcp = []
    SEASON_prcp_asc = []
    SEASON_prcpDAYS = []
    SEASON_prcpDAYS_asc = []
    SEASON_snow = []
    SEASON_snow_asc = []
    SEASON_snowDAYS = []
    SEASON_snowDAYS_asc = []
    SEASON_tavg = []
    SEASON_tmax = []
    SEASON_tmin = []
    
    for y in [YR for YR in metclmt if type(YR) == int]:
        try:
            SEASON_prcp.append(month_attr(y,round(sum(metclmt[y][season]["prcp"]),2)))
            SEASON_prcpDAYS.append(month_attr(y,metclmt[y][season]["prcpDAYS"]))
            if metclmt[y][season]["recordqty"] > excludeseason:
                SEASON_prcp_asc.append(month_attr(y,round(sum(metclmt[y][season]["prcp"]),2)))
                SEASON_prcpDAYS_asc.append(month_attr(y,metclmt[y][season]["prcpDAYS"]))
            SEASON_snow.append(month_attr(y,round(sum(metclmt[y][season]["snow"]),1)))
            if metclmt[y][season]["recordqty"] > excludeseason: SEASON_snow_asc.append(month_attr(y,round(sum(metclmt[y][season]["snow"]),1)))
            SEASON_snowDAYS.append(month_attr(y,metclmt[y][season]["snowDAYS"]))
            if metclmt[y][season]["recordqty"] > excludeseason: SEASON_snowDAYS_asc.append(month_attr(y,metclmt[y][season]["snowDAYS"]))
        except:
            pass
        try:
            if len(metclmt[y][season]["tempAVGlist"]) > excludeseason_tavg:
                SEASON_tavg.append(month_attr(y,round(mean(metclmt[y][season]["tempAVGlist"]),1)))
        except:
            pass
        try:
            if len(metclmt[y][season]["tmax"]) > excludeseason:
                SEASON_tmax.append(month_attr(y,round(mean(metclmt[y][season]["tmax"]),1)))
        except:
            pass
        try:
            if len(metclmt[y][season]["tmin"]) > excludeseason:
                SEASON_tmin.append(month_attr(y,round(mean(metclmt[y][season]["tmin"]),1)))
        except:
            pass

    #SEASON_prcp_asc = SEASON_prcp.copy()
    SEASON_prcp.sort(key=lambda x:x.number,reverse=True)
    SEASON_prcp_asc.sort(key=lambda x:x.number)
    #SEASON_prcpDAYS_asc = SEASON_prcpDAYS.copy()
    SEASON_prcpDAYS.sort(key=lambda x:x.number,reverse=True)
    SEASON_prcpDAYS_asc.sort(key=lambda x:x.number)
    SEASON_snow.sort(key=lambda x:x.number,reverse=True)
    SEASON_snow_asc.sort(key=lambda x:x.number)
    SEASON_snowDAYS.sort(key=lambda x:x.number,reverse=True)
    SEASON_snowDAYS_asc.sort(key=lambda x:x.number)
    SEASON_tavg_asc = SEASON_tavg.copy()
    SEASON_tavg.sort(key=lambda x:x.number,reverse=True)
    SEASON_tavg_asc.sort(key=lambda x:x.number)
    SEASON_tmax_asc = SEASON_tmax.copy()
    SEASON_tmax.sort(key=lambda x:x.number,reverse=True)
    SEASON_tmax_asc.sort(key=lambda x:x.number)
    SEASON_tmin_asc = SEASON_tmin.copy()
    SEASON_tmin.sort(key=lambda x:x.number,reverse=True)
    SEASON_tmin_asc.sort(key=lambda x:x.number)
    if "seasonStatsRun" in kwargs and kwargs["seasonStatsRun"] == True:
        prcpaschist = sorted(list(set([x.number for x in SEASON_prcp_asc])))
        prcpdeschist = sorted(list(set([x.number for x in SEASON_prcp])),reverse=True)
        prcpDAYSaschist = sorted(list(set([x.number for x in SEASON_prcpDAYS_asc])))
        prcpDAYSdeschist = sorted(list(set([x.number for x in SEASON_prcpDAYS])),reverse=True)
        snowaschist = sorted(list(set([x.number for x in SEASON_snow_asc])))
        snowdeschist = sorted(list(set([x.number for x in SEASON_snow])),reverse=True)
        snowDAYSaschist = sorted(list(set([x.number for x in SEASON_snowDAYS_asc])))
        snowDAYSdeschist = sorted(list(set([x.number for x in SEASON_snowDAYS])),reverse=True)
        tmaxaschist = sorted(list(set([x.number for x in SEASON_tmax_asc])))
        tmaxdeschist = sorted(list(set([x.number for x in SEASON_tmax])),reverse=True)
        tminaschist = sorted(list(set([x.number for x in SEASON_tmin_asc])))
        tmindeschist = sorted(list(set([x.number for x in SEASON_tmin])),reverse=True)
        tavgaschist = sorted(list(set([x.number for x in SEASON_tavg_asc])))
        tavgdeschist = sorted(list(set([x.number for x in SEASON_tavg])),reverse=True)
        return prcpaschist, prcpdeschist, prcpDAYSaschist, prcpDAYSdeschist, snowaschist, snowdeschist, snowDAYSaschist, snowDAYSdeschist, tmaxaschist, tmaxdeschist, tminaschist, tmindeschist, tavgaschist, tavgdeschist
    else:
        print("")
        if attribute == "prcp":
            print("{:^103}".format("Meteorological {} Ranked Precipitation Amounts and Days".format(season.capitalize())))
            print("{:^103}".format("{}, {}".format(metclmt["station"],metclmt["station_name"])))
            print("{:^103}".format("Seasons with >= {} day(s) of data".format(excludeseason+1)))
            print("{:-^103}".format(""))
            print("{:^69}|{:^33}".format("Rain","Snow"))
            print("{:-^69}|{:-^33}".format("",""))
            print("{:^18}|{:^18}|{:^15}|{:^15}|{:^17}|{:^15}".format("Wettest","Driest","Most Days","Least Days","Snowiest","Most Days"))
            print("{:-^18}|{:-^18}|{:-^15}|{:-^15}|{:-^17}|{:-^15}".format("","","","","",""))
            i = 1;j = 1;k = 1;l = 1;m = 1;n = 1
            ranked_i = [];ranked_j = [];ranked_k = [];ranked_l = [];ranked_m = [];ranked_n = []
            for x in range(min(len(SEASON_prcp),len(SEASON_prcp_asc),len(SEASON_prcpDAYS_asc),len(SEASON_prcpDAYS),len(SEASON_snow),len(SEASON_snowDAYS))):
                if x == 0:
                    print(" {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:>3} | {:2}{} {:4}  {:>3} | {:2}{} {:4}  {:>5} | {:2}{} {:4}  {:>3} ".format(
                        1,".",SEASON_prcp[x].year,"{:.2f}".format(SEASON_prcp[x].number),
                        1,".",SEASON_prcp_asc[x].year,"{:.2f}".format(SEASON_prcp_asc[x].number),
                        1,".",SEASON_prcpDAYS[x].year,SEASON_prcpDAYS[x].number,
                        1,".",SEASON_prcpDAYS_asc[x].year,SEASON_prcpDAYS_asc[x].number,
                        1 if SEASON_snow[x].number else "","." if SEASON_snow[x].number > 0 else " ",
                        SEASON_snow[x].year if SEASON_snow[x].number > 0 else "","{:.1f}".format(SEASON_snow[x].number) if SEASON_snow[x].number > 0 else "",
                        1 if SEASON_snowDAYS[x].number > 0 else "","." if SEASON_snowDAYS[x].number > 0 else " ",
                        SEASON_snowDAYS[x].year if SEASON_snowDAYS[x].number > 0 else "",SEASON_snowDAYS[x].number if SEASON_snowDAYS[x].number > 0 else ""))
                    ranked_i.append(i);ranked_j.append(j);ranked_k.append(k);ranked_l.append(l);ranked_m.append(m);ranked_n.append(n)
                else:
                    if i not in ranked_i and i <= qty: ranked_i.append(i)
                    if j not in ranked_j and j <= qty: ranked_j.append(j)
                    if k not in ranked_k and k <= qty: ranked_k.append(k)
                    if l not in ranked_l and l <= qty: ranked_l.append(l)
                    if m not in ranked_m and m <= qty: ranked_m.append(m)
                    if n not in ranked_n and n <= qty: ranked_n.append(n)
                    if SEASON_prcp[x].number != SEASON_prcp[x-1].number: i += 1
                    if SEASON_prcp_asc[x].number != SEASON_prcp_asc[x-1].number: j += 1
                    if SEASON_prcpDAYS[x].number != SEASON_prcpDAYS[x-1].number: k += 1
                    if SEASON_prcpDAYS_asc[x].number != SEASON_prcpDAYS_asc[x-1].number: l += 1
                    if SEASON_snow[x].number != SEASON_snow[x-1].number: m += 1
                    if SEASON_snowDAYS[x].number != SEASON_snowDAYS[x-1].number: n += 1
                    if SEASON_prcp[x].number == 0: i = qty + 1
                    if SEASON_prcpDAYS[x].number == 0: k = qty + 1
                    if SEASON_snow[x].number == 0: m = qty + 1
                    if SEASON_snowDAYS[x].number == 0: n = qty + 1
                    if i <= qty or j <= qty or k <= qty or l <= qty or m <= qty or n <= qty:
                        print(" {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:>3} | {:2}{} {:4}  {:>3} | {:2}{} {:4}  {:>5} | {:2}{} {:4}  {:>3} ".format(
                            i if i not in ranked_i and i <= qty else "","." if i not in ranked_i and i <= qty else " ",
                            SEASON_prcp[x].year if i <= qty else "","{:.2f}".format(SEASON_prcp[x].number) if i <= qty else "",
                            j if j not in ranked_j and j <= qty else "","." if j not in ranked_j and j <= qty else " ",
                            SEASON_prcp_asc[x].year if j <= qty else "","{:.2f}".format(SEASON_prcp_asc[x].number) if j <= qty else "",
                            k if k not in ranked_k and k <= qty else "","." if k not in ranked_k and k <= qty else " ",
                            SEASON_prcpDAYS[x].year if k <= qty else "",SEASON_prcpDAYS[x].number if k <= qty else "",
                            l if l not in ranked_l and l <= qty else "","." if l not in ranked_l and l <= qty else " ",
                            SEASON_prcpDAYS_asc[x].year if l <= qty else "",SEASON_prcpDAYS_asc[x].number if l <= qty else "",
                            m if m not in ranked_m and m <= qty else "","." if m not in ranked_m and m <= qty else " ",
                            SEASON_snow[x].year if m <= qty else "","{:.1f}".format(SEASON_snow[x].number) if m <= qty else "",
                            n if n not in ranked_n and n <= qty else "","." if n not in ranked_n and n <= qty else " ",
                            SEASON_snowDAYS[x].year if n <= qty else "",SEASON_snowDAYS[x].number if n <= qty else ""))
                if i > qty and j > qty and k > qty and l > qty and m > qty and n > qty: break
        if attribute == "temp":
            print("{:^111}".format("Meteorological {} Ranked Temperatures".format(season.capitalize())))
            print("{:^111}".format("{}, {}".format(metclmt["station"],metclmt["station_name"])))
            print("{:^111}".format("Seasons with >= {} day(s) of data".format(excludeseason+1)))
            print("{:-^111}".format(""))
            print("{:^36}|{:^37}|{:^36}".format("AVG TEMP","TMAX","TMIN"))
            print("{:-^36}|{:-^37}|{:-^36}".format("","",""))
            print("{:^17}|{:^18}|{:^18}|{:^18}|{:^18}|{:^17}".format("Warmest","Coolest","Warmest","Coolest","Warmest","Coolest"))
            print("{:-^17}|{:-^18}|{:-^18}|{:-^18}|{:-^18}|{:-^17}".format("","","","","",""))
            i = 1; j = 1; k = 1; l = 1; m = 1; n = 1
            ranked_i = []; ranked_j = []; ranked_k = []; ranked_l = []; ranked_m = []; ranked_n = []
            for x in range(len(SEASON_tmax)):
                if x == 0:
                    print("{:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}".format(
                                                                    1,".",SEASON_tavg[x].year,"{:.1f}".format(SEASON_tavg[x].number),
                                                                    1,".",SEASON_tavg_asc[x].year,"{:.1f}".format(SEASON_tavg_asc[x].number),
                                                                    1,".",SEASON_tmax[x].year,"{:.1f}".format(SEASON_tmax[x].number),
                                                                    1,".",SEASON_tmax_asc[x].year,"{:.1f}".format(SEASON_tmax_asc[x].number),
                                                                    1,".",SEASON_tmin[x].year,"{:.1f}".format(SEASON_tmin[x].number),
                                                                    1,".",SEASON_tmin_asc[x].year,"{:.1f}".format(SEASON_tmin_asc[x].number)))
                    ranked_i.append(i); ranked_j.append(j); ranked_k.append(k); ranked_l.append(l); ranked_m.append(m); ranked_n.append(n)
                else:
                    if i not in ranked_i and i <= qty: ranked_i.append(i)
                    if j not in ranked_j and j <= qty: ranked_j.append(j)
                    if k not in ranked_k and k <= qty: ranked_k.append(k)
                    if l not in ranked_l and l <= qty: ranked_l.append(l)
                    if m not in ranked_m and m <= qty: ranked_m.append(m)
                    if n not in ranked_n and n <= qty: ranked_n.append(n)
                    if SEASON_tavg[x].number != SEASON_tavg[x-1].number: i += 1
                    if SEASON_tavg_asc[x].number != SEASON_tavg_asc[x-1].number: j += 1
                    if SEASON_tmax[x].number != SEASON_tmax[x-1].number: k += 1
                    if SEASON_tmax_asc[x].number != SEASON_tmax_asc[x-1].number: l += 1
                    if SEASON_tmin[x].number != SEASON_tmin[x-1].number: m += 1
                    if SEASON_tmin_asc[x].number != SEASON_tmin_asc[x-1].number: n += 1
                    if i <= qty or j <= qty or k <= qty or l <= qty or m <= qty or n <= qty:
                        print("{:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}".format(
                                i if i not in ranked_i and i <= qty else "","." if i not in ranked_i and i <= qty else " ",
                                SEASON_tavg[x].year if i <= qty else "","{:.1f}".format(SEASON_tavg[x].number) if i <= qty else "",
                                j if j not in ranked_j and j <= qty else "","." if j not in ranked_j and j <= qty else " ",
                                SEASON_tavg_asc[x].year if j <= qty else "","{:.1f}".format(SEASON_tavg_asc[x].number) if j <= qty else "",
                                k if k not in ranked_k and k <= qty else "","." if k not in ranked_k and k <= qty else " ",
                                SEASON_tmax[x].year if k <= qty else "","{:.1f}".format(SEASON_tmax[x].number) if k <= qty else "",
                                l if l not in ranked_l and l <= qty else "","." if l not in ranked_l and l <= qty else " ",
                                SEASON_tmax_asc[x].year if l <= qty else "","{:.1f}".format(SEASON_tmax_asc[x].number) if l <= qty else "",
                                m if m not in ranked_m and m <= qty else "","." if m not in ranked_m and m <= qty else " ",
                                SEASON_tmin[x].year if m <= qty else "","{:.1f}".format(SEASON_tmin[x].number) if m <= qty else "",
                                n if n not in ranked_n and n <= qty else "","." if n not in ranked_n and n <= qty else " ",
                                SEASON_tmin_asc[x].year if n <= qty else "","{:.1f}".format(SEASON_tmin_asc[x].number) if n <= qty else ""))
                if i > qty and j > qty and k > qty and l > qty and m > qty and n > qty: break
        print("")

def metYearRank(attribute,qty,**kwargs):
    """Returns a list of rankings (maxs and mins) for all meteorological years
    (March to February) on record. The attribute ("prcp" or "temp") must be in
    string format. The quantity, denoting how many rankings you desire, must
    be an integer.
    
    metYearRank(attribute,quantity)
    
    EXAMPLE: metYearRank("rain",12) -> Returns the "Top 12" Precip-based
                                       Rankings for all Meteorological Years
                                       on record
    """
    class month_attr:
        def __init__(self,y,number):
            self.year = y
            self.number = number

    if attribute not in ["temp","temps","temperature","temperatures","tmax","tmin","tavg","prcp","precip","rain","snow"]:
        return print("* OOPS! Attribute must be 'temp' or 'prcp'. Try again!")
    if type(qty) != int or qty > 50 or qty < 5: return print("* SORRY! Ensure desired quantity is an integer in the range [5,50]")
    if attribute in ["prcp","precip","rain","snow"]: attribute = "prcp"
    if attribute in ["temp","temps","temperature","temperatures","tmax","tmin","tavg"]: attribute = "temp"
    
    YEARS_prcp = []
    YEARS_prcp_asc = []
    YEARS_prcpDAYS = []
    YEARS_prcpDAYS_asc = []
    YEARS_snow = []
    YEARS_snow_asc = []
    YEARS_snowDAYS = []
    YEARS_snowDAYS_asc = []
    YEARS_tavg = []
    YEARS_tmax = []
    YEARS_tmin = []
    
    for y in [YR for YR in clmt if type(YR) == int]:
        try:
            YEARS_prcp.append(month_attr(y,round(sum(metclmt[y]["prcp"]),2)))
            YEARS_prcpDAYS.append(month_attr(y,metclmt[y]["prcpDAYS"]))
            if metclmt[y]["recordqty"] > excludeyear:
                YEARS_prcp_asc.append(month_attr(y,round(sum(metclmt[y]["prcp"]),2)))
                YEARS_prcpDAYS_asc.append(month_attr(y,metclmt[y]["prcpDAYS"]))
            YEARS_snow.append(month_attr(y,round(sum(metclmt[y]["snow"]),1)))
            if metclmt[y]["recordqty"] > excludeyear: YEARS_snow_asc.append(month_attr(y,round(sum(metclmt[y]["snow"]),1)))
            YEARS_snowDAYS.append(month_attr(y,metclmt[y]["snowDAYS"]))
            if metclmt[y]["recordqty"] > excludeyear: YEARS_snowDAYS_asc.append(month_attr(y,metclmt[y]["snowDAYS"]))
        except:
            pass
        try:
            if len(metclmt[y]["tempAVGlist"]) > excludeyear_tavg:
                YEARS_tavg.append(month_attr(y,round(mean(metclmt[y]["tempAVGlist"]),1)))
        except:
            pass
        try:
            if len(metclmt[y]["tmax"]) > excludeyear:
                YEARS_tmax.append(month_attr(y,round(mean(metclmt[y]["tmax"]),1)))
        except:
            pass
        try:
            if len(metclmt[y]["tmin"]) > excludeyear:
                YEARS_tmin.append(month_attr(y,round(mean(metclmt[y]["tmin"]),1)))
        except:
            pass

    #YEARS_prcp_asc = YEARS_prcp.copy()
    YEARS_prcp.sort(key=lambda x:x.number,reverse=True)
    YEARS_prcp_asc.sort(key=lambda x:x.number)
    #YEARS_prcpDAYS_asc = YEARS_prcpDAYS.copy()
    YEARS_prcpDAYS.sort(key=lambda x:x.number,reverse=True)
    YEARS_prcpDAYS_asc.sort(key=lambda x:x.number)
    YEARS_snow.sort(key=lambda x:x.number,reverse=True)
    YEARS_snow_asc.sort(key=lambda x:x.number)
    YEARS_snowDAYS.sort(key=lambda x:x.number,reverse=True)
    YEARS_snowDAYS_asc.sort(key=lambda x:x.number)
    YEARS_tavg_asc = YEARS_tavg.copy()
    YEARS_tavg.sort(key=lambda x:x.number,reverse=True)
    YEARS_tavg_asc.sort(key=lambda x:x.number)
    YEARS_tmax_asc = YEARS_tmax.copy()
    YEARS_tmax.sort(key=lambda x:x.number,reverse=True)
    YEARS_tmax_asc.sort(key=lambda x:x.number)
    YEARS_tmin_asc = YEARS_tmin.copy()
    YEARS_tmin.sort(key=lambda x:x.number,reverse=True)
    YEARS_tmin_asc.sort(key=lambda x:x.number)
    if "yearStatsRun" in kwargs and kwargs["yearStatsRun"] == True:
        prcpaschist = sorted(list(set([x.number for x in YEARS_prcp_asc])))
        prcpdeschist = sorted(list(set([x.number for x in YEARS_prcp])),reverse=True)
        prcpDAYSaschist = sorted(list(set([x.number for x in YEARS_prcpDAYS_asc])))
        prcpDAYSdeschist = sorted(list(set([x.number for x in YEARS_prcpDAYS])),reverse=True)
        snowaschist = sorted(list(set([x.number for x in YEARS_snow_asc])))
        snowdeschist = sorted(list(set([x.number for x in YEARS_snow])),reverse=True)
        snowDAYSaschist = sorted(list(set([x.number for x in YEARS_snowDAYS_asc])))
        snowDAYSdeschist = sorted(list(set([x.number for x in YEARS_snowDAYS])),reverse=True)
        tmaxaschist = sorted(list(set([x.number for x in YEARS_tmax_asc])))
        tmaxdeschist = sorted(list(set([x.number for x in YEARS_tmax])),reverse=True)
        tminaschist = sorted(list(set([x.number for x in YEARS_tmin_asc])))
        tmindeschist = sorted(list(set([x.number for x in YEARS_tmin])),reverse=True)
        tavgaschist = sorted(list(set([x.number for x in YEARS_tavg_asc])))
        tavgdeschist = sorted(list(set([x.number for x in YEARS_tavg])),reverse=True)
        return prcpaschist, prcpdeschist, prcpDAYSaschist, prcpDAYSdeschist, snowaschist, snowdeschist, snowDAYSaschist, snowDAYSdeschist, tmaxaschist, tmaxdeschist, tminaschist, tmindeschist, tavgaschist, tavgdeschist
    else:
        print("")
        if attribute == "prcp":
            print("{:^103}".format("Meteorological Annual Ranked Precipitation Amounts and Days"))
            print("{:^103}".format("{}, {}".format(metclmt["station"],metclmt["station_name"])))
            print("{:^103}".format("Years with >= {} day(s) of data".format(excludeyear+1)))
            print("{:-^103}".format(""))
            print("{:^69}|{:^33}".format("Rain","Snow"))
            print("{:-^69}|{:-^33}".format("",""))
            print("{:^18}|{:^18}|{:^15}|{:^15}|{:^17}|{:^15}".format("Wettest","Driest","Most Days","Least Days","Snowiest","Most Days"))
            print("{:-^18}|{:-^18}|{:-^15}|{:-^15}|{:-^17}|{:-^15}".format("","","","","",""))
            i = 1;j = 1;k = 1;l = 1;m = 1;n = 1
            ranked_i = [];ranked_j = [];ranked_k = [];ranked_l = [];ranked_m = [];ranked_n = []
            for x in range(min(len(YEARS_prcp),len(YEARS_prcp_asc),len(YEARS_prcpDAYS_asc),len(YEARS_prcpDAYS),len(YEARS_snow),len(YEARS_snowDAYS))):
                if x == 0:
                    print(" {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:>3} | {:2}{} {:4}  {:>3} | {:2}{} {:4}  {:>5} | {:2}{} {:4}  {:>3} ".format(
                        1,".",YEARS_prcp[x].year,"{:.2f}".format(YEARS_prcp[x].number),
                        1,".",YEARS_prcp_asc[x].year,"{:.2f}".format(YEARS_prcp_asc[x].number),
                        1,".",YEARS_prcpDAYS[x].year,YEARS_prcpDAYS[x].number,
                        1,".",YEARS_prcpDAYS_asc[x].year,YEARS_prcpDAYS_asc[x].number,
                        1 if YEARS_snow[x].number else "","." if YEARS_snow[x].number > 0 else " ",
                        YEARS_snow[x].year if YEARS_snow[x].number > 0 else "","{:.1f}".format(YEARS_snow[x].number) if YEARS_snow[x].number > 0 else "",
                        1 if YEARS_snowDAYS[x].number > 0 else "","." if YEARS_snowDAYS[x].number > 0 else " ",
                        YEARS_snowDAYS[x].year if YEARS_snowDAYS[x].number > 0 else "",YEARS_snowDAYS[x].number if YEARS_snowDAYS[x].number > 0 else ""))
                    ranked_i.append(i);ranked_j.append(j);ranked_k.append(k);ranked_l.append(l);ranked_m.append(m);ranked_n.append(n)
                else:
                    if i not in ranked_i and i <= qty: ranked_i.append(i)
                    if j not in ranked_j and j <= qty: ranked_j.append(j)
                    if k not in ranked_k and k <= qty: ranked_k.append(k)
                    if l not in ranked_l and l <= qty: ranked_l.append(l)
                    if m not in ranked_m and m <= qty: ranked_m.append(m)
                    if n not in ranked_n and n <= qty: ranked_n.append(n)
                    if YEARS_prcp[x].number != YEARS_prcp[x-1].number: i += 1
                    if YEARS_prcp_asc[x].number != YEARS_prcp_asc[x-1].number: j += 1
                    if YEARS_prcpDAYS[x].number != YEARS_prcpDAYS[x-1].number: k += 1
                    if YEARS_prcpDAYS_asc[x].number != YEARS_prcpDAYS_asc[x-1].number: l += 1
                    if YEARS_snow[x].number != YEARS_snow[x-1].number: m += 1
                    if YEARS_snowDAYS[x].number != YEARS_snowDAYS[x-1].number: n += 1
                    if YEARS_prcp[x].number == 0: i = qty + 1
                    if YEARS_prcpDAYS[x].number == 0: k = qty + 1
                    if YEARS_snow[x].number == 0: m = qty + 1
                    if YEARS_snowDAYS[x].number == 0: n = qty + 1
                    if i <= qty or j <= qty or k <= qty or l <= qty or m <= qty or n <= qty:
                        print(" {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:>3} | {:2}{} {:4}  {:>3} | {:2}{} {:4}  {:>5} | {:2}{} {:4}  {:>3} ".format(
                            i if i not in ranked_i and i <= qty else "","." if i not in ranked_i and i <= qty else " ",
                            YEARS_prcp[x].year if i <= qty else "","{:.2f}".format(YEARS_prcp[x].number) if i <= qty else "",
                            j if j not in ranked_j and j <= qty else "","." if j not in ranked_j and j <= qty else " ",
                            YEARS_prcp_asc[x].year if j <= qty else "","{:.2f}".format(YEARS_prcp_asc[x].number) if j <= qty else "",
                            k if k not in ranked_k and k <= qty else "","." if k not in ranked_k and k <= qty else " ",
                            YEARS_prcpDAYS[x].year if k <= qty else "",YEARS_prcpDAYS[x].number if k <= qty else "",
                            l if l not in ranked_l and l <= qty else "","." if l not in ranked_l and l <= qty else " ",
                            YEARS_prcpDAYS_asc[x].year if l <= qty else "",YEARS_prcpDAYS_asc[x].number if l <= qty else "",
                            m if m not in ranked_m and m <= qty else "","." if m not in ranked_m and m <= qty else " ",
                            YEARS_snow[x].year if m <= qty else "","{:.1f}".format(YEARS_snow[x].number) if m <= qty else "",
                            n if n not in ranked_n and n <= qty else "","." if n not in ranked_n and n <= qty else " ",
                            YEARS_snowDAYS[x].year if n <= qty else "",YEARS_snowDAYS[x].number if n <= qty else ""))
                if i > qty and j > qty and k > qty and l > qty and m > qty and n > qty: break
        if attribute == "temp":
            print("{:^111}".format("Meteorological Annual Ranked Temperatures"))
            print("{:^111}".format("{}, {}".format(metclmt["station"],metclmt["station_name"])))
            print("{:^111}".format("Years with >= {} day(s) of data".format(excludeyear+1)))
            print("{:-^111}".format(""))
            print("{:^36}|{:^37}|{:^36}".format("AVG TEMP","TMAX","TMIN"))
            print("{:-^36}|{:-^37}|{:-^36}".format("","",""))
            print("{:^17}|{:^18}|{:^18}|{:^18}|{:^18}|{:^17}".format("Warmest","Coolest","Warmest","Coolest","Warmest","Coolest"))
            print("{:-^17}|{:-^18}|{:-^18}|{:-^18}|{:-^18}|{:-^17}".format("","","","","",""))
            i = 1; j = 1; k = 1; l = 1; m = 1; n = 1
            ranked_i = []; ranked_j = []; ranked_k = []; ranked_l = []; ranked_m = []; ranked_n = []
            for x in range(len(YEARS_tmax)):
                if x == 0:
                    print("{:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}".format(
                                                                    1,".",YEARS_tavg[x].year,"{:.1f}".format(YEARS_tavg[x].number),
                                                                    1,".",YEARS_tavg_asc[x].year,"{:.1f}".format(YEARS_tavg_asc[x].number),
                                                                    1,".",YEARS_tmax[x].year,"{:.1f}".format(YEARS_tmax[x].number),
                                                                    1,".",YEARS_tmax_asc[x].year,"{:.1f}".format(YEARS_tmax_asc[x].number),
                                                                    1,".",YEARS_tmin[x].year,"{:.1f}".format(YEARS_tmin[x].number),
                                                                    1,".",YEARS_tmin_asc[x].year,"{:.1f}".format(YEARS_tmin_asc[x].number)))
                    ranked_i.append(i); ranked_j.append(j); ranked_k.append(k); ranked_l.append(l); ranked_m.append(m); ranked_n.append(n)
                else:
                    if i not in ranked_i and i <= qty: ranked_i.append(i)
                    if j not in ranked_j and j <= qty: ranked_j.append(j)
                    if k not in ranked_k and k <= qty: ranked_k.append(k)
                    if l not in ranked_l and l <= qty: ranked_l.append(l)
                    if m not in ranked_m and m <= qty: ranked_m.append(m)
                    if n not in ranked_n and n <= qty: ranked_n.append(n)
                    if YEARS_tavg[x].number != YEARS_tavg[x-1].number: i += 1
                    if YEARS_tavg_asc[x].number != YEARS_tavg_asc[x-1].number: j += 1
                    if YEARS_tmax[x].number != YEARS_tmax[x-1].number: k += 1
                    if YEARS_tmax_asc[x].number != YEARS_tmax_asc[x-1].number: l += 1
                    if YEARS_tmin[x].number != YEARS_tmin[x-1].number: m += 1
                    if YEARS_tmin_asc[x].number != YEARS_tmin_asc[x-1].number: n += 1
                    if i <= qty or j <= qty or k <= qty or l <= qty or m <= qty or n <= qty:
                        print("{:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}".format(
                                i if i not in ranked_i and i <= qty else "","." if i not in ranked_i and i <= qty else " ",
                                YEARS_tavg[x].year if i <= qty else "","{:.1f}".format(YEARS_tavg[x].number) if i <= qty else "",
                                j if j not in ranked_j and j <= qty else "","." if j not in ranked_j and j <= qty else " ",
                                YEARS_tavg_asc[x].year if j <= qty else "","{:.1f}".format(YEARS_tavg_asc[x].number) if j <= qty else "",
                                k if k not in ranked_k and k <= qty else "","." if k not in ranked_k and k <= qty else " ",
                                YEARS_tmax[x].year if k <= qty else "","{:.1f}".format(YEARS_tmax[x].number) if k <= qty else "",
                                l if l not in ranked_l and l <= qty else "","." if l not in ranked_l and l <= qty else " ",
                                YEARS_tmax_asc[x].year if l <= qty else "","{:.1f}".format(YEARS_tmax_asc[x].number) if l <= qty else "",
                                m if m not in ranked_m and m <= qty else "","." if m not in ranked_m and m <= qty else " ",
                                YEARS_tmin[x].year if m <= qty else "","{:.1f}".format(YEARS_tmin[x].number) if m <= qty else "",
                                n if n not in ranked_n and n <= qty else "","." if n not in ranked_n and n <= qty else " ",
                                YEARS_tmin_asc[x].year if n <= qty else "","{:.1f}".format(YEARS_tmin_asc[x].number) if n <= qty else ""))
                if i > qty and j > qty and k > qty and l > qty and m > qty and n > qty: break
        print("")

def customRank(attribute,qty,m1,d1,*date2,**kwargs):
    """Returns a list of rankings (maxs and mins) for all specified custom
    period of time. Note that the order of the passed arguments are different
    with this function than similar ranking functions. The attribute ("prcp"
    or "temp") must be a string; the quantity (how many rankings you want), M1
    (month), and D1 (day), and the optional M2 and D2 must be integers. If M2
    and D2 are not given, 12-31 will be considered the final date of the 
    custom-period. The attribute ("prcp" or "temp") must be in string format.
    The quantity, denoting how many rankings you desire, must be an integer.
    If the end day given occurs before the start day in the calendar year, the
    end day of the following year will be used.
    
    customRank(attribute,quantity,M1,D1,*[M2,D2])

    OPT *args: M2,D2 --> These optional entries represent the ending month,
                         and day of the period
    
    EXAMPLE: customRank("temp",10,11,1) -> Returns the "Top 10" Temperature-
                                           based Rankings for the custom
                                           period of Nov 1 thru Dec 31.

    EXAMPLE: customRank("prcp",10,9,1,3,31) -> Returns the "Top 10"
                                               Temperature-based Rankings for
                                               the frame of Sept 1 thru Mar 31
    """
    class e_attr:
        def __init__(self,y,number):
            self.year = y
            self.number = number
    if len(clmt) == 0: return print("* OOPS! Run the clmtAnalyze function first.")
    valid_yrs = [x for x in clmt.keys() if type(x) == int]
    valid_yrs.sort()
    if any(type(x) != int for x in [m1,d1]): return print("*** OOPS! Ensure that only integers are entered ***")

    if len(date2) == 0: pass
    elif len(date2) != 2: return print("*** OOPS! For the 2nd (optional) date, ensure only a Month and Date are entered ***")
    elif any(type(x) != int for x in [date2[0],date2[1]]): return print("*** OOPS! Ensure that only integers are entered ***")

    if attribute not in ["temp","temps","temperature","temperatures","tmax","tmin","tavg","prcp","precip","rain","snow"]:
        return print("* OOPS! Attribute must be 'temp' or 'prcp'. Try again!")
    if type(qty) != int or qty > 50 or qty < 5: return print("* SORRY! Ensure desired quantity is an integer in the range [5,50]")
    if attribute in ["prcp","precip","rain","snow"]: attribute = "prcp"
    if attribute in ["temp","temps","temperature","temperatures","tmax","tmin","tavg"]: attribute = "temp"

    if len(date2) == 2:
        m2 = date2[0]
        d2 = date2[1]
    else:
        m2 = 12
        d2 = 31
    if m2 == m1:
        if d2 == d1: return print("*** OOPS! Ensure different dates! ***")
    if m1 == 2 and d1 == 29: d1 = 28
    if m2 == 2 and d2 == 29: d2 = 28
    # Determine total length of period (used for exclusion calculation)
    s = datetime.date(1900,m1,d1)
    test = datetime.date(1900,m2,d2)
    if test > s: e = test
    else: e = datetime.date(1901,m2,d2)
    timelength = (e - s).days + 1
    
    if timelength <= 5: EXCLD = timelength-1
    elif timelength == 6: EXCLD = 4
    elif timelength == 7: EXCLD = excludeweek
    elif timelength == 8: EXCLD = excludeweek
    elif timelength in [28,29,30,31]: EXCLD = excludemonth
    elif timelength >= 350: EXCLD = excludeyear
    else: EXCLD = round(excludecustom * timelength)

    e = {}  # Will hold the date-to-date (represented by a parent year) stats
    
    for YYYY in valid_yrs:
        startday = datetime.date(YYYY,m1,d1)
        incr_day = startday
        if m2 < m1: endday = datetime.date(YYYY+1,m2,d2)   # if end month is less, the results will bleed into the following year
        elif m2 == m1:  # Deals with if the months of the dates are exactly the same
            if d2 < d1: endday = datetime.date(YYYY+1,m2,d2)     # like above, if month is the same, but date is less, results will bleed into following year
            else: endday = datetime.date(YYYY,m2,d2)               # OTHERWISE, it is assumed the same year
        else: endday = datetime.date(YYYY,m2,d2)       # If month2 is > than month 1, the active year will be used
        
        if endday.year > max(valid_yrs): break

        #if YYYY not in e:
        e[YYYY] = {"recordqty":0,
                   "prcp":[],"prcpDAYS":0,"snow":[],"snowDAYS":0,
                   "tempAVGlist":[],"tmax":[],"tmin":[]}

        while incr_day <= endday:
            y = incr_day.year; m = incr_day.month; d = incr_day.day
            if y in clmt and m in clmt[y] and d in clmt[y][m]:
                e[YYYY]["recordqty"] += 1
                # PRCP
                if clmt[y][m][d].prcpQ in ignoreflags and clmt[y][m][d].prcp not in ["9999","-9999",""]:
                    if float(clmt[y][m][d].prcp) > 0: e[YYYY]["prcp"].append(round(float(clmt[y][m][d].prcp),2))
                    if float(clmt[y][m][d].prcp) > 0 or clmt[y][m][d].prcpM == "T": e[YYYY]["prcpDAYS"] += 1
                if clmt[y][m][d].prcpQ in ignoreflags and clmt[y][m][d].prcp == "" and clmt[y][m][d].prcpM == "T": e[YYYY]["prcpDAYS"] += 1
                # SNOW
                if clmt[y][m][d].snowQ in ignoreflags and clmt[y][m][d].snow not in ["9999","-9999",""]:
                    if float(clmt[y][m][d].snow) > 0: e[YYYY]["snow"].append(round(float(clmt[y][m][d].snow),2))
                    if float(clmt[y][m][d].snow) > 0 or clmt[y][m][d].snowM == "T": e[YYYY]["snowDAYS"] += 1
                if clmt[y][m][d].snowQ in ignoreflags and clmt[y][m][d].snow == "" and clmt[y][m][d].snowM == "T": e[YYYY]["snowDAYS"] += 1
                # TAVG
                if clmt[y][m][d].tmaxQ in ignoreflags and clmt[y][m][d].tmax not in ["9999","-9999",""] and clmt[y][m][d].tminQ in ignoreflags and clmt[y][m][d].tmin not in ["9999","-9999",""] and int(clmt[y][m][d].tmax) >= int(clmt[y][m][d].tmin):
                    e[YYYY]["tempAVGlist"].append(int(clmt[y][m][d].tmax))
                    e[YYYY]["tempAVGlist"].append(int(clmt[y][m][d].tmin))
                # TMAX
                if clmt[y][m][d].tmaxQ in ignoreflags and clmt[y][m][d].tmax not in ["9999","-9999",""]:
                    if clmt[y][m][d].tmin != "" and int(clmt[y][m][d].tmax) >= int(clmt[y][m][d].tmin):
                        e[YYYY]["tmax"].append(int(clmt[y][m][d].tmax))
                # TMIN
                if clmt[y][m][d].tminQ in ignoreflags and clmt[y][m][d].tmin not in ["9999","-9999",""]:
                    if clmt[y][m][d].tmax != "" and int(clmt[y][m][d].tmin) <= int(clmt[y][m][d].tmax):
                        e[YYYY]["tmin"].append(int(clmt[y][m][d].tmin))
            incr_day += datetime.timedelta(days=1)  # GO ON TO TEST NEXT DAY

    E_prcp = []
    E_prcp_asc = []
    E_prcpDAYS = []
    E_prcpDAYS_asc = []
    E_snow = []
    E_snow_asc = []
    E_snowDAYS = []
    E_snowDAYS_asc = []
    E_tavg = []
    E_tmax = []
    E_tmin = []

    for YYYY in e:
        try:
            E_prcp.append(e_attr(YYYY,round(sum(e[YYYY]["prcp"]),2)))
            E_prcpDAYS.append(e_attr(YYYY,e[YYYY]["prcpDAYS"]))
            if e[YYYY]["recordqty"] > EXCLD:
                E_prcp_asc.append(e_attr(YYYY,round(sum(e[YYYY]["prcp"]),2)))
                E_prcpDAYS_asc.append(e_attr(YYYY,e[YYYY]["prcpDAYS"]))
            E_snow.append(e_attr(YYYY,round(sum(e[YYYY]["snow"]),1)))
            if e[YYYY]["recordqty"] > EXCLD: E_snow_asc.append(e_attr(YYYY,round(sum(e[YYYY]["snow"]),1)))
            E_snowDAYS.append(e_attr(YYYY,e[YYYY]["snowDAYS"]))
            if e[YYYY]["recordqty"] > EXCLD: E_snowDAYS_asc.append(e_attr(YYYY,e[YYYY]["snowDAYS"]))
        except:
            pass
        try:
            if len(e[YYYY]["tempAVGlist"]) > EXCLD * 2:
                E_tavg.append(e_attr(YYYY,round(mean(e[YYYY]["tempAVGlist"]),1)))
        except:
            pass
        try:
            if len(e[YYYY]["tmax"]) > EXCLD:
                E_tmax.append(e_attr(YYYY,round(mean(e[YYYY]["tmax"]),1)))
        except:
            pass
        try:
            if len(e[YYYY]["tmin"]) > EXCLD:
                E_tmin.append(e_attr(YYYY,round(mean(e[YYYY]["tmin"]),1)))
        except:
            pass

    E_LENGTHS_OF_ALL = []
    #E_prcp_asc = E_prcp.copy()
    E_prcp.sort(key=lambda x:x.number,reverse=True); E_LENGTHS_OF_ALL.append(len(E_prcp))
    E_prcp_asc.sort(key=lambda x:x.number); E_LENGTHS_OF_ALL.append(len(E_prcp_asc))
    #E_prcpDAYS_asc = E_prcpDAYS.copy()
    E_prcpDAYS.sort(key=lambda x:x.number,reverse=True); E_LENGTHS_OF_ALL.append(len(E_prcpDAYS))
    E_prcpDAYS_asc.sort(key=lambda x:x.number); E_LENGTHS_OF_ALL.append(len(E_prcpDAYS_asc))
    E_snow.sort(key=lambda x:x.number,reverse=True); E_LENGTHS_OF_ALL.append(len(E_snow))
    E_snow_asc.sort(key=lambda x:x.number); E_LENGTHS_OF_ALL.append(len(E_snow_asc))
    E_snowDAYS.sort(key=lambda x:x.number,reverse=True); E_LENGTHS_OF_ALL.append(len(E_snowDAYS))
    E_snowDAYS_asc.sort(key=lambda x:x.number); E_LENGTHS_OF_ALL.append(len(E_snowDAYS_asc))
    E_tavg_asc = E_tavg.copy()
    E_tavg.sort(key=lambda x:x.number,reverse=True); E_LENGTHS_OF_ALL.append(len(E_tavg))
    E_tavg_asc.sort(key=lambda x:x.number); E_LENGTHS_OF_ALL.append(len(E_tavg_asc))
    E_tmax_asc = E_tmax.copy()
    E_tmax.sort(key=lambda x:x.number,reverse=True); E_LENGTHS_OF_ALL.append(len(E_tmax))
    E_tmax_asc.sort(key=lambda x:x.number); E_LENGTHS_OF_ALL.append(len(E_tmax_asc))
    E_tmin_asc = E_tmin.copy()
    E_tmin.sort(key=lambda x:x.number,reverse=True); E_LENGTHS_OF_ALL.append(len(E_tmin))
    E_tmin_asc.sort(key=lambda x:x.number); E_LENGTHS_OF_ALL.append(len(E_tmin_asc))
    if "customStatsRun" in kwargs and kwargs["customStatsRun"] == True:
        prcpaschist = sorted(list(set([x.number for x in E_prcp_asc])))
        prcpdeschist = sorted(list(set([x.number for x in E_prcp])),reverse=True)
        prcpDAYSaschist = sorted(list(set([x.number for x in E_prcpDAYS_asc])))
        prcpDAYSdeschist = sorted(list(set([x.number for x in E_prcpDAYS])),reverse=True)
        snowaschist = sorted(list(set([x.number for x in E_snow_asc])))
        snowdeschist = sorted(list(set([x.number for x in E_snow])),reverse=True)
        snowDAYSaschist = sorted(list(set([x.number for x in E_snowDAYS_asc])))
        snowDAYSdeschist = sorted(list(set([x.number for x in E_snowDAYS])),reverse=True)
        tmaxaschist = sorted(list(set([x.number for x in E_tmax_asc])))
        tmaxdeschist = sorted(list(set([x.number for x in E_tmax])),reverse=True)
        tminaschist = sorted(list(set([x.number for x in E_tmin_asc])))
        tmindeschist = sorted(list(set([x.number for x in E_tmin])),reverse=True)
        tavgaschist = sorted(list(set([x.number for x in E_tavg_asc])))
        tavgdeschist = sorted(list(set([x.number for x in E_tavg])),reverse=True)
        return prcpaschist, prcpdeschist, prcpDAYSaschist, prcpDAYSdeschist, snowaschist, snowdeschist, snowDAYSaschist, snowDAYSdeschist, tmaxaschist, tmaxdeschist, tminaschist, tmindeschist, tavgaschist, tavgdeschist    
    else:
        print("")
        if attribute == "prcp":
            print("{:^100}".format("Ranked Precipitation Amounts and Days for {} {} thru {} {}".format(calendar.month_abbr[startday.month],startday.day,calendar.month_abbr[endday.month],endday.day)))
            print("{:^103}".format("{}, {}".format(clmt["station"],clmt["station_name"])))
            if EXCLD <= 5: print("{:^103}".format("Periods with {} Total days of Data".format(EXCLD+1)))
            else: print("{:^103}".format("Periods with >= {} Day(s) of Data".format(EXCLD+1)))
            
            print("{:-^103}".format(""))
            print("{:^70} {:^33}".format("Rain","Snow"))
            print("{:-^70} {:-^33}".format("",""))
            print("{:^18}|{:^18}|{:^15}|{:^15}|{:^17}|{:^15}".format("Wettest","Driest","Most Days","Least Days","Snowiest","Most Days"))
            print("{:-^18}|{:-^18}|{:-^15}|{:-^15}|{:-^17}|{:-^15}".format("","","","","",""))
            i = 1;j = 1;k = 1;l = 1;m = 1;n = 1
            printed_j = 0; printed_l = 0
            ranked_i = [];ranked_j = [];ranked_k = [];ranked_l = [];ranked_m = [];ranked_n = []
            for x in range(min(E_LENGTHS_OF_ALL)):
                if x == 0:
                    print(" {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:3} | {:2}{} {:4}  {:3} | {:2}{} {:4}  {:>5} | {:2}{} {:4}  {:>3} ".format(
                        1,".",E_prcp[x].year,"{:.2f}".format(E_prcp[x].number),
                        1,".",E_prcp_asc[x].year,"{:.2f}".format(E_prcp_asc[x].number),
                        1,".",E_prcpDAYS[x].year,E_prcpDAYS[x].number,
                        1,".",E_prcpDAYS_asc[x].year,E_prcpDAYS_asc[x].number,
                        1 if E_snow[x].number else "","." if E_snow[x].number > 0 else " ",
                        E_snow[x].year if E_snow[x].number > 0 else "","{:.1f}".format(E_snow[x].number) if E_snow[x].number > 0 else "",
                        1 if E_snowDAYS[x].number > 0 else "","." if E_snowDAYS[x].number > 0 else " ",
                        E_snowDAYS[x].year if E_snowDAYS[x].number > 0 else "",E_snowDAYS[x].number if E_snowDAYS[x].number > 0 else ""))
                    ranked_i.append(i);ranked_j.append(j);ranked_k.append(k);ranked_l.append(l);ranked_m.append(m);ranked_n.append(n)
                else:
                    if i not in ranked_i and i <= qty: ranked_i.append(i)
                    if j not in ranked_j and j <= qty:
                        ranked_j.append(j)
                        #printed_j += 1
                    if k not in ranked_k and k <= qty: ranked_k.append(k)
                    if l not in ranked_l and l <= qty:
                        ranked_l.append(l)
                        #printed_l += 1
                    if m not in ranked_m and m <= qty: ranked_m.append(m)
                    if n not in ranked_n and n <= qty: ranked_n.append(n)
                    if E_prcp[x].number != E_prcp[x-1].number: i += 1
                    if E_prcp_asc[x].number != E_prcp_asc[x-1].number: j += 1
                    if E_prcpDAYS[x].number != E_prcpDAYS[x-1].number: k += 1
                    if E_prcpDAYS_asc[x].number != E_prcpDAYS_asc[x-1].number: l += 1
                    if E_snow[x].number != E_snow[x-1].number: m += 1
                    if E_snowDAYS[x].number != E_snowDAYS[x-1].number: n += 1
                    if E_prcp[x].number == 0: i = qty + 1
                    #if printed_j == len(valid_yrs)-10: j = qty + 1
                    if E_prcpDAYS[x].number == 0: k = qty + 1
                    #if printed_l == len(valid_yrs)-10: l = qty + 1
                    if E_snow[x].number == 0: m = qty + 1
                    if E_snowDAYS[x].number == 0: n = qty + 1
                    if i <= qty or j <= qty or k <= qty or l <= qty or m <= qty or n <= qty:
                        print(" {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:>6} | {:2}{} {:4}  {:3} | {:2}{} {:4}  {:3} | {:2}{} {:4}  {:>5} | {:2}{} {:4}  {:>3} ".format(
                            i if i not in ranked_i and i <= qty else "","." if i not in ranked_i and i <= qty else " ",
                            E_prcp[x].year if i <= qty else "","{:.2f}".format(E_prcp[x].number) if i <= qty else "",
                            j if j not in ranked_j and j <= qty else "","." if j not in ranked_j and j <= qty else " ",
                            E_prcp_asc[x].year if j <= qty else "","{:.2f}".format(E_prcp_asc[x].number) if j <= qty else "",
                            k if k not in ranked_k and k <= qty else "","." if k not in ranked_k and k <= qty else " ",
                            E_prcpDAYS[x].year if k <= qty else "",E_prcpDAYS[x].number if k <= qty else "",
                            l if l not in ranked_l and l <= qty else "","." if l not in ranked_l and l <= qty else " ",
                            E_prcpDAYS_asc[x].year if l <= qty else "",E_prcpDAYS_asc[x].number if l <= qty else "",
                            m if m not in ranked_m and m <= qty else "","." if m not in ranked_m and m <= qty else " ",
                            E_snow[x].year if m <= qty else "","{:.1f}".format(E_snow[x].number) if m <= qty else "",
                            n if n not in ranked_n and n <= qty else "","." if n not in ranked_n and n <= qty else " ",
                            E_snowDAYS[x].year if n <= qty else "",E_snowDAYS[x].number if n <= qty else ""))
                if i > qty and j > qty and k > qty and l > qty and m > qty and n > qty: break
        if attribute == "temp":
            print("{:^111}".format("Ranked Temperatures for {} {} thru {} {}".format(calendar.month_abbr[startday.month],startday.day,calendar.month_abbr[endday.month],endday.day)))
            print("{:^111}".format("{}, {}".format(clmt["station"],clmt["station_name"])))
            print("{:^111}".format("Periods with >= {} Day(s) of Data".format(EXCLD+1)))
            print("{:-^111}".format(""))
            print("{:^36}|{:^37}|{:^36}".format("AVG TEMP","TMAX","TMIN"))
            print("{:-^36}|{:-^37}|{:-^36}".format("","",""))
            print("{:^17}|{:^18}|{:^18}|{:^18}|{:^18}|{:^17}".format("Warmest","Coolest","Warmest","Coolest","Warmest","Coolest"))
            print("{:-^17}|{:-^18}|{:-^18}|{:-^18}|{:-^18}|{:-^17}".format("","","","","",""))
            i = 1; j = 1; k = 1; l = 1; m = 1; n = 1
            ranked_i = []; ranked_j = []; ranked_k = []; ranked_l = []; ranked_m = []; ranked_n = []
            for x in range(len(E_tmax)):
                if x == 0:
                    print("{:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}".format(
                                                                    1,".",E_tavg[x].year,"{:.1f}".format(E_tavg[x].number),
                                                                    1,".",E_tavg_asc[x].year,"{:.1f}".format(E_tavg_asc[x].number),
                                                                    1,".",E_tmax[x].year,"{:.1f}".format(E_tmax[x].number),
                                                                    1,".",E_tmax_asc[x].year,"{:.1f}".format(E_tmax_asc[x].number),
                                                                    1,".",E_tmin[x].year,"{:.1f}".format(E_tmin[x].number),
                                                                    1,".",E_tmin_asc[x].year,"{:.1f}".format(E_tmin_asc[x].number)))
                    ranked_i.append(i); ranked_j.append(j); ranked_k.append(k); ranked_l.append(l); ranked_m.append(m); ranked_n.append(n)
                else:
                    if i not in ranked_i and i <= qty: ranked_i.append(i)
                    if j not in ranked_j and j <= qty: ranked_j.append(j)
                    if k not in ranked_k and k <= qty: ranked_k.append(k)
                    if l not in ranked_l and l <= qty: ranked_l.append(l)
                    if m not in ranked_m and m <= qty: ranked_m.append(m)
                    if n not in ranked_n and n <= qty: ranked_n.append(n)
                    if E_tavg[x].number != E_tavg[x-1].number: i += 1
                    if E_tavg_asc[x].number != E_tavg_asc[x-1].number: j += 1
                    if E_tmax[x].number != E_tmax[x-1].number: k += 1
                    if E_tmax_asc[x].number != E_tmax_asc[x-1].number: l += 1
                    if E_tmin[x].number != E_tmin[x-1].number: m += 1
                    if E_tmin_asc[x].number != E_tmin_asc[x-1].number: n += 1
                    if i <= qty or j <= qty or k <= qty or l <= qty or m <= qty or n <= qty:
                        print("{:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}  | {:2}{} {:4}  {:>5}".format(
                                i if i not in ranked_i and i <= qty else "","." if i not in ranked_i and i <= qty else " ",
                                E_tavg[x].year if i <= qty else "","{:.1f}".format(E_tavg[x].number) if i <= qty else "",
                                j if j not in ranked_j and j <= qty else "","." if j not in ranked_j and j <= qty else " ",
                                E_tavg_asc[x].year if j <= qty else "","{:.1f}".format(E_tavg_asc[x].number) if j <= qty else "",
                                k if k not in ranked_k and k <= qty else "","." if k not in ranked_k and k <= qty else " ",
                                E_tmax[x].year if k <= qty else "","{:.1f}".format(E_tmax[x].number) if k <= qty else "",
                                l if l not in ranked_l and l <= qty else "","." if l not in ranked_l and l <= qty else " ",
                                E_tmax_asc[x].year if l <= qty else "","{:.1f}".format(E_tmax_asc[x].number) if l <= qty else "",
                                m if m not in ranked_m and m <= qty else "","." if m not in ranked_m and m <= qty else " ",
                                E_tmin[x].year if m <= qty else "","{:.1f}".format(E_tmin[x].number) if m <= qty else "",
                                n if n not in ranked_n and n <= qty else "","." if n not in ranked_n and n <= qty else " ",
                                E_tmin_asc[x].year if n <= qty else "","{:.1f}".format(E_tmin_asc[x].number) if n <= qty else ""))
                if i > qty and j > qty and k > qty and l > qty and m > qty and n > qty: break
        print("")

def allDayRank(attribute,qty,**kw):
    """Returns a list of rankings, comparing only specific days to one
    another. If season keyword is present, month keyword will be ignored. If
    season and year are specified, only results from the season from the 
    specific year will be used. If year and month are specified, only data
    from that time period will be used. If only month is specified, all data
    occurring from that month, regardless of year, will be used.
    
    allDayRank(attribute,quantity,**kwargs)
    
    Accepted Attributes:
        "prcp", "snow", "snwd", "tmax", "tmin", "tavg"
    
    Keyword Arguments (displayed in heirarchal order):
        season="season"  -> limit season <"spring"|"summer"|"fall"|"winter">
        year=YYYY        -> limit results to a specific year
        month=M          -> limit results to a specific month
        ascending=False  -> alters order of data (only affects temp attrs)
        custom=[m1,d1,m2,d2]    -> limits results if the record falls within
                                   the date-range given
    
    EXAMPLE: allDayRank("snow",10)
                    -> top 10 ranks all days acc. to snow
             allDayRank("prcp",15,season="summer")
                    -> top 15 rain days in summer
             allDayRank("tmax",10,season="fall",year=2005)
                    -> top 10 warmest daily highs from Fall 2005
             allDayRank("tmin",10,year=2009,ascending=True)
                    -> top 10 coolest daily lows in 2009
             allDayRank("prcp",20,custom=[12,3,5,1])
                    -> top 20 rain-days between Dec3 and May1
    """

    # clmt_vars_days = {"prcp":{},"snow":{},"snwd":{},"tavg":{},"tmax":{},"tmin":{}}
    # clmt_vars_days["prcp"][amount] = [list, of, days, that, had, that, value]
    # consider adding a "finite" kwarg. This setting would only report the quantity of days that a match was made rather than a potentially long list of days
    # consider adding an "order" or "reverse" kwarg
    valid_yrs = sorted([x for x in clmt.keys() if type(x) == int])
    valid_metyrs = sorted([x for x in metclmt.keys() if type(x) == int])
    hascustom = False
    hasseason = False
    hasyear = False
    hasmonth = False

    daysinmonths = ["_",31,28,31,30,31,30,31,31,30,31,30,31]    # used to quickly determine validity of dates entered with custom keyword

    #ERROR CHECKS
    if attribute not in ["prcp","snow","snwd","tmax","tmin","tavg"]: return print('OOPS! "{}" is an Invalid Attribute. Try Again! Valid Attributes: "prcp","snow","snwd","tmax","tmin","tavg"'.format(attribute))
    if type(qty) != int: return print("OOPS! Ensure the quantity is an integer! Try again!")
    # Custom Date Range
    if "custom" in kw:
        try:
            m1 = kw["custom"][0]
            d1 = kw["custom"][1]
            m2 = kw["custom"][2]
            d2 = kw["custom"][3]
        except:
            return print("OOPS! Something is wrong with the dates. Ensure a format of [m1,d1,m2,d2]")
        if type(kw["custom"]) not in [list,tuple]: return print("OOPS! Pass your custom range in a list. ex: [m1,d1,m2,d2]")
        elif any(type(x) != int for x in kw["custom"]) or len(kw["custom"]) != 4: return print("OOPS! Ensure all variables passed in your list are integers representing month/dates of interest and that a start/end month day sets are included, ex: [m1,d1,m2,d2]")
        elif (1 <= m1 <= 12) == False or (1 <= m2 <= 12) == False: return print("OOPS! An invalid month was entered.") 
        elif (d1 <= 0 or d1 > daysinmonths[m1]) or (d2 <= 0 or d2 > daysinmonths[m2]): return print("OOPS! One or both of the dates are invalid.")
        elif m1 == m2 and d1 == d2: return print("OOPS! The first and second dates cannot be alike.")
        hascustom = True
        # If February 29, we want to default to the 28th
        if m1 == 2 and d1 == 29: d1 = 28
        if m2 == 2 and d2 == 29: d2 = 28

    # Specified Season
    elif "season" in kw:
        if kw["season"].lower() not in ["spring","summer","fall","winter"]: return print('OOPS! "{}" is an invalid season. Try again! Valid Seasons (all lower case):"spring","summer","fall","winter"'.format(kw["season"]))
        hasseason = True
        # for specifying a year of a season
        if "year" in kw:
            hasyear = True
            YEAR = int(kw["year"])
            if YEAR not in valid_yrs: return print("OOPS! No data for the year {} found. Try again!".format(YEAR))
    # Specifying a year
    elif "year" in kw:
        hasyear = True
        YEAR = int(kw["year"])
        if YEAR not in clmt: return print("OOPS! No data for the year {} found. Try again!".format(YEAR))
        # Focusing on a specific month in a specific year
        if "month" in kw:
            hasmonth = True
            MONTH = int(kw["month"])
            if MONTH not in range(1,12+1): return print("OOPS! Invalid Month. Try again!")
            if MONTH not in clmt[YEAR]: return print("OOPS! No data for {} {} found. Try again!".format(calendar.month_name[MONTH],YEAR))
    # Specifying a month
    elif "month" in kw:
        hasmonth = True
        MONTH = int(kw["month"])
        if MONTH not in range(1,12+1): return print("OOPS! Invalid Month. Try again!")
    ##########################
    r = 0
    printed = []    # Will hold the printed rankings
    print("\n-----------------------------------------------")
    # HEADER ------------------
    if hascustom == True: print("Top {} Daily {} Records for the Range of {} {} thru {} {}".format(
            qty,attribute.upper(),d1,calendar.month_abbr[m1].upper(),
            d2,calendar.month_abbr[m2].upper()
        ))
    elif hasseason == True:
        if hasyear == True: print("Top {} Daily {} Records for {} {}".format(qty,attribute.upper(),kw["season"].capitalize(),YEAR))
        else: print("Top {} Daily {} Records for {}".format(qty,attribute.upper(),kw["season"].capitalize()))
    elif hasyear == True:
        if hasmonth == True: print("Top {} Daily {} Records for {} {}".format(qty,attribute.upper(),calendar.month_name[MONTH],YEAR))
        else: print("Top {} Daily {} Records for {}".format(qty,attribute.upper(),YEAR))
    elif hasmonth == True: print("Top {} Daily {} Records for {}".format(qty,attribute.upper(),calendar.month_name[MONTH]))
    else: print("Top {} Daily {} Records for All-Time".format(qty,attribute.upper()))
    # -------------------------
    # -------------------------
    print("{}, {}".format(clmt["station"],clmt["station_name"]))
    if "ascending" in kw and attribute in ["tmax","tmin","tavg"]:
        if kw["ascending"] == True:
            keys = sorted([key for key in clmt_vars_days[attribute].keys()])
            print("--- Coolest to Warmest ---")
    else:
        keys = sorted([key for key in clmt_vars_days[attribute].keys()],reverse=True)
        if attribute in ["tmax","tmin","tavg"]: print("--- Warmest to Coolest ---")
    print("-----------------------------------------------")
    # -------------------------
    validated = {}
    # 12-3  to 1,10
    #               (1959,1,7)
    if hascustom == True:
        for x in keys:
            for y in range(len(clmt_vars_days[attribute][x])):
                # When the 2nd month refers to an earlier month(or the same)
                if datetime.date(2100,m2,d2) < datetime.date(2100,m1,d1):
                    try:
                        if (clmt_vars_days[attribute][x][y] >= datetime.date(clmt_vars_days[attribute][x][y].year,m1,d1)) or (clmt_vars_days[attribute][x][y] <= datetime.date(clmt_vars_days[attribute][x][y].year,m2,d2)):
                            if x not in validated: validated[x] = [clmt_vars_days[attribute][x][y]]
                            else: validated[x].append(clmt_vars_days[attribute][x][y])
                    except Exception as e:
                        pass
                # When the 2nd month is later than the first month
                else:
                    if datetime.date(clmt_vars_days[attribute][x][y].year,m1,d1) <= clmt_vars_days[attribute][x][y] <= datetime.date(clmt_vars_days[attribute][x][y].year,m2,d2):
                        if x not in validated: validated[x] = [clmt_vars_days[attribute][x][y]]
                        else: validated[x].append(clmt_vars_days[attribute][x][y])
    elif hasseason == True and hasyear == False: # Only assess a season
        # metclmt[y][s]["valid"] = [3,4,5]
        # clmt_vars_days[attribute][x][y]
        for x in keys:
            for y in range(len(clmt_vars_days[attribute][x])):
                if clmt_vars_days[attribute][x][y].month <= 2 and clmt_vars_days[attribute][x][y].year-1 in metclmt and clmt_vars_days[attribute][x][y].month in metclmt[clmt_vars_days[attribute][x][y].year-1][kw["season"]]["valid"]:
                    if x not in validated:
                        validated[x] = [clmt_vars_days[attribute][x][y]]
                    else:
                        validated[x].append(clmt_vars_days[attribute][x][y])
                elif clmt_vars_days[attribute][x][y].month >= 3 and clmt_vars_days[attribute][x][y].month in metclmt[clmt_vars_days[attribute][x][y].year][kw["season"]]["valid"]:
                    if x not in validated:
                        validated[x] = [clmt_vars_days[attribute][x][y]]
                    else:
                        validated[x].append(clmt_vars_days[attribute][x][y])
    elif hasseason == True and hasyear == True: # Only assess a season of a particular year
        # metclmt[y][s]["valid"] = [3,4,5]
        # clmt_vars_days[attribute][x][y]
        for x in keys:
            for y in range(len(clmt_vars_days[attribute][x])):
                if kw["season"].lower() == "winter":
                    if clmt_vars_days[attribute][x][y].month in metclmt[clmt_vars_days[attribute][x][y].year][kw["season"]]["valid"]:
                        if clmt_vars_days[attribute][x][y].month in [1,2] and clmt_vars_days[attribute][x][y].year == YEAR+1:
                            if x not in validated:
                                validated[x] = [clmt_vars_days[attribute][x][y]]
                            else:
                                validated[x].append(clmt_vars_days[attribute][x][y])
                        if clmt_vars_days[attribute][x][y].month == 12 and clmt_vars_days[attribute][x][y].year == YEAR:
                            if x not in validated:
                                validated[x] = [clmt_vars_days[attribute][x][y]]
                            else:
                                validated[x].append(clmt_vars_days[attribute][x][y])
                else:
                    if clmt_vars_days[attribute][x][y].year == YEAR and clmt_vars_days[attribute][x][y].month in metclmt[clmt_vars_days[attribute][x][y].year][kw["season"]]["valid"]:
                        if x not in validated:
                            validated[x] = [clmt_vars_days[attribute][x][y]]
                        else:
                            validated[x].append(clmt_vars_days[attribute][x][y])
    elif hasyear == True and hasmonth == False:   # Only assess a particular year
        for x in keys:
            for y in range(len(clmt_vars_days[attribute][x])):
                if clmt_vars_days[attribute][x][y].year == YEAR:
                    if x not in validated:
                        validated[x] = [clmt_vars_days[attribute][x][y]]
                    else:
                        validated[x].append(clmt_vars_days[attribute][x][y])
    elif hasyear == True and hasmonth == True:  # Only assess a particular month of a particular year
        for x in keys:
            for y in range(len(clmt_vars_days[attribute][x])):
                if clmt_vars_days[attribute][x][y].year == YEAR and clmt_vars_days[attribute][x][y].month == MONTH:
                    if x not in validated:
                        validated[x] = [clmt_vars_days[attribute][x][y]]
                    else:
                        validated[x].append(clmt_vars_days[attribute][x][y])
    elif hasmonth == True:  # Only assess data from a particular month
        for x in keys:
            for y in range(len(clmt_vars_days[attribute][x])):
                if clmt_vars_days[attribute][x][y].month == MONTH:
                    if x not in validated:
                        validated[x] = [clmt_vars_days[attribute][x][y]]
                    else:
                        validated[x].append(clmt_vars_days[attribute][x][y])
    else:   # Assesses data from the entire record
        for x in keys:
            for y in range(len(clmt_vars_days[attribute][x])):
                if x not in validated:
                    validated[x] = [clmt_vars_days[attribute][x][y]]
                else:
                    validated[x].append(clmt_vars_days[attribute][x][y])
    for x in validated:
        r += 1
        if r > qty: break
        for y in range(len(validated[x])):
            if attribute == "prcp": print("{:>2}{} {:>5.2f} - {}".format(r if r not in printed else " ","." if r not in printed else " ",x,validated[x][y]))
            elif attribute in ["snow","snwd","tavg"]: print("{:>2}{} {:>5.1f} - {}".format(r if r not in printed else " ","." if r not in printed else " ",x,validated[x][y]))
            else: print("{:>2}{} {:>3} - {}".format(r if r not in printed else " ","." if r not in printed else " ",x,validated[x][y]))
            if r not in printed: printed.append(r)
    #-------------------------------------------
    print("")

def allMonthRank(attribute,qty,**kw):
    """Returns a list of rankings, comparing only specific months to one
    another. Optional season kewyord included to limit results to a specific
    season. Optional ascending keyword, if set to True, will reverse the
    order of results
    
    allMonthRank(attribute,quantity,**kwargs)
    
    Accepted Attributes:
        "prcp", "prcpDAYS", "snow", "snowDAYS", "snwd", "snwdDAYS",
        "tmax","tmin", "tavg"
    
    Keyword Arguments (Optional):
        season="season"  -> limit season <"spring"|"summer"|"fall"|"winter">
        ascending=False  -> alters order of data (only affects temp or prcp
                            attrs)
    
    EXAMPLE: allMonthRank("snow",10)
                    -> top 10 ranks all months acc. to snow
             allMonthRank("prcp",15,season="summer")
                    -> top 15 rain months in summer
             allMonthRank("tmin",10,ascending=True)
                    -> top 10 coolest months based on avg lows
    """
    valid_yrs = sorted([x for x in clmt.keys() if type(x) == int])
    valid_metyrs = sorted([x for x in metclmt.keys() if type(x) == int])
    valid_season = {"spring":[3,4,5],"summer":[6,7,8],"fall":[9,10,11],"winter":[12,1,2]}
    hasseason = False
    
    #ERROR CHECKS
    if attribute not in ["prcp","prcpDAYS","snow","snowDAYS","snwd","snwdDAYS","tmax","tmin","tavg"]: return print('OOPS! "{}" is an Invalid Attribute. Try Again! Valid Attributes: "prcp","snow",,"snowDAYS","snwd","snwdDAYS","tmax","tmin","tavg"'.format(attribute))
    if type(qty) != int: return print("OOPS! Ensure the quantity is an integer! Try again!")
    
    # Specified Season
    if "season" in kw:
        if kw["season"].lower() not in ["spring","summer","fall","winter"]: return print('OOPS! "{}" is an invalid season. Try again! Valid Seasons (all lower case):"spring","summer","fall","winter"'.format(kw["season"]))
        hasseason = True

    ##########################
    r = 0
    printed = []    # Will hold the printed rankings
    appendr = False
    print("\n-----------------------------------------------")
    # HEADER ------------------
    if hasseason == True:
        print("Top {} Monthly {} Records Inclusive of {} Months Only".format(qty,attribute.upper(),kw["season"].capitalize()))
    else: print("Top {} Monthly {} Records for All-Time".format(qty,attribute.upper()))
    # -------------------------
    print("{}, {}".format(clmt["station"],clmt["station_name"]))
    if "ascending" in kw and kw["ascending"] == True and attribute not in ["snow","snowDAYS","snwd","snwdDAYS"]:
        keys = sorted([key for key in clmt_vars_months[attribute].keys()])
        if attribute in ["tmax","tmin","tavg"]: print("--- Coolest to Warmest ---")
        if attribute in ["prcp"]: print("--- Driest to Wettest ---")
    else:
        keys = sorted([key for key in clmt_vars_months[attribute].keys()],reverse=True)
        if attribute in ["tmax","tmin","tavg"]: print("--- Warmest to Coolest ---")
        if attribute in ["prcp"]: print("--- Wettest to Driest ---")
        if attribute in ["prcpDAYS","snow","snowDAYS","snwd","snwdDAYS"]: print("--- Greatest to Least ---")
    print("-----------------------------------------------")
    # -------------------------
    if hasseason == True: # Only assess a season
        # metclmt[y][s]["valid"] = [3,4,5]
        # clmt_vars_days[attribute][x][y]
        metkeys = {}
        for x in keys:
            for y in range(len(clmt_vars_months[attribute][x])):
                if clmt_vars_months[attribute][x][y].month in valid_season[kw["season"]]:
                    if x not in metkeys:
                        metkeys[x] = [clmt_vars_months[attribute][x][y]]
                    else:
                        metkeys[x].append(clmt_vars_months[attribute][x][y])
        #for x in metkeys:
            #print("{} - {}".format(x,metkeys[x]))
        for x in metkeys:
            r += 1
            if r > qty: break
            for y in range(len(metkeys[x])):
                if metkeys[x][y].month <= 2:
                    if attribute == "tavg":
                        if "ascending" not in kw or "ascending" in kw and kw["ascending"] == False or "ascending" in kw and kw["ascending"] == True and clmt[metkeys[x][y].year][metkeys[x][y].month]["recordqty"] > excludemonth * 2:
                            appendr = True
                            print("{:>2}{} {:6.1f} - {} {}".format(r if r not in printed else " ","." if r not in printed else " ",x,calendar.month_abbr[metkeys[x][y].month],metkeys[x][y].year))
                    else:
                        if "ascending" not in kw or "ascending" in kw and kw["ascending"] == False or "ascending" in kw and kw["ascending"] == True and clmt[metkeys[x][y].year][metkeys[x][y].month]["recordqty"] > excludemonth:
                            appendr = True
                            if attribute == "prcp":
                                print("{:>2}{} {:6.2f} - {} {}".format(r if r not in printed else " ","." if r not in printed else " ",x,calendar.month_abbr[metkeys[x][y].month],metkeys[x][y].year))
                            elif attribute in ["prcpDAYS","snowDAYS","snwdDAYS"]:
                                print("{:>2}{} {:2} - {} {}".format(r if r not in printed else " ","." if r not in printed else " ",x,calendar.month_abbr[metkeys[x][y].month],metkeys[x][y].year))
                            else:
                                print("{:>2}{} {:6.1f} - {} {}".format(r if r not in printed else " ","." if r not in printed else " ",x,calendar.month_abbr[metkeys[x][y].month],metkeys[x][y].year))
                else:
                    if attribute == "tavg":
                        if "ascending" not in kw or "ascending" in kw and kw["ascending"] == False or "ascending" in kw and kw["ascending"] == True and clmt[metkeys[x][y].year][metkeys[x][y].month]["recordqty"] > excludemonth * 2:
                            appendr = True
                            print("{:>2}{} {:6.1f} - {} {}".format(r if r not in printed else " ","." if r not in printed else " ",x,calendar.month_abbr[metkeys[x][y].month],metkeys[x][y].year))
                    else:
                        if "ascending" not in kw or "ascending" in kw and kw["ascending"] == False or "ascending" in kw and kw["ascending"] == True and clmt[metkeys[x][y].year][metkeys[x][y].month]["recordqty"] > excludemonth:
                            appendr = True
                            if attribute == "prcp":
                                print("{:>2}{} {:6.2f} - {} {}".format(r if r not in printed else " ","." if r not in printed else " ",x,calendar.month_abbr[metkeys[x][y].month],metkeys[x][y].year))
                            elif attribute in ["prcpDAYS","snowDAYS","snwdDAYS"]:
                                print("{:>2}{} {:2} - {} {}".format(r if r not in printed else " ","." if r not in printed else " ",x,calendar.month_abbr[metkeys[x][y].month],metkeys[x][y].year))
                            else:
                                print("{:>2}{} {:6.1f} - {} {}".format(r if r not in printed else " ","." if r not in printed else " ",x,calendar.month_abbr[metkeys[x][y].month],metkeys[x][y].year))
                if r not in printed and appendr == True:
                    printed.append(r)
                    appendr = False
    else:   # Assesses data from the entire record
        for x in keys:
            r += 1
            if r > qty: break
            for y in range(len(clmt_vars_months[attribute][x])):
                if attribute == "tavg":
                    if "ascending" not in kw or ("ascending" in kw and kw["ascending"] == False) or ("ascending" in kw and kw["ascending"] == True and clmt[clmt_vars_months[attribute][x][y].year][clmt_vars_months[attribute][x][y].month]["recordqty"] > excludemonth * 2):
                        appendr = True
                        print("{:>2}{} {:6.1f} - {} {}".format(r if r not in printed else " ","." if r not in printed else " ",x,calendar.month_abbr[clmt_vars_months[attribute][x][y].month],clmt_vars_months[attribute][x][y].year))
                else:
                    if "ascending" not in kw or ("ascending" in kw and kw["ascending"] == False) or ("ascending" in kw and kw["ascending"] == True and clmt[clmt_vars_months[attribute][x][y].year][clmt_vars_months[attribute][x][y].month]["recordqty"] > excludemonth):
                        appendr = True
                        if attribute == "prcp":
                            print("{:>2}{} {:6.2f} - {} {}".format(r if r not in printed else " ","." if r not in printed else " ",x,calendar.month_abbr[clmt_vars_months[attribute][x][y].month],clmt_vars_months[attribute][x][y].year))
                        elif attribute in ["prcpDAYS","snowDAYS","snwdDAYS"]:
                            print("{:>2}{} {:2} - {} {}".format(r if r not in printed else " ","." if r not in printed else " ",x,calendar.month_abbr[clmt_vars_months[attribute][x][y].month],clmt_vars_months[attribute][x][y].year))
                        else:
                            print("{:>2}{} {:6.1f} - {} {}".format(r if r not in printed else " ","." if r not in printed else " ",x,calendar.month_abbr[clmt_vars_months[attribute][x][y].month],clmt_vars_months[attribute][x][y].year))
                if r not in printed and appendr == True:
                    printed.append(r)
                    appendr = False
    #-------------------------------------------
    print("")

def valueSearch(stat_type,op,value,**kwargs):
    """Quick function to designate a value, and the days or months where the
    attribute of interest exceeded, equalled, or was less than the passed
    value

    valueSearch("attribute","operator",value,**{sortmonth=False})
    
    * "attribute" must be in ["prcp","snow","snwd","tavg","tmax","tmin"] (other
                values are accepted, but these are what are assessed
    * "operator" must be in ["<=","<","==","!=",">",">="]
    * value must be an integer or a float
    
    OPT **kwarg: sortmonth = True --> If set to true, it will do a value
                                     search based on monthly data instead of
                                     daily (no snwd data is available for
                                     months though)
    
    EXAMPLE: valueSearch("prcp",">=",5) --> returns a list of all days on 
                                            record where 5+ inches of rain
                                            fell
    """
    #operator=">", year=1984, month=12,season="winter"
    # v, args[rain,prcp,snow,temp,avgtemp,tmax,avgtmax,tmin,avgtmin], kwargs[condition,year,metyear,season,month]
    valid_yrs = sorted([x for x in clmt.keys() if type(x) == int])
    valid_metyrs = sorted([x for x in metclmt.keys() if type(x) == int])
    
    # ERROR HANDLING
    if stat_type.lower() not in ["rain","prcp","precip","snow","snwd","temp","temps","temperature","temperatures","avgtemp","tavg","tempavglist","tmax","hi","high","tmin","lo","low"]:
        return print("OOPS! {} is not a supported stat category. Try again!".format(stat_type))
    if op not in ["<","<=","==",">",">="]: return print("OOPS! '{}' is not a supported operator. Try again!".format(op))
    if type(value) not in [int,float]: return print("OOPS! Only integers or floats are supported for value intake")
   
    # Format passed variables
    stat_type = stat_type.lower()   # Convert to lower-case for homogeniety
    if stat_type in ["rain","prcp","precip"]: stat_type = "prcp"
    if stat_type in ["snow"]: stat_type = "snow"
    if stat_type in ["snwd"]: stat_type = "snwd"
    if stat_type in ["avgtemp","tavg","tempavglist","temp","temps","temperature","temperatures"]: stat_type = "tavg"
    if stat_type in ["tmax","hi","high"]: stat_type = "tmax"
    if stat_type in ["tmin","lo","low"]: stat_type = "tmin"
   
    if "sortmonth" in kwargs and kwargs["sortmonth"] == True:
        CLMTDICT = clmt_vars_months
        stype = "month"
    else:   # Just sorting indv days
        CLMTDICT = clmt_vars_days
        stype = "day"

    results = []
    for VAR in CLMTDICT[stat_type]:
        for DAY in CLMTDICT[stat_type][VAR]:
            if op == "<":
                if stype == "month":
                    if VAR < value and clmt[DAY.year][DAY.month]["recordqty"] > excludemonth: results.append(DAY)
                else:
                    if VAR < value: results.append(DAY)
            elif op == "<=":
                if stype == "month":
                    if VAR <= value and clmt[DAY.year][DAY.month]["recordqty"] > excludemonth: results.append(DAY)
                else:
                    if VAR <= value: results.append(DAY)
            elif op == "!=":
                if VAR != value: results.append(DAY)
            elif op == "==":
                if VAR == value: results.append(DAY)
            elif op == ">=":
                if VAR >= value: results.append(DAY)
            elif op == ">":
                if VAR > value: results.append(DAY)
    results.sort()
    
    if "sortmonth" in kwargs and kwargs["sortmonth"] == True:
        if stat_type == "prcp": print("Total months where the Total Rainfall {} {}: {}".format(op,value,len(results)))
        elif stat_type == "snow": print("Total months where the Total Snowfall {} {}: {}".format(op,value,len(results)))
        elif stat_type in ["tmax","tmin"]:
            print("Total months where the Average {} {} {}: {}".format(stat_type.upper(),op,value,len(results)))
        elif stat_type == "tavg":
            print("Total months where the Average Temperature {} {}: {}".format(op,value,len(results)))
        else:
            return print("*** valueSearch does not report on monthly variations of {} ***".format(stat_type))
        if len(results) <= 50: stillprint = True
        else:
            stillpr = input("print results? ('y'/'n'): ")
            if stillpr == "y": stillprint = True
            else: stillprint = False
        if stillprint == True:
            if stat_type == "prcp":
                for x in results: print("{:6.2f}: {} {}".format(round(sum(clmt[x.year][x.month]["prcp"]),2),calendar.month_abbr[x.month],x.year))
            if stat_type == "snow":
                for x in results: print("{:5.1f}: {} {}".format(round(sum(clmt[x.year][x.month]["snow"]),1),calendar.month_abbr[x.month],x.year))
            #if stat_type == "snwd":
                #for x in results: print("{:5.1f}: {} {}".format(round(sum(clmt[x.year][x.month]["snwd"]),1),calendar.month_abbr[x.month],x.year))
            if stat_type == "tavg":
                for x in results: print("{:5.1f}: {} {}".format(round(mean(clmt[x.year][x.month]["tempAVGlist"]),1),calendar.month_abbr[x.month],x.year))
            if stat_type == "tmax":
                for x in results: print("{:5.1f}: {} {}".format(round(mean(clmt[x.year][x.month]["tmax"]),1),calendar.month_abbr[x.month],x.year))
            if stat_type == "tmin":
                for x in results: print("{:5.1f}: {} {}".format(round(mean(clmt[x.year][x.month]["tmin"]),1),calendar.month_abbr[x.month],x.year))
    else:   # Just assessing individual days
        print("Total days where '{}' {} {}: {}".format(stat_type,op,value,len(results)))
        if len(results) <= 50: stillprint = True
        else:
            stillpr = input("print results? ('y'/'n'): ")
            if stillpr == "y": stillprint = True
            else: stillprint = False
        if stillprint == True:
            if stat_type == "prcp":
                for x in results: print("{:>5.2f}: {}".format(float(clmt[x.year][x.month][x.day].prcp),x))
            if stat_type == "snow":
                for x in results: print("{:>5.1f}: {}".format(float(clmt[x.year][x.month][x.day].snow),x))
            if stat_type == "snwd":
                for x in results: print("{:>5.1f}: {}".format(float(clmt[x.year][x.month][x.day].snwd),x))
            if stat_type == "tmax":
                for x in results: print("{:>3}: {}".format(clmt[x.year][x.month][x.day].tmax,x))
            if stat_type == "tmin":
                for x in results: print("{:>3}: {}".format(clmt[x.year][x.month][x.day].tmin,x))
    print("")

def corrections():
    """Activates correction mode"""

    print("CORRECTIONS MODE ACTIVATED - {}".format(clmt["station_name"]))
    print("------------------------------------------------")
    print("* Input a comma-separated list of the Year, Month, Date, Attribute, and new reading")
    print("* Ex: INPUT CORRECTION: 1899,1,30,\"prcp\",2.02")
    print("* When finished, type DONE and press enter")
    fix = []
    while True:
        inp = input("INPUT CORRECTION: ").split(",")
        if inp[0].upper() == "DONE" or inp[0] == "": break
        elif len(inp) != 5: print("* not enough data given. Try again *")
        elif any(x.isdigit() == False for x in inp[0:3]): print("* Dates entered must be numeric. Try again.")
        elif inp[3].strip('"') not in ["prcp","snow","snwd","tmax","tmin"]:
            print("* Invalid Attr. Valid Attributes: '{}','{}','{}','{}'".format("prcp","snow","snwd","tmax","tmin"))
        else:
            y = int(inp[0])
            m = int(inp[1])
            d = int(inp[2])
            if y not in clmt or m not in clmt[y] or d not in clmt[y][m]:
                print("* No valid entry for {}-{}-{} exists. Try again".format(int(inp[0]),int(inp[1]),int(inp[2])))
            else:
                try:
                    if inp[3].strip('"') == "prcp":
                        testvalue = round(float(inp[4]),2)
                        if clmt[int(inp[0])][int(inp[1])][int(inp[2])].prcpQ == "":
                            print("HEADS UP! {} already had no PRCP quality flag".format(clmt[int(inp[0])][int(inp[1])][int(inp[2])].daystr))
                        clmt[int(inp[0])][int(inp[1])][int(inp[2])].prcp = inp[4]
                        clmt[int(inp[0])][int(inp[1])][int(inp[2])].prcpQ = ""
                        fix.append("{},{},,,,".format(clmt[int(inp[0])][int(inp[1])][int(inp[2])].daystr,inp[4]))
                        print("    Amendment for {} PRCP successful: {}".format(clmt[int(inp[0])][int(inp[1])][int(inp[2])].daystr,inp[4]))
                    if inp[3].strip('"') == "snow":
                        testvalue = round(float(inp[4]),1)
                        if clmt[int(inp[0])][int(inp[1])][int(inp[2])].snowQ == "":
                            print("HEADS UP! {} already had no SNOW quality flag".format(clmt[int(inp[0])][int(inp[1])][int(inp[2])].daystr))
                        clmt[int(inp[0])][int(inp[1])][int(inp[2])].snow = inp[4]
                        clmt[int(inp[0])][int(inp[1])][int(inp[2])].snowQ = ""
                        fix.append("{},,{},,,".format(clmt[int(inp[0])][int(inp[1])][int(inp[2])].daystr,inp[4]))
                        print("    Amendment for {} SNOW successful: {}".format(clmt[int(inp[0])][int(inp[1])][int(inp[2])].daystr,inp[4]))
                    if inp[3].strip('"') == "snwd":
                        testvalue = round(float(inp[4]),1)
                        if clmt[int(inp[0])][int(inp[1])][int(inp[2])].snwdQ == "":
                            print("HEADS UP! {} already had no SNWD quality flag".format(clmt[int(inp[0])][int(inp[1])][int(inp[2])].daystr))
                        clmt[int(inp[0])][int(inp[1])][int(inp[2])].snwd = inp[4]
                        clmt[int(inp[0])][int(inp[1])][int(inp[2])].snwdQ = ""
                        fix.append("{},,,{},,".format(clmt[int(inp[0])][int(inp[1])][int(inp[2])].daystr,inp[4]))
                        print("    Amendment for {} SNWD successful: {}".format(clmt[int(inp[0])][int(inp[1])][int(inp[2])].daystr,inp[4]))
                    if inp[3].strip('"') == "tmax":
                        testvalue = int(inp[4])
                        if clmt[int(inp[0])][int(inp[1])][int(inp[2])].tmaxQ == "":
                            print("HEADS UP! {} already had no TMAX quality flag".format(clmt[int(inp[0])][int(inp[1])][int(inp[2])].daystr))
                        clmt[int(inp[0])][int(inp[1])][int(inp[2])].tmax = inp[4]
                        clmt[int(inp[0])][int(inp[1])][int(inp[2])].tmaxQ = ""
                        fix.append("{},,,,{},".format(clmt[int(inp[0])][int(inp[1])][int(inp[2])].daystr,inp[4]))
                        print("    Amendment for {} TMAX successful: {}".format(clmt[int(inp[0])][int(inp[1])][int(inp[2])].daystr,inp[4]))
                    if inp[3].strip('"') == "tmin":
                        testvalue = int(inp[4])
                        if clmt[int(inp[0])][int(inp[1])][int(inp[2])].tminQ == "":
                            print("HEADS UP! {} already had no TMIN quality flag".format(clmt[int(inp[0])][int(inp[1])][int(inp[2])].daystr))
                        clmt[int(inp[0])][int(inp[1])][int(inp[2])].tmin = inp[4]
                        clmt[int(inp[0])][int(inp[1])][int(inp[2])].tminQ = ""
                        fix.append("{},,,,,{}".format(clmt[int(inp[0])][int(inp[1])][int(inp[2])].daystr,inp[4]))
                        print("    Amendment for {} TMIN successful: {}".format(clmt[int(inp[0])][int(inp[1])][int(inp[2])].daystr,inp[4]))
                except:
                    print("Hmm. Double check your input value. Try again")
    if len(fix) > 0:
        with open("APPENDED_" + FILE,"w") as f:
            f.write('"STATION","NAME","LATITUDE","LONGITUDE","ELEVATION","DATE","PRCP","PRCP_ATTRIBUTES","SNOW","SNOW_ATTRIBUTES","SNWD","SNWD_ATTRIBUTES","TMAX","TMAX_ATTRIBUTES","TMIN","TMIN_ATTRIBUTES"\n')
            for yr in [YR for YR in clmt if type(YR) == int]:
                for mo in [MO for MO in clmt[yr] if type(MO) == int]:
                    for dy in [DY for DY in clmt[yr][mo] if type(DY) == int]:
                        f.write('"{}",'.format(clmt[yr][mo][dy].stationid))
                        f.write('"{}",'.format(clmt[yr][mo][dy].station_name))
                        f.write('"{}",'.format(clmt[yr][mo][dy].station_lat))
                        f.write('"{}",'.format(clmt[yr][mo][dy].station_lon))
                        f.write('"{}",'.format(clmt[yr][mo][dy].station_elev))
                        f.write('"{}",'.format(clmt[yr][mo][dy].daystr))
                        f.write('"{}",'.format(clmt[yr][mo][dy].prcp))
                        f.write('"{},{},{},{}",'.format(clmt[yr][mo][dy].prcpM,clmt[yr][mo][dy].prcpQ,clmt[yr][mo][dy].prcpS,clmt[yr][mo][dy].prcpT))
                        f.write('"{}",'.format(clmt[yr][mo][dy].snow))
                        f.write('"{},{},{},{}",'.format(clmt[yr][mo][dy].snowM,clmt[yr][mo][dy].snowQ,clmt[yr][mo][dy].snowS,clmt[yr][mo][dy].snowT))
                        f.write('"{}",'.format(clmt[yr][mo][dy].snwd))
                        f.write('"{},{},{},{}",'.format(clmt[yr][mo][dy].snwdM,clmt[yr][mo][dy].snwdQ,clmt[yr][mo][dy].snwdS,clmt[yr][mo][dy].snwdT))
                        f.write('"{}",'.format(clmt[yr][mo][dy].tmax))
                        f.write('"{},{},{},{}",'.format(clmt[yr][mo][dy].tmaxM,clmt[yr][mo][dy].tmaxQ,clmt[yr][mo][dy].tmaxS,clmt[yr][mo][dy].tmaxT))
                        f.write('"{}",'.format(clmt[yr][mo][dy].tmin))
                        f.write('"{},{},{},{}"\n'.format(clmt[yr][mo][dy].tminM,clmt[yr][mo][dy].tminQ,clmt[yr][mo][dy].tminS,clmt[yr][mo][dy].tminT))
            print("Output of '{}' finished!".format("AMENDED_" + FILE))
    else: return print("::: NO VALUES CHANGED :::")

    if len(fix) > 0:
        timenow = datetime.datetime.now()
        timestr = "{:%Y%m%d_%H%M}".format(timenow)
        with open("CHG_" + timestr + "_" + FILE,"w") as f:
            f.write("{},{},{},{},{},{}\n".format("DAY","PRCP","SNOW","SNWD","TMAX","TMIN"))
            for each in fix:
                f.write(each); f.write("\n")
        print("Output of '{}' finished!".format("CHG_" + timestr + "_" + FILE))

def clmthelp():
    """An extensive list within the script of available functions to the user
    """                                                                                 #
    print("* PLEASE SEE README.md FOR A FULL BREAKDOWN OF PROGRAM'S CAPABILITIES *")
    for x in wrap("* TO START: -When you start, the clmtmenu() function automatically runs. If canceled, simply run the function again. it displays all csv's in the folder",width=78,subsequent_indent="    "): print(x)
    print("            -takes optional keyword argument <city>")
    for x in wrap("CLIMATOLOGY VARIABLES: At the end of the script, you'll see two variables: clmt_len_rpt and clmt_inc_rpt. These are strictly used in the Report functions. The former is to allow the user to modify the length of climatologies (so if you want to assess them at 10, 20, or even 50-yr); the latter controls the frequency of the assessment",width=78,subsequent_indent="    "): print(x)
    print("        clmt_len_rpt = 30   # Default Climatology Length in reports")
    print("        clmt_inc_rpt = 5    # Default running-mean increment")
    for x in wrap("RECORD THRESHOLDS: At the end of the script, you'll find record thresholds. These are controls employed whilst running report/rank functions to prevent partial years/months/weeks from polluting the overall data if it would affect it",width=78,subsequent_indent="    "): print(x)
    print("        DEFAULT VALUES (can be modified before or after compiling the data):")
    print("            excludeyear = 300       # Exclude years from ranking/reports if ")
    print("                                      year recordqty <= to this threshold")
    print("            excludemonth = 20       # Exclude months from ranking/reports if")
    print("                                      month recordqty <= to this threshold")
    print("            excludeweek = 4         # Exclude weeks from ranking/reports if")
    print("                                      week recordqty <= to this threshold")
    print("            excludecustom = .75     # Exclude custom periods from ranking or")
    print("                                      reports if week recordqty <= 75% of a")
    print("                                      threshold")
    print("DAILY SUMMARIES:")
    print("    -- daySummary(y1,m1,d1,*[y2,m2,d2]) :: Dumps a list of day-by-day data in a given range of dates")
    print("ERRORS OVERVIEW:")
    print("    -- Run qflagCheck() to get the code and definition for various quality flags in the record")
    print("    -- Run errorStats() to get get a report on errors that might be worth veryfying the data for.")
    print("           * this function will report on every error unless it is a temperature with an 'I' flag.")
    print("               - These can be quite numerous. So won't be included in the report")
    print("           * by default, data with any type of quality flag will NOT be included in stats/reports")
    print("           * User can change these settings by one of two ways:")
    print("               - Find where the 'ignoreflags' list is in the script, and add or take away from the list")
    print("               - On the fly, with the command ignoreflags.append('<flag>') or ignoreflags.remove('<flag>')")
    print("           * using corrections(), It is possible to verify the data and remove the quality flag so it will be included")
    print("               - this process amends the data and outputs a new file; reload using clmtAnalyze() for best results")
    print("           * Please see README.md to read more about this process")
    print("BUILT-IN FUNCTIONS: (these won't work until you run the clmtAnalyze function)")
    print("    -- dayStats(year,month,day) :: Returns a basic report for the specified day")
    print("    -- weekStats(year,month,day) :: Returns a basic weekly report; the included day will be the ")
    print("       center of the week")
    print("    -- monthStats(year,month) :: Returns a basic report for the specified month")
    print("    -- yearStats(year) :: Returns a basic report for the specified year")
    print("    -- metYearStats(year) :: Returns a basic report for the specified meteorological year")
    print("    -- seasonStats(year,season) :: Returns a basic report for the specified meteorological ")
    print("       season ('spring','summer','fall','winter')")
    print("    -- customStats(y1,m1,d1,*y2,*m2,*d2)")
    print("    Climatology Functions :: Detailed stats based on 30-yr climatologies incremented by")
    print("       5 years and enables basic climatological tendency analysis")
    print("    -- dayReport(month,day) :: Returns detailed statistics and climatology for all specified")
    print("       days in the record")
    print("    -- weekReport(month,day) :: Returns detailed statistics and climatology for determined 7-day")
    print("       period and the included day will be the center of the week")
    print("    -- monthReport(month) :: Returns detailed statistics and climatology for the specified month")
    print("    -- yearReport() :: NOTHING is passed to this function. It returns detailed statistics based ")
    print("       on data for all years")
    print("    -- metYearReport() :: NOTHING is passed to this function. It returns detailed statistics based ")
    print("       on data for all meteorological years")
    print("    -- seasonReport(season) :: Returns detailed statistics and climatology for the specified season")
    print("    -- customReport(M1,D1,*[M2,D2]) :: Returns detailed statistics and climatology for the specified,")
    print("       custom period of time. The ending month and date are optional")
    print("    Rank/Record Functions")
    print("    -- dayRank(month,day,howmany) :: Prints daily records from the climate data.")
    print("    -- weekRank(month,day,howmany) :: Prints records based on a week's period, centered on the ")
    print("       day entered (3 days before; 3 after)")
    print("    -- monthRank(month,'<temps>|<rain>',howmany) :: Prints month-based records for the given month")
    print("    -- yearRank('<temps>|<rain>',howmany) :: Prints yearly-based records for the entire record (Jan-Dec)")
    print("    -- metYearRank('<temps>|<rain>',howmany) :: Prints meteorological-yearly-based records for the ")
    print("       entire record (Jan-Dec)")
    print("    -- seasonRank(season,'<temps>|<rain>',howmany) :: Prints season-based records for the inquired season")
    print("    -- customRank(attribute,quantity,M1,D1,*[M2,D2]) :: Prints ranked-records for the inquired period of time")
    print("       The ending date is optional. This is a good function for proxy of a YTD function")
    print("    -- allDayRank('attribute',quantity,**{season,year,month,ascending}) :: compares all daily data on record.")
    print("       optional temporal keyword arguments accepted")
    print("    -- allMonthRank(attribute,quantity,**{season,ascending}) :: compares all monthly data on record to one")
    print("       another. Optional keyword arguments of <season> or <ascending=True> are accepted")

def clmtmenu():
    """Enables the user to select which csv file (as such, which city) that
    they'd like to load/mount into the program; automatically ran at
    initilization of the script, but can be ran at anytime; replaces the
    csvFileList() function.
    
    clmtmenu()    
    """
    tempcsvlist = os.listdir()
    csvs_in_dir = [x for x in tempcsvlist if x[len(x)-3:] == "csv" and x[0:9] not in ["dayReport","weekRepor","monthRepo","yearRepor","seasonRep","metYearRe","customRep"]]
    selection = False   # Will cause the function to wait until an accepted answer is input
    print("**********************************************************")
    print("          CLIMATE PARSER (clmt-parser.py) v2.91")
    print("                  by K. Gentry (ksgwxfan)")
    print("**********************************************************")
    print("- Make selection and press <ENTER>; type-in cancel to exit function")
    print("- Run this function again by entering clmtmenu()")
    print("- OPTIONAL: enter in a custom city name (useful if the file has")
    print("      multiple stations). Just separate by a comma.")
    print("      Example -->   Enter Selection: 2, CITY")
    print("-----------------------------------------------------------")
    for each in csvs_in_dir:
        print("{:>3}. {}".format(csvs_in_dir.index(each) + 1,each))
    print("-----------------------------------------------------------")
    while selection == False:   # only jumps out of while-loop if answer is valids
        userselection = input("Enter Selection: ")
        userselection = userselection.split(",")
        if userselection[0].isnumeric() and int(userselection[0]) > 0 and int(userselection[0]) <= len(csvs_in_dir) or userselection[0].lower() == "cancel":
            selection = True
        else: print("OOPS! Invalid selection. Try again!")
        if len(userselection) >= 2:
            citystr = userselection[1].strip(" ")
            for x in range(2,len(userselection)):
                citystr = citystr + ", " + userselection[x].strip(" ")
    if userselection[0].lower() != "cancel":
        if len(userselection) == 1: clmtAnalyze(csvs_in_dir[int(userselection[0])-1])
        else:
            #citystr = userselection[1].strip(" ") + ", " + userselection[2].strip(" ")
            clmtAnalyze(csvs_in_dir[int(userselection[0])-1],city=citystr)

# MAIN PROGRAM --------------------------------------------------------------
clmt = {}
metclmt = {}
clmt_vars_days = {"prcp":{},"snow":{},"snwd":{},"tavg":{},"tmax":{},"tmin":{}}
clmt_vars_months = {"prcp":{},"prcpDAYS":{},"snow":{},"snowDAYS":{},"snwd":{},"snwdDAYS":{},"tavg":{},"tmax":{},"tmin":{}}
station_ids = []
FILE = None

# Climatology Report-related variables
clmt_len_rpt = 30   # Default Climatology Length respected in reports (x-yr climatology)
clmt_inc_rpt = 5    # Default "running"-mean increment (tendency frequency? i guess)

# Threshold Quantities
ignoreflags = [""]      # If there are Quality Flags that you wish to ignore, place them here (or append upon starting; see README)
excludeyear = 300       # Exclude years from ranking/reports if year recordqty <= to this threshold
excludeseason = 70      # Exclude season from rankings/reports if season recordqty <= to this threshold
excludemonth = 20       # Exclude months from ranking/reports if month recordqty <= to this threshold
excludeweek = 4         # Exclude weeks from ranking/reports if week recordqty <= to this threshold
excludecustom = .75     # Excludes custom periods if recordqty isn't at least this percentage of threshold

# tempAVGlist Threshold Quantities (DO NOT TOUCH!!! these are handled from above variables)
excludeyear_tavg = excludeyear * 2
excludeseason_tavg = excludeseason * 2
excludemonth_tavg = excludemonth * 2
excludeweek_tavg = excludeweek * 2

clmtmenu()

# li = sorted([{"year":y,"month":m,"snwdDAYS":clmt[y][m]["snwdDAYS"]} for y in clmt if type(y) == int for m in clmt[y] if type(m) == int and clmt[y][m]["snwdDAYS"] > 0],key=lambda x:x["snwdDAYS"],reverse=True)