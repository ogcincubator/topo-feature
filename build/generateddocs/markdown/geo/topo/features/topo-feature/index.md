
# Feature with topology (Schema)

`ogc.geo.topo.features.topo-feature` *v0.1*

This building block defines a GeoJSON feature with topological relationships to point nodes, or other to TopoFeatures

[*Status*](http://www.opengis.net/def/status): Under development

## Description

## Feature with explicit Topology

A feature type using a topology property to reference an ordered list of references to other features. 

Other features may be either features with topology properties or GeoJSON (or FG-JSON) point objects.

This is a generalisation of the TopoJSON concept using inline data, (nested sets of coordinates) but not limited to the LineStrings. Topological defined objects 
can be solids, swept volumes or any other concept. (It doesnt use TopoJSON coordinate compaction and transformation, however it does allow for explicit CRS, and coordinate compaction transformations could be defined as derived CRS if required.)


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
  "@context": "https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature/context.jsonld",
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
  "@context": "https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature/context.jsonld",
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

#### ttl
```ttl
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

<http://www.example.com/features/TriangleP1P2P3> a geojson:Feature ;
    geojson:topology [ a geojson:Polygon ;
            geojson:relatedFeatures ( ( <http://www.example.com/features/LineP1P2> <http://www.example.com/features/LineP2P3> <http://www.example.com/features/LineP3P1> ) ) ] .


```

## Schema

```yaml
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
    "geometry": "geojson:geometry",
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

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/topo-feature](https://github.com/ogcincubator/topo-feature)
* Path: `_sources/features/topo-feature`

