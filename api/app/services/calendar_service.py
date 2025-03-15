"""
日历服务
"""
import logging
import calendar
from datetime import datetime
from typing import List, Tuple, Optional, Dict

# 日志记录器
logger = logging.getLogger("紫微斗数API")

class CalendarService:
    """日历服务"""

    def __init__(self):
        """初始化日历服务"""
        logger.info("日历服务初始化完成")

    def get_month_days(self, date_str: str) -> Tuple[Optional[dict], Optional[str]]:
        """
        获取指定月份的所有天数

        Args:
            date_str: 日期字符串，格式为YYYY-MM或YYYY-M

        Returns:
            (days_data, error): 天数数据和可能的错误信息
        """
        logger.info(f"获取月份天数: 日期={date_str}")

        try:
            # 解析输入日期
            parts = date_str.split("-")
            if len(parts) != 2:
                return None, "日期格式不正确，应为YYYY-MM或YYYY-M"
            
            try:
                year = int(parts[0])
                month = int(parts[1])
            except ValueError:
                return None, "年份或月份不是有效数字"
            
            # 验证年月
            if not (1900 <= year <= 2100):
                return None, "年份超出范围(1900-2100)"
            if not (1 <= month <= 12):
                return None, "月份超出范围(1-12)"
            
            # 计算该月的天数
            _, days_in_month = calendar.monthrange(year, month)
            
            # 格式化每一天的日期
            days_list = []
            for day in range(1, days_in_month + 1):
                # 使用ISO格式(YYYY-MM-DD)
                day_str = f"{year}-{month:02d}-{day:02d}"
                days_list.append(day_str)
            
            # 构建返回数据
            result = {
                "year": year,
                "month": month,
                "days": days_list,
                "count": len(days_list)
            }
            
            return result, None
            
        except Exception as e:
            logger.error(f"获取月份天数失败: {str(e)}")
            return None, f"获取月份天数失败: {str(e)}"
            
    def get_year_days(self, year_str: str) -> Tuple[Optional[dict], Optional[str]]:
        """
        获取指定年份的所有天数
        
        Args:
            year_str: 年份字符串，格式为YYYY
            
        Returns:
            (days_data, error): 天数数据和可能的错误信息
        """
        logger.info(f"获取年份天数: 年份={year_str}")
        
        try:
            # 解析输入年份
            try:
                year = int(year_str)
            except ValueError:
                return None, "年份不是有效数字"
                
            # 验证年份
            if not (1900 <= year <= 2100):
                return None, "年份超出范围(1900-2100)"
                
            # 存储每个月的日期和天数
            months_data = {}
            days_per_month = {}
            total_days = 0
            
            # 遍历12个月
            for month in range(1, 13):
                # 计算当月天数
                _, days_in_month = calendar.monthrange(year, month)
                
                # 格式化每一天的日期
                days_list = []
                for day in range(1, days_in_month + 1):
                    day_str = f"{year}-{month:02d}-{day:02d}"
                    days_list.append(day_str)
                
                # 保存当月数据
                months_data[month] = days_list
                days_per_month[month] = days_in_month
                total_days += days_in_month
            
            # 构建返回数据
            result = {
                "year": year,
                "months": months_data,
                "count": total_days,
                "days_per_month": days_per_month
            }
            
            # 尝试使用iztro库获取额外的日历信息
            try:
                # 检查是否能导入iztro库
                from py_iztro import Calendar
                logger.info("使用py_iztro库获取额外的日历信息")
                
                # 待实现: 如果需要使用iztro库的其他功能，可以在这里添加代码
                
            except ImportError:
                logger.warning("未能导入py_iztro库，不提供额外的日历信息")
            except Exception as e:
                logger.warning(f"使用py_iztro获取日历信息时出错: {str(e)}")
            
            return result, None
            
        except Exception as e:
            logger.error(f"获取年份天数失败: {str(e)}")
            return None, f"获取年份天数失败: {str(e)}" 