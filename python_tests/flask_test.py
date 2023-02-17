import flask
import json
import sys
import Webuntis_request

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

    r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

    r = r*0.299
    g = g*0.587
    b = b*0.114
    Y = r + g + b

    if Y > 150:
        return "#00000f"
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

    
    

    try:
        if len(KaiFU_data[0]) >= len(hlg_data[0]):
            list_of_periods = periods_in_a_week(KaiFU_data)
        elif len(KaiFU_data[0]) < len(hlg_data[0]):
            list_of_periods = periods_in_a_week(hlg_data)
    except IndexError:
        try: 
            list_of_periods = periods_in_a_week(KaiFU_data)
        except:
            try:
                list_of_periods = periods_in_a_week(hlg_data)
            except:
                pass
        
    timetable_html_element = ""
    
    
    timetable_html_element += f"""<form action="/save_timetable" class="timetable_wrapper_form" method="POST">"""
    timetable_html_element += f"""<div class="timetable_wrapper">"""
    

    weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
    timetable_html_element += f"""<div class="weekday"></div>"""
    for index_tag, tag in enumerate(KaiFU_data):
        timetable_html_element += f"""<div class="weekday">{weekdays[index_tag]}</div>"""
        
        
    for index_stunde in range(len(list_of_periods)-1):
        stunde_first = str(list_of_periods[index_stunde][0])
        stunde_second = str(list_of_periods[index_stunde][1])
        if len(stunde_first) == 3:
            stunde_first = "0" + stunde_first
        stunde_first = stunde_first[0:2] + ":" + stunde_first[2:4]
        if len(stunde_second) == 3:
            stunde_second = "0" + stunde_second
        stunde_second = stunde_second[0:2] + ":" + stunde_second[2:4]
        
        timetable_html_element += f"""<div class="period"><div class="period_time"><div class="period_start_time">{stunde_first}</div><div class="period_end_time">{stunde_second}</div> </div></div>"""
        for index_tag in range(5):
            timetable_html_element += f"""<div class="period"><div class="period_time"></div>"""
            try:
                for index_fach, fach in enumerate(KaiFU_data[index_tag][index_stunde]):
                    for index_element, element in enumerate(fach["elements"]):
                        for index_fach_informationen, fach_informationen in enumerate(KaiFU_subjects):
                            if fach_informationen["id"] == element["id"]:
                                
                                if element["type"] == 3:
                                    fach_name = fach_informationen["name"]
                                    fach_lang_name = ""#fach_informationen["longName"]
                                    
                                    fach_html_element = f"""<div class="subject_name"><div class="subject_short_name">{fach_name}</div><div class="subject_long_name">{fach_lang_name}</div></div>"""
                                    
                                elif element["type"] == 4:
                                    raum_name = fach_informationen["name"]
                                    raum_lang_name = fach_informationen["longName"]
                                    if raum_name == raum_lang_name:
                                        raum_html_element = f"""<div class="room_name">{raum_name}</div>"""
                                    elif raum_name != raum_lang_name:
                                        raum_html_element = f"""<div class="room_name">{raum_name} ({raum_lang_name})</div>"""
                    id_for_checkbox = fach["id"]
                    try:
                        timetable_html_element += f"""<input type="checkbox" name="{id_for_checkbox}" value="{id_for_checkbox}" id="checkbox_number_{id_for_checkbox}"><label for="checkbox_number_{id_for_checkbox}" class="subject"><div class="info">{fach_html_element}{raum_html_element}</div></label>"""            
                    except UnboundLocalError:
                        pass
            except IndexError:
                pass
            try:
                for index_fach, fach in enumerate(hlg_data[index_tag][index_stunde]):
                    for index_element, element in enumerate(fach["elements"]):
                        for index_fach_informationen, fach_informationen in enumerate(hlg_subjects):
                            if fach_informationen["id"] == element["id"]:
                                
                                if element["type"] == 3:
                                    fach_name = fach_informationen["name"]
                                    fach_lang_name = ""#fach_informationen["longName"]
                                    
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
        
        
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@500&display=swap" rel="stylesheet">
        
        
        <title>WebUntis 2.0</title>
    </head>
    <body>
        <div class="container">{timetable_html_element}</div>
    </body>
    </html>"""
    return html

@app.route("/save_timetable", methods=["GET", "POST"])
def save_timetable():
    with open("python_tests/src/webuntis_data/data_formatted_187.json", "r") as f:
        KaiFU_data = json.load(f)
    with open("python_tests/src/webuntis_data/subjects_187.json", "r") as f:
        KaiFU_subjects = json.load(f)
        
    with open("python_tests/src/webuntis_data/data_formatted_475.json", "r") as f:
        hlg_data = json.load(f)
    with open("python_tests/src/webuntis_data/subjects_475.json", "r") as f:
        hlg_subjects = json.load(f)
    
        
    
    
    
    list_of_KaiFU_subjects_id = []
    
    for i, j in enumerate(KaiFU_data):
        for k, l in enumerate(j):
            for m, n in enumerate(l):
                if n["id"] not in list_of_KaiFU_subjects_id:
                    list_of_KaiFU_subjects_id.append(n["id"])
    
    list_of_hlg_subjects_id = []
    
    for i, j in enumerate(hlg_data):
        for k, l in enumerate(j):
            for m, n in enumerate(l):
                if n["id"] not in list_of_hlg_subjects_id:
                    list_of_hlg_subjects_id.append(n["id"])
    
    
    selected_KaiFU_subjects_lesson_id = []
    selected_hlg_subjects_lesson_id = []
    blocked_KaiFU_ids = []
    blocked_hlg_ids = []
    if flask.request.method == "POST":
        for i, j in enumerate(list_of_KaiFU_subjects_id):
            if flask.request.form.get(str(j)):
                for k, l in enumerate(KaiFU_data):
                    for m, n in enumerate(l):
                        for o, p in enumerate(n):
                            if p["id"] == j:
                                print(p["lessonId"], file=sys.stderr)
                                selected_KaiFU_subjects_lesson_id.append(p["lessonId"])
        for i, j in enumerate(KaiFU_data):
            for k, l in enumerate(j):
                for m, n in enumerate(l):
                    if n["lessonId"] not in selected_KaiFU_subjects_lesson_id:
                        blocked_KaiFU_ids.append(n["lessonId"])
                        
        
        for i, j in enumerate(list_of_hlg_subjects_id):
            if flask.request.form.get(str(j)):
                for k, l in enumerate(hlg_data):
                    for m, n in enumerate(l):
                        for o, p in enumerate(n):
                            if p["id"] == j:
                                selected_hlg_subjects_lesson_id.append(p["lessonId"])
        for i, j in enumerate(hlg_data):
            for k, l in enumerate(j):
                for m, n in enumerate(l):
                    if n["lessonId"] not in selected_hlg_subjects_lesson_id:
                        blocked_hlg_ids.append(n["lessonId"])
    try:
        with open("python_tests/src/webuntis_data/blocked_ids.json", "w") as f:
        
            blocked_ids = {
                "blocked_KaiFU_ids": blocked_KaiFU_ids,
                "blocked_hlg_ids": blocked_hlg_ids
            }
            f.write(json.dumps(blocked_ids))
    except:
        pass
    
    return flask.redirect("/personalized_timetable")
    


@app.route("/personalized_timetable", methods=["GET", "POST"])
def selected_subjects():
    start_date = "2023-02-13"
    try:
        Webuntis_request.WebUntis_request(1, 475, start_date, "hh5864").API_call()
    except:
        pass
    try:
        Webuntis_request.WebUntis_request(1, 187, start_date, "hh5846").API_call()
    except:
        pass
    with open("python_tests/src/webuntis_data/data_formatted_187.json", "r") as f:
        KaiFU_data = json.load(f)
    with open("python_tests/src/webuntis_data/subjects_187.json", "r") as f:
        KaiFU_subjects = json.load(f)
        
    with open("python_tests/src/webuntis_data/data_formatted_475.json", "r") as f:
        hlg_data = json.load(f)
    with open("python_tests/src/webuntis_data/subjects_475.json", "r") as f:
        hlg_subjects = json.load(f)
        
    
    
    
    # list_of_KaiFU_subjects_id = []
    
    # for i, j in enumerate(KaiFU_data):
    #     for k, l in enumerate(j):
    #         for m, n in enumerate(l):
    #             if n["id"] not in list_of_KaiFU_subjects_id:
    #                 list_of_KaiFU_subjects_id.append(n["id"])
    
    # list_of_hlg_subjects_id = []
    
    # for i, j in enumerate(hlg_data):
    #     for k, l in enumerate(j):
    #         for m, n in enumerate(l):
    #             if n["id"] not in list_of_hlg_subjects_id:
    #                 list_of_hlg_subjects_id.append(n["id"])
    
    
    # selected_KaiFU_subjects_lesson_id = []
    # selected_hlg_subjects_lesson_id = []
    # blocked_KaiFU_ids = []
    # blocked_hlg_ids = []
    # if flask.request.method == "POST":
    #     print(flask.request.form, file=sys.stderr)
    #     for i, j in enumerate(list_of_KaiFU_subjects_id):
    #         if flask.request.form.get(str(j)):
    #             for k, l in enumerate(KaiFU_data):
    #                 for m, n in enumerate(l):
    #                     for o, p in enumerate(n):
    #                         if p["id"] == j:
    #                             print(p["lessonId"], file=sys.stderr)
    #                             selected_KaiFU_subjects_lesson_id.append(p["lessonId"])
    #     for i, j in enumerate(KaiFU_data):
    #         for k, l in enumerate(j):
    #             for m, n in enumerate(l):
    #                 if n["lessonId"] not in selected_KaiFU_subjects_lesson_id:
    #                     blocked_KaiFU_ids.append(n["lessonId"])
                        
        
    #     for i, j in enumerate(list_of_hlg_subjects_id):
    #         if flask.request.form.get(str(j)):
    #             for k, l in enumerate(hlg_data):
    #                 for m, n in enumerate(l):
    #                     for o, p in enumerate(n):
    #                         if p["id"] == j:
    #                             selected_hlg_subjects_lesson_id.append(p["lessonId"])
    #     for i, j in enumerate(hlg_data):
    #         for k, l in enumerate(j):
    #             for m, n in enumerate(l):
    #                 if n["lessonId"] not in selected_hlg_subjects_lesson_id:
    #                     blocked_hlg_ids.append(n["lessonId"])
    
    with open("python_tests/src/webuntis_data/blocked_ids.json", "r") as f:
        blocked_ids_file = json.load(f)
    
    blocked_KaiFU_ids = blocked_ids_file["blocked_KaiFU_ids"]
    blocked_hlg_ids = blocked_ids_file["blocked_hlg_ids"]
    
        
            
    
    
    date_switcher_html_element = ""
    
    date_switcher_html_element += f"""<div class="date_switcher"><form action="/personalized_timetable" method="POST"><input type="submit" value="<"><input type="submit" value=">"></form></div>"""
    
    
    
    
    if len(KaiFU_data[0]) >= len(hlg_data[0]):
        print("KaiFU has more periods", file=sys.stderr)
        list_of_periods = periods_in_a_week(KaiFU_data)
    elif len(KaiFU_data[0]) < len(hlg_data[0]):
        print("hlg has more periods", file=sys.stderr)
        list_of_periods = periods_in_a_week(hlg_data)
    
    
    timetable_html_element = ""
    
    
    timetable_html_element += f"""<div class="timetable_wrapper">"""
    

    weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
    timetable_html_element += f"""<div class="weekday"></div>"""
    for index_tag, tag in enumerate(KaiFU_data):
        timetable_html_element += f"""<div class="weekday">{weekdays[index_tag]}</div>"""
        
        # untis_date = str(j["date"])
        #     untis_start_time = str(j["startTime"])
        #     if len(untis_start_time) == 3:
        #         untis_start_time = "0" + untis_start_time
    try:
        for index_stunde in range(len(list_of_periods)-1):
            stunde_first = str(list_of_periods[index_stunde][0])
            stunde_second = str(list_of_periods[index_stunde][1])
            if len(stunde_first) == 3:
                stunde_first = "0" + stunde_first
            stunde_first = stunde_first[0:2] + ":" + stunde_first[2:4]
            if len(stunde_second) == 3:
                stunde_second = "0" + stunde_second
            stunde_second = stunde_second[0:2] + ":" + stunde_second[2:4]
            timetable_html_element += f"""<div class="period"><div class="period_time_value"><div class="period_start_time">{stunde_first}</div><div class="period_end_time">{stunde_second}</div></div></div>"""
            for index_tag in range(5):
                timetable_html_element += f"""<div class="period"><div class="period_time"></div>"""
                try:
                    for index_fach, fach in enumerate(KaiFU_data[index_tag][index_stunde]):
                        if fach["lessonId"] not in blocked_KaiFU_ids:
                            
                                
                            for index_element, element in enumerate(fach["elements"]):
                                for index_fach_informationen, fach_informationen in enumerate(KaiFU_subjects):
                                    if fach_informationen["id"] == element["id"]:
                                                                            
                                        if element["type"] == 3:
                                            try: 
                                                backColor = fach_informationen["backColor"]
                                                foreColor = generate_foreColor(backColor)
                                            except KeyError: 
                                                backColor = "#F49F25"
                                                foreColor = "#000000"
                                                
                                            fach_name = fach_informationen["name"]
                                            fach_lang_name = ""#fach_informationen["longName"]
                                            
                                            fach_html_element = f"""<div class="subject_name"><div class="subject_short_name">{fach_name}</div><div class="subject_long_name">{fach_lang_name}</div></div>"""
                                            
                                        elif element["type"] == 4:
                                            raum_name = fach_informationen["name"]
                                            raum_lang_name = fach_informationen["longName"]
                                            if raum_name == raum_lang_name:
                                                raum_html_element = f"""<div class="room_name">{raum_name}</div>"""
                                            elif raum_name != raum_lang_name:
                                                raum_html_element = f"""<div class="room_name">{raum_name}<div class="room_lang_name">({raum_lang_name})</div></div>"""
                            if fach["hasPeriodText"] == True or fach["cellState"] == "CANCEL":
                                if fach["substText"] != "":
                                    ausfall_text = fach["substText"]
                                elif fach["periodText"] != "":
                                    ausfall_text = fach["periodText"]
                                else:
                                    ausfall_text = "Entfall"
                                ausfall_html_element = f"""<div class="ausfall">{ausfall_text}</div>"""
                                backColor = "#979797"
                                foreColor = "#00000F"
                                border = " border: #F00000 solid 3px;"
                            else:
                                ausfall_html_element = ""
                                border = ""
                            id_for_checkbox = fach["id"]
                            timetable_html_element += f"""<label class="subject" style="background-color: {backColor}; color: {foreColor};{border}"><div class="info">{fach_html_element}{ausfall_html_element}{raum_html_element}</div></label>"""            
                            ausfall_html_element = ""
                except IndexError:
                    pass
                try:
                    for index_fach, fach in enumerate(hlg_data[index_tag][index_stunde]):
                        if fach["lessonId"] not in blocked_hlg_ids:
                            for index_element, element in enumerate(fach["elements"]):
                                for index_fach_informationen, fach_informationen in enumerate(hlg_subjects):
                                    if fach_informationen["id"] == element["id"]:
                                        
                                        
                                        
                                        if element["type"] == 3:
                                            try: 
                                                backColor = fach_informationen["backColor"]
                                                foreColor = generate_foreColor(backColor)
                                            except KeyError: 
                                                backColor = "#F49F25"
                                                foreColor = "#000000"
                                                
                                            fach_name = fach_informationen["name"]
                                            fach_lang_name = ""#fach_informationen["longName"]
                                            
                                            fach_html_element = f"""<div class="subject_name"><div class="subject_short_name">{fach_name}</div><div class="subject_long_name">{fach_lang_name}</div></div>"""
                                            
                                        elif element["type"] == 4:
                                            raum_name = fach_informationen["name"]
                                            raum_lang_name = fach_informationen["longName"]
                                            if raum_name == raum_lang_name:
                                                raum_html_element = f"""<div class="room_name">{raum_name}</div>"""
                                            elif raum_name != raum_lang_name:
                                                raum_html_element = f"""<div class="room_name">{raum_name}<div class="room_lang_name">({raum_lang_name})</div></div>"""
                            id_for_checkbox = fach["id"]
                            timetable_html_element += f"""<label class="subject" style="background-color: {backColor}; color: {foreColor}"><div class="info">{fach_html_element}{raum_html_element}</div></label>"""            
                except IndexError:
                    pass
                    
                timetable_html_element += "</div>"
    except:
        pass
    timetable_html_element += "</div>"
    
    
    # timetable_html_element += f"""<div class="wrapper">"""
    # for i, j in enumerate(KaiFU_subjects):
    #     try:
    #         if j["type"] == 3:
    #             try:
    #                 back = j["backColor"]
    #             except KeyError:
    #                 back = "#ff0000"
    #             try:
    #                 fore = generate_foreColor(back)
    #             except KeyError:
    #                 fore = "#F3DFC1"
    #             timetable_html_element += f"""<div style="background-color: {back}; padding: 30px;"><p style="color: {fore};">{j["longName"]}</p></div>"""
    #     except KeyError:
    #         print(j)
    
    # for i, j in enumerate(hlg_subjects):
    #     try:
    #         if j["type"] == 3:
    #             try:
    #                 back = j["backColor"]
    #             except KeyError:
    #                 back = "#ff0000"
    #             try:
    #                 fore = generate_foreColor(back)
    #             except KeyError:
    #                 fore = "#F3DFC1"
    #             timetable_html_element += f"""<div style="background-color: {back}; padding: 30px;"><p style="color: {fore};">{j["longName"]}</p></div>"""
    #     except KeyError:
    #         print(j)
    # timetable_html_element += f"""</div>""" 
    
        
            
            
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
        {date_switcher_html_element}
        <div class="container">{timetable_html_element}</div>
    </body>
    </html>"""
    return html
    


if __name__ == "__main__":
    app.run(debug=True)