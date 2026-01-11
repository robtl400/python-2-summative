#!/usr/bin/env python3
"""
Main entry point for the Project Management CLI tool.
Provides command-line interface for managing users, projects, and tasks.
"""

import argparse
import sys
from models import User, Project, Task
from utils import DataStore, display_users, display_projects, display_tasks
from utils.display import print_success, print_error, print_info


def add_user_command(args, store: DataStore) -> None:
    """
    Add a new user to the system.

    Args:
        args: Parsed command line arguments
        store: DataStore instance
    """
    try:
        # Check if user already exists
        existing_user = store.get_user_by_name(args.name)
        if existing_user:
            print_error(f"User with name '{args.name}' already exists.")
            return

        user = User(name=args.name, email=args.email)
        store.add_user(user)
        print_success(f"User '{user.name}' added successfully with ID {user.id}.")
    except ValueError as e:
        print_error(f"Error creating user: {e}")


def list_users_command(args, store: DataStore) -> None:
    """
    List all users in the system.

    Args:
        args: Parsed command line arguments
        store: DataStore instance
    """
    users = store.get_users()
    display_users(users)


def add_project_command(args, store: DataStore) -> None:
    """
    Add a new project to a user.

    Args:
        args: Parsed command line arguments
        store: DataStore instance
    """
    try:
        # Find user by name
        user = store.get_user_by_name(args.user)
        if not user:
            print_error(f"User '{args.user}' not found.")
            return

        # Check if project already exists
        existing_project = store.get_project_by_title(args.title)
        if existing_project:
            print_error(f"Project with title '{args.title}' already exists.")
            return

        # Create project
        project = Project(
            title=args.title,
            description=args.description if args.description else "",
            owner_id=user.id,
            due_date=args.due_date
        )
        store.add_project(project)

        # Add project to user
        user.add_project(project.id)
        store.update_user(user)

        print_success(f"Project '{project.title}' added successfully with ID {project.id} for user '{user.name}'.")
    except ValueError as e:
        print_error(f"Error creating project: {e}")


def list_projects_command(args, store: DataStore) -> None:
    """
    List all projects or projects for a specific user.

    Args:
        args: Parsed command line arguments
        store: DataStore instance
    """
    if args.user:
        user = store.get_user_by_name(args.user)
        if not user:
            print_error(f"User '{args.user}' not found.")
            return
        projects = store.get_projects_by_user(user.id)
        print_info(f"Projects for user '{user.name}':")
    else:
        projects = store.get_projects()

    users = store.get_users()
    display_projects(projects, users)


def add_task_command(args, store: DataStore) -> None:
    """
    Add a new task to a project.

    Args:
        args: Parsed command line arguments
        store: DataStore instance
    """
    try:
        # Find project by title
        project = store.get_project_by_title(args.project)
        if not project:
            print_error(f"Project '{args.project}' not found.")
            return

        # Create task
        task = Task(
            title=args.title,
            project_id=project.id,
            status='pending'
        )
        store.add_task(task)

        # Add task to project
        project.add_task(task.id)
        store.update_project(project)

        # Assign users if specified
        if args.assign:
            for username in args.assign:
                user = store.get_user_by_name(username)
                if user:
                    task.assign_user(user.id)
                else:
                    print_error(f"Warning: User '{username}' not found. Skipping assignment.")

            store.update_task(task)

        print_success(f"Task '{task.title}' added successfully with ID {task.id} to project '{project.title}'.")
    except ValueError as e:
        print_error(f"Error creating task: {e}")


def list_tasks_command(args, store: DataStore) -> None:
    """
    List all tasks or tasks for a specific project.

    Args:
        args: Parsed command line arguments
        store: DataStore instance
    """
    if args.project:
        project = store.get_project_by_title(args.project)
        if not project:
            print_error(f"Project '{args.project}' not found.")
            return
        tasks = store.get_tasks_by_project(project.id)
        print_info(f"Tasks for project '{project.title}':")
    else:
        tasks = store.get_tasks()

    projects = store.get_projects()
    users = store.get_users()
    display_tasks(tasks, projects, users)


