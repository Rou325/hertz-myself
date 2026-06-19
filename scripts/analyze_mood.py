#!/usr/bin/env python3
"""
分析对话情绪和主题
支持集成天气信息
"""

import re
from typing import Dict, List, Tuple, Optional
from collections import Counter

class MoodAnalyzer:
    """对话情绪分析器"""

    # 情绪关键词映射
    MOOD_KEYWORDS = {
        'positive': [
            '开心', '高兴', '快乐', '太好了', '棒', '赞', '喜欢', '爱',
            'happy', 'great', 'awesome', 'love', 'wonderful', 'excellent',
            '好', '不错', '可以', '行', '没问题', '解决了', '成功'
        ],
        'negative': [
            '难过', '伤心', '烦', '累', '讨厌', '无聊', '郁闷', '焦虑',
            'sad', 'tired', 'bored', 'angry', 'frustrated', 'depressed',
            '不好', '不行', '失败', '问题', '错误', 'bug', '困难'
        ],
        'neutral': [
            '一般', '还行', '普通', '正常', '平常',
            'normal', 'ok', 'fine', 'usual'
        ]
    }

    # 主题关键词映射
    THEME_KEYWORDS = {
        'work': [
            '工作', '代码', '编程', '项目', '任务', '会议', '报告',
            'work', 'code', 'programming', 'project', 'task', 'meeting'
        ],
        'life': [
            '生活', '吃饭', '睡觉', '休息', '周末', '假期', '旅行',
            'life', 'eat', 'sleep', 'rest', 'weekend', 'holiday', 'travel'
        ],
        'study': [
            '学习', '看书', '课程', '知识', '技能', '考试',
            'study', 'learn', 'course', 'knowledge', 'skill', 'exam'
        ],
        'entertainment': [
            '电影', '音乐', '游戏', '综艺', '娱乐', '放松',
            'movie', 'music', 'game', 'entertainment', 'relax'
        ],
        'technology': [
            '技术', 'AI', '人工智能', '编程', '开发', '软件',
            'technology', 'AI', 'development', 'software'
        ]
    }

    def __init__(self):
        """初始化分析器"""
        pass

    def analyze(self, conversations: List[Dict], weather: Optional[Dict] = None) -> Dict:
        """
        分析对话内容

        Args:
            conversations: 对话历史列表
            weather: 天气信息（可选）

        Returns:
            分析结果，包含：
            - mood: 情绪类型（positive/negative/neutral）
            - mood_score: 情绪分数（-1 到 1）
            - theme: 主题类型
            - keywords: 关键词列表
            - summary: 对话摘要
            - weather: 天气信息（如果有）
        """
        if not conversations:
            return self._default_result()

        # 提取所有对话内容
        contents = [msg['content'] for msg in conversations if 'content' in msg]
        all_text = ' '.join(contents)

        # 分析情绪
        mood, mood_score = self._analyze_mood(all_text)

        # 分析主题
        theme = self._analyze_theme(all_text)

        # 提取关键词
        keywords = self._extract_keywords(all_text)

        # 生成摘要
        summary = self._generate_summary(conversations, mood, theme)

        # 如果有天气信息，调整情绪和主题
        if weather:
            weather_mood = self._get_weather_mood(weather)
            weather_theme = self._get_weather_theme(weather)

            # 根据天气调整情绪（权重 30%）
            if weather_mood != mood:
                mood = self._blend_moods(mood, weather_mood, 0.7)

            # 根据天气调整主题（权重 20%）
            if weather_theme != theme:
                theme = self._blend_themes(theme, weather_theme, 0.8)

        result = {
            'mood': mood,
            'mood_score': mood_score,
            'theme': theme,
            'keywords': keywords,
            'summary': summary
        }

        # 如果有天气信息，添加到结果中
        if weather:
            result['weather'] = weather
            result['weather_info'] = self._format_weather_info(weather)

        return result

    def _get_weather_mood(self, weather: Dict) -> str:
        """
        根据天气获取情绪

        Args:
            weather: 天气信息

        Returns:
            情绪类型
        """
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

    def _get_weather_theme(self, weather: Dict) -> str:
        """
        根据天气获取主题

        Args:
            weather: 天气信息

        Returns:
            主题类型
        """
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

    def _blend_moods(self, mood1: str, mood2: str, weight1: float) -> str:
        """
        混合两种情绪

        Args:
            mood1: 情绪1
            mood2: 情绪2
            weight1: 情绪1的权重

        Returns:
            混合后的情绪
        """
        # 简单实现：返回权重更高的情绪
        if weight1 > 0.5:
            return mood1
        else:
            return mood2

    def _blend_themes(self, theme1: str, theme2: str, weight1: float) -> str:
        """
        混合两种主题

        Args:
            theme1: 主题1
            theme2: 主题2
            weight1: 主题1的权重

        Returns:
            混合后的主题
        """
        # 简单实现：返回权重更高的主题
        if weight1 > 0.5:
            return theme1
        else:
            return theme2

    def _format_weather_info(self, weather: Dict) -> str:
        """
        格式化天气信息

        Args:
            weather: 天气信息

        Returns:
            格式化的天气信息
        """
        city = weather.get('city', '未知')
        temperature = weather.get('temperature', '未知')
        condition = weather.get('condition', '未知')

        return f"🌤️ 当前天气：{city} {condition} {temperature}°C"

    def _analyze_mood(self, text: str) -> Tuple[str, float]:
        """
        分析情绪

        Args:
            text: 对话文本

        Returns:
            (情绪类型, 情绪分数)
        """
        text_lower = text.lower()

        positive_count = 0
        negative_count = 0
        neutral_count = 0

        # 统计各类情绪词出现次数
        for word in self.MOOD_KEYWORDS['positive']:
            if word in text_lower:
                positive_count += 1

        for word in self.MOOD_KEYWORDS['negative']:
            if word in text_lower:
                negative_count += 1

        for word in self.MOOD_KEYWORDS['neutral']:
            if word in text_lower:
                neutral_count += 1

        total = positive_count + negative_count + neutral_count

        if total == 0:
            return 'neutral', 0.0

        # 计算情绪分数
        mood_score = (positive_count - negative_count) / total

        # 确定情绪类型
        if mood_score > 0.2:
            mood = 'positive'
        elif mood_score < -0.2:
            mood = 'negative'
        else:
            mood = 'neutral'

        return mood, mood_score

    def _analyze_theme(self, text: str) -> str:
        """
        分析主题

        Args:
            text: 对话文本

        Returns:
            主题类型
        """
        text_lower = text.lower()
        theme_scores = {}

        for theme, keywords in self.THEME_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            theme_scores[theme] = score

        if not theme_scores or max(theme_scores.values()) == 0:
            return 'general'

        return max(theme_scores, key=theme_scores.get)

    def _extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """
        提取关键词

        Args:
            text: 对话文本
            top_n: 返回前 N 个关键词

        Returns:
            关键词列表
        """
        # 简单的分词（实际应使用更复杂的分词工具）
        words = re.findall(r'[一-龥]+|[a-zA-Z]+', text)

        # 过滤停用词
        stopwords = {'的', '了', '是', '在', '我', '你', '他', '她', '它',
                     'the', 'a', 'an', 'is', 'are', 'was', 'were', 'i', 'you'}
        words = [w for w in words if w not in stopwords and len(w) > 1]

        # 统计词频
        word_counts = Counter(words)

        # 返回前 N 个关键词
        return [word for word, count in word_counts.most_common(top_n)]

    def _generate_summary(self, conversations: List[Dict], mood: str, theme: str) -> str:
        """
        生成对话摘要

        Args:
            conversations: 对话历史
            mood: 情绪类型
            theme: 主题类型

        Returns:
            摘要文本
        """
        mood_map = {
            'positive': '积极向上',
            'negative': '有些低落',
            'neutral': '平稳正常'
        }

        theme_map = {
            'work': '工作相关',
            'life': '生活日常',
            'study': '学习充电',
            'entertainment': '娱乐放松',
            'technology': '技术讨论',
            'general': '日常交流'
        }

        mood_desc = mood_map.get(mood, '未知')
        theme_desc = theme_map.get(theme, '未知')

        return f"今日心情{mood_desc}，主要话题为{theme_desc}"

    def _default_result(self) -> Dict:
        """返回默认结果"""
        return {
            'mood': 'neutral',
            'mood_score': 0.0,
            'theme': 'general',
            'keywords': [],
            'summary': '暂无对话记录'
        }

def analyze_conversation_mood(conversations: List[Dict], weather: Optional[Dict] = None) -> Dict:
    """
    便捷函数：分析对话情绪

    Args:
        conversations: 对话历史列表
        weather: 天气信息（可选）

    Returns:
        分析结果
    """
    analyzer = MoodAnalyzer()
    return analyzer.analyze(conversations, weather)

if __name__ == '__main__':
    # 测试分析
    test_conversations = [
        {"timestamp": "2026-06-13T09:00:00", "role": "user", "content": "今天天气真好，心情不错"},
        {"timestamp": "2026-06-13T10:30:00", "role": "user", "content": "在写代码，遇到一个 bug，有点烦"},
        {"timestamp": "2026-06-13T14:00:00", "role": "user", "content": "终于解决了！开心"}
    ]

    result = analyze_conversation_mood(test_conversations)
    print(f"情绪: {result['mood']}")
    print(f"情绪分数: {result['mood_score']}")
    print(f"主题: {result['theme']}")
    print(f"关键词: {result['keywords']}")
    print(f"摘要: {result['summary']}")
