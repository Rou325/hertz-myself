#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索工具模块 - 支持多种搜索方式
预留 Tavily、Spotify 等接口
"""

import json
import os
import random
from typing import Dict, List, Optional
from datetime import datetime

class SearchTools:
    """搜索工具集合 - 支持多种搜索方式"""

    def __init__(self, config_dir: str = None):
        """
        初始化搜索工具

        Args:
            config_dir: 配置文件目录
        """
        self.config_dir = config_dir or os.path.join(
            os.path.dirname(__file__), '..', 'config'
        )
        self.config_file = os.path.join(self.config_dir, 'search_config.json')

        # 加载配置
        self.config = self._load_config()

        # 搜索历史
        self.search_history = []

    def _load_config(self) -> Dict:
        """加载搜索配置"""
        default_config = {
            'exa': {
                'enabled': False,
                'api_key': None,
                'priority': 1  # 优先级：1=最高
            },
            'tavily': {
                'enabled': False,
                'api_key': None,
                'priority': 2
            },
            'spotify': {
                'enabled': False,
                'client_id': None,
                'client_secret': None,
                'priority': 3
            },
            'browser': {
                'enabled': False,
                'type': 'playwright',  # playwright 或 puppeteer
                'priority': 4
            },
            'websearch': {
                'enabled': True,
                'priority': 5  # 默认方案
            },
            'first_run': True
        }

        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 合并默认配置
                    for key in default_config:
                        if key not in config:
                            config[key] = default_config[key]
                    return config
        except Exception as e:
            print(f"加载配置失败: {e}")

        return default_config

    def _save_config(self):
        """保存搜索配置"""
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")

    def is_first_run(self) -> bool:
        """是否首次运行"""
        return self.config.get('first_run', True)

    def mark_configured(self):
        """标记已配置"""
        self.config['first_run'] = False
        self._save_config()

    def setup_api_keys(self, api_keys: Dict) -> str:
        """
        设置 API 密钥

        Args:
            api_keys: API 密钥字典
                - exa_api_key: Exa API 密钥
                - tavily_api_key: Tavily API 密钥
                - spotify_client_id: Spotify Client ID
                - spotify_client_secret: Spotify Client Secret

        Returns:
            设置结果消息
        """
        results = []

        # 设置 Exa
        if 'exa_api_key' in api_keys and api_keys['exa_api_key']:
            self.config['exa']['api_key'] = api_keys['exa_api_key']
            self.config['exa']['enabled'] = True
            results.append("✅ Exa API 已配置")

        # 设置 Tavily
        if 'tavily_api_key' in api_keys and api_keys['tavily_api_key']:
            self.config['tavily']['api_key'] = api_keys['tavily_api_key']
            self.config['tavily']['enabled'] = True
            results.append("✅ Tavily API 已配置")

        # 设置 Spotify
        if 'spotify_client_id' in api_keys and 'spotify_client_secret' in api_keys:
            if api_keys['spotify_client_id'] and api_keys['spotify_client_secret']:
                self.config['spotify']['client_id'] = api_keys['spotify_client_id']
                self.config['spotify']['client_secret'] = api_keys['spotify_client_secret']
                self.config['spotify']['enabled'] = True
                results.append("✅ Spotify API 已配置")

        # 保存配置
        self._save_config()
        self.mark_configured()

        if not results:
            return "未配置任何 API，将使用默认 WebSearch 工具"

        return "\n".join(results)

    def get_setup_prompt(self) -> str:
        """
        获取首次配置提示（选项模式）

        Returns:
            配置提示文本
        """
        prompt = """
🎵 hertz-myself | 听见自己的频率 - 首次配置

欢迎使用 hertz-myself！为了提供更好的推荐体验，请选择配置：

## 第一步：选择配置方式

### 选项 1：使用默认配置（推荐新手）
- 使用 WebSearch 工具
- 完全免费，无需配置
- 立即开始使用

### 选项 2：配置 API（推荐进阶用户）
- 配置 Exa 或 Tavily API（AI 优化搜索，质量更高）
- 配置 Spotify API（专业音乐数据，注意国内服务器限制）
- 免费额度足够个人使用

### 选项 3：跳过配置
- 跳过本次配置
- 稍后可通过命令重新配置

请回复数字 1、2 或 3：

## API 说明

### Exa API（推荐）
- 用途：AI 优化的搜索引擎
- 获取：https://exa.ai
- 免费：每月 1000 次
- **国内友好**：✅ 可以在国内服务器使用

