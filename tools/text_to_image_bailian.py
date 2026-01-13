#!/usr/bin/env python3
"""
文本转图片工具 - 使用阿里云百炼通义万象 V2 API

使用阿里云百炼的通义万象文生图 V2 功能，根据描述生成图片并保存到指定目录。
模型: wan2.6-t2i
"""

import os
import sys
import argparse
import json
import time
from pathlib import Path
from http import HTTPStatus

try:
    import dashscope
    from dashscope.aigc.image_generation import ImageGeneration
    from dashscope.api_entities.dashscope_response import Message
except ImportError:
    print("❌ 错误: 未安装 dashscope 库")
    print("请运行: pip install dashscope")
    sys.exit(1)


def generate_image(prompt: str, size: str = "1024*1024", output_path: str = None) -> bool:
    """
    生成图片并保存到指定路径
    
    Args:
        prompt: 图片生成描述
        size: 图片尺寸，格式为 "宽*高"，如 "1024*1024"
        output_path: 输出文件路径
    
    Returns:
        bool: 是否成功生成
    """
    # 获取 API Key
    api_key = os.getenv('BAILIAN_KEY')
    if not api_key:
        print("❌ 错误: 未找到环境变量 BAILIAN_KEY")
        print("请设置环境变量: export BAILIAN_KEY='your_api_key'")
        return False
    
    # 验证尺寸格式
    valid_sizes = ["1024*1024", "720*1280", "1280*720", "1280*1280", "1104*1472", "1472*1104", "960*1696", "1696*960"]
    if size not in valid_sizes:
        print(f"⚠️  警告: 尺寸 {size} 不在推荐列表中")
        print(f"   支持的尺寸: {', '.join(valid_sizes)}")
    
    print(f"🎨 开始生成图片...")
    print(f"   描述: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
    print(f"   尺寸: {size}")
    
    try:
        # 构建消息
        message = Message(
            role="user",
            content=[{'text': prompt}]
        )
        
        # 调用 API (wan2.6-t2i 使用同步调用)
        rsp = ImageGeneration.call(
            model="wan2.6-t2i",
            api_key=api_key,
            messages=[message],
            negative_prompt="",
            prompt_extend=True,
            watermark=False,
            n=1,
            size=size
        )
        
        if rsp.status_code != HTTPStatus.OK:
            print(f"❌ API 调用失败: {rsp.code} - {rsp.message}")
            return False
        
        # 获取图片 URL
        if not rsp.output or not rsp.output.choices:
            print("❌ 未返回图片结果")
            return False
        
        image_url = rsp.output.choices[0].message.content[0]['image']
        print(f"✅ 图片生成成功")
        print(f"   URL: {image_url}")
        
        # 下载图片
        if output_path:
            import urllib.request
            
            # 确保输出目录存在
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"📥 下载图片到: {output_path}")
            urllib.request.urlretrieve(image_url, output_path)
            
            # 验证文件
            if Path(output_path).exists():
                file_size = Path(output_path).stat().st_size
                print(f"✅ 图片已保存 ({file_size / 1024:.1f} KB)")
                return True
            else:
                print("❌ 文件保存失败")
                return False
        else:
            print("⚠️  未指定输出路径，仅生成图片 URL")
            return True
            
    except Exception as e:
        print(f"❌ 生成失败: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='使用阿里云百炼通义万象 V2 API 生成图片',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成 1280x1280 的图片
  python3 tools/text_to_image_bailian.py "现代科技感抽象背景，深蓝渐变" -o images/bg.png
  
  # 生成 16:9 横版图片
  python3 tools/text_to_image_bailian.py "团队协作场景" -s "1280*720" -o images/team.png
  
  # 生成 9:16 竖版图片
  python3 tools/text_to_image_bailian.py "产品展示" -s "720*1280" -o images/product.png

支持的尺寸:
  - 1280*1280 (1:1 方形，推荐)
  - 1024*1024 (1:1 方形)
  - 1280*720  (16:9 横版)
  - 1696*960  (16:9 横版，高分辨率)
  - 720*1280  (9:16 竖版)
  - 960*1696  (9:16 竖版，高分辨率)
  - 1104*1472 (3:4 竖版)
  - 1472*1104 (4:3 横版)

模型: wan2.6-t2i (通义万象 V2)
        """
    )
    
    parser.add_argument('prompt', help='图片生成描述')
    parser.add_argument('-s', '--size', default='1280*1280',
                        help='图片尺寸 (默认: 1280*1280)')
    parser.add_argument('-o', '--output', required=True,
                        help='输出文件路径 (必需)')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='静默模式')
    
    args = parser.parse_args()
    
    # 静默模式
    if args.quiet:
        sys.stdout = open(os.devnull, 'w')
    
    # 生成图片
    success = generate_image(args.prompt, args.size, args.output)
    
    # 恢复输出
    if args.quiet:
        sys.stdout = sys.__stdout__
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
