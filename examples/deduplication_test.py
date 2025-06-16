# 杂鱼♡～本喵的图片去重测试脚本喵～
import os
import sys
import time
import threading

# 杂鱼♡～杂鱼主人的路径设置，本喵勉强帮你修复了喵～
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# 杂鱼♡～设置日志级别喵～
from ci_board.utils.logger import setup_ci_board_logging
from ci_board import create_monitor, BMPData

setup_ci_board_logging(debug=True)  # 杂鱼♡～开启调试模式查看去重日志喵～

# 杂鱼♡～统计数据喵～
image_count = 0
duplicate_count = 0
processed_hashes = set()


def on_image_change(bData: BMPData, source_info=None):
    """杂鱼♡～图片变化回调函数，带去重统计喵～"""
    global image_count, duplicate_count

    image_count += 1

    if bData.success:
        try:
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(bData.data))

            # 杂鱼♡～计算简单的图片特征哈希喵～
            image_signature = f"{image.mode}_{image.size}_{len(bData.data)}"

            if image_signature in processed_hashes:
                duplicate_count += 1
                print(f"🔄 杂鱼♡～检测到疑似重复图片 #{image_count} (重复#{duplicate_count})喵～")
                print(f"   特征：{image_signature}")
            else:
                processed_hashes.add(image_signature)
                print(f"🖼️ 杂鱼♡～新图片 #{image_count}：{image.mode} {image.size}，{len(bData.data)}字节喵～")

            # 杂鱼♡～显示源应用程序信息喵～
            if source_info:
                print(f"   📱 源应用程序：{source_info.get('process_name', 'Unknown')}")
                if source_info.get('window_title'):
                    print(f"   🪟 窗口标题：{source_info['window_title']}")

        except Exception as e:
            print(f"杂鱼♡～PIL打开失败喵：{e}")
    else:
        print(f"杂鱼♡～BMP转换失败，返回原始数据{len(bData.data)}字节喵～")

    print(f"📊 统计：总计{image_count}次图片事件，其中{duplicate_count}次可能重复")
    print("-" * 60)


def show_stats():
    """杂鱼♡～定期显示统计信息喵～"""
    while True:
        time.sleep(10)
        print(f"\n📈 杂鱼♡～10秒统计：总图片事件{image_count}次，疑似重复{duplicate_count}次")
        if image_count > 0:
            duplicate_rate = (duplicate_count / image_count) * 100
            print(f"   重复率：{duplicate_rate:.1f}%")
        print()


if __name__ == "__main__":
    print("=" * 70)
    print("杂鱼♡～本喵的图片去重测试开始了喵～")
    print("=" * 70)
    print("🎯 测试目标：")
    print("  - 检测多步骤处理导致的重复图片事件")
    print("  - 验证新的图片指纹算法效果")
    print("  - 统计去重效果和性能")
    print("  - 按Ctrl+C结束测试")
    print("=" * 70)

    # 杂鱼♡～启动统计线程喵～
    stats_thread = threading.Thread(target=show_stats, daemon=True)
    stats_thread.start()

    # 杂鱼♡～创建监控器喵～
    monitor = create_monitor()

    # 杂鱼♡～只监控图片变化喵～
    image_handler = monitor.add_handler('image', on_image_change)

    print("杂鱼♡～开始监控图片剪贴板事件喵～")
    print("💡 提示：复制同一张图片多次，观察去重效果")

    try:
        if monitor.start():
            time.sleep(1)
            print("✅ 杂鱼♡～监控器启动成功，开始复制图片测试吧喵～")

            # 杂鱼♡～显示监控器状态喵～
            status = monitor.get_status()
            print(f"🔧 监控器状态：事件驱动={status['event_driven']}, 源追踪={status['source_tracking_enabled']}")

            # 杂鱼♡～等待剪贴板变化喵～
            monitor.wait()
        else:
            print("❌ 杂鱼♡～启动监控器失败了喵！")

    except KeyboardInterrupt:
        print("\n" + "=" * 70)
        print("🏁 杂鱼♡～图片去重测试结束了喵～")
        print("=" * 70)
        print("📊 最终统计：")
        print(f"   总图片事件：{image_count}次")
        print(f"   疑似重复：{duplicate_count}次")
        if image_count > 0:
            duplicate_rate = (duplicate_count / image_count) * 100
            efficiency = 100 - duplicate_rate
            print(f"   重复率：{duplicate_rate:.1f}%")
            print(f"   去重效率：{efficiency:.1f}%")
        print("杂鱼♡～本喵的去重算法表现如何？喵～")
        print("=" * 70)
    finally:
        monitor.stop()
