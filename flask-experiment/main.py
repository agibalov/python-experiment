from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/hello/plaintext', methods=['GET'])
def hello_plaintext():
    return 'hi there!', 200


@app.route('/hello/json', methods=['GET'])
def hello_json():
    return jsonify({
        'message': 'hi there!!!1'
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
