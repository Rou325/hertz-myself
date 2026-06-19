# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**hertz-myself** — 根据每日对话内容，分析情绪，实时搜索并推荐一首歌。核心玩法是：读聊天记录 → 分析心情 → 搜歌 → 过滤热歌 → 推给用户 → 用户打分 → 越推越准。

## Common Commands

```bash
# 手动触发一次推荐
python -X utf8 scripts/main.py --manual

# 首次配置（如果还没配过）
python -X utf8 scripts/main.py --manual

# 查看评分统计
python -X utf8 scripts/main.py --stats

# 设置推荐时间
python -X utf8 scripts/main.py --set-trigger-time "18:00"

# 启动定时调度器
python -X utf8 scripts/main.py --scheduler

# 运行全部测试
python -X utf8 tests/test_main.py

# 打包成 .skill 文件
python package_skill.py .

# 打包 Python 包
python setup.py sdist bdist_wheel
```

## Architecture

### Module Overview

| 文件 | 代码量 | 职责 |
|------|--------|------|
| `search_tools.py` | 843 行 | **核心** — 搜索 API 管理（Exa/Tavily/Spotify/WebSearch）、配置系统、搜索查询生成、首次配置流程 |
| `main.py` | 504 行 | **入口** — 编排推荐流程、命令行参数、评分处理、开场白集成 |
| `user_rating.py` | 514 行 | 1-10 分评分系统、偏好学习、统计、评分提示生成 |
| `analyze_mood.py` | 388 行 | 情绪分析、主题识别、关键词提取、天气情绪混合 |
| `greeting.py` | 225 行 | 开场白生成（随机模板、人格风格、天气集成） |
| `personality_detector.py` | 252 行 | 人格文件加载与应用（soul.md 等） |
| `weather_detector.py` | 213 行 | 天气 skill 检测与调用 |
| `scheduler.py` | 209 行 | 定时触发管理（固定/随机/多种时间） |
| `read_history.py` | 135 行 | 对话历史读取 |

### Data Flow

```
User Input
  │
  ▼
read_history.py ──── 读取当天对话
  │
  ▼
weather_detector.py ─ 检测天气 skill（可选）
  │
  ▼
personality_detector.py ─ 加载人格文件（可选）
  │
  ▼
analyze_mood.py ──── 分析情绪 + 主题
  │
  ▼
search_tools.py ──── 生成搜索查询 → 过滤热歌 → 输出搜索指令
  │
  ▼
greeting.py ──────── 生成开场白（随机模板 or 人格风格）
  │
  ▼
full output ──────── 歌曲信息 + 开场白 + 评分提示
  │
  ▼
user_rating.py ───── 用户评分 → 记录偏好 → 下一次推荐更准
```

### Config Files

| 文件 | 内容 | 备注 |
|------|------|------|
| `config/search_config.json` | API 密钥、启用状态 | **不上传 GitHub**（被 gitignore） |
| `config/scheduler_config.json` | 触发时间列表 | 上传，不含敏感信息 |
| `data/user_ratings.json` | 评分历史 | **不上传 GitHub** |
| `data/user_preferences.json` | 偏好数据 | **不上传 GitHub** |

## Key Design Decisions

1. **无硬编码密钥** — 所有 API key 走配置文件，`data/` 和 `search_config.json` 被 gitignore
2. **人格/天气都是可选** — 检测到就用，没有就跳过，不影响核心推荐
3. **不提供音乐链接** — 链接容易失效，让用户自己搜歌名更可靠
4. **1-10 分制** — 比常见的 1-5 更细腻，7 以上才算"喜欢"，3 以下进黑名单
5. **用户驱动配置** — 首次运行时通过 UI 界面（Claude Code）或文本问答（其他 agent）完成

## Testing

`tests/test_main.py` 涵盖 10 个测试项：

```bash
python -X utf8 tests/test_main.py
```

测试覆盖：导入、搜索工具、评分系统、天气检测、情绪分析、调度器、配置文件、文档、开场白、人格集成。**10/10 通过。**

## Windows 注意事项

- 所有 Python 命令加上 `-X utf8`，否则 Windows 默认编码会报错
- 删除文件用回收站（[Microsoft.VisualBasic.FileIO]::DeleteFile），不要直接 `rm -f`
- `.skill` 打包文件在 `release/` 目录下，不上传 GitHub

## Key Files to Read First

1. **scripts/main.py** — 入口逻辑，看完就懂整个流程
2. **scripts/search_tools.py** — 最复杂的模块，配置系统都在这里
3. **scripts/user_rating.py** — 评分和偏好学习逻辑
