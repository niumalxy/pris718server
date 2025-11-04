from enum import Enum

class Strategy(Enum):
    #满足容量需求且占机器显存最少
    LEAST_GPU_MEMORY = 1
    #尽可能找更多显存的机器
    MAXIMUM_GPU_MEMORY = 2