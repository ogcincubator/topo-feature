
# Feature with topology (Schema)

`ogc.geo.topo.features.topo-feature` *v0.1*

This building block defines a GeoJSON feature with topological relationships to point nodes, or other to TopoFeatures

[*Status*](http://www.opengis.net/def/status): Under development

## Description

## Feature with explicit Topology 

%definition% 

A feature type using a topology property to reference an ordered list of references to other features. 

Other features may be either features with topology properties or GeoJSON (or FG-JSON) point objects.

This is a generalisation of the TopoJSON concept using inline data, but not limited to the LineStrings. Topological defined objects 
can be solids, swept volumes or any other concept.


## Examples

### Example of a LineString
#### json
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

#### jsonld
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

#### ttl
```ttl
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

<http://www.example.com/features/LineP1P2> a geojson:Feature ;
    geojson:topology [ a geojson:LineString ;
            geojson:relatedFeatures ( <http://www.example.com/features/P1> <http://www.example.com/features/P2> ) ] .


```


### Example of a Polygon
#### json
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

#### jsonld
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

#### ttl
```ttl
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

<http://www.example.com/features/TriangleP1P2P3> a geojson:Feature ;
    geojson:topology [ a geojson:Polygon ;
            geojson:relatedFeatures ( "['LineP1P2', 'LineP2P3', 'LineP3P1']" ) ] .


```

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
description: Feature with defined topology for bounding elements
$defs:
  FeatureOptions:
    anyOf:
    - $ref: https://opengeospatial.github.io/bblocks/annotated-schemas/geo/json-fg/feature/schema.json
    - $ref: https://geojson.org/schema/Feature.json
allOf:
- $ref: '#/$defs/FeatureOptions'
- type: object
  properties:
    id:
      type: string
    topology:
      $ref: ../../datatypes/topology/schema.json
      x-jsonld-type: '@id'
      x-jsonld-id: https://purl.org/geojson/vocab#topology
  required:
  - topology
x-jsonld-prefixes:
  geojson: https://purl.org/geojson/vocab#

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature/schema.yaml)


# JSON-LD Context

```jsonld
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

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/topo-feature](https://github.com/ogcincubator/topo-feature)
* Path: `_sources/features/topo-feature`

