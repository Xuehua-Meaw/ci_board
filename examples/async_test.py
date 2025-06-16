# 杂鱼♡～本喵的异步处理测试脚本喵～
import os
import sys
import threading
import time

# 杂鱼♡～杂鱼主人的路径设置，本喵勉强帮你修复了喵～
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ci_board import create_monitor

# 杂鱼♡～全局计数器，用于测试并发处理喵～
text_counter = 0
image_counter = 0
file_counter = 0


def fast_text_handler(text, source_info=None):
    """杂鱼♡～快速文本处理器喵～"""
    global text_counter
    text_counter += 1
    print(f"🚀 [快速文本处理器] #{text_counter} - 长度: {len(text)} 字符")
    if source_info:
        print(f"   源应用: {source_info.get('process_name', 'Unknown')}")
    print(f"   线程: {threading.current_thread().name}")
    print("-" * 30)


def slow_text_handler(text, source_info=None):
    """杂鱼♡～慢速文本处理器（10秒延迟）喵～"""
    global text_counter
    text_counter += 1
    print(f"🐌 [慢速文本处理器] #{text_counter} - 开始处理，长度: {len(text)} 字符")
    if source_info:
        print(f"   源应用: {source_info.get('process_name', 'Unknown')}")
    print(f"   线程: {threading.current_thread().name}")
    print("   杂鱼♡～慢速处理器开始等待10秒...")

    # 杂鱼♡～模拟耗时操作喵～
    time.sleep(10)

    print(f"🎉 [慢速文本处理器] #{text_counter} - 处理完成！")
    print("-" * 30)


def fast_image_handler(data, source_info=None):
    """杂鱼♡～快速图片处理器喵～"""
    global image_counter
    image_counter += 1
    print(f"🖼️ [快速图片处理器] #{image_counter} - 检测到图片变化")
    if source_info:
        print(f"   源应用: {source_info.get('process_name', 'Unknown')}")
    print(f"   线程: {threading.current_thread().name}")
    print("-" * 30)


def slow_image_handler(data, source_info=None):
    """杂鱼♡～慢速图片处理器（5秒延迟）喵～"""
    global image_counter
    image_counter += 1
    print(f"🐌 [慢速图片处理器] #{image_counter} - 开始处理图片")
    if source_info:
        print(f"   源应用: {source_info.get('process_name', 'Unknown')}")
    print(f"   线程: {threading.current_thread().name}")
    print("   杂鱼♡～慢速图片处理器开始等待5秒...")

    # 杂鱼♡～模拟耗时操作喵～
    time.sleep(5)

    print(f"🎉 [慢速图片处理器] #{image_counter} - 处理完成！")
    print("-" * 30)

# def statistics_handler(data, source_info=None):
#     """杂鱼♡～统计处理器，显示处理总数喵～"""
#     content_type, content = data
#     print(f"🔄 [统计处理器] 最后变化: {content_type}")
#     print(f"   文本处理次数: {text_counter}")
#     print(f"   图片处理次数: {image_counter}")
#     print(f"   文件处理次数: {file_counter}")
#     print(f"   线程: {threading.current_thread().name}")
#     print("-" * 30)


def test_async_mode():
    """杂鱼♡～测试异步模式喵～"""
    print("🚀" * 20)
    print("杂鱼♡～异步模式测试开始喵～")
    print("🚀" * 20)
    print("杂鱼♡～在异步模式下，慢速处理器不会阻塞快速处理器喵～")
    print("杂鱼♡～你可以快速连续复制文本，观察处理器的并发执行喵～")
    print("🚀" * 20)

    # 杂鱼♡～创建异步监控器喵～
    monitor = create_monitor(
        async_processing=True,      # 杂鱼♡～启用异步处理喵～
        max_workers=6,              # 杂鱼♡～6个工作线程喵～
        handler_timeout=15.0        # 杂鱼♡～15秒超时喵～
    )

    # 杂鱼♡～注册多个处理器喵～
    monitor.add_handler('text', fast_text_handler)
    monitor.add_handler('text', slow_text_handler)  # 杂鱼♡～这个会延迟10秒喵～
    monitor.add_handler('image', fast_image_handler)
    monitor.add_handler('image', slow_image_handler)  # 杂鱼♡～这个会延迟5秒喵～

    return monitor


