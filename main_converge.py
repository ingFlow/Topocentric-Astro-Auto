from datetime import datetime
from pd_automate import EventType, AspectType
import aspects_implementation as asp
import json

class timesFileType:
    POLARIS = 0
    DATE_N_TIME = 1
    TIMES_ONLY = 2
    MANUAL_RECT = 3

''' 
  {"datetime": "2013-12-11T12:00:00", "event_type": "---"},
      {"datetime": "2018-02-19T12:00:00", "event_type": "--"},
      {"datetime": "2017-09-15T12:00:00", "event_type": "---"},
      {"datetime": "2021-07-10T12:00:00", "event_type": "---"},
  '''

'''datetime(1974, 6, 13, 22, 16, 16),
    datetime(1974, 6, 13, 20, 30, 32),
    datetime(1974, 6, 13, 22, 26, 8),
    datetime(1974, 6, 13, 22, 28, 8),
    datetime(1974, 6, 13, 22, 46, 40),
    datetime(1974, 6, 13, 23, 3, 20),
    datetime(1974, 6, 13, 23, 46, 24)'''

def convert_birth_data_json(file_to_write_str):
    dt_radix_start = datetime(1935,1,8, 2, 00, 00)
    dt_radix_end = datetime(1935,1,8, 2, 00, 00)
    dt_actual_dob = datetime(1935,1,8, 9, 21, 20)
    geopos = [34.25, -88.716666667, 85.0]
    list_of_events = [
        (datetime(1954,7,30, 12, 00, 00) ,EventType.SUCCESS,[34.25, -88.716666667, 85.0]),
        (datetime(1955,5,1, 12, 00, 00) ,EventType.TRAVEL_OVERSEAS_POSITIVE,[34.25, -88.716666667, 85.0]),
        (datetime(1956,1,28, 12, 00, 00) ,EventType.SUCCESS,[34.25, -88.716666667, 85.0]),
        (datetime(1956,9,9, 12, 00, 00) ,EventType.SUCCESS,[34.25, -88.716666667, 85.0]),
        (datetime(1958,3,24, 12, 00, 00) ,EventType.MOBILIZATION,[34.25, -88.716666667, 85.0]),
        (datetime(1958,8,14, 12, 00, 00) ,EventType.DEATH_MOTHER_GRAND,[34.25, -88.716666667, 85.0]),
        (datetime(1958,10,1, 12, 00, 00) ,EventType.TRAVEL_OVERSEAS_POSITIVE,[34.25, -88.716666667, 85.0]),
        (datetime(1959,6,1, 12, 00, 00) ,EventType.SUCCESS,[34.25, -88.716666667, 85.0]),
        (datetime(1960,3,5, 12, 00, 00) ,EventType.DEMOBILIZATION_RELEASE,[34.25, -88.716666667, 85.0]),
        (datetime(1967,5,1, 12, 00, 00) ,EventType.MARRIAGE_FOR_MALE,[34.25, -88.716666667, 85.0]),
        (datetime(1968,2,1, 12, 00, 00) ,EventType.BIRTH_DAUGHTER,[34.25, -88.716666667, 85.0]),
        (datetime(1972,8,15, 12, 00, 00) ,EventType.DIVORCE_SEPARATION,[34.25, -88.716666667, 85.0]),
        (datetime(1977,8,16, 12, 00, 00) ,EventType.DEATH,[34.25, -88.716666667, 85.0]),
        (datetime(1979,6,26, 12, 00, 00) ,EventType.DEATH_FATHER_GRAND,[34.25, -88.716666667, 85.0])    
    ]
    
    data = {
        "dt_radix_start": dt_radix_start.isoformat(),
        "dt_radix_end": dt_radix_end.isoformat(),
        "dt_actual_dob": dt_actual_dob.isoformat(),
        "geopos_natal": geopos,
        "list_of_events": [
            {"datetime": event[0].isoformat(), "event_type": EventType.get_name(event[1]), "geopos": event[2]} for event in list_of_events
        ]
    }

    with open(f"{file_to_write_str}.json", "a") as outfile:
        json.dump(data, outfile, indent=4)

def get_json_birth_data(filename):   
    with open(filename, 'r') as f:
        data = json.load(f)
    dt_radix_start = datetime.fromisoformat(data['dt_radix_start'])
    dt_radix_end = datetime.fromisoformat(data['dt_radix_end'])
    real_dob = datetime.fromisoformat(data['dt_actual_dob'])

    geopos_natal = data['geopos_natal']
    list_of_events = [
        (datetime.fromisoformat(event['datetime']), getattr(EventType, event['event_type']), event['geopos'])
        for event in data['list_of_events']
    ]
    return real_dob, dt_radix_start, dt_radix_end, geopos_natal, list_of_events

def pd_rect_grid_score_create(filename_birth_data, str_output_prefix, time_increment_seconds: int): 
    _, dt_radix_start, dt_radix_end, geopos, list_of_events = get_json_birth_data(filename_birth_data)

    level_aspects = AspectType.ANGLE_HOUSE_ANY_PLANET
    str_date = str_output_prefix
    techniques = [
    (asp.TechniqueType.PRIMARY_DIRECT, "_primaries")
    ]

    for technique, suffix in techniques:
        filename = f"{str_date}{dt_radix_end.strftime('%Y-%m-%d')}{suffix}"
        asp.generate_grid_angular_aspects(
            filename, dt_radix_start, dt_radix_end, time_increment_seconds, list_of_events, geopos, level_aspects, technique
        )
        asp.count_aspect_groups_txt(filename,False)
        asp.resetvars()  

