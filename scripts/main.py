#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
听见自己的频率 - 音乐推荐后端命令
AI（通过 SKILL.md）负责编排，脚本只做代码该做的事
"""

import sys
import os
import time
import argparse
import json
from datetime import datetime

# 设置标准输出编码为 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from scripts.search_tools import search_tools
from scripts.user_rating import user_rating_system
from scripts.scheduler import create_scheduler
from scripts.weather_detector import weather_detector
from scripts.personality_detector import personality_detector
from scripts.read_history import read_history


def cmd_search(query: str, count: int = 5):
    """执行搜索，返回 JSON 结果"""
    best_method = search_tools.get_best_method()
    print(json.dumps({
        'query': query,
        'method': best_method,
        'instructions': f'请使用 {best_method.upper()} 搜索：{query}',
        'count': count,
        'filters': ['exclude:抖音热歌', 'exclude:网络神曲', 'exclude:口水歌']
    }, ensure_ascii=False))


def cmd_rate(song_name: str, score: int, feedback: str = '', artist: str = ''):
    """记录评分"""
    song_info = {'name': song_name, 'artist': artist or '未知'}
    result = user_rating_system.parse_rating_input(f'{score} {feedback}')
    if result is None:
        print(json.dumps({'success': False, 'error': '无效评分'}))
        return
    success = user_rating_system.add_rating(
        song_info, result['rating'], result.get('feedback', ''),
        mood=result.get('mood'), scene=result.get('scene')
    )
    stats = user_rating_system.get_rating_statistics()
    print(json.dumps({
        'success': success,
        'score': result['rating'],
        'feedback': result.get('feedback', ''),
        'total_ratings': stats.get('total_ratings', 0),
        'average_rating': round(stats.get('average_rating', 0), 1)
    }, ensure_ascii=False))


def cmd_stats(format: str = 'text'):
    """查看评分统计"""
    stats_text = user_rating_system.format_statistics()
    print(stats_text)


def cmd_history():
    """读取对话历史，返回 JSON"""
    history = read_history()
    print(json.dumps(history, ensure_ascii=False, indent=2))


def cmd_config_status():
    """查看配置状态"""
    available = search_tools.get_available_methods()
    best = search_tools.get_best_method()
    has_weather = weather_detector.has_weather_skill()
    has_personality = personality_detector.has_personality()
    first_run = search_tools.is_first_run()
    print(json.dumps({
        'first_run': first_run,
        'available_methods': available,
        'best_method': best,
        'has_weather_skill': has_weather,
        'has_personality': has_personality
    }, ensure_ascii=False))


def cmd_check_first_run():
    """检查是否首次运行"""
    result = search_tools.is_first_run()
    print(json.dumps({'first_run': result}))


def cmd_setup():
    """进入配置流程"""
    print(search_tools.get_setup_prompt())


def cmd_scheduler():
    """启动定时调度器"""
    scheduler = create_scheduler(lambda: print("触发推荐"), auto_start=True)
    schedule = scheduler.get_trigger_times()
    if not schedule:
        print("⚠️ 未设置触发时间")
        return
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()
        print("\n调度器已停止")


def cmd_set_trigger_time(time_str: str = None, random_mode: bool = False,
                         random_count: int = 1, window_start: str = '09:00',
                         window_end: str = '21:00'):
    """设置触发时间"""
    scheduler = create_scheduler(lambda: None)
    if random_mode:
        scheduler.set_random_trigger(
            count=random_count,
            window_start=window_start,
            window_end=window_end
        )
        print(json.dumps({
            'success': True,
            'mode': 'random',
            'count': random_count,
            'window_start': window_start,
            'window_end': window_end
        }))
        return
    if time_str:
        try:
            times = [t.strip() for t in time_str.split(',')]
            for t in times:
                datetime.strptime(t, '%H:%M')
            scheduler.set_trigger_times(times)
            print(json.dumps({'success': True, 'mode': 'fixed', 'times': times}))
        except ValueError:
            print(json.dumps({'success': False, 'error': '时间格式错误，请使用 HH:MM'}))
    else:
        print(json.dumps({'success': False, 'error': '请提供时间或使用 --random'}))


def cmd_personality(file_path: str = None):
    """处理人格文件"""
    if file_path and os.path.exists(file_path):
        p = personality_detector.load_personality_from_file(file_path)
        if p:
            print(json.dumps({
                'loaded': True,
                'style': p.get('style', 'unknown'),
                'file': file_path
            }, ensure_ascii=False))
            return
    print(json.dumps({'loaded': False, 'style': 'default'}))


def main():
    parser = argparse.ArgumentParser(description='听见自己的频率 - 后端命令')
    parser.add_argument('--search', help='搜索歌曲，参数为搜索词')
    parser.add_argument('--rate', nargs=2, metavar=('歌曲名', '评分'), help='记录评分')
    parser.add_argument('--feedback', help='评分反馈（与 --rate 配合使用）')
    parser.add_argument('--artist', help='歌手名（与 --rate 配合使用）')
    parser.add_argument('--history', action='store_true', help='读取对话历史')
    parser.add_argument('--stats', action='store_true', help='查看评分统计')
    parser.add_argument('--config-status', action='store_true', help='查看配置状态')
    parser.add_argument('--check-first-run', action='store_true', help='检查是否首次运行')
    parser.add_argument('--setup', action='store_true', help='进入配置流程')
    parser.add_argument('--scheduler', action='store_true', help='启动定时调度器')
    parser.add_argument('--set-trigger-time', help='设置固定触发时间（HH:MM 格式，多个逗号分隔）')
    parser.add_argument('--random', action='store_true', help='使用随机时间模式')
    parser.add_argument('--count', type=int, default=1, help='随机模式每天次数（默认1）')
    parser.add_argument('--window-start', default='09:00', help='随机模式起始时间（默认09:00）')
    parser.add_argument('--window-end', default='21:00', help='随机模式结束时间（默认21:00）')
    parser.add_argument('--personality', help='加载人格文件路径')
    parser.add_argument('--test', action='store_true', help='测试模式')

    args = parser.parse_args()

    if args.search:
        cmd_search(args.search)
    elif args.rate:
        score = int(args.rate[1]) if args.rate[1].isdigit() else 0
        cmd_rate(args.rate[0], score, args.feedback or '', args.artist or '')
    elif args.history:
        cmd_history()
    elif args.stats:
        cmd_stats()
    elif args.config_status:
        cmd_config_status()
    elif args.check_first_run:
        cmd_check_first_run()
    elif args.personality:
        cmd_personality(args.personality)
    elif args.setup:
        cmd_setup()
    elif args.set_trigger_time or args.random:
        cmd_set_trigger_time(
            time_str=args.set_trigger_time,
            random_mode=args.random,
            random_count=args.count,
            window_start=args.window_start,
            window_end=args.window_end
        )
    elif args.scheduler:
        cmd_scheduler()
    elif args.test:
        print("✅ 测试模式 - 所有模块就绪")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
