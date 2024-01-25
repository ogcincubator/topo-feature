---
title: TopoFeatureCollection (Schema)

language_tabs:
  - json: JSON
  - jsonld: JSON-LD
  - turtle: RDF/Turtle

toc_footers:
  - Version 0.1
  - <a href='#'>TopoFeatureCollection</a>
  - <a href='https://blocks.ogc.org/register.html'>Building Blocks register</a>

search: true

code_clipboard: true

meta:
  - name: TopoFeatureCollection (Schema)
---


# TopoFeatureCollection `ogc.geo.topo.features.topo-feature-collection`

This building block defines a GeoJSON (or FG-JSON) Feature Collection for a set of features with geometries defined by topological relationships. From these it is possible to derive simplified geometries using coordinates for each feature.

<p class="status">
    <span data-rainbow-uri="http://www.opengis.net/def/status">Status</span>:
    <a href="http://www.opengis.net/def/status/under-development" target="_blank" data-rainbow-uri>Under development</a>
</p>

<aside class="success">
This building block is <strong><a href="https://github.com/ogcincubator/topo-feature/blob/master/build/tests/geo/topo/features/topo-feature-collection/" target="_blank">valid</a></strong>
</aside>

# Description

## Feature Collection with Explicit Topology 

%definition% 

A Feature Collection where the set of TopoFeatures contained describe the full geometry of higher-dimension features by topology relationships, ultimately grounded in Point features with explicit coordinates.

TopoFeature is feature type using a topology property to reference an ordered list of references to other features. 

Other features may be either features with topology properties or GeoJSON (or FG-JSON) point objects.

This is a generalisation of the TopoJSON concept using inline data, but not limited to the LineStrings. Topological defined objects 
can be solids, swept volumes or any other concept.


# Examples

## Example referenced points (no topology)



```json
{
  "type": "FeatureCollection",
  "id": "pointsonly",
  "features": [
    {
      "type": "Feature",
      "id": "P1",
      "geometry": {
        "type": "Point",
        "coordinates": [
          10,
          10
        ]
      },
      "properties": null
    },
    {
      "type": "Feature",
      "id": "P2",
      "geometry": {
        "type": "Point",
        "coordinates": [
          20,
          20
        ]
      },
      "properties": null
    }
  ]
}
```

<blockquote class="lang-specific json">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-feature-collection/example_1_1.json">Open in new window</a>
    <a target="_blank" href="https://avillar.github.io/TreedocViewer/?dataParser=json&amp;dataUrl=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-feature-collection%2Fexample_1_1.json&amp;expand=2&amp;option=%7B%22showTable%22%3A+false%7D">View on JSON Viewer</a></p>
</blockquote>




```jsonld
{
  "type": "FeatureCollection",
  "id": "pointsonly",
  "features": [
    {
      "type": "Feature",
      "id": "P1",
      "geometry": {
        "type": "Point",
        "coordinates": [
          10,
          10
        ]
      },
      "properties": null
    },
    {
      "type": "Feature",
      "id": "P2",
      "geometry": {
        "type": "Point",
        "coordinates": [
          20,
          20
        ]
      },
      "properties": null
    }
  ],
  "@context": "https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-collection/context.jsonld"
}
```

<blockquote class="lang-specific jsonld">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-feature-collection/example_1_1.jsonld">Open in new window</a>
    <a target="_blank" href="https://json-ld.org/playground/#json-ld=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-feature-collection%2Fexample_1_1.jsonld">View on JSON-LD Playground</a>
</blockquote>




```turtle
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://www.example.com/features/pointsonly> a geojson:FeatureCollection ;
    geojson:features <http://www.example.com/features/P1>,
        <http://www.example.com/features/P2> .

<http://www.example.com/features/P1> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 10 10 ) ] .

<http://www.example.com/features/P2> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 20 20 ) ] .


```

<blockquote class="lang-specific turtle">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-feature-collection/example_1_1.ttl">Open in new window</a>
</blockquote>



## Example Lines



