"""
紫微斗数计算服务提供者
"""
import logging
import sys
from datetime import datetime
from typing import Dict, Any, Tuple, Optional, Union

# 日志记录器
logger = logging.getLogger("紫微斗数API")

# 模拟的紫微斗数计算引擎
class MockAstroEngine:
    """模拟的紫微斗数计算引擎，当无法使用真实引擎时使用"""
    
    def __init__(self):
        """初始化模拟引擎"""
        logger.info("初始化模拟紫微斗数计算引擎")
    
    def by_solar(self, solar_date: str, time_index: int, gender: str, 
                 fix_leap: bool = True, language: str = "zh-CN") -> Dict[str, Any]:
        """
        模拟通过阳历获取星盘
        
        Args:
            solar_date: 阳历日期，格式为YYYY-MM-DD或YYYY-M-D
            time_index: 出生时辰序号，0-12
            gender: 性别，"男"或"女"
            fix_leap: 是否调整闰月情况
            language: 输出语言
            
        Returns:
            模拟的星盘数据
        """
        # 返回模拟数据
        birth_year = int(solar_date.split('-')[0])
        current_year = datetime.now().year
        age = current_year - birth_year
        
        return {
            "gender": gender,
            "solarDate": solar_date,
            "lunarDate": f"模拟农历日期-{solar_date}",
            "chineseDate": f"模拟中文日期-{solar_date}",
            "time": time_index,
            "timeRange": f"模拟时辰范围-{time_index}",
            "age": age,
            "message": "注意：这是模拟数据，因为无法导入py_iztro库",
            "palaces": []
        }
    
    def horoscope(self, natal_chart: Dict[str, Any], target_date: str) -> Dict[str, Any]:
        """
        模拟大限流年计算
        
        Args:
            natal_chart: 本命盘数据
            target_date: 目标日期，格式为YYYY-MM-DD或YYYY-M-D
            
        Returns:
            模拟的大限流年数据
        """
        # 从命盘获取出生日期
        solar_date = natal_chart.get("solarDate", "2000-1-1")
        birth_year = int(solar_date.split('-')[0])
        
        # 从目标日期获取年份
        target_year = int(target_date.split('-')[0])
        age = target_year - birth_year
        
        return {
            "target_date": target_date,
            "age": age,
            "message": "注意：这是模拟数据，因为无法导入py_iztro库",
            "horoscope_data": []
        }

class AstroProvider:
    """紫微斗数计算服务提供者，用于获取不同的计算引擎"""
    
    @staticmethod
    def get_engine():
        """
        获取紫微斗数计算引擎
        
        Returns:
            适用的计算引擎对象
        """
        # 尝试导入紫微斗数计算类
        try:
            from py_iztro import Astro
            logger.info("成功导入py_iztro库")
            return Astro(), True
        except ImportError:
            logger.warning("无法导入py_iztro库，将使用模拟数据引擎")
            return MockAstroEngine(), False 