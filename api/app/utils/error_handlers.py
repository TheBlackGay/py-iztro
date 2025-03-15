"""
错误处理工具
"""
import logging
import traceback
import signal
import sys
import time
from typing import Callable, Any, Tuple, Optional

# 获取日志记录器
logger = logging.getLogger("紫微斗数API")

# SIGSEGV信号处理器
def setup_signal_handlers():
    """
    设置信号处理器，捕获SIGSEGV等信号
    """
    def handle_segfault(signum, frame):
        logger.error(f"检测到信号 {signum}! 程序即将优雅退出。")
        sys.exit(1)
    
    # 注册信号处理器
    signal.signal(signal.SIGSEGV, handle_segfault)
    signal.signal(signal.SIGTERM, handle_segfault)
    logger.info("已设置信号处理器")

# 安全执行函数
def safe_execute(func: Callable, *args, **kwargs) -> Tuple[Any, Optional[str]]:
    """
    安全执行函数，防止SIGSEGV导致的崩溃
    
    Args:
        func: 要执行的函数
        *args: 函数的位置参数
        **kwargs: 函数的关键字参数
    
    Returns:
        (result, error): 函数执行结果和可能的错误信息
    """
    try:
        # 设置超时检测（无法直接防止SIGSEGV，但可以检测长时间无响应）
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        
        if execution_time > 10:  # 如果执行时间超过10秒，记录警告
            logger.warning(f"函数 {func.__name__} 执行时间较长: {execution_time:.2f}秒")
            
        return result, None
    except Exception as e:
        logger.error(f"函数 {func.__name__} 执行出错: {str(e)}")
        logger.error(traceback.format_exc())
        return None, str(e) 