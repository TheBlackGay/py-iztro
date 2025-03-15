"""
紫微斗数计算服务
"""
import logging
from typing import Dict, Any, Tuple, Optional, Union
from datetime import datetime

from ..utils import safe_execute, handle_result, calculate_age
from .astro_provider import AstroProvider

# 日志记录器
logger = logging.getLogger("紫微斗数API")

class AstroService:
    """紫微斗数计算服务"""
    
    def __init__(self):
        """初始化紫微斗数计算服务"""
        self.engine, self.using_real_engine = AstroProvider.get_engine()
        logger.info(f"紫微斗数计算服务初始化完成，使用真实引擎: {self.using_real_engine}")
        # 保存本命盘原始对象的缓存
        self._natal_chart_cache = {}
        # 记录是否已经尝试过重新获取本命盘对象
        self._retry_attempted = set()
    
    def get_natal_chart(self, solar_date: str, time_index: int, gender: str, 
                        fix_leap: bool = True, language: str = "zh-CN") -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        获取本命盘
        
        Args:
            solar_date: 阳历日期，格式为YYYY-MM-DD或YYYY-M-D
            time_index: 出生时辰序号，0-12
            gender: 性别，"男"或"女"
            fix_leap: 是否调整闰月情况
            language: 输出语言
            
        Returns:
            (natal_chart, error): 本命盘数据和可能的错误信息
        """
        logger.info(f"计算本命盘: 日期={solar_date}, 时辰={time_index}, 性别={gender}")
        
        # 创建缓存键
        cache_key = f"{solar_date}_{time_index}_{gender}_{fix_leap}_{language}"
        
        # 安全执行本命盘计算
        natal_chart, error = safe_execute(
            self.engine.by_solar,
            solar_date, 
            time_index, 
            gender, 
            fix_leap, 
            language
        )
        
        if error:
            logger.error(f"计算本命盘失败: {error}")
            return None, error
        
        # 处理结果
        try:
            # 保存原始对象到缓存中，以便后续计算大限流年使用
            if self.using_real_engine:
                self._natal_chart_cache[cache_key] = natal_chart
            
            result = handle_result(natal_chart)
            return result, None
        except Exception as e:
            logger.error(f"处理本命盘结果失败: {str(e)}")
            return None, str(e)
    
    def get_horoscope(self, natal_chart: Dict[str, Any], target_date: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        获取大限流年
        
        Args:
            natal_chart: 本命盘数据
            target_date: 目标日期，格式为YYYY-MM-DD或YYYY-M-D
            
        Returns:
            (horoscope, error): 大限流年数据和可能的错误信息
        """
        logger.info(f"计算大限流年: 目标日期={target_date}")
        
        # 如果使用的是模拟数据引擎，则生成模拟大限流年数据
        if not self.using_real_engine:
            logger.warning("使用模拟数据引擎，生成模拟大限流年数据")
            return self._generate_mock_horoscope(natal_chart, target_date)
        
        try:
            # 获取必要的参数
            solar_date = natal_chart.get("solarDate")
            time_index = natal_chart.get("time")
            gender = natal_chart.get("gender")
            
            if not all([solar_date, time_index is not None, gender]):
                logger.error("本命盘数据缺少必要参数")
                return None, "本命盘数据缺少必要参数"
            
            # 创建缓存键
            cache_key = f"{solar_date}_{time_index}_{gender}_True_zh-CN"
            retry_key = f"{cache_key}_{target_date}"
            
            # 检查是否已经尝试过重新获取本命盘对象
            if retry_key in self._retry_attempted:
                logger.warning(f"已经尝试过重新获取本命盘对象，直接返回基本信息: {retry_key}")
                return self._generate_mock_horoscope(natal_chart, target_date, "已尝试重新获取本命盘对象但失败，返回基本信息")
            
            # 检查是否有缓存的命盘对象
            original_chart = self._natal_chart_cache.get(cache_key)
            
            if original_chart is None:
                logger.warning("缓存中没有找到本命盘对象，重新获取")
                # 标记已尝试重新获取
                self._retry_attempted.add(retry_key)
                
                # 重新获取本命盘对象
                original_chart, error = safe_execute(
                    self.engine.by_solar,
                    solar_date, 
                    time_index, 
                    gender
                )
                
                if error:
                    logger.error(f"重新获取本命盘对象失败: {error}")
                    return self._generate_mock_horoscope(natal_chart, target_date, f"无法重新获取本命盘对象: {error}")
            
            # 在本命盘对象上调用horoscope方法，参考daxian.py的调用方式
            logger.info("在本命盘对象上调用horoscope方法")
            horoscope_data, error = safe_execute(
                original_chart.horoscope,
                target_date,
                0  # 使用默认的运限类型
            )
            
            if error:
                logger.error(f"计算大限流年失败: {error}")
                return self._generate_mock_horoscope(natal_chart, target_date, f"计算大限流年失败: {error}")
            
            # 处理结果
            result = handle_result(horoscope_data)
            return result, None
            
        except Exception as e:
            logger.error(f"处理大限流年计算失败: {str(e)}")
            return self._generate_mock_horoscope(natal_chart, target_date, f"处理大限流年计算失败: {str(e)}")
    
    def _generate_mock_horoscope(self, natal_chart: Dict[str, Any], target_date: str, error_message: str = None) -> Tuple[Dict[str, Any], Optional[str]]:
        """
        生成模拟的大限流年数据
        
        Args:
            natal_chart: 本命盘数据
            target_date: 目标日期
            error_message: 错误信息
            
        Returns:
            (mock_data, error): 模拟数据和可能的错误信息
        """
        # 获取出生日期和年龄
        solar_date = natal_chart.get("solarDate", "2000-1-1")
        age = calculate_age(solar_date, target_date)
        
        # 创建模拟数据
        mock_data = {
            "target_date": target_date,
            "age": age,
            "message": error_message or "注意：这是模拟数据，无法获取完整大限流年信息",
            "horoscope_data": []
        }
        
        return mock_data, error_message
    
    def get_complete_horoscope(self, solar_date: str, time_index: int, gender: str, 
                              target_date: str, fix_leap: bool = True, 
                              language: str = "zh-CN") -> Dict[str, Any]:
        """
        获取完整的星盘和大限流年数据
        
        Args:
            solar_date: 阳历日期，格式为YYYY-MM-DD或YYYY-M-D
            time_index: 出生时辰序号，0-12
            gender: 性别，"男"或"女"
            target_date: 目标日期，格式为YYYY-MM-DD或YYYY-M-D
            fix_leap: 是否调整闰月情况
            language: 输出语言
            
        Returns:
            包含结果状态、数据和错误信息的字典
        """
        # 获取本命盘
        natal_chart, natal_error = self.get_natal_chart(
            solar_date, time_index, gender, fix_leap, language
        )
        
        if natal_error:
            return {
                "status": "error",
                "message": f"计算本命盘失败: {natal_error}",
                "natal_chart": None,
                "horoscope": None,
                "error": natal_error
            }
        
        # 获取大限流年
        horoscope_data, horoscope_error = self.get_horoscope(natal_chart, target_date)
        
        if horoscope_error:
            # 如果大限流年计算失败，但本命盘成功，返回部分成功响应
            # 计算年龄作为替代信息
            age = calculate_age(solar_date, target_date)
            
            fallback_horoscope = {
                "target_date": target_date,
                "age": age,
                "error": horoscope_error,
                "message": "大限流年计算失败，仅返回基本信息"
            }
            
            return {
                "status": "partial",
                "message": f"本命盘计算成功，但大限流年计算失败: {horoscope_error}",
                "natal_chart": natal_chart,
                "horoscope": fallback_horoscope,
                "error": horoscope_error
            }
        
        # 两者都成功
        return {
            "status": "ok",
            "message": "计算成功",
            "natal_chart": natal_chart,
            "horoscope": horoscope_data,
            "error": None
        } 