from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, override

from pydantic import Field, model_validator

from .models import CommonEnvelope, EvidenceExcerpt, EvidenceQuote, FrozenModel


class EvidenceItem(FrozenModel):
    evidence_id: Annotated[str, Field(min_length=1)]
    pdf_page: Annotated[int, Field(ge=1)]
    quote: Annotated[str, Field(min_length=1)]

    @model_validator(mode="before")
    @classmethod
    def accept_legacy_names(cls, value: object) -> object:
        if isinstance(value, dict) and "page" in value:
            converted = dict(value)
            converted["pdf_page"] = converted.pop("page")
            converted["quote"] = converted.pop("text")
            return converted
        return value

    @property
    def page(self) -> int:
        return self.pdf_page

    @property
    def text(self) -> str:
        return self.quote


class PacketSource(FrozenModel):
    pdf_sha256: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
    page_count: Annotated[int, Field(ge=1)]


class EvidencePacket(FrozenModel):
    schema_version: Annotated[int, Field(ge=1)] = 1
    record_id: Annotated[str, Field(pattern=r"^R\d{2}$")]
    source: PacketSource
    instructions: Annotated[str, Field(min_length=1)] = "Evidence packet"
    scope: Annotated[str, Field(min_length=1)] | None = None
    evidence: Annotated[tuple[EvidenceItem, ...], Field(min_length=1)]

    @model_validator(mode="after")
    def evidence_ids_are_unique(self) -> EvidencePacket:
        identifiers = tuple(item.evidence_id for item in self.evidence)
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("evidence ids must be unique")
        return self

    @model_validator(mode="before")
    @classmethod
    def accept_legacy_names(cls, value: object) -> object:
        if isinstance(value, dict) and "pdf_id" in value:
            converted = dict(value)
            items = converted["items"]
            pages = (
                item.page if isinstance(item, EvidenceItem) else item["page"]
                for item in items
            )
            converted["source"] = {
                "pdf_sha256": converted.pop("pdf_id"),
                "page_count": max(pages),
            }
            converted["evidence"] = converted.pop("items")
            return converted
        return value

    @property
    def pdf_id(self) -> str:
        return self.source.pdf_sha256

    @property
    def items(self) -> tuple[EvidenceItem, ...]:
        return self.evidence


@dataclass(frozen=True, slots=True)
class EvidenceError(Exception):
    evidence_id: str
    reason: str

    @override
    def __str__(self) -> str:
        return f"{self.evidence_id}: {self.reason}"


def validate_quotes(packet: EvidencePacket, quotes: tuple[EvidenceQuote, ...]) -> None:
    indexed = {item.evidence_id: item for item in packet.items}
    for quote in quotes:
        item = indexed.get(quote.evidence_id)
        if item is None:
            raise EvidenceError(quote.evidence_id, "unknown evidence id")
        if quote.pdf_id != packet.pdf_id or quote.page != item.page:
            raise EvidenceError(quote.evidence_id, "source identity or page mismatch")
        if quote.quote != item.text:
            raise EvidenceError(quote.evidence_id, "quote does not equal the frozen packet quotation")


def validate_envelope(packet: EvidencePacket, envelope: CommonEnvelope) -> None:
    excerpts = tuple(
        excerpt
        for diagnostic in envelope.diagnostics
        for excerpt in diagnostic.exact_quotes
    ) + tuple(
        excerpt
        for recommendation in envelope.recommendations
        for excerpt in recommendation.exact_quotes
    )
    _validate_excerpts(packet, excerpts)


def _validate_excerpts(
    packet: EvidencePacket, excerpts: tuple[EvidenceExcerpt, ...]
) -> None:
    indexed = {item.evidence_id: item for item in packet.items}
    for excerpt in excerpts:
        item = indexed.get(excerpt.evidence_id)
        if item is None:
            raise EvidenceError(excerpt.evidence_id, "unknown evidence id")
        if excerpt.exact_quote != item.text:
            raise EvidenceError(excerpt.evidence_id, "quote does not equal the frozen packet quotation")
