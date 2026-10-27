"""In-memory task storage, kept separate so the tests can exercise it alone."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from itertools import count

VALID_PRIORITIES = ("low", "normal", "high")


@dataclass
class Task:
    id: int
    title: str
    priority: str = "normal"
    done: bool = False
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "done": self.done,
            "created_at": self.created_at,
        }


class TaskStore:
    def __init__(self):
        self._tasks = {}
        self._ids = count(1)

    def add(self, title, priority="normal"):
        if priority not in VALID_PRIORITIES:
            priority = "normal"
        task = Task(id=next(self._ids), title=title, priority=priority)
        self._tasks[task.id] = task
        return task

    def get(self, task_id):
        return self._tasks.get(task_id)

    def list(self, status=None):
        tasks = sorted(self._tasks.values(), key=lambda t: t.id)
        if status == "done":
            return [t for t in tasks if t.done]
        if status == "open":
            return [t for t in tasks if not t.done]
        return tasks

    def complete(self, task_id):
        task = self._tasks.get(task_id)
        if task is not None:
            task.done = True
        return task

    def remove(self, task_id):
        return self._tasks.pop(task_id, None) is not None

    def count(self):
        return len(self._tasks)
