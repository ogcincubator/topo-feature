## Question

> GeoSPARQL defines a topology relation and function `sfWithin` based on `simpleFeatures` 2D topology.  
> What is the equivalent generalised term grounded in ISO 19107 that applies to 3D topology?
> Is this formalised in schemas or vocabularies published by any authority?

### `sfWithin` to the ISO 19107 generalisation: **`contains`** (and its converse `within`)

#### The 2D foundation: `sfWithin` and DE-9IM

GeoSPARQL's `sfWithin` is named with the `sf` prefix to signal its grounding in the **OGC/ISO Simple Features Access** model (ISO 19125), which restricts topology to **2-dimensional Euclidean space (ℝ²)**. 
The function tests whether the first geometry is spatially within the second, with the defining DE-9IM intersection pattern `T*F**F***`. 
GeoSPARQL also carries the Egenhofer-family equivalent `ehInside`/`ehContains`, and the corresponding RCC8 predicates `rcc8ntpp`/`rcc8ntppi`, all expressed as implementable topology-vocabulary properties in the standard.

The DE-9IM itself, while powerful, was originally formulated for **2D regions in ℝ²**. 
It describes the spatial relations of two regions (two geometries in two dimensions, R²) in geometry, point-set topology, and geospatial topology.

#### The ISO 19107 generalisation: `Geometry::contains()` / `Geometry::within()`

The ISO 19107 Spatial Schema describes an **n-dimensional generalisation**. 
Where Simple Features is restricted to 2D, ISO 19107 specifies conceptual schemas and spatial operations for geographic entities covering vector geometry and topology, with geometric coordinate spaces having up to three spatial dimensions, one temporal dimension, and any number of other spatially dependent parameters as needed by a particular application. 
In general, the topological dimension of the spatial projections of the geometric objects will be at most three.

In ISO 19107, topology is defined on the root class **`Geometry`** (equivalent to the older `GM_Object`), and the containment predicate is simply named **`contains()`** (with its converse **`within()`**). 
These are defined as operations on `Geometry` objects in full generality across dimensionalities: points (GM_Point, 0D), curves (GM_Curve, 1D), surfaces (GM_Surface, 2D), and **solids (GM_Solid, 3D)**. 
The 3D primitives as defined in ISO 19107 are a generalisation to 3D of the 2D ones: a 0D primitive is a GM_Point, a 1D a GM_Curve, a 2D a GM_Surface, and a 3D a GM_Solid.
Each d-dimensional primitive is built with a set of (d-1)-dimensional primitives.

The key conceptual distinction is:

| Term                                | Standard                        | Scope                                     |
|-------------------------------------|---------------------------------|-------------------------------------------|
| `sfWithin`                          | OGC Simple Features / ISO 19125 | 2D geometries only, DE-9IM in ℝ²          |
| `Geometry::within()` / `contains()` | **ISO 19107 Spatial Schema**    | n-dimensional (0D–3D), including GM_Solid |

The `sf` prefix in `sfWithin` is explicitly there to signal this 2D restriction. 
The ISO 19107 `contains`/`within` operations are the dimension-agnostic, set-theoretic equivalents grounded in point-set topology. 
A geometry **A** `contains` geometry **B** if and only if every point of **B** is also a point of **A**, which applies identically whether **A** and **B** are solids, surfaces, curves, or points.

#### Is this formalised in published schemas or vocabularies?

**The answer is: partially, and with notable gaps.**

**1. ISO 19107:2019 UML/Conceptual Schema (normative)**
The operations are fully specified in the ISO standard itself. 
ISO 19107:2019 is the second edition, reviewed and confirmed in 2025, and remains current. 
It defines `Geometry::contains()`, `Geometry::within()`, and the full DE-9IM-based predicate family as operations on `Geometry` objects up to 3D topological dimension.

**2. GeoSPARQL 1.1 (OGC, 2022/2024) — partial**
The class `geo:Geometry` is conceptually derived from the UML class `Geometry` in ISO 19107, described as _the root class of the geometric object taxonomy and supports interfaces common to all geographically referenced geometric objects._ 
However, GeoSPARQL's topology relations (including `sfWithin`) are practically restricted to 2D geometry because the WKT and GML serialisations used by virtually all implementations don't support solid geometry semantics for topological testing.

**3. ISO/TC 211 OWL Ontologies (def.isotc211.org) — not yet available**
This is the most significant gap. 
No ontologies have yet been published in production by ISO/TC 211. 
Previously TC-211 test-published ontologies in XML only, but these have been withdrawn. 
A complete set of TC-211 Harmonised Model-based ontologies are expected by May 2026. 
So the ISO 19107:2019 `contains`/`within` operations are **not yet formally published as a Semantic Web vocabulary** under the authoritative `def.isotc211.org` namespace. 
A 2003-edition OWL rendering was produced experimentally by CSIRO/GOM and hosted at `def.seegrid.csiro.au`, but this is unofficial and based on the superseded edition.

**4. GML 3.x (OGC) — serialisation only**
GML (Geography Markup Language) encodes ISO 19107 geometry classes including `gml:Solid`, but does not define topology predicate operations as vocabulary terms.

**5. Research / community implementations**
The DE-9IM extended to 3D has been studied academically. 
3D-to-3D solid and 2D-to-2D surface topological interactions have been defined and proved using the DE-9IM, with "meet (touches)" and "overlaps" being the main topological relationships used in the 3D cadastre context. 
There is also work extending GeoSPARQL with 3D topology (e.g., for BIM/IFC and CityGML), but none is yet formalised as an OGC or ISO normative vocabulary.

#### Summary

The generalised ISO 19107 term equivalent to `sfWithin` is simply **`contains`** (or its converse `within`), defined as an operation on **`Geometry`** objects applicable across all dimensions from 0D to 3D, including on `GM_Solid` objects. 
The `sf` prefix in GeoSPARQL signals the restriction to the OGC Simple Features 2D subset. 
The full 3D-capable version is normatively specified in **ISO 19107:2019** but is not yet published as a live, resolvable Semantic Web vocabulary.
We note publication from ISO/TC 211 GOM is expected imminently (reportedly targeting mid-2026).