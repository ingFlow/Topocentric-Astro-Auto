import pd_automate
from datetime import timedelta, datetime
import julian
import swisseph as swe
import pd_automate
import secondary_automate
import pssr_swiss_auto as pssr_auto
import transit_swiss_auto as transit_auto
import sra_auto
import pandas as pd
import lunar_auto as lunar
import re
from constants import calc_planets_pof_houses_labelled
from aspects_base import calculate_obliquity

class TechniqueType:
    PRIMARY_DIRECT = 0
    SECONDARY_DIRECT = 1
    PSSR = 2
    TRANSIT = 3
    LUNAR = 4

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
    rad_planets_equatorial = pd_automate.calc_rad_planets_equatorial(jd_radix)
    rad_planets_pof_houses_labelled = calc_planets_pof_houses_labelled(jd_radix, geo_positions)
    e = calculate_obliquity(jd_radix)

    event_index = 0
    for dt_event, event_id, _ in list_dt_events:
        if date_technique == TechniqueType.PRIMARY_DIRECT:
            pd_auto_obj  = pd_automate.PD_Automate(jd_radix, julian.to_jd(dt_event), geo_positions, rad_planets_pof_houses_labelled, rad_planets_equatorial, rad_houses_info, e)
            str_rad_dir_aspects, str_rad_conv_aspects = pd_auto_obj.get_aspects_str()
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects   
        elif date_technique == TechniqueType.SECONDARY_DIRECT:
            secondary_obj = secondary_automate.Secondary_Auto(jd_radix, julian.to_jd(dt_event), geo_positions[0], geo_positions[1], e, rad_houses_info[1][2], rad_planets_pof_houses_labelled)
            str_rad_n_prog_aspects, str_rad_n_reg_aspects = secondary_obj.get_str_aspects()
            str_all_directed_aspects = str_rad_n_prog_aspects + '\n' + str_rad_n_reg_aspects
        elif date_technique == TechniqueType.PSSR:
            pssr_obj = pssr_auto.PSSR_Auto(julian.from_jd(jd_radix), dt_event, rad_planets_pof_houses_labelled)
            str_rad_dir_aspects, str_rad_conv_aspects = pssr_obj.get_str_aspects()
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects 
        elif date_technique == TechniqueType.TRANSIT:
            transit_obj = transit_auto.Transit_Auto(jd_radix, julian.to_jd(dt_event), geo_positions, rad_planets_pof_houses_labelled)
            str_rad_dir_aspects, str_rad_conv_aspects = transit_obj.get_str_aspects()
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects 
        elif date_technique == TechniqueType.SRA:
            sra_auto_obj = sra_auto.SRA_Auto(julian.from_jd(jd_radix), dt_event, geo_positions,rad_planets_pof_houses_labelled)
            str_rad_dir_aspects, str_rad_conv_aspects = sra_auto_obj.get_str_aspects()
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects 
            str_all_directed_aspects = str_all_directed_aspects.replace(")(", ")\n(")
        
    
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

def count_ben_mal_planets_lunar(jd_radix):
    ca = lunar.get

