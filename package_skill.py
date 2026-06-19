#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能打包脚本
将项目打包成 .skill 文件
"""

import os
import sys
import json
import zipfile
from datetime import datetime
from pathlib import Path

# 排除的目录和文件
EXCLUDE_DIRS = {"__pycache__", "node_modules", ".git", "dist", "release", "build", "*.egg-info"}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db", "*.pyc"}
EXCLUDE_PATTERNS = {"*.pyc", "*.pyo", "*.pyd", ".git*", ".svn*"}

def should_exclude(path: str) -> bool:
    """检查是否应该排除该路径"""
    path_obj = Path(path)

    # 检查排除的目录
    for part in path_obj.parts:
        if part in EXCLUDE_DIRS:
            return True

    # 检查排除的文件
    if path_obj.name in EXCLUDE_FILES:
        return True

    # 检查排除的模式
    for pattern in EXCLUDE_PATTERNS:
        if path_obj.match(pattern):
            return True

    return False

def get_skill_info(skill_dir: str) -> dict:
    """获取技能信息"""
    skill_md = os.path.join(skill_dir, "SKILL.md")

    if not os.path.exists(skill_md):
        return None

    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()

    # 解析 YAML frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            # 简单解析
            info = {}
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    info[key.strip()] = value.strip()
            return info

    return None

def package_skill(skill_dir: str, output_dir: str = None) -> str:
    """
    打包技能

    Args:
        skill_dir: 技能目录路径
        output_dir: 输出目录路径

    Returns:
        生成的 .skill 文件路径
    """
    skill_dir = os.path.abspath(skill_dir)

    # 检查技能目录
    if not os.path.exists(skill_dir):
        raise FileNotFoundError(f"技能目录不存在: {skill_dir}")

    # 获取技能信息
    skill_info = get_skill_info(skill_dir)
    if not skill_info:
        raise ValueError("无法读取 SKILL.md 文件")

    skill_name = skill_info.get('name', os.path.basename(skill_dir))

    # 设置输出目录
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(skill_dir), 'release')

    os.makedirs(output_dir, exist_ok=True)

    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    skill_file = os.path.join(output_dir, f"{skill_name}_{timestamp}.skill")

    # 创建 ZIP 文件
    print(f"📦 打包技能: {skill_name}")
    print(f"📁 技能目录: {skill_dir}")
    print(f"📄 输出文件: {skill_file}")
    print()

    with zipfile.ZipFile(skill_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历技能目录
        for root, dirs, files in os.walk(skill_dir):
            # 过滤排除的目录
            dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]

            for file in files:
                file_path = os.path.join(root, file)

                # 检查是否应该排除
                if should_exclude(file_path):
                    continue

                # 计算相对路径
                rel_path = os.path.relpath(file_path, skill_dir)

                # 添加到 ZIP
                zipf.write(file_path, rel_path)
                print(f"  ✅ 添加: {rel_path}")

    print()
    print(f"✅ 打包完成: {skill_file}")

    # 显示文件大小
    file_size = os.path.getsize(skill_file)
    if file_size > 1024 * 1024:
        size_str = f"{file_size / 1024 / 1024:.2f} MB"
    elif file_size > 1024:
        size_str = f"{file_size / 1024:.2f} KB"
    else:
        size_str = f"{file_size} B"

    print(f"📦 文件大小: {size_str}")

    return skill_file

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python package_skill.py <技能目录> [输出目录]")
        print("示例: python package_skill.py . ./release")
        sys.exit(1)

    skill_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        skill_file = package_skill(skill_dir, output_dir)
        print()
        print("🎉 技能打包成功！")
        print(f"📦 文件位置: {skill_file}")
    except Exception as e:
        print(f"❌ 打包失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
