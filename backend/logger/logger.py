import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# 创建文件处理器
current_time = datetime.now()
formatted_time = current_time.strftime("%Y%m%d%H%M%S")
file_handler = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)).split("logger")[0], "log", f"log{formatted_time}.log"))
file_handler.setLevel(logging.INFO)



# 设置日志格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)


# 将处理器添加到日志记录器
logger.addHandler(file_handler)

# 创建控制台处理器
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)

# 记录日志
logger.info("logger start.")