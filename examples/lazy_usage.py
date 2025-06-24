# 杂鱼♡～本喵的懒人API使用示例喵～
import os
import sys
import time

# 杂鱼♡～杂鱼主人的路径设置，本喵勉强帮你修复了喵～
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# 杂鱼♡～设置日志级别（可以改为quiet=True来减少输出）喵～
from ci_board.utils.logger import LogLevel, setup_ci_board_logging, get_logger

setup_ci_board_logging(
    console_level=LogLevel.WARNING
)  # 杂鱼♡～可以改为LogLevel.INFO来减少输出喵～

from ci_board import BMPData, ProcessInfo, create_monitor


def on_text_change(text, source_info: ProcessInfo):
    """杂鱼♡～文本变化回调函数（支持源信息）喵～"""
    print("杂鱼♡～检测到文本变化喵：")
    print(f"{'-'*50}")
    for line in text.split('\n'):
        print(f"{line}")
    print(f"{'-'*50}")

    # 杂鱼♡～显示源应用程序信息喵～
    print(f"杂鱼♡～源应用程序信息：{source_info}")

    print("-" * 50)


def on_image_change(bData: BMPData, source_info: ProcessInfo):
    """杂鱼♡～图片变化回调函数（支持源信息）喵～"""
    # print("杂鱼♡～检测到图片变化喵～")
    # print(f"数据类型：{type(data)}")
    if bData.success:
        try:
            # import io

            # from PIL import Image

            # image = Image.open(io.BytesIO(bData.data))
            # print(f"杂鱼♡～成功打开图片：{image.width} {image.height}喵～")
            # print(f"杂鱼♡～BMP数据大小：{len(bData.data)}字节喵～")
            print(f"杂鱼♡～BMPData尺寸：{bData.width}x{bData.height}喵～")
            # image.show()
            print(f"杂鱼♡～源应用程序信息：{source_info}")
        except Exception as e:
            print(f"杂鱼♡～PIL打开失败喵：{e}")
    else:
        if bData.data:
            print(f"杂鱼♡～BMP转换失败，返回原始数据{len(bData.data)}字节喵～")
        else:
            print("杂鱼♡～BMP转换失败，数据为空喵～")

    # 杂鱼♡～显示源应用程序信息喵～
    if source_info:
        print(f"  源应用程序：{source_info.process_name or 'Unknown'}")
        if source_info.process_path:
            print(f"  程序路径：{source_info.process_path}")
        if source_info.window_title:
            print(f"  窗口标题：{source_info.window_title}")
    print("-" * 50)


def on_files_change(files, source_info: ProcessInfo):
    """杂鱼♡～文件变化回调函数（支持源信息）喵～"""
    print(f"杂鱼♡～检测到文件变化喵：{files}")

    # 杂鱼♡～显示源应用程序信息喵～
    print(f"杂鱼♡～源应用程序信息：{source_info}")


def on_clipboard_update(data, source_info: ProcessInfo):
    """杂鱼♡～剪贴板更新回调函数（支持源信息）喵～"""
    content_type, content = data
    print(f"杂鱼♡～剪贴板内容更新了喵～类型：{content_type}")
    print(f"杂鱼♡～剪贴板内容：{str(content)[:300]}")

    print(f"杂鱼♡～源应用程序信息：{source_info}")


if __name__ == "__main__":
    print("=" * 60)
    print("杂鱼♡～本喵的懒人API演示开始了喵～")
    print("=" * 60)
    print("杂鱼♡～懒人特色：")
    print("  - 不需要创建处理器实例")
    print("  - 直接传入回调函数就行")
    print("  - 本喵会自动创建对应的处理器")
    print("  - 按Ctrl+C结束测试")
    print("=" * 60)

    # 杂鱼♡～创建监控器喵～
    monitor = create_monitor()

    # 杂鱼♡～懒人方式：直接传入回调函数喵～
    print("杂鱼♡～使用懒人API注册处理器喵～")

    text_handler = monitor.add_handler("text", on_text_change)
    image_handler = monitor.add_handler("image", on_image_change)
    files_handler = monitor.add_handler("files", on_files_change)
    # update_handler = monitor.add_handler("update", on_clipboard_update)

    print("杂鱼♡～自动创建的处理器类型：")
    print(f"  文本处理器：{type(text_handler).__name__}")
    print(f"  图片处理器：{type(image_handler).__name__}")
    print(f"  文件处理器：{type(files_handler).__name__}")
    # print(f"  更新处理器：{type(update_handler).__name__}")

    # 杂鱼♡～懒人还可以对自动创建的处理器进行配置喵～
    print("杂鱼♡～懒人也可以配置自动创建的处理器喵～")

    try:
        print("杂鱼♡～懒人监控器启动中...请稍等喵～")
        if monitor.start():
            time.sleep(1)
            print("杂鱼♡～懒人可以开始复制内容测试了喵～")

            # 杂鱼♡～显示监控器状态喵～
            status = monitor.get_status()
            
            print(f"杂鱼♡～懒人监控器状态：{status}")

            # 杂鱼♡～等待剪贴板变化喵～
            monitor.wait()
        else:
            print("杂鱼♡～启动监控器失败了喵！")

    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("杂鱼♡～懒人演示结束了喵～")
        print("杂鱼♡～本喵的懒人API让杂鱼主人更轻松了吧～")
        print("杂鱼♡～不用谢本喵，这是本喵应该做的喵～～")
        print("=" * 60)
    finally:
        monitor.stop()

# 杂鱼♡～对比一下两种使用方式喵～
"""
传统方式（非懒人）：
    from clipboard_package import create_monitor, create_text_handler

    monitor = create_monitor()
    text_handler = create_text_handler(callback_function)
    monitor.add_handler('text', text_handler)

懒人方式：
    from clipboard_package import create_monitor

    monitor = create_monitor()
    text_handler = monitor.add_handler('text', callback_function)  # 杂鱼♡～一步到位喵～
"""
