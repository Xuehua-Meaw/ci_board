# 杂鱼♡～本喵的源应用程序追踪示例喵～
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ci_board import (
    create_monitor,
    create_text_handler, 
    create_image_handler, 
    create_file_handler
)
from ci_board.handlers.text_handler import SourceApplicationFilter
from ci_board.handlers.image_handler import SourceApplicationImageFilter
from ci_board.handlers.file_handler import SourceApplicationFileFilter
import time

def advanced_text_callback(text, source_info=None):
    """杂鱼♡～高级文本回调函数，展示源追踪功能喵～"""
    print("\n" + "="*60)
    print("杂鱼♡～检测到文本复制事件喵～")
    print("="*60)
    
    # 杂鱼♡～显示文本信息喵～
    print(f"📝 文本长度：{len(text)} 字符")
    print(f"📄 文本预览：{text[:100]}{'...' if len(text) > 100 else ''}")
    
    # 杂鱼♡～详细显示源应用程序信息喵～
    if source_info:
        print("\n🔍 源应用程序信息：")
        print(f"  进程名：{source_info.get('process_name', 'Unknown')}")
        print(f"  进程ID：{source_info.get('process_id', 'Unknown')}")
        print(f"  程序路径：{source_info.get('process_path', 'Unknown')}")
        print(f"  窗口标题：{source_info.get('window_title', 'Unknown')}")
        print(f"  窗口类：{source_info.get('window_class', 'Unknown')}")
        
        # 杂鱼♡～显示检测方法信息喵～
        detection_method = source_info.get('detection_method', 'unknown')
        print(f"  🔍 检测方法：{detection_method}")
        
        if detection_method == 'foreground_window':
            print(f"  📋 原始剪贴板拥有者：{source_info.get('clipboard_owner_process', 'Unknown')}")
            print(f"  💡 说明：{source_info.get('note', '')}")
        elif source_info.get('is_system_process'):
            print(f"  ⚠️ 系统进程：是")
        
        if source_info.get('error'):
            print(f"  ❌ 错误：{source_info['error']}")
    else:
        print("\n❌ 未获取到源应用程序信息")
    
    print("="*60)

def advanced_image_callback(data, source_info=None):
    """杂鱼♡～高级图片回调函数，展示源追踪功能喵～"""
    print("\n" + "="*60)
    print("杂鱼♡～检测到图片复制事件喵～")
    print("="*60)
    
    # 杂鱼♡～显示图片信息喵～
    if isinstance(data, dict):
        print(f"🖼️ 图片格式：{data.get('format', 'Unknown')}")
        if 'size' in data:
            print(f"📐 图片尺寸：{data['size'][0]}x{data['size'][1]}")
        if 'bit_count' in data:
            print(f"🎨 位深度：{data.get('bit_count', 'Unknown')} 位")
        if 'file_size' in data:
            print(f"💾 文件大小：{data.get('file_size', 'Unknown')} 字节")
    
    # 杂鱼♡～详细显示源应用程序信息喵～
    if source_info:
        print("\n🔍 源应用程序信息：")
        print(f"  进程名：{source_info.get('process_name', 'Unknown')}")
        print(f"  进程ID：{source_info.get('process_id', 'Unknown')}")
        print(f"  程序路径：{source_info.get('process_path', 'Unknown')}")
        print(f"  窗口标题：{source_info.get('window_title', 'Unknown')}")
        print(f"  窗口类：{source_info.get('window_class', 'Unknown')}")
        
        # 杂鱼♡～显示检测方法信息喵～
        detection_method = source_info.get('detection_method', 'unknown')
        print(f"  🔍 检测方法：{detection_method}")
        
        if detection_method == 'foreground_window':
            print(f"  📋 原始剪贴板拥有者：{source_info.get('clipboard_owner_process', 'Unknown')}")
            print(f"  💡 说明：{source_info.get('note', '')}")
            print(f"  🎯 可能的截图工具或系统操作")
        elif source_info.get('is_system_process'):
            print(f"  ⚠️ 系统进程：是")
        
        if source_info.get('error'):
            print(f"  ❌ 错误：{source_info['error']}")
    else:
        print("\n❌ 未获取到源应用程序信息")
    
    print("="*60)

