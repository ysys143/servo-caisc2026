from __future__ import annotations

import shutil
import sys
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import assert_never, override


class ProviderBinary(StrEnum):
    CLAUDE = "claude"
    CODEX = "codex"
    AGY = "agy"


@dataclass(frozen=True, slots=True)
class SandboxConfigurationError(Exception):
    detail: str

    @override
    def __str__(self) -> str:
        return self.detail


def build_execution_command(provider_command: tuple[str, ...]) -> tuple[str, ...]:
    match sys.platform:
        case "darwin":
            pass
        case platform:
            raise SandboxConfigurationError(
                f"no fail-closed process sandbox is configured for {platform}"
            )
    if not provider_command:
        raise SandboxConfigurationError("provider command is empty")
    try:
        provider = ProviderBinary(provider_command[0])
    except ValueError as error:
        raise SandboxConfigurationError(
            f"unsupported provider executable: {provider_command[0]}"
        ) from error
    match provider:
        case ProviderBinary.CODEX:
            executable, allowed = _codex_invocation()
        case ProviderBinary.CLAUDE:
            return provider_command
        case ProviderBinary.AGY:
            resolved = _resolve_executable(provider.value)
            executable, allowed = (resolved,), (resolved, "/usr/bin/security")
        case unreachable:
            assert_never(unreachable)
    profile = _seatbelt_profile(allowed)
    return ("/usr/bin/sandbox-exec", "-p", profile, *executable, *provider_command[1:])


def _codex_invocation() -> tuple[tuple[str, ...], tuple[str, ...]]:
    node = _resolve_executable("node")
    codex_script = Path(_resolve_executable("codex")).resolve()
    native_candidates = tuple(
        codex_script.parents[1].glob(
            "node_modules/@openai/codex-*/vendor/*/bin/codex"
        )
    )
    if len(native_candidates) != 1:
        raise SandboxConfigurationError(
            f"expected one native Codex executable, found {len(native_candidates)}"
        )
    native = str(native_candidates[0].resolve())
    return (node, str(codex_script)), (node, native)


def _resolve_executable(name: str) -> str:
    resolved = shutil.which(name)
    if resolved is None:
        raise SandboxConfigurationError(f"required executable is unavailable: {name}")
    return str(Path(resolved).resolve())


def _seatbelt_profile(allowed: tuple[str, ...]) -> str:
    literals = " ".join(
        f'(literal "{path.replace(chr(92), chr(92) * 2).replace(chr(34), chr(92) + chr(34))}")'
        for path in allowed
    )
    return f"(version 1)(allow default)(deny process-exec)(allow process-exec {literals})"
