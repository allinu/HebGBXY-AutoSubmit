# HebGBXY-AutoSubmit

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP8-brightgreen.svg)](https://www.python.org/dev/peps/pep-0008/)

## 📖 项目简介

HebGBXY-AutoSubmit 是一个学习平台的自动化工具，能够自动提交课程学习记录，帮助用户高效完成在线学习任务。

### ✨ 主要特性

- 🔄 **自动提交**：自动识别课程列表并提交学习记录
- ⚡ **多线程处理**：支持并发处理多个课程
- 🔒 **安全可靠**：使用会话认证，保护用户隐私
- 📊 **详细日志**：实时显示处理进度和结果
- ⚙️ **灵活配置**：可自定义请求延迟、默认时长等参数
- 🛡️ **错误处理**：完善的异常处理和重试机制

## 🚀 快速开始

### 环境要求

- Python 3.13 或更高版本

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/yourusername/HebGBXY-AutoSubmit.git
   cd HebGBXY-AutoSubmit
   ```

2. **安装依赖**
   ```bash
   # 使用 uv（推荐）
   uv sync
   
   # 或使用 pip
   pip install beautifulsoup4 requests
   ```

3. **配置项目**
   - 打开 `HebGBXY-AutoSubmit.py` 文件
   - 修改 `SESSION` 和 `URL` 配置（详见配置说明）

4. **运行程序**
   ```bash
   python HebGBXY-AutoSubmit.py
   ```

## ⚙️ 配置说明

### 必需配置

在 `HebGBXY-AutoSubmit.py` 文件中找到以下配置项并进行修改：

```python
# TODO SESSION cookie值
SESSION = "your_session_cookie_here"

# TODO 课程列表URL
URL = "https:///student/class_detail_course.do?cid=<课程ID>&elective_type=1&menu=myclass&tab_index=0"
```

### 可选配置

```python
# 请求延迟（秒），避免请求过快被封
REQUEST_DELAY = 10

# 默认视频时长（秒），当无法解析到分钟数时使用
DEFAULT_DURATION = 1800

# SSL证书验证（如果遇到证书错误，可以设置为False）
VERIFY_SSL = False
```

### 如何获取 SESSION

1. 登录河北网络干部学院平台
2. 打开浏览器开发者工具（F12）
3. 进入 Network（网络）标签页
4. 刷新页面或进行任意操作
5. 找到任意请求，查看 Request Headers 中的 Cookie
6. 复制 `SESSION=` 后面的值

### 如何获取课程 URL

1. 登录河北网络干部学院平台
2. 进入"我的课程"页面
3. 选择需要自动学习的课程
4. 复制浏览器地址栏中的 URL

## 📖 使用指南

### 基本使用

1. **配置参数**：按照上述说明配置 `SESSION` 和 `URL`
2. **运行程序**：执行 `uv run HebGBXY-AutoSubmit.py`
3. **查看结果**：程序将显示处理进度和最终结果

### 输出示例

```
[2024-03-24 15:11:14] 河北网络干部学院自动提交程序启动
==================================================
[2024-03-24 15:11:14] SESSION: abcdef1234567890...
[2024-03-24 15:11:14] URL: https:///student/class_detail_course.do?cid=12345
[2024-03-24 15:11:14] User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Apple...
[2024-03-24 15:11:14] 请求延迟: 10秒
[2024-03-24 15:11:14] 默认时长: 1800秒
==================================================
[2024-03-24 15:11:14] 开始处理课程...
[2024-03-24 15:11:14] 找到 5 个课程记录
[2024-03-24 15:11:14] 处理第 1/5 个课程: ID=1001, 课程ID=2001
[2024-03-24 15:11:15] 课程页面 id=1001 访问成功
[2024-03-24 15:11:16] 资源清单 course=2001 获取成功
[2024-03-24 15:11:17] [✓] 提交记录 ID=1001, 课程=2001 成功
...
==================================================
[2024-03-24 15:12:14] 处理完成: 成功 5 个，失败 0 个，总计 5 个
==================================================
```

### 高级功能

#### 自定义请求延迟
如果遇到请求频率限制，可以增加 `REQUEST_DELAY` 值：
```python
REQUEST_DELAY = 15  # 增加延迟到15秒
```

#### 处理特定课程
可以通过修改 URL 参数来指定特定课程：
```python
URL = "https://www.hebgb.gov.cn/student/class_detail_course.do?cid=12345&elective_type=1&menu=myclass&tab_index=0"
```

## 🔧 项目结构

```
HebGBXY-AutoSubmit/
├── HebGBXY-AutoSubmit.py    # 主程序文件
├── README.md                # 项目说明文档
├── pyproject.toml           # 项目配置和依赖
├── uv.lock                  # 依赖锁定文件
├── .gitignore              # Git忽略文件
├── .python-version         # Python版本指定
└── .venv/                  # 虚拟环境目录（可选）
```

### 核心模块说明

- **`submit_data()`**：主提交函数，初始化请求并启动处理线程
- **`process_requests()`**：核心处理逻辑，解析课程并提交记录
- **`print_output()`**：格式化输出函数，提供时间戳和日志信息

## 🐛 故障排除

### 常见问题

#### Q1: 程序提示"请先修改代码开头的SESSION配置"
**A**: 需要按照配置说明获取并设置正确的 SESSION 值。

#### Q2: 程序运行后没有找到任何课程记录
**A**: 检查以下事项：
1. URL 是否正确（需要是课程详情页URL）
2. SESSION 是否有效（可能已过期）
3. 网络连接是否正常

#### Q3: 提交记录失败，返回状态码非200
**A**: 可能是以下原因：
1. 课程ID不正确
2. 服务器限制请求频率（尝试增加 `REQUEST_DELAY`）
3. 平台更新导致接口变化

#### Q4: SSL证书验证错误
**A**: 可以设置 `VERIFY_SSL = False`，但请注意安全风险。

### 错误代码说明

| 状态码 | 说明 | 解决方案 |
|--------|------|----------|
| 200 | 请求成功 | - |
| 403 | 禁止访问 | 检查 SESSION 是否有效 |
| 404 | 资源不存在 | 检查 URL 和课程ID |
| 500 | 服务器错误 | 稍后重试或联系平台管理员 |

## ⚠️ 注意事项

### 使用规范
1. **合法使用**：请确保使用本工具符合河北网络干部学院平台的使用规定
2. **学习目的**：本工具旨在辅助学习，不应替代实际学习过程
3. **频率限制**：避免过于频繁的请求，以免对服务器造成压力

### 技术限制
1. **平台变更**：如果河北网络干部学院平台更新，可能需要调整代码
2. **会话过期**：SESSION 有有效期，过期后需要重新获取
3. **网络环境**：需要稳定的网络连接

### 安全提示
1. **保护隐私**：不要分享你的 SESSION 值
2. **定期更新**：关注项目更新，及时获取最新版本
3. **备份配置**：定期备份你的配置文件

## 🔄 更新日志

### v0.1.0 (2024-03-24)
- ✅ 初始版本发布
- ✅ 基础自动提交功能
- ✅ 多线程支持
- ✅ 详细日志输出
- ✅ 可配置参数

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

### 开发流程
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范
- 遵循 PEP 8 代码风格
- 添加适当的注释和文档
- 编写单元测试（如果适用）

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 感谢所有贡献者和用户的支持
- 感谢开源社区提供的工具和库

---

**免责声明**：本工具仅供学习和研究使用，使用者应遵守相关平台规定和法律法规。作者不对因使用本工具而产生的任何后果负责。