def advanced_file_callback(files, source_info=None):
    """杂鱼♡～高级文件回调函数，展示源追踪功能喵～"""
    print("\n" + "="*60)
    print("杂鱼♡～检测到文件复制事件喵～")
    print("="*60)
    
    # 杂鱼♡～显示文件信息喵～
    print(f"📁 文件数量：{len(files)}")
    for i, file_path in enumerate(files[:5], 1):  # 杂鱼♡～最多显示前5个文件喵～
        print(f"  {i}. {os.path.basename(file_path)}")
    
    if len(files) > 5:
        print(f"  ... 还有 {len(files) - 5} 个文件")
    
    # 杂鱼♡～详细显示源应用程序信息喵～
    if source_info:
        print("\n🔍 源应用程序信息：")
        print(f"  进程名：{source_info.get('process_name', 'Unknown')}")
        print(f"  进程ID：{source_info.get('process_id', 'Unknown')}")
        print(f"  程序路径：{source_info.get('process_path', 'Unknown')}")
        print(f"  窗口标题：{source_info.get('window_title', 'Unknown')}")
        print(f"  窗口类：{source_info.get('window_class', 'Unknown')}")
        
        # 杂鱼♡～显示检测方法信息喵～
        detection_method = source_info.get('detection_method', 'unknown')
        print(f"  🔍 检测方法：{detection_method}")
        
        if detection_method == 'foreground_window':
            print(f"  📋 原始剪贴板拥有者：{source_info.get('clipboard_owner_process', 'Unknown')}")
            print(f"  💡 说明：{source_info.get('note', '')}")
        elif source_info.get('is_system_process'):
            print(f"  ⚠️ 系统进程：是")
        
        if source_info.get('error'):
            print(f"  ❌ 错误：{source_info['error']}")
    else:
        print("\n❌ 未获取到源应用程序信息")
    
    print("="*60)

def setup_source_filters():
    """杂鱼♡～设置源应用程序过滤器的示例喵～"""
    # 杂鱼♡～创建各种过滤器喵～
    
    # 杂鱼♡～只允许来自编辑器的文本复制喵～
    editor_only_filter = SourceApplicationFilter(
        allowed_processes=['notepad.exe', 'notepad++.exe', 'code.exe', 'cursor.exe', 'sublime_text.exe']
    )
    
    # 杂鱼♡～禁止来自浏览器的图片复制喵～
    no_browser_images_filter = SourceApplicationImageFilter(
        blocked_processes=['chrome.exe', 'firefox.exe', 'edge.exe', 'brave.exe', 'opera.exe']
    )
    
    # 杂鱼♡～只允许来自文件管理器的文件复制喵～
    file_manager_only_filter = SourceApplicationFileFilter(
        allowed_processes=['explorer.exe', 'totalcmd.exe', 'freecommander.exe']
    )
    
    return editor_only_filter, no_browser_images_filter, file_manager_only_filter

def demonstrate_source_info():
    """杂鱼♡～演示如何获取当前剪贴板的源信息喵～"""
    from ci_board.utils.clipboard_utils import ClipboardUtils
    
    print("\n" + "🔍"*30)
    print("杂鱼♡～当前剪贴板源信息分析喵～")
    print("🔍"*30)
    
    # 杂鱼♡～获取当前剪贴板内容和源信息喵～
    try:
        content_type, content, source_info = ClipboardUtils.get_clipboard_content_with_source()
        
        print(f"📋 当前剪贴板类型：{content_type or 'Empty'}")
        
        if source_info:
            print("🔍 源应用程序分析：")
            print(f"  进程名：{source_info.get('process_name', 'Unknown')}")
            print(f"  进程ID：{source_info.get('process_id', 'Unknown')}")
            print(f"  程序路径：{source_info.get('process_path', 'Unknown')}")
            print(f"  窗口标题：{source_info.get('window_title', 'Unknown')}")
            print(f"  窗口类：{source_info.get('window_class', 'Unknown')}")
            
            # 杂鱼♡～显示检测方法信息喵～
            detection_method = source_info.get('detection_method', 'unknown')
            print(f"  🔍 检测方法：{detection_method}")
            
            if detection_method == 'foreground_window':
                print(f"  📋 原始剪贴板拥有者：{source_info.get('clipboard_owner_process', 'Unknown')}")
                print(f"  💡 说明：{source_info.get('note', '')}")
            elif source_info.get('is_system_process'):
                print(f"  ⚠️ 系统进程：是")
            
            if source_info.get('error'):
                print(f"  ❌ 错误：{source_info['error']}")
        else:
            print("❌ 无法获取源应用程序信息")
            
    except Exception as e:
        print(f"❌ 获取信息时出错：{e}")
    
    print("🔍"*30)

