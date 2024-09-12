from datetime import datetime
import pd_automate as pd
import aspects_analysis
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

list_of_events = [
    (datetime(1949, 8, 15, 12, 00, 00),pd.EventType.TRAVEL_POSITIVE),
    (datetime(1952, 1, 21, 12, 00, 00),pd.EventType.MARRIAGE_FOR_FEMALE),
    (datetime(1953, 4, 18, 12, 00, 00),pd.EventType.MARRIAGE_FOR_FEMALE),
    (datetime(1953, 6, 25, 12, 00, 00),pd.EventType.MARRIAGE_FOR_FEMALE),
    (datetime(1953, 9, 12, 12, 00, 00),pd.EventType.MARRIAGE_FOR_FEMALE),
    (datetime(1956, 8, 23, 12, 00, 00),pd.EventType.DEATH),
    (datetime(1957, 8, 3, 12, 00, 00),pd.EventType.DEATH_FATHER_GRAND),
    (datetime(1957, 11, 27, 12, 00, 00),pd.EventType.BIRTH_DAUGHTER),
    (datetime(1958, 11, 4, 12, 00, 00),pd.EventType.SUCCESS),
    (datetime(1960, 11, 25, 12, 00, 00),pd.EventType.BIRTH_SON),
    (datetime(1963, 8, 7, 12, 00, 00),pd.EventType.BIRTH_SON),
    (datetime(1963, 8, 9, 12, 00, 00),pd.EventType.DEATH_SON),
    (datetime(1963, 11, 22, 12, 00, 00),pd.EventType.DEATH_HUSBAND),
    (datetime(1964, 6, 15, 12, 00, 00),pd.EventType.TRAVEL_NEGATIVE),
    (datetime(1957, 11, 15, 12, 00, 00),pd.EventType.TRAVEL_POSITIVE),
    (datetime(1968, 3, 15, 12, 00, 00),pd.EventType.TRAVEL_POSITIVE),
    (datetime(1968, 6, 5, 12, 00, 00),pd.EventType.DEATH),
    (datetime(1968, 10, 20, 12, 00, 00),pd.EventType.MARRIAGE_FOR_FEMALE),
    (datetime(1975, 3, 15, 12, 00, 00),pd.EventType.DEATH_HUSBAND),
    (datetime(1994, 5, 20, 12, 00, 00),pd.EventType.DEATH),
  ]

def main(): 
  with open('data_input/jacquiline onassis.json', 'r') as f:
      data = json.load(f)
  dt_radix_start = datetime.fromisoformat(data['dt_radix_start'])
  dt_radix_end = datetime.fromisoformat(data['dt_radix_end'])
  geopos = data['geopos']
  list_of_events = [
      (datetime.fromisoformat(event['datetime']), getattr(pd.EventType, event['event_type']))
      for event in data['list_of_events']
  ]
  '''(aspects_analysis.TechniqueType.SECONDARY_DIRECT, "_secondaries"),
      (aspects_analysis.TechniqueType.PSSR, "_pssr"),
      (aspects_analysis.TechniqueType.TRANSIT, "_transit"),'''
  level_aspects = pd.AspectType.ANGLE_HOUSE_ANY_PLANET
  time_increment = 8
  str_date = "9_11_ver2_"
  techniques = [
      (aspects_analysis.TechniqueType.PRIMARY_DIRECT, "_primaries")
  ]

  for technique, suffix in techniques:
      filename = f"{str_date}{dt_radix_end.strftime('%Y-%m-%d')}{suffix}"
      aspects_analysis.generate_grid_angular_aspects(
          filename, dt_radix_start, dt_radix_end, time_increment, list_of_events, geopos, level_aspects, technique
      )
      aspects_analysis.count_aspect_groups_txt(filename)
      aspects_analysis.resetvars()  

main()
