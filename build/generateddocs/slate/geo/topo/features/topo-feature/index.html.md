---
title: Feature with topology (Schema)

language_tabs:
  - json: JSON
  - jsonld: JSON-LD
  - turtle: RDF/Turtle

toc_footers:
  - Version 0.1
  - <a href='#'>Feature with topology</a>
  - <a href='https://blocks.ogc.org/register.html'>Building Blocks register</a>

search: true

code_clipboard: true

meta:
  - name: Feature with topology (Schema)
---


# Feature with topology `ogc.geo.topo.features.topo-feature`

This building block defines a GeoJSON feature with topological relationships to point nodes, or other to TopoFeatures

<p class="status">
    <span data-rainbow-uri="http://www.opengis.net/def/status">Status</span>:
    <a href="http://www.opengis.net/def/status/under-development" target="_blank" data-rainbow-uri>Under development</a>
</p>

<aside class="success">
This building block is <strong><a href="https://github.com/ogcincubator/topo-feature/blob/master/build/tests/geo/topo/features/topo-feature/" target="_blank">valid</a></strong>
</aside>

# Description

## Feature with explicit Topology

A feature type using a topology property to reference an ordered list of references to other features. 

Other features may be either features with topology properties or GeoJSON (or FG-JSON) point objects.

This is a generalisation of the TopoJSON concept using inline data, (nested sets of coordinates) but not limited to the LineStrings. Topological defined objects 
can be solids, swept volumes or any other concept. (It doesnt use TopoJSON coordinate compaction and transformation, however it does allow for explicit CRS, and coordinate compaction transformations could be defined as derived CRS if required.)


# Examples

## Example of a LineString



```json
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
}
```

<blockquote class="lang-specific json">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-feature/example_1_1.json">Open in new window</a>
    <a target="_blank" href="https://avillar.github.io/TreedocViewer/?dataParser=json&amp;dataUrl=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-feature%2Fexample_1_1.json&amp;expand=2&amp;option=%7B%22showTable%22%3A+false%7D">View on JSON Viewer</a></p>
</blockquote>




```jsonld
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
  "properties": null,
  "@context": "https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature/context.jsonld"
}
```

<blockquote class="lang-specific jsonld">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-feature/example_1_1.jsonld">Open in new window</a>
    <a target="_blank" href="https://json-ld.org/playground/#json-ld=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-feature%2Fexample_1_1.jsonld">View on JSON-LD Playground</a>
</blockquote>




```turtle
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

<http://www.example.com/features/LineP1P2> a geojson:Feature ;
    geojson:topology [ a geojson:LineString ;
            geojson:relatedFeatures ( <http://www.example.com/features/P1> <http://www.example.com/features/P2> ) ] .


```

<blockquote class="lang-specific turtle">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-feature/example_1_1.ttl">Open in new window</a>
</blockquote>



## Example of a Polygon



```json
{
  "type": "Feature",
  "id": "TriangleP1P2P3",
  "geometry": null,
  "topology": {
    "type": "Polygon",
    "references": [
      [
        "LineP1P2",
        "LineP2P3",
        "LineP3P1"
      ]
    ]
  },
  "properties": null
}
```

<blockquote class="lang-specific json">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-feature/example_2_1.json">Open in new window</a>
    <a target="_blank" href="https://avillar.github.io/TreedocViewer/?dataParser=json&amp;dataUrl=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-feature%2Fexample_2_1.json&amp;expand=2&amp;option=%7B%22showTable%22%3A+false%7D">View on JSON Viewer</a></p>
</blockquote>




```jsonld
{
  "type": "Feature",
  "id": "TriangleP1P2P3",
  "geometry": null,
  "topology": {
    "type": "Polygon",
    "references": [
      [
        "LineP1P2",
        "LineP2P3",
        "LineP3P1"
      ]
    ]
  },
  "properties": null,
  "@context": "https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature/context.jsonld"
}
```

<blockquote class="lang-specific jsonld">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-feature/example_2_1.jsonld">Open in new window</a>
    <a target="_blank" href="https://json-ld.org/playground/#json-ld=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Ftests%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-feature%2Fexample_2_1.jsonld">View on JSON-LD Playground</a>
</blockquote>




```turtle
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

<http://www.example.com/features/TriangleP1P2P3> a geojson:Feature ;
    geojson:topology [ a geojson:Polygon ;
            geojson:relatedFeatures ( ( <http://www.example.com/features/LineP1P2> <http://www.example.com/features/LineP2P3> <http://www.example.com/features/LineP3P1> ) ) ] .


```

