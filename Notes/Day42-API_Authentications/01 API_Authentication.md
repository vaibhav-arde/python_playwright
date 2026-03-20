# API Authentication uisng Playwright (Python and JS)


## What is Basic Authentication?

Basic Authentication sends **username and password in the Authorization header** (Base64 encoded).

Header format:

```http
Authorization: Basic base64(username:password)
```

Example:

```http
Authorization: Basic dXNlcjpwYXNzd29yZA==
```

In **Playwright**, Basic Auth can be handled in **two main ways**.

---

# 1️⃣ Basic Auth Using `httpCredentials` (Recommended)

Playwright automatically attaches the authentication header.

## JavaScript Example

```javascript
import { test, expect } from '@playwright/test';

test('basic auth example', async ({ browser }) => {

  const context = await browser.newContext({
    httpCredentials: {
      username: 'admin',
      password: 'password123'
    }
  });

  const page = await context.newPage();

  await page.goto('https://example.com');

});
```

Playwright internally sends:

```http
Authorization: Basic base64(admin:password123)
```

---

## Python Example

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()

    context = browser.new_context(
        http_credentials={
            "username": "admin",
            "password": "password123"
        }
    )

    page = context.new_page()
    page.goto("https://example.com")

    browser.close()
```

---

# 2️⃣ Basic Auth in API Requests

When using **Playwright API testing (`APIRequestContext`)**.

## JavaScript

```javascript
import { request } from '@playwright/test';

const apiContext = await request.newContext({
  httpCredentials: {
    username: 'admin',
    password: 'password123'
  }
});

const response = await apiContext.get('/api/users');
```

---

## Python

```python
api_context = playwright.request.new_context(
    http_credentials={
        "username": "admin",
        "password": "password123"
    }
)

response = api_context.get("/api/users")
```

---

# 3️⃣ Manual Header (Alternative Way)

You can manually set the header.

## JavaScript

```javascript
const auth = Buffer.from("admin:password123").toString("base64");

await request.get("/api/users", {
  headers: {
    Authorization: `Basic ${auth}`
  }
});
```

---

## Python

```python
import base64

auth = base64.b64encode(b"admin:password123").decode()

headers = {
    "Authorization": f"Basic {auth}"
}

response = api_context.get("/api/users", headers=headers)
```

---

# How Basic Auth Works (Flow)

```text
Client → Request without auth
Server → 401 Unauthorized
Server → WWW-Authenticate: Basic
Client → Sends Authorization header
Server → Grants access
```

---

# Quick Interview Answer ⭐

If asked:

**How do you handle Basic Authentication in Playwright?**

Best answer:

> In Playwright we handle Basic Authentication using `httpCredentials` while creating a browser context or API request context. Playwright automatically adds the Authorization header with Base64 encoded credentials.

---
---



## 🔐 What is Bearer Token Authentication?

Bearer authentication uses a **token (usually JWT)** to authorize API requests.

Header format:

```http
Authorization: Bearer <token>
```

Example:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

The server checks the token to verify **who the user is and whether they have permission**.

---

# 1️⃣ Bearer Token in Playwright (JavaScript)

The most common way is using **extraHTTPHeaders** when creating a request context.

```javascript
import { request } from '@playwright/test';

const apiContext = await request.newContext({
  extraHTTPHeaders: {
    Authorization: 'Bearer YOUR_ACCESS_TOKEN'
  }
});

const response = await apiContext.get('/api/users');

console.log(await response.json());
```

Now every request automatically sends:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

# 2️⃣ Bearer Token Per Request (JS)

If you want to send the token only for one request:

```javascript
const response = await apiContext.get('/api/users', {
  headers: {
    Authorization: `Bearer ${token}`
  }
});
```

---

# 3️⃣ Bearer Token in Playwright (Python)

Using **extra_http_headers** while creating API context.

```python
api_context = playwright.request.new_context(
    extra_http_headers={
        "Authorization": "Bearer YOUR_ACCESS_TOKEN"
    }
)

response = api_context.get("/api/users")

