#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天气检测模块
检测是否有天气 skill，有就调用，没有就返回 None（AI 会用 WebSearch 代替）
"""

import json
import os
import subprocess
from typing import Dict, Optional


class WeatherDetector:
    """天气检测器"""

    def __init__(self):
        self.cached_weather = None

    def has_weather_skill(self) -> bool:
        """检测系统是否有天气 skill"""
        # 检查 ~/.claude/skills 下是否有天气相关的 skill
        skill_dirs = [
            os.path.expanduser('~/.claude/skills'),
            os.path.expanduser('~/.config/claude/skills'),
        ]
        weather_names = ['weather', '天气', 'get-weather']
        for sd in skill_dirs:
            if os.path.exists(sd):
                for name in weather_names:
                    if os.path.exists(os.path.join(sd, name)):
                        return True
        return False

    def get_weather(self, city: str = None) -> Optional[Dict]:
        """
        调用天气 skill 获取天气

        Args:
            city: 城市名（可选）

        Returns:
            天气信息字典，获取失败则返回 None
        """
        if not self.has_weather_skill():
            return None
        try:
            cmd = ['weather']
            if city:
                cmd.append(city)
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return self._parse_output(result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        return None

    def _parse_output(self, output: str) -> Dict:
        """解析天气命令输出"""
        weather = {
            'city': '未知', 'temperature': 20,
            'condition': '晴', 'description': output.strip()
        }
        for line in output.strip().split('\n'):
            if '°C' in line or '度' in line:
                try:
                    digits = ''.join(filter(str.isdigit, line.split('°')[0].split('度')[0]))
                    if digits:
                        weather['temperature'] = int(digits)
                except:
                    pass
        return weather


# 全局实例
weather_detector = WeatherDetector()
