import os
import random
import time
import requests
import json
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


# https://www.weather.gov/wrh/climate

def get_weather(sid: str, sDate: str, eDate: str):

    # URL endpoint
    url = "https://data.rcc-acis.org/StnData"

    # Parameters from your network tab
    params = {
        "elems": [
            {"name": "maxt", "add": "t"},
            {"name": "mint", "add": "t"},
            # {"name": "avgt", "add": "t"},
            # {"name": "avgt", "normal": "departure91", "add": "t"},
            # {"name": "hdd", "add": "t"},
            # {"name": "cdd", "add": "t"},
            {"name": "pcpn", "add": "t"},
            {"name": "snow", "add": "t"},
            {"name": "snwd", "add": "t"}
        ],
        "sid": sid,
        "sDate": sDate,
        "eDate": eDate
    }

    # The website sends this JSON as URL-encoded form data
    payload = {"params": json.dumps(params), "output": "json"}

    # Optional headers (some endpoints require a User-Agent)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "python-requests/2.x"
    }

    # Make the POST request
    response = requests.post(url, data=payload, headers=headers)

    # Check response
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            # print(json.dumps(data, indent=2))  # pretty-print
            return data['data']
        else:
            print("Error:", data)

    else:
        print("Error:", response.status_code)


def get_stations(region: str):
    response = requests.get(f'https://nowdata.rcc-acis.org/{region}/station_list.txt')
    if response.status_code == 200:
        return response.json()
    else:
        # afc - https://nowdata.rcc-acis.org/pafc/station_list.txt
        # afg - https://nowdata.rcc-acis.org/pafg/station_list.txt
        # ajk - https://nowdata.rcc-acis.org/pajk/station_list.txt
        # hfo - https://nowdata.rcc-acis.org/hnl/station_list.txt

        response = requests.get(f'https://nowdata.rcc-acis.org/p{region}/station_list.txt')
        if response.status_code == 200:
                return response.json()
        else:
            if region == "hfo":
                response = requests.get(f'https://nowdata.rcc-acis.org/hnl/station_list.txt')
                if response.status_code == 200:
                    return response.json()
            elif region == "ppg":
                response = requests.get(f'https://nowdata.rcc-acis.org/samoa/station_list.txt')
                if response.status_code == 200:
                    return response.json()
            elif region == "gum":
                response = requests.get(f'https://nowdata.rcc-acis.org/guam/station_list.txt')
                if response.status_code == 200:
                    return response.json()
                

        print("Error:", response.status_code)





# https://nowdata.rcc-acis.org/slc/station_list.txt
# https://nowdata.rcc-acis.org/gjt/station_list.txt
# https://nowdata.rcc-acis.org/car/station_list.txt


def scrape_empty_dates(file_path):


    lines = []
    with open(file_path, "r") as f:
        lines = f.readlines()

    if len(lines) == 0: 
        return

    with open(file_path, "w") as f:
        f.write(lines[0])
        
        line_found_with_date = False
        for i in range(0, len(lines)):
            line = lines[i]
            if "M,M,M,M,M" not in line and i != 0:
                line_found_with_date = True

            if line_found_with_date:
                f.write(line)

def fix_up():


    for root, dirs, files in os.walk("."):
        for name in files:

            file_path = os.path.join(root, name)
            if file_path.endswith(".csv"):
                print(file_path)
                scrape_empty_dates(file_path)



REGIONS = [
    "abq",
    "abr",
    "afc",
    "afg",
    "ajk",
    "akq",
    "aly",
    "ama",
    "apx",
    "arx",
    "bgm",
    "bis",
    "bmx",
    "boi",
    "bou",
    "box",
    "bro",
    "btv",
    "buf",
    "byz",
    "cae",
    "car",
    "chs",
    "cle",
    "crp",
    "ctp",
    "cys",
    "ddc",
    "dlh",
    "dmx",
    "dtx",
    "dvn",
    "eax",
    "eka",
    "epz",
    "ewx",
    "ffc",
    "fgf",
    "fgz",
    "fsd",
    "fwd",
    "ggw",
    "gid",
    "gjt",
    "gld",
    "grb",
    "grr",
    "gsp",
    "gum",
    "gyx",
    "hfo",
    "hgx",
    "hnx",
    "hun",
    "ict",
    "ilm",
    "iln",
    "ilx",
    "ind",
    "iwx",
    "jan",
    "jax",
    "jkl",
    "lbf",
    "lch",
    "lix",
    "lkn",
    "lmk",
    "lot",
    "lox",
    "lsx",
    "lub",
    "lwx",
    "lzk",
    "maf",
    "meg",
    "mfl",
    "mfr",
    "mhx",
    "mkx",
    "mlb",
    "mob",
    "mpx",
    "mqt",
    "mrx",
    "mso",
    "mtr",
    "oax",
    "ohx",
    "okx",
    "otx",
    "oun",
    "pah",
    "pbz",
    "pdt",
    "phi",
    "pih",
    "ppg",
    "pqr",
    "psr",
    "pub",
    "rah",
    "rev",
    "riw",
    "rlx",
    "rnk",
    "sew",
    "sgf",
    "sgx",
    "shv",
    "sjt",
    "sju",
    "slc",
    "sto",
    "tae",
    "tbw",
    "tfx",
    "top",
    "tsa",
    "twc",
    "unr",
    "vef"
]



def download_all():

    for region in REGIONS:
        stations = get_stations(region)

        print()
        print(f'REGION {region}')
        print()
        os.makedirs(region, exist_ok=True)

        if stations == None:
            continue
        
        for station in stations:
            SID = station[0]

            FILE = f'{region}/{station[1].replace("/", "-")}.csv'
            SDATE = str(date(1850, 1, 1))
            EDATE = str(date(2025, 11, 30))
            print(FILE)

            if not os.path.exists(FILE):

                with open(FILE, "w") as f:


                    weather = get_weather(SID, SDATE, EDATE)
                    if weather != None:
                        f.write("date,max_temp_f,min_temp_f,precip_in,snow_in,snow_depth_in\n")
                        for day in weather:
                            entry_date = day[0]
                            max_t = day[1][0]
                            min_t = day[2][0]
                            precip = day[3][0]
                            snow = day[4][0]
                            snwd = day[5][0]
                            if max_t != 'M' or min_t != 'M' or precip != 'M' or snow != 'M' or snwd != 'M':
                                f.write(f'{entry_date},{max_t},{min_t},{precip},{snow},{snwd}\n')
                        f.flush() 


                short_mins_to_sleep = random.randint(int(0.01*60*1000), int(0.3*60*1000))/1000/60
                long_mins_to_sleep = random.randint(int(1*60*1000), int(1.1*60*1000))/1000/60
                mins_to_sleep = short_mins_to_sleep if random.randint(0, 100) < 90 else long_mins_to_sleep 
                print(f'sleeping {mins_to_sleep:.2f}min')
                time.sleep(mins_to_sleep * 60)


def get_oldest():

    oldest_ones = []
    for root, dirs, files in os.walk("."):
        for name in files:

            file_path = os.path.join(root, name)
            if file_path.endswith(".csv"):
                lines = []
                with open(file_path, "r") as f:
                    lines = f.readlines()

                if len(lines) != 0:

                    year = int(lines[1].split("-")[0])

                    if (year < 1900):
                        oldest_ones.append([year, file_path])
                
                # else:
                #     os.remove(file_path)

    oldest_ones.sort(key=lambda x: x[0])
    for year, file_path in oldest_ones:
        print(year, file_path)

get_oldest()