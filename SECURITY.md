# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by:

1. Opening a GitHub Security Advisory at https://github.com/TDProServices/conversation-analyzer/security/advisories/new
2. Or emailing: [security contact - add your email]

Please include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

## Security Considerations

### Local Processing

Conversation Analyzer is designed with privacy and security in mind:

- **100% Local:** All LLM processing happens locally via Ollama
- **No External APIs:** No data is sent to external services
- **No Network Required:** Can operate completely offline

### Data Storage

- All data is stored in local SQLite database
- File paths and content are stored locally
- No telemetry or analytics are collected

### Input Validation

- All file paths are validated to prevent path traversal
- SQL queries use parameterized statements
- User inputs are validated with Pydantic models

### Dependencies

We regularly monitor dependencies for vulnerabilities:

- Run `pip list --outdated` to check for updates
- Update dependencies: `pip install -r requirements.txt --upgrade`
- Check for known vulnerabilities: `pip-audit` (install separately)

## Best Practices

When using Conversation Analyzer:

1. **Don't commit sensitive data:** Add `.env` and `data/` to `.gitignore`
2. **Review extracted items:** Verify accuracy before acting on high-priority items
3. **Keep Ollama updated:** Security fixes may be released
4. **Use virtual environments:** Isolate dependencies
5. **Set file permissions:** Protect database and reports from unauthorized access

## Disclosure Policy

When we receive a security report:

1. We will confirm receipt within 48 hours
2. We will assess the vulnerability and determine severity
3. We will develop and test a fix
4. We will release a patch and security advisory
5. We will credit the reporter (unless they prefer anonymity)

## Security Updates

Subscribe to:
- GitHub repository watch notifications
- Release notifications
- Security advisories

Thank you for helping keep Conversation Analyzer secure!
