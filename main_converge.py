from datetime import datetime, timedelta
import pd_automate as pd
import aspects_implementation as asp
import json

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
    dt_radix_start = datetime(1926, 4, 21, 20, 00, 00)
    dt_radix_end = datetime(1926, 4, 21, 20, 00, 00)
    dt_actual_dob = datetime(1926, 4, 21, 1, 12, 50)
    geopos = [51.526667, -0.008527778, 15.0]
    list_of_events = [
        (datetime(1930, 8, 21, 12, 00, 00),pd.EventType.BIRTH_SISTER),
        (datetime(1948, 11, 14, 12, 00, 00),pd.EventType.BIRTH_SON),
        (datetime(1950, 8, 15, 12, 00, 00),pd.EventType.DEATH_DAUGHTER)
    ]
    
    data = {
        "dt_radix_start": dt_radix_start.isoformat(),
        "dt_radix_end": dt_radix_end.isoformat(),
        "dt_actual_dob": dt_actual_dob.isoformat(),
        "geopos": geopos,
        "list_of_events": [
            {"datetime": event[0].isoformat(), "event_type": pd.EventType.get_name(event[1])} for event in list_of_events
        ]
    }

    with open(f"{file_to_write_str}.json", "w") as outfile:
        json.dump(data, outfile, indent=4)

def get_json_birth_data(filename):   
  with open(filename, 'r') as f:
      data = json.load(f)
  dt_radix_start = datetime.fromisoformat(data['dt_radix_start'])
  dt_radix_end = datetime.fromisoformat(data['dt_radix_end'])
  real_dob = datetime.fromisoformat(data['dt_actual_dob'])

  geopos_natal = data['geopos_natal']
  list_of_events = [
      (datetime.fromisoformat(event['datetime']), getattr(pd.EventType, event['event_type']), event['geopos'])
      for event in data['list_of_events']
  ]
  return real_dob, dt_radix_start, dt_radix_end, geopos_natal, list_of_events

def pd_rect_grid_score_create(filename_birth_data, str_output_prefix, time_increment_seconds: int): 
  _, dt_radix_start, dt_radix_end, geopos, list_of_events = get_json_birth_data(filename_birth_data)
  
  level_aspects = pd.AspectType.ANGLE_HOUSE_ANY_PLANET
  str_date = str_output_prefix
  techniques = [
      (asp.TechniqueType.PRIMARY_DIRECT, "_primaries")
  ]

  for technique, suffix in techniques:
      filename = f"{str_date}{dt_radix_end.strftime('%Y-%m-%d')}{suffix}"
      asp.generate_grid_angular_aspects(
          filename, dt_radix_start, dt_radix_end, time_increment_seconds, list_of_events, geopos, level_aspects, technique
      )
      asp.count_aspect_groups_txt(filename)
      asp.resetvars()  

def other_techniques_from_pd_rect(csv_filename, birth_data_filename, prefix_data_str, count_times_to_process, i_timezone):
    _, dt_radix_end, geopos, list_of_events = get_json_birth_data(birth_data_filename)
   
    file_path = csv_filename
    date_str = dt_radix_end.strftime('%d %B %Y')
 
    list_times_to_process = asp.process_csv(file_path, date_str,count_times_to_process, i_timezone)
    str_date = prefix_data_str

    techniques = [
        (asp.TechniqueType.SECONDARY_DIRECT, "_secondaries"),
        (asp.TechniqueType.PSSR, "_pssr"),
        (asp.TechniqueType.TRANSIT, "_transit"),
    ]

    for technique, suffix in techniques:
        filename = f"{str_date}{dt_radix_end.strftime('%Y-%m-%d')}{suffix}"
        flag_pssr_count_moon = False
        if technique == asp.TechniqueType.PSSR:
            level_aspects = pd.AspectType.MOON_ANGLE_HOUSE_PRIMARY
            flag_pssr_count_moon = True
        elif technique == asp.TechniqueType.TRANSIT:
            level_aspects = pd.AspectType.ANGLE_PRIMARY
        elif technique == asp.TechniqueType.SECONDARY_DIRECT:
            level_aspects = pd.AspectType.ANGLE_HOUSE_PRIMARY
           
        asp.generate_grid_times_manual(filename, list_times_to_process, list_of_events, geopos, level_aspects, technique)
        asp.count_aspect_groups_txt(filename, flag_pssr_count_moon)
        asp.resetvars()  

#pd_rect_grid_score_create('data_input/jacquiline onassis.json','9_11_ver2_',8)
#other_techniques_from_pd_rect('txt/9_9_ver3_sorted_planet_data.csv', 'data_input/jacquiline onassis.json', '9_14_ver1_', 100, -4)
convert_birth_data_json('data_input/queen elizabeth')