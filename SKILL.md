---
name: hertz-myself
description: 听见自己的频率 - 智能音乐推荐技能，根据对话内容实时搜索歌曲，拒绝网络热歌，支持用户评分
triggers:
  - 听见自己的频率
  - hertz-myself
  - 音乐推荐
  - 推荐音乐
  - 今日推荐
  - /hertz-myself
---

# 🎵 听见自己的频率 - 智能音乐推荐技能

根据当天的对话历史，智能分析内容，实时搜索推荐歌曲。你负责思考，脚本只做代码擅长的事。

## 核心特点

- **实时搜索**：根据对话内容实时搜索歌曲，不用预设数据库
- **情绪分析**：你来分析对话情绪和主题，推荐最适合的歌曲
- **随机性强**：每次推荐都不同，探索新音乐
- **拒绝热歌**：过滤抖音热歌、网络神曲、口水歌
- **范围要广**：不限风格/语言/年代，什么好歌都推荐
- **全球范围**：不限语言，中文、英文、日文、韩文等均可
- **评分系统**：用户听完后可评分（1-10分），记录偏好
- **天气集成**：首次询问用户地区，同意后有 weather skill 就用，没有就 WebSearch 查
- **人格集成**：支持 soul.md、personality.md 等文件，套用语言风格

## 工作流程

### 平台检测

你的运行环境可能是 Claude Code、opencode 或 Hermes。与用户交互时，按平台选择正确的方式：

- **Claude Code** → 用 `AskUserQuestion` 工具
- **opencode** → 用 `UserInput`（自由输入）或 `SelectOption`（选项选择）
- **Hermes** → 用文本模式提问，等用户回复

以下步骤中所有「询问用户」均按此映射选择交互方式。

### 第零步：首次运行检查

调用脚本检查是否首次使用：

```bash
python -X utf8 scripts/main.py --config-status
```

如果返回 `first_run: true`，说明从未配置过。直接进入配置——**不废话问要不要，直接问第一步。** 每步都有「跳过」选项。

全程你（AI）自己问、自己解析回复、自己调脚本保存。不要调 `scripts/main.py --setup`（那是旧版文本提示）。

---

**第一步：搜索方式**

问：搜歌用什么？

选项：WebSearch（默认免费）/ Exa API / Tavily API / Spotify API

选 WebSearch 直接下一步。选了需要 Key 的 API 时，紧接着问 Key。

先用 AskUserQuestion 给两个选项：「我有 Key」和「跳过」。用户选「我有 Key」后，让对方直接在对话里发 Key（如「Key 是 xxx」）。收到后用 `--test-api` 验证：

```bash
python -X utf8 scripts/main.py --test-api "API名称" --api-key "用户给的Key"
```

Spotify 需要 Client ID + Client Secret：
```bash
python -X utf8 scripts/main.py --test-api spotify --api-key "ClientID" --client-secret "ClientSecret"
```

测试通过（`success: true`）后启用：

```bash
python -X utf8 scripts/main.py --config-api "api名称"
```

测试失败则告诉用户 Key 不对，让对方重新发。

---

**第二步：推荐时间**

问：什么时间推？

选项：固定时间 / 随机时间 / 不定时 / 跳过

选固定 → 追问时间点（如 18:00）
选随机 → 追问次数和窗口（如每天 1 次，9:00-21:00）

保存：

```bash
python -X utf8 scripts/main.py --set-trigger-time "18:00,20:00"
# 或
python -X utf8 scripts/main.py --random --count 2 --window-start 10:00 --window-end 22:00
```

选「跳过」或「不定时」则不定时，只手动触发。

---

**第三步：语言风格**

问：推荐时用什么语气？

选项：默认 / 用人格文件 / 跳过

选人格文件 → 追问路径，调：

```bash
python -X utf8 scripts/main.py --personality "人格文件路径"
```

---

三步走完后，标记配置完成：

```bash
python -X utf8 scripts/main.py --config-save '{"first_run":false}'
```

然后继续第一步推荐流程。

非首次运行跳过整个第零步。

### 第一步：读取对话历史

用 Read 工具读取当天的对话历史。了解今天用户聊了什么。

