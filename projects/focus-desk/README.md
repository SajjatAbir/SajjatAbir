# Focus Desk

A small Python desktop task app with a navy interface and local JSON storage.

## Run

Install Python 3.10 or newer with Tkinter, then run from this folder:

```sh
python app.py
```

Tkinter is usually included with Python's Windows and macOS installers. Some Linux distributions provide it separately as `python3-tk`.

## Use

1. Enter a task and click **Add task** (or press Enter).
2. Select a task and click **Complete / reopen** (or press Space).
3. Use **All**, **Active**, and **Completed** to filter your list.
4. **Delete selected** removes a task after confirmation.

Tasks save after each change to `~/.focus-desk/tasks.json`. Writes replace the save file atomically. If loading fails, the app preserves the file and displays an error instead of overwriting it. Back up and repair or rename that file before restarting.

This is a single-user learning project. Run one instance at a time. There is no cloud sync, account system, or packaged installer.

## Check storage behavior

```sh
python -m unittest test_app.py
```
