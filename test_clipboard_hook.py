# 杂鱼♡～简单的剪贴板钩子测试喵～
"""

杂鱼♡～测试Windows剪贴板钩子是否正常工作喵～
现在还能检测是哪个杂鱼程序复制的内容喵～
"""
import ctypes
import ctypes.wintypes as w
import sys
import os

# --- 杂鱼♡～Windows API 和常量定义喵～ ---
user32 = ctypes.WinDLL('user32')
kernel32 = ctypes.WinDLL('kernel32')
shell32 = ctypes.WinDLL('shell32')
psapi = ctypes.WinDLL('psapi')

# 杂鱼♡～消息常量喵～
WM_CLIPBOARDUPDATE = 0x031D

# 杂鱼♡～进程访问权限常量喵～
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

# 杂鱼♡～剪贴板格式喵～
PREDEFINED_FORMATS = {
    1: "CF_TEXT",
    2: "CF_BITMAP",
    3: "CF_METAFILEPICT",
    4: "CF_SYLK",
    5: "CF_DIF",
    6: "CF_TIFF",
    7: "CF_OEMTEXT",
    8: "CF_DIB",
    9: "CF_PALETTE",
    10: "CF_PENDATA",
    11: "CF_RIFF",
    12: "CF_WAVE",
    13: "CF_UNICODETEXT",
    14: "CF_ENHMETAFILE",
    15: "CF_HDROP",
    16: "CF_LOCALE",
    17: "CF_DIBV5",
    # 更多其他格式可以按需添加喵～
}

# --- 杂鱼♡～定义API函数签名，这是修复的关键喵～ ---
# By defining argtypes and restype, we ensure ctypes handles data correctly on both 32-bit and 64-bit systems.
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

# 杂鱼♡～新增的API函数签名，用于获取源应用程序喵～
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
# 杂鱼♡～定义WNDENUMPROC函数指针类型喵～
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
        ('dwSize', w.DWORD),
        ('cntUsage', w.DWORD),
        ('th32ProcessID', w.DWORD),
        ('th32DefaultHeapID', ctypes.POINTER(w.ULONG)),
        ('th32ModuleID', w.DWORD),
        ('cntThreads', w.DWORD),
        ('th32ParentProcessID', w.DWORD),
        ('pcPriClassBase', w.LONG),
        ('dwFlags', w.DWORD),
        ('szExeFile', w.WCHAR * 260)
    ]

# 杂鱼♡～消息计数器和运行状态喵～
message_count = 0
running = True
window_proc_func = None # 杂鱼♡～防止被垃圾回收喵～
recent_windows = [] # 杂鱼♡～最近活动窗口历史喵～
last_foreground_hwnd = None # 杂鱼♡～上一个前台窗口喵～

# 杂鱼♡～系统进程黑名单喵～
SYSTEM_PROCESSES = {
    'svchost.exe', 'dwm.exe', 'explorer.exe', 'winlogon.exe', 'csrss.exe',
    'screenclippinghost.exe', 'taskhostw.exe', 'runtimebroker.exe',
    'sihost.exe', 'shellexperiencehost.exe', 'searchui.exe', 'cortana.exe',
    'windowsinternal.composableshell.experiences.textinput.inputapp.exe'
}

def get_parent_process_info(process_id):
    """杂鱼♡～获取父进程信息喵～"""
    try:
        # 杂鱼♡～创建进程快照喵～
        snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        if snapshot == -1:
            return None
        
        try:
            pe32 = PROCESSENTRY32W()
            pe32.dwSize = ctypes.sizeof(PROCESSENTRY32W)
            
            if not kernel32.Process32FirstW(snapshot, ctypes.byref(pe32)):
                return None
            
            parent_chain = []
            current_pid = process_id
            
            # 杂鱼♡～向上追踪5层父进程喵～
            for depth in range(5):
                found_parent = False
                
                # 杂鱼♡～重置枚举位置喵～
                kernel32.Process32FirstW(snapshot, ctypes.byref(pe32))
                
                while True:
                    if pe32.th32ProcessID == current_pid:
                        parent_pid = pe32.th32ParentProcessID
                        if parent_pid != 0 and parent_pid != current_pid:
                            parent_info = get_process_path(parent_pid)
                            parent_chain.append({
                                'pid': parent_pid,
                                'name': parent_info['name'],
                                'path': parent_info['path'],
                                'depth': depth + 1
                            })
                            current_pid = parent_pid
                            found_parent = True
                        break
                    
                    if not kernel32.Process32NextW(snapshot, ctypes.byref(pe32)):
                        break
                
                if not found_parent:
                    break
            
            return parent_chain
            
        finally:
            kernel32.CloseHandle(snapshot)
            
    except Exception as e:
        return [{'error': f'杂鱼♡～获取父进程信息失败喵～：{str(e)}'}]

