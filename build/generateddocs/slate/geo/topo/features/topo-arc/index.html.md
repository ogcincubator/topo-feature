---
title: Non-linear Arc and Spline Descriptions using Point topology (Schema)

language_tabs:
  - json: JSON
  - jsonld: JSON-LD
  - turtle: RDF/Turtle

toc_footers:
  - Version 0.1
  - <a href='#'>Non-linear Arc and Spline Descriptions using Point topology</a>
  - <a href='https://blocks.ogc.org/register.html'>Building Blocks register</a>

search: true

code_clipboard: true

meta:
  - name: Non-linear Arc and Spline Descriptions using Point topology (Schema)
---


# Non-linear Arc and Spline Descriptions using Point topology `ogc.geo.topo.features.topo-arc`

Defines options for describing Arcs, Circles, Splines using point features as canonical source of geometry coordinates

<p class="status">
    <span data-rainbow-uri="http://www.opengis.net/def/status">Status</span>:
    <a href="http://www.opengis.net/def/status/under-development" target="_blank" data-rainbow-uri>Under development</a>
</p>

<aside class="success">
This building block is <strong><a href="https://github.com/ogcincubator/topo-feature/blob/master/build/tests/geo/topo/features/topo-arc/" target="_blank">valid</a></strong>
</aside>

# Description

## Topology defining Arcs, Circles, Splines

A feature type using a topology property to reference points defining non-linear curves.

Each geometry type has a specific number of references to "features" defining point geometries.

