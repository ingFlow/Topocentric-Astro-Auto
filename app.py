from flask import Flask, render_template, jsonify, request
import pd_automate 
import main_converge
import julian

app = Flask(__name__)

@app.route('/')
def home():
    dt_actual_dob, _, _, geopos, list_of_events = main_converge.get_json_birth_data("data_input/jacquiline onassis.json")
    jd_radix = julian.to_jd(dt_actual_dob)
    list_dt_events = [t[0] for t in list_of_events]
    str_asp_dir, str_asp_conv = pd_automate.pd_for_time_event_norad(jd_radix,julian.to_jd(list_dt_events[0]),geopos)
    list_all_asp = [*str_asp_dir.split('\n'),*str_asp_conv.split('\n')]
    

    left_items = list_dt_events
    right_items = list_all_asp
    return render_template('index.html', left_column_items=left_items, right_column_items=right_items)

@app.route('/update_content')
def update_content():
    left_radio = request.args.get('left_radio', '')
    right_radio = request.args.get('right_radio', '')
    left_item = request.args.get('left_item', '')
    right_item = request.args.get('right_item', '')

    content = f"Left Radio: {left_radio}, Right Radio: {right_radio}, Left Item: {left_item}, Right Item: {right_item}"
    
    return jsonify({'message': content})

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
