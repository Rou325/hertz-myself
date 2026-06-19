#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
听见自己的频率 - 智能音乐推荐主程序
支持多种搜索方式、多维度评分、个性化推荐
"""

import sys
import os
import argparse
import json
from datetime import datetime
from typing import Dict, Optional

# 设置标准输出编码为 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加当前目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from scripts.read_history import read_history
from scripts.analyze_mood import analyze_conversation_mood
from scripts.search_tools import search_tools
from scripts.user_rating import user_rating_system
from scripts.scheduler import create_scheduler
from scripts.weather_detector import weather_detector
from scripts.personality_detector import personality_detector
from scripts.greeting import greeting_generator

class HertzMyself:
    """听见自己的频率 - 智能音乐推荐主类"""

    def __init__(self, config_path: str = None):
        """
        初始化

        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path
        self.history = []
        self.mood_result = {}
        self.recommendation_request = None

    def check_first_run(self) -> Optional[Dict]:
        """
        检查是否首次运行

        Returns:
            如果是首次运行，返回配置提示和选项；否则返回 None
        """
        if search_tools.is_first_run():
            return {
                'prompt': search_tools.get_setup_prompt(),
                'options': search_tools.get_setup_options(),
                'use_ui': True,  # 标记使用 UI 界面
                'ui_tools': ['AskUserQuestion', 'UserInput', 'SelectOption']  # 支持多种 UI 工具
            }
        return None

    def setup_api_keys(self, api_keys: Dict) -> str:
        """
        设置 API 密钥

        Args:
            api_keys: API 密钥字典

        Returns:
            设置结果消息
        """
        return search_tools.setup_api_keys(api_keys)

    def process_setup_choice(self, choice: str) -> Dict:
        """
        处理配置选择

        Args:
            choice: 用户选择（1/2/3）

        Returns:
            处理结果
        """
        return search_tools.process_setup_choice(choice)

    def process_api_config(self, api_id: str, config: Dict) -> str:
        """
        处理 API 配置

        Args:
            api_id: API ID（exa/tavily/spotify）
            config: 配置信息

        Returns:
            配置结果消息
        """
        return search_tools.process_api_config(api_id, config)

    def process_trigger_time_choice(self, choice: str, time_input: str = None) -> Dict:
        """
        处理触发时间选择

        Args:
            choice: 用户选择（1/2/3/4）
            time_input: 用户输入的时间

        Returns:
            处理结果
        """
        return search_tools.process_trigger_time_choice(choice, time_input)

    def process_personality_choice(self, choice: str, file_path: str = None) -> Dict:
        """
        处理人格检测选择

        Args:
            choice: 用户选择（1/2）
            file_path: 人格文件路径（选择 2 时需要）

        Returns:
            处理结果
        """
        return search_tools.process_personality_choice(choice, file_path)

    def run(self, manual: bool = False) -> Dict:
        """
        执行推荐

        Args:
            manual: 是否手动触发

        Returns:
            推荐结果信息
        """
        try:
            # 1. 检查是否首次运行
            first_run_result = self.check_first_run()
            if first_run_result:
                print(first_run_result['prompt'])
                return {
                    'first_run': True,
                    'prompt': first_run_result['prompt'],
                    'options': first_run_result['options']
                }

            # 2. 读取对话历史
            print("📖 读取对话历史...")
            self.history = read_history(self.config_path)
            print(f"   读取到 {len(self.history)} 条记录")

            # 3. 检测天气（如果有天气 skill）
            weather = None
            if weather_detector.has_weather_skill():
                print("🌤️ 检测到天气 skill，获取天气信息...")
                weather = weather_detector.get_weather_from_skill()
                if weather:
                    print(f"   天气：{weather.get('condition', '未知')} {weather.get('temperature', '未知')}°C")
                else:
                    print("   天气信息获取失败")
            else:
                print("🌤️ 未检测到天气 skill，跳过天气信息")

            # 4. 检查是否已加载人格文件
            personality = None
            if personality_detector.has_personality():
                print("🎭 已加载人格文件，使用人格风格...")
                personality = personality_detector.get_personality()
                if personality:
                    print(f"   人格风格：{personality.get('style', '未知')}")
                else:
                    print("   人格信息加载失败")
            else:
                print("🎭 未加载人格文件，使用默认风格")

            # 5. 分析情绪（结合天气）
            print("🎭 分析对话情绪...")
            self.mood_result = analyze_conversation_mood(self.history, weather)
            print(f"   情绪: {self.mood_result['mood']}")
            print(f"   主题: {self.mood_result['theme']}")

            # 6. 获取个性化建议
            print("📊 获取个性化建议...")
            suggestions = user_rating_system.get_personalized_suggestions(
                mood=self.mood_result.get('mood'),
                time_of_day=self._get_time_of_day()
            )

            # 7. 生成搜索查询
            print("🔍 生成搜索查询...")
            search_queries = search_tools.generate_search_queries(
                self.mood_result,
                diversity_level=3
            )

            # 8. 获取最佳搜索方法
            best_method = search_tools.get_best_method()
            print(f"   使用搜索方式: {best_method.upper()}")

            # 9. 生成推荐请求
            self.recommendation_request = {
                'timestamp': datetime.now().isoformat(),
                'mood_analysis': self.mood_result,
                'search_queries': search_queries,
                'personalized_suggestions': suggestions,
                'search_method': best_method,
                'search_instructions': search_tools.format_search_tool_prompt(search_queries),
                'personality': personality
            }

            # 10. 输出推荐请求
            print("\n✅ 推荐请求已生成！")
            print("请根据以下建议搜索歌曲：")
            print("=" * 50)
            print(self.recommendation_request['search_instructions'])
            print("=" * 50)

            return self.recommendation_request

        except Exception as e:
            error_msg = f"❌ 推荐失败: {e}"
            print(error_msg)
            return {'error': error_msg}

    def _get_time_of_day(self) -> str:
        """获取当前时间段"""
        hour = datetime.now().hour
        if 6 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'afternoon'
        elif 18 <= hour < 22:
            return 'evening'
        else:
            return 'night'

    def process_song_recommendation(self, song_info: Dict, weather: Dict = None) -> str:
        """
        处理歌曲推荐结果

        Args:
            song_info: 歌曲信息
            weather: 天气信息

        Returns:
            格式化的推荐文本
        """
        # 检查是否应该再次推荐
        if not user_rating_system.should_recommend_again(song_info):
            return "这首歌最近已经推荐过了，让我为你推荐另一首..."

        # 检查是否有历史评分
        history = user_rating_system.get_recommendation_feedback(song_info)
        history_text = ''
        if history:
            history_text = f"\n📊 你之前评分为：{'⭐' * history['rating']}"

        song_name = song_info.get('name', '未知')
        artist = song_info.get('artist', '未知')
        album = song_info.get('album', '未知')
        genre = song_info.get('genre', '未知')
        release_date = song_info.get('release_date', '未知')
        link = song_info.get('link', '未知')
        reason = song_info.get('reason', '')
        artist_intro = song_info.get('artist_intro', '')

        # 检测人格并应用风格
        personality = personality_detector.get_personality()
        if personality:
            # 应用人格风格到推荐理由
            reason = personality_detector.apply_personality(reason)

        # 获取情绪信息
        mood = self.mood_result.get('mood', 'neutral') if hasattr(self, 'mood_result') else 'neutral'

        # 获取人格信息
        personality = personality_detector.get_personality()

        # 获取歌曲名称
        song_name = song_info.get('name', None)

        # 生成开场白
        greeting = greeting_generator.generate(mood=mood, weather=weather, personality=personality, song_name=song_name)

        output = f"""
{greeting}

---

🎵 今日音乐推荐

🎶 歌曲信息

歌名：《{song_name}》
歌手：{artist}
专辑：{album}
风格：{genre}
发行时间：{release_date}

🎤 歌手简介
{artist_intro}

💡 推荐理由
{reason}
{history_text}

---

满分10分，回复数字即可，例如：8 很好听
写下你的感受能帮助我更好地了解你的喜好！

🎵 享受《{song_name}》带来的感动！
"""
        return output

    def process_user_rating(self, song_info: Dict, user_input: str) -> str:
        """
        处理用户评分

        Args:
            song_info: 歌曲信息
            user_input: 用户输入

        Returns:
            评分结果文本
        """
        # 解析用户输入
        rating_result = user_rating_system.parse_rating_input(user_input)

        if rating_result is None:
            return "请输入有效的评分（1-10分），例如：8 很好听"

        # 添加评分
        success = user_rating_system.add_rating(
            song_info,
            rating_result['rating'],
            rating_result.get('feedback', ''),
            mood=rating_result.get('mood'),
            scene=rating_result.get('scene')
        )

        if success:
            rating = rating_result['rating']
            stars = '⭐' * rating

            # 获取统计信息
            stats = user_rating_system.get_rating_statistics()
            total = stats.get('total_ratings', 0)
            avg = stats.get('average_rating', 0)

            return f"""
✅ 评分已记录！

你的评分：{stars} ({rating}分)
{'反馈：' + rating_result.get('feedback', '') if rating_result.get('feedback') else ''}
{'心情：' + rating_result.get('mood', '') if rating_result.get('mood') else ''}
{'场景：' + rating_result.get('scene', '') if rating_result.get('scene') else ''}

📊 评分统计
- 总评分次数：{total}
- 平均评分：{avg:.1f}分

感谢你的反馈！这将帮助我更好地推荐歌曲给你。
"""
        else:
            return "❌ 评分记录失败，请稍后重试"

    def get_user_statistics(self) -> str:
        """
        获取用户评分统计

        Returns:
            统计信息文本
        """
        return user_rating_system.format_statistics()

    def get_search_statistics(self) -> str:
        """
        获取搜索统计

        Returns:
            统计信息文本
        """
        stats = search_tools.get_search_statistics()

        if stats.get('total_searches', 0) == 0:
            return "暂无搜索记录"

        output = f"""
🔍 搜索统计

📊 搜索概览
- 总搜索次数：{stats.get('total_searches', 0)}
- 唯一查询数：{stats.get('unique_queries', 0)}
- 最后搜索：{stats.get('last_search', '未知')}

🔧 搜索方式分布
"""
        for method, count in stats.get('method_distribution', {}).items():
            output += f"- {method.upper()}: {count} 次\n"

        return output

    def get_config_status(self) -> str:
        """
        获取配置状态

        Returns:
            配置状态文本
        """
        available_methods = search_tools.get_available_methods()
        best_method = search_tools.get_best_method()

        output = f"""
⚙️ 配置状态

🔧 可用搜索方式
"""
        for method in available_methods:
            output += f"- ✅ {method.upper()}\n"

        output += f"\n🎯 推荐搜索方式：{best_method.upper()}"

        return output

    def start_scheduler(self):
        """启动定时调度器"""
        print("🚀 启动定时调度器...")
        scheduler = create_scheduler(self.run, auto_start=True)
        return scheduler

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='听见自己的频率 - 智能音乐推荐')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--manual', action='store_true', help='手动触发推荐')
    parser.add_argument('--scheduler', action='store_true', help='启动定时调度器')
    parser.add_argument('--test', action='store_true', help='测试模式')
    parser.add_argument('--stats', action='store_true', help='查看评分统计')
    parser.add_argument('--search-stats', action='store_true', help='查看搜索统计')
    parser.add_argument('--config-status', action='store_true', help='查看配置状态')
    parser.add_argument('--setup', action='store_true', help='重新配置 API 密钥')
    parser.add_argument('--set-trigger-time', help='设置触发时间，例如：18:00 或 8:00,12:00,18:00')

    args = parser.parse_args()

    # 创建推荐实例
    recommender = HertzMyself(args.config)

    if args.setup:
        # 重新配置
        print(search_tools.get_setup_prompt())
    elif args.set_trigger_time:
        # 设置触发时间
        try:
            times = [t.strip() for t in args.set_trigger_time.split(',')]
            for t in times:
                datetime.strptime(t, '%H:%M')  # 验证时间格式
            scheduler = recommender.start_scheduler()
            scheduler.set_trigger_times(times)
            print(f"✅ 已设置触发时间：{', '.join(times)}")
        except ValueError:
            print("❌ 时间格式错误，请使用 HH:MM 格式，例如：18:00 或 8:00,12:00,18:00")
    elif args.scheduler:
        # 启动定时调度器
        scheduler = recommender.start_scheduler()
        if scheduler.trigger_times:
            try:
                import time
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                scheduler.stop()
                print("\n定时调度器已停止")
        else:
            print("⚠️ 未设置触发时间，请使用 --set-trigger-time 设置")
    elif args.stats:
        # 查看评分统计
        print(recommender.get_user_statistics())
    elif args.search_stats:
        # 查看搜索统计
        print(recommender.get_search_statistics())
    elif args.config_status:
        # 查看配置状态
        print(recommender.get_config_status())
    elif args.test:
        # 测试模式
        print("🧪 测试模式")
        result = recommender.run(manual=True)
        if 'error' not in result and 'first_run' not in result:
            print("\n推荐请求生成成功！")
            print("请根据搜索指令查找歌曲。")
    else:
        # 手动触发
        result = recommender.run(manual=True)
        if 'error' not in result and 'first_run' not in result:
            print("\n推荐请求生成成功！")
            print("请根据搜索指令查找歌曲。")

if __name__ == '__main__':
    main()
