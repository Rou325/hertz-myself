from setuptools import setup, find_packages

setup(
    name="hertz-myself",
    version="2.2.0",
    author="hertz-myself",
    description="听见自己的频率 - 智能音乐推荐系统",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        # 无外部依赖，使用 Python 标准库
    ],
    entry_points={
        "console_scripts": [
            "hertz-myself=scripts.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio",
    ],
)
