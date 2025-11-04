from pydantic import BaseModel
from typing import Optional
from model import Strategy

class registerReq(BaseModel):
    host: str
    userName: Optional[str]
    password: str

class getBestDeviceReq(BaseModel):
    # gpu_needs统一单位 MB
    gpu_needs: int  
    #选择策略
    strategy: Strategy(default=Strategy.LEAST_GPU_MEMORY)
