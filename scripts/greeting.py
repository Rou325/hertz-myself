#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开场白模块
生成专属的开场白
支持随机模板、天气、聊天内容和音乐类型
"""

import random
from typing import Dict, Optional

class GreetingGenerator:
    """开场白生成器"""

    def __init__(self):
        """初始化开场白生成器"""
        self.project_name = "hertz-myself"

    def generate(self, mood: str = None, weather: Dict = None, personality: Dict = None, song_name: str = None) -> str:
        """
        生成开场白

        Args:
            mood: 情绪类型
            weather: 天气信息
            personality: 人格信息
            song_name: 歌曲名称

        Returns:
            开场白文本
        """
        # 如果有人格文件，用人格的语气写开场白
        if personality:
            return self._generate_with_personality(mood, weather, personality, song_name)

        # 如果没有人格文件，使用随机模板
        return self._generate_with_random_template(mood, weather, song_name)

    def _get_weather_desc(self, weather: Dict) -> str:
        """
        获取天气描述

        Args:
            weather: 天气信息

        Returns:
            天气描述文本
        """
        if not weather:
            return ''

        city = weather.get('city', '你的城市')
        temperature = weather.get('temperature', '未知')
        condition = weather.get('condition', '未知')

        if '晴' in condition or 'sunny' in condition.lower():
            return f"今天 {city} 阳光正好，{temperature}°C 的温暖"
        elif '雨' in condition or 'rain' in condition.lower():
            return f"今天 {city} 细雨绵绵，{temperature}°C 的凉意"
        elif '阴' in condition or 'cloudy' in condition.lower():
            return f"今天 {city} 云层低垂，{temperature}°C 的沉静"
        elif '雪' in condition or 'snow' in condition.lower():
            return f"今天 {city} 雪花飘落，{temperature}°C 的纯净"
        else:
            return f"今天 {city} {condition}，{temperature}°C"

    def _get_music_desc(self, song_name: str) -> str:
        """
        获取音乐描述

        Args:
            song_name: 歌曲名称

        Returns:
            音乐描述文本
        """
        if not song_name:
            return ''

        templates = [
            f"来一首《{song_name}》吧",
            f"送你一首《{song_name}》",
            f"推荐一首《{song_name}》",
            f"今天适合听《{song_name}》",
        ]
        return random.choice(templates)

    def _generate_with_personality(self, mood: str, weather: Dict, personality: Dict, song_name: str) -> str:
        """
        生成带人格的开场白

        Args:
            mood: 情绪类型
            weather: 天气信息
            personality: 人格信息
            song_name: 歌曲名称

        Returns:
            开场白文本
        """
        style = personality.get('style', 'neutral')
        vocabulary = personality.get('vocabulary', [])

        # 根据人格风格生成开场白
        if style == 'cute':
            return self._generate_cute_greeting(weather, vocabulary, song_name)
        elif style == 'formal':
            return self._generate_formal_greeting(weather, song_name)
        elif style == 'humorous':
            return self._generate_humorous_greeting(weather, vocabulary, song_name)
        elif style == 'gentle':
            return self._generate_gentle_greeting(weather, vocabulary, song_name)
        else:
            return self._generate_with_random_template(mood, weather, song_name)

    def _generate_cute_greeting(self, weather: Dict, vocabulary: list, song_name: str) -> str:
        """生成可爱风格的开场白"""
        suffix = vocabulary[0] if vocabulary else '呢'
        weather_desc = self._get_weather_desc(weather)
        music_desc = self._get_music_desc(song_name)

        greeting = f"""
我是 {self.project_name}{suffix}

捕捉到你情绪的起伏啦{suffix}
{weather_desc}{suffix}
{music_desc}{suffix}

戴上耳机，听见自己{suffix}
"""
        return greeting.strip()

    def _generate_formal_greeting(self, weather: Dict, song_name: str) -> str:
        """生成正式风格的开场白"""
        weather_desc = self._get_weather_desc(weather)
        music_desc = self._get_music_desc(song_name)

        greeting = f"""
我是 {self.project_name}

{weather_desc}
为您推荐《{song_name}》

戴上耳机，听见自己
"""
        return greeting.strip()

    def _generate_humorous_greeting(self, weather: Dict, vocabulary: list, song_name: str) -> str:
        """生成幽默风格的开场白"""
        prefix = vocabulary[0] if vocabulary else '哈哈'
        weather_desc = self._get_weather_desc(weather)
        music_desc = self._get_music_desc(song_name)

        greeting = f"""
{prefix}，我是 {self.project_name}

{weather_desc}
{music_desc}

戴上耳机，听见自己
"""
        return greeting.strip()

    def _generate_gentle_greeting(self, weather: Dict, vocabulary: list, song_name: str) -> str:
        """生成温柔风格的开场白"""
        suffix = vocabulary[0] if vocabulary else '亲爱的'
        weather_desc = self._get_weather_desc(weather)
        music_desc = self._get_music_desc(song_name)

        greeting = f"""
我是 {self.project_name}，{suffix}

{weather_desc}
{music_desc}

戴上耳机，听见自己
"""
        return greeting.strip()

    def _generate_with_random_template(self, mood: str, weather: Dict, song_name: str) -> str:
        """
        使用随机模板生成开场白

        Args:
            mood: 情绪类型
            weather: 天气信息
            song_name: 歌曲名称

        Returns:
            开场白文本
        """
        weather_desc = self._get_weather_desc(weather)
        music_desc = self._get_music_desc(song_name)

        # 随机开场白模板
        templates = [
            f"""我是 {self.project_name}，捕捉到了你情绪的起伏
{weather_desc}
{music_desc}

戴上耳机，听见自己""",

            f"""我是 {self.project_name}，感受到了今天空气里的温度
{weather_desc}
{music_desc}

戴上耳机，听见自己""",

            f"""我是 {self.project_name}，你的专属频率
{weather_desc}
{music_desc}

戴上耳机，听见自己""",

            f"""我是 {self.project_name}，今天为你准备了一首歌
{weather_desc}
{music_desc}

戴上耳机，听见自己""",
        ]

        return random.choice(templates).strip()

# 创建全局实例
greeting_generator = GreetingGenerator()
