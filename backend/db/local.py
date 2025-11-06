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
    return [x for x in getMachineList() if x["lab"] == lab]