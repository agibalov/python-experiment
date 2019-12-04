from typing import Any

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_json() -> Any:
    return jsonify({
        'message': 'hello world'
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
