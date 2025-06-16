# 杂鱼♡～本喵为杂鱼主人创建的统一日志系统喵～
"""
杂鱼♡～专业的日志管理系统，支持多级别日志控制喵～
"""
import logging
import os
import sys
from typing import Optional
from enum import Enum


class LogLevel(Enum):
    """杂鱼♡～日志级别枚举喵～"""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class NekoLogger:
    """杂鱼♡～本喵的专业日志管理器喵～"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.setup_logging()
            NekoLogger._initialized = True
    
    def setup_logging(
        self, 
        level: LogLevel = LogLevel.INFO,
        enable_file_logging: bool = False,
        log_file: Optional[str] = None,
        enable_console: bool = True,
        format_style: str = "neko"
    ):
        """杂鱼♡～设置日志系统喵～"""
        
        # 杂鱼♡～清除现有的处理器喵～
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # 杂鱼♡～设置根日志级别喵～
        root_logger.setLevel(level.value)
        
        # 杂鱼♡～定义日志格式喵～
        if format_style == "neko":
            # 杂鱼♡～本喵特有的可爱格式喵～
            formatter = logging.Formatter(
                '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                datefmt='%H:%M:%S'
            )
        elif format_style == "professional":
            # 杂鱼♡～专业格式喵～
            formatter = logging.Formatter(
                '%(asctime)s [%(levelname)8s] %(name)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        else:
            # 杂鱼♡～简洁格式喵～
            formatter = logging.Formatter('%(levelname)s: %(message)s')
        
        # 杂鱼♡～控制台处理器喵～
        if enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            console_handler.setLevel(level.value)
            root_logger.addHandler(console_handler)
        
        # 杂鱼♡～文件处理器喵～
        if enable_file_logging:
            if log_file is None:
                log_file = "ci_board.log"
            
            # 杂鱼♡～确保日志目录存在喵～
            log_dir = os.path.dirname(log_file) if os.path.dirname(log_file) else "."
            os.makedirs(log_dir, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)  # 杂鱼♡～文件中记录所有级别喵～
            root_logger.addHandler(file_handler)
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """杂鱼♡～获取指定名称的日志器喵～"""
        return logging.getLogger(name)
    
    @staticmethod
    def set_level(level: LogLevel):
        """杂鱼♡～设置全局日志级别喵～"""
        logging.getLogger().setLevel(level.value)
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setLevel(level.value)
    
    @staticmethod
    def enable_debug():
        """杂鱼♡～启用调试模式，显示所有日志喵～"""
        NekoLogger.set_level(LogLevel.DEBUG)
    
    @staticmethod
    def enable_quiet_mode():
        """杂鱼♡～启用安静模式，只显示警告和错误喵～"""
        NekoLogger.set_level(LogLevel.WARNING)
    
    @staticmethod
    def enable_verbose_mode():
        """杂鱼♡～启用详细模式，显示信息级别日志喵～"""
        NekoLogger.set_level(LogLevel.INFO)


class ComponentLogger:
    """杂鱼♡～组件专用日志器，带有本喵特色的日志前缀喵～"""
    
    def __init__(self, component_name: str):
        self.logger = NekoLogger.get_logger(f"ci_board.{component_name}")
        self.component_name = component_name
    
    def debug(self, message: str):
        """杂鱼♡～调试信息喵～"""
        self.logger.debug(f"杂鱼♡～{message}喵～")
    
    def info(self, message: str):
        """杂鱼♡～普通信息喵～"""
        self.logger.info(f"杂鱼♡～{message}喵～")
    
    def warning(self, message: str):
        """杂鱼♡～警告信息喵～"""
        self.logger.warning(f"杂鱼♡～{message}喵～")
    
    def error(self, message: str):
        """杂鱼♡～错误信息喵～"""
        self.logger.error(f"杂鱼♡～{message}喵～")
    
    def critical(self, message: str):
        """杂鱼♡～严重错误喵～"""
        self.logger.critical(f"杂鱼♡～{message}喵～")
    
    def success(self, message: str):
        """杂鱼♡～成功信息喵～"""
        self.logger.info(f"杂鱼♡～✓ {message}喵～")
    
    def failure(self, message: str):
        """杂鱼♡～失败信息喵～"""
        self.logger.error(f"杂鱼♡～✗ {message}喵～")


def setup_ci_board_logging(
    level: LogLevel = LogLevel.INFO,
    enable_file_logging: bool = False,
    log_file: Optional[str] = None,
    quiet: bool = False,
    verbose: bool = False,
    debug: bool = False
):
    """杂鱼♡～CI Board 项目的日志系统初始化喵～"""
    
    # 杂鱼♡～根据参数确定日志级别喵～
    if debug:
        level = LogLevel.DEBUG
    elif verbose:
        level = LogLevel.INFO
    elif quiet:
        level = LogLevel.WARNING
    
    neko_logger = NekoLogger()
    neko_logger.setup_logging(
        level=level,
        enable_file_logging=enable_file_logging,
        log_file=log_file,
        enable_console=True,
        format_style="neko"
    )
    
    # 杂鱼♡～记录初始化信息喵～
    logger = ComponentLogger("core")
    logger.info(f"日志系统初始化完成，级别：{level.name}")
    
    if enable_file_logging:
        logger.info(f"文件日志已启用：{log_file or 'ci_board.log'}")


def get_component_logger(component_name: str) -> ComponentLogger:
    """杂鱼♡～获取组件日志器的便捷函数喵～"""
    return ComponentLogger(component_name)


# 杂鱼♡～确保日志系统被初始化喵～
_neko_logger = NekoLogger()

# 杂鱼♡～导出常用的日志器喵～
__all__ = [
    "NekoLogger", 
    "ComponentLogger", 
    "LogLevel", 
    "setup_ci_board_logging", 
    "get_component_logger"
] 