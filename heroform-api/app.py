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
    clientTask = request.json['clientTask']
    heroNum = int(request.json['heroNum'])
    weekNum = int(request.json['weekNum'])
    dayPerWeek = int(request.json['dayPerWeek'])
    weekdayHours = int(request.json['weekdayHours'])
    (detailed_work_plan, hero_client_relation) = calculate(clientTask, heroNum, weekNum, dayPerWeek, weekdayHours)
    return jsonify({'workplan': detailed_work_plan, 'clientRelation': hero_client_relation})

if __name__ == '__main__':
    app.run(debug=True)