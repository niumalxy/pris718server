from utils.expirableDict import expirableDict
from utils.ssh import ssh
import re
from logger.logger import logger
from model import command

# 全局变量，用于防止连接过多导致服务器崩溃
statusCache = expirableDict()

def parseGpuUsageInfo(info: str) -> dict:
    lines = info.split("\n")
    gpu_infos = []
    for line in lines:
        items = line.split(",")
        # 跳过最后一行
        if len(items) < 3:
            break
        gpu_infos.append({
            "gpu_type": items[0],
            "usage": int(items[1].strip()),
            "total": int(items[2].strip())
        })
    return gpu_infos
    
def getGpuUsageList(machineList: list):
    status = []
    for machine in machineList:
        cache = statusCache.get(machine["host"])
        if cache:
            logger.info("Hit cache!")
            status.append({machine["host"]: cache})
            continue
        # try:
        conn = ssh(host=machine["host"], username=machine["username"], password=machine["password"], port=machine["port"])
        cmdResult = conn.run_command(command=command.GPU_INFO_COMMAND)
        conn.close()
        gpu_infos = parseGpuUsageInfo(cmdResult)
        status.append({machine["host"]: gpu_infos})
        # 缓存，10s过期
        statusCache.set(machine["host"], gpu_infos, expire=10)
        # except Exception as e:
        #     logger.error(f"machine {machine} goes wrong, msg: ", e)
        #     continue
    return status

if __name__ == "__main__":
    machineList = machineFactory.getMachineList()
    print(getGpuUsageList)