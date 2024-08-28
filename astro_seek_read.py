from os import write
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

ORDER_PLANETS = ['ASC', 'MC', 'Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Node', 'Lilith', 'Chiron', 'Fortune', 'Vertex']



def construct_birthchart_url(params):
    day, month, year, hour, minute, second = params
    '''base_url = "https://horoscopes.astro-seek.com/calculate-birth-chart-horoscope-online/"
    url = (f"{base_url}?send_calculation=1&poslat_rozbor=ano&narozeni_den={day}&"
           f"narozeni_mesic={month}&narozeni_rok={year}&narozeni_hodina={hour}&"
           f"narozeni_minuta={minute}&narozeni_sekunda={second}&house_system=topocentric&"
           f"narozeni_sirka_smer=1&narozeni_sirka_stupne=4&narozeni_sirka_minuty=3&"
           f"narozeni_delka_smer=0&narozeni_delka_stupne=39&narozeni_delka_minuty=40&"
           f"narozeni_timezone_form=auto&narozeni_timezone_dst_form=auto&"
           f"narozeni_city=Johannesburg%2C+South+Africa&narozeni_mesto_hidden=Johannesburg&"
           f"narozeni_stat_hidden=ZA&narozeni_podstat_kratky_hidden=&narozeni_podstat_kratky_hidden="
           f"&narozeni_podstat2_kratky_hidden=&"
           f"narozeni_podstat3_kratky_hidden=&hid_fortune=1&hid_chiron=1&"
           f"hid_lilith=1&hid_uzel=1&hid_fortune_check=on&hid_vertex_check=on&"
           f"hid_chiron_check=on&hid_lilith_check=on&hid_uzel_check=on&nick=&&tolerance=1")'''
    
    url_mombasa = f"https://horoscopes.astro-seek.com/calculate-birth-chart-horoscope-online/?input_natal=1&send_calculation=1&narozeni_den={day}&narozeni_mesic={month}&narozeni_rok={year}&narozeni_hodina={hour}&narozeni_minuta={minute}&narozeni_sekunda={second}&narozeni_city=Mombasa%2C+Kenya&narozeni_mesto_hidden=Mombasa&narozeni_stat_hidden=KE&narozeni_podstat_kratky_hidden=Mombasa+County&narozeni_sirka_stupne=4&narozeni_sirka_minuty=3&narozeni_sirka_smer=1&narozeni_delka_stupne=39&narozeni_delka_minuty=40&narozeni_delka_smer=0&narozeni_timezone_form=auto&narozeni_timezone_dst_form=auto&house_system=topocentric&hid_fortune=1&hid_fortune_check=on&hid_vertex=1&hid_vertex_check=on&hid_chiron=1&hid_chiron_check=on&hid_lilith=1&hid_lilith_check=on&hid_uzel=1&hid_uzel_check=on&tolerance=1&aya=&tolerance_paral=1.2&zmena_nastaveni=1&aktivni_tab=&hide_aspects=0&dominanta_metoda=1&dominanta_rulership=1#tabs_redraw"

    url_joburg = f"https://horoscopes.astro-seek.com/calculate-birth-chart-horoscope-online/?input_natal=1&send_calculation=1&narozeni_den={day}&narozeni_mesic={month}&narozeni_rok={year}&narozeni_hodina={hour}&narozeni_minuta={minute}&narozeni_sekunda={second}&narozeni_city=Johannesburg%2C+South+Africa&narozeni_mesto_hidden=Johannesburg&narozeni_stat_hidden=ZA&narozeni_podstat_kratky_hidden=&narozeni_sirka_stupne=26&narozeni_sirka_minuty=12&narozeni_sirka_smer=1&narozeni_delka_stupne=28&narozeni_delka_minuty=3&narozeni_delka_smer=0&narozeni_timezone_form=auto&narozeni_timezone_dst_form=auto&house_system=topocentric&hid_fortune=1&hid_fortune_check=on&hid_vertex=1&hid_vertex_check=on&hid_chiron=1&hid_chiron_check=on&hid_lilith=1&hid_lilith_check=on&hid_uzel=1&hid_uzel_check=on&tolerance=1&aya=&tolerance_paral=1.2&zmena_nastaveni=1&aktivni_tab=&hide_aspects=0&dominanta_metoda=1&dominanta_rulership=1#tabs_redraw"

    return url_mombasa

def construct_ephemeris_url(params):
    month,year = params
    base_url = "https://horoscopes.astro-seek.com/"
    url = (f"{base_url}calculate-astrology-ephemeris-{month}-{year}/"
           f"?table=&bg_0=&aya=fagan&presnost=1&barva=p&uzel_true=&lilith_true=")
    
    return url

