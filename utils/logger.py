from datetime import datetime 
import os

logDirectory = "logs"
log_file = os.path.join(logDirectory, "security.log")

def log_event(event):
    os.makedirs(logDirectory, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    with open(log_file, "a") as logfile:
        logfile.write(f"{event} at [{timestamp}]\n")
    return f"[{timestamp}] {event}"
