"""TaskFlow — a small task tracker with a REST API."""

from flask import Flask, jsonify, request

from store import TaskStore

app = Flask(__name__)
store = TaskStore()


@app.get("/health")
def health():
    return jsonify(status="ok", tasks=store.count())


@app.get("/tasks")
def list_tasks():
    status = request.args.get("status")
    return jsonify(tasks=[t.as_dict() for t in store.list(status)])


@app.post("/tasks")
def create_task():
    payload = request.get_json(silent=True) or {}
    title = (payload.get("title") or "").strip()
    if not title:
        return jsonify(error="title is required"), 400
    task = store.add(title, payload.get("priority", "normal"))
    return jsonify(task.as_dict()), 201


@app.get("/tasks/<int:task_id>")
def get_task(task_id):
    task = store.get(task_id)
    if task is None:
        return jsonify(error="no such task"), 404
    return jsonify(task.as_dict())


@app.post("/tasks/<int:task_id>/done")
def complete_task(task_id):
    task = store.complete(task_id)
    if task is None:
        return jsonify(error="no such task"), 404
    return jsonify(task.as_dict())


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    if not store.remove(task_id):
        return jsonify(error="no such task"), 404
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
