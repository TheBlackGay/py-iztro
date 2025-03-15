"""
响应模型定义
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class APIResponse(BaseModel):
    """API响应模型"""
    status: str = "ok"
    message: str = "计算成功"
    timestamp: str = datetime.now().isoformat()
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    class Config:
        """模型配置"""
        populate_by_name = True
        validate_assignment = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

    @classmethod
    def success(cls, result: Dict[str, Any], message: str = "计算成功"):
        """创建成功响应"""
        return cls(
            status="ok",
            message=message,
            timestamp=datetime.now().isoformat(),
            result=result
        )
    
    @classmethod
    def error(cls, error_message: str, error_detail: str = None):
        """创建错误响应"""
        return cls(
            status="error",
            message=f"计算失败: {error_message}",
            timestamp=datetime.now().isoformat(),
            error=error_detail or error_message
        )
    
    @classmethod
    def partial(cls, result: Dict[str, Any], error_message: str, error_detail: str = None):
        """创建部分成功响应"""
        return cls(
            status="partial",
            message=f"部分计算成功: {error_message}",
            timestamp=datetime.now().isoformat(),
            result=result,
            error=error_detail or error_message
        ) 