def count_aspect_groups_txt(filename, flag_count_pssr_moon):
    results = []

    with open(filename, 'r') as infile:
        for line in infile:
            parts = eval(line.strip())
            time = parts[0]
            aspects = parts[1:-1]
            count = parts[-1]

            opp_conj_count = 0
            sqr_tri_sext_count = 0
            minor_count = 0
            moon_conj_opp_count = 0
            moon_sqr_tri_sext_count = 0
            empty_event_count = 0

            for all_aspect in aspects:
                if all_aspect:
                    if all_aspect[0] != '(':
                        empty_event_count += 1

                    if '\n' in all_aspect:
                        individual_aspects_list = all_aspect.split('\n')
                    else:
                        individual_aspects_list = [all_aspect]

                    for asp in individual_aspects_list:
                        if ('sesquisquare' in asp) or ('semisquare' in asp) or ('semisextile' in asp) or ('quincunx' in asp):
                            minor_count += 1
                        elif ('opposition' in asp) or ('conjunction' in asp):
                            if (flag_count_pssr_moon and (')) (Moon' in asp)):
                                moon_conj_opp_count += 1
                            opp_conj_count += 1
                        elif ('square' in asp) or ('sextile' in asp) or ('trine' in asp):
                            if (flag_count_pssr_moon and (')) (Moon' in asp)):
                                moon_sqr_tri_sext_count += 1
                            sqr_tri_sext_count += 1
                        
            if flag_count_pssr_moon:
                results.append([f"{time}, {count}, opp-conj: {opp_conj_count}, sqr-tri-sext: {sqr_tri_sext_count}, major: {sqr_tri_sext_count+opp_conj_count}, minor: {minor_count}, moon-opp-conj: {moon_conj_opp_count}, moon-sqr-tri-sext: {moon_sqr_tri_sext_count}, empty: {empty_event_count}"])                
            else:
                results.append([f"{time}, {count}, opp-conj: {opp_conj_count}, sqr-tri-sext: {sqr_tri_sext_count}, major: {sqr_tri_sext_count+opp_conj_count}, minor: {minor_count}, empty: {empty_event_count}"])                
    print(results)

    with open(f"{filename[:-4]}COUNT.txt", 'w') as outfile:
        for result in results:
            outfile.write(str(result) + '\n')

def generate_grid_times_manual(filename, list_times, list_dt_events, geo_positions: list[3], type: pd_automate.AspectType, technique: TechniqueType):
    global grid_aspects, date_technique, aspect_type
    date_technique = technique
    aspect_type = type
    temp_list_event = ['Time']

    for i in range(0,len(list_dt_events)):
        temp_list_event.append(f"{i}: {list_dt_events[i][0].strftime('%Y-%m-%d')}")
    temp_list_event.append('Count')
    grid_aspects.append(temp_list_event)
    
    for current_time in list_times:
        print(f"working on: {current_time}....")
        append_grid_acceptable_angles(list_dt_events, julian.to_jd(current_time),geo_positions)
    
    with open(f"{filename}.txt", "w") as file:
        for time in grid_aspects:
            file.write(f"{str(time)}\n")

from datetime import timedelta

def add_timezone_to_24_hours(timezone):
    base_time = timedelta(hours=24)
    adjusted_time = base_time + timedelta(hours=timezone)
    result_hours = adjusted_time.seconds // 3600 % 24
    
    return result_hours

def process_csv(file_path, end_date_str, count_times_wanted, i_timezone):
    """end date is day of birth 
    timezone is whatever you need to add to UT to get the local time"""
    df = pd.read_csv(file_path)
    times = df['Time'][:count_times_wanted].tolist()
    
    dt_bday = datetime.strptime(end_date_str, '%d %B %Y')
    
    datetime_list = []
    
    for time_str in times:
        time_obj = datetime.strptime(time_str, '%H:%M:%S')
        
        if time_obj.hour < add_timezone_to_24_hours(i_timezone):
            if i_timezone <= 0:
                datetime_obj = datetime.combine(dt_bday, time_obj.time())
            else: 
                datetime_obj = datetime.combine(dt_bday + timedelta(days=1), time_obj.time())
        else:
            if i_timezone <= 0:
                datetime_obj = datetime.combine(dt_bday - timedelta(days=1), time_obj.time())
            else:
                datetime_obj = datetime.combine(dt_bday, time_obj.time())
    
        datetime_list.append(datetime_obj)
    
    return datetime_list

def process_polaris_times(file_name, count_times_wanted):
    """Processes a text file with date and time entries.
    
    Args:
        file_path (str): Path to the text file.
        count_times_wanted (int): Number of times to process.
        i_timezone (int): Timezone offset to apply.

    Returns:
        List[datetime]: A list of datetime objects.
    """
    with open(file_name, 'r') as file:
        lines = file.readlines()

    datetime_list = []

    for i in range(0, count_times_wanted, 2):
        date_str = lines[i].strip()
        date_str = re.sub(r'\s+', ' ', date_str).strip()
        date_str_list = date_str.split(' ')
        date_time_str = lines[i + 1].strip() + ' ' + date_str_list[0] + ' ' + date_str_list[1] + ' ' + date_str_list[2]

        dt = datetime.strptime(date_time_str, '%Y %d %b %H:%M:%S')
        datetime_list.append(dt)

    return datetime_list

