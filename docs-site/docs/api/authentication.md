---
title: Authentication
description: Authentication and authorization
sidebar_position: 4
---

# Authentication

The platform uses JWT-based authentication for API access.

## Getting a Token

### Via API

```http
POST /v1/auth/login
```

**Request Body:**

```json
{
  "username": "user@example.com",
  "password": "your-password"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

### Via CLI

```bash
# Login and store token
cli login --username user@example.com

# Token stored in ~/.config/cli/token.json
```

## Using the Token

Include the token in the Authorization header:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.example.com/v1/skills
```

## Token Refresh

Access tokens expire after 1 hour. Use the refresh token to get a new access token:

```http
POST /v1/auth/refresh
```

**Request Body:**

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

## Token Structure

The JWT token contains:

```json
{
  "sub": "user-123",
  "name": "John Doe",
  "email": "john@example.com",
  "roles": ["user", "developer"],
  "iat": 1706342400,
  "exp": 1706346000
}
```

## Scopes

Tokens can include specific scopes:

| Scope | Description |
|-------|-------------|
| `read:skills` | Read skills |
| `write:skills` | Create/update skills |
| `generate:projects` | Generate projects |
| `admin` | Full access |

Request specific scopes during login:

```http
POST /v1/auth/login?scope=read:skills,write:skills
```

## SDK Examples

### Python

```python
from {{SITE_NAME}} import Client

client = Client(token="YOUR_TOKEN")
skills = client.skills.list()
```

### JavaScript

```javascript
import { Client } from '@{{SITE_SLUG}}/sdk';

const client = new Client({ token: 'YOUR_TOKEN' });
const skills = await client.skills.list();
```

### CLI

```bash
# Login once
cli login

# Token automatically used
cli skills list
```

## Next Steps

- [REST API](./rest.md) - REST endpoints
- [WebSocket](./websocket.md) - Real-time updates
