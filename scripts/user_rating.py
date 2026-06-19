#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户评分系统 - 记录用户对推荐歌曲的反馈
"""
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional
from collections import Counter


class UserRatingSystem:
    """用户评分系统"""

    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or os.path.join(
            os.path.dirname(__file__), '..', 'data'
        )
        self.ratings_file = os.path.join(self.data_dir, 'user_ratings.json')
        self.ratings_log = os.path.join(self.data_dir, '.ratings_log')
        self.preferences_file = os.path.join(self.data_dir, 'user_preferences.json')
        os.makedirs(self.data_dir, exist_ok=True)
        self.ratings = self._load_ratings()
        self.preferences = self._load_preferences()

    def _load_ratings(self) -> Dict:
        """加载评分，先从主文件读，再合并追加日志"""
        ratings = {'ratings': [], 'statistics': {}}
        try:
            if os.path.exists(self.ratings_file):
                with open(self.ratings_file, 'r', encoding='utf-8') as f:
                    ratings = json.load(f)
        except Exception:
            pass
        # 合并追加日志中的新评分
        try:
            if os.path.exists(self.ratings_log):
                with open(self.ratings_log, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            record = json.loads(line)
                            ratings.setdefault('ratings', []).append(record)
                        except json.JSONDecodeError:
                            pass
                # 合并完成后写回主文件并清空日志
                with open(self.ratings_file, 'w', encoding='utf-8') as f:
                    json.dump(ratings, f, ensure_ascii=False, indent=2)
                os.remove(self.ratings_log)
        except Exception:
            pass
        return ratings

    def _load_preferences(self) -> Dict:
        try:
            if os.path.exists(self.preferences_file):
                with open(self.preferences_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {'favorite_artists': [], 'favorite_genres': [], 'disliked_songs': []}

    def _save_ratings(self):
        try:
            with open(self.ratings_file, 'w', encoding='utf-8') as f:
                json.dump(self.ratings, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _save_preferences(self):
        try:
            with open(self.preferences_file, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def add_rating(self, song_info: Dict, rating: int, feedback: str = '',
                   mood: str = None, scene: str = None) -> bool:
        if not 1 <= rating <= 10:
            return False

        record = {
            'id': len(self.ratings.get('ratings', [])) + 1,
            'timestamp': datetime.now().isoformat(),
            'song': {
                'name': song_info.get('name', ''),
                'artist': song_info.get('artist', ''),
                'genre': song_info.get('genre', ''),
            },
            'rating': rating,
            'feedback': feedback,
        }

        if 'ratings' not in self.ratings:
            self.ratings['ratings'] = []
        self.ratings['ratings'].append(record)
        self._update_stats(song_info, rating)
        self._update_prefs(song_info, rating)
        self._save_ratings()
        self._save_preferences()
        return True

    def _update_stats(self, song_info: Dict, rating: int):
        if 'statistics' not in self.ratings or not isinstance(self.ratings['statistics'], dict):
            self.ratings['statistics'] = {'average_rating': 0.0, 'total_ratings': 0}
        stats = self.ratings['statistics']
        if 'total_ratings' not in stats:
            stats['total_ratings'] = 0
            stats['average_rating'] = 0.0
        total = stats['total_ratings']
        stats['average_rating'] = (stats['average_rating'] * total + rating) / (total + 1)
        stats['total_ratings'] = total + 1

    def _update_prefs(self, song_info: Dict, rating: int):
        artist = song_info.get('artist', '')
        genre = song_info.get('genre', '')
        if rating >= 7:
            if artist and artist not in self.preferences['favorite_artists']:
                self.preferences['favorite_artists'].append(artist)
            if genre and genre not in self.preferences['favorite_genres']:
                self.preferences['favorite_genres'].append(genre)
        elif rating <= 3:
            key = f"{artist} - {song_info.get('name', '')}"
            if key not in self.preferences['disliked_songs']:
                self.preferences['disliked_songs'].append(key)

    def get_rating_statistics(self) -> Dict:
        return self.ratings.get('statistics', {})

    def get_user_preferences(self) -> Dict:
        return self.preferences

    def get_recent_ratings(self, limit: int = 10) -> List[Dict]:
        ratings = self.ratings.get('ratings', [])
        return ratings[-limit:] if len(ratings) > limit else ratings

    def parse_rating_input(self, user_input: str) -> Optional[Dict]:
        user_input = user_input.strip()
        match = re.search(r'\b(\d{1,2})\b', user_input)
        if not match:
            return None
        rating = int(match.group(1))
        if not 1 <= rating <= 10:
            return None
        pos = user_input.find(str(rating))
        feedback = user_input[pos + len(str(rating)):].strip().lstrip('，。、；：')
        return {'rating': rating, 'feedback': feedback}

    def format_statistics(self) -> str:
        stats = self.get_rating_statistics()
        prefs = self.get_user_preferences()
        recent = self.get_recent_ratings(5)
        total = stats.get('total_ratings', 0)
        avg = stats.get('average_rating', 0)

        out = f"📊 评分统计\n总评分：{total}  平均：{avg:.1f}分\n\n"
        out += f"🎤 喜欢的歌手：{', '.join(prefs.get('favorite_artists', ['暂无'])[-5:])}\n"
        out += f"🎸 喜欢的风格：{', '.join(prefs.get('favorite_genres', ['暂无'])[-3:])}\n\n"
        out += "📝 最近评分：\n"
        for r in recent:
            song = r.get('song', {})
            out += f"- 《{song.get('name', '未知')}》{song.get('artist', '')}：{'⭐' * r.get('rating', 0)}\n"
        return out


# 全局实例
user_rating_system = UserRatingSystem()