def complete_task_command(args, store: DataStore) -> None:
    """
    Mark a task as completed.

    Args:
        args: Parsed command line arguments
        store: DataStore instance
    """
    try:
        task = store.get_task_by_id(args.id)
        if not task:
            print_error(f"Task with ID {args.id} not found.")
            return

        task.mark_completed()
        store.update_task(task)
        print_success(f"Task '{task.title}' marked as completed.")
    except ValueError as e:
        print_error(f"Error updating task: {e}")


def update_task_status_command(args, store: DataStore) -> None:
    """
    Update the status of a task.

    Args:
        args: Parsed command line arguments
        store: DataStore instance
    """
    try:
        task = store.get_task_by_id(args.id)
        if not task:
            print_error(f"Task with ID {args.id} not found.")
            return

        task.status = args.status
        store.update_task(task)
        print_success(f"Task '{task.title}' status updated to '{args.status}'.")
    except ValueError as e:
        print_error(f"Error updating task: {e}")


def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description='Project Management CLI - Manage users, projects, and tasks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s add-user --name "Alex" --email "alex@example.com"
  %(prog)s add-project --user "Alex" --title "CLI Tool" --description "Build a CLI app"
  %(prog)s add-task --project "CLI Tool" --title "Implement add-task"
  %(prog)s complete-task --id 1
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add user command
    add_user_parser = subparsers.add_parser('add-user', help='Add a new user')
    add_user_parser.add_argument('--name', required=True, help='User name')
    add_user_parser.add_argument('--email', required=True, help='User email')

    # List users command
    subparsers.add_parser('list-users', help='List all users')

    # Add project command
    add_project_parser = subparsers.add_parser('add-project', help='Add a new project')
    add_project_parser.add_argument('--user', required=True, help='Owner username')
    add_project_parser.add_argument('--title', required=True, help='Project title')
    add_project_parser.add_argument('--description', help='Project description')
    add_project_parser.add_argument('--due-date', dest='due_date', help='Due date (e.g., 2024-12-31)')

    # List projects command
    list_projects_parser = subparsers.add_parser('list-projects', help='List all projects or projects for a user')
    list_projects_parser.add_argument('--user', help='Filter by username')

    # Add task command
    add_task_parser = subparsers.add_parser('add-task', help='Add a new task to a project')
    add_task_parser.add_argument('--project', required=True, help='Project title')
    add_task_parser.add_argument('--title', required=True, help='Task title')
    add_task_parser.add_argument('--assign', nargs='+', help='Assign to user(s)')

    # List tasks command
    list_tasks_parser = subparsers.add_parser('list-tasks', help='List all tasks or tasks for a project')
    list_tasks_parser.add_argument('--project', help='Filter by project title')

    # Complete task command
    complete_task_parser = subparsers.add_parser('complete-task', help='Mark a task as completed')
    complete_task_parser.add_argument('--id', type=int, required=True, help='Task ID')

    # Update task status command
    update_task_parser = subparsers.add_parser('update-task-status', help='Update task status')
    update_task_parser.add_argument('--id', type=int, required=True, help='Task ID')
    update_task_parser.add_argument('--status', required=True,
                                     choices=['pending', 'in_progress', 'completed'],
                                     help='New status')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Initialize data store
    store = DataStore()

    # Route to appropriate command handler
    commands = {
        'add-user': add_user_command,
        'list-users': list_users_command,
        'add-project': add_project_command,
        'list-projects': list_projects_command,
        'add-task': add_task_command,
        'list-tasks': list_tasks_command,
        'complete-task': complete_task_command,
        'update-task-status': update_task_status_command,
    }

    if args.command in commands:
        commands[args.command](args, store)
    else:
        print_error(f"Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
