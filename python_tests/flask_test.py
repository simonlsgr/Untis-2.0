import flask
import json
import sys

app = flask.Flask(__name__)

@app.route("/")
def index():
    with open("test_output.json", "r") as f:
        data = json.load(f)
    with open("test.json", "r") as f:
        subjects = json.load(f)
    
    subjects = subjects["data"]["result"]["data"]["elements"]
    
    placeholder = ["", "", "", "", ""]
    # times = []
    # for i, j in enumerate(data):
    #     for k, l in enumerate(j):
    #         if not any(d["startTime"] == l[0]["startTime"] for d in times):
    #             times.append({"startTime": l[0]["startTime"], "endTime": l[0]["endTime"]})
    
    # # sort times
    # times.sort(key=lambda x: x["startTime"])
    # print(json.dumps(times, indent=4), file=sys.stderr)
    # times_placeholder = "<div class=\"time\">"
    # for i, j in enumerate(times):
    #     times_placeholder += f"""<div class="time">{j["startTime"]}-{j["endTime"]}</div>"""
    # times_placeholder += "</div>"
            
    
    ## weekdays (from 0 to 4)
    # for i, j in enumerate(data):
    #     counter += 1
    #     # periods (from 0 to n)
    #     for k, l in enumerate(j):
    #         counter += 1
    #         placeholder[i] += f"""<form class="period"><div class="period_time">{l[0]["startTime"]}-{l[0]["endTime"]}</div>"""
    #         counter = 0
    #         for m, n in enumerate(l):
    #             counter += 1
                
    #             try:
    #                 for o, p in enumerate(subjects):
    #                     counter += 1
    #                     if p["id"] == n["elements"][0]["id"]:
    #                         subject = "<div class=\"subject_name\"><div class=\"subject_short_name\">"+ p["name"] + "</div><div class=\"subject_long_name\">" + p["longName"] + "</div></div>"
    #                     elif p["id"] == n["elements"][1]["id"]:
    #                         if p["name"] == p["longName"]:
    #                             room = "<div class=\"room_name\">" + p["name"] + "</div>"
    #                         else:
    #                             room = "<div class=\"room_name\">" + p["name"] + " (" + p["longName"] + ")</div>"
    #                 # subject = str(n["elements"][0]["id"])
    #                 # room = str(n["elements"][1]["id"])
    #                 id_for_checkbox = n["id"]
    #                 placeholder[i] += f"""<input type="checkbox" id="checkbox_number_{id_for_checkbox}"><label for="checkbox_number_{id_for_checkbox}" class="subject"><div class="info">{subject}{room}</div></label>"""
    #             except IndexError:
    #                 continue
    #                 # print(placeholder[i], file=sys.stderr)
                    
                    
    #         placeholder[i] += "</form>"
    
    timetable_html_element = ""
    # loop through the lessons of a day
    # for index_lesson, lesson in enumerate(data[0]):
    #     # loop through each day
    for index_day, day in enumerate(data):
        timetable_html_element += f"""<div class="day"><div class="day_name">{index_day}</div>"""
        for index_lessons_in_day, lessons_in_day in enumerate(day):
            timetable_html_element += f"""<form class="period"><div class="period_time"></div>"""
            for index_lessons_in_day_lesson, lessons_in_day_lesson in enumerate(lessons_in_day):
                try:
                    for o, p in enumerate(subjects):
                        if p["id"] == lessons_in_day_lesson["elements"][0]["id"]:
                            subject = "<div class=\"subject_name\"><div class=\"subject_short_name\">"+ p["name"] + "</div><div class=\"subject_long_name\">" + p["longName"] + "</div></div>"
                        elif p["id"] == lessons_in_day_lesson["elements"][1]["id"]:
                            if p["name"] == p["longName"]:
                                room = "<div class=\"room_name\">" + p["name"] + str(lessons_in_day_lesson["startTime"]) + "</div>"
                            else:
                                room = "<div class=\"room_name\">" + p["name"] + " (" + p["longName"] +str(lessons_in_day_lesson["startTime"]) +  ")</div>"
                    # subject = str(n["elements"][0]["id"])
                    # room = str(n["elements"][1]["id"])
                    id_for_checkbox = lessons_in_day_lesson["id"]
                    timetable_html_element += f"""<input type="checkbox" id="checkbox_number_{id_for_checkbox}"><label for="checkbox_number_{id_for_checkbox}" class="subject"><div class="info">{subject}{room}</div></label>"""
                    # placeholder[i] += f"""<input type="checkbox" id="checkbox_number_{id_for_checkbox}"><label for="checkbox_number_{id_for_checkbox}" class="subject"><div class="info">{subject}{room}</div></label>"""
                except IndexError:
                    continue
                    # print(placeholder[i], file=sys.stderr)
            timetable_html_element += "</form>"    
        timetable_html_element += "</div>"
            # print(lessons_in_day, file=sys.stderr)
            
            
        
        
            
                
        
            
                        
            
        
    
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{flask.url_for('static', filename='css/main.css')}">
    <title>Document</title>
</head>
<body>
<div class="container">
{timetable_html_element}
</div>

</body>
</html>"""
    return html

# <div class="weekday monday"><h1>Monday</h1><div class="day">{placeholder[0]}</div></div>
# <div class="weekday tuesday"><h1>Tuesday</h1><div class="day">{placeholder[1]}</div></div>
# <div class="weekday wednesday"><h1>Wednesday</h1><div class="day">{placeholder[2]}</div></div>
# <div class="weekday thursday"><h1>Thursday</h1><div class="day">{placeholder[3]}</div></div>
# <div class="weekday friday"><h1>Friday</h1><div class="day">{placeholder[4]}</div></div>

if __name__ == "__main__":
    app.run(debug=True)