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

def generate_foreColor(hex_color: str):
    hex_color = hex_color.replace("#", "")
    print(hex_color, file=sys.stderr)

    r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

    r = r*0.299
    g = g*0.587
    b = b*0.114
    Y = r + g + b

    if Y > 186:
        return "#1d1f2b"
    else:
        return "#ffffff"
    



@app.route("/")
def index():
    # with open("src/timetable.json", "r") as f:
    #     timetable_input = json.load(f)
    
    # if timetable_input:
    #     return str(timetable_input)
    # else:
    #     return str(timetable_input)
    return flask.redirect("/selecting_subjects")
    

@app.route("/selecting_subjects", methods=["GET", "POST"])
def selecting_subjects():
    
    with open("python_tests/src/webuntis_data/data_formatted_187.json", "r") as f:
        KaiFU_data = json.load(f)
    with open("python_tests/src/webuntis_data/subjects_187.json", "r") as f:
        KaiFU_subjects = json.load(f)
        
        
    with open("python_tests/src/webuntis_data/data_formatted_475.json", "r") as f:
        hlg_data = json.load(f)
    with open("python_tests/src/webuntis_data/subjects_475.json", "r") as f:
        hlg_subjects = json.load(f)

    
    

    
    if len(KaiFU_data[0]) >= len(hlg_data[0]):
        list_of_periods = periods_in_a_week(KaiFU_data)
    elif len(KaiFU_data[0]) < len(hlg_data[0]):
        list_of_periods = periods_in_a_week(hlg_data)
        
    timetable_html_element = ""
    
    
    timetable_html_element += f"""<form action="/personalized_timetable" class="timetable_wrapper_form" method="POST">"""
    timetable_html_element += f"""<div class="timetable_wrapper">"""
    

    weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
    timetable_html_element += f"""<div class="weekday"></div>"""
    for index_tag, tag in enumerate(KaiFU_data):
        timetable_html_element += f"""<div class="weekday">{weekdays[index_tag]}</div>"""
        
        
    for index_stunde in range(len(list_of_periods)-1):
        timetable_html_element += f"""<div class="period"><div class="period_time">{list_of_periods[index_stunde][0]}-{list_of_periods[index_stunde][1]}</div></div>"""
        for index_tag in range(5):
            timetable_html_element += f"""<div class="period"><div class="period_time">{index_stunde}</div>"""
            try:
                for index_fach, fach in enumerate(KaiFU_data[index_tag][index_stunde]):
                    for index_element, element in enumerate(fach["elements"]):
                        for index_fach_informationen, fach_informationen in enumerate(KaiFU_subjects):
                            if fach_informationen["id"] == element["id"]:
                                
                                if element["type"] == 3:
                                    fach_name = fach_informationen["name"]
                                    fach_lang_name = fach_informationen["longName"]
                                    
                                    fach_html_element = f"""<div class="subject_name"><div class="subject_short_name">{fach_name}</div><div class="subject_long_name">{fach_lang_name}</div></div>"""
                                    
                                elif element["type"] == 4:
                                    raum_name = fach_informationen["name"]
                                    raum_lang_name = fach_informationen["longName"]
                                    if raum_name == raum_lang_name:
                                        raum_html_element = f"""<div class="room_name">{raum_name}</div>"""
                                    elif raum_name != raum_lang_name:
                                        raum_html_element = f"""<div class="room_name">{raum_name} ({raum_lang_name})</div>"""
                    id_for_checkbox = fach["id"]
                    timetable_html_element += f"""<input type="checkbox" name="{id_for_checkbox}" value="{id_for_checkbox}" id="checkbox_number_{id_for_checkbox}"><label for="checkbox_number_{id_for_checkbox}" class="subject"><div class="info">{fach_html_element}{raum_html_element}</div></label>"""            
            except IndexError:
                pass
            try:
                for index_fach, fach in enumerate(hlg_data[index_tag][index_stunde]):
                    for index_element, element in enumerate(fach["elements"]):
                        for index_fach_informationen, fach_informationen in enumerate(hlg_subjects):
                            if fach_informationen["id"] == element["id"]:
                                
                                if element["type"] == 3:
                                    fach_name = fach_informationen["name"]
                                    fach_lang_name = fach_informationen["longName"]
                                    
                                    fach_html_element = f"""<div class="subject_name"><div class="subject_short_name">{fach_name}</div><div class="subject_long_name">{fach_lang_name}</div></div>"""
                                    
                                elif element["type"] == 4:
                                    raum_name = fach_informationen["name"]
                                    raum_lang_name = fach_informationen["longName"]
                                    if raum_name == raum_lang_name:
                                        raum_html_element = f"""<div class="room_name">{raum_name}</div>"""
                                    elif raum_name != raum_lang_name:
                                        raum_html_element = f"""<div class="room_name">{raum_name} ({raum_lang_name})</div>"""
                    id_for_checkbox = fach["id"]
                    timetable_html_element += f"""<input type="checkbox" name="{id_for_checkbox}" value="{id_for_checkbox}" id="checkbox_number_{id_for_checkbox}"><label for="checkbox_number_{id_for_checkbox}" class="subject"><div class="info">{fach_html_element}{raum_html_element}</div></label>"""            
            except IndexError:
                pass
            timetable_html_element += "</div>"
        
    timetable_html_element += "</div>"
    timetable_html_element += """<input type="submit" value="Submit">"""
    timetable_html_element += "</form>"
            
            
    html = f"""    
    <!DOCTYPE html>
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


@app.route("/personalized_timetable", methods=["GET", "POST"])
def selected_subjects():
    with open("python_tests/src/webuntis_data/data_formatted_187.json", "r") as f:
        KaiFU_data = json.load(f)
    with open("python_tests/src/webuntis_data/subjects_187.json", "r") as f:
        KaiFU_subjects = json.load(f)
        
    
    
    
    list_of_KaiFU_subjects_id = []
    
    for i, j in enumerate(KaiFU_data):
        for k, l in enumerate(j):
            for m, n in enumerate(l):
                if n["id"] not in list_of_KaiFU_subjects_id:
                    list_of_KaiFU_subjects_id.append(n["id"])
    
    
    selected_KaiFU_subjects_lesson_id = []
    blocked_ids = []
    if flask.request.method == "POST":
        for i, j in enumerate(list_of_KaiFU_subjects_id):
            if flask.request.form.get(str(j)):
                for k, l in enumerate(KaiFU_data):
                    for m, n in enumerate(l):
                        for o, p in enumerate(n):
                            if p["id"] == j:
                                selected_KaiFU_subjects_lesson_id.append(p["lessonId"])
        for i, j in enumerate(KaiFU_data):
            for k, l in enumerate(j):
                for m, n in enumerate(l):
                    if n["lessonId"] not in selected_KaiFU_subjects_lesson_id:
                        blocked_ids.append(n["lessonId"])
            
    
    
    
    
    
    list_of_periods = periods_in_a_week(KaiFU_data)
    
    timetable_html_element = ""
    
    
    timetable_html_element += f"""<div class="timetable_wrapper">"""
    

    weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
    timetable_html_element += f"""<div class="weekday"></div>"""
    for index_tag, tag in enumerate(KaiFU_data):
        timetable_html_element += f"""<div class="weekday">{weekdays[index_tag]}</div>"""
        
        
    for index_stunde in range(len(KaiFU_data[0])):
        timetable_html_element += f"""<div class="period"><div class="period_time">{list_of_periods[index_stunde][0]}-{list_of_periods[index_stunde][1]}</div></div>"""
        for index_tag, tag in enumerate(KaiFU_data):
            timetable_html_element += f"""<div class="period"><div class="period_time"></div>"""
            for index_fach, fach in enumerate(tag[index_stunde]):
                if fach["lessonId"] not in blocked_ids:
                    for index_element, element in enumerate(fach["elements"]):
                        for index_fach_informationen, fach_informationen in enumerate(KaiFU_subjects):
                            if fach_informationen["id"] == element["id"]:
                                
                                
                                
                                if element["type"] == 3:
                                    try: 
                                        backColor = fach_informationen["backColor"]
                                        foreColor = generate_foreColor(backColor)
                                    except KeyError: 
                                        backColor = "#1d1f2b"
                                        foreColor = "#F3DFC1"
                                        
                                    fach_name = fach_informationen["name"]
                                    fach_lang_name = fach_informationen["longName"]
                                    
                                    fach_html_element = f"""<div class="subject_name"><div class="subject_short_name">{fach_name}</div><div class="subject_long_name">{fach_lang_name}</div></div>"""
                                    
                                elif element["type"] == 4:
                                    raum_name = fach_informationen["name"]
                                    raum_lang_name = fach_informationen["longName"]
                                    if raum_name == raum_lang_name:
                                        raum_html_element = f"""<div class="room_name">{raum_name}</div>"""
                                    elif raum_name != raum_lang_name:
                                        raum_html_element = f"""<div class="room_name">{raum_name} ({raum_lang_name})</div>"""
                    id_for_checkbox = fach["id"]
                    timetable_html_element += f"""<label class="subject" style="background-color: {backColor}; color: {foreColor}"><div class="info">{fach_html_element}{raum_html_element}</div></label>"""            
            timetable_html_element += "</div>"
        
    timetable_html_element += "</div>"
    
    
    timetable_html_element += f"""<div class="wrapper">"""
    for i, j in enumerate(KaiFU_subjects):
        try:
            if j["type"] == 3:
                try:
                    back = j["backColor"]
                except KeyError:
                    back = "#1d1f2b"
                try:
                    fore = generate_foreColor(back)
                except KeyError:
                    fore = "#F3DFC1"
                timetable_html_element += f"""<div style="background-color: {back}; padding: 30px;"><p style="color: {fore};">{j["longName"]}</p></div>"""
        except KeyError:
            print(j)
    timetable_html_element += f"""</div>"""
        
            
            
    html = f"""    
    <!DOCTYPE html>
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