```json
{
  "type": "FeatureCollection",
  "id": "line",
  "features": [
    {
      "type": "Feature",
      "id": "LineP1P2",
      "geometry": null,
      "topology": {
        "type": "LineString",
        "references": [
          "P1",
          "P2"
        ]
      },
      "properties": null
    },
    {
      "type": "Feature",
      "id": "P1",
      "geometry": {
        "type": "Point",
        "coordinates": [
          10,
          10
        ]
      },
      "properties": null
    },
    {
      "type": "Feature",
      "id": "P2",
      "geometry": {
        "type": "Point",
        "coordinates": [
          20,
          20
        ]
      },
      "properties": null
    }
  ]
}
```

<blockquote class="lang-specific json">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-feature-collection/example_2_1.json">Open in new window</a>
    <a target="_blank" href="https://avillar.github.io/TreedocViewer/?dataParser=json&amp;dataUrl=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-feature-collection%2Fexample_2_1.json&amp;expand=2&amp;option=%7B%22showTable%22%3A+false%7D">View on JSON Viewer</a></p>
</blockquote>




```jsonld
{
  "type": "FeatureCollection",
  "id": "line",
  "features": [
    {
      "type": "Feature",
      "id": "LineP1P2",
      "geometry": null,
      "topology": {
        "type": "LineString",
        "references": [
          "P1",
          "P2"
        ]
      },
      "properties": null
    },
    {
      "type": "Feature",
      "id": "P1",
      "geometry": {
        "type": "Point",
        "coordinates": [
          10,
          10
        ]
      },
      "properties": null
    },
    {
      "type": "Feature",
      "id": "P2",
      "geometry": {
        "type": "Point",
        "coordinates": [
          20,
          20
        ]
      },
      "properties": null
    }
  ],
  "@context": "https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-collection/context.jsonld"
}
```

<blockquote class="lang-specific jsonld">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-feature-collection/example_2_1.jsonld">Open in new window</a>
    <a target="_blank" href="https://json-ld.org/playground/#json-ld=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-feature-collection%2Fexample_2_1.jsonld">View on JSON-LD Playground</a>
</blockquote>




```turtle
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://www.example.com/features/line> a geojson:FeatureCollection ;
    geojson:features <http://www.example.com/features/LineP1P2>,
        <http://www.example.com/features/P1>,
        <http://www.example.com/features/P2> .

<http://www.example.com/features/LineP1P2> a geojson:Feature ;
    geojson:topology [ a geojson:LineString ;
            geojson:relatedFeatures ( <http://www.example.com/features/P1> <http://www.example.com/features/P2> ) ] .

<http://www.example.com/features/P1> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 10 10 ) ] .

<http://www.example.com/features/P2> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 20 20 ) ] .


```

<blockquote class="lang-specific turtle">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-feature-collection/example_2_1.ttl">Open in new window</a>
</blockquote>



## Points Lines and Polygons



```json
{
  "type": "FeatureCollection",
  "id": "TopoCollectionExample",
  "features": [
    {
      "type": "Feature",
      "id": "P1",
      "geometry": {
        "type": "Point",
        "coordinates": [
          10,
          10
        ]
      },
      "properties": null
    },
    {
      "type": "Feature",
      "id": "P2",
      "geometry": {
        "type": "Point",
        "coordinates": [
          20,
          20
        ]
      },
      "properties": null
    },
    {
      "type": "Feature",
      "id": "P3",
      "geometry": {
        "type": "Point",
        "coordinates": [
          10,
          20
        ]
      },
      "properties": null
    },
    {
      "type": "Feature",
      "id": "LineP1P2",
      "geometry": null,
      "topology": {
        "type": "LineString",
        "references": [
          "P1",
          "P2"
        ]
      },
      "properties": null
    },
    {
      "type": "Feature",
      "id": "LineP2P3",
      "geometry": null,
      "topology": {
        "type": "LineString",
        "references": [
          "P2",
          "P3"
        ]
      },
      "properties": null
    },
    {
      "type": "Feature",
      "id": "LineP3P1",
      "geometry": null,
      "topology": {
        "type": "LineString",
        "references": [
          "P3",
          "P1"
        ]
      },
      "properties": null
    },
    {
      "type": "Feature",
      "id": "TriangleP1P2P3",
      "geometry": null,
      "topology": {
        "type": "Polygon",
        "references": [
          "LineP1P2",
          "LineP2P3",
          "LineP3P1"
        ]
      },
      "properties": null
    }
  ]
}
```

