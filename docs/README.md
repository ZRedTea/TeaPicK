
<h1 align="center">TeaPicK 学生便利工具</h1>
<div align="center">

<img src="https://img.shields.io/badge/Python-3.12-blue" />
<img src="https://img.shields.io/badge/Platform-Windows-yellow" />
<img src="https://img.shields.io/badge/License-MIT-red" />
<img src="https://img.shields.io/badge/Version-0.3.1-purple" />

</div>

---

## 📋 项目简介

TeaPicK 是一款基于Python的效率工具。用于节省学生们在这方面的时间以用于其他更有用的工作，同时让学生能感受到科技的便捷。

---

## ⚙️ 系统功能

### 🔌 模拟登录
TeaPicK 可以不需要再手动登录，只需要在配置中输入自己的账号密码即可实现自动登录系统

### 🔗 获取课程
TeaPicK 可以根据配置文件获取你需要的课程，来实现业务

### 🧮 线程并发
TeaPicK 可以实现最大8线程的同时进行业务，提高业务效率

---

## 🚧 施工计划

- 修复模拟登陆中的问题
- 使用PyQt6实现GUI

---

## 🚀 快速开始

### 💿 环境要求
- Windows 11 或 Linux 任意发行版
- Python 3.12+
- uv 0.8+

### 📦 克隆项目
```BASH
git clone git@github.com:ZRedTea/TeaPicK.git
cd TeaPicK
```

### 📰 安装依赖
```BASH
uv sync
```

### ⚙️ 修改配置
> Linux环境
```BASH
cd src/TeaPicK/config
nano courseList.json
```

> Windows环境
```BASH
cd src/TeaPicK/config
code courseList.json # VS Code
```

### 🔧 启动项目
```BASH
python src/TeaPicK/application.py
```

---
<div align="center">

如果这个项目帮到了你，请点一下⭐Star!

</div>
