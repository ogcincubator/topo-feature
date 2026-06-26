#!/usr/bin/env python3

"""Topology validation transform and fixture runner.

In Building Blocks transform mode, this script validates one input JSON document
and returns a JSON validation report.

When run directly, it can validate one file or a glob of fixture files. In fixture
mode, files ending with "-fail.json" are expected to produce validation errors;
all other JSON files are expected to pass.
"""

from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class SupportsRead(Protocol):
    """File-like object that supports read()."""

    def read(self, *args: Any, **kwargs: Any) -> str:
        """Read text from the object."""


def _repo_root() -> Path:
    """Return the repository root in CLI mode or Building Blocks transform mode."""
    file_name = globals().get("__file__")

    if isinstance(file_name, str):
        return Path(file_name).resolve().parents[4]

    current = Path.cwd().resolve()
    candidates = [current, *current.parents]

    for candidate in candidates:
        if (candidate / "bblocks-config.yaml").exists():
            return candidate
        if (candidate / "tools" / "topo-validator").exists():
            return candidate

    return current


def _ensure_validator_on_path() -> None:
    """Make the local topo_validator package importable when run from the repo."""
    validator_src = _repo_root() / "tools" / "topo-validator"
    if validator_src.exists():
        sys.path.insert(0, str(validator_src))


_ensure_validator_on_path()

from topo_validator.loader import from_csdm_json  # noqa: E402
from topo_validator.validator import validate_topology  # noqa: E402


def load_json_document(source: str | Path | SupportsRead) -> dict[str, Any]:
    """Load a JSON object from raw JSON text, a path, or a file-like object."""
    if isinstance(source, SupportsRead):
        data = json.load(source)
    elif isinstance(source, Path):
        data = json.loads(source.read_text(encoding="utf-8"))
    elif isinstance(source, str):
        try:
            data = json.loads(source)
        except json.JSONDecodeError:
            candidate = Path(source)
            data = json.loads(candidate.read_text(encoding="utf-8"))
    else:
        raise TypeError(f"Unsupported input type: {type(source)!r}")

    if not isinstance(data, dict):
        raise ValueError(
            f"Expected a JSON object at the document root, got {type(data).__name__}."
        )

    return data


def issue_to_json(issue: Any) -> dict[str, Any]:
    """Convert a validator issue into a JSON-serializable dictionary."""
    if isinstance(issue, dict):
        return {
            "code": issue.get("code"),
            "severity": issue.get("severity"),
            "message": issue.get("message"),
            "object_id": issue.get("object_id"),
            "path": issue.get("path"),
            "extra": issue.get("extra", {}),
        }

    return {
        "code": getattr(issue, "code", None),
        "severity": getattr(issue, "severity", None),
        "message": getattr(issue, "message", str(issue)),
        "object_id": getattr(issue, "object_id", None),
        "path": getattr(issue, "path", None),
        "extra": getattr(issue, "extra", {}),
    }


def get_transform_metadata() -> dict[str, Any]:
    """Return Building Blocks transform metadata when available."""
    metadata_object = globals().get("transform_metadata")
    metadata = getattr(metadata_object, "metadata", None)

    if isinstance(metadata, dict):
        return metadata

    return {}

def validate_document(
    data: dict[str, Any],
    *,
    source: str | None = None,
    conformance_classes: list[str] | None = None,
) -> dict[str, Any]:
    """Validate one topology document and return a JSON report."""
    topology_data = from_csdm_json(data)
    issues = validate_topology(
        topology_data,
        conformance_classes=conformance_classes,
    )
    normalized_issues = [issue_to_json(issue) for issue in issues]

    errors = [
        issue
        for issue in normalized_issues
        if issue.get("severity") == "error"
    ]

    warnings = [
        issue
        for issue in normalized_issues
        if issue.get("severity") == "warning"
    ]

    return {
        "source": source,
        "valid": len(errors) == 0,
        "summary": {
            "issues": len(normalized_issues),
            "errors": len(errors),
            "warnings": len(warnings),
        },
        "issues": normalized_issues,
    }


def expected_to_fail(path: Path) -> bool:
    """Return True when a fixture filename declares an expected validation failure."""
    return path.name.endswith("-fail.json")


def validate_fixture(path: Path) -> dict[str, Any]:
    """Validate one fixture and compare the result with its filename expectation."""
    data = load_json_document(path)
    report = validate_document(data, source=str(path))

    expected_failure = expected_to_fail(path)
    actual_failure = not report["valid"]

    expectation_met = actual_failure if expected_failure else not actual_failure

    return {
        "fixture": str(path),
        "expected": "fail" if expected_failure else "pass",
        "actual": "fail" if actual_failure else "pass",
        "passed": expectation_met,
        "validation": report,
    }


def validate_fixtures(pattern: str) -> dict[str, Any]:
    """Validate fixture files matching a glob pattern."""
    fixture_paths = [
        Path(match)
        for match in sorted(glob.glob(pattern))
        if Path(match).is_file()
    ]

    results = [validate_fixture(path) for path in fixture_paths]
    failed_results = [result for result in results if not result["passed"]]

    return {
        "pattern": pattern,
        "passed": len(failed_results) == 0,
        "summary": {
            "fixtures": len(results),
            "passed": len(results) - len(failed_results),
            "failed": len(failed_results),
        },
        "results": results,
    }


def process(
    input_value: str | Path | Any,
    *,
    conformance_classes: list[str] | None = None,
    fail_on_error: bool = False,
) -> str:
    """Process one transform input and return a JSON validation report string."""
    data = load_json_document(input_value)
    report = validate_document(data, conformance_classes=conformance_classes)

    if fail_on_error and not report["valid"]:
        raise ValueError(
            "Topology validation failed with "
            f"{report['summary']['errors']} error(s)."
        )

    return json.dumps(report, indent=2)


def main() -> int:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="Validate Topo Feature topology data.")
    parser.add_argument(
        "input",
        nargs="?",
        help="Input JSON file or fixture glob. Example: _sources/features/topology-validator/tests/*.json",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Write JSON report to this file instead of stdout.",
    )
    parser.add_argument(
        "--fixtures",
        action="store_true",
        help="Treat input as fixture glob and apply *-fail.json expectation logic.",
    )
    parser.add_argument(
        "--conformance-class",
        action="append",
        dest="conformance_classes",
        help="Run only the selected conformance class. Can be repeated.",
    )

    args = parser.parse_args()

    if not args.input:
        parser.error("An input file or fixture glob is required.")

    if args.fixtures:
        report = validate_fixtures(args.input)
        exit_code = 0 if report["passed"] else 1
    else:
        report = validate_document(
            load_json_document(Path(args.input)),
            source=args.input,
            conformance_classes=args.conformance_classes,
        )
        exit_code = 0 if report["valid"] else 1

    report_text = json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(report_text + "\n", encoding="utf-8")
    else:
        print(report_text)

    return exit_code


_transform_input_data = globals().get("input_data")

if _transform_input_data is not None:
    _metadata = get_transform_metadata()
    output_data = process(
        _transform_input_data,
        fail_on_error=bool(_metadata.get("fail_on_error", False)),
    )
elif __name__ == "__main__":
    raise SystemExit(main())