如果读不到历史记录，改用随机推荐模式。

### 第二步：获取天气（可选）

天气会影响推荐，但不是必须的。按以下顺序：

**首次推荐时**，先问用户要不要用天气（用平台对应的交互方式问）。用户同意的话，记下城市，以后就不用再问了；用户拒绝就跳过。

**有城市后**，按优先级获取天气：
1. 如果系统有 weather skill → 调用它
2. 没有就用 WebSearch 查当天天气
3. 都查不到就跳过

### 第三步：分析情绪和主题

你来分析对话的语气。不要用脚本，你自己判断：

- **情绪**：positive（积极）/ negative（低落）/ neutral（平稳）/ calm（安静）
- **主题**：work（工作）/ life（生活）/ study（学习）/ entertainment（娱乐）/ love（情感）
- **关键词**：对话中出现的几个核心词
- 有天气的话，把天气状况纳入情绪判断

### 第四步：决定搜索策略

根据情绪和主题，自己设计 3-5 个有差异化的搜索词。

**要求**：
- 每个搜索词角度不同（按情绪、按风格、按语种、按年代等）
- 避免直接搜"抖音热歌"、"网络神曲"之类的词
- 可以搜英文、日文、韩文等外语歌曲
- 可以搜独立音乐人、小众风格
- 参考用户历史评分记录来规避踩过的雷——优先推荐喜欢的歌手和风格，避开不喜欢的
- 每次开始前先看 `data/user_preferences.json`，了解用户口味变化

**示例**（只是示例，每次都要自己想新的）：
```
英美独立摇滚 冷门佳作
治愈系日语歌曲
jazz hiphop 深夜
90年代经典 女声
```

### 第五步：搜索歌曲

用 WebSearch 工具或调用脚本搜索。如果用户配置了 Spotify / Exa / Tavily API，优先用 API 搜（曲库更全、元数据更准）。

对每个搜索结果：
1. 看歌名和歌手
2. 过滤掉抖音热歌、网络神曲、口水歌
3. 挑出最符合当前情绪的那首
4. 不要推荐链接（链接容易失效）

如果搜索不到满意的结果，就换一批搜索词再搜。

### 第六步：写开场白

自己写开场白，不要用模板。结合以下元素自由发挥：

- 当前情绪和主题
- 天气（如果有）
- 人格风格（如果配置了人格文件）
- 歌曲名

**要求**：
- 每次都不一样
- 自然、不套路
- 不要用句号结尾
- 如果有人在格文件，用它的语气说

### 第七步：输出推荐

**严格按照下面模板输出，只替换 `{{占位符}}` 里的内容，其他任何字符（包括分隔线、emoji、行距）都不改。**

```
{{一句自然开场白，不要用句号结尾}}

---

🎵 今日音乐推荐

🎶 歌曲信息

歌名：《{{歌名}}》
歌手：{{歌手名}}
专辑：{{专辑名}}
发行日期：{{年份}}
风格：{{风格}}

💡 推荐理由
{{为什么这首歌适合现在的你，不要说网上都说好}}

---

满分10分，回复数字即可，也可以带上评价，例如：8 很好听
写下你的感受能帮助我更好地了解你的喜好

🎵 享受《{{歌名}}》带来的感动
```

### 第八步：处理评分

用户回复评分后做两件事：

**① 存评分** — 追加一行到 `scripts/../data/.ratings_log`：
```json
{"song":{"name":"歌名","artist":"歌手","genre":"风格"},"rating":8,"feedback":"很好听"}
```

**② 更新偏好** — 读 `scripts/../data/user_preferences.json`，按规则更新：
- 评分 ≥7 → 歌手没在 `favorite_artists` 就加上，风格没在 `favorite_genres` 就加上
- 评分 ≤3 → 加到 `disliked_songs`（格式 `"歌手 - 歌名"`）
- 写回文件

偏好文件格式：
```json
{"favorite_artists":["歌手A"],"favorite_genres":["风格"],"disliked_songs":["歌手B - 歌名"]}
```

**规则：**
- 评分范围 1-10，超出不记
- 写不了就跳过，不强求
- 如果脚本可用也可以用：`python -X utf8 scripts/main.py --rate "歌名" 8 --feedback "很好听" --artist "歌手"`
- 下次推荐时会读偏好来调优，所以偏好一定要更新