def enum_windows_callback(hwnd, lParam):
    """杂鱼♡～枚举窗口回调函数喵～"""
    try:
        windows_list = ctypes.cast(lParam, ctypes.py_object).value
        
        if not user32.IsWindowVisible(hwnd):
            return True
        
        # 杂鱼♡～获取窗口信息喵～
        window_info = get_window_info(hwnd, "")
        if isinstance(window_info, dict):
            # 杂鱼♡～过滤掉明显的系统窗口喵～
            if (window_info['title'] and 
                window_info['title'] != "杂鱼♡～无标题" and
                window_info['exe_info']['name'].lower() not in SYSTEM_PROCESSES and
                len(window_info['title'].strip()) > 0):
                windows_list.append(window_info)
        
        return True
    except:
        return True

def get_all_visible_windows():
    """杂鱼♡～获取所有可见窗口列表喵～"""
    try:
        windows_list = []
        enum_proc = WNDENUMPROC(enum_windows_callback)
        
        user32.EnumWindows(enum_proc, ctypes.py_object(windows_list))
        
        # 杂鱼♡～按进程名排序并去重喵～
        unique_apps = {}
        for window in windows_list:
            app_key = window['exe_info']['name'].lower()
            if app_key not in unique_apps or len(window['title']) > len(unique_apps[app_key]['title']):
                unique_apps[app_key] = window
        
        return list(unique_apps.values())
        
    except Exception as e:
        return [{'error': f'杂鱼♡～枚举窗口失败喵～：{str(e)}'}]

def update_window_history(current_hwnd):
    """杂鱼♡～更新窗口活动历史喵～"""
    global recent_windows, last_foreground_hwnd
    
    try:
        if current_hwnd and current_hwnd != last_foreground_hwnd:
            window_info = get_window_info(current_hwnd, "")
            if isinstance(window_info, dict):
                # 杂鱼♡～检查是否为非系统窗口喵～
                if (window_info['exe_info']['name'].lower() not in SYSTEM_PROCESSES and
                    window_info['title'] != "杂鱼♡～无标题" and
                    len(window_info['title'].strip()) > 0):
                    
                    # 杂鱼♡～移除已存在的相同进程喵～
                    recent_windows = [w for w in recent_windows 
                                    if w['exe_info']['name'].lower() != window_info['exe_info']['name'].lower()]
                    
                    # 杂鱼♡～添加到历史前面喵～
                    recent_windows.insert(0, window_info)
                    
                    # 杂鱼♡～只保留最近5个喵～
                    recent_windows = recent_windows[:5]
            
            last_foreground_hwnd = current_hwnd
            
    except Exception:
        pass

