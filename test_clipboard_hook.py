# 杂鱼♡～简单的剪贴板钩子测试喵～
"""
杂鱼♡～测试Windows剪贴板钩子是否正常工作喵～
现在还能检测是哪个杂鱼程序复制的内容喵～
添加了焦点跟踪钩子来准确识别源应用程序喵～
现在把主循环放到一个独立的线程里了，可以随时按Ctrl+C优雅地停下喵～
(这次修复了线程会冻结的问题喵！)
"""
import ctypes
import ctypes.wintypes as w
import sys
import os
import threading
import time

# --- 杂鱼♡～Windows API 和常量定义喵～ ---
user32 = ctypes.WinDLL('user32')
kernel32 = ctypes.WinDLL('kernel32')
shell32 = ctypes.WinDLL('shell32')
psapi = ctypes.WinDLL('psapi')

# 杂鱼♡～消息常量喵～
WM_CLIPBOARDUPDATE = 0x031D
WM_QUIT = 0x0012 # 杂鱼♡～我们需要这个来优雅地退出喵～

# 杂鱼♡～窗口事件常量喵～
EVENT_SYSTEM_FOREGROUND = 0x0003
WINEVENT_OUTOFCONTEXT = 0x0000
WINEVENT_SKIPOWNPROCESS = 0x0002

# 杂鱼♡～进程访问权限常量喵～
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

# 杂鱼♡～剪贴板格式喵～
PREDEFINED_FORMATS = {
    1: "CF_TEXT", 2: "CF_BITMAP", 3: "CF_METAFILEPICT", 4: "CF_SYLK",
    5: "CF_DIF", 6: "CF_TIFF", 7: "CF_OEMTEXT", 8: "CF_DIB",
    9: "CF_PALETTE", 10: "CF_PENDATA", 11: "CF_RIFF", 12: "CF_WAVE",
    13: "CF_UNICODETEXT", 14: "CF_ENHMETAFILE", 15: "CF_HDROP",
    16: "CF_LOCALE", 17: "CF_DIBV5",
}

