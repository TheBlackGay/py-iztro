"""
紫微斗数API路由
"""
import logging
from fastapi import APIRouter, Query, Depends
from typing import Dict, Any
from datetime import datetime

from ..models import SolarRequest, HoroscopeRequest, APIResponse
from ..models import GenderType, LangueType, TimeIndexType
from ..services import AstroService

# 获取日志记录器
logger = logging.getLogger("紫微斗数API")

# 创建路由器
router = APIRouter(prefix="/astro", tags=["astro"])

# 依赖注入：获取紫微斗数服务
def get_astro_service():
    """提供紫微斗数服务实例"""
    return AstroService()

# 创建错误响应
def create_error_response(error_message: str, error_detail: str = None):
    """创建标准错误响应"""
    return {
        "status": "error",
        "message": f"计算失败: {error_message}",
        "timestamp": datetime.now().isoformat(),
        "result": None,
        "error": error_detail or error_message
    }

# 创建成功响应
def create_success_response(result: Dict[str, Any], message: str = "计算成功"):
    """创建标准成功响应"""
    return {
        "status": "ok",
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "result": result,
        "error": None
    }

# 创建部分成功响应
def create_partial_response(result: Dict[str, Any], error_message: str, error_detail: str = None):
    """创建标准部分成功响应"""
    return {
        "status": "partial",
        "message": f"部分计算成功: {error_message}",
        "timestamp": datetime.now().isoformat(),
        "result": result,
        "error": error_detail or error_message
    }

# 通过阳历获取星盘信息（GET方法）
@router.get("/by_solar")
def calculate_by_solar_get(
    solar_date: str = Query(..., description="阳历日期，格式：YYYY-M-D"),
    time_index: TimeIndexType = Query(..., description="出生时辰序号：0-12，0为早子时，1为丑时，依此类推"),
    gender: GenderType = Query(..., description="性别：男/女"),
    fix_leap: bool = Query(True, description="是否调整闰月情况"),
    language: LangueType = Query("zh-CN", description="输出语言"),
    astro_service: AstroService = Depends(get_astro_service)
):
    """通过阳历获取星盘信息"""
    try:
        logger.info(f"接收到GET请求: 日期={solar_date}, 时辰={time_index}, 性别={gender}")
        
        # 获取本命盘
        natal_chart, error = astro_service.get_natal_chart(
            solar_date, time_index, gender, fix_leap, language
        )
        
        if error:
            return create_error_response(error)
        
        return create_success_response(natal_chart)
    except Exception as e:
        logger.error(f"处理请求时出错: {str(e)}")
        return create_error_response(str(e))

# 通过阳历获取星盘信息（POST方法）
@router.post("/by_solar")
def calculate_by_solar(
    request: SolarRequest,
    astro_service: AstroService = Depends(get_astro_service)
):
    """通过阳历获取星盘信息"""
    try:
        logger.info(f"接收到POST请求: {request.model_dump()}")
        
        # 获取本命盘
        natal_chart, error = astro_service.get_natal_chart(
            request.solar_date, 
            request.time_index, 
            request.gender, 
            request.fix_leap, 
            request.language
        )
        
        if error:
            return create_error_response(error)
        
        return create_success_response(natal_chart)
    except Exception as e:
        logger.error(f"处理请求时出错: {str(e)}")
        return create_error_response(str(e))

# 计算大限流年（GET方法）
@router.get("/horoscope")
def calculate_horoscope_get(
    solar_date: str = Query(..., description="阳历日期，格式：YYYY-M-D"),
    time_index: TimeIndexType = Query(..., description="出生时辰序号：0-12，0为早子时，1为丑时，依此类推"),
    gender: GenderType = Query(..., description="性别：男/女"),
    target_date: str = Query(..., description="目标日期，格式：YYYY-MM-DD"),
    fix_leap: bool = Query(True, description="是否调整闰月情况"),
    language: LangueType = Query("zh-CN", description="输出语言"),
    astro_service: AstroService = Depends(get_astro_service)
):
    """通过阳历获取大限流年信息"""
    try:
        logger.info(f"接收到大限流年GET请求: 日期={solar_date}, 时辰={time_index}, 性别={gender}, 目标日期={target_date}")
        
        # 获取完整大限流年数据
        result = astro_service.get_complete_horoscope(
            solar_date, time_index, gender, target_date, fix_leap, language
        )
        
        if result["status"] == "error":
            return create_error_response(result["message"], result["error"])
        elif result["status"] == "partial":
            return create_partial_response(
                {"natal_chart": result["natal_chart"], "horoscope": result["horoscope"]},
                result["message"],
                result["error"]
            )
        else:
            return create_success_response(
                {"natal_chart": result["natal_chart"], "horoscope": result["horoscope"]},
                "大限流年计算成功"
            )
    except Exception as e:
        logger.error(f"处理大限流年请求时出错: {str(e)}")
        return create_error_response(f"大限流年计算失败: {str(e)}")

# 计算大限流年（POST方法）
@router.post("/horoscope")
def calculate_horoscope_post(
    request: HoroscopeRequest,
    astro_service: AstroService = Depends(get_astro_service)
):
    """通过阳历获取大限流年信息"""
    try:
        logger.info(f"接收到大限流年POST请求: {request.model_dump()}")
        
        # 获取完整大限流年数据
        result = astro_service.get_complete_horoscope(
            request.solar_date, 
            request.time_index, 
            request.gender, 
            request.target_date, 
            request.fix_leap, 
            request.language
        )
        
        if result["status"] == "error":
            return create_error_response(result["message"], result["error"])
        elif result["status"] == "partial":
            return create_partial_response(
                {"natal_chart": result["natal_chart"], "horoscope": result["horoscope"]},
                result["message"],
                result["error"]
            )
        else:
            return create_success_response(
                {"natal_chart": result["natal_chart"], "horoscope": result["horoscope"]},
                "大限流年计算成功"
            )
    except Exception as e:
        logger.error(f"处理大限流年请求时出错: {str(e)}")
        return create_error_response(f"大限流年计算失败: {str(e)}") 