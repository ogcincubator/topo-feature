# Topology Validator

## Overview

The Topology Validator Building Block defines a validation framework for Topo Feature datasets and related 3D CSDM encodings.

The validator provides automated topology quality checks for points, curves, surfaces, shells, solids, parcel relationships, and containment relationships represented using the Topo Feature Building Blocks.

The validator is intended to support conformance testing, data quality assessment, and implementation verification for 3D cadastral datasets.

## Scope

This Building Block specifies:

* topology validation conformance classes;
* topology validation report structure;
* execution of topology validation rules against Topo Feature datasets; and
* mapping of validation results to human-readable reports.

This Building Block does not redefine topology rules. The authoritative topology rules are defined in the referenced documents.

## Conformance Classes

The validator currently supports the following conformance classes:

| Class | Description                        |
| ----- | ---------------------------------- |
| CC-01 | Point topology                     |
| CC-02 | Curve topology                     |
| CC-03 | Surface topology                   |
| CC-04 | Shell topology                     |
| CC-05 | Solid topology                     |
| CC-06 | Solid relationship topology        |
| CC-07 | Parcel containment topology        |
| CC-08 | 2D / 2.5D parcel coverage topology |

Each conformance class consists of one or more topology validation rules.

## Validation Rules

The topology rules implemented by this validator are defined in:

* [WA 3D CSDM Topology Rules](https://github.com/surroundaustralia/topo-feature/blob/topo-feature-ah-topo-validation/proposals/topology_rules.md)
* [NGSC Topology Questions and Responses](https://github.com/surroundaustralia/topo-feature/blob/topo-feature-ah-topo-validation/proposals/response_to_topology_questions.md)

These documents define rule identifiers, scope, interpretation guidance, implementation notes, examples, and known limitations.

Implementations may support all or a subset of the available rules.

## Validation Reports

Validation results shall be reported as individual rule outcomes.

Each reported issue should include:

* Rule identifier
* Severity
* Affected object identifier
* Human-readable message
* Optional implementation-specific diagnostic information

Implementations may additionally provide machine-readable outputs.

## References

* Topo Feature Building Blocks
* WA 3D CSDM Topology Rules
* NGSC Topology Questions and Responses
* ISO 19107 Geographic Information — Spatial Schema
* OGC Features and Geometries Standards
* OGC Building Blocks Framework
