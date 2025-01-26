from flask import Flask, render_template, jsonify, request, send_from_directory
import pd_automate 
import pssr_swiss_auto
import secondary_automate
import transit_swiss_auto
import lunar_auto
import sra_auto
import harmonics_auto
import main_techniques
import julian
import process_techniques_files
from datetime import datetime
import swisseph as swe
from timezonefinder import TimezoneFinder
import os
import re
import shutil
import json
from constants import calc_planets_pof_houses_labelled
from aspects_base import calculate_obliquity
from kerykeion import AstrologicalSubject, KerykeionChartSVG

class aTechniqueType:
    PRIMARY_DIRECT = 0  #diff order of technique type specific to index.html
    SECONDARY_DIRECT = 1
    PSSR = 2
    TRANSIT = 3
    LUNAR = 4
    SRA = 5
    HARMONICS = 6
    NATAL = 7

geo_pos_natal = []
dt_radix = None
lunar_orb = 9
restrict_orb = 3
current_file = "ing tea.json"
DATA_INPUT_DIR = 'data_input'

app = Flask(__name__)

@app.route('/')
def home():
    global current_file
    files = [f for f in os.listdir(DATA_INPUT_DIR) if f.endswith('.json')]
    current_file = request.args.get('filename', current_file)
    if current_file not in files:
        current_file = files[0]

    dt_actual_dob, _, dt_epoch, geopos_nat, list_of_events = main_techniques.get_json_birth_data(f"data_input/{current_file}")
    global geo_pos_natal, dt_radix
    geo_pos_natal = geopos_nat
    dt_radix = dt_actual_dob
    
    list_dt_events = [t[0].isoformat() for t in list_of_events]
    list_type_events = [pd_automate.EventType.get_name(t[1]) for t in list_of_events]
    list_event_locations = [t[2] for t in list_of_events]
    list_event_index = [t[1] for t in list_of_events]
    #CHANGE HERE FOR LEFT COL TIMES
    list_times = [
        datetime(1929,7,27,21,17,36),
        datetime(1929,7,28,18,30,4),
        datetime(1929,7,27,21,41,20),
        datetime(1929,7,27,22,14,24)
        #07:49:20
        #15:49:36
        
    ]

    time_strings = [
        "1:51:36", "7:46:40", "13:49:20", "10:38:48", "13:41:12", "15:26:56",
        "12:58:24", "11:27:52", "10:15:36", "12:29:28", "15:24:56",
        "11:39:44", "15:29:20", "7:49:12", "9:23:28", "14:26:56",
        "5:37:36", "13:08:40", "13:46:32", "6:06:56", "9:21:28",
        "8:28:16", "15:44:56", "12:09:04", "9:44:00", "14:09:12"
    ]

    #list_times = [datetime.strptime(f"1874-11-30 {time}", "%Y-%m-%d %H:%M:%S") for time in time_strings]
    
    str_date = dt_actual_dob.strftime('%d %B %Y')
    #list_times = aspects_implementation.process_manual_rect_csv('ingtea_ver3_sorted_data.csv',str_date,100,+2)
    #list_times = process_techniques_files.process_polaris_times('data_times/jacqui sorted max a 4 rect.txt', 100)
    list_times = process_techniques_files.process_datetime_count_csv('data_times/winston narrow.csv')
    list_times = [dt_actual_dob, dt_epoch]
    list_times.append(dt_actual_dob)
    temp = process_techniques_files.generate_hourly_datetimes(geo_pos_natal,dt_actual_dob)
    for t in temp:
        list_times.append(t)
    
    #left_items = [t.isoformat() for t in list_times]
    left_items = list_times
    print(list_times)
    right_items = [f"{dt}, {ty}, {i}, {loc}" for dt, ty, i, loc in zip(list_dt_events, list_type_events, list_event_index,list_event_locations)]
    return render_template('index.html', left_column_items=left_items, right_column_items=right_items, files=files, current_file=current_file)

