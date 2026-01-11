"""
Unit tests for the DataStore class.
Tests file I/O operations and data persistence.
"""

import unittest
import os
import json
from models import User, Project, Task
from utils.storage import DataStore


class TestDataStore(unittest.TestCase):
    """Test cases for the DataStore class."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_file = 'test_store.json'
        self.store = DataStore(self.test_file)
        User.reset_id_counter()
        Project.reset_id_counter()
        Task.reset_id_counter()

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_datastore_creation(self):
        """Test creating a new DataStore."""
        self.assertTrue(os.path.exists(self.test_file))
        self.assertIn('users', self.store.data)
        self.assertIn('projects', self.store.data)
        self.assertIn('tasks', self.store.data)

    def test_add_and_get_user(self):
        """Test adding and retrieving a user."""
        user = User(name="Alice", email="alice@example.com")
        self.store.add_user(user)

        users = self.store.get_users()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].name, "Alice")

    def test_get_user_by_id(self):
        """Test retrieving a user by ID."""
        user = User(name="Alice", email="alice@example.com")
        self.store.add_user(user)

        retrieved = self.store.get_user_by_id(user.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Alice")

    def test_get_user_by_name(self):
        """Test retrieving a user by name."""
        user = User(name="Alice", email="alice@example.com")
        self.store.add_user(user)

        retrieved = self.store.get_user_by_name("Alice")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.email, "alice@example.com")

    def test_update_user(self):
        """Test updating a user."""
        user = User(name="Alice", email="alice@example.com")
        self.store.add_user(user)

        user.name = "Alicia"
        self.store.update_user(user)

        retrieved = self.store.get_user_by_id(user.id)
        self.assertEqual(retrieved.name, "Alicia")

    def test_add_and_get_project(self):
        """Test adding and retrieving a project."""
        project = Project(title="CLI Tool", description="Test", owner_id=1)
        self.store.add_project(project)

        projects = self.store.get_projects()
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0].title, "CLI Tool")

    def test_get_project_by_title(self):
        """Test retrieving a project by title."""
        project = Project(title="CLI Tool", description="Test", owner_id=1)
        self.store.add_project(project)

        retrieved = self.store.get_project_by_title("CLI Tool")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.owner_id, 1)

    def test_get_projects_by_user(self):
        """Test retrieving projects by user."""
        project1 = Project(title="Project 1", description="Test", owner_id=1)
        project2 = Project(title="Project 2", description="Test", owner_id=1)
        project3 = Project(title="Project 3", description="Test", owner_id=2)

        self.store.add_project(project1)
        self.store.add_project(project2)
        self.store.add_project(project3)

        user_projects = self.store.get_projects_by_user(1)
        self.assertEqual(len(user_projects), 2)

    def test_add_and_get_task(self):
        """Test adding and retrieving a task."""
        task = Task(title="Implement feature", project_id=1)
        self.store.add_task(task)

        tasks = self.store.get_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Implement feature")

    def test_get_tasks_by_project(self):
        """Test retrieving tasks by project."""
        task1 = Task(title="Task 1", project_id=1)
        task2 = Task(title="Task 2", project_id=1)
        task3 = Task(title="Task 3", project_id=2)

        self.store.add_task(task1)
        self.store.add_task(task2)
        self.store.add_task(task3)

        project_tasks = self.store.get_tasks_by_project(1)
        self.assertEqual(len(project_tasks), 2)

    def test_update_task(self):
        """Test updating a task."""
        task = Task(title="Test", project_id=1)
        self.store.add_task(task)

        task.mark_completed()
        self.store.update_task(task)

        retrieved = self.store.get_task_by_id(task.id)
        self.assertEqual(retrieved.status, "completed")

    def test_delete_task(self):
        """Test deleting a task."""
        task = Task(title="Test", project_id=1)
        self.store.add_task(task)

        result = self.store.delete_task(task.id)
        self.assertTrue(result)

        tasks = self.store.get_tasks()
        self.assertEqual(len(tasks), 0)

    def test_persistence(self):
        """Test that data persists across DataStore instances."""
        user = User(name="Alice", email="alice@example.com")
        self.store.add_user(user)

        # Create new store instance
        new_store = DataStore(self.test_file)
        users = new_store.get_users()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].name, "Alice")

    def test_malformed_json_handling(self):
        """Test handling of malformed JSON file."""
        with open(self.test_file, 'w') as f:
            f.write("invalid json content")

        store = DataStore(self.test_file)
        self.assertIn('users', store.data)
        self.assertEqual(len(store.data['users']), 0)


if __name__ == '__main__':
    unittest.main()
