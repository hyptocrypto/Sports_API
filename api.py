from flask import Flask, jsonify, request
import time
from config import app, db, UFC, NFL, NBA, MLB
from serializer import NBAShareSchema, NFLShareSchema, MLBShareSchema, UFCShareSchema
from sqlalchemy import desc
import datetime
import traceback
from flask_cors import CORS

CORS(app)
NFL_seriaizer = NFLShareSchema(many=True)
NBA_seriaizer = NBAShareSchema(many=True)
MLB_seriaizer = MLBShareSchema(many=True)
UFC_seriaizer = UFCShareSchema(many=True)

###################################   ON DATE #############################################


@app.route("/api/v2/ufc/on_date", methods=["POST"])
def queryUFC_onDate():
    if request.method == "POST":
        data = request.get_data()
        try:
            date = datetime.datetime.strptime(data.decode("utf-8"), "%Y-%m-%d")
        except:
            traceback.print_exc()
            return "Invalid Date format. Please use (YYYY-MM-DD)"
        ret_data = UFC.query.filter(
            UFC.date == date.strftime("%Y-%m-%d")).all()
        print(ret_data)
        ret = UFC_seriaizer.dump(ret_data)
        return jsonify(ret)


@app.route("/api/v2/nfl/on_date", methods=["POST"])
def queryNFL_onDate():
    if request.method == "POST":
        data = request.get_data()
        try:
            date = datetime.datetime.strptime(data.decode("utf-8"), "%Y-%m-%d")
        except:
            traceback.print_exc()
            return "Invalid Date format. Please use (YYYY-MM-DD)"
        ret_data = NFL.query.filter(
            NFL.date == date.strftime("%Y-%m-%d")).all()
        print(ret_data)
        ret = NFL_seriaizer.dump(ret_data)
        return jsonify(ret)


@app.route("/api/v2/nba/on_date", methods=["POST"])
def queryNBA_onDate():
    if request.method == "POST":
        data = request.get_data()
        try:
            date = datetime.datetime.strptime(data.decode("utf-8"), "%Y-%m-%d")
        except:
            traceback.print_exc()
            return "Invalid Date format. Please use (YYYY-MM-DD)"
        ret_data = NBA.query.filter(
            NBA.date == date.strftime("%Y-%m-%d")).all()
        print(ret_data)
        ret = NBA_seriaizer.dump(ret_data)
        return jsonify(ret)


@app.route("/api/v2/mlb/on_date", methods=["POST"])
def queryMLB_onDate():
    if request.method == "POST":
        data = request.get_data()
        try:
            date = datetime.datetime.strptime(data.decode("utf-8"), "%Y-%m-%d")
        except:
            traceback.print_exc()
            return "Invalid Date format. Please use (YYYY-MM-DD)"
        ret_data = MLB.query.filter(
            MLB.date == date.strftime("%Y-%m-%d")).all()
        print(ret_data)
        ret = MLB_seriaizer.dump(ret_data)
        return jsonify(ret)

############################ FROM DATE ###########################################


@app.route("/api/v2/ufc/date", methods=["POST"])
def queryUFC_date():
    if request.method == "POST":
        data = request.get_data()
        try:
            date = datetime.datetime.strptime(data.decode("utf-8"), "%Y-%m-%d")
        except:
            traceback.print_exc()
            return "Invalid Date format. Please use (YYYY-MM-DD)"
        ret_data = UFC.query.filter(UFC.date >= date)
        ret = UFC_seriaizer.dump(ret_data)
        return jsonify(ret)


@ app.route("/api/v2/nfl/date", methods=["POST"])
def queryNFL_date():
    if request.method == "POST":
        data = request.get_data()
        try:
            date = datetime.datetime.strptime(data.decode("utf-8"), "%Y-%m-%d")
        except:
            traceback.print_exc()
            return "Invalid Date format. Please use (YYYY-MM-DD)"
        ret_data = NFL.query.filter(NFL.date >= date)
        ret = NFL_seriaizer.dump(ret_data)
        return jsonify(ret)


@ app.route("/api/v2/nba/date", methods=["POST"])
def queryNBA_date():
    if request.method == "POST":
        data = request.get_data()
        try:
            date = datetime.datetime.strptime(data.decode("utf-8"), "%Y-%m-%d")
        except:
            traceback.print_exc()
            return "Invalid Date format. Please use (YYYY-MM-DD)"
        ret_data = NBA.query.filter(NBA.date >= date)
        ret = NBA_seriaizer.dump(ret_data)
        return jsonify(ret)


@ app.route("/api/v2/mlb/date", methods=["POST"])
def queryMLB_date():
    if request.method == "POST":
        data = request.get_data()
        try:
            date = datetime.datetime.strptime(data.decode("utf-8"), "%Y-%m-%d")
        except:
            traceback.print_exc()
            return "Invalid Date format. Please use (YYYY-MM-DD)"
        ret_data = MLB.query.filter(MLB.date >= date)
        ret = MLB_seriaizer.dump(ret_data)
        return jsonify(ret)


################################ COUNT ###############################
@ app.route("/api/v2/nfl/count", methods=["POST"])
def queryNFL_number():
    if request.method == "POST":
        data = request.get_data()
        if not data.decode("utf-8").isnumeric():
            return "Vaild Int Please"
        ret_data = NFL.query.order_by(desc(NFL.date)).limit(data).all()
        ret = NFL_seriaizer.dump(ret_data)
        return jsonify(ret)


@ app.route("/api/v2/nba/count", methods=["POST"])
def queryNBA_number():
    if request.method == "POST":
        data = request.get_data()
        if not data.decode("utf-8").isnumeric():
            return "Vaild Int Please"
        ret_data = NBA.query.order_by(desc(NBA.date)).limit(data).all()
        ret = NBA_seriaizer.dump(ret_data)
        return jsonify(ret)


@ app.route("/api/v2/mlb/count", methods=["POST"])
def queryMLB_number():
    if request.method == "POST":
        data = request.get_data()
        if not data.decode("utf-8").isnumeric():
            return "Vaild Int Please"
        ret_data = MLB.query.order_by(desc(MLB.date)).limit(data).all()
        ret = MLB_seriaizer.dump(ret_data)
        return jsonify(ret)


@ app.route("/api/v2/ufc/count", methods=["POST"])
def queryUFC_number():
    if request.method == "POST":
        data = request.get_data()
        if not data.decode("utf-8").isnumeric():
            return "Vaild Int Please"
        ret_data = UFC.query.order_by(desc(UFC.date)).limit(data).all()
        ret = UFC_seriaizer.dump(ret_data)
        return jsonify(ret)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
