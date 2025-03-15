"""
结果处理工具
"""
import logging
from typing import Any, Dict, Optional

# 获取日志记录器
logger = logging.getLogger("紫微斗数API")

def handle_result(data: Any) -> Dict:
    """
    处理返回结果，兼容不同类型的返回值
    
    Args:
        data: 要处理的数据对象
        
    Returns:
        处理后的字典数据
    """
    try:
        if hasattr(data, 'dict'):
            # 尝试使用model_dump（较新的pydantic版本）
            if hasattr(data, 'model_dump'):
                return data.model_dump(by_alias=True)
            # 回退到dict方法（较旧的pydantic版本）
            return data.dict(by_alias=True)
        
        # 如果是普通字典或其他类型，直接返回
        return data
    except Exception as e:
        logger.error(f"处理结果时出错: {str(e)}")
        # 返回一个简单的字典以避免完全失败
        return {"error": str(e), "data_type": str(type(data))}


def calculate_age(birth_date: str, target_date: str) -> Optional[int]:
    """
    计算两个日期之间的年龄差
    
    Args:
        birth_date: 出生日期，格式为YYYY-MM-DD或YYYY-M-D
        target_date: 目标日期，格式为YYYY-MM-DD或YYYY-M-D
        
    Returns:
        年龄差或None（出错时）
    """
    try:
        birth_year = int(birth_date.split('-')[0])
        target_year = int(target_date.split('-')[0])
        return target_year - birth_year
    except Exception as e:
        logger.error(f"计算年龄时出错: {str(e)}")
        return None 