def test_sync_mode():
    """杂鱼♡～测试同步模式（对比用）喵～"""
    print("🐌" * 20)
    print("杂鱼♡～同步模式测试开始喵～")
    print("🐌" * 20)
    print("杂鱼♡～在同步模式下，慢速处理器会阻塞快速处理器喵～")
    print("杂鱼♡～你会发现复制操作会被阻塞喵～")
    print("🐌" * 20)

    # 杂鱼♡～创建同步监控器喵～
    monitor = create_monitor(
        async_processing=False,     # 杂鱼♡～禁用异步处理喵～
        max_workers=6,
        handler_timeout=15.0
    )

    # 杂鱼♡～注册相同的处理器喵～
    monitor.add_handler('text', fast_text_handler)
    monitor.add_handler('text', slow_text_handler)
    monitor.add_handler('image', fast_image_handler)
    monitor.add_handler('image', slow_image_handler)

    return monitor


def show_status(monitor):
    """杂鱼♡～显示监控器状态喵～"""
    while True:
        try:
            time.sleep(10)
            status = monitor.get_status()
            print("\n" + "=" * 50)
            print("📊 监控器状态报告:")
            print(f"   运行状态: {status['is_running']}")
            print(f"   处理器数量: {status['handlers_count']}")
            print(f"   源追踪: {status['source_tracking_enabled']}")

            if 'async_stats' in status:
                async_stats = status['async_stats']
                print(f"   异步模式: {async_stats['async_enabled']}")
                if async_stats['async_enabled']:
                    print(f"   工作线程: {async_stats['max_workers']}")
                    print(f"   队列大小: {async_stats['queue_size']}")
                    print(f"   已提交任务: {async_stats['tasks_submitted']}")
                    print(f"   已完成任务: {async_stats['tasks_completed']}")
                    print(f"   失败任务: {async_stats['tasks_failed']}")
                    print(f"   超时任务: {async_stats['tasks_timeout']}")
                    print(f"   活跃任务: {async_stats['active_tasks']}")

            print("=" * 50 + "\n")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"杂鱼♡～状态报告出错了喵：{e}")


if __name__ == "__main__":
    print("杂鱼♡～选择测试模式喵～")
    print("1. 异步模式（推荐）- 处理器并发执行")
    print("2. 同步模式（对比用）- 处理器顺序执行")
    print("3. 退出")

    choice = input("杂鱼♡～请选择 (1/2/3): ").strip()

    if choice == "1":
        monitor = test_async_mode()
    elif choice == "2":
        monitor = test_sync_mode()
    elif choice == "3":
        print("杂鱼♡～再见喵～")
        sys.exit(0)
    else:
        print("杂鱼♡～默认使用异步模式喵～")
        monitor = test_async_mode()

    try:
        print("杂鱼♡～启动监控器喵～")
        if monitor.start():
            time.sleep(1)
            print("杂鱼♡～监控器启动成功，开始测试喵～")
            print("杂鱼♡～现在可以复制文本或图片来测试喵～")
            print("杂鱼♡～快速连续复制看看异步处理的效果喵～")
            print("杂鱼♡～按Ctrl+C结束测试喵～")

            # 杂鱼♡～启动状态监控线程喵～
            status_thread = threading.Thread(target=show_status, args=(monitor,), daemon=True)
            status_thread.start()

            # 杂鱼♡～等待剪贴板变化喵～
            monitor.wait()
        else:
            print("杂鱼♡～启动监控器失败了喵！")

    except KeyboardInterrupt:
        print("\n" + "🎉" * 20)
        print("杂鱼♡～测试结束喵～")
        final_status = monitor.get_async_stats()
        if final_status['async_enabled']:
            print("📊 最终统计:")
            print(f"   已提交任务: {final_status['tasks_submitted']}")
            print(f"   已完成任务: {final_status['tasks_completed']}")
            print(f"   失败任务: {final_status['tasks_failed']}")
            print(f"   超时任务: {final_status['tasks_timeout']}")
        print("杂鱼♡～感谢使用本喵的异步测试工具喵～～")
        print("🎉" * 20)
    finally:
        print("杂鱼♡～清理监控器资源喵～")
        monitor.stop()
