'''from flask import Flask, render_template, request, send_file
from kerykeion import AstrologicalSubject, KerykeionChartSVG
import os
import shutil
from datetime import datetime

app = Flask(__name__)

# Route for the main page
@app.route('/')
def index():
    return render_template('index_k.html')

def clear_directory(directory_path):
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        shutil.rmtree(directory_path)
        os.makedirs(directory_path)  # Recreate the empty directory
    else:
        print("Directory does not exist or is not a directory.")

# Route to generate and serve the SVG chart
@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    clear_directory("static/charts")
    
    # Get form data
    name = request.form['name']
    birthdate = request.form['birthdate']  # Format: YYYY-MM-DD
    birthtime = request.form['birthtime']  # Format: HH:MM
    seconds = int(request.form['seconds'])  # Get seconds as an integer
    
    # Parse the combined birth date and time
    date_obj = datetime.strptime(birthdate, '%Y-%m-%d')
    time_obj = datetime.strptime(birthtime, '%H:%M')
    
    birthcity = request.form['birthcity']
    
    svg_path = f"static/charts/{name} - Natal Chart.svg"
    
    dark_theme_subject = AstrologicalSubject(
        name,
        date_obj.year,
        date_obj.month,
        date_obj.day,
        time_obj.hour,
        time_obj.minute,
        seconds,  # Add seconds here
        lng=50,
        lat=50,
        tz_str="Europe/Rome",
        houses_system_identifier="T"
    )
    
    dark_theme_natal_chart = KerykeionChartSVG(dark_theme_subject, theme="dark-high-contrast", new_output_directory="static/charts")
    dark_theme_natal_chart.makeSVG()

    return send_file(svg_path, mimetype='image/svg+xml')

if __name__ == '__main__':
    os.makedirs("static/charts", exist_ok=True)
    app.run(debug=True)
'''
'''
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('inf.html')

@app.route('/custom_action', methods=['POST'])
def custom_action():
    # Perform your custom server-side action here
    return jsonify({"message": "Custom action performed successfully!"})

if __name__ == '__main__':
    app.run(debug=True)'''
from kerykeion import AstrologicalSubject, KerykeionChartSVG
from app import get_timezone_name_from_pos
from datetime import datetime

def main(geopos, chart_datetime):
    timezone_name = get_timezone_name_from_pos(geopos)
    filename = f"{chart_datetime.strftime("%Y-%m-%d %H:%M:%S")} {geopos}"    
    filename = "yes"
    svg_path = f"static/charts/{filename} - Natal Chart.svg"
    
    chart_subject = AstrologicalSubject(
        filename,
        chart_datetime.year,
        chart_datetime.month,
        chart_datetime.day,
        chart_datetime.hour,
        chart_datetime.minute,
        chart_datetime.second,  
        lng=geopos[0],
        lat=geopos[1],
        tz_str=timezone_name,
        houses_system_identifier="T"
    )
    
    date_natal_chart = KerykeionChartSVG(chart_subject, theme="dark-high-contrast", new_output_directory="static/charts")
    date_natal_chart.makeSVG()

geopos = [-26.075, 28.09472, 1753.0]
chart_datetime = datetime.fromisoformat('2008-09-05T12:00:00')
main(geopos,chart_datetime)