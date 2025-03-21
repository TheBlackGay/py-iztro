"""
紫微斗数API路由
"""
import logging
from fastapi import APIRouter, Query, Depends
from typing import Dict, Any
from datetime import datetime

from ..models import SolarRequest, HoroscopeRequest, APIResponse
from ..models import GenderType, LangueType, TimeIndexType
from ..services import AstroService, DBService

# 获取日志记录器
logger = logging.getLogger("紫微斗数API")

# 创建路由器
router = APIRouter(prefix="/astro", tags=["astro"])

# 依赖注入：获取紫微斗数服务
def get_astro_service():
    """提供紫微斗数服务实例"""
    return AstroService()

# 依赖注入：获取数据库服务
def get_db_service():
    """提供数据库服务实例"""
    return DBService()

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
    astro_service: AstroService = Depends(get_astro_service),
    db_service: DBService = Depends(get_db_service)
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

        # 自动保存到数据库
        try:
            # 先检查是否已存在相同的命盘数据
            existing_id = db_service.check_astro_data_exists(
                solar_date,
                time_index,
                gender
            )
            
            if existing_id:
                # 数据已存在，直接更新并返回
                logger.info(f"命盘数据已存在，ID: {existing_id}，将更新已有记录")
                
                try:
                    db_service.update_astro_data(
                        existing_id, 
                        {
                            'astro_data': natal_chart,
                            'fix_leap': fix_leap,
                            'language': language
                        }, 
                        update_user="system"
                    )
                    logger.info(f"已更新现有命盘数据，ID: {existing_id}")
                except Exception as update_err:
                    logger.warning(f"更新现有命盘数据失败: {str(update_err)}")
                
                # 在结果中添加数据库ID
                natal_chart["db_id"] = existing_id
                return create_success_response(natal_chart, "命盘计算成功 (数据已存在)")
            
            # 如果不存在则正常保存
            new_id = db_service.save_astro_data(
                solar_date,
                time_index,
                gender,
                natal_chart,
                fix_leap,
                language,
                "system"  # 默认创建用户为system
            )
            logger.info(f"命盘数据已保存到数据库，ID: {new_id}")
            
            # 在结果中添加数据库ID
            natal_chart["db_id"] = new_id
        except Exception as e:
            logger.error(f"保存命盘数据到数据库失败: {str(e)}")
            # 尝试从错误消息中提取可能的ID
            if "Duplicate entry" in str(e) and "uniq_data" in str(e):
                try:
                    # 重新查询ID
                    retry_id = db_service.check_astro_data_exists(
                        solar_date,
                        time_index,
                        gender
                    )
                    if retry_id:
                        logger.info(f"检测到重复数据，找到已存在的ID: {retry_id}")
                        natal_chart["db_id"] = retry_id
                        return create_success_response(natal_chart, "命盘计算成功 (数据已存在)")
                except Exception:
                    pass
            # 即使保存失败，我们仍然返回命盘数据

        return create_success_response(natal_chart, "命盘计算成功")
    except Exception as e:
        logger.error(f"处理请求时出错: {str(e)}")
        return create_error_response(str(e))

