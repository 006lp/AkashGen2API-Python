# AkashGen2API-Python

<div align="center">

[简体中文](https://github.com/006lp/AkashGen2API-Python/blob/main/README_CN.md) | [English](https://github.com/006lp/AkashGen2API-Python) || [JavaScript Version](https://github.com/006lp/AkashGen2API)

</div>

This project provides a proxy service for Akash Network's image generation API. It allows you to generate images through a simple API interface that can be deployed to services like Vercel.

## Features

- Authentication with Bearer tokens
- Image generation via Akash Network
- Direct image viewing through generated URLs
- Docker and Docker Compose support
- Configurable API prefix

## Setup

### Environment Variables

Create a `.env` file with the following variables:

```
API_PREFIX=/ 
API_KEY=your_api_key 
SESSION_TOKEN=your_session_token_from_akash 
BASE_URL=https://your-deployment-url.com
```

### Installation

#### Local Development

1. Clone the repository
2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the application:

```
python main.py
```


#### Docker
```
docker-compose up -d
```

## API Usage

### Authentication

All API endpoints require authentication using a Bearer token:

Authorization: Bearer your_api_key


### Endpoints

- `GET /`: Check if the API is running
- `GET /ping`: Simple health check (returns "pong")
- `POST /v1/chat/completions`: Generate an image
- `GET /images?id=job_id`: View the generated image

### Generate Image

POST /v1/chat/completions Authorization: Bearer your_api_key Content-Type: application/json
```
{ "messages": [ { "role": "user", "content": "a cute girl" } ], "model": "AkashGen", "stream": true }
```

## Deployment

This service can be deployed to any platform that supports Python applications, such as:

- Vercel
- Heroku
- AWS Lambda
- Google Cloud Run
- Self-hosted with Docker

Remember to set the environment variables appropriately for your deployment platform.