### Tavily API（推荐）
- 用途：AI 优化的搜索引擎
- 获取：https://tavily.com
- 免费：每月 1000 次
- **国内友好**：✅ 可以在国内服务器使用

### Spotify API（可选）
- 用途：专业音乐数据
- 获取：https://developer.spotify.com
- 免费：足够个人使用
- **国内友好**：❌ 在国内服务器可能无法访问
- **解决方案**：需要配置代理或 VPN
"""
        return prompt

    def get_trigger_time_prompt(self) -> str:
        """
        获取触发时间配置提示

        Returns:
            触发时间配置提示文本
        """
        prompt = """
## 第二步：设置推荐时间

请选择你希望何时收到 hertz-myself 的推荐：

### 选项 1：固定时间（推荐）
- 每天在指定时间自动推荐
- 例如：每天 18:00 推荐

### 选项 2：多个固定时间
- 每天在多个时间点推荐
- 例如：每天 8:00、12:00、18:00 各推荐一次

### 选项 3：随机时间
- 每天在随机时间推荐
- 增加惊喜感

### 选项 4：不设置定时
- 只在手动调用时推荐
- 适合使用外部 cron 工具的用户

请回复数字 1、2、3 或 4：

## 定时说明

### 固定时间
回复格式：`18:00` 或 `8:00,12:00,18:00`

### 随机时间
系统会在 8:00-22:00 之间随机选择时间

### 外部 cron 工具
如果你使用 openclaw、hermes 等机器人，可以使用它们自带的 cron 功能定时调用本技能。

示例 cron 配置：
```
# 每天 18:00 推荐
0 18 * * * /path/to/hertz-myself

# 每天 8:00 和 18:00 推荐
0 8,18 * * * /path/to/hertz-myself
```
"""
        return prompt

    def get_personality_prompt(self) -> str:
        """
        获取人格检测配置提示

        Returns:
            人格检测配置提示文本
        """
        prompt = """
## 第三步：选择语言风格

请选择推荐时的语言风格：

### 选项 1：使用默认语气
- 使用标准、友好的语气
- 适合大多数用户

### 选项 2：使用人格文件
- 使用你的人格文件（如 soul.md、personality.md 等）
- 套用人格语言风格
- 请提供人格文件的完整路径

请回复数字 1 或 2：

