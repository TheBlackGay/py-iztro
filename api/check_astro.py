#!/usr/bin/env python
"""
检查py_iztro.Astro类的可用方法
"""
import sys

try:
    from py_iztro import Astro
    
    astro = Astro()
    print("Astro类初始化成功")
    
    # 列出非私有方法
    methods = [m for m in dir(astro) if not m.startswith('_')]
    print(f"可用方法: {methods}")
    
    # 检查特定方法
    if hasattr(astro, 'by_solar'):
        print("存在by_solar方法")
    
    if hasattr(astro, 'horoscope'):
        print("存在horoscope方法")
    else:
        print("不存在horoscope方法")
        
        # 尝试查找类似的方法
        similar_methods = [m for m in methods if 'horo' in m.lower() or 'destiny' in m.lower() or 'fortune' in m.lower() or 'flow' in m.lower() or 'fate' in m.lower()]
        if similar_methods:
            print(f"可能相关的方法: {similar_methods}")
    
except ImportError as e:
    print(f"导入错误: {e}")
except Exception as e:
    print(f"其他错误: {e}") 