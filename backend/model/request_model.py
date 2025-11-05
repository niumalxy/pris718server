from pydantic import BaseModel, Field
from typing import Optional
from model.model import Strategy

class addHostReq(BaseModel):
    host: str
    userName: Optional[str]
    password: str

class getBestDeviceReq(BaseModel):
    # gpu_needs统一单位 MB
    gpu_needs: int  
    #选择策略
    strategy: Strategy = Field(default=Strategy.LEAST_GPU_MEMORY)