如果选择 2，请提供人格文件路径，例如：
`/path/to/your/soul.md`
"""
        return prompt

    def get_setup_options(self) -> Dict:
        """
        获取配置选项（用于交互式选择）

        Returns:
            配置选项字典
        """
        return {
            'options': [
                {
                    'id': '1',
                    'name': '使用默认配置',
                    'description': '使用 WebSearch 工具，完全免费，无需配置',
                    'action': 'use_default'
                },
                {
                    'id': '2',
                    'name': '配置 API',
                    'description': '配置 Exa、Tavily 或 Spotify API，获得更好的搜索体验',
                    'action': 'configure_api'
                },
                {
                    'id': '3',
                    'name': '跳过配置',
                    'description': '跳过本次配置，稍后可通过命令重新配置',
                    'action': 'skip'
                }
            ]
        }

    def get_api_options(self) -> Dict:
        """
        获取 API 选项（用于交互式选择）

        Returns:
            API 选项字典
        """
        return {
            'apis': [
                {
                    'id': 'exa',
                    'name': 'Exa API',
                    'description': 'AI 优化的搜索引擎，搜索质量高',
                    'url': 'https://exa.ai',
                    'free_limit': '每月 1000 次',
                    'priority': 1,
                    'fields': ['api_key'],
                    'region': 'global',  # 全球可用
                    'china_friendly': True  # 国内友好
                },
                {
                    'id': 'tavily',
                    'name': 'Tavily API',
                    'description': 'AI 优化的搜索引擎，搜索质量高',
                    'url': 'https://tavily.com',
                    'free_limit': '每月 1000 次',
                    'priority': 2,
                    'fields': ['api_key'],
                    'region': 'global',  # 全球可用
                    'china_friendly': True  # 国内友好
                },
                {
                    'id': 'spotify',
                    'name': 'Spotify API',
                    'description': '专业音乐数据，全球曲库覆盖（注意：在国内服务器可能无法访问）',
                    'url': 'https://developer.spotify.com',
                    'free_limit': '足够个人使用',
                    'priority': 3,
                    'fields': ['client_id', 'client_secret'],
                    'region': 'global',  # 全球可用
                    'china_friendly': False,  # 国内不友好
                    'warning': '在国内服务器可能无法访问，需要代理或VPN'
                }
            ]
        }

    def process_setup_choice(self, choice: str) -> Dict:
        """
        处理配置选择

        Args:
            choice: 用户选择（1/2/3）

        Returns:
            处理结果
        """
        if choice == '1':
            # 使用默认配置，进入触发时间配置
            return {
                'action': 'configure_trigger_time',
                'message': '✅ 已选择默认配置，请设置推荐时间：',
                'prompt': self.get_trigger_time_prompt()
            }
        elif choice == '2':
            # 配置 API
            return {
                'action': 'configure_api',
                'message': '请提供 API 配置：',
                'options': self.get_api_options()
            }
        elif choice == '3':
            # 跳过配置
            self.mark_configured()
            return {
                'action': 'skip',
                'message': '已跳过配置，可以稍后通过命令重新配置。'
            }
        else:
            return {
                'action': 'error',
                'message': '无效选择，请输入 1、2 或 3'
            }

    def process_trigger_time_choice(self, choice: str, time_input: str = None) -> Dict:
        """
        处理触发时间选择

        Args:
            choice: 用户选择（1/2/3/4）
            time_input: 用户输入的时间

        Returns:
            处理结果
        """
        if choice in ['1', '2']:
            # 固定时间或多个固定时间
            if time_input:
                try:
                    times = [t.strip() for t in time_input.split(',')]
                    valid_times = []
                    for t in times:
                        datetime.strptime(t, '%H:%M')
                        valid_times.append(t)
                    self.mark_configured()
                    return {
                        'action': 'set_trigger_times',
                        'times': valid_times,
                        'message': f'✅ 已设置推荐时间：{", ".join(valid_times)}'
                    }
                except ValueError:
                    return {
                        'action': 'error',
                        'message': '❌ 时间格式错误，请使用 HH:MM 格式，例如：18:00 或 8:00,12:00,18:00'
                    }
            else:
                return {
                    'action': 'error',
                    'message': '❌ 请输入时间，例如：18:00 或 8:00,12:00,18:00'
                }
        elif choice == '3':
            # 随机时间
            self.mark_configured()
            return {
                'action': 'set_random_trigger',
                'message': '✅ 已设置随机推荐时间（8:00-22:00 之间）'
            }
        elif choice == '4':
            # 不设置定时，进入人格检测配置
            return {
                'action': 'configure_personality',
                'message': '✅ 已跳过定时设置，请选择语言风格：',
                'prompt': self.get_personality_prompt()
            }
        else:
            return {
                'action': 'error',
                'message': '无效选择，请输入 1、2、3 或 4'
            }

    def process_personality_choice(self, choice: str, file_path: str = None) -> Dict:
        """
        处理人格检测选择

        Args:
            choice: 用户选择（1/2）
            file_path: 人格文件路径（选择 2 时需要）

        Returns:
            处理结果
        """
        if choice == '1':
            # 使用默认语气
            self.mark_configured()
            return {
                'action': 'use_default_personality',
                'message': '✅ 已选择使用默认语气'
            }
        elif choice == '2':
            # 使用人格文件
            if file_path:
                # 检查文件是否存在
                if os.path.exists(file_path):
                    self.mark_configured()
                    return {
                        'action': 'use_personality_file',
                        'file_path': file_path,
                        'message': f'✅ 已选择使用人格文件：{file_path}'
                    }
                else:
                    return {
                        'action': 'error',
                        'message': f'❌ 文件不存在：{file_path}'
                    }
            else:
                return {
                    'action': 'error',
                    'message': '❌ 请提供人格文件路径，例如：/path/to/your/soul.md'
                }
        else:
            return {
                'action': 'error',
                'message': '无效选择，请输入 1 或 2'
            }

    def process_api_config(self, api_id: str, config: Dict) -> str:
        """
        处理 API 配置

        Args:
            api_id: API ID（exa/tavily/spotify）
            config: 配置信息

        Returns:
            配置结果消息
        """
        if api_id == 'exa':
            if 'api_key' in config and config['api_key']:
                self.config['exa']['api_key'] = config['api_key']
                self.config['exa']['enabled'] = True
                self._save_config()
                self.mark_configured()
                return "✅ Exa API 已配置成功！"
            else:
                return "❌ 请提供有效的 Exa API 密钥"

        elif api_id == 'tavily':
            if 'api_key' in config and config['api_key']:
                self.config['tavily']['api_key'] = config['api_key']
                self.config['tavily']['enabled'] = True
                self._save_config()
                self.mark_configured()
                return "✅ Tavily API 已配置成功！"
            else:
                return "❌ 请提供有效的 Tavily API 密钥"

        elif api_id == 'spotify':
            if 'client_id' in config and 'client_secret' in config:
                if config['client_id'] and config['client_secret']:
                    self.config['spotify']['client_id'] = config['client_id']
                    self.config['spotify']['client_secret'] = config['client_secret']
                    self.config['spotify']['enabled'] = True
                    self._save_config()
                    self.mark_configured()
                    return "✅ Spotify API 已配置成功！"
                else:
                    return "❌ 请提供有效的 Spotify Client ID 和 Client Secret"
            else:
                return "❌ 请提供 Spotify Client ID 和 Client Secret"

        else:
            return f"❌ 未知的 API: {api_id}"

    def get_available_methods(self) -> List[str]:
        """获取可用的搜索方法"""
        methods = []

        if self.config['exa']['enabled'] and self.config['exa']['api_key']:
            methods.append('exa')

        if self.config['tavily']['enabled'] and self.config['tavily']['api_key']:
            methods.append('tavily')

        if self.config['spotify']['enabled']:
            methods.append('spotify')

        if self.config['browser']['enabled']:
            methods.append('browser')

        if self.config['websearch']['enabled']:
            methods.append('websearch')

        return methods

    def get_best_method(self) -> str:
        """获取最佳搜索方法"""
        methods = self.get_available_methods()

        if not methods:
            return 'websearch'  # 默认

        # 按优先级排序
        priority_map = {
            'exa': self.config['exa']['priority'],
            'tavily': self.config['tavily']['priority'],
            'spotify': self.config['spotify']['priority'],
            'browser': self.config['browser']['priority'],
            'websearch': self.config['websearch']['priority']
        }

        # 返回优先级最高的方法
        return min(methods, key=lambda m: priority_map.get(m, 999))

    def generate_search_queries(self, mood_analysis: Dict, diversity_level: int = 3) -> List[Dict]:
        """
        生成多样化的搜索查询

        Args:
            mood_analysis: 情绪分析结果
            diversity_level: 多样性等级 (1-5)

        Returns:
            搜索查询列表
        """
        mood = mood_analysis.get('mood', 'neutral')
        theme = mood_analysis.get('theme', 'general')

        queries = []

        # 基础搜索查询
        base_queries = self._get_base_queries(mood, theme)
        queries.extend(base_queries)

        # 多样化搜索查询
        if diversity_level >= 2:
            diverse_queries = self._get_diverse_queries(mood, theme)
            queries.extend(diverse_queries)

        if diversity_level >= 3:
            genre_queries = self._get_genre_queries(mood)
            queries.extend(genre_queries)

        if diversity_level >= 4:
            era_queries = self._get_era_queries()
            queries.extend(era_queries)

        if diversity_level >= 5:
            random_queries = self._get_random_queries()
            queries.extend(random_queries)

        # 去重并限制数量
        unique_queries = self._deduplicate_queries(queries)
        return unique_queries[:10]

    def _get_base_queries(self, mood: str, theme: str) -> List[Dict]:
        """获取基础搜索查询"""
        queries = []

        mood_map = {
            'positive': ['快乐', '开心', '阳光', '活力', '励志'],
            'negative': ['悲伤', '忧郁', '治愈', '安静', '深沉'],
            'neutral': ['平静', '舒适', '放松', '轻柔', '温柔']
        }

        theme_map = {
            'work': ['工作', '奋斗', '职场', '加班', '通勤'],
            'life': ['生活', '日常', '平凡', '简单', '幸福'],
            'study': ['学习', '成长', '青春', '校园', '考试'],
            'entertainment': ['娱乐', '放松', '电影', '旅行', '咖啡'],
            'love': ['爱情', '恋爱', '暗恋', '分手', '思念'],
            'technology': ['科技', '未来', '电子', '数字', '编程'],
            'general': ['日常', '普通', '平凡', '简单', '自然']
        }

        mood_keywords = mood_map.get(mood, mood_map['neutral'])
        theme_keywords = theme_map.get(theme, theme_map['general'])

        for mood_word in mood_keywords[:2]:
            for theme_word in theme_keywords[:2]:
                queries.append({
                    'query': f"{mood_word} {theme_word} 音乐",
                    'type': 'mood_theme',
                    'priority': 1
                })

        return queries

    def _get_diverse_queries(self, mood: str, theme: str) -> List[Dict]:
        """获取多样化搜索查询"""
        queries = []

        styles = [
            '民谣', '摇滚', '电子', '古典', '爵士',
            'R&B', '嘻哈', '轻音乐', '后摇', '氛围'
        ]

        selected_styles = random.sample(styles, min(3, len(styles)))

        for style in selected_styles:
            queries.append({
                'query': f"{style} 音乐 推荐",
                'type': 'style',
                'priority': 2
            })

        return queries

    def _get_genre_queries(self, mood: str) -> List[Dict]:
        """获取流派相关查询"""
        queries = []

        if mood == 'positive':
            genres = ['励志摇滚', '轻快民谣', '电子舞曲', '流行金曲']
        elif mood == 'negative':
            genres = ['治愈系', '安静钢琴', '后摇', '氛围音乐']
        else:
            genres = ['独立音乐', '小众佳作', '文艺民谣', '爵士蓝调']

        for genre in genres:
            queries.append({
                'query': f"{genre} 推荐",
                'type': 'genre',
                'priority': 3
            })

        return queries

    def _get_era_queries(self) -> List[Dict]:
        """获取年代相关查询"""
        queries = []

        eras = ['90年代', '2000年代', '2010年代', '2020年代']
        selected_eras = random.sample(eras, min(2, len(eras)))

        for era in selected_eras:
            queries.append({
                'query': f"{era} 经典歌曲",
                'type': 'era',
                'priority': 4
            })

        return queries

    def _get_random_queries(self) -> List[Dict]:
        """获取随机查询"""
        queries = []

        random_topics = [
            '被低估的歌曲', '冷门宝藏', '独立音乐人',
            '现场演出常客', '音乐节常客', '乐评人推荐',
            '歌词有深度', '旋律有特色', '编曲精良'
        ]

        selected_topics = random.sample(random_topics, min(2, len(random_topics)))

        for topic in selected_topics:
            queries.append({
                'query': f"{topic} 推荐",
                'type': 'random',
                'priority': 5
            })

        return queries

    def _deduplicate_queries(self, queries: List[Dict]) -> List[Dict]:
        """去重查询"""
        seen = set()
        unique_queries = []

        for query in queries:
            query_text = query['query']
            if query_text not in seen:
                seen.add(query_text)
                unique_queries.append(query)

        return unique_queries

    def format_search_tool_prompt(self, queries: List[Dict]) -> str:
        """
        格式化搜索工具提示

        Args:
            queries: 搜索查询列表

        Returns:
            格式化的提示文本
        """
        best_method = self.get_best_method()
        available_methods = self.get_available_methods()

        prompt = f"""