# --- 杂鱼♡～定义API函数签名，这是修复的关键喵～ ---
user32.OpenClipboard.argtypes = [w.HWND]
user32.OpenClipboard.restype = w.BOOL
user32.CloseClipboard.restype = w.BOOL
user32.EnumClipboardFormats.argtypes = [w.UINT]
user32.EnumClipboardFormats.restype = w.UINT
user32.GetClipboardFormatNameW.argtypes = [w.UINT, w.LPWSTR, ctypes.c_int]
user32.GetClipboardFormatNameW.restype = ctypes.c_int
user32.GetClipboardData.argtypes = [w.UINT]
user32.GetClipboardData.restype = w.HANDLE
user32.DefWindowProcW.argtypes = [w.HWND, w.UINT, w.WPARAM, w.LPARAM]
user32.DefWindowProcW.restype = w.LPARAM
user32.AddClipboardFormatListener.argtypes = [w.HWND]
user32.AddClipboardFormatListener.restype = w.BOOL
user32.PostThreadMessageW.argtypes = [w.DWORD, w.UINT, w.WPARAM, w.LPARAM]
user32.PostThreadMessageW.restype = w.BOOL
user32.GetClipboardOwner.restype = w.HWND
user32.GetWindowThreadProcessId.argtypes = [w.HWND, ctypes.POINTER(w.DWORD)]
user32.GetWindowThreadProcessId.restype = w.DWORD
user32.GetWindowTextW.argtypes = [w.HWND, w.LPWSTR, ctypes.c_int]
user32.GetWindowTextW.restype = ctypes.c_int
user32.IsWindow.argtypes = [w.HWND]
user32.IsWindow.restype = w.BOOL
user32.GetForegroundWindow.restype = w.HWND
user32.GetWindowTextLengthW.argtypes = [w.HWND]
user32.GetWindowTextLengthW.restype = ctypes.c_int
user32.GetClassNameW.argtypes = [w.HWND, w.LPWSTR, ctypes.c_int]
user32.GetClassNameW.restype = ctypes.c_int
WINEVENTPROC = ctypes.WINFUNCTYPE(None, w.HANDLE, w.DWORD, w.HWND, w.LONG, w.LONG, w.DWORD, w.DWORD)
user32.SetWinEventHook.argtypes = [w.DWORD, w.DWORD, w.HANDLE, WINEVENTPROC, w.DWORD, w.DWORD, w.DWORD]
user32.SetWinEventHook.restype = w.HANDLE
user32.UnhookWinEvent.argtypes = [w.HANDLE]
user32.UnhookWinEvent.restype = w.BOOL
WNDENUMPROC = ctypes.WINFUNCTYPE(w.BOOL, w.HWND, w.LPARAM)
user32.EnumWindows.argtypes = [WNDENUMPROC, w.LPARAM]
user32.EnumWindows.restype = w.BOOL
user32.IsWindowVisible.argtypes = [w.HWND]
user32.IsWindowVisible.restype = w.BOOL
user32.GetWindow.argtypes = [w.HWND, w.UINT]
user32.GetWindow.restype = w.HWND
user32.GetParent.argtypes = [w.HWND]
user32.GetParent.restype = w.HWND
kernel32.GlobalLock.argtypes = [w.HGLOBAL]
kernel32.GlobalLock.restype = w.LPVOID
kernel32.GlobalUnlock.argtypes = [w.HGLOBAL]
kernel32.GlobalUnlock.restype = w.BOOL
kernel32.GetLastError.restype = w.DWORD
kernel32.OpenProcess.argtypes = [w.DWORD, w.BOOL, w.DWORD]
kernel32.OpenProcess.restype = w.HANDLE
kernel32.CloseHandle.argtypes = [w.HANDLE]
kernel32.CloseHandle.restype = w.BOOL
kernel32.QueryFullProcessImageNameW.argtypes = [w.HANDLE, w.DWORD, w.LPWSTR, ctypes.POINTER(w.DWORD)]
kernel32.QueryFullProcessImageNameW.restype = w.BOOL
kernel32.CreateToolhelp32Snapshot.argtypes = [w.DWORD, w.DWORD]
kernel32.CreateToolhelp32Snapshot.restype = w.HANDLE
kernel32.Process32FirstW.argtypes = [w.HANDLE, ctypes.c_void_p]
kernel32.Process32FirstW.restype = w.BOOL
kernel32.Process32NextW.argtypes = [w.HANDLE, ctypes.c_void_p]
kernel32.Process32NextW.restype = w.BOOL
kernel32.GetCurrentThreadId.restype = w.DWORD
shell32.DragQueryFileW.argtypes = [w.HANDLE, w.UINT, w.LPWSTR, w.UINT]
shell32.DragQueryFileW.restype = w.UINT
psapi.GetModuleFileNameExW.argtypes = [w.HANDLE, w.HANDLE, w.LPWSTR, w.DWORD]
psapi.GetModuleFileNameExW.restype = w.DWORD

# 杂鱼♡～进程快照常量喵～
TH32CS_SNAPPROCESS = 0x00000002
GW_HWNDPREV = 3

# 杂鱼♡～进程信息结构体喵～
class PROCESSENTRY32W(ctypes.Structure):
    _fields_ = [
        ('dwSize', w.DWORD), ('cntUsage', w.DWORD), ('th32ProcessID', w.DWORD),
        ('th32DefaultHeapID', ctypes.POINTER(w.ULONG)), ('th32ModuleID', w.DWORD),
        ('cntThreads', w.DWORD), ('th32ParentProcessID', w.DWORD),
        ('pcPriClassBase', w.LONG), ('dwFlags', w.DWORD), ('szExeFile', w.WCHAR * 260)
    ]

# 杂鱼♡～全局变量喵～
message_count = 0
focus_history = []
current_focus_info = None
focus_lock = threading.Lock()

# 杂鱼♡～系统进程黑名单喵～
SYSTEM_PROCESSES = {
    'svchost.exe', 'dwm.exe', 'explorer.exe', 'winlogon.exe', 'csrss.exe',
    'screenclippinghost.exe', 'taskhostw.exe', 'runtimebroker.exe',
    'sihost.exe', 'shellexperiencehost.exe', 'searchui.exe', 'cortana.exe',
    'windowsinternal.composableshell.experiences.textinput.inputapp.exe',
    'applicationframehost.exe', 'searchapp.exe', 'startmenuexperiencehost.exe'
}

