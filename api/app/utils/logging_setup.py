"""
日志配置工具
"""
import logging
import sys

def setup_logging(name: str = "紫微斗数API", level: int = logging.INFO):
    """
    配置应用的日志
    
    Args:
        name: 日志记录器名称
        level: 日志级别
    
    Returns:
        配置好的日志记录器
    """
    # 配置日志
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # 获取并返回日志记录器
    logger = logging.getLogger(name)
    return logger 