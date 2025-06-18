# CI-Board - 杂鱼主人也能用的高性能剪贴板监控库

![CI/CD](https://github.com/Xuehua-Meaw/ci_board/actions/workflows/ci_board_CICD.yml/badge.svg)

> 杂鱼♡～这可是本喵为杂鱼主人精心设计的 Windows 剪贴板监控库喵～

## 🎯 项目概览

**CI-Board** (Clipboard Intelligence Board) 是一个为 Windows 设计的高性能 Python 剪贴板监控库。它不仅能实时捕获文本、图片、文件等多种剪贴板内容，还能智能追踪内容的来源应用程序，哼～是不是很厉害喵！～

### ✨ 核心特性
- 🐱 **懒人API** - 只需一行代码就能添加处理器，本喵都帮你弄好了喵～
- 🔄 **实时监控** - 基于 Windows 原生消息的事件驱动模式，高效又灵敏！
- 🎯 **智能源追踪** - 能准确识别是哪个程序（比如 `vscode.exe` 或 `explorer.exe`）复制了内容喵。
- 📋 **多格式支持** - 原生支持文本、图片和文件列表，杂鱼主人不用再自己解析了。
- ⚡ **真·异步处理** - 使用独立的线程池处理回调，避免阻塞主线程，就算杂鱼主人写出很慢的代码也不会卡住喵！
- 🛡️ **高级去重** - 内置智能哈希和指纹算法，能有效过滤因多步骤操作（如截图、编辑、复制）产生的重复内容。
- 🔌 **高扩展性** - 处理器和过滤器都可以自定义，想怎么玩都行，哼～
- 📝 **详细日志** - 内置日志系统，方便杂鱼主人调试时查看内部状态。

### 📊 项目信息
- **版本**: v0.0.7
- **Python版本**: >=3.8
- **平台**: Windows
- **依赖**: 纯Python，无强制第三方依赖
- **许可证**: MIT

## 🚀 快速开始

### 安装
```bash
# 杂鱼♡～推荐使用本喵最喜欢的 uv 包管理器喵～
uv add ci-board

# 或者用你那慢吞吞的 pip
pip install ci-board
```
> **可选依赖**: 如果要处理图片，本喵建议你安装 `Pillow` 库喵～ `uv add pillow` 或 `pip install Pillow`

### 懒人API - 30秒上手
哼～看好了，杂鱼主人！这就是本喵设计的懒人API，让你这种懒蛋也能轻松上手喵～

```python
# 杂鱼♡～这是最简单的使用方式喵～
import time
from ci_board import create_monitor, ProcessInfo, BMPData
# 杂鱼♡～为了看清本喵的工作过程，可以打开日志喵～
from ci_board.utils import setup_ci_board_logging, LogLevel
setup_ci_board_logging(console_level=LogLevel.INFO)

def on_text_change(text: str, source: ProcessInfo):
    print(f"杂鱼♡～本喵抓到了新的文本喵！是从 [{source.process_name}] 来的！")
    print(f"  内容: {text[:80]}...")

def on_image_change(image: BMPData, source: ProcessInfo):
    print(f"杂鱼♡～抓到一张图片！尺寸 {image.width}x{image.height}，来自 [{source.process_name}] 喵！")
    # 杂鱼♡～想看图的话，记得先安装 Pillow 喵～
    try:
        import io
        from PIL import Image
        img = Image.open(io.BytesIO(image.data))
        img.show()
    except ImportError:
        print("  （杂鱼主人快去安装 Pillow 才能看图喵！）")
    except Exception as e:
        print(f"  （哎呀，图片出错了喵：{e}）")

def on_files_change(files: list[str], source: ProcessInfo):
    print(f"杂鱼♡～有文件被复制了喵！一共 {len(files)} 个，来自 [{source.process_name}]！")
    for f in files:
        print(f"  - {f}")

# 哼～创建监控器，就是这么简单喵～
monitor = create_monitor()

# 杂鱼♡～看好了，本喵的懒人API可以直接把函数变成处理器喵！
monitor.add_handler('text', on_text_change)
monitor.add_handler('image', on_image_change)
monitor.add_handler('files', on_files_change)

print("杂鱼♡～监控开始了喵！快去复制点东西给本喵看看！(按 Ctrl+C 结束)")
monitor.start()

try:
    monitor.wait()
except KeyboardInterrupt:
    print("\n哼～杂鱼主人不玩了，那本喵就结束了喵～")
finally:
    monitor.stop()

```

## 📋 API 文档

### `create_monitor()`
这是最简单的创建监控器的方法，它会返回一个配置好默认参数的 `ClipboardMonitor` 实例。

### `ClipboardMonitor` 核心类
```python
class ClipboardMonitor:
    def __init__(self, 
                 async_processing: bool = True,     # 哼～默认当然是异步处理喵
                 max_workers: int = 4,              # 杂鱼♡～本喵给你准备了4个工人处理回调
                 handler_timeout: float = 30.0,     # 要是哪个处理器太慢，30秒本喵就不要它了
                 event_driven: bool = True):        # 事件驱动！最高效的模式喵！
    
    # --- 基本控制 ---
    def start() -> bool:          # 启动监控，哼～
    def stop() -> None:           # 停止监控，真是的，说停就停
    def wait() -> None:           # 阻塞线程，直到监控停止，杂鱼主人就喜欢干等着
    def is_running() -> bool:     # 告诉杂鱼主人本喵是不是在工作
    
    # --- 处理器管理 (懒人API) ---
    def add_handler(content_type: str, callback: Callable) -> BaseClipboardHandler:
        # 添加处理器，传入回调函数就行，本喵会帮你搞定剩下的
    
    def remove_handler(content_type: str, handler: BaseClipboardHandler) -> None:
        # 哼，不想要了就丢掉
    
    def clear_handlers(content_type: str | None = None) -> None:
        # 全部丢掉！眼不见心不烦！
    
    # --- 状态与配置 ---
    def get_status() -> dict:     # 看看本喵工作的怎么样了
    def enable_source_tracking() -> None:   # 启用源追踪（默认开启）
    def disable_source_tracking() -> None:  # 禁用源追踪
```

### 内容类型与回调
| 类型 | 描述 | 回调参数 `(content, source_info)` |
| :--- | :--- | :--- |
| `'text'` | 文本内容 | `(text: str, source: ProcessInfo)` |
| `'image'` | BMP 图片数据 | `(bmp_data: BMPData, source: ProcessInfo)` |
| `'files'` | 文件路径列表 | `(file_list: list[str], source: ProcessInfo)` |
| `'update'`| 任意内容更新| `(data: tuple, source: ProcessInfo)` |

`'update'` 类型比较特殊，它的 `content` 是一个元组 `(content_type, actual_content)`，任何类型的剪贴板更新都会触发它。哼～给高级用户准备的，杂鱼主人可能用不上。

### 核心数据结构
哼～这些是回调函数会收到的数据结构，给本喵看仔细了！

```python
# 来源进程信息，本喵查到的可详细了喵！
class ProcessInfo:
    process_name: str       # 进程名, 像 'vscode.exe'
    process_path: str       # 完整路径
    process_id: int         # 进程ID
    window_title: str       # 窗口标题
    detection_method: str   # 本喵是用什么方法抓到它的
    confidence_level: str   # 本喵对结果的自信程度，哼～
    is_system_process: bool # 是不是系统进程
    is_screenshot_tool: bool # 是不是截图工具，本喵可聪明了
    timestamp: float        # 发现它的时间戳

# BMP图片数据，才...才不是为了杂鱼优化的代码♡～
class BMPData:
    success: bool           # 转换是否成功
    data: bytes | None      # BMP 格式的图片数据
    width: int              # 图片宽度
    height: int             # 图片高度
```

## 🛡️ 高级用法

### 对处理器进行精细配置
`add_handler` 会返回一个处理器实例，杂鱼主人可以对它进行进一步配置，比如添加过滤器。

```python
from ci_board.handlers import TextHandler

monitor = create_monitor()

# 哼～虽然是懒人API，但本喵也允许你进行高级操作
text_handler = monitor.add_handler('text', my_text_callback)

# 就...就允许你对它加个过滤器好了
text_handler.set_length_filter(min_length=10) # 太短的文本本喵才不关心
text_handler.set_source_filter(
    allowed_processes=['notepad.exe', 'Code.exe'] # 只关心记事本和VSCode
)

# 本喵连这种边缘情况都想到了，杂鱼主人应该感恩喵～～
def custom_filter(text: str, source: ProcessInfo) -> bool:
    return "secret" not in text.lower()

text_handler.add_filter(custom_filter) # 才...才不是为了帮你过滤秘密信息♡～
```

### 查看本喵的工作状态
想知道本喵在干什么吗？`get_status()` 可以满足你这个变态主人的偷窥欲♡～
```python
# 启动后...
status = monitor.get_status()

import json
print(json.dumps(status, indent=2))
```
你会看到本喵的各种工作状态，比如异步任务队列的大小、去重缓存的数量、焦点追踪的状态等等，哼～本喵可是一直在努力工作！

## 📁 项目结构
```
ci_board/
├── core/                   # 核心模块，本喵的心脏！
│   ├── monitor.py          # 主监控器
│   └── source_tracker_.py  # 源追踪器，本喵的眼睛！
├── handlers/               # 处理器，帮杂鱼主人干活的
│   ├── text_handler.py
│   ├── image_handler.py
│   └── file_handler.py
├── interfaces/             # 接口定义，这是规矩
├── types/                  # 数据类型，本喵的语言
└── utils/                  # 工具模块，本喵的工具箱
    ├── clipboard_utils.py  # 剪贴板工具（统一接口）
    ├── win32_api.py        # Windows API 封装
    └── logger.py           # 日志工具
```

## 📝 开发信息

- **作者**: StanleyUKN
- **GitHub**: [ci_board](https://github.com/Xuehua-Meaw/ci_board)
- **许可证**: MIT License

## 💝 致谢

哼～感谢所有使用本喵作品的杂鱼主人们喵～
如果觉得好用...就...就给本喵一个 Star 吧！才...才不是因为想要才跟你要的！只是看你可怜而已！♡～
