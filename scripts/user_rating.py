#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户评分系统 - 记录用户对推荐歌曲的反馈
支持多维度评分、偏好学习、个性化推荐
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import Counter

class UserRatingSystem:
    """用户评分系统 - 支持多维度评分和偏好学习"""

    def __init__(self, data_dir: str = None):
        """
        初始化评分系统

        Args:
            data_dir: 数据存储目录
        """
        self.data_dir = data_dir or os.path.join(
            os.path.dirname(__file__), '..', 'data'
        )
        self.ratings_file = os.path.join(self.data_dir, 'user_ratings.json')
        self.preferences_file = os.path.join(self.data_dir, 'user_preferences.json')

        # 确保目录存在
        os.makedirs(self.data_dir, exist_ok=True)

        # 加载数据
        self.ratings = self._load_ratings()
        self.preferences = self._load_preferences()

    def _load_ratings(self) -> Dict:
        """加载评分数据"""
        try:
            if os.path.exists(self.ratings_file):
                with open(self.ratings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载评分数据失败: {e}")
        return {'ratings': [], 'statistics': {}}

    def _load_preferences(self) -> Dict:
        """加载用户偏好"""
        try:
            if os.path.exists(self.preferences_file):
                with open(self.preferences_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载用户偏好失败: {e}")
        return {
            'favorite_artists': [],
            'favorite_genres': [],
            'favorite_moods': [],
            'favorite_languages': [],
            'disliked_songs': [],
            'preferred_eras': [],
            'listening_time_preferences': {},
            'rating_history': []
        }

    def _save_ratings(self):
        """保存评分数据"""
        try:
            with open(self.ratings_file, 'w', encoding='utf-8') as f:
                json.dump(self.ratings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存评分数据失败: {e}")

    def _save_preferences(self):
        """保存用户偏好"""
        try:
            with open(self.preferences_file, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存用户偏好失败: {e}")

    def add_rating(self, song_info: Dict, rating: int, feedback: str = '',
                   mood: str = None, scene: str = None, time_of_day: str = None) -> bool:
        """
        添加多维度评分

        Args:
            song_info: 歌曲信息
            rating: 评分 (1-10)
            feedback: 用户反馈
            mood: 评分时的心情
            scene: 评分时的场景
            time_of_day: 评分时间（早晨/下午/晚上/深夜）

        Returns:
            是否添加成功
        """
        if not 1 <= rating <= 10:
            print("评分必须在 1-10 之间")
            return False

        # 获取当前时间信息
        now = datetime.now()
        hour = now.hour

        if time_of_day is None:
            if 6 <= hour < 12:
                time_of_day = 'morning'
            elif 12 <= hour < 18:
                time_of_day = 'afternoon'
            elif 18 <= hour < 22:
                time_of_day = 'evening'
            else:
                time_of_day = 'night'

        rating_record = {
            'id': len(self.ratings.get('ratings', [])) + 1,
            'timestamp': now.isoformat(),
            'song': {
                'name': song_info.get('name', ''),
                'artist': song_info.get('artist', ''),
                'album': song_info.get('album', ''),
                'genre': song_info.get('genre', ''),
                'language': song_info.get('language', ''),
                'release_date': song_info.get('release_date', ''),
                'tags': song_info.get('tags', [])
            },
            'rating': rating,
            'feedback': feedback,
            'context': {
                'mood': mood,
                'scene': scene,
                'time_of_day': time_of_day,
                'day_of_week': now.strftime('%A'),
                'hour': hour
            }
        }

        if 'ratings' not in self.ratings:
            self.ratings['ratings'] = []

        self.ratings['ratings'].append(rating_record)

        # 更新统计信息
        self._update_statistics(song_info, rating, time_of_day)

        # 更新用户偏好
        self._update_preferences(song_info, rating, mood, time_of_day)

        # 保存数据
        self._save_ratings()
        self._save_preferences()

        return True

    def _update_statistics(self, song_info: Dict, rating: int, time_of_day: str):
        """更新统计信息"""
        if 'statistics' not in self.ratings:
            self.ratings['statistics'] = {
                'average_rating': 0,
                'total_ratings': 0,
                'rating_distribution': {str(i): 0 for i in range(1, 6)},
                'time_distribution': {},
                'genre_distribution': {},
                'artist_distribution': {}
            }

        stats = self.ratings['statistics']

        # 更新平均评分
        total = stats.get('total_ratings', 0)
        current_avg = stats.get('average_rating', 0)
        stats['average_rating'] = (current_avg * total + rating) / (total + 1)
        stats['total_ratings'] = total + 1

        # 更新评分分布
        stats['rating_distribution'][str(rating)] = stats['rating_distribution'].get(str(rating), 0) + 1

        # 更新时间分布
        if 'time_distribution' not in stats:
            stats['time_distribution'] = {}
        stats['time_distribution'][time_of_day] = stats['time_distribution'].get(time_of_day, 0) + 1

        # 更新风格分布
        genre = song_info.get('genre', '未知')
        if 'genre_distribution' not in stats:
            stats['genre_distribution'] = {}
        stats['genre_distribution'][genre] = stats['genre_distribution'].get(genre, 0) + 1

        # 更新歌手分布
        artist = song_info.get('artist', '未知')
        if 'artist_distribution' not in stats:
            stats['artist_distribution'] = {}
        stats['artist_distribution'][artist] = stats['artist_distribution'].get(artist, 0) + 1

    def _update_preferences(self, song_info: Dict, rating: int, mood: str = None, time_of_day: str = None):
        """更新用户偏好"""
        artist = song_info.get('artist', '')
        genre = song_info.get('genre', '')
        language = song_info.get('language', '')
        release_date = song_info.get('release_date', '')

        # 提取年代
        era = None
        if release_date:
            try:
                year = int(release_date[:4])
                if year < 2000:
                    era = '90s'
                elif year < 2010:
                    era = '2000s'
                elif year < 2020:
                    era = '2010s'
                else:
                    era = '2020s'
            except:
                pass

        # 高评分 (7-10) 更新喜好
        if rating >= 7:
            if artist and artist not in self.preferences['favorite_artists']:
                self.preferences['favorite_artists'].append(artist)

            if genre and genre not in self.preferences['favorite_genres']:
                self.preferences['favorite_genres'].append(genre)

            if language and language not in self.preferences['favorite_languages']:
                self.preferences['favorite_languages'].append(language)

            if era and era not in self.preferences['preferred_eras']:
                self.preferences['preferred_eras'].append(era)

            if mood and mood not in self.preferences['favorite_moods']:
                self.preferences['favorite_moods'].append(mood)

            # 记录时间偏好
            if time_of_day:
                if 'listening_time_preferences' not in self.preferences:
                    self.preferences['listening_time_preferences'] = {}
                if time_of_day not in self.preferences['listening_time_preferences']:
                    self.preferences['listening_time_preferences'][time_of_day] = []
                self.preferences['listening_time_preferences'][time_of_day].append(genre)

        # 低评分 (1-3) 更新不喜欢
        elif rating <= 3:
            song_key = f"{artist} - {song_info.get('name', '')}"
            if song_key not in self.preferences['disliked_songs']:
                self.preferences['disliked_songs'].append(song_key)

        # 记录评分历史
        if 'rating_history' not in self.preferences:
            self.preferences['rating_history'] = []
        self.preferences['rating_history'].append({
            'timestamp': datetime.now().isoformat(),
            'rating': rating,
            'genre': genre,
            'artist': artist,
            'mood': mood
        })

        # 限制历史记录数量
        if len(self.preferences['rating_history']) > 100:
            self.preferences['rating_history'] = self.preferences['rating_history'][-100:]

    def get_user_preferences(self) -> Dict:
        """获取用户偏好"""
        return self.preferences

    def get_rating_statistics(self) -> Dict:
        """获取评分统计"""
        return self.ratings.get('statistics', {})

    def get_recent_ratings(self, limit: int = 10) -> List[Dict]:
        """获取最近的评分记录"""
        ratings = self.ratings.get('ratings', [])
        return ratings[-limit:] if len(ratings) > limit else ratings

    def get_high_rated_songs(self, min_rating: int = 7) -> List[Dict]:
        """获取高评分歌曲"""
        ratings = self.ratings.get('ratings', [])
        return [r for r in ratings if r.get('rating', 0) >= min_rating]

    def get_recommendation_feedback(self, song_info: Dict) -> Optional[Dict]:
        """
        获取歌曲的历史评分

        Args:
            song_info: 歌曲信息

        Returns:
            历史评分记录（如果有）
        """
        ratings = self.ratings.get('ratings', [])
        song_name = song_info.get('name', '')
        artist = song_info.get('artist', '')

        for rating in ratings:
            if (rating['song']['name'] == song_name and
                rating['song']['artist'] == artist):
                return rating

        return None

    def should_recommend_again(self, song_info: Dict) -> bool:
        """
        判断是否应该再次推荐该歌曲

        Args:
            song_info: 歌曲信息

        Returns:
            是否应该推荐
        """
        # 检查是否在不喜欢列表中
        song_key = f"{song_info.get('artist', '')} - {song_info.get('name', '')}"
        if song_key in self.preferences.get('disliked_songs', []):
            return False

        # 检查历史评分
        history = self.get_recommendation_feedback(song_info)
        if history:
            # 如果之前评分为 1-3，不再推荐
            if history.get('rating', 0) <= 3:
                return False

            # 如果最近 7 天内推荐过，不再推荐
            try:
                last_time = datetime.fromisoformat(history['timestamp'])
                days_since = (datetime.now() - last_time).days
                if days_since < 7:
                    return False
            except:
                pass

        return True

    def get_personalized_suggestions(self, mood: str = None, time_of_day: str = None) -> Dict:
        """
        获取个性化推荐建议

        Args:
            mood: 当前心情
            time_of_day: 当前时间

        Returns:
            个性化建议
        """
        preferences = self.preferences
        stats = self.get_rating_statistics()

        suggestions = {
            'preferred_artists': preferences.get('favorite_artists', [])[-5:],
            'preferred_genres': preferences.get('favorite_genres', [])[-3:],
            'preferred_languages': preferences.get('favorite_languages', [])[-2:],
            'preferred_eras': preferences.get('preferred_eras', [])[-2:],
            'disliked_songs': preferences.get('disliked_songs', [])[-10:],
            'time_preferences': {}
        }

        # 时间偏好
        if time_of_day:
            time_prefs = preferences.get('listening_time_preferences', {})
            if time_of_day in time_prefs:
                # 统计该时间段最常听的风格
                genre_counts = Counter(time_prefs[time_of_day])
                suggestions['time_preferences'] = {
                    'top_genres': [g for g, _ in genre_counts.most_common(3)]
                }

        # 心情偏好
        if mood:
            mood_history = [r for r in preferences.get('rating_history', [])
                          if r.get('mood') == mood and r.get('rating', 0) >= 4]
            if mood_history:
                mood_genres = [r.get('genre') for r in mood_history if r.get('genre')]
                if mood_genres:
                    genre_counts = Counter(mood_genres)
                    suggestions['mood_preferences'] = {
                        'top_genres': [g for g, _ in genre_counts.most_common(3)]
                    }

        return suggestions

    def generate_rating_prompt(self, song_info: Dict) -> str:
        """
        生成评分提示语

        Args:
            song_info: 歌曲信息

        Returns:
            评分提示语
        """
        song_name = song_info.get('name', '这首歌')
        artist = song_info.get('artist', '未知艺术家')

        prompt = f"""
《{song_name}》- {artist} 听完感觉如何？

满分10分，回复数字即可，例如：8 很好听
写下你的感受能帮助我更好地了解你的喜好！
"""
        return prompt

    def parse_rating_input(self, user_input: str) -> Optional[Dict]:
        """
        解析用户评分输入

        Args:
            user_input: 用户输入

        Returns:
            解析结果
        """
        user_input = user_input.strip()

        # 提取评分数字
        rating = None
        feedback = ''
        mood = None
        scene = None

        # 提取评分（支持10分制）
        # 首先尝试提取两位数
        import re
        rating_match = re.search(r'\b(\d{1,2})\b', user_input)
        if rating_match:
            rating = int(rating_match.group(1))
            if not 1 <= rating <= 10:
                rating = None

        if rating is None:
            return None

        # 提取反馈
        rating_pos = user_input.find(str(rating))
        if rating_pos != -1:
            remaining = user_input[rating_pos + len(str(rating)):].strip()
            # 去掉可能的分隔符
            if remaining and remaining[0] in '，。、；：':
                remaining = remaining[1:].strip()

            # 尝试提取心情和场景
            mood_keywords = ['快乐', '开心', '平静', '忧郁', '悲伤', '兴奋', '放松']
            scene_keywords = ['工作', '休息', '运动', '学习', '睡觉', '开车']

            for keyword in mood_keywords:
                if keyword in remaining:
                    mood = keyword
                    remaining = remaining.replace(keyword, '').strip()
                    break

            for keyword in scene_keywords:
                if keyword in remaining:
                    scene = keyword
                    remaining = remaining.replace(keyword, '').strip()
                    break

            feedback = remaining

        return {
            'rating': rating,
            'feedback': feedback,
            'mood': mood,
            'scene': scene
        }

    def format_statistics(self) -> str:
        """格式化统计信息"""
        stats = self.get_rating_statistics()
        preferences = self.get_user_preferences()
        recent_ratings = self.get_recent_ratings(5)

        total = stats.get('total_ratings', 0)
        avg = stats.get('average_rating', 0)
        distribution = stats.get('rating_distribution', {})

        output = f"""
📊 你的音乐评分统计

🎵 评分概览
- 总评分次数：{total}
- 平均评分：{avg:.1f}分

⭐ 评分分布
- 5分：{distribution.get('5', 0)} 次
- 4分：{distribution.get('4', 0)} 次
- 3分：{distribution.get('3', 0)} 次
- 2分：{distribution.get('2', 0)} 次
- 1分：{distribution.get('1', 0)} 次

🎤 喜欢的歌手
{', '.join(preferences.get('favorite_artists', ['暂无'])[-5:])}

🎸 喜欢的风格
{', '.join(preferences.get('favorite_genres', ['暂无'])[-3:])}

🌍 偏好语言
{', '.join(preferences.get('favorite_languages', ['暂无'])[-2:])}

📅 偏好年代
{', '.join(preferences.get('preferred_eras', ['暂无'])[-2:])}

📝 最近评分
"""
        for rating in recent_ratings:
            stars = '⭐' * rating.get('rating', 0)
            song = rating.get('song', {})
            output += f"- 《{song.get('name', '未知')}》- {song.get('artist', '未知')}：{stars}\n"

        return output

# 创建全局实例
user_rating_system = UserRatingSystem()
