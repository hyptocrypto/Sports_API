from flask import Flask, jsonify
import time



app = Flask(__name__)


 
@app.route('/api/v1/all')
def all():
    with open('nfl.txt', 'r') as f:
        nfl = f.read()
        f.close()

    with open('nba.txt', 'r') as f:
        nba = f.read()
        f.close()


    with open('mlb.txt') as f:
        mlb = f.read()
        f.close()

    with open('ufc.txt', 'r') as f:
        ufc = f.read()
        f.close()
    return jsonify({'results': [nfl, nba,  mlb, ufc]})


@app.route('/api/v1/nfl')
def nfl():
    with open('nfl.txt', 'r') as f:
        data = f.read()
        f.close()
    return jsonify(data)


@app.route('/api/v1/nba')
def nba():
    with open('nba.txt', 'r') as f:
        data = f.read()
        f.close()
    return jsonify(data)

@app.route('/api/v1/mlb')
def mlb():
    with open('mlb.txt') as f:
        data = f.read()
        f.close()
    return jsonify(data)

@app.route('/api/v1/ufc')
def ufc():
    with open('ufc.txt', 'r') as f:
        data = f.read()
        f.close()
    return jsonify(data)




if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = 8000)
