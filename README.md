# Project Management CLI

Command-line tool for managing users, projects, and tasks.

## Setup

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Commands

Add user:
```
python main.py add-user --name "Alex" --email "alex@example.com"
```

List users:
```
python main.py list-users
```

Add project:
```
python main.py add-project --user "Alex" --title "My Project" --description "Something"
```

List projects:
```
python main.py list-projects
```

Add task:
```
python main.py add-task --project "My Project" --title "Do thing"
```

List tasks:
```
python main.py list-tasks
```

Complete task:
```
python main.py complete-task --id 1
```

## Run Tests
```
python -m unittest discover -v
```

## Files

- main.py - main program
- models/ - classes
- utils/ - helpers
- store.json - data storage

