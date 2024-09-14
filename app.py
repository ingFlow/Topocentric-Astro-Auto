from flask import Flask, render_template, request
import aspects_implementation as asp
import main_converge as mc
from datetime import datetime, timedelta

app = Flask(__name__)

# Simulated function that returns a list of datetimes
def get_datetimes():
    dt_radix_start, dt_radix_end, geopos, list_of_events = mc.get_json_birth_data('data_input/jacquiline onassis.json')
    file_path = '9_14_ver1_sorted_planet_data.csv'
    dt_day_before_rad = dt_radix_end - timedelta(days=1)
    start_date_str = dt_day_before_rad.strftime('%d %B %Y')

    list_times_to_process = asp.process_csv(file_path, start_date_str,100, -4)
    return list_times_to_process

@app.route('/')
def index():
    # Get the list of datetimes from the function
    list_times_to_process = get_datetimes()
    return render_template('index.html', datetimes=list_times_to_process)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
