import argparse
import json
from datetime import datetime
import os

LOG_FILE = "daily_logs.json"
CONFIG_FILE = "config.json"

def load_config():
    """Load configuration settings."""
    try:
        with open(CONFIG_FILE, "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Config file {CONFIG_FILE} not found. Please create one with the required settings.")
        exit(1)

CONFIG = load_config()
OBSIDIAN_VAULT_PATH = CONFIG.get("obsidian_vault_path", "./")  # Default to current directory if not set

def load_logs():
    """Load existing logs from file."""
    try:
        with open(LOG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_logs(logs):
    """Save logs to file."""
    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)

def format_markdown(date, log_entry):
    """Format log entry as Markdown."""
    tasks = "\n".join([f"- [ ] {task}" for task in log_entry["tasks"]])
    reflection = log_entry["reflection"]
    return (
        f"# {date}\n\n## Tasks\n{tasks if tasks else 'No tasks logged.'}\n\n## Reflection\n{reflection if reflection else 'No reflection added.'}\n"
    )

def add_entry(task=None, reflection=None):
    """Add a new entry to the log."""
    logs = load_logs()
    date = datetime.now().strftime("%Y-%m-%d")
    logs.setdefault(date, {"tasks": [], "reflection": ""})
    if task:
        logs[date]["tasks"].append(task)
    if reflection:
        logs[date]["reflection"] = reflection
    save_logs(logs)
    export_to_obsidian(date, logs[date])  # Export to Obsidian after saving
    print(f"Entry added for {date}")

def batch_add(batch_data):
    """Add multiple entries to the log from batch data."""
    logs = load_logs()
    for date, entry in batch_data.items():
        logs.setdefault(date, {"tasks": [], "reflection": ""})
        logs[date]["tasks"].extend(entry.get("tasks", []))
        if entry.get("reflection"):
            logs[date]["reflection"] = entry["reflection"]
        export_to_obsidian(date, logs[date])  # Export to Obsidian after saving
    save_logs(logs)
    print("Batch entries added successfully.")

def export_to_obsidian(date, log_entry):
    """Export the log entry to an Obsidian markdown file."""
    file_path = os.path.join(OBSIDIAN_VAULT_PATH, f"{date}.md")
    content = format_markdown(date, log_entry)
    try:
        with open(file_path, "w") as file:
            file.write(content)
        print(f"Log exported to Obsidian: {file_path}")
    except Exception as e:
        print(f"Failed to export log to Obsidian: {e}")

def list_logs():
    """Print all logs in JSON format."""
    logs = load_logs()
    print(json.dumps(logs, indent=4))

def main():
    """Main function to handle CLI arguments."""
    parser = argparse.ArgumentParser(description="Daily Log CLI Tool")
    parser.add_argument("--add-task", type=str, help="Add a task")
    parser.add_argument("--add-reflection", type=str, help="Add a reflection")
    parser.add_argument("--batch-add", type=str, help="Batch add tasks and reflections from a JSON string or file")
    parser.add_argument("--list-logs", action="store_true", help="List all logs")
    args = parser.parse_args()

    if args.add_task or args.add_reflection:
        add_entry(task=args.add_task, reflection=args.add_reflection)
    elif args.batch_add:
        try:
            # Load batch data from JSON string or file
            if os.path.exists(args.batch_add):
                with open(args.batch_add, "r") as file:
                    batch_data = json.load(file)
            else:
                batch_data = json.loads(args.batch_add)
            batch_add(batch_data)
        except Exception as e:
            print(f"Failed to process batch add: {e}")
    elif args.list_logs:
        list_logs()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
