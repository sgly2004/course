# 简介

以复习为主要目的，通过自主生成问题创造知识应用场景，结合艾宾浩斯遗忘曲线这一描述记忆衰退过程的理论合理安排复习，达到及时巩固记忆的效果。

---

# 运行环境

- Python版本：3.11
- MySQL版本：3.8



---

# 快速开始

## 1. OpenAI账号注册

前往 [OpenAI注册页面](https://beta.openai.com/signup) 创建账号，参考这篇 [教程](https://www.pythonthree.com/register-openai-chatgpt/) 可以通过虚拟手机号来接收验证码。创建完账号则前往 [API管理页面](https://beta.openai.com/account/api-keys)创建一个 API Key 并保存。

## 2. 前端启动方式

### Install

```bash
pnpm install
```

### Run

```bash
pnpm dev
```

## 3. 启动MySQL数据库

1. 找到mysql的安装路径：`C:\Program Files\MySQL\MySQL Server 5.6\bin`（我的路径在这里）
2. `mysql -u root -p`（我的默认密码为空，直接回车即可）
3. `net start`（后面应该接服务名，但我的默认服务名为空，直接回车即可）
4. 查看所有的数据库名字：SHOW DATABASES;  选择一个数据库操作： USE ${database_name}（注意：指令均为大写，小写无法识别）
5. 查看当前数据库下所有的表名：SHOW TABLES。
6. 修改`MySQLHandler`中的'user'、'password'、'port'、'database'（这个是数据库名，不是表名。）

## 4. 后端启动方式

### Install

```bash
pip install -r requirements.txt
```

### Run

```bash
uvicorn main:app --reload --port 51717 --host 0.0.0.0
```

## 5. 启动后的设置

- 打开设置页面，添加ChatGPT的API，如果是中转，则需要修改API_BASE。

---

# TODO

- 将已有笔记进行自动重构
- 提炼提纲
- 基于笔记内容进行问答