@app.route('/update_content')
def update_content():
    global restrict_orb
    flag_show_accepted = request.args.get('show_accepted', default='false') == 'true'
    technique = int(request.args.get('right_radio', ''))
    radix_date = request.args.get('left_item', '')
    dt_event = request.args.get('right_item', '')  
    restrict_orb = int(request.args.get('orb_input',restrict_orb))
    flag_orb_restrict = True if (restrict_orb != -1) else False
    flag_show_data = request.args.get('show_data', default='false') == 'true'

    try:
        radix_date = datetime.fromisoformat(request.args.get('left_item', ''))
        jd_radix = julian.to_jd(radix_date)
        static_message = ''
        event_info = request.args.get('right_item', '').split(', ')
        dt_event = datetime.fromisoformat(event_info[0])
        event_id = int(event_info[2])
        event_locstr = [event_info[3][1:],event_info[4],event_info[5][:-1]]
        event_geopos = [float(i) for i in event_locstr]
        score = 0

        rad_houses_info = swe.houses(jd_radix, geo_pos_natal[0], geo_pos_natal[1], b'T')
        rad_planets_equatorial = pd_automate.calc_rad_planets_equatorial(jd_radix)
        rad_planets_pof_houses_labelled = calc_planets_pof_houses_labelled(jd_radix, geo_pos_natal)
        if technique == aTechniqueType.PRIMARY_DIRECT:
            e = calculate_obliquity(jd_radix)
            pd_auto_obj  = pd_automate.PD_Automate(jd_radix, julian.to_jd(dt_event), geo_pos_natal, rad_planets_pof_houses_labelled, rad_planets_equatorial, rad_houses_info, e)
            str_rad_dir_aspects, str_rad_conv_aspects = pd_auto_obj.get_aspects_str()
            pd_info = pd_auto_obj.get_extended_information()
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects   
            mdos_list = pd_auto_obj.get_mdos_natal()
            print(mdos_list)
        elif technique == aTechniqueType.SECONDARY_DIRECT:
            e = calculate_obliquity(jd_radix)
            secondary_obj = secondary_automate.Secondary_Auto(jd_radix, julian.to_jd(dt_event), geo_pos_natal[0], geo_pos_natal[1], e, rad_houses_info[1][2], rad_planets_pof_houses_labelled)
            secondary_info = secondary_obj.get_dict_info()
            str_rad_n_prog_aspects, str_rad_n_reg_aspects = secondary_obj.get_str_aspects()
            str_all_directed_aspects = str_rad_n_prog_aspects + '\n' + str_rad_n_reg_aspects
        elif technique == aTechniqueType.PSSR:
            pssr_obj = pssr_swiss_auto.PSSR_Auto(julian.from_jd(jd_radix), dt_event, rad_planets_pof_houses_labelled)
            str_rad_dir_aspects, str_rad_conv_aspects = pssr_obj.get_str_aspects()
            pssr_info = pssr_obj.get_dict_info()
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects 
        elif technique == aTechniqueType.TRANSIT:
            transit_obj = transit_swiss_auto.Transit_Auto(jd_radix, julian.to_jd(dt_event), event_geopos, rad_planets_pof_houses_labelled)
            str_rad_dir_aspects, str_rad_conv_aspects = transit_obj.get_str_aspects()
            transit_info = transit_obj.get_dict_info()
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects 
        elif technique == aTechniqueType.SRA:
            sra_auto_obj = sra_auto.SRA_Auto(julian.from_jd(jd_radix), dt_event, geo_pos_natal,rad_planets_pof_houses_labelled)
            str_rad_dir_aspects, str_rad_conv_aspects = sra_auto_obj.get_str_aspects()
            sra_info = sra_auto_obj.get_info()
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects 
            str_all_directed_aspects = str_all_directed_aspects.replace(")(", ")\n(")
        elif technique == aTechniqueType.NATAL:
            str_all_directed_aspects = ''
            for p in rad_planets_pof_houses_labelled:
                str_all_directed_aspects+= f"{p}\n"
        elif technique == aTechniqueType.LUNAR:
            lunar_obj = lunar_auto.Lunar_Auto(julian.from_jd(jd_radix),dt_event,event_geopos,geo_pos_natal,lunar_orb)
            lunar_info = lunar_obj.get_info()
            all_charts = lunar_obj.get_all_lunars()
            str_all_directed_aspects = lunar_auto.get_str_labelled_aspects_from_array(all_charts)
            counts = lunar_auto.count_each_planet_lunars(str_all_directed_aspects)
            str_counts = lunar_auto.get_str_planet_counts(counts)
            mal_count, ben_count = lunar_auto.count_mal_ben_from_str_aspects(str_all_directed_aspects)
            static_message = f"{str_counts} #Malefics: {mal_count} vs Benefics: {ben_count}#"
        elif technique == aTechniqueType.HARMONICS:
            harmonics_obj = harmonics_auto.Harmonics_Auto(jd_radix, julian.to_jd(dt_event), geo_pos_natal, rad_planets_pof_houses_labelled)
            str_rad_harm_aspects = harmonics_obj.get_str_aspects()
            harmonics_info = harmonics_obj.get_dict_info()
            str_all_directed_aspects = str_rad_harm_aspects
        
        str_all_directed_aspects = re.sub(r"H10,","MC,", str_all_directed_aspects)
        str_all_directed_aspects = re.sub(r"H1,","AS,", str_all_directed_aspects)
        str_all_directed_aspects = re.sub(r"H7,","DS,", str_all_directed_aspects)
        str_all_directed_aspects = re.sub(r"H4,","IC,", str_all_directed_aspects)

        list_all_asp = str_all_directed_aspects.split('\n')

        if flag_show_accepted:
            if technique != aTechniqueType.LUNAR and technique != aTechniqueType.PSSR:
                score, str_accepted_aspects = pd_automate.count_pd_score_acceptable_aspects(event_id, str_all_directed_aspects, 0)
                list_all_asp = str_accepted_aspects.split('\n')
            elif technique == aTechniqueType.PSSR:
                score, str_accepted_aspects = pd_automate.count_event_acceptable_aspects(event_id,str_all_directed_aspects,0,pd_automate.AspectType.FAST_TO_SLOW_COMBO)
                list_all_asp = str_accepted_aspects.split('\n')
                
        temp_arr = []
        if flag_orb_restrict:
            for line in list_all_asp:
                match = re.search(r'(\d+(\.\d+)?)\'', line)
                if match:
                    asp_orb_deg = float(match.group(1))
                    if asp_orb_deg <= restrict_orb:
                        temp_arr.append(line)
                else:
                    temp_arr.append(line)
            list_all_asp = temp_arr
        
        list_all_asp = list(filter(lambda s: s.strip(), list_all_asp))
        html_list = "<ul>" + "".join(f"<li>{item}</li>" for item in list_all_asp) + "</ul>"
        
        if technique == aTechniqueType.LUNAR and flag_show_accepted:
            html_list = str_counts.replace(",", "\n")

        if flag_show_data:
            technique_data = None
            if technique == aTechniqueType.PRIMARY_DIRECT:
                technique_data = pd_info
            elif technique == aTechniqueType.SECONDARY_DIRECT:
                technique_data = secondary_info
            elif technique == aTechniqueType.PSSR:
                technique_data = pssr_info
            elif technique == aTechniqueType.TRANSIT:
                technique_data = transit_info
            elif technique == aTechniqueType.LUNAR:
                technique_data = lunar_info
            elif technique == aTechniqueType.SRA:
                technique_data = sra_info
            elif technique == aTechniqueType.HARMONICS:
                technique_data = harmonics_info
            
            if technique == aTechniqueType.PRIMARY_DIRECT or technique == aTechniqueType.LUNAR:
                data_list = []
                for main_key, sub_dict in technique_data.items():
                    data_list.append(f"{main_key}:") 
                    
                    if main_key == "MDOs":
                        data_list.append(sub_dict)
                    else:
                        for sub_key, value in sub_dict.items():
                            data_list.append(f"  {sub_key}: {value}")
            else:  
                data_list = [f"{key}: {value}" for key, value in technique_data.items()]
            html_list = "<ul>" + "".join(f"<li>{item}</li>" for item in data_list) + "</ul>"

        static_message = static_message + f"Radix Date: {radix_date} &nbsp;&nbsp;&nbsp;&nbsp; GEO_LAT: {geo_pos_natal[0]} &nbsp;&nbsp;&nbsp;&nbsp; GEO_LONG: {geo_pos_natal[1]} <br> Event Date: {dt_event} &nbsp;&nbsp;&nbsp;&nbsp; Event Type: {event_info[1]}: {event_id} &nbsp;&nbsp;&nbsp;&nbsp; Score: {score}"           
        scrollable_message = f"{html_list}"
    except:
        static_message = f"Static Content: Only show accepted directions?: {flag_show_accepted}, Technique: {technique}"
        scrollable_message = f"Scrollable Content: Detailed information about {type(radix_date)} {radix_date} and {type(dt_event)} {dt_event} "

    return jsonify({
        'static_message': static_message,
        'scrollable_message': scrollable_message
    })

