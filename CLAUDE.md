# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**hertz-myself** is an intelligent music recommendation skill that analyzes daily conversations to recommend songs.

## Common Commands

```bash
# Run tests
python -X utf8 tests/test_main.py

# Manual trigger
python -X utf8 scripts/main.py --manual

# View statistics
python -X utf8 scripts/main.py --stats

# Set trigger time
python -X utf8 scripts/main.py --set-trigger-time "18:00"

# Start scheduler
python -X utf8 scripts/main.py --scheduler
```

## Architecture

### Core Modules

1. **main.py** - Main entry point
2. **greeting.py** - Opening greeting generation
3. **search_tools.py** - Search API management
4. **user_rating.py** - User rating system (1-10 scale)
5. **analyze_mood.py** - Mood and theme analysis
6. **weather_detector.py** - Weather skill detection (optional)
7. **personality_detector.py** - Personality file loading (optional)
8. **scheduler.py** - Trigger time management
9. **read_history.py** - Conversation history reading

### Data Flow

```
User Input → History Reading → Mood Analysis → Search Query → Song Recommendation
```

### Configuration Files

- `config/search_config.json` - Search API configuration
- `config/scheduler_config.json` - Trigger time configuration
- `data/user_ratings.json` - User rating history
- `data/user_preferences.json` - User preference learning

## Key Design Decisions

1. **No hardcoded API keys** - All keys stored in config files
2. **Modular architecture** - Each module handles specific functionality
3. **Optional integrations** - Weather and personality are optional
4. **User-driven configuration** - First-run setup asks user preferences
5. **1-10 rating scale** - More granular than traditional 1-5 scale

## Testing

Tests are in `tests/test_main.py` and cover:
- Module imports
- Search tools configuration
- User rating system
- Weather detection
- Mood analysis
- Scheduler functionality
- Config file validation
- Documentation completeness

Run with: `python -X utf8 tests/test_main.py`

## Important Notes

- Use `-X utf8` flag when running Python scripts (Windows encoding)
- First-run configuration is interactive (user selects options)
- No automatic detection of external skills - user provides paths
- Links are not provided in recommendations (they expire)
- Rating prompts encourage users to write feedback
