# Utility functions for filters
from typing import Any, Dict, List, Optional

class SourceApplicationFilter:
    """杂鱼♡～通用源应用程序过滤器类喵～"""

    def __init__(
        self,
        allowed_processes: Optional[List[str]] = None,
        blocked_processes: Optional[List[str]] = None,
    ):
        """
        杂鱼♡～初始化源应用程序过滤器喵～

        Args:
            allowed_processes: 允许的进程名列表（例如：['notepad.exe', 'cursor.exe']）
            blocked_processes: 禁止的进程名列表
        """
        self.allowed_processes = [p.lower() for p in (allowed_processes or [])]
        self.blocked_processes = [p.lower() for p in (blocked_processes or [])]

    def __call__(self, data: Any, source_info: Optional[Dict[str, Any]] = None) -> bool:
        """
        杂鱼♡～根据源应用程序过滤数据喵～
        'data' anr 'source_info' are the standard arguments passed to filter callables.
        'data' is unused in this filter but included for compatibility.
        """
        if not source_info or not source_info.get("process_name"):
            # 杂鱼♡～如果没有源信息，或者源信息中没有进程名，默认允许喵～
            # 杂鱼♡～这确保了如果源跟踪失败或不可用，过滤器不会意外阻止所有内容喵～
            return True

        process_name = source_info["process_name"].lower()

        # 杂鱼♡～检查是否在禁止列表中喵～
        if self.blocked_processes and process_name in self.blocked_processes:
            return False

        # 杂鱼♡～如果有允许列表，检查是否在其中喵～
        # 杂鱼♡～如果允许列表为空，则表示除非被禁止，否则都允许喵～
        if self.allowed_processes:
            return process_name in self.allowed_processes

        # 杂鱼♡～如果既不在禁止列表，允许列表也为空，则允许喵～
        return True
