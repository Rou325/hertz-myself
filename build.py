#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本
"""

import os
import sys
import shutil
import subprocess
from datetime import datetime

def clean_build():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist', '*.egg-info']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ 清理目录: {dir_name}")

def build_package():
    """构建包"""
    print("🔨 开始构建包...")

    # 使用 setuptools 构建
    try:
        subprocess.run([sys.executable, "setup.py", "sdist", "bdist_wheel"], check=True)
        print("✅ 包构建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 包构建失败: {e}")
        return False

def create_zip():
    """创建 ZIP 包"""
    print("📦 创建 ZIP 包...")

    # 创建输出目录
    output_dir = "release"
    os.makedirs(output_dir, exist_ok=True)

    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"hertz-myself_v2.2.0_{timestamp}.zip"
    zip_path = os.path.join(output_dir, zip_name)

    # 需要包含的文件和目录
    include_items = [
        'SKILL.md',
        'README.md',
        'CHANGELOG.md',
        'VERSION.md',
        'CLAUDE.md',
        'OPTIMIZATION_SUMMARY.md',
        '.gitignore',
        'setup.py',
        'MANIFEST.in',
        'scripts/',
        'tests/',
        'config/',
        'evals/',
    ]

    # 创建 ZIP 文件
    import zipfile
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in include_items:
            if os.path.isfile(item):
                zipf.write(item)
                print(f"  ✅ 添加文件: {item}")
            elif os.path.isdir(item):
                for root, dirs, files in os.walk(item):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path)
                        print(f"  ✅ 添加文件: {file_path}")

    print(f"✅ ZIP 包创建成功: {zip_path}")
    return zip_path

def main():
    """主函数"""
    print("=" * 50)
    print("🎵 hertz-myself - 打包工具")
    print("=" * 50)
    print()

    # 清理构建目录
    clean_build()
    print()

    # 构建包
    if build_package():
        print()
        # 创建 ZIP 包
        zip_path = create_zip()
        print()
        print("=" * 50)
        print("✅ 打包完成！")
        print(f"📦 ZIP 包位置: {zip_path}")
        print("=" * 50)
    else:
        print("❌ 打包失败")
        sys.exit(1)

if __name__ == '__main__':
    main()
