#!/usr/bin/env python3
"""
随机延迟脚本：cron 固定时间触发 → 脚本等一段随机时间 → Agent 才开始干活

两种模式：
  无参数         → 从 scheduler_config 读取窗口，在窗口内等一个随机时刻
  --max-delay N  → 等 0~N 秒内的随机时长（N 单位秒），如 --max-delay 180 = 3 分钟内随机
"""
import json
import os
import random
import sys
import time
from datetime import datetime

config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'scheduler_config.json')

# ── 模式一：指定最大等待秒数 ──
if '--max-delay' in sys.argv:
    idx = sys.argv.index('--max-delay')
    if idx + 1 < len(sys.argv):
        try:
            delay = random.uniform(0, int(sys.argv[idx + 1]))
            time.sleep(delay)
        except ValueError:
            pass
    exit(0)

# ── 模式二：从配置读取窗口 ──
try:
    with open(config_path, encoding='utf-8') as f:
        cfg = json.load(f)
except Exception:
    exit(0)

if cfg.get('mode') != 'random':
    exit(0)  # 非随机模式不用等

start_str = cfg.get('random_window_start', '09:00')
end_str = cfg.get('random_window_end', '21:00')
count = cfg.get('random_count', 1)

def to_minutes(t: str) -> int:
    h, m = map(int, t.split(':'))
    return h * 60 + m

s = to_minutes(start_str)
e = to_minutes(end_str)
if s >= e:
    exit(0)

now_offset = datetime.now().hour * 60 + datetime.now().minute

# 从窗口里随机选 count 个分钟数，排序后找第一个还没过的
picks = sorted(random.sample(range(s, e), min(count, e - s)))
target = next((p for p in picks if p >= now_offset), None)
if target is None:
    exit(0)  # 今天的随机时间都过了

# 等
now = datetime.now()
target_time = now.replace(hour=target // 60, minute=target % 60, second=0, microsecond=0)
delay = (target_time - now).total_seconds()
if delay > 0:
    time.sleep(delay)
