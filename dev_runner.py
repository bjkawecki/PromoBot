import subprocess
import threading
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from scripts import dynamodb_local


def is_dynamodb_local_running():
    try:
        output = (
            subprocess.check_output(
                [
                    "docker",
                    "ps",
                    "--filter",
                    "ancestor=amazon/dynamodb-local",
                    "--format",
                    "{{.ID}}",
                ]
            )
            .decode()
            .strip()
        )
        return len(output) > 0
    except subprocess.CalledProcessError:
        return False


def start_dynamodb_local():
    print("Starte DynamoDB Local Container...")
    subprocess.run(
        [
            "docker",
            "run",
            "-d",
            "-p",
            "8000:8000",
            "-v",
            "./dynamodb-local-data:/home/dynamodblocal/data",
            "amazon/dynamodb-local:latest",
        ],
        check=True,
    )
    print("DynamoDB Local gestartet.")


class RestartOnChangeHandler(FileSystemEventHandler):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = self.start_process()
        self.last_restart = 0
        self.restart_timer = None

    def start_process(self):
        return subprocess.Popen(self.cmd)

    def restart_process(self):
        print("🌀 Code geändert. Neustart ...")
        self.process.kill()
        self.process = self.start_process()

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".py") and "src/" in event.src_path:
            self.schedule_restart()

    def schedule_restart(self):
        if self.restart_timer:
            self.restart_timer.cancel()
        self.restart_timer = threading.Timer(0.2, self.restart_process)
        self.restart_timer.start()


if __name__ == "__main__":
    if not is_dynamodb_local_running():
        start_dynamodb_local()

    else:
        print("DynamoDB Local läuft bereits.")
    dynamodb_local.create_seller_table()
    dynamodb_local.create_buyer_table()
    dynamodb_local.read_schema()
    path = "."
    cmd = ["python", "src/main.py"]
    event_handler = RestartOnChangeHandler(cmd)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print("👀 Beobachte Änderungen...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
