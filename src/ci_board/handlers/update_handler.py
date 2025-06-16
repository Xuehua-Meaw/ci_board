from typing import Any, Dict, Optional

from ..interfaces.callback_interface import BaseClipboardHandler


class SimpleUpdateHandler(BaseClipboardHandler):
    """杂鱼♡～简单的更新处理器喵～"""

    def __init__(self, callback=None):
        super().__init__(callback)

    def is_valid(self, data: Any) -> bool:
        return True

    def _default_handle(
        self, data: Any, source_info: Optional[Dict[str, Any]] = None
    ) -> None:
        """杂鱼♡～默认的更新处理方法喵～"""
        content_type, content = data
        print(f"杂鱼♡～剪贴板内容更新了喵～类型：{content_type}")

        # 杂鱼♡～显示源应用程序信息喵～
        if source_info and self._include_source_info:
            print(f"  源应用程序：{source_info.get('process_name', 'Unknown')}")
            if source_info.get('process_path'):
                print(f"  程序路径：{source_info['process_path']}")
            if source_info.get('window_title'):
                print(f"  窗口标题：{source_info['window_title']}")
