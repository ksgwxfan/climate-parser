import datetime
from time import time
import calendar
from statistics import mean, pstdev
import csv
import os

class DayRecord:
    def __init__(self,raw):
        self.stationid = raw[0]
        self.station_name = raw[1]
        self.station_lat = raw[2]
        self.station_lon = raw[3]
        self.station_elev = raw[4]
        ry = int(raw[5][0:4])
        rm = int(raw[5][5:7])
        rd = int(raw[5][8:10])
        self.daystr = "{}-{}-{}".format(ry,str(rm).zfill(2),str(rd).zfill(2))
        self.entryday = datetime.date(ry,rm,rd)
        # PRCP - Precipitation
        self.prcp = raw[6]
        flags_prcp = raw[7].split(",")
        self.prcpM, self.prcpQ, self.prcpS, self.prcpT = attchk(flags_prcp)
        # SNOW - Snow
        self.snow = raw[8]
        flags_snow = raw[9].split(",")
        self.snowM, self.snowQ, self.snowS, self.snowT = attchk(flags_snow)
        # SNWD - Snow Depth
        self.snwd = raw[10]
        flags_snwd = raw[11].split(",")
        self.snwdM, self.snwdQ, self.snwdS, self.snwdT = attchk(flags_snwd)
        # TMAX - Maximum Temperature
        self.tmax = raw[12]
        flags_tmax = raw[13].split(",")
        self.tmaxM, self.tmaxQ, self.tmaxS, self.tmaxT = attchk(flags_tmax)
        # TMIN - Minimum Temperature
        self.tmin = raw[14]
        flags_tmin = raw[15].split(",")
        self.tminM, self.tminQ, self.tminS, self.tminT = attchk(flags_tmin)

def clmtAnalyze(filename,**CITY):
    if os.path.isfile(filename) == False: return print('"{}" not found! Try again!'.format(filename))
    global clmt
    global FILE
    FILE = filename
    clmt = {}
    START = time()
    print("*** Script Running. Please Wait ***")

    with open(filename,newline="") as f:
        print("--- COMPILING DICTIONARIES ---")
        csvfile = csv.reader(f, delimiter=',')
        for each in csvfile:
            if each[0] in ["STATION",'"STATION"']:
                pass
            else:
                if "station" not in clmt:
                    if "city" in CITY: clmt["station_name"] = CITY["city"]
                    else: clmt["station_name"] = each[1]
                    if "station" in CITY: clmt["station"] = CITY["station"]
                    else: clmt["station"] = each[0]
                    print("--- City: {} ---".format(clmt["station_name"]))
                    clmt["coordinates"] = "{}, {}".format(each[2],each[3])
                    clmt["elevation"] = each[4]
                #if y % 10 == 0: print("{},".format(each[5][0:4]),end=" ")
                y = int(each[5][0:4])
                m = int(each[5][5:7])
                d = int(each[5][8:10])
                if y not in clmt:   # YEAR
                    clmt[y] = {}
                if m not in clmt[y]:   # MONTH
                    clmt[y][m] = {}
                # DAY Record stuff
                if d in clmt[y][m]:    # Skipped if a record entry has already been made for that date
                    pass
                else:
                    clmt[y][m][d] = DayRecord(each)
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
                    if "tmax" not in clmt[y]:
                        clmt[y]["tempAVGlist"] = []
                        clmt[y]["tmax"] = []
                        clmt[y]["tmaxPROP"] = {"day_max":[-999,[]],"day_min":[999,[]],"month_AVG_max":[-999,"n/a"],"month_AVG_min":[999,"n/a"]}
                    if "tmax" not in clmt[y][m]:
                        clmt[y][m]["tempAVGlist"] = []
                        clmt[y][m]["tmax"] = []
                        clmt[y][m]["tmaxPROP"] = {"day_max":[-999,[]],"day_min":[999,[]]}
                    if "tmin" not in clmt[y]:
                        clmt[y]["tmin"] = []
                        clmt[y]["tminPROP"] = {"day_max":[-999,[]],"day_min":[999,[]],"month_AVG_max":[-999,"n/a"],"month_AVG_min":[999,"n/a"]}
                    if "tmin" not in clmt[y][m]:
                        clmt[y][m]["tmin"] = []
                        clmt[y][m]["tminPROP"] = {"day_max":[-999,[]],"day_min":[999,[]]}
                    if clmt[y][m][d].tmaxQ in ignoreflags and clmt[y][m][d].tmax not in ["9999","-9999",""]:
                        if clmt[y][m][d].tmin != "" and int(clmt[y][m][d].tmax) >= int(clmt[y][m][d].tmin):
                            clmt[y]["tmax"].append(int(clmt[y][m][d].tmax))
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
                            clmt[y][m]["tmax"].append(int(clmt[y][m][d].tmax))
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
                        if clmt[y][m][d].tmax != "" and int(clmt[y][m][d].tmin) <= int(clmt[y][m][d].tmax):
                            clmt[y]["tmin"].append(int(clmt[y][m][d].tmin))
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
                            clmt[y][m]["tmin"].append(int(clmt[y][m][d].tmin))
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

    # MONTHLY STATS
    for y in [YR for YR in clmt if type(YR) == int]:
        for m in [MO for MO in clmt[y] if type(MO) == int]:
            # PRCP
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
            try:
                if round(sum(clmt[y][m]["snow"]),1) == clmt[y]["snowPROP"]["month_max"][0]:
                    clmt[y]["snowPROP"]["month_max"][1].append(m)
                elif round(sum(clmt[y][m]["snow"]),1) > clmt[y]["snowPROP"]["month_max"][0]:
                    clmt[y]["snowPROP"]["month_max"][0] = round(sum(clmt[y][m]["snow"]),1)
                    clmt[y]["snowPROP"]["month_max"][1] = []
                    clmt[y]["snowPROP"]["month_max"][1].append(m)
            except:
                print("*** SKIPPED: Insufficient or erroneous SNOW data - {}-{}".format(y,str(m).zfill(2)))
            # TMAX
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
    END = time()
    print("*** SCRIPT COMPLETE ***")
    print("Runtime: {} seconds".format(round(END - START,2)))

def attchk(attstr):
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
                    print("Day: {}; PRCP: {}; Quality Flag (prcpQ): {}".format(y.daystr,y.prcp,qflagCheck(y.prcpQ)))
            if x == 1:
                if y.snowQ not in [i for i in ignoreflags if i != "I"] or y.snow in ["9999","-9999"]:
                    print("Day: {}; SNOW: {}; Quality Flag (snowQ): {}".format(y.daystr,y.snow,qflagCheck(y.snowQ)))
            if x == 2:
                if y.snwdQ not in ignoreflags or y.snwd in ["9999","-9999"]:
                    print("Day: {}; SNWD: {}; Quality Flag (snwdQ): {}".format(y.daystr,y.snwd,qflagCheck(y.snwdQ)))
            if x == 3:
                if y.tmaxQ not in ignoreflags and y.tmaxQ != "I" or y.tmax in ["9999","-9999"]:
                    print("Day: {}; TMAX: {}; Quality Flag (tmaxQ): {}".format(y.daystr,y.tmax,qflagCheck(y.tmaxQ)))
            if x == 4:
                if y.tminQ not in ignoreflags and y.tminQ != "I" or y.tmax in ["9999","-9999"]:
                    print("Day: {}; TMIN: {}; Quality Flag (tminQ): {}".format(y.daystr,y.tmin,qflagCheck(y.tminQ)))

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

def checkDate(*args):
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

def qflagCheck(*q):
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

def dayStats(y,m,d):
    ranks = ["th","st","nd","rd","th","th","th","th","th","th"]
    if len(clmt) == 0: return print("* OOPS! Run the clmtAnalyze function first.")
    dayExists = checkDate(y,m,d)
    if dayExists:
        dayobj = clmt[y][m][d]
        print("Statistics for {}".format(dayobj.entryday))
        print("{}: {}".format(clmt["station"],clmt["station_name"]))
        print("-------------------")
        if dayobj.prcpM == "T":     # PRCP - Trace Amount
            if dayobj.prcpQ != "": print("PRCP: T, Flag: {} - {}".format(dayobj.prcpQ,qflagCheck(dayobj.prcpQ)))
            else: print("PRCP: T")
        else:   # PRCP - 0 or greater; no trace
            prcphist = sorted(list(set(list(round(float(clmt[Y][m][d].prcp),2) for Y in clmt if type(Y) == int and m in clmt[Y] and d in clmt[Y][m] and clmt[Y][m][d].prcp != "" and float(clmt[Y][m][d].prcp) != 0 and clmt[Y][m][d].prcpQ == ""))),reverse=True)
            if dayobj.prcpQ != "":  # if PRCP has an error flag
                if float(dayobj.prcp) == 0: print("PRCP: {}, Flag: {} - {}".format(dayobj.prcp,dayobj.prcpQ,qflagCheck(dayobj.prcpQ)))
                else: print("PRCP: {}, Rank: {}, Flag: {} - {}".format(dayobj.prcp,prcphist.index(round(float(dayobj.prcp),2))+1,dayobj.prcpQ,qflagCheck(dayobj.prcpQ)))
            else: # NO error Flag
                if float(dayobj.prcp) == 0: print("PRCP: {}".format(dayobj.prcp))
                else: print("PRCP: {}, Rank: {}".format(dayobj.prcp,prcphist.index(round(float(dayobj.prcp),2))+1))
        if dayobj.snowM != "" or dayobj.snow != "" and float(dayobj.snow) != 0:
            if dayobj.snowM == "T":     # SNOW - Trace
                if dayobj.snowQ != "": print("SNOW: T, Flag: {} - {}".format(dayobj.snowQ,qflagCheck(dayobj.snowQ)))
                else: print("SNOW: T")
            else: # Snow - 0 or more; no trace recorded
                snowhist = sorted(list(set(list(round(float(clmt[Y][m][d].snow),1) for Y in clmt if type(Y) == int and m in clmt[Y] and d in clmt[Y][m] and clmt[Y][m][d].snow != "" and float(clmt[Y][m][d].snow) != 0 and clmt[Y][m][d].snowQ == ""))),reverse=True)
                if dayobj.snowQ != "": # if SNOW has an error flag
                    if float(dayobj.snow) == 0: print("SNOW: {}, Flag: {} - {}".format(dayobj.snow,dayobj.snowQ,qflagCheck(dayobj.snowQ)))
                    else: print("SNOW: {}, Rank: {}, Flag: {} - {}".format(dayobj.snow,snowhist.index(round(float(dayobj.snow),1))+1,dayobj.snowQ,qflagCheck(dayobj.snowQ)))
                else: # No error flag
                    if float(dayobj.snow) == 0: print("SNOW: {}".format(dayobj.snow))
                    else: print("SNOW: {}, Rank: {}".format(dayobj.snow,snowhist.index(round(float(dayobj.snow),1))+1))
        if dayobj.snwd != "" and float(dayobj.snwd) > 0:
            if dayobj.snwdM == "T":     # snwd - Trace
                if dayobj.snwdQ != "": print("SNWD: T, Flag: {} - {}".format(dayobj.snwdQ,qflagCheck(dayobj.snwdQ)))
                else: print("SNWD: T")
            else: # snwd - 0 or more; no trace recorded
                snwdhist = sorted(list(set(list(round(float(clmt[Y][m][d].snwd),1) for Y in clmt if type(Y) == int and m in clmt[Y] and d in clmt[Y][m] and clmt[Y][m][d].snwd != "" and float(clmt[Y][m][d].snwd) != 0 and clmt[Y][m][d].snwdQ == ""))),reverse=True)
                if dayobj.snwdQ != "": # if snwd has an error flag
                    if float(dayobj.snwd) == 0: print("SNWD: {}, Flag: {} - {}".format(dayobj.snwd,dayobj.snwdQ,qflagCheck(dayobj.snwdQ)))
                    else: print("SNWD: {}, Rank: {}, Flag: {} - {}".format(dayobj.snwd,snwdhist.index(round(float(dayobj.snwd),1))+1,dayobj.snwdQ,qflagCheck(dayobj.snwdQ)))
                else: # No error flag
                    if float(dayobj.snwd) == 0: print("snwd: {}".format(dayobj.snwd))
                    else: print("SNWD: {}, Rank: {}".format(dayobj.snwd,snwdhist.index(round(float(dayobj.snwd),1))+1))
        tmaxdeschist = sorted(list(set(list(int(clmt[Y][m][d].tmax) for Y in clmt if type(Y) == int and m in clmt[Y] and d in clmt[Y][m] and clmt[Y][m][d].tmax != "" and clmt[Y][m][d].tmaxQ == ""))),reverse=True)
        tmaxaschist = sorted(list(set(list(int(clmt[Y][m][d].tmax) for Y in clmt if type(Y) == int and m in clmt[Y] and d in clmt[Y][m] and clmt[Y][m][d].tmax != "" and clmt[Y][m][d].tmaxQ == ""))))
        if dayobj.tmaxQ != "": # TMAX Error flag
            if dayobj.tmax == "": print("TMAX: N/A, Flag: {} - {}".format(dayobj.tmax,dayobj.tmaxQ,qflagCheck(dayobj.tmaxQ)))
            else: # if temp was recorded
                print("TMAX: {}, Rank: {}{} Warmest; {}{} Coolest, Flag: {} - {}".format(dayobj.tmax,
             tmaxdeschist.index(int(dayobj.tmax))+1,
             ranks[int(str(tmaxdeschist.index(int(dayobj.tmax))+1)[len(str(tmaxdeschist.index(int(dayobj.tmax))+1))-1])] if tmaxdeschist.index(int(dayobj.tmax))+1 not in [11,12,13] else "th",
             tmaxaschist.index(int(dayobj.tmax))+1,
             ranks[int(str(tmaxaschist.index(int(dayobj.tmax))+1)[len(str(tmaxaschist.index(int(dayobj.tmax))+1))-1])] if tmaxaschist.index(int(dayobj.tmax))+1 not in [11,12,13] else "th",
             dayobj.tmaxQ,
             qflagCheck(dayobj.tmaxQ)))
        else: # no TMAX error flag
            if dayobj.tmax == "": print("TMAX: N/A".format(dayobj.tmax))
            else: # if temp was recorded
                print("TMAX: {}, Rank: {}{} Warmest; {}{} Coolest".format(dayobj.tmax,
             tmaxdeschist.index(int(dayobj.tmax))+1,
             ranks[int(str(tmaxdeschist.index(int(dayobj.tmax))+1)[len(str(tmaxdeschist.index(int(dayobj.tmax))+1))-1])] if tmaxdeschist.index(int(dayobj.tmax))+1 not in [11,12,13] else "th",
             tmaxaschist.index(int(dayobj.tmax))+1,
             ranks[int(str(tmaxaschist.index(int(dayobj.tmax))+1)[len(str(tmaxaschist.index(int(dayobj.tmax))+1))-1])] if tmaxaschist.index(int(dayobj.tmax))+1 not in [11,12,13] else "th"))
        tmindeschist = sorted(list(set(list(int(clmt[Y][m][d].tmin) for Y in clmt if type(Y) == int and m in clmt[Y] and d in clmt[Y][m] and clmt[Y][m][d].tmin != "" and clmt[Y][m][d].tminQ == ""))),reverse=True)
        tminaschist = sorted(list(set(list(int(clmt[Y][m][d].tmin) for Y in clmt if type(Y) == int and m in clmt[Y] and d in clmt[Y][m] and clmt[Y][m][d].tmin != "" and clmt[Y][m][d].tminQ == ""))))
        if dayobj.tminQ != "": # tmin Error flag
            if dayobj.tmin == "": print("TMIN: N/A, Flag: {} - {}".format(dayobj.tmin,dayobj.tminQ,qflagCheck(dayobj.tminQ)))
            else: # if temp was recorded
                print("TMIN: {}, Rank: {}{} Warmest; {}{} Coolest, Flag: {} - {}".format(dayobj.tmin,
         tmindeschist.index(int(dayobj.tmin))+1,
         ranks[int(str(tmindeschist.index(int(dayobj.tmin))+1)[len(str(tmindeschist.index(int(dayobj.tmin))+1))-1])] if tmindeschist.index(int(dayobj.tmin))+1 not in [11,12,13] else "th",
         tminaschist.index(int(dayobj.tmin))+1,
         ranks[int(str(tminaschist.index(int(dayobj.tmin))+1)[len(str(tminaschist.index(int(dayobj.tmin))+1))-1])] if tminaschist.index(int(dayobj.tmin))+1 not in [11,12,13] else "th",
         dayobj.tminQ,
         qflagCheck(dayobj.tminQ)))
        else: # no tmin error flag
            if dayobj.tmin == "": print("TMIN: N/A".format(dayobj.tmin))
            else: # if temp was recorded
                print("TMIN: {}, Rank: {}{} Warmest; {}{} Coolest".format(dayobj.tmin,
         tmindeschist.index(int(dayobj.tmin))+1,
         ranks[int(str(tmindeschist.index(int(dayobj.tmin))+1)[len(str(tmindeschist.index(int(dayobj.tmin))+1))-1])] if tmindeschist.index(int(dayobj.tmin))+1 not in [11,12,13] else "th",
         tminaschist.index(int(dayobj.tmin))+1,
         ranks[int(str(tminaschist.index(int(dayobj.tmin))+1)[len(str(tminaschist.index(int(dayobj.tmin))+1))-1])] if tminaschist.index(int(dayobj.tmin))+1 not in [11,12,13] else "th"))
        try:
            if int(dayobj.tmax) < int(dayobj.tmin): print("*** CHECK DATA: TMIN > TMAX ***")
        except:
            pass

