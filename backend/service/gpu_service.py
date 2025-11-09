from utils.expirableDict import expirableDict
from utils.ssh import ssh
import re
from logger.logger import logger
from model import command
from db.mysql import mysql
from concurrent.futures import ThreadPoolExecutor
import json
import concurrent.futures as futures

threadPool = ThreadPoolExecutor(max_workers=3)
# 全局变量，用于防止连接过多导致服务器崩溃
statusCache = expirableDict()

# TODO: 提升响应速度，线程池多任务访问服务器

def getHostList(lab: str):
    return mysql.queryHostListByLab(lab)

def parseGpuUsageInfo(info: str) -> dict:
    lines = info.split("\n")
    gpu_infos = []
    for line in lines:
        items = line.split(",")
        # 跳过不相关的行
        if len(items) < 3:
            continue
        gpu_infos.append({
            "gpu_type": items[0],
            "usage": int(items[1].strip()),
            "total": int(items[2].strip())
        })
    return gpu_infos

LAB2LABNAME = {
    'dft': "东方通",
    'school': "校园网"
}

def fetch_data(machine):
    try:
        conn = ssh(machine["host"], machine["username"], machine["port"], machine["password"])
        cmdResult = conn.run_command(command=command.GPU_INFO_COMMAND)
        conn.close()
        gpu_infos = parseGpuUsageInfo(cmdResult)
        #带上机房名称
        host_name = LAB2LABNAME[machine['lab']] + ":" + machine["host"]
        # 缓存，10s过期
        statusCache.set(host_name, gpu_infos, expire=10)
        return {host_name: gpu_infos}
    except Exception as e:
        logger.error(f"Machine {machine} goes wrong, msg: ", e)
        return None
    
def getGpuUsageList(machineList: list):
    status = []
    future_tasks = []
    for machine in machineList:
        cache = statusCache.get(machine["host"])
        if cache:
            logger.info(f"Hit cache: {machine['host']}")
            status.append({machine["host"]: cache})
            continue
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_tasks.append(executor.submit(fetch_data, machine))
    # 获取结果
    for future in futures.as_completed(future_tasks):
        result = future.result(timeout=5)
        if result:
            status.append(result)
            logger.info(f"Get data from {result}")

    # 按空闲量排序
    def get_total(x):
        x = x[list(x.keys())[0]]
        total = 0
        for item in x:
            total += item["total"] - item["usage"]
        return total
    status.sort(key=get_total, reverse=True)
    return status

if __name__ == "__main__":
    machineList = machineFactory.getMachineList()
    print(getGpuUsageList)