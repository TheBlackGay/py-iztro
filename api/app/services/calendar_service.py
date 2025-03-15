"""
日历服务
"""
import logging
import calendar
from datetime import datetime
from typing import List, Tuple, Optional

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