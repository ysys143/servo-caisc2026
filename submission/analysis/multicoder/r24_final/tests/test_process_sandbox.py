from __future__ import annotations

from pathlib import Path

import r24_final.adapters as adapters
from r24_final.adapters import Vendor
from r24_final.process_sandbox import build_execution_command


def test_codex_execution_command_denies_unlisted_subprocesses() -> None:
    # Given
    provider_command = ("codex", "exec", "--ephemeral", "-")

    # When
    execution = build_execution_command(provider_command)

    # Then
    assert execution[0] == "/usr/bin/sandbox-exec"
    assert execution[1] == "-p"
    assert "(deny process-exec)" in execution[2]
    assert "/bin/zsh" not in execution[2]
    assert Path(execution[3]).name == "node"


def test_native_provider_execution_command_allows_only_provider_binary() -> None:
    # Given
    provider_command = ("agy", "--version")

    # When
    execution = build_execution_command(provider_command)

    # Then
    assert execution[0] == "/usr/bin/sandbox-exec"
    assert execution[1] == "-p"
    assert "(deny process-exec)" in execution[2]
    assert '(literal "/usr/bin/security")' in execution[2]
    assert Path(execution[3]).name == "agy"
    assert execution[4:] == ("--version",)


def test_claude_uses_host_login_with_model_tools_disabled_by_adapter() -> None:
    # Given
    provider_command = ("claude", "--safe-mode", "--tools", "", "--print")

    # When
    execution = build_execution_command(provider_command)

    # Then
    assert execution == provider_command


def test_subprocess_environment_preserves_host_login_identity() -> None:
    # Given
    source = {
        "PATH": "/bin",
        "HOME": "/host/home",
        "USER": "researcher",
        "LOGNAME": "researcher",
        "SHELL": "/bin/zsh",
        "__CF_USER_TEXT_ENCODING": "0x1F5:0x0:0x0",
        "UNRELATED": "forbidden",
    }

    # When
    environment = adapters.subprocess_environment(source)

    # Then
    assert environment == {key: value for key, value in source.items() if key != "UNRELATED"}


def test_isolation_commands_retain_provider_safety_controls() -> None:
    # Given / When
    commands = {vendor: adapters.build_isolation_command(vendor) for vendor in Vendor}

    # Then
    assert commands[Vendor.CLAUDE].arguments[commands[Vendor.CLAUDE].arguments.index("--tools") + 1] == ""
    assert "read-only" in commands[Vendor.CODEX].arguments
    assert "--sandbox" in commands[Vendor.GEMINI].arguments
