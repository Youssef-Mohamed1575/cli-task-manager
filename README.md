# CLI Task Manager

A terminal-based task manager written in Python. Add tasks with due dates, browse them week by week, edit or delete them, and track completion status — all from the command line.

## Features

- Add tasks with a name and a due date
- View tasks in a week-by-week calendar layout, with easy navigation to past/future weeks
- Edit a task's name, date, or completion status
- Delete individual tasks or bulk-delete past / completed tasks
- Flexible date entry: exact dates, `today`, or a weekday name
- Personalized greeting with a saved username
- Every command has multiple accepted keywords (see below), so you don't have to remember exact wording

## Requirements

- Python 3.12 or later
- No external dependencies — uses only the standard library (`os`, `datetime`, `time`, `sys`, `json`)

## Files

| File | Purpose |
|---|---|
| `main.py` | The application itself — menus, task logic, input handling |
| `storage.py` | Loads and saves task data to `tasks.json` |
| `tasks.json` | Created automatically on first run; stores your username and tasks |

## Running it

```
python3 main.py
```

On first run, you'll be asked for a username, then dropped into the main menu.

## Basic usage

From the main menu, type a number or a keyword to pick an action (see the full command reference below for every accepted word on every screen):

```
[1] View tasks
[2] New task
[3] Edit task
[4] Delete task
[5] Settings
[e/exit] Exit
```

You can also skip the menu entirely and just type a task name directly at the main menu — the app will offer to add it as a new task.

When adding or editing a task's date, you can type an exact date (`2026-09-15`), the word `today`, or a weekday name like `friday`.

## Data storage

Tasks are stored locally in `tasks.json` in the same folder as `main.py`, in plain JSON:

```json
{
  "username": "Alex",
  "tasks": [
    {"id": 1, "name": "Buy milk", "date": "2026-09-15", "is_done": false}
  ]
}
```

If `tasks.json` doesn't exist yet, it's created automatically on first run. If the file becomes corrupted or unreadable, the app resets to a blank state rather than crashing.

## Known limitations

- Tasks stay in storage indefinitely unless manually pruned or cleared via Settings.
- No recurring tasks, priorities, or tags.
- Single-user, local file storage only — no sync or multi-device support.

## Command reference

All commands are case-insensitive and ignore leading/trailing whitespace.

### Main menu

Typed at the main menu prompt. Anything not matching a keyword below is treated as a new task name.

| Action | Keywords |
|---|---|
| View tasks | `1`, `view`, `show`, `look`, `see`, `quick` |
| New task | `2`, `new`, `add`, `create` |
| Edit task | `3`, `edit`, `change` |
| Delete task | `4`, `del`, `delete`, `remove`, `erase` |
| Settings | `5`, `set`, `username`, `user` |
| Exit app | `6`, `leave`, `exit`, `bye`, `e` |

### Navigation (view / edit / delete screens)

Used on the weekly task list, the edit-task-selection screen, and the delete-task-selection screen.

| Action | Keywords |
|---|---|
| Next week | `next`, `n` |
| Previous week | `previous`, `prev`, `pre`, `p` |
| Return / cancel | `q`, `c`, `e`, `exit`, `cancel`, `back`, `return` |
| Select a task | any number matching a listed task, e.g. `1`, `2`, `3` |

### Edit-task screen

Used once a specific task is selected for editing.

| Action | Keywords |
|---|---|
| Edit name | `1`, `name`, `n` |
| Edit date | `2`, `date`, `d` |
| Edit status | `3`, `status`, `s` |
| Return / cancel | `q`, `c`, `e`, `exit`, `cancel`, `back`, `return` |

### Settings screen

| Action            | Keywords                                          |
|-------------------|---------------------------------------------------|
| Change username   | `1`, `username`, `change`, `name`                 |
| Delete past tasks | `2`, `pre`, `prev`                                |
| Delete done tasks | `3`, `done`                                       |
| Return / cancel   | `q`, `c`, `e`, `exit`, `cancel`, `back`, `return` |

### Yes / no prompts

Used for every confirmation (deleting a task, saving a new task, confirming a username change, marking a task done).

| Answer | Keywords |
|---|---|
| Yes | `yes`, `ye`, `yeah`, `ok`, `y` |
| No | `no`, `nah`, `na`, `nope`, `exit`, `n` |

If the input doesn't match either list, you'll be asked again until it does.

### Date input

When prompted for a date (creating or editing a task), any of the following are accepted:

- `today` — today's date
- A weekday name or abbreviation, e.g. `friday` or `fri` — resolves to the next occurrence of that day within the coming week
- A date in any of these formats: `DD-MM-YYYY`, `DD/MM/YYYY`, `DD.MM.YYYY`, `YYYY-MM-DD`, `YYYY/MM/DD`, `YYYY.MM.DD`
- `q`, `c`, `e`, `exit`, `cancel`, `back`, `return` — cancels the date entry