# 通过阳历获取星盘信息（POST方法）
@router.post("/by_solar")
def calculate_by_solar(
    request: SolarRequest,
    astro_service: AstroService = Depends(get_astro_service),
    db_service: DBService = Depends(get_db_service)
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

        # 自动保存到数据库
        try:
            # 先检查是否已存在相同的命盘数据
            existing_id = db_service.check_astro_data_exists(
                request.solar_date,
                request.time_index,
                request.gender
            )
            
            if existing_id:
                # 数据已存在，直接更新并返回
                logger.info(f"命盘数据已存在，ID: {existing_id}，将更新已有记录")
                
                try:
                    db_service.update_astro_data(
                        existing_id, 
                        {
                            'astro_data': natal_chart,
                            'fix_leap': request.fix_leap,
                            'language': request.language
                        }, 
                        update_user="system"
                    )
                    logger.info(f"已更新现有命盘数据，ID: {existing_id}")
                except Exception as update_err:
                    logger.warning(f"更新现有命盘数据失败: {str(update_err)}")
                
                # 在结果中添加数据库ID
                natal_chart["db_id"] = existing_id
                return create_success_response(natal_chart, "命盘计算成功 (数据已存在)")
            
            # 如果不存在则正常保存
            new_id = db_service.save_astro_data(
                request.solar_date,
                request.time_index,
                request.gender,
                natal_chart,
                request.fix_leap,
                request.language,
                "system"  # 默认创建用户为system
            )
            logger.info(f"命盘数据已保存到数据库，ID: {new_id}")
            
            # 在结果中添加数据库ID
            natal_chart["db_id"] = new_id
        except Exception as e:
            logger.error(f"保存命盘数据到数据库失败: {str(e)}")
            # 尝试从错误消息中提取可能的ID
            if "Duplicate entry" in str(e) and "uniq_data" in str(e):
                try:
                    # 重新查询ID
                    retry_id = db_service.check_astro_data_exists(
                        request.solar_date,
                        request.time_index,
                        request.gender
                    )
                    if retry_id:
                        logger.info(f"检测到重复数据，找到已存在的ID: {retry_id}")
                        natal_chart["db_id"] = retry_id
                        return create_success_response(natal_chart, "命盘计算成功 (数据已存在)")
                except Exception:
                    pass
            # 即使保存失败，我们仍然返回命盘数据

        return create_success_response(natal_chart, "命盘计算成功")
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
    target_time_index: int = Query(..., description="目标时辰序号：0-12，0为早子时，1为丑时，依此类推"),
    fix_leap: bool = Query(True, description="是否调整闰月情况"),
    language: LangueType = Query("zh-CN", description="输出语言"),
    astro_service: AstroService = Depends(get_astro_service),
    db_service: DBService = Depends(get_db_service)
):
    """通过阳历获取大限流年信息"""
    try:
        logger.info(f"接收到大限流年GET请求: 日期={solar_date}, 时辰={time_index}, 性别={gender}, 目标日期={target_date}")

        # 获取完整大限流年数据
        result = astro_service.get_complete_horoscope(
            solar_date, time_index, gender, target_date, target_time_index, fix_leap, language
        )

        if result["status"] == "error":
            return create_error_response(result["message"], result["error"])
        
        # 如果有结果，保存大限数据到数据库
        if result["status"] == "ok" or result["status"] == "partial":
            try:
                horoscope_data = result.get("horoscope", {})
                
                # 检查是否已存在相同的大限数据
                existing_id = db_service.check_horoscope_data_exists(
                    solar_date,
                    time_index,
                    gender,
                    target_date,
                    target_time_index
                )
                
                if existing_id:
                    # 数据已存在，更新并返回
                    logger.info(f"大限数据已存在，ID: {existing_id}，将更新已有记录")
                    try:
                        db_service.update_horoscope_data(
                            existing_id, 
                            {
                                'horoscope_data': horoscope_data
                            }, 
                            update_user="system"
                        )
                        logger.info(f"已更新现有大限数据，ID: {existing_id}")
                    except Exception as update_err:
                        logger.warning(f"更新现有大限数据失败: {str(update_err)}")
                    
                    # 在结果中添加数据库ID
                    if isinstance(horoscope_data, dict):
                        horoscope_data["db_id"] = existing_id
                        result["horoscope"] = horoscope_data
                else:
                    # 如果不存在则正常保存
                    try:
                        new_id = db_service.save_horoscope_data(
                            solar_date,
                            time_index,
                            gender,
                            target_date,
                            target_time_index,
                            horoscope_data,
                            "system"  # 默认创建用户为system
                        )
                        logger.info(f"大限数据已保存到数据库，ID: {new_id}")
                        
                        # 在结果中添加数据库ID
                        if isinstance(horoscope_data, dict):
                            horoscope_data["db_id"] = new_id
                            result["horoscope"] = horoscope_data
                    except Exception as e:
                        logger.error(f"保存大限数据到数据库失败: {str(e)}")
                        # 尝试从错误消息中提取可能的ID
                        if "Duplicate entry" in str(e) and "uniq_data" in str(e):
                            try:
                                # 重新查询ID
                                retry_id = db_service.check_horoscope_data_exists(
                                    solar_date,
                                    time_index,
                                    gender,
                                    target_date,
                                    target_time_index
                                )
                                if retry_id:
                                    logger.info(f"检测到重复数据，找到已存在的ID: {retry_id}")
                                    if isinstance(horoscope_data, dict):
                                        horoscope_data["db_id"] = retry_id
                                        result["horoscope"] = horoscope_data
                            except Exception:
                                pass
            except Exception as db_err:
                logger.error(f"处理大限数据存储过程失败: {str(db_err)}")
                # 即使保存失败，我们仍然返回大限数据
        
        # 返回结果
        if result["status"] == "partial":
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
    astro_service: AstroService = Depends(get_astro_service),
    db_service: DBService = Depends(get_db_service)
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
            request.target_time_index,
            request.fix_leap,
            request.language
        )

        if result["status"] == "error":
            return create_error_response(result["message"], result["error"])
        
        # 如果有结果，保存大限数据到数据库
        if result["status"] == "ok" or result["status"] == "partial":
            try:
                horoscope_data = result.get("horoscope", {})
                
                # 检查是否已存在相同的大限数据
                existing_id = db_service.check_horoscope_data_exists(
                    request.solar_date,
                    request.time_index,
                    request.gender,
                    request.target_date,
                    request.target_time_index
                )
                
                if existing_id:
                    # 数据已存在，更新并返回
                    logger.info(f"大限数据已存在，ID: {existing_id}，将更新已有记录")
                    try:
                        db_service.update_horoscope_data(
                            existing_id, 
                            {
                                'horoscope_data': horoscope_data
                            }, 
                            update_user="system"
                        )
                        logger.info(f"已更新现有大限数据，ID: {existing_id}")
                    except Exception as update_err:
                        logger.warning(f"更新现有大限数据失败: {str(update_err)}")
                    
                    # 在结果中添加数据库ID
                    if isinstance(horoscope_data, dict):
                        horoscope_data["db_id"] = existing_id
                        result["horoscope"] = horoscope_data
                else:
                    # 如果不存在则正常保存
                    try:
                        new_id = db_service.save_horoscope_data(
                            request.solar_date,
                            request.time_index,
                            request.gender,
                            request.target_date,
                            request.target_time_index,
                            horoscope_data,
                            "system"  # 默认创建用户为system
                        )
                        logger.info(f"大限数据已保存到数据库，ID: {new_id}")
                        
                        # 在结果中添加数据库ID
                        if isinstance(horoscope_data, dict):
                            horoscope_data["db_id"] = new_id
                            result["horoscope"] = horoscope_data
                    except Exception as e:
                        logger.error(f"保存大限数据到数据库失败: {str(e)}")
                        # 尝试从错误消息中提取可能的ID
                        if "Duplicate entry" in str(e) and "uniq_data" in str(e):
                            try:
                                # 重新查询ID
                                retry_id = db_service.check_horoscope_data_exists(
                                    request.solar_date,
                                    request.time_index,
                                    request.gender,
                                    request.target_date,
                                    request.target_time_index
                                )
                                if retry_id:
                                    logger.info(f"检测到重复数据，找到已存在的ID: {retry_id}")
                                    if isinstance(horoscope_data, dict):
                                        horoscope_data["db_id"] = retry_id
                                        result["horoscope"] = horoscope_data
                            except Exception:
                                pass
            except Exception as db_err:
                logger.error(f"处理大限数据存储过程失败: {str(db_err)}")
                # 即使保存失败，我们仍然返回大限数据
        
        # 返回结果
        if result["status"] == "partial":
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
