import pd_automate
from datetime import timedelta
import julian
import swisseph as swe
import pd_automate
import secondary_automate
import pssr_swiss_auto as pssr_auto
import transit_swiss_auto as transit_auto
 
class TechniqueType:
    PRIMARY_DIRECT = 0
    SECONDARY_DIRECT = 1
    PSSR = 2
    TRANSIT = 3

PLANETS = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Mean_Node']
grid_aspects =[]
date_technique = -1
aspect_type = -1

def resetvars():
    global grid_aspects, date_technique, aspect_type
    grid_aspects = []
    date_technique = -1
    aspect_type = -1

def generate_grid_angular_aspects(filename, start_time, end_time, increment_seconds, list_dt_events, geo_positions: list[3], type: pd_automate.AspectType, technique: TechniqueType):
    global grid_aspects, date_technique, aspect_type
    date_technique = technique
    aspect_type = type
    temp_list_event = ['Time']

    for i in range(0,len(list_dt_events)):
        temp_list_event.append(f"{i}: {list_dt_events[i][0].strftime('%Y-%m-%d')}")
    temp_list_event.append('Count')
    grid_aspects.append(temp_list_event)
    
    current_time = start_time
    increment = timedelta(seconds=increment_seconds)
    
    while current_time <= end_time:
        print(f"working on: {current_time}....")
        append_grid_acceptable_angles(list_dt_events, julian.to_jd(current_time),geo_positions)
        current_time += increment

    # Handle the case where the last increment might exceed the end time
    if current_time > end_time:
        append_grid_acceptable_angles(list_dt_events, julian.to_jd(current_time),geo_positions)
    
    with open(f"{filename}.txt", "w") as file:
        for time in grid_aspects:
            file.write(f"{str(time)}\n")
    
def append_grid_acceptable_angles(list_dt_events, jd_radix : julian, geo_positions: list[3]):
    formatted_time = julian.from_jd(jd_radix).strftime('%H:%M:%S')
    temp_list_event = [formatted_time] 
    count = 0
    
    rad_houses_info = swe.houses(jd_radix, geo_positions[0], geo_positions[1], b'T')
    rad_planets_labelled = pd_automate.calc_natal_planets_labelled(jd_radix)
    rad_planets_equatorial = pd_automate.calc_rad_planets_equatorial(jd_radix)
    rad_planets_houses_labelled = calc_rad_planet_houses_labelled(jd_radix, geo_positions[0], geo_positions[1])

    event_index = 0
    for dt_event, event_id in list_dt_events:
        if date_technique == TechniqueType.PRIMARY_DIRECT:
            str_rad_dir_aspects, str_rad_conv_aspects = pd_automate.pd_for_time_event(jd_radix, julian.to_jd(dt_event), geo_positions, rad_planets_labelled, rad_planets_equatorial, rad_houses_info)
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects   
        elif date_technique == TechniqueType.SECONDARY_DIRECT:
            str_rad_n_prog_aspects, str_rad_n_reg_aspects = secondary_automate.secondary_for_event(jd_radix, julian.to_jd(dt_event), geo_positions[0], geo_positions[1])
            str_all_directed_aspects = str_rad_n_prog_aspects + '\n' + str_rad_n_reg_aspects
        elif date_technique == TechniqueType.PSSR:
            str_rad_dir_aspects, str_rad_conv_aspects = pssr_auto.calc_pssr_for_date(julian.from_jd(jd_radix), dt_event, rad_planets_houses_labelled)
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects 
        elif date_technique == TechniqueType.TRANSIT:
            str_rad_dir_aspects, str_rad_conv_aspects = transit_auto.calc_transits_for_date(jd_radix, julian.to_jd(dt_event), rad_planets_houses_labelled)
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects 
        
        
    
        if date_technique == TechniqueType.PRIMARY_DIRECT:
            count, str_acceptable_aspects = pd_automate.count_pd_score_acceptable_aspects(event_id, str_all_directed_aspects, count)
        else:
            count, str_acceptable_aspects = pd_automate.count_event_acceptable_aspects(event_id, str_all_directed_aspects, count, aspect_type)

        if str_acceptable_aspects == '':
            temp_list_event.append(f"{str(event_index)}")
        else:
            temp_list_event.append(str_acceptable_aspects)
    
        event_index += 1

    temp_list_event.append(count)

    global grid_aspects
    grid_aspects.append(temp_list_event)    
    return

def count_aspect_groups_txt(filename):
    results = []

    with open(f"{filename}.txt", 'r') as infile:
        for line in infile:
            parts = eval(line.strip())
            time = parts[0]
            aspects = parts[1:-1]
            count = parts[-1]

            opp_conj_count = 0
            sqr_tri_sext_count = 0
            minor_count = 0

            for all_aspect in aspects:
                if all_aspect:
                    aspect = all_aspect.split(', ')
                    for asp in aspect:
                        if asp[0] == '(':
                            if '\n' in asp:
                                asp_lines = asp.split('\n')
                                for line in asp_lines:
                                    asp = line.split(' ')[2]

                                    if ('sesquisquare' in asp) or ('semisquare' in asp) or ('semisextile' in asp) or ('quincunx' in asp):
                                        minor_count += 1
                                    elif ('opposition' in asp) or ('conjunction' in asp):
                                        opp_conj_count += 1
                                    elif ('square' in asp) or ('sextile' in asp) or ('trine' in asp):
                                        sqr_tri_sext_count += 1
                            else:
                                asp = asp.split(' ')[2]

                                if ('sesquisquare' in asp) or ('semisquare' in asp) or ('semisextile' in asp) or ('quincunx' in asp):
                                    minor_count += 1
                                elif ('opposition' in asp) or ('conjunction' in asp):
                                    opp_conj_count += 1
                                elif ('square' in asp) or ('sextile' in asp) or ('trine' in asp):
                                    sqr_tri_sext_count += 1

            results.append([f"{time}, {count}, opp/conj: {opp_conj_count}", f"sqr/tri/sext: {sqr_tri_sext_count}", f"major: {sqr_tri_sext_count+opp_conj_count}", f"minor: {minor_count}"])                
    print(results)
    with open(f"{filename}COUNT.txt", 'w') as outfile:
        for result in results:
            outfile.write(str(result) + '\n')

def calc_rad_planet_houses_labelled(jd_radix, geo_latitude, geo_longitude):
    rad_planets = pd_automate.calc_natal_planets_labelled(jd_radix)
    houses = swe.houses(jd_radix, geo_latitude, geo_longitude, b'T')
    ac = houses[0][0]
    sun_long = rad_planets[PLANETS.index('Sun')][1]
    moon_long = rad_planets[PLANETS.index('Moon')][1]
    pof_long = swe.degnorm(ac + moon_long - sun_long)
    rad_planets.append(('POF',pof_long,'(r)'))
    for house_no in range(0,len(houses[0])):
        rad_planets.append((f'H{house_no+1}',houses[0][house_no],'(r)'))
    return  rad_planets