def rect_ver_data_create(times_filename, times_type : timesFileType, birth_data_filename, prefix_data_str, count_times_wanted_pola_man=None):
    """prefix data str must be like: txt/26_10_24_IngTea_v3/26_10_24_"""
    real_dob, _, _, geopos, list_of_events = get_json_birth_data(birth_data_filename)

    if times_type == timesFileType.POLARIS:
        list_times_to_process = asp.process_polaris_times(times_filename,count_times_wanted_pola_man)
    elif times_type == timesFileType.DATE_N_TIME:
        list_times_to_process = asp.process_datetime_count_csv(times_filename)
        list_times_to_process = [datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') for date_str in list_times_to_process]    
    elif times_type == timesFileType.TIMES_ONLY:
        list_times_to_process = asp.process_time_count_csv(times_filename,real_dob,geopos)
    elif times_type == timesFileType.MANUAL_RECT:
        list_times_to_process = asp.process_manual_rect_csv(times_filename,real_dob,count_times_wanted_pola_man,geopos)
    
    str_date = prefix_data_str

    techniques = [
        (asp.TechniqueType.SECONDARY_DIRECT, "_second"),
        (asp.TechniqueType.PSSR, "_pssr"),
        (asp.TechniqueType.TRANSIT, "_trans"),
        (asp.TechniqueType.PRIMARY_DIRECT, "_primdir")
    ]

    for technique, suffix in techniques:
        filename = f"{str_date}{real_dob.strftime('%Y-%m-%d')}{suffix}"
        flag_count_moon = False
        if technique == asp.TechniqueType.PSSR:
            flag_count_moon = True
            level_aspects = AspectType.MOON_ANGLE_HOUSE_SECONDARY
        elif technique == asp.TechniqueType.TRANSIT:
            level_aspects = AspectType.ANGLE_SECONDARY
        elif technique == asp.TechniqueType.SECONDARY_DIRECT:
            flag_count_moon = True
            level_aspects = AspectType.MOON_ANGLE_HOUSE_SECONDARY
        elif technique == asp.TechniqueType.PRIMARY_DIRECT:
            level_aspects = AspectType.ANGLE_HOUSE_SECONDARY
        
        asp.generate_grid_times_manual(filename, list_times_to_process, list_of_events, geopos, level_aspects, technique)
        asp.count_extended_aspect_groups_txt(filename, technique)
        asp.resetvars()  

def other_techniques_from_times(times_filename, birth_data_filename, prefix_data_str, count_times_to_process=None):
    real_dob, _, dt_radix_end, geopos, list_of_events = get_json_birth_data(birth_data_filename)
    date_str = dt_radix_end.strftime('%d %B %Y')

    #list_times_to_process = asp.process_manual_rect_csv(times_filename, real_dob,count_times_to_process, i_timezone)
    list_times_to_process = asp.process_datetime_count_csv(times_filename)
    str_date = prefix_data_str

    techniques = [
        (asp.TechniqueType.SECONDARY_DIRECT, "_secondaries"),
        (asp.TechniqueType.PSSR, "_pssr"),
        (asp.TechniqueType.TRANSIT, "_transit"),
    ]

    for technique, suffix in techniques:
        filename = f"{str_date}{real_dob.strftime('%Y-%m-%d')}{suffix}"
        flag_pssr_count_moon = False
        if technique == asp.TechniqueType.PSSR:
            level_aspects = AspectType.MOON_ANGLE_HOUSE_PRIMARY
            flag_pssr_count_moon = True
        elif technique == asp.TechniqueType.TRANSIT:
            level_aspects = AspectType.ANGLE_PRIMARY
        elif technique == asp.TechniqueType.SECONDARY_DIRECT:
            level_aspects = AspectType.ANGLE_HOUSE_PRIMARY
           
        asp.generate_grid_times_manual(filename, list_times_to_process, list_of_events, geopos, level_aspects, technique)
        asp.count_aspect_groups_txt(filename, flag_pssr_count_moon)
        asp.resetvars()  

def count_pssr_moon_write(filename_write, filename_json, filename_polaris, no_times):
    _, _, _, geopos, list_of_events = get_json_birth_data(filename_json)
    list_times = asp.process_polaris_times(filename_polaris, no_times)
    asp.count_pssr_moon_from_times_events(filename_write,list_times,list_of_events,geopos)


#convert_birth_data_json('data_input/elvis presley')
#rect_ver_data_create('txt/19_10_24 IngTea rect.txt', timesFileType.POLARIS,'data_input/ing tea prim.json','txt/26_10_24_IngTea_v3/26_10_24_',70)
#count_pssr_moon_write('19_10_24_ing_tea_pssr_Pmoons_top50.csv','data_input/ing tea prim.json','txt/19_10_24 IngTea rect.txt', 50)
#count_pssr_moon_write('19_10_24_ing_tea_pssr_Pmoons_top30.csv','data_input/ing tea prim.json','txt/19_10_24 IngTea rect.txt', 30)
