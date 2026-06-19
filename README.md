# hertz-myself | 听见自己的频率

音乐推荐 AI 技能 / Music Recommendation Skill — 给 Agent 装上审美，每天推一首好歌。

不推网络热歌，不跟风口水歌。
翻你今天聊了什么，看一眼窗外天气，找一首现在最该听的

## 🎧 它能干嘛

读你的聊天记录，猜你现在什么心情，再结合天气——然后扔一首歌过来。不是短视频里那种洗脑神曲，是真的能沉下心听的。

**盲盒式推送**：每天推送时间不一样，打开就是惊喜。
**打分就行**：听完打个 1-10，越评越准。不打也行。
**不求你**：不会催你打分，不会天天烦你。

## 📦 安装

### Claude Code

直接跟它说「帮我装个技能」：

> 帮我安装 hertz-myself，地址 https://github.com/Rou325/hertz-myself

或者：

```bash
/install-skill hertz-myself.skill
```

Claude Code 没有后台，没法自动推，只能说一声「推荐一首歌」。

### Hermes / openclaw

对 Agent 说：

> 帮我装个技能 hertz-myself，从 https://github.com/Rou325/hertz-myself 拉下来

或者手动：

```bash
git clone https://github.com/Rou325/hertz-myself.git
cp -r hertz-myself ~/.hermes/skills/
```

装完说一声你想什么时间推，Agent 会配好 cron。不用自己搞。

> **去掉 cron 投递头尾**：Hermes 默认会在消息前后加 job_id 和 "To stop or manage..."。跑这个命令就干净了：
> ```bash
> hermes config set cron.wrap_response false
> ```

## 🛠️ 使用指南

### 第一次：告诉它你喜欢什么

说「推荐一首歌」，它会问你几件事（就一次，以后不啰嗦）：

| 问题 | 选项 | 备注 |
|--------|------|------|
| 🔍 用什么搜歌 | WebSearch / Exa / Tavily / Spotify | WebSearch 免费；接 API 搜得更准 |
| ⏰ 什么时间推 | 固定 / 随机 / 手动 | Hermes / openclaw 才能自动推 |
| 🗣️ 什么语气 | 默认 / 自定义人格 | 可以丢个 soul.md 让它学你说话 |
| 🌤️ 要天气吗 | 开 / 关 | 开了给个城市，以后自动看天推荐 |

> 💡 如果你系统里有天气技能（weather skill），配置时记得提一嘴，它会直接调你的天气技能查天气，不用联网搜。

配 API Key 时会自动测试能不能用，不行直接告诉你，不会白配。

### 日常

- **想听歌**：说「推荐一首歌」
- **自动推**（Hermes / openclaw）：到点自动跑完一套
- **打分**：回复 1-10，越评越准。不打也行

## 💌 举个例子

```
今天北京 22°C，阳光挺好
来一首《Midnight City》

---

🎵 Midnight City
🎤 M83
💿 Hurry Up, We're Dreaming
🎸 电子 / Synth-pop

💡 推荐理由：
合成器的音墙像午后阳光穿过百叶窗，
适合在明亮但懒得动的心情里发会儿呆。

满分10分，回复数字就行，也可以带上话
```

## 💰 花多少钱

| 模式 | 用量 | 备注 |
|------|------|------|
| 🔍 带联网搜 | **~19,000 tokens** | 读历史 → 搜歌 → 输出 |
| 📚 纯知识推荐 | **~9,000 tokens** | 不搜网络，直接推 |

DeepSeek V4 Flash 价格：

- 输出：¥2 / 百万 tokens
- 输入（缓存命中）：¥0.02 / 百万 tokens
- 输入（未命中）：¥1 / 百万 tokens

一天推 3 次，一个月 **几毛钱**。

## ⭐ Star History

<a href="https://www.star-history.com/?repos=Rou325%2Fhertz-myself&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=Rou325/hertz-myself&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=Rou325/hertz-myself&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=Rou325/hertz-myself&type=date&legend=top-left" />
 </picture>
</a>

## 📄 License

MIT
