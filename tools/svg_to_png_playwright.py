#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SVG 转 PNG 脚本 (使用 Playwright)
使用 Playwright 浏览器引擎渲染 SVG，完美支持 emoji 和所有样式

安装依赖:
    pip install playwright
    playwright install chromium

使用方法:
    # 转换单个文件
    python svg_to_png_playwright.py input.svg

    # 转换单个文件并指定输出路径
    python svg_to_png_playwright.py input.svg output.png

    # 批量转换目录
    python svg_to_png_playwright.py ./svg_output

    # 批量转换并指定输出目录
    python svg_to_png_playwright.py ./svg_output ./png_output

    # 指定缩放倍数（默认1倍）
    python svg_to_png_playwright.py ./svg_output ./png_output --scale 2

参数说明:
    input_path      输入的 SVG 文件或目录
    output_path     输出的 PNG 文件或目录（可选）
    --scale         缩放倍数，默认 1（生成默认尺寸的图片）
    --recursive     递归处理子目录（默认开启）
    --no-recursive  不递归处理子目录
"""

import os
import sys
import argparse
import time
import base64
from pathlib import Path
from typing import List, Tuple

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("错误: 未找到 playwright 库")
    print("请运行:")
    print("  pip install playwright")
    print("  playwright install chromium")
    sys.exit(1)


class SvgToPngConverter:
    """SVG 转 PNG 转换器（使用 Playwright）"""

    def __init__(self, scale: float = 1.0, recursive: bool = True):
        """
        初始化转换器

        Args:
            scale: 缩放倍数，默认 1.0
            recursive: 是否递归处理子目录
        """
        self.scale = scale
        self.recursive = recursive
        self.success_count = 0
        self.fail_count = 0
        self.failed_files = []
        self.playwright = None
        self.browser = None
        self.page = None

    def __enter__(self):
        """启动浏览器"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """关闭浏览器"""
        if self.page:
            self.page.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def get_svg_files(self, directory: Path) -> List[Path]:
        """
        获取目录中的所有 SVG 文件

        Args:
            directory: 目录路径

        Returns:
            SVG 文件路径列表
        """
        svg_files = []

        if self.recursive:
            # 递归查找
            svg_files = list(directory.rglob("*.svg"))
        else:
            # 只查找当前目录
            svg_files = list(directory.glob("*.svg"))

        return sorted(svg_files)

    def convert_file(self, svg_path: Path, png_path: Path) -> Tuple[bool, str]:
        """
        转换单个 SVG 文件为 PNG

        Args:
            svg_path: SVG 文件路径
            png_path: PNG 输出路径

        Returns:
            (是否成功, 错误信息)
        """
        try:
            # 确保输出目录存在
            png_path.parent.mkdir(parents=True, exist_ok=True)

            # 读取 SVG 内容
            with open(svg_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()

            # 从 SVG 中提取 viewBox 尺寸
            import re
            viewbox_match = re.search(r'viewBox=["\']([^"\']+)["\']', svg_content)
            if viewbox_match:
                viewbox_values = viewbox_match.group(1).split()
                if len(viewbox_values) == 4:
                    svg_width = float(viewbox_values[2])
                    svg_height = float(viewbox_values[3])
                else:
                    # 如果无法解析 viewBox，使用默认值
                    svg_width = 750
                    svg_height = 1000
            else:
                # 如果没有 viewBox，使用默认值
                svg_width = 750
                svg_height = 1000

            # 创建 HTML 页面包含 SVG（设置明确的 width 和 height）
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                    }}
                    svg {{
                        display: block;
                        width: {svg_width}px;
                        height: {svg_height}px;
                    }}
                </style>
            </head>
            <body>
                {svg_content}
            </body>
            </html>
            """

            # 设置页面内容
            self.page.set_content(html_content)

            # 等待 SVG 加载
            self.page.wait_for_selector('svg', timeout=5000)

            # 使用从 viewBox 读取的尺寸
            width = svg_width
            height = svg_height

            # 设置视口大小（应用缩放）
            viewport_width = int(width * self.scale)
            viewport_height = int(height * self.scale)

            self.page.set_viewport_size({
                'width': viewport_width,
                'height': viewport_height
            })

            # 获取 SVG 元素
            svg_element = self.page.query_selector('svg')

            # 截图（使用 css 模式，避免设备像素比放大）
            svg_element.screenshot(
                path=str(png_path),
                type='png',
                scale='css'
            )

            self.success_count += 1
            return True, ""

        except Exception as e:
            self.fail_count += 1
            error_msg = str(e)
            self.failed_files.append((svg_path.name, error_msg))
            return False, error_msg

    def convert_single(self, svg_path: Path, png_path: Path = None) -> bool:
        """
        转换单个文件

        Args:
            svg_path: SVG 文件路径
            png_path: PNG 输出路径（可选）

        Returns:
            是否成功
        """
        if not svg_path.exists():
            print(f"❌ 错误: 文件不存在 - {svg_path}")
            return False

        if not svg_path.suffix.lower() == '.svg':
            print(f"❌ 错误: 不是 SVG 文件 - {svg_path}")
            return False

        # 如果没有指定输出路径，使用相同目录和文件名
        if png_path is None:
            png_path = svg_path.with_suffix('.png')

        print(f"📄 转换: {svg_path.name}")
        success, error = self.convert_file(svg_path, png_path)

        if success:
            print(f"✅ 成功: {png_path}")
            return True
        else:
            print(f"❌ 失败: {error}")
            return False

    def convert_batch(self, input_dir: Path, output_dir: Path = None) -> None:
        """
        批量转换目录中的 SVG 文件

        Args:
            input_dir: 输入目录
            output_dir: 输出目录（可选）
        """
        if not input_dir.exists():
            print(f"❌ 错误: 目录不存在 - {input_dir}")
            return

        if not input_dir.is_dir():
            print(f"❌ 错误: 不是目录 - {input_dir}")
            return

        # 如果没有指定输出目录，使用 png_output
        if output_dir is None:
            output_dir = input_dir.parent / "png_output"

        # 创建输出目录
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"📂 扫描目录: {input_dir}")
        svg_files = self.get_svg_files(input_dir)

        if not svg_files:
            print("未找到 SVG 文件")
            return

        print(f"📊 找到 {len(svg_files)} 个 SVG 文件")
        print(f"📁 输出目录: {output_dir}")
        print(f"🔧 缩放倍数: {self.scale}x")
        print("")

        # 转换每个文件
        for i, svg_path in enumerate(svg_files, 1):
            # 计算相对路径，保持目录结构
            rel_path = svg_path.relative_to(input_dir)
            png_path = output_dir / rel_path.with_suffix('.png')

            print(f"进度: {i}/{len(svg_files)} - {svg_path.name}")
            self.convert_file(svg_path, png_path)

    def print_summary(self) -> None:
        """打印转换结果摘要"""
        print("")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"✅ 成功: {self.success_count}")
        print(f"❌ 失败: {self.fail_count}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        if self.failed_files:
            print("")
            print("失败的文件:")
            for filename, error in self.failed_files:
                print(f"  - {filename}: {error}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="SVG 转 PNG 转换工具 (Playwright) - 完美支持 emoji",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s slide.svg                    # 转换单个文件
  %(prog)s slide.svg output.png         # 指定输出文件名
  %(prog)s ./svg_output                 # 批量转换
  %(prog)s ./svg_output ./png_output    # 指定输出目录
  %(prog)s ./svg_output --scale 2       # 2倍缩放
        """
    )

    parser.add_argument(
        'input_path',
        type=str,
        help='输入的 SVG 文件或目录'
    )

    parser.add_argument(
        'output_path',
        type=str,
        nargs='?',
        default=None,
        help='输出的 PNG 文件或目录（可选）'
    )

    parser.add_argument(
        '--scale',
        type=float,
        default=1.0,
        help='缩放倍数（默认: 1.0）'
    )

    parser.add_argument(
        '--no-recursive',
        action='store_true',
        help='不递归处理子目录'
    )

    args = parser.parse_args()

    # 转换路径
    input_path = Path(args.input_path)
    output_path = Path(args.output_path) if args.output_path else None

    print("🎨 SVG 转 PNG 转换工具 (Playwright)")
    print("=" * 50)
    print("")

    start_time = time.time()

    # 使用 context manager 管理浏览器生命周期
    with SvgToPngConverter(
        scale=args.scale,
        recursive=not args.no_recursive
    ) as converter:
        # 判断是文件还是目录
        if input_path.is_file():
            # 单个文件转换
            converter.convert_single(input_path, output_path)
        elif input_path.is_dir():
            # 批量转换
            converter.convert_batch(input_path, output_path)
        else:
            print(f"❌ 错误: 路径不存在 - {input_path}")
            sys.exit(1)

        # 打印摘要
        if converter.success_count > 0 or converter.fail_count > 0:
            converter.print_summary()

    elapsed = time.time() - start_time
    print("")
    print(f"⏱️  耗时: {elapsed:.2f} 秒")


if __name__ == "__main__":
    main()
