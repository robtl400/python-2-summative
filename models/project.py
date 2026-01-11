"""
Project model for the Project Management system.
Represents a project owned by a user with multiple tasks.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from dateutil import parser


class Project:
    """
    Represents a project in the project management system.

    Attributes:
        _id_counter (int): Class attribute for auto-incrementing project IDs
        id (int): Unique identifier for the project
        title (str): Project title
        description (str): Project description
        due_date (datetime): Project due date
        owner_id (int): ID of the user who owns this project
        tasks (List[int]): List of task IDs associated with this project
    """

    _id_counter = 1

    def __init__(
        self,
        title: str,
        description: str,
        owner_id: int,
        due_date: Optional[str] = None,
        project_id: Optional[int] = None
    ):
        """
        Initialize a new Project instance.

        Args:
            title (str): The project title
            description (str): The project description
            owner_id (int): The ID of the user who owns this project
            due_date (Optional[str]): Due date string (will be parsed)
            project_id (Optional[int]): Existing project ID (for loading from file)
        """
        if project_id is None:
            self._id = Project._id_counter
            Project._id_counter += 1
        else:
            self._id = project_id
            if project_id >= Project._id_counter:
                Project._id_counter = project_id + 1

        self._title = title
        self._description = description
        self._owner_id = owner_id
        self._due_date = self._parse_date(due_date) if due_date else None
        self._tasks: List[int] = []

    @staticmethod
    def _parse_date(date_string: str) -> Optional[datetime]:
        """
        Parse a date string into a datetime object.

        Args:
            date_string (str): Date string to parse

        Returns:
            Optional[datetime]: Parsed datetime or None if parsing fails
        """
        try:
            return parser.parse(date_string)
        except (ValueError, TypeError):
            return None

    @property
    def id(self) -> int:
        """Get the project's ID."""
        return self._id

    @property
    def title(self) -> str:
        """Get the project's title."""
        return self._title

    @title.setter
    def title(self, value: str):
        """
        Set the project's title.

        Args:
            value (str): New title for the project

        Raises:
            ValueError: If title is empty
        """
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        self._title = value.strip()

    @property
    def description(self) -> str:
        """Get the project's description."""
        return self._description

    @description.setter
    def description(self, value: str):
        """
        Set the project's description.

        Args:
            value (str): New description for the project
        """
        self._description = value.strip() if value else ""

    @property
    def due_date(self) -> Optional[datetime]:
        """Get the project's due date."""
        return self._due_date

    @due_date.setter
    def due_date(self, value: str):
        """
        Set the project's due date.

        Args:
            value (str): Date string to parse and set
        """
        self._due_date = self._parse_date(value)

    @property
    def owner_id(self) -> int:
        """Get the ID of the user who owns this project."""
        return self._owner_id

    @property
    def tasks(self) -> List[int]:
        """Get the list of task IDs associated with this project."""
        return self._tasks.copy()

    def add_task(self, task_id: int) -> None:
        """
        Add a task to the project's task list.

        Args:
            task_id (int): The ID of the task to add
        """
        if task_id not in self._tasks:
            self._tasks.append(task_id)

    def remove_task(self, task_id: int) -> None:
        """
        Remove a task from the project's task list.

        Args:
            task_id (int): The ID of the task to remove
        """
        if task_id in self._tasks:
            self._tasks.remove(task_id)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Project object to a dictionary for JSON serialization.

        Returns:
            Dict[str, Any]: Dictionary representation of the project
        """
        return {
            'id': self._id,
            'title': self._title,
            'description': self._description,
            'owner_id': self._owner_id,
            'due_date': self._due_date.isoformat() if self._due_date else None,
            'tasks': self._tasks
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        """
        Create a Project object from a dictionary.

        Args:
            data (Dict[str, Any]): Dictionary containing project data

        Returns:
            Project: A new Project instance
        """
        project = cls(
            title=data['title'],
            description=data['description'],
            owner_id=data['owner_id'],
            due_date=data.get('due_date'),
            project_id=data['id']
        )
        project._tasks = data.get('tasks', [])
        return project

    @classmethod
    def reset_id_counter(cls) -> None:
        """Reset the ID counter to 1. Useful for testing."""
        cls._id_counter = 1

    def __str__(self) -> str:
        """String representation of the project."""
        due = self._due_date.strftime('%Y-%m-%d') if self._due_date else 'No due date'
        return f"Project(id={self._id}, title='{self._title}', due={due})"

    def __repr__(self) -> str:
        """Detailed string representation of the project."""
        return (f"Project(id={self._id}, title='{self._title}', "
                f"owner_id={self._owner_id}, tasks={len(self._tasks)})")
