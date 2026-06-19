#!/usr/bin/env python3
"""
读取对话历史
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class HistoryReader:
    """对话历史读取器"""

    def __init__(self, config: Dict):
        """
        初始化读取器

        Args:
            config: 配置信息
                - api_url: API 地址
                - api_key: API 密钥
                - user_id: 用户 ID
        """
        self.api_url = config.get('api_url', 'http://localhost:8080/api')
        self.api_key = config.get('api_key', '')
        self.user_id = config.get('user_id', '')

    def read_today_history(self) -> List[Dict]:
        """
        读取今天的对话历史

        Returns:
            对话历史列表，每条记录包含：
            - timestamp: 时间戳
            - role: 角色（user/assistant）
            - content: 对话内容
        """
        today = datetime.now().strftime('%Y-%m-%d')
        return self.read_history_by_date(today)

    def read_history_by_date(self, date: str) -> List[Dict]:
        """
        读取指定日期的对话历史

        Args:
            date: 日期，格式为 YYYY-MM-DD

        Returns:
            对话历史列表
        """
        # TODO: 实现实际的 API 调用
        # 这里提供一个示例实现框架

        try:
            # 示例：从本地文件读取（实际应调用 API）
            history_file = f"history_{date}.json"

            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                return history
            else:
                # 返回示例数据用于测试
                return self._get_sample_history()

        except Exception as e:
            print(f"读取对话历史失败: {e}")
            return []

    def _get_sample_history(self) -> List[Dict]:
        """获取示例对话历史（用于测试）"""
        return [
            {
                "timestamp": "2026-06-13T09:00:00",
                "role": "user",
                "content": "今天天气真好，心情不错"
            },
            {
                "timestamp": "2026-06-13T09:05:00",
                "role": "assistant",
                "content": "是的，天气确实很好！有什么计划吗？"
            },
            {
                "timestamp": "2026-06-13T10:30:00",
                "role": "user",
                "content": "在写代码，遇到一个 bug，有点烦"
            },
            {
                "timestamp": "2026-06-13T10:35:00",
                "role": "assistant",
                "content": "别着急，我们一起看看问题在哪里"
            },
            {
                "timestamp": "2026-06-13T14:00:00",
                "role": "user",
                "content": "终于解决了！开心"
            },
            {
                "timestamp": "2026-06-13T14:05:00",
                "role": "assistant",
                "content": "太好了！解决问题的感觉很棒吧"
            }
        ]

def read_history(config_path: str = None) -> List[Dict]:
    """
    便捷函数：读取今天的对话历史

    Args:
        config_path: 配置文件路径

    Returns:
        对话历史列表
    """
    # 加载配置
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        # 默认配置
        config = {
            'api_url': 'http://localhost:8080/api',
            'api_key': '',
            'user_id': ''
        }

    reader = HistoryReader(config)
    return reader.read_today_history()

if __name__ == '__main__':
    # 测试读取
    history = read_history()
    print(f"读取到 {len(history)} 条对话记录")
    for record in history:
        print(f"[{record['timestamp']}] {record['role']}: {record['content']}")