def get_deep_source_analysis():
    """杂鱼♡～深度源应用程序分析喵～"""
    try:
        result_lines = []
        
        # 杂鱼♡～方法1：获取剪贴板拥有者窗口喵～
        owner_hwnd = user32.GetClipboardOwner()
        if owner_hwnd:
            owner_info = get_window_info(owner_hwnd, "剪贴板拥有者")
            if isinstance(owner_info, dict):
                result_lines.append("杂鱼♡～剪贴板拥有者信息喵～")
                result_lines.append(f"  进程: {owner_info['exe_info']['name']}")
                result_lines.append(f"  路径: {owner_info['exe_info']['path']}")
                result_lines.append(f"  窗口: {owner_info['title']}")
                result_lines.append(f"  类名: {owner_info['class']}")
                result_lines.append(f"  PID: {owner_info['pid']}")
                
                # 杂鱼♡～如果是系统进程，分析父进程链喵～
                if owner_info['exe_info']['name'].lower() in SYSTEM_PROCESSES:
                    parent_chain = get_parent_process_info(owner_info['pid'])
                    if parent_chain:
                        result_lines.append("  杂鱼♡～父进程链:")
                        for parent in parent_chain:
                            if 'error' not in parent:
                                result_lines.append(f"    └─ 第{parent['depth']}层: {parent['name']} (PID: {parent['pid']})")
            else:
                result_lines.append(f"杂鱼♡～剪贴板拥有者：{owner_info}")
        else:
            result_lines.append("杂鱼♡～无法获取剪贴板拥有者喵～（可能是系统操作）")
        
        # 杂鱼♡～方法2：获取前台窗口（当前活动窗口）喵～
        foreground_hwnd = user32.GetForegroundWindow()
        if foreground_hwnd:
            # 杂鱼♡～更新窗口历史喵～
            update_window_history(foreground_hwnd)
            
            if foreground_hwnd != owner_hwnd:
                foreground_info = get_window_info(foreground_hwnd, "前台")
                if isinstance(foreground_info, dict):
                    result_lines.append("\n杂鱼♡～当前前台应用程序喵～")
                    result_lines.append(f"  进程: {foreground_info['exe_info']['name']}")
                    result_lines.append(f"  路径: {foreground_info['exe_info']['path']}")
                    result_lines.append(f"  窗口: {foreground_info['title']}")
                    result_lines.append(f"  类名: {foreground_info['class']}")
                    result_lines.append(f"  PID: {foreground_info['pid']}")
                    
                    # 杂鱼♡～如果前台也是系统进程，分析父进程链喵～
                    if foreground_info['exe_info']['name'].lower() in SYSTEM_PROCESSES:
                        parent_chain = get_parent_process_info(foreground_info['pid'])
                        if parent_chain:
                            result_lines.append("  杂鱼♡～父进程链:")
                            for parent in parent_chain:
                                if 'error' not in parent:
                                    result_lines.append(f"    └─ 第{parent['depth']}层: {parent['name']} (PID: {parent['pid']})")
        
        # 杂鱼♡～方法3：显示最近活动的应用程序历史喵～
        if recent_windows:
            result_lines.append("\n杂鱼♡～最近活动的应用程序喵～")
            for i, window in enumerate(recent_windows):
                result_lines.append(f"  {i+1}. {window['exe_info']['name']} - {window['title']}")
        
        # 杂鱼♡～方法4：如果检测到系统服务操作，显示可能的真实源应用程序喵～
        if (owner_hwnd and foreground_hwnd and 
            isinstance(get_window_info(owner_hwnd, ""), dict) and 
            isinstance(get_window_info(foreground_hwnd, ""), dict)):
            
            owner_name = get_window_info(owner_hwnd, "")['exe_info']['name'].lower()
            foreground_name = get_window_info(foreground_hwnd, "")['exe_info']['name'].lower()
            
            if owner_name in SYSTEM_PROCESSES or foreground_name in SYSTEM_PROCESSES:
                result_lines.insert(0, "杂鱼♡～检测到系统服务操作剪贴板喵～")
                
                # 杂鱼♡～尝试找到真正的用户应用程序喵～
                if recent_windows:
                    real_app = recent_windows[0]  # 最近的非系统应用
                    result_lines.append(f"\n杂鱼♡～推测的真实源应用程序喵～")
                    result_lines.append(f"  进程: {real_app['exe_info']['name']}")
                    result_lines.append(f"  路径: {real_app['exe_info']['path']}")
                    result_lines.append(f"  窗口: {real_app['title']}")
                    result_lines.append(f"  PID: {real_app['pid']}")
        
        return "\n".join(result_lines) if result_lines else "杂鱼♡～无法获取任何应用程序信息喵～"
        
    except Exception as e:
        return f"杂鱼♡～深度分析时出错喵～：{str(e)}"

def get_source_application():
    """杂鱼♡～获取剪贴板源应用程序信息（简化版，用于向后兼容）喵～"""
    return get_deep_source_analysis()

def get_window_info(hwnd, description=""):
    """杂鱼♡～获取窗口详细信息的通用函数喵～"""
    if not hwnd or not user32.IsWindow(hwnd):
        return f"杂鱼♡～{description}窗口无效喵～"
    
    try:
        # 杂鱼♡～获取窗口标题（改进版）喵～
        title_length = user32.GetWindowTextLengthW(hwnd)
        if title_length > 0:
            window_title_buffer = ctypes.create_unicode_buffer(title_length + 1)
            actual_length = user32.GetWindowTextW(hwnd, window_title_buffer, title_length + 1)
            window_title = window_title_buffer.value if actual_length > 0 else "杂鱼♡～无标题"
        else:
            window_title = "杂鱼♡～无标题"
        
        # 杂鱼♡～获取窗口类名喵～
        class_buffer = ctypes.create_unicode_buffer(256)
        class_length = user32.GetClassNameW(hwnd, class_buffer, 256)
        window_class = class_buffer.value if class_length > 0 else "杂鱼♡～未知类名"
        
        # 杂鱼♡～获取进程信息喵～
        process_id = w.DWORD()
        thread_id = user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
        
        if not process_id.value:
            return f"杂鱼♡～{description}无法获取进程ID喵～（窗口：{window_title}，类名：{window_class}）"
        
        # 杂鱼♡～获取可执行文件路径喵～
        exe_info = get_process_path(process_id.value)
        
        return {
            'title': window_title,
            'class': window_class,
            'pid': process_id.value,
            'exe_info': exe_info,
            'hwnd': hwnd
        }
        
    except Exception as e:
        return f"杂鱼♡～获取{description}窗口信息时出错喵～：{str(e)}"