# 杂鱼♡～以下是回调和工具函数，保持不变喵～
def winevent_proc(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    """杂鱼♡～窗口事件钩子回调函数喵～"""
    global current_focus_info, focus_history
    if event == EVENT_SYSTEM_FOREGROUND and hwnd:
        try:
            window_info = get_window_info(hwnd, "")
            if isinstance(window_info, dict):
                if (window_info['exe_info']['name'].lower() not in SYSTEM_PROCESSES and
                    window_info['title'] != "杂鱼♡～无标题" and
                    len(window_info['title'].strip()) > 0):
                    with focus_lock:
                        current_focus_info = window_info.copy()
                        current_focus_info['focus_time'] = time.time()
                        focus_history = [f for f in focus_history if f['exe_info']['name'].lower() != window_info['exe_info']['name'].lower()]
                        focus_history.insert(0, current_focus_info)
                        focus_history = focus_history[:10]
        except Exception:
            pass

def get_process_path(process_id):
    """杂鱼♡～获取进程路径信息喵～"""
    try:
        process_handle = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_QUERY_LIMITED_INFORMATION, False, process_id)
        if not process_handle:
            process_handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, process_id)
        if not process_handle:
            return {'name': f'PID:{process_id}', 'path': '杂鱼♡～无法打开进程'}
        try:
            path_buffer = ctypes.create_unicode_buffer(1024)
            path_size = w.DWORD(1024)
            if kernel32.QueryFullProcessImageNameW(process_handle, 0, path_buffer, ctypes.byref(path_size)):
                exe_path = path_buffer.value
            else:
                if psapi.GetModuleFileNameExW(process_handle, None, path_buffer, 1024):
                    exe_path = path_buffer.value
                else:
                    return {'name': f'PID:{process_id}', 'path': '杂鱼♡～无法获取路径'}
            return {'name': os.path.basename(exe_path), 'path': exe_path}
        finally:
            kernel32.CloseHandle(process_handle)
    except Exception as e:
        return {'name': f'PID:{process_id}', 'path': f'杂鱼♡～出错：{str(e)}'}

def get_window_info(hwnd, description=""):
    """杂鱼♡～获取窗口详细信息的通用函数喵～"""
    if not hwnd or not user32.IsWindow(hwnd):
        return f"杂鱼♡～{description}窗口无效喵～"
    try:
        title_length = user32.GetWindowTextLengthW(hwnd)
        window_title = "杂鱼♡～无标题"
        if title_length > 0:
            buffer = ctypes.create_unicode_buffer(title_length + 1)
            if user32.GetWindowTextW(hwnd, buffer, title_length + 1) > 0:
                window_title = buffer.value
        class_buffer = ctypes.create_unicode_buffer(256)
        window_class = "杂鱼♡～未知类名"
        if user32.GetClassNameW(hwnd, class_buffer, 256) > 0:
            window_class = class_buffer.value
        process_id = w.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
        if not process_id.value:
            return f"杂鱼♡～{description}无法获取进程ID喵～"
        return {
            'title': window_title, 'class': window_class, 'pid': process_id.value,
            'exe_info': get_process_path(process_id.value), 'hwnd': hwnd
        }
    except Exception as e:
        return f"杂鱼♡～获取{description}窗口信息时出错喵～：{str(e)}"

def get_smart_source_analysis():
    """杂鱼♡～智能源应用程序分析（结合焦点信息）喵～"""
    # This function remains the same, it correctly uses the global state
    # protected by the focus_lock.
    with focus_lock:
        current_focus = current_focus_info.copy() if current_focus_info else None
        recent_focus = focus_history[:5] if focus_history else []
    
    owner_hwnd = user32.GetClipboardOwner()
    owner_info = get_window_info(owner_hwnd, "剪贴板拥有者") if owner_hwnd else None
    
    real_source, confidence = None, "未知"
    
    if current_focus:
        if isinstance(owner_info, dict) and current_focus['pid'] == owner_info['pid']:
            real_source, confidence = current_focus, "高 (当前焦点 = 拥有者)"
        elif current_focus.get('focus_time', 0) > time.time() - 2:
            real_source, confidence = current_focus, "中 (最近获得焦点)"
        elif isinstance(owner_info, dict) and owner_info['exe_info']['name'].lower() in SYSTEM_PROCESSES:
            real_source, confidence = current_focus, "中 (拥有者是系统进程)"

    if not real_source and isinstance(owner_info, dict):
        real_source, confidence = owner_info, "低 (仅基于拥有者)"
    
    if not real_source and recent_focus:
        real_source, confidence = recent_focus[0], "低 (基于最近焦点历史)"

    if real_source:
        return (f"杂鱼♡～智能源分析结果 (置信度: {confidence}) 喵～\n"
                f"  - 进程: {real_source['exe_info']['name']} (PID: {real_source['pid']})\n"
                f"  - 路径: {real_source['exe_info']['path']}\n"
                f"  - 标题: {real_source['title']}")
    return "杂鱼♡～无法获取任何应用程序信息喵～"


