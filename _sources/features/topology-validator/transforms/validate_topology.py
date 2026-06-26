#!/usr/bin/env python3

"""Topology validation transform and fixture runner.

In Building Blocks transform mode, this script validates one input JSON document
and returns the configured validation report format.

When run directly, it can validate one file or a glob of fixture files. In fixture
mode, files ending with "-fail.json" are expected to produce validation errors;
all other JSON files are expected to pass.
"""

from __future__ import annotations

import argparse
import glob
import json
import re
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
from topo_validator.model import Issue, Severity  # noqa: E402
from topo_validator.report import to_html_report, to_json_report, to_text_report  # noqa: E402
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


def _string_or_none(value: Any) -> str | None:
    """Return a string value or None."""
    return value if isinstance(value, str) else None


def _issue_severity(value: Any) -> Severity:
    """Return valid issue severity."""
    return "warning" if value == "warning" else "error"


def _issue_extra(value: Any) -> dict[str, Any]:
    """Return issue extra data when it is a dictionary."""
    if not isinstance(value, dict):
        return {}

    return {str(key): extra_value for key, extra_value in value.items()}


def issue_to_json(issue: Any) -> Issue:
    """Convert a validator issue into a JSON-serializable dictionary."""
    if isinstance(issue, dict):
        return {
            "code": str(issue.get("code", "")),
            "severity": _issue_severity(issue.get("severity")),
            "message": str(issue.get("message", "")),
            "object_id": _string_or_none(issue.get("object_id")),
            "path": _string_or_none(issue.get("path")),
            "extra": _issue_extra(issue.get("extra")),
        }

    return {
        "code": str(getattr(issue, "code", "")),
        "severity": _issue_severity(getattr(issue, "severity", None)),
        "message": str(getattr(issue, "message", str(issue))),
        "object_id": _string_or_none(getattr(issue, "object_id", None)),
        "path": _string_or_none(getattr(issue, "path", None)),
        "extra": _issue_extra(getattr(issue, "extra", {})),
    }


def get_transform_metadata() -> dict[str, Any]:
    """Return Building Blocks transform metadata when available."""
    for metadata_object in (
        globals().get("transform_metadata"),
        globals().get("metadata"),
    ):
        if isinstance(metadata_object, dict):
            nested_metadata = metadata_object.get("metadata")
            if isinstance(nested_metadata, dict):
                return nested_metadata
            return metadata_object

        metadata = getattr(metadata_object, "metadata", None)

        if isinstance(metadata, dict):
            return metadata

    return {}


def get_transform_source_name(metadata: dict[str, Any]) -> str | None:
    """Return the transform input source name when the runner provides one."""
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


def title_to_json_filename(title: str) -> str | None:
    """Return a safe JSON filename derived from a human-readable title."""
    normalised = re.sub(r"[^0-9A-Za-z]+", "-", title).strip("_").lower()

    if not normalised:
        return None

    return f"{normalised}.json"


def get_document_source_name(data: dict[str, Any]) -> str | None:
    """Return a source name declared or derived from the input document."""
    metadata = data.get("metadata")

    if isinstance(metadata, dict):
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

    for key in ("surveyTitle", "name"):
        value = data.get(key)
        if isinstance(value, str) and value:
            source_name = title_to_json_filename(value)
            if source_name is not None:
                return source_name

    return None


def format_validation_report(
    issues: list[Any],
    output_format: str,
    *,
    source: str | None = None,
) -> str:
    """Return validation issues formatted as JSON, HTML, or text."""
    report_format = output_format.lower()
    normalized_issues = [issue_to_json(issue) for issue in issues]

    if report_format == "html":
        return to_html_report(normalized_issues, source_name=source)
    if report_format == "json":
        return to_json_report(normalized_issues)
    if report_format == "text":
        return to_text_report(normalized_issues)

    raise ValueError(f"Unsupported output format: {output_format!r}")


def run_validation(
    data: dict[str, Any],
    *,
    source: str | None = None,
    conformance_classes: list[str] | None = None,
    progress: Any | None = None,
) -> tuple[dict[str, Any], list[Issue]]:
    """Validate one topology document and return the JSON report plus raw issues."""
    topology_data = from_csdm_json(data)
    issues = validate_topology(
        topology_data,
        conformance_classes=conformance_classes,
        progress=progress,
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

    report = {
        "source": source,
        "valid": len(errors) == 0,
        "summary": {
            "issues": len(normalized_issues),
            "errors": len(errors),
            "warnings": len(warnings),
        },
        "issues": normalized_issues,
    }

    return report, issues


def validate_document(
    data: dict[str, Any],
    *,
    source: str | None = None,
    conformance_classes: list[str] | None = None,
) -> dict[str, Any]:
    """Validate one topology document and return a JSON report."""
    report, _issues = run_validation(
        data,
        source=source,
        conformance_classes=conformance_classes,
    )
    return report


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
    output_format: str = "json",
    source: str | None = None,
    progress: Any | None = None,
) -> str:
    """Process one transform input and return a validation report string."""
    if source is None and isinstance(input_value, Path):
        source = input_value.name

    data = load_json_document(input_value)

    if source is None:
        source = get_document_source_name(data)

    report, issues = run_validation(
        data,
        source=source,
        conformance_classes=conformance_classes,
        progress=progress,
    )

    if fail_on_error and not report["valid"]:
        raise ValueError(
            "Topology validation failed with "
            f"{report['summary']['errors']} error(s)."
        )

    return format_validation_report(
        issues,
        output_format,
        source=source,
    )


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
        help="Write report to this file instead of stdout.",
    )
    parser.add_argument(
        "--format",
        choices=["json", "html", "text"],
        default="json",
        help="Report format for single-file validation.",
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
        if args.format != "json":
            parser.error("--fixtures only supports the JSON aggregate report.")
        report = validate_fixtures(args.input)
        report_text = json.dumps(report, indent=2)
        exit_code = 0 if report["passed"] else 1
    else:
        data = load_json_document(Path(args.input))
        report, issues = run_validation(
            data,
            source=args.input,
            conformance_classes=args.conformance_classes,
        )
        report_text = format_validation_report(
            issues,
            args.format,
            source=args.input,
        )
        exit_code = 0 if report["valid"] else 1

    if args.output:
        Path(args.output).write_text(report_text + "\n", encoding="utf-8")
    else:
        print(report_text)

    return exit_code


def run_transform_from_globals(default_output_format: str = "json") -> None:
    """Run the Building Blocks transform when input_data is available."""
    transform_input_data = globals().get("input_data")

    if transform_input_data is None:
        return

    metadata = get_transform_metadata()
    verbose = bool(metadata.get("verbose", False))
    globals()["output_data"] = process(
        transform_input_data,
        fail_on_error=bool(metadata.get("fail_on_error", False)),
        output_format=str(metadata.get("output_format", default_output_format)),
        source=get_transform_source_name(metadata),
        progress=print if verbose else None,
    )


run_transform_from_globals()

if __name__ == "__main__":
    raise SystemExit(main())
