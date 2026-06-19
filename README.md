# 🎵 hertz-myself | 听见自己的频率

智能音乐推荐系统，根据对话内容推荐歌曲。

## 快速开始

### 首次使用
```bash
python -X utf8 scripts/main.py --manual
```

系统会询问：
1. API 配置（可选）
2. 推荐时间设置
3. 语言风格选择

### 常用命令
```bash
# 手动触发推荐
python -X utf8 scripts/main.py --manual

# 查看评分统计
python -X utf8 scripts/main.py --stats

# 设置触发时间
python -X utf8 scripts/main.py --set-trigger-time "18:00"

# 启动定时调度器
python -X utf8 scripts/main.py --scheduler

# 运行测试
python -X utf8 tests/test_main.py
```

## 核心功能

### 1. 智能推荐
- 根据对话内容推荐歌曲
- 支持天气集成（可选）
- 支持人格文件（可选）

### 2. 多平台支持
- Claude Code（UI 界面）
- opencode（UI 界面）
- hermes、openclaw（文本模式）

### 3. 评分系统
- 1-10 分评分
- 记录用户偏好
- 个性化推荐

### 4. 定时推荐
- 固定时间
- 多个时间点
- 随机时间
- 外部 cron 工具

## 配置说明

### API 配置
- **Exa**：AI 搜索引擎（国内友好）
- **Tavily**：AI 搜索引擎（国内友好）
- **Spotify**：专业音乐数据（国内不友好）
- **WebSearch**：默认方案（免费）

### 人格文件
支持文件：soul.md、personality.md、character.md、persona.md、role.md

### 天气集成
自动检测天气 skill，有就用，没有就跳过。

## 文件结构

```
hertz-myself/
├── SKILL.md                    # 技能说明
├── README.md                   # 本文件
├── CLAUDE.md                   # Claude Code 指南
├── scripts/
│   ├── main.py                 # 主程序
│   ├── greeting.py             # 开场白
│   ├── search_tools.py         # 搜索工具
│   ├── user_rating.py          # 评分系统
│   ├── analyze_mood.py         # 情绪分析
│   ├── weather_detector.py     # 天气检测
│   ├── personality_detector.py # 人格检测
│   ├── scheduler.py            # 定时触发
│   └── read_history.py         # 历史读取
├── tests/
│   └── test_main.py            # 测试脚本
├── config/
│   ├── search_config.json      # 搜索配置
│   └── scheduler_config.json   # 调度配置
└── data/
    ├── user_ratings.json       # 评分数据
    └── user_preferences.json   # 偏好数据
```

## 输出示例

```
我是 hertz-myself，捕捉到了你情绪的起伏
今天 北京 阳光正好，22°C 的温暖
送你一首《Midnight City》

戴上耳机，听见自己

---

🎵 Midnight City
🎤 M83
💿 Hurry Up, We're Dreaming
🎸 电子/Synth-pop/Dream Pop
📅 2011-07-19

M83 是法国电子音乐项目，由 Anthony Gonzalez 创立。

这首歌的合成器旋律和梦幻氛围，就像夜晚城市的霓虹灯。

满分10分，回复数字即可，例如：8 很好听
写下你的感受能帮助我更好地了解你的喜好！

🎵 享受《Midnight City》带来的感动
```

## Token 消耗

- 每次推荐：约 2500 tokens
- 每月成本：约 0.05-0.11 元（DeepSeek V4 Flash）
- 每年成本：约 0.6-1.3 元

## 注意事项

- 使用 `-X utf8` 标志运行 Python 脚本（Windows 编码）
- 首次配置是交互式的
- 不提供收听链接（容易失效）
- 评分提示鼓励用户写反馈

## 更新日志

### v2.2.0 (2026-06-14)
- 自定义触发时间
- 评分满分 10 分
- 天气集成
- 人格集成
- 随机开场白
- 多平台 UI 支持

### v2.1.0 (2026-06-13)
- 交互式配置
- 多种 API 支持
- 多维度评分
- 个性化推荐

### v2.0.0 (2026-06-13)
- 智能推荐系统
- 实时搜索
- 用户评分系统

### v1.0.0 (2026-06-13)
- 初始版本
- 预设歌曲数据库
- 基础情绪分析
