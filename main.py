import aspects_base as aspects
import astro_seek_read 
import pssr_automate as pssr
from datetime import datetime
import pd_automate as pd
import secondary_automate as secondary

ORB_TRANSIT = 1.15
ORB_PSSR = 0.24
TIMEZONE = 3

def transit_for_event_date(radix_date, event_date):
  str_append = ""
  rad_start_string, none = astro_seek_read.m_get_astro_chart_positions(radix_date.day, radix_date.month, radix_date.year, radix_date.hour,radix_date.minute, radix_date.second)

  check_string, none = astro_seek_read.m_get_astro_chart_positions(event_date.day, event_date.month, event_date.year, event_date.hour,event_date.minute, event_date.second)

  label = str(radix_date) + " for " + str(event_date) + '\n'
  str_append += aspects.m_aspects_between_two_sets_positions(rad_start_string.split(), check_string.split(), label, ORB_TRANSIT, house_check=True, process_type=aspects.ProcessType.TRANSIT)

  return str_append


#change timezone and orb here
def pssr_for_event_rad(radix_date, event_date):
  str_append = ""
  dates_to_check = pssr.m_auto_pssr\
  (radix_date.day, radix_date.month, radix_date.year, radix_date.hour,\
   radix_date.minute, radix_date.second, event_date.day, event_date.month,\
   event_date.year, event_date.hour, event_date.minute, event_date.second, TIMEZONE)

  rad_start_string, none = astro_seek_read.m_get_astro_chart_positions(radix_date.day, radix_date.month, radix_date.year, radix_date.hour,radix_date.minute, radix_date.second)
  
  start_positions = rad_start_string.split()

  counter = 1
  for date in dates_to_check:
    check_string, none = astro_seek_read.m_get_astro_chart_positions(date.day, date.month, date.year, date.hour,date.minute, date.second)
    check_positions = check_string.split()
    
    label = str(counter) + ') ' + str(radix_date) + " for " + str(event_date) + '\n'
    str_append += aspects.m_aspects_between_two_sets_positions(start_positions, check_positions, label, ORB_PSSR, house_check=True, process_type=aspects.ProcessType.PSSR)
    counter+=1

  return str_append

'''datetime(1994, 7, 2, 12, 00, 00),
    datetime(1997, 8, 13, 12, 00, 00),
    datetime(1997, 11, 16, 12, 00, 00),
    datetime(2000, 3, 11, 12, 00, 00),
    datetime(2021, 2, 20, 12, 00, 00),
    datetime(2013, 12, 11, 12, 00, 0'''

def process_multiple_events(radix_date, type_process):  
  str_output = ""
  list_of_events = [
    datetime(2014, 3, 24, 12, 00, 00),
    datetime(2018, 2, 19, 12, 00, 00),
    datetime(2013, 12, 11, 12, 00, 00),
    datetime(2017, 9, 15, 12, 00, 00),
    datetime(2021, 7, 10, 12, 00, 00),
    datetime(2021, 4, 6, 12, 00, 00),
    datetime(2022, 5, 25, 12, 00, 00),
    datetime(2022, 1, 3, 12, 00, 00)
  ]

  filename = ''
  if (type_process == aspects.ProcessType.PSSR):
    filename = 'pssr_'
    for event_date in list_of_events:
      print('processing event', str(event_date), 'for', str(radix_date))
      str_output += pssr_for_event_rad(radix_date, event_date)
  elif (type_process == aspects.ProcessType.TRANSIT):
    filename = 'transit_'
    for event_date in list_of_events:
      print('processing event', str(event_date), 'for', str(radix_date))
      prenatal_datetime = pssr.get_prenatal_trans_date(radix_date, event_date)
      str_output += transit_for_event_date(radix_date, event_date)
      str_output += transit_for_event_date(radix_date, prenatal_datetime)

  with open(f"{filename}{str(radix_date)}.txt", "a") as f:
    f.write(str_output)
    print(str_output)

'''datetime(1974, 6, 13, 22, 16, 16),
    datetime(1974, 6, 13, 20, 30, 32),
    datetime(1974, 6, 13, 22, 26, 8),
    datetime(1974, 6, 13, 22, 28, 8),
    datetime(1974, 6, 13, 22, 46, 40),
    datetime(1974, 6, 13, 23, 3, 20),
    datetime(1974, 6, 13, 23, 46, 24)'''

def main():
  dt_radix_start = datetime(1940, 10, 8, 23, 00, 00)
  dt_radix_end = datetime(1940, 10, 8, 23, 00, 8)
  geopos = [53.4, -2.9833333, 70.0]
  '''dt_radix = datetime(1889, 4, 16, 19, 40, 48)
  geopos = [51.48333, 0.001, 306]
  dt_event = datetime(1901, 5, 9, 12, 00, 00)'''

  list_of_events = [
    (datetime(1956, 7, 15, 12, 00, 00),pd.EventType.DEATH_MOTHER_GRAND),
    (datetime(1962, 8, 23, 12, 00, 00),pd.EventType.MARRIAGE_FOR_MALE),
    (datetime(1963, 4, 18, 12, 00, 00),pd.EventType.BIRTH_SON),
    (datetime(1964, 2, 6, 12, 00, 00),pd.EventType.SUCCESS),
    (datetime(1965, 6, 12, 12, 00, 00),pd.EventType.SUCCESS),
    (datetime(1967, 8, 26, 12, 00, 00),pd.EventType.DEATH),
    (datetime(1968, 11, 28, 12, 00, 00),pd.EventType.ARREST),
    (datetime(1969, 3, 20, 12, 00, 00),pd.EventType.MARRIAGE_FOR_MALE),
    (datetime(1970, 4, 15, 12, 00, 00),pd.EventType.LOSSES),
    (datetime(1972, 3, 6, 12, 00, 00),pd.EventType.LOSSES),
    (datetime(1974, 7, 18, 12, 00, 00),pd.EventType.LOSSES),
    (datetime(1975, 10, 9, 12, 00, 00),pd.EventType.BIRTH_SON),
    (datetime(1975, 1, 15, 12, 00, 00),pd.EventType.SUCCESS),
    (datetime(1976, 7, 27, 12, 00, 00),pd.EventType.TRAVEL_POSITIVE),
    (datetime(1980, 12, 8, 12, 00, 00),pd.EventType.ASSASINATION_SUICIDE)
  ]
  flag_pd_sec = False
  level_aspects = 2
  time_increment = 8
  if flag_pd_sec:
    filename = f"{dt_radix_end.strftime('%Y-%m-%d')}_primaries.txt"
  else:
    filename = f"{dt_radix_end.strftime('%Y-%m-%d')}_secondaries.txt"

  pd.generate_grid_angular_aspects(filename, dt_radix_start, dt_radix_end, time_increment, list_of_events, geopos, level_aspects, flag_pd_sec)
  pd.count_aspect_groups_txt(filename)

  flag_pd_sec = True
  if flag_pd_sec:
    filename = f"{dt_radix_end.strftime('%Y-%m-%d')}_primaries.txt"
  else:
    filename = f"{dt_radix_end.strftime('%Y-%m-%d')}_secondaries.txt"

  pd.generate_grid_angular_aspects(filename, dt_radix_start, dt_radix_end, time_increment, list_of_events, geopos, level_aspects, flag_pd_sec)
  pd.count_aspect_groups_txt(filename)

main()
