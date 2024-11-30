import pd_automate
import datetime 
import julian
import swisseph as swe
import secondary_automate
import pssr_swiss_auto as pssr_auto
import transit_swiss_auto as transit_auto
import sra_auto
import pandas as pd
import lunar_auto as lunar
import re
import os
import csv
from timezonefinder import TimezoneFinder
import pytz
from constants import calc_planets_pof_houses_labelled, PLANETS
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
    
def append_grid_acceptable_angles(list_dt_events, jd_radix : julian, geopos_natal: list[3]):
    formatted_datetime = julian.from_jd(jd_radix).strftime("%Y-%m-%d %H:%M:%S")
    temp_list_event = [formatted_datetime] 
    count = 0
    
    rad_houses_info = swe.houses(jd_radix, geopos_natal[0], geopos_natal[1], b'T')
    rad_planets_equatorial = pd_automate.calc_rad_planets_equatorial(jd_radix)
    rad_planets_pof_houses_labelled = calc_planets_pof_houses_labelled(jd_radix, geopos_natal)
    e = calculate_obliquity(jd_radix)

    event_index = 0
    for dt_event, event_id, geopos in list_dt_events:
        if date_technique == TechniqueType.PRIMARY_DIRECT:
            pd_auto_obj  = pd_automate.PD_Automate(jd_radix, julian.to_jd(dt_event), geopos_natal, rad_planets_pof_houses_labelled, rad_planets_equatorial, rad_houses_info, e)
            str_rad_dir_aspects, str_rad_conv_aspects = pd_auto_obj.get_aspects_str()
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects   
        elif date_technique == TechniqueType.SECONDARY_DIRECT:
            secondary_obj = secondary_automate.Secondary_Auto(jd_radix, julian.to_jd(dt_event), geopos_natal[0], geopos_natal[1], e, rad_houses_info[1][2], rad_planets_pof_houses_labelled)
            str_rad_n_prog_aspects, str_rad_n_reg_aspects = secondary_obj.get_str_aspects()
            str_all_directed_aspects = str_rad_n_prog_aspects + '\n' + str_rad_n_reg_aspects
        elif date_technique == TechniqueType.PSSR:
            pssr_obj = pssr_auto.PSSR_Auto(julian.from_jd(jd_radix), dt_event, rad_planets_pof_houses_labelled)
            str_rad_dir_aspects, str_rad_conv_aspects = pssr_obj.get_str_aspects()
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects 
        elif date_technique == TechniqueType.TRANSIT:
            transit_obj = transit_auto.Transit_Auto(jd_radix, julian.to_jd(dt_event), geopos, rad_planets_pof_houses_labelled)
            str_rad_dir_aspects, str_rad_conv_aspects = transit_obj.get_str_aspects()
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects 
        elif date_technique == TechniqueType.SRA:
            sra_auto_obj = sra_auto.SRA_Auto(julian.from_jd(jd_radix), dt_event, geopos_natal,rad_planets_pof_houses_labelled)
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

def categorize_aspect(first, second, aspect):
    conj_asp = ['conjunction', 'opposition']
    maj_asp = ['trine', 'sextile', 'square']
    ANGLES = ['H1', 'H4', 'H7', 'H10']

    if first in ANGLES and second in PLANETS :
        if aspect in conj_asp:
            return 'p_a_conj'
        elif aspect in maj_asp:
            return 'p_a_maj'
        else:
            return 'p_a_min'
    elif second in ANGLES and first in PLANETS:
        if aspect in conj_asp:
            return 'a_p_conj'
        elif aspect in maj_asp:
            return 'a_p_maj'
        else:
            return 'a_p_min'
    elif first.startswith('H') and second in PLANETS: #the other angle to house already evaluated so if its still H its not an angle
        if aspect in conj_asp:
            return 'p_h_conj'
        elif aspect in maj_asp:
            return 'p_h_maj'
        else:
            return 'p_h_min'
    elif second.startswith('H') and first in PLANETS: 
        if aspect in conj_asp:
            return 'h_p_conj'
        elif aspect in maj_asp:
            return 'h_p_maj'
        else:
            return 'h_p_min'
    elif first in PLANETS and second == 'Moon':
        if aspect in conj_asp:
            return 'mon_p_conj'
        elif aspect in maj_asp:
            return 'mon_p_maj'
        else:
            return 'mon_p_min'
    else:
        return None

