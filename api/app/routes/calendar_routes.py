"""
日历相关路由
"""
import logging
from fastapi import APIRouter, HTTPException, Query, Body
from datetime import datetime
from pydantic import BaseModel, Field

from ..services.calendar_service import CalendarService
from ..models.calendar_models import MonthDaysResponse

# 日志记录器
logger = logging.getLogger("紫微斗数API")

# 路由
router = APIRouter(tags=["calendar"])

# 服务实例
calendar_service = CalendarService()

# 请求模型
class MonthDaysRequest(BaseModel):
    """月份天数请求"""
    date: str = Field(..., description="日期，格式为YYYY-MM或YYYY-M")


@router.get("/month_days", response_model=MonthDaysResponse)
async def get_month_days(date: str = Query(..., description="日期，格式为YYYY-MM或YYYY-M")):
    """
    获取指定月份的所有天数
    
    参数:
    - date: 日期，格式为YYYY-MM或YYYY-M，如2025-03或2025-3
    
    返回:
    - 该月所有天的日期列表
    """
    logger.info(f"接收到获取月份天数GET请求: date={date}")
    
    # 调用服务
    result, error = calendar_service.get_month_days(date)
    
    if error:
        logger.error(f"获取月份天数失败: {error}")
        raise HTTPException(status_code=400, detail=error)
    
    logger.info(f"获取月份天数成功: 共{result['count']}天")
    return result


@router.post("/month_days", response_model=MonthDaysResponse)
async def post_month_days(request: MonthDaysRequest):
    """
    获取指定月份的所有天数 (POST方法)
    
    请求体:
    - date: 日期，格式为YYYY-MM或YYYY-M，如2025-03或2025-3
    
    返回:
    - 该月所有天的日期列表
    """
    logger.info(f"接收到获取月份天数POST请求: date={request.date}")
    
    # 调用服务
    result, error = calendar_service.get_month_days(request.date)
    
    if error:
        logger.error(f"获取月份天数失败: {error}")
        raise HTTPException(status_code=400, detail=error)
    
    logger.info(f"获取月份天数成功: 共{result['count']}天")
    return result 