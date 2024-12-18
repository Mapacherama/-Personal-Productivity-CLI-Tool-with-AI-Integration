import argparse
import json
from datetime import datetime

LOG_FILE = "daily_logs.json"

def load_logs():
    try:
        with open(LOG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_logs(logs):
    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)

def add_entry(task=None, reflection=None):
    logs = load_logs()
    date = datetime.now().strftime("%Y-%m-%d")
    logs.setdefault(date, {"tasks": [], "reflection": ""})
    if task:
        logs[date]["tasks"].append(task)
    if reflection:
        logs[date]["reflection"] = reflection
    save_logs(logs)
    print(f"Entry added for {date}")

def main():
    parser = argparse.ArgumentParser(description="Daily Log CLI Tool")
    parser.add_argument("--add-task", type=str, help="Add a task")
    parser.add_argument("--add-reflection", type=str, help="Add a reflection")
    parser.add_argument("--list-logs", action="store_true", help="List all logs")
    args = parser.parse_args()

    if args.add_task or args.add_reflection:
        add_entry(task=args.add_task, reflection=args.add_reflection)
    elif args.list_logs:
        logs = load_logs()
        print(json.dumps(logs, indent=4))

if __name__ == "__main__":
    main()
