import pytest

from store import TaskStore


@pytest.fixture
def store():
    return TaskStore()


def test_a_new_store_is_empty(store):
    assert store.count() == 0
    assert store.list() == []


def test_added_tasks_get_sequential_ids(store):
    first = store.add("write the deck")
    second = store.add("rehearse it")
    assert (first.id, second.id) == (1, 2)


def test_an_unknown_priority_falls_back_to_normal(store):
    assert store.add("something", priority="urgent").priority == "normal"
    assert store.add("something else", priority="high").priority == "high"


def test_completing_a_task_marks_it_done(store):
    task = store.add("ship it")
    assert task.done is False
    assert store.complete(task.id).done is True


def test_completing_a_task_that_is_not_there_returns_none(store):
    assert store.complete(999) is None


def test_listing_filters_by_status(store):
    store.add("one")
    second = store.add("two")
    store.complete(second.id)

    assert [t.title for t in store.list("open")] == ["one"]
    assert [t.title for t in store.list("done")] == ["two"]
    assert len(store.list()) == 2


def test_removing_a_task_takes_it_out_of_the_count(store):
    task = store.add("temporary")
    assert store.remove(task.id) is True
    assert store.remove(task.id) is False
    assert store.count() == 0
