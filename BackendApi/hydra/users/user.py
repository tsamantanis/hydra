"""Create user class for utility, may delete later."""


class User:
    """Create User class."""

    def __init__(self, id, firstName, lastName, email, password):
        """Initialize properties of users."""
        self.id = str(id)
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
