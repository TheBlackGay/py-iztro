"""
日历相关数据模型
"""
from typing import List
from pydantic import BaseModel, Field


class MonthDaysResponse(BaseModel):
    """月份天数响应"""
    year: int = Field(..., description="年份")
    month: int = Field(..., description="月份")
    days: List[str] = Field(..., description="该月的所有日期，格式为YYYY-MM-DD")
    count: int = Field(..., description="天数") 