def count_extended_aspect_groups_txt(filename, technique):
    aspect_categories = {
        'p_a_conj': 0,
        'p_a_maj': 0,
        'p_a_allm': 0,
        'p_a_min': 0,
        'a_p_conj': 0,
        'a_p_maj': 0,
        'a_p_allm': 0,
        'a_p_min': 0,
        'p_h_conj': 0,
        'p_h_maj': 0,
        'p_h_allm': 0,
        'p_h_min': 0,
        'h_p_conj': 0,
        'h_p_maj': 0,
        'h_p_allm': 0,
        'h_p_min': 0,
        'mon_p_conj': 0,
        'mon_p_maj': 0,
        'mon_p_allm': 0,
        'mon_p_min': 0,
        'e': 0,
    }
    results = []
    flag_1st_row = True

    with open(f"{filename}.txt", 'r') as infile:
        for row in infile:
            if flag_1st_row:
                flag_1st_row = False
            else:
                parts = eval(row.strip())
                time = parts[0]
                aspects = parts[1:-1]
                count_total = parts[-1]
                counts = {
                    'time': time
                }
                counts.update(aspect_categories.copy())  #Reset counts

                for aspect in aspects: 
                    if aspect.isdigit():
                        counts['e'] += 1
                    else:
                        aspects = aspect.split('\n')  # Split multiple aspects
                        for a in aspects:
                            parts = a.strip().strip('()').split(') (')
                            if len(parts) == 3:
                                first = parts[0].split(',')[0]  # Get the first planet info
                                second = parts[1].split(',')[0]  # Get the second planet info
                                asp_type = parts[2].split(',')[0] #Is it conjunction or quincunx etc.
                                category = categorize_aspect(first, second, asp_type)
                                if category:
                                    counts[category] += 1
                counts.update({'total_count':count_total})
                counts['p_a_allm'] = counts['p_a_conj'] + counts['p_a_maj']
                counts['a_p_allm'] = counts['a_p_conj'] + counts['a_p_maj']
                counts['p_h_allm'] = counts['p_h_conj'] + counts['p_h_maj']
                counts['h_p_allm'] = counts['h_p_conj'] + counts['h_p_maj']
                counts['mon_p_allm'] = counts['mon_p_conj'] + counts['mon_p_maj']
                counts['all_conj'] = counts['p_a_conj'] + counts['a_p_conj'] + counts['p_h_conj'] + counts['h_p_conj'] + counts['mon_p_conj']
                counts['p_a_mon_conj'] = counts['p_a_conj'] + counts['mon_p_conj']
                counts['a_p_p_a_conj'] = counts['a_p_conj'] + counts['p_a_conj']    
                counts['all_maj'] = counts['p_h_maj'] + counts['p_a_maj'] + counts['mon_p_maj'] + counts['a_p_maj'] + counts['h_p_maj']

                results.append(counts) 

    with open(f"{filename}COUNT.txt", 'w') as f:
        for index, count in enumerate(results):
            if technique == TechniqueType.PRIMARY_DIRECT:
                selected_categories = ['time', 'p_a_conj', 'p_a_maj', 'p_a_allm', 'p_a_min', 'a_p_conj', 'a_p_maj', 'a_p_allm', 'a_p_min', 'p_h_conj', 'p_h_maj', 'p_h_allm', 'p_h_min', 'h_p_conj', 'h_p_maj', 'h_p_allm', 'h_p_min', 'e', 'all_conj', 'all_maj', 'a_p_p_a_conj']
            elif technique == TechniqueType.SECONDARY_DIRECT:
                selected_categories = ['time', 'p_a_conj', 'p_a_maj', 'p_a_allm', 'p_a_min', 'a_p_conj', 'a_p_maj', 'a_p_allm', 'a_p_min', 'p_h_conj', 'p_h_maj', 'p_h_allm', 'p_h_min', 'h_p_conj', 'h_p_maj', 'h_p_allm', 'h_p_min', 'mon_p_conj', 'mon_p_maj', 'mon_p_allm', 'mon_p_min', 'e', 'all_maj', 'all_conj']
            elif technique == TechniqueType.PSSR:
                selected_categories = ['time', 'p_a_conj', 'p_a_maj', 'p_a_allm', 'p_a_min', 'p_h_conj', 'p_h_maj', 'p_h_allm', 'p_h_min', 'mon_p_conj', 'mon_p_maj', 'mon_p_allm', 'mon_p_min', 'e', 'all_conj', 'all_maj', 'p_a_mon_conj']
            elif technique == TechniqueType.TRANSIT:
                selected_categories = ['time', 'p_a_allm', 'p_a_min', 'e', 'p_a_maj', 'p_a_conj']

            filtered_counts = {key: count[key] for key in selected_categories if key in count}
            f.write(f"Row {index + 1}: {filtered_counts}\n")

