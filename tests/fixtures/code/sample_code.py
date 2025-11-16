"""Sample code file with various TODO/FIXME comments."""

class UserService:
    """Handle user-related operations."""

    def __init__(self, db):
        self.db = db

    def authenticate(self, username, password):
        """Authenticate a user.

        TODO: Add rate limiting to prevent brute force attacks
        FIXME: This is vulnerable to SQL injection! Use parameterized queries.
        """
        # This is intentionally bad code for testing extraction
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        return self.db.execute(query)

    def create_user(self, username, email, password):
        """Create a new user.

        BUG: Email validation is not working properly - allows invalid emails
        TODO: Hash passwords before storing
        """
        # TODO: Add email verification
        user = {
            'username': username,
            'email': email,
            'password': password  # Should be hashed!
        }
        return self.db.insert('users', user)

    def get_user_permissions(self, user_id):
        """Get permissions for a user.

        NOTE: We should cache this result for performance
        FEATURE REQUEST: Add role-based access control (RBAC)
        """
        return self.db.query(f"SELECT permissions FROM users WHERE id={user_id}")


# TODO: Create a separate module for authentication logic
# IDEA: Consider using OAuth2 for third-party authentication
