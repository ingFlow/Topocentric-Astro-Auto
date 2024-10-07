from flask import Flask, render_template, jsonify, request
import pd_automate 
import pssr_swiss_auto
import secondary_automate
import transit_swiss_auto
import main_converge
import analysis
import julian
import aspects_implementation
from datetime import datetime
import swisseph as swe
import lunar_auto
import os
import re

class aTechniqueType:
    PRIMARY_DIRECT = 0  #diff oorder of technique type specific to index.html
    SECONDARY_DIRECT = 1
    PSSR = 2
    TRANSIT = 3
    LUNAR = 4
    NATAL = 5

geo_pos_natal = []
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

    dt_actual_dob, _, _, geopos_nat, list_of_events = main_converge.get_json_birth_data(f"data_input/{current_file}")
    global geo_pos_natal
    geo_pos_natal = geopos_nat
    
    list_dt_events = [t[0].isoformat() for t in list_of_events]
    list_type_events = [pd_automate.EventType.get_name(t[1]) for t in list_of_events]
    list_event_locations = [t[2] for t in list_of_events]
    list_event_index = [t[1] for t in list_of_events]
    #CHANGE HERE FOR LEFT COL TIMES
    '''list_times = [
        datetime(2000,3,11,9,00,2),
        datetime(2000,3,11,14,10,24),
        datetime(2000,3,11,14,12,56),
        datetime(2000,3,11,12,00,2)
    ]'''
    
    str_date = dt_actual_dob.strftime('%d %B %Y')
    #list_times = aspects_implementation.process_csv('ingtea_ver3_sorted_data.csv',str_date,100,+2)
    list_times = aspects_implementation.process_polaris_times('txt/ingtea rect ver 2 - 1 date was wrong.txt', 50)
    list_times = [dt_actual_dob]
    left_items = [t.isoformat() for t in list_times]
    right_items = [f"{dt}, {ty}, {i}, {loc}" for dt, ty, i, loc in zip(list_dt_events, list_type_events, list_event_index,list_event_locations)]
    return render_template('index.html', left_column_items=left_items, right_column_items=right_items, files=files, current_file=current_file)

