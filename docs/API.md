# 📡 Faceless Platform API

## Overview

The Faceless Platform API provides programmatic access to all platform features including content creation, voice generation, scheduling, and analytics.

## Base URL

```
https://api.facelessplatform.com/v1
```

## Authentication

All API requests require authentication using Bearer tokens:

```bash
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
     https://api.facelessplatform.com/v1/content
```

## Endpoints

### Content Management

#### Create Content
```http
POST /content
```

**Request Body:**
```json
{
  "template": "modern-tech",
  "script": "Your content script here",
  "voice": "professional-female",
  "schedule": "2024-01-15T10:00:00Z",
  "settings": {
    "duration": 60,
    "quality": "hd",
    "background_music": true
  }
}
```

**Response:**
```json
{
  "id": "content_123",
  "status": "processing",
  "estimated_completion": "2024-01-15T09:02:00Z",
  "download_url": null
}
```

#### Get Content Status
```http
GET /content/{content_id}
```

**Response:**
```json
{
  "id": "content_123",
  "status": "completed",
  "download_url": "https://cdn.facelessplatform.com/content_123.mp4",
  "analytics": {
    "views": 1250,
    "engagement_rate": 0.085
  }
}
```

### Voice Generation

#### List Available Voices
```http
GET /voices
```

#### Generate Voice
```http
POST /voices/generate
```

### Templates

#### List Templates
```http
GET /templates
```

#### Get Template Details
```http
GET /templates/{template_id}
```

### Analytics

#### Get Performance Metrics
```http
GET /analytics/content/{content_id}
```

#### Get Dashboard Data
```http
GET /analytics/dashboard
```

## Rate Limiting

- **Free tier**: 100 requests per hour
- **Pro tier**: 1,000 requests per hour
- **Enterprise**: Custom limits

## Error Handling

```json
{
  "error": {
    "code": "INVALID_TEMPLATE",
    "message": "The specified template does not exist",
    "details": {
      "template_id": "invalid-template"
    }
  }
}
```

## SDKs

### JavaScript
```javascript
import { FacelessPlatform } from '@faceless/platform-js';

const client = new FacelessPlatform({
  apiKey: 'your-api-key'
});

const content = await client.content.create({
  template: 'modern-tech',
  script: 'Hello world!'
});
```

### Python
```python
from faceless_platform import FacelessPlatform

client = FacelessPlatform(api_key='your-api-key')

content = client.content.create(
    template='modern-tech',
    script='Hello world!'
)
```

## Webhooks

Subscribe to events using webhooks:

```http
POST /webhooks
```

**Request:**
```json
{
  "url": "https://yourapp.com/webhook",
  "events": ["content.completed", "content.failed"]
}
```

**Webhook Payload:**
```json
{
  "event": "content.completed",
  "data": {
    "content_id": "content_123",
    "download_url": "https://cdn.facelessplatform.com/content_123.mp4"
  },
  "timestamp": "2024-01-15T10:00:00Z"
}
```

For more details, visit our [complete API documentation](https://docs.facelessplatform.com/api).