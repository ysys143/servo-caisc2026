from __future__ import annotations

import json
from typing import assert_never

from pydantic import ValidationError

from r24_final.evidence import EvidenceError, EvidencePacket, validate_envelope, validate_quotes
from r24_final.models import BaselineCoding, ServoCoding
from r24_final.schedule import Condition, Trial


def _validate_output(
    trial: Trial,
    raw: str,
    packet: EvidencePacket | None = None,
    requested_model: str | None = None,
) -> tuple[str, str | None]:
    normalized = _single_json_document(raw)
    try:
        value = json.loads(
            normalized,
            object_pairs_hook=_reject_duplicate_json_keys,
            parse_constant=_reject_nonfinite_json_number,
        )
        if not isinstance(value, dict):
            return normalized, "output must be a JSON object"
        if requested_model is not None:
            value["model_id"] = requested_model
            normalized = json.dumps(value, ensure_ascii=False, sort_keys=True)
        match trial.condition:
            case Condition.BASELINE:
                coding = BaselineCoding.model_validate_json(normalized)
            case Condition.SERVO:
                coding = ServoCoding.model_validate_json(normalized)
            case unreachable:
                assert_never(unreachable)
        if coding.record_id != trial.record_id or coding.vendor != trial.vendor:
            return normalized, "record_id or vendor does not match the scheduled trial"
        if packet is not None:
            if packet.record_id != trial.record_id:
                return normalized, "packet record_id does not match the scheduled trial"
            validate_envelope(packet, coding.envelope)
            if isinstance(coding, ServoCoding):
                for channel in coding.channels:
                    validate_quotes(packet, channel.quotes)
    except (json.JSONDecodeError, ValidationError, EvidenceError, ValueError) as error:
        return normalized, str(error)
    return normalized, None


def _single_json_document(raw: str) -> str:
    return raw.strip()


def _reject_duplicate_json_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def _reject_nonfinite_json_number(value: str) -> object:
    raise ValueError(f"non-finite JSON number: {value}")
