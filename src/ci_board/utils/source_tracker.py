# 杂鱼♡～本喵为杂鱼主人创建的智能源应用追踪器喵～
"""
杂鱼♡～基于焦点跟踪的智能源应用程序分析器喵～
从 test_clipboard_hook.py 中提取的核心功能，结合焦点跟踪实现准确的源识别喵～
"""
import ctypes
import ctypes.wintypes as w
import os
import threading
import time
from typing import Any, Dict, List, Optional

from .win32_api import Win32API


class SourceTracker:
    """杂鱼♡～智能源应用程序追踪器，结合焦点跟踪和剪贴板拥有者分析喵～"""

    # 杂鱼♡～类级别变量，跟踪焦点变化喵～
    _focus_tracker = None
    _focus_lock = threading.Lock()
    _current_focus_info = None
    _focus_history = []
    _focus_hook_handle = None
    _winevent_proc_func = None
    _message_loop_thread = None
    _is_tracking = False
    _stop_event = threading.Event()

    # 杂鱼♡～系统进程黑名单喵～
    SYSTEM_PROCESSES = {
        'svchost.exe', 'dwm.exe', 'explorer.exe', 'winlogon.exe', 'csrss.exe',
        'screenclippinghost.exe', 'taskhostw.exe', 'runtimebroker.exe',
        'sihost.exe', 'shellexperiencehost.exe', 'searchui.exe', 'cortana.exe',
        'windowsinternal.composableshell.experiences.textinput.inputapp.exe',
        'applicationframehost.exe', 'searchapp.exe', 'startmenuexperiencehost.exe'
    }

    # 杂鱼♡～窗口事件常量喵～
    EVENT_SYSTEM_FOREGROUND = 0x0003
    WINEVENT_OUTOFCONTEXT = 0x0000
    WINEVENT_SKIPOWNPROCESS = 0x0002
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

    @classmethod
    def initialize_focus_tracking(cls) -> bool:
        """杂鱼♡～初始化焦点跟踪功能喵～"""
        if cls._is_tracking:
            return True
            
        print("杂鱼♡～初始化智能焦点跟踪器喵～")
        
        try:
            cls._stop_event.clear()
            
            # 杂鱼♡～启动消息循环线程来处理钩子事件喵～
            cls._message_loop_thread = threading.Thread(
                target=cls._focus_tracking_message_loop, 
                daemon=False,
                name="FocusTrackingThread"
            )
            cls._message_loop_thread.start()
            
            # 杂鱼♡～等待一点时间确保钩子设置成功喵～
            time.sleep(1.0)
            
            # 杂鱼♡～检查钩子是否设置成功喵～
            if cls._focus_hook_handle is not None:
                cls._is_tracking = True
                print("杂鱼♡～焦点跟踪器初始化成功喵～")
                return True
            else:
                print("杂鱼♡～焦点跟踪器初始化失败 - 钩子未设置喵～")
                cls._is_tracking = False
                return False
                
        except Exception as e:
            print(f"杂鱼♡～初始化焦点跟踪器时出错喵～：{str(e)}")
            cls._is_tracking = False
            return False

    @classmethod
    def _focus_tracking_message_loop(cls):
        """杂鱼♡～焦点跟踪的消息循环线程喵～"""
        try:
            print("杂鱼♡～启动焦点跟踪消息循环线程喵～")
            
            # 杂鱼♡～在消息循环线程中设置钩子喵～
            WINEVENTPROC = ctypes.WINFUNCTYPE(
                None, w.HANDLE, w.DWORD, w.HWND, w.LONG, w.LONG, w.DWORD, w.DWORD
            )
            cls._winevent_proc_func = WINEVENTPROC(cls._winevent_proc)
            
            # 杂鱼♡～设置Windows事件钩子喵～
            cls._focus_hook_handle = Win32API.user32.SetWinEventHook(
                cls.EVENT_SYSTEM_FOREGROUND,
                cls.EVENT_SYSTEM_FOREGROUND,
                None,
                cls._winevent_proc_func,
                0,
                0,
                cls.WINEVENT_OUTOFCONTEXT | cls.WINEVENT_SKIPOWNPROCESS
            )
            
            if cls._focus_hook_handle:
                print("杂鱼♡～焦点跟踪钩子设置成功喵～")
                
                # 杂鱼♡～初始化当前焦点信息喵～
                current_hwnd = Win32API.user32.GetForegroundWindow()
                if current_hwnd:
                    cls._winevent_proc(None, cls.EVENT_SYSTEM_FOREGROUND, current_hwnd, 0, 0, 0, 0)
                
                # 杂鱼♡～运行消息循环喵～
                cls._run_message_loop()
            else:
                print(f"杂鱼♡～设置焦点钩子失败喵！错误码：{Win32API.kernel32.GetLastError()}")
                
        except Exception as e:
            print(f"杂鱼♡～焦点跟踪消息循环出错喵～：{str(e)}")
        finally:
            # 杂鱼♡～清理钩子喵～
            if cls._focus_hook_handle:
                Win32API.user32.UnhookWinEvent(cls._focus_hook_handle)
                cls._focus_hook_handle = None
            print("杂鱼♡～焦点跟踪消息循环线程结束喵～")

    @classmethod
    def _run_message_loop(cls):
        """杂鱼♡～运行Windows消息循环喵～"""
        print("杂鱼♡～开始运行消息循环喵～")
        from .win32_api import Win32Structures
        msg = Win32Structures.MSG()
        
        while not cls._stop_event.is_set():
            try:
                # 杂鱼♡～使用PeekMessage进行非阻塞消息检查喵～
                bRet = Win32API.user32.PeekMessageW(
                    ctypes.byref(msg), 
                    None, 
                    0, 
                    0, 
                    1  # PM_REMOVE
                )
                
                if bRet:
                    # 杂鱼♡～处理消息喵～
                    Win32API.user32.TranslateMessage(ctypes.byref(msg))
                    Win32API.user32.DispatchMessageW(ctypes.byref(msg))
                    
                    # 杂鱼♡～检查是否为退出消息喵～
                    if msg.message == 0x0012:  # WM_QUIT
                        print("杂鱼♡～收到退出消息，结束消息循环喵～")
                        break
                
                # 杂鱼♡～短暂休眠，无论是否有消息喵～
                time.sleep(0.01)
                    
            except Exception as e:
                print(f"杂鱼♡～消息循环处理出错喵～：{str(e)}")
                time.sleep(0.1)

    @classmethod
    def cleanup_focus_tracking(cls):
        """杂鱼♡～清理焦点跟踪功能喵～"""
        if not cls._is_tracking:
            return
            
        print("杂鱼♡～清理焦点跟踪器喵～")
        
        try:
            cls._stop_event.set()
            cls._is_tracking = False
            
            # 杂鱼♡～等待消息循环线程结束喵～
            if cls._message_loop_thread and cls._message_loop_thread.is_alive():
                cls._message_loop_thread.join(timeout=3.0)
                if cls._message_loop_thread.is_alive():
                    print("杂鱼♡～消息循环线程在3秒内未能结束喵～")
                
            # 杂鱼♡～清理状态喵～
            with cls._focus_lock:
                cls._current_focus_info = None
                cls._focus_history.clear()
                
            cls._message_loop_thread = None
            print("杂鱼♡～焦点跟踪器已清理喵～")
            
        except Exception as e:
            print(f"杂鱼♡～清理焦点跟踪器时出错喵～：{str(e)}")

    @staticmethod
    def _winevent_proc(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
        """杂鱼♡～窗口事件钩子回调函数喵～"""
        if event == SourceTracker.EVENT_SYSTEM_FOREGROUND and hwnd:
            try:
                window_info = SourceTracker._get_window_info(hwnd)
                if isinstance(window_info, dict):
                    # print(f"杂鱼♡～检测到窗口焦点变化: {window_info['exe_info']['name']} - {window_info['title']}")
                    
                    # 杂鱼♡～过滤系统窗口和无效窗口喵～
                    if (window_info['exe_info']['name'].lower() not in SourceTracker.SYSTEM_PROCESSES and
                        window_info['title'] != "杂鱼♡～无标题" and
                        len(window_info['title'].strip()) > 0):
                        
                        # print(f"杂鱼♡～有效的焦点切换: {window_info['exe_info']['name']}")
                        
                        with SourceTracker._focus_lock:
                            SourceTracker._current_focus_info = window_info.copy()
                            SourceTracker._current_focus_info['focus_time'] = time.time()
                            
                            # 杂鱼♡～更新焦点历史，避免重复喵～
                            SourceTracker._focus_history = [
                                f for f in SourceTracker._focus_history 
                                if f['exe_info']['name'].lower() != window_info['exe_info']['name'].lower()
                            ]
                            SourceTracker._focus_history.insert(0, SourceTracker._current_focus_info)
                            
                            # 杂鱼♡～只保留最近10个喵～
                            SourceTracker._focus_history = SourceTracker._focus_history[:10]
                    else:
                        print(f"杂鱼♡～过滤掉的窗口: {window_info['exe_info']['name']} - {window_info['title']}")
                            
            except Exception as e:
                print(f"杂鱼♡～焦点钩子回调出错喵～：{str(e)}")

    @classmethod
    def _get_window_info(cls, hwnd, description=""):
        """杂鱼♡～获取窗口详细信息的通用函数喵～"""
        if not hwnd or not Win32API.user32.IsWindow(hwnd):
            return f"杂鱼♡～{description}窗口无效喵～"
        
        try:
            # 杂鱼♡～获取窗口标题（改进版）喵～
            title_length = Win32API.user32.GetWindowTextLengthW(hwnd)
            if title_length > 0:
                window_title_buffer = ctypes.create_unicode_buffer(title_length + 1)
                actual_length = Win32API.user32.GetWindowTextW(hwnd, window_title_buffer, title_length + 1)
                window_title = window_title_buffer.value if actual_length > 0 else "杂鱼♡～无标题"
            else:
                window_title = "杂鱼♡～无标题"
            
            # 杂鱼♡～获取窗口类名喵～
            class_buffer = ctypes.create_unicode_buffer(256)
            class_length = Win32API.user32.GetClassNameW(hwnd, class_buffer, 256)
            window_class = class_buffer.value if class_length > 0 else "杂鱼♡～未知类名"
            
            # 杂鱼♡～获取进程信息喵～
            process_id = w.DWORD()
            thread_id = Win32API.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
            
            if not process_id.value:
                return f"杂鱼♡～{description}无法获取进程ID喵～（窗口：{window_title}，类名：{window_class}）"
            
            # 杂鱼♡～获取可执行文件路径喵～
            exe_info = cls._get_process_path(process_id.value)
            
            return {
                'title': window_title,
                'class': window_class,
                'pid': process_id.value,
                'exe_info': exe_info,
                'hwnd': hwnd
            }
            
        except Exception as e:
            return f"杂鱼♡～获取{description}窗口信息时出错喵～：{str(e)}"

    @classmethod
    def _get_process_path(cls, process_id):
        """杂鱼♡～获取进程路径信息喵～"""
        try:
            # 杂鱼♡～打开进程获取详细信息喵～
            process_handle = Win32API.kernel32.OpenProcess(
                cls.PROCESS_QUERY_INFORMATION | cls.PROCESS_QUERY_LIMITED_INFORMATION, 
                False, 
                process_id
            )
            
            if not process_handle:
                # 杂鱼♡～尝试较低权限喵～
                process_handle = Win32API.kernel32.OpenProcess(cls.PROCESS_QUERY_LIMITED_INFORMATION, False, process_id)
            
            if not process_handle:
                return {'name': f'PID:{process_id}', 'path': '杂鱼♡～无法打开进程'}
            
            try:
                # 杂鱼♡～尝试获取完整进程路径喵～
                exe_path = None
                
                # 杂鱼♡～方法1：使用QueryFullProcessImageName（推荐）喵～
                path_buffer = ctypes.create_unicode_buffer(1024)
                path_size = w.DWORD(1024)
                if Win32API.kernel32.QueryFullProcessImageNameW(process_handle, 0, path_buffer, ctypes.byref(path_size)):
                    exe_path = path_buffer.value
                
                if exe_path:
                    exe_name = os.path.basename(exe_path)
                    return {'name': exe_name, 'path': exe_path}
                else:
                    return {'name': f'PID:{process_id}', 'path': '杂鱼♡～无法获取路径'}
                    
            finally:
                Win32API.kernel32.CloseHandle(process_handle)
                
        except Exception as e:
            return {'name': f'PID:{process_id}', 'path': f'杂鱼♡～出错：{str(e)}'}

    @classmethod
    def get_source_application_info(cls) -> Dict[str, Any]:
        """杂鱼♡～获取智能源应用程序分析结果喵～"""
        # 杂鱼♡～确保焦点跟踪已初始化喵～
        if not cls._is_tracking:
            cls.initialize_focus_tracking()
        
        try:
            # 杂鱼♡～获取当前焦点信息喵～
            with cls._focus_lock:
                current_focus = cls._current_focus_info.copy() if cls._current_focus_info else None
                recent_focus = cls._focus_history[:5] if cls._focus_history else []
            
            # 杂鱼♡～获取剪贴板拥有者喵～
            owner_hwnd = Win32API.user32.GetClipboardOwner()
            owner_info = None
            if owner_hwnd:
                owner_info = cls._get_window_info(owner_hwnd, "剪贴板拥有者")
            
            # 杂鱼♡～分析真实的源应用程序喵～
            real_source = None
            confidence_level = "未知"
            detection_method = "unknown"
            
            if current_focus:
                # 杂鱼♡～检查当前焦点是否就是剪贴板拥有者喵～
                if (owner_info and isinstance(owner_info, dict) and 
                    current_focus['pid'] == owner_info['pid']):
                    real_source = current_focus
                    confidence_level = "高"
                    detection_method = "focus_and_owner_match"
                
                # 杂鱼♡～检查最近焦点切换时间喵～
                elif current_focus.get('focus_time', 0) > time.time() - 2:  # 杂鱼♡～2秒内的焦点切换喵～
                    real_source = current_focus
                    confidence_level = "中等"
                    detection_method = "recent_focus"
                
                # 杂鱼♡～如果剪贴板拥有者是系统进程，使用当前焦点喵～
                elif (owner_info and isinstance(owner_info, dict) and 
                      owner_info['exe_info']['name'].lower() in cls.SYSTEM_PROCESSES):
                    real_source = current_focus
                    confidence_level = "中等"
                    detection_method = "system_owner_fallback"
            
            # 杂鱼♡～如果还是没有，使用剪贴板拥有者喵～
            if not real_source and owner_info and isinstance(owner_info, dict):
                real_source = owner_info
                confidence_level = "低"
                detection_method = "clipboard_owner_only"
            
            # 杂鱼♡～如果还是没有，使用最近的焦点应用程序喵～
            if not real_source and recent_focus:
                real_source = recent_focus[0]
                confidence_level = "低"
                detection_method = "focus_history_fallback"
            
            # 杂鱼♡～构建兼容的返回结果喵～
            result = {
                "process_name": None,
                "process_path": None,
                "process_id": None,
                "window_title": None,
                "window_class": None,
                "detection_method": detection_method,
                "confidence_level": confidence_level,
                "is_system_process": False,
                "is_screenshot_tool": False,
                "timestamp": time.time(),
            }
            
            if real_source:
                result.update({
                    "process_name": real_source['exe_info']['name'],
                    "process_path": real_source['exe_info']['path'],
                    "process_id": real_source['pid'],
                    "window_title": real_source['title'],
                    "window_class": real_source['class'],
                    "is_system_process": real_source['exe_info']['name'].lower() in cls.SYSTEM_PROCESSES,
                })
            
            return result
            
        except Exception as e:
            return {
                "process_name": None,
                "process_path": None,
                "process_id": None,
                "window_title": None,
                "window_class": None,
                "detection_method": "error",
                "confidence_level": "无",
                "error": f"杂鱼♡～智能分析时出错喵～：{str(e)}",
                "timestamp": time.time(),
            }

    @classmethod
    def get_detailed_analysis(cls) -> str:
        """杂鱼♡～获取详细的源应用程序分析报告喵～"""
        try:
            result_lines = []
            
            # 杂鱼♡～获取当前焦点信息喵～
            with cls._focus_lock:
                current_focus = cls._current_focus_info.copy() if cls._current_focus_info else None
                recent_focus = cls._focus_history[:5] if cls._focus_history else []
            
            # 杂鱼♡～获取剪贴板拥有者喵～
            owner_hwnd = Win32API.user32.GetClipboardOwner()
            owner_info = None
            if owner_hwnd:
                owner_info = cls._get_window_info(owner_hwnd, "剪贴板拥有者")
            
            # 杂鱼♡～获取智能分析结果喵～
            source_info = cls.get_source_application_info()
            
            result_lines.append("杂鱼♡～智能源应用程序分析结果喵～")
            result_lines.append(f"置信度: {source_info.get('confidence_level', '未知')}")
            result_lines.append(f"检测方法: {source_info.get('detection_method', 'unknown')}")
            
            if source_info.get('process_name'):
                result_lines.append(f"进程名: {source_info['process_name']}")
                result_lines.append(f"可执行文件路径: {source_info.get('process_path', 'Unknown')}")
                result_lines.append(f"窗口标题: {source_info.get('window_title', 'Unknown')}")
                result_lines.append(f"窗口类名: {source_info.get('window_class', 'Unknown')}")
                result_lines.append(f"进程ID: {source_info.get('process_id', 'Unknown')}")
            
            # 杂鱼♡～显示详细分析信息喵～
            result_lines.append("\n" + "="*30)
            result_lines.append("杂鱼♡～详细分析信息喵～")
            
            # 杂鱼♡～当前焦点信息喵～
            if current_focus:
                result_lines.append(f"\n当前焦点应用程序:")
                result_lines.append(f"  进程: {current_focus['exe_info']['name']}")
                result_lines.append(f"  窗口: {current_focus['title']}")
                result_lines.append(f"  PID: {current_focus['pid']}")
                if current_focus.get('focus_time'):
                    focus_age = time.time() - current_focus['focus_time']
                    result_lines.append(f"  获得焦点时间: {focus_age:.1f}秒前")
            
            # 杂鱼♡～剪贴板拥有者信息喵～
            if owner_info and isinstance(owner_info, dict):
                result_lines.append(f"\n剪贴板拥有者:")
                result_lines.append(f"  进程: {owner_info['exe_info']['name']}")
                result_lines.append(f"  窗口: {owner_info['title']}")
                result_lines.append(f"  PID: {owner_info['pid']}")
            elif owner_hwnd:
                result_lines.append(f"\n剪贴板拥有者: {owner_info}")
            else:
                result_lines.append(f"\n剪贴板拥有者: 无法获取")
            
            # 杂鱼♡～最近焦点历史喵～
            if recent_focus:
                result_lines.append(f"\n最近焦点历史:")
                for i, focus in enumerate(recent_focus[:3]):
                    age = time.time() - focus.get('focus_time', 0)
                    result_lines.append(f"  {i+1}. {focus['exe_info']['name']} - {focus['title']} ({age:.1f}秒前)")
            
            return "\n".join(result_lines) if result_lines else "杂鱼♡～无法获取任何应用程序信息喵～"
            
        except Exception as e:
            return f"杂鱼♡～详细分析时出错喵～：{str(e)}"

    @classmethod  
    def get_focus_status(cls) -> Dict[str, Any]:
        """杂鱼♡～获取焦点跟踪状态喵～"""
        with cls._focus_lock:
            return {
                "is_tracking": cls._is_tracking,
                "current_focus": cls._current_focus_info.copy() if cls._current_focus_info else None,
                "focus_history_count": len(cls._focus_history),
                "has_hook": cls._focus_hook_handle is not None,
                "message_thread_alive": cls._message_loop_thread.is_alive() if cls._message_loop_thread else False,
            }


# 杂鱼♡～保持向后兼容性喵～
__all__ = ["SourceTracker"]
