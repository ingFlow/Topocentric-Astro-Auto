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

def main_trans_pssr():
  dates = [
    datetime(2000, 3, 11, 12, 14, 32),
    datetime(2000, 3, 11, 13, 28, 48),
    datetime(2000, 3, 11, 10, 27, 44),
    datetime(2000, 3, 11, 15, 4, 0),
    datetime(2000, 3, 11, 15, 41, 4),
    datetime(2000, 3, 11, 13, 12, 56),
    datetime(2000, 3, 11, 11, 45, 28),
    datetime(2000, 3, 11, 10, 0, 16),
    datetime(2000, 3, 11, 15, 49, 44),
    datetime(2000, 3, 11, 10, 46, 16),
    datetime(2000, 3, 11, 14, 32, 8),
    datetime(2000, 3, 11, 16, 9, 12),
    datetime(2000, 3, 11, 16, 26, 56)
  ]
  #for date in dates:
    #process_multiple_events(date, aspects.ProcessType.TRANSIT)
    #process_multiple_events(date, aspects.ProcessType.PSSR)

def main():
  dt_radix = datetime(1940, 10, 9, 17, 24, 17)
  geopos = [53.4, -2.9833333, 70.0]
  '''dt_radix = datetime(1889, 4, 16, 19, 40, 48)
  geopos = [51.48333, 0.001, 306]
  dt_event = datetime(1901, 5, 9, 12, 00, 00)'''

  list_of_events = [
    datetime(1956, 7, 15, 12, 00, 00),
    datetime(1962, 8, 23, 12, 00, 00),
    datetime(1963, 4, 18, 12, 00, 00),
    datetime(1964, 2, 6, 12, 00, 00),
    datetime(1965, 6, 12, 12, 00, 00),
    datetime(1967, 8, 26, 12, 00, 00),
    datetime(1968, 11, 28, 12, 00, 00),
    datetime(1969, 3, 20, 12, 00, 00),
    datetime(1970, 4, 15, 12, 00, 00),
    datetime(1972, 3, 6, 12, 00, 00),
    datetime(1974, 7, 18, 12, 00, 00),
    datetime(1975, 1, 15, 12, 00, 00),
    datetime(1975, 10, 9, 12, 00, 00),
    datetime(1976, 7, 27, 12, 00, 00),
    datetime(1980, 12, 8, 12, 00, 00)
  ]
  #for dt_event in list_of_events:
    #pd.pd_automated(pssr.dt_gregorian_to_julian(dt_radix), pssr.dt_gregorian_to_julian(dt_event), geopos)
  str = "(MC,55.552,(r)) (Saturn,325.600,(d)) (square,3')\n(AC,176.030,(r)) (Mars,220.994,(d)) (45-semisquare,2')\n(Pluto,124.188,(r)) (Venus,184.231,(d)) (sextile,3')\n(Neptune,190.583,(r)) (DC,325.600,(d)) (135-sesquisquare,1')\n(Uranus,320.168,(r)) (MC,290.150,(d)) (30-semisextile,1')"
  print(pd.count_all_acceptable_angles(1, str))

  #for dt_event in list_of_events:
  ''''''
  #econdary.secondary_auto(pssr.dt_gregorian_to_julian(dt_radix), pssr.dt_gregorian_to_julian(dt_event), geopos[0], geopos[1], 0.534)

main()