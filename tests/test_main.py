#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化测试脚本
"""

import sys
import os
import json
import tempfile
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """测试导入"""
    print("🧪 测试导入...")
    try:
        from scripts.main import HertzMyself
        from scripts.search_tools import search_tools
        from scripts.user_rating import user_rating_system
        from scripts.weather_detector import weather_detector
        from scripts.analyze_mood import MoodAnalyzer
        from scripts.scheduler import create_scheduler
        print("   ✅ 导入测试通过")
        return True
    except Exception as e:
        print(f"   ❌ 导入测试失败: {e}")
        return False

def test_search_tools():
    """测试搜索工具"""
    print("🧪 测试搜索工具...")
    try:
        from scripts.search_tools import search_tools

        # 测试获取配置选项
        options = search_tools.get_setup_options()
        assert 'options' in options
        assert len(options['options']) == 3

        # 测试获取 API 选项
        api_options = search_tools.get_api_options()
        assert 'apis' in api_options
        assert len(api_options['apis']) == 3

        print("   ✅ 搜索工具测试通过")
        return True
    except Exception as e:
        print(f"   ❌ 搜索工具测试失败: {e}")
        return False

def test_user_rating():
    """测试用户评分系统"""
    print("🧪 测试用户评分系统...")
    try:
        from scripts.user_rating import user_rating_system

        # 测试解析评分输入
        result = user_rating_system.parse_rating_input("8 very good")
        assert result is not None
        assert result['rating'] == 8
        assert 'feedback' in result

        # 测试无效输入
        result = user_rating_system.parse_rating_input("invalid")
        assert result is None

        print("   ✅ 用户评分系统测试通过")
        return True
    except Exception as e:
        print(f"   ❌ 用户评分系统测试失败: {e}")
        return False

def test_weather_detector():
    """测试天气检测器"""
    print("🧪 测试天气检测器...")
    try:
        from scripts.weather_detector import weather_detector

        # 测试获取天气心情
        weather = {'condition': 'sunny', 'temperature': 25}
        mood = weather_detector.get_weather_mood(weather)
        assert mood == 'positive', f"期望 'positive'，实际 '{mood}'"

        # 测试获取天气主题
        theme = weather_detector.get_weather_theme(weather)
        assert theme in ['entertainment', 'life'], f"期望 'entertainment' 或 'life'，实际 '{theme}'"

        # 测试格式化天气信息
        info = weather_detector.format_weather_info(weather)
        assert 'sunny' in info, f"期望包含 'sunny'，实际 '{info}'"
        assert '25' in info, f"期望包含 '25'，实际 '{info}'"

        print("   ✅ 天气检测器测试通过")
        return True
    except Exception as e:
        print(f"   ❌ 天气检测器测试失败: {e}")
        return False

def test_analyze_mood():
    """测试情绪分析"""
    print("🧪 测试情绪分析...")
    try:
        from scripts.analyze_mood import MoodAnalyzer

        analyzer = MoodAnalyzer()

        # 测试分析对话
        conversations = [
            {'content': '今天心情不错'},
            {'content': '工作很顺利'}
        ]

        result = analyzer.analyze(conversations)
        assert 'mood' in result
        assert 'theme' in result
        assert 'keywords' in result

        # 测试带天气的分析
        weather = {'condition': '晴', 'temperature': 25}
        result_with_weather = analyzer.analyze(conversations, weather)
        assert 'weather' in result_with_weather

        print("   ✅ 情绪分析测试通过")
        return True
    except Exception as e:
        print(f"   ❌ 情绪分析测试失败: {e}")
        return False

def test_scheduler():
    """测试调度器"""
    print("🧪 测试调度器...")
    try:
        from scripts.scheduler import create_scheduler

        # 创建调度器
        def dummy_callback():
            pass

        scheduler = create_scheduler(dummy_callback)

        # 测试设置触发时间
        scheduler.set_trigger_times(["18:00", "20:00"])
        assert scheduler.trigger_times == ["18:00", "20:00"]

        # 测试获取触发时间
        times = scheduler.get_trigger_times()
        assert times == ["18:00", "20:00"]

        print("   ✅ 调度器测试通过")
        return True
    except Exception as e:
        print(f"   ❌ 调度器测试失败: {e}")
        return False

def test_config_files():
    """测试配置文件"""
    print("🧪 测试配置文件...")
    try:
        # 检查配置文件是否存在
        config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

        # 检查搜索配置
        search_config = os.path.join(config_dir, 'search_config.json')
        assert os.path.exists(search_config), "search_config.json 不存在"

        # 检查调度器配置
        scheduler_config = os.path.join(config_dir, 'scheduler_config.json')
        assert os.path.exists(scheduler_config), "scheduler_config.json 不存在"

        # 检查数据目录
        assert os.path.exists(data_dir), "data 目录不存在"

        # 检查用户评分文件
        ratings_file = os.path.join(data_dir, 'user_ratings.json')
        assert os.path.exists(ratings_file), "user_ratings.json 不存在"

        # 检查用户偏好文件
        preferences_file = os.path.join(data_dir, 'user_preferences.json')
        assert os.path.exists(preferences_file), "user_preferences.json 不存在"

        print("   ✅ 配置文件测试通过")
        return True
    except Exception as e:
        print(f"   ❌ 配置文件测试失败: {e}")
        return False

def test_documentation():
    """测试文档"""
    print("🧪 测试文档...")
    try:
        project_root = os.path.dirname(os.path.dirname(__file__))

        # 检查必要的文档文件
        required_docs = [
            'SKILL.md',
            'README.md',
            'CHANGELOG.md',
            'VERSION.md',
            '.gitignore'
        ]

        for doc in required_docs:
            doc_path = os.path.join(project_root, doc)
            assert os.path.exists(doc_path), f"{doc} 不存在"

        print("   ✅ 文档测试通过")
        return True
    except Exception as e:
        print(f"   ❌ 文档测试失败: {e}")
        return False

def test_greeting():
    """测试开场白"""
    print("🧪 测试开场白...")
    try:
        from scripts.greeting import greeting_generator

        # 测试默认风格
        greeting = greeting_generator.generate(mood='positive', song_name='Test Song')
        assert 'hertz-myself' in greeting
        assert 'Test Song' in greeting
        assert '。' not in greeting  # 检查没有句号

        # 测试带天气
        weather = {'city': '北京', 'temperature': 22, 'condition': '晴'}
        greeting = greeting_generator.generate(mood='positive', weather=weather, song_name='Test Song')
        assert '北京' in greeting
        assert '22°C' in greeting

        print("   ✅ 开场白测试通过")
        return True
    except Exception as e:
        print(f"   ❌ 开场白测试失败: {e}")
        return False

def test_personality():
    """测试人格集成"""
    print("🧪 测试人格集成...")
    try:
        from scripts.personality_detector import personality_detector

        # 测试加载人格文件
        result = personality_detector.load_personality_from_file('/path/to/soul.md')
        assert result is None  # 文件不存在

        # 测试应用人格风格
        text = "这是一首好听的歌"
        result = personality_detector.apply_personality(text)
        assert result == text  # 没有人格文件，返回原文

        print("   ✅ 人格集成测试通过")
        return True
    except Exception as e:
        print(f"   ❌ 人格集成测试失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("🎵 听见自己的频率 - 自动化测试")
    print("=" * 50)
    print()

    tests = [
        test_imports,
        test_search_tools,
        test_user_rating,
        test_weather_detector,
        test_analyze_mood,
        test_scheduler,
        test_config_files,
        test_documentation,
        test_greeting,
        test_personality
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
        print("✅ 所有测试通过！")
        return 0
    else:
        print(f"❌ {failed} 个测试失败")
        return 1

if __name__ == '__main__':
    sys.exit(run_all_tests())
