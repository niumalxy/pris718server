import time

class expirableDict:
    """
    基于Dict和lazy expire实现的可过期dict
    """
    def __init__(self):
        self.dict = {}

    def __str__(self):
        return self.dict

    def convert_data(self, value, expire_timestamp, create_timestamp):
        return {
            "value": value,
            "expire_timestamp": expire_timestamp,
            "create_timestamp": create_timestamp
        }

    def get(self, key):
        if key not in self.dict:
            return None
        # 超时删除
        if time.time() >= self.dict[key]["expire_timestamp"] + self.dict[key]["create_timestamp"]:
            del self.dict[key]
            return None
        return self.dict[key]["value"]
    """
    expire表示过期时间（秒）
    """
    def set(self, key, value=None, expire=0): 
        data = self.get(key)
        if data:
            value = data["value"] if value is None else value
            expire_timestamp = data["expire_timestamp"] if expire == 0 else expire
            create_timestamp = data["create_timestamp"] if expire == 0 else time.time()
            self.dict[key] = self.convert_data(value, expire_timestamp, create_timestamp)
        else:
            #不设置expire，则永不过期
            expire_timestamp = 1640995200 if expire == 0 else expire 
            create_timestamp = time.time()
            self.dict[key] = self.convert_data(value, expire_timestamp, create_timestamp)



