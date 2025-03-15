"""
紫微斗数计算服务提供者
"""
import logging
import sys
from datetime import datetime
from typing import Dict, Any, Tuple, Optional, Union
import json
import os
import traceback

# 日志记录器
logger = logging.getLogger("紫微斗数API")

# 全局实例缓存
_astro_instances = {}
_astro_results_cache = {}
_engine_instance = None
_engine_is_real = None

# 模拟的紫微斗数计算引擎
class MockAstroEngine:
    """模拟的紫微斗数计算引擎，当无法使用真实引擎时使用"""

    def __init__(self):
        """初始化模拟引擎"""
        logger.info("初始化模拟紫微斗数计算引擎")

    def by_solar(self, solar_date: str, time_index: int, gender: str,
                 fix_leap: bool = True, language: str = "zh-CN") -> Dict[str, Any]:
        """
        模拟通过阳历获取星盘

        Args:
            solar_date: 阳历日期，格式为YYYY-MM-DD或YYYY-M-D
            time_index: 出生时辰序号，0-12
            gender: 性别，"男"或"女"
            fix_leap: 是否调整闰月情况,true、false
            language: 输出语言

        Returns:
            模拟的星盘数据
        """
        # 返回模拟数据
        birth_year = int(solar_date.split('-')[0])
        current_year = datetime.now().year
        age = current_year - birth_year

        return {
            "gender": gender,
            "solarDate": solar_date,
            "lunarDate": f"模拟农历日期-{solar_date}",
            "chineseDate": f"模拟中文日期-{solar_date}",
            "time": time_index,
            "timeRange": f"模拟时辰范围-{time_index}",
            "age": age,
            "message": "注意：这是模拟数据，因为无法导入py_iztro库",
            "palaces": []
        }

    def horoscope(self, natal_chart: Dict[str, Any], target_date: str) -> Dict[str, Any]:
        """
        模拟大限流年计算

        Args:
            natal_chart: 本命盘数据
            target_date: 目标日期，格式为YYYY-MM-DD或YYYY-M-D

        Returns:
            模拟的大限流年数据
        """
        # 从命盘获取出生日期
        solar_date = natal_chart.get("solarDate", "2000-1-1")
        birth_year = int(solar_date.split('-')[0])

        # 从目标日期获取年份
        target_year = int(target_date.split('-')[0])
        age = target_year - birth_year

        return {
            "target_date": target_date,
            "age": age,
            "message": "注意：这是模拟数据，因为无法导入py_iztro库",
            "horoscope_data": []
        }