<blockquote class="lang-specific json">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-feature-collection/example_3_1.json">Open in new window</a>
    <a target="_blank" href="https://avillar.github.io/TreedocViewer/?dataParser=json&amp;dataUrl=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-feature-collection%2Fexample_3_1.json&amp;expand=2&amp;option=%7B%22showTable%22%3A+false%7D">View on JSON Viewer</a></p>
</blockquote>




```jsonld
{
  "type": "FeatureCollection",
  "id": "TopoCollectionExample",
  "features": [
    {
      "type": "Feature",
      "id": "P1",
      "geometry": {
        "type": "Point",
        "coordinates": [
          10,
          10
        ]
      },
      "properties": null
    },
    {
      "type": "Feature",
      "id": "P2",
      "geometry": {
        "type": "Point",
        "coordinates": [
          20,
          20
        ]
      },
      "properties": null
    },
    {
      "type": "Feature",
      "id": "P3",
      "geometry": {
        "type": "Point",
        "coordinates": [
          10,
          20
        ]
      },
      "properties": null
    },
    {
      "type": "Feature",
      "id": "LineP1P2",
      "geometry": null,
      "topology": {
        "type": "LineString",
        "references": [
          "P1",
          "P2"
        ]
      },
      "properties": null
    },
    {
      "type": "Feature",
      "id": "LineP2P3",
      "geometry": null,
      "topology": {
        "type": "LineString",
        "references": [
          "P2",
          "P3"
        ]
      },
      "properties": null
    },
    {
      "type": "Feature",
      "id": "LineP3P1",
      "geometry": null,
      "topology": {
        "type": "LineString",
        "references": [
          "P3",
          "P1"
        ]
      },
      "properties": null
    },
    {
      "type": "Feature",
      "id": "TriangleP1P2P3",
      "geometry": null,
      "topology": {
        "type": "Polygon",
        "references": [
          "LineP1P2",
          "LineP2P3",
          "LineP3P1"
        ]
      },
      "properties": null
    }
  ],
  "@context": "https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-collection/context.jsonld"
}
```

<blockquote class="lang-specific jsonld">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-feature-collection/example_3_1.jsonld">Open in new window</a>
    <a target="_blank" href="https://json-ld.org/playground/#json-ld=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-feature-collection%2Fexample_3_1.jsonld">View on JSON-LD Playground</a>
</blockquote>




```turtle
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://www.example.com/features/TopoCollectionExample> a geojson:FeatureCollection ;
    geojson:features <http://www.example.com/features/LineP1P2>,
        <http://www.example.com/features/LineP2P3>,
        <http://www.example.com/features/LineP3P1>,
        <http://www.example.com/features/P1>,
        <http://www.example.com/features/P2>,
        <http://www.example.com/features/P3>,
        <http://www.example.com/features/TriangleP1P2P3> .

<http://www.example.com/features/TriangleP1P2P3> a geojson:Feature ;
    geojson:topology [ a geojson:Polygon ;
            geojson:relatedFeatures ( <http://www.example.com/features/LineP1P2> <http://www.example.com/features/LineP2P3> <http://www.example.com/features/LineP3P1> ) ] .

<http://www.example.com/features/LineP1P2> a geojson:Feature ;
    geojson:topology [ a geojson:LineString ;
            geojson:relatedFeatures ( <http://www.example.com/features/P1> <http://www.example.com/features/P2> ) ] .

<http://www.example.com/features/LineP2P3> a geojson:Feature ;
    geojson:topology [ a geojson:LineString ;
            geojson:relatedFeatures ( <http://www.example.com/features/P2> <http://www.example.com/features/P3> ) ] .

<http://www.example.com/features/LineP3P1> a geojson:Feature ;
    geojson:topology [ a geojson:LineString ;
            geojson:relatedFeatures ( <http://www.example.com/features/P3> <http://www.example.com/features/P1> ) ] .

<http://www.example.com/features/P1> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 10 10 ) ] .

<http://www.example.com/features/P2> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 20 20 ) ] .

<http://www.example.com/features/P3> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 10 20 ) ] .


```

