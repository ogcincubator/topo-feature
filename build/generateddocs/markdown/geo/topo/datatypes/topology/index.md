
# Geometry using references (Schema)

`ogc.geo.topo.datatypes.topology` *v0.1*

Demonstration of a schema using coordinates of points, withpout duplication

[*Status*](http://www.opengis.net/def/status): Under development

## Description

## Topology

%definition% 

A datatype containing ordered list of references to other features. 

Other features may be either features with topology properties or GeoJSON (or FG-JSON) point objects.

This is a generalisation of the TopoJSON concept using inline data, and not limited to linestrings.

Note this requires JSON-LD V1.1 processing to handle nested arrays of references for Polygons etc.


## Examples

### Example Topology object
See panel to right - note that a more user friendly "collapsable" version is in development. 
#### json
```json
{
  "type": "LineString",
  "references": [
    "P1",
    "P2"
  ]
}
```

#### jsonld
```jsonld
{
  "type": "LineString",
  "references": [
    "P1",
    "P2"
  ],
  "@context": "https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/datatypes/topology/context.jsonld"
}
```

#### ttl
```ttl
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

[] a geojson:LineString ;
    geojson:relatedFeatures ( <http://www.example.com/features/P1> <http://www.example.com/features/P2> ) .


```

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
description: feature with geometry by reference
oneOf:
- properties:
    type:
      type: string
      not:
        enum:
        - Polygon
        - MultiLineString
        - MultiPolygon
      x-jsonld-id: '@type'
    references:
      type: array
      items:
        type: string
      x-jsonld-id: https://purl.org/geojson/vocab#relatedFeatures
      x-jsonld-type: '@id'
      x-jsonld-container: '@list'
- properties:
    type:
      type: string
      enum:
      - MultiPolygon
      x-jsonld-id: '@type'
    references:
      type: array
      items:
        type: array
        items:
          type: array
          items:
            type: string
      x-jsonld-id: https://purl.org/geojson/vocab#relatedFeatures
      x-jsonld-type: '@id'
      x-jsonld-container: '@list'
- properties:
    type:
      type: string
      enum:
      - Polygon
      - MultiLineString
      x-jsonld-id: '@type'
    references:
      type: array
      items:
        type: array
        items:
          type: string
      x-jsonld-id: https://purl.org/geojson/vocab#relatedFeatures
      x-jsonld-type: '@id'
      x-jsonld-container: '@list'
required:
- references
- type
x-jsonld-extra-terms:
  LineString: https://purl.org/geojson/vocab#LineString
  MultiLineString: https://purl.org/geojson/vocab#MultiLineString
  MultiPolygon: https://purl.org/geojson/vocab#MultiPolygon
  Polygon: https://purl.org/geojson/vocab#Polygon
  Arc: https://purl.org/geojson/vocab#Arc
  ArcWithCenter: https://purl.org/geojson/vocab#ArcWithCenter
  ArcByChord: https://purl.org/geojson/vocab#ArcByChord
  CircleByCenter: https://purl.org/geojson/vocab#CircleByCenter
  CubicSpline: https://purl.org/geojson/vocab#CubicSpline
  radius: https://purl.org/geojson/vocab#radius
  arcLength: https://purl.org/geojson/vocab#arcLength
  startTangentVector: https://purl.org/geojson/vocab#startTangentVector
  endTangentVector: https://purl.org/geojson/vocab#endTangentVector
x-jsonld-prefixes:
  geojson: https://purl.org/geojson/vocab#
  csdm: https://linked.data.gov.au/def/csdm/
  dct: http://purl.org/dc/terms/

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/datatypes/topology/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/datatypes/topology/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "type": "@type",
    "references": {
      "@id": "geojson:relatedFeatures",
      "@type": "@id",
      "@container": "@list"
    },
    "LineString": "geojson:LineString",
    "MultiLineString": "geojson:MultiLineString",
    "MultiPolygon": "geojson:MultiPolygon",
    "Polygon": "geojson:Polygon",
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
    "csdm": "https://linked.data.gov.au/def/csdm/",
    "dct": "http://purl.org/dc/terms/",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/datatypes/topology/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/topo-feature](https://github.com/ogcincubator/topo-feature)
* Path: `_sources/datatypes/topology`

