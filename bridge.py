from flask import Flask, request, jsonify
from creon import Creon
import constants


app = Flask(__name__)
c = Creon()


@app.route('/connection', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_connect():
    c = Creon()
    if request.method == 'GET':
        # check connection status
        return jsonify(c.connected())
    elif request.method == 'POST':
        # make connection
        data = request.get_json()
        _id = data['id']
        _pwd = data['pwd']
        _pwdcert = data['pwdcert']
        return jsonify(c.connect(_id, _pwd, _pwdcert))
    elif request.method == 'DELETE':
        # disconnect
        res = c.disconnect()
        c.kill_client()
        return jsonify(res)


@app.route('/stockcodes', methods=['GET'])
def handle_stockcodes():
    c = Creon()
    c.avoid_reqlimitwarning()
    market = request.args.get('market')
    if market == 'kospi':
        return jsonify(c.get_stockcodes(constants.MARKET_CODE_KOSPI))
    elif market == 'kosdaq':
        return jsonify(c.get_stockcodes(constants.MARKET_CODE_KOSDAQ))
    else:
        return '"market" should be one of "kospi" and "kosdaq".', 400


@app.route('/stockstatus', methods=['GET'])
def handle_stockstatus():
    c = Creon()
    c.avoid_reqlimitwarning()
    stockcode = request.args.get('code')
    if not stockcode:
        return '', 400
    status = c.get_stockstatus(stockcode)
    return jsonify(status)


@app.route('/stockcandles', methods=['GET'])
def handle_stockcandles():
    c = Creon()
    c.avoid_reqlimitwarning()
    stockcode = request.args.get('code')
    n = request.args.get('n')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if not (n or date_from):
        return 'Need to provide "n" or "date_from" argument.', 400
    stockcandles = c.get_chart(stockcode, target='A', unit='D', n=n, date_from=date_from, date_to=date_to)
    return jsonify(stockcandles)


@app.route('/marketcandles', methods=['GET'])
def handle_marketcandles():
    c = Creon()
    c.avoid_reqlimitwarning()
    marketcode = request.args.get('code')
    n = request.args.get('n')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if marketcode == 'kospi':
        marketcode = '001'
    elif marketcode == 'kosdaq':
        marketcode = '201'
    elif marketcode == 'kospi200':
        marketcode = '180'
    else:
        return [], 400
    if not (n or date_from):
        return '', 400
    marketcandles = c.get_chart(marketcode, target='U', unit='D', n=n, date_from=date_from, date_to=date_to)
    return jsonify(marketcandles)


@app.route('/stockfeatures', methods=['GET'])
def handle_stockfeatures():
    c = Creon()
    c.avoid_reqlimitwarning()
    stockcode = request.args.get('code')
    if not stockcode:
        return '', 400
    stockfeatures = c.get_stockfeatures(stockcode)
    return jsonify(stockfeatures)


@app.route('/short', methods=['GET'])
def handle_short():
    c = Creon()
    c.avoid_reqlimitwarning()
    stockcode = request.args.get('code')
    n = request.args.get('n')
    if not stockcode:
        return '', 400
    stockfeatures = c.get_shortstockselling(stockcode, n=n)
    return jsonify(stockfeatures)


if __name__ == "__main__":
    app.run()