<blockquote class="lang-specific turtle">
  <p class="example-links">
    <a target="_blank" href="https://ogcincubator.github.io/topo-feature/build/tests/geo/topo/features/topo-feature/example_2_1.ttl">Open in new window</a>
</blockquote>



# JSON Schema

```yaml--schema
$schema: https://json-schema.org/draft/2020-12/schema
description: Feature with defined topology for bounding elements
$defs:
  FeatureOptions:
    anyOf:
    - $ref: https://opengeospatial.github.io/bblocks/annotated-schemas/geo/json-fg/feature/schema.yaml
    - $ref: https://opengeospatial.github.io/bblocks/annotated-schemas/geo/common/data_types/geojson/schema.yaml
allOf:
- $ref: '#/$defs/FeatureOptions'
- type: object
  properties:
    id:
      type: string
    topology:
      $ref: https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/datatypes/topology/schema.yaml
      x-jsonld-type: '@id'
      x-jsonld-id: https://purl.org/geojson/vocab#topology
  required:
  - topology
x-jsonld-prefixes:
  geojson: https://purl.org/geojson/vocab#

```

> <a target="_blank" href="https://avillar.github.io/TreedocViewer/?dataParser=yaml&amp;dataUrl=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Fannotated%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-feature%2Fschema.yaml&amp;expand=2&amp;option=%7B%22showTable%22%3A+false%7D">View on YAML Viewer</a>

Links to the schema:

* YAML version: <a href="https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature/schema.yaml" target="_blank">https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature/schema.yaml</a>
* JSON version: <a href="https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature/schema.json" target="_blank">https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature/schema.json</a>


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
    "time": {
      "@context": {
        "date": {
          "@id": "owlTime:hasTime",
          "@type": "xsd:date"
        },
        "timestamp": {
          "@id": "owlTime:hasTime",
          "@type": "xsd:dateTime"
        },
        "interval": {
          "@id": "owlTime:hasTime",
          "@container": "@list"
        }
      },
      "@id": "dct:time"
    },
    "coordRefSys": "http://www.opengis.net/def/glossary/term/CoordinateReferenceSystemCRS",
    "place": "dct:spatial",
    "Polyhedron": "geojson:Polyhedron",
    "MultiPolyhedron": "geojson:MultiPolyhedron",
    "Prism": {
      "@id": "geojson:Prism",
      "@context": {
        "base": "geojson:prismBase",
        "lower": "geojson:prismLower",
        "upper": "geojson:prismUpper"
      }
    },
    "MultiPrism": {
      "@id": "geojson:MultiPrism",
      "@context": {
        "prisms": "geojson:prisms"
      }
    },
    "coordinates": {
      "@container": "@list",
      "@id": "geojson:coordinates"
    },
    "geometries": {
      "@id": "geojson:geometry",
      "@container": "@list"
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
    "owlTime": "http://www.w3.org/2006/time#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "csdm": "https://linked.data.gov.au/def/csdm/",
    "@version": 1.1
  }
}
```

> <a target="_blank" href="https://json-ld.org/playground/#json-ld=https%3A%2F%2Fogcincubator.github.io%2Ftopo-feature%2Fbuild%2Fannotated%2Fgeo%2Ftopo%2Ffeatures%2Ftopo-feature%2Fcontext.jsonld">View on JSON-LD Playground</a>

You can find the full JSON-LD context here:
<a href="https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature/context.jsonld" target="_blank">https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature/context.jsonld</a>

# Validation

## SHACL Shapes

The following sets of SHACL shapes are used for validating this building block:

* Feature with topology <small><code>ogc.geo.topo.features.topo-feature</code></small>
  * [https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature/tests/geometry-coordinates.shacl](https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature/tests/geometry-coordinates.shacl)
  * [https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature-collection/tests/topo-refs-exist.shacl](https://ogcincubator.github.io/topo-feature/_sources/features/topo-feature-collection/tests/topo-refs-exist.shacl)

# For developers

The source code for this Building Block can be found in the following repository:

* URL: <a href="https://github.com/ogcincubator/topo-feature" target="_blank">https://github.com/ogcincubator/topo-feature</a>
* Path:
<code><a href="https://github.com/ogcincubator/topo-feature/blob/HEAD/_sources/features/topo-feature" target="_blank">_sources/features/topo-feature</a></code>

