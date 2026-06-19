#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索配置管理
"""
import json
import os
from typing import Dict, List


class SearchTools:
    """搜索配置管理"""

    def __init__(self, config_dir: str = None):
        self.config_dir = config_dir or os.path.join(
            os.path.dirname(__file__), '..', 'config'
        )
        self.config_file = os.path.join(self.config_dir, 'search_config.json')
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        default = {
            'exa': {'enabled': False, 'api_key': None, 'priority': 1},
            'tavily': {'enabled': False, 'api_key': None, 'priority': 2},
            'spotify': {'enabled': False, 'client_id': None, 'client_secret': None, 'priority': 3},
            'websearch': {'enabled': True, 'priority': 5},
            'first_run': True,
        }
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    cfg = json.load(f)
                    for k in default:
                        if k not in cfg:
                            cfg[k] = default[k]
                    return cfg
        except Exception:
            pass
        return default

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
        pri = {
            'exa': self.config['exa']['priority'],
            'tavily': self.config['tavily']['priority'],
            'spotify': self.config['spotify']['priority'],
            'websearch': self.config['websearch']['priority'],
        }
        return min(methods, key=lambda m: pri.get(m, 999))


# 全局实例
search_tools = SearchTools()
