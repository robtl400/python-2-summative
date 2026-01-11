"""
Unit tests for the data models (User, Project, Task).
Tests class methods, properties, and data validation.
"""

import unittest
from datetime import datetime
from models import User, Project, Task


class TestUser(unittest.TestCase):
    """Test cases for the User class."""

    def setUp(self):
        """Reset ID counter before each test."""
        User.reset_id_counter()

    def test_user_creation(self):
        """Test creating a new user."""
        user = User(name="Alice", email="alice@example.com")
        self.assertEqual(user.name, "Alice")
        self.assertEqual(user.email, "alice@example.com")
        self.assertEqual(user.id, 1)
        self.assertEqual(len(user.projects), 0)

    def test_user_id_auto_increment(self):
        """Test that user IDs auto-increment."""
        user1 = User(name="Alice", email="alice@example.com")
        user2 = User(name="Bob", email="bob@example.com")
        self.assertEqual(user1.id, 1)
        self.assertEqual(user2.id, 2)

    def test_user_name_setter(self):
        """Test setting user name."""
        user = User(name="Alice", email="alice@example.com")
        user.name = "Alicia"
        self.assertEqual(user.name, "Alicia")

    def test_user_name_validation(self):
        """Test that empty names raise ValueError."""
        user = User(name="Alice", email="alice@example.com")
        with self.assertRaises(ValueError):
            user.name = ""

    def test_user_email_validation(self):
        """Test that invalid emails raise ValueError."""
        user = User(name="Alice", email="alice@example.com")
        with self.assertRaises(ValueError):
            user.email = "invalid-email"

    def test_add_project(self):
        """Test adding a project to a user."""
        user = User(name="Alice", email="alice@example.com")
        user.add_project(1)
        user.add_project(2)
        self.assertEqual(len(user.projects), 2)
        self.assertIn(1, user.projects)
        self.assertIn(2, user.projects)

    def test_add_duplicate_project(self):
        """Test that duplicate projects are not added."""
        user = User(name="Alice", email="alice@example.com")
        user.add_project(1)
        user.add_project(1)
        self.assertEqual(len(user.projects), 1)

    def test_remove_project(self):
        """Test removing a project from a user."""
        user = User(name="Alice", email="alice@example.com")
        user.add_project(1)
        user.remove_project(1)
        self.assertEqual(len(user.projects), 0)

    def test_user_to_dict(self):
        """Test converting user to dictionary."""
        user = User(name="Alice", email="alice@example.com")
        user.add_project(1)
        data = user.to_dict()
        self.assertEqual(data['name'], "Alice")
        self.assertEqual(data['email'], "alice@example.com")
        self.assertEqual(data['projects'], [1])

    def test_user_from_dict(self):
        """Test creating user from dictionary."""
        data = {
            'id': 5,
            'name': 'Alice',
            'email': 'alice@example.com',
            'projects': [1, 2]
        }
        user = User.from_dict(data)
        self.assertEqual(user.id, 5)
        self.assertEqual(user.name, "Alice")
        self.assertEqual(len(user.projects), 2)