<blockquote class="lang-specific turtle">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-feature-collection/example_3_1.ttl">Open in new window</a>
</blockquote>



# JSON Schema

```yaml--schema
$schema: https://json-schema.org/draft/2020-12/schema
description: Feature Collection with defined topology for bounding elements
$defs:
  FeatureCollectionOptions:
    anyOf:
    - $ref: https://beta.schemas.opengis.net/json-fg/featurecollection.json
    - $ref: https://opengeospatial.github.io/bblocks/annotated-schemas/geo/json-fg/featureCollection-lenient/schema.json
    - $ref: https://geojson.org/schema/FeatureCollection.json
  FeatureOptions:
    anyOf:
    - $ref: https://beta.schemas.opengis.net/json-fg/feature.json
    - $ref: https://geojson.org/schema/Feature.json
  PointOptions:
    anyOf:
    - allOf:
      - $ref: '#/$defs/FeatureOptions'
      - properties:
          geometry:
            properties:
              type:
                type: string
                enum:
                - Point
allOf:
- $ref: '#/$defs/FeatureCollectionOptions'
properties:
  features:
    type: array
    items:
      anyOf:
      - $ref: ../topo-feature/schema.yaml
      - $ref: '#/$defs/PointOptions'

```

> <a target="_blank" href="https://avillar.github.io/TreedocViewer/?dataParser=yaml&amp;dataUrl=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Fannotated%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-feature-collection%2Fschema.yaml&amp;expand=2&amp;option=%7B%22showTable%22%3A+false%7D">View on YAML Viewer</a>

Links to the schema:

* YAML version: <a href="https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-collection/schema.yaml" target="_blank">https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-collection/schema.yaml</a>
* JSON version: <a href="https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-collection/schema.json" target="_blank">https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-collection/schema.json</a>


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
      "@id": "geojson:features",
      "@context": {
        "featureType": "@type"
      }
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
    "featureType": "geojson:collectionFeatureType",
    "coordinates": {
      "@container": "@list",
      "@id": "geojson:coordinates"
    },
    "topology": {
      "@context": {
        "references": {
          "@id": "geojson:relatedFeatures",
          "@type": "@id",
          "@container": "@list"
        }
      },
      "@type": "@id",
      "@id": "geojson:topology"
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

> <a target="_blank" href="https://json-ld.org/playground/#json-ld=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Fannotated%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-feature-collection%2Fcontext.jsonld">View on JSON-LD Playground</a>

You can find the full JSON-LD context here:
<a href="https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-collection/context.jsonld" target="_blank">https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-collection/context.jsonld</a>

# Validation

## SHACL Shapes

The following sets of SHACL shapes are used for validating this building block:

* TopoFeatureCollection <small><code>ogc.geo.topo.features.topo-feature-collection</code></small>
  * [https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature-collection/tests/topo-refs-exist.shacl](https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature-collection/tests/topo-refs-exist.shacl)
  * [https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature/tests/geometry-coordinates.shacl](https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature/tests/geometry-coordinates.shacl)
* Feature with topology <small><code>ogc.geo.topo.features.topo-feature</code></small>
  * [https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature-collection/tests/topo-refs-exist.shacl](https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature-collection/tests/topo-refs-exist.shacl)
  * [https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature/tests/geometry-coordinates.shacl](https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature/tests/geometry-coordinates.shacl)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: <a href="https://github.com/ogcincubator/topo-feature" target="_blank">https://github.com/ogcincubator/topo-feature</a>
* Path:
<code><a href="https://github.com/ogcincubator/topo-feature/blob/HEAD/_sources/features/topo-feature-collection" target="_blank">_sources/features/topo-feature-collection</a></code>