![Example](https://ogcincubator.github.io/topo-feature/_sources/features/topo-arc/assets/arc.png)

Where additional properties are required to define the geometry these are included as sub-properties of the topology property.

Additional properties "radius" and "arcLength" are defined for optional use as feature properties.

Note: the geojson: namespace is used for semantic annotations - this may be replaced with a more suitable namespace when a target ontology is available (such as the planned Geosparql version 1.3)



# Examples

## Example GeoJSON feature using ArcWithCenter topology



```json
{
  "id": "1853004",
  "type": "Feature",
  "featureType": "my:ArcFeature",
  "geometry": null,
  "topology": {
    "type": "ArcWithCenter",
    "x-description": "References is an ordered list of features with point geometries Start,End,Center",
    "references": [
      "P1",
      "P2",
      "PC"
    ],
    "orientation": "ccw"
  },
  "properties": {
    "arcLength": 25.615,
    "radius": 105.438
  }
}
```

<blockquote class="lang-specific json">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-arc/example_1_1.json">Open in new window</a>
    <a target="_blank" href="https://avillar.github.io/TreedocViewer/?dataParser=json&amp;dataUrl=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-arc%2Fexample_1_1.json&amp;expand=2&amp;option=%7B%22showTable%22%3A+false%7D">View on JSON Viewer</a></p>
</blockquote>




```jsonld
{
  "id": "1853004",
  "type": "Feature",
  "featureType": "my:ArcFeature",
  "geometry": null,
  "topology": {
    "type": "ArcWithCenter",
    "x-description": "References is an ordered list of features with point geometries Start,End,Center",
    "references": [
      "P1",
      "P2",
      "PC"
    ],
    "orientation": "ccw"
  },
  "properties": {
    "arcLength": 25.615,
    "radius": 105.438
  },
  "@context": "https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-arc/context.jsonld"
}
```

<blockquote class="lang-specific jsonld">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-arc/example_1_1.jsonld">Open in new window</a>
    <a target="_blank" href="https://json-ld.org/playground/#json-ld=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-arc%2Fexample_1_1.jsonld">View on JSON-LD Playground</a>
</blockquote>




```turtle
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://www.example.com/features/1853004> a geojson:Feature,
        <my:ArcFeature> ;
    geojson:arcLength 2.5615e+01 ;
    geojson:radius 1.05438e+02 ;
    geojson:topology [ a geojson:ArcWithCenter ;
            geojson:relatedFeatures ( <http://www.example.com/features/P1> <http://www.example.com/features/P2> <http://www.example.com/features/PC> ) ] .


```

<blockquote class="lang-specific turtle">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-arc/example_1_1.ttl">Open in new window</a>
</blockquote>


Arc with Center example.

Topology defined by 2 end points and a centre that are references to features with point geometry.

![Example](assets/arc-by-center.png)

radius and arcLength are implicit but may be provided as optional properties of the feature.


## Example GeoJSON feature using Arc topology



```json
{
  "id": "arc1",
  "type": "Feature",
  "featureType": "my:ArcFeature",
  "geometry": null,
  "topology": {
    "type": "Arc",
    "x-description": "References is an ordered list of 3 features with point geometries defining Arc",
    "references": [
      "P1",
      "P3",
      "P2"
    ]
  },
  "properties": {
    "arcLength": 25.615,
    "radius": 105.438
  }
}
```

<blockquote class="lang-specific json">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-arc/example_2_1.json">Open in new window</a>
    <a target="_blank" href="https://avillar.github.io/TreedocViewer/?dataParser=json&amp;dataUrl=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-arc%2Fexample_2_1.json&amp;expand=2&amp;option=%7B%22showTable%22%3A+false%7D">View on JSON Viewer</a></p>
</blockquote>




```jsonld
{
  "id": "arc1",
  "type": "Feature",
  "featureType": "my:ArcFeature",
  "geometry": null,
  "topology": {
    "type": "Arc",
    "x-description": "References is an ordered list of 3 features with point geometries defining Arc",
    "references": [
      "P1",
      "P3",
      "P2"
    ]
  },
  "properties": {
    "arcLength": 25.615,
    "radius": 105.438
  },
  "@context": "https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-arc/context.jsonld"
}
```

<blockquote class="lang-specific jsonld">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-arc/example_2_1.jsonld">Open in new window</a>
    <a target="_blank" href="https://json-ld.org/playground/#json-ld=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-arc%2Fexample_2_1.jsonld">View on JSON-LD Playground</a>
</blockquote>




```turtle
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://www.example.com/features/arc1> a geojson:Feature,
        <my:ArcFeature> ;
    geojson:arcLength 2.5615e+01 ;
    geojson:radius 1.05438e+02 ;
    geojson:topology [ a geojson:Arc ;
            geojson:relatedFeatures ( <http://www.example.com/features/P1> <http://www.example.com/features/P3> <http://www.example.com/features/P2> ) ] .


```

<blockquote class="lang-specific turtle">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-arc/example_2_1.ttl">Open in new window</a>
</blockquote>


Arc example (3 points).

Note that properties "radius" and "arcLength" are not required in the containing feature but defined for convenience.

![Example](assets/arc.png)


## Example GeoJSON feature using ArcByChord topology



```json
{
  "id": "chord1",
  "type": "Feature",
  "featureType": "my:ArcChordFeature",
  "geometry": null,
  "topology": {
    "type": "ArcByChord",
    "x-description": "References is an ordered list of features with for an Arc Chord, radius and length determine geometry",
    "references": [
      "P1",
      "P2"
    ],
    "radius": 105.438,
    "orientation": "cw"
  },
  "properties": {
    "arcLength": 25.615
  }
}
```

<blockquote class="lang-specific json">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-arc/example_3_1.json">Open in new window</a>
    <a target="_blank" href="https://avillar.github.io/TreedocViewer/?dataParser=json&amp;dataUrl=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-arc%2Fexample_3_1.json&amp;expand=2&amp;option=%7B%22showTable%22%3A+false%7D">View on JSON Viewer</a></p>
</blockquote>




```jsonld
{
  "id": "chord1",
  "type": "Feature",
  "featureType": "my:ArcChordFeature",
  "geometry": null,
  "topology": {
    "type": "ArcByChord",
    "x-description": "References is an ordered list of features with for an Arc Chord, radius and length determine geometry",
    "references": [
      "P1",
      "P2"
    ],
    "radius": 105.438,
    "orientation": "cw"
  },
  "properties": {
    "arcLength": 25.615
  },
  "@context": "https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-arc/context.jsonld"
}
```

<blockquote class="lang-specific jsonld">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-arc/example_3_1.jsonld">Open in new window</a>
    <a target="_blank" href="https://json-ld.org/playground/#json-ld=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-arc%2Fexample_3_1.jsonld">View on JSON-LD Playground</a>
</blockquote>




```turtle
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://www.example.com/features/chord1> a geojson:Feature,
        <my:ArcChordFeature> ;
    geojson:arcLength 2.5615e+01 ;
    geojson:topology [ a geojson:ArcByChord ;
            geojson:radius 1.05438e+02 ;
            geojson:relatedFeatures ( <http://www.example.com/features/P1> <http://www.example.com/features/P2> ) ] .


```

<blockquote class="lang-specific turtle">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-arc/example_3_1.ttl">Open in new window</a>
</blockquote>


Arc by Chord example.

![Example](assets/arc-by-chord.png)


## Example GeoJSON feature using  CircleWithCenter topology

Circle with Center example.

![Example](assets/circle-with-center.png)


## Example 5



```json
{
  "id": "1853004",
  "type": "Feature",
  "featureType": "my:CircleFeature",
  "geometry": null,
  "topology": {
    "type": "CircleByCenter",
    "x-description": "Reference is the feature defining the centre point of a circle - it must have a Point geometry.",
    "references": [
      "PC"
    ],
    "radius": 10
  },
  "properties": null
}
```

<blockquote class="lang-specific json">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-arc/example_5_1.json">Open in new window</a>
    <a target="_blank" href="https://avillar.github.io/TreedocViewer/?dataParser=json&amp;dataUrl=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-arc%2Fexample_5_1.json&amp;expand=2&amp;option=%7B%22showTable%22%3A+false%7D">View on JSON Viewer</a></p>
</blockquote>




```jsonld
{
  "id": "1853004",
  "type": "Feature",
  "featureType": "my:CircleFeature",
  "geometry": null,
  "topology": {
    "type": "CircleByCenter",
    "x-description": "Reference is the feature defining the centre point of a circle - it must have a Point geometry.",
    "references": [
      "PC"
    ],
    "radius": 10
  },
  "properties": null,
  "@context": "https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-arc/context.jsonld"
}
```

<blockquote class="lang-specific jsonld">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-arc/example_5_1.jsonld">Open in new window</a>
    <a target="_blank" href="https://json-ld.org/playground/#json-ld=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-arc%2Fexample_5_1.jsonld">View on JSON-LD Playground</a>
</blockquote>




```turtle
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://www.example.com/features/1853004> a geojson:Feature,
        <my:CircleFeature> ;
    geojson:topology [ a geojson:CircleByCenter ;
            geojson:radius 10 ;
            geojson:relatedFeatures ( <http://www.example.com/features/PC> ) ] .


```

<blockquote class="lang-specific turtle">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-arc/example_5_1.ttl">Open in new window</a>
</blockquote>



## Example GeoJSON feature using Cubic Spline topology

Cubic Spline example.

![Example](assets/spline.png)


## Example 7



```json
{
  "id": "1853004",
  "type": "Feature",
  "featureType": "my:SplineFeature",
  "geometry": null,
  "topology": {
    "type": "CubicSpline",
    "x-description": "References is an ordered list of features with point geometries",
    "references": [
      "P1",
      "Px1",
      "Px2",
      "P2"
    ]
  },
  "properties": null
}
```

<blockquote class="lang-specific json">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-arc/example_7_1.json">Open in new window</a>
    <a target="_blank" href="https://avillar.github.io/TreedocViewer/?dataParser=json&amp;dataUrl=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-arc%2Fexample_7_1.json&amp;expand=2&amp;option=%7B%22showTable%22%3A+false%7D">View on JSON Viewer</a></p>
</blockquote>




```jsonld
{
  "id": "1853004",
  "type": "Feature",
  "featureType": "my:SplineFeature",
  "geometry": null,
  "topology": {
    "type": "CubicSpline",
    "x-description": "References is an ordered list of features with point geometries",
    "references": [
      "P1",
      "Px1",
      "Px2",
      "P2"
    ]
  },
  "properties": null,
  "@context": "https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-arc/context.jsonld"
}
```

<blockquote class="lang-specific jsonld">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-arc/example_7_1.jsonld">Open in new window</a>
    <a target="_blank" href="https://json-ld.org/playground/#json-ld=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-arc%2Fexample_7_1.jsonld">View on JSON-LD Playground</a>
</blockquote>




```turtle
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

<http://www.example.com/features/1853004> a geojson:Feature,
        <my:SplineFeature> ;
    geojson:topology [ a geojson:CubicSpline ;
            geojson:relatedFeatures ( <http://www.example.com/features/P1> <http://www.example.com/features/Px1> <http://www.example.com/features/Px2> <http://www.example.com/features/P2> ) ] .


```

<blockquote class="lang-specific turtle">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-arc/example_7_1.ttl">Open in new window</a>
</blockquote>



## Example GeoJSON feature using Cubic Spline topology with start and end tangents



```json
{
  "id": "1853004",
  "type": "Feature",
  "featureType": "my:SplineFeature",
  "geometry": null,
  "topology": {
    "type": "CubicSpline",
    "x-description": "References is an ordered list of features with point geometries, with tangent vectors defining entry and exit angles",
    "startTangentVector": {
      "references": [
        "PVS",
        "P1"
      ]
    },
    "endTangentVector": {
      "references": [
        "P2",
        "PVE"
      ]
    },
    "references": [
      "P1",
      "P2"
    ]
  },
  "properties": null
}
```

<blockquote class="lang-specific json">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-arc/example_8_1.json">Open in new window</a>
    <a target="_blank" href="https://avillar.github.io/TreedocViewer/?dataParser=json&amp;dataUrl=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-arc%2Fexample_8_1.json&amp;expand=2&amp;option=%7B%22showTable%22%3A+false%7D">View on JSON Viewer</a></p>
</blockquote>




```jsonld
{
  "id": "1853004",
  "type": "Feature",
  "featureType": "my:SplineFeature",
  "geometry": null,
  "topology": {
    "type": "CubicSpline",
    "x-description": "References is an ordered list of features with point geometries, with tangent vectors defining entry and exit angles",
    "startTangentVector": {
      "references": [
        "PVS",
        "P1"
      ]
    },
    "endTangentVector": {
      "references": [
        "P2",
        "PVE"
      ]
    },
    "references": [
      "P1",
      "P2"
    ]
  },
  "properties": null,
  "@context": "https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-arc/context.jsonld"
}
```

<blockquote class="lang-specific jsonld">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-arc/example_8_1.jsonld">Open in new window</a>
    <a target="_blank" href="https://json-ld.org/playground/#json-ld=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-arc%2Fexample_8_1.jsonld">View on JSON-LD Playground</a>
</blockquote>




```turtle
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

<http://www.example.com/features/1853004> a geojson:Feature,
        <my:SplineFeature> ;
    geojson:topology [ a geojson:CubicSpline ;
            geojson:endTangentVector [ geojson:relatedFeatures ( <http://www.example.com/features/P2> <http://www.example.com/features/PVE> ) ] ;
            geojson:relatedFeatures ( <http://www.example.com/features/P1> <http://www.example.com/features/P2> ) ;
            geojson:startTangentVector [ geojson:relatedFeatures ( <http://www.example.com/features/PVS> <http://www.example.com/features/P1> ) ] ] .


```

<blockquote class="lang-specific turtle">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-arc/example_8_1.ttl">Open in new window</a>
</blockquote>


Cubic Spline with Tangents example.


# JSON Schema

```yaml--schema
$schema: https://json-schema.org/draft/2020-12/schema
description: Arc Feature with geometry by reference
allOf:
- $ref: ../topo-feature/schema.json
- properties:
    topology:
      allOf:
      - $ref: ../../datatypes/topology/schema.json
      - oneOf:
        - properties:
            type:
              type: string
              const: Arc
            references:
              minItems: 3
              maxItems: 3
        - properties:
            type:
              type: string
              const: ArcWithCenter
            references:
              minItems: 3
              maxItems: 3
            orientation:
              type: string
              enum:
              - cw
              - ccw
          required:
          - orientation
        - properties:
            type:
              type: string
              const: ArcByChord
            references:
              minItems: 2
              maxItems: 2
            radius:
              type: number
            orientation:
              type: string
              enum:
              - cw
              - ccw
          required:
          - radius
          - orientation
        - properties:
            type:
              type: string
              const: CircleByCenter
            references:
              minItems: 1
              maxItems: 1
            radius:
              type: number
          required:
          - radius
        - properties:
            type:
              type: string
              const: CubicSpline
            references:
              minItems: 3
          not:
            required:
            - startTangentVector
            - endTangentVector
        - properties:
            type:
              type: string
              const: CubicSpline
            references:
              minItems: 2
            startTangentVector:
              properties:
                references:
                  minItems: 2
            endTangentVector:
              properties:
                references:
                  minItems: 2
          required:
          - startTangentVector
          - endTangentVector
    radius:
      type: number
      description: optional property of the feature defining radius according to coordinate
        reference system of the referenced geometry. Note where necessary to define
        geometry this is a mandatory sub-property of the topology property.
    arcLength:
      type: number
      description: optional property of the feature defining arcLength according to
        coordinate reference system of the referenced geometry.
  required:
  - topology

```

> <a target="_blank" href="https://avillar.github.io/TreedocViewer/?dataParser=yaml&amp;dataUrl=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Fannotated%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-arc%2Fschema.yaml&amp;expand=2&amp;option=%7B%22showTable%22%3A+false%7D">View on YAML Viewer</a>

Links to the schema:

* YAML version: <a href="https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-arc/schema.yaml" target="_blank">https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-arc/schema.yaml</a>
* JSON version: <a href="https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-arc/schema.json" target="_blank">https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-arc/schema.json</a>


# JSON-LD Context

```json--ldContext
{
  "@context": {
    "type": "@type",
    "id": "@id",
    "properties": "@nest",
    "geometry": {
      "@context": {},
      "@id": "geojson:geometry"
    },
    "bbox": {
      "@container": "@list",
      "@id": "geojson:bbox"
    },
    "Feature": "geojson:Feature",
    "FeatureCollection": "geojson:FeatureCollection",
    "GeometryCollection": "geojson:GeometryCollection",
    "LineString": "geojson:LineString",
    "MultiLineString": "geojson:MultiLineString",
    "MultiPoint": "geojson:MultiPoint",
    "MultiPolygon": "geojson:MultiPolygon",
    "Point": "geojson:Point",
    "Polygon": "geojson:Polygon",
    "features": {
      "@container": "@set",
      "@id": "geojson:features"
    },
    "links": {
      "@context": {
        "href": {
          "@type": "@id",
          "@id": "oa:hasTarget"
        },
        "rel": {
          "@context": {
            "@base": "http://www.iana.org/assignments/relation/"
          },
          "@id": "http://www.iana.org/assignments/relation",
          "@type": "@id"
        },
        "type": "dct:type",
        "hreflang": "dct:language",
        "title": "rdfs:label",
        "length": "dct:extent"
      },
      "@id": "rdfs:seeAlso"
    },
    "featureType": "@type",
    "coordinates": {
      "@container": "@list",
      "@id": "geojson:coordinates"
    },
    "topology": {
      "@context": {},
      "@type": "@id",
      "@id": "geojson:topology"
    },
    "references": {
      "@id": "geojson:relatedFeatures",
      "@type": "@id",
      "@container": "@list"
    },
    "Arc": "geojson:Arc",
    "ArcWithCenter": "geojson:ArcWithCenter",
    "ArcByChord": "geojson:ArcByChord",
    "CircleByCenter": "geojson:CircleByCenter",
    "CubicSpline": "geojson:CubicSpline",
    "radius": "geojson:radius",
    "arcLength": "geojson:arcLength",
    "startTangentVector": "geojson:startTangentVector",
    "endTangentVector": "geojson:endTangentVector",
    "geojson": "https://purl.org/geojson/vocab#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "oa": "http://www.w3.org/ns/oa#",
    "dct": "http://purl.org/dc/terms/",
    "csdm": "https://linked.data.gov.au/def/csdm/",
    "@version": 1.1
  }
}
```

> <a target="_blank" href="https://json-ld.org/playground/#json-ld=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Fannotated%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-arc%2Fcontext.jsonld">View on JSON-LD Playground</a>

You can find the full JSON-LD context here:
<a href="https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-arc/context.jsonld" target="_blank">https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-arc/context.jsonld</a>

# Validation

## SHACL Shapes

The following sets of SHACL shapes are used for validating this building block:

* Non-linear Arc and Spline Descriptions using Point topology <small><code>ogc.geo.topo.features.topo-arc</code></small>
  * [https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature-collection/tests/topo-refs-exist.shacl](https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature-collection/tests/topo-refs-exist.shacl)
  * [https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature/tests/geometry-coordinates.shacl](https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature/tests/geometry-coordinates.shacl)
* Feature with topology <small><code>ogc.geo.topo.features.topo-feature</code></small>
  * [https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature-collection/tests/topo-refs-exist.shacl](https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature-collection/tests/topo-refs-exist.shacl)
  * [https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature/tests/geometry-coordinates.shacl](https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature/tests/geometry-coordinates.shacl)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: <a href="https://github.com/ogcincubator/topo-feature" target="_blank">https://github.com/ogcincubator/topo-feature</a>
* Path:
<code><a href="https://github.com/ogcincubator/topo-feature/blob/HEAD/_sources/features/topo-arc" target="_blank">_sources/features/topo-arc</a></code>