🔍 搜索工具使用指南

## 当前搜索方式
**推荐使用**: {best_method.upper()}
**可用方式**: {', '.join([m.upper() for m in available_methods])}

## 搜索查询建议

请尝试以下搜索查询：

"""
        for i, query in enumerate(queries, 1):
            prompt += f"""
{i}. **{query['type'].upper()}**
   查询：{query['query']}
   优先级：{'⭐' * (6 - query['priority'])}
"""

        prompt += """
## 搜索策略

1. **多样性**：尝试不同类型的查询
2. **随机性**：每次使用不同的查询组合
3. **过滤**：排除抖音热歌、口水歌
4. **质量**：优先推荐独立音乐、小众佳作

## 输出格式

搜索后，请输出以下格式的歌曲信息：

```json
{
  "name": "歌曲名称",
  "artist": "歌手名称",
  "album": "专辑名称",
  "genre": "风格",
  "release_date": "发行时间",
  "language": "语言",
  "link": "收听链接",
  "reason": "推荐理由",
  "artist_intro": "歌手简介",
  "tags": ["标签1", "标签2"]
}
```

## 注意事项

- 不要推荐抖音热歌、网络神曲
- 不要推荐过于口水的歌曲
- 可以推荐冷门小众但优质的歌曲
- 随机性要强，每次都要不同
- 考虑当前时间和用户心情
"""
        return prompt

    def record_search(self, query: str, results: List[Dict], method: str = 'websearch'):
        """记录搜索历史"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'results_count': len(results),
            'method': method
        }
        self.search_history.append(record)

    def get_search_statistics(self) -> Dict:
        """获取搜索统计"""
        if not self.search_history:
            return {'total_searches': 0}

        total = len(self.search_history)
        queries = [r['query'] for r in self.search_history]

        # 统计搜索方法
        method_counts = {}
        for record in self.search_history:
            method = record.get('method', 'unknown')
            method_counts[method] = method_counts.get(method, 0) + 1

        return {
            'total_searches': total,
            'unique_queries': len(set(queries)),
            'method_distribution': method_counts,
            'last_search': self.search_history[-1]['timestamp']
        }

# 创建全局实例
search_tools = SearchTools()