def get_process_path(process_id):
    """杂鱼♡～获取进程路径信息喵～"""
    try:
        # 杂鱼♡～打开进程获取详细信息喵～
        process_handle = kernel32.OpenProcess(
            PROCESS_QUERY_INFORMATION | PROCESS_QUERY_LIMITED_INFORMATION, 
            False, 
            process_id
        )
        
        if not process_handle:
            # 杂鱼♡～尝试较低权限喵～
            process_handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, process_id)
        
        if not process_handle:
            return f"杂鱼♡～无法打开进程 PID:{process_id} 喵～"
        
        try:
            # 杂鱼♡～尝试获取完整进程路径喵～
            exe_path = None
            
            # 杂鱼♡～方法1：使用QueryFullProcessImageName（推荐）喵～
            path_buffer = ctypes.create_unicode_buffer(1024)
            path_size = w.DWORD(1024)
            if kernel32.QueryFullProcessImageNameW(process_handle, 0, path_buffer, ctypes.byref(path_size)):
                exe_path = path_buffer.value
            
            # 杂鱼♡～方法2：如果方法1失败，尝试GetModuleFileNameEx喵～
            if not exe_path:
                path_buffer = ctypes.create_unicode_buffer(1024)
                if psapi.GetModuleFileNameExW(process_handle, None, path_buffer, 1024):
                    exe_path = path_buffer.value
            
            if exe_path:
                exe_name = os.path.basename(exe_path)
                return {'name': exe_name, 'path': exe_path}
            else:
                return {'name': f'PID:{process_id}', 'path': '杂鱼♡～无法获取路径'}
                
        finally:
            kernel32.CloseHandle(process_handle)
            
    except Exception as e:
        return {'name': f'PID:{process_id}', 'path': f'杂鱼♡～出错：{str(e)}'}

def get_clipboard_info():
    """杂鱼♡～获取剪贴板详细信息（安全版）喵～"""
    if not user32.OpenClipboard(None):
        return "杂鱼♡～打开剪贴板失败喵！"

    info_lines = ["杂鱼♡～剪贴板内容分析喵～"]
    try:
        # 杂鱼♡～枚举所有格式喵～
        formats = []
        format_id = 0
        while True:
            format_id = user32.EnumClipboardFormats(format_id)
            if format_id == 0:
                break
            formats.append(format_id)
        
        info_lines.append(f"杂鱼♡～检测到 {len(formats)} 种数据格式喵～")

        # 杂鱼♡～显示所有格式名称喵～
        for fmt in formats:
            # 杂鱼♡～先检查是不是预定义格式喵～
            format_name = PREDEFINED_FORMATS.get(fmt)
            if format_name:
                info_lines.append(f"  - 内置格式: {format_name} (ID: {fmt})")
            else:
                # 杂鱼♡～如果不是，再尝试获取自定义格式名称喵～
                buffer = ctypes.create_unicode_buffer(256)
                if user32.GetClipboardFormatNameW(fmt, buffer, 256) > 0:
                    info_lines.append(f"  - 自定义格式: {buffer.value} (ID: {fmt})")
                else:
                    # 杂鱼♡～未知的格式喵～
                    info_lines.append(f"  - 未知/无名格式 (ID: {fmt})")

        # 杂鱼♡～安全地读取文本内容喵～
        if user32.IsClipboardFormatAvailable(13):
            handle = user32.GetClipboardData(13)
            if handle:
                text_ptr = kernel32.GlobalLock(handle)
                if text_ptr:
                    try:
                        text = ctypes.c_wchar_p(text_ptr).value
                        if text and text.strip():
                            preview = text[:200] + "..." if len(text) > 200 else text
                            info_lines.append(f"杂鱼♡～Unicode文本内容 ({len(text)} 字符):")
                            info_lines.append(f"  \"{preview}\"")
                        else:
                            info_lines.append("杂鱼♡～Unicode文本为空喵！")
                    finally:
                        kernel32.GlobalUnlock(handle)
        
        # 杂鱼♡～安全地读取文件列表喵～
        if user32.IsClipboardFormatAvailable(15):
            handle = user32.GetClipboardData(15)
            if handle:
                file_count = shell32.DragQueryFileW(handle, 0xFFFFFFFF, None, 0)
                info_lines.append(f"杂鱼♡～文件列表 ({file_count} 个文件):")
                for i in range(min(file_count, 10)):
                    buffer = ctypes.create_unicode_buffer(260)
                    shell32.DragQueryFileW(handle, i, buffer, 260)
                    info_lines.append(f"  - {buffer.value}")
                if file_count > 10:
                    info_lines.append(f"  ... 还有 {file_count - 10} 个文件")

    finally:
        user32.CloseClipboard()
    
    return "\n".join(info_lines)

