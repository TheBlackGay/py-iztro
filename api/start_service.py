#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
紫微斗数API服务启动脚本
"""

import logging
import traceback
import os
import sys
import subprocess

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("紫微斗数API启动脚本")

# 确保能够找到模块
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

if __name__ == "__main__":
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
        
        logger.info("正在启动紫微斗数API服务...")
        
        # 导入主模块并启动服务
        from main import main
        main()
    except Exception as e:
        logger.error(f"服务启动失败: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1) 