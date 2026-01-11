"""
Display utilities for pretty-printing data in the CLI.
Uses the 'rich' library for enhanced terminal output.
"""

from typing import List
from rich.console import Console
from rich.table import Table
from models import User, Project, Task

console = Console()


def display_users(users: List[User]) -> None:
    """
    Display a list of users in a formatted table.

    Args:
        users (List[User]): List of User objects to display
    """
    if not users:
        console.print("[yellow]No users found.[/yellow]")
        return

    table = Table(title="Users")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Email", style="blue")
    table.add_column("Projects", style="magenta")

    for user in users:
        table.add_row(
            str(user.id),
            user.name,
            user.email,
            str(len(user.projects))
        )

    console.print(table)


def display_projects(projects: List[Project], users: List[User] = None) -> None:
    """
    Display a list of projects in a formatted table.

    Args:
        projects (List[Project]): List of Project objects to display
        users (List[User]): Optional list of users for looking up owner names
    """
    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return

    table = Table(title="Projects")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="green")
    table.add_column("Description", style="white")
    table.add_column("Owner", style="blue")
    table.add_column("Due Date", style="yellow")
    table.add_column("Tasks", style="magenta")

    # Create user lookup dict
    user_lookup = {}
    if users:
        user_lookup = {u.id: u.name for u in users}

    for project in projects:
        owner_name = user_lookup.get(project.owner_id, f"ID:{project.owner_id}")
        due_date = project.due_date.strftime('%Y-%m-%d') if project.due_date else "No due date"

        table.add_row(
            str(project.id),
            project.title,
            project.description[:50] + "..." if len(project.description) > 50 else project.description,
            owner_name,
            due_date,
            str(len(project.tasks))
        )

    console.print(table)


def display_tasks(tasks: List[Task], projects: List[Project] = None, users: List[User] = None) -> None:
    """
    Display a list of tasks in a formatted table.

    Args:
        tasks (List[Task]): List of Task objects to display
        projects (List[Project]): Optional list of projects for looking up project names
        users (List[User]): Optional list of users for looking up assignee names
    """
    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    table = Table(title="Tasks")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="green")
    table.add_column("Status", style="white")
    table.add_column("Project", style="blue")
    table.add_column("Assigned To", style="magenta")

    # Create lookup dicts
    project_lookup = {}
    if projects:
        project_lookup = {p.id: p.title for p in projects}

    user_lookup = {}
    if users:
        user_lookup = {u.id: u.name for u in users}

    for task in tasks:
        project_name = project_lookup.get(task.project_id, f"ID:{task.project_id}")

        # Get assigned users
        assigned_names = []
        for user_id in task.assigned_to:
            assigned_names.append(user_lookup.get(user_id, f"ID:{user_id}"))
        assigned_str = ", ".join(assigned_names) if assigned_names else "Unassigned"

        # Color status
        status = task.status
        if status == "completed":
            status_display = f"[green]{status}[/green]"
        elif status == "in_progress":
            status_display = f"[yellow]{status}[/yellow]"
        else:
            status_display = f"[red]{status}[/red]"

        table.add_row(
            str(task.id),
            task.title,
            status_display,
            project_name,
            assigned_str
        )

    console.print(table)


def print_success(message: str) -> None:
    """
    Print a success message.

    Args:
        message (str): The success message to display
    """
    console.print(f"[green]✓ {message}[/green]")


def print_error(message: str) -> None:
    """
    Print an error message.

    Args:
        message (str): The error message to display
    """
    console.print(f"[red]✗ {message}[/red]")


def print_info(message: str) -> None:
    """
    Print an info message.

    Args:
        message (str): The info message to display
    """
    console.print(f"[blue]ℹ {message}[/blue]")
