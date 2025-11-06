from logger.logger import logger
import configparser
from pymysql.err import OperationalError
import pymysql

class mysql:
    def __init__(self):
        config = self._read_mysql_config()
        try:
            self.conn = pymysql.connect(**config)
        except OperationalError as e:
            # 连接错误（如地址、端口、密码错误）
            log.error("数据库连接失败！")
            self.conn = None
        
    def queryHostListByLab(self, lab: str):
        sql = "SELECT * FROM server_info WHERE lab = %s"
        params = (lab, )
        cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        logger.info("execute sql: "+cursor.mogrify(sql, params))
        cursor.execute(sql, params)
        results = cursor.fetchall()
        return results
    def _read_mysql_config(self, config_path="conf/mysql.conf"):
        """
        读取 MySQL 配置文件
        :param config_path: 配置文件路径
        :return: 配置字典
        """
        # 初始化配置解析器
        config = configparser.ConfigParser()
        
        # 读取配置文件（若文件不存在或无 mysql 节点，抛出异常）
        if not config.read(config_path, encoding="utf-8"):
            raise FileNotFoundError(f"配置文件 {config_path} 不存在或无法读取")
        if "mysql" not in config.sections():
            raise ValueError("配置文件中缺少 [mysql] 节点")
        
        # 提取配置（转换端口为整数，其他为字符串）
        mysql_config = {
            "host": config.get("mysql", "host"),
            "port": config.getint("mysql", "port"),
            "user": config.get("mysql", "user"),
            "password": config.get("mysql", "password"),
            "database": config.get("mysql", "database"),
            "charset": config.get("mysql", "charset", fallback="utf8mb4"), 
        }
        return mysql_config
    

mysql = mysql()