class TestProject(unittest.TestCase):
    """Test cases for the Project class."""

    def setUp(self):
        """Reset ID counter before each test."""
        Project.reset_id_counter()

    def test_project_creation(self):
        """Test creating a new project."""
        project = Project(
            title="CLI Tool",
            description="A command-line tool",
            owner_id=1
        )
        self.assertEqual(project.title, "CLI Tool")
        self.assertEqual(project.description, "A command-line tool")
        self.assertEqual(project.owner_id, 1)
        self.assertEqual(project.id, 1)
        self.assertIsNone(project.due_date)

    def test_project_with_due_date(self):
        """Test creating a project with a due date."""
        project = Project(
            title="CLI Tool",
            description="A command-line tool",
            owner_id=1,
            due_date="2024-12-31"
        )
        self.assertIsInstance(project.due_date, datetime)

    def test_project_title_validation(self):
        """Test that empty titles raise ValueError."""
        project = Project(title="CLI Tool", description="Test", owner_id=1)
        with self.assertRaises(ValueError):
            project.title = ""

    def test_add_task(self):
        """Test adding a task to a project."""
        project = Project(title="CLI Tool", description="Test", owner_id=1)
        project.add_task(1)
        project.add_task(2)
        self.assertEqual(len(project.tasks), 2)

    def test_remove_task(self):
        """Test removing a task from a project."""
        project = Project(title="CLI Tool", description="Test", owner_id=1)
        project.add_task(1)
        project.remove_task(1)
        self.assertEqual(len(project.tasks), 0)

    def test_project_to_dict(self):
        """Test converting project to dictionary."""
        project = Project(title="CLI Tool", description="Test", owner_id=1)
        data = project.to_dict()
        self.assertEqual(data['title'], "CLI Tool")
        self.assertEqual(data['owner_id'], 1)

    def test_project_from_dict(self):
        """Test creating project from dictionary."""
        data = {
            'id': 3,
            'title': 'CLI Tool',
            'description': 'Test',
            'owner_id': 1,
            'due_date': None,
            'tasks': [1, 2]
        }
        project = Project.from_dict(data)
        self.assertEqual(project.id, 3)
        self.assertEqual(len(project.tasks), 2)


class TestTask(unittest.TestCase):
    """Test cases for the Task class."""

    def setUp(self):
        """Reset ID counter before each test."""
        Task.reset_id_counter()

    def test_task_creation(self):
        """Test creating a new task."""
        task = Task(title="Implement feature", project_id=1)
        self.assertEqual(task.title, "Implement feature")
        self.assertEqual(task.project_id, 1)
        self.assertEqual(task.status, "pending")
        self.assertEqual(task.id, 1)

    def test_task_title_validation(self):
        """Test that empty titles raise ValueError."""
        task = Task(title="Test", project_id=1)
        with self.assertRaises(ValueError):
            task.title = ""

    def test_task_status_validation(self):
        """Test that invalid status raises ValueError."""
        task = Task(title="Test", project_id=1)
        with self.assertRaises(ValueError):
            task.status = "invalid_status"

    def test_assign_user(self):
        """Test assigning a user to a task."""
        task = Task(title="Test", project_id=1)
        task.assign_user(1)
        task.assign_user(2)
        self.assertEqual(len(task.assigned_to), 2)
        self.assertIn(1, task.assigned_to)

    def test_unassign_user(self):
        """Test unassigning a user from a task."""
        task = Task(title="Test", project_id=1)
        task.assign_user(1)
        task.unassign_user(1)
        self.assertEqual(len(task.assigned_to), 0)

    def test_mark_completed(self):
        """Test marking a task as completed."""
        task = Task(title="Test", project_id=1)
        task.mark_completed()
        self.assertEqual(task.status, "completed")

    def test_mark_in_progress(self):
        """Test marking a task as in progress."""
        task = Task(title="Test", project_id=1)
        task.mark_in_progress()
        self.assertEqual(task.status, "in_progress")

    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(title="Test", project_id=1, status="pending")
        task.assign_user(1)
        data = task.to_dict()
        self.assertEqual(data['title'], "Test")
        self.assertEqual(data['status'], "pending")
        self.assertEqual(data['assigned_to'], [1])

    def test_task_from_dict(self):
        """Test creating task from dictionary."""
        data = {
            'id': 4,
            'title': 'Test',
            'status': 'in_progress',
            'project_id': 1,
            'assigned_to': [1, 2]
        }
        task = Task.from_dict(data)
        self.assertEqual(task.id, 4)
        self.assertEqual(task.status, "in_progress")
        self.assertEqual(len(task.assigned_to), 2)


if __name__ == '__main__':
    unittest.main()
