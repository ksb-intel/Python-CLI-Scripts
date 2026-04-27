import sys
import os
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress_bar import ProgressBar

console = Console()
DB_FILE = "tasks.txt"


def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f: pass


def format_time(seconds):
    mins, secs = divmod(int(seconds), 60)
    hours, mins = divmod(mins, 60)
    return f"{hours:02d}:{mins:02d}:{secs:02d}"


def load_tasks():
    if not os.path.exists(DB_FILE): return []
    with open(DB_FILE, "r") as f:
        return [line.strip() for line in f.readlines()]


def save_tasks(tasks):
    with open(DB_FILE, "w") as f:
        for task in tasks:
            f.write(task + "\n")


def add_task(description, goal_minutes=60):
    tasks = load_tasks()
    task_id = len(tasks) + 1
    goal_seconds = int(goal_minutes) * 60
    # Format: ID | Desc | Status | Total | Start | Goal
    new_task = f"{task_id} | {description} | [ ] | 0 | 0 | {goal_seconds}"
    tasks.append(new_task)
    save_tasks(tasks)
    console.print(f"[bold green]✔[/bold green] Added: [cyan]{description}[/cyan] (Goal: {goal_minutes}m)")


def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = []
    found = False
    for task in tasks:
        parts = task.split(" | ")
        if parts[0] == str(task_id):
            found = True
            continue
        new_tasks.append(task)

    # Re-index IDs so they stay 1, 2, 3...
    reindexed = []
    for i, task in enumerate(new_tasks, 1):
        parts = task.split(" | ")
        parts[0] = str(i)
        reindexed.append(" | ".join(parts))

    save_tasks(reindexed)
    if found:
        console.print(f"[bold red]✘[/bold red] Task {task_id} deleted and list re-indexed.")
    else:
        console.print(f"[red]Task {task_id} not found.[/red]")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        console.print("[yellow]Your task list is empty![/yellow]")
        return

    table = Table(title="🚀 Task Dashboard", header_style="bold magenta", expand=True)
    table.add_column("ID", justify="center", style="dim")
    table.add_column("Task", style="white", width=20)
    table.add_column("Time Spent", justify="right", style="green")
    table.add_column("Progress", justify="center", width=30)
    table.add_column("Status", justify="center")

    for task in tasks:
        parts = task.split(" | ")
        total_time = float(parts[3])
        goal_time = float(parts[5]) if len(parts) > 5 else 3600  # Default 1hr if missing

        if parts[4] != "0":  # If running
            total_time += time.time() - float(parts[4])
            status = "[bold blue]RUNNING[/bold blue]"
        else:
            status = "[grey50]PAUSED[/grey50]"

        # Calculate progress percentage
        percentage = min(total_time / goal_time, 1.0)

        table.add_row(
            parts[0],
            parts[1],
            format_time(total_time),
            ProgressBar(total=1.0, completed=percentage, width=25),
            status
        )

    console.print(table)


def start_task(task_id):
    tasks = load_tasks()
    updated = []
    found = False
    for task in tasks:
        parts = task.split(" | ")
        if parts[0] == str(task_id):
            parts[4] = str(time.time())
            found = True
            console.print(f"[bold green]▶ Starting:[/bold green] {parts[1]}")
            updated.append(" | ".join(parts))
        else:
            updated.append(task)
    if found: save_tasks(updated)


def stop_task(task_id):
    tasks = load_tasks()
    updated = []
    found = False
    for task in tasks:
        parts = task.split(" | ")
        if parts[0] == str(task_id):
            if parts[4] != "0":
                elapsed = time.time() - float(parts[4])
                parts[3] = str(float(parts[3]) + elapsed)
                parts[4] = "0"
                found = True
                console.print(f"[bold red]◼ Stopped:[/bold red] {parts[1]}")
            updated.append(" | ".join(parts))
        else:
            updated.append(task)
    if found: save_tasks(updated)


def main():
    init_db()
    args = sys.argv
    if len(args) < 2:
        console.print(Panel("[bold cyan]Task Tracker v2.0[/bold cyan]\n"
                            "add [name] [mins] | list | start [id] | stop [id] | delete [id]"))
        return

    cmd = args[1].lower()
    if cmd == "add" and len(args) > 2:
        mins = args[3] if len(args) > 3 else 60
        add_task(args[2], mins)
    elif cmd == "list":
        list_tasks()
    elif cmd == "start" and len(args) > 2:
        start_task(args[2])
    elif cmd == "stop" and len(args) > 2:
        stop_task(args[2])
    elif cmd == "delete" and len(args) > 2:
        delete_task(args[2])
    else:
        console.print("[red]Invalid Command.[/red]")


if __name__ == "__main__":
    main()