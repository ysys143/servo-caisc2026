# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
# How to run: imported by r24_final.runner

from __future__ import annotations

import os
import subprocess
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import assert_never

from r24_final.schedule import Trial
from r24_final.process_sandbox import build_execution_command


class Vendor(StrEnum):
    CLAUDE = "claude"
    CODEX = "codex"
    GEMINI = "gemini"


@dataclass(frozen=True, slots=True)
class Command:
    arguments: tuple[str, ...]
    vendor: Vendor
    requested_model: str


class CommandPolicyError(ValueError):
    pass


def validate_command(command: Command) -> None:
    args = command.arguments
    flags = tuple(arg for arg in args if arg.startswith("-") and arg != "-")
    forbidden = {
        "--dangerously-skip-permissions",
        "--dangerously-bypass-approvals-and-sandbox",
        "--add-dir",
        "--continue",
        "--conversation",
        "--resume",
        "--plugin-dir",
        "--plugin-url",
    }
    present = forbidden.intersection(args)
    if present:
        raise CommandPolicyError(f"forbidden runtime flags: {sorted(present)}")
    match command.vendor:
        case Vendor.CLAUDE:
            allowed = {
                "--model", "--print", "--output-format", "--no-session-persistence",
                "--safe-mode", "--disable-slash-commands", "--no-chrome", "--tools",
                "--strict-mcp-config", "--json-schema",
            }
            required = {"--safe-mode", "--no-session-persistence", "--strict-mcp-config", "--tools"}
            if not required.issubset(args) or args[args.index("--tools") + 1] != "":
                raise CommandPolicyError("Claude must run stateless with an empty tool set")
        case Vendor.CODEX:
            allowed = {
                "--model", "--sandbox", "--ephemeral", "--ignore-user-config",
                "--ignore-rules", "--skip-git-repo-check", "--cd", "--output-schema", "-c",
            }
            required = {"--ephemeral", "--ignore-user-config", "--ignore-rules", "--sandbox", "--cd"}
            if not required.issubset(args):
                raise CommandPolicyError("Codex isolation flags are incomplete")
            if args[args.index("--sandbox") + 1] != "read-only" or args[args.index("--cd") + 1] != ".":
                raise CommandPolicyError("Codex must be read-only and rooted at the staged cwd")
            schema = args[args.index("--output-schema") + 1]
            if Path(schema).is_absolute() or ".." in Path(schema).parts:
                raise CommandPolicyError("Codex schema path must remain inside the staged cwd")
            if 'web_search="disabled"' not in args:
                raise CommandPolicyError("Codex web search must be disabled")
        case Vendor.GEMINI:
            allowed = {"--model", "--sandbox", "--print-timeout", "--prompt"}
            if "--sandbox" not in args or any(flag in args for flag in ("--project", "--new-project")):
                raise CommandPolicyError("agy must use a fresh restricted sandbox")
        case unreachable:
            assert_never(unreachable)
    unknown = set(flags) - allowed
    if unknown:
        raise CommandPolicyError(f"unknown runtime flags: {sorted(unknown)}")
    duplicates = {flag for flag in flags if flags.count(flag) > 1}
    if duplicates:
        raise CommandPolicyError(f"duplicate runtime flags: {sorted(duplicates)}")


def build_command(trial: Trial, schema_path: Path, cwd: Path | None = None) -> Command:
    vendor = Vendor(trial.vendor)
    match vendor:
        case Vendor.CLAUDE:
            command = Command(
                (
                    "claude", "--model", "claude-opus-4-8", "--print",
                    "--output-format", "text", "--no-session-persistence",
                    "--safe-mode", "--disable-slash-commands", "--no-chrome",
                    "--tools", "", "--strict-mcp-config", "--json-schema",
                    (cwd / schema_path if cwd is not None else schema_path).read_text(encoding="utf-8"),
                ),
                vendor,
                "claude-opus-4-8",
            )
        case Vendor.CODEX:
            command = Command(
                (
                    "codex", "exec", "--model", "gpt-5.5", "--sandbox", "read-only",
                    "--ephemeral", "--ignore-user-config", "--ignore-rules",
                    "--skip-git-repo-check", "--cd", ".", "--output-schema", str(schema_path),
                    "-c", 'web_search="disabled"', "-",
                ),
                vendor,
                "gpt-5.5",
            )
        case Vendor.GEMINI:
            command = Command(
                (
                    "agy", "--model", "Gemini 3.1 Pro (High)", "--sandbox",
                    "--print-timeout", "590s", "--prompt",
                ),
                vendor,
                "Gemini 3.1 Pro (High)",
            )
        case unreachable:
            assert_never(unreachable)
    validate_command(command)
    return command


def build_isolation_command(
    vendor: Vendor, schema_path: Path = Path("input/attack.schema.json")
) -> Command:
    match vendor:
        case Vendor.CLAUDE:
            command = Command(
                (
                    "claude", "--model", "claude-opus-4-8", "--print",
                    "--output-format", "text", "--no-session-persistence",
                    "--safe-mode", "--disable-slash-commands", "--no-chrome",
                    "--tools", "", "--strict-mcp-config",
                ),
                vendor,
                "claude-opus-4-8",
            )
        case Vendor.CODEX:
            command = Command(
                (
                    "codex", "exec", "--model", "gpt-5.5", "--sandbox", "read-only",
                    "--ephemeral", "--ignore-user-config", "--ignore-rules",
                    "--skip-git-repo-check", "--cd", ".",
                    "--output-schema", str(schema_path),
                    "-c", 'web_search="disabled"', "-",
                ),
                vendor,
                "gpt-5.5",
            )
        case Vendor.GEMINI:
            command = Command(
                (
                    "agy", "--model", "Gemini 3.1 Pro (High)", "--sandbox",
                    "--print-timeout", "590s", "--prompt",
                ),
                vendor,
                "Gemini 3.1 Pro (High)",
            )
        case unreachable:
            assert_never(unreachable)
    validate_command(command)
    return command


def subprocess_transport(
    arguments: tuple[str, ...], prompt: str, cwd: Path, timeout_seconds: int
) -> subprocess.CompletedProcess[str]:
    provider_command = (*arguments, prompt) if arguments[0] == "agy" else arguments
    command = build_execution_command(provider_command)
    input_text = None if arguments[0] == "agy" else prompt
    environment = subprocess_environment(os.environ)
    return subprocess.run(
        command,
        cwd=cwd,
        input=input_text,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
        check=False,
        env=environment,
    )


def subprocess_environment(source: Mapping[str, str]) -> dict[str, str]:
    allowed_names = {
        "PATH",
        "HOME",
        "TMPDIR",
        "LANG",
        "LC_ALL",
        "USER",
        "LOGNAME",
        "SHELL",
        "__CF_USER_TEXT_ENCODING",
        "SSL_CERT_FILE",
        "SSL_CERT_DIR",
        "ANTHROPIC_API_KEY",
        "OPENAI_API_KEY",
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
    }
    return {key: value for key, value in source.items() if key in allowed_names}
