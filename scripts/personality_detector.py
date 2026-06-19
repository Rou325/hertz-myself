#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人格文件读取模块
读取用户指定的人格文件，套用语言风格
"""

import os
import json
from typing import Dict, Optional

class PersonalityDetector:
    """人格文件读取器"""

    def __init__(self):
        """初始化人格文件读取器"""
        self.personality_cache = None

    def has_personality(self) -> bool:
        """
        检查是否已加载人格文件

        Returns:
            是否已加载人格文件
        """
        return self.personality_cache is not None

    def get_personality(self) -> Optional[Dict]:
        """
        获取人格信息

        Returns:
            人格信息字典，如果没有人格文件则返回 None
        """
        return self.personality_cache

    def load_personality_from_file(self, file_path: str) -> Optional[Dict]:
        """
        从文件加载人格信息

        Args:
            file_path: 人格文件路径

        Returns:
            人格信息字典，如果加载失败则返回 None
        """
        try:
            if not os.path.exists(file_path):
                print(f"文件不存在：{file_path}")
                return None

            personality = self._load_personality(file_path)
            if personality:
                self.personality_cache = personality
                return personality
        except Exception as e:
            print(f"加载人格文件失败: {e}")

        return None

    def _load_personality(self, file_path: str) -> Optional[Dict]:
        """
        加载人格文件

        Args:
            file_path: 人格文件路径

        Returns:
            人格信息字典
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 解析人格文件
            personality = {
                'file': file_path,
                'content': content,
                'style': self._extract_style(content),
                'tone': self._extract_tone(content),
                'vocabulary': self._extract_vocabulary(content)
            }

            return personality
        except Exception as e:
            print(f"读取人格文件失败: {e}")
            return None

    def _extract_style(self, content: str) -> str:
        """
        提取语言风格

        Args:
            content: 人格文件内容

        Returns:
            语言风格
        """
        # 简单的风格提取
        if '可爱' in content or '萌' in content:
            return 'cute'
        elif '严肃' in content or '正式' in content:
            return 'formal'
        elif '幽默' in content or '搞笑' in content:
            return 'humorous'
        elif '温柔' in content or '亲切' in content:
            return 'gentle'
        else:
            return 'neutral'

    def _extract_tone(self, content: str) -> str:
        """
        提取语调

        Args:
            content: 人格文件内容

        Returns:
            语调
        """
        # 简单的语调提取
        if '活泼' in content or '热情' in content:
            return 'enthusiastic'
        elif '冷静' in content or '理性' in content:
            return 'calm'
        elif '温暖' in content or '友好' in content:
            return 'warm'
        else:
            return 'neutral'

    def _extract_vocabulary(self, content: str) -> list:
        """
        提取词汇偏好

        Args:
            content: 人格文件内容

        Returns:
            词汇偏好列表
        """
        # 简单的词汇提取
        vocabulary = []

        if '可爱' in content:
            vocabulary.extend(['呢', '呀', '啦', '哦'])
        if '幽默' in content:
            vocabulary.extend(['哈哈', '嘿嘿', '哎呀'])
        if '温柔' in content:
            vocabulary.extend(['亲爱的', '宝贝', '小心肝'])

        return vocabulary

    def apply_personality(self, text: str) -> str:
        """
        应用人格风格到文本

        Args:
            text: 原始文本

        Returns:
            应用人格风格后的文本
        """
        personality = self.get_personality()

        if not personality:
            return text

        style = personality.get('style', 'neutral')
        tone = personality.get('tone', 'neutral')
        vocabulary = personality.get('vocabulary', [])

        # 根据风格调整文本
        if style == 'cute':
            text = self._apply_cute_style(text, vocabulary)
        elif style == 'formal':
            text = self._apply_formal_style(text)
        elif style == 'humorous':
            text = self._apply_humorous_style(text, vocabulary)
        elif style == 'gentle':
            text = self._apply_gentle_style(text, vocabulary)

        return text

    def _apply_cute_style(self, text: str, vocabulary: list) -> str:
        """
        应用可爱风格

        Args:
            text: 原始文本
            vocabulary: 词汇偏好

        Returns:
            可爱风格的文本
        """
        # 添加可爱的后缀
        if vocabulary:
            suffix = vocabulary[0]
            text = text.rstrip('。！？') + suffix

        return text

    def _apply_formal_style(self, text: str) -> str:
        """
        应用正式风格

        Args:
            text: 原始文本

        Returns:
            正式风格的文本
        """
        # 保持正式风格
        return text

    def _apply_humorous_style(self, text: str, vocabulary: list) -> str:
        """
        应用幽默风格

        Args:
            text: 原始文本
            vocabulary: 词汇偏好

        Returns:
            幽默风格的文本
        """
        # 添加幽默元素
        if vocabulary:
            prefix = vocabulary[0]
            text = prefix + '，' + text

        return text

    def _apply_gentle_style(self, text: str, vocabulary: list) -> str:
        """
        应用温柔风格

        Args:
            text: 原始文本
            vocabulary: 词汇偏好

        Returns:
            温柔风格的文本
        """
        # 添加温柔元素
        if vocabulary:
            suffix = vocabulary[0]
            text = text.rstrip('。！？') + '，' + suffix

        return text

# 创建全局实例
personality_detector = PersonalityDetector()
