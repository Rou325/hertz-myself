#!/usr/bin/env python3
"""
定时触发器
支持用户自定义触发时间
"""

import time
from datetime import datetime, timedelta
from typing import Callable, Optional, List
import threading
import json
import os

class MusicScheduler:
    """音乐推荐定时调度器"""

    def __init__(self, callback: Callable, config_path: str = None):
        """
        初始化调度器

        Args:
            callback: 触发时调用的回调函数
            config_path: 配置文件路径
        """
        self.callback = callback
        self.running = False
        self.thread = None
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), '..', 'config', 'scheduler_config.json'
        )
        self.trigger_times = []  # 用户自定义的触发时间列表
        self.today_triggered = set()  # 今天已触发的时间

        # 加载配置
        self._load_config()

    def _load_config(self):
        """加载调度器配置"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.trigger_times = config.get('trigger_times', [])
        except Exception as e:
            print(f"加载调度器配置失败: {e}")
            self.trigger_times = []

    def _save_config(self):
        """保存调度器配置"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            config = {
                'trigger_times': self.trigger_times
            }
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存调度器配置失败: {e}")

    def set_trigger_times(self, times: List[str]):
        """
        设置触发时间

        Args:
            times: 触发时间列表，格式为 ["HH:MM", "HH:MM", ...]
        """
        # 验证时间格式
        valid_times = []
        for t in times:
            try:
                datetime.strptime(t, '%H:%M')
                valid_times.append(t)
            except ValueError:
                print(f"无效的时间格式: {t}，跳过")

        self.trigger_times = valid_times
        self._save_config()
        print(f"已设置触发时间: {self.trigger_times}")

    def get_trigger_times(self) -> List[str]:
        """获取触发时间列表"""
        return self.trigger_times

    def start(self):
        """启动调度器"""
        if self.running:
            return

        if not self.trigger_times:
            print("未设置触发时间，请先设置触发时间")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print(f"音乐推荐调度器已启动，触发时间: {self.trigger_times}")

    def stop(self):
        """停止调度器"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("音乐推荐调度器已停止")

    def _run(self):
        """运行调度器主循环"""
        while self.running:
            now = datetime.now()

            # 检查是否在触发时间
            if self._should_trigger(now):
                self._trigger(now)

            # 每分钟检查一次
            time.sleep(60)

    def _should_trigger(self, now: datetime) -> bool:
        """
        判断是否应该触发

        Args:
            now: 当前时间

        Returns:
            是否应该触发
        """
        current_time = now.strftime('%H:%M')

        # 检查当前时间是否在触发时间列表中
        if current_time in self.trigger_times:
            # 检查今天是否已经触发过这个时间
            if current_time not in self.today_triggered:
                return True

        return False

    def _trigger(self, now: datetime):
        """
        触发推荐

        Args:
            now: 当前时间
        """
        current_time = now.strftime('%H:%M')
        try:
            print(f"[{now}] 触发音乐推荐（{current_time}）...")
            self.callback()
            self.today_triggered.add(current_time)
        except Exception as e:
            print(f"触发推荐失败: {e}")

    def reset_daily(self):
        """重置每日触发状态（每天 0 点调用）"""
        self.today_triggered.clear()

class ManualScheduler:
    """手动触发调度器（用于测试）"""

    def __init__(self, callback: Callable):
        """
        初始化调度器

        Args:
            callback: 触发时调用的回调函数
        """
        self.callback = callback

    def trigger(self):
        """手动触发推荐"""
        try:
            print(f"[{datetime.now()}] 手动触发音乐推荐...")
            self.callback()
        except Exception as e:
            print(f"触发推荐失败: {e}")

def create_scheduler(callback: Callable, config_path: str = None, auto_start: bool = False) -> MusicScheduler:
    """
    创建调度器

    Args:
        callback: 触发时调用的回调函数
        config_path: 配置文件路径
        auto_start: 是否自动启动

    Returns:
        调度器实例
    """
    scheduler = MusicScheduler(callback, config_path)

    if auto_start:
        scheduler.start()

    return scheduler

if __name__ == '__main__':
    # 测试调度器
    def on_trigger():
        print("触发音乐推荐！")

    scheduler = create_scheduler(on_trigger, auto_start=False)

    # 设置触发时间
    scheduler.set_trigger_times(["08:00", "12:00", "18:00"])

    # 显示触发时间
    print(f"触发时间: {scheduler.get_trigger_times()}")

    # 模拟手动触发
    scheduler._trigger(datetime.now())
