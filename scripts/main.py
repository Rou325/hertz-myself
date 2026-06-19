#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import argparse
import json
from datetime import datetime

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from scripts.search_tools import search_tools
from scripts.user_rating import user_rating_system
from scripts.scheduler import create_scheduler
from scripts.weather_detector import weather_detector
from scripts.personality_detector import personality_detector


def cmd_search(query: str, count: int = 5):
    best_method = search_tools.get_best_method()
    print(json.dumps({
        'query': query,
        'method': best_method,
        'instructions': f'请使用 {best_method.upper()} 搜索：{query}',
        'count': count,
        'filters': ['exclude:抖音热歌', 'exclude:网络神曲', 'exclude:口水歌']
    }, ensure_ascii=False))


def cmd_rate(song_name: str, score: int, feedback: str = '', artist: str = ''):
    song_info = {'name': song_name, 'artist': artist or '未知'}
    result = user_rating_system.parse_rating_input(f'{score} {feedback}')
    if result is None:
        print(json.dumps({'success': False, 'error': '无效评分'}))
        return
    success = user_rating_system.add_rating(
        song_info, result['rating'], result.get('feedback', '')
    )
    stats = user_rating_system.get_rating_statistics()
    print(json.dumps({
        'success': success,
        'score': result['rating'],
        'feedback': result.get('feedback', ''),
        'total_ratings': stats.get('total_ratings', 0),
        'average_rating': round(stats.get('average_rating', 0), 1)
    }, ensure_ascii=False))


def cmd_stats():
    print(user_rating_system.format_statistics())


def cmd_config_status():
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


def cmd_set_trigger_time(time_str: str = None, random_mode: bool = False,
                         random_count: int = 1, window_start: str = '09:00',
                         window_end: str = '21:00'):
    scheduler = create_scheduler()
    if random_mode:
        scheduler.set_random_trigger(
            count=random_count, window_start=window_start, window_end=window_end
        )
        print(json.dumps({
            'success': True, 'mode': 'random',
            'count': random_count, 'window_start': window_start, 'window_end': window_end
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


def cmd_config_save(json_str: str):
    try:
        data = json.loads(json_str)
        for key, value in data.items():
            search_tools.config[key] = value
        search_tools._save_config()
        print(json.dumps({'success': True}))
    except json.JSONDecodeError as e:
        print(json.dumps({'success': False, 'error': str(e)}))


def cmd_config_api(api_names: str):
    result = {}
    for name in api_names.split(','):
        name = name.strip().lower()
        if name in ('exa', 'tavily', 'spotify', 'websearch'):
            search_tools.config[name]['enabled'] = True
            result[name] = 'enabled'
        else:
            result[name] = 'unknown'
    search_tools._save_config()
    if not search_tools.is_first_run():
        search_tools.mark_configured()
    print(json.dumps({'success': True, 'apis': result}))


def cmd_test_api(api_name: str, api_key: str = None, client_secret: str = None):
    import urllib.request, urllib.error
    api_name = api_name.strip().lower()
    try:
        if api_name == 'exa':
            req = urllib.request.Request(
                'https://api.exa.ai/search',
                headers={'x-api-key': api_key or '', 'Content-Type': 'application/json'},
                data=b'{"query":"test","numResults":1}'
            )
            resp = urllib.request.urlopen(req, timeout=10)
            print(json.dumps({'success': resp.status == 200, 'api': 'exa'}))
        elif api_name == 'tavily':
            import urllib.parse
            data = urllib.parse.urlencode({
                'api_key': api_key or '', 'query': 'test', 'max_results': 1
            }).encode()
            req = urllib.request.Request('https://api.tavily.com/search', data=data)
            resp = urllib.request.urlopen(req, timeout=10)
            print(json.dumps({'success': resp.status == 200, 'api': 'tavily'}))
        elif api_name == 'spotify':
            import base64
            auth = base64.b64encode(f'{api_key or ""}:{client_secret or ""}'.encode()).decode()
            req = urllib.request.Request(
                'https://accounts.spotify.com/api/token',
                headers={'Authorization': f'Basic {auth}'},
                data=b'grant_type=client_credentials'
            )
            resp = urllib.request.urlopen(req, timeout=10)
            print(json.dumps({'success': resp.status == 200, 'api': 'spotify'}))
        else:
            print(json.dumps({'success': False, 'error': f'未知 API: {api_name}'}))
    except urllib.error.HTTPError as e:
        print(json.dumps({'success': False, 'api': api_name, 'error': f'HTTP {e.code}'}))
    except Exception as e:
        print(json.dumps({'success': False, 'api': api_name, 'error': str(e)}))


def cmd_personality(file_path: str = None):
    if file_path and os.path.exists(file_path):
        p = personality_detector.load_personality_from_file(file_path)
        if p:
            print(json.dumps({'loaded': True, 'style': 'custom', 'file': file_path}, ensure_ascii=False))
            return
    print(json.dumps({'loaded': False, 'style': 'default'}))


def main():
    parser = argparse.ArgumentParser(description='听见自己的频率 - 后端命令')
    parser.add_argument('--search', help='搜索歌曲，参数为搜索词')
    parser.add_argument('--rate', nargs=2, metavar=('歌曲名', '评分'), help='记录评分')
    parser.add_argument('--feedback', help='评分反馈')
    parser.add_argument('--artist', help='歌手名')
    parser.add_argument('--stats', action='store_true', help='查看评分统计')
    parser.add_argument('--config-status', action='store_true', help='查看配置状态')
    parser.add_argument('--set-trigger-time', help='设置固定触发时间（HH:MM，多个逗号分隔）')
    parser.add_argument('--random', action='store_true', help='使用随机时间模式')
    parser.add_argument('--count', type=int, default=1, help='随机模式每天次数')
    parser.add_argument('--window-start', default='09:00', help='随机模式起始时间')
    parser.add_argument('--window-end', default='21:00', help='随机模式结束时间')
    parser.add_argument('--config-save', help='保存配置 JSON')
    parser.add_argument('--config-api', help='启用 API（逗号分隔）')
    parser.add_argument('--test-api', help='测试 API Key（exa/tavily/spotify）')
    parser.add_argument('--api-key', help='API Key')
    parser.add_argument('--client-secret', help='Client Secret（配合 --test-api spotify）')
    parser.add_argument('--personality', help='加载人格文件路径')
    parser.add_argument('--test', action='store_true', help='测试模式')

    args = parser.parse_args()

    if args.search:
        cmd_search(args.search)
    elif args.rate:
        score = int(args.rate[1]) if args.rate[1].isdigit() else 0
        cmd_rate(args.rate[0], score, args.feedback or '', args.artist or '')
    elif args.stats:
        cmd_stats()
    elif args.config_status:
        cmd_config_status()
    elif args.config_save:
        cmd_config_save(args.config_save)
    elif args.config_api:
        cmd_config_api(args.config_api)
    elif args.test_api:
        cmd_test_api(args.test_api, args.api_key, args.client_secret)
    elif args.personality:
        cmd_personality(args.personality)
    elif args.set_trigger_time or args.random:
        cmd_set_trigger_time(
            time_str=args.set_trigger_time, random_mode=args.random,
            random_count=args.count, window_start=args.window_start,
            window_end=args.window_end
        )
    elif args.test:
        print("✅ 测试模式 - 所有模块就绪")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
