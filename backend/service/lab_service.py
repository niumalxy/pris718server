from db.mysql import mysql

def getLabBackend(lab):
    backend_info = mysql.queryLabBackend(lab)
    backend_url = "http://" + backend_info["ip"] + ":" + str(backend_info["port"])
    return backend_url
    