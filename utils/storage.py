"""
Storage utilities for persisting data to JSON files.
Handles loading and saving of users, projects, and tasks.
"""

import json
import os
from typing import Dict, List, Any, Optional
from models import User, Project, Task


class DataStore:
    """
    Manages data persistence for the project management system.

    Attributes:
        data_file (str): Path to the JSON data file
        data (Dict): In-memory representation of all data
    """

    def __init__(self, data_file: str = 'store.json'):
        """
        Initialize the DataStore.

        Args:
            data_file (str): Path to the JSON file for data storage
        """
        self.data_file = data_file
        self.data: Dict[str, Any] = {
            'users': [],
            'projects': [],
            'tasks': []
        }
        self.load()

    def load(self) -> None:
        """
        Load data from the JSON file.
        Creates a new file with empty data if file doesn't exist or is malformed.
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    content = f.read().strip()
                    if content:
                        self.data = json.loads(content)
                    else:
                        self.data = {'users': [], 'projects': [], 'tasks': []}

                # Ensure all required keys exist
                if 'users' not in self.data:
                    self.data['users'] = []
                if 'projects' not in self.data:
                    self.data['projects'] = []
                if 'tasks' not in self.data:
                    self.data['tasks'] = []

                # Update ID counters based on loaded data
                self._update_id_counters()
            else:
                # Create new file with empty data
                self.save()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load data file. Starting with empty data. Error: {e}")
            self.data = {'users': [], 'projects': [], 'tasks': []}
            self.save()

    def _update_id_counters(self) -> None:
        """Update class ID counters based on loaded data."""
        if self.data['users']:
            max_user_id = max(u['id'] for u in self.data['users'])
            User._id_counter = max_user_id + 1

        if self.data['projects']:
            max_project_id = max(p['id'] for p in self.data['projects'])
            Project._id_counter = max_project_id + 1

        if self.data['tasks']:
            max_task_id = max(t['id'] for t in self.data['tasks'])
            Task._id_counter = max_task_id + 1

    def save(self) -> None:
        """
        Save data to the JSON file.
        Creates backup and handles errors gracefully.
        """
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except IOError as e:
            print(f"Error: Could not save data to {self.data_file}. Error: {e}")

    def add_user(self, user: User) -> None:
        """
        Add a user to the data store.

        Args:
            user (User): The user object to add
        """
        self.data['users'].append(user.to_dict())
        self.save()

    def get_users(self) -> List[User]:
        """
        Retrieve all users from the data store.

        Returns:
            List[User]: List of all User objects
        """
        return [User.from_dict(u) for u in self.data['users']]

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by ID.

        Args:
            user_id (int): The ID of the user to retrieve

        Returns:
            Optional[User]: The User object if found, None otherwise
        """
        for user_data in self.data['users']:
            if user_data['id'] == user_id:
                return User.from_dict(user_data)
        return None

    def get_user_by_name(self, name: str) -> Optional[User]:
        """
        Retrieve a user by name.

        Args:
            name (str): The name of the user to retrieve

        Returns:
            Optional[User]: The User object if found, None otherwise
        """
        for user_data in self.data['users']:
            if user_data['name'].lower() == name.lower():
                return User.from_dict(user_data)
        return None

    def update_user(self, user: User) -> None:
        """
        Update a user in the data store.

        Args:
            user (User): The user object with updated data
        """
        for i, user_data in enumerate(self.data['users']):
            if user_data['id'] == user.id:
                self.data['users'][i] = user.to_dict()
                self.save()
                return

    def add_project(self, project: Project) -> None:
        """
        Add a project to the data store.

        Args:
            project (Project): The project object to add
        """
        self.data['projects'].append(project.to_dict())
        self.save()

    def get_projects(self) -> List[Project]:
        """
        Retrieve all projects from the data store.

        Returns:
            List[Project]: List of all Project objects
        """
        return [Project.from_dict(p) for p in self.data['projects']]

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """
        Retrieve a project by ID.

        Args:
            project_id (int): The ID of the project to retrieve

        Returns:
            Optional[Project]: The Project object if found, None otherwise
        """
        for project_data in self.data['projects']:
            if project_data['id'] == project_id:
                return Project.from_dict(project_data)
        return None

    def get_project_by_title(self, title: str) -> Optional[Project]:
        """
        Retrieve a project by title.

        Args:
            title (str): The title of the project to retrieve

        Returns:
            Optional[Project]: The Project object if found, None otherwise
        """
        for project_data in self.data['projects']:
            if project_data['title'].lower() == title.lower():
                return Project.from_dict(project_data)
        return None

    def get_projects_by_user(self, user_id: int) -> List[Project]:
        """
        Retrieve all projects owned by a specific user.

        Args:
            user_id (int): The ID of the user

        Returns:
            List[Project]: List of Project objects owned by the user
        """
        return [Project.from_dict(p) for p in self.data['projects']
                if p['owner_id'] == user_id]

    def update_project(self, project: Project) -> None:
        """
        Update a project in the data store.

        Args:
            project (Project): The project object with updated data
        """
        for i, project_data in enumerate(self.data['projects']):
            if project_data['id'] == project.id:
                self.data['projects'][i] = project.to_dict()
                self.save()
                return

    def add_task(self, task: Task) -> None:
        """
        Add a task to the data store.

        Args:
            task (Task): The task object to add
        """
        self.data['tasks'].append(task.to_dict())
        self.save()

    def get_tasks(self) -> List[Task]:
        """
        Retrieve all tasks from the data store.

        Returns:
            List[Task]: List of all Task objects
        """
        return [Task.from_dict(t) for t in self.data['tasks']]

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by ID.

        Args:
            task_id (int): The ID of the task to retrieve

        Returns:
            Optional[Task]: The Task object if found, None otherwise
        """
        for task_data in self.data['tasks']:
            if task_data['id'] == task_id:
                return Task.from_dict(task_data)
        return None

    def get_tasks_by_project(self, project_id: int) -> List[Task]:
        """
        Retrieve all tasks for a specific project.

        Args:
            project_id (int): The ID of the project

        Returns:
            List[Task]: List of Task objects in the project
        """
        return [Task.from_dict(t) for t in self.data['tasks']
                if t['project_id'] == project_id]

    def update_task(self, task: Task) -> None:
        """
        Update a task in the data store.

        Args:
            task (Task): The task object with updated data
        """
        for i, task_data in enumerate(self.data['tasks']):
            if task_data['id'] == task.id:
                self.data['tasks'][i] = task.to_dict()
                self.save()
                return

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task from the data store.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if task was deleted, False otherwise
        """
        for i, task_data in enumerate(self.data['tasks']):
            if task_data['id'] == task_id:
                del self.data['tasks'][i]
                self.save()
                return True
        return False
