import flask
import json
import sys

app = flask.Flask(__name__)


def periods_in_a_week(timetable_formatted):
    list_of_periods = []
    for i, j in enumerate(timetable_formatted):
        for k, l in enumerate(j):
            for m, n in enumerate(l):
                if [n["startTime"], n["endTime"]] not in list_of_periods:
                    list_of_periods.append([n["startTime"], n["endTime"]])
                

    list_of_periods.sort()
    return list_of_periods


@app.route("/", methods=["GET", "POST"])
def index():
    
    
    with open("test_output.json", "r") as f:
        data = json.load(f)
    with open("test.json", "r") as f:
        subjects = json.load(f)
    
    subjects = subjects["data"]["result"]["data"]["elements"]
    
    list_of_subjects_id = []
    
    for i, j in enumerate(data):
        for k, l in enumerate(j):
            for m, n in enumerate(l):
                if n["id"] not in list_of_subjects_id:
                    list_of_subjects_id.append(n["id"])
    
    if flask.request.method == "POST":
        # for i, j in enumerate(list_of_checked_subjects):
        #     if flask.request.form.get(j):
        #         print("test")
        # return flask.redirect(flask.url_for("index"))
        # print(list_of_checked_subjects)
        for i, j in enumerate(list_of_subjects_id):
            if flask.request.form.get(str(j)):
                print(str(j))
        # if flask.request.form.getlist("376850"):
        #     print(flask.request.form.getlist("376850"))
    list_of_subjects_id.clear()
    
    
    
    
    


    list_of_periods = periods_in_a_week(data)
    
    timetable_html_element = ""
    
    
    timetable_html_element += f"""<form action="/" class="timetable_wrapper_form" method="POST">"""
    timetable_html_element += f"""<div class="timetable_wrapper">"""
    

    weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
    timetable_html_element += f"""<div class="weekday"></div>"""
    for index_tag, tag in enumerate(data):
        timetable_html_element += f"""<div class="weekday">{weekdays[index_tag]}</div>"""
        
        
    for index_stunde in range(len(data[0])):
        timetable_html_element += f"""<div class="period"><div class="period_time">{list_of_periods[index_stunde][0]}-{list_of_periods[index_stunde][1]}</div></div>"""
        for index_tag, tag in enumerate(data):
            timetable_html_element += f"""<div class="period"><div class="period_time">{index_stunde}</div>"""
            for index_fach, fach in enumerate(tag[index_stunde]):
                for index_element, element in enumerate(fach["elements"]):
                    for index_fach_informationen, fach_informationen in enumerate(subjects):
                        if fach_informationen["id"] == element["id"]:
                            
                            if index_element == 0:
                                fach_name = fach_informationen["name"]
                                fach_lang_name = fach_informationen["longName"]
                                
                                fach_html_element = f"""<div class="subject_name"><div class="subject_short_name">{fach_name}</div><div class="subject_long_name">{fach_lang_name}</div></div>"""
                                
                            elif index_element == 1:
                                raum_name = fach_informationen["name"]
                                raum_lang_name = fach_informationen["longName"]
                                if raum_name == raum_lang_name:
                                    raum_html_element = f"""<div class="room_name">{raum_name}</div>"""
                                elif raum_name != raum_lang_name:
                                    raum_html_element = f"""<div class="room_name">{raum_name} ({raum_lang_name})</div>"""
                id_for_checkbox = fach["id"]
                timetable_html_element += f"""<input type="checkbox" name="{id_for_checkbox}" value="{id_for_checkbox}" id="checkbox_number_{id_for_checkbox}"><label for="checkbox_number_{id_for_checkbox}" class="subject"><div class="info">{fach_html_element}{raum_html_element}</div></label>"""            
            timetable_html_element += "</div>"
        
    timetable_html_element += "</div>"
    timetable_html_element += f"""<input type="submit" value="Submit">"""
    timetable_html_element += "</form>"
            
            

        
    
    
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
<div class="container">{timetable_html_element}</div>
</body>
</html>"""
    return html

if __name__ == "__main__":
    app.run(debug=True)