@app.route('/custom_action', methods=['POST'])
def custom_action():
    data = request.get_json()
    selected_text = data.get('selected_text')
    left_item = data.get('left_item')
    right_item = data.get('right_item')
    right_radio = data.get('right_radio')

    # Process received data as needed
    message = f"Received text: {selected_text}, Left Item: {left_item}, Right Item: {right_item}, Radio Value: {right_radio}"
    return jsonify({"message": message})

def clear_directory(directory_path):
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        shutil.rmtree(directory_path)
        os.makedirs(directory_path)  # Recreate the empty directory
    else:
        print("Directory does not exist or is not a directory.")

def get_timezone_name_from_pos(geopos):
    tf = TimezoneFinder()
    geo_lat = geopos[0]
    geo_long = geopos[1]
    
    return tf.timezone_at(lat=geo_lat, lng=geo_long)

def reset_globals():
    global geo_pos_natal, dt_radix
    geo_pos_natal = []
    dt_radix = None
    
@app.route('/generate_chart')
def generate_chart():
    global geo_pos_natal

    chart_datetime = request.args.get('chart_datetime', default=dt_radix) 
    chart_pos = request.args.get('chart_pos', default=geo_pos_natal)
    technique = int(request.args.get('right_radio', ''))
    event_info = request.args.get('right_item', '').split(', ')

    try:
        event_locstr = [event_info[3][1:],event_info[4],event_info[5][:-1]]
        event_pos = [float(i) for i in event_locstr]
    except:
        event_pos = chart_pos
    
    if chart_datetime != dt_radix:
        try:
            chart_datetime = datetime.fromisoformat(chart_datetime)
        except ValueError:
            try:
                chart_datetime = datetime.strptime(chart_datetime, "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                try:
                    chart_datetime = datetime.strptime(chart_datetime, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    return None # 

    if technique in [aTechniqueType.SRA, aTechniqueType.LUNAR, aTechniqueType.TRANSIT] and chart_pos == geo_pos_natal:
        chart_pos = [event_pos[0],event_pos[1]]
    
    #timezone_name = get_timezone_name_from_pos(chart_pos)
    filename = f'{chart_datetime.strftime("%Y-%m-%d %H_%M_%S")}'    
    svg_full_path = f"static/charts/{filename} - Natal Chart.svg"
    svg_path = f"{filename} - Natal Chart.svg" 
    
    chart_subject = AstrologicalSubject(
        filename,
        chart_datetime.year,
        chart_datetime.month,
        chart_datetime.day,
        chart_datetime.hour,
        chart_datetime.minute,
        chart_datetime.second,  
        lng=chart_pos[1],
        lat=chart_pos[0],
        tz_str="UTC",
        houses_system_identifier="T"
    )
    
    date_natal_chart = KerykeionChartSVG(chart_subject, theme="dark-high-contrast", new_output_directory="static/charts")
    date_natal_chart.makeSVG()

    if os.path.exists(svg_full_path):
        return send_from_directory('static/charts', svg_path) 
    else:
        return "File not found", 404
    
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

'''@app.route('/chart-data')
def chart_data():
    data_radix = {
        "planets": {
            "Moon": [45.930008627285154],
            "Venus": [263.2584780960899],
            "Jupiter": [173.07043720306802],
            "NNode": [174.6895307834239],
            "Mars": [217.97167231451178],
            "Lilith": [196.19480722950317],
            "Saturn": [252.92341772675047],
            "Chiron": [348.1157239728284],
            "Uranus": [16.7900184974611],
            "Sun": [297.68062428797253],
            "Mercury": [289.10132025725494],
            "Neptune": [338.01899718442604],
            "Pluto": [285.6473452237151, -0.123]
        },
        "cusps": [
            348.20510089894015,
            38.108507808919654,
            65.20783751818992,
            84.96083001338991,
            103.77897207128007,
            127.1084408347092,
            168.20510089894015,
            218.10850780891965,
            245.20783751818993,
            264.9608300133899,
            283.77897207128007,
            307.1084408347092
        ]
    }

    data_transit = {
        "planets": {
            "Moon": [60.739220451080115],
            "Venus": [305.6996431634707],
            "Jupiter": [198.6565699576221],
            "NNode": [157.25592636170012],
            "Mars": [324.84013049518734],
            "Lilith": [232.88904207991555],
            "Saturn": [259.1015412368795, -0.2],
            "Chiron": [350.7285587924208],
            "Uranus": [20.678747795787075],
            "Sun": [260.94912160755536],
            "Mercury": [281.5699804920016],
            "Neptune": [339.3848859932604],
            "Pluto": [286.29683069280685]
        },
        "cusps": [296, 350, 30, 56, 75, 94, 116, 170, 210, 236, 255, 274]
    }

    return jsonify({"radix": data_radix, "transit": data_transit})'''

if __name__ == '__main__':
    #THIS DOES NOT WORK  main_converge.pd_rect_grid_score_create('data_input/ing tea prim.json','ingtea_rect_ver4_',8)
    #main_techniques.rect_ver_data_create('data_times/winston narrow.csv', main_techniques.timesFileType.DATE_N_TIME, 'data_input/winston.json', 'data_rect/02_12_24_Winston_v1/02_12_24_')
    #DONT USE UNLESS NEEDED
    #aspects_implementation.count_aspect_groups_txt('ingtea_rect_ver4_2000-03-12_primaries.txt',False)
    #analysis.create_csv_count_txt(['txt/26_10_24_Jacqui/26_10_24_1929-07-28_primdirCOUNT.txt','txt/26_10_24_Jacqui/26_10_24_1929-07-28_secondCOUNT.txt','txt/26_10_24_Jacqui/26_10_24_1929-07-28_pssrCOUNT.txt','txt/26_10_24_Jacqui/26_10_24_1929-07-28_transCOUNT.txt'],'txt/26_10_24_Jacqui/26_10_24_Jacqui_data_tally.csv')
    #analysis.create_csv_count_txt(['txt/26_10_24_Jacqui/26_10_24_1929-07-28_primdirCOUNT.txt'],'txt/26_10_24_Jacqui/26_10_24_Jacqui_data_tally.csv')
    
    app.run(debug=True)