def weekStats(y,m,d):
    if len(clmt) == 0: return print("* OOPS! Run the clmtAnalyze function first.")
    wkstart = datetime.date(y,m,d) - datetime.timedelta(days=3)
    c = wkstart
    wkend = datetime.date(y,m,d) + datetime.timedelta(days=3)
    w_prcp = 0
    w_prcpDAYS = 0
    w_snow = 0
    w_snowDAYS = 0
    w_snwd = []
    w_tmax = []
    w_tmin = []
    w_alltemps = []
    records_in_week = 0
    weekExists = checkDate(y,m,d)
    if weekExists:
        for x in range(7):
            try:
                if clmt[c.year][c.month][c.day]: records_in_week += 1
                if clmt[c.year][c.month][c.day].prcpQ in ignoreflags and clmt[c.year][c.month][c.day].prcp not in ["9999","-9999",""]:
                    w_prcp += float(clmt[c.year][c.month][c.day].prcp)
                    if float(clmt[c.year][c.month][c.day].prcp) > 0 or clmt[c.year][c.month][c.day].prcpM == "T": w_prcpDAYS += 1
                if clmt[c.year][c.month][c.day].snowQ in ignoreflags and clmt[c.year][c.month][c.day].snow not in ["9999","-9999",""]:
                    w_snow += float(clmt[c.year][c.month][c.day].snow)
                    if float(clmt[c.year][c.month][c.day].snow) > 0 or clmt[c.year][c.month][c.day].snowM == "T": w_snowDAYS += 1
                if clmt[y][m][d].tmaxQ in ignoreflags and clmt[y][m][d].tmax not in ["9999","-9999",""]:
                    w_tmax.append(int(clmt[y][m][d].tmax))
                if clmt[y][m][d].tminQ in ignoreflags and clmt[y][m][d].tmin not in ["9999","-9999",""]:
                    w_tmin.append(int(clmt[y][m][d].tmin))
                if clmt[y][m][d].tmaxQ in ignoreflags and clmt[y][m][d].tmax not in ["9999","-9999",""] and clmt[y][m][d].tminQ in ignoreflags and clmt[y][m][d].tmin not in ["9999","-9999",""]:
                    w_alltemps.append(int(clmt[y][m][d].tmax))
                    w_alltemps.append(int(clmt[y][m][d].tmin))
            except KeyError:
                continue
            c += datetime.timedelta(days=1)

        if records_in_week <= 4:
            print("-------------------------------------")
            print("*** WEEKLY STATS LIKELY UNDERREPRESENTED ***")

        print("-------------------------------------")
        print("Weekly Statistics for {} thru {}".format(wkstart,wkend))
        print("{}: {}".format(clmt["station"],clmt["station_name"]))
        print("Quantity of Records: {}".format(records_in_week))
        print("-----")
        print("Total Precipitation: {}".format(round(w_prcp,2)))
        print("Total Precipitation Days (>= T): {}".format(w_prcpDAYS))
        if w_snowDAYS >= 1:
            print("Total Snow: {}".format(round(w_snow,2)))
            print("Total Snow Days (>= T): {}".format(w_snowDAYS))
        if records_in_week > 4 and (len(w_tmax) <= 4 or len(w_tmin) <= 4): print("*** TEMPERATURE STATS LIKELY UNDERREPRESENTED ***")
        try:
            print("Average Temperature: {}".format(round(mean(w_alltemps),2)))
        except:
            print("Average Max Temperature: N/A")
        try:
            print("Average Max Temperature: {}".format(round(mean(w_tmax),2)))
        except:
            print("Average Max Temperature: N/A")
        try:
            print("Average Min Temperature: {}".format(round(mean(w_tmin),2)))
        except:
            print("Average Min Temperature: N/A")
        print("-----")
    

def monthStats(y,m):
    if len(clmt) == 0: return print("* OOPS! Run the clmtAnalyze function first.")
    monthExists = checkDate(y,m)
    if monthExists:
        if clmt[y][m]["recordqty"] < 20:
            print("-------------------------------------")
            print("*** MONLTHLY STATS MAY NOT BE COMPLETE FOR RELIANCE ON STATISTICS ***")

        print("-------------------------------------")
        print("Monthly Statistics for {} {}".format(calendar.month_name[m],y))
        print("{}: {}".format(clmt["station"],clmt["station_name"]))
        print("Quantity of Records: {}".format(clmt[y][m]["recordqty"]))
        print("-----")
        try:
            print("Total Precipitation: {}".format(round(sum(clmt[y][m]["prcp"]),2)))
            print("Total Precipitation Days (>= T): {}".format(clmt[y][m]["prcpDAYS"]))
            if round(sum(clmt[y][m]["prcp"]),2) > 0:
                print("-- Highest Precip: {}".format(clmt[y][m]["prcpPROP"]["day_max"][0]),end=" ::: ")
                for x in range(len(clmt[y][m]["prcpPROP"]["day_max"][1])):
                    if x != len(clmt[y][m]["prcpPROP"]["day_max"][1])-1: print("{},".format(clmt[y][m]["prcpPROP"]["day_max"][1][x].daystr),end=" ")
                    else: print("{}".format(clmt[y][m]["prcpPROP"]["day_max"][1][x].daystr))
        except:
            print("*** No Reliable PRCP data recorded for month ***")
        try:
            if round(sum(clmt[y][m]["snow"]),2) > 0 or clmt[y][m]["snowDAYS"] > 0:
                print("Total Snow: {}".format(round(sum(clmt[y][m]["snow"]),2)))
                print("Total Snow Days (>= T): {}".format(clmt[y][m]["snowDAYS"]))
                if clmt[y][m]["snowPROP"]["day_max"][0] > 0:
                    print("-- Highest Snow: {}".format(clmt[y][m]["snowPROP"]["day_max"][0]),end=" ::: ")
                    for x in range(len(clmt[y][m]["snowPROP"]["day_max"][1])):
                        if x != len(clmt[y][m]["snowPROP"]["day_max"][1])-1: print("{},".format(clmt[y][m]["snowPROP"]["day_max"][1][x].daystr),end=" ")
                        else: print("{}".format(clmt[y][m]["snowPROP"]["day_max"][1][x].daystr))
        except:
            pass    # Means no snow data for month
        try:
            print("Average Temperature: {}".format(round(mean(clmt[y][m]["tempAVGlist"]),1)))
            print("Average Max Temperature: {}".format(round(mean(clmt[y][m]["tmax"]),1)))
            print("-- Warmest Max Temperature: {}".format(clmt[y][m]["tmaxPROP"]["day_max"][0]),end=" ::: ")
            for x in range(len(clmt[y][m]["tmaxPROP"]["day_max"][1])):
                if x != len(clmt[y][m]["tmaxPROP"]["day_max"][1])-1: print("{},".format(clmt[y][m]["tmaxPROP"]["day_max"][1][x].daystr),end=" ")
                else: print("{}".format(clmt[y][m]["tmaxPROP"]["day_max"][1][x].daystr))
                
            #print([x.daystr for x in clmt[y][m]["tmaxPROP"]["day_max"][1]])
            print("-- Coolest Max Temperature: {}".format(clmt[y][m]["tmaxPROP"]["day_min"][0]),end=" ::: ")
            for x in range(len(clmt[y][m]["tmaxPROP"]["day_min"][1])):
                if x != len(clmt[y][m]["tmaxPROP"]["day_min"][1])-1: print("{},".format(clmt[y][m]["tmaxPROP"]["day_min"][1][x].daystr),end=" ")
                else: print("{}".format(clmt[y][m]["tmaxPROP"]["day_min"][1][x].daystr))
            print("Average Min Temperature: {}".format(round(mean(clmt[y][m]["tmin"]),1)))
            print("-- Warmest Min Temperature: {}".format(clmt[y][m]["tminPROP"]["day_max"][0]),end=" ::: ")
            for x in range(len(clmt[y][m]["tminPROP"]["day_max"][1])):
                if x != len(clmt[y][m]["tminPROP"]["day_max"][1])-1: print("{},".format(clmt[y][m]["tminPROP"]["day_max"][1][x].daystr),end=" ")
                else: print("{}".format(clmt[y][m]["tminPROP"]["day_max"][1][x].daystr))
            print("-- Coolest Min Temperature: {}".format(clmt[y][m]["tminPROP"]["day_min"][0]),end=" ::: ")
            for x in range(len(clmt[y][m]["tminPROP"]["day_min"][1])):
                if x != len(clmt[y][m]["tminPROP"]["day_min"][1])-1: print("{},".format(clmt[y][m]["tminPROP"]["day_min"][1][x].daystr),end=" ")
                else: print("{}".format(clmt[y][m]["tminPROP"]["day_min"][1][x].daystr))
        except:
            print("*** No Reliable Temperature Data for {} {}".format(calendar.month_abbr[m],y))
        print("-----")

