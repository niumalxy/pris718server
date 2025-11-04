from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/check')
def check():
    return jsonify({'code': 500,'message': 'success'})

#注册新机器
@app.route('/api/register', method=["POST"])
def register():
    pass

@app.route('/api/gpu_usage', method=["GET"])
def getGpuUsage():
    pass

@app.route('/api/best_device', method=["POST"])
def getBestDevice():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
