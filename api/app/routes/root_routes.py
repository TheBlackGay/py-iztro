"""
根路径API路由
"""
from fastapi import APIRouter

# 创建路由器
router = APIRouter()

# 根路径
@router.get("/")
def read_root():
    """API根路径，返回欢迎信息"""
    return {"message": "欢迎使用紫微斗数API服务"} 