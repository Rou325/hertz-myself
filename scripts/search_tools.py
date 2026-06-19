#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索工具模块 - 管理搜索配置，执行搜索
AI 负责生成搜索词，脚本负责调用 API
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class SearchTools:
    """搜索工具集合 - 配置管理 + API 调用"""

    def __init__(self, config_dir: str = None):
        self.config_dir = config_dir or os.path.join(
            os.path.dirname(__file__), '..', 'config'
        )
        self.config_file = os.path.join(self.config_dir, 'search_config.json')
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        default_config = {
            'exa': {'enabled': False, 'api_key': None, 'priority': 1},
            'tavily': {'enabled': False, 'api_key': None, 'priority': 2},
            'spotify': {'enabled': False, 'client_id': None, 'client_secret': None, 'priority': 3},
            'websearch': {'enabled': True, 'priority': 5},
            'first_run': True
        }
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    for key in default_config:
                        if key not in config:
                            config[key] = default_config[key]
                    return config
        except Exception:
            pass
        return default_config

    def _save_config(self):
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def is_first_run(self) -> bool:
        return self.config.get('first_run', True)

    def mark_configured(self):
        self.config['first_run'] = False
        self._save_config()

    def setup_api_keys(self, api_keys: Dict) -> str:
        results = []
        if 'exa_api_key' in api_keys and api_keys['exa_api_key']:
            self.config['exa']['api_key'] = api_keys['exa_api_key']
            self.config['exa']['enabled'] = True
            results.append("✅ Exa API 已配置")
        if 'tavily_api_key' in api_keys and api_keys['tavily_api_key']:
            self.config['tavily']['api_key'] = api_keys['tavily_api_key']
            self.config['tavily']['enabled'] = True
            results.append("✅ Tavily API 已配置")
        if 'spotify_client_id' in api_keys and 'spotify_client_secret' in api_keys:
            if api_keys['spotify_client_id'] and api_keys['spotify_client_secret']:
                self.config['spotify']['client_id'] = api_keys['spotify_client_id']
                self.config['spotify']['client_secret'] = api_keys['spotify_client_secret']
                self.config['spotify']['enabled'] = True
                results.append("✅ Spotify API 已配置")
        self._save_config()
        self.mark_configured()
        return "\n".join(results) if results else "未配置任何 API，将使用默认 WebSearch 工具"

    def process_api_config(self, api_id: str, config: Dict) -> str:
        if api_id == 'exa':
            if 'api_key' in config and config['api_key']:
                self.config['exa']['api_key'] = config['api_key']
                self.config['exa']['enabled'] = True
                self._save_config()
                self.mark_configured()
                return "✅ Exa API 已配置成功！"
            return "❌ 请提供有效的 Exa API 密钥"
        elif api_id == 'tavily':
            if 'api_key' in config and config['api_key']:
                self.config['tavily']['api_key'] = config['api_key']
                self.config['tavily']['enabled'] = True
                self._save_config()
                self.mark_configured()
                return "✅ Tavily API 已配置成功！"
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
                return "❌ 请提供有效的 Spotify Client ID 和 Client Secret"
            return "❌ 请提供 Spotify Client ID 和 Client Secret"
        return f"❌ 未知的 API: {api_id}"

    def get_setup_prompt(self) -> str:
        return """
🎵 hertz-myself | 听见自己的频率 - 首次配置

欢迎使用 hertz-myself！请选择配置方式：

## 选项 1：使用默认配置（推荐新手）
- 使用 WebSearch 工具，完全免费
- 无需配置，立即使用

## 选项 2：配置 API（推荐进阶用户）
- 使用 Exa/Tavily API 获得更好的搜索效果
- 免费额度足够个人使用

## 选项 3：跳过配置
- 稍后可通过命令重新配置

请回复数字 1、2 或 3：

## API 说明

### Exa API（推荐）
- AI 优化的搜索引擎
- 获取：https://exa.ai
- 免费：每月 1000 次
- **国内友好**：✅

### Tavily API（推荐）
- AI 优化的搜索引擎
- 获取：https://tavily.com
- 免费：每月 1000 次
- **国内友好**：✅

### Spotify API（可选）
- 专业音乐数据
- 获取：https://developer.spotify.com
- **国内友好**：❌ 需代理
"""

    def get_trigger_time_prompt(self) -> str:
        return """
## 第二步：设置推荐时间

请选择推荐方式：

### 选项 1：固定时间（推荐）
每天固定时间自动推荐，如 18:00

### 选项 2：多个固定时间
每天多个时间点推荐，如 8:00、12:00、18:00

### 选项 3：随机时间
在时间窗口内随机选时间推荐，每天都有惊喜

### 选项 4：不设置定时
只在手动调用时推荐

请回复数字 1、2、3 或 4：
"""

    def get_random_time_config_prompt(self) -> str:
        return """
## 随机时间配置

请输入配置，格式：次数,开始时间,结束时间

示例：
- `1,09:00,21:00` → 每天 9:00-21:00 之间随机 1 次
- `2,10:00,20:00` → 每天 10:00-20:00 之间随机 2 次
- `3,08:00,22:00` → 每天 8:00-22:00 之间随机 3 次

不输入直接回车 = 默认：1次，9:00-21:00
"""

    def get_personality_prompt(self) -> str:
        return """
## 第三步：选择语言风格

### 选项 1：使用默认语气
标准、友好的语气

### 选项 2：使用人格文件
套用 soul.md、personality.md 等文件的语言风格

请回复数字 1 或 2：
"""

    def get_setup_options(self) -> Dict:
        return {
            'options': [
                {'id': '1', 'name': '使用默认配置', 'description': '使用 WebSearch 工具，完全免费', 'action': 'use_default'},
                {'id': '2', 'name': '配置 API', 'description': '配置 Exa/Tavily/Spotify API', 'action': 'configure_api'},
                {'id': '3', 'name': '跳过配置', 'description': '稍后可通过命令重新配置', 'action': 'skip'}
            ]
        }

    def process_setup_choice(self, choice: str) -> Dict:
        if choice == '1':
            return {'action': 'configure_trigger_time', 'message': '✅ 已选择默认配置，请设置推荐时间：', 'prompt': self.get_trigger_time_prompt()}
        elif choice == '2':
            return {'action': 'configure_api', 'message': '请提供 API 配置：'}
        elif choice == '3':
            self.mark_configured()
            return {'action': 'skip', 'message': '已跳过配置'}
        return {'action': 'error', 'message': '无效选择'}

    def process_trigger_time_choice(self, choice: str, time_input: str = None) -> Dict:
        if choice in ['1', '2']:
            if time_input:
                try:
                    times = [t.strip() for t in time_input.split(',')]
                    for t in times:
                        datetime.strptime(t, '%H:%M')
                    self.mark_configured()
                    return {'action': 'set_trigger_times', 'times': times, 'message': f'✅ 已设置：{", ".join(times)}'}
                except ValueError:
                    return {'action': 'error', 'message': '❌ 时间格式错误，请使用 HH:MM'}
            return {'action': 'error', 'message': '❌ 请输入时间（HH:MM 格式，多个用逗号分隔）'}
        elif choice == '3':
            # 解析随机时间输入：次数,开始,结束  例如 "2,09:00,21:00"
            if time_input:
                try:
                    parts = [p.strip() for p in time_input.split(',')]
                    count = int(parts[0]) if len(parts) >= 1 else 1
                    start = parts[1] if len(parts) >= 2 else '09:00'
                    end = parts[2] if len(parts) >= 3 else '21:00'
                    # 验证时间格式
                    datetime.strptime(start, '%H:%M')
                    datetime.strptime(end, '%H:%M')
                    count = max(1, min(count, 10))
                    self.mark_configured()
                    return {
                        'action': 'set_random_trigger',
                        'count': count,
                        'window_start': start,
                        'window_end': end,
                        'message': f'✅ 已设置随机推荐：每天 {count} 次，{start}-{end}'
                    }
                except (ValueError, IndexError):
                    return {'action': 'error', 'message': '❌ 格式错误，请按格式输入：次数,开始时间,结束时间'}
            # 没有输入，用默认值
            self.mark_configured()
            return {
                'action': 'set_random_trigger',
                'count': 1,
                'window_start': '09:00',
                'window_end': '21:00',
                'message': '✅ 已设置随机推荐：每天 1 次，09:00-21:00（默认）'
            }
        elif choice == '4':
            return {'action': 'configure_personality', 'message': '请选择语言风格：', 'prompt': self.get_personality_prompt()}
        return {'action': 'error', 'message': '无效选择'}

    def process_personality_choice(self, choice: str, file_path: str = None) -> Dict:
        if choice == '1':
            self.mark_configured()
            return {'action': 'use_default_personality', 'message': '✅ 使用默认语气'}
        elif choice == '2':
            if file_path and os.path.exists(file_path):
                self.mark_configured()
                return {'action': 'use_personality_file', 'file_path': file_path, 'message': f'✅ 已加载：{file_path}'}
            return {'action': 'error', 'message': '❌ 文件不存在'}
        return {'action': 'error', 'message': '无效选择'}

    def get_available_methods(self) -> List[str]:
        methods = []
        if self.config['exa']['enabled'] and self.config['exa']['api_key']:
            methods.append('exa')
        if self.config['tavily']['enabled'] and self.config['tavily']['api_key']:
            methods.append('tavily')
        if self.config['spotify']['enabled']:
            methods.append('spotify')
        if self.config['websearch']['enabled']:
            methods.append('websearch')
        return methods

    def get_best_method(self) -> str:
        methods = self.get_available_methods()
        if not methods:
            return 'websearch'
        priority_map = {
            'exa': self.config['exa']['priority'],
            'tavily': self.config['tavily']['priority'],
            'spotify': self.config['spotify']['priority'],
            'websearch': self.config['websearch']['priority']
        }
        return min(methods, key=lambda m: priority_map.get(m, 999))


# 全局实例
search_tools = SearchTools()
