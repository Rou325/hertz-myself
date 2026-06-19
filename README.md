# hertz-myself | 听见自己的频率

拒绝抖音热歌，告别算法口水歌。
基于你的聊天情绪与当下天气，为你寻找此刻最契合的那首歌。

## ✨ 核心体验

**情绪共振**：读取当日聊天记录，捕捉你未言明的心情。

**环境感知**：结合实时天气与温度，让音乐成为环境的延伸。

**审美过滤**：自动屏蔽短视频神曲与同质化口水歌，只推有质感的作品。

**盲盒惊喜**：支持定时/随机推送，把「听什么」变成一种期待。

**越用越懂**：简单的 1-10 分反馈机制，让推荐精度随时间生长。

## 📦 安装

直接让 Agent 帮你装，不用手动敲命令。

### Claude Code

对 Claude 说：

> 帮我安装 hertz-myself 技能，地址 https://github.com/Rou325/hertz-myself

或者手动：

```bash
/install-skill hertz-myself.skill
```

### Hermes

对 Hermes 说：

> 帮我装个技能 hertz-myself，从 https://github.com/Rou325/hertz-myself 拉下来放到 skills 目录

或者手动：

```bash
git clone https://github.com/Rou325/hertz-myself.git
cp -r hertz-myself ~/.hermes/skills/
```

> ⚠️ Hermes 用户注意：安装后请在配置中启用该 Skill，并务必设置定时调用，否则调度器无法自动触发推送。

## 🎧 使用指南

### 首次启动：定义你的频率

发送「推荐一首歌」，完成一次性偏好设定：

| 配置项 | 选项 | 说明 |
|--------|------|------|
| 🔍 搜索源 | WebSearch（默认）/ Exa / Tavily | WebSearch 免费可用，API 搜索更精准 |
| ⏰ 推送时间 | 固定 / 随机 / 手动 | 随机模式下每天时间点不同，如拆盲盒 |
| 🗣️ 语气风格 | 默认 / 自定义人格 | 可关联 soul.md / personality.md |
| 🌤️ 天气联动 | 开启 / 关闭 | 开启后需提供城市，自动感知阴晴冷暖 |

以上配置仅需一次，后续自动记忆。

### 日常使用

**主动触发**：随时说「推荐一首歌」即可。

**自动推送**：到达预设时间后，自动走完「情绪分析 → 天气查询 → 搜索筛选 → 生成推荐」全流程。

**反馈打分**：收到推荐后回复 1-10 的数字即可调教模型；不打分也不影响使用。

## 💌 推送示例

```
今天北京 22°C，阳光正好
来一首《Midnight City》

---

🎵 Midnight City
🎤 M83
💿 Hurry Up, We're Dreaming
🎸 电子 / Synth-pop

💡 推荐理由：
合成器的迷幻音墙像午后阳光穿过百叶窗，
适合在明亮却慵懒的情绪里短暂出神。

满分10分，回复数字即可，也可以带上评价
```

## 💰 成本估算

单次推荐消耗约 5,000 tokens。以 DeepSeek V4 Flash 为例：

- 输出：¥2 / 百万 tokens
- 输入（缓存命中）：¥0.02 / 百万 tokens

按每日推送 3 次计算，月成本仅需几毛钱。

## 📄 License

MIT
