# 🎵 hertz-myself | 听见自己的频率

智能音乐推荐系统，根据对话内容分析情绪，实时推荐歌曲。拒绝抖音热歌，专注品质音乐。

[![Version](https://img.shields.io/badge/version-2.2.0-blue)](./VERSION.md)
[![Python](https://img.shields.io/badge/python-3.7%2B-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange)](./LICENSE)

---

## ✨ 特性

- 🎯 **智能推荐**：分析对话情绪和主题，推荐最合适的歌曲
- 🚫 **拒绝热歌**：过滤抖音热歌、口水歌、网红歌
- 🌍 **全球范围**：不限语言，中文、英文、日文、韩文等均可
- 🎭 **人格集成**：支持人格文件，套用语言风格
- 🌤️ **天气集成**：结合天气状况优化推荐（可选）
- 📊 **评分系统**：1-10 分评分，记录用户偏好
- ⏰ **定时推荐**：支持固定时间、多个时间、随机时间
- 🔑 **多种 API**：Exa、Tavily、Spotify、WebSearch
- 🧪 **自动化测试**：10/10 测试通过

## 🚀 快速开始

### 首次使用

```bash
python -X utf8 scripts/main.py --manual
```

首次运行时，系统会询问：
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

## 📤 输出示例

```
我是 hertz-myself，捕捉到了你情绪的起伏
今天 北京 阳光正好，22°C 的温暖
来一首《Midnight City》吧

戴上耳机，听见自己

---

🎵 今日音乐推荐

🎶 歌曲信息

歌名：《Midnight City》
歌手：M83
专辑：Hurry Up, We're Dreaming
风格：电子/Synth-pop/Dream Pop
发行时间：2011-07-19

🎤 歌手简介
M83 是法国电子音乐项目，由 Anthony Gonzalez 创立。

💡 推荐理由
这首歌的合成器旋律和梦幻氛围，就像夜晚城市的霓虹灯。

---

满分10分，回复数字即可，例如：8 很好听
写下你的感受能帮助我更好地了解你的喜好！

🎵 享受《Midnight City》带来的感动
```

## 🔧 配置说明

### API 配置

支持以下搜索引擎：

| API | 用途 | 免费额度 | 国内可用 |
|-----|------|----------|----------|
| **Exa** | AI 搜索引擎 | 1000次/月 | ✅ |
| **Tavily** | AI 搜索引擎 | 1000次/月 | ✅ |
| **Spotify** | 音乐数据 | 个人使用 | ❌ 需代理 |
| **WebSearch** | 默认方案 | 无限制 | ✅ |

### 人格文件

支持以下人格文件：`soul.md`、`personality.md`、`character.md`、`persona.md`、`role.md`

### 天气集成

自动检测天气 skill，有就用，没有就跳过。

## 📁 项目结构

```
hertz-myself/
├── SKILL.md                    # 技能说明
├── README.md                   # 本文件
├── CHANGELOG.md                # 更新日志
├── VERSION.md                  # 版本记录
├── CLAUDE.md                   # Claude Code 指南
├── scripts/
│   ├── main.py                 # 主程序
│   ├── greeting.py             # 开场白生成
│   ├── search_tools.py         # 搜索工具
│   ├── user_rating.py          # 评分系统（1-10分）
│   ├── analyze_mood.py         # 情绪分析
│   ├── weather_detector.py     # 天气检测
│   ├── personality_detector.py # 人格文件加载
│   ├── scheduler.py            # 定时触发
│   └── read_history.py         # 对话历史读取
├── tests/
│   ├── test_main.py            # 主测试（10/10通过）
│   └── test_optimization.py    # 优化测试
├── evals/
│   └── evals.json              # 测试用例
├── config/
│   └── scheduler_config.json   # 调度配置
└── examples/
    └── obsidian_example.md     # Obsidian 示例
```

## 🔒 安全说明

- ✅ 无硬编码 API 密钥
- ✅ 配置文件使用占位符
- ✅ 用户数据不上传（data/ 目录排除）
- ✅ 支持本地运行

## 📊 Token 消耗

- 每次推荐：约 2500 tokens
- 每月成本：约 0.05-0.11 元（DeepSeek V4 Flash）
- 每年成本：约 0.6-1.3 元

## 🧪 测试

```bash
# 运行所有测试
python -X utf8 tests/test_main.py

# 测试结果：10/10 通过
```

## 📦 安装

### 方式1：直接使用
```bash
git clone https://github.com/Rou325/hertz-myself.git
cd hertz-myself
python -X utf8 scripts/main.py --manual
```

### 方式2：pip 安装
```bash
pip install .
hertz-myself --manual
```

### 方式3：技能包安装
```bash
# 在 Claude Code 中
/install-skill hertz-myself.skill
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📝 更新日志

详见 [CHANGELOG.md](./CHANGELOG.md)

## 📄 许可证

MIT License

---

🎵 听见自己的频率 - 智能音乐推荐系统
