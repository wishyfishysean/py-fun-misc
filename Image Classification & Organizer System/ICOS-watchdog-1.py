from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class Watcher(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.lower().endswith((".jpg", ".jpeg", ".png")):
            print(f"\new image detected: {event.src_path}")
            organize_images()

if __name__ == "__main__":
    event_handler = Watcher()
    observer = Observer()
    observer.schedule(event_handler, INPUT_FOLDER, recursive=False)
    observer.start()
    print("Watching for new images...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
