import flask
import json
import sys
import Webuntis_request
import datetime

app = flask.Flask(__name__)

date_counter = 0

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
    
    
def timetable_periods_selector_generator(data, index_tag, index_stunde, subjects):
    timetable_html_element = ""
    try:
        for index_fach, fach in enumerate(data[index_tag][index_stunde]):
            for index_element, element in enumerate(fach["elements"]):
                for index_fach_informationen, fach_informationen in enumerate(subjects):
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
    
    
    return str(timetable_html_element)
    



@app.route("/")
def index():
    try:
        with open("app/src/webuntis_data/blocked_ids.json", "r") as f:
            blocked_ids_file = json.load(f)
    except:
        blocked_ids_file = []

    navbar_html_element = """<a class="homepage-navbar-link active" href="/"><img class="homepage-navbar-image" src="/static/logo.png"></a>"""
    for i in range(len(blocked_ids_file)):
        navbar_html_element += f"""<a class="links-navbar" href="/personalisierter_Stundenplan/{blocked_ids_file[i]["name"]}" title="{blocked_ids_file[i]["name"]}"><p>{blocked_ids_file[i]["name"][0]}</p></a>"""
    navbar_html_element += """<a class="links-navbar" href="/Faecherauswahl"><p><img class="plus-sign" src="/static/plus-sign.png"></p></a>"""
    
    homepage_html_element = """<div class="homepage_container">
    <h1 class="homepage_h1">Willkommen bei WebUntis 2.0</h1>
    <h2 class="homepage_h2">Was ist WebUntis 2.0?</h2>
    <p class="homepage_p">WebUntis 2.0 ist eine aufpolierte Webanwendung für das Stundenplan-Programm Untis. Das Programm ist auf Schüler und Schülerinnen des KaiFUs und HLGs aus der Oberstufe* und deren Eltern ausgerichtet. Die Hauptvorteile gegenüber UntisBeta liegen darin, dass die Fächer mit HLG und KaiFU Lehrern und Lehrerinnen auf einem Plan sind. Zudem ist es möglich nur die Fächer, die einen interessieren, auszuwählen und es überzeugt mit einem extrem anwenderfreundlichen Design. Entwickelt und vermarktet wurde das Programm von den Entrepreneurs Simon Latschinger und Paul Stramm, mehr von uns unter <a class="github-link" href="https://github.com/simonlsr/Untis-2.0">GitHub</a>.<br><a class="kleingedrucktes">*nicht für Schüler der Klassenstufe 11</a></p>
    <h2 class="homepage_h2">Wie funktioniert WebUntis 2.0?</h2>
    <p class="homepage_p">Um sich ein Stundenplan-Profil anzulegen, muss man oben links auf das Plus drücken. Dann kann man oben den gewünschten Namen für den Stundenplan eingeben und danach alle Kurse, die man angezeigt haben möchte, auswählen. Dabei reicht es, wenn man jeden Kurs nur ein mal anklickt. Sobald man alle Kurse ausgewählt hat, klickt man auf erstellen. Wenn man auf der linken Seite wieder auf das Plus drückt, kann man auf die gleiche Art ein neues Profil erstellen. Mit einem Klick auf das Untis 2.0 Logo kommen sie wieder auf die Startseite. Wenn man die erstellten Profile auf der linken Seite aufruft, sieht man den jeweiligen Stundenplan und in welchen Fächern Entfall etc. ist. Über die Pfeile über dem Stundenplan kann man in die nächste und vorherige Woche wechseln und zwischen den Pfeilen sieht man das Datum und des jeweils ersten Tages in der Woche.</p>
    
    </div>"""
    
    html = f"""    
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="{flask.url_for('static', filename='css/main.css')}">
        
        <link rel="shortcut icon" href="{flask.url_for('static', filename='logo.png')}">
        
        
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@500&display=swap" rel="stylesheet">
        
        
        <title>WebUntis 2.0</title>
    </head>
    <body>
        <nav class="navbar">{navbar_html_element}</nav>
        <div class="main_container_homepage"><div class="sub_container_homepage">
        {homepage_html_element}
        </div>
        </div>
    </body>
    </html>"""
    
    
    return html
    

