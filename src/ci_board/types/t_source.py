# 杂鱼♡～本喵定义的源应用程序相关类型喵～
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import time


@dataclass
class ProcessInfo:
    """杂鱼♡～进程信息结构体喵～"""
    name: str
    path: str
    pid: int


@dataclass
class WindowInfo:
    """杂鱼♡～窗口信息结构体喵～"""
    title: str
    class_name: str
    hwnd: int


@dataclass
class SourceInfo:
    """杂鱼♡～源应用程序完整信息喵～"""
    process: ProcessInfo
    window: WindowInfo
    focus_time: float
    confidence_level: str
    
    def to_dict(self) -> Dict[str, Any]:
        """杂鱼♡～转换为字典格式喵～"""
        return {
            'process': {
                'name': self.process.name,
                'path': self.process.path,
                'pid': self.process.pid
            },
            'window': {
                'title': self.window.title,
                'class_name': self.window.class_name,
                'hwnd': self.window.hwnd
            },
            'focus_time': self.focus_time,
            'confidence_level': self.confidence_level
        }


@dataclass
class FocusEvent:
    """杂鱼♡～焦点切换事件喵～"""
    source_info: SourceInfo
    timestamp: float
    event_type: str  # "focus_gained", "focus_lost"
    
    def __post_init__(self):
        if self.timestamp == 0:
            self.timestamp = time.time()