## 推荐规则

### ✅ 推荐（范围要广）
- **不限风格**：流行、摇滚、电子、民谣、爵士、R&B、嘻哈、古典、金属、雷鬼……都可以
- **不限语言**：中文、英文、日文、韩文、法文、西班牙文……都可以
- **不限年代**：80年代经典、90年代金曲、00年代怀旧、最新发行都可以
- **不限热度**：热门歌手也可以，只要歌本身有质量
- 唯一标准：**歌好听、有诚意、不是流水线产物**

### ❌ 过滤（只过滤这些）
- 抖音热歌、网络神曲
- 口水歌、洗脑旋律、15秒副歌
- 网红歌曲、变装BGM、挑战BGM
- 最近推荐过的歌曲（翻一下历史记录避免重复）

## 情绪参考（只是参考，不是限制）

别被这些限制住，它们只是帮你快速联想。只要是符合情绪的好歌，什么风格都可以。

### 积极向上 → 不限于励志摇滚、轻快民谣、电子舞曲、K-Pop、Indie Pop

### 有些低落 → 不限于治愈系、安静钢琴、后摇、R&B、Ballad

### 平稳正常 → 不限于独立小众、爵士、轻音乐、Indie Folk、Lo-fi

## 后端命令（脚本负责执行，你按需调用）

```bash
# ── 搜索与评分 ──

# 搜索歌曲（返回可用搜索方式和过滤要求）
python -X utf8 scripts/main.py --search "搜索词"

# 保存用户评分
python -X utf8 scripts/main.py --rate "歌名" 8 --feedback "很好听" --artist "歌手名"

# 查看历史评分统计
python -X utf8 scripts/main.py --stats

# ── 配置 ──

# 查看配置状态（含 first_run）
python -X utf8 scripts/main.py --config-status

# 启用 API（逗号分隔：websearch,exa,tavily,spotify）
python -X utf8 scripts/main.py --config-api "exa,spotify"

# 保存任意 JSON 配置
python -X utf8 scripts/main.py --config-save '{"api":"exa","api_key":"xxx"}'

# ── 定时 ──

# 设置固定触发时间
python -X utf8 scripts/main.py --set-trigger-time "18:00,20:00"

# 设置随机触发时间（每天 2 次，10:00-20:00 之间随机）
python -X utf8 scripts/main.py --random --count 2 --window-start 10:00 --window-end 20:00

# ── 其他 ──

# 加载人格文件
python -X utf8 scripts/main.py --personality "path/to/soul.md"

# 测试 API Key 是否有效
python -X utf8 scripts/main.py --test-api tavily --api-key "xxx"
```

## Cron 定时推送专用（Hermes / openclaw）

设置 cron 时直接用下面这段 prompt，AI 会自行搜索推荐：

```
凭你的知识推荐一首歌。必须严格按以下模板输出，只替换{{占位符}}内容，其他任何字符不动：
- 开场白一句，不要用句号结尾
- 歌名用书名号《》
- 推荐理由是写给你的，不是复述网评
- 结尾满分10分那两行一个字都不能改

模板：
{{一句自然开场白，不要用句号结尾}}

---

🎵 今日音乐推荐

🎶 歌曲信息

歌名：《{{歌名}}》
歌手：{{歌手名}}
专辑：{{专辑名}}
发行日期：{{年份}}
风格：{{风格}}

💡 推荐理由
{{为什么这首歌适合现在的你}}

---

满分10分，回复数字即可，也可以带上评价，例如：8 很好听
写下你的感受能帮助我更好地了解你的喜好

🎵 享受《{{歌名}}》带来的感动
```

## 注意事项

1. **不用脚本分析情绪**——你自己判断更准
2. **不用脚本写开场白**——你写得更自然
3. **不用脚本生成搜索词**——你自己想更好
4. **每次推荐都要不同**，避免重复
5. **严格遵守过滤规则**，拒绝抖音热歌、口水歌
6. **不提供收听链接**，让用户在音乐平台搜歌名
7. **推荐完提醒用户打分**，但不是必须的
