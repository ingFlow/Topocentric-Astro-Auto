from flask import Flask, render_template, jsonify, request
import pd_automate 
import pssr_swiss_auto
import secondary_automate
import transit_swiss_auto
import main_converge
import julian
import aspects_implementation
from datetime import datetime
import swisseph as swe
import lunar_auto

class aTechniqueType:
    PRIMARY_DIRECT = 0  #diff oorder of technique type specific to index.html
    SECONDARY_DIRECT = 1
    PSSR = 2
    TRANSIT = 3
    LUNAR = 4
    ALL = 5

geo_positions = []
lunar_orb = 9

app = Flask(__name__)

@app.route('/')
def home():
    dt_actual_dob, _, _, geopos, list_of_events = main_converge.get_json_birth_data("data_input/queen victoria.json")
    global geo_positions
    geo_positions = geopos
    
    list_dt_events = [t[0].isoformat() for t in list_of_events]
    list_type_events = [pd_automate.EventType.get_name(t[1]) for t in list_of_events]
    list_event_index = [t[1] for t in list_of_events]
    #CHANGE HERE FOR LEFT COL TIMES
    list_times = [dt_actual_dob]
    '''str_date = dt_actual_dob.strftime('%d %B %Y')
    list_times = aspects_implementation.process_csv('9_14_ver1_sorted_planet_data.csv',str_date,100,-4)
    '''
    left_items = [t.isoformat() for t in list_times]
    right_items = [f"{dt}, {ty}, {i}" for dt, ty, i in zip(list_dt_events, list_type_events, list_event_index)]
    return render_template('index.html', left_column_items=left_items, right_column_items=right_items)

@app.route('/update_content')
def update_content():
    left_radio = request.args.get('left_radio', '')
    flag_show_accepted = True if left_radio == 'accepted' else False
    technique = int(request.args.get('right_radio', ''))
    radix_date = request.args.get('left_item', '')
    dt_event = request.args.get('right_item', '')
    try:
        radix_date = datetime.fromisoformat(request.args.get('left_item', ''))
        jd_radix = julian.to_jd(radix_date)
    
        event_info = request.args.get('right_item', '').split(', ')
        dt_event = datetime.fromisoformat(event_info[0])
        event_id = int(event_info[2])
        jd_event = julian.to_jd(dt_event)
        score = 0

        '''if technique == aTechniqueType.PRIMARY_DIRECT:
            str_asp_dir, str_asp_conv = pd_automate.pd_for_time_event_norad(jd_radix,jd_event,geo_positions)
            str_all_aspects = str_asp_dir + str_asp_conv
        elif technique == aTechniqueType.PSSR:
            str_asp_dir, str_asp_conv = pssr_swiss_auto.pssr_for_date_event_norad(jd_radix,jd_event,geo_positions)
            str_all_aspects = str_asp_dir + str_asp_conv'''
        rad_houses_info = swe.houses(jd_radix, geo_positions[0], geo_positions[1], b'T')
        rad_planets_labelled = pd_automate.calc_natal_planets_labelled(jd_radix)
        rad_planets_equatorial = pd_automate.calc_rad_planets_equatorial(jd_radix)
        rad_planets_houses_labelled = aspects_implementation.calc_rad_planet_houses_labelled(jd_radix, geo_positions[0], geo_positions[1])
        if technique == aTechniqueType.PRIMARY_DIRECT:
            str_rad_dir_aspects, str_rad_conv_aspects = pd_automate.pd_for_time_event(jd_radix, julian.to_jd(dt_event), geo_positions, rad_planets_labelled, rad_planets_equatorial, rad_houses_info)
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects   
        elif technique == aTechniqueType.SECONDARY_DIRECT:
            str_rad_n_prog_aspects, str_rad_n_reg_aspects = secondary_automate.secondary_for_event(jd_radix, julian.to_jd(dt_event), geo_positions[0], geo_positions[1])
            str_all_directed_aspects = str_rad_n_prog_aspects + '\n' + str_rad_n_reg_aspects
        elif technique == aTechniqueType.PSSR:
            str_rad_dir_aspects, str_rad_conv_aspects = pssr_swiss_auto.calc_pssr_for_date(julian.from_jd(jd_radix), dt_event, rad_planets_houses_labelled)
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects 
        elif technique == aTechniqueType.TRANSIT:
            str_rad_dir_aspects, str_rad_conv_aspects = transit_swiss_auto.calc_transits_for_date(jd_radix, julian.to_jd(dt_event), rad_planets_houses_labelled)
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects 
        elif technique == aTechniqueType.ALL:
            str_all_directed_aspects = ''
            for p in rad_planets_houses_labelled:
                str_all_directed_aspects+= f"{p}\n"
        elif technique == aTechniqueType.LUNAR:
            all_charts = lunar_auto.calc_all_lunars_for_date(julian.from_jd(jd_radix),dt_event,geo_positions,geo_positions,lunar_orb)
            str_all_directed_aspects = lunar_auto.get_str_only_aspects_from_array(all_charts)
            counts = lunar_auto.count_each_planet_lunars(str_all_directed_aspects)
            str_counts = lunar_auto.get_str_counts(counts)
            mal_count, ben_count = lunar_auto.count_mal_ben_all_lunars(julian.from_jd(jd_radix),dt_event,geo_positions,geo_positions,lunar_orb)
            static_message = f"{str_counts} #Malefics: {mal_count} vs Benefics: {ben_count}#"
        list_all_asp = str_all_directed_aspects.split('\n')

        if flag_show_accepted:
            score, str_accepted_aspects = pd_automate.count_pd_score_acceptable_aspects(event_id, str_all_directed_aspects, 0)
            list_all_asp = str_accepted_aspects.split('\n')
        
        list_all_asp = list(filter(lambda s: s.strip(), list_all_asp))
        html_list = "<ul>" + "".join(f"<li>{item}</li>" for item in list_all_asp) + "</ul>"

        static_message = static_message + f" Radix Date: {radix_date} &nbsp;&nbsp;&nbsp;&nbsp; GEO_LAT: {geo_positions[0]} &nbsp;&nbsp;&nbsp;&nbsp; GEO_LONG: {geo_positions[1]} <br> Event Date: {dt_event} &nbsp;&nbsp;&nbsp;&nbsp; Event Type: {event_info[1]}: {event_id} &nbsp;&nbsp;&nbsp;&nbsp; Score: {score}"           
        scrollable_message = f"{html_list}"
    except:
        static_message = f"Static Content: Only show accepted directions?: {flag_show_accepted}, Technique: {technique}"
        scrollable_message = f"Scrollable Content: Detailed information about {type(radix_date)} {radix_date} and {type(dt_event)} {dt_event} "

    return jsonify({
        'static_message': static_message,
        'scrollable_message': scrollable_message
    })

def reset_globals():
    global geo_positions
    geo_positions = []

if __name__ == '__main__':
    app.run(debug=True)

