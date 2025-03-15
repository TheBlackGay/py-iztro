"""
数据模型包
"""
from .request_models import SolarRequest, HoroscopeRequest, GenderType, LangueType, TimeIndexType
from .response_models import APIResponse

__all__ = [
    'SolarRequest',
    'HoroscopeRequest',
    'APIResponse',
    'GenderType',
    'LangueType',
    'TimeIndexType'
] 