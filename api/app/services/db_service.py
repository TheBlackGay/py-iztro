"""
数据库服务 - 处理紫微斗数命盘数据的存储和查询
"""
import logging
import json
import pymysql
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

# 日志记录器
logger = logging.getLogger("紫微斗数API")

class DBService:
    """数据库服务 - 处理命盘数据的存储和查询"""
    
    def __init__(self):
        """初始化数据库连接配置"""
        self.db_config = {
            'host': 'localhost',
            'port': 13306,
            'user': 'root',
            'password': 'sally',
            'database': 'py_iztro',
            'charset': 'utf8mb4'
        }
        logger.info("数据库服务初始化完成")
    
    def get_connection(self):
        """获取数据库连接"""
        try:
            connection = pymysql.connect(**self.db_config)
            return connection
        except Exception as e:
            logger.error(f"数据库连接失败: {str(e)}")
            raise Exception(f"数据库连接失败: {str(e)}")
    
    def check_astro_data_exists(self, solar_date: str, time_index: int, gender: str) -> Optional[int]:
        """
        检查命盘数据是否已存在
        
        Args:
            solar_date: 阳历日期，格式为YYYY-MM-DD
            time_index: 出生时辰序号
            gender: 性别
            
        Returns:
            存在则返回记录ID，不存在则返回None
        """
        # 格式化日期为yyyyMMdd
        formatted_date = solar_date.replace('-', '')
        
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                sql = """
                SELECT id FROM iztro_astro 
                WHERE solar_date = %s AND time_index = %s AND gender = %s
                LIMIT 1
                """
                cursor.execute(sql, (formatted_date, time_index, gender))
                result = cursor.fetchone()
                
                if result:
                    return result[0]  # 返回ID
                return None
        except Exception as e:
            logger.error(f"检查命盘数据是否存在失败: {str(e)}")
            return None
        finally:
            if conn:
                conn.close()
    
    def save_astro_data(self, solar_date: str, time_index: int, gender: str, 
                        astro_data: Dict[str, Any], fix_leap: bool = True, 
                        language: str = "zh-CN", create_user: str = "system") -> int:
        """
        保存命盘数据到数据库
        
        Args:
            solar_date: 阳历日期，格式为YYYY-MM-DD
            time_index: 出生时辰序号
            gender: 性别
            astro_data: 命盘数据
            fix_leap: 是否调整闰月情况
            language: 输出语言
            create_user: 创建用户
            
        Returns:
            新增记录的ID或已存在记录的ID
        """
        # 先检查是否已存在相同的命盘数据
        existing_id = self.check_astro_data_exists(solar_date, time_index, gender)
        if existing_id:
            logger.info(f"命盘数据已存在，ID: {existing_id}，不再重复插入")
            # 可选：更新已有记录的数据
            try:
                self.update_astro_data(
                    existing_id, 
                    {
                        'astro_data': astro_data,
                        'fix_leap': fix_leap,
                        'language': language
                    }, 
                    update_user=create_user
                )
                logger.info(f"已更新现有命盘数据，ID: {existing_id}")
            except Exception as e:
                logger.warning(f"更新现有命盘数据失败: {str(e)}")
            
            return existing_id
            
        # 格式化日期为yyyyMMdd
        formatted_date = solar_date.replace('-', '')
        fix_leap_int = 1 if fix_leap else 0
        
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                # 转换命盘数据为JSON字符串
                astro_json = json.dumps(astro_data, ensure_ascii=False)
                
                sql = """
                INSERT INTO iztro_astro 
                (solar_date, time_index, gender, fix_leap, language, astro_data, create_user, update_user) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    formatted_date, 
                    time_index, 
                    gender, 
                    fix_leap_int, 
                    language, 
                    astro_json, 
                    create_user, 
                    create_user
                ))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"保存命盘数据失败: {str(e)}")
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
                
    def update_astro_data(self, astro_id: int, update_data: Dict[str, Any], update_user: str = "system") -> bool:
        """
        更新命盘数据
        
        Args:
            astro_id: 命盘数据ID
            update_data: 要更新的数据
            update_user: 更新用户
            
        Returns:
            是否更新成功
        """
        conn = None
        try:
            conn = self.get_connection()
            
            # 构建更新字段
            update_fields = []
            params = []
            
            if 'solar_date' in update_data:
                update_fields.append("solar_date = %s")
                params.append(update_data['solar_date'].replace('-', ''))
                
            if 'time_index' in update_data:
                update_fields.append("time_index = %s")
                params.append(update_data['time_index'])
                
            if 'gender' in update_data:
                update_fields.append("gender = %s")
                params.append(update_data['gender'])
                
            if 'fix_leap' in update_data:
                update_fields.append("fix_leap = %s")
                params.append(1 if update_data['fix_leap'] else 0)
                
            if 'language' in update_data:
                update_fields.append("language = %s")
                params.append(update_data['language'])
                
            if 'astro_data' in update_data:
                update_fields.append("astro_data = %s")
                astro_json = json.dumps(update_data['astro_data'], ensure_ascii=False)
                params.append(astro_json)
                
            # 添加更新时间和用户
            update_fields.append("update_time = %s")
            params.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            
            update_fields.append("update_user = %s")
            params.append(update_user)
            
            if not update_fields:
                logger.warning("没有要更新的字段")
                return False
                
            # 执行更新
            with conn.cursor() as cursor:
                sql = f"""
                UPDATE iztro_astro 
                SET {', '.join(update_fields)} 
                WHERE id = %s
                """
                params.append(astro_id)
                affected_rows = cursor.execute(sql, params)
                conn.commit()
                
                return affected_rows > 0
        except Exception as e:
            logger.error(f"更新命盘数据失败: {str(e)}")
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close() 