@app.route("/Faecherauswahl", methods=["GET", "POST"])
def Faecherauswahl():
    start_date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    
    
    # try:
    #     Webuntis_request.WebUntis_request(1, 475, start_date, "hh5864").API_call()
    # except:
    #     pass
    # try:
    #     Webuntis_request.WebUntis_request(1, 187, start_date, "hh5846").API_call()
    # except:
    #     pass
    
    
    
    with open("app/src/webuntis_data/data_formatted_187.json", "r") as f:
        KaiFU_data = json.load(f)
    with open("app/src/webuntis_data/subjects_187.json", "r") as f:
        KaiFU_subjects = json.load(f)
        
        
    with open("app/src/webuntis_data/data_formatted_475.json", "r") as f:
        hlg_data = json.load(f)
    with open("app/src/webuntis_data/subjects_475.json", "r") as f:
        hlg_subjects = json.load(f)
        
    try:
        with open("app/src/webuntis_data/blocked_ids.json", "r") as f:
            blocked_ids_file = json.load(f)
    except:
        blocked_ids_file = []

    navbar_html_element = """<a class="homepage-navbar-link" href="/"><img class="homepage-navbar-image" src="/static/logo.png"></a>"""
    for i in range(len(blocked_ids_file)):
        navbar_html_element += f"""<a class="links-navbar" href="/personalisierter_Stundenplan/{blocked_ids_file[i]["name"]}" title="{blocked_ids_file[i]["name"]}"><p>{blocked_ids_file[i]["name"][0]}</p></a>"""
    navbar_html_element += """<a class="links-navbar active" href="/Faecherauswahl"><p><img class="plus-sign" src="/static/plus-sign.png"></p></a>"""
    

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
    
    timetable_html_element += f"""<input id="input-profile-name-id" name="input-profile-name-name" class="input-profile-name" type="text" placeholder="Profilname eingeben…" />"""
    
    
    timetable_html_element += f"""<div class="weekdays_wrapper">"""

    weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
    timetable_html_element += f"""<div class="weekday">12</div>"""
    for index_tag, tag in enumerate(KaiFU_data):
        timetable_html_element += f"""<div class="weekday">{weekdays[index_tag]}</div>"""
        
    timetable_html_element += f"""</div>"""
        
    timetable_html_element += f"""<div class="timetable_wrapper">"""
        
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
            timetable_html_element += """<div class="period"><div class="period_time"></div>"""
            timetable_html_element += str(timetable_periods_selector_generator(data=KaiFU_data, subjects=KaiFU_subjects, index_tag=index_tag, index_stunde=index_stunde))
            timetable_html_element += str(timetable_periods_selector_generator(data=hlg_data, subjects=hlg_subjects, index_tag=index_tag, index_stunde=index_stunde))
            timetable_html_element += "</div>"
        
    timetable_html_element += "</div>"
    timetable_html_element += """<input class="submit_timetable"type="submit" value="Erstellen">"""
    timetable_html_element += "</form>"
            
            
    html = f"""    
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="{flask.url_for('static', filename='css/main.css')}">
        
        <link rel="shortcut icon" href="{flask.url_for('static', filename='logo.png')}">
        
        
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@500&display=swap" rel="stylesheet">
        
        
        <title>WebUntis 2.0</title>
    </head>
    <body>
        <nav class="navbar">{navbar_html_element}</nav>
        <div class="main_container">
        <div class="sub_container">{timetable_html_element}</div>
        </div>
    </body>
    </html>"""
    return html

@app.route("/save_timetable", methods=["GET", "POST"])
def save_timetable():
    with open("app/src/webuntis_data/data_formatted_187.json", "r") as f:
        KaiFU_data = json.load(f)
    with open("app/src/webuntis_data/subjects_187.json", "r") as f:
        KaiFU_subjects = json.load(f)
        
    with open("app/src/webuntis_data/data_formatted_475.json", "r") as f:
        hlg_data = json.load(f)
    with open("app/src/webuntis_data/subjects_475.json", "r") as f:
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
        profile_name = flask.request.form.getlist("input-profile-name-name")[0]
        
    try:
        with open("app/src/webuntis_data/blocked_ids.json", "r") as f:
            blocked_ids = json.load(f)
        with open("app/src/webuntis_data/blocked_ids.json", "w") as f:
            index = len(blocked_ids)
            if profile_name == "":
                profile_name = "Mein Stundenplan " + str(index + 1)
            blocked_ids.append({
                "blocked_KaiFU_ids": blocked_KaiFU_ids,
                "blocked_hlg_ids": blocked_hlg_ids,
                "name": profile_name
            })
            
            f.write(json.dumps(blocked_ids))
    except:
        index = 0
    
    return flask.redirect("/personalisierter_Stundenplan/"+str(profile_name))
    


