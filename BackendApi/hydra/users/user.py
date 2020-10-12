"""Create user class for flask_login, may delete later."""
from flask_login import UserMixin


class User(UserMixin):
    """Create User class, inherits from flask-login's user mixin."""

    def __init__(self, id, authToken, firstName, lastName, email, password):
        """Initialize properties of users."""
        self.id = str(id)
        self.authToken = authToken
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.enrolledGroups = []
        self.ownedGroups = []
        self.is_admin = False
        self.is_root = False
        self.stripeId = None
        self.profilePhotoUrl = (
            None  # TODO: Set this to be a default profile image.
        )

    # is_authenticated cannot be camel-cased for Flask-login
    def is_authenticated(self):
        """Set isAuthenticated to true for all signed in users."""
        return True

    def setIsAdmin(self):
        """Set isAdmin to true under certain conditions."""
        pass

    def setIsRoot(self):
        """Set isRoot to true under certain conditions."""
        pass

    def setEnrolledGroups(self):
        """For students, set enrolled groups when they subscribe."""
        pass

    def setOwnedGroups(self):
        """For tutors/instructors, set owned groups when created."""
        pass
