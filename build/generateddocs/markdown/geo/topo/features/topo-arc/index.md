
# Arc Description using Point topology (Schema)

`ogc.geo.topo.features.topo-arc` *v0.1*

Defines options for describing Arcs using point features as canonical source of geometry coordinates

[*Status*](http://www.opengis.net/def/status): Under development

## Description

## Topology defined Arc

%definition% 

A feature type using a topology property to reference points defining an Arc.

![Example](https://ogcincubator.github.io/topo-feature/_sources/features/topo-arc/assets/arc.png)
## Examples

### Example GeoJSON feature using topology
Arc with Center example.
#### json
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
    ]
  },
  "properties": {
    "arcLength": 25.615,
    "radius": 105.438
  }
}
```

#### jsonld
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
    ]
  },
  "properties": {
    "arcLength": 25.615,
    "radius": 105.438
  },
  "@context": "https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-arc/context.jsonld"
}
```

#### ttl
```ttl
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

<http://www.example.com/features/1853004> a geojson:Feature ;
    geojson:topology [ a <http://www.example.com/features/ArcWithCenter> ;
            geojson:relatedFeatures ( <http://www.example.com/features/P1> <http://www.example.com/features/P2> <http://www.example.com/features/PC> ) ] .


```

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
description: Arc Feature with geometry by reference
allOf:
- $ref: ../topo-feature/schema.json
- properties:
    topology:
      allOf:
      - $ref: ../../datatypes/topology/schema.json
      - properties:
          type:
            type: string
            const: ArcWithCenter
          references:
            minItems: 3
            maxItems: 3
  required:
  - topology

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-arc/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-arc/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "topology": {
      "@context": {},
      "@type": "@id",
      "@id": "geojson:topology"
    },
    "type": "@type",
    "references": {
      "@id": "geojson:relatedFeatures",
      "@type": "@id",
      "@container": "@list"
    },
    "LineString": "geojson:LineString",
    "Feature": "geojson:Feature",
    "FeatureCollection": "geojson:FeatureCollection",
    "GeometryCollection": "geojson:GeometryCollection",
    "MultiLineString": "geojson:MultiLineString",
    "MultiPoint": "geojson:MultiPoint",
    "MultiPolygon": "geojson:MultiPolygon",
    "Point": "geojson:Point",
    "Polygon": "geojson:Polygon",
    "bbox": {
      "@container": "@list",
      "@id": "geojson:bbox"
    },
    "coordinates": {
      "@container": "@list",
      "@id": "geojson:coordinates"
    },
    "features": {
      "@container": "@set",
      "@id": "geojson:features"
    },
    "id": "@id",
    "links": {
      "@context": {
        "href": "oa:hasTarget",
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
    "geometry": "geojson:geometry",
    "properties": "@nest",
    "geojson": "https://purl.org/geojson/vocab#",
    "csdm": "https://linked.data.gov.au/def/csdm/",
    "dct": "http://purl.org/dc/terms/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "oa": "http://www.w3.org/ns/oa#",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/topo-feature/build/annotated/geo/topo/features/topo-arc/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/topo-feature](https://github.com/ogcincubator/topo-feature)
* Path: `_sources/features/topo-arc`