if __name__ == "__main__":
    print("🚀" + "="*58 + "🚀")
    print("杂鱼♡～源应用程序追踪功能演示开始了喵～")
    print("🚀" + "="*58 + "🚀")
    
    print("\n📋 功能说明：")
    print("  🎯 追踪每个剪贴板事件的源应用程序")
    print("  📊 显示详细的进程和窗口信息")
    print("  🛡️ 支持基于源应用程序的过滤规则")
    print("  ⚙️ 可以启用或禁用源追踪功能")
    print("  🔄 兼容旧版回调函数")
    
    # 杂鱼♡～先显示当前剪贴板的源信息喵～
    demonstrate_source_info()
    
    # 杂鱼♡～创建监控器喵～
    monitor = create_monitor()
    
    # 杂鱼♡～创建高级处理器喵～
    text_handler = create_text_handler(advanced_text_callback)
    image_handler = create_image_handler(advanced_image_callback)
    file_handler = create_file_handler(advanced_file_callback)
    
    # 杂鱼♡～设置过滤器（可选）喵～
    print("\n🛡️ 过滤器设置选项：")
    print("  1. 启用编辑器文本过滤器（只接受来自编辑器的文本）")
    print("  2. 启用浏览器图片过滤器（拒绝来自浏览器的图片）")
    print("  3. 启用文件管理器过滤器（只接受来自文件管理器的文件）")
    print("  杂鱼♡～如需启用过滤器，请取消下面代码的注释喵～")
    
    # 杂鱼♡～设置过滤器（默认注释掉，用户可以根据需要启用）喵～
    editor_filter, no_browser_filter, file_manager_filter = setup_source_filters()
    
    # 杂鱼♡～取消注释下面的行来启用对应的过滤器喵～
    # text_handler.add_filter(editor_filter)
    # image_handler.add_filter(no_browser_filter)
    # file_handler.add_filter(file_manager_filter)
    
    # 杂鱼♡～演示如何禁用源信息显示喵～
    # text_handler.disable_source_info()
    
    # 杂鱼♡～演示如何禁用整个监控器的源追踪功能喵～
    # monitor.disable_source_tracking()
    
    # 杂鱼♡～注册处理器喵～
    monitor.add_handler('text', text_handler)
    monitor.add_handler('image', image_handler)
    monitor.add_handler('files', file_handler)
    
    try:
        print("\n🚀 监控器启动中...")
        if monitor.start():
            time.sleep(1)
            print("✅ 监控器启动成功！")
            print("\n📢 现在可以在不同程序中复制内容来测试源追踪功能喵～")
            print("💡 建议测试：")
            print("  - 在记事本中复制文本")
            print("  - 在浏览器中复制图片")
            print("  - 在文件管理器中复制文件")
            print("  - 在不同编辑器中复制代码")
            
            # 杂鱼♡～显示监控器状态喵～
            status = monitor.get_status()
            print(f"\n📊 监控器状态：")
            print(f"  源追踪启用：{status.get('source_tracking_enabled', False)}")
            print(f"  处理器数量：{status.get('handlers_count', {})}")
            
            print("\n⏹️ 按 Ctrl+C 结束监控")
            monitor.wait()
        else:
            print("❌ 监控器启动失败！")
    
    except KeyboardInterrupt:
        print("\n\n🛑 用户手动停止监控")
    except Exception as e:
        print(f"\n❌ 发生错误：{e}")
    finally:
        monitor.stop()
        print("\n✅ 监控器已停止")
        print("🎯 源应用程序追踪演示结束，谢谢杂鱼主人的测试♡～") 