@app.route("/personalisierter_Stundenplan/<profile_name>", methods=["GET", "POST"])
def selected_subjects(profile_name):
    start_date = str(datetime.date.today() - datetime.timedelta(days=int(datetime.date.weekday(datetime.date.today())))+ datetime.timedelta(days=date_counter))
    formatted_date = start_date[8:10] + "." + start_date[5:7] + "." + start_date[0:4]
    try:
        Webuntis_request.WebUntis_request(1, 475, start_date, "hh5864").API_call()
    except:
        pass
    try:
        Webuntis_request.WebUntis_request(1, 187, start_date, "hh5846").API_call()
    except:
        pass
    with open("app/src/webuntis_data/data_formatted_187.json", "r") as f:
        KaiFU_data = json.load(f)
    with open("app/src/webuntis_data/subjects_187.json", "r") as f:
        KaiFU_subjects = json.load(f)
        
    with open("app/src/webuntis_data/data_formatted_475.json", "r") as f:
        hlg_data = json.load(f)
    with open("app/src/webuntis_data/subjects_475.json", "r") as f:
        hlg_subjects = json.load(f)
        

    with open("app/src/webuntis_data/blocked_ids.json", "r") as f:
        blocked_ids_file = json.load(f)
        
    for i, j in enumerate(blocked_ids_file):
        if j["name"] == profile_name:
            profile_number = i
            break
    
    
    blocked_KaiFU_ids = blocked_ids_file[int(profile_number)]["blocked_KaiFU_ids"]
    blocked_hlg_ids = blocked_ids_file[int(profile_number)]["blocked_hlg_ids"]
    
    navbar_html_element = """<a class="homepage-navbar-link" href="/"><img class="homepage-navbar-image" src="/static/logo.png"></a>"""
    for i in range(len(blocked_ids_file)):
        if i == int(profile_number):
            navbar_html_element += f"""<a class="links-navbar active" href="/personalisierter_Stundenplan/{blocked_ids_file[i]["name"]}" title="{blocked_ids_file[i]["name"]}"><p>{blocked_ids_file[i]["name"][0]}</p></a>"""
        else:
            navbar_html_element += f"""<a class="links-navbar" href="/personalisierter_Stundenplan/{blocked_ids_file[i]["name"]}"title="{blocked_ids_file[i]["name"]}"><p>{blocked_ids_file[i]["name"][0]}</p></a>"""
    navbar_html_element += """<a class="links-navbar" href="/Faecherauswahl"><p><img class="plus-sign" src="/static/plus-sign.png"></p></a>"""
        
            
    
    
    date_switcher_html_element = ""
    
    date_switcher_html_element += f"""<div class="date_switcher"><form class="date_switcher_button_parent" action="/date_counter_subtract/{profile_number}" method="POST"><button class="date_switcher_button" id="date_subtract" type="submit"><i class="fa fa-arrow-left"></i></button></form><label class="current_date">{formatted_date}</label><form class="date_switcher_button_parent" action="/date_counter_add/{profile_number}" method="POST"><button class="date_switcher_button" id="date_add" type="submit"><i class="fa fa-arrow-right"></i></button></form></div>"""
    
    
    
    try:
        if len(KaiFU_data[0]) >= len(hlg_data[0]):
            list_of_periods = periods_in_a_week(KaiFU_data)
        elif len(KaiFU_data[0]) < len(hlg_data[0]):
            list_of_periods = periods_in_a_week(hlg_data)
    except TypeError:
        try:
            list_of_periods = periods_in_a_week(KaiFU_data)
        except TypeError:
            try:
                list_of_periods = periods_in_a_week(hlg_data)
            except TypeError:
                list_of_periods = []
    
    
    timetable_html_element = ""
    
    
    
    
    
    
    timetable_html_element += f"""<div class="weekdays_wrapper">"""
    
    weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
    
    timetable_html_element += f"""<div class="weekday">{"12"}</div>"""
    for index_tag, tag in enumerate(KaiFU_data):
        timetable_html_element += f"""<div class="weekday">{weekdays[index_tag]}</div>"""
        
    timetable_html_element += f"""</div>"""    
    timetable_html_element += f"""<div class="timetable_wrapper">"""
    
    try:
        for index_stunde in range(len(list_of_periods)):
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
    
        
            
            
    html = f"""    
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="{flask.url_for('static', filename='css/main.css')}">
        <link rel="shortcut icon" href="{flask.url_for('static', filename='logo.png')}">
        <title>WebUntis 2.0</title>
        
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@500&display=swap" rel="stylesheet">
        
        <script src="https://kit.fontawesome.com/fc9ee00639.js" crossorigin="anonymous"></script>
    </head>
    <body>
        <nav class="navbar">{navbar_html_element}</nav>
        <div class="main_container">
        <div class="sub_container">{date_switcher_html_element}{timetable_html_element}</div>
        </div>
    </body>
    </html>"""
    return html
    
    
@app.route("/date_counter_subtract/<number>", methods=["GET", "POST"])
def date_counter_subtract(number):
    global date_counter
    date_counter -= 7
    with open("app/src/webuntis_data/blocked_ids.json", "r") as file:
        blocked_ids = json.load(file)
    name = blocked_ids[int(number)]["name"]
    
    return flask.redirect("/personalisierter_Stundenplan/"+name)

@app.route("/date_counter_add/<number>", methods=["GET", "POST"])
def date_counter_add (number):
    global date_counter
    date_counter += 7
    with open("app/src/webuntis_data/blocked_ids.json", "r") as file:
        blocked_ids = json.load(file)
    name = blocked_ids[int(number)]["name"]
    
    return flask.redirect("/personalisierter_Stundenplan/"+name)

if __name__ == "__main__":
    app.run(debug=True)