print(response.json())
```

---

# 4️⃣ Bearer Token Per Request (Python)

```python
response = api_context.get(
    "/api/users",
    headers={
        "Authorization": f"Bearer {token}"
    }
)
```

---

# 5️⃣ Real Automation Flow (Login → Get Token → Use Token)

Most APIs require **login first**.

## JavaScript Example

```javascript
const login = await apiContext.post('/login', {
  data: {
    username: 'admin',
    password: 'password'
  }
});

const token = (await login.json()).token;

const response = await apiContext.get('/orders', {
  headers: {
    Authorization: `Bearer ${token}`
  }
});
```

---

## Python Example

```python
login = api_context.post(
    "/login",
    data={
        "username": "admin",
        "password": "password"
    }
)

token = login.json()["token"]

response = api_context.get(
    "/orders",
    headers={
        "Authorization": f"Bearer {token}"
    }
)
```

---

# 6️⃣ Best Practice (Set Token Globally)

Set it once so **all requests use it automatically**.

### JavaScript

```javascript
const apiContext = await request.newContext({
  extraHTTPHeaders: {
    Authorization: `Bearer ${token}`
  }
});
```

### Python

```python
api_context = playwright.request.new_context(
    extra_http_headers={
        "Authorization": f"Bearer {token}"
    }
)
```

---

# Authentication Flow

```
Client → POST /login
Server → returns token

Client → GET /orders
Authorization: Bearer token
Server → validates token → returns data
```

---

# ⭐ Interview Answer

If asked:

**How do you handle Bearer Token authentication in Playwright?**

Best answer:

> Bearer authentication is handled by sending the token in the `Authorization` header using `Bearer <token>`. In Playwright we usually configure it globally using `extraHTTPHeaders` in the request context or send it per request using the `headers` option.

---

💡 **Senior SDET Tip:**
In large frameworks we usually create an **auth fixture** that:

1. Logs in once
2. Extracts token
3. Stores it
4. Injects it into all API requests automatically

---
---

## 🔑 What is API Key Authentication?

API Key authentication uses a **unique key issued by the server** to identify and authorize the client.

Example API key:

```text
123abcXYZ789
```

The key is usually sent in:

1️⃣ **Header** (most common)
2️⃣ **Query parameter**
3️⃣ **Request body** (rare)

---

# 1️⃣ API Key in Header (Most Common)

Example header:

```http
x-api-key: 123abcXYZ789
```

or

```http
Authorization: ApiKey 123abcXYZ789
```

---

# Playwright Implementation

---

# 2️⃣ API Key Authentication — JavaScript

### Set API key globally (best approach)

```javascript
import { request } from '@playwright/test';

const apiContext = await request.newContext({
  extraHTTPHeaders: {
    "x-api-key": "123abcXYZ789"
  }
});

const response = await apiContext.get("/api/users");

console.log(await response.json());
```

All requests automatically send:

```http
x-api-key: 123abcXYZ789
```

---

### API Key per request

```javascript
const response = await apiContext.get("/api/users", {
  headers: {
    "x-api-key": "123abcXYZ789"
  }
});
```

---

# 3️⃣ API Key Authentication — Python

### Set globally

```python
api_context = playwright.request.new_context(
    extra_http_headers={
        "x-api-key": "123abcXYZ789"
    }
)

response = api_context.get("/api/users")

