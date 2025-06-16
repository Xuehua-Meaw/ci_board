# 杂鱼♡～事件驱动剪贴板监控示例喵～
"""
杂鱼♡～本喵给杂鱼主人演示新的事件驱动监控模式喵～
这个模式比轮询更高效，CPU占用更低，响应更及时喵～
"""

import sys
import os
import time

# 杂鱼♡～添加项目路径喵～
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ci_board.core.monitor import ClipboardMonitor


def main():
    print("杂鱼♡～事件驱动剪贴板监控示例喵～")
    print("=" * 50)

    # 杂鱼♡～创建监控器，启用事件驱动模式喵～
    monitor = ClipboardMonitor(
        async_processing=True,      # 杂鱼♡～启用异步处理喵～
        max_workers=2,              # 杂鱼♡～2个工作线程足够了喵～
        handler_timeout=10.0,       # 杂鱼♡～10秒超时喵～
        event_driven=True           # 杂鱼♡～启用事件驱动（推荐）喵～
    )

    # 杂鱼♡～添加文本处理器喵～
    def on_text_change(text_content, source_info=None):
        print("杂鱼♡～检测到文本变化喵～")
        print(f"  内容长度：{len(text_content)} 字符")
        print(f"  内容预览：{repr(text_content[:50])}{'...' if len(text_content) > 50 else ''}")
        if source_info:
            print(f"  源应用：{source_info.get('process_name', 'Unknown')}")
            if source_info.get('window_title'):
                print(f"  窗口标题：{source_info['window_title']}")
        print()

    # 杂鱼♡～添加图片处理器喵～
    def on_image_change(image_content, source_info=None):
        print("杂鱼♡～检测到图片变化喵～")
        if isinstance(image_content, dict):
            print(f"  图片格式：{image_content.get('format', 'Unknown')}")
            print(f"  图片尺寸：{image_content.get('width', 0)} x {image_content.get('height', 0)}")
            print(f"  色深：{image_content.get('bit_count', 0)} bit")
        if source_info:
            print(f"  源应用：{source_info.get('process_name', 'Unknown')}")
        print()

    # 杂鱼♡～添加通用更新处理器喵～
    def on_clipboard_update(content_data, source_info=None):
        content_type, content = content_data
        print(f"杂鱼♡～剪贴板更新喵～类型：{content_type}")
        if source_info:
            print(f"  检测方法：{source_info.get('detection_method', 'unknown')}")
            if source_info.get('note'):
                print(f"  备注：{source_info['note']}")
        print("-" * 30)

    # 杂鱼♡～注册处理器喵～
    monitor.add_handler('text', on_text_change)
    monitor.add_handler('image', on_image_change)
    monitor.add_handler('update', on_clipboard_update)

    # 杂鱼♡～显示当前配置喵～
    print("杂鱼♡～当前配置喵～")
    status = monitor.get_status()
    print(f"  监控模式：{status['monitoring_mode']}")
    print(f"  事件驱动：{status['event_driven']}")
    print(f"  异步处理：{status['async_stats']['async_enabled']}")
    print(f"  源追踪：{status['source_tracking_enabled']}")
    print()

    # 杂鱼♡～启动监控喵～
    if monitor.start():
        print("杂鱼♡～监控已启动，现在可以复制一些内容试试喵～")
        print("杂鱼♡～按 Ctrl+C 停止监控喵～")
        print()

        try:
            # 杂鱼♡～等待用户操作喵～
            monitor.wait()
        except KeyboardInterrupt:
            print("\n杂鱼♡～检测到用户中断喵～")
        finally:
            monitor.stop()
            print("杂鱼♡～监控已停止喵～")

            # 杂鱼♡～显示统计信息喵～
            final_stats = monitor.get_async_stats()
            print("\n杂鱼♡～最终统计喵～")
            print(f"  提交任务：{final_stats['tasks_submitted']}")
            print(f"  完成任务：{final_stats['tasks_completed']}")
            print(f"  失败任务：{final_stats['tasks_failed']}")
            print(f"  超时任务：{final_stats['tasks_timeout']}")
    else:
        print("杂鱼♡～启动监控失败了喵！")


def compare_modes():
    """杂鱼♡～比较两种监控模式的性能喵～"""
    print("\n杂鱼♡～监控模式对比喵～")
    print("=" * 50)

    modes = [
        ("轮询模式", False),
        ("事件驱动模式", True)
    ]

    for mode_name, event_driven in modes:
        print(f"\n测试 {mode_name}...")

        monitor = ClipboardMonitor(
            async_processing=False,  # 杂鱼♡～同步模式便于测试喵～
            event_driven=event_driven
        )

        changes_detected = 0

        def count_changes(content_data, source_info=None):
            nonlocal changes_detected
            changes_detected += 1

        monitor.add_handler('update', count_changes)

        if monitor.start():
            print(f"  {mode_name} 已启动，请在5秒内复制一些内容...")
            time.sleep(5)
            monitor.stop()
            print(f"  {mode_name} 检测到 {changes_detected} 次变化")
        else:
            print(f"  {mode_name} 启动失败")


if __name__ == "__main__":
    main()

    # 杂鱼♡～可选：运行性能对比喵～
    # compare_modes()
