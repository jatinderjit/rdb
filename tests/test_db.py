from rdb import Database


def test_db():
    db = Database()

    assert db.get("a") is None
    assert db.get("b") is None

    db.set("a", "A")
    assert db.get("a") == "A"
    assert db.get("b") is None
