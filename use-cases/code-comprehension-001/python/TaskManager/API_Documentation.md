# API Documentation Exercise
**Endpoint:** `POST /api/users/register`
**Language:** Python (Flask)

---

## Table of Contents

1. [Original Endpoint Code](#1-original-endpoint-code)
2. [Comprehensive Endpoint Documentation — Prompt 1](#2-comprehensive-endpoint-documentation--prompt-1)
3. [OpenAPI / Swagger Format — Prompt 2](#3-openapi--swagger-format--prompt-2)
4. [Developer Usage Guide — Prompt 3](#4-developer-usage-guide--prompt-3)
5. [Reflection](#5-reflection)

---

## 1. Original Endpoint Code

```python
@app.route('/api/users/register', methods=['POST'])
def register_user():
    """Register a new user"""
    data = request.get_json()

    # Validate required fields
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'error': 'Missing required field',
                'message': f'{field} is required'
            }), 400

    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            'error': 'Username taken',
            'message': 'Username is already in use'
        }), 409

    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            'error': 'Email exists',
            'message': 'An account with this email already exists'
        }), 409

    # Validate email format
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", data['email']):
        return jsonify({
            'error': 'Invalid email',
            'message': 'Please provide a valid email address'
        }), 400

    # Validate password strength
    if len(data['password']) < 8:
        return jsonify({
            'error': 'Weak password',
            'message': 'Password must be at least 8 characters long'
        }), 400

    # Create new user
    try:
        password_hash = generate_password_hash(data['password'])
        new_user = User(
            username=data['username'],
            email=data['email'].lower(),
            password_hash=password_hash,
            created_at=datetime.utcnow(),
            role='user'
        )
        db.session.add(new_user)
        db.session.commit()

        confirmation_token = generate_confirmation_token(new_user.id)
        try:
            send_confirmation_email(new_user.email, confirmation_token)
        except Exception as e:
            app.logger.error(f"Failed to send confirmation email: {str(e)}")

        user_data = {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'created_at': new_user.created_at.isoformat(),
            'role': new_user.role
        }
        return jsonify({
            'message': 'User registered successfully',
            'user': user_data
        }), 201

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error registering user: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': 'Failed to register user'
        }), 500
```

---

## 2. Comprehensive Endpoint Documentation — Prompt 1

> **Prompt used:**
> *"Please create comprehensive documentation for this API endpoint. Endpoint: POST /api/users/register. Implementation code: [code above]. Please include: a clear description of the endpoint's purpose, request parameters with types and descriptions, response format with status codes and examples, authentication requirements, potential error responses with codes and messages, at least 2 example requests with their responses, and any rate limiting or special considerations."*

---

### POST /api/users/register

**Description**

Registers a new user account in the system. The endpoint validates all input fields, checks for uniqueness of the username and email, hashes the password securely before storage, and triggers a confirmation email to the provided address. On success it returns the newly created user's profile (excluding the password) with HTTP status 201.

---

### Authentication

This endpoint does **not** require authentication. It is publicly accessible and intended for new users who do not yet have an account.

---

### Request

**Method:** `POST`
**URL:** `/api/users/register`
**Content-Type:** `application/json`

#### Request Body Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `username` | string | Yes | The desired username. Must be unique across all accounts. |
| `email` | string | Yes | A valid email address. Must be unique. Stored in lowercase. |
| `password` | string | Yes | The account password. Minimum 8 characters. Stored as a secure hash — never in plain text. |

---

### Response

#### Success — 201 Created

Returned when the user is registered successfully.

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 42,
    "username": "jane_doe",
    "email": "jane@example.com",
    "created_at": "2024-09-15T10:30:00",
    "role": "user"
  }
}
```

#### Response Fields

| Field | Type | Description |
|---|---|---|
| `message` | string | Confirmation message |
| `user.id` | integer | Auto-generated unique user ID |
| `user.username` | string | The registered username |
| `user.email` | string | The registered email (lowercased) |
| `user.created_at` | string (ISO 8601) | Timestamp of account creation in UTC |
| `user.role` | string | Default role assigned — always `"user"` on registration |

---

### Error Responses

| Status Code | Error | Message | Cause |
|---|---|---|---|
| `400` | `Missing required field` | `{field} is required` | One of `username`, `email`, or `password` is absent from the request body |
| `400` | `Invalid email` | `Please provide a valid email address` | The email field does not match a valid email format |
| `400` | `Weak password` | `Password must be at least 8 characters long` | The password is fewer than 8 characters |
| `409` | `Username taken` | `Username is already in use` | Another account already uses the provided username |
| `409` | `Email exists` | `An account with this email already exists` | Another account already uses the provided email |
| `500` | `Server error` | `Failed to register user` | An unexpected server or database error occurred |

---

### Example Requests and Responses

#### Example 1 — Successful Registration

**Request:**
```http
POST /api/users/register
Content-Type: application/json

{
  "username": "jane_doe",
  "email": "Jane@Example.com",
  "password": "SecurePass123"
}
```

**Response — 201 Created:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 42,
    "username": "jane_doe",
    "email": "jane@example.com",
    "created_at": "2024-09-15T10:30:00",
    "role": "user"
  }
}
```

Note: the email is stored and returned in lowercase regardless of how it was submitted.

---

#### Example 2 — Missing Required Field

**Request:**
```http
POST /api/users/register
Content-Type: application/json

{
  "username": "jane_doe",
  "email": "jane@example.com"
}
```

**Response — 400 Bad Request:**
```json
{
  "error": "Missing required field",
  "message": "password is required"
}
```

---

#### Example 3 — Duplicate Username

**Request:**
```http
POST /api/users/register
Content-Type: application/json

{
  "username": "jane_doe",
  "email": "newuser@example.com",
  "password": "AnotherPass99"
}
```

**Response — 409 Conflict:**
```json
{
  "error": "Username taken",
  "message": "Username is already in use"
}
```

---

### Special Considerations

**Email confirmation:** After successful registration, the system attempts to send a confirmation email. If the email service is unavailable, the error is logged server-side but the registration still succeeds and a 201 is returned. The client will not be notified of the email failure.

**Email case handling:** Email addresses are stored in lowercase. `Jane@Example.com` and `jane@example.com` are treated as the same address.

**Password security:** Passwords are never stored or returned in plain text. The endpoint uses `generate_password_hash()` before persisting to the database.

**Default role:** All accounts created through this endpoint are assigned the role `"user"` automatically. Admin roles must be assigned separately.

**Rate limiting:** Not implemented in the current code. It is strongly recommended to add rate limiting to this endpoint in production to prevent spam registrations and brute-force attempts.

---

## 3. OpenAPI / Swagger Format — Prompt 2

> **Prompt used:**
> *"Please convert this API information into a structured OpenAPI document. API details: [documentation from Prompt 1]. I need the documentation to include: endpoint definitions with paths and methods, request parameters and body schemas, response schemas with status codes, example requests and responses, and error handling information. Format the output as a complete, valid OpenAPI document."*

```yaml
openapi: 3.0.3

info:
  title: User Registration API
  description: API for registering new user accounts
  version: 1.0.0

paths:
  /api/users/register:
    post:
      summary: Register a new user
      description: >
        Creates a new user account. Validates input, checks for uniqueness,
        hashes the password, and triggers a confirmation email.
        Returns the created user profile on success.
      operationId: registerUser
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RegisterRequest'
            examples:
              valid_request:
                summary: Valid registration
                value:
                  username: jane_doe
                  email: jane@example.com
                  password: SecurePass123
              missing_password:
                summary: Missing password field
                value:
                  username: jane_doe
                  email: jane@example.com

      responses:
        '201':
          description: User registered successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RegisterSuccess'
              example:
                message: User registered successfully
                user:
                  id: 42
                  username: jane_doe
                  email: jane@example.com
                  created_at: '2024-09-15T10:30:00'
                  role: user

        '400':
          description: Bad request — validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              examples:
                missing_field:
                  summary: Missing required field
                  value:
                    error: Missing required field
                    message: password is required
                invalid_email:
                  summary: Invalid email format
                  value:
                    error: Invalid email
                    message: Please provide a valid email address
                weak_password:
                  summary: Password too short
                  value:
                    error: Weak password
                    message: Password must be at least 8 characters long

        '409':
          description: Conflict — username or email already exists
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              examples:
                username_taken:
                  summary: Username already in use
                  value:
                    error: Username taken
                    message: Username is already in use
                email_exists:
                  summary: Email already registered
                  value:
                    error: Email exists
                    message: An account with this email already exists

        '500':
          description: Internal server error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
              example:
                error: Server error
                message: Failed to register user

components:
  schemas:
    RegisterRequest:
      type: object
      required:
        - username
        - email
        - password
      properties:
        username:
          type: string
          description: Desired username. Must be unique.
          example: jane_doe
        email:
          type: string
          format: email
          description: Valid email address. Must be unique. Stored in lowercase.
          example: jane@example.com
        password:
          type: string
          minLength: 8
          description: Account password. Minimum 8 characters. Never stored in plain text.
          example: SecurePass123

    RegisterSuccess:
      type: object
      properties:
        message:
          type: string
          example: User registered successfully
        user:
          $ref: '#/components/schemas/UserProfile'

    UserProfile:
      type: object
      properties:
        id:
          type: integer
          description: Auto-generated unique user ID
          example: 42
        username:
          type: string
          example: jane_doe
        email:
          type: string
          example: jane@example.com
        created_at:
          type: string
          format: date-time
          description: Account creation timestamp in UTC (ISO 8601)
          example: '2024-09-15T10:30:00'
        role:
          type: string
          description: User role. Always "user" on registration.
          example: user

    ErrorResponse:
      type: object
      properties:
        error:
          type: string
          description: Short error identifier
          example: Missing required field
        message:
          type: string
          description: Human-readable explanation of the error
          example: password is required
```

---

## 4. Developer Usage Guide — Prompt 3

> **Prompt used:**
> *"Please create a developer guide for using this API endpoint. The guide should explain how to: authenticate with the API, properly format requests, handle and interpret responses, deal with common errors, and include example code in Python and JavaScript for making requests. API information: [documentation from Prompt 1]. Target audience: beginner to intermediate developers integrating this API for the first time. Tone: friendly and practical."*

---

### Developer Guide: Registering a User via the API

Welcome! This guide walks you through everything you need to call the `POST /api/users/register` endpoint successfully. Whether you are building a frontend signup form or integrating from a backend service, this guide has you covered.

---

#### Authentication

No authentication is required for this endpoint. It is intentionally public — users cannot log in until they have an account, so no token is needed to call it.

---

#### Formatting Your Request

Send a `POST` request to `/api/users/register` with a JSON body containing three fields:

```
Content-Type: application/json
```

```json
{
  "username": "your_username",
  "email": "your@email.com",
  "password": "yourpassword"
}
```

**Rules to follow:**
- All three fields are required — omitting any one returns a `400` error
- The password must be at least 8 characters
- The email must be a valid format (e.g. `user@domain.com`)
- The username and email must not already be registered

---

#### Example Code

**Python (using `requests`):**

```python
import requests

url = "https://yourapi.com/api/users/register"

payload = {
    "username": "jane_doe",
    "email": "jane@example.com",
    "password": "SecurePass123"
}

response = requests.post(url, json=payload)

if response.status_code == 201:
    user = response.json()["user"]
    print(f"Account created! Welcome, {user['username']} (ID: {user['id']})")
elif response.status_code == 400:
    print(f"Validation error: {response.json()['message']}")
elif response.status_code == 409:
    print(f"Conflict: {response.json()['message']}")
else:
    print(f"Unexpected error: {response.status_code}")
```

---

**JavaScript (using `fetch`):**

```javascript
const registerUser = async () => {
  const response = await fetch("https://yourapi.com/api/users/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username: "jane_doe",
      email: "jane@example.com",
      password: "SecurePass123"
    })
  });

  const data = await response.json();

  if (response.status === 201) {
    console.log(`Welcome, ${data.user.username}! Your ID is ${data.user.id}`);
  } else if (response.status === 400) {
    console.error(`Validation failed: ${data.message}`);
  } else if (response.status === 409) {
    console.error(`Conflict: ${data.message}`);
  } else {
    console.error(`Server error: ${data.message}`);
  }
};

registerUser();
```

---

#### Handling Responses

**On success (201):** You receive the new user's profile. Store the `id` — you will need it to reference this user in future requests.

**On validation error (400):** The `message` field tells you exactly which field failed and why. Display this directly to your user — it is written in plain language.

**On conflict (409):** Either the username or email is already taken. Show the `message` to the user and prompt them to choose a different value.

**On server error (500):** Something went wrong on the server. Do not retry immediately. Log the error and display a generic "please try again later" message to the user.

---

#### Common Errors and How to Fix Them

| Error | Status | What to do |
|---|---|---|
| `Missing required field` | 400 | Check that `username`, `email`, and `password` are all present in your request body |
| `Invalid email` | 400 | Validate the email format on the client side before sending |
| `Weak password` | 400 | Enforce an 8-character minimum in your form before the request is made |
| `Username taken` | 409 | Prompt the user to choose a different username |
| `Email exists` | 409 | Offer a "forgot password" link — the user likely already has an account |
| `Server error` | 500 | Log it, show a friendly retry message, do not expose raw error details to users |

---

#### Things Worth Knowing

**Confirmation email:** After a successful registration, the API sends a confirmation email automatically. If the email service is down, the registration still succeeds — your user has an account but may not receive the email immediately.

**Email case:** You can submit `Jane@Example.com` or `jane@example.com` — the API lowercases it before storing. Both refer to the same account.

**Password:** Never stored in plain text. You do not need to hash it before sending — the API handles that.

**Role:** Every new account gets the role `"user"` by default. You cannot set a different role through this endpoint.

---

## 5. Reflection

**Which parts of the API were most challenging to document?**
The email confirmation behaviour was the trickiest — the code sends an email but catches the failure silently and continues. This is easy to miss when reading the code quickly, but important for developers to know because their users might not receive a confirmation email without any error being returned. Behaviour that is intentionally hidden from the response is the hardest thing to document clearly.

**How were the prompts adjusted for better results?**
Prompt 3 was made more specific by naming both Python and JavaScript as target languages and specifying "beginner to intermediate" as the experience level. Generic prompts like "write a guide" produce generic results. The more the prompt described the audience and their likely pain points, the more practical the output became.

**Which documentation format was most effective?**
The OpenAPI/Swagger format (Prompt 2) is the most useful in a real development workflow because it is machine-readable — it can be pasted directly into tools like Swagger UI, Postman, or Stoplight to generate interactive documentation automatically. The Prompt 1 Markdown format is better for human readers in a README or wiki. Both serve different purposes and complement each other.

**How would this approach fit into a development workflow?**
The most practical integration point is right after an endpoint is written and before it is merged. A developer pastes the implementation code into the three prompts, reviews the output for accuracy against the actual code, and commits the documentation alongside the feature. This keeps documentation in sync with the code and removes the common excuse that documentation takes too long to write.

---