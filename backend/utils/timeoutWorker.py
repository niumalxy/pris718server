import threading
import queue
import time
from typing import Callable, Any, Optional

def timeout_return_none(
    func: Callable[..., Any],
    timeout: float,
    *args,
    **kwargs
) -> Optional[Any]:
    # 用队列传递函数结果（线程安全）
    result_queue = queue.Queue(maxsize=1)

    def worker():
        """子线程执行目标函数，将结果存入队列"""
        try:
            result = func(*args, **kwargs)
            # 避免队列满时阻塞（仅存1个结果）
            result_queue.put_nowait(result)
        except Exception:
            # 函数执行出错也返回None（如需捕获异常可修改此处）
            result_queue.put_nowait(None)

    # 启动子线程
    thread = threading.Thread(target=worker)
    thread.daemon = True  # 守护线程：主线程退出时自动终止
    thread.start()

    # 等待超时时间，获取队列结果
    try:
        # 超时后抛出queue.Empty异常
        return result_queue.get(timeout=timeout)
    except queue.Empty:
        # 超时返回None（子线程会随主线程退出自动终止）
        return None
