# Akash Network API 代理

<div align="center">

[简体中文](https://github.com/006lp/AkashGen2API-Python/blob/main/README_CN.md) | [English](https://github.com/006lp/AkashGen2API-Python) || [JavaScript Version](https://github.com/006lp/AkashGen2API)

</div>

本项目提供了一个 Akash Network 图像生成 API 的代理服务。它允许您通过简单的 API 接口生成图像，该接口可以部署到 Vercel 等服务上。

## 功能特点

- 使用 Bearer 令牌进行身份验证
- 通过 Akash Network 生成图像
- 通过生成的 URL 直接查看图像
- 支持 Docker 和 Docker Compose
- 可配置的 API 前缀

## 设置

### 环境变量

创建一个包含以下变量的 `.env` 文件：
```
API_PREFIX=/ 
API_KEY=your_api_key 
SESSION_TOKEN=your_session_token_from_akash 
BASE_URL=https://your-deployment-url.com
```

### 安装

#### 本地开发

1. 克隆仓库
2. 安装依赖：
```
pip install -r requirements.txt
```

3. 运行应用程序：
```
python main.py
```

#### Docker
```
docker-compose up -d
```

## API 使用

### 认证

所有 API 端点都需要使用 Bearer 令牌进行身份验证：

Authorization: Bearer your_api_key


### 端点

- `GET /`：检查 API 是否正在运行
- `GET /ping`：简单的健康检查（返回 "pong"）
- `POST /v1/chat/completions`：生成图像
- `GET /images?id=job_id`：查看生成的图像

### 生成图像

POST /v1/chat/completions Authorization: Bearer your_api_key Content-Type: application/json
```
{ "messages": [ { "role": "user", "content": "一个可爱的女孩" } ], "model": "AkashGen", "stream": true }
```

## 部署

此服务可以部署到任何支持 Python 应用程序的平台，例如：

- Vercel
- Heroku
- AWS Lambda
- Google Cloud Run
- 使用 Docker 自托管

记得为您的部署平台适当设置环境变量。