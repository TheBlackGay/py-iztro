"""
请求模型定义
"""
from pydantic import BaseModel
from typing import Literal

# 定义类型别名
GenderType = Literal["男", "女"]
LangueType = Literal["zh-CN", "zh-TW", "en-US"]
# 时辰索引类型：0-12，0为早子时，1为丑时，依此类推
TimeIndexType = int

class SolarRequest(BaseModel):
    """阳历请求模型"""
    solar_date: str
    time_index: TimeIndexType
    gender: GenderType
    fix_leap: bool = True
    language: LangueType = "zh-CN"

class HoroscopeRequest(BaseModel):
    """大限流年请求模型"""
    solar_date: str
    time_index: TimeIndexType
    gender: GenderType
    target_date: str
    fix_leap: bool = True
    language: LangueType = "zh-CN" 