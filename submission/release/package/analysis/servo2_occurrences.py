from __future__ import annotations

from .servo2_io import Servo2Error

def validate_occurrence_tokens(
    event_refs: tuple[str, ...], witness_id: str
) -> tuple[str, ...]:
    if any("@" in ref or not ref for ref in event_refs):
        raise Servo2Error("OCCURRENCE_TOKEN_INVALID", witness_id)
    if len(set(event_refs)) != len(event_refs):
        raise Servo2Error("OCCURRENCE_ID_REUSED", witness_id)
    for ref in event_refs:
        if not all(character.isalnum() or character in "_.-" for character in ref):
            raise Servo2Error("OCCURRENCE_TOKEN_INVALID", witness_id)
    return event_refs


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
