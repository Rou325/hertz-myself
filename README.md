# hertz-myself | 听见自己的频率

根据聊天内容推荐歌。不听抖音热歌。

![](https://img.shields.io/badge/version-2.2.0-blue)
![](https://img.shields.io/badge/python-3.7+-green)
![](https://img.shields.io/badge/license-MIT-orange)

---

## 它能做什么

你每天聊天，它每天推荐一首歌。分析你的对话情绪，从网上搜合适的音乐，推给你。听完打分，它会记住你喜欢什么。

- 根据对话情绪推荐
- 过滤抖音热歌、口水歌
- 支持天气集成（有天气 skill 就用，没有就跳过）
- 支持人格文件（soul.md、personality.md 等）
- 1-10 分评分，越评越懂你

## 安装

```bash
# 直接克隆
git clone https://github.com/Rou325/hertz-myself.git
cd hertz-myself

# pip 安装
pip install .

# 或者直接运行
python scripts/main.py --manual
```

如果你用 Claude Code，直接装 skill 包：

```bash
/install-skill hertz-myself.skill
```

npx 方式需要先把 Python 打包成 Node 包，暂时不支持。如果真的需要，我可以帮你做一个 npx 兼容的版本——但说实话，这技能是 Python 写的，用 pip 更自然。

## 怎么用

第一次运行会问你几个问题：

1. 要不要配 API（不配也能用）
2. 什么时候推荐（固定时间、随机、或交给外部 cron）
3. 要不要用人格文件

```bash
# 手动触发
python scripts/main.py --manual

# 固定时间触发
python scripts/main.py --set-trigger-time "18:00"

# 看看统计数据
python scripts/main.py --stats

# 跑测试
python tests/test_main.py
```

## 推荐长什么样

```
我是 hertz-myself，捕捉到了你情绪的起伏
今天 北京 阳光正好，22°C 的温暖
来一首《Midnight City》吧

戴上耳机，听见自己

---

🎵 Midnight City
🎤 M83
💿 Hurry Up, We're Dreaming
🎸 电子/Synth-pop/Dream Pop
📅 2011-07-19

M83 是法国电子音乐项目，由 Anthony Gonzalez 创立。

这首歌的合成器旋律就像夜晚城市的霓虹灯。

满分10分，回复数字即可，例如：8 很好听

🎵 享受《Midnight City》带来的感动
```

## 它怎么工作的

```
聊天记录 → 分析情绪 → 搜索歌曲 → 过滤热歌 → 推荐给你 → 你打分 → 越推越准
```

## 省钱吗

每次推荐大约 2500 tokens。用 DeepSeek V4 Flash：
- 缓存命中：每月 5 分钱
- 缓存未命中：每月 1 毛钱

## 隐私

你的评分数据、API 密钥、配置文件都不会上传。data/ 目录已被 gitignore 排除。

## 项目结构

```
hertz-myself/
├── SKILL.md              # 技能说明
├── README.md             # 本文件
├── CLAUDE.md             # AI 助手指南
├── scripts/
│   ├── main.py           # 主程序
│   ├── greeting.py       # 开场白
│   ├── search_tools.py   # 搜索工具
│   ├── user_rating.py    # 评分系统
│   ├── analyze_mood.py   # 情绪分析
│   ├── weather_detector.py
│   ├── personality_detector.py
│   ├── scheduler.py      # 定时触发
│   └── read_history.py
├── tests/                # 10/10 测试通过
├── evals/                # 测试用例
├── config/               # 配置文件
└── examples/             # 输出示例
```

## 支持哪些平台

- Claude Code（AskUserQuestion 交互界面）
- opencode（UserInput/SelectOption 交互界面）
- 其他 agent 回退到文本模式

## 搜索 API 对比

| API | 免费额度 | 国内能用 |
|-----|----------|----------|
| Exa | 1000次/月 | 能 |
| Tavily | 1000次/月 | 能 |
| Spotify | 个人用够 | 要代理 |
| WebSearch | 无限 | 能 |

## License

MIT