def count_aspect_groups_txt(filename, flag_count_moon):
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
                            if (flag_count_moon and (')) (Moon' in asp)):
                                moon_conj_opp_count += 1
                            opp_conj_count += 1
                        elif ('square' in asp) or ('sextile' in asp) or ('trine' in asp):
                            if (flag_count_moon and (')) (Moon' in asp)):
                                moon_sqr_tri_sext_count += 1
                            sqr_tri_sext_count += 1
                        
            if flag_count_moon:
                results.append([f"{time}, {count}, opp-conj: {opp_conj_count}, sqr-tri-sext: {sqr_tri_sext_count}, major: {sqr_tri_sext_count+opp_conj_count}, minor: {minor_count}, moon-opp-conj: {moon_conj_opp_count}, moon-sqr-tri-sext: {moon_sqr_tri_sext_count}, empty: {empty_event_count}"])                
            else:
                results.append([f"{time}, {count}, opp-conj: {opp_conj_count}, sqr-tri-sext: {sqr_tri_sext_count}, major: {sqr_tri_sext_count+opp_conj_count}, minor: {minor_count}, empty: {empty_event_count}"])                
    print(results)

    with open(f"{filename}COUNT.txt", 'w') as outfile:
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
    
    directory = os.path.dirname(filename)
    os.makedirs(directory, exist_ok=True)

    with open(f"{filename}.txt", "w") as file:
        for time in grid_aspects:
            file.write(f"{str(time)}\n")

from datetime import timedelta

def add_timezone_to_24_hours(timezone):
    base_time = timedelta(hours=24)
    adjusted_time = base_time + timedelta(hours=timezone)
    result_hours = adjusted_time.seconds // 3600 % 24
    
    return result_hours

def process_manual_rect_csv(file_path, dt_bday, count_times_wanted, geopos):
    """end date is day of birth 
    timezone is whatever you need to add to UT to get the local time"""
    i_timezone = get_timezone_from_pos(geopos)
    df = pd.read_csv(file_path)
    times = df['Time'][:count_times_wanted].tolist()
    
    datetime_list = get_list_datetime_from_times(times, dt_bday, i_timezone)
    
    return datetime_list

def get_list_datetime_from_times(str_times, dt_bday, i_timezone):
    datetime_list = []

    for time_str in str_times:
        time_obj = datetime.datetime.strptime(time_str, '%H:%M:%S')
        
        if time_obj.hour < add_timezone_to_24_hours(i_timezone):
            if i_timezone <= 0:
                datetime_obj = datetime.datetime.combine(dt_bday, time_obj.time())
            else: 
                datetime_obj = datetime.datetime.combine(dt_bday + timedelta(days=1), time_obj.time())
        else:
            if i_timezone <= 0:
                datetime_obj = datetime.datetime.combine(dt_bday - timedelta(days=1), time_obj.time())
            else:
                datetime_obj = datetime.datetime.combine(dt_bday, time_obj.time())
    
        datetime_list.append(datetime_obj)
    
    return datetime_list

def sort_polaris_times(file_name, file_write＿name, count_times_wanted, threshold=None):
    '''
    created new file with polaris times sorted according to A value the if you give threshold
    removes the lines that do not have enough A points
    '''
    line_count = 0
    with open(file_name, 'r') as file:
        for line in file:
            line_count += 1
    if count_times_wanted > (line_count/2):
        print('Not enough times for that count...')
        count_times_wanted = 50 #assume polaris will always give over 50 peaks?
        return 

    with open(file_name, 'r') as file:
        lines = file.readlines()

    valid_lines = [line for line in lines if len(line.split()) > 3]
    non_valid_lines = [line for line in lines if len(line.split()) <= 3]
    year = non_valid_lines[0].strip()

    sorted_lines = sorted(valid＿lines, key=lambda x: int(x.split()[4]), reverse=True)
    #sorted_lines = sorted(valid_lines, key=lambda x: int(x.split()[4]) + int(x.split()[5]), reverse=True)

    filtered_lines = [
        line.strip()
        for line in sorted_lines
        if len(line.split()) > 5 and int(line.split()[4]) >= threshold
    ]
    filtered_lines = ["\t" + line.strip() + f"\n\t{year}" for line in filtered_lines]

    with open(file_write_name, 'w')  as file:
        for line in filtered_lines:
            file.write(line + '\n')

    return

