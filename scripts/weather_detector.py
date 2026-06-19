#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天气检测模块
检测是否有天气相关的 skills 可用，有就获取天气信息，没有就跳过
本模块不提供天气查询功能，只是利用已有的天气 skills
"""

import json
import os
import subprocess
from typing import Dict, Optional

class WeatherDetector:
    """天气检测器"""

    def __init__(self):
        """初始化天气检测器"""
        self.weather_skills = [
            'weather',
            '天气',
            'get-weather',
            'weather-skill'
        ]
        self.cached_weather = None

    def has_weather_skill(self) -> bool:
        """
        检测是否有天气相关的 skills 可用

        Returns:
            是否有天气 skills
        """
        # 检查常见的天气 skills 路径
        skill_paths = [
            os.path.expanduser('~/.claude/skills'),
            os.path.expanduser('~/.config/claude/skills'),
            os.path.join(os.path.dirname(__file__), '..', '..', '..', 'skills')
        ]

        for skill_path in skill_paths:
            if os.path.exists(skill_path):
                for skill_name in self.weather_skills:
                    skill_dir = os.path.join(skill_path, skill_name)
                    if os.path.exists(skill_dir):
                        return True

        return False

    def get_weather_from_skill(self, city: str = None) -> Optional[Dict]:
        """
        从天气 skill 获取天气信息

        Args:
            city: 城市名称

        Returns:
            天气信息字典，如果没有天气 skill 则返回 None
        """
        if not self.has_weather_skill():
            return None

        # 尝试调用天气 skill
        try:
            # 这里假设天气 skill 提供了命令行接口
            # 实际实现需要根据具体的天气 skill 来调整
            weather_info = self._call_weather_skill(city)
            return weather_info
        except Exception as e:
            print(f"调用天气 skill 失败: {e}")
            return None

    def _call_weather_skill(self, city: str = None) -> Optional[Dict]:
        """
        调用天气 skill

        Args:
            city: 城市名称

        Returns:
            天气信息
        """
        # 这里是示例实现，实际需要根据具体的天气 skill 来调整
        # 假设天气 skill 提供了命令行接口

        # 示例：尝试调用 weather 命令
        try:
            cmd = ['weather']
            if city:
                cmd.append(city)

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                # 解析天气输出
                return self._parse_weather_output(result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        return None

    def _parse_weather_output(self, output: str) -> Optional[Dict]:
        """
        解析天气输出

        Args:
            output: 天气命令的输出

        Returns:
            解析后的天气信息
        """
        # 简单解析，实际需要根据具体的输出格式来调整
        lines = output.strip().split('\n')

        weather = {
            'city': '未知',
            'temperature': 20,
            'condition': '晴',
            'humidity': 50,
            'wind': '微风',
            'description': output.strip()
        }

        # 尝试解析温度
        for line in lines:
            if '°C' in line or '度' in line:
                try:
                    temp = ''.join(filter(str.isdigit, line.split('°')[0].split('度')[0]))
                    if temp:
                        weather['temperature'] = int(temp)
                except:
                    pass

        return weather

    def get_weather_mood(self, weather: Optional[Dict]) -> str:
        """
        根据天气获取心情推荐

        Args:
            weather: 天气信息

        Returns:
            心情推荐
        """
        if not weather:
            return 'neutral'

        condition = weather.get('condition', '')
        temperature = weather.get('temperature', 20)

        if '晴' in condition or 'sunny' in condition.lower():
            return 'positive'
        elif '雨' in condition or 'rain' in condition.lower():
            return 'calm'
        elif '阴' in condition or 'cloudy' in condition.lower():
            return 'neutral'
        elif '雪' in condition or 'snow' in condition.lower():
            return 'calm'
        else:
            return 'neutral'

    def get_weather_theme(self, weather: Optional[Dict]) -> str:
        """
        根据天气获取主题推荐

        Args:
            weather: 天气信息

        Returns:
            主题推荐
        """
        if not weather:
            return 'general'

        condition = weather.get('condition', '')
        temperature = weather.get('temperature', 20)

        if '晴' in condition and temperature > 25:
            return 'entertainment'
        elif '雨' in condition:
            return 'study'
        elif '雪' in condition:
            return 'entertainment'
        else:
            return 'life'

    def format_weather_info(self, weather: Optional[Dict]) -> str:
        """
        格式化天气信息

        Args:
            weather: 天气信息

        Returns:
            格式化的天气信息
        """
        if not weather:
            return ""

        city = weather.get('city', '未知')
        temperature = weather.get('temperature', '未知')
        condition = weather.get('condition', '未知')

        return f"🌤️ 当前天气：{city} {condition} {temperature}°C"

# 创建全局实例
weather_detector = WeatherDetector()
