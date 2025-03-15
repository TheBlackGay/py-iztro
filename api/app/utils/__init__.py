"""
工具函数包
"""
from .logging_setup import setup_logging
from .error_handlers import setup_signal_handlers, safe_execute
from .result_handlers import handle_result, calculate_age

__all__ = [
    'setup_logging',
    'setup_signal_handlers',
    'safe_execute',
    'handle_result',
    'calculate_age'
] 