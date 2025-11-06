def getMachineList():
    return [
        {
            "host": "10.160.4.55", 
            "username": "lxy", 
            "password": "pris.1234",
            "port": None,
            "lab": "school"
        },
    ]

def getHostList(lab):
    machineList = getMachineList()
    return [x for x in machineList if x["lab"] == lab]