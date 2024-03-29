from flask import Flask, request, abort, jsonify
from timetable_util import calculate
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/heroform', methods=["POST"])
def heroform():
    if not request.json:
        abort(400)
    client_task = request.json['clientTask']

    hero_num = int(request.json['heroNum'])

    weekday_hours = int(request.json['weekdayHours'])

    ###updated###
    # Fro month, already parsed into the API mode which means 1-12 other than 0-11
    start_year = int(request.json['startDateYear'])
    start_month = int(request.json['startDateMonth'])
    start_day = int(request.json['startDateDay'])
    end_year = int(request.json['endDateYear'])
    end_month = int(request.json['endDateMonth'])
    end_day = int(request.json['endDateDay'])

    start_date = request.json['startDate']
    end_date = request.json['endDate']

    weekday_calendar, scale_factor, detailed_work_plan, hero_client_relation = calculate(client_task, hero_num, weekday_hours,
                                                         start_year, start_month, start_day, end_year, end_month, end_day)

    return jsonify({'weekdayCalendar': weekday_calendar,
                    'scaleFactor': scale_factor,
                    'workPlan': detailed_work_plan,
                    'clientRelation': hero_client_relation,
                    'startDate': start_date,
                    'endDate': end_date})


if __name__ == '__main__':
    app.run(debug=True)