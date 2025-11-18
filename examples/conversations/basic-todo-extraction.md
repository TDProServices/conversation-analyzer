# Example Conversation: Basic TODO Extraction

**Purpose:** Demonstrates explicit TODO markers that should extract with 95%+ confidence

**User:** Hey Claude, I'm working on the authentication system. Can you help me review the login flow?

**Claude:** I'd be happy to help review your authentication login flow. To give you the most useful feedback, could you share:

1. The current login endpoint code
2. How you're handling password hashing
3. Session management approach

**User:** Here's the login route:

```python
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:  # TODO: Hash password!
        session['user_id'] = user.id
        return jsonify({"success": True})
    return jsonify({"success": False}), 401
```

**Claude:** I can see several security issues here that need to be addressed:

**CRITICAL ISSUES:**

1. **Password storage:** You're storing passwords in plaintext (`user.password == password`). This is a major security vulnerability.

2. **No rate limiting:** Attackers can attempt unlimited login attempts (brute force attack).

3. **No CSRF protection:** The endpoint is vulnerable to CSRF attacks.

**Recommendations:**

```python
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limiting
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Input validation
    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        session['csrf_token'] = generate_csrf_token()
        return jsonify({"success": True, "csrf_token": session['csrf_token']})

    # Generic error message (don't reveal if user exists)
    return jsonify({"error": "Invalid credentials"}), 401
```

**User:** Thanks! That's really helpful. I'll implement these changes.

TODO: Add password hashing with bcrypt
TODO: Implement rate limiting with Flask-Limiter
TODO: Add CSRF protection for all forms
FIXME: Update User model to use password_hash column instead of password

Also, I noticed the session management might have issues. We should look at that next.

**Claude:** Good catch on the session management. A few things to consider:

1. **Session timeout:** Currently sessions never expire
2. **Secure cookie settings:** Make sure you have:
   - `SESSION_COOKIE_SECURE = True` (HTTPS only)
   - `SESSION_COOKIE_HTTPONLY = True` (prevent XSS)
   - `SESSION_COOKIE_SAMESITE = 'Lax'` (CSRF protection)

**User:** Oh yeah, I need to fix those settings too.

TODO: Configure secure session cookies in config.py
TODO: Add session timeout (30 minutes of inactivity)
TODO: Implement logout endpoint that clears session

I'll work on these tomorrow. Thanks for the help!

---

**Expected Extractions:**

1. TODO: Hash password! (from code comment)
2. TODO: Add password hashing with bcrypt
3. TODO: Implement rate limiting with Flask-Limiter
4. TODO: Add CSRF protection for all forms
5. FIXME: Update User model to use password_hash column instead of password
6. TODO: Configure secure session cookies in config.py
7. TODO: Add session timeout (30 minutes of inactivity)
8. TODO: Implement logout endpoint that clears session

**Expected Confidence:** 95-100% for all (explicit markers)
