"""
测试API路由
"""
import logging
from datetime import datetime
from fastapi import APIRouter, Depends
from typing import Dict, Any

from ..services import AstroService

# 获取日志记录器
logger = logging.getLogger("紫微斗数API")

# 创建路由器
router = APIRouter(tags=["test"])

# 依赖注入：获取紫微斗数服务
def get_astro_service():
    """提供紫微斗数服务实例"""
    return AstroService()

# 测试接口
@router.get("/test")
def test_endpoint(astro_service: AstroService = Depends(get_astro_service)):
    """测试API是否正常运行"""
    try:
        # 检查服务是否正常
        engine_type = type(astro_service.engine).__name__
        
        # 构建测试响应
        response = {
            "status": "ok",
            "message": "API服务正常运行",
            "timestamp": datetime.now().isoformat(),
            "astro_service_initialized": True,
            "engine_type": engine_type,
            "using_real_engine": astro_service.using_real_engine,
            "test_result": {
                "sample_data": "测试成功"
            },
            "test_error": None
        }
        
        return response
    except Exception as e:
        logger.error(f"API测试失败: {str(e)}")
        
        # 构建错误响应
        response = {
            "status": "error",
            "message": "API测试失败",
            "timestamp": datetime.now().isoformat(),
            "astro_service_initialized": False,
            "engine_type": None,
            "using_real_engine": False,
            "test_result": None,
            "test_error": str(e)
        }
        
        return response 