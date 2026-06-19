#!/usr/bin/env python3
"""
定时配置管理
支持固定时间和随机时间两种模式
"""
import json
import os
import random
from datetime import datetime
from typing import Callable, List, Optional


class MusicScheduler:
    """调度配置管理器"""

    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), '..', 'config', 'scheduler_config.json'
        )
        self.trigger_times = []
        self.mode = 'fixed'
        self.random_count = 1
        self.random_window_start = '09:00'
        self.random_window_end = '21:00'
        self._today_random_times = []
        self._load_config()

    def _load_config(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    cfg = json.load(f)
                    self.trigger_times = cfg.get('trigger_times', [])
                    self.mode = cfg.get('mode', 'fixed')
                    self.random_count = cfg.get('random_count', 1)
                    self.random_window_start = cfg.get('random_window_start', '09:00')
                    self.random_window_end = cfg.get('random_window_end', '21:00')
        except Exception:
            pass

    def _save_config(self):
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'mode': self.mode,
                    'trigger_times': self.trigger_times,
                    'random_count': self.random_count,
                    'random_window_start': self.random_window_start,
                    'random_window_end': self.random_window_end,
                    'last_generated': datetime.now().isoformat(),
                }, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def set_trigger_times(self, times: List[str]):
        valid = []
        for t in times:
            try:
                datetime.strptime(t.strip(), '%H:%M')
                valid.append(t.strip())
            except ValueError:
                pass
        self.trigger_times = valid
        self.mode = 'fixed'
        self._save_config()

    def set_random_trigger(self, count: int = 1,
                           window_start: str = '09:00',
                           window_end: str = '21:00'):
        self.mode = 'random'
        self.random_count = max(1, min(count, 10))
        self.random_window_start = window_start
        self.random_window_end = window_end
        self._save_config()

    def _generate_random_times(self) -> List[str]:
        """生成随机时间，只取 :00/:30 整半点以对齐 cron"""
        now = datetime.now()
        try:
            start = datetime.strptime(self.random_window_start, '%H:%M')
            end = datetime.strptime(self.random_window_end, '%H:%M')
        except ValueError:
            return []

        start_slots = (start.hour * 60 + start.minute) // 30
        end_slots = (end.hour * 60 + end.minute) // 30
        now_slot = (now.hour * 60 + now.minute) // 30
        if now.minute > 15:
            now_slot += 1

        effective = max(start_slots, now_slot)
        if effective >= end_slots:
            return []

        available = list(range(effective, end_slots))
        count = min(self.random_count, len(available))
        if count == 0:
            return []

        picks = sorted(random.sample(available, count))
        return [f'{h:02d}:{m:02d}' for s in picks for h, m in [(divmod(s * 30, 60))]]

    def get_trigger_times(self) -> List[str]:
        if self.mode == 'random':
            if not self._today_random_times:
                self._today_random_times = self._generate_random_times()
            return self._today_random_times
        return self.trigger_times


def create_scheduler(config_path: str = None) -> MusicScheduler:
    return MusicScheduler(config_path)