class AstroProvider:
    """紫微斗数计算服务提供者，用于获取不同的计算引擎"""

    def __init__(self):
        """初始化"""
        self.use_real_engine = True

        try:
            # 尝试导入紫微斗数库
            from py_iztro import Astro
            logger.info("成功导入py_iztro库")
            self.use_real_engine = True
        except ImportError:
            logger.warning("无法导入py_iztro库，将使用模拟数据引擎")
            self.use_real_engine = False
            self._init_mock_engine()

    @staticmethod
    def get_engine():
        """
        获取紫微斗数计算引擎（带缓存）

        Returns:
            (engine, is_real_engine): 引擎实例和是否为真实引擎的标志
        """
        global _engine_instance, _engine_is_real

        # 如果已有缓存的引擎实例，直接返回
        if _engine_instance is not None:
            logger.info("获取到py_iztro库缓存实例")
            return _engine_instance, _engine_is_real

        # 否则创建新的引擎实例
        try:
            from py_iztro import Astro
            logger.info("成功导入py_iztro库，创建Astro实例")
            _engine_instance = Astro()
            _engine_is_real = True
        except ImportError:
            logger.warning("无法导入py_iztro库，将使用模拟数据引擎")
            # 使用已存在的MockAstroEngine类
            _engine_instance = MockAstroEngine()
            _engine_is_real = False

        return _engine_instance, _engine_is_real

    def _init_mock_engine(self):
        """初始化模拟紫微斗数计算引擎"""
        logger.info("初始化模拟紫微斗数计算引擎")

    def _get_cache_key(self, solar_date: str, time_index: int, gender: str) -> str:
        """
        获取缓存键

        Args:
            solar_date: 阳历日期（格式：YYYY-MM-DD）
            time_index: 时辰索引
            gender: 性别

        Returns:
            缓存键
        """
        return f"{solar_date}_{time_index}_{gender}"

    def _get_horoscope_cache_key(self, solar_date: str, time_index: int, gender: str, target_date: str) -> str:
        """
        获取大限流年缓存键

        Args:
            solar_date: 阳历日期（格式：YYYY-MM-DD）
            time_index: 时辰索引
            gender: 性别
            target_date: 目标日期

        Returns:
            缓存键
        """
        return f"{solar_date}_{time_index}_{gender}_{target_date}"

    def get_astrolabe(self, solar_date: str, time_index: int, gender: str,
                      fix_leap: bool = True, lang: str = "zh-CN") -> Tuple[Optional[Dict], Optional[str]]:
        """
        获取紫微斗数命盘

        Args:
            solar_date: 阳历日期（格式：YYYY-MM-DD）
            time_index: 时辰索引
            gender: 性别
            fix_leap: 是否修复闰月
            lang: 语言

        Returns:
            (result, error): 结果和可能的错误
        """
        cache_key = self._get_cache_key(solar_date, time_index, gender)

        # 检查缓存
        if cache_key in _astro_results_cache:
            logger.info(f"命盘数据缓存命中: {cache_key}")
            return _astro_results_cache[cache_key], None

        try:
            if self.use_real_engine:
                # 使用真实紫微斗数引擎
                astro_instance = self._get_or_create_astro_instance(solar_date, time_index, gender, fix_leap, lang)
                astrolabe = astro_instance.get_astrolabe()

                # 转换为字典并缓存结果
                result = json.loads(json.dumps(astrolabe, default=lambda o: o.__dict__))
                _astro_results_cache[cache_key] = result

                return result, None
            else:
                # 使用模拟数据
                logger.warning("使用模拟数据引擎，生成模拟命盘数据")
                mock_data = self._generate_mock_astrolabe_data(solar_date, time_index, gender)

                # 缓存结果
                _astro_results_cache[cache_key] = mock_data

                return mock_data, None

        except Exception as e:
            logger.error(f"获取紫微斗数命盘失败: {str(e)}")
            logger.error(traceback.format_exc())
            return None, f"计算紫微斗数命盘失败: {str(e)}"

    def _get_or_create_astro_instance(self, solar_date: str, time_index: int, gender: str,
                                     fix_leap: bool = True, lang: str = "zh-CN"):
        """
        获取或创建Astro实例（使用缓存）

        Args:
            solar_date: 阳历日期（格式：YYYY-MM-DD）
            time_index: 时辰索引
            gender: 性别
            fix_leap: 是否修复闰月
            lang: 语言

        Returns:
            Astro实例
        """
        cache_key = self._get_cache_key(solar_date, time_index, gender)

        if cache_key not in _astro_instances:
            from py_iztro import Astro
            _astro_instances[cache_key] = Astro(
                solar_date=solar_date,
                time_index=time_index,
                gender=gender,
                fix_leap=fix_leap,
                lang=lang
            )

        return _astro_instances[cache_key]

    def get_horoscope(self, solar_date: str, time_index: int, target_time_index: int,
                      gender: str, target_date: str, fix_leap: bool = True,
                      lang: str = "zh-CN") -> Tuple[Optional[Dict], Optional[str]]:
        """
        获取大限流年

        Args:
            solar_date: 阳历日期（格式：YYYY-MM-DD）
            time_index: 时辰索引
            target_time_index: 目标时辰索引
            gender: 性别
            target_date: 目标日期
            fix_leap: 是否修复闰月
            lang: 语言

        Returns:
            (result, error): 结果和可能的错误
        """
        horoscope_cache_key = self._get_horoscope_cache_key(solar_date, time_index, gender, target_date)

        # 检查缓存
        if horoscope_cache_key in _astro_results_cache:
            logger.info(f"大限流年数据缓存命中: {horoscope_cache_key}")
            return _astro_results_cache[horoscope_cache_key], None

        try:
            if self.use_real_engine:
                # 使用真实紫微斗数引擎
                astro_instance = self._get_or_create_astro_instance(solar_date, time_index, gender, fix_leap, lang)
                horoscope = astro_instance.get_horoscope(target_date)

                # 转换为字典并缓存结果
                result = json.loads(json.dumps(horoscope, default=lambda o: o.__dict__))
                _astro_results_cache[horoscope_cache_key] = result

                return result, None
            else:
                # 使用模拟数据
                logger.warning("使用模拟数据引擎，生成模拟大限流年数据")
                mock_data = self._generate_mock_horoscope_data(solar_date, time_index, gender, target_date)

                # 缓存结果
                _astro_results_cache[horoscope_cache_key] = mock_data

                return mock_data, None

        except Exception as e:
            logger.error(f"获取大限流年失败: {str(e)}")
            logger.error(traceback.format_exc())
            return None, f"计算大限流年失败: {str(e)}"

    def _generate_mock_astrolabe_data(self, solar_date: str, time_index: int, gender: str) -> Dict:
        """生成模拟命盘数据"""
        return {
            "solar_date": solar_date,
            "lunar_date": "模拟农历日期",
            "time_index": time_index,
            "gender": gender,
            "palaces": [
                {"palace_name": "命宫", "stars": ["紫微", "天机"]},
                {"palace_name": "财帛", "stars": ["武曲", "天相"]},
                # ... 其他宫位
            ],
            # ... 其他数据
        }

    def _generate_mock_horoscope_data(self, solar_date: str, time_index: int, gender: str, target_date: str) -> Dict:
        """生成模拟大限流年数据"""
        return {
            "solar_date": solar_date,
            "time_index": time_index,
            "gender": gender,
            "target_date": target_date,
            "age": 30,  # 模拟年龄
            "palaces": [
                {"palace_name": "命宫", "stars": ["流年紫微", "流年天机"]},
                {"palace_name": "财帛", "stars": ["流年武曲", "流年天相"]},
                # ... 其他宫位
            ],
            # ... 其他数据
        }
