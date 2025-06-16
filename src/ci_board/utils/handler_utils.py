# Utility functions for handlers
from typing import Any, Dict, List, Optional

def format_source_info_display(source_info: Optional[Dict[str, Any]]) -> List[str]:
    """
    Formats the source_info dictionary into a list of strings for display.
    """
    output_lines = []
    if not source_info:
        output_lines.append("  源应用程序：❓ 未知 (无详细信息)")
        return output_lines

    error_message = source_info.get("error")
    if error_message:
        output_lines.append(f"  源应用程序：❓ 未知 (无法获取)")
        output_lines.append(f"    原因：{error_message}")
        return output_lines

    process_name = source_info.get("process_name", "未知进程")
    detection_method = source_info.get("detection_method")
    note = source_info.get("note")

    if detection_method:
        output_lines.append(f"  源应用程序：🔄 {process_name} (推测)")
        output_lines.append(f"    检测方法：{detection_method}")
        if note:
            output_lines.append(f"    说明：{note}")
    else:
        output_lines.append(f"  源应用程序：{process_name}")

    process_path = source_info.get("process_path")
    if process_path:
        output_lines.append(f"  程序路径：{process_path}")

    window_title = source_info.get("window_title")
    if window_title:
        output_lines.append(f"  窗口标题：{window_title}")

    process_id = source_info.get("process_id")
    if process_id:
        output_lines.append(f"  进程ID：{process_id}")

    if not output_lines: # Should not happen if source_info is not None and not an error
        output_lines.append("  源应用程序：❓ 未知 (信息不完整)")

    return output_lines
