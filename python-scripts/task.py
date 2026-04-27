import sys
import os
import time

DB_FILE = "../tasks.txt"


def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            pass


def format_time(seconds):
    """Converts seconds into a readable HH:MM:SS string."""
    mins, secs = divmod(int(seconds), 60)
    hours, mins = divmod(mins, 60)
    return f"{hours:02d}:{mins:02d}:{secs:02d}"


def load_tasks():
    with open(DB_FILE, "r") as f:
        return [line.strip() for line in f.readlines()]


def save_tasks(tasks):
    with open(DB_FILE, "w") as f:
        for task in tasks:
            f.write(task + "\n")


def add_task(description):
    tasks = load_tasks()
    task_id = len(tasks) + 1
    # Format: ID | Description | Status | TotalTime(s) | StartTimestamp (0 if not running)
    new_task = f"{task_id} | {description} | [ ] | 0 | 0"
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Added: {description}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Your task list is empty!")
        return
    print(f"\n{'ID':<3} | {'Task':<20} | {'Status':<6} | {'Time Spent'}")
    print("-" * 50)
    for task in tasks:
        parts = task.split(" | ")
        # If currently running, show live accumulated time
        total_time = float(parts[3])
        if parts[4] != "0":
            total_time += time.time() - float(parts[4])

        print(f"{parts[0]:<3} | {parts[1]:<20} | {parts[2]:<6} | {format_time(total_time)}")


def start_task(task_id):
    tasks = load_tasks()
    updated = []
    found = False
    for task in tasks:
        parts = task.split(" | ")
        if parts[0] == str(task_id):
            if parts[4] == "0":
                parts[4] = str(time.time())
                found = True
                print(f"Started timer for task {task_id}.")
            else:
                print(f"Task {task_id} is already running!")
            updated.append(" | ".join(parts))
        else:
            updated.append(task)
    save_tasks(updated) if found else None


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
                print(f"Stopped timer. Added {format_time(elapsed)} to task {task_id}.")
            else:
                print(f"Task {task_id} was not running.")
            updated.append(" | ".join(parts))
        else:
            updated.append(task)
    save_tasks(updated) if found else None


def main():
    init_db()
    if len(sys.argv) < 2:
        print("Usage: python task.py [add/list/start/stop/done]")
        return

    cmd = sys.argv[1].lower()
    if cmd == "add" and len(sys.argv) > 2:
        add_task(sys.argv[2])
    elif cmd == "list":
        list_tasks()
    elif cmd == "start" and len(sys.argv) > 2:
        start_task(sys.argv[2])
    elif cmd == "stop" and len(sys.argv) > 2:
        stop_task(sys.argv[2])
    else:
        print("Invalid command.")


if __name__ == "__main__":
    main()

