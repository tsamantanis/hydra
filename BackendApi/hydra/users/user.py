"""Dependencies and package import."""
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from hydra import create_app


class User:
    """Create User class."""

    def __init__(self, firstName, lastName, email, password):
        """Initialize properties of users."""
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.enrolledGroups = []
        self.ownedGroups = []
        self.is_admin = False
        self.is_root = False
        self.stripeId = None
        self.bio = None
        self.profilePhotoUrl = (
            None  # TODO: Set this to be a default profile image.
        )

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

    def getResetToken(self, expires_sec=900):
        """Enable 'forgot password' functionality."""
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verifyResetToken(token):
        """Verify that the user enters the correct pass reset token."""
        s = Serializer(app.config["SECRET_KEY"])
        try:
            userId = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)
