#!/usr/bin/env python3

"""HTML entry point for the topology validation Building Blocks transform."""

from __future__ import annotations

import runpy
from pathlib import Path
from typing import Any


def _repo_root() -> Path:
    """Return the repository root from the Building Blocks working directory."""
    current = Path.cwd().resolve()
    candidates = [current, *current.parents]

    for candidate in candidates:
        if (candidate / "bblocks-config.yaml").exists():
            return candidate

    return current


def _implementation_path() -> Path:
    """Return the shared validation transform implementation path."""
    return (
        _repo_root()
        / "_sources"
        / "features"
        / "topology-validator"
        / "transforms"
        / "validate_topology.py"
    )


_impl: dict[str, Any] = runpy.run_path(
    str(_implementation_path()),
    run_name="topology_validation_html_transform",
)

_transform_input_data = globals().get("input_data")


def _source_name_from_metadata() -> str | None:
    """Return the transform input source name when the runner provides one."""
    for metadata_object in (
        globals().get("transform_metadata"),
        globals().get("metadata"),
    ):
        if isinstance(metadata_object, dict):
            metadata = metadata_object.get("metadata", metadata_object)
        else:
            metadata = getattr(metadata_object, "metadata", None)

        if not isinstance(metadata, dict):
            continue

        for key in (
            "source",
            "source_name",
            "input_source",
            "input_filename",
            "filename",
            "file_name",
            "path",
        ):
            value = metadata.get(key)
            if isinstance(value, str) and value:
                return Path(value).name

    return None


if _transform_input_data is not None:
    output_data = _impl["process"](
        _transform_input_data,
        fail_on_error=True,
        output_format="html",
        source=_source_name_from_metadata(),
        progress=print,
    )