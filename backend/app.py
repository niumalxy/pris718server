import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, jsonify, request
from model.request_model import *
from service import gpu_service
from db.mysql import mysql

app = Flask(__name__)

@app.route('/check')
def check():
    return jsonify({'code': 500,'message': 'success'})

#加入新机器
@app.route('/api/add_host', methods=["POST"])
def addHost():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "请求数据不是有效的 JSON"}), 400
    try:
        req = addHostReq.parse_obj(json_data)
    except Exception as e:
        return jsonify({"message": e + "请提供完整信息。"})
    # TODO，加入mysql
    # result = addHostService
    return jsonify({"message": "已完成"})

@app.route('/api/host_list/<lab>')
def getHostList(lab: str):
    hostList = gpu_service.getHostList(lab)
    return jsonify(hostList)
    
@app.route('/api/list_gpu_usage/<lab>')
def getGpuUsageList(lab: str):
    #machineList = getMachineList()
    machineList = mysql.queryHostListByLab(lab)
    return jsonify(gpu_service.getGpuUsageList(machineList))

@app.route('/api/gpu_usage_by_list', methods=["POST"])
def getGpuUsageListByHostList():
    machineList = request.json()
    return jsonify(gpu_service.getGpuUsageList(machineList))

@app.route('/api/best_device', methods=["POST"])
def getBestDevice():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
