"""
User model for the Project Management system.
Represents a user who can own multiple projects.
"""

from typing import List, Optional, Dict, Any


class User:
    """
    Represents a user in the project management system.

    Attributes:
        _id_counter (int): Class attribute for auto-incrementing user IDs
        id (int): Unique identifier for the user
        name (str): User's name
        email (str): User's email address
        projects (List): List of project IDs assigned to this user
    """

    _id_counter = 1

    def __init__(self, name: str, email: str, user_id: Optional[int] = None):
        """
        Initialize a new User instance.

        Args:
            name (str): The user's name
            email (str): The user's email address
            user_id (Optional[int]): Existing user ID (for loading from file)
        """
        if user_id is None:
            self._id = User._id_counter
            User._id_counter += 1
        else:
            self._id = user_id
            if user_id >= User._id_counter:
                User._id_counter = user_id + 1

        self._name = name
        self._email = email
        self._projects: List[int] = []

    @property
    def id(self) -> int:
        """Get the user's ID."""
        return self._id

    @property
    def name(self) -> str:
        """Get the user's name."""
        return self._name

    @name.setter
    def name(self, value: str):
        """
        Set the user's name.

        Args:
            value (str): New name for the user

        Raises:
            ValueError: If name is empty
        """
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()

    @property
    def email(self) -> str:
        """Get the user's email."""
        return self._email

    @email.setter
    def email(self, value: str):
        """
        Set the user's email.

        Args:
            value (str): New email for the user

        Raises:
            ValueError: If email is invalid
        """
        if not value or '@' not in value:
            raise ValueError("Invalid email address")
        self._email = value.strip()

    @property
    def projects(self) -> List[int]:
        """Get the list of project IDs assigned to this user."""
        return self._projects.copy()

    def add_project(self, project_id: int) -> None:
        """
        Add a project to the user's project list.

        Args:
            project_id (int): The ID of the project to add
        """
        if project_id not in self._projects:
            self._projects.append(project_id)

    def remove_project(self, project_id: int) -> None:
        """
        Remove a project from the user's project list.

        Args:
            project_id (int): The ID of the project to remove
        """
        if project_id in self._projects:
            self._projects.remove(project_id)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the User object to a dictionary for JSON serialization.

        Returns:
            Dict[str, Any]: Dictionary representation of the user
        """
        return {
            'id': self._id,
            'name': self._name,
            'email': self._email,
            'projects': self._projects
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """
        Create a User object from a dictionary.

        Args:
            data (Dict[str, Any]): Dictionary containing user data

        Returns:
            User: A new User instance
        """
        user = cls(
            name=data['name'],
            email=data['email'],
            user_id=data['id']
        )
        user._projects = data.get('projects', [])
        return user

    @classmethod
    def reset_id_counter(cls) -> None:
        """Reset the ID counter to 1. Useful for testing."""
        cls._id_counter = 1

    def __str__(self) -> str:
        """String representation of the user."""
        return f"User(id={self._id}, name='{self._name}', email='{self._email}')"

    def __repr__(self) -> str:
        """Detailed string representation of the user."""
        return f"User(id={self._id}, name='{self._name}', email='{self._email}', projects={len(self._projects)})"