def process_polaris_times(file_name, count_times_wanted):
    """Processes a text file with date and time entries.
    
    Args:
        file_path (str): Path to the text file.
        count_times_wanted (int): Number of times to process.
        i_timezone (int): Timezone offset to apply.

    Returns:
        List[datetime]: A list of datetime objects.
    """
    line_count = 0
    with open(file_name, 'r') as file:
        for line in file:
            line_count += 1
    if count_times_wanted > (line_count/2):
        print('Not enough times for that count...')
        return 

    with open(file_name, 'r') as file:
        lines = file.readlines()

    datetime_list = []

    for i in range(0, count_times_wanted*2, 2):
        date_str = lines[i].strip()
        date_str = re.sub(r'\s+', ' ', date_str).strip()
        date_str_list = date_str.split(' ')
        date_time_str = lines[i + 1].strip() + ' ' + date_str_list[0] + ' ' + date_str_list[1] + ' ' + date_str_list[2]

        dt = datetime.datetime.strptime(date_time_str, '%Y %d %b %H:%M:%S')
        datetime_list.append(dt)

    return datetime_list

def count_pssr_moon_from_times_events(filename_write, list_datetimes: list, events_list :list, geopos):
    count_array = [('DateTime','count')]
    aspect_type = pd_automate.AspectType.MOON_PRIMARY

    for dtime in list_datetimes:
        count_moon_conj_opp = 0
        for dt_event, event_id, _ in events_list:
            pssr_obj = pssr_auto.PSSR_Auto(dtime, dt_event, None, geopos)
            str_rad_dir_aspects, str_rad_conv_aspects = pssr_obj.get_str_aspects()
            str_all_directed_aspects = str_rad_dir_aspects + str_rad_conv_aspects 
            _, str_acceptable_aspects = pd_automate.count_event_acceptable_aspects(event_id, str_all_directed_aspects, 0, aspect_type)
            list_aspects = str_acceptable_aspects.split('\n')
            temp_arr = []
            for str_aspect in list_aspects:
                try:
                    if pd_automate.is_aspect_conj_opp(str_aspect):
                        temp_arr.append(str_aspect)
                except:
                    pass
            list_aspects = temp_arr
            count_moon_conj_opp += len(list_aspects)
        count_array.append((dtime,count_moon_conj_opp))

    count_array = [count_array[0]] + sorted(count_array[1:], key=lambda x: x[1], reverse=True)

    with open(filename_write, mode='w', newline='') as file:
        writer_csv = csv.writer(file)
        for item in count_array:
            writer_csv.writerow([item[0].strftime('%Y-%m-%d %H:%M:%S') if isinstance(item[0], datetime.datetime) else item[0], item[1]])

def process_datetime_count_csv(filename_read):
    datetime_list = []

    with open(filename_read, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        
        for row in reader:
            dt = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
            datetime_list.append(row[0])

    return datetime_list

def process_time_count_csv(filename_read, dt_bday, geopos):
    time_list = []

    i_timezone = get_timezone_from_pos(geopos)

    with open(filename_read, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        
        for row in reader:
            time_list.append(row[0])

    datetime_list = get_list_datetime_from_times(time_list, dt_bday, i_timezone)

    return datetime_list

def get_timezone_from_pos(geopos):
    tf = TimezoneFinder()
    geo_lat = geopos[0]
    geo_long = geopos[1]
    timezone_name = tf.timezone_at(lat=geo_lat, lng=geo_long)
    timezone = pytz.timezone(timezone_name)
    now = datetime.datetime.now(timezone)
    utc_offset = now.utcoffset().total_seconds() / 3600

    return utc_offset

def delete_rows_below_threshold_counttxt(threshold, file_name): 
    with open(file_name, 'r') as file:
        rows = file.readlines()

    filtered_rows = []
    for row in rows:
        start_index = row.find('{')
        end_index = row.rfind('}')
        if start_index != -1 and end_index != -1:
            row_dict = eval(row[start_index:end_index + 1])
            last_value = list(row_dict.values())[-1]
            
            if isinstance(last_value, (int, float)) and last_value >= threshold:
                filtered_rows.append((last_value, row))

    filtered_rows.sort(reverse=True, key=lambda x: x[0])
    sorted_rows = [row[1] for row in filtered_rows]

    with open(file_name, 'w') as file:
        file.writelines(sorted_rows)

    

#sort_polaris_times('data_times/bin k rect.txt', 'data_times/bin k sorted max a 1 rect.txt',49, 1)
delete_rows_below_threshold_counttxt(8,'data_rect/30_11_24_Ingtea_v1/30_11_24_2000-03-11_pssrCOUNT.txt')