def yearStats(y):
    if len(clmt) == 0: return print("* OOPS! Run the clmtAnalyze function first.")
    # clmt[int(each[2][0:4])]["prcpPROP"] = {"day_max":[-1,[]],"month_max":[-1,[]],"month_min":[999,[]]}
    # clmt[int(each[2][0:4])]["snowPROP"] = {"day_max":[-1,[]],"month_max":[-1,[]]}
    # clmt[int(each[2][0:4])]["tempAVGlist"] = []
    # clmt[int(each[2][0:4])]["tmax"] = []
    # clmt[int(each[2][0:4])]["tmaxPROP"] = {"day_max":[-999,[]],"day_min":[999,[]],"month_AVG_max":[-999,"n/a"],"month_AVG_min":[999,"n/a"]}
    yearExists = checkDate(y)
    if yearExists:
        if clmt[y]["recordqty"] <= 300:
            print("-------------------------------------")
            print("*** YEAR STATS MAY NOT BE COMPLETE FOR RELIANCE ON STATISTICS ***")
        print("-------------------------------------")
        print("Yearly Statistics for {}".format(y))
        print("{}: {}".format(clmt["station"],clmt["station_name"]))
        print("Quantity of Records: {}".format(clmt[y]["recordqty"]))
        print("-----")
        try:
            print("Total Precipitation: {}".format(round(sum(clmt[y]["prcp"]),2)))
            print("Total Precipitation Days (>= T): {}".format(clmt[y]["prcpDAYS"]))
            if sum(clmt[y]["prcp"]) > 0:
                print("-- Highest Daily Precip: {}".format(clmt[y]["prcpPROP"]["day_max"][0]),end=" ::: ")
                for x in range(len(clmt[y]["prcpPROP"]["day_max"][1])):
                    if x != len(clmt[y]["prcpPROP"]["day_max"][1])-1: print("{},".format(clmt[y]["prcpPROP"]["day_max"][1][x].daystr),end=" ")
                    else: print("{}".format(clmt[y]["prcpPROP"]["day_max"][1][x].daystr))
                print("-- Wettest Month: {}".format(round(clmt[y]["prcpPROP"]["month_max"][0],2)),end=" ::: ")
                for x in range(len(clmt[y]["prcpPROP"]["month_max"][1])):
                    if x != len(clmt[y]["prcpPROP"]["month_max"][1])-1: print("{},".format(calendar.month_name[clmt[y]["prcpPROP"]["month_max"][1][x]]),end=" ")
                    else: print("{}".format(calendar.month_name[clmt[y]["prcpPROP"]["month_max"][1][x]]))
                print("-- Driest Month: {}".format(round(clmt[y]["prcpPROP"]["month_min"][0],2)),end=" ::: ")
                for x in range(len(clmt[y]["prcpPROP"]["month_min"][1])):
                    if x != len(clmt[y]["prcpPROP"]["month_min"][1])-1: print("{},".format(calendar.month_name[clmt[y]["prcpPROP"]["month_min"][1][x]]),end=" ")
                    else: print("{}".format(calendar.month_name[clmt[y]["prcpPROP"]["month_min"][1][x]]))
        except:
            print("*** No Reliable PRCP data recorded for month ***")
        try:
            if sum(clmt[y]["snow"]) > 0 or clmt[y]["snowDAYS"] > 0:
                print("Total Snow: {}".format(round(sum(clmt[y]["snow"]),1)))
                print("Total Snow Days (>= T): {}".format(clmt[y]["snowDAYS"]))
                if clmt[y]["snowPROP"]["day_max"][0] > 0:
                    print("-- Highest Daily Snow: {}".format(clmt[y]["snowPROP"]["day_max"][0]),end=" ::: ")
                    for x in range(len(clmt[y]["snowPROP"]["day_max"][1])):
                        if x != len(clmt[y]["snowPROP"]["day_max"][1])-1: print("{},".format(clmt[y]["snowPROP"]["day_max"][1][x].daystr),end=" ")
                        else: print("{}".format(clmt[y]["snowPROP"]["day_max"][1][x].daystr))
                    print("-- Snowiest Month: {}".format(round(clmt[y]["snowPROP"]["month_max"][0],2)),end=" ::: ")
                    for x in range(len(clmt[y]["snowPROP"]["month_max"][1])):
                        if x != len(clmt[y]["snowPROP"]["month_max"][1])-1: print("{},".format(calendar.month_name[clmt[y]["snowPROP"]["month_max"][1][x]]),end=" ")
                        else: print("{}".format(calendar.month_name[clmt[y]["snowPROP"]["month_max"][1][x]]))
        except:
            pass    # Means no snow data for month
        print("Average Temperature: {}".format(round(mean(clmt[y]["tempAVGlist"]),1)))
        print("Average Max Temperature: {}".format(round(mean(clmt[y]["tmax"]),1)))
        print("-- Warmest Daily Max Temperature: {}".format(clmt[y]["tmaxPROP"]["day_max"][0]),end=" ::: ")
        for x in range(len(clmt[y]["tmaxPROP"]["day_max"][1])):
            if x != len(clmt[y]["tmaxPROP"]["day_max"][1])-1: print("{},".format(clmt[y]["tmaxPROP"]["day_max"][1][x].daystr),end=" ")
            else: print("{}".format(clmt[y]["tmaxPROP"]["day_max"][1][x].daystr))
        print("-- Coolest Daily Max Temperature: {}".format(clmt[y]["tmaxPROP"]["day_min"][0]),end=" ::: ")
        for x in range(len(clmt[y]["tmaxPROP"]["day_min"][1])):
            if x != len(clmt[y]["tmaxPROP"]["day_min"][1])-1: print("{},".format(clmt[y]["tmaxPROP"]["day_min"][1][x].daystr),end=" ")
            else: print("{}".format(clmt[y]["tmaxPROP"]["day_min"][1][x].daystr))
        print("-- Warmest AVG Monthly Max Temperature: {}".format(round(clmt[y]["tmaxPROP"]["month_AVG_max"][0],1)),end=" ::: ")
        for x in range(len(clmt[y]["tmaxPROP"]["month_AVG_max"][1])):
            if x != len(clmt[y]["tmaxPROP"]["month_AVG_max"][1])-1: print("{},".format(calendar.month_name[clmt[y]["tmaxPROP"]["month_AVG_max"][1][x]]),end=" ")
            else: print("{}".format(calendar.month_name[clmt[y]["tmaxPROP"]["month_AVG_max"][1][x]]))
        print("-- Coolest AVG Monthly Max Temperature: {}".format(round(clmt[y]["tmaxPROP"]["month_AVG_min"][0],1)),end=" ::: ")
        for x in range(len(clmt[y]["tmaxPROP"]["month_AVG_min"][1])):
            if x != len(clmt[y]["tmaxPROP"]["month_AVG_min"][1])-1: print("{},".format(calendar.month_name[clmt[y]["tmaxPROP"]["month_AVG_min"][1][x]]),end=" ")
            else: print("{}".format(calendar.month_name[clmt[y]["tmaxPROP"]["month_AVG_min"][1][x]]))
        print("Average Min Temperature: {}".format(round(mean(clmt[y]["tmin"]),1)))
        print("-- Warmest Min Temperature: {}".format(clmt[y]["tminPROP"]["day_max"][0]),end=" ::: ")
        for x in range(len(clmt[y]["tminPROP"]["day_max"][1])):
            if x != len(clmt[y]["tminPROP"]["day_max"][1])-1: print("{},".format(clmt[y]["tminPROP"]["day_max"][1][x].daystr),end=" ")
            else: print("{}".format(clmt[y]["tminPROP"]["day_max"][1][x].daystr))
        print("-- Coolest Min Temperature: {}".format(clmt[y]["tminPROP"]["day_min"][0]),end=" ::: ")
        for x in range(len(clmt[y]["tminPROP"]["day_min"][1])):
            if x != len(clmt[y]["tminPROP"]["day_min"][1])-1: print("{},".format(clmt[y]["tminPROP"]["day_min"][1][x].daystr),end=" ")
            else: print("{}".format(clmt[y]["tminPROP"]["day_min"][1][x].daystr))
        print("-- Warmest AVG Monthly Min Temperature: {}".format(round(clmt[y]["tminPROP"]["month_AVG_max"][0],1)),end=" ::: ")
        for x in range(len(clmt[y]["tminPROP"]["month_AVG_max"][1])):
            if x != len(clmt[y]["tminPROP"]["month_AVG_max"][1])-1: print("{},".format(calendar.month_name[clmt[y]["tminPROP"]["month_AVG_max"][1][x]]),end=" ")
            else: print("{}".format(calendar.month_name[clmt[y]["tminPROP"]["month_AVG_max"][1][x]]))
        print("-- Coolest AVG Monthly Min Temperature: {}".format(round(clmt[y]["tminPROP"]["month_AVG_min"][0],1)),end=" ::: ")
        for x in range(len(clmt[y]["tminPROP"]["month_AVG_min"][1])):
            if x != len(clmt[y]["tminPROP"]["month_AVG_min"][1])-1: print("{},".format(calendar.month_name[clmt[y]["tminPROP"]["month_AVG_min"][1][x]]),end=" ")
            else: print("{}".format(calendar.month_name[clmt[y]["tminPROP"]["month_AVG_min"][1][x]]))
        print("-----")

def valueSearch(*args,**kwargs):
    valid_yrs = [x for x in clmt.keys() if type(x) == int]
    for x in args:
        if type(x) != int: return print("* ERROR! month/year values need to be integers! Try again. *")
    if len(args) == 0: return print("* ERROR! input at least a month value *")
    elif len(args) == 1:    # year OR month
        if args[0] in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]+1): searchScope = "year"
        elif args[0] not in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]+1) and args[0] > 1000: return print("* ERROR! Ensure year value between {} and {} *".format(valid_yrs[0],valid_yrs[len(valid_yrs)-1]))
        elif args[0] in range(1,13): searchScope = "month"
        elif args[0] not in range(1,13): return print("* ERROR! Ensure month value between 1 and 12 *")
    elif len(args) == 2:    # year AND month
        if args[0] in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]+1) and args[1] in range(1,13): searchScope = "yearmonth"
        else:
            return print("* ERROR! Ensure format of valueSearch(y,m,**kwargs) ::: Year must be between {} and {}; Month between 1 and 12 *".format(valid_yrs[0],valid_yrs[len(valid_yrs)-1]))
        
    else: return print("* OOPS! Too many variables! Try again. *")

