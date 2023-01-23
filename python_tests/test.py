import json
import requests
import datetime
import itertools


### WEBUNTIS REQUEST ###

url = "https://ikarus.webuntis.com/WebUntis/api/public/timetable/weekly/data"

querystring = {"elementType":"1","elementId":"187","date":"2023-01-30"}

payload = ""
headers = {
    "cookie": "schoolname=%22_aGg1ODQ2%22; traceId=dbb69fa1e2dc8af353694414c2035671990c360d; JSESSIONID=4A9A47A4A726D2C56A3464F58F4AC75C",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://ikarus.webuntis.com/WebUntis/?school=hh5846",
    "DNT": "1",
    "Connection": "keep-alive",
    "Cookie": "traceId=e09d53487ed6066b8abffd29aed5cc75a9a1a4b0; schoolname=\"_aGg1ODQ2\"; schoolname=\"_aGg1ODQ2\"; JSESSIONID=B1E7E1D372B14ECCFEE5474DC920600E; schoolname=\"_aGg1ODQ2\"; traceId=e09d53487ed6066b8abffd29aed5cc75a9a1a4b0",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

with open("python_tests/test.json", "w") as f:
    f.write(response.text)

###

blocked_ids = []


with open("python_tests/test.json") as f:
    data = json.load(f)

# for i, j in enumerate(data["data"]["result"]["data"]["elementPeriods"]["187"]):
#     if j["hasPeriodText"]:
#         try:
#             print(j["periodText"])
#         except KeyError:
#             try: 
#                 print(j["substText"])
#             except KeyError:
#                 pass
#         print(j["startTime"])
#         print(j["endTime"])
#         for k, l in enumerate(j["elements"]):
#             for m, n in enumerate(data["data"]["result"]["data"]["elements"]):
#                 if n["id"] == l["id"]:
#                     print(n["name"])
#                     print(n["longName"])
#         print()
#         print()


date_list = [[],[],[],[],[]]

for i,j in enumerate(data["data"]["result"]["data"]["elementPeriods"]["187"]):
    untis_date = str(j["date"])
    untis_start_time = str(j["startTime"])
    if len(untis_start_time) == 3:
        untis_start_time = "0" + untis_start_time
    
    date = datetime.datetime(year=int(untis_date[0:4]), month=int(untis_date[4:6]), day=int(untis_date[6:8]), hour=int(untis_start_time[0:2]), minute=int(untis_start_time[2:4]))
    j["datetime_start"] = str(date)
    date_list[date.weekday()].append(j)


for i, j in enumerate(date_list):
    j.sort(key=lambda x: x["datetime_start"])

for i, j in enumerate(date_list):
    temp_list = []
    for k, g in itertools.groupby(j, key=lambda x: x["startTime"]):
        temp_list.append(list(g))
    date_list[i] = temp_list
    print(i)

    
start_times = []    
for i, j in enumerate(date_list):
    for k, l in enumerate(j):
        if l[0]["startTime"] not in start_times:
            start_times.append(l[0]["startTime"])
start_times.sort()
print(json.dumps(start_times, indent=4))

new_date_list = [[],[],[],[],[]]

for i, j in enumerate(new_date_list):
    new_date_list[i] = [[] for k in range(len(start_times))]

for i, j in enumerate(date_list):
    for k, l in enumerate(j):
        for m, n in enumerate(start_times):
            if l[0]["startTime"] == n:
                new_date_list[i][m] = l

date_list = new_date_list
    

with open("python_tests/test_output.json", "w") as f:
    f.write(json.dumps(date_list, indent=4))
      
