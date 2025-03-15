#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
紫微斗数API服务主入口文件
"""
import logging
import os
import sys
import traceback
import subprocess
import uvicorn
from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("紫微斗数API")

# 确保可以导入app包
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

def check_dependencies():
    """检查依赖项"""
    try:
        # 尝试导入关键依赖
        import fastapi
        import uvicorn
        import pydantic
        
        # 尝试导入py_iztro（可选）
        try:
            import py_iztro
            logger.info(f"检测到py_iztro库，版本: {getattr(py_iztro, '__version__', '未知')}")
        except ImportError:
            logger.warning("未检测到py_iztro库，将使用模拟数据模式运行")
            
        return True
    except ImportError as e:
        logger.warning(f"缺少关键依赖: {str(e)}")
        return False
    
def install_requirements():
    """安装依赖项"""
    logger.info("正在安装依赖项...")
    requirements_file = os.path.join(current_dir, "requirements.txt")
    
    if not os.path.exists(requirements_file):
        logger.error(f"未找到依赖文件: {requirements_file}")
        return False
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        logger.info("依赖项安装成功")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"安装依赖项失败: {str(e)}")
        return False

# 导入应用程序组件 - 在检查依赖后再导入
from api.app.utils import setup_logging
# 使用我们自己的日志配置
logger = setup_logging()

# 导入路由组件
from api.app.routes import astro_routes, test_routes, root_routes, calendar_routes

# 创建FastAPI应用
app = FastAPI(
    title="紫微斗数API",
    description="提供紫微斗数命盘和大限流年计算的API服务",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    logger.error(f"全局异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": f"服务器内部错误: {str(exc)}"}
    )

# 添加根路由
app.include_router(root_routes.router)

# 创建总的API路由器，添加/api前缀
api_router = APIRouter(prefix="/api")

# 将子路由器添加到API路由器
api_router.include_router(astro_routes.router)
api_router.include_router(test_routes.router)
api_router.include_router(calendar_routes.router, prefix="/calendar")

# 将API路由器添加到应用
app.include_router(api_router)

# 应用启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时的事件处理"""
    logger.info("紫微斗数API服务启动")

# 应用关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的事件处理"""
    logger.info("紫微斗数API服务关闭")

def main():
    """
    API服务主入口函数
    用于启动紫微斗数API服务
    """
    try:
        # 检查并安装依赖
        if not check_dependencies():
            logger.info("尝试安装依赖...")
            if install_requirements():
                logger.info("依赖安装成功")
                if not check_dependencies():
                    logger.warning("依赖检查失败，但将尝试继续运行")
            else:
                logger.warning("依赖安装失败，但将尝试继续运行")
                
        # 启动服务
        logger.info("正在启动紫微斗数API服务...")
        uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as e:
        logger.error(f"服务启动失败: {e}", exc_info=True)
        logger.error(traceback.format_exc())
        sys.exit(1)

# 主入口
if __name__ == "__main__":
    main()
