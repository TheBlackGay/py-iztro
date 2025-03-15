"""
紫微斗数API服务主入口文件
"""
import logging
import os
import sys
import uvicorn
from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# 确保可以导入app包
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入应用程序组件
from api.app.routes import astro_routes, test_routes, root_routes, calendar_routes
from api.app.utils import setup_logging

# 配置日志
logger = setup_logging()

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

# 主入口
if __name__ == "__main__":
    try:
        # 启动服务
        logger.info("正在启动紫微斗数API服务...")
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as e:
        logger.error(f"服务启动失败: {e}", exc_info=True)
        sys.exit(1)
