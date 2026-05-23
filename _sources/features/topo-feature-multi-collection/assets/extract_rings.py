"""
extract_rings.py

Processes a topology JSON file (either a flat FeatureCollection or a
structured document with named arrays like points/edges/faces/solids).

For each inline topology object found inside directed_references or shells
that has a "type" key (i.e. is an inline Ring, Shell, etc. rather than a
plain {ref, orientation} pointer):
  - A new Feature is created with a fresh uuid
  - The inline object is replaced with a {ref, orientation:"+"} pointer
  - The new Feature is appended to the appropriate named array
    (Ring -> rings, Shell -> shells_out, or a configurable mapping)

Usage:
    python extract_rings.py input.json output.json
    python extract_rings.py input.json          # writes input_extracted.json
"""

import json
import uuid
import sys
from pathlib import Path


# Maps topology type -> which top-level array to collect into.
# Extend this dict for new types as needed.
TYPE_TO_ARRAY = {
    "Ring":  "rings",
    "Shell": "shells",
}

DEFAULT_ARRAY = "extracted"   # fallback if type not in mapping


def make_uuid() -> str:
    return f"uuid:{uuid.uuid4()}"


def extract_from_directed_refs(directed_refs: list, collected: dict) -> list:
    """
    Walk a directed_references list. Any item that is an inline topology
    object (has a "type" key) is hoisted: wrapped as a Feature, stored in
    collected[array_name], and replaced with a plain pointer.
    Returns the updated list.
    """
    new_refs = []
    for item in directed_refs:
        if not isinstance(item, dict):
            new_refs.append(item)
            continue

        if "type" in item:
            # Recurse first so deeper nesting is resolved bottom-up
            item = extract_topology_node(item, collected)

            new_id = make_uuid()
            topo_type = item.get("type", "")
            array_name = TYPE_TO_ARRAY.get(topo_type, DEFAULT_ARRAY)

            feature = {
                "id": new_id,
                "type": "Feature",
                "geometry": None,
                "topology": item,
                "properties": {},
            }
            collected.setdefault(array_name, []).append(feature)
            new_refs.append({"ref": new_id, "orientation": "+"})
        else:
            new_refs.append(item)

    return new_refs


def extract_topology_node(node: dict, collected: dict) -> dict:
    """
    Recursively process a topology node, extracting any inline children
    from directed_references or shells[].directed_references.
    """
    # Handle directed_references at this level
    if "directed_references" in node and isinstance(node["directed_references"], list):
        node["directed_references"] = extract_from_directed_refs(
            node["directed_references"], collected
        )

    # Handle shells list (Solid topology pattern)
    if "shells" in node and isinstance(node["shells"], list):
        new_shells = []
        for shell in node["shells"]:
            if isinstance(shell, dict) and "type" in shell:
                # Inline Shell object — recurse into it then hoist
                shell = extract_topology_node(shell, collected)
                new_id = make_uuid()
                array_name = TYPE_TO_ARRAY.get(shell.get("type", ""), DEFAULT_ARRAY)
                feature = {
                    "id": new_id,
                    "type": "Feature",
                    "geometry": None,
                    "topology": shell,
                    "properties": {},
                }
                collected.setdefault(array_name, []).append(feature)
                new_shells.append({"ref": new_id, "orientation": "+"})
            else:
                new_shells.append(shell)
        node["shells"] = new_shells

    return node


def process_feature(feature: dict, collected: dict) -> dict:
    """Process a single Feature's topology in-place."""
    topology = feature.get("topology")
    if isinstance(topology, dict):
        feature["topology"] = extract_topology_node(topology, collected)
    return feature


def process(data: dict) -> dict:
    """
    Accept either:
      - A flat FeatureCollection  (features array)
      - A structured document     (named arrays: points, edges, faces, solids, …)
    Returns the document with inline topology objects hoisted out.
    """
    collected: dict = {}   # array_name -> [Feature, ...]

    if data.get("type") == "FeatureCollection" and isinstance(data.get("features"), list) and data["features"]:
        # Flat FeatureCollection
        data["features"] = [process_feature(f, collected) for f in data["features"]]
    else:
        # Structured document — walk every named array whose items look like Features
        SKIP_KEYS = {"type", "metadata"}
        for key, value in data.items():
            if key in SKIP_KEYS or not isinstance(value, list):
                continue
            for item in value:
                if isinstance(item, dict):
                    # Each item may itself be a FeatureCollection wrapper
                    if item.get("type") == "FeatureCollection" and isinstance(item.get("features"), list):
                        item["features"] = [process_feature(f, collected) for f in item["features"]]
                    elif item.get("type") == "Feature":
                        process_feature(item, collected)

    # Merge collected arrays back into the document
    for array_name, features in collected.items():
        if array_name in data and isinstance(data[array_name], list):
            data[array_name].extend(features)
        else:
            data[array_name] = features

    return data


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_rings.py input.json [output.json]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = (
        Path(sys.argv[2]) if len(sys.argv) >= 3
        else input_path.with_name(input_path.stem + "_extracted" + input_path.suffix)
    )

    with input_path.open(encoding="utf-8") as f:
        data = json.load(f)

    result = process(data)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    # Summary
    total = sum(len(v) for v in {k: result.get(k, []) for k in TYPE_TO_ARRAY.values()}.values())
    for array_name in sorted(set(TYPE_TO_ARRAY.values()) | {DEFAULT_ARRAY}):
        arr = result.get(array_name)
        if arr:
            print(f"  {array_name}: {len(arr)} feature(s)")
    print(f"Output written to: {output_path}")


if __name__ == "__main__":
    main()
