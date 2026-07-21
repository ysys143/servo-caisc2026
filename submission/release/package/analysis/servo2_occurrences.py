from __future__ import annotations

import re

from .servo2_io import Servo2Error


_OCCURRENCE = re.compile(
    r"^(?P<event>[A-Za-z0-9_.-]+)@t(?P<offset>\+1)?$"
)


def validate_occurrence_tokens(
    event_refs: tuple[str, ...], witness_id: str
) -> tuple[str, ...]:
    event_ids: list[str] = []
    offsets: list[int] = []
    for ref in event_refs:
        match = _OCCURRENCE.fullmatch(ref)
        if match is None:
            raise Servo2Error("OCCURRENCE_TOKEN_INVALID", witness_id)
        event_ids.append(match.group("event"))
        offsets.append(1 if match.group("offset") else 0)
    if offsets and (offsets[0] != 0 or offsets != sorted(offsets)):
        raise Servo2Error("OCCURRENCE_TOKEN_INVALID", witness_id)
    return tuple(event_ids)


def validate_ordered_event_edge_binding(
    event_ids: tuple[str, ...],
    edge_rows: tuple[dict[str, str], ...],
    witness_id: str,
) -> None:
    last_event_index = 0
    for edge in edge_rows:
        source_event = edge["source_event_id"]
        if source_event not in event_ids:
            raise Servo2Error("CLOSURE_WITNESS_EVENT_EDGE_MISMATCH", witness_id)
        candidates = tuple(
            index
            for index, event_id in enumerate(event_ids)
            if event_id == source_event and index >= last_event_index
        )
        if not candidates:
            raise Servo2Error(
                "CLOSURE_WITNESS_EVENT_EDGE_ORDER_MISMATCH", witness_id
            )
        last_event_index = candidates[0]
