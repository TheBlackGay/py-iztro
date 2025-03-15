"""
日历相关数据模型
"""
from typing import List, Dict
from pydantic import BaseModel, Field


class MonthDaysResponse(BaseModel):
    """月份天数响应"""
    year: int = Field(..., description="年份")
    month: int = Field(..., description="月份")
    days: List[str] = Field(..., description="该月的所有日期，格式为YYYY-MM-DD")
    count: int = Field(..., description="天数")


class YearDaysResponse(BaseModel):
    """年份天数响应"""
    year: int = Field(..., description="年份")
    months: Dict[int, List[str]] = Field(..., description="每个月的所有日期，格式为{月份: [日期列表]}")
    count: int = Field(..., description="总天数")
    days_per_month: Dict[int, int] = Field(..., description="每个月的天数") 