# 杂鱼♡～本喵的日志系统演示喵～
"""
杂鱼♡～演示如何使用新的日志系统控制输出详细程度喵～
支持不同的日志级别：DEBUG, INFO, WARNING, ERROR
"""
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ci_board.utils.logger import setup_ci_board_logging, LogLevel, get_component_logger
from ci_board.core.monitor import ClipboardMonitor


def demo_different_log_levels():
    """杂鱼♡～演示不同日志级别的效果喵～"""
    print("=" * 60)
    print("杂鱼♡～日志系统演示开始了喵～")
    print("=" * 60)
    
    # 杂鱼♡～演示1：安静模式（只显示警告和错误）喵～
    print("\n🔇 安静模式演示 - 只显示警告和错误:")
    print("-" * 40)
    setup_ci_board_logging(quiet=True)
    
    monitor1 = ClipboardMonitor()
    logger = get_component_logger("demo")
    
    logger.debug("这是调试信息，安静模式下不会显示")
    logger.info("这是普通信息，安静模式下不会显示")
    logger.warning("这是警告信息，会显示")
    logger.error("这是错误信息，会显示")
    
    print("\n📢 详细模式演示 - 显示所有信息:")
    print("-" * 40)
    setup_ci_board_logging(verbose=True)
    
    logger.debug("这是调试信息，详细模式下不会显示")
    logger.info("这是普通信息，详细模式下会显示")
    logger.warning("这是警告信息，会显示")
    logger.error("这是错误信息，会显示")
    
    print("\n🐛 调试模式演示 - 显示所有调试信息:")
    print("-" * 40)
    setup_ci_board_logging(debug=True)
    
    logger.debug("这是调试信息，调试模式下会显示")
    logger.info("这是普通信息，会显示")
    logger.warning("这是警告信息，会显示")
    logger.error("这是错误信息，会显示")


def demo_clipboard_monitoring_with_different_verbosity():
    """杂鱼♡～演示不同详细程度下的剪贴板监控喵～"""
    print("\n" + "=" * 60)
    print("杂鱼♡～剪贴板监控日志级别演示喵～")
    print("=" * 60)
    
    # 杂鱼♡～让用户选择日志级别喵～
    print("杂鱼♡～请选择日志级别喵～：")
    print("1. 🔇 安静模式 (只显示警告和错误)")
    print("2. 📢 标准模式 (显示重要信息)")
    print("3. 🐛 调试模式 (显示所有调试信息)")
    
    choice = input("请输入选择 (1-3): ").strip()
    
    if choice == "1":
        setup_ci_board_logging(quiet=True)
        print("杂鱼♡～已设置为安静模式喵～")
    elif choice == "3":
        setup_ci_board_logging(debug=True)
        print("杂鱼♡～已设置为调试模式，会显示很多详细信息喵～")
    else:
        setup_ci_board_logging(verbose=True)
        print("杂鱼♡～已设置为标准模式喵～")
    
    print("\n杂鱼♡～启动剪贴板监控器喵～")
    print("复制一些内容试试看，按 Ctrl+C 结束")
    print("-" * 60)
    
    # 杂鱼♡～创建监控器喵～
    monitor = ClipboardMonitor()
    
    # 杂鱼♡～添加简单的处理器喵～
    def on_text_change(text, source_info=None):
        logger = get_component_logger("demo")
        logger.info(f"检测到文本变化: {text[:50]}{'...' if len(text) > 50 else ''}")
        if source_info:
            logger.info(f"源应用程序: {source_info.get('process_name', 'Unknown')}")
    
    def on_image_change(image_data, source_info=None):
        logger = get_component_logger("demo")
        if image_data:
            logger.info(f"检测到图片变化: {image_data.size[0]}x{image_data.size[1]}")
            if source_info:
                logger.info(f"源应用程序: {source_info.get('process_name', 'Unknown')}")
    
    monitor.add_handler("text", on_text_change)
    monitor.add_handler("image", on_image_change)
    
    try:
        if monitor.start():
            monitor.wait()
    except KeyboardInterrupt:
        print("\n杂鱼♡～被用户中断了喵～")
    finally:
        monitor.stop()
        print("杂鱼♡～监控器已停止喵～")


def demo_file_logging():
    """杂鱼♡～演示文件日志功能喵～"""
    print("\n" + "=" * 60)
    print("杂鱼♡～文件日志演示喵～")
    print("=" * 60)
    
    # 杂鱼♡～启用文件日志喵～
    setup_ci_board_logging(
        verbose=True,
        enable_file_logging=True,
        log_file="ci_board_demo.log"
    )
    
    logger = get_component_logger("file_demo")
    
    logger.info("开始文件日志演示")
    logger.debug("这是调试信息，会记录到文件中")
    logger.warning("这是警告信息")
    logger.error("这是错误信息")
    
    print("杂鱼♡～日志已记录到 'ci_board_demo.log' 文件中喵～")
    print("杂鱼♡～你可以打开文件查看完整的日志记录喵～")


if __name__ == "__main__":
    print("杂鱼♡～欢迎使用日志系统演示喵～")
    print("这个演示会展示不同的日志级别效果")
    
    try:
        # 杂鱼♡～演示不同日志级别喵～
        demo_different_log_levels()
        
        # 杂鱼♡～演示文件日志喵～
        demo_file_logging()
        
        # 杂鱼♡～演示剪贴板监控喵～
        demo_clipboard_monitoring_with_different_verbosity()
        
    except Exception as e:
        print(f"杂鱼♡～演示过程中出错了喵：{e}")
    
    print("\n" + "=" * 60)
    print("杂鱼♡～日志系统演示结束了喵～")
    print("现在你知道如何控制日志输出详细程度了喵～")
    print("=" * 60) 