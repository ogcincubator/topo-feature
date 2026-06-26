import runpy
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
TRANSFORM_PATH = (
    REPO_ROOT
    / "_sources"
    / "features"
    / "topology-validator"
    / "transforms"
    / "validate_topology.py"
)
EXAMPLE_PATH = (
    REPO_ROOT
    / "_sources"
    / "features"
    / "topology-validator"
    / "examples"
    / "cube.json"
)


def test_process_html_uses_standalone_html_report():
    module_globals = runpy.run_path(str(TRANSFORM_PATH), run_name="topology_transform_test")

    report = module_globals["process"](
        EXAMPLE_PATH,
        output_format="html",
        source=EXAMPLE_PATH.name,
    )

    assert report.startswith("<!doctype html>")
    assert "<h1>Topology Validation Report</h1>" in report
    assert "<h2>Rule results</h2>" in report
    assert f"<strong>{EXAMPLE_PATH.name}</strong>" in report


def test_transform_mode_reads_plain_dict_metadata_for_html_output():
    result_globals = runpy.run_path(
        str(TRANSFORM_PATH),
        init_globals={
            "input_data": EXAMPLE_PATH.read_text(encoding="utf-8"),
            "transform_metadata": {
                "output_format": "html",
                "fail_on_error": False,
            },
        },
        run_name="topology_transform_test",
    )

    output_data = result_globals["output_data"]

    assert output_data.startswith("<!doctype html>")
    assert "Topology Validation Report" in output_data
    assert '"valid"' not in output_data