def window_proc(hwnd, msg, wParam, lParam):
    """杂鱼♡～窗口过程函数喵～"""
    global message_count
    
    if msg == WM_CLIPBOARDUPDATE:
        message_count += 1
        print(f"\n{'='*50}")
        print(f"杂鱼♡～剪贴板更新事件 #{message_count} 喵～")
        print(f"{'='*50}")
        
        # 杂鱼♡～获取源应用程序信息喵～
        source_app_info = get_source_application()
        print(source_app_info)
        print("-" * 30)
        
        clipboard_info = get_clipboard_info()
        print(clipboard_info)
        print(f"{'='*50}\n")
        
        return 0
    print(f"杂鱼♡～收到消息：{msg}")
    return user32.DefWindowProcW(hwnd, msg, wParam, lParam)

def main_loop():
    """杂鱼♡～主消息循环喵～"""
    global running, window_proc_func
    
    print("杂鱼♡～开始测试剪贴板钩子喵～")
    
    WNDPROC = ctypes.WINFUNCTYPE(w.LPARAM, w.HWND, w.UINT, w.WPARAM, w.LPARAM)
    window_proc_func = WNDPROC(window_proc)
    
    hinstance = kernel32.GetModuleHandleW(None)
    
    # 杂鱼♡～使用 message-only 窗口，更可靠喵～
    hwnd = user32.CreateWindowExW(0, "STATIC", "ClipboardTest", 0, 0, 0, 0, 0, w.HWND(-3), None, hinstance, None)
    
    if not hwnd:
        print(f"杂鱼♡～创建窗口失败喵！错误码：{kernel32.GetLastError()}")
        return
        
    print(f"杂鱼♡～创建窗口成功，句柄：{hwnd}")
    
    # 杂鱼♡～设置窗口过程喵～
    GWLP_WNDPROC = -4
    if sys.maxsize > 2**32:
        user32.SetWindowLongPtrW.argtypes = [w.HWND, ctypes.c_int, WNDPROC]
        user32.SetWindowLongPtrW.restype = WNDPROC
        user32.SetWindowLongPtrW(hwnd, GWLP_WNDPROC, window_proc_func)
    else:
        user32.SetWindowLongW.argtypes = [w.HWND, ctypes.c_int, WNDPROC]
        user32.SetWindowLongW.restype = WNDPROC
        user32.SetWindowLongW(hwnd, GWLP_WNDPROC, window_proc_func)

    if not user32.AddClipboardFormatListener(hwnd):
        print(f"杂鱼♡～添加剪贴板监听器失败喵！错误码：{kernel32.GetLastError()}")
        user32.DestroyWindow(hwnd)
        return
        
    print("杂鱼♡～剪贴板监听器添加成功喵～")
    print("杂鱼♡～现在可以复制一些内容测试喵～")
    print("杂鱼♡～按Ctrl+C结束测试喵～")
    
    msg = w.MSG()
    try:
        while running and user32.GetMessageW(ctypes.byref(msg), hwnd, 0, 0) != 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
            
    except KeyboardInterrupt:
        print("\n杂鱼♡～用户中断测试喵～")
    finally:
        running = False
        user32.DestroyWindow(hwnd)
        print("杂鱼♡～销毁窗口并结束喵～")

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\n杂鱼♡～再见了喵～")