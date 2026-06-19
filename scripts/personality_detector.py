#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人格文件读取模块
读取用户指定的人格文件，AI 负责套用语言风格
"""

import os
from typing import Dict, Optional


class PersonalityDetector:
    """人格文件读取器"""

    def __init__(self):
        self.personality_cache = None

    def has_personality(self) -> bool:
        return self.personality_cache is not None

    def get_personality(self) -> Optional[Dict]:
        return self.personality_cache

    def load_personality_from_file(self, file_path: str) -> Optional[Dict]:
        try:
            if not os.path.exists(file_path):
                return None
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            personality = {
                'file': file_path,
                'content': content,
            }
            self.personality_cache = personality
            return personality
        except Exception:
            return None


# 全局实例
personality_detector = PersonalityDetector()
