import pytest

from app import app, store


@pytest.fixture
def client():
    store.__init__()  # a clean store for every test
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_reports_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_creating_a_task_returns_it_with_an_id(client):
    response = client.post("/tasks", json={"title": "write tests"})
    assert response.status_code == 201

    body = response.get_json()
    assert body["title"] == "write tests"
    assert body["done"] is False
    assert body["id"] >= 1


def test_a_task_needs_a_title(client):
    assert client.post("/tasks", json={}).status_code == 400
    assert client.post("/tasks", json={"title": "   "}).status_code == 400


def test_fetching_a_task_that_does_not_exist_is_a_404(client):
    assert client.get("/tasks/4242").status_code == 404


def test_a_task_can_be_completed_then_read_back(client):
    created = client.post("/tasks", json={"title": "deploy"}).get_json()

    assert client.post("/tasks/%d/done" % created["id"]).status_code == 200
    assert client.get("/tasks/%d" % created["id"]).get_json()["done"] is True


def test_deleting_a_task_leaves_nothing_behind(client):
    created = client.post("/tasks", json={"title": "temporary"}).get_json()

    assert client.delete("/tasks/%d" % created["id"]).status_code == 204
    assert client.get("/tasks/%d" % created["id"]).status_code == 404