def dayReport(m,d):   # As of this version, this function will be valid for records from 1811 to 2040
    if len(clmt) == 0: return print("* OOPS! Run the clmtAnalyze function first.")
    valid_yrs = [x for x in clmt.keys() if type(x) == int]
    valid_yrs.sort()
    climo30yrs = {}
    for x in range(1811,2016,5):
        if x in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]) and x+29 in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]+1):
            climo30yrs[(x,x+29)] = dict(years=(x,x+29),prcp=[],prcpPROP={"day_max":[-1,[]]},
                                        snow=[],snowPROP={"day_max":[-1,[]]},
                                        tmax=[],tmaxPROP={"day_max":[-999,[]],"day_min":[999,[]]},
                                        tmin=[],tminPROP={"day_max":[-999,[]],"day_min":[999,[]]})

    alltime = {"years":(valid_yrs[0],valid_yrs[len(valid_yrs)-1]),
               "prcp": [],"prcpPROP":{"day_max":[-1,[]]},
               "snow": [],"snowPROP":{"day_max":[-1,[]]},
               "tmax": [],"tmaxPROP":{"day_max":[-999,[]],"day_min":[999,[]]},
               "tmin": [],"tminPROP":{"day_max":[-999,[]],"day_min":[999,[]]}}
    # {"day_max":[-1,[]],"month_max":[-1,[]],"month_min":[999,[]]}
    # {"day_max":[-999,[]],"day_min":[999,[]],"month_AVG_max":[-999,"n/a"],"month_AVG_min":[999,"n/a"]}
    # if clmt[int(each[2][0:4])][int(each[2][5:7])][int(each[2][8:10])].prcpQ in ignoreflags and clmt[int(each[2][0:4])][int(each[2][5:7])][int(each[2][8:10])].prcp not in ["9999","-9999",""]:
    # if clmt[int(each[2][0:4])][int(each[2][5:7])][int(each[2][8:10])].tmaxQ in ignoreflags and clmt[int(each[2][0:4])][int(each[2][5:7])][int(each[2][8:10])].tmax not in ["9999","-9999",""]:
    for y in valid_yrs:
        try:
            if clmt[y][m][d].prcpQ in ignoreflags and clmt[y][m][d].prcp not in ["9999","-9999",""]:
                alltime["prcp"].append(float(clmt[y][m][d].prcp))
                if float(clmt[y][m][d].prcp) == alltime["prcpPROP"]["day_max"][0]:
                    alltime["prcpPROP"]["day_max"][1].append(clmt[y][m][d])
                elif float(clmt[y][m][d].prcp) > alltime["prcpPROP"]["day_max"][0]:
                    alltime["prcpPROP"]["day_max"][0] = float(clmt[y][m][d].prcp)
                    alltime["prcpPROP"]["day_max"][1] = []
                    alltime["prcpPROP"]["day_max"][1].append(clmt[y][m][d])
                for c in climo30yrs:
                    if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                        climo30yrs[c]["prcp"].append(float(clmt[y][m][d].prcp))
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
                if float(clmt[y][m][d].snow) == alltime["snowPROP"]["day_max"][0]:
                    alltime["snowPROP"]["day_max"][1].append(clmt[y][m][d])
                elif float(clmt[y][m][d].snow) > alltime["snowPROP"]["day_max"][0]:
                    alltime["snowPROP"]["day_max"][0] = float(clmt[y][m][d].snow)
                    alltime["snowPROP"]["day_max"][1] = []
                    alltime["snowPROP"]["day_max"][1].append(clmt[y][m][d])
                for c in climo30yrs:
                    if y >= c[0] and y <= c[1] and c[0] >= min(YR for YR in clmt  if type(YR) == int) and c[1] <= max(YR for YR in clmt  if type(YR) == int):
                        climo30yrs[c]["snow"].append(float(clmt[y][m][d].snow))
                        if float(clmt[y][m][d].snow) == climo30yrs[c]["snowPROP"]["day_max"][0]:
                            climo30yrs[c]["snowPROP"]["day_max"][1].append(clmt[y][m][d])
                        elif float(clmt[y][m][d].snow) > climo30yrs[c]["snowPROP"]["day_max"][0]:
                            climo30yrs[c]["snowPROP"]["day_max"][0] = float(clmt[y][m][d].snow)
                            climo30yrs[c]["snowPROP"]["day_max"][1] = []
                            climo30yrs[c]["snowPROP"]["day_max"][1].append(clmt[y][m][d])
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
    print("---------------------------------")
    print("Climatology Report for {} {}".format(calendar.month_name[m],d))
    print("City: {}, {}".format(clmt["station"],clmt["station_name"]))
    print("---------------------------------")
    print("{:▒^9} {:▒^12} {:▒^12} {:▒^8} {:▒^9}  {:▒^9} {:▒^8} {:▒^9}  {:▒^9}".format("YEARS","PRCP","SNOW","TMAX","TMAX","TMAX","TMIN","TMIN","TMIN"))
    print("{:▒^9} {:▒^12} {:▒^12} {:▒^8} {:▒^9}  {:▒^9} {:▒^8} {:▒^9}  {:▒^9}".format(     "","hi","hi","avg","hi","lo","avg","hi","lo"))
    print("{:.^9} {:.^12} {:.^12} {:.^8} {:.^9}  {:.^9} {:.^8} {:.^9}  {:.^9}".format("","","","","","","","",""))
    print("{:^9} {:>6}, {:>4} {:>6}, {:^4} {:^8} {:>3}, {:^4}  {:>3}, {:^4} {:^8} {:>3}, {:^4}  {:>3}, {:^4}".format(str(alltime["years"][0])+"-"+str(alltime["years"][1]),
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
            print("{:^9} {:>6}, {:>4} {:>6}, {:^4} {:^8} {:>3}, {:^4}  {:>3}, {:^4} {:^8} {:>3}, {:^4}  {:>3}, {:^4}".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
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

def weekReport(m,d):
    if len(clmt) == 0: return print("* OOPS! Run the clmtAnalyze function first.")
    valid_yrs = [x for x in clmt.keys() if type(x) == int]
    valid_yrs.sort()
    climo30yrs = {}
    for x in range(1811,2016,5):
        if x in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]) and x+29 in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]+1):
            climo30yrs[(x,x+29)] = {"years":(x,x+29),"total_days":0,
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
    wkstart = datetime.date(1999,m,d) - datetime.timedelta(days=3)
    currday = wkstart
    wkend = datetime.date(1999,m,d) + datetime.timedelta(days=3)
    for y in valid_yrs:
        wk = []
        wk_prcp = []
        wk_snow = []
        wk_tempAVGlist = []
        wk_tmax = []
        wk_tmin = []
        while currday <= wkend:
            try:
                wk.append(clmt[y][currday.month][currday.day])
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
            if len(wk_tempAVGlist) >= 8:
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
            if len(wk_tempAVGlist) >= 8:
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
            if len(wk_tmax) >= 4:
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
            if len(wk_tmin) >= 4:
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
                    if len(wk_tempAVGlist) >= 8:
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
                    if len(wk_tmax) >= 4:
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
                    if len(wk_tmin) >= 4:
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
    print("--------------------------------------------------")

    print("\nPart 1: Precipitation Stats")
    print("{:▒^9} {:▒^11} {:▒^6} {:▒^12} {:▒^11} {:▒^6} {:▒^12}".format("Years","PRCP","PRCP","PRCP","SNOW","SNOW","SNOW"))
    print("{:▒^9} {:▒^11} {:▒^6} {:▒^12} {:▒^11} {:▒^6} {:▒^12}".format("","DAYS","AVG", "MAX","DAYS","AVG", "MAX"))
    #         Y     PD     PA      PM       SD     SA      SM
    print("{:-^9} {:-^11} {:-^6} {:-^12} {:-^11} {:-^6} {:-^12}".format("","","","","","",""))
    print("{:^9} {:4}:{:>5}% {:^6} {:>5}, {:^5} {:4}:{:>5}% {:^6} {:>5}, {:^5}".format(str(alltime["years"][0])+"-"+str(alltime["years"][1]),
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
            print("{:^9} {:4}:{:>5}% {:^6} {:>5}, {:^5} {:4}:{:>5}% {:^6} {:>5}, {:^5}".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
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
    print("{:^9} {:^5} {:^5} {:>5}, {:^5} {:>5}, {:^5} | {:^5} {:^5} {:>5}, {:^5} {:>5}, {:^5} | {:^5} {:^5} {:>5}, {:^5} {:>5}, {:^5}".format(str(alltime["years"][0])+"-"+str(alltime["years"][1]),
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
            print("{:^9} {:^5} {:^5} {:>5}, {:^5} {:>5}, {:^5} | {:^5} {:^5} {:>5}, {:^5} {:>5}, {:^5} | {:^5} {:^5} {:>5}, {:^5} {:>5}, {:^5}".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
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

def monthReport(m):
    #print([x for x in clmt.keys()])
    valid_yrs = [x for x in clmt.keys() if type(x) == int]
    valid_yrs.sort()
    climo30yrs = {}
    for x in range(1811,2016,5):
        if x in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]) and x+29 in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]+1):
            climo30yrs[(x,x+29)] = {"years":(x,x+29),"total_days":0,
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
            if clmt[y][m]["recordqty"] > 20:
                if clmt[y][m]["prcpDAYS"] == alltime["prcpPROP"]["month_max_days"][0]: alltime["prcpPROP"]["month_max_days"][1].append(y)
                elif clmt[y][m]["prcpDAYS"] > alltime["prcpPROP"]["month_max_days"][0]:
                    alltime["prcpPROP"]["month_max_days"][0] = clmt[y][m]["prcpDAYS"]
                    alltime["prcpPROP"]["month_max_days"][1] = []
                    alltime["prcpPROP"]["month_max_days"][1].append(y)
                if clmt[y][m]["prcpDAYS"] == alltime["prcpPROP"]["month_min_days"][0]: alltime["prcpPROP"]["month_min_days"][1].append(y)
                elif clmt[y][m]["prcpDAYS"] < alltime["prcpPROP"]["month_min_days"][0]:
                    alltime["prcpPROP"]["month_min_days"][0] = clmt[y][m]["prcpDAYS"]
                    alltime["prcpPROP"]["month_min_days"][1] = []
                    alltime["prcpPROP"]["month_min_days"][1].append(y)
                if sum(clmt[y][m]["prcp"]) == alltime["prcpPROP"]["month_max"][0]: alltime["prcpPROP"]["month_max"][1].append(y)
                elif sum(clmt[y][m]["prcp"]) > alltime["prcpPROP"]["month_max"][0]:
                    alltime["prcpPROP"]["month_max"][0] = sum(clmt[y][m]["prcp"])
                    alltime["prcpPROP"]["month_max"][1] = []
                    alltime["prcpPROP"]["month_max"][1].append(y)
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
                    if clmt[y][m]["recordqty"] > 20:
                        if clmt[y][m]["prcpDAYS"] == climo30yrs[c]["prcpPROP"]["month_max_days"][0]: climo30yrs[c]["prcpPROP"]["month_max_days"][1].append(y)
                        elif clmt[y][m]["prcpDAYS"] > climo30yrs[c]["prcpPROP"]["month_max_days"][0]:
                            climo30yrs[c]["prcpPROP"]["month_max_days"][0] = clmt[y][m]["prcpDAYS"]
                            climo30yrs[c]["prcpPROP"]["month_max_days"][1] = []
                            climo30yrs[c]["prcpPROP"]["month_max_days"][1].append(y)
                        if clmt[y][m]["prcpDAYS"] == climo30yrs[c]["prcpPROP"]["month_min_days"][0]: climo30yrs[c]["prcpPROP"]["month_min_days"][1].append(y)
                        elif clmt[y][m]["prcpDAYS"] < climo30yrs[c]["prcpPROP"]["month_min_days"][0]:
                            climo30yrs[c]["prcpPROP"]["month_min_days"][0] = clmt[y][m]["prcpDAYS"]
                            climo30yrs[c]["prcpPROP"]["month_min_days"][1] = []
                            climo30yrs[c]["prcpPROP"]["month_min_days"][1].append(y)
                        if sum(clmt[y][m]["prcp"]) == climo30yrs[c]["prcpPROP"]["month_max"][0]: climo30yrs[c]["prcpPROP"]["month_max"][1].append(y)
                        elif sum(clmt[y][m]["prcp"]) > climo30yrs[c]["prcpPROP"]["month_max"][0]:
                            climo30yrs[c]["prcpPROP"]["month_max"][0] = sum(clmt[y][m]["prcp"])
                            climo30yrs[c]["prcpPROP"]["month_max"][1] = []
                            climo30yrs[c]["prcpPROP"]["month_max"][1].append(y)
                        if sum(clmt[y][m]["prcp"]) == climo30yrs[c]["prcpPROP"]["month_min"][0]: climo30yrs[c]["prcpPROP"]["month_min"][1].append(y)
                        elif sum(clmt[y][m]["prcp"]) < climo30yrs[c]["prcpPROP"]["month_min"][0]:
                            climo30yrs[c]["prcpPROP"]["month_min"][0] = sum(clmt[y][m]["prcp"])
                            climo30yrs[c]["prcpPROP"]["month_min"][1] = []
                            climo30yrs[c]["prcpPROP"]["month_min"][1].append(y)

            # SNOW
            alltime["snow"].append(sum(clmt[y][m]["snow"]))
            alltime["snowPROP"]["days"] += clmt[y][m]["snowDAYS"]
            if clmt[y][m]["recordqty"] > 20:
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
                    if clmt[y][m]["recordqty"] > 20:
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
            if len(clmt[y][m]["tempAVGlist"]) >= 42:
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
                    if len(clmt[y][m]["tempAVGlist"]) >= 42:
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
            if len(clmt[y][m]["tmax"]) > 20:
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
                    if len(clmt[y][m]["tmax"]) > 20:
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
            if len(clmt[y][m]["tmin"]) > 20:
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
                    if len(clmt[y][m]["tmin"]) > 20:
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
    print("--------------------------------")
    print("Part 1: {} Precipitation Stats".format(calendar.month_name[m]))
    print("{:▒^9} {:▒^11}  {:▒^8}  {:▒^8} {:▒^6} {:▒^12} {:▒^12} | {:▒^11}  {:▒^8} {:▒^6} {:▒^12} |".format("Years","PRCP","PRCP","PRCP","PRCP","PRCP","PRCP","SNOW","SNOW","SNOW","SNOW"))
    print("{:▒^9} {:▒^11}  {:▒^8}  {:▒^8} {:▒^6} {:▒^12} {:▒^12} | {:▒^11}  {:▒^8} {:▒^6} {:▒^12} |".format("","DAYS","DAYS MAX","DAYS MIN","AVG", "MAX","MIN","DAYS","DAYS MAX","AVG", "MAX"))
    #         Y     PD       PDx    PDn      PA      PM     Pmin      SD     SDx       SA      SM
    print("{:-^9} {:-^11}  {:-^8}  {:-^8} {:-^6} {:-^12} {:-^12} | {:-^11}  {:-^8} {:-^6} {:-^12} |".format("","","","","","","","","","",""))
    print("{:^9} {:4}:{:>5}%  {:>2}, {:^4}  {:>2}, {:^4} {:^6} {:>5}, {:^5} {:>5}, {:^5} | {:4}:{:>5}%  {:>2}, {:^4} {:^6} {:>5}, {:^5} |".format(str(alltime["years"][0])+"-"+str(alltime["years"][1]),
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
            print("{:^9} {:4}:{:>5}%  {:>2}, {:^4}  {:>2}, {:^4} {:^6} {:>5}, {:^5} {:>5}, {:^5} | {:4}:{:>5}%  {:>2}, {:^4} {:^6} {:>5}, {:^5} |".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
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
    print("{:^9} {:^5} {:^5} {:>5}, {:^5} {:>5}, {:^5} | {:^5} {:^5} {:>5}, {:^5} {:>5}, {:^5} | {:^5} {:^5} {:>5}, {:^5} {:>5}, {:^5}".format(str(alltime["years"][0])+"-"+str(alltime["years"][1]),
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
            print("{:^9} {:^5} {:^5} {:>5}, {:^5} {:>5}, {:^5} | {:^5} {:^5} {:>5}, {:^5} {:>5}, {:^5} | {:^5} {:^5} {:>5}, {:^5} {:>5}, {:^5}".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
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

def yearReport():
    # assisted on nested list comprehensions: https://www.geeksforgeeks.org/nested-list-comprehensions-in-python/
    valid_yrs = [x for x in clmt.keys() if type(x) == int]
    valid_yrs.sort()
    climo30yrs = {}
    for x in range(1811,2016,5):
        if x in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]) and x+29 in range(valid_yrs[0],valid_yrs[len(valid_yrs)-1]+1):
            climo30yrs[(x,x+29)] = {"years":(x,x+29),"total_days":0,
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
        if clmt[y]["recordqty"] > 300:
            if clmt[y]["prcpDAYS"] == alltime["prcpPROP"]["year_max_days"][0]: alltime["prcpPROP"]["year_max_days"][1].append(y)
            elif clmt[y]["prcpDAYS"] > alltime["prcpPROP"]["year_max_days"][0]:
                alltime["prcpPROP"]["year_max_days"][0] = clmt[y]["prcpDAYS"]
                alltime["prcpPROP"]["year_max_days"][1] = []
                alltime["prcpPROP"]["year_max_days"][1].append(y)
            if clmt[y]["prcpDAYS"] == alltime["prcpPROP"]["year_min_days"][0]: alltime["prcpPROP"]["year_min_days"][1].append(y)
            elif clmt[y]["prcpDAYS"] < alltime["prcpPROP"]["year_min_days"][0]:
                alltime["prcpPROP"]["year_min_days"][0] = clmt[y]["prcpDAYS"]
                alltime["prcpPROP"]["year_min_days"][1] = []
                alltime["prcpPROP"]["year_min_days"][1].append(y)
            if sum(clmt[y]["prcp"]) == alltime["prcpPROP"]["year_max"][0]: alltime["prcpPROP"]["year_max"][1].append(y)
            elif sum(clmt[y]["prcp"]) > alltime["prcpPROP"]["year_max"][0]:
                alltime["prcpPROP"]["year_max"][0] = sum(clmt[y]["prcp"])
                alltime["prcpPROP"]["year_max"][1] = []
                alltime["prcpPROP"]["year_max"][1].append(y)
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
                if clmt[y]["recordqty"] > 300:
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
        if clmt[y]["recordqty"] > 300:
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
                if clmt[y]["recordqty"] > 20:
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
        if len(clmt[y]["tempAVGlist"]) >= 600:
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
                if len(clmt[y]["tempAVGlist"]) >= 600:
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
        if len(clmt[y]["tmax"]) > 300:
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
                if len(clmt[y]["tmax"]) > 300:
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
        if len(clmt[y]["tmin"]) > 300:
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
                if len(clmt[y]["tmin"]) > 300:
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
    print("---------------------------")
    print("Climatology Report for All Years on Record")
    print("City: {}, {}".format(clmt["station"],clmt["station_name"]))
    print("---------------------------")
    print("Part 1: Precipitation Stats")
    print("{:▒^9} {:▒^12}  {:▒^9}  {:▒^9}  {:▒^6} {:▒^12} {:▒^12} | {:▒^11}  {:▒^9} {:▒^6} {:▒^11} |".format("Years","PRCP","PRCP","PRCP","PRCP","PRCP","PRCP","SNOW","SNOW","SNOW","SNOW"))
    print("{:▒^9} {:▒^12}  {:▒^9}  {:▒^9}  {:▒^6} {:▒^12} {:▒^12} | {:▒^11}  {:▒^9} {:▒^6} {:▒^11} |".format("","DAYS","DAYS MAX","DAYS MIN","AVG", "MAX","MIN","DAYS","DAYS MAX","AVG", "MAX"))
    #         Y     PD       PDx    PDn      PA      PM     Pmin      SD     SDx       SA      SM
    print("{:-^9} {:-^12}  {:-^9}  {:-^9}  {:-^6} {:-^12} {:-^12} | {:-^11}  {:-^9} {:-^6} {:-^11} |".format("","","","","","","","","","",""))
    print("{:^9} {:5}:{:>5}%  {:>3}, {:^4}  {:>3}, {:^4}  {:^6} {:>6}, {:^4} {:>6}, {:^4} | {:4}:{:>5}%  {:>3}, {:^4} {:^6} {:>5}, {:^4} |".format(str(alltime["years"][0])+"-"+str(alltime["years"][1]),
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
            print("{:^9} {:5}:{:>5}%  {:>3}, {:^4}  {:>3}, {:^4}  {:^6} {:>6}, {:^4} {:>6}, {:^4} | {:4}:{:>5}%  {:>3}, {:^4} {:^6} {:>5}, {:^4} |".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
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
    print("{:^9} {:^5} {:^5} {:>5}, {:^5} {:>5}, {:^5} | {:^5} {:^5} {:>5}, {:^5} {:>5}, {:^5} | {:^5} {:^5} {:>5}, {:^5} {:>5}, {:^5}".format(str(alltime["years"][0])+"-"+str(alltime["years"][1]),
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
            print("{:^9} {:^5} {:^5} {:>5}, {:^5} {:>5}, {:^5} | {:^5} {:^5} {:>5}, {:^5} {:>5}, {:^5} | {:^5} {:^5} {:>5}, {:^5} {:>5}, {:^5}".format(str(climo30yrs[c]["years"][0])+"-"+str(climo30yrs[c]["years"][1]),
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

def dayRank(m,d,qty):
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

    DAYS_tmax = []
    DAYS_tmin = []
    DAYS_prcp = []
    DAYS_snow = []
    for y in [YR for YR in clmt if type(YR) == int]:
        try:
            if clmt[y][m][d].tmaxQ in ignoreflags:
                DAYS_tmax.append(day_attr(y,int(clmt[y][m][d].tmax)))
        except:
            pass
        try:
            if clmt[y][m][d].tminQ in ignoreflags:
                DAYS_tmin.append(day_attr(y,int(clmt[y][m][d].tmin)))
        except:
            pass
        try:
            if clmt[y][m][d].prcpQ in ignoreflags:
                DAYS_prcp.append(day_attr(y,round(float(clmt[y][m][d].prcp),2)))
        except:
            pass
        try:
            if clmt[y][m][d].snowQ in ignoreflags:
                DAYS_snow.append(day_attr(y,round(float(clmt[y][m][d].snow),1)))
        except:
            pass
    DAYS_tmax_asc = DAYS_tmax.copy()
    DAYS_tmax.sort(key=lambda x:x.number,reverse=True)
    DAYS_tmax_asc.sort(key=lambda x:x.number)
    DAYS_tmin_asc = DAYS_tmin.copy()
    DAYS_tmin.sort(key=lambda x:x.number,reverse=True)
    DAYS_tmin_asc.sort(key=lambda x:x.number)
    DAYS_prcp.sort(key=lambda x:x.number,reverse=True)
    DAYS_snow.sort(key=lambda x:x.number,reverse=True)

    print("{:^39}".format("Precipitation Records for {} {}".format(calendar.month_name[m],d)))
    print("{:^39}".format("{}, {}".format(clmt["station"],clmt["station_name"])))
    print("{:-^39}".format(""))
    print("{:^19}|{:^19}".format("Rain","Snow"))
    print("{:-^19}|{:-^19}".format("",""))
    i = 1
    j = 1
    ranked_i = []
    ranked_j = []
    for x in range(len(DAYS_prcp)):
        if x == 0:
            print("  {:2}{} {:4}  {:5}  |  {:2}{} {:4}  {:5}  ".format(1 if DAYS_prcp[x].number > 0 else "--",
                                                                       "." if DAYS_prcp[x].number > 0 else " ",
                                                                       DAYS_prcp[x].year if DAYS_prcp[x].number > 0 else "--",
                                                                       DAYS_prcp[x].number,
                                                                       1 if DAYS_snow[x].number > 0 else "--",
                                                                       "." if DAYS_snow[x].number > 0 else " ",
                                                                       DAYS_snow[x].year if DAYS_snow[x].number > 0 else "--",
                                                                       DAYS_snow[x].number))
            ranked_i.append(i)
            ranked_j.append(j)
        else:
            if i not in ranked_i and i <= qty: ranked_i.append(i)
            if j not in ranked_j and j <= qty: ranked_j.append(j)
            if DAYS_prcp[x].number != DAYS_prcp[x-1].number: i += 1
            try:
                if DAYS_prcp[x].number == 0: i = qty + 1
                if DAYS_snow[x].number == 0: j = qty + 1
                if DAYS_snow[x].number != DAYS_snow[x-1].number: j += 1
            except:
                pass
            if i <= qty or j <= qty:
                try:
                    print("  {:2}{} {:4}  {:5}  |  {:2}{} {:4}  {:5}  ".format(i if i not in ranked_i and i <= qty else "",
                                                                               "." if i not in ranked_i and i <= qty else " ",
                                                                               DAYS_prcp[x].year if i <= qty else "",
                                                                               DAYS_prcp[x].number if i <= qty else "",
                                                                               j if DAYS_snow[x].number > 0 and j not in ranked_j and j <= qty else "",
                                                                               "." if DAYS_snow[x].number > 0 and j not in ranked_j and j <= qty else " ",
                                                                               DAYS_snow[x].year if DAYS_snow[x].number > 0 and j <= qty else "",
                                                                               DAYS_snow[x].number if DAYS_snow[x].number > 0 and j <= qty else ""))
                except:
                    if len(DAYS_prcp) > len(DAYS_snow):
                        print("  {:2}{} {:4}  {:5}  |                   ".format(i if i not in ranked_i and i <= qty else "",
                                                                                   "." if i not in ranked_i and i <= qty else " ",
                                                                                   DAYS_prcp[x].year if i <= qty else "",
                                                                                   DAYS_prcp[x].number if i <= qty else ""))
                    elif len(DAYS_snow) > len(DAYS_prcp):
                        print("                   |  {:2}{} {:4}  {:5}  ".format(j if j not in ranked_j and j <= qty else "",
                                                                                   "." if j not in ranked_j and j <= qty else " ",
                                                                                   DAYS_snow[x].year if DAYS_snow[x].number > 0 and j <= qty else "",
                                                                                   DAYS_snow[x].number if DAYS_snow[x].number > 0 and j <= qty else ""))

        if i > qty and j > qty: break
    print("\n{:^65}".format("Temperature Records for {} {}".format(calendar.month_name[m],d)))
    print("{:^65}".format("{}, {}".format(clmt["station"],clmt["station_name"])))
    print("{:-^65}".format(""))
    print("{:^32}|{:^32}".format("TMAX","TMIN"))
    print("{:-^32}|{:-^32}".format("",""))
    print("{:^15}|{:^16}|{:^16}|{:^15}".format("Warmest","Coolest","Warmest","Coolest"))
    print("{:-^15}|{:-^16}|{:-^16}|{:-^15}".format("","","",""))
    i = 1
    j = 1
    k = 1
    l = 1
    ranked_i = []
    ranked_j = []
    ranked_k = []
    ranked_l = []
    for x in range(len(DAYS_tmax)):
        if x == 0:
            print("{:2}{} {:4}  {:3}  | {:2}{} {:4}  {:3}  | {:2}{} {:4}  {:3}  | {:2}{} {:4}  {:3}".format(1,".",DAYS_tmax[x].year,DAYS_tmax[x].number,
                                                                                                            1,".",DAYS_tmax_asc[x].year,DAYS_tmax_asc[x].number,
                                                                                                            1,".",DAYS_tmin[x].year,DAYS_tmin[x].number,
                                                                                                            1,".",DAYS_tmin_asc[x].year,DAYS_tmin_asc[x].number))
            ranked_i.append(i)
            ranked_j.append(j)
            ranked_k.append(k)
            ranked_l.append(l)
        else:
            if i not in ranked_i and i <= qty: ranked_i.append(i)
            if j not in ranked_j and j <= qty: ranked_j.append(j)
            if k not in ranked_k and k <= qty: ranked_k.append(k)
            if l not in ranked_l and l <= qty: ranked_l.append(l)
            if DAYS_tmax[x].number != DAYS_tmax[x-1].number: i += 1
            if DAYS_tmax_asc[x].number != DAYS_tmax_asc[x-1].number: j += 1
            if DAYS_tmin[x].number != DAYS_tmin[x-1].number: k += 1
            if DAYS_tmin_asc[x].number != DAYS_tmin_asc[x-1].number: l += 1
            if i <= qty or j <= qty or k <= qty or l <= qty:
                print("{:2}{} {:4}  {:3}  | {:2}{} {:4}  {:3}  | {:2}{} {:4}  {:3}  | {:2}{} {:4}  {:3}".format(i if i not in ranked_i and i <= qty else "",
                                                                                                                "." if i not in ranked_i and i <= qty else " ",
                                                                                                                DAYS_tmax[x].year if i <= qty else "",
                                                                                                                DAYS_tmax[x].number if i <= qty else "",
                                                                                                                j if j not in ranked_j and j <= qty else "",
                                                                                                                "." if j not in ranked_j and j <= qty else " ",
                                                                                                                DAYS_tmax_asc[x].year if j <= qty else "",
                                                                                                                DAYS_tmax_asc[x].number if j <= qty else "",
                                                                                                                k if k not in ranked_k and k <= qty else "",
                                                                                                                "." if k not in ranked_k and k <= qty else " ",
                                                                                                                DAYS_tmin[x].year if k <= qty else "",
                                                                                                                DAYS_tmin[x].number if k <= qty else "",
                                                                                                                l if l not in ranked_l and l <= qty else "",
                                                                                                                "." if l not in ranked_l and l <= qty else " ",
                                                                                                                DAYS_tmin_asc[x].year if l <= qty else "",
                                                                                                                DAYS_tmin_asc[x].number if l <= qty else ""))
        if i > qty and j > qty and k > qty and l > qty: break

def weekRank(mo,d,qty):
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
        wk_tavg = []
        wk_tmax = []
        wk_tmin = []
        for DAY in range(7):
            wklist.append(wkstart)
            wkstart += datetime.timedelta(days=1)
        for DAY in wklist:
            try:
                if clmt[y][DAY.month][DAY.day].prcpQ in ignoreflags:
                    wk_prcp.append(float(clmt[y][DAY.month][DAY.day].prcp))
            except:
                pass
            try:
                if clmt[y][DAY.month][DAY.day].snowQ in ignoreflags:
                    wk_snow.append(float(clmt[y][DAY.month][DAY.day].snow))
            except:
                pass
            try:
                if clmt[y][DAY.month][DAY.day].tmaxQ in ignoreflags and clmt[y][DAY.month][DAY.day].tmax not in ["9999","-9999",""] and clmt[y][DAY.month][DAY.day].tminQ in ignoreflags and clmt[y][DAY.month][DAY.day].tmin not in ["9999","-9999",""]:
                    wk_tavg.append(int(clmt[y][DAY.month][DAY.day].tmax))
                    wk_tavg.append(int(clmt[y][DAY.month][DAY.day].tmin))
            except:
                pass
            try:
                if clmt[y][DAY.month][DAY.day].tmaxQ in ignoreflags:
                    wk_tmax.append(int(clmt[y][DAY.month][DAY.day].tmax))
            except:
                pass
            try:
                if clmt[y][DAY.month][DAY.day].tminQ in ignoreflags:
                    wk_tmin.append(int(clmt[y][DAY.month][DAY.day].tmin))
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
        if len(wk_tavg) >= 8:
            try:
                WEEKS_tavg.append(week_attr(y,round(mean(wk_tavg),1)))
            except:
                pass
        if len(wk_tmax) >= 4:
            try:
                WEEKS_tmax.append(week_attr(y,round(mean(wk_tmax),1)))
            except:
                pass
        if len(wk_tmin) >= 4:
            try:
                WEEKS_tmin.append(week_attr(y,round(mean(wk_tmin),1)))
            except:
                pass

    WEEKS_prcp.sort(key=lambda x:x.number,reverse=True)
    WEEKS_snow.sort(key=lambda x:x.number,reverse=True)
    WEEKS_tavg_asc = WEEKS_tavg.copy()
    WEEKS_tavg.sort(key=lambda x:x.number,reverse=True)
    WEEKS_tavg_asc.sort(key=lambda x:x.number)
    WEEKS_tmax_asc = WEEKS_tmax.copy()
    WEEKS_tmax.sort(key=lambda x:x.number,reverse=True)
    WEEKS_tmax_asc.sort(key=lambda x:x.number)
    WEEKS_tmin_asc = WEEKS_tmin.copy()
    WEEKS_tmin.sort(key=lambda x:x.number,reverse=True)
    WEEKS_tmin_asc.sort(key=lambda x:x.number)

    print("{:^39}".format("Precipitation Records for the Week of {} {} - {} {}".format(calendar.month_abbr[wkorig.month],wkorig.day,
                                                                                  calendar.month_abbr[(wkorig + datetime.timedelta(days=6)).month],(wkorig + datetime.timedelta(days=7)).day)))
    print("{:^39}".format("{}, {}".format(clmt["station"],clmt["station_name"])))
    print("{:-^39}".format(""))
    print("{:^19}|{:^19}".format("Rain","Snow"))
    print("{:-^19}|{:-^19}".format("",""))
    i = 1
    j = 1
    ranked_i = []
    ranked_j = []
    for x in range(len(WEEKS_prcp)):
        if x == 0:
            print("  {:2}{} {:4}  {:5}  |  {:2}{} {:4}  {:5}  ".format(1 if WEEKS_prcp[x].number > 0 else "--",
                                                                       "." if WEEKS_prcp[x].number > 0 else " ",
                                                                       WEEKS_prcp[x].year if WEEKS_prcp[x].number > 0 else "--",
                                                                       WEEKS_prcp[x].number,
                                                                       1 if WEEKS_snow[x].number > 0 else "--",
                                                                       "." if WEEKS_snow[x].number > 0 else " ",
                                                                       WEEKS_snow[x].year if WEEKS_snow[x].number > 0 else "--",
                                                                       WEEKS_snow[x].number))
            ranked_i.append(i)
            ranked_j.append(j)
        else:
            if i not in ranked_i and i <= qty: ranked_i.append(i)
            if j not in ranked_j and j <= qty: ranked_j.append(j)
            if WEEKS_prcp[x].number != WEEKS_prcp[x-1].number: i += 1
            try:
                if WEEKS_prcp[x].number == 0: i = qty + 1
                if WEEKS_snow[x].number == 0: j = qty + 1
                if WEEKS_snow[x].number != WEEKS_snow[x-1].number: j += 1
            except:
                pass
            if i <= qty or j <= qty:
                try:
                    print("  {:2}{} {:4}  {:5}  |  {:2}{} {:4}  {:5}  ".format(i if i not in ranked_i and i <= qty else "",
                                                                               "." if i not in ranked_i and i <= qty else " ",
                                                                               WEEKS_prcp[x].year if i <= qty else "",
                                                                               WEEKS_prcp[x].number if i <= qty else "",
                                                                               j if WEEKS_snow[x].number > 0 and j not in ranked_j and j <= qty else "",
                                                                               "." if WEEKS_snow[x].number > 0 and j not in ranked_j and j <= qty else " ",
                                                                               WEEKS_snow[x].year if WEEKS_snow[x].number > 0 and j <= qty else "",
                                                                               WEEKS_snow[x].number if WEEKS_snow[x].number > 0 and j <= qty else ""))
                except:
                    if len(WEEKS_prcp) > len(WEEKS_snow):
                        print("  {:2}{} {:4}  {:5}  |                   ".format(i if i not in ranked_i and i <= qty else "",
                                                                                   "." if i not in ranked_i and i <= qty else " ",
                                                                                   WEEKS_prcp[x].year if i <= qty else "",
                                                                                   WEEKS_prcp[x].number if i <= qty else ""))
                    elif len(WEEKS_snow) > len(WEEKS_prcp):
                        print("                   |  {:2}{} {:4}  {:5}  ".format(j if j not in ranked_j and j <= qty else "",
                                                                                   "." if j not in ranked_j and j <= qty else " ",
                                                                                   WEEKS_snow[x].year if WEEKS_snow[x].number > 0 and j <= qty else "",
                                                                                   WEEKS_snow[x].number if WEEKS_snow[x].number > 0 and j <= qty else ""))

        if i > qty and j > qty: break
    print("\n{:^111}".format("Temperature Records for the Week of {} {} - {} {}".format(calendar.month_abbr[wkorig.month],wkorig.day,
                                                                                calendar.month_abbr[(wkorig + datetime.timedelta(days=7)).month],(wkorig + datetime.timedelta(days=7)).day)))
    print("{:^111}".format("{}, {}".format(clmt["station"],clmt["station_name"])))
    print("{:-^111}".format(""))
    print("{:^36}|{:^37}|{:^36}".format("AVG TEMP","TMAX","TMIN"))
    print("{:-^36}|{:-^37}|{:-^36}".format("","",""))
    print("{:^17}|{:^18}|{:^18}|{:^18}|{:^18}|{:^17}".format("Warmest","Coolest","Warmest","Coolest","Warmest","Coolest"))
    print("{:-^17}|{:-^18}|{:-^18}|{:-^18}|{:-^18}|{:-^17}".format("","","","","",""))
    i = 1
    j = 1
    k = 1
    l = 1
    m = 1
    n = 1
    ranked_i = []
    ranked_j = []
    ranked_k = []
    ranked_l = []
    ranked_m = []
    ranked_n = []
    for x in range(len(WEEKS_tmax)):
        if x == 0:
            print("{:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}".format(1,
                                                            ".",WEEKS_tavg[x].year,WEEKS_tavg[x].number,
                                                            1,".",WEEKS_tavg_asc[x].year,WEEKS_tavg_asc[x].number,
                                                            1,".",WEEKS_tmax[x].year,WEEKS_tmax[x].number,
                                                            1,".",WEEKS_tmax_asc[x].year,WEEKS_tmax_asc[x].number,
                                                            1,".",WEEKS_tmin[x].year,WEEKS_tmin[x].number,
                                                            1,".",WEEKS_tmin_asc[x].year,WEEKS_tmin_asc[x].number))
            ranked_i.append(i)
            ranked_j.append(j)
            ranked_k.append(k)
            ranked_l.append(l)
            ranked_m.append(m)
            ranked_n.append(n)
        else:
            if i not in ranked_i and i <= qty: ranked_i.append(i)
            if j not in ranked_j and j <= qty: ranked_j.append(j)
            if k not in ranked_k and k <= qty: ranked_k.append(k)
            if l not in ranked_l and l <= qty: ranked_l.append(l)
            if m not in ranked_m and m <= qty: ranked_m.append(m)
            if n not in ranked_n and n <= qty: ranked_n.append(n)
            if WEEKS_tavg[x].number != WEEKS_tavg[x-1].number: i += 1
            if WEEKS_tavg_asc[x].number != WEEKS_tavg_asc[x-1].number: j += 1
            if WEEKS_tmax[x].number != WEEKS_tmax[x-1].number: k += 1
            if WEEKS_tmax_asc[x].number != WEEKS_tmax_asc[x-1].number: l += 1
            if WEEKS_tmin[x].number != WEEKS_tmin[x-1].number: m += 1
            if WEEKS_tmin_asc[x].number != WEEKS_tmin_asc[x-1].number: n += 1
            if i <= qty or j <= qty or k <= qty or l <= qty or m <= qty or n <= qty:
                print("{:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}".format(
                        i if i not in ranked_i and i <= qty else "",
                        "." if i not in ranked_i and i <= qty else " ",
                        WEEKS_tavg[x].year if i <= qty else "",
                        WEEKS_tavg[x].number if i <= qty else "",
                        j if j not in ranked_j and j <= qty else "",
                        "." if j not in ranked_j and j <= qty else " ",
                        WEEKS_tavg_asc[x].year if j <= qty else "",
                        WEEKS_tavg_asc[x].number if j <= qty else "",
                        k if k not in ranked_k and k <= qty else "",
                        "." if k not in ranked_k and k <= qty else " ",
                        WEEKS_tmax[x].year if k <= qty else "",
                        WEEKS_tmax[x].number if k <= qty else "",
                        l if l not in ranked_l and l <= qty else "",
                        "." if l not in ranked_l and l <= qty else " ",
                        WEEKS_tmax_asc[x].year if l <= qty else "",
                        WEEKS_tmax_asc[x].number if l <= qty else "",
                        m if m not in ranked_m and m <= qty else "",
                        "." if m not in ranked_m and m <= qty else " ",
                        WEEKS_tmin[x].year if m <= qty else "",
                        WEEKS_tmin[x].number if m <= qty else "",
                        n if n not in ranked_n and n <= qty else "",
                        "." if n not in ranked_n and n <= qty else " ",
                        WEEKS_tmin_asc[x].year if n <= qty else "",
                        WEEKS_tmin_asc[x].number if n <= qty else ""))
        if i > qty and j > qty and k > qty and l > qty and m > qty and n > qty: break

def monthRank(mo,attribute,qty):
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
    MONTHS_prcpDAYS = []
    MONTHS_snow = []
    MONTHS_snowDAYS = []
    MONTHS_tavg = []
    MONTHS_tmax = []
    MONTHS_tmin = []
    
    for y in [YR for YR in clmt if type(YR) == int]:
        try:
            if clmt[y][mo]["recordqty"] > 20:
                MONTHS_prcp.append(month_attr(y,mo,round(sum(clmt[y][mo]["prcp"]),2)))
                MONTHS_prcpDAYS.append(month_attr(y,mo,clmt[y][mo]["prcpDAYS"]))
            MONTHS_snow.append(month_attr(y,mo,round(sum(clmt[y][mo]["snow"]),1)))
            MONTHS_snowDAYS.append(month_attr(y,mo,clmt[y][mo]["snowDAYS"]))
        except:
            pass
        try:
            if clmt[y][mo]["recordqty"] > 20:
                try:
                    if len(clmt[y][mo]["tempAVGlist"]) > 20:
                        MONTHS_tavg.append(month_attr(y,mo,round(mean(clmt[y][mo]["tempAVGlist"]),1)))
                except:
                    pass
                try:
                    if len(clmt[y][mo]["tmax"]) > 20:
                        MONTHS_tmax.append(month_attr(y,mo,round(mean(clmt[y][mo]["tmax"]),1)))
                except:
                    pass
                try:
                    if len(clmt[y][mo]["tmin"]) > 20:
                        MONTHS_tmin.append(month_attr(y,mo,round(mean(clmt[y][mo]["tmin"]),1)))
                except:
                    pass
        except:
            pass

    MONTHS_prcp_asc = MONTHS_prcp.copy()
    MONTHS_prcp.sort(key=lambda x:x.number,reverse=True)
    MONTHS_prcp_asc.sort(key=lambda x:x.number)
    MONTHS_prcpDAYS_asc = MONTHS_prcpDAYS.copy()
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
    if attribute == "prcp":
        print("{:^100}".format("Ranked {} Monthly Precipitation Amounts and Days".format(calendar.month_name[mo])))
        print("{:^100}".format("{}, {}".format(clmt["station"],clmt["station_name"])))
        print("{:-^100}".format(""))
        print("{:^67}|{:^32}".format("Rain","Snow"))
        print("{:-^67}|{:-^32}".format("",""))
        print("{:^18}|{:^18}|{:^14}|{:^14}|{:^17}|{:^14}".format("Wettest","Driest","Most Days","Least Days","Snowiest","Most Days"))
        print("{:-^18}|{:-^18}|{:-^14}|{:-^14}|{:-^17}|{:-^14}".format("","","","","",""))
        i = 1;j = 1;k = 1;l = 1;m = 1;n = 1
        ranked_i = [];ranked_j = [];ranked_k = [];ranked_l = [];ranked_m = [];ranked_n = []
        for x in range(len(MONTHS_prcp)):
            if x == 0:
                print(" {:2}{} {:4}  {:6} | {:2}{} {:4}  {:6} | {:2}{} {:4}  {:2} | {:2}{} {:4}  {:2} | {:2}{} {:4}  {:5} | {:2}{} {:4}  {:2} ".format(
                    1,".",MONTHS_prcp[x].year,MONTHS_prcp[x].number,
                    1,".",MONTHS_prcp_asc[x].year,MONTHS_prcp_asc[x].number,
                    1,".",MONTHS_prcpDAYS[x].year,MONTHS_prcpDAYS[x].number,
                    1,".",MONTHS_prcpDAYS_asc[x].year,MONTHS_prcpDAYS_asc[x].number,
                    1 if MONTHS_snow[x].number else "","." if MONTHS_snow[x].number > 0 else " ",
                    MONTHS_snow[x].year if MONTHS_snow[x].number > 0 else "",MONTHS_snow[x].number if MONTHS_snow[x].number > 0 else "",
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
                    print(" {:2}{} {:4}  {:6} | {:2}{} {:4}  {:6} | {:2}{} {:4}  {:2} | {:2}{} {:4}  {:2} | {:2}{} {:4}  {:5} | {:2}{} {:4}  {:2} ".format(
                        i if i not in ranked_i and i <= qty else "","." if i not in ranked_i and i <= qty else " ",
                        MONTHS_prcp[x].year if i <= qty else "",MONTHS_prcp[x].number if i <= qty else "",
                        j if j not in ranked_j and j <= qty else "","." if j not in ranked_j and j <= qty else " ",
                        MONTHS_prcp_asc[x].year if j <= qty else "",MONTHS_prcp_asc[x].number if j <= qty else "",
                        k if k not in ranked_k and k <= qty else "","." if k not in ranked_k and k <= qty else " ",
                        MONTHS_prcpDAYS[x].year if k <= qty else "",MONTHS_prcpDAYS[x].number if k <= qty else "",
                        l if l not in ranked_l and l <= qty else "","." if l not in ranked_l and l <= qty else " ",
                        MONTHS_prcpDAYS_asc[x].year if l <= qty else "",MONTHS_prcpDAYS_asc[x].number if l <= qty else "",
                        m if m not in ranked_m and m <= qty else "","." if m not in ranked_m and m <= qty else " ",
                        MONTHS_snow[x].year if m <= qty else "",MONTHS_snow[x].number if m <= qty else "",
                        n if n not in ranked_n and n <= qty else "","." if n not in ranked_n and n <= qty else " ",
                        MONTHS_snowDAYS[x].year if n <= qty else "",MONTHS_snowDAYS[x].number if n <= qty else ""))
            if i > qty and j > qty and k > qty and l > qty and m > qty and n > qty: break
    if attribute == "temp":
        print("\n{:^111}".format("Ranked {} Monthly Temperatures".format(calendar.month_name[mo])))
        print("{:^111}".format("{}, {}".format(clmt["station"],clmt["station_name"])))
        print("{:-^111}".format(""))
        print("{:^36}|{:^37}|{:^36}".format("AVG TEMP","TMAX","TMIN"))
        print("{:-^36}|{:-^37}|{:-^36}".format("","",""))
        print("{:^17}|{:^18}|{:^18}|{:^18}|{:^18}|{:^17}".format("Warmest","Coolest","Warmest","Coolest","Warmest","Coolest"))
        print("{:-^17}|{:-^18}|{:-^18}|{:-^18}|{:-^18}|{:-^17}".format("","","","","",""))
        i = 1; j = 1; k = 1; l = 1; m = 1; n = 1
        ranked_i = []; ranked_j = []; ranked_k = []; ranked_l = []; ranked_m = []; ranked_n = []
        for x in range(len(MONTHS_tmax)):
            if x == 0:
                print("{:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}".format(
                                                                1,".",MONTHS_tavg[x].year,MONTHS_tavg[x].number,
                                                                1,".",MONTHS_tavg_asc[x].year,MONTHS_tavg_asc[x].number,
                                                                1,".",MONTHS_tmax[x].year,MONTHS_tmax[x].number,
                                                                1,".",MONTHS_tmax_asc[x].year,MONTHS_tmax_asc[x].number,
                                                                1,".",MONTHS_tmin[x].year,MONTHS_tmin[x].number,
                                                                1,".",MONTHS_tmin_asc[x].year,MONTHS_tmin_asc[x].number))
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
                    print("{:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}".format(
                            i if i not in ranked_i and i <= qty else "","." if i not in ranked_i and i <= qty else " ",
                            MONTHS_tavg[x].year if i <= qty else "",MONTHS_tavg[x].number if i <= qty else "",
                            j if j not in ranked_j and j <= qty else "","." if j not in ranked_j and j <= qty else " ",
                            MONTHS_tavg_asc[x].year if j <= qty else "",MONTHS_tavg_asc[x].number if j <= qty else "",
                            k if k not in ranked_k and k <= qty else "","." if k not in ranked_k and k <= qty else " ",
                            MONTHS_tmax[x].year if k <= qty else "",MONTHS_tmax[x].number if k <= qty else "",
                            l if l not in ranked_l and l <= qty else "","." if l not in ranked_l and l <= qty else " ",
                            MONTHS_tmax_asc[x].year if l <= qty else "",MONTHS_tmax_asc[x].number if l <= qty else "",
                            m if m not in ranked_m and m <= qty else "","." if m not in ranked_m and m <= qty else " ",
                            MONTHS_tmin[x].year if m <= qty else "",MONTHS_tmin[x].number if m <= qty else "",
                            n if n not in ranked_n and n <= qty else "","." if n not in ranked_n and n <= qty else " ",
                            MONTHS_tmin_asc[x].year if n <= qty else "",MONTHS_tmin_asc[x].number if n <= qty else ""))
            if i > qty and j > qty and k > qty and l > qty and m > qty and n > qty: break

def yearRank(attribute,qty):
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
    YEARS_prcpDAYS = []
    YEARS_snow = []
    YEARS_snowDAYS = []
    YEARS_tavg = []
    YEARS_tmax = []
    YEARS_tmin = []
    
    for y in [YR for YR in clmt if type(YR) == int]:
        try:
            if clmt[y]["recordqty"] > 300:
                YEARS_prcp.append(month_attr(y,round(sum(clmt[y]["prcp"]),2)))
                YEARS_prcpDAYS.append(month_attr(y,clmt[y]["prcpDAYS"]))
            YEARS_snow.append(month_attr(y,round(sum(clmt[y]["snow"]),1)))
            YEARS_snowDAYS.append(month_attr(y,clmt[y]["snowDAYS"]))
        except:
            pass
        try:
            if clmt[y]["recordqty"] > 300:
                try:
                    if len(clmt[y]["tempAVGlist"]) > 600:
                        YEARS_tavg.append(month_attr(y,round(mean(clmt[y]["tempAVGlist"]),1)))
                except:
                    pass
                try:
                    if len(clmt[y]["tmax"]) > 300:
                        YEARS_tmax.append(month_attr(y,round(mean(clmt[y]["tmax"]),1)))
                except:
                    pass
                try:
                    if len(clmt[y]["tmin"]) > 300:
                        YEARS_tmin.append(month_attr(y,round(mean(clmt[y]["tmin"]),1)))
                except:
                    pass
        except:
            pass

    YEARS_prcp_asc = YEARS_prcp.copy()
    YEARS_prcp.sort(key=lambda x:x.number,reverse=True)
    YEARS_prcp_asc.sort(key=lambda x:x.number)
    YEARS_prcpDAYS_asc = YEARS_prcpDAYS.copy()
    YEARS_prcpDAYS.sort(key=lambda x:x.number,reverse=True)
    YEARS_prcpDAYS_asc.sort(key=lambda x:x.number)
    YEARS_snow.sort(key=lambda x:x.number,reverse=True)
    YEARS_snowDAYS.sort(key=lambda x:x.number,reverse=True)
    YEARS_tavg_asc = YEARS_tavg.copy()
    YEARS_tavg.sort(key=lambda x:x.number,reverse=True)
    YEARS_tavg_asc.sort(key=lambda x:x.number)
    YEARS_tmax_asc = YEARS_tmax.copy()
    YEARS_tmax.sort(key=lambda x:x.number,reverse=True)
    YEARS_tmax_asc.sort(key=lambda x:x.number)
    YEARS_tmin_asc = YEARS_tmin.copy()
    YEARS_tmin.sort(key=lambda x:x.number,reverse=True)
    YEARS_tmin_asc.sort(key=lambda x:x.number)
    """
    with open("htmltest2.html","w") as h:
        h.write("<!DOCTYPE html>\n")
        h.write("<html>\n")
        h.write("\t<head>\n")
        h.write("\t\t<title>Year Rank</title>\n")
        h.write("\t\t<style>\n")
        h.write(
			.tabl {
				display: table;
				width:100%;
				max-width:600px;
				min-width:500px;
				border-collapse: collapse;
			}
			.row {
				display: table-row;
			}
			.col {
				display: table-cell;
				border: 1px solid black;
				text-align: center;
				vertical-align: middle;
			}

        divcol = '<div class="col" style="font-weight:bold;">'
        h.write("\t\t</style>\n")
        h.write("\t</head>\n")
        h.write('\t<body style="margin:auto;">\n')
        h.write('\t\t')
        h.write("YEAR RANK\n")
        h.write('\t\t<div class="tabl">\n')
        h.write('\t\t\t<div class="row">\n')
        for xyz in ["Rank","TAVG MAX","TAVG min"]:
            h.write('\t\t\t\t{}{}</div>\n'.format(divcol,xyz))
        h.write('\t\t\t</div>\n')
        h.write('\t\t\t\t')
        """

        
    
    if attribute == "prcp":
        print("{:^103}".format("Ranked Yearly Precipitation Amounts and Days"))
        print("{:^103}".format("{}, {}".format(clmt["station"],clmt["station_name"])))
        print("{:-^103}".format(""))
        print("{:^69}|{:^33}".format("Rain","Snow"))
        print("{:-^69}|{:-^33}".format("",""))
        print("{:^18}|{:^18}|{:^15}|{:^15}|{:^17}|{:^15}".format("Wettest","Driest","Most Days","Least Days","Snowiest","Most Days"))
        print("{:-^18}|{:-^18}|{:-^15}|{:-^15}|{:-^17}|{:-^15}".format("","","","","",""))
        i = 1;j = 1;k = 1;l = 1;m = 1;n = 1
        ranked_i = [];ranked_j = [];ranked_k = [];ranked_l = [];ranked_m = [];ranked_n = []
        for x in range(len(YEARS_prcp)):
            if x == 0:
                print(" {:2}{} {:4}  {:6} | {:2}{} {:4}  {:6} | {:2}{} {:4}  {:3} | {:2}{} {:4}  {:3} | {:2}{} {:4}  {:5} | {:2}{} {:4}  {:3} ".format(
                    1,".",YEARS_prcp[x].year,YEARS_prcp[x].number,
                    1,".",YEARS_prcp_asc[x].year,YEARS_prcp_asc[x].number,
                    1,".",YEARS_prcpDAYS[x].year,YEARS_prcpDAYS[x].number,
                    1,".",YEARS_prcpDAYS_asc[x].year,YEARS_prcpDAYS_asc[x].number,
                    1 if YEARS_snow[x].number else "","." if YEARS_snow[x].number > 0 else " ",
                    YEARS_snow[x].year if YEARS_snow[x].number > 0 else "",YEARS_snow[x].number if YEARS_snow[x].number > 0 else "",
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
                    print(" {:2}{} {:4}  {:6} | {:2}{} {:4}  {:6} | {:2}{} {:4}  {:3} | {:2}{} {:4}  {:3} | {:2}{} {:4}  {:5} | {:2}{} {:4}  {:3} ".format(
                        i if i not in ranked_i and i <= qty else "","." if i not in ranked_i and i <= qty else " ",
                        YEARS_prcp[x].year if i <= qty else "",YEARS_prcp[x].number if i <= qty else "",
                        j if j not in ranked_j and j <= qty else "","." if j not in ranked_j and j <= qty else " ",
                        YEARS_prcp_asc[x].year if j <= qty else "",YEARS_prcp_asc[x].number if j <= qty else "",
                        k if k not in ranked_k and k <= qty else "","." if k not in ranked_k and k <= qty else " ",
                        YEARS_prcpDAYS[x].year if k <= qty else "",YEARS_prcpDAYS[x].number if k <= qty else "",
                        l if l not in ranked_l and l <= qty else "","." if l not in ranked_l and l <= qty else " ",
                        YEARS_prcpDAYS_asc[x].year if l <= qty else "",YEARS_prcpDAYS_asc[x].number if l <= qty else "",
                        m if m not in ranked_m and m <= qty else "","." if m not in ranked_m and m <= qty else " ",
                        YEARS_snow[x].year if m <= qty else "",YEARS_snow[x].number if m <= qty else "",
                        n if n not in ranked_n and n <= qty else "","." if n not in ranked_n and n <= qty else " ",
                        YEARS_snowDAYS[x].year if n <= qty else "",YEARS_snowDAYS[x].number if n <= qty else ""))
            if i > qty and j > qty and k > qty and l > qty and m > qty and n > qty: break
    if attribute == "temp":
        print("\n{:^111}".format("Ranked Yearly Temperatures"))
        print("{:^111}".format("{}, {}".format(clmt["station"],clmt["station_name"])))
        print("{:-^111}".format(""))
        print("{:^36}|{:^37}|{:^36}".format("AVG TEMP","TMAX","TMIN"))
        print("{:-^36}|{:-^37}|{:-^36}".format("","",""))
        print("{:^17}|{:^18}|{:^18}|{:^18}|{:^18}|{:^17}".format("Warmest","Coolest","Warmest","Coolest","Warmest","Coolest"))
        print("{:-^17}|{:-^18}|{:-^18}|{:-^18}|{:-^18}|{:-^17}".format("","","","","",""))
        i = 1; j = 1; k = 1; l = 1; m = 1; n = 1
        ranked_i = []; ranked_j = []; ranked_k = []; ranked_l = []; ranked_m = []; ranked_n = []
        for x in range(len(YEARS_tmax)):
            if x == 0:
                print("{:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}".format(
                                                                1,".",YEARS_tavg[x].year,YEARS_tavg[x].number,
                                                                1,".",YEARS_tavg_asc[x].year,YEARS_tavg_asc[x].number,
                                                                1,".",YEARS_tmax[x].year,YEARS_tmax[x].number,
                                                                1,".",YEARS_tmax_asc[x].year,YEARS_tmax_asc[x].number,
                                                                1,".",YEARS_tmin[x].year,YEARS_tmin[x].number,
                                                                1,".",YEARS_tmin_asc[x].year,YEARS_tmin_asc[x].number))
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
                    print("{:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}  | {:2}{} {:4}  {:5}".format(
                            i if i not in ranked_i and i <= qty else "","." if i not in ranked_i and i <= qty else " ",
                            YEARS_tavg[x].year if i <= qty else "",YEARS_tavg[x].number if i <= qty else "",
                            j if j not in ranked_j and j <= qty else "","." if j not in ranked_j and j <= qty else " ",
                            YEARS_tavg_asc[x].year if j <= qty else "",YEARS_tavg_asc[x].number if j <= qty else "",
                            k if k not in ranked_k and k <= qty else "","." if k not in ranked_k and k <= qty else " ",
                            YEARS_tmax[x].year if k <= qty else "",YEARS_tmax[x].number if k <= qty else "",
                            l if l not in ranked_l and l <= qty else "","." if l not in ranked_l and l <= qty else " ",
                            YEARS_tmax_asc[x].year if l <= qty else "",YEARS_tmax_asc[x].number if l <= qty else "",
                            m if m not in ranked_m and m <= qty else "","." if m not in ranked_m and m <= qty else " ",
                            YEARS_tmin[x].year if m <= qty else "",YEARS_tmin[x].number if m <= qty else "",
                            n if n not in ranked_n and n <= qty else "","." if n not in ranked_n and n <= qty else " ",
                            YEARS_tmin_asc[x].year if n <= qty else "",YEARS_tmin_asc[x].number if n <= qty else ""))
            if i > qty and j > qty and k > qty and l > qty and m > qty and n > qty: break

def seasonStats(y,season):
    if type(season) != str and season.lower() not in ["spring","summer","fall","autumn","winter"]: return print("* OOPS! '{}' is not a valid season. Try again!".format(season))
    #season = season.lower()
    if type(y) != int and y not in [YR for YR in clmt if type(YR) == int]: return print("* Hmm. No record for {} was found. Try again!".format(y))
    if season.lower() == "spring": months = [3,4,5]
    elif season.lower() == "summer": months = [6,7,8]
    elif season.lower() == "fall" or season.lower() == "autumn": months = [9,10,11]
    elif season.lower() == "winter": months = [12,1,2]     # WINTER
    #        alltime = {"years":(valid_yrs[0],valid_yrs[len(valid_yrs)-1]),
    #                   "prcp": [],"prcpPROP":{"day_max":[-1,[]]},
    #                   "snow": [],"snowPROP":{"day_max":[-1,[]]},
    #                   "tmax": [],"tmaxPROP":{"day_max":[-999,[]],"day_min":[999,[]]},
    #                   "tmin": [],"tminPROP":{"day_max":[-999,[]],"day_min":[999,[]]}}
    # Record qty
    rqty = 0

    # Other vars
    season_prcp = 0
    season_prcpDAYS = 0
    season_prcpPROP = {"day_max":[-1,[]],"month_max":[-1,[]]}
    for m in months:
        try:
            rqty += clmt[y][m]["recordqty"]
            season_prcp += sum(clmt[y][m]["prcp"])
            season_prcpDAYS += clmt[y][m]["prcpDAYS"]
            if clmt[y][m]["prcpPROP"]["day_max"][0] == season_prcpPROP["day_max"][0]: season_prcpPROP["day_max"][1].append(clmt[y][m]["prcpPROP"]["day_max"][1])
            elif clmt[y][m]["prcpPROP"]["day_max"][0] > season_prcpPROP["day_max"][0]:
                season_prcpPROP["day_max"][0] = clmt[y][m]["prcpPROP"]["day_max"][0]
                season_prcpPROP["day_max"][1] = []
                season_prcpPROP["day_max"][1].append(clmt[y][m]["prcpPROP"]["day_max"][1])
        except:
            pass

def seasonReport():
	pass

def seasonRank():
    pass

def metYearStats():
    pass

def metYearReport():
    pass

def metYearRank():
    pass

def csvFileList():
    tempcsvlist = os.listdir()
    csvs_in_dir = [x for x in tempcsvlist if x[len(x)-3:] == "csv"]

    print("CSV's in Current Directory w/Convenient Basic Copy/Paste Loading Calls:")
    print("----------------------------------------------------------")
    for each in csvs_in_dir:
        print(".. {:<40} ::   {}".format(each,'clmtAnalyze("{}")'.format(each)))
    print("")

def clmthelp():
    print("* PLEASE SEE README.md FOR A FULL BREAKDOWN OF PROGRAM'S CAPABILITIES *")
    print("* TO START: -execute clmtAnalyze('your_csv_file.csv'")
    print("            -takes optional keyword arguments <city> and <station>")
    print("            -If needed, execute the csvFileList() function to see a list of csv files in the ")
    print("             current directory")
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
    print("    Climatology Functions :: Detailed stats based on 30-yr climatologies incremented by")
    print("       5 years and enables basic climatological tendency analysis")
    print("    -- dayReport(month,day) :: Returns detailed statistics and climatology for all specified")
    print("       days in the record")
    print("    -- weekReport(month,day) :: Returns detailed statistics and climatology for determined 7-day")
    print("       period and the included day will be the center of the week")
    print("    -- monthReport(month) :: Returns detailed statistics and climatology for the specified month")
    print("    -- yearReport() :: NOTHING is passed to this function. It returns detailed statistics based ")
    print("       on data for all years")
    print("    Rank/Record Functions")
    print("    -- dayRank(month,day,howmany) :: Prints daily records from the climate data.")
    print("    -- weekRank(month,day,howmany) :: Prints records based on a week's period, centered on the ")
    print("       day entered (3 days before; 3 after)")
    print("    -- monthRank(month,'<temps>|<rain>',howmany) :: Prints month-based records for the given month")
    print("    -- yearRank('<temps>|<rain>',howmany) :: Prints yearly-based records for the entire record (Jan-Dec)")

def corrections():

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

# MAIN PROGRAM --------------------------------------------------------------
clmt = {}
ignoreflags = [""]
FILE = None

# WELCOME MESSAGE UPON STARTING
print("************************************")
print("CLIMATE PARSER (clmt-parser.py) v1.8")
print("  by K. Gentry (ksgwxfan)")
print("************************************\n")

print(" INSTRUCTIONS: (*** See README.md for data retrieval and exensive instructions ***)")
print('    1) Find the filename of your .csv, then run clmtAnalyze("citydata.csv")')
print("       -- csvFileList() will return a list of all csv's in the working directory and")
print("          their basic calls")
print("       -- OPTIONAL keyword arguments for station ID and city:")
print('             clmtAnalyze("citydata.csv",city="CITY NAME, USA",station="2 Stations")')
print("    2) After completion, you can then run reports on the data")
print(" -------------------------------------------------------------------------------------")
print(" For more detailed assistance, enter clmthelp() for a breakdown of available functions")
print(" that you can use once the data is mounted")
print(" -------------------------------------------------------------------------------------")
