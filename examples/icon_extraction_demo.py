# 杂鱼♡～本喵的图标提取功能演示喵～
"""
图标提取功能演示
=============

演示如何从Windows可执行文件中提取图标，完美处理透明度♡～
"""

import os
import sys

# 杂鱼♡～设置路径，让杂鱼主人能正确导入喵～
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ci_board import (
    extract_icon,
    extract_icon_as_bytes,
    save_icon_with_transparency_preview
)


def demo_basic_extraction():
    """杂鱼♡～基础图标提取演示喵～"""
    print("=" * 60)
    print("杂鱼♡～基础图标提取演示开始了喵～")
    print("=" * 60)
    
    # 杂鱼♡～测试几个常见的Windows程序喵～
    test_programs = [
        r"C:\Windows\System32\notepad.exe",
        r"C:\Windows\System32\calc.exe",
        r"C:\Windows\System32\cmd.exe",
        r"C:\Windows\explorer.exe",
    ]
    
    output_dir = "icon_output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for program in test_programs:
        if os.path.exists(program):
            try:
                print(f"\n杂鱼♡～正在提取图标：{program}")
                
                # 杂鱼♡～提取大图标喵～
                icon_image = extract_icon(program, large_icon=True)
                
                # 杂鱼♡～生成输出文件名喵～
                base_name = os.path.splitext(os.path.basename(program))[0]
                output_path = os.path.join(output_dir, f"{base_name}_icon.png")
                
                # 杂鱼♡～保存图标并生成预览喵～
                saved_path, preview_path = save_icon_with_transparency_preview(
                    icon_image, 
                    output_path
                )
                
                print(f"  ✓ 图标已保存：{saved_path}")
                print(f"  ✓ 预览图已保存：{preview_path}")
                print(f"  图标尺寸：{icon_image.size}")
                
            except Exception as e:
                print(f"  ✗ 提取失败：{e}")
        else:
            print(f"\n杂鱼♡～文件不存在喵：{program}")


def demo_bytes_extraction():
    """杂鱼♡～字节数据提取演示喵～"""
    print("\n" + "=" * 60)
    print("杂鱼♡～字节数据提取演示喵～")
    print("=" * 60)
    
    test_file = r"C:\Windows\System32\notepad.exe"
    
    if os.path.exists(test_file):
        try:
            # 杂鱼♡～直接获取PNG格式的字节数据喵～
            icon_bytes = extract_icon_as_bytes(test_file, large_icon=True, format="PNG")
            
            print(f"杂鱼♡～成功提取图标字节数据喵～")
            print(f"  文件：{test_file}")
            print(f"  数据大小：{len(icon_bytes)} 字节")
            print(f"  格式：PNG（支持透明度）")
            
            # 杂鱼♡～也可以保存为其他格式喵～
            ico_bytes = extract_icon_as_bytes(test_file, large_icon=False, format="ICO")
            print(f"  ICO格式大小：{len(ico_bytes)} 字节")
            
        except Exception as e:
            print(f"杂鱼♡～提取失败了喵：{e}")


def demo_custom_file():
    """杂鱼♡～让杂鱼主人选择文件提取图标喵～"""
    print("\n" + "=" * 60)
    print("杂鱼♡～自定义文件图标提取喵～")
    print("=" * 60)
    
    print("杂鱼♡～请输入要提取图标的文件路径（支持exe、dll等）：")
    file_path = input("> ").strip('"')  # 杂鱼♡～去除可能的引号喵～
    
    if os.path.exists(file_path):
        try:
            # 杂鱼♡～提取大小两种图标喵～
            print("\n杂鱼♡～正在提取图标喵～")
            
            # 大图标
            large_icon = extract_icon(file_path, large_icon=True)
            large_output = f"custom_large_icon.png"
            large_icon.save(large_output)
            print(f"  ✓ 大图标已保存：{large_output} ({large_icon.size})")
            
            # 小图标
            small_icon = extract_icon(file_path, large_icon=False)
            small_output = f"custom_small_icon.png"
            small_icon.save(small_output)
            print(f"  ✓ 小图标已保存：{small_output} ({small_icon.size})")
            
        except Exception as e:
            print(f"杂鱼♡～提取失败了喵：{e}")
    else:
        print("杂鱼♡～文件不存在喵！杂鱼主人检查一下路径吧～")


if __name__ == "__main__":
    print("杂鱼♡～欢迎使用本喵的图标提取功能喵！～")
    print("本喵可以从Windows程序中提取图标，完美处理透明度哦～～")
    
    # 杂鱼♡～运行基础演示喵～
    demo_basic_extraction()
    
    # 杂鱼♡～运行字节提取演示喵～
    demo_bytes_extraction()
    
    # 杂鱼♡～询问是否要自定义提取喵～
    print("\n杂鱼♡～想要提取其他文件的图标吗？(y/n)")
    if input("> ").lower() == 'y':
        demo_custom_file()
    
    print("\n" + "=" * 60)
    print("杂鱼♡～演示结束了喵～")
    print("杂鱼主人可以在代码中这样使用：")
    print("  from ci_board import extract_icon")
    print("  icon = extract_icon('path/to/file.exe')")
    print("  icon.save('output.png')")
    print("真是个杂鱼♡～需要本喵手把手教呢～～")
    print("=" * 60) 