@app.route('/update_content')
def update_content():
    global restrict_orb
    left_radio = request.args.get('left_radio', '')
    flag_show_accepted = True if left_radio == 'accepted' else False
    technique = int(request.args.get('right_radio', ''))
    radix_date = request.args.get('left_item', '')
    dt_event = request.args.get('right_item', '')  
    restrict_orb = int(request.args.get('orb_input',restrict_orb))
    flag_orb_restrict = True if (restrict_orb != -1) else False

    try:
        radix_date = datetime.fromisoformat(request.args.get('left_item', ''))
        jd_radix = julian.to_jd(radix_date)
        static_message = ''
        event_info = request.args.get('right_item', '').split(', ')
        dt_event = datetime.fromisoformat(event_info[0])
        event_id = int(event_info[2])
        event_locstr = [event_info[3][1:],event_info[4],event_info[5][:-1]]
        event_loc = [float(i) for i in event_locstr]
        score = 0

        rad_houses_info = swe.houses(jd_radix, geo_pos_natal[0], geo_pos_natal[1], b'T')
        rad_planets_labelled = pd_automate.calc_natal_planets_labelled(jd_radix)
        rad_planets_equatorial = pd_automate.calc_rad_planets_equatorial(jd_radix)
        rad_planets_houses_labelled = aspects_implementation.calc_rad_planet_houses_labelled(jd_radix, geo_pos_natal[0], geo_pos_natal[1])
        if technique == aTechniqueType.PRIMARY_DIRECT:
            str_rad_dir_aspects, str_rad_conv_aspects = pd_automate.pd_for_time_event(jd_radix, julian.to_jd(dt_event), geo_pos_natal, rad_planets_labelled, rad_planets_equatorial, rad_houses_info)
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects   
        elif technique == aTechniqueType.SECONDARY_DIRECT:
            str_rad_n_prog_aspects, str_rad_n_reg_aspects = secondary_automate.secondary_for_event(jd_radix, julian.to_jd(dt_event), geo_pos_natal[0], geo_pos_natal[1])
            str_all_directed_aspects = str_rad_n_prog_aspects + '\n' + str_rad_n_reg_aspects
        elif technique == aTechniqueType.PSSR:
            str_rad_dir_aspects, str_rad_conv_aspects = pssr_swiss_auto.calc_pssr_for_date(julian.from_jd(jd_radix), dt_event, rad_planets_houses_labelled)
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects 
        elif technique == aTechniqueType.TRANSIT:
            str_rad_dir_aspects, str_rad_conv_aspects = transit_swiss_auto.calc_transits_for_date(jd_radix, julian.to_jd(dt_event), rad_planets_houses_labelled)
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects 
        elif technique == aTechniqueType.NATAL:
            str_all_directed_aspects = ''
            for p in rad_planets_houses_labelled:
                str_all_directed_aspects+= f"{p}\n"
        elif technique == aTechniqueType.LUNAR:
            all_charts = lunar_auto.calc_all_lunars_for_date(julian.from_jd(jd_radix),dt_event,event_loc,geo_pos_natal,lunar_orb)
            str_all_directed_aspects = lunar_auto.get_str_labelled_aspects_from_array(all_charts)
            counts = lunar_auto.count_each_planet_lunars(str_all_directed_aspects)
            str_counts = lunar_auto.get_str_planet_counts(counts)
            mal_count, ben_count = lunar_auto.count_mal_ben_all_lunars(julian.from_jd(jd_radix),dt_event,event_loc,geo_pos_natal,lunar_orb)
            static_message = f"{str_counts} #Malefics: {mal_count} vs Benefics: {ben_count}#"
        
        list_all_asp = str_all_directed_aspects.split('\n')

        if flag_show_accepted:
            if technique != aTechniqueType.LUNAR:
                score, str_accepted_aspects = pd_automate.count_pd_score_acceptable_aspects(event_id, str_all_directed_aspects, 0)
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

        static_message = static_message + f"Radix Date: {radix_date} &nbsp;&nbsp;&nbsp;&nbsp; GEO_LAT: {geo_pos_natal[0]} &nbsp;&nbsp;&nbsp;&nbsp; GEO_LONG: {geo_pos_natal[1]} <br> Event Date: {dt_event} &nbsp;&nbsp;&nbsp;&nbsp; Event Type: {event_info[1]}: {event_id} &nbsp;&nbsp;&nbsp;&nbsp; Score: {score}"           
        scrollable_message = f"{html_list}"
    except:
        static_message = f"Static Content: Only show accepted directions?: {flag_show_accepted}, Technique: {technique}"
        scrollable_message = f"Scrollable Content: Detailed information about {type(radix_date)} {radix_date} and {type(dt_event)} {dt_event} "

    return jsonify({
        'static_message': static_message,
        'scrollable_message': scrollable_message
    })

'''@app.route('/update_file', methods=['POST'])
def update_file():
    global current_file
    data = request.get_json()
    current_file = data['filename']  # Update the global file name
    home()
    return render_template('index.html', left_column_items=['this'], right_column_items=['that'], files=['no'], current_file=current_file)
'''
def reset_globals():
    global geo_pos_natal
    geo_pos_natal = []

if __name__ == '__main__':
    #main_converge.pd_rect_grid_score_create('data_input/ing tea.json','ingtea_rect_ver3_',8)
    #main_converge.other_techniques_from_pd_rect('txt/9_9_ver3_sorted_planet_data.csv', 'data_input/jacquiline onassis.json', '9_14_ver1_', 100, -4)
    #DONT USE UNLESS NEEDED
    #aspects_implementation.count_aspect_groups_txt('ingtea_rect_ver3_2000-03-12_primaries.txt',False)
    #analysis.create_csv_count_txt('ingtea_rect_ver3_2000-03-12_primariesCOUNT.txt','ingtea_ver3_sorted_data.csv')
    
    app.run(debug=True)


