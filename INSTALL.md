# 🎵 hertz-myself - 安装说明

## 打包文件

打包完成后，会生成以下文件：

### 1. Python 包
- `dist/hertz_myself-2.2.0-py3-none-any.whl` - Wheel 包
- `dist/hertz_myself-2.2.0.tar.gz` - 源码包

### 2. ZIP 包
- `release/hertz-myself_v2.2.0_*.zip` - 完整项目包

## 安装方式

### 方式1：使用 pip 安装（推荐）

```bash
# 安装 Wheel 包
pip install dist/hertz_myself-2.2.0-py3-none-any.whl

# 或者安装源码包
pip install dist/hertz_myself-2.2.0.tar.gz
```

### 方式2：直接使用

```bash
# 解压 ZIP 包
unzip release/hertz-myself_v2.2.0_*.zip

# 进入目录
cd hertz-myself

# 运行
python -X utf8 scripts/main.py --manual
```

### 方式3：开发模式安装

```bash
# 进入项目目录
cd hertz-myself

# 开发模式安装
pip install -e .
```

## 使用方法

### 安装后使用

```bash
# 使用命令行工具
hertz-myself --manual

# 或者使用 Python 模块
python -m scripts.main --manual
```

### 直接使用

```bash
# 进入项目目录
cd hertz-myself

# 运行
python -X utf8 scripts/main.py --manual
```

## 卸载

```bash
# 卸载 pip 安装的包
pip uninstall hertz-myself
```

## 依赖说明

本项目无外部依赖，仅使用 Python 标准库。

### Python 版本要求
- Python 3.7+

### 可选依赖
- 无

## 文件说明

### 核心文件
- `SKILL.md` - 技能说明
- `README.md` - 使用说明
- `CHANGELOG.md` - 版本更新日志
- `VERSION.md` - 版本记录

### 脚本文件
- `scripts/main.py` - 主程序
- `scripts/greeting.py` - 开场白
- `scripts/search_tools.py` - 搜索工具
- `scripts/user_rating.py` - 评分系统
- `scripts/analyze_mood.py` - 情绪分析
- `scripts/weather_detector.py` - 天气检测
- `scripts/personality_detector.py` - 人格检测
- `scripts/scheduler.py` - 定时触发
- `scripts/read_history.py` - 历史读取

### 配置文件
- `config/search_config.json` - 搜索配置
- `config/scheduler_config.json` - 调度配置

### 测试文件
- `tests/test_main.py` - 主测试
- `tests/test_optimization.py` - 优化测试

## 常见问题

### Q: 安装后无法运行？
A: 确保 Python 版本 >= 3.7，并检查是否正确安装。

### Q: 如何更新配置？
A: 编辑 `config/search_config.json` 文件。

### Q: 如何查看日志？
A: 运行时添加 `--verbose` 参数。

### Q: 如何重置配置？
A: 删除 `config/search_config.json` 文件，重新运行。

## 技术支持

如有问题，请查看：
- `README.md` - 使用说明
- `CHANGELOG.md` - 版本更新日志
- `OPTIMIZATION_SUMMARY.md` - 优化总结

---

🎵 享受音乐推荐！