def get_clipboard_info():
    """杂鱼♡～获取剪贴板详细信息（安全版）喵～"""
    if not user32.OpenClipboard(None): return "杂鱼♡～打开剪贴板失败喵！"
    info_lines = ["杂鱼♡～剪贴板内容分析喵～"]
    try:
        formats = []
        fmt = 0
        while True:
            fmt = user32.EnumClipboardFormats(fmt)
            if fmt == 0: break
            formats.append(fmt)
        info_lines.append(f"杂鱼♡～检测到 {len(formats)} 种数据格式喵～")
        for f in formats:
            name = PREDEFINED_FORMATS.get(f)
            if not name:
                buf = ctypes.create_unicode_buffer(256)
                if user32.GetClipboardFormatNameW(f, buf, 256) > 0:
                    name = f"自定义: {buf.value}"
                else:
                    name = f"未知/无名格式"
            info_lines.append(f"  - {name} (ID: {f})")

        if 13 in formats: # CF_UNICODETEXT
            handle = user32.GetClipboardData(13)
            if handle:
                ptr = kernel32.GlobalLock(handle)
                if ptr:
                    try:
                        text = ctypes.c_wchar_p(ptr).value
                        preview = text[:200] + ('...' if len(text) > 200 else '')
                        info_lines.append(f"文本预览: \"{preview}\"")
                    finally:
                        kernel32.GlobalUnlock(handle)
        if 15 in formats: # CF_HDROP
            handle = user32.GetClipboardData(15)
            if handle:
                count = shell32.DragQueryFileW(handle, 0xFFFFFFFF, None, 0)
                info_lines.append(f"文件列表 ({count} 个):")
                for i in range(min(count, 10)):
                    buf = ctypes.create_unicode_buffer(260)
                    shell32.DragQueryFileW(handle, i, buf, 260)
                    info_lines.append(f"  - {buf.value}")
    finally:
        user32.CloseClipboard()
    return "\n".join(info_lines)

def window_proc(hwnd, msg, wParam, lParam):
    """杂鱼♡～窗口过程函数喵～"""
    global message_count
    if msg == WM_CLIPBOARDUPDATE:
        message_count += 1
        print(f"\n{'='*50}\n杂鱼♡～剪贴板更新 #{message_count} 喵～\n{'='*50}")
        print(get_smart_source_analysis())
        print("-" * 25)
        print(get_clipboard_info())
        print(f"{'='*50}\n")
        return 0
    return user32.DefWindowProcW(hwnd, msg, wParam, lParam)

