from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/check')
def hello_world():
    return jsonify({'code': 500,'message': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
