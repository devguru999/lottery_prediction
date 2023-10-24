from flask import Flask, render_template, request, jsonify
from scripts import lotteryai
import json

app = Flask(__name__, static_folder='./templates/static')
app.config['SECRET_KEY'] = 'lottery-ai!@#'

@app.route('/', methods=['GET'])
def index():
    with open('data/area_code.json') as file:
        area_codes = json.load(file)
    return render_template('index.html', area_list=area_codes)

@app.route('/lottery', methods=['POST'])
def getLotteries():
    query = request.get_json()
    lotteries = lotteryai.load_lotteries_for(query["area_code"])
    return jsonify(lotteries)

@app.route('/data', methods=['POST'])
def getLotData():
    query = request.get_json()
    values = lotteryai.load_data_for(query["area_code"], query["lottery"])
    return jsonify(values.tolist())

@app.route('/predict', methods=['POST'])
def getPrediction():
    query = request.get_json()
    values = lotteryai.get_prediction(query["area_code"], query["lottery"])
    return jsonify(list(values))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')