def construct_sunsearch_url(params):
    degrees, minutes, seconds, sign, year = params
    base_url = "https://horoscopes.astro-seek.com/calculate-planet-ingresses-and-particular-degree-returns/?"
    url = (f"{base_url}planeta_navrat_en=sun&znameni_stupen={degrees}&znameni_minuta={minutes}"
          f"&znameni_sekunda={seconds}&znameni_navrat_en={sign}&ingres_narozeni_rok={year}&aya=")
    
    return url


def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text

def extract_planet_positions(html):
    '''returns a string with the planet sign and degree and a dictionary with planet, longitude and speed'''
    soup = BeautifulSoup(html, 'html.parser')

    textarea = soup.find('textarea', {'id': 'txtarea1'})
    div_positions = soup.find('div', {'id': 'tab5'})

    textarea_content = textarea.get_text(strip=True) if textarea else "No content found"

    # Extract planet data
    rows = div_positions.find_all('tr')
    planet_data = {}
    temp_speed = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 6:  # Ensure there are enough columns
            planet = cells[1].get_text(strip=True)
            longitude = cells[2].get_text(strip=True)
            speed = cells[-1].get_text(strip=True)
            planet_data[planet] = {'longitude': longitude, 'speed': speed}
            temp_speed.append(speed)

    text_list = textarea_content.split()
    counte = 0
    for text in text_list:
        text_split = text.split(',')
        planet = text_split[0] + ':'
        deg_min = text_split[2][:-1]     
        try:
            speed = planet_data[planet]['speed']
            text += f",{speed}"
        except KeyError:
            speed = '-'
        text = text_split[0] + ',' + text_split[1] + ',' + deg_min + ',' + speed
        speed = ''
        text_list[counte] = text
        counte += 1

    text_return = '\n'.join(text_list)
        
    return text_return, planet_data

def extract_ephemeris_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    td_element = soup.find('td', style=lambda value: value and 'background: #DDDDDD' in value)
    if td_element:
        # Extract the text from the <td> element
        span_text = td_element.get_text(strip=True)

        match = re.search(r'Ayanamsha: Fagan-Bradley', span_text)

        if match:
            match = re.search(r'(\d+)  (\d+)   ', span_text)
            degrees = match.group(1) if match else None
            minutes = match.group(2) if match else None

            return degrees, minutes
        else:
            print("Degree information not found.")
    else:
        print("Table with specified style not found.")

def extract_sunsearch_time(html):
    soup = BeautifulSoup(html, 'html.parser')
    td_element = soup.find('td', style=lambda value: value and 'width: 130px;  padding: 4px 10px 4px 5px; text-align: right;' in value)
    
    if td_element:
        return td_element.get_text(strip=True)
    else:
        print("No <td> element found with the specified style.")

def extract_primary_dir_data(html):
    soup = BeautifulSoup(html, 'html.parser')
        
    textarea = soup.find('textarea', {'id': 'txtarea1'})
    div_positions = soup.find('div', {'id': 'tab5'})

    textarea_content = textarea.get_text(strip=True) if textarea else "No content found"

    # Extract planet data
    rows = div_positions.find_all('tr')
    planet_data = {}
    temp_speed = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 6:  # Ensure there are enough columns
            planet = cells[1].get_text(strip=True)
            longitude = cells[2].get_text(strip=True)
            speed = cells[-1].get_text(strip=True)
            planet_data[planet] = {'longitude': longitude, 'speed': speed}
            temp_speed.append(speed)

    text_list = textarea_content.split()
    counte = 0
    for text in text_list:
        text_split = text.split(',')
        planet = text_split[0] + ':'
        deg_min = text_split[2][:-1]     
        try:
            speed = planet_data[planet]['speed']
            text += f",{speed}"
        except KeyError:
            speed = '-'
        text = text_split[0] + ',' + text_split[1] + ',' + deg_min + ',' + speed
        speed = ''
        text_list[counte] = text
        counte += 1

    text_return = '\n'.join(text_list)



def change_timezone(params, timezone_offset):
    day, month, year, hour, minute, second = params
    gmt_time = datetime(year, month, day, hour, minute, second)
    local_time = gmt_time + timedelta(hours=timezone_offset)
    return local_time

def convert_str_date_tuple(date_str):
    # Split the date string into date and time components
    second_comma_index = date_str.find(",", date_str.find(",") + 1)
    date_part = date_str[:second_comma_index]
    time_part = date_str[second_comma_index + 1:].strip() 
    month_day, year = date_part.split(", ")
    month, day = month_day.split(" ")
    hour, minute = time_part.split(":")
    month_number = datetime.strptime(month, "%b").month
    
    day = int(day)
    month_number = int(month_number)
    year = int(year)
    hour = int(hour)
    minute = int(minute)
    #TODO remember if seconds changes look here
    second = 0

    return (day, month_number, year, hour, minute, second)
    
