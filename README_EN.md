[🇨🇳 中文](README.md) | [🇬🇧 English](README_EN.md)

# hertz-myself | Hear Your Frequency

A music recommendation skill for your AI agent. Reads your chat mood, checks the weather, and picks a song that actually fits. No TikTok hits, no algorithm junk.

## 🎧 What It Does

Reads what you've been talking about today, figures out your vibe — then throws a song at you. Not the kind that's stuck in everyone's head for 15 seconds. The kind you actually want to listen to.

**Blind-box delivery** — push times change daily, keeps it a surprise.
**Just rate it** — drop a number 1-10, it learns as you go. Skip if you can't be bothered.
**No nagging** — won't bug you to rate, won't spam you.

## 📦 Install

### Claude Code

Just tell it:

> Install the skill hertz-myself from https://github.com/Rou325/hertz-myself

Or manually:

```bash
/install-skill hertz-myself.skill
```

Claude Code can't auto-push — say "recommend a song" when you want one.

### Hermes / openclaw

Tell your agent:

> Install the skill hertz-myself from https://github.com/Rou325/hertz-myself

Or manually:

```bash
git clone https://github.com/Rou325/hertz-myself.git
cp -r hertz-myself ~/.hermes/skills/
```

#### ⏰ Scheduled Push

Agent will set up the cron, no manual work needed

> **Clean up cron output** — Hermes wraps every push with job_id and "To stop or manage...". Run this and it's gone:
> ```bash
> hermes config set cron.wrap_response false
> ```

## 🛠️ How To Use

### First Time: Set Your Preferences

Say "recommend a song" and it'll ask a few things (once, never again):

| What | Options | Notes |
|------|---------|-------|
| 🔍 Search source | WebSearch / Exa / Tavily / Spotify | WebSearch is free; APIs give better results |
| ⏰ Push time | Fixed / Random / Manual | Auto-push works on Hermes / openclaw |
| 🗣️ Tone | Default / Personality file | Drop a soul.md and it'll talk like you |
| 🌤️ Weather | On / Off | Turn it on, give a city, done |

If you set up API keys, it'll test them before saving. Won't let you waste time on a bad key.

### Daily

- **Want a song** — say "recommend a song"
- **Auto-push** (Hermes / openclaw) — runs the full pipeline on schedule
- **Rate** — reply with 1-10, it gets better over time. Skip if you want

## 💌 Example

```
Beijing, 22°C, nice sun
How about 《Midnight City》

---

🎵 Midnight City
🎤 M83
💿 Hurry Up, We're Dreaming
🎸 Electronic / Synth-pop

💡 Why this song:
Synth wall hitting like afternoon sun through blinds,
perfect for a bright-but-lazy mood.

Rate it 1-10, or just say something
```

## 💰 Cost

| Mode | Usage | Notes |
|------|-------|-------|
| 🔍 With web search | **~19,000 tokens** | Full pipeline |
| 📚 Knowledge only | **~9,000 tokens** | No search, direct pick |

At DeepSeek V4 Flash pricing:

- Output: ¥2 / million tokens
- Input (cache hit): ¥0.02 / million tokens
- Input (miss): ¥1 / million tokens

At 3 pushes a day, that's pocket change

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
