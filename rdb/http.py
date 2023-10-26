from http import HTTPStatus

from .db import Database
from .server import JsonResponse, Request, Response, register_route, start_server

db: Database = None


def run(database: Database):
    global db
    db = database

    start_server()


@register_route("/get")
def db_get(request: Request) -> Response:
    """
    Returns the value stored in the database for the given key.
    If the key isn't stored, null will be returned.
    """
    key = request.params.get("key")
    if key is None:
        return JsonResponse(
            {"error": "Please specify the key"},
            status=HTTPStatus.BAD_REQUEST,
        )
    return JsonResponse({"key": key, "value": db.get(key)})


@register_route("/set")
def db_set(request: Request) -> Response:
    """
    Saves the key-value pair from the request into the database.
    If the key already exists, its value will be replaced.
    Raises error in case there are zero or multiple params provided in the request.

    Example: /set?some_key=some_value
    """
    if len(request.params) != 1:
        return JsonResponse(
            {"error": "Please specify one key-value pair"},
            status=HTTPStatus.BAD_REQUEST,
        )
    key, value = next(iter(request.params.items()))
    db.set(key, value)
    return JsonResponse({"key": key, "value": value}, status=HTTPStatus.CREATED)
