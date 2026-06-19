# 🎵 hertz-myself - 版本记录

## 当前版本：v2.2.0

**发布日期**：2026-06-14

**版本类型**：个人开发版本

## 核心能力

### 1. 🎯 交互式配置
- 首次调用时询问用户配置
- 支持多种 UI 工具（AskUserQuestion、UserInput、SelectOption）
- 自动回退到文本模式

### 2. 🔑 多种 API 支持
- Exa：AI 优化的搜索引擎（国内友好）
- Tavily：AI 优化的搜索引擎（国内友好）
- Spotify：专业音乐数据（国内不友好）
- WebSearch：默认方案（完全免费）

### 3. 🎵 多平台音乐链接
- 国内平台：网易云音乐、QQ音乐、酷我音乐、酷狗音乐
- 国外平台：Spotify、Apple Music、YouTube Music

### 4. 🇨🇳 国内服务器支持
- API 可用性：明确标注哪些 API 在国内可用
- 国内友好：Exa、Tavily、WebSearch 国内可用
- 国内不友好：Spotify 需要代理或 VPN

### 5. 📊 多维度评分系统
- 评分维度：评分、心情、场景、时间
- 满分 10 分：评分范围 1-10
- 偏好学习：根据评分记录用户喜好

### 6. 🌤️ 天气集成
- 自动检测：检测是否有天气 skill 可用
- 智能结合：结合天气状况优化推荐
- 无感使用：有天气 skill 就用，没有就跳过

### 7. 🎭 人格集成
- 首次询问：首次调用时询问用户是否使用人格文件
- 套用风格：如果有人格文件，套用人格语言风格
- 支持文件：soul.md、personality.md、character.md、persona.md、role.md

### 8. 🔍 智能搜索
- 实时搜索：根据对话内容实时搜索歌曲
- 多种搜索方式：自动选择最佳方案
- 随机性强：每次推荐都不同
- 智能过滤：自动过滤抖音热歌、口水歌

### 9. 🧪 自动化测试
- 测试覆盖：10 个测试用例全部通过
- 功能测试：导入、配置、评分、天气、情绪分析、调度器
- 文档测试：配置文件、文档完整性
- 开场白测试：验证开场白生成
- 人格集成测试：验证人格文件加载

## 文件结构

```
hertz-myself/
├── SKILL.md                    # 技能说明
├── README.md                   # 使用说明
├── CHANGELOG.md                # 版本更新日志
├── VERSION.md                  # 本文件
├── CLAUDE.md                   # Claude Code 指南
├── .gitignore                  # Git 忽略文件
├── scripts/
│   ├── main.py                 # 主程序
│   ├── greeting.py             # 开场白
│   ├── search_tools.py         # 搜索工具
│   ├── user_rating.py          # 用户评分系统
│   ├── analyze_mood.py         # 情绪分析
│   ├── weather_detector.py     # 天气检测
│   ├── personality_detector.py # 人格检测
│   ├── scheduler.py            # 定时触发
│   └── read_history.py         # 历史读取
├── tests/
│   ├── test_main.py            # 主测试
│   └── test_optimization.py    # 优化测试
├── evals/
│   └── evals.json              # 测试用例
├── config/
│   ├── search_config.json      # 搜索配置
│   └── scheduler_config.json   # 调度配置
└── data/
    ├── user_ratings.json       # 评分数据
    └── user_preferences.json   # 偏好数据
```

## 使用方法

### 首次使用
```bash
python -X utf8 scripts/main.py --manual
```

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

## Token 消耗

- 每次推荐：约 2500 tokens
- 每月成本：约 0.05-0.11 元（DeepSeek V4 Flash）
- 每年成本：约 0.6-1.3 元
