# Example Conversation: Bug Report

**Purpose:** Demonstrates bug mentions that should be tracked

**User:** Users are reporting that they're getting logged out randomly. I can't reproduce it consistently, but it's happening a lot according to support tickets.

**Claude:** Random logouts are frustrating for users. Let's troubleshoot this systematically. A few questions:

1. Are there any error messages in the logs?
2. What's your session configuration?
3. Are there any patterns - specific browsers, times of day, etc?

**User:** Let me check the logs... Here's what I'm seeing:

```
2025-11-18 10:23:45 - WARNING - Session validation failed for user 1847
2025-11-18 10:24:12 - WARNING - Session validation failed for user 2301
2025-11-18 10:25:03 - WARNING - Session validation failed for user 1847
```

Session config:

```python
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
```

**Claude:** I see a potential issue. You're using filesystem sessions, which can cause problems in certain environments. A few questions:

1. Are you running multiple application instances (load balancer)?
2. What happens to the session files when the server restarts?
3. Is the filesystem shared across instances?

**User:** Oh... we're running 3 instances behind a load balancer. The session files are stored locally on each server, not shared.

**Claude:** There's your problem! When a user's request goes to Server A, their session is created there. But the next request might go to Server B, which doesn't have that session file. Hence the "random" logouts.

**Solutions:**

1. **Redis sessions** (recommended):
```python
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
```

2. **Sticky sessions** on load balancer (not recommended - causes uneven load)

3. **Database sessions** (slower but works)

**User:** Ugh, I should have known that. Yeah, we need to switch to Redis sessions ASAP. This is affecting production users.

There's another issue too - sometimes users get a 500 error when uploading profile pictures. I think it's related to file size validation.

**Claude:** What's the error message for the 500 error?

**User:** Looking at the stack trace:

```
Traceback (most recent call last):
  File "app.py", line 156, in upload_profile_picture
    if file.size > MAX_FILE_SIZE:
AttributeError: 'FileStorage' object has no attribute 'size'
```

Oops, I'm checking `.size` but it should be checking the Content-Length header or reading the file.

**Claude:** Right. FileStorage doesn't have a `.size` attribute. You need to either:

```python
# Option 1: Check Content-Length
file_size = request.content_length

# Option 2: Read file to check size
file.seek(0, os.SEEK_END)
file_size = file.tell()
file.seek(0)

if file_size > MAX_FILE_SIZE:
    return "File too large", 413
```

**User:** Thanks. I'll fix that. Also, the error page users see is terrible - it just shows the stack trace in production. We need proper error handlers.

**Claude:** Definitely. You should have custom error pages:

```python
@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {error}")
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404
```

**User:** Yeah, we need that. And we should probably set up error monitoring like Sentry so we know when these errors happen.

Oh, and one more thing - the password reset emails aren't being sent. I think the email configuration is broken since we migrated servers.

**Claude:** What email backend are you using?

**User:** SMTP with SendGrid. But I'm seeing connection timeout errors in the logs.

**Claude:** Check that:
1. SendGrid API key is set in new environment
2. Firewall allows outbound SMTP (port 587)
3. SendGrid account is active and not suspended

**User:** I'll check those. Thanks for the help!

---

**Expected Extractions:**

**Bugs:**
1. Random logouts due to filesystem sessions with load balancer (CRITICAL)
2. 500 error on profile picture upload - incorrect .size attribute check
3. Stack traces visible to users in production (security issue)
4. Password reset emails not sending (email config broken)
5. Email connection timeouts with SendGrid

**Features/TODOs:**
1. Switch to Redis sessions for load-balanced environment (HIGH PRIORITY)
2. Fix file size validation in profile picture upload
3. Implement custom error handlers (500, 404 pages)
4. Set up error monitoring (Sentry or similar)
5. Verify SendGrid configuration in production

**Expected Confidence:**
- Bugs: 90-95% (clearly described, reproducible)
- Fixes: 85-90% (clear action items)

**Expected Priority:** HIGH (affecting production users)
