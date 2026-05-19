# Face Topology Feature

A **Face** is a topological feature representing a bounded planar region (a polygon surface) described by an outer boundary Ring and zero or more inner boundary Rings (holes).

## Topology Model

A Face's topology consists of:

- `type`: `"Face"`
- `rings`: an ordered array of Ring topology objects
  - The **first** ring is the **outer boundary**
  - Any **subsequent** rings are **inner boundaries** (holes)

Each Ring contains a `directed_references` array — an ordered list of [Oriented Object References](../../datatypes/oriented-ref/) that reference Edge features, with orientation (`+` or `-`) indicating direction of traversal.

The `geometry` property is `null` — actual coordinates are derived from the referenced Edge and Point features.

## Relationship to other types

| Lower dimension                                            | Face dimension                                    | Higher dimension                                    |
|:-----------------------------------------------------------|---------------------------------------------------|:----------------------------------------------------|
| **Edge** <br/>(referenced in **Ring** directed_references) | **Face** <br/> (directed_references to **Rings**) | **Shell** <br/>(directed_references to  **Faces** ) |

Note **directed references** are required for 3D, whereas 2D may use **ordered references**, and directions can be calculated if required. For 3D this calculation burden is much greater and explicit directions are required.