print(response.json())
```

---

### Per request

```python
response = api_context.get(
    "/api/users",
    headers={
        "x-api-key": "123abcXYZ789"
    }
)
```

---

# 4️⃣ API Key as Query Parameter

Some APIs require the key in URL.

Example request:

```http
GET /users?api_key=123abcXYZ789
```

### JavaScript

```javascript
const response = await apiContext.get("/users", {
  params: {
    api_key: "123abcXYZ789"
  }
});
```

---

### Python

```python
response = api_context.get(
    "/users",
    params={
        "api_key": "123abcXYZ789"
    }
)
```

---

# 5️⃣ API Key as Authorization Header

Some APIs use:

```http
Authorization: ApiKey 123abcXYZ789
```

### JavaScript

```javascript
extraHTTPHeaders: {
  Authorization: "ApiKey 123abcXYZ789"
}
```

---

### Python

```python
extra_http_headers={
    "Authorization": "ApiKey 123abcXYZ789"
}
```

---

# Authentication Flow

```text
Client → API request with API key
Server → validates API key
Server → returns response if valid
```

---

# Quick Interview Answer ⭐

If asked:

**How do you handle API key authentication in Playwright?**

Answer:

> API Key authentication is handled by sending the key either in request headers or query parameters. In Playwright we typically configure it using `extraHTTPHeaders` in the request context so the API key is automatically included in every request.

---

💡 **Senior SDET Tip**

In automation frameworks we usually create an **API client fixture** that automatically injects:

* API key
* bearer token
* common headers

So tests only call:

```python
api_client.get("/orders")
```

instead of repeating headers.
---
---

## 🔐 What is OAuth Authentication?

**OAuth (Open Authorization)** is a protocol that allows applications to **access resources on behalf of a user without exposing the user's credentials**.

Most modern APIs use **OAuth 2.0**.

Common examples:

* Google APIs
* GitHub APIs
* Microsoft APIs

OAuth typically returns an **Access Token**, which is then used as a **Bearer token**.

---

# OAuth Flow (Simplified)

```text
Client → Authorization server (login)
Authorization server → returns access_token
Client → API request with Bearer token
Server → validates token
Server → returns data
```

Example header:

```http
Authorization: Bearer ACCESS_TOKEN
```

---

# 1️⃣ OAuth in Playwright (JavaScript)

Usually the automation flow is:

1. Request token from OAuth server
2. Extract access_token
3. Use token in API requests

### Example

```javascript
import { request } from '@playwright/test';

const authContext = await request.newContext();

const tokenResponse = await authContext.post(
  "https://api.example.com/oauth/token",
  {
    form: {
      grant_type: "client_credentials",
      client_id: "CLIENT_ID",
      client_secret: "CLIENT_SECRET"
    }
  }
);

const token = (await tokenResponse.json()).access_token;

const apiContext = await request.newContext({
  extraHTTPHeaders: {
    Authorization: `Bearer ${token}`
  }
});

const response = await apiContext.get("/users");

console.log(await response.json());
```

---

# 2️⃣ OAuth in Playwright (Python)

### Example

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    request_context = p.request.new_context()

    token_response = request_context.post(
        "https://api.example.com/oauth/token",
        form={
            "grant_type": "client_credentials",
            "client_id": "CLIENT_ID",
            "client_secret": "CLIENT_SECRET"
        }
    )

    token = token_response.json()["access_token"]

    api_context = p.request.new_context(
        extra_http_headers={
            "Authorization": f"Bearer {token}"
        }
    )

    response = api_context.get("/users")

    print(response.json())
```

---

# 3️⃣ OAuth Grant Types (Important for Interviews)

| Grant Type         | Use Case                |
| ------------------ | ----------------------- |
| Authorization Code | User login via browser  |
| Client Credentials | Machine-to-machine APIs |
| Password Grant     | Legacy systems          |
| Refresh Token      | Get new access tokens   |

Most **API automation uses Client Credentials**.

---

# OAuth Example Request

Token request:

```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded
```

Body:

```text
grant_type=client_credentials
client_id=abc
client_secret=xyz
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

---

# Real Automation Flow

```text
Step 1 → Get OAuth token
Step 2 → Store token
Step 3 → Use token in Authorization header
Step 4 → Run API tests
```

---

# ⭐ Interview Answer

If asked:

**How do you handle OAuth authentication in Playwright?**

Best answer:

> In Playwright we first request the OAuth token from the authorization server using client credentials or another OAuth flow. Then we extract the access token from the response and include it in the `Authorization: Bearer` header for all API requests.

---

💡 **Senior SDET Tip**

In production frameworks we usually:

* create **auth fixture**
* fetch OAuth token **once**
* cache it
* refresh when expired

Example pattern:

```python
@pytest.fixture(scope="session")
def token():
```

This avoids generating token for every test.

---
---
