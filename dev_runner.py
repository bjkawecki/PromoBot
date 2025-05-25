import subprocess
import threading
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


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