# 杂鱼♡～新的线程封装类喵～
class ClipboardMonitorThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.hwnd = None
        self.focus_hook_handle = None
        self.winevent_proc_func = None
        self.window_proc_func = None
        self.thread_id = None
        self.init_event = threading.Event()

    def setup_focus_hook(self):
        """杂鱼♡～设置窗口焦点钩子喵～"""
        self.winevent_proc_func = WINEVENTPROC(winevent_proc)
        self.focus_hook_handle = user32.SetWinEventHook(
            EVENT_SYSTEM_FOREGROUND, EVENT_SYSTEM_FOREGROUND,
            None, self.winevent_proc_func,
            0, 0, WINEVENT_OUTOFCONTEXT | WINEVENT_SKIPOWNPROCESS
        )
        if self.focus_hook_handle:
            print("杂鱼♡～窗口焦点钩子设置成功喵～")
            current_hwnd = user32.GetForegroundWindow()
            if current_hwnd:
                winevent_proc(None, EVENT_SYSTEM_FOREGROUND, current_hwnd, 0, 0, 0, 0)
            return True
        print(f"杂鱼♡～设置窗口焦点钩子失败喵！错误码：{kernel32.GetLastError()}")
        return False

    def cleanup_focus_hook(self):
        """杂鱼♡～清理窗口焦点钩子喵～"""
        if self.focus_hook_handle:
            user32.UnhookWinEvent(self.focus_hook_handle)
            print("杂鱼♡～窗口焦点钩子已清理喵～")
            self.focus_hook_handle = None

    def run(self):
        """杂鱼♡～线程的主消息循环喵～"""
        self.thread_id = kernel32.GetCurrentThreadId()

        if not self.setup_focus_hook():
            self.init_event.set()
            return
        
        WNDPROC = ctypes.WINFUNCTYPE(w.LPARAM, w.HWND, w.UINT, w.WPARAM, w.LPARAM)
        self.window_proc_func = WNDPROC(window_proc)
        
        hinstance = kernel32.GetModuleHandleW(None)
        self.hwnd = user32.CreateWindowExW(0, "STATIC", "ClipboardTest", 0, 0, 0, 0, 0, w.HWND(-3), None, hinstance, None)
        
        if not self.hwnd:
            print(f"杂鱼♡～创建窗口失败喵！错误码：{kernel32.GetLastError()}")
            self.init_event.set()
            return

        GWLP_WNDPROC = -4
        if sys.maxsize > 2**32:
            user32.SetWindowLongPtrW.argtypes = [w.HWND, ctypes.c_int, WNDPROC]
            user32.SetWindowLongPtrW.restype = WNDPROC
            user32.SetWindowLongPtrW(self.hwnd, GWLP_WNDPROC, self.window_proc_func)
        else:
            user32.SetWindowLongW.argtypes = [w.HWND, ctypes.c_int, WNDPROC]
            user32.SetWindowLongW.restype = WNDPROC
            user32.SetWindowLongW(self.hwnd, GWLP_WNDPROC, self.window_proc_func)

        if not user32.AddClipboardFormatListener(self.hwnd):
            print(f"杂鱼♡～添加剪贴板监听器失败喵！错误码：{kernel32.GetLastError()}")
            user32.DestroyWindow(self.hwnd)
            self.init_event.set()
            return
            
        print("杂鱼♡～剪贴板监听器添加成功喵～")
        print("杂鱼♡～现在可以复制一些内容测试喵～")
        print("杂鱼♡～按Ctrl+C结束测试喵～")
        
        # Signal that initialization is complete
        self.init_event.set()
        
        msg = w.MSG()
        #
        # --- 杂鱼♡～这就是关键的修复喵！ ---
        # Using NULL (None) for the HWND makes GetMessageW retrieve both
        # window messages AND thread messages (like WM_QUIT).
        #
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
            
        # Cleanup after the loop is broken
        print("杂鱼♡～消息循环结束，开始清理喵～")
        if self.hwnd:
            user32.DestroyWindow(self.hwnd)
            print("杂鱼♡～销毁窗口喵～")
        self.cleanup_focus_hook()
    
    def stop(self):
        """杂鱼♡～从外部停止线程的方法喵～"""
        if self.thread_id:
            print("杂鱼♡～正在发送退出消息给监控线程喵～")
            user32.PostThreadMessageW(self.thread_id, WM_QUIT, 0, 0)

# 杂鱼♡～这里是新的主程序入口喵～
if __name__ == "__main__":
    monitor_thread = ClipboardMonitorThread()
    try:
        monitor_thread.start()
        # Wait for the thread to signal that it's initialized before continuing
        monitor_thread.init_event.wait()
        
        # Keep the main thread alive to listen for KeyboardInterrupt
        while monitor_thread.is_alive():
            time.sleep(0.5) # A simple wait
    except KeyboardInterrupt:
        print("\n杂鱼♡～用户中断测试喵～")
    finally:
        if monitor_thread.is_alive():
            monitor_thread.stop()
            monitor_thread.join() # Wait for the thread to fully clean up and exit
        print("杂鱼♡～再见了喵～")

