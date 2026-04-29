# Tool Support for Referenced Local / Engineering CRS Data

The 3D CSDM requires authoritative survey observations and cadastral geometry to be supplied using a jurisdictionally recognised coordinate reference system (CRS). 
However, supporting datasets referenced during preparation, review, validation, or visualisation may originate from BIM, CAD, engineering, architectural, or project-local coordinate systems.

This note describes a tool-support capability for documenting and using those local coordinate systems so that supporting data can be transformed, visualised, and compared against 3D CSDM content in a recognised CRS. 
The intent is not to permit authoritative 3D CSDM survey observations or cadastral geometry to be delivered in a local Engineering CRS. 
Rather, it is to allow software tools to understand how externally referenced local-grid datasets can be positioned relative to a jurisdictional CRS used by a 3D CSDM package.

A tool consuming a 3D CSDM package, or associated supporting data, should be able to identify the source local CRS, identify the target jurisdictional CRS, and apply a documented coordinate operation where such information is available. 
This may support visualisation of BIM or CAD context, comparison with survey geometry, quality assurance, and transformation of non-authoritative supporting data such as referenced Occupation Information, into a map-ready coordinate space.

## Background

## Background

This document is a preliminary work in progress. 
There is ongoing work by OGC to develop a Semantic Web counterpart to [ISO 19111:2019 Geographic Information - Referencing by Coordinates](https://www.iso.org/obp/ui/en/#iso:std:iso:19111:ed-3:v1:en).  
The OGC work can be found in the [OGC CRS Ontology project](https://github.com/opengeospatial/ontology-crs).

The OGC CRS Ontology provides vocabularies for describing coordinate reference systems, spatial reference systems, and their components.
The work is expected to include modules for core CRS concepts, coordinate systems, coordinate operations, datums, and related CRS metadata.
This is relevant to 3D CSDM tooling because local CRS support should not be treated only as a JSON or matrix convention. 
It should also be expressible as a set of CRS and coordinate-operation resources that can be understood by people and machines.

Local or Engineering CRSs are commonly used in BIM, CAD, engineering, architectural, and construction datasets.  
These systems are often defined relative to a project origin, building grid, site control point, BIM Project Base Point, or another local reference point.  
They may also use project-specific axis directions, rotations, scale factors, vertical references, or unit conventions.

[OGC WKT2:2019](https://docs.ogc.org/is/18-010r7/18-010r7.html) recognises Local or Engineering CRSs.
It is also aligned with [ISO 19111:2019 Geographic Information - Referencing by Coordinates](https://www.iso.org/obp/ui/en/#iso:std:iso:19111:ed-3:v1:en), and [ISO 19162:2019 Geographic Information - Well-known text representation of coordinate reference systems](https://www.iso.org/obp/ui/en/#iso:std:iso:19162:ed-2:v1:en).
[PROJJSON](https://proj.org/en/stable/specifications/projjson.html) provides a JSON encoding of [OGC WKT2:2019](https://docs.ogc.org/is/18-010r7/18-010r7.html) / [ISO 19162](https://www.iso.org/obp/ui/en/#iso:std:iso:19162:ed-2:v1:en) CRS concepts and can be converted to and from [WKT2:2019](https://docs.ogc.org/is/18-010r7/18-010r7.html).
This makes [PROJJSON](https://proj.org/en/stable/specifications/projjson.html) suitable for JSON-based tooling where a machine-readable CRS or coordinate operation definition is required.

BIM adopts a similar concept.
In [IFC, `IfcMapConversion`](https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcMapConversion.htm) is used to transform a local engineering coordinate system into a defined map CRS.  
It is useful for 3D CSDM tooling to be broadly compatible with standards such as [IFC](https://ifc43-docs.standards.buildingsmart.org/), because BIM data is expected to become a common supporting data format in 3D CSDM workflows.

The 3D CSDM need not adopt BIM terminology directly.
For example, a BIM Project Base Point may be represented more generally as a `localOrigin`, `sourceControlPoint`, or transformation reference point.
The important requirement is that tooling can understand the source CRS, target CRS, coordinate operation, operation parameters, axis definitions, units, rotations, scale, vertical reference, and provenance needed to position the supporting data correctly.

## Ontology Alignment

To align with the OGC CRS Ontology, local CRS transformation metadata should distinguish between:

1. the **source CRS**, usually a local or Engineering CRS used by the supporting dataset;
2. the **target CRS**, usually the jurisdictional or recognised CRS used by the 3D CSDM package;
3. the **coordinate operation** that transforms coordinates from the source CRS to the target CRS;
4. the **operation method**, such as a Helmert, similarity, affine, translation, rotation, or scale operation;
5. the **operation parameters**, such as translation, rotation, scale, matrix coefficients, units, and accuracy; and
6. the **operation encoding**, such as [WKT2](https://docs.ogc.org/is/18-010r7/18-010r7.html), [PROJJSON](https://proj.org/en/stable/specifications/projjson.html), or a 4 $\times$ 4 implementation matrix.

The matrix, [WKT2](https://docs.ogc.org/is/18-010r7/18-010r7.html), or [PROJJSON](https://proj.org/en/stable/specifications/projjson.html) representation should be treated as an implementation or serialisation of the coordinate operation.
It should not be treated as the only semantic description of the CRS relationship.

In this pattern:

- the local BIM, CAD, engineering, or project coordinate system is described as an Engineering CRS;
- the jurisdictional CRS is identified by an EPSG or OGC CRS URI where possible;
- the transformation is described as a coordinate operation resource;
- the operation identifies its source CRS and target CRS;
- the operation identifies its method and parameters; and
- any executable matrix, [WKT2](https://docs.ogc.org/is/18-010r7/18-010r7.html), or [PROJJSON](https://proj.org/en/stable/specifications/projjson.html) encoding is carried as an implementation encoding of the coordinate operation.

## Tool Capability

Where supporting data referenced by a 3D CSDM package is supplied in a local, engineering, BIM, CAD, or project coordinate system, tools should be able to read or receive metadata describing that local coordinate system and its relationship to a recognised target CRS.

The transformation metadata should be sufficient to allow the supporting data to be positioned, visualised, or compared against 3D CSDM survey and cadastral content expressed in the required jurisdictional CRS.
The transformation metadata should not be interpreted as replacing the CRS requirements for authoritative 3D CSDM survey observations or cadastral geometry.

## Example Local CRS and Transformation Metadata

An example of local CRS and coordinate operation metadata using a JSON-LD style structure suitable for tool support might look like the following:

```json
{
  "@context": {
    "geosrs": "https://w3id.org/geosrs/",
    "srs": "https://w3id.org/geosrs/srs/",
    "co": "https://w3id.org/geosrs/co/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "csdm-crs": "https://example.org/3d-csdm/crs-support/"
  },
  "coordinateReferenceSystems": [
    {
      "@id": "csdm-crs:crs/local-building-a",
      "@type": "srs:EngineeringCRS",
      "rdfs:label": "Building A BIM Local Engineering CRS",
      "description": "Local BIM coordinate system based on the project base point.",
      "coordinateSystem": {
        "type": "CartesianCS",
        "axis": [
          {
            "name": "local X",
            "abbreviation": "X",
            "direction": "east",
            "unit": "metre"
          },
          {
            "name": "local Y",
            "abbreviation": "Y",
            "direction": "north",
            "unit": "metre"
          },
          {
            "name": "local Z",
            "abbreviation": "Z",
            "direction": "up",
            "unit": "metre"
          }
        ]
      }
    },
    {
      "@id": "http://www.opengis.net/def/crs/EPSG/0/7850",
      "@type": "srs:ProjectedCRS",
      "authority": "EPSG",
      "code": "7850",
      "rdfs:label": "GDA2020 / MGA zone 50"
    }
  ],
  "coordinateOperations": [
    {
      "@id": "csdm-crs:operation/local-to-map",
      "@type": "co:CoordinateOperation",
      "rdfs:label": "Building A local engineering CRS to GDA2020 / MGA zone 50",
      "co:sourceCRS": "csdm-crs:crs/local-building-a",
      "co:targetCRS": "http://www.opengis.net/def/crs/EPSG/0/7850",
      "operationMethod": "Restricted Helmert / similarity transformation with Z-axis rotation",
      "localOrigin": {
        "x": 392000.0,
        "y": 6465000.0,
        "z": 12.4,
        "crs": "http://www.opengis.net/def/crs/EPSG/0/7850"
      },
      "operationParameters": {
        "translation": {
          "tx": 392000.0,
          "ty": 6465000.0,
          "tz": 12.4,
          "unit": "metre"
        },
        "rotation": {
          "zAxisDegrees": 34.46031,
          "unit": "degree"
        },
        "scale": {
          "value": 1.0,
          "unit": "unity"
        }
      },
      "operationConventions": {
        "transformationDirection": "source-to-target",
        "matrixConvention": "column-vector; target = M * source",
        "axisConvention": "right-handed; X east, Y north, Z up",
        "zAxisRotationConvention": "positive counter-clockwise from +X/east"
      },
      "implementationMatrix": [
        [0.8243, -0.5662, 0.0, 392000.0],
        [0.5662,  0.8243, 0.0, 6465000.0],
        [0.0,     0.0,    1.0, 12.4],
        [0.0,     0.0,    0.0, 1.0]
      ],
      "operationEncoding": {
        "format": "PROJJSON",
        "definition": {}
      }
    }
  ]
}
```

This provides:

- a semantic description of the source CRS;
- a semantic reference to the target CRS;
- a coordinate operation resource linking the two CRSs;
- human-readable transformation parameters;
- explicit implementation conventions; and
- an executable matrix or standards-based operation encoding.

The `operationEncoding.definition` field may contain, or reference, the authoritative machine-readable CRS or coordinate operation definition.
The `implementationMatrix` is useful for execution by software, but it should be accompanied by the source CRS, target CRS, operation method, parameter values, units, direction, and conventions.

For tooling, the authoritative CRS or coordinate operation definition should preferably be one of:

1. an EPSG URI or code, where the CRS is already known;
2. [WKT2:2019](https://docs.ogc.org/is/18-010r7/18-010r7.html), where a complete custom CRS or coordinate operation must be defined; 
3. [PROJJSON](https://proj.org/en/stable/specifications/projjson.html), where a native JSON representation of [WKT2 / ISO 19111](https://docs.ogc.org/is/18-010r7/18-010r7.html) concepts is required; or 
4. an ontology-aligned CRS and coordinate-operation resource, where Linked Data / Semantic Web expression is required.

[PROJ4](https://proj4js.org/) strings may be useful for compatibility with some software, but should not be treated as the authoritative definition for custom local, engineering, vertical, or Helmert / affine transformation metadata.

## Helmert vs Affine Transformations

A Helmert or similarity transformation is often sufficient for transforming BIM or CAD coordinates into a known CRS where the supporting dataset has a limited geographic footprint. 
A typical [3D Helmert transformation](https://proj.org/en/stable/operations/transformations/helmert.html) uses:

```text
translation in X, Y, Z
rotation about X, Y, Z
one common scale factor
```

For simple map-alignment use cases, a restricted Helmert / similarity transformation may use:

```text
translation in X, Y, Z
rotation about the Z axis
one common scale factor
```

This restricted form is suitable where the supporting dataset only needs to be shifted, rotated in plan, and scaled uniformly to align with the target CRS.
It preserves shape because the same scale factor is applied to all axes.

However, some supporting data may require an Affine transformation. 
The main difference is that a Helmert transformation applies one common scale factor, whereas an Affine transformation can support different scale factors for each axis and, where required, a full transformation matrix.

A [3D Affine transformation](https://proj.org/en/stable/operations/transformations/affine.html) may use:

```
translation in X, Y, Z
rotation about X, Y, Z
scale factor for X, Y, and Z
optional shear terms
```

In ontology-aligned terms, both Helmert and Affine transformations should be described as coordinate operations.
The operation method and operation parameters should make clear whether the transformation is a restricted similarity transformation, a full Helmert transformation, an affine transformation, or another operation type.

## Helmert / Similarity Transformation as a Coordinate Operation

For tool-support purposes, a Helmert or similarity transformation should be described as a coordinate operation between a source CRS and a target CRS.

In the local CRS use case, the source CRS will commonly be an Engineering CRS representing the BIM, CAD, engineering, or project-local coordinate system.
The target CRS will normally be the jurisdictional or recognised CRS used to visualise or compare the supporting data with 3D CSDM content.

A restricted Helmert / similarity transformation can be used where the supporting data can be positioned using:

- translation in X, Y, and Z;
- rotation, often only about the Z axis for simple map alignment; and
- one common scale factor.

This transformation preserves shape because the same scale factor is applied to all axes.
In implementation, the transformation may be represented as a 4 $\times$ 4 homogeneous matrix.
Semantically, however, it should be treated as a coordinate operation with a source CRS, target CRS, operation method, operation parameters, and stated conventions.


## Suggested Tool Support Requirement

Tools supporting 3D CSDM preparation, validation, review, or visualisation should be able to use transformation metadata for supporting datasets supplied in local, engineering, BIM, CAD, or project coordinate systems.

Where such supporting data is referenced, the tool should be able to identify the source local CRS and apply a documented coordinate operation to a recognised target CRS, such as the jurisdictional CRS used by the 3D CSDM package.
The coordinate operation should include, as required:

- the source CRS;
- the target CRS;
- the coordinate operation method;
- operation parameters;
- local origin expressed in the target CRS;
- axis definitions;
- units;
- rotation convention;
- scale factor or transformation matrix;
- vertical reference;
- transformation accuracy or uncertainty; and
- provenance.

This requirement supports visualisation and comparison of referenced supporting data.
It does not permit authoritative 3D CSDM survey observations or cadastral geometry to be supplied in a non-jurisdictional CRS unless allowed by the relevant jurisdiction.

## Suggested Capability Levels

The following capability levels could be used by tools to support referenced local CRS data.

### Level 1: Known CRS Only

Use where the supporting dataset is already supplied in a recognised CRS.

```json
{
  "horizontalCRS": "http://www.opengis.net/def/crs/EPSG/0/7850",
  "verticalCRS": "http://www.opengis.net/def/crs/EPSG/0/5711"
}
```
### Level 2: Local Engineering CRS with Simple Map Conversion

Use where the supporting BIM or CAD data is supplied in a local coordinate system and can be positioned using a local origin, rotation about the vertical axis, and a single scale factor.

```json
{
  "@type": "co:CoordinateOperation",
  "sourceCRS": "csdm-crs:crs/local-building-a",
  "targetCRS": "http://www.opengis.net/def/crs/EPSG/0/7850",
  "operationMethod": "Restricted Helmert / similarity transformation",
  "originInTargetCRS": [392000.0, 6465000.0, 12.4],
  "rotationAboutZDegrees": 34.46031,
  "scale": 1.0
}
```

This is similar to IFC `ifcMapConversion`.

### Level 3: Full 3D Affine Operation

Use where the supporting data requires rotations about X, Y, and Z, axis-specific scale factors, shear terms, or a more rigorous 3D transformation.

```json
{
  "@type": "co:CoordinateOperation",
  "sourceCRS": "csdm-crs:crs/local-building-a",
  "targetCRS": "http://www.opengis.net/def/crs/EPSG/0/4979",
  "operationMethod": "3D affine transformation",
  "implementationMatrix": [
    [0.8241, -0.5664, 0.0000, 115.23],
    [0.5664,  0.8241, 0.0000, 604.87],
    [0.0000,  0.0000, 1.0000,  12.40],
    [0.0000,  0.0000, 0.0000,   1.00]
  ],
  "operationEncoding": {
    "format": "PROJJSON",
    "definition": {}
  }
}
```

The matrix form is often the least ambiguous computational representation, provided the matrix convention, coordinate order, units, transformation direction, and operation metadata are explicitly stated.

## Information Required to Avoid Ambiguity

Where local CRS transformation metadata is used for supporting data, the following information should be provided where relevant:

1. Source CRS: the local or Engineering CRS, including units, axis order, and axis orientation.
2. Target CRS: preferably an EPSG-coded jurisdictional or recognised CRS.
3. Coordinate operation: the operation that transforms coordinates from the source CRS to the target CRS.
4. Operation method: restricted Helmert, full Helmert, affine, translation, rotation, scale, or another operation type.
5. Operation parameters: translation, rotation, scale, matrix coefficients, or other required parameters.
6. Origin point: the local origin expressed in the target CRS, where applicable.
7. Rotation convention: axis order, sign convention, angular units, and whether the system is right-handed or left-handed.
8. Scale convention: single scale factor, per-axis scale factors, or full matrix.
9. Vertical reference: ellipsoidal height, Australian Height Datum, chart datum, building datum, floor datum, or other relevant vertical reference.
10. Transformation direction: source-to-target or target-to-source.
11. Authoritative operation encoding: CRS URI, EPSG reference, WKT2:2019, PROJJSON, or ontology-aligned resource, where available.
12. Accuracy and uncertainty: expected transformation accuracy, source method, procedure, responsible agent, and limitations.
13. Provenance: whether the transformation was derived from BIM Project Base Point metadata, survey control, IFC `IfcMapConversion`, manual georeferencing, least-squares fitting, or another process.

## Summary 

The 3D CSDM should continue to require authoritative survey observations and cadastral geometry to be supplied in the jurisdictionally required CRS.
However, tools that support 3D CSDM workflows should be able to work with referenced BIM, CAD, engineering, and other local-grid datasets.

Where such supporting data is supplied in a local or Engineering CRS, tooling should be able to use local CRS metadata and a documented coordinate operation to transform or display that data in a recognised target CRS.
[EPSG](https://epsg.io/) or OGC CRS identifiers should be used where the CRS is already known.
[WKT2:2019](https://docs.ogc.org/is/18-010r7/18-010r7.html) or [PROJJSON](https://proj.org/en/stable/specifications/projjson.html) should be used where a custom Engineering CRS or coordinate operation must be defined in a CRS tooling environment.
An ontology-aligned CRS and coordinate-operation resource should be used where Linked Data or Semantic Web expression is required.

[PROJ4](https://proj4js.org/) strings may be included for software compatibility, but should not be treated as the authoritative definition.

This pattern allows local-grid supporting data to be visualised and compared with 3D CSDM content without weakening the CRS requirements for authoritative cadastral and survey data.

## The Math

1. [Helmert Transformation](helmert.md)

## References

buildingSMART International Limited. 2024. ‘IFC 4.3.2 Documentation’. https://ifc43-docs.standards.buildingsmart.org/ 

CRS Ontology Working Group Github. 2026. ‘Ontology-CRS’. https://github.com/opengeospatial/ontology-crs.

ISO, 2019. ‘ISO 19111:2019(En), Geographic Information — Referencing by Coordinates’. https://www.iso.org/obp/ui/en/#iso:std:iso:19111:ed-3:v1:en:en). (April 29, 2026).

Lott, Roger, ed. 2019. ‘Geographic Information — Well-Known Text Representation of Coordinate Reference Systems’. https://docs.ogc.org/is/18-010r7/18-010r7.html.

PROJ Contributors. 2026. ‘PROJJSON — PROJ 9.8.1 Documentation’. https://proj.org/en/stable/specifications/projjson.html

Robinson, A.H., J.L. Morrison, P.C. Muehrcke, A.J. Kimerling, and S.C. Guptill. 1995. Elements of Cartography. 6th edn Hoboken, NJ: John Wiley & Sons.

Snyder, J.P. 1987. Map Projections–a Working Manual. USGPO. http://pubs.er.usgs.gov/publication/pp1395.

Wolf, Paul R., Bon DeWitt, and Benjamin Wilkinson. 2014. Elements of Photogrammetry with Application in GIS. 4th edn London, UK: McGraw-Hill.


