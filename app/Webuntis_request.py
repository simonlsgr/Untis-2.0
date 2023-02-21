import json
import requests
import datetime
import itertools


### WEBUNTIS REQUEST ###


class WebUntis_request:
    def __init__(self, element_type, element_id, date, schoolname):
        self.element_type = str(element_type)
        self.element_id = str(element_id)
        self.date = str(date)
        self.schoolname = str(schoolname)
        
    def API_call(self) -> None:
        
        
        url_get_cookies = f'https://ikarus.webuntis.com/WebUntis/?school={self.schoolname}#/basic/timetable'

        response_get_cookies = requests.get(url_get_cookies)

        jsessionid_cookies = response_get_cookies.headers['Set-Cookie'].split(';')[0].split('=')[1]

        schoolname_cookies = response_get_cookies.headers['Set-Cookie'].split(';')[4].split('=')[2]

        url = "https://ikarus.webuntis.com/WebUntis/api/public/timetable/weekly/data"

        querystring = {"elementType": self.element_type,"elementId": self.element_id,"date": self.date}

        payload = ""
        headers = {
            "cookie": "schoolname="+schoolname_cookies+"; traceId=dbb69fa1e2dc8af353694414c2035671990c360d; JSESSIONID="+jsessionid_cookies+"",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://ikarus.webuntis.com/WebUntis/?school="+self.schoolname+"",
            "DNT": "1",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

        with open("app/src/webuntis_data/data_unformatted_"+self.element_id+".json", "w") as f:
            f.write(response.text)
        
        with open("app/src/webuntis_data/data_unformatted_"+self.element_id+".json", "r") as f:
            data = json.load(f)


        date_list = [[],[],[],[],[]]
        
        try:
            for i,j in enumerate(data["data"]["result"]["data"]["elementPeriods"][self.element_id]):
                untis_date = str(j["date"])
                untis_start_time = str(j["startTime"])
                if len(untis_start_time) == 3:
                    untis_start_time = "0" + untis_start_time
                
                date = datetime.datetime(year=int(untis_date[0:4]), month=int(untis_date[4:6]), day=int(untis_date[6:8]), hour=int(untis_start_time[0:2]), minute=int(untis_start_time[2:4]))
                j["datetime_start"] = str(date)
                date_list[date.weekday()].append(j)
        except:
            with open("app/src/webuntis_data/data_formatted_"+self.element_id+".json", "w") as f:
                f.write(json.dumps(["0"], indent=4))
            return None


        for i, j in enumerate(date_list):
            j.sort(key=lambda x: x["datetime_start"])

        for i, j in enumerate(date_list):
            temp_list = []
            for k, g in itertools.groupby(j, key=lambda x: x["startTime"]):
                temp_list.append(list(g))
            date_list[i] = temp_list
            

            
        start_times = []    
        for i, j in enumerate(date_list):
            for k, l in enumerate(j):
                if l[0]["startTime"] not in start_times:
                    start_times.append(l[0]["startTime"])
        start_times.sort()
        

        new_date_list = [[],[],[],[],[]]

        for i, j in enumerate(new_date_list):
            new_date_list[i] = [[] for k in range(len(start_times))]

        for i, j in enumerate(date_list):
            for k, l in enumerate(j):
                for m, n in enumerate(start_times):
                    if l[0]["startTime"] == n:
                        new_date_list[i][m] = l

        date_list = new_date_list
            

        with open("app/src/webuntis_data/data_formatted_"+self.element_id+".json", "w") as f:
            f.write(json.dumps(date_list, indent=4))
        
        subjects = response.text
        subjects = json.loads(subjects)["data"]["result"]["data"]["elements"]
        with open("app/src/webuntis_data/subjects_"+self.element_id+".json", "w") as f:
            f.write(json.dumps(subjects))
        return None
    

if __name__ == "__main__":
    WebUntis_request(1, 475, "2023-02-20", "hh5864").API_call()
    WebUntis_request(1, 187, "2023-02-20", "hh5846").API_call()
      