def m_get_sun_longitude(detailed_planet_data):
    sun_long = detailed_planet_data['Sun:']['longitude']
    return sun_long

def m_get_GEO_LAT(event_date):
    birthchart_url = construct_birthchart_url((event_date.day, event_date.month, event_date.year, event_date.hour, event_date.minute, event_date.second))
    html = fetch_html(birthchart_url)

    extract_primary_dir_data(html)
    
    soup = BeautifulSoup(html, 'html.parser')

    #GEO_LAT
    div_vlevo = soup.find('div', class_='ascendent-vypocet-vlevo', text='Latitude, Longitude:')
    div_vpravo = div_vlevo.find_next_sibling('div', class_='ascendent-vypocet-vpravo')
    latitude_text = div_vpravo.find('em').text

    degrees = int(latitude_text.split('  ')[0])
    minutes = int(latitude_text.split('  ')[1].split('\'')[0])
    direction = latitude_text.split('\'')[1]
    
    GEO_LAT = degrees + (minutes / 60)
    if direction == 'S':
      GEO_LAT *= -1

    return GEO_LAT

def m_get_LST(event_date):
    birthchart_url = construct_birthchart_url((event_date.day, event_date.month, event_date.year, event_date.hour, event_date.minute, event_date.second))
    html = fetch_html(birthchart_url)

    extract_primary_dir_data(html)

    soup = BeautifulSoup(html, 'html.parser')

    #LST
    divs_vlevo = soup.find_all('div', class_='ascendent-vypocet-vlevo')
    LST = ''
   
    for div_vlevo in divs_vlevo:
        if "Local Sidereal Time" in div_vlevo.text:
            div_time = div_vlevo.find_next_sibling('div', class_='ascendent-vypocet-vpravo')
            LST = div_time.find('em').text

    return datetime.strptime(LST, "%H:%M:%S").time()

def m_get_RAMC_RA_DECL_point(event_date, point):
    birthchart_url = construct_birthchart_url((event_date.day, event_date.month, event_date.year, event_date.hour, event_date.minute, event_date.second))
    html = fetch_html(birthchart_url)

    extract_primary_dir_data(html)
    soup = BeautifulSoup(html, 'html.parser')

    div = soup.find('div', id='tab5')
    RAMC, RA, DECL = 0, 0, 0

    if div:
        table = div.find('table')

        if table:
            #+2 to skip the headers of the table
            rows = table.find_all('tr')[2:]
            target_row = ORDER_PLANETS.index(point) + 2
            target_row_element = table.find_all('tr')[target_row]
            cells = target_row_element.find_all('td')

            RA = cells[4].text.strip()
            DECL = cells[5].text.strip() 

            target_row_element = table.find_all('tr')[ORDER_PLANETS.index('MC') + 2]
            cells = target_row_element.find_all('td')
            RAMC = cells[4].text.strip()

        else:
            print("No table found within the div.")
    else:
        print("No div with id 'tab5' found.")

    return RAMC, RA, DECL    

    


def m_get_astro_chart_positions(day, month, year, hour, minute, second):
    '''returns a string with the planet sign and degree and a dictionary 
    with planet, longitude and speed'''
    
    params = (day, month, year, hour, minute, second)

    birthchart_url = construct_birthchart_url(params)
    
    html = fetch_html(birthchart_url)
    #print("HTML fetched successfully.")
    str_planet_data, detailed_planet_data = extract_planet_positions(html)
    #print("Extracted positions successfully.")
    return str_planet_data, detailed_planet_data

def m_get_astro_emphemeris_ayanam(month, year):
    params = (month, year)
    
    ephemeris_url = construct_ephemeris_url(params)
    html = fetch_html(ephemeris_url)
    #print("HTML fetched successfully.")
    degrees, minutes = extract_ephemeris_data(html)
    #print("Extracted ayanamsa successfully.")
    return degrees, minutes

def m_get_astro_sun_return(degrees, minutes, seconds, sign, year, timezone):
    params = (degrees, minutes, seconds, sign, year)
    
    sunsearch_url = construct_sunsearch_url(params)
    html = fetch_html(sunsearch_url)
    #print("HTML fetched successfully.")
    str_datetime = extract_sunsearch_time(html)
    
    #convert to local time
    datetime_params = convert_str_date_tuple(str_datetime)
    local_time = change_timezone(datetime_params, timezone)  
    #print("Successfully extracted return local datetime.")

    return local_time