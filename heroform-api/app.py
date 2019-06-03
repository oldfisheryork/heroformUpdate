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
    week_num = int(request.json['weekNum'])
    days_per_week = int(request.json['dayPerWeek'])
    weekday_hours = int(request.json['weekdayHours'])

    detailed_work_plan, hero_client_relation = calculate(client_task, hero_num, week_num, days_per_week, weekday_hours)

    return jsonify({'workPlan': detailed_work_plan, 'clientRelation': hero_client_relation})


if __name__ == '__main__':
    app.run(debug=True)