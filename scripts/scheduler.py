#!/usr/bin/env python3
"""
定时触发器
支持固定时间和随机时间两种模式
"""

import time
import random
from datetime import datetime, timedelta
from typing import Callable, Optional, List
import threading
import json
import os


class MusicScheduler:
    """音乐推荐定时调度器"""

    def __init__(self, callback: Callable, config_path: str = None):
        self.callback = callback
        self.running = False
        self.thread = None
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), '..', 'config', 'scheduler_config.json'
        )
        # 固定时间模式
        self.trigger_times = []
        # 随机时间模式
        self.mode = 'fixed'  # 'fixed' | 'random' | 'off'
        self.random_count = 1  # 每天随机推几次
        self.random_window_start = '09:00'
        self.random_window_end = '21:00'
        # 今日状态
        self.today_triggered = set()
        self._today_random_times = []

        self._load_config()

    def _load_config(self):
        """加载配置"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.trigger_times = config.get('trigger_times', [])
                    self.mode = config.get('mode', 'fixed')
                    self.random_count = config.get('random_count', 1)
                    self.random_window_start = config.get('random_window_start', '09:00')
                    self.random_window_end = config.get('random_window_end', '21:00')
        except Exception as e:
            print(f"加载配置失败: {e}")

    def _save_config(self):
        """保存配置"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            config = {
                'mode': self.mode,
                'trigger_times': self.trigger_times,
                'random_count': self.random_count,
                'random_window_start': self.random_window_start,
                'random_window_end': self.random_window_end
            }
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")

    # ── 固定时间 ──────────────────────────────

    def set_trigger_times(self, times: List[str]):
        """设置固定触发时间，如 ["08:00", "18:00"]"""
        valid_times = []
        for t in times:
            try:
                datetime.strptime(t.strip(), '%H:%M')
                valid_times.append(t.strip())
            except ValueError:
                print(f"无效的时间格式: {t}，跳过")
        self.trigger_times = valid_times
        self.mode = 'fixed'
        self._save_config()
        print(f"已设置固定触发时间: {self.trigger_times}")

    # ── 随机时间 ──────────────────────────────

    def set_random_trigger(self, count: int = 1,
                           window_start: str = '09:00',
                           window_end: str = '21:00'):
        """设置随机触发：在时间窗口内随机选 count 个时间点"""
        self.mode = 'random'
        self.random_count = max(1, min(count, 10))
        self.random_window_start = window_start
        self.random_window_end = window_end
        self._today_random_times = self._generate_random_times()
        self._save_config()
        print(f"已设置随机触发: 每天 {self.random_count} 次，"
              f"窗口 {self.random_window_start}-{self.random_window_end}")

    def _generate_random_times(self):
        """今天还没过完的话，在剩余窗口里随机生成触发时间"""
        now = datetime.now()
        try:
            start = datetime.strptime(self.random_window_start, '%H:%M')
            end = datetime.strptime(self.random_window_end, '%H:%M')
        except ValueError:
            return []

        start_minutes = start.hour * 60 + start.minute
        end_minutes = end.hour * 60 + end.minute
        now_minutes = now.hour * 60 + now.minute

        # 只生成今天剩余的时间
        effective_start = max(start_minutes, now_minutes + 1)
        if effective_start >= end_minutes:
            return []

        # 在有效窗口内随机选 time_count 个不重复的分钟数
        available = list(range(effective_start, end_minutes))
        count = min(self.random_count, len(available))
        if count == 0:
            return []

        picks = sorted(random.sample(available, count))
        times = []
        for m in picks:
            h, mi = divmod(m, 60)
            times.append(f'{h:02d}:{mi:02d}')
        return times

    # ── 调度核心 ──────────────────────────────

    def get_trigger_times(self) -> List[str]:
        """获取今日实际的触发时间列表"""
        if self.mode == 'random':
            return self._today_random_times
        return self.trigger_times

    def start(self):
        """启动调度器"""
        if self.running:
            return
        if self.mode == 'fixed' and not self.trigger_times:
            print("未设置触发时间")
            return
        self.running = True
        self._today_random_times = self._generate_random_times() if self.mode == 'random' else []
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        times = self._today_random_times if self.mode == 'random' else self.trigger_times
        print(f"调度器已启动（{self.mode}模式），今日触发: {times}")

    def stop(self):
        """停止调度器"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("调度器已停止")

    def _run(self):
        """主循环，每分钟检查一次"""
        last_date = datetime.now().date()
        while self.running:
            now = datetime.now()
            if now.date() != last_date:
                self.reset_daily()
                last_date = now.date()
            if self._should_trigger(now):
                self._trigger(now)
            time.sleep(60)

    def _should_trigger(self, now: datetime) -> bool:
        current_time = now.strftime('%H:%M')
        if current_time in self.today_triggered:
            return False
        if self.mode == 'random':
            return current_time in self._today_random_times
        return current_time in self.trigger_times

    def _trigger(self, now: datetime):
        current_time = now.strftime('%H:%M')
        try:
            print(f"[{now}] 触发推荐（{current_time}）...")
            self.callback()
            self.today_triggered.add(current_time)
        except Exception as e:
            print(f"触发失败: {e}")

    def reset_daily(self):
        """每天 0 点重置状态，随机模式重新生成时间"""
        self.today_triggered.clear()
        if self.mode == 'random':
            self._today_random_times = self._generate_random_times()
            print(f"新的一天，随机触发时间: {self._today_random_times}")


class ManualScheduler:
    """手动触发（测试用）"""

    def __init__(self, callback: Callable):
        self.callback = callback

    def trigger(self):
        try:
            print(f"[{datetime.now()}] 手动触发...")
            self.callback()
        except Exception as e:
            print(f"触发失败: {e}")


def create_scheduler(callback: Callable, config_path: str = None,
                     auto_start: bool = False) -> MusicScheduler:
    scheduler = MusicScheduler(callback, config_path)
    if auto_start:
        scheduler.start()
    return scheduler


if __name__ == '__main__':
    def on_trigger():
        print("→ 触发音乐推荐！")

    s = create_scheduler(on_trigger)

    # 测试固定时间
    s.set_trigger_times(["08:00", "18:00"])
    print(f"固定模式触发时间: {s.get_trigger_times()}")

    # 测试随机时间
    s.set_random_trigger(count=2, window_start='10:00', window_end='20:00')
    s._today_random_times = s._generate_random_times()
    print(f"随机模式今日触发: {s._today_random_times}")
