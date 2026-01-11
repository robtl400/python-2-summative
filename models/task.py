"""
Task model for the Project Management system.
Represents a task within a project that can be assigned to users.
"""

from typing import Optional, Dict, Any, List


class Task:
    """
    Represents a task in the project management system.

    Attributes:
        _id_counter (int): Class attribute for auto-incrementing task IDs
        id (int): Unique identifier for the task
        title (str): Task title
        status (str): Task status (pending, in_progress, completed)
        project_id (int): ID of the project this task belongs to
        assigned_to (List[int]): List of user IDs assigned to this task
    """

    _id_counter = 1
    VALID_STATUSES = ['pending', 'in_progress', 'completed']

    def __init__(
        self,
        title: str,
        project_id: int,
        status: str = 'pending',
        assigned_to: Optional[List[int]] = None,
        task_id: Optional[int] = None
    ):
        """
        Initialize a new Task instance.

        Args:
            title (str): The task title
            project_id (int): The ID of the project this task belongs to
            status (str): The task status (default: 'pending')
            assigned_to (Optional[List[int]]): List of user IDs assigned to this task
            task_id (Optional[int]): Existing task ID (for loading from file)
        """
        if task_id is None:
            self._id = Task._id_counter
            Task._id_counter += 1
        else:
            self._id = task_id
            if task_id >= Task._id_counter:
                Task._id_counter = task_id + 1

        self._title = title
        self._project_id = project_id
        self._status = status if status in Task.VALID_STATUSES else 'pending'
        self._assigned_to: List[int] = assigned_to if assigned_to else []

    @property
    def id(self) -> int:
        """Get the task's ID."""
        return self._id

    @property
    def title(self) -> str:
        """Get the task's title."""
        return self._title

    @title.setter
    def title(self, value: str):
        """
        Set the task's title.

        Args:
            value (str): New title for the task

        Raises:
            ValueError: If title is empty
        """
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        self._title = value.strip()

    @property
    def status(self) -> str:
        """Get the task's status."""
        return self._status

    @status.setter
    def status(self, value: str):
        """
        Set the task's status.

        Args:
            value (str): New status for the task

        Raises:
            ValueError: If status is not valid
        """
        if value not in Task.VALID_STATUSES:
            raise ValueError(f"Status must be one of {Task.VALID_STATUSES}")
        self._status = value

    @property
    def project_id(self) -> int:
        """Get the ID of the project this task belongs to."""
        return self._project_id

    @property
    def assigned_to(self) -> List[int]:
        """Get the list of user IDs assigned to this task."""
        return self._assigned_to.copy()

    def assign_user(self, user_id: int) -> None:
        """
        Assign a user to this task.

        Args:
            user_id (int): The ID of the user to assign
        """
        if user_id not in self._assigned_to:
            self._assigned_to.append(user_id)

    def unassign_user(self, user_id: int) -> None:
        """
        Unassign a user from this task.

        Args:
            user_id (int): The ID of the user to unassign
        """
        if user_id in self._assigned_to:
            self._assigned_to.remove(user_id)

    def mark_completed(self) -> None:
        """Mark this task as completed."""
        self._status = 'completed'

    def mark_in_progress(self) -> None:
        """Mark this task as in progress."""
        self._status = 'in_progress'

    def mark_pending(self) -> None:
        """Mark this task as pending."""
        self._status = 'pending'

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Task object to a dictionary for JSON serialization.

        Returns:
            Dict[str, Any]: Dictionary representation of the task
        """
        return {
            'id': self._id,
            'title': self._title,
            'status': self._status,
            'project_id': self._project_id,
            'assigned_to': self._assigned_to
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """
        Create a Task object from a dictionary.

        Args:
            data (Dict[str, Any]): Dictionary containing task data

        Returns:
            Task: A new Task instance
        """
        return cls(
            title=data['title'],
            project_id=data['project_id'],
            status=data.get('status', 'pending'),
            assigned_to=data.get('assigned_to', []),
            task_id=data['id']
        )

    @classmethod
    def reset_id_counter(cls) -> None:
        """Reset the ID counter to 1. Useful for testing."""
        cls._id_counter = 1

    def __str__(self) -> str:
        """String representation of the task."""
        return f"Task(id={self._id}, title='{self._title}', status='{self._status}')"

    def __repr__(self) -> str:
        """Detailed string representation of the task."""
        return (f"Task(id={self._id}, title='{self._title}', status='{self._status}', "
                f"project_id={self._project_id}, assigned_to={self._assigned_to})")
