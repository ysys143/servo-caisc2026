from __future__ import annotations

from pydantic import BaseModel, TypeAdapter

from .models import BaselineCoding, ServoCoding
from .schedule import Trial, build_schedule


type JsonValue = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]

_JSON_ADAPTER = TypeAdapter(JsonValue)


def _provider_schema(model: type[BaseModel]) -> dict[str, JsonValue]:
    schema = _strip_unsupported_keywords(
        _JSON_ADAPTER.validate_python(model.model_json_schema())
    )
    match schema:
        case dict() as mapping:
            return mapping
        case _:
            raise TypeError("provider schema must be a JSON object")


def _strip_unsupported_keywords(value: JsonValue) -> JsonValue:
    match value:
        case dict() as mapping:
            return {
                key: _strip_unsupported_keywords(item)
                for key, item in mapping.items()
                if key != "uniqueItems"
            }
        case list() as items:
            return [_strip_unsupported_keywords(item) for item in items]
        case None | bool() | int() | float() | str():
            return value
        case _:
            raise TypeError("unsupported JSON schema value")


def servo_json_schema() -> dict[str, JsonValue]:
    return _provider_schema(ServoCoding)


def baseline_json_schema() -> dict[str, JsonValue]:
    return _provider_schema(BaselineCoding)


def schedule_json(record_ids: tuple[str, ...], seed: int) -> bytes:
    schedule = build_schedule(record_ids, seed)
    return TypeAdapter(tuple[Trial, ...]).dump_json(schedule, indent=2)
