#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化测试脚本
验证 Karpathy Guidelines 优化效果
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """测试导入"""
    print("🧪 测试导入...")
    try:
        from scripts.main import HertzMyself
        from scripts.greeting import greeting_generator
        from scripts.search_tools import search_tools
        from scripts.user_rating import user_rating_system
        print("   ✅ 导入测试通过")
        return True
    except Exception as e:
        print(f"   ❌ 导入测试失败: {e}")
        return False

def test_greeting():
    """测试开场白"""
    print("🧪 测试开场白...")
    try:
        from scripts.greeting import greeting_generator

        # 测试默认风格
        weather = {'city': '北京', 'temperature': 22, 'condition': '晴'}
        greeting = greeting_generator.generate(mood='positive', weather=weather, song_name='Test Song')
        assert 'hertz-myself' in greeting
        assert 'Test Song' in greeting
        assert '。' not in greeting  # 检查没有句号

        print("   ✅ 开场白测试通过")
        return True
    except Exception as e:
        print(f"   ❌ 开场白测试失败: {e}")
        return False

def test_rating():
    """测试评分系统"""
    print("🧪 测试评分系统...")
    try:
        from scripts.user_rating import user_rating_system

        # 测试解析评分
        result = user_rating_system.parse_rating_input("8 很好听")
        assert result is not None
        assert result['rating'] == 8

        # 测试无效输入
        result = user_rating_system.parse_rating_input("invalid")
        assert result is None

        print("   ✅ 评分系统测试通过")
        return True
    except Exception as e:
        print(f"   ❌ 评分系统测试失败: {e}")
        return False

def test_search_tools():
    """测试搜索工具"""
    print("🧪 测试搜索工具...")
    try:
        from scripts.search_tools import search_tools

        # 测试获取配置选项
        options = search_tools.get_setup_options()
        assert 'options' in options

        # 测试获取 API 选项
        api_options = search_tools.get_api_options()
        assert 'apis' in api_options

        print("   ✅ 搜索工具测试通过")
        return True
    except Exception as e:
        print(f"   ❌ 搜索工具测试失败: {e}")
        return False

def test_file_structure():
    """测试文件结构"""
    print("🧪 测试文件结构...")
    try:
        project_root = os.path.dirname(os.path.dirname(__file__))

        # 检查必要的文件
        required_files = [
            'SKILL.md',
            'README.md',
            'CLAUDE.md',
            '.gitignore',
        ]

        for file in required_files:
            file_path = os.path.join(project_root, file)
            assert os.path.exists(file_path), f"{file} 不存在"

        # 检查脚本文件
        script_files = [
            'scripts/main.py',
            'scripts/greeting.py',
            'scripts/search_tools.py',
            'scripts/user_rating.py',
            'scripts/analyze_mood.py',
            'scripts/weather_detector.py',
            'scripts/personality_detector.py',
            'scripts/scheduler.py',
            'scripts/read_history.py',
        ]

        for file in script_files:
            file_path = os.path.join(project_root, file)
            assert os.path.exists(file_path), f"{file} 不存在"

        print("   ✅ 文件结构测试通过")
        return True
    except Exception as e:
        print(f"   ❌ 文件结构测试失败: {e}")
        return False

def test_no_redundant_files():
    """测试没有冗余文件"""
    print("🧪 测试没有冗余文件...")
    try:
        project_root = os.path.dirname(os.path.dirname(__file__))

        # 检查不应该存在的文件
        redundant_files = [
            'CHANGELOG.md',
            'SECURITY.md',
            'VERSION.md',
            'FINAL.md',
        ]

        for file in redundant_files:
            file_path = os.path.join(project_root, file)
            assert not os.path.exists(file_path), f"{file} 存在（应该删除）"

        print("   ✅ 冗余文件测试通过")
        return True
    except Exception as e:
        print(f"   ❌ 冗余文件测试失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("🎵 hertz-myself - 优化测试")
    print("=" * 50)
    print()

    tests = [
        test_imports,
        test_greeting,
        test_rating,
        test_search_tools,
        test_file_structure,
        test_no_redundant_files,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"   ❌ 测试异常: {e}")
            failed += 1
        print()

    print("=" * 50)
    print(f"📊 测试结果: {passed}/{passed + failed} 通过")
    print("=" * 50)

    if failed == 0:
        print("✅ 所有优化测试通过！")
        return 0
    else:
        print(f"❌ {failed} 个测试失败")
        return 1

if __name__ == '__main__':
    sys.exit(run_all_tests())
