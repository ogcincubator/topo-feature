
# Topo Feature Multi-Collection (Schema)

`ogc.geo.topo.features.topo-feature-multi-collection` *v0.1*

A schema for a structured topology dataset containing typed Feature Collections for each topological dimension: points, edges (Line features), faces (Face features), and solids (Polyhedron features). Each collection is restricted to its specific building block type, enabling referential integrity across the topology hierarchy.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

# Topo Feature Multi-Collection

A **Topo Feature Multi-Collection** is a structured dataset that organises topological features into typed named collections, one for each topological dimension. This enables representation of a full topology hierarchy — from point nodes to volumetric solids — in a single, self-describing document.

## Structure

| Collection key | Feature type | Building block | Topology property |
|---|---|---|---|
| `points` | Point geometry nodes | GeoJSON Feature (Point geometry) | — (explicit coordinates) |
| `edges` | Edge (line) topology | `topo-line` | `references`: ordered string IDs |
| `faces` | Face (polygon surface) topology | `topo-face` | `rings[].directed_references`: oriented Edge refs |
| `shells` | Shell (closed surface) topology | `topo-shell` | `directed_references`: oriented Face refs |
| `solids` | Solid (volumetric) topology | `topo-feature` (Solid/Shell) | `shells[].directed_references`: oriented Face refs |

## Reference models

Two reference styles are used, each appropriate to the relationship type:

- **`references`** — a plain ordered array of string feature IDs. Used for edges referencing point nodes, where position (not direction) is what matters.
- **`directed_references`** — an ordered array of oriented object references `{ "ref": "...", "orientation": "+"|"-" }`. Used for Rings referencing Edges, and Shells referencing Faces, where traversal direction determines the sense of the boundary.

The two styles must not coexist within the same topology object.

## Referential integrity chain

```
solids
  └─ topology.shells[].directed_references → Face IDs
       └─ topology.rings[].directed_references → Edge IDs
            └─ topology.references → Point IDs
                 └─ geometry.coordinates (actual 3D coordinates)
```

`geometry` is `null` on all feature types except Points — coordinates are derived by following the reference chain.

## Example skeleton

```json
{
  "type": "FeatureCollection",
  "points": [ { "type": "Feature", "geometry": { "type": "Point", "coordinates": [...] }, ... } ],
  "edges":  [ { "type": "Feature", "geometry": null, "topology": { "type": "Edge", "references": ["uuid:...", "uuid:..."] }, ... } ],
  "faces":  [ { "type": "Feature", "geometry": null, "topology": { "type": "Face",   "rings": [{ "type": "Ring", "directed_references": [...] }] }, ... } ],
  "solids": [ { "type": "Feature", "geometry": null, "topology": { "type": "Solid",  "shells": [{ "type": "Shell", "directed_references": [...] }] }, ... } ]
}
```

## Examples

### Cube example
Self-contained collection of topology objects defining a Cube
![Cube Example](assets/cube.png)

#### json
```json
{
  "@context": {
    "vocabs": "https://linked.data.gov.au/def/csdm/",
    "wa-surveypoint-purpose": "https://linked.data.gov.au/def/csdm/wa-surveypoint-purpose/",
    "wa-survey-purpose": "https://linked.data.gov.au/def/csdm/wa-survey-purpose/",
    "wa-survey-type": "https://linked.data.gov.au/def/csdm/wa-survey-type/",
    "wa-procedure-used": "https://linked.data.gov.au/def/csdm/wa-procedure-used/",
    "wa-survey-documentation-type": "https://linked.data.gov.au/def/csdm/wa-survey-documentation-type/",
    "wa-annotation-role": "https://linked.data.gov.au/def/csdm/wa-annotation/",
    "wa-parcel-purpose": "https://linked.data.gov.au/def/csdm/wa-parcel-purpose/",
    "wa-parcel-type": "https://linked.data.gov.au/def/csdm/wa-parcel-type/",
    "wa-parcel-state": "https://linked.data.gov.au/def/csdm/wa-parcel-state/",
    "wa-nonprimary-parcel-type": "https://linked.data.gov.au/def/csdm/wa-secondary-parcel-type/",
    "wa-monument-form": "https://linked.data.gov.au/def/csdm/wa-monument-form/",
    "wa-monument-condition": "https://linked.data.gov.au/def/csdm/wa-monument-condition/",
    "wa-monument-state": "https://linked.data.gov.au/def/csdm/wa-monument-state/",
    "wa-vector-purpose": "https://linked.data.gov.au/def/csdm/wa-vector-purpose/",
    "wa-vector-type": "https://linked.data.gov.au/def/csdm/wa-vector-type/",
    "wa-secondary-parcel-purpose": "https://linked.data.gov.au/def/csdm/wa-secondary-parcel-purpose/",
    "wa-secondary-parcel-type": "https://linked.data.gov.au/def/csdm/wa-secondary-parcel-type/",
    "wa-secondary-purpose": "https://linked.data.gov.au/def/csdm/wa-secondary-purpose/",
    "wa-interest-type": "https://linked.data.gov.au/def/csdm/wa-interest-type/",
    "wa-interest": "https://linked.data.gov.au/def/csdm/wa-interest/",
    "wa-locality": "https://linked.data.gov.au/def/csdm/wa-locality/",
    "wa-local-government": "https://linked.data.gov.au/def/csdm/wa-local-government/",
    "registered-surveyors": "https://wa.gov.au/surveyors/",
    "foaf": "https://xmlns.com/foaf/0.1/",
    "activityType": "@type"
  },
  "id": "uuid:f685d306-9752-461b-9668-c0de2c5f314b",
  "name": "DP 12345",
  "description": "Cube test for Solid validation",
  "type": "FeatureCollection",
  "featureType": "CSD",
  "tenureType": "wa-parcel-type:freehold",
  "planType": "wa-survey-type:deposited-plan",
  "purpose": "wa-survey-purpose:subdivision",
  "surveyType": "wa-survey-type:SSA",
  "time": {
    "date": "2026-04-22"
  },
  "horizontalCRS": "epsg:7850",
  "verticalCRS": "epsg:5711",
  "bearingRotation": 0.0,
  "surveyTitle": "Cube",
  "adminUnit": [],
  "hasProvenance": [],
  "wasGeneratedBy": {
    "id": "uuid:196649f5-06d7-487e-b525-88b64fbbcd86",
    "endedAtTime": "2026-04-29T04:46:14.358402+00:00"
  },
  "features": [],
  "referencedCSDs": [],
  "points": [
    {
      "id": "uuid:fc5c26bc-6ab0-4ba1-a284-9a3cb1a75139",
      "type": "FeatureCollection",
      "featureType": "CadastralMark",
      "features": [
        {
          "id": "uuid:50447df5-e5a0-45fe-b9f1-9647fc1822a4",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T04:46:14.354281+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99419160999591,
              -31.88795465588693,
              2.5
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404878.496,
              6471542.499,
              2.5
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:a9a916c0-7014-4c99-8c36-7ef46ef50656",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T04:46:14.354281+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99419062965137,
              -31.888044843628364,
              2.5
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404878.496,
              6471532.501,
              2.5
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:9c35c3cd-f638-4d26-8e11-14c9cd2a1432",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T04:46:14.354281+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99408493587124,
              -31.88804400722897,
              2.5
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404868.499,
              6471532.501,
              2.5
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:63c6eeab-41a1-4259-8311-840754422246",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T04:46:14.354281+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99408591631878,
              -31.887953819490452,
              2.5
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404868.499,
              6471542.499,
              2.5
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:ec47d6c8-7252-4d21-a9ec-72eb19275740",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T04:46:14.354281+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99419160999591,
              -31.88795465588693,
              12.5
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404878.496,
              6471542.499,
              12.5
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:1d6deefc-950b-4612-97d6-2a0ab0e9a7b2",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T04:46:14.354281+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99419062965137,
              -31.888044843628364,
              12.5
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404878.496,
              6471532.501,
              12.5
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:de936c58-46ed-4448-991f-f6b526d87f0a",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T04:46:14.354281+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99408591631878,
              -31.887953819490452,
              12.5
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404868.499,
              6471542.499,
              12.5
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:3ddd4be9-563e-44b3-9543-d528eb1246d3",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T04:46:14.354281+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99408493587124,
              -31.88804400722897,
              12.5
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404868.499,
              6471532.501,
              12.5
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        }
      ]
    }
  ],
  "vectorObservations": [],
  "observedVectors": [],
  "parcels": [],
  "edges": [
    {
      "id": "uuid:2e6ccc7c-5281-4bcd-9a4d-a3d6ecea9f7c",
      "type": "FeatureCollection",
      "featureType": "Edge",
      "features": [
        {
          "id": "uuid:6384bde9-4ced-4171-a7f0-d004039fca80",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:50447df5-e5a0-45fe-b9f1-9647fc1822a4",
                "uuid:a9a916c0-7014-4c99-8c36-7ef46ef50656"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.998
          }
        },
        {
          "id": "uuid:eff3a191-d0cc-496c-9b24-6134842b1c46",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:a9a916c0-7014-4c99-8c36-7ef46ef50656",
                "uuid:9c35c3cd-f638-4d26-8e11-14c9cd2a1432"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.997
          }
        },
        {
          "id": "uuid:e5d652b1-1998-4ecc-bd5a-94e5ca1e839c",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:9c35c3cd-f638-4d26-8e11-14c9cd2a1432",
                "uuid:63c6eeab-41a1-4259-8311-840754422246"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.998
          }
        },
        {
          "id": "uuid:75e3a244-67db-4eeb-bd03-7168b92b519a",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:63c6eeab-41a1-4259-8311-840754422246",
                "uuid:50447df5-e5a0-45fe-b9f1-9647fc1822a4"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.997
          }
        },
        {
          "id": "uuid:443eb63f-c20d-4f3e-a6c9-8d81bce492c7",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:50447df5-e5a0-45fe-b9f1-9647fc1822a4",
                "uuid:ec47d6c8-7252-4d21-a9ec-72eb19275740"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 10.0
          }
        },
        {
          "id": "uuid:0761370f-a608-49b2-8527-993f891eb14b",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:1d6deefc-950b-4612-97d6-2a0ab0e9a7b2",
                "uuid:ec47d6c8-7252-4d21-a9ec-72eb19275740"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.998
          }
        },
        {
          "id": "uuid:7b7393b6-9568-4657-a1aa-72c94f11276b",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:1d6deefc-950b-4612-97d6-2a0ab0e9a7b2",
                "uuid:a9a916c0-7014-4c99-8c36-7ef46ef50656"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 10.0
          }
        },
        {
          "id": "uuid:080940ec-1a56-4a4b-8c15-bc27322310b0",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:ec47d6c8-7252-4d21-a9ec-72eb19275740",
                "uuid:de936c58-46ed-4448-991f-f6b526d87f0a"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.997
          }
        },
        {
          "id": "uuid:e8f2be65-98b8-4907-b5f7-a805b70e0af9",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:de936c58-46ed-4448-991f-f6b526d87f0a",
                "uuid:3ddd4be9-563e-44b3-9543-d528eb1246d3"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.998
          }
        },
        {
          "id": "uuid:3833d35f-5a7f-4ef0-81f2-1c257002ff5f",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:3ddd4be9-563e-44b3-9543-d528eb1246d3",
                "uuid:1d6deefc-950b-4612-97d6-2a0ab0e9a7b2"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.997
          }
        },
        {
          "id": "uuid:b3752f9d-1e6c-4cfe-9e20-3130921e7107",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:63c6eeab-41a1-4259-8311-840754422246",
                "uuid:de936c58-46ed-4448-991f-f6b526d87f0a"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 10.0
          }
        },
        {
          "id": "uuid:49a9bd3d-5d7d-4264-b59e-31cb630f51e1",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:9c35c3cd-f638-4d26-8e11-14c9cd2a1432",
                "uuid:3ddd4be9-563e-44b3-9543-d528eb1246d3"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 10.0
          }
        }
      ]
    }
  ],
  "rings": [
    {
      "id": "uuid:e2b2be5f-d7b2-4dc5-875f-c4493e60da78",
      "type": "FeatureCollection",
      "featureType": "Ring",
      "features": [
        {
          "id": "uuid:79d45224-6489-45f6-9be1-9dbf01783ab8",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:6384bde9-4ced-4171-a7f0-d004039fca80",
                "orientation": "+"
              },
              {
                "ref": "uuid:eff3a191-d0cc-496c-9b24-6134842b1c46",
                "orientation": "+"
              },
              {
                "ref": "uuid:e5d652b1-1998-4ecc-bd5a-94e5ca1e839c",
                "orientation": "+"
              },
              {
                "ref": "uuid:75e3a244-67db-4eeb-bd03-7168b92b519a",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "circumference": 39.99
          }
        },
        {
          "id": "uuid:fbc3a8b2-ce00-4879-8451-dc80529265d9",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:6384bde9-4ced-4171-a7f0-d004039fca80",
                "orientation": "-"
              },
              {
                "ref": "uuid:443eb63f-c20d-4f3e-a6c9-8d81bce492c7",
                "orientation": "+"
              },
              {
                "ref": "uuid:0761370f-a608-49b2-8527-993f891eb14b",
                "orientation": "-"
              },
              {
                "ref": "uuid:7b7393b6-9568-4657-a1aa-72c94f11276b",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "circumference": 39.996
          }
        },
        {
          "id": "uuid:5bc28af6-d34e-4eea-bd1a-5b0ab56d3d69",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:0761370f-a608-49b2-8527-993f891eb14b",
                "orientation": "+"
              },
              {
                "ref": "uuid:080940ec-1a56-4a4b-8c15-bc27322310b0",
                "orientation": "+"
              },
              {
                "ref": "uuid:e8f2be65-98b8-4907-b5f7-a805b70e0af9",
                "orientation": "+"
              },
              {
                "ref": "uuid:3833d35f-5a7f-4ef0-81f2-1c257002ff5f",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "circumference": 39.99
          }
        },
        {
          "id": "uuid:4a8cf176-e22f-4b98-a71c-8e9f34503875",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:75e3a244-67db-4eeb-bd03-7168b92b519a",
                "orientation": "-"
              },
              {
                "ref": "uuid:b3752f9d-1e6c-4cfe-9e20-3130921e7107",
                "orientation": "+"
              },
              {
                "ref": "uuid:080940ec-1a56-4a4b-8c15-bc27322310b0",
                "orientation": "-"
              },
              {
                "ref": "uuid:443eb63f-c20d-4f3e-a6c9-8d81bce492c7",
                "orientation": "-"
              }
            ]
          },
          "properties": {
            "circumference": 39.994
          }
        },
        {
          "id": "uuid:0e718fc4-e7ab-4d71-9dc1-e853d7c6d058",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:e5d652b1-1998-4ecc-bd5a-94e5ca1e839c",
                "orientation": "-"
              },
              {
                "ref": "uuid:49a9bd3d-5d7d-4264-b59e-31cb630f51e1",
                "orientation": "+"
              },
              {
                "ref": "uuid:e8f2be65-98b8-4907-b5f7-a805b70e0af9",
                "orientation": "-"
              },
              {
                "ref": "uuid:b3752f9d-1e6c-4cfe-9e20-3130921e7107",
                "orientation": "-"
              }
            ]
          },
          "properties": {
            "circumference": 39.996
          }
        },
        {
          "id": "uuid:aa0b47a7-eaf1-454b-8206-137a9f5a6ddf",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:eff3a191-d0cc-496c-9b24-6134842b1c46",
                "orientation": "-"
              },
              {
                "ref": "uuid:7b7393b6-9568-4657-a1aa-72c94f11276b",
                "orientation": "-"
              },
              {
                "ref": "uuid:3833d35f-5a7f-4ef0-81f2-1c257002ff5f",
                "orientation": "-"
              },
              {
                "ref": "uuid:49a9bd3d-5d7d-4264-b59e-31cb630f51e1",
                "orientation": "-"
              }
            ]
          },
          "properties": {
            "circumference": 39.994
          }
        }
      ]
    }
  ],
  "faces": [
    {
      "id": "uuid:c8072ddf-ca2c-487f-a0db-ea9734ff5f83",
      "type": "FeatureCollection",
      "featureType": "Face",
      "features": [
        {
          "id": "uuid:ec5881db-dc4f-4acd-b89b-f00d333d7ecd",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:79d45224-6489-45f6-9be1-9dbf01783ab8",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              1.491151358216829e-06,
              7.876927158248097e-08,
              -0.9999999999988852
            ],
            "area": 99.95,
            "description": "Bottom boundary face, [Cube]"
          }
        },
        {
          "id": "uuid:fb03e104-a811-4d6c-877d-a0307d9a9c5e",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:fbc3a8b2-ce00-4879-8451-dc80529265d9",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              0.9999999999950753,
              2.167074932871163e-06,
              2.2700698904251706e-06
            ],
            "area": 99.98,
            "description": "East-facing boundary face, [Cube]"
          }
        },
        {
          "id": "uuid:3d789109-fa30-4596-848a-c2455e81375e",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:5bc28af6-d34e-4eea-bd1a-5b0ab56d3d69",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              -1.4886383938598346e-06,
              -7.85830713343613e-08,
              0.999999999998889
            ],
            "area": 99.95,
            "description": "Top boundary face, [Cube]"
          }
        },
        {
          "id": "uuid:86528cc7-4554-48ac-b760-ecabee7a839f",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:4a8cf176-e22f-4b98-a71c-8e9f34503875",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              -2.1532830796335323e-06,
              0.9999999999972471,
              9.322506564778303e-07
            ],
            "area": 99.97,
            "description": "North-facing boundary face, [Cube]"
          }
        },
        {
          "id": "uuid:31264be9-fe48-4388-bdc8-13354e4c0241",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:0e718fc4-e7ab-4d71-9dc1-e853d7c6d058",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              -0.9999999999974037,
              -2.1672380337658753e-06,
              -7.040161281095843e-07
            ],
            "area": 99.98,
            "description": "West-facing boundary face, [Cube]"
          }
        },
        {
          "id": "uuid:1505844c-0cce-4f91-9691-a72d00f822c9",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:aa0b47a7-eaf1-454b-8206-137a9f5a6ddf",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              2.176710274047926e-06,
              -0.9999999999974256,
              6.410791044193729e-07
            ],
            "area": 99.97,
            "description": "South-facing boundary face, [Cube]"
          }
        }
      ]
    }
  ],
  "shells": [
    {
      "id": "uuid:f7278c9b-232a-4e89-a57e-1a928929b1b3",
      "type": "FeatureCollection",
      "featureType": "Shell",
      "features": [
        {
          "id": "uuid:e0a2fca1-71d5-4385-858b-8f5e21a4db49",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Shell",
            "directed_references": [
              {
                "ref": "uuid:ec5881db-dc4f-4acd-b89b-f00d333d7ecd",
                "orientation": "+"
              },
              {
                "ref": "uuid:fb03e104-a811-4d6c-877d-a0307d9a9c5e",
                "orientation": "+"
              },
              {
                "ref": "uuid:3d789109-fa30-4596-848a-c2455e81375e",
                "orientation": "+"
              },
              {
                "ref": "uuid:86528cc7-4554-48ac-b760-ecabee7a839f",
                "orientation": "+"
              },
              {
                "ref": "uuid:31264be9-fe48-4388-bdc8-13354e4c0241",
                "orientation": "+"
              },
              {
                "ref": "uuid:1505844c-0cce-4f91-9691-a72d00f822c9",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "description": "Exterior Shell of Cube"
          }
        }
      ]
    }
  ],
  "solids": [
    {
      "id": "uuid:dcffe577-9eaa-4c3d-a6c7-c17dd3b21368",
      "type": "FeatureCollection",
      "featureType": "Solid",
      "features": [
        {
          "id": "uuid:efab6176-b745-42d9-8e3f-e727274a7ccf",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Solid",
            "shells": [
              {
                "ref": "uuid:e0a2fca1-71d5-4385-858b-8f5e21a4db49",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "name": "Cube",
            "floors": [
              1
            ],
            "volume": 999.422
          }
        }
      ]
    }
  ],
  "supportingDocuments": [],
  "annotations": [],
  "statistics": {
    "point_count": 8,
    "edge_count": 12,
    "ring_count": 6,
    "face_count": 6,
    "shell_count": 1,
    "solid_count": 1
  }
}
```

#### jsonld
```jsonld
{
  "@context": [
    "https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-multi-collection/context.jsonld",
    {
      "vocabs": "https://linked.data.gov.au/def/csdm/",
      "wa-surveypoint-purpose": "https://linked.data.gov.au/def/csdm/wa-surveypoint-purpose/",
      "wa-survey-purpose": "https://linked.data.gov.au/def/csdm/wa-survey-purpose/",
      "wa-survey-type": "https://linked.data.gov.au/def/csdm/wa-survey-type/",
      "wa-procedure-used": "https://linked.data.gov.au/def/csdm/wa-procedure-used/",
      "wa-survey-documentation-type": "https://linked.data.gov.au/def/csdm/wa-survey-documentation-type/",
      "wa-annotation-role": "https://linked.data.gov.au/def/csdm/wa-annotation/",
      "wa-parcel-purpose": "https://linked.data.gov.au/def/csdm/wa-parcel-purpose/",
      "wa-parcel-type": "https://linked.data.gov.au/def/csdm/wa-parcel-type/",
      "wa-parcel-state": "https://linked.data.gov.au/def/csdm/wa-parcel-state/",
      "wa-nonprimary-parcel-type": "https://linked.data.gov.au/def/csdm/wa-secondary-parcel-type/",
      "wa-monument-form": "https://linked.data.gov.au/def/csdm/wa-monument-form/",
      "wa-monument-condition": "https://linked.data.gov.au/def/csdm/wa-monument-condition/",
      "wa-monument-state": "https://linked.data.gov.au/def/csdm/wa-monument-state/",
      "wa-vector-purpose": "https://linked.data.gov.au/def/csdm/wa-vector-purpose/",
      "wa-vector-type": "https://linked.data.gov.au/def/csdm/wa-vector-type/",
      "wa-secondary-parcel-purpose": "https://linked.data.gov.au/def/csdm/wa-secondary-parcel-purpose/",
      "wa-secondary-parcel-type": "https://linked.data.gov.au/def/csdm/wa-secondary-parcel-type/",
      "wa-secondary-purpose": "https://linked.data.gov.au/def/csdm/wa-secondary-purpose/",
      "wa-interest-type": "https://linked.data.gov.au/def/csdm/wa-interest-type/",
      "wa-interest": "https://linked.data.gov.au/def/csdm/wa-interest/",
      "wa-locality": "https://linked.data.gov.au/def/csdm/wa-locality/",
      "wa-local-government": "https://linked.data.gov.au/def/csdm/wa-local-government/",
      "registered-surveyors": "https://wa.gov.au/surveyors/",
      "foaf": "https://xmlns.com/foaf/0.1/",
      "activityType": "@type"
    }
  ],
  "id": "uuid:f685d306-9752-461b-9668-c0de2c5f314b",
  "name": "DP 12345",
  "description": "Cube test for Solid validation",
  "type": "FeatureCollection",
  "featureType": "CSD",
  "tenureType": "wa-parcel-type:freehold",
  "planType": "wa-survey-type:deposited-plan",
  "purpose": "wa-survey-purpose:subdivision",
  "surveyType": "wa-survey-type:SSA",
  "time": {
    "date": "2026-04-22"
  },
  "horizontalCRS": "epsg:7850",
  "verticalCRS": "epsg:5711",
  "bearingRotation": 0.0,
  "surveyTitle": "Cube",
  "adminUnit": [],
  "hasProvenance": [],
  "wasGeneratedBy": {
    "id": "uuid:196649f5-06d7-487e-b525-88b64fbbcd86",
    "endedAtTime": "2026-04-29T04:46:14.358402+00:00"
  },
  "features": [],
  "referencedCSDs": [],
  "points": [
    {
      "id": "uuid:fc5c26bc-6ab0-4ba1-a284-9a3cb1a75139",
      "type": "FeatureCollection",
      "featureType": "CadastralMark",
      "features": [
        {
          "id": "uuid:50447df5-e5a0-45fe-b9f1-9647fc1822a4",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T04:46:14.354281+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99419160999591,
              -31.88795465588693,
              2.5
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404878.496,
              6471542.499,
              2.5
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:a9a916c0-7014-4c99-8c36-7ef46ef50656",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T04:46:14.354281+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99419062965137,
              -31.888044843628364,
              2.5
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404878.496,
              6471532.501,
              2.5
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:9c35c3cd-f638-4d26-8e11-14c9cd2a1432",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T04:46:14.354281+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99408493587124,
              -31.88804400722897,
              2.5
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404868.499,
              6471532.501,
              2.5
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:63c6eeab-41a1-4259-8311-840754422246",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T04:46:14.354281+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99408591631878,
              -31.887953819490452,
              2.5
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404868.499,
              6471542.499,
              2.5
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:ec47d6c8-7252-4d21-a9ec-72eb19275740",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T04:46:14.354281+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99419160999591,
              -31.88795465588693,
              12.5
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404878.496,
              6471542.499,
              12.5
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:1d6deefc-950b-4612-97d6-2a0ab0e9a7b2",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T04:46:14.354281+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99419062965137,
              -31.888044843628364,
              12.5
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404878.496,
              6471532.501,
              12.5
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:de936c58-46ed-4448-991f-f6b526d87f0a",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T04:46:14.354281+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99408591631878,
              -31.887953819490452,
              12.5
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404868.499,
              6471542.499,
              12.5
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:3ddd4be9-563e-44b3-9543-d528eb1246d3",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T04:46:14.354281+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99408493587124,
              -31.88804400722897,
              12.5
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404868.499,
              6471532.501,
              12.5
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        }
      ]
    }
  ],
  "vectorObservations": [],
  "observedVectors": [],
  "parcels": [],
  "edges": [
    {
      "id": "uuid:2e6ccc7c-5281-4bcd-9a4d-a3d6ecea9f7c",
      "type": "FeatureCollection",
      "featureType": "Edge",
      "features": [
        {
          "id": "uuid:6384bde9-4ced-4171-a7f0-d004039fca80",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:50447df5-e5a0-45fe-b9f1-9647fc1822a4",
                "uuid:a9a916c0-7014-4c99-8c36-7ef46ef50656"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.998
          }
        },
        {
          "id": "uuid:eff3a191-d0cc-496c-9b24-6134842b1c46",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:a9a916c0-7014-4c99-8c36-7ef46ef50656",
                "uuid:9c35c3cd-f638-4d26-8e11-14c9cd2a1432"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.997
          }
        },
        {
          "id": "uuid:e5d652b1-1998-4ecc-bd5a-94e5ca1e839c",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:9c35c3cd-f638-4d26-8e11-14c9cd2a1432",
                "uuid:63c6eeab-41a1-4259-8311-840754422246"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.998
          }
        },
        {
          "id": "uuid:75e3a244-67db-4eeb-bd03-7168b92b519a",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:63c6eeab-41a1-4259-8311-840754422246",
                "uuid:50447df5-e5a0-45fe-b9f1-9647fc1822a4"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.997
          }
        },
        {
          "id": "uuid:443eb63f-c20d-4f3e-a6c9-8d81bce492c7",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:50447df5-e5a0-45fe-b9f1-9647fc1822a4",
                "uuid:ec47d6c8-7252-4d21-a9ec-72eb19275740"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 10.0
          }
        },
        {
          "id": "uuid:0761370f-a608-49b2-8527-993f891eb14b",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:1d6deefc-950b-4612-97d6-2a0ab0e9a7b2",
                "uuid:ec47d6c8-7252-4d21-a9ec-72eb19275740"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.998
          }
        },
        {
          "id": "uuid:7b7393b6-9568-4657-a1aa-72c94f11276b",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:1d6deefc-950b-4612-97d6-2a0ab0e9a7b2",
                "uuid:a9a916c0-7014-4c99-8c36-7ef46ef50656"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 10.0
          }
        },
        {
          "id": "uuid:080940ec-1a56-4a4b-8c15-bc27322310b0",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:ec47d6c8-7252-4d21-a9ec-72eb19275740",
                "uuid:de936c58-46ed-4448-991f-f6b526d87f0a"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.997
          }
        },
        {
          "id": "uuid:e8f2be65-98b8-4907-b5f7-a805b70e0af9",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:de936c58-46ed-4448-991f-f6b526d87f0a",
                "uuid:3ddd4be9-563e-44b3-9543-d528eb1246d3"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.998
          }
        },
        {
          "id": "uuid:3833d35f-5a7f-4ef0-81f2-1c257002ff5f",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:3ddd4be9-563e-44b3-9543-d528eb1246d3",
                "uuid:1d6deefc-950b-4612-97d6-2a0ab0e9a7b2"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.997
          }
        },
        {
          "id": "uuid:b3752f9d-1e6c-4cfe-9e20-3130921e7107",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:63c6eeab-41a1-4259-8311-840754422246",
                "uuid:de936c58-46ed-4448-991f-f6b526d87f0a"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 10.0
          }
        },
        {
          "id": "uuid:49a9bd3d-5d7d-4264-b59e-31cb630f51e1",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:9c35c3cd-f638-4d26-8e11-14c9cd2a1432",
                "uuid:3ddd4be9-563e-44b3-9543-d528eb1246d3"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 10.0
          }
        }
      ]
    }
  ],
  "rings": [
    {
      "id": "uuid:e2b2be5f-d7b2-4dc5-875f-c4493e60da78",
      "type": "FeatureCollection",
      "featureType": "Ring",
      "features": [
        {
          "id": "uuid:79d45224-6489-45f6-9be1-9dbf01783ab8",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:6384bde9-4ced-4171-a7f0-d004039fca80",
                "orientation": "+"
              },
              {
                "ref": "uuid:eff3a191-d0cc-496c-9b24-6134842b1c46",
                "orientation": "+"
              },
              {
                "ref": "uuid:e5d652b1-1998-4ecc-bd5a-94e5ca1e839c",
                "orientation": "+"
              },
              {
                "ref": "uuid:75e3a244-67db-4eeb-bd03-7168b92b519a",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "circumference": 39.99
          }
        },
        {
          "id": "uuid:fbc3a8b2-ce00-4879-8451-dc80529265d9",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:6384bde9-4ced-4171-a7f0-d004039fca80",
                "orientation": "-"
              },
              {
                "ref": "uuid:443eb63f-c20d-4f3e-a6c9-8d81bce492c7",
                "orientation": "+"
              },
              {
                "ref": "uuid:0761370f-a608-49b2-8527-993f891eb14b",
                "orientation": "-"
              },
              {
                "ref": "uuid:7b7393b6-9568-4657-a1aa-72c94f11276b",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "circumference": 39.996
          }
        },
        {
          "id": "uuid:5bc28af6-d34e-4eea-bd1a-5b0ab56d3d69",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:0761370f-a608-49b2-8527-993f891eb14b",
                "orientation": "+"
              },
              {
                "ref": "uuid:080940ec-1a56-4a4b-8c15-bc27322310b0",
                "orientation": "+"
              },
              {
                "ref": "uuid:e8f2be65-98b8-4907-b5f7-a805b70e0af9",
                "orientation": "+"
              },
              {
                "ref": "uuid:3833d35f-5a7f-4ef0-81f2-1c257002ff5f",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "circumference": 39.99
          }
        },
        {
          "id": "uuid:4a8cf176-e22f-4b98-a71c-8e9f34503875",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:75e3a244-67db-4eeb-bd03-7168b92b519a",
                "orientation": "-"
              },
              {
                "ref": "uuid:b3752f9d-1e6c-4cfe-9e20-3130921e7107",
                "orientation": "+"
              },
              {
                "ref": "uuid:080940ec-1a56-4a4b-8c15-bc27322310b0",
                "orientation": "-"
              },
              {
                "ref": "uuid:443eb63f-c20d-4f3e-a6c9-8d81bce492c7",
                "orientation": "-"
              }
            ]
          },
          "properties": {
            "circumference": 39.994
          }
        },
        {
          "id": "uuid:0e718fc4-e7ab-4d71-9dc1-e853d7c6d058",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:e5d652b1-1998-4ecc-bd5a-94e5ca1e839c",
                "orientation": "-"
              },
              {
                "ref": "uuid:49a9bd3d-5d7d-4264-b59e-31cb630f51e1",
                "orientation": "+"
              },
              {
                "ref": "uuid:e8f2be65-98b8-4907-b5f7-a805b70e0af9",
                "orientation": "-"
              },
              {
                "ref": "uuid:b3752f9d-1e6c-4cfe-9e20-3130921e7107",
                "orientation": "-"
              }
            ]
          },
          "properties": {
            "circumference": 39.996
          }
        },
        {
          "id": "uuid:aa0b47a7-eaf1-454b-8206-137a9f5a6ddf",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:eff3a191-d0cc-496c-9b24-6134842b1c46",
                "orientation": "-"
              },
              {
                "ref": "uuid:7b7393b6-9568-4657-a1aa-72c94f11276b",
                "orientation": "-"
              },
              {
                "ref": "uuid:3833d35f-5a7f-4ef0-81f2-1c257002ff5f",
                "orientation": "-"
              },
              {
                "ref": "uuid:49a9bd3d-5d7d-4264-b59e-31cb630f51e1",
                "orientation": "-"
              }
            ]
          },
          "properties": {
            "circumference": 39.994
          }
        }
      ]
    }
  ],
  "faces": [
    {
      "id": "uuid:c8072ddf-ca2c-487f-a0db-ea9734ff5f83",
      "type": "FeatureCollection",
      "featureType": "Face",
      "features": [
        {
          "id": "uuid:ec5881db-dc4f-4acd-b89b-f00d333d7ecd",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:79d45224-6489-45f6-9be1-9dbf01783ab8",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              1.491151358216829e-06,
              7.876927158248097e-08,
              -0.9999999999988852
            ],
            "area": 99.95,
            "description": "Bottom boundary face, [Cube]"
          }
        },
        {
          "id": "uuid:fb03e104-a811-4d6c-877d-a0307d9a9c5e",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:fbc3a8b2-ce00-4879-8451-dc80529265d9",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              0.9999999999950753,
              2.167074932871163e-06,
              2.2700698904251706e-06
            ],
            "area": 99.98,
            "description": "East-facing boundary face, [Cube]"
          }
        },
        {
          "id": "uuid:3d789109-fa30-4596-848a-c2455e81375e",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:5bc28af6-d34e-4eea-bd1a-5b0ab56d3d69",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              -1.4886383938598346e-06,
              -7.85830713343613e-08,
              0.999999999998889
            ],
            "area": 99.95,
            "description": "Top boundary face, [Cube]"
          }
        },
        {
          "id": "uuid:86528cc7-4554-48ac-b760-ecabee7a839f",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:4a8cf176-e22f-4b98-a71c-8e9f34503875",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              -2.1532830796335323e-06,
              0.9999999999972471,
              9.322506564778303e-07
            ],
            "area": 99.97,
            "description": "North-facing boundary face, [Cube]"
          }
        },
        {
          "id": "uuid:31264be9-fe48-4388-bdc8-13354e4c0241",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:0e718fc4-e7ab-4d71-9dc1-e853d7c6d058",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              -0.9999999999974037,
              -2.1672380337658753e-06,
              -7.040161281095843e-07
            ],
            "area": 99.98,
            "description": "West-facing boundary face, [Cube]"
          }
        },
        {
          "id": "uuid:1505844c-0cce-4f91-9691-a72d00f822c9",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:aa0b47a7-eaf1-454b-8206-137a9f5a6ddf",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              2.176710274047926e-06,
              -0.9999999999974256,
              6.410791044193729e-07
            ],
            "area": 99.97,
            "description": "South-facing boundary face, [Cube]"
          }
        }
      ]
    }
  ],
  "shells": [
    {
      "id": "uuid:f7278c9b-232a-4e89-a57e-1a928929b1b3",
      "type": "FeatureCollection",
      "featureType": "Shell",
      "features": [
        {
          "id": "uuid:e0a2fca1-71d5-4385-858b-8f5e21a4db49",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Shell",
            "directed_references": [
              {
                "ref": "uuid:ec5881db-dc4f-4acd-b89b-f00d333d7ecd",
                "orientation": "+"
              },
              {
                "ref": "uuid:fb03e104-a811-4d6c-877d-a0307d9a9c5e",
                "orientation": "+"
              },
              {
                "ref": "uuid:3d789109-fa30-4596-848a-c2455e81375e",
                "orientation": "+"
              },
              {
                "ref": "uuid:86528cc7-4554-48ac-b760-ecabee7a839f",
                "orientation": "+"
              },
              {
                "ref": "uuid:31264be9-fe48-4388-bdc8-13354e4c0241",
                "orientation": "+"
              },
              {
                "ref": "uuid:1505844c-0cce-4f91-9691-a72d00f822c9",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "description": "Exterior Shell of Cube"
          }
        }
      ]
    }
  ],
  "solids": [
    {
      "id": "uuid:dcffe577-9eaa-4c3d-a6c7-c17dd3b21368",
      "type": "FeatureCollection",
      "featureType": "Solid",
      "features": [
        {
          "id": "uuid:efab6176-b745-42d9-8e3f-e727274a7ccf",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Solid",
            "shells": [
              {
                "ref": "uuid:e0a2fca1-71d5-4385-858b-8f5e21a4db49",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "name": "Cube",
            "floors": [
              1
            ],
            "volume": 999.422
          }
        }
      ]
    }
  ],
  "supportingDocuments": [],
  "annotations": [],
  "statistics": {
    "point_count": 8,
    "edge_count": 12,
    "ring_count": 6,
    "face_count": 6,
    "shell_count": 1,
    "solid_count": 1
  }
}
```

#### ttl
```ttl
@prefix dct: <http://purl.org/dc/terms/> .
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix time: <http://www.w3.org/2006/time#> .
@prefix topo: <https://purl.org/geojson/topo#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<uuid:0761370f-a608-49b2-8527-993f891eb14b> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( ( <uuid:1d6deefc-950b-4612-97d6-2a0ab0e9a7b2> <uuid:ec47d6c8-7252-4d21-a9ec-72eb19275740> ) ) ] .

<uuid:080940ec-1a56-4a4b-8c15-bc27322310b0> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( ( <uuid:ec47d6c8-7252-4d21-a9ec-72eb19275740> <uuid:de936c58-46ed-4448-991f-f6b526d87f0a> ) ) ] .

<uuid:2e6ccc7c-5281-4bcd-9a4d-a3d6ecea9f7c> a topo:Edge,
        geojson:FeatureCollection ;
    geojson:features <uuid:0761370f-a608-49b2-8527-993f891eb14b>,
        <uuid:080940ec-1a56-4a4b-8c15-bc27322310b0>,
        <uuid:3833d35f-5a7f-4ef0-81f2-1c257002ff5f>,
        <uuid:443eb63f-c20d-4f3e-a6c9-8d81bce492c7>,
        <uuid:49a9bd3d-5d7d-4264-b59e-31cb630f51e1>,
        <uuid:6384bde9-4ced-4171-a7f0-d004039fca80>,
        <uuid:75e3a244-67db-4eeb-bd03-7168b92b519a>,
        <uuid:7b7393b6-9568-4657-a1aa-72c94f11276b>,
        <uuid:b3752f9d-1e6c-4cfe-9e20-3130921e7107>,
        <uuid:e5d652b1-1998-4ecc-bd5a-94e5ca1e839c>,
        <uuid:e8f2be65-98b8-4907-b5f7-a805b70e0af9>,
        <uuid:eff3a191-d0cc-496c-9b24-6134842b1c46> .

<uuid:3833d35f-5a7f-4ef0-81f2-1c257002ff5f> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( ( <uuid:3ddd4be9-563e-44b3-9543-d528eb1246d3> <uuid:1d6deefc-950b-4612-97d6-2a0ab0e9a7b2> ) ) ] .

<uuid:443eb63f-c20d-4f3e-a6c9-8d81bce492c7> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( ( <uuid:50447df5-e5a0-45fe-b9f1-9647fc1822a4> <uuid:ec47d6c8-7252-4d21-a9ec-72eb19275740> ) ) ] .

<uuid:49a9bd3d-5d7d-4264-b59e-31cb630f51e1> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( ( <uuid:9c35c3cd-f638-4d26-8e11-14c9cd2a1432> <uuid:3ddd4be9-563e-44b3-9543-d528eb1246d3> ) ) ] .

<uuid:6384bde9-4ced-4171-a7f0-d004039fca80> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( ( <uuid:50447df5-e5a0-45fe-b9f1-9647fc1822a4> <uuid:a9a916c0-7014-4c99-8c36-7ef46ef50656> ) ) ] .

<uuid:75e3a244-67db-4eeb-bd03-7168b92b519a> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( ( <uuid:63c6eeab-41a1-4259-8311-840754422246> <uuid:50447df5-e5a0-45fe-b9f1-9647fc1822a4> ) ) ] .

<uuid:7b7393b6-9568-4657-a1aa-72c94f11276b> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( ( <uuid:1d6deefc-950b-4612-97d6-2a0ab0e9a7b2> <uuid:a9a916c0-7014-4c99-8c36-7ef46ef50656> ) ) ] .

<uuid:b3752f9d-1e6c-4cfe-9e20-3130921e7107> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( ( <uuid:63c6eeab-41a1-4259-8311-840754422246> <uuid:de936c58-46ed-4448-991f-f6b526d87f0a> ) ) ] .

<uuid:e5d652b1-1998-4ecc-bd5a-94e5ca1e839c> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( ( <uuid:9c35c3cd-f638-4d26-8e11-14c9cd2a1432> <uuid:63c6eeab-41a1-4259-8311-840754422246> ) ) ] .

<uuid:e8f2be65-98b8-4907-b5f7-a805b70e0af9> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( ( <uuid:de936c58-46ed-4448-991f-f6b526d87f0a> <uuid:3ddd4be9-563e-44b3-9543-d528eb1246d3> ) ) ] .

<uuid:eff3a191-d0cc-496c-9b24-6134842b1c46> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( ( <uuid:a9a916c0-7014-4c99-8c36-7ef46ef50656> <uuid:9c35c3cd-f638-4d26-8e11-14c9cd2a1432> ) ) ] .

<uuid:1d6deefc-950b-4612-97d6-2a0ab0e9a7b2> a <file:///github/workspace/BoundaryMark>,
        geojson:Feature ;
    dct:spatial [ a geojson:Point ;
            geojson:coordinates ( 4.048785e+05 6.471533e+06 1.25e+01 ) ] ;
    dct:time "2026-04-29T04:46:14.354281+00:00" ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.159942e+02 -3.188804e+01 1.25e+01 ) ] .

<uuid:3ddd4be9-563e-44b3-9543-d528eb1246d3> a <file:///github/workspace/BoundaryMark>,
        geojson:Feature ;
    dct:spatial [ a geojson:Point ;
            geojson:coordinates ( 4.048685e+05 6.471533e+06 1.25e+01 ) ] ;
    dct:time "2026-04-29T04:46:14.354281+00:00" ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.159941e+02 -3.188804e+01 1.25e+01 ) ] .

<uuid:50447df5-e5a0-45fe-b9f1-9647fc1822a4> a <file:///github/workspace/BoundaryMark>,
        geojson:Feature ;
    dct:spatial [ a geojson:Point ;
            geojson:coordinates ( 4.048785e+05 6.471542e+06 2.5e+00 ) ] ;
    dct:time "2026-04-29T04:46:14.354281+00:00" ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.159942e+02 -3.188795e+01 2.5e+00 ) ] .

<uuid:63c6eeab-41a1-4259-8311-840754422246> a <file:///github/workspace/BoundaryMark>,
        geojson:Feature ;
    dct:spatial [ a geojson:Point ;
            geojson:coordinates ( 4.048685e+05 6.471542e+06 2.5e+00 ) ] ;
    dct:time "2026-04-29T04:46:14.354281+00:00" ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.159941e+02 -3.188795e+01 2.5e+00 ) ] .

<uuid:9c35c3cd-f638-4d26-8e11-14c9cd2a1432> a <file:///github/workspace/BoundaryMark>,
        geojson:Feature ;
    dct:spatial [ a geojson:Point ;
            geojson:coordinates ( 4.048685e+05 6.471533e+06 2.5e+00 ) ] ;
    dct:time "2026-04-29T04:46:14.354281+00:00" ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.159941e+02 -3.188804e+01 2.5e+00 ) ] .

<uuid:a9a916c0-7014-4c99-8c36-7ef46ef50656> a <file:///github/workspace/BoundaryMark>,
        geojson:Feature ;
    dct:spatial [ a geojson:Point ;
            geojson:coordinates ( 4.048785e+05 6.471533e+06 2.5e+00 ) ] ;
    dct:time "2026-04-29T04:46:14.354281+00:00" ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.159942e+02 -3.188804e+01 2.5e+00 ) ] .

<uuid:de936c58-46ed-4448-991f-f6b526d87f0a> a <file:///github/workspace/BoundaryMark>,
        geojson:Feature ;
    dct:spatial [ a geojson:Point ;
            geojson:coordinates ( 4.048685e+05 6.471542e+06 1.25e+01 ) ] ;
    dct:time "2026-04-29T04:46:14.354281+00:00" ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.159941e+02 -3.188795e+01 1.25e+01 ) ] .

<uuid:ec47d6c8-7252-4d21-a9ec-72eb19275740> a <file:///github/workspace/BoundaryMark>,
        geojson:Feature ;
    dct:spatial [ a geojson:Point ;
            geojson:coordinates ( 4.048785e+05 6.471542e+06 1.25e+01 ) ] ;
    dct:time "2026-04-29T04:46:14.354281+00:00" ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.159942e+02 -3.188795e+01 1.25e+01 ) ] .

[] a geojson:FeatureCollection ;
    time: [ ] ;
    topo:edges ( <uuid:2e6ccc7c-5281-4bcd-9a4d-a3d6ecea9f7c> ) ;
    topo:faces ( [ a geojson:FeatureCollection ;
                geojson:features [ a geojson:Feature ],
                    [ a geojson:Feature ],
                    [ a geojson:Feature ],
                    [ a geojson:Feature ],
                    [ a geojson:Feature ],
                    [ a geojson:Feature ] ] ) ;
    topo:points ( [ a geojson:FeatureCollection ;
                geojson:collectionFeatureType "CadastralMark" ;
                geojson:features <uuid:1d6deefc-950b-4612-97d6-2a0ab0e9a7b2>,
                    <uuid:3ddd4be9-563e-44b3-9543-d528eb1246d3>,
                    <uuid:50447df5-e5a0-45fe-b9f1-9647fc1822a4>,
                    <uuid:63c6eeab-41a1-4259-8311-840754422246>,
                    <uuid:9c35c3cd-f638-4d26-8e11-14c9cd2a1432>,
                    <uuid:a9a916c0-7014-4c99-8c36-7ef46ef50656>,
                    <uuid:de936c58-46ed-4448-991f-f6b526d87f0a>,
                    <uuid:ec47d6c8-7252-4d21-a9ec-72eb19275740> ] ) ;
    topo:rings ( [ a geojson:FeatureCollection ;
                geojson:features [ a geojson:Feature ],
                    [ a geojson:Feature ],
                    [ a geojson:Feature ],
                    [ a geojson:Feature ],
                    [ a geojson:Feature ],
                    [ a geojson:Feature ] ] ) ;
    topo:shells ( [ a geojson:FeatureCollection ;
                geojson:features [ a geojson:Feature ] ] ),
        ( [ a geojson:FeatureCollection ;
                geojson:features [ a geojson:Feature ] ] ) .


```


### Tetrahedron example
Self-contained collection of topology objects defining a Tetrahedron
![Tetrahedron Example](assets/tetrahedron.png)

#### json
```json
{
  "@context": {
    "vocabs": "https://linked.data.gov.au/def/csdm/",
    "wa-surveypoint-purpose": "https://linked.data.gov.au/def/csdm/wa-surveypoint-purpose/",
    "wa-survey-purpose": "https://linked.data.gov.au/def/csdm/wa-survey-purpose/",
    "wa-survey-type": "https://linked.data.gov.au/def/csdm/wa-survey-type/",
    "wa-procedure-used": "https://linked.data.gov.au/def/csdm/wa-procedure-used/",
    "wa-survey-documentation-type": "https://linked.data.gov.au/def/csdm/wa-survey-documentation-type/",
    "wa-annotation-role": "https://linked.data.gov.au/def/csdm/wa-annotation/",
    "wa-parcel-purpose": "https://linked.data.gov.au/def/csdm/wa-parcel-purpose/",
    "wa-parcel-type": "https://linked.data.gov.au/def/csdm/wa-parcel-type/",
    "wa-parcel-state": "https://linked.data.gov.au/def/csdm/wa-parcel-state/",
    "wa-nonprimary-parcel-type": "https://linked.data.gov.au/def/csdm/wa-secondary-parcel-type/",
    "wa-monument-form": "https://linked.data.gov.au/def/csdm/wa-monument-form/",
    "wa-monument-condition": "https://linked.data.gov.au/def/csdm/wa-monument-condition/",
    "wa-monument-state": "https://linked.data.gov.au/def/csdm/wa-monument-state/",
    "wa-vector-purpose": "https://linked.data.gov.au/def/csdm/wa-vector-purpose/",
    "wa-vector-type": "https://linked.data.gov.au/def/csdm/wa-vector-type/",
    "wa-secondary-parcel-purpose": "https://linked.data.gov.au/def/csdm/wa-secondary-parcel-purpose/",
    "wa-secondary-parcel-type": "https://linked.data.gov.au/def/csdm/wa-secondary-parcel-type/",
    "wa-secondary-purpose": "https://linked.data.gov.au/def/csdm/wa-secondary-purpose/",
    "wa-interest-type": "https://linked.data.gov.au/def/csdm/wa-interest-type/",
    "wa-interest": "https://linked.data.gov.au/def/csdm/wa-interest/",
    "wa-locality": "https://linked.data.gov.au/def/csdm/wa-locality/",
    "wa-local-government": "https://linked.data.gov.au/def/csdm/wa-local-government/",
    "registered-surveyors": "https://wa.gov.au/surveyors/",
    "foaf": "https://xmlns.com/foaf/0.1/",
    "activityType": "@type"
  },
  "id": "uuid:dc6544b1-4890-465c-9e0e-2e3c9190e167",
  "name": "DP 12346",
  "description": "Tetrahedron test for Solid validation",
  "type": "FeatureCollection",
  "featureType": "CSD",
  "tenureType": "wa-parcel-type:freehold",
  "planType": "wa-survey-type:deposited-plan",
  "purpose": "wa-survey-purpose:subdivision",
  "surveyType": "wa-survey-type:SSA",
  "time": {
    "date": "2026-04-22"
  },
  "horizontalCRS": "epsg:7850",
  "verticalCRS": "epsg:5711",
  "bearingRotation": 0.0,
  "surveyTitle": "Tetrahedron",
  "adminUnit": [],
  "hasProvenance": [],
  "wasGeneratedBy": {
    "id": "uuid:0caed182-4c7f-469c-bd22-353a0caa6029",
    "endedAtTime": "2026-04-29T10:56:47.958523+00:00"
  },
  "features": [],
  "referencedCSDs": [],
  "points": [
    {
      "id": "uuid:ec81ba8d-22d4-4e48-9b1d-766a3a237c14",
      "type": "FeatureCollection",
      "featureType": "CadastralMark",
      "features": [
        {
          "id": "uuid:0cb551de-32c8-4e8e-b35c-29dafd16d194",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T10:56:47.956526+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99407161066546,
              -31.884890946830822,
              7.0
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404863.997,
              6471882.0,
              7.0
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:d0d49749-4274-409c-9445-49dd23ff004f",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T10:56:47.956526+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99396592049114,
              -31.88489011040608,
              7.0
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404854.0,
              6471882.0,
              7.0
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:6c915239-26ce-458b-ac64-92c7c4192d84",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T10:56:47.956526+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99401961985716,
              -31.884812428470113,
              7.0
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404858.999,
              6471890.658,
              7.0
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:8c7e2a33-ab89-4612-a9c0-a17f521dae4c",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T10:56:47.956526+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99401905386198,
              -31.884864495270993,
              15.165
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404858.999,
              6471884.886,
              15.165
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        }
      ]
    }
  ],
  "vectorObservations": [],
  "observedVectors": [],
  "parcels": [],
  "edges": [
    {
      "id": "uuid:fb8a9ceb-5327-43dd-9903-9e55f944c504",
      "type": "FeatureCollection",
      "featureType": "Edge",
      "features": [
        {
          "id": "uuid:b2d5631c-35d2-40a3-b220-b2c96cbf7e28",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:0cb551de-32c8-4e8e-b35c-29dafd16d194",
                "uuid:d0d49749-4274-409c-9445-49dd23ff004f"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.997
          }
        },
        {
          "id": "uuid:50813a67-e5a5-4387-8f08-42fad0fb30c8",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:d0d49749-4274-409c-9445-49dd23ff004f",
                "uuid:6c915239-26ce-458b-ac64-92c7c4192d84"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.998
          }
        },
        {
          "id": "uuid:1829c5f4-dadd-4fc3-b45c-2fbb5ccd2a4d",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:0cb551de-32c8-4e8e-b35c-29dafd16d194",
                "uuid:6c915239-26ce-458b-ac64-92c7c4192d84"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.997
          }
        },
        {
          "id": "uuid:ecd6673f-14f4-4a5e-955c-3bd37a285555",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:8c7e2a33-ab89-4612-a9c0-a17f521dae4c",
                "uuid:0cb551de-32c8-4e8e-b35c-29dafd16d194"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.999
          }
        },
        {
          "id": "uuid:97c57559-d350-41e0-b9b1-ddfce388269a",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:8c7e2a33-ab89-4612-a9c0-a17f521dae4c",
                "uuid:d0d49749-4274-409c-9445-49dd23ff004f"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.999
          }
        },
        {
          "id": "uuid:e5764f3b-563a-443f-a72e-5cbe720ab5b1",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:6c915239-26ce-458b-ac64-92c7c4192d84",
                "uuid:8c7e2a33-ab89-4612-a9c0-a17f521dae4c"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.999
          }
        }
      ]
    }
  ],
  "rings": [
    {
      "id": "uuid:8e35a252-be7e-4b9c-a944-eaa459a6edbc",
      "type": "FeatureCollection",
      "featureType": "Ring",
      "features": [
        {
          "id": "uuid:eb83167b-f5af-4913-9829-3c7d77bea88d",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:b2d5631c-35d2-40a3-b220-b2c96cbf7e28",
                "orientation": "+"
              },
              {
                "ref": "uuid:50813a67-e5a5-4387-8f08-42fad0fb30c8",
                "orientation": "+"
              },
              {
                "ref": "uuid:1829c5f4-dadd-4fc3-b45c-2fbb5ccd2a4d",
                "orientation": "-"
              }
            ]
          },
          "properties": {
            "circumference": 29.992
          }
        },
        {
          "id": "uuid:4647be42-4c58-429c-a841-b3be89e0d224",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:b2d5631c-35d2-40a3-b220-b2c96cbf7e28",
                "orientation": "-"
              },
              {
                "ref": "uuid:ecd6673f-14f4-4a5e-955c-3bd37a285555",
                "orientation": "-"
              },
              {
                "ref": "uuid:97c57559-d350-41e0-b9b1-ddfce388269a",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "circumference": 29.995
          }
        },
        {
          "id": "uuid:fbd9c4a0-3923-46d4-9af9-5795b81a61f2",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:1829c5f4-dadd-4fc3-b45c-2fbb5ccd2a4d",
                "orientation": "+"
              },
              {
                "ref": "uuid:e5764f3b-563a-443f-a72e-5cbe720ab5b1",
                "orientation": "+"
              },
              {
                "ref": "uuid:ecd6673f-14f4-4a5e-955c-3bd37a285555",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "circumference": 29.995
          }
        },
        {
          "id": "uuid:a04d6ffa-9361-43cc-bf4d-0bf8da93fb49",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:50813a67-e5a5-4387-8f08-42fad0fb30c8",
                "orientation": "-"
              },
              {
                "ref": "uuid:97c57559-d350-41e0-b9b1-ddfce388269a",
                "orientation": "-"
              },
              {
                "ref": "uuid:e5764f3b-563a-443f-a72e-5cbe720ab5b1",
                "orientation": "-"
              }
            ]
          },
          "properties": {
            "circumference": 29.996
          }
        }
      ]
    }
  ],
  "faces": [
    {
      "id": "uuid:884e192c-c6a5-4ea2-b074-18e83338f4de",
      "type": "FeatureCollection",
      "featureType": "Face",
      "features": [
        {
          "id": "uuid:4c8c60fa-a557-42ad-8933-72f3df60c105",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:eb83167b-f5af-4913-9829-3c7d77bea88d",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              7.849577686166764e-07,
              4.565325398400118e-07,
              -0.9999999999995878
            ],
            "area": 0.0,
            "description": "Bottom boundary face, [Tetrahedron]"
          }
        },
        {
          "id": "uuid:57fed3e9-9913-4bb5-b264-5a0dfe258ff0",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:4647be42-4c58-429c-a841-b3be89e0d224",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              1.7808205469580298e-06,
              -0.9428393898010157,
              0.33324748316600555
            ],
            "area": 0.0,
            "description": "South-facing boundary face, [Tetrahedron]"
          }
        },
        {
          "id": "uuid:6715b0e9-60cf-4f3a-be10-e74f48ba1bba",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:fbd9c4a0-3923-46d4-9af9-5795b81a61f2",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              0.8165214269277999,
              0.47142121449788443,
              0.33324885279491834
            ],
            "area": 0.0,
            "description": "East-facing boundary face, [Tetrahedron]"
          }
        },
        {
          "id": "uuid:332536ee-1da7-43cb-8b2f-f02bb954e577",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:a04d6ffa-9361-43cc-bf4d-0bf8da93fb49",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              -0.8165239843361661,
              0.47141769035309583,
              0.33324757197306776
            ],
            "area": 43.29,
            "description": "West-facing boundary face, [Tetrahedron]"
          }
        }
      ]
    }
  ],
  "shells": [
    {
      "id": "uuid:cfbb341d-3d43-4222-9cdf-6c160d814dbe",
      "type": "FeatureCollection",
      "featureType": "Shell",
      "features": [
        {
          "id": "uuid:3ab4f36c-87bb-49d8-b2c7-b54922c37a9d",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Shell",
            "directed_references": [
              {
                "ref": "uuid:4c8c60fa-a557-42ad-8933-72f3df60c105",
                "orientation": "+"
              },
              {
                "ref": "uuid:57fed3e9-9913-4bb5-b264-5a0dfe258ff0",
                "orientation": "+"
              },
              {
                "ref": "uuid:6715b0e9-60cf-4f3a-be10-e74f48ba1bba",
                "orientation": "+"
              },
              {
                "ref": "uuid:332536ee-1da7-43cb-8b2f-f02bb954e577",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "description": "Exterior Shell of Tetrahedron"
          }
        }
      ]
    }
  ],
  "solids": [
    {
      "id": "uuid:c682a120-5f65-46c6-aaa4-b55670d13c2c",
      "type": "FeatureCollection",
      "featureType": "Solid",
      "features": [
        {
          "id": "uuid:7a8cf526-c5d4-4c95-951f-468c096f5ab1",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Solid",
            "shells": [
              {
                "ref": "uuid:3ab4f36c-87bb-49d8-b2c7-b54922c37a9d",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "name": "Tetrahedron",
            "floors": [
              1
            ],
            "volume": 117.783
          }
        }
      ]
    }
  ],
  "supportingDocuments": [],
  "annotations": [],
  "statistics": {
    "point_count": 4,
    "edge_count": 6,
    "ring_count": 4,
    "face_count": 4,
    "shell_count": 1,
    "solid_count": 1
  }
}
```

#### jsonld
```jsonld
{
  "@context": [
    "https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-multi-collection/context.jsonld",
    {
      "vocabs": "https://linked.data.gov.au/def/csdm/",
      "wa-surveypoint-purpose": "https://linked.data.gov.au/def/csdm/wa-surveypoint-purpose/",
      "wa-survey-purpose": "https://linked.data.gov.au/def/csdm/wa-survey-purpose/",
      "wa-survey-type": "https://linked.data.gov.au/def/csdm/wa-survey-type/",
      "wa-procedure-used": "https://linked.data.gov.au/def/csdm/wa-procedure-used/",
      "wa-survey-documentation-type": "https://linked.data.gov.au/def/csdm/wa-survey-documentation-type/",
      "wa-annotation-role": "https://linked.data.gov.au/def/csdm/wa-annotation/",
      "wa-parcel-purpose": "https://linked.data.gov.au/def/csdm/wa-parcel-purpose/",
      "wa-parcel-type": "https://linked.data.gov.au/def/csdm/wa-parcel-type/",
      "wa-parcel-state": "https://linked.data.gov.au/def/csdm/wa-parcel-state/",
      "wa-nonprimary-parcel-type": "https://linked.data.gov.au/def/csdm/wa-secondary-parcel-type/",
      "wa-monument-form": "https://linked.data.gov.au/def/csdm/wa-monument-form/",
      "wa-monument-condition": "https://linked.data.gov.au/def/csdm/wa-monument-condition/",
      "wa-monument-state": "https://linked.data.gov.au/def/csdm/wa-monument-state/",
      "wa-vector-purpose": "https://linked.data.gov.au/def/csdm/wa-vector-purpose/",
      "wa-vector-type": "https://linked.data.gov.au/def/csdm/wa-vector-type/",
      "wa-secondary-parcel-purpose": "https://linked.data.gov.au/def/csdm/wa-secondary-parcel-purpose/",
      "wa-secondary-parcel-type": "https://linked.data.gov.au/def/csdm/wa-secondary-parcel-type/",
      "wa-secondary-purpose": "https://linked.data.gov.au/def/csdm/wa-secondary-purpose/",
      "wa-interest-type": "https://linked.data.gov.au/def/csdm/wa-interest-type/",
      "wa-interest": "https://linked.data.gov.au/def/csdm/wa-interest/",
      "wa-locality": "https://linked.data.gov.au/def/csdm/wa-locality/",
      "wa-local-government": "https://linked.data.gov.au/def/csdm/wa-local-government/",
      "registered-surveyors": "https://wa.gov.au/surveyors/",
      "foaf": "https://xmlns.com/foaf/0.1/",
      "activityType": "@type"
    }
  ],
  "id": "uuid:dc6544b1-4890-465c-9e0e-2e3c9190e167",
  "name": "DP 12346",
  "description": "Tetrahedron test for Solid validation",
  "type": "FeatureCollection",
  "featureType": "CSD",
  "tenureType": "wa-parcel-type:freehold",
  "planType": "wa-survey-type:deposited-plan",
  "purpose": "wa-survey-purpose:subdivision",
  "surveyType": "wa-survey-type:SSA",
  "time": {
    "date": "2026-04-22"
  },
  "horizontalCRS": "epsg:7850",
  "verticalCRS": "epsg:5711",
  "bearingRotation": 0.0,
  "surveyTitle": "Tetrahedron",
  "adminUnit": [],
  "hasProvenance": [],
  "wasGeneratedBy": {
    "id": "uuid:0caed182-4c7f-469c-bd22-353a0caa6029",
    "endedAtTime": "2026-04-29T10:56:47.958523+00:00"
  },
  "features": [],
  "referencedCSDs": [],
  "points": [
    {
      "id": "uuid:ec81ba8d-22d4-4e48-9b1d-766a3a237c14",
      "type": "FeatureCollection",
      "featureType": "CadastralMark",
      "features": [
        {
          "id": "uuid:0cb551de-32c8-4e8e-b35c-29dafd16d194",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T10:56:47.956526+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99407161066546,
              -31.884890946830822,
              7.0
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404863.997,
              6471882.0,
              7.0
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:d0d49749-4274-409c-9445-49dd23ff004f",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T10:56:47.956526+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99396592049114,
              -31.88489011040608,
              7.0
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404854.0,
              6471882.0,
              7.0
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:6c915239-26ce-458b-ac64-92c7c4192d84",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T10:56:47.956526+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99401961985716,
              -31.884812428470113,
              7.0
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404858.999,
              6471890.658,
              7.0
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        },
        {
          "id": "uuid:8c7e2a33-ab89-4612-a9c0-a17f521dae4c",
          "type": "Feature",
          "featureType": "BoundaryMark",
          "time": "2026-04-29T10:56:47.956526+00:00",
          "geometry": {
            "type": "Point",
            "coordinates": [
              115.99401905386198,
              -31.884864495270993,
              15.165
            ]
          },
          "place": {
            "type": "Point",
            "coordinates": [
              404858.999,
              6471884.886,
              15.165
            ]
          },
          "properties": {
            "purpose": "wa-surveypoint-purpose:boundary",
            "ptQualityMeasure": 0.1,
            "comment": null,
            "monumentedBy": {
              "form": "wa-monument-form:cadastral-point-unmarked",
              "condition": "wa-monument-condition:ok",
              "state": "wa-monument-state:unmarked"
            }
          }
        }
      ]
    }
  ],
  "vectorObservations": [],
  "observedVectors": [],
  "parcels": [],
  "edges": [
    {
      "id": "uuid:fb8a9ceb-5327-43dd-9903-9e55f944c504",
      "type": "FeatureCollection",
      "featureType": "Edge",
      "features": [
        {
          "id": "uuid:b2d5631c-35d2-40a3-b220-b2c96cbf7e28",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:0cb551de-32c8-4e8e-b35c-29dafd16d194",
                "uuid:d0d49749-4274-409c-9445-49dd23ff004f"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.997
          }
        },
        {
          "id": "uuid:50813a67-e5a5-4387-8f08-42fad0fb30c8",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:d0d49749-4274-409c-9445-49dd23ff004f",
                "uuid:6c915239-26ce-458b-ac64-92c7c4192d84"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.998
          }
        },
        {
          "id": "uuid:1829c5f4-dadd-4fc3-b45c-2fbb5ccd2a4d",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:0cb551de-32c8-4e8e-b35c-29dafd16d194",
                "uuid:6c915239-26ce-458b-ac64-92c7c4192d84"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.997
          }
        },
        {
          "id": "uuid:ecd6673f-14f4-4a5e-955c-3bd37a285555",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:8c7e2a33-ab89-4612-a9c0-a17f521dae4c",
                "uuid:0cb551de-32c8-4e8e-b35c-29dafd16d194"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.999
          }
        },
        {
          "id": "uuid:97c57559-d350-41e0-b9b1-ddfce388269a",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:8c7e2a33-ab89-4612-a9c0-a17f521dae4c",
                "uuid:d0d49749-4274-409c-9445-49dd23ff004f"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.999
          }
        },
        {
          "id": "uuid:e5764f3b-563a-443f-a72e-5cbe720ab5b1",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Edge",
            "references": [
              [
                "uuid:6c915239-26ce-458b-ac64-92c7c4192d84",
                "uuid:8c7e2a33-ab89-4612-a9c0-a17f521dae4c"
              ]
            ]
          },
          "properties": {
            "vectorPurpose": "wa-vector-purpose:3D-Construct",
            "comment": null,
            "length": 9.999
          }
        }
      ]
    }
  ],
  "rings": [
    {
      "id": "uuid:8e35a252-be7e-4b9c-a944-eaa459a6edbc",
      "type": "FeatureCollection",
      "featureType": "Ring",
      "features": [
        {
          "id": "uuid:eb83167b-f5af-4913-9829-3c7d77bea88d",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:b2d5631c-35d2-40a3-b220-b2c96cbf7e28",
                "orientation": "+"
              },
              {
                "ref": "uuid:50813a67-e5a5-4387-8f08-42fad0fb30c8",
                "orientation": "+"
              },
              {
                "ref": "uuid:1829c5f4-dadd-4fc3-b45c-2fbb5ccd2a4d",
                "orientation": "-"
              }
            ]
          },
          "properties": {
            "circumference": 29.992
          }
        },
        {
          "id": "uuid:4647be42-4c58-429c-a841-b3be89e0d224",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:b2d5631c-35d2-40a3-b220-b2c96cbf7e28",
                "orientation": "-"
              },
              {
                "ref": "uuid:ecd6673f-14f4-4a5e-955c-3bd37a285555",
                "orientation": "-"
              },
              {
                "ref": "uuid:97c57559-d350-41e0-b9b1-ddfce388269a",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "circumference": 29.995
          }
        },
        {
          "id": "uuid:fbd9c4a0-3923-46d4-9af9-5795b81a61f2",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:1829c5f4-dadd-4fc3-b45c-2fbb5ccd2a4d",
                "orientation": "+"
              },
              {
                "ref": "uuid:e5764f3b-563a-443f-a72e-5cbe720ab5b1",
                "orientation": "+"
              },
              {
                "ref": "uuid:ecd6673f-14f4-4a5e-955c-3bd37a285555",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "circumference": 29.995
          }
        },
        {
          "id": "uuid:a04d6ffa-9361-43cc-bf4d-0bf8da93fb49",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:50813a67-e5a5-4387-8f08-42fad0fb30c8",
                "orientation": "-"
              },
              {
                "ref": "uuid:97c57559-d350-41e0-b9b1-ddfce388269a",
                "orientation": "-"
              },
              {
                "ref": "uuid:e5764f3b-563a-443f-a72e-5cbe720ab5b1",
                "orientation": "-"
              }
            ]
          },
          "properties": {
            "circumference": 29.996
          }
        }
      ]
    }
  ],
  "faces": [
    {
      "id": "uuid:884e192c-c6a5-4ea2-b074-18e83338f4de",
      "type": "FeatureCollection",
      "featureType": "Face",
      "features": [
        {
          "id": "uuid:4c8c60fa-a557-42ad-8933-72f3df60c105",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:eb83167b-f5af-4913-9829-3c7d77bea88d",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              7.849577686166764e-07,
              4.565325398400118e-07,
              -0.9999999999995878
            ],
            "area": 0.0,
            "description": "Bottom boundary face, [Tetrahedron]"
          }
        },
        {
          "id": "uuid:57fed3e9-9913-4bb5-b264-5a0dfe258ff0",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:4647be42-4c58-429c-a841-b3be89e0d224",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              1.7808205469580298e-06,
              -0.9428393898010157,
              0.33324748316600555
            ],
            "area": 0.0,
            "description": "South-facing boundary face, [Tetrahedron]"
          }
        },
        {
          "id": "uuid:6715b0e9-60cf-4f3a-be10-e74f48ba1bba",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:fbd9c4a0-3923-46d4-9af9-5795b81a61f2",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              0.8165214269277999,
              0.47142121449788443,
              0.33324885279491834
            ],
            "area": 0.0,
            "description": "East-facing boundary face, [Tetrahedron]"
          }
        },
        {
          "id": "uuid:332536ee-1da7-43cb-8b2f-f02bb954e577",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Face",
            "rings": [
              {
                "ref": "uuid:a04d6ffa-9361-43cc-bf4d-0bf8da93fb49",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "normal": [
              -0.8165239843361661,
              0.47141769035309583,
              0.33324757197306776
            ],
            "area": 43.29,
            "description": "West-facing boundary face, [Tetrahedron]"
          }
        }
      ]
    }
  ],
  "shells": [
    {
      "id": "uuid:cfbb341d-3d43-4222-9cdf-6c160d814dbe",
      "type": "FeatureCollection",
      "featureType": "Shell",
      "features": [
        {
          "id": "uuid:3ab4f36c-87bb-49d8-b2c7-b54922c37a9d",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Shell",
            "directed_references": [
              {
                "ref": "uuid:4c8c60fa-a557-42ad-8933-72f3df60c105",
                "orientation": "+"
              },
              {
                "ref": "uuid:57fed3e9-9913-4bb5-b264-5a0dfe258ff0",
                "orientation": "+"
              },
              {
                "ref": "uuid:6715b0e9-60cf-4f3a-be10-e74f48ba1bba",
                "orientation": "+"
              },
              {
                "ref": "uuid:332536ee-1da7-43cb-8b2f-f02bb954e577",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "description": "Exterior Shell of Tetrahedron"
          }
        }
      ]
    }
  ],
  "solids": [
    {
      "id": "uuid:c682a120-5f65-46c6-aaa4-b55670d13c2c",
      "type": "FeatureCollection",
      "featureType": "Solid",
      "features": [
        {
          "id": "uuid:7a8cf526-c5d4-4c95-951f-468c096f5ab1",
          "type": "Feature",
          "geometry": null,
          "topology": {
            "type": "Solid",
            "shells": [
              {
                "ref": "uuid:3ab4f36c-87bb-49d8-b2c7-b54922c37a9d",
                "orientation": "+"
              }
            ]
          },
          "properties": {
            "name": "Tetrahedron",
            "floors": [
              1
            ],
            "volume": 117.783
          }
        }
      ]
    }
  ],
  "supportingDocuments": [],
  "annotations": [],
  "statistics": {
    "point_count": 4,
    "edge_count": 6,
    "ring_count": 4,
    "face_count": 4,
    "shell_count": 1,
    "solid_count": 1
  }
}
```

#### ttl
```ttl
@prefix dct: <http://purl.org/dc/terms/> .
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix time: <http://www.w3.org/2006/time#> .
@prefix topo: <https://purl.org/geojson/topo#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<uuid:1829c5f4-dadd-4fc3-b45c-2fbb5ccd2a4d> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( ( <uuid:0cb551de-32c8-4e8e-b35c-29dafd16d194> <uuid:6c915239-26ce-458b-ac64-92c7c4192d84> ) ) ] .

<uuid:50813a67-e5a5-4387-8f08-42fad0fb30c8> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( ( <uuid:d0d49749-4274-409c-9445-49dd23ff004f> <uuid:6c915239-26ce-458b-ac64-92c7c4192d84> ) ) ] .

<uuid:97c57559-d350-41e0-b9b1-ddfce388269a> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( ( <uuid:8c7e2a33-ab89-4612-a9c0-a17f521dae4c> <uuid:d0d49749-4274-409c-9445-49dd23ff004f> ) ) ] .

<uuid:b2d5631c-35d2-40a3-b220-b2c96cbf7e28> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( ( <uuid:0cb551de-32c8-4e8e-b35c-29dafd16d194> <uuid:d0d49749-4274-409c-9445-49dd23ff004f> ) ) ] .

<uuid:e5764f3b-563a-443f-a72e-5cbe720ab5b1> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( ( <uuid:6c915239-26ce-458b-ac64-92c7c4192d84> <uuid:8c7e2a33-ab89-4612-a9c0-a17f521dae4c> ) ) ] .

<uuid:ecd6673f-14f4-4a5e-955c-3bd37a285555> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( ( <uuid:8c7e2a33-ab89-4612-a9c0-a17f521dae4c> <uuid:0cb551de-32c8-4e8e-b35c-29dafd16d194> ) ) ] .

<uuid:fb8a9ceb-5327-43dd-9903-9e55f944c504> a topo:Edge,
        geojson:FeatureCollection ;
    geojson:features <uuid:1829c5f4-dadd-4fc3-b45c-2fbb5ccd2a4d>,
        <uuid:50813a67-e5a5-4387-8f08-42fad0fb30c8>,
        <uuid:97c57559-d350-41e0-b9b1-ddfce388269a>,
        <uuid:b2d5631c-35d2-40a3-b220-b2c96cbf7e28>,
        <uuid:e5764f3b-563a-443f-a72e-5cbe720ab5b1>,
        <uuid:ecd6673f-14f4-4a5e-955c-3bd37a285555> .

<uuid:0cb551de-32c8-4e8e-b35c-29dafd16d194> a <file:///github/workspace/BoundaryMark>,
        geojson:Feature ;
    dct:spatial [ a geojson:Point ;
            geojson:coordinates ( 4.04864e+05 6.471882e+06 7e+00 ) ] ;
    dct:time "2026-04-29T10:56:47.956526+00:00" ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.159941e+02 -3.188489e+01 7e+00 ) ] .

<uuid:6c915239-26ce-458b-ac64-92c7c4192d84> a <file:///github/workspace/BoundaryMark>,
        geojson:Feature ;
    dct:spatial [ a geojson:Point ;
            geojson:coordinates ( 4.04859e+05 6.471891e+06 7e+00 ) ] ;
    dct:time "2026-04-29T10:56:47.956526+00:00" ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.15994e+02 -3.188481e+01 7e+00 ) ] .

<uuid:8c7e2a33-ab89-4612-a9c0-a17f521dae4c> a <file:///github/workspace/BoundaryMark>,
        geojson:Feature ;
    dct:spatial [ a geojson:Point ;
            geojson:coordinates ( 4.04859e+05 6.471885e+06 1.5165e+01 ) ] ;
    dct:time "2026-04-29T10:56:47.956526+00:00" ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.15994e+02 -3.188486e+01 1.5165e+01 ) ] .

<uuid:d0d49749-4274-409c-9445-49dd23ff004f> a <file:///github/workspace/BoundaryMark>,
        geojson:Feature ;
    dct:spatial [ a geojson:Point ;
            geojson:coordinates ( 4.04854e+05 6.471882e+06 7e+00 ) ] ;
    dct:time "2026-04-29T10:56:47.956526+00:00" ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.15994e+02 -3.188489e+01 7e+00 ) ] .

[] a geojson:FeatureCollection ;
    time: [ ] ;
    topo:edges ( <uuid:fb8a9ceb-5327-43dd-9903-9e55f944c504> ) ;
    topo:faces ( [ a geojson:FeatureCollection ;
                geojson:features [ a geojson:Feature ],
                    [ a geojson:Feature ],
                    [ a geojson:Feature ],
                    [ a geojson:Feature ] ] ) ;
    topo:points ( [ a geojson:FeatureCollection ;
                geojson:collectionFeatureType "CadastralMark" ;
                geojson:features <uuid:0cb551de-32c8-4e8e-b35c-29dafd16d194>,
                    <uuid:6c915239-26ce-458b-ac64-92c7c4192d84>,
                    <uuid:8c7e2a33-ab89-4612-a9c0-a17f521dae4c>,
                    <uuid:d0d49749-4274-409c-9445-49dd23ff004f> ] ) ;
    topo:rings ( [ a geojson:FeatureCollection ;
                geojson:features [ a geojson:Feature ],
                    [ a geojson:Feature ],
                    [ a geojson:Feature ],
                    [ a geojson:Feature ] ] ) ;
    topo:shells ( [ a geojson:FeatureCollection ;
                geojson:features [ a geojson:Feature ] ] ),
        ( [ a geojson:FeatureCollection ;
                geojson:features [ a geojson:Feature ] ] ) .


```


### Points collection (topology nodes)
A minimal example showing 5 Point features used as topology nodes.
Points have explicit 3D coordinates and serve as the base geometry for all higher-order topology.
All other feature types reference these points (directly or transitively) to resolve coordinates.

#### json
```json
{
  "type": "FeatureCollection",
  "features": [],
  "points": [
    {
      "type": "FeatureCollection",
      "features": [
        {
          "id": "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:fad324b9-801f-40f4-b65b-91f8753e9698",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        }
      ]
    }
  ]
}
```

#### jsonld
```jsonld
{
  "@context": "https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-multi-collection/context.jsonld",
  "type": "FeatureCollection",
  "features": [],
  "points": [
    {
      "type": "FeatureCollection",
      "features": [
        {
          "id": "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:fad324b9-801f-40f4-b65b-91f8753e9698",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        }
      ]
    }
  ]
}
```

#### ttl
```ttl
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix topo: <https://purl.org/geojson/topo#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 1e+01 6e+00 ) ] .

<uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 2e+00 3e+00 ) ] .

<uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 1e+01 3e+00 ) ] .

<uuid:c611f840-2829-44b2-b367-3915ca7875a4> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 2e+00 6e+00 ) ] .

<uuid:fad324b9-801f-40f4-b65b-91f8753e9698> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 2e+00 3e+00 ) ] .

[] a geojson:FeatureCollection ;
    topo:points ( [ a geojson:FeatureCollection ;
                geojson:features <uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0>,
                    <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d>,
                    <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38>,
                    <uuid:c611f840-2829-44b2-b367-3915ca7875a4>,
                    <uuid:fad324b9-801f-40f4-b65b-91f8753e9698> ] ) .


```


### Edges collection (LineString topology referencing points)
Edge features using the 'references' model of topology — each edge has type 'LineString'
and references two Point feature IDs in its topology.references array.
geometry is null; actual coordinates are resolved from the referenced points.

#### json
```json
{
  "type": "FeatureCollection",
  "features": [],
  "points": [
    {
      "type": "FeatureCollection",
      "features": [
        {
          "id": "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:fad324b9-801f-40f4-b65b-91f8753e9698",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        }
      ]
    }
  ],
  "edges": [
    {
      "id": "uuid:c60507ba-226b-4e49-a702-e9afef899b23",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0",
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698",
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38"
        ]
      },
      "properties": {
        "length": 8.0
      }
    }
  ]
}
```

#### jsonld
```jsonld
{
  "@context": "https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-multi-collection/context.jsonld",
  "type": "FeatureCollection",
  "features": [],
  "points": [
    {
      "type": "FeatureCollection",
      "features": [
        {
          "id": "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:fad324b9-801f-40f4-b65b-91f8753e9698",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        }
      ]
    }
  ],
  "edges": [
    {
      "id": "uuid:c60507ba-226b-4e49-a702-e9afef899b23",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0",
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698",
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38"
        ]
      },
      "properties": {
        "length": 8.0
      }
    }
  ]
}
```

#### ttl
```ttl
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix topo: <https://purl.org/geojson/topo#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0> <uuid:c611f840-2829-44b2-b367-3915ca7875a4> ) ] .

<uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:c611f840-2829-44b2-b367-3915ca7875a4> <uuid:fad324b9-801f-40f4-b65b-91f8753e9698> ) ] .

<uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 2e+00 3e+00 ) ] .

<uuid:c60507ba-226b-4e49-a702-e9afef899b23> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> <uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0> ) ] .

<uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:fad324b9-801f-40f4-b65b-91f8753e9698> <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> ) ] .

<uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 1e+01 6e+00 ) ] .

<uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 1e+01 3e+00 ) ] .

<uuid:c611f840-2829-44b2-b367-3915ca7875a4> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 2e+00 6e+00 ) ] .

<uuid:fad324b9-801f-40f4-b65b-91f8753e9698> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 2e+00 3e+00 ) ] .

[] a geojson:FeatureCollection ;
    topo:edges ( <uuid:c60507ba-226b-4e49-a702-e9afef899b23> <uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac> <uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569> <uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8> ) ;
    topo:points ( [ a geojson:FeatureCollection ;
                geojson:features <uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0>,
                    <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d>,
                    <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38>,
                    <uuid:c611f840-2829-44b2-b367-3915ca7875a4>,
                    <uuid:fad324b9-801f-40f4-b65b-91f8753e9698> ] ) .


```


### Faces collection (faces referencing edges via Ring directed_references)
Face features referencing edges via Ring topology with directed_references.
Each face has one or more Rings; each Ring's directed_references is an ordered array
of oriented Edge references with 'ref' and 'orientation' ('+' or '-') indicating
direction of traversal. geometry is null on all non-point features — coordinates
are derived from the topological reference chain.

#### json
```json
{
  "type": "FeatureCollection",
  "features": [],
  "points": [
    {
      "type": "FeatureCollection",
      "features": [
        {
          "id": "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:fad324b9-801f-40f4-b65b-91f8753e9698",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              6.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              6.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              6.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              6.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:e7300a01-f8c1-4351-9511-02790a5376b0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:307b7db6-8014-4628-b80e-ff925bf71168",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:caa6045e-4189-4571-8914-1189e51ac71e",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              6.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              6.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              10.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              10.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:206806a4-a2f8-4c04-858e-99d289858a40",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              6.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              6.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:793997c5-bcc4-4610-984b-6cf2c2997348",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8e503e04-ad51-423b-8102-708a845189b6",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              10.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              6.0,
              0.0
            ]
          },
          "properties": null
        }
      ]
    }
  ],
  "edges": [
    {
      "id": "uuid:c60507ba-226b-4e49-a702-e9afef899b23",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0",
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698",
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:8582d9c2-6053-495a-8413-f5493691c0de",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071",
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3",
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3",
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70",
          "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8",
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:7da1c2fe-f798-43cc-af44-ac63f968139c",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3",
          "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:745aa367-94b6-4949-a856-5271ec6672e9",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0",
          "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:f921656a-58e3-4375-bdff-ac8019f524cf",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd",
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0",
          "uuid:307b7db6-8014-4628-b80e-ff925bf71168"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6",
          "uuid:307b7db6-8014-4628-b80e-ff925bf71168"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6",
          "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:307b7db6-8014-4628-b80e-ff925bf71168",
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:fb03276b-4250-4d52-81e1-035a0bd92895",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d",
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:af347f25-a547-477c-b246-cb810756d4dc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "uuid:caa6045e-4189-4571-8914-1189e51ac71e"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:caa6045e-4189-4571-8914-1189e51ac71e",
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:caa6045e-4189-4571-8914-1189e51ac71e",
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:242a8400-a076-4817-86c6-acd56087cec6",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:4ad210b7-5de5-4732-af7c-978de28f988b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6",
          "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9",
          "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:4406e3f5-89dc-463b-84e4-487490f71f1a",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d",
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:511c6e7d-728b-4f1f-9763-9461eb628586",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4",
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9",
          "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:06babc8d-f0d6-43eb-bfad-931055bae084",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51",
          "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:fc877bbe-72a8-4e59-b959-010e6660984a",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09",
          "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:aafd209b-cd13-401a-83f5-26751a02cffe",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51",
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:9238cbda-d019-4b57-8319-0cc355656802",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:91cdc345-f745-4643-bc88-a24f8e2216b0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:206806a4-a2f8-4c04-858e-99d289858a40",
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a",
          "uuid:206806a4-a2f8-4c04-858e-99d289858a40"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:61f99921-a94d-4e0d-8353-f027d76227c5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:474fef44-eb6e-4e19-a871-433f9bac5650",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3",
          "uuid:206806a4-a2f8-4c04-858e-99d289858a40"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717",
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:71af0dde-7fc9-4290-9624-119e91f422ea",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348",
          "uuid:8e503e04-ad51-423b-8102-708a845189b6"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:ad13a84c-df97-4b75-9dc1-1ce452249964",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8e503e04-ad51-423b-8102-708a845189b6",
          "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:c2a00070-f12b-42f9-b78c-b33daa500873",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606",
          "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:13dd8184-f73e-4d9f-9977-3e573274fccc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8e503e04-ad51-423b-8102-708a845189b6",
          "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606",
          "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:ed666061-98c5-439d-ab0d-5a792437a873",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:5a36c75b-053b-4d7b-b512-6777786d6180",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1",
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348",
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0",
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0",
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:a604828d-a36b-4fac-ba6f-6160ade95301",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4",
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:38499704-81f7-4d47-965f-435e0b7b0850",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d",
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:b6e30631-9768-4020-8947-c32137328216",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3"
        ]
      },
      "properties": {
        "length": 4.0
      }
    }
  ],
  "faces": [
    {
      "id": "uuid:4ac3b91b-eeb7-428c-b5e9-7e8a3f0998ae",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:c60507ba-226b-4e49-a702-e9afef899b23",
                "orientation": "+"
              },
              {
                "ref": "uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac",
                "orientation": "+"
              },
              {
                "ref": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
                "orientation": "+"
              },
              {
                "ref": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          1.0,
          0.0,
          -0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:4a294022-4864-49c7-8cee-f9e43360bc4e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
                "orientation": "+"
              },
              {
                "ref": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
                "orientation": "-"
              },
              {
                "ref": "uuid:8582d9c2-6053-495a-8413-f5493691c0de",
                "orientation": "+"
              },
              {
                "ref": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          3.007964248051e-16
        ],
        "area": 18.0
      }
    }
  ]
}
```

#### jsonld
```jsonld
{
  "@context": "https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-multi-collection/context.jsonld",
  "type": "FeatureCollection",
  "features": [],
  "points": [
    {
      "type": "FeatureCollection",
      "features": [
        {
          "id": "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:fad324b9-801f-40f4-b65b-91f8753e9698",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              6.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              6.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              6.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              6.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:e7300a01-f8c1-4351-9511-02790a5376b0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:307b7db6-8014-4628-b80e-ff925bf71168",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:caa6045e-4189-4571-8914-1189e51ac71e",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              6.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              6.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              10.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              10.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:206806a4-a2f8-4c04-858e-99d289858a40",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              6.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              6.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:793997c5-bcc4-4610-984b-6cf2c2997348",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8e503e04-ad51-423b-8102-708a845189b6",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              10.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              6.0,
              0.0
            ]
          },
          "properties": null
        }
      ]
    }
  ],
  "edges": [
    {
      "id": "uuid:c60507ba-226b-4e49-a702-e9afef899b23",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0",
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698",
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:8582d9c2-6053-495a-8413-f5493691c0de",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071",
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3",
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3",
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70",
          "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8",
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:7da1c2fe-f798-43cc-af44-ac63f968139c",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3",
          "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:745aa367-94b6-4949-a856-5271ec6672e9",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0",
          "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:f921656a-58e3-4375-bdff-ac8019f524cf",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd",
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0",
          "uuid:307b7db6-8014-4628-b80e-ff925bf71168"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6",
          "uuid:307b7db6-8014-4628-b80e-ff925bf71168"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6",
          "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:307b7db6-8014-4628-b80e-ff925bf71168",
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:fb03276b-4250-4d52-81e1-035a0bd92895",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d",
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:af347f25-a547-477c-b246-cb810756d4dc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "uuid:caa6045e-4189-4571-8914-1189e51ac71e"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:caa6045e-4189-4571-8914-1189e51ac71e",
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:caa6045e-4189-4571-8914-1189e51ac71e",
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:242a8400-a076-4817-86c6-acd56087cec6",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:4ad210b7-5de5-4732-af7c-978de28f988b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6",
          "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9",
          "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:4406e3f5-89dc-463b-84e4-487490f71f1a",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d",
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:511c6e7d-728b-4f1f-9763-9461eb628586",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4",
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9",
          "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:06babc8d-f0d6-43eb-bfad-931055bae084",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51",
          "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:fc877bbe-72a8-4e59-b959-010e6660984a",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09",
          "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:aafd209b-cd13-401a-83f5-26751a02cffe",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51",
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:9238cbda-d019-4b57-8319-0cc355656802",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:91cdc345-f745-4643-bc88-a24f8e2216b0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:206806a4-a2f8-4c04-858e-99d289858a40",
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a",
          "uuid:206806a4-a2f8-4c04-858e-99d289858a40"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:61f99921-a94d-4e0d-8353-f027d76227c5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:474fef44-eb6e-4e19-a871-433f9bac5650",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3",
          "uuid:206806a4-a2f8-4c04-858e-99d289858a40"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717",
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:71af0dde-7fc9-4290-9624-119e91f422ea",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348",
          "uuid:8e503e04-ad51-423b-8102-708a845189b6"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:ad13a84c-df97-4b75-9dc1-1ce452249964",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8e503e04-ad51-423b-8102-708a845189b6",
          "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:c2a00070-f12b-42f9-b78c-b33daa500873",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606",
          "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:13dd8184-f73e-4d9f-9977-3e573274fccc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8e503e04-ad51-423b-8102-708a845189b6",
          "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606",
          "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:ed666061-98c5-439d-ab0d-5a792437a873",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:5a36c75b-053b-4d7b-b512-6777786d6180",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1",
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348",
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0",
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0",
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:a604828d-a36b-4fac-ba6f-6160ade95301",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4",
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:38499704-81f7-4d47-965f-435e0b7b0850",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d",
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:b6e30631-9768-4020-8947-c32137328216",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3"
        ]
      },
      "properties": {
        "length": 4.0
      }
    }
  ],
  "faces": [
    {
      "id": "uuid:4ac3b91b-eeb7-428c-b5e9-7e8a3f0998ae",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:c60507ba-226b-4e49-a702-e9afef899b23",
                "orientation": "+"
              },
              {
                "ref": "uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac",
                "orientation": "+"
              },
              {
                "ref": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
                "orientation": "+"
              },
              {
                "ref": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          1.0,
          0.0,
          -0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:4a294022-4864-49c7-8cee-f9e43360bc4e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
                "orientation": "+"
              },
              {
                "ref": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
                "orientation": "-"
              },
              {
                "ref": "uuid:8582d9c2-6053-495a-8413-f5493691c0de",
                "orientation": "+"
              },
              {
                "ref": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          3.007964248051e-16
        ],
        "area": 18.0
      }
    }
  ]
}
```

#### ttl
```ttl
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix topo: <https://purl.org/geojson/topo#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<uuid:06babc8d-f0d6-43eb-bfad-931055bae084> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:20d3c864-4a8c-4440-b600-a1d424e92f51> <uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09> ) ] .

<uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:307b7db6-8014-4628-b80e-ff925bf71168> <uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d> ) ] .

<uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:11caaac5-b631-4bd8-a6af-f82cb6371071> <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> ) ] .

<uuid:13dd8184-f73e-4d9f-9977-3e573274fccc> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:8e503e04-ad51-423b-8102-708a845189b6> <uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1> ) ] .

<uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:caa6045e-4189-4571-8914-1189e51ac71e> <uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70> ) ] .

<uuid:242a8400-a076-4817-86c6-acd56087cec6> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e> <uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d> ) ] .

<uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e> <uuid:22138e52-65ef-4773-b69d-5ea2628fad7b> ) ] .

<uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> <uuid:fad324b9-801f-40f4-b65b-91f8753e9698> ) ] .

<uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0> <uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a> ) ] .

<uuid:38499704-81f7-4d47-965f-435e0b7b0850> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d> <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> ) ] .

<uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:22138e52-65ef-4773-b69d-5ea2628fad7b> <uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3> ) ] .

<uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717> <uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df> ) ] .

<uuid:4406e3f5-89dc-463b-84e4-487490f71f1a> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:c060c1dc-6544-4595-b583-72ecf603fd6d> <uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4> ) ] .

<uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3> <uuid:8087116e-84cc-44d1-8047-78dc3837d7e8> ) ] .

<uuid:474fef44-eb6e-4e19-a871-433f9bac5650> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:f34d9f2e-4180-41de-a613-46f78f4c178f> <uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a> ) ] .

<uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df> <uuid:793997c5-bcc4-4610-984b-6cf2c2997348> ) ] .

<uuid:4ad210b7-5de5-4732-af7c-978de28f988b> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6> <uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9> ) ] .

<uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3> <uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0> ) ] .

<uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4> <uuid:793997c5-bcc4-4610-984b-6cf2c2997348> ) ] .

<uuid:511c6e7d-728b-4f1f-9763-9461eb628586> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4> <uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6> ) ] .

<uuid:5a36c75b-053b-4d7b-b512-6777786d6180> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1> <uuid:e7300a01-f8c1-4351-9511-02790a5376b0> ) ] .

<uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:f34d9f2e-4180-41de-a613-46f78f4c178f> <uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70> ) ] .

<uuid:61f99921-a94d-4e0d-8353-f027d76227c5> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e> <uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a> ) ] .

<uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a> <uuid:206806a4-a2f8-4c04-858e-99d289858a40> ) ] .

<uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:e7300a01-f8c1-4351-9511-02790a5376b0> <uuid:307b7db6-8014-4628-b80e-ff925bf71168> ) ] .

<uuid:71af0dde-7fc9-4290-9624-119e91f422ea> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:793997c5-bcc4-4610-984b-6cf2c2997348> <uuid:8e503e04-ad51-423b-8102-708a845189b6> ) ] .

<uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ca62577e-8e24-4af2-88bf-33b34e25e606> <uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1> ) ] .

<uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3> <uuid:206806a4-a2f8-4c04-858e-99d289858a40> ) ] .

<uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70> <uuid:8087116e-84cc-44d1-8047-78dc3837d7e8> ) ] .

<uuid:745aa367-94b6-4949-a856-5271ec6672e9> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:e7300a01-f8c1-4351-9511-02790a5376b0> <uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd> ) ] .

<uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9> <uuid:20d3c864-4a8c-4440-b600-a1d424e92f51> ) ] .

<uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:8087116e-84cc-44d1-8047-78dc3837d7e8> <uuid:11caaac5-b631-4bd8-a6af-f82cb6371071> ) ] .

<uuid:7da1c2fe-f798-43cc-af44-ac63f968139c> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:f34d9f2e-4180-41de-a613-46f78f4c178f> <uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3> ) ] .

<uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0> <uuid:c611f840-2829-44b2-b367-3915ca7875a4> ) ] .

<uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> <uuid:22138e52-65ef-4773-b69d-5ea2628fad7b> ) ] .

<uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:c611f840-2829-44b2-b367-3915ca7875a4> <uuid:fad324b9-801f-40f4-b65b-91f8753e9698> ) ] .

<uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> <uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3> ) ] .

<uuid:8582d9c2-6053-495a-8413-f5493691c0de> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:c611f840-2829-44b2-b367-3915ca7875a4> <uuid:11caaac5-b631-4bd8-a6af-f82cb6371071> ) ] .

<uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:caa6045e-4189-4571-8914-1189e51ac71e> <uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e> ) ] .

<uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e> <uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3> ) ] .

<uuid:91cdc345-f745-4643-bc88-a24f8e2216b0> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> <uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4> ) ] .

<uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3> <uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70> ) ] .

<uuid:9238cbda-d019-4b57-8319-0cc355656802> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> <uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09> ) ] .

<uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:22138e52-65ef-4773-b69d-5ea2628fad7b> <uuid:e7300a01-f8c1-4351-9511-02790a5376b0> ) ] .

<uuid:a604828d-a36b-4fac-ba6f-6160ade95301> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df> <uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6> ) ] .

<uuid:aafd209b-cd13-401a-83f5-26751a02cffe> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:20d3c864-4a8c-4440-b600-a1d424e92f51> <uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e> ) ] .

<uuid:ad13a84c-df97-4b75-9dc1-1ce452249964> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:8e503e04-ad51-423b-8102-708a845189b6> <uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717> ) ] .

<uuid:af347f25-a547-477c-b246-cb810756d4dc> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9> <uuid:caa6045e-4189-4571-8914-1189e51ac71e> ) ] .

<uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:793997c5-bcc4-4610-984b-6cf2c2997348> <uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d> ) ] .

<uuid:b6e30631-9768-4020-8947-c32137328216> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9> <uuid:11caaac5-b631-4bd8-a6af-f82cb6371071> ) ] .

<uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9> <uuid:c060c1dc-6544-4595-b583-72ecf603fd6d> ) ] .

<uuid:c2a00070-f12b-42f9-b78c-b33daa500873> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ca62577e-8e24-4af2-88bf-33b34e25e606> <uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717> ) ] .

<uuid:c60507ba-226b-4e49-a702-e9afef899b23> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> <uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0> ) ] .

<uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9> <uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6> ) ] .

<uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:fad324b9-801f-40f4-b65b-91f8753e9698> <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> ) ] .

<uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6> <uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd> ) ] .

<uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df> <uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0> ) ] .

<uuid:ed666061-98c5-439d-ab0d-5a792437a873> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e> <uuid:ca62577e-8e24-4af2-88bf-33b34e25e606> ) ] .

<uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:22138e52-65ef-4773-b69d-5ea2628fad7b> <uuid:f34d9f2e-4180-41de-a613-46f78f4c178f> ) ] .

<uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0> <uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e> ) ] .

<uuid:f921656a-58e3-4375-bdff-ac8019f524cf> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd> <uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3> ) ] .

<uuid:fb03276b-4250-4d52-81e1-035a0bd92895> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d> <uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9> ) ] .

<uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6> <uuid:307b7db6-8014-4628-b80e-ff925bf71168> ) ] .

<uuid:fc877bbe-72a8-4e59-b959-010e6660984a> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09> <uuid:c060c1dc-6544-4595-b583-72ecf603fd6d> ) ] .

<uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e> <uuid:f34d9f2e-4180-41de-a613-46f78f4c178f> ) ] .

<uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:206806a4-a2f8-4c04-858e-99d289858a40> <uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6> ) ] .

<uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+00 1e+01 6e+00 ) ] .

<uuid:206806a4-a2f8-4c04-858e-99d289858a40> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 6e+00 0e+00 ) ] .

<uuid:20d3c864-4a8c-4440-b600-a1d424e92f51> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+01 1e+01 0e+00 ) ] .

<uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+01 1e+01 3e+00 ) ] .

<uuid:307b7db6-8014-4628-b80e-ff925bf71168> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+00 2e+00 3e+00 ) ] .

<uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+00 2e+00 6e+00 ) ] .

<uuid:8087116e-84cc-44d1-8047-78dc3837d7e8> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 6e+00 6e+00 ) ] .

<uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 0e+00 1e+01 3e+00 ) ] .

<uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 1e+01 6e+00 ) ] .

<uuid:8e503e04-ad51-423b-8102-708a845189b6> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 0e+00 0e+00 3e+00 ) ] .

<uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+01 0e+00 0e+00 ) ] .

<uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 6e+00 0e+00 ) ] .

<uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 0e+00 0e+00 0e+00 ) ] .

<uuid:c060c1dc-6544-4595-b583-72ecf603fd6d> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+01 0e+00 3e+00 ) ] .

<uuid:c611f840-2829-44b2-b367-3915ca7875a4> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 2e+00 6e+00 ) ] .

<uuid:ca62577e-8e24-4af2-88bf-33b34e25e606> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 0e+00 1e+01 0e+00 ) ] .

<uuid:caa6045e-4189-4571-8914-1189e51ac71e> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 6e+00 6e+00 ) ] .

<uuid:fad324b9-801f-40f4-b65b-91f8753e9698> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 2e+00 3e+00 ) ] .

<uuid:11caaac5-b631-4bd8-a6af-f82cb6371071> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 2e+00 6e+00 ) ] .

<uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1e+01 1e+01 0e+00 ) ] .

<uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1e+01 1e+01 6e+00 ) ] .

<uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1e+01 6e+00 6e+00 ) ] .

<uuid:793997c5-bcc4-4610-984b-6cf2c2997348> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 0e+00 3e+00 ) ] .

<uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 0e+00 3e+00 ) ] .

<uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 2e+00 6e+00 ) ] .

<uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 0e+00 0e+00 ) ] .

<uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 1e+01 3e+00 ) ] .

<uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1e+01 6e+00 0e+00 ) ] .

<uuid:e7300a01-f8c1-4351-9511-02790a5376b0> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+00 1e+01 3e+00 ) ] .

<uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 0e+00 0e+00 ) ] .

<uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 6e+00 3e+00 ) ] .

<uuid:22138e52-65ef-4773-b69d-5ea2628fad7b> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1e+01 1e+01 3e+00 ) ] .

<uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 6e+00 3e+00 ) ] .

<uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 2e+00 3e+00 ) ] .

<uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 2e+00 3e+00 ) ] .

<uuid:f34d9f2e-4180-41de-a613-46f78f4c178f> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1e+01 6e+00 3e+00 ) ] .

[] a geojson:FeatureCollection ;
    topo:edges ( <uuid:c60507ba-226b-4e49-a702-e9afef899b23> <uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac> <uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569> <uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8> <uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b> <uuid:8582d9c2-6053-495a-8413-f5493691c0de> <uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add> <uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555> <uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81> <uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03> <uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0> <uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d> <uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5> <uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7> <uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5> <uuid:7da1c2fe-f798-43cc-af44-ac63f968139c> <uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1> <uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6> <uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d> <uuid:745aa367-94b6-4949-a856-5271ec6672e9> <uuid:f921656a-58e3-4375-bdff-ac8019f524cf> <uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24> <uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3> <uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05> <uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78> <uuid:fb03276b-4250-4d52-81e1-035a0bd92895> <uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf> <uuid:af347f25-a547-477c-b246-cb810756d4dc> <uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b> <uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3> <uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724> <uuid:242a8400-a076-4817-86c6-acd56087cec6> <uuid:4ad210b7-5de5-4732-af7c-978de28f988b> <uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e> <uuid:4406e3f5-89dc-463b-84e4-487490f71f1a> <uuid:511c6e7d-728b-4f1f-9763-9461eb628586> <uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc> <uuid:06babc8d-f0d6-43eb-bfad-931055bae084> <uuid:fc877bbe-72a8-4e59-b959-010e6660984a> <uuid:aafd209b-cd13-401a-83f5-26751a02cffe> <uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03> <uuid:9238cbda-d019-4b57-8319-0cc355656802> <uuid:91cdc345-f745-4643-bc88-a24f8e2216b0> <uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4> <uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94> <uuid:61f99921-a94d-4e0d-8353-f027d76227c5> <uuid:474fef44-eb6e-4e19-a871-433f9bac5650> <uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda> <uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0> <uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985> <uuid:71af0dde-7fc9-4290-9624-119e91f422ea> <uuid:ad13a84c-df97-4b75-9dc1-1ce452249964> <uuid:c2a00070-f12b-42f9-b78c-b33daa500873> <uuid:13dd8184-f73e-4d9f-9977-3e573274fccc> <uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f> <uuid:ed666061-98c5-439d-ab0d-5a792437a873> <uuid:5a36c75b-053b-4d7b-b512-6777786d6180> <uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0> <uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17> <uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635> <uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4> <uuid:a604828d-a36b-4fac-ba6f-6160ade95301> <uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280> <uuid:38499704-81f7-4d47-965f-435e0b7b0850> <uuid:b6e30631-9768-4020-8947-c32137328216> <uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa> ) ;
    topo:faces ( [ a geojson:Feature ] [ a geojson:Feature ] ) ;
    topo:points ( [ a geojson:FeatureCollection ;
                geojson:features <uuid:11caaac5-b631-4bd8-a6af-f82cb6371071>,
                    <uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e>,
                    <uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e>,
                    <uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd>,
                    <uuid:206806a4-a2f8-4c04-858e-99d289858a40>,
                    <uuid:20d3c864-4a8c-4440-b600-a1d424e92f51>,
                    <uuid:22138e52-65ef-4773-b69d-5ea2628fad7b>,
                    <uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09>,
                    <uuid:307b7db6-8014-4628-b80e-ff925bf71168>,
                    <uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6>,
                    <uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3>,
                    <uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70>,
                    <uuid:793997c5-bcc4-4610-984b-6cf2c2997348>,
                    <uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4>,
                    <uuid:8087116e-84cc-44d1-8047-78dc3837d7e8>,
                    <uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3>,
                    <uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1>,
                    <uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0>,
                    <uuid:8e503e04-ad51-423b-8102-708a845189b6>,
                    <uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9>,
                    <uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9>,
                    <uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0>,
                    <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d>,
                    <uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df>,
                    <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38>,
                    <uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717>,
                    <uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d>,
                    <uuid:c060c1dc-6544-4595-b583-72ecf603fd6d>,
                    <uuid:c611f840-2829-44b2-b367-3915ca7875a4>,
                    <uuid:ca62577e-8e24-4af2-88bf-33b34e25e606>,
                    <uuid:caa6045e-4189-4571-8914-1189e51ac71e>,
                    <uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a>,
                    <uuid:e7300a01-f8c1-4351-9511-02790a5376b0>,
                    <uuid:f34d9f2e-4180-41de-a613-46f78f4c178f>,
                    <uuid:fad324b9-801f-40f4-b65b-91f8753e9698>,
                    <uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6> ] ) .


```


### Solid (Polyhedron) referencing faces via Shell directed_references
A Solid feature referencing faces via a Shell topology. The solid's topology contains
a 'shells' array; each Shell has a directed_references array of oriented Face references.
All supporting points, edges and faces are included to make the example self-contained.

#### json
```json
{
  "type": "FeatureCollection",
  "features": [],
  "metadata": {
    "units": "meters",
    "coordinate_precision": 3,
    "conversion_factor": 0.0254
  },
  "points": [
    {
      "type": "FeatureCollection",
      "features": [
        {
          "id": "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:fad324b9-801f-40f4-b65b-91f8753e9698",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              6.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              6.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              6.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              6.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:e7300a01-f8c1-4351-9511-02790a5376b0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:307b7db6-8014-4628-b80e-ff925bf71168",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:caa6045e-4189-4571-8914-1189e51ac71e",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              6.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              6.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              10.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              10.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:206806a4-a2f8-4c04-858e-99d289858a40",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              6.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              6.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:793997c5-bcc4-4610-984b-6cf2c2997348",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8e503e04-ad51-423b-8102-708a845189b6",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              10.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              6.0,
              0.0
            ]
          },
          "properties": null
        }
      ]
    }
  ],
  "edges": [
    {
      "id": "uuid:c60507ba-226b-4e49-a702-e9afef899b23",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0",
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698",
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:8582d9c2-6053-495a-8413-f5493691c0de",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071",
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3",
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3",
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70",
          "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8",
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:7da1c2fe-f798-43cc-af44-ac63f968139c",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3",
          "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:745aa367-94b6-4949-a856-5271ec6672e9",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0",
          "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:f921656a-58e3-4375-bdff-ac8019f524cf",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd",
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0",
          "uuid:307b7db6-8014-4628-b80e-ff925bf71168"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6",
          "uuid:307b7db6-8014-4628-b80e-ff925bf71168"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6",
          "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:307b7db6-8014-4628-b80e-ff925bf71168",
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:fb03276b-4250-4d52-81e1-035a0bd92895",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d",
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:af347f25-a547-477c-b246-cb810756d4dc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "uuid:caa6045e-4189-4571-8914-1189e51ac71e"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:caa6045e-4189-4571-8914-1189e51ac71e",
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:caa6045e-4189-4571-8914-1189e51ac71e",
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:242a8400-a076-4817-86c6-acd56087cec6",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:4ad210b7-5de5-4732-af7c-978de28f988b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6",
          "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9",
          "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:4406e3f5-89dc-463b-84e4-487490f71f1a",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d",
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:511c6e7d-728b-4f1f-9763-9461eb628586",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4",
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9",
          "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:06babc8d-f0d6-43eb-bfad-931055bae084",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51",
          "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:fc877bbe-72a8-4e59-b959-010e6660984a",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09",
          "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:aafd209b-cd13-401a-83f5-26751a02cffe",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51",
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:9238cbda-d019-4b57-8319-0cc355656802",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:91cdc345-f745-4643-bc88-a24f8e2216b0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:206806a4-a2f8-4c04-858e-99d289858a40",
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a",
          "uuid:206806a4-a2f8-4c04-858e-99d289858a40"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:61f99921-a94d-4e0d-8353-f027d76227c5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:474fef44-eb6e-4e19-a871-433f9bac5650",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3",
          "uuid:206806a4-a2f8-4c04-858e-99d289858a40"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717",
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:71af0dde-7fc9-4290-9624-119e91f422ea",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348",
          "uuid:8e503e04-ad51-423b-8102-708a845189b6"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:ad13a84c-df97-4b75-9dc1-1ce452249964",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8e503e04-ad51-423b-8102-708a845189b6",
          "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:c2a00070-f12b-42f9-b78c-b33daa500873",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606",
          "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:13dd8184-f73e-4d9f-9977-3e573274fccc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8e503e04-ad51-423b-8102-708a845189b6",
          "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606",
          "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:ed666061-98c5-439d-ab0d-5a792437a873",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:5a36c75b-053b-4d7b-b512-6777786d6180",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1",
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348",
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0",
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0",
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:a604828d-a36b-4fac-ba6f-6160ade95301",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4",
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:38499704-81f7-4d47-965f-435e0b7b0850",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d",
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:b6e30631-9768-4020-8947-c32137328216",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3"
        ]
      },
      "properties": {
        "length": 4.0
      }
    }
  ],
  "faces": [
    {
      "id": "uuid:4ac3b91b-eeb7-428c-b5e9-7e8a3f0998ae",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:c60507ba-226b-4e49-a702-e9afef899b23",
                "orientation": "+"
              },
              {
                "ref": "uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac",
                "orientation": "+"
              },
              {
                "ref": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
                "orientation": "+"
              },
              {
                "ref": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          1.0,
          0.0,
          -0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:4a294022-4864-49c7-8cee-f9e43360bc4e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
                "orientation": "+"
              },
              {
                "ref": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
                "orientation": "-"
              },
              {
                "ref": "uuid:8582d9c2-6053-495a-8413-f5493691c0de",
                "orientation": "+"
              },
              {
                "ref": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          3.007964248051e-16
        ],
        "area": 18.0
      }
    },
    {
      "id": "uuid:01947f47-ee13-44a9-85a4-2bcb4881982a",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555",
                "orientation": "+"
              },
              {
                "ref": "uuid:c60507ba-226b-4e49-a702-e9afef899b23",
                "orientation": "-"
              },
              {
                "ref": "uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81",
                "orientation": "+"
              },
              {
                "ref": "uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:607a3363-3eb7-4ce6-a633-86d2e565692b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:8582d9c2-6053-495a-8413-f5493691c0de",
                "orientation": "-"
              },
              {
                "ref": "uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac",
                "orientation": "-"
              },
              {
                "ref": "uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555",
                "orientation": "-"
              },
              {
                "ref": "uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0",
                "orientation": "+"
              },
              {
                "ref": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
                "orientation": "+"
              },
              {
                "ref": "uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 56.0
      }
    },
    {
      "id": "uuid:3c1f5c4b-d842-40b6-a332-99d50015fa8f",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
                "orientation": "+"
              },
              {
                "ref": "uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5",
                "orientation": "+"
              },
              {
                "ref": "uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0",
                "orientation": "-"
              },
              {
                "ref": "uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:fe522919-1421-4fd1-9930-8c6551e3f2a5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:7da1c2fe-f798-43cc-af44-ac63f968139c",
                "orientation": "+"
              },
              {
                "ref": "uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1",
                "orientation": "+"
              },
              {
                "ref": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
                "orientation": "-"
              },
              {
                "ref": "uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 6.0
      }
    },
    {
      "id": "uuid:2387ae98-9236-42fe-9414-c45b99954c41",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6",
                "orientation": "+"
              },
              {
                "ref": "uuid:7da1c2fe-f798-43cc-af44-ac63f968139c",
                "orientation": "-"
              },
              {
                "ref": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
                "orientation": "-"
              },
              {
                "ref": "uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81",
                "orientation": "-"
              },
              {
                "ref": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
                "orientation": "-"
              },
              {
                "ref": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          -1.0
        ],
        "area": 56.0
      }
    },
    {
      "id": "uuid:4ba85faa-3935-4e89-a9f8-dcd647a5dbed",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6",
                "orientation": "-"
              },
              {
                "ref": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
                "orientation": "-"
              },
              {
                "ref": "uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5",
                "orientation": "-"
              },
              {
                "ref": "uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:c55c88db-d187-4d7e-9aaa-b9d3dce52663",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d",
                "orientation": "+"
              },
              {
                "ref": "uuid:745aa367-94b6-4949-a856-5271ec6672e9",
                "orientation": "+"
              },
              {
                "ref": "uuid:f921656a-58e3-4375-bdff-ac8019f524cf",
                "orientation": "+"
              },
              {
                "ref": "uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:dbd99467-ea83-4dff-b03f-eef2aad2687c",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:745aa367-94b6-4949-a856-5271ec6672e9",
                "orientation": "-"
              },
              {
                "ref": "uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24",
                "orientation": "+"
              },
              {
                "ref": "uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3",
                "orientation": "-"
              },
              {
                "ref": "uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -3.007964248051e-16
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:0e55e87d-8475-4c92-89e7-d62f97ce9ec2",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3",
                "orientation": "+"
              },
              {
                "ref": "uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78",
                "orientation": "+"
              },
              {
                "ref": "uuid:fb03276b-4250-4d52-81e1-035a0bd92895",
                "orientation": "+"
              },
              {
                "ref": "uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 18.0
      }
    },
    {
      "id": "uuid:6a5ff199-56a7-4e65-94b5-bfdf2ae3449d",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:f921656a-58e3-4375-bdff-ac8019f524cf",
                "orientation": "-"
              },
              {
                "ref": "uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05",
                "orientation": "-"
              },
              {
                "ref": "uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf",
                "orientation": "-"
              },
              {
                "ref": "uuid:af347f25-a547-477c-b246-cb810756d4dc",
                "orientation": "+"
              },
              {
                "ref": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
                "orientation": "+"
              },
              {
                "ref": "uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 56.0
      }
    },
    {
      "id": "uuid:e499fea3-19f7-4863-8a58-751caff7d884",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3",
                "orientation": "+"
              },
              {
                "ref": "uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5",
                "orientation": "+"
              },
              {
                "ref": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
                "orientation": "-"
              },
              {
                "ref": "uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 6.0
      }
    },
    {
      "id": "uuid:9e4c0c0e-6acf-401b-b35e-0e917ce3a5fc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:242a8400-a076-4817-86c6-acd56087cec6",
                "orientation": "+"
              },
              {
                "ref": "uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78",
                "orientation": "-"
              },
              {
                "ref": "uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24",
                "orientation": "-"
              },
              {
                "ref": "uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d",
                "orientation": "-"
              },
              {
                "ref": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
                "orientation": "+"
              },
              {
                "ref": "uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          -1.0
        ],
        "area": 56.0
      }
    },
    {
      "id": "uuid:3f5c452f-9815-4b21-9b2d-0127ae80c385",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:242a8400-a076-4817-86c6-acd56087cec6",
                "orientation": "-"
              },
              {
                "ref": "uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724",
                "orientation": "-"
              },
              {
                "ref": "uuid:af347f25-a547-477c-b246-cb810756d4dc",
                "orientation": "-"
              },
              {
                "ref": "uuid:fb03276b-4250-4d52-81e1-035a0bd92895",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          1.0,
          0.0,
          -0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:66a430c0-123f-42df-9d11-64347362bcb3",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:4ad210b7-5de5-4732-af7c-978de28f988b",
                "orientation": "+"
              },
              {
                "ref": "uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e",
                "orientation": "+"
              },
              {
                "ref": "uuid:4406e3f5-89dc-463b-84e4-487490f71f1a",
                "orientation": "+"
              },
              {
                "ref": "uuid:511c6e7d-728b-4f1f-9763-9461eb628586",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:31d8f2b5-cc74-4f72-b230-d27dad0fd589",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc",
                "orientation": "+"
              },
              {
                "ref": "uuid:06babc8d-f0d6-43eb-bfad-931055bae084",
                "orientation": "+"
              },
              {
                "ref": "uuid:fc877bbe-72a8-4e59-b959-010e6660984a",
                "orientation": "+"
              },
              {
                "ref": "uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          1.0,
          0.0,
          -0.0
        ],
        "area": 30.0
      }
    },
    {
      "id": "uuid:65959e29-11cb-4568-904d-61c4a7c17b98",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:aafd209b-cd13-401a-83f5-26751a02cffe",
                "orientation": "+"
              },
              {
                "ref": "uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03",
                "orientation": "+"
              },
              {
                "ref": "uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81",
                "orientation": "-"
              },
              {
                "ref": "uuid:9238cbda-d019-4b57-8319-0cc355656802",
                "orientation": "+"
              },
              {
                "ref": "uuid:06babc8d-f0d6-43eb-bfad-931055bae084",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 30.0
      }
    },
    {
      "id": "uuid:e2efe498-c6d5-4f9c-ac07-4c1c9e406675",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
                "orientation": "-"
              },
              {
                "ref": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
                "orientation": "-"
              },
              {
                "ref": "uuid:91cdc345-f745-4643-bc88-a24f8e2216b0",
                "orientation": "+"
              },
              {
                "ref": "uuid:4406e3f5-89dc-463b-84e4-487490f71f1a",
                "orientation": "-"
              },
              {
                "ref": "uuid:fc877bbe-72a8-4e59-b959-010e6660984a",
                "orientation": "-"
              },
              {
                "ref": "uuid:9238cbda-d019-4b57-8319-0cc355656802",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 32.0
      }
    },
    {
      "id": "uuid:5bcee2b5-be9b-47d6-9a8b-35dac021f661",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:4ad210b7-5de5-4732-af7c-978de28f988b",
                "orientation": "-"
              },
              {
                "ref": "uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4",
                "orientation": "-"
              },
              {
                "ref": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
                "orientation": "-"
              },
              {
                "ref": "uuid:61f99921-a94d-4e0d-8353-f027d76227c5",
                "orientation": "-"
              },
              {
                "ref": "uuid:aafd209b-cd13-401a-83f5-26751a02cffe",
                "orientation": "-"
              },
              {
                "ref": "uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -0.0,
          -0.0,
          -1.0
        ],
        "area": 88.0
      }
    },
    {
      "id": "uuid:91ce0c52-11c3-4e32-8bcc-dea958a3969e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:474fef44-eb6e-4e19-a871-433f9bac5650",
                "orientation": "-"
              },
              {
                "ref": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
                "orientation": "-"
              },
              {
                "ref": "uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03",
                "orientation": "-"
              },
              {
                "ref": "uuid:61f99921-a94d-4e0d-8353-f027d76227c5",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:56283886-1f4c-448c-b785-80fb9740a9cc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda",
                "orientation": "+"
              },
              {
                "ref": "uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4",
                "orientation": "+"
              },
              {
                "ref": "uuid:511c6e7d-728b-4f1f-9763-9461eb628586",
                "orientation": "-"
              },
              {
                "ref": "uuid:91cdc345-f745-4643-bc88-a24f8e2216b0",
                "orientation": "-"
              },
              {
                "ref": "uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -0.0
        ],
        "area": 18.0
      }
    },
    {
      "id": "uuid:f3338301-b0e3-401c-af23-41ac2ae8e969",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda",
                "orientation": "-"
              },
              {
                "ref": "uuid:7da1c2fe-f798-43cc-af44-ac63f968139c",
                "orientation": "-"
              },
              {
                "ref": "uuid:474fef44-eb6e-4e19-a871-433f9bac5650",
                "orientation": "+"
              },
              {
                "ref": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 6.0
      }
    },
    {
      "id": "uuid:a2117d6b-4621-4a6b-9809-9fab3dfc4ff0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0",
                "orientation": "+"
              },
              {
                "ref": "uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985",
                "orientation": "+"
              },
              {
                "ref": "uuid:71af0dde-7fc9-4290-9624-119e91f422ea",
                "orientation": "+"
              },
              {
                "ref": "uuid:ad13a84c-df97-4b75-9dc1-1ce452249964",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:9d67557a-e130-4a47-b63d-c6a2bdf21fa2",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:c2a00070-f12b-42f9-b78c-b33daa500873",
                "orientation": "+"
              },
              {
                "ref": "uuid:ad13a84c-df97-4b75-9dc1-1ce452249964",
                "orientation": "-"
              },
              {
                "ref": "uuid:13dd8184-f73e-4d9f-9977-3e573274fccc",
                "orientation": "+"
              },
              {
                "ref": "uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -0.0
        ],
        "area": 30.0
      }
    },
    {
      "id": "uuid:d45fca44-8685-4146-92a5-b84d82fdc838",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:ed666061-98c5-439d-ab0d-5a792437a873",
                "orientation": "+"
              },
              {
                "ref": "uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f",
                "orientation": "+"
              },
              {
                "ref": "uuid:5a36c75b-053b-4d7b-b512-6777786d6180",
                "orientation": "+"
              },
              {
                "ref": "uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d",
                "orientation": "-"
              },
              {
                "ref": "uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 30.0
      }
    },
    {
      "id": "uuid:2497a842-0932-4fe5-ac1a-2f773473f338",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0",
                "orientation": "+"
              },
              {
                "ref": "uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78",
                "orientation": "-"
              },
              {
                "ref": "uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24",
                "orientation": "-"
              },
              {
                "ref": "uuid:5a36c75b-053b-4d7b-b512-6777786d6180",
                "orientation": "-"
              },
              {
                "ref": "uuid:13dd8184-f73e-4d9f-9977-3e573274fccc",
                "orientation": "-"
              },
              {
                "ref": "uuid:71af0dde-7fc9-4290-9624-119e91f422ea",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 32.0
      }
    },
    {
      "id": "uuid:04ea47e9-b4dd-4bed-a8f4-4802d1735c74",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:ed666061-98c5-439d-ab0d-5a792437a873",
                "orientation": "-"
              },
              {
                "ref": "uuid:61f99921-a94d-4e0d-8353-f027d76227c5",
                "orientation": "+"
              },
              {
                "ref": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
                "orientation": "-"
              },
              {
                "ref": "uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635",
                "orientation": "-"
              },
              {
                "ref": "uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0",
                "orientation": "-"
              },
              {
                "ref": "uuid:c2a00070-f12b-42f9-b78c-b33daa500873",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -0.0,
          -0.0,
          -1.0
        ],
        "area": 88.0
      }
    },
    {
      "id": "uuid:b5fd960f-0d14-4257-9182-40de738a7e50",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4",
                "orientation": "+"
              },
              {
                "ref": "uuid:242a8400-a076-4817-86c6-acd56087cec6",
                "orientation": "+"
              },
              {
                "ref": "uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0",
                "orientation": "-"
              },
              {
                "ref": "uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985",
                "orientation": "-"
              },
              {
                "ref": "uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          1.0,
          0.0,
          -0.0
        ],
        "area": 18.0
      }
    },
    {
      "id": "uuid:e119b096-e589-49bd-b1db-a1182dc2dade",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:474fef44-eb6e-4e19-a871-433f9bac5650",
                "orientation": "-"
              },
              {
                "ref": "uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3",
                "orientation": "-"
              },
              {
                "ref": "uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4",
                "orientation": "-"
              },
              {
                "ref": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 6.0
      }
    },
    {
      "id": "uuid:67842d3a-7c79-4f2a-8630-744711071e93",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:a604828d-a36b-4fac-ba6f-6160ade95301",
                "orientation": "-"
              },
              {
                "ref": "uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635",
                "orientation": "+"
              },
              {
                "ref": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
                "orientation": "+"
              },
              {
                "ref": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
                "orientation": "+"
              },
              {
                "ref": "uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -0.0,
          -0.0,
          -1.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:f1c1a636-d6ab-414c-a0aa-855fc7e85e1f",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280",
                "orientation": "+"
              },
              {
                "ref": "uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985",
                "orientation": "-"
              },
              {
                "ref": "uuid:a604828d-a36b-4fac-ba6f-6160ade95301",
                "orientation": "+"
              },
              {
                "ref": "uuid:511c6e7d-728b-4f1f-9763-9461eb628586",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:a22a6c54-306e-44bc-9b94-6c32c705e63e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280",
                "orientation": "-"
              },
              {
                "ref": "uuid:91cdc345-f745-4643-bc88-a24f8e2216b0",
                "orientation": "-"
              },
              {
                "ref": "uuid:38499704-81f7-4d47-965f-435e0b7b0850",
                "orientation": "-"
              },
              {
                "ref": "uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 8.0
      }
    },
    {
      "id": "uuid:9ed21e0a-b062-4000-88e2-50bd9153e417",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:b6e30631-9768-4020-8947-c32137328216",
                "orientation": "+"
              },
              {
                "ref": "uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5",
                "orientation": "-"
              },
              {
                "ref": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
                "orientation": "-"
              },
              {
                "ref": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
                "orientation": "-"
              },
              {
                "ref": "uuid:af347f25-a547-477c-b246-cb810756d4dc",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 16.0
      }
    },
    {
      "id": "uuid:802ff3d8-b8da-423f-8a02-7b2288485edd",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:38499704-81f7-4d47-965f-435e0b7b0850",
                "orientation": "+"
              },
              {
                "ref": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
                "orientation": "-"
              },
              {
                "ref": "uuid:b6e30631-9768-4020-8947-c32137328216",
                "orientation": "-"
              },
              {
                "ref": "uuid:fb03276b-4250-4d52-81e1-035a0bd92895",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          3.609557097661e-16,
          -1.0,
          0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:16c13b7b-aeda-4130-a793-d63f62bcc75b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4",
                "orientation": "+"
              },
              {
                "ref": "uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa",
                "orientation": "+"
              },
              {
                "ref": "uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda",
                "orientation": "+"
              },
              {
                "ref": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
                "orientation": "-"
              },
              {
                "ref": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:786e8738-1690-426d-8e2f-f5e734336a67",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724",
                "orientation": "-"
              },
              {
                "ref": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
                "orientation": "+"
              },
              {
                "ref": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
                "orientation": "+"
              },
              {
                "ref": "uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1",
                "orientation": "-"
              },
              {
                "ref": "uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 12.0
      }
    }
  ],
  "solids": [
    {
      "id": "uuid:758590d2-8cc6-4ff7-8fcc-d7ecd01b3498",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Solid",
        "shells": [
          {
            "type": "Shell",
            "directed_references": [
              {
                "ref": "uuid:4ac3b91b-eeb7-428c-b5e9-7e8a3f0998ae",
                "orientation": "+"
              },
              {
                "ref": "uuid:4a294022-4864-49c7-8cee-f9e43360bc4e",
                "orientation": "+"
              },
              {
                "ref": "uuid:01947f47-ee13-44a9-85a4-2bcb4881982a",
                "orientation": "+"
              },
              {
                "ref": "uuid:607a3363-3eb7-4ce6-a633-86d2e565692b",
                "orientation": "+"
              },
              {
                "ref": "uuid:3c1f5c4b-d842-40b6-a332-99d50015fa8f",
                "orientation": "+"
              },
              {
                "ref": "uuid:fe522919-1421-4fd1-9930-8c6551e3f2a5",
                "orientation": "+"
              },
              {
                "ref": "uuid:2387ae98-9236-42fe-9414-c45b99954c41",
                "orientation": "+"
              },
              {
                "ref": "uuid:4ba85faa-3935-4e89-a9f8-dcd647a5dbed",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "name": "Upper East",
        "levels": [
          2
        ],
        "volume": 168.0
      }
    }
  ]
}
```

#### jsonld
```jsonld
{
  "@context": "https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-multi-collection/context.jsonld",
  "type": "FeatureCollection",
  "features": [],
  "metadata": {
    "units": "meters",
    "coordinate_precision": 3,
    "conversion_factor": 0.0254
  },
  "points": [
    {
      "type": "FeatureCollection",
      "features": [
        {
          "id": "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:fad324b9-801f-40f4-b65b-91f8753e9698",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              6.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              6.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              6.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              6.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:e7300a01-f8c1-4351-9511-02790a5376b0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:307b7db6-8014-4628-b80e-ff925bf71168",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:caa6045e-4189-4571-8914-1189e51ac71e",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              6.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              6.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              10.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              10.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:206806a4-a2f8-4c04-858e-99d289858a40",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              6.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              6.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:793997c5-bcc4-4610-984b-6cf2c2997348",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8e503e04-ad51-423b-8102-708a845189b6",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              10.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              6.0,
              0.0
            ]
          },
          "properties": null
        }
      ]
    }
  ],
  "edges": [
    {
      "id": "uuid:c60507ba-226b-4e49-a702-e9afef899b23",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0",
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698",
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:8582d9c2-6053-495a-8413-f5493691c0de",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071",
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3",
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3",
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70",
          "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8",
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:7da1c2fe-f798-43cc-af44-ac63f968139c",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3",
          "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:745aa367-94b6-4949-a856-5271ec6672e9",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0",
          "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:f921656a-58e3-4375-bdff-ac8019f524cf",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd",
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0",
          "uuid:307b7db6-8014-4628-b80e-ff925bf71168"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6",
          "uuid:307b7db6-8014-4628-b80e-ff925bf71168"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6",
          "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:307b7db6-8014-4628-b80e-ff925bf71168",
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:fb03276b-4250-4d52-81e1-035a0bd92895",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d",
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:af347f25-a547-477c-b246-cb810756d4dc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "uuid:caa6045e-4189-4571-8914-1189e51ac71e"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:caa6045e-4189-4571-8914-1189e51ac71e",
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:caa6045e-4189-4571-8914-1189e51ac71e",
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:242a8400-a076-4817-86c6-acd56087cec6",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:4ad210b7-5de5-4732-af7c-978de28f988b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6",
          "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9",
          "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:4406e3f5-89dc-463b-84e4-487490f71f1a",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d",
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:511c6e7d-728b-4f1f-9763-9461eb628586",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4",
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9",
          "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:06babc8d-f0d6-43eb-bfad-931055bae084",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51",
          "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:fc877bbe-72a8-4e59-b959-010e6660984a",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09",
          "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:aafd209b-cd13-401a-83f5-26751a02cffe",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51",
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:9238cbda-d019-4b57-8319-0cc355656802",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:91cdc345-f745-4643-bc88-a24f8e2216b0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:206806a4-a2f8-4c04-858e-99d289858a40",
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a",
          "uuid:206806a4-a2f8-4c04-858e-99d289858a40"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:61f99921-a94d-4e0d-8353-f027d76227c5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:474fef44-eb6e-4e19-a871-433f9bac5650",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3",
          "uuid:206806a4-a2f8-4c04-858e-99d289858a40"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717",
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:71af0dde-7fc9-4290-9624-119e91f422ea",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348",
          "uuid:8e503e04-ad51-423b-8102-708a845189b6"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:ad13a84c-df97-4b75-9dc1-1ce452249964",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8e503e04-ad51-423b-8102-708a845189b6",
          "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:c2a00070-f12b-42f9-b78c-b33daa500873",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606",
          "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:13dd8184-f73e-4d9f-9977-3e573274fccc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8e503e04-ad51-423b-8102-708a845189b6",
          "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606",
          "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:ed666061-98c5-439d-ab0d-5a792437a873",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:5a36c75b-053b-4d7b-b512-6777786d6180",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1",
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348",
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0",
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0",
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:a604828d-a36b-4fac-ba6f-6160ade95301",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4",
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:38499704-81f7-4d47-965f-435e0b7b0850",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d",
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:b6e30631-9768-4020-8947-c32137328216",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3"
        ]
      },
      "properties": {
        "length": 4.0
      }
    }
  ],
  "faces": [
    {
      "id": "uuid:4ac3b91b-eeb7-428c-b5e9-7e8a3f0998ae",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:c60507ba-226b-4e49-a702-e9afef899b23",
                "orientation": "+"
              },
              {
                "ref": "uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac",
                "orientation": "+"
              },
              {
                "ref": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
                "orientation": "+"
              },
              {
                "ref": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          1.0,
          0.0,
          -0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:4a294022-4864-49c7-8cee-f9e43360bc4e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
                "orientation": "+"
              },
              {
                "ref": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
                "orientation": "-"
              },
              {
                "ref": "uuid:8582d9c2-6053-495a-8413-f5493691c0de",
                "orientation": "+"
              },
              {
                "ref": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          3.007964248051e-16
        ],
        "area": 18.0
      }
    },
    {
      "id": "uuid:01947f47-ee13-44a9-85a4-2bcb4881982a",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555",
                "orientation": "+"
              },
              {
                "ref": "uuid:c60507ba-226b-4e49-a702-e9afef899b23",
                "orientation": "-"
              },
              {
                "ref": "uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81",
                "orientation": "+"
              },
              {
                "ref": "uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:607a3363-3eb7-4ce6-a633-86d2e565692b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:8582d9c2-6053-495a-8413-f5493691c0de",
                "orientation": "-"
              },
              {
                "ref": "uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac",
                "orientation": "-"
              },
              {
                "ref": "uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555",
                "orientation": "-"
              },
              {
                "ref": "uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0",
                "orientation": "+"
              },
              {
                "ref": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
                "orientation": "+"
              },
              {
                "ref": "uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 56.0
      }
    },
    {
      "id": "uuid:3c1f5c4b-d842-40b6-a332-99d50015fa8f",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
                "orientation": "+"
              },
              {
                "ref": "uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5",
                "orientation": "+"
              },
              {
                "ref": "uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0",
                "orientation": "-"
              },
              {
                "ref": "uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:fe522919-1421-4fd1-9930-8c6551e3f2a5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:7da1c2fe-f798-43cc-af44-ac63f968139c",
                "orientation": "+"
              },
              {
                "ref": "uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1",
                "orientation": "+"
              },
              {
                "ref": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
                "orientation": "-"
              },
              {
                "ref": "uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 6.0
      }
    },
    {
      "id": "uuid:2387ae98-9236-42fe-9414-c45b99954c41",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6",
                "orientation": "+"
              },
              {
                "ref": "uuid:7da1c2fe-f798-43cc-af44-ac63f968139c",
                "orientation": "-"
              },
              {
                "ref": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
                "orientation": "-"
              },
              {
                "ref": "uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81",
                "orientation": "-"
              },
              {
                "ref": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
                "orientation": "-"
              },
              {
                "ref": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          -1.0
        ],
        "area": 56.0
      }
    },
    {
      "id": "uuid:4ba85faa-3935-4e89-a9f8-dcd647a5dbed",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6",
                "orientation": "-"
              },
              {
                "ref": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
                "orientation": "-"
              },
              {
                "ref": "uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5",
                "orientation": "-"
              },
              {
                "ref": "uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:c55c88db-d187-4d7e-9aaa-b9d3dce52663",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d",
                "orientation": "+"
              },
              {
                "ref": "uuid:745aa367-94b6-4949-a856-5271ec6672e9",
                "orientation": "+"
              },
              {
                "ref": "uuid:f921656a-58e3-4375-bdff-ac8019f524cf",
                "orientation": "+"
              },
              {
                "ref": "uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:dbd99467-ea83-4dff-b03f-eef2aad2687c",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:745aa367-94b6-4949-a856-5271ec6672e9",
                "orientation": "-"
              },
              {
                "ref": "uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24",
                "orientation": "+"
              },
              {
                "ref": "uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3",
                "orientation": "-"
              },
              {
                "ref": "uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -3.007964248051e-16
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:0e55e87d-8475-4c92-89e7-d62f97ce9ec2",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3",
                "orientation": "+"
              },
              {
                "ref": "uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78",
                "orientation": "+"
              },
              {
                "ref": "uuid:fb03276b-4250-4d52-81e1-035a0bd92895",
                "orientation": "+"
              },
              {
                "ref": "uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 18.0
      }
    },
    {
      "id": "uuid:6a5ff199-56a7-4e65-94b5-bfdf2ae3449d",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:f921656a-58e3-4375-bdff-ac8019f524cf",
                "orientation": "-"
              },
              {
                "ref": "uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05",
                "orientation": "-"
              },
              {
                "ref": "uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf",
                "orientation": "-"
              },
              {
                "ref": "uuid:af347f25-a547-477c-b246-cb810756d4dc",
                "orientation": "+"
              },
              {
                "ref": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
                "orientation": "+"
              },
              {
                "ref": "uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 56.0
      }
    },
    {
      "id": "uuid:e499fea3-19f7-4863-8a58-751caff7d884",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3",
                "orientation": "+"
              },
              {
                "ref": "uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5",
                "orientation": "+"
              },
              {
                "ref": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
                "orientation": "-"
              },
              {
                "ref": "uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 6.0
      }
    },
    {
      "id": "uuid:9e4c0c0e-6acf-401b-b35e-0e917ce3a5fc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:242a8400-a076-4817-86c6-acd56087cec6",
                "orientation": "+"
              },
              {
                "ref": "uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78",
                "orientation": "-"
              },
              {
                "ref": "uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24",
                "orientation": "-"
              },
              {
                "ref": "uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d",
                "orientation": "-"
              },
              {
                "ref": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
                "orientation": "+"
              },
              {
                "ref": "uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          -1.0
        ],
        "area": 56.0
      }
    },
    {
      "id": "uuid:3f5c452f-9815-4b21-9b2d-0127ae80c385",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:242a8400-a076-4817-86c6-acd56087cec6",
                "orientation": "-"
              },
              {
                "ref": "uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724",
                "orientation": "-"
              },
              {
                "ref": "uuid:af347f25-a547-477c-b246-cb810756d4dc",
                "orientation": "-"
              },
              {
                "ref": "uuid:fb03276b-4250-4d52-81e1-035a0bd92895",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          1.0,
          0.0,
          -0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:66a430c0-123f-42df-9d11-64347362bcb3",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:4ad210b7-5de5-4732-af7c-978de28f988b",
                "orientation": "+"
              },
              {
                "ref": "uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e",
                "orientation": "+"
              },
              {
                "ref": "uuid:4406e3f5-89dc-463b-84e4-487490f71f1a",
                "orientation": "+"
              },
              {
                "ref": "uuid:511c6e7d-728b-4f1f-9763-9461eb628586",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:31d8f2b5-cc74-4f72-b230-d27dad0fd589",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc",
                "orientation": "+"
              },
              {
                "ref": "uuid:06babc8d-f0d6-43eb-bfad-931055bae084",
                "orientation": "+"
              },
              {
                "ref": "uuid:fc877bbe-72a8-4e59-b959-010e6660984a",
                "orientation": "+"
              },
              {
                "ref": "uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          1.0,
          0.0,
          -0.0
        ],
        "area": 30.0
      }
    },
    {
      "id": "uuid:65959e29-11cb-4568-904d-61c4a7c17b98",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:aafd209b-cd13-401a-83f5-26751a02cffe",
                "orientation": "+"
              },
              {
                "ref": "uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03",
                "orientation": "+"
              },
              {
                "ref": "uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81",
                "orientation": "-"
              },
              {
                "ref": "uuid:9238cbda-d019-4b57-8319-0cc355656802",
                "orientation": "+"
              },
              {
                "ref": "uuid:06babc8d-f0d6-43eb-bfad-931055bae084",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 30.0
      }
    },
    {
      "id": "uuid:e2efe498-c6d5-4f9c-ac07-4c1c9e406675",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
                "orientation": "-"
              },
              {
                "ref": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
                "orientation": "-"
              },
              {
                "ref": "uuid:91cdc345-f745-4643-bc88-a24f8e2216b0",
                "orientation": "+"
              },
              {
                "ref": "uuid:4406e3f5-89dc-463b-84e4-487490f71f1a",
                "orientation": "-"
              },
              {
                "ref": "uuid:fc877bbe-72a8-4e59-b959-010e6660984a",
                "orientation": "-"
              },
              {
                "ref": "uuid:9238cbda-d019-4b57-8319-0cc355656802",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 32.0
      }
    },
    {
      "id": "uuid:5bcee2b5-be9b-47d6-9a8b-35dac021f661",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:4ad210b7-5de5-4732-af7c-978de28f988b",
                "orientation": "-"
              },
              {
                "ref": "uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4",
                "orientation": "-"
              },
              {
                "ref": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
                "orientation": "-"
              },
              {
                "ref": "uuid:61f99921-a94d-4e0d-8353-f027d76227c5",
                "orientation": "-"
              },
              {
                "ref": "uuid:aafd209b-cd13-401a-83f5-26751a02cffe",
                "orientation": "-"
              },
              {
                "ref": "uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -0.0,
          -0.0,
          -1.0
        ],
        "area": 88.0
      }
    },
    {
      "id": "uuid:91ce0c52-11c3-4e32-8bcc-dea958a3969e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:474fef44-eb6e-4e19-a871-433f9bac5650",
                "orientation": "-"
              },
              {
                "ref": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
                "orientation": "-"
              },
              {
                "ref": "uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03",
                "orientation": "-"
              },
              {
                "ref": "uuid:61f99921-a94d-4e0d-8353-f027d76227c5",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:56283886-1f4c-448c-b785-80fb9740a9cc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda",
                "orientation": "+"
              },
              {
                "ref": "uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4",
                "orientation": "+"
              },
              {
                "ref": "uuid:511c6e7d-728b-4f1f-9763-9461eb628586",
                "orientation": "-"
              },
              {
                "ref": "uuid:91cdc345-f745-4643-bc88-a24f8e2216b0",
                "orientation": "-"
              },
              {
                "ref": "uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -0.0
        ],
        "area": 18.0
      }
    },
    {
      "id": "uuid:f3338301-b0e3-401c-af23-41ac2ae8e969",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda",
                "orientation": "-"
              },
              {
                "ref": "uuid:7da1c2fe-f798-43cc-af44-ac63f968139c",
                "orientation": "-"
              },
              {
                "ref": "uuid:474fef44-eb6e-4e19-a871-433f9bac5650",
                "orientation": "+"
              },
              {
                "ref": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 6.0
      }
    },
    {
      "id": "uuid:a2117d6b-4621-4a6b-9809-9fab3dfc4ff0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0",
                "orientation": "+"
              },
              {
                "ref": "uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985",
                "orientation": "+"
              },
              {
                "ref": "uuid:71af0dde-7fc9-4290-9624-119e91f422ea",
                "orientation": "+"
              },
              {
                "ref": "uuid:ad13a84c-df97-4b75-9dc1-1ce452249964",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:9d67557a-e130-4a47-b63d-c6a2bdf21fa2",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:c2a00070-f12b-42f9-b78c-b33daa500873",
                "orientation": "+"
              },
              {
                "ref": "uuid:ad13a84c-df97-4b75-9dc1-1ce452249964",
                "orientation": "-"
              },
              {
                "ref": "uuid:13dd8184-f73e-4d9f-9977-3e573274fccc",
                "orientation": "+"
              },
              {
                "ref": "uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -0.0
        ],
        "area": 30.0
      }
    },
    {
      "id": "uuid:d45fca44-8685-4146-92a5-b84d82fdc838",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:ed666061-98c5-439d-ab0d-5a792437a873",
                "orientation": "+"
              },
              {
                "ref": "uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f",
                "orientation": "+"
              },
              {
                "ref": "uuid:5a36c75b-053b-4d7b-b512-6777786d6180",
                "orientation": "+"
              },
              {
                "ref": "uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d",
                "orientation": "-"
              },
              {
                "ref": "uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 30.0
      }
    },
    {
      "id": "uuid:2497a842-0932-4fe5-ac1a-2f773473f338",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0",
                "orientation": "+"
              },
              {
                "ref": "uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78",
                "orientation": "-"
              },
              {
                "ref": "uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24",
                "orientation": "-"
              },
              {
                "ref": "uuid:5a36c75b-053b-4d7b-b512-6777786d6180",
                "orientation": "-"
              },
              {
                "ref": "uuid:13dd8184-f73e-4d9f-9977-3e573274fccc",
                "orientation": "-"
              },
              {
                "ref": "uuid:71af0dde-7fc9-4290-9624-119e91f422ea",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 32.0
      }
    },
    {
      "id": "uuid:04ea47e9-b4dd-4bed-a8f4-4802d1735c74",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:ed666061-98c5-439d-ab0d-5a792437a873",
                "orientation": "-"
              },
              {
                "ref": "uuid:61f99921-a94d-4e0d-8353-f027d76227c5",
                "orientation": "+"
              },
              {
                "ref": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
                "orientation": "-"
              },
              {
                "ref": "uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635",
                "orientation": "-"
              },
              {
                "ref": "uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0",
                "orientation": "-"
              },
              {
                "ref": "uuid:c2a00070-f12b-42f9-b78c-b33daa500873",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -0.0,
          -0.0,
          -1.0
        ],
        "area": 88.0
      }
    },
    {
      "id": "uuid:b5fd960f-0d14-4257-9182-40de738a7e50",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4",
                "orientation": "+"
              },
              {
                "ref": "uuid:242a8400-a076-4817-86c6-acd56087cec6",
                "orientation": "+"
              },
              {
                "ref": "uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0",
                "orientation": "-"
              },
              {
                "ref": "uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985",
                "orientation": "-"
              },
              {
                "ref": "uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          1.0,
          0.0,
          -0.0
        ],
        "area": 18.0
      }
    },
    {
      "id": "uuid:e119b096-e589-49bd-b1db-a1182dc2dade",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:474fef44-eb6e-4e19-a871-433f9bac5650",
                "orientation": "-"
              },
              {
                "ref": "uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3",
                "orientation": "-"
              },
              {
                "ref": "uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4",
                "orientation": "-"
              },
              {
                "ref": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 6.0
      }
    },
    {
      "id": "uuid:67842d3a-7c79-4f2a-8630-744711071e93",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:a604828d-a36b-4fac-ba6f-6160ade95301",
                "orientation": "-"
              },
              {
                "ref": "uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635",
                "orientation": "+"
              },
              {
                "ref": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
                "orientation": "+"
              },
              {
                "ref": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
                "orientation": "+"
              },
              {
                "ref": "uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -0.0,
          -0.0,
          -1.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:f1c1a636-d6ab-414c-a0aa-855fc7e85e1f",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280",
                "orientation": "+"
              },
              {
                "ref": "uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985",
                "orientation": "-"
              },
              {
                "ref": "uuid:a604828d-a36b-4fac-ba6f-6160ade95301",
                "orientation": "+"
              },
              {
                "ref": "uuid:511c6e7d-728b-4f1f-9763-9461eb628586",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:a22a6c54-306e-44bc-9b94-6c32c705e63e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280",
                "orientation": "-"
              },
              {
                "ref": "uuid:91cdc345-f745-4643-bc88-a24f8e2216b0",
                "orientation": "-"
              },
              {
                "ref": "uuid:38499704-81f7-4d47-965f-435e0b7b0850",
                "orientation": "-"
              },
              {
                "ref": "uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 8.0
      }
    },
    {
      "id": "uuid:9ed21e0a-b062-4000-88e2-50bd9153e417",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:b6e30631-9768-4020-8947-c32137328216",
                "orientation": "+"
              },
              {
                "ref": "uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5",
                "orientation": "-"
              },
              {
                "ref": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
                "orientation": "-"
              },
              {
                "ref": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
                "orientation": "-"
              },
              {
                "ref": "uuid:af347f25-a547-477c-b246-cb810756d4dc",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 16.0
      }
    },
    {
      "id": "uuid:802ff3d8-b8da-423f-8a02-7b2288485edd",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:38499704-81f7-4d47-965f-435e0b7b0850",
                "orientation": "+"
              },
              {
                "ref": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
                "orientation": "-"
              },
              {
                "ref": "uuid:b6e30631-9768-4020-8947-c32137328216",
                "orientation": "-"
              },
              {
                "ref": "uuid:fb03276b-4250-4d52-81e1-035a0bd92895",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          3.609557097661e-16,
          -1.0,
          0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:16c13b7b-aeda-4130-a793-d63f62bcc75b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4",
                "orientation": "+"
              },
              {
                "ref": "uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa",
                "orientation": "+"
              },
              {
                "ref": "uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda",
                "orientation": "+"
              },
              {
                "ref": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
                "orientation": "-"
              },
              {
                "ref": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:786e8738-1690-426d-8e2f-f5e734336a67",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724",
                "orientation": "-"
              },
              {
                "ref": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
                "orientation": "+"
              },
              {
                "ref": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
                "orientation": "+"
              },
              {
                "ref": "uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1",
                "orientation": "-"
              },
              {
                "ref": "uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 12.0
      }
    }
  ],
  "solids": [
    {
      "id": "uuid:758590d2-8cc6-4ff7-8fcc-d7ecd01b3498",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Solid",
        "shells": [
          {
            "type": "Shell",
            "directed_references": [
              {
                "ref": "uuid:4ac3b91b-eeb7-428c-b5e9-7e8a3f0998ae",
                "orientation": "+"
              },
              {
                "ref": "uuid:4a294022-4864-49c7-8cee-f9e43360bc4e",
                "orientation": "+"
              },
              {
                "ref": "uuid:01947f47-ee13-44a9-85a4-2bcb4881982a",
                "orientation": "+"
              },
              {
                "ref": "uuid:607a3363-3eb7-4ce6-a633-86d2e565692b",
                "orientation": "+"
              },
              {
                "ref": "uuid:3c1f5c4b-d842-40b6-a332-99d50015fa8f",
                "orientation": "+"
              },
              {
                "ref": "uuid:fe522919-1421-4fd1-9930-8c6551e3f2a5",
                "orientation": "+"
              },
              {
                "ref": "uuid:2387ae98-9236-42fe-9414-c45b99954c41",
                "orientation": "+"
              },
              {
                "ref": "uuid:4ba85faa-3935-4e89-a9f8-dcd647a5dbed",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "name": "Upper East",
        "levels": [
          2
        ],
        "volume": 168.0
      }
    }
  ]
}
```

#### ttl
```ttl
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix topo: <https://purl.org/geojson/topo#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<uuid:06babc8d-f0d6-43eb-bfad-931055bae084> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:20d3c864-4a8c-4440-b600-a1d424e92f51> <uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09> ) ] .

<uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:307b7db6-8014-4628-b80e-ff925bf71168> <uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d> ) ] .

<uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:11caaac5-b631-4bd8-a6af-f82cb6371071> <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> ) ] .

<uuid:13dd8184-f73e-4d9f-9977-3e573274fccc> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:8e503e04-ad51-423b-8102-708a845189b6> <uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1> ) ] .

<uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:caa6045e-4189-4571-8914-1189e51ac71e> <uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70> ) ] .

<uuid:242a8400-a076-4817-86c6-acd56087cec6> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e> <uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d> ) ] .

<uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e> <uuid:22138e52-65ef-4773-b69d-5ea2628fad7b> ) ] .

<uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> <uuid:fad324b9-801f-40f4-b65b-91f8753e9698> ) ] .

<uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0> <uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a> ) ] .

<uuid:38499704-81f7-4d47-965f-435e0b7b0850> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d> <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> ) ] .

<uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:22138e52-65ef-4773-b69d-5ea2628fad7b> <uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3> ) ] .

<uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717> <uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df> ) ] .

<uuid:4406e3f5-89dc-463b-84e4-487490f71f1a> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:c060c1dc-6544-4595-b583-72ecf603fd6d> <uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4> ) ] .

<uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3> <uuid:8087116e-84cc-44d1-8047-78dc3837d7e8> ) ] .

<uuid:474fef44-eb6e-4e19-a871-433f9bac5650> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:f34d9f2e-4180-41de-a613-46f78f4c178f> <uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a> ) ] .

<uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df> <uuid:793997c5-bcc4-4610-984b-6cf2c2997348> ) ] .

<uuid:4ad210b7-5de5-4732-af7c-978de28f988b> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6> <uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9> ) ] .

<uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3> <uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0> ) ] .

<uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4> <uuid:793997c5-bcc4-4610-984b-6cf2c2997348> ) ] .

<uuid:511c6e7d-728b-4f1f-9763-9461eb628586> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4> <uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6> ) ] .

<uuid:5a36c75b-053b-4d7b-b512-6777786d6180> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1> <uuid:e7300a01-f8c1-4351-9511-02790a5376b0> ) ] .

<uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:f34d9f2e-4180-41de-a613-46f78f4c178f> <uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70> ) ] .

<uuid:61f99921-a94d-4e0d-8353-f027d76227c5> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e> <uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a> ) ] .

<uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a> <uuid:206806a4-a2f8-4c04-858e-99d289858a40> ) ] .

<uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:e7300a01-f8c1-4351-9511-02790a5376b0> <uuid:307b7db6-8014-4628-b80e-ff925bf71168> ) ] .

<uuid:71af0dde-7fc9-4290-9624-119e91f422ea> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:793997c5-bcc4-4610-984b-6cf2c2997348> <uuid:8e503e04-ad51-423b-8102-708a845189b6> ) ] .

<uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ca62577e-8e24-4af2-88bf-33b34e25e606> <uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1> ) ] .

<uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3> <uuid:206806a4-a2f8-4c04-858e-99d289858a40> ) ] .

<uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70> <uuid:8087116e-84cc-44d1-8047-78dc3837d7e8> ) ] .

<uuid:745aa367-94b6-4949-a856-5271ec6672e9> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:e7300a01-f8c1-4351-9511-02790a5376b0> <uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd> ) ] .

<uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9> <uuid:20d3c864-4a8c-4440-b600-a1d424e92f51> ) ] .

<uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:8087116e-84cc-44d1-8047-78dc3837d7e8> <uuid:11caaac5-b631-4bd8-a6af-f82cb6371071> ) ] .

<uuid:7da1c2fe-f798-43cc-af44-ac63f968139c> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:f34d9f2e-4180-41de-a613-46f78f4c178f> <uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3> ) ] .

<uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0> <uuid:c611f840-2829-44b2-b367-3915ca7875a4> ) ] .

<uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> <uuid:22138e52-65ef-4773-b69d-5ea2628fad7b> ) ] .

<uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:c611f840-2829-44b2-b367-3915ca7875a4> <uuid:fad324b9-801f-40f4-b65b-91f8753e9698> ) ] .

<uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> <uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3> ) ] .

<uuid:8582d9c2-6053-495a-8413-f5493691c0de> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:c611f840-2829-44b2-b367-3915ca7875a4> <uuid:11caaac5-b631-4bd8-a6af-f82cb6371071> ) ] .

<uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:caa6045e-4189-4571-8914-1189e51ac71e> <uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e> ) ] .

<uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e> <uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3> ) ] .

<uuid:91cdc345-f745-4643-bc88-a24f8e2216b0> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> <uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4> ) ] .

<uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3> <uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70> ) ] .

<uuid:9238cbda-d019-4b57-8319-0cc355656802> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> <uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09> ) ] .

<uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:22138e52-65ef-4773-b69d-5ea2628fad7b> <uuid:e7300a01-f8c1-4351-9511-02790a5376b0> ) ] .

<uuid:a604828d-a36b-4fac-ba6f-6160ade95301> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df> <uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6> ) ] .

<uuid:aafd209b-cd13-401a-83f5-26751a02cffe> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:20d3c864-4a8c-4440-b600-a1d424e92f51> <uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e> ) ] .

<uuid:ad13a84c-df97-4b75-9dc1-1ce452249964> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:8e503e04-ad51-423b-8102-708a845189b6> <uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717> ) ] .

<uuid:af347f25-a547-477c-b246-cb810756d4dc> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9> <uuid:caa6045e-4189-4571-8914-1189e51ac71e> ) ] .

<uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:793997c5-bcc4-4610-984b-6cf2c2997348> <uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d> ) ] .

<uuid:b6e30631-9768-4020-8947-c32137328216> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9> <uuid:11caaac5-b631-4bd8-a6af-f82cb6371071> ) ] .

<uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9> <uuid:c060c1dc-6544-4595-b583-72ecf603fd6d> ) ] .

<uuid:c2a00070-f12b-42f9-b78c-b33daa500873> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ca62577e-8e24-4af2-88bf-33b34e25e606> <uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717> ) ] .

<uuid:c60507ba-226b-4e49-a702-e9afef899b23> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> <uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0> ) ] .

<uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9> <uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6> ) ] .

<uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:fad324b9-801f-40f4-b65b-91f8753e9698> <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> ) ] .

<uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6> <uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd> ) ] .

<uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df> <uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0> ) ] .

<uuid:ed666061-98c5-439d-ab0d-5a792437a873> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e> <uuid:ca62577e-8e24-4af2-88bf-33b34e25e606> ) ] .

<uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:22138e52-65ef-4773-b69d-5ea2628fad7b> <uuid:f34d9f2e-4180-41de-a613-46f78f4c178f> ) ] .

<uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0> <uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e> ) ] .

<uuid:f921656a-58e3-4375-bdff-ac8019f524cf> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd> <uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3> ) ] .

<uuid:fb03276b-4250-4d52-81e1-035a0bd92895> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d> <uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9> ) ] .

<uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6> <uuid:307b7db6-8014-4628-b80e-ff925bf71168> ) ] .

<uuid:fc877bbe-72a8-4e59-b959-010e6660984a> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09> <uuid:c060c1dc-6544-4595-b583-72ecf603fd6d> ) ] .

<uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e> <uuid:f34d9f2e-4180-41de-a613-46f78f4c178f> ) ] .

<uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:206806a4-a2f8-4c04-858e-99d289858a40> <uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6> ) ] .

<uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+00 1e+01 6e+00 ) ] .

<uuid:206806a4-a2f8-4c04-858e-99d289858a40> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 6e+00 0e+00 ) ] .

<uuid:20d3c864-4a8c-4440-b600-a1d424e92f51> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+01 1e+01 0e+00 ) ] .

<uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+01 1e+01 3e+00 ) ] .

<uuid:307b7db6-8014-4628-b80e-ff925bf71168> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+00 2e+00 3e+00 ) ] .

<uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+00 2e+00 6e+00 ) ] .

<uuid:8087116e-84cc-44d1-8047-78dc3837d7e8> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 6e+00 6e+00 ) ] .

<uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 0e+00 1e+01 3e+00 ) ] .

<uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 1e+01 6e+00 ) ] .

<uuid:8e503e04-ad51-423b-8102-708a845189b6> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 0e+00 0e+00 3e+00 ) ] .

<uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+01 0e+00 0e+00 ) ] .

<uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 6e+00 0e+00 ) ] .

<uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 0e+00 0e+00 0e+00 ) ] .

<uuid:c060c1dc-6544-4595-b583-72ecf603fd6d> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+01 0e+00 3e+00 ) ] .

<uuid:c611f840-2829-44b2-b367-3915ca7875a4> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 2e+00 6e+00 ) ] .

<uuid:ca62577e-8e24-4af2-88bf-33b34e25e606> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 0e+00 1e+01 0e+00 ) ] .

<uuid:caa6045e-4189-4571-8914-1189e51ac71e> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 6e+00 6e+00 ) ] .

<uuid:fad324b9-801f-40f4-b65b-91f8753e9698> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 2e+00 3e+00 ) ] .

<uuid:11caaac5-b631-4bd8-a6af-f82cb6371071> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 2e+00 6e+00 ) ] .

<uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1e+01 1e+01 0e+00 ) ] .

<uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1e+01 1e+01 6e+00 ) ] .

<uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1e+01 6e+00 6e+00 ) ] .

<uuid:793997c5-bcc4-4610-984b-6cf2c2997348> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 0e+00 3e+00 ) ] .

<uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 0e+00 3e+00 ) ] .

<uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 2e+00 6e+00 ) ] .

<uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 0e+00 0e+00 ) ] .

<uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 1e+01 3e+00 ) ] .

<uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1e+01 6e+00 0e+00 ) ] .

<uuid:e7300a01-f8c1-4351-9511-02790a5376b0> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+00 1e+01 3e+00 ) ] .

<uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 0e+00 0e+00 ) ] .

<uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 6e+00 3e+00 ) ] .

<uuid:22138e52-65ef-4773-b69d-5ea2628fad7b> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1e+01 1e+01 3e+00 ) ] .

<uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 6e+00 3e+00 ) ] .

<uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 2e+00 3e+00 ) ] .

<uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 2e+00 3e+00 ) ] .

<uuid:f34d9f2e-4180-41de-a613-46f78f4c178f> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1e+01 6e+00 3e+00 ) ] .

[] a geojson:FeatureCollection ;
    topo:edges ( <uuid:c60507ba-226b-4e49-a702-e9afef899b23> <uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac> <uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569> <uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8> <uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b> <uuid:8582d9c2-6053-495a-8413-f5493691c0de> <uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add> <uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555> <uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81> <uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03> <uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0> <uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d> <uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5> <uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7> <uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5> <uuid:7da1c2fe-f798-43cc-af44-ac63f968139c> <uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1> <uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6> <uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d> <uuid:745aa367-94b6-4949-a856-5271ec6672e9> <uuid:f921656a-58e3-4375-bdff-ac8019f524cf> <uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24> <uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3> <uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05> <uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78> <uuid:fb03276b-4250-4d52-81e1-035a0bd92895> <uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf> <uuid:af347f25-a547-477c-b246-cb810756d4dc> <uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b> <uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3> <uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724> <uuid:242a8400-a076-4817-86c6-acd56087cec6> <uuid:4ad210b7-5de5-4732-af7c-978de28f988b> <uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e> <uuid:4406e3f5-89dc-463b-84e4-487490f71f1a> <uuid:511c6e7d-728b-4f1f-9763-9461eb628586> <uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc> <uuid:06babc8d-f0d6-43eb-bfad-931055bae084> <uuid:fc877bbe-72a8-4e59-b959-010e6660984a> <uuid:aafd209b-cd13-401a-83f5-26751a02cffe> <uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03> <uuid:9238cbda-d019-4b57-8319-0cc355656802> <uuid:91cdc345-f745-4643-bc88-a24f8e2216b0> <uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4> <uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94> <uuid:61f99921-a94d-4e0d-8353-f027d76227c5> <uuid:474fef44-eb6e-4e19-a871-433f9bac5650> <uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda> <uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0> <uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985> <uuid:71af0dde-7fc9-4290-9624-119e91f422ea> <uuid:ad13a84c-df97-4b75-9dc1-1ce452249964> <uuid:c2a00070-f12b-42f9-b78c-b33daa500873> <uuid:13dd8184-f73e-4d9f-9977-3e573274fccc> <uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f> <uuid:ed666061-98c5-439d-ab0d-5a792437a873> <uuid:5a36c75b-053b-4d7b-b512-6777786d6180> <uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0> <uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17> <uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635> <uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4> <uuid:a604828d-a36b-4fac-ba6f-6160ade95301> <uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280> <uuid:38499704-81f7-4d47-965f-435e0b7b0850> <uuid:b6e30631-9768-4020-8947-c32137328216> <uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa> ) ;
    topo:faces ( [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] ) ;
    topo:points ( [ a geojson:FeatureCollection ;
                geojson:features <uuid:11caaac5-b631-4bd8-a6af-f82cb6371071>,
                    <uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e>,
                    <uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e>,
                    <uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd>,
                    <uuid:206806a4-a2f8-4c04-858e-99d289858a40>,
                    <uuid:20d3c864-4a8c-4440-b600-a1d424e92f51>,
                    <uuid:22138e52-65ef-4773-b69d-5ea2628fad7b>,
                    <uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09>,
                    <uuid:307b7db6-8014-4628-b80e-ff925bf71168>,
                    <uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6>,
                    <uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3>,
                    <uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70>,
                    <uuid:793997c5-bcc4-4610-984b-6cf2c2997348>,
                    <uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4>,
                    <uuid:8087116e-84cc-44d1-8047-78dc3837d7e8>,
                    <uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3>,
                    <uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1>,
                    <uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0>,
                    <uuid:8e503e04-ad51-423b-8102-708a845189b6>,
                    <uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9>,
                    <uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9>,
                    <uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0>,
                    <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d>,
                    <uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df>,
                    <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38>,
                    <uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717>,
                    <uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d>,
                    <uuid:c060c1dc-6544-4595-b583-72ecf603fd6d>,
                    <uuid:c611f840-2829-44b2-b367-3915ca7875a4>,
                    <uuid:ca62577e-8e24-4af2-88bf-33b34e25e606>,
                    <uuid:caa6045e-4189-4571-8914-1189e51ac71e>,
                    <uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a>,
                    <uuid:e7300a01-f8c1-4351-9511-02790a5376b0>,
                    <uuid:f34d9f2e-4180-41de-a613-46f78f4c178f>,
                    <uuid:fad324b9-801f-40f4-b65b-91f8753e9698>,
                    <uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6> ] ) ;
    topo:shells ( [ a geojson:Feature ] ) .


```


### Complete 2D Sections Topology (all feature types)
The full 2D sections topology dataset derived from a building floor plan,
expressed in the multi-collection model. All geometry is null except on Point features;
topology is encoded via references and directed_references. Contains:
- 36 point features (3D coordinate geometry nodes)
- 66 edge features (LineString topology via references to point IDs)
- 37 face features (Face topology via rings of directed_references to Edge IDs)
- 5 solid features (Solid topology via shells of directed_references to Face IDs)

#### json
```json
{
  "type": "FeatureCollection",
  "metadata": {
    "units": "meters",
    "coordinate_precision": 3,
    "conversion_factor": 0.0254
  },
  "points": [
    {
      "type": "FeatureCollection",
      "features": [
        {
          "id": "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:fad324b9-801f-40f4-b65b-91f8753e9698",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              6.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              6.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              6.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              6.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:e7300a01-f8c1-4351-9511-02790a5376b0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:307b7db6-8014-4628-b80e-ff925bf71168",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:caa6045e-4189-4571-8914-1189e51ac71e",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              6.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              6.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              10.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              10.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:206806a4-a2f8-4c04-858e-99d289858a40",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              6.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              6.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:793997c5-bcc4-4610-984b-6cf2c2997348",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8e503e04-ad51-423b-8102-708a845189b6",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              10.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              6.0,
              0.0
            ]
          },
          "properties": null
        }
      ]
    }
  ],
  "edges": [
    {
      "id": "uuid:c60507ba-226b-4e49-a702-e9afef899b23",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0",
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698",
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:8582d9c2-6053-495a-8413-f5493691c0de",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071",
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3",
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3",
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70",
          "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8",
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:7da1c2fe-f798-43cc-af44-ac63f968139c",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3",
          "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:745aa367-94b6-4949-a856-5271ec6672e9",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0",
          "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:f921656a-58e3-4375-bdff-ac8019f524cf",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd",
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0",
          "uuid:307b7db6-8014-4628-b80e-ff925bf71168"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6",
          "uuid:307b7db6-8014-4628-b80e-ff925bf71168"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6",
          "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:307b7db6-8014-4628-b80e-ff925bf71168",
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:fb03276b-4250-4d52-81e1-035a0bd92895",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d",
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:af347f25-a547-477c-b246-cb810756d4dc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "uuid:caa6045e-4189-4571-8914-1189e51ac71e"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:caa6045e-4189-4571-8914-1189e51ac71e",
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:caa6045e-4189-4571-8914-1189e51ac71e",
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:242a8400-a076-4817-86c6-acd56087cec6",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:4ad210b7-5de5-4732-af7c-978de28f988b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6",
          "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9",
          "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:4406e3f5-89dc-463b-84e4-487490f71f1a",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d",
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:511c6e7d-728b-4f1f-9763-9461eb628586",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4",
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9",
          "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:06babc8d-f0d6-43eb-bfad-931055bae084",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51",
          "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:fc877bbe-72a8-4e59-b959-010e6660984a",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09",
          "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:aafd209b-cd13-401a-83f5-26751a02cffe",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51",
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:9238cbda-d019-4b57-8319-0cc355656802",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:91cdc345-f745-4643-bc88-a24f8e2216b0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:206806a4-a2f8-4c04-858e-99d289858a40",
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a",
          "uuid:206806a4-a2f8-4c04-858e-99d289858a40"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:61f99921-a94d-4e0d-8353-f027d76227c5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:474fef44-eb6e-4e19-a871-433f9bac5650",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3",
          "uuid:206806a4-a2f8-4c04-858e-99d289858a40"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717",
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:71af0dde-7fc9-4290-9624-119e91f422ea",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348",
          "uuid:8e503e04-ad51-423b-8102-708a845189b6"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:ad13a84c-df97-4b75-9dc1-1ce452249964",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8e503e04-ad51-423b-8102-708a845189b6",
          "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:c2a00070-f12b-42f9-b78c-b33daa500873",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606",
          "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:13dd8184-f73e-4d9f-9977-3e573274fccc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8e503e04-ad51-423b-8102-708a845189b6",
          "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606",
          "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:ed666061-98c5-439d-ab0d-5a792437a873",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:5a36c75b-053b-4d7b-b512-6777786d6180",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1",
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348",
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0",
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0",
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:a604828d-a36b-4fac-ba6f-6160ade95301",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4",
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:38499704-81f7-4d47-965f-435e0b7b0850",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d",
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:b6e30631-9768-4020-8947-c32137328216",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3"
        ]
      },
      "properties": {
        "length": 4.0
      }
    }
  ],
  "faces": [
    {
      "id": "uuid:4ac3b91b-eeb7-428c-b5e9-7e8a3f0998ae",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:c60507ba-226b-4e49-a702-e9afef899b23",
                "orientation": "+"
              },
              {
                "ref": "uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac",
                "orientation": "+"
              },
              {
                "ref": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
                "orientation": "+"
              },
              {
                "ref": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          1.0,
          0.0,
          -0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:4a294022-4864-49c7-8cee-f9e43360bc4e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
                "orientation": "+"
              },
              {
                "ref": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
                "orientation": "-"
              },
              {
                "ref": "uuid:8582d9c2-6053-495a-8413-f5493691c0de",
                "orientation": "+"
              },
              {
                "ref": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          3.007964248051e-16
        ],
        "area": 18.0
      }
    },
    {
      "id": "uuid:01947f47-ee13-44a9-85a4-2bcb4881982a",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555",
                "orientation": "+"
              },
              {
                "ref": "uuid:c60507ba-226b-4e49-a702-e9afef899b23",
                "orientation": "-"
              },
              {
                "ref": "uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81",
                "orientation": "+"
              },
              {
                "ref": "uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:607a3363-3eb7-4ce6-a633-86d2e565692b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:8582d9c2-6053-495a-8413-f5493691c0de",
                "orientation": "-"
              },
              {
                "ref": "uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac",
                "orientation": "-"
              },
              {
                "ref": "uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555",
                "orientation": "-"
              },
              {
                "ref": "uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0",
                "orientation": "+"
              },
              {
                "ref": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
                "orientation": "+"
              },
              {
                "ref": "uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 56.0
      }
    },
    {
      "id": "uuid:3c1f5c4b-d842-40b6-a332-99d50015fa8f",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
                "orientation": "+"
              },
              {
                "ref": "uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5",
                "orientation": "+"
              },
              {
                "ref": "uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0",
                "orientation": "-"
              },
              {
                "ref": "uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:fe522919-1421-4fd1-9930-8c6551e3f2a5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:7da1c2fe-f798-43cc-af44-ac63f968139c",
                "orientation": "+"
              },
              {
                "ref": "uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1",
                "orientation": "+"
              },
              {
                "ref": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
                "orientation": "-"
              },
              {
                "ref": "uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 6.0
      }
    },
    {
      "id": "uuid:2387ae98-9236-42fe-9414-c45b99954c41",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6",
                "orientation": "+"
              },
              {
                "ref": "uuid:7da1c2fe-f798-43cc-af44-ac63f968139c",
                "orientation": "-"
              },
              {
                "ref": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
                "orientation": "-"
              },
              {
                "ref": "uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81",
                "orientation": "-"
              },
              {
                "ref": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
                "orientation": "-"
              },
              {
                "ref": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          -1.0
        ],
        "area": 56.0
      }
    },
    {
      "id": "uuid:4ba85faa-3935-4e89-a9f8-dcd647a5dbed",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6",
                "orientation": "-"
              },
              {
                "ref": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
                "orientation": "-"
              },
              {
                "ref": "uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5",
                "orientation": "-"
              },
              {
                "ref": "uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:c55c88db-d187-4d7e-9aaa-b9d3dce52663",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d",
                "orientation": "+"
              },
              {
                "ref": "uuid:745aa367-94b6-4949-a856-5271ec6672e9",
                "orientation": "+"
              },
              {
                "ref": "uuid:f921656a-58e3-4375-bdff-ac8019f524cf",
                "orientation": "+"
              },
              {
                "ref": "uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:dbd99467-ea83-4dff-b03f-eef2aad2687c",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:745aa367-94b6-4949-a856-5271ec6672e9",
                "orientation": "-"
              },
              {
                "ref": "uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24",
                "orientation": "+"
              },
              {
                "ref": "uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3",
                "orientation": "-"
              },
              {
                "ref": "uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -3.007964248051e-16
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:0e55e87d-8475-4c92-89e7-d62f97ce9ec2",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3",
                "orientation": "+"
              },
              {
                "ref": "uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78",
                "orientation": "+"
              },
              {
                "ref": "uuid:fb03276b-4250-4d52-81e1-035a0bd92895",
                "orientation": "+"
              },
              {
                "ref": "uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 18.0
      }
    },
    {
      "id": "uuid:6a5ff199-56a7-4e65-94b5-bfdf2ae3449d",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:f921656a-58e3-4375-bdff-ac8019f524cf",
                "orientation": "-"
              },
              {
                "ref": "uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05",
                "orientation": "-"
              },
              {
                "ref": "uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf",
                "orientation": "-"
              },
              {
                "ref": "uuid:af347f25-a547-477c-b246-cb810756d4dc",
                "orientation": "+"
              },
              {
                "ref": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
                "orientation": "+"
              },
              {
                "ref": "uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 56.0
      }
    },
    {
      "id": "uuid:e499fea3-19f7-4863-8a58-751caff7d884",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3",
                "orientation": "+"
              },
              {
                "ref": "uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5",
                "orientation": "+"
              },
              {
                "ref": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
                "orientation": "-"
              },
              {
                "ref": "uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 6.0
      }
    },
    {
      "id": "uuid:9e4c0c0e-6acf-401b-b35e-0e917ce3a5fc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:242a8400-a076-4817-86c6-acd56087cec6",
                "orientation": "+"
              },
              {
                "ref": "uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78",
                "orientation": "-"
              },
              {
                "ref": "uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24",
                "orientation": "-"
              },
              {
                "ref": "uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d",
                "orientation": "-"
              },
              {
                "ref": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
                "orientation": "+"
              },
              {
                "ref": "uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          -1.0
        ],
        "area": 56.0
      }
    },
    {
      "id": "uuid:3f5c452f-9815-4b21-9b2d-0127ae80c385",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:242a8400-a076-4817-86c6-acd56087cec6",
                "orientation": "-"
              },
              {
                "ref": "uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724",
                "orientation": "-"
              },
              {
                "ref": "uuid:af347f25-a547-477c-b246-cb810756d4dc",
                "orientation": "-"
              },
              {
                "ref": "uuid:fb03276b-4250-4d52-81e1-035a0bd92895",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          1.0,
          0.0,
          -0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:66a430c0-123f-42df-9d11-64347362bcb3",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:4ad210b7-5de5-4732-af7c-978de28f988b",
                "orientation": "+"
              },
              {
                "ref": "uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e",
                "orientation": "+"
              },
              {
                "ref": "uuid:4406e3f5-89dc-463b-84e4-487490f71f1a",
                "orientation": "+"
              },
              {
                "ref": "uuid:511c6e7d-728b-4f1f-9763-9461eb628586",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:31d8f2b5-cc74-4f72-b230-d27dad0fd589",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc",
                "orientation": "+"
              },
              {
                "ref": "uuid:06babc8d-f0d6-43eb-bfad-931055bae084",
                "orientation": "+"
              },
              {
                "ref": "uuid:fc877bbe-72a8-4e59-b959-010e6660984a",
                "orientation": "+"
              },
              {
                "ref": "uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          1.0,
          0.0,
          -0.0
        ],
        "area": 30.0
      }
    },
    {
      "id": "uuid:65959e29-11cb-4568-904d-61c4a7c17b98",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:aafd209b-cd13-401a-83f5-26751a02cffe",
                "orientation": "+"
              },
              {
                "ref": "uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03",
                "orientation": "+"
              },
              {
                "ref": "uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81",
                "orientation": "-"
              },
              {
                "ref": "uuid:9238cbda-d019-4b57-8319-0cc355656802",
                "orientation": "+"
              },
              {
                "ref": "uuid:06babc8d-f0d6-43eb-bfad-931055bae084",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 30.0
      }
    },
    {
      "id": "uuid:e2efe498-c6d5-4f9c-ac07-4c1c9e406675",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
                "orientation": "-"
              },
              {
                "ref": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
                "orientation": "-"
              },
              {
                "ref": "uuid:91cdc345-f745-4643-bc88-a24f8e2216b0",
                "orientation": "+"
              },
              {
                "ref": "uuid:4406e3f5-89dc-463b-84e4-487490f71f1a",
                "orientation": "-"
              },
              {
                "ref": "uuid:fc877bbe-72a8-4e59-b959-010e6660984a",
                "orientation": "-"
              },
              {
                "ref": "uuid:9238cbda-d019-4b57-8319-0cc355656802",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 32.0
      }
    },
    {
      "id": "uuid:5bcee2b5-be9b-47d6-9a8b-35dac021f661",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:4ad210b7-5de5-4732-af7c-978de28f988b",
                "orientation": "-"
              },
              {
                "ref": "uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4",
                "orientation": "-"
              },
              {
                "ref": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
                "orientation": "-"
              },
              {
                "ref": "uuid:61f99921-a94d-4e0d-8353-f027d76227c5",
                "orientation": "-"
              },
              {
                "ref": "uuid:aafd209b-cd13-401a-83f5-26751a02cffe",
                "orientation": "-"
              },
              {
                "ref": "uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -0.0,
          -0.0,
          -1.0
        ],
        "area": 88.0
      }
    },
    {
      "id": "uuid:91ce0c52-11c3-4e32-8bcc-dea958a3969e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:474fef44-eb6e-4e19-a871-433f9bac5650",
                "orientation": "-"
              },
              {
                "ref": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
                "orientation": "-"
              },
              {
                "ref": "uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03",
                "orientation": "-"
              },
              {
                "ref": "uuid:61f99921-a94d-4e0d-8353-f027d76227c5",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:56283886-1f4c-448c-b785-80fb9740a9cc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda",
                "orientation": "+"
              },
              {
                "ref": "uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4",
                "orientation": "+"
              },
              {
                "ref": "uuid:511c6e7d-728b-4f1f-9763-9461eb628586",
                "orientation": "-"
              },
              {
                "ref": "uuid:91cdc345-f745-4643-bc88-a24f8e2216b0",
                "orientation": "-"
              },
              {
                "ref": "uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -0.0
        ],
        "area": 18.0
      }
    },
    {
      "id": "uuid:f3338301-b0e3-401c-af23-41ac2ae8e969",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda",
                "orientation": "-"
              },
              {
                "ref": "uuid:7da1c2fe-f798-43cc-af44-ac63f968139c",
                "orientation": "-"
              },
              {
                "ref": "uuid:474fef44-eb6e-4e19-a871-433f9bac5650",
                "orientation": "+"
              },
              {
                "ref": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 6.0
      }
    },
    {
      "id": "uuid:a2117d6b-4621-4a6b-9809-9fab3dfc4ff0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0",
                "orientation": "+"
              },
              {
                "ref": "uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985",
                "orientation": "+"
              },
              {
                "ref": "uuid:71af0dde-7fc9-4290-9624-119e91f422ea",
                "orientation": "+"
              },
              {
                "ref": "uuid:ad13a84c-df97-4b75-9dc1-1ce452249964",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:9d67557a-e130-4a47-b63d-c6a2bdf21fa2",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:c2a00070-f12b-42f9-b78c-b33daa500873",
                "orientation": "+"
              },
              {
                "ref": "uuid:ad13a84c-df97-4b75-9dc1-1ce452249964",
                "orientation": "-"
              },
              {
                "ref": "uuid:13dd8184-f73e-4d9f-9977-3e573274fccc",
                "orientation": "+"
              },
              {
                "ref": "uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -0.0
        ],
        "area": 30.0
      }
    },
    {
      "id": "uuid:d45fca44-8685-4146-92a5-b84d82fdc838",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:ed666061-98c5-439d-ab0d-5a792437a873",
                "orientation": "+"
              },
              {
                "ref": "uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f",
                "orientation": "+"
              },
              {
                "ref": "uuid:5a36c75b-053b-4d7b-b512-6777786d6180",
                "orientation": "+"
              },
              {
                "ref": "uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d",
                "orientation": "-"
              },
              {
                "ref": "uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 30.0
      }
    },
    {
      "id": "uuid:2497a842-0932-4fe5-ac1a-2f773473f338",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0",
                "orientation": "+"
              },
              {
                "ref": "uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78",
                "orientation": "-"
              },
              {
                "ref": "uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24",
                "orientation": "-"
              },
              {
                "ref": "uuid:5a36c75b-053b-4d7b-b512-6777786d6180",
                "orientation": "-"
              },
              {
                "ref": "uuid:13dd8184-f73e-4d9f-9977-3e573274fccc",
                "orientation": "-"
              },
              {
                "ref": "uuid:71af0dde-7fc9-4290-9624-119e91f422ea",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 32.0
      }
    },
    {
      "id": "uuid:04ea47e9-b4dd-4bed-a8f4-4802d1735c74",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:ed666061-98c5-439d-ab0d-5a792437a873",
                "orientation": "-"
              },
              {
                "ref": "uuid:61f99921-a94d-4e0d-8353-f027d76227c5",
                "orientation": "+"
              },
              {
                "ref": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
                "orientation": "-"
              },
              {
                "ref": "uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635",
                "orientation": "-"
              },
              {
                "ref": "uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0",
                "orientation": "-"
              },
              {
                "ref": "uuid:c2a00070-f12b-42f9-b78c-b33daa500873",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -0.0,
          -0.0,
          -1.0
        ],
        "area": 88.0
      }
    },
    {
      "id": "uuid:b5fd960f-0d14-4257-9182-40de738a7e50",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4",
                "orientation": "+"
              },
              {
                "ref": "uuid:242a8400-a076-4817-86c6-acd56087cec6",
                "orientation": "+"
              },
              {
                "ref": "uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0",
                "orientation": "-"
              },
              {
                "ref": "uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985",
                "orientation": "-"
              },
              {
                "ref": "uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          1.0,
          0.0,
          -0.0
        ],
        "area": 18.0
      }
    },
    {
      "id": "uuid:e119b096-e589-49bd-b1db-a1182dc2dade",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:474fef44-eb6e-4e19-a871-433f9bac5650",
                "orientation": "-"
              },
              {
                "ref": "uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3",
                "orientation": "-"
              },
              {
                "ref": "uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4",
                "orientation": "-"
              },
              {
                "ref": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 6.0
      }
    },
    {
      "id": "uuid:67842d3a-7c79-4f2a-8630-744711071e93",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:a604828d-a36b-4fac-ba6f-6160ade95301",
                "orientation": "-"
              },
              {
                "ref": "uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635",
                "orientation": "+"
              },
              {
                "ref": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
                "orientation": "+"
              },
              {
                "ref": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
                "orientation": "+"
              },
              {
                "ref": "uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -0.0,
          -0.0,
          -1.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:f1c1a636-d6ab-414c-a0aa-855fc7e85e1f",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280",
                "orientation": "+"
              },
              {
                "ref": "uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985",
                "orientation": "-"
              },
              {
                "ref": "uuid:a604828d-a36b-4fac-ba6f-6160ade95301",
                "orientation": "+"
              },
              {
                "ref": "uuid:511c6e7d-728b-4f1f-9763-9461eb628586",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:a22a6c54-306e-44bc-9b94-6c32c705e63e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280",
                "orientation": "-"
              },
              {
                "ref": "uuid:91cdc345-f745-4643-bc88-a24f8e2216b0",
                "orientation": "-"
              },
              {
                "ref": "uuid:38499704-81f7-4d47-965f-435e0b7b0850",
                "orientation": "-"
              },
              {
                "ref": "uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 8.0
      }
    },
    {
      "id": "uuid:9ed21e0a-b062-4000-88e2-50bd9153e417",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:b6e30631-9768-4020-8947-c32137328216",
                "orientation": "+"
              },
              {
                "ref": "uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5",
                "orientation": "-"
              },
              {
                "ref": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
                "orientation": "-"
              },
              {
                "ref": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
                "orientation": "-"
              },
              {
                "ref": "uuid:af347f25-a547-477c-b246-cb810756d4dc",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 16.0
      }
    },
    {
      "id": "uuid:802ff3d8-b8da-423f-8a02-7b2288485edd",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:38499704-81f7-4d47-965f-435e0b7b0850",
                "orientation": "+"
              },
              {
                "ref": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
                "orientation": "-"
              },
              {
                "ref": "uuid:b6e30631-9768-4020-8947-c32137328216",
                "orientation": "-"
              },
              {
                "ref": "uuid:fb03276b-4250-4d52-81e1-035a0bd92895",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          3.609557097661e-16,
          -1.0,
          0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:16c13b7b-aeda-4130-a793-d63f62bcc75b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4",
                "orientation": "+"
              },
              {
                "ref": "uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa",
                "orientation": "+"
              },
              {
                "ref": "uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda",
                "orientation": "+"
              },
              {
                "ref": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
                "orientation": "-"
              },
              {
                "ref": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:786e8738-1690-426d-8e2f-f5e734336a67",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724",
                "orientation": "-"
              },
              {
                "ref": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
                "orientation": "+"
              },
              {
                "ref": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
                "orientation": "+"
              },
              {
                "ref": "uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1",
                "orientation": "-"
              },
              {
                "ref": "uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 12.0
      }
    }
  ],
  "solids": [
    {
      "id": "uuid:758590d2-8cc6-4ff7-8fcc-d7ecd01b3498",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Solid",
        "shells": [
          {
            "type": "Shell",
            "directed_references": [
              {
                "ref": "uuid:4ac3b91b-eeb7-428c-b5e9-7e8a3f0998ae",
                "orientation": "+"
              },
              {
                "ref": "uuid:4a294022-4864-49c7-8cee-f9e43360bc4e",
                "orientation": "+"
              },
              {
                "ref": "uuid:01947f47-ee13-44a9-85a4-2bcb4881982a",
                "orientation": "+"
              },
              {
                "ref": "uuid:607a3363-3eb7-4ce6-a633-86d2e565692b",
                "orientation": "+"
              },
              {
                "ref": "uuid:3c1f5c4b-d842-40b6-a332-99d50015fa8f",
                "orientation": "+"
              },
              {
                "ref": "uuid:fe522919-1421-4fd1-9930-8c6551e3f2a5",
                "orientation": "+"
              },
              {
                "ref": "uuid:2387ae98-9236-42fe-9414-c45b99954c41",
                "orientation": "+"
              },
              {
                "ref": "uuid:4ba85faa-3935-4e89-a9f8-dcd647a5dbed",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "name": "Upper East",
        "levels": [
          2
        ],
        "volume": 168.0
      }
    },
    {
      "id": "uuid:82ce9302-e51d-48ff-a119-79bb5501ed1c",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Solid",
        "shells": [
          {
            "type": "Shell",
            "directed_references": [
              {
                "ref": "uuid:c55c88db-d187-4d7e-9aaa-b9d3dce52663",
                "orientation": "+"
              },
              {
                "ref": "uuid:dbd99467-ea83-4dff-b03f-eef2aad2687c",
                "orientation": "+"
              },
              {
                "ref": "uuid:0e55e87d-8475-4c92-89e7-d62f97ce9ec2",
                "orientation": "+"
              },
              {
                "ref": "uuid:6a5ff199-56a7-4e65-94b5-bfdf2ae3449d",
                "orientation": "+"
              },
              {
                "ref": "uuid:3c1f5c4b-d842-40b6-a332-99d50015fa8f",
                "orientation": "-"
              },
              {
                "ref": "uuid:e499fea3-19f7-4863-8a58-751caff7d884",
                "orientation": "+"
              },
              {
                "ref": "uuid:9e4c0c0e-6acf-401b-b35e-0e917ce3a5fc",
                "orientation": "+"
              },
              {
                "ref": "uuid:3f5c452f-9815-4b21-9b2d-0127ae80c385",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "name": "Upper West",
        "levels": [
          2
        ],
        "volume": 168.0
      }
    },
    {
      "id": "uuid:1070811c-70bd-4698-a08f-92c62e41aafc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Solid",
        "shells": [
          {
            "type": "Shell",
            "directed_references": [
              {
                "ref": "uuid:66a430c0-123f-42df-9d11-64347362bcb3",
                "orientation": "+"
              },
              {
                "ref": "uuid:31d8f2b5-cc74-4f72-b230-d27dad0fd589",
                "orientation": "+"
              },
              {
                "ref": "uuid:65959e29-11cb-4568-904d-61c4a7c17b98",
                "orientation": "+"
              },
              {
                "ref": "uuid:e2efe498-c6d5-4f9c-ac07-4c1c9e406675",
                "orientation": "+"
              },
              {
                "ref": "uuid:5bcee2b5-be9b-47d6-9a8b-35dac021f661",
                "orientation": "+"
              },
              {
                "ref": "uuid:91ce0c52-11c3-4e32-8bcc-dea958a3969e",
                "orientation": "+"
              },
              {
                "ref": "uuid:56283886-1f4c-448c-b785-80fb9740a9cc",
                "orientation": "+"
              },
              {
                "ref": "uuid:f3338301-b0e3-401c-af23-41ac2ae8e969",
                "orientation": "+"
              },
              {
                "ref": "uuid:2387ae98-9236-42fe-9414-c45b99954c41",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "name": "Lower East",
        "levels": [
          1
        ],
        "volume": 264.0
      }
    },
    {
      "id": "uuid:74618bd4-0bbe-4490-92b3-27a4da496c39",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Solid",
        "shells": [
          {
            "type": "Shell",
            "directed_references": [
              {
                "ref": "uuid:a2117d6b-4621-4a6b-9809-9fab3dfc4ff0",
                "orientation": "+"
              },
              {
                "ref": "uuid:9d67557a-e130-4a47-b63d-c6a2bdf21fa2",
                "orientation": "+"
              },
              {
                "ref": "uuid:d45fca44-8685-4146-92a5-b84d82fdc838",
                "orientation": "+"
              },
              {
                "ref": "uuid:2497a842-0932-4fe5-ac1a-2f773473f338",
                "orientation": "+"
              },
              {
                "ref": "uuid:04ea47e9-b4dd-4bed-a8f4-4802d1735c74",
                "orientation": "+"
              },
              {
                "ref": "uuid:b5fd960f-0d14-4257-9182-40de738a7e50",
                "orientation": "+"
              },
              {
                "ref": "uuid:e119b096-e589-49bd-b1db-a1182dc2dade",
                "orientation": "+"
              },
              {
                "ref": "uuid:91ce0c52-11c3-4e32-8bcc-dea958a3969e",
                "orientation": "-"
              },
              {
                "ref": "uuid:9e4c0c0e-6acf-401b-b35e-0e917ce3a5fc",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "name": "Lower West",
        "levels": [
          1
        ],
        "volume": 264.0
      }
    },
    {
      "id": "uuid:50453cb2-89bd-4432-8c7c-fdc2318febc2",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Solid",
        "shells": [
          {
            "type": "Shell",
            "directed_references": [
              {
                "ref": "uuid:67842d3a-7c79-4f2a-8630-744711071e93",
                "orientation": "+"
              },
              {
                "ref": "uuid:f1c1a636-d6ab-414c-a0aa-855fc7e85e1f",
                "orientation": "+"
              },
              {
                "ref": "uuid:a22a6c54-306e-44bc-9b94-6c32c705e63e",
                "orientation": "+"
              },
              {
                "ref": "uuid:9ed21e0a-b062-4000-88e2-50bd9153e417",
                "orientation": "+"
              },
              {
                "ref": "uuid:802ff3d8-b8da-423f-8a02-7b2288485edd",
                "orientation": "+"
              },
              {
                "ref": "uuid:4ba85faa-3935-4e89-a9f8-dcd647a5dbed",
                "orientation": "-"
              },
              {
                "ref": "uuid:56283886-1f4c-448c-b785-80fb9740a9cc",
                "orientation": "-"
              },
              {
                "ref": "uuid:3f5c452f-9815-4b21-9b2d-0127ae80c385",
                "orientation": "-"
              },
              {
                "ref": "uuid:b5fd960f-0d14-4257-9182-40de738a7e50",
                "orientation": "-"
              },
              {
                "ref": "uuid:16c13b7b-aeda-4130-a793-d63f62bcc75b",
                "orientation": "+"
              },
              {
                "ref": "uuid:786e8738-1690-426d-8e2f-f5e734336a67",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "name": "Stairwell",
        "levels": [
          1,
          2
        ],
        "volume": 120.0
      }
    }
  ]
}
```

#### jsonld
```jsonld
{
  "@context": "https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-multi-collection/context.jsonld",
  "type": "FeatureCollection",
  "metadata": {
    "units": "meters",
    "coordinate_precision": 3,
    "conversion_factor": 0.0254
  },
  "points": [
    {
      "type": "FeatureCollection",
      "features": [
        {
          "id": "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:fad324b9-801f-40f4-b65b-91f8753e9698",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              18.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              6.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              6.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              6.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              6.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:e7300a01-f8c1-4351-9511-02790a5376b0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              10.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:307b7db6-8014-4628-b80e-ff925bf71168",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              2.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              2.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              2.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:caa6045e-4189-4571-8914-1189e51ac71e",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              6.0,
              6.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              6.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              10.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              20.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              10.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:206806a4-a2f8-4c04-858e-99d289858a40",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              12.0,
              6.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              10.0,
              6.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              0.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:793997c5-bcc4-4610-984b-6cf2c2997348",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8e503e04-ad51-423b-8102-708a845189b6",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              0.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              10.0,
              0.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              0.0,
              10.0,
              3.0
            ]
          },
          "properties": null
        },
        {
          "id": "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0",
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              8.0,
              6.0,
              0.0
            ]
          },
          "properties": null
        }
      ]
    }
  ],
  "edges": [
    {
      "id": "uuid:c60507ba-226b-4e49-a702-e9afef899b23",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0",
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698",
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "uuid:fad324b9-801f-40f4-b65b-91f8753e9698"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:8582d9c2-6053-495a-8413-f5493691c0de",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c611f840-2829-44b2-b367-3915ca7875a4",
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071",
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3",
          "uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3",
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70",
          "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8",
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:7da1c2fe-f798-43cc-af44-ac63f968139c",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3",
          "uuid:8087116e-84cc-44d1-8047-78dc3837d7e8"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b",
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:745aa367-94b6-4949-a856-5271ec6672e9",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0",
          "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:f921656a-58e3-4375-bdff-ac8019f524cf",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd",
          "uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0",
          "uuid:307b7db6-8014-4628-b80e-ff925bf71168"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6",
          "uuid:307b7db6-8014-4628-b80e-ff925bf71168"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6",
          "uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:307b7db6-8014-4628-b80e-ff925bf71168",
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:fb03276b-4250-4d52-81e1-035a0bd92895",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d",
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:af347f25-a547-477c-b246-cb810756d4dc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "uuid:caa6045e-4189-4571-8914-1189e51ac71e"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:caa6045e-4189-4571-8914-1189e51ac71e",
          "uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:caa6045e-4189-4571-8914-1189e51ac71e",
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:242a8400-a076-4817-86c6-acd56087cec6",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:4ad210b7-5de5-4732-af7c-978de28f988b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6",
          "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9",
          "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:4406e3f5-89dc-463b-84e4-487490f71f1a",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d",
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:511c6e7d-728b-4f1f-9763-9461eb628586",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4",
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9",
          "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:06babc8d-f0d6-43eb-bfad-931055bae084",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51",
          "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:fc877bbe-72a8-4e59-b959-010e6660984a",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09",
          "uuid:c060c1dc-6544-4595-b583-72ecf603fd6d"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:aafd209b-cd13-401a-83f5-26751a02cffe",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:20d3c864-4a8c-4440-b600-a1d424e92f51",
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "uuid:22138e52-65ef-4773-b69d-5ea2628fad7b"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:9238cbda-d019-4b57-8319-0cc355656802",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38",
          "uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:91cdc345-f745-4643-bc88-a24f8e2216b0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d",
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:206806a4-a2f8-4c04-858e-99d289858a40",
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a",
          "uuid:206806a4-a2f8-4c04-858e-99d289858a40"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:61f99921-a94d-4e0d-8353-f027d76227c5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:474fef44-eb6e-4e19-a871-433f9bac5650",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:f34d9f2e-4180-41de-a613-46f78f4c178f",
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3",
          "uuid:206806a4-a2f8-4c04-858e-99d289858a40"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717",
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:71af0dde-7fc9-4290-9624-119e91f422ea",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348",
          "uuid:8e503e04-ad51-423b-8102-708a845189b6"
        ]
      },
      "properties": {
        "length": 8.0
      }
    },
    {
      "id": "uuid:ad13a84c-df97-4b75-9dc1-1ce452249964",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8e503e04-ad51-423b-8102-708a845189b6",
          "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:c2a00070-f12b-42f9-b78c-b33daa500873",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606",
          "uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:13dd8184-f73e-4d9f-9977-3e573274fccc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8e503e04-ad51-423b-8102-708a845189b6",
          "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606",
          "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:ed666061-98c5-439d-ab0d-5a792437a873",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e",
          "uuid:ca62577e-8e24-4af2-88bf-33b34e25e606"
        ]
      },
      "properties": {
        "length": 10.0
      }
    },
    {
      "id": "uuid:5a36c75b-053b-4d7b-b512-6777786d6180",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1",
          "uuid:e7300a01-f8c1-4351-9511-02790a5376b0"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348",
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0",
          "uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a"
        ]
      },
      "properties": {
        "length": 2.0
      }
    },
    {
      "id": "uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0"
        ]
      },
      "properties": {
        "length": 6.0
      }
    },
    {
      "id": "uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0",
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e"
        ]
      },
      "properties": {
        "length": 3.0
      }
    },
    {
      "id": "uuid:a604828d-a36b-4fac-ba6f-6160ade95301",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df",
          "uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4",
          "uuid:793997c5-bcc4-4610-984b-6cf2c2997348"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:38499704-81f7-4d47-965f-435e0b7b0850",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d",
          "uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:b6e30631-9768-4020-8947-c32137328216",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9",
          "uuid:11caaac5-b631-4bd8-a6af-f82cb6371071"
        ]
      },
      "properties": {
        "length": 4.0
      }
    },
    {
      "id": "uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Edge",
        "references": [
          "uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e",
          "uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3"
        ]
      },
      "properties": {
        "length": 4.0
      }
    }
  ],
  "faces": [
    {
      "id": "uuid:4ac3b91b-eeb7-428c-b5e9-7e8a3f0998ae",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:c60507ba-226b-4e49-a702-e9afef899b23",
                "orientation": "+"
              },
              {
                "ref": "uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac",
                "orientation": "+"
              },
              {
                "ref": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
                "orientation": "+"
              },
              {
                "ref": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          1.0,
          0.0,
          -0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:4a294022-4864-49c7-8cee-f9e43360bc4e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
                "orientation": "+"
              },
              {
                "ref": "uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569",
                "orientation": "-"
              },
              {
                "ref": "uuid:8582d9c2-6053-495a-8413-f5493691c0de",
                "orientation": "+"
              },
              {
                "ref": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          3.007964248051e-16
        ],
        "area": 18.0
      }
    },
    {
      "id": "uuid:01947f47-ee13-44a9-85a4-2bcb4881982a",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555",
                "orientation": "+"
              },
              {
                "ref": "uuid:c60507ba-226b-4e49-a702-e9afef899b23",
                "orientation": "-"
              },
              {
                "ref": "uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81",
                "orientation": "+"
              },
              {
                "ref": "uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:607a3363-3eb7-4ce6-a633-86d2e565692b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:8582d9c2-6053-495a-8413-f5493691c0de",
                "orientation": "-"
              },
              {
                "ref": "uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac",
                "orientation": "-"
              },
              {
                "ref": "uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555",
                "orientation": "-"
              },
              {
                "ref": "uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0",
                "orientation": "+"
              },
              {
                "ref": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
                "orientation": "+"
              },
              {
                "ref": "uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 56.0
      }
    },
    {
      "id": "uuid:3c1f5c4b-d842-40b6-a332-99d50015fa8f",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
                "orientation": "+"
              },
              {
                "ref": "uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5",
                "orientation": "+"
              },
              {
                "ref": "uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0",
                "orientation": "-"
              },
              {
                "ref": "uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:fe522919-1421-4fd1-9930-8c6551e3f2a5",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:7da1c2fe-f798-43cc-af44-ac63f968139c",
                "orientation": "+"
              },
              {
                "ref": "uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1",
                "orientation": "+"
              },
              {
                "ref": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
                "orientation": "-"
              },
              {
                "ref": "uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 6.0
      }
    },
    {
      "id": "uuid:2387ae98-9236-42fe-9414-c45b99954c41",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6",
                "orientation": "+"
              },
              {
                "ref": "uuid:7da1c2fe-f798-43cc-af44-ac63f968139c",
                "orientation": "-"
              },
              {
                "ref": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
                "orientation": "-"
              },
              {
                "ref": "uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81",
                "orientation": "-"
              },
              {
                "ref": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
                "orientation": "-"
              },
              {
                "ref": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          -1.0
        ],
        "area": 56.0
      }
    },
    {
      "id": "uuid:4ba85faa-3935-4e89-a9f8-dcd647a5dbed",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6",
                "orientation": "-"
              },
              {
                "ref": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
                "orientation": "-"
              },
              {
                "ref": "uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5",
                "orientation": "-"
              },
              {
                "ref": "uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:c55c88db-d187-4d7e-9aaa-b9d3dce52663",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d",
                "orientation": "+"
              },
              {
                "ref": "uuid:745aa367-94b6-4949-a856-5271ec6672e9",
                "orientation": "+"
              },
              {
                "ref": "uuid:f921656a-58e3-4375-bdff-ac8019f524cf",
                "orientation": "+"
              },
              {
                "ref": "uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:dbd99467-ea83-4dff-b03f-eef2aad2687c",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:745aa367-94b6-4949-a856-5271ec6672e9",
                "orientation": "-"
              },
              {
                "ref": "uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24",
                "orientation": "+"
              },
              {
                "ref": "uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3",
                "orientation": "-"
              },
              {
                "ref": "uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -3.007964248051e-16
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:0e55e87d-8475-4c92-89e7-d62f97ce9ec2",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3",
                "orientation": "+"
              },
              {
                "ref": "uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78",
                "orientation": "+"
              },
              {
                "ref": "uuid:fb03276b-4250-4d52-81e1-035a0bd92895",
                "orientation": "+"
              },
              {
                "ref": "uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 18.0
      }
    },
    {
      "id": "uuid:6a5ff199-56a7-4e65-94b5-bfdf2ae3449d",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:f921656a-58e3-4375-bdff-ac8019f524cf",
                "orientation": "-"
              },
              {
                "ref": "uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05",
                "orientation": "-"
              },
              {
                "ref": "uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf",
                "orientation": "-"
              },
              {
                "ref": "uuid:af347f25-a547-477c-b246-cb810756d4dc",
                "orientation": "+"
              },
              {
                "ref": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
                "orientation": "+"
              },
              {
                "ref": "uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 56.0
      }
    },
    {
      "id": "uuid:e499fea3-19f7-4863-8a58-751caff7d884",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3",
                "orientation": "+"
              },
              {
                "ref": "uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5",
                "orientation": "+"
              },
              {
                "ref": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
                "orientation": "-"
              },
              {
                "ref": "uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 6.0
      }
    },
    {
      "id": "uuid:9e4c0c0e-6acf-401b-b35e-0e917ce3a5fc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:242a8400-a076-4817-86c6-acd56087cec6",
                "orientation": "+"
              },
              {
                "ref": "uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78",
                "orientation": "-"
              },
              {
                "ref": "uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24",
                "orientation": "-"
              },
              {
                "ref": "uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d",
                "orientation": "-"
              },
              {
                "ref": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
                "orientation": "+"
              },
              {
                "ref": "uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          -1.0
        ],
        "area": 56.0
      }
    },
    {
      "id": "uuid:3f5c452f-9815-4b21-9b2d-0127ae80c385",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:242a8400-a076-4817-86c6-acd56087cec6",
                "orientation": "-"
              },
              {
                "ref": "uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724",
                "orientation": "-"
              },
              {
                "ref": "uuid:af347f25-a547-477c-b246-cb810756d4dc",
                "orientation": "-"
              },
              {
                "ref": "uuid:fb03276b-4250-4d52-81e1-035a0bd92895",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          1.0,
          0.0,
          -0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:66a430c0-123f-42df-9d11-64347362bcb3",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:4ad210b7-5de5-4732-af7c-978de28f988b",
                "orientation": "+"
              },
              {
                "ref": "uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e",
                "orientation": "+"
              },
              {
                "ref": "uuid:4406e3f5-89dc-463b-84e4-487490f71f1a",
                "orientation": "+"
              },
              {
                "ref": "uuid:511c6e7d-728b-4f1f-9763-9461eb628586",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:31d8f2b5-cc74-4f72-b230-d27dad0fd589",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc",
                "orientation": "+"
              },
              {
                "ref": "uuid:06babc8d-f0d6-43eb-bfad-931055bae084",
                "orientation": "+"
              },
              {
                "ref": "uuid:fc877bbe-72a8-4e59-b959-010e6660984a",
                "orientation": "+"
              },
              {
                "ref": "uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          1.0,
          0.0,
          -0.0
        ],
        "area": 30.0
      }
    },
    {
      "id": "uuid:65959e29-11cb-4568-904d-61c4a7c17b98",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:aafd209b-cd13-401a-83f5-26751a02cffe",
                "orientation": "+"
              },
              {
                "ref": "uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03",
                "orientation": "+"
              },
              {
                "ref": "uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81",
                "orientation": "-"
              },
              {
                "ref": "uuid:9238cbda-d019-4b57-8319-0cc355656802",
                "orientation": "+"
              },
              {
                "ref": "uuid:06babc8d-f0d6-43eb-bfad-931055bae084",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 30.0
      }
    },
    {
      "id": "uuid:e2efe498-c6d5-4f9c-ac07-4c1c9e406675",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8",
                "orientation": "-"
              },
              {
                "ref": "uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b",
                "orientation": "-"
              },
              {
                "ref": "uuid:91cdc345-f745-4643-bc88-a24f8e2216b0",
                "orientation": "+"
              },
              {
                "ref": "uuid:4406e3f5-89dc-463b-84e4-487490f71f1a",
                "orientation": "-"
              },
              {
                "ref": "uuid:fc877bbe-72a8-4e59-b959-010e6660984a",
                "orientation": "-"
              },
              {
                "ref": "uuid:9238cbda-d019-4b57-8319-0cc355656802",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 32.0
      }
    },
    {
      "id": "uuid:5bcee2b5-be9b-47d6-9a8b-35dac021f661",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:4ad210b7-5de5-4732-af7c-978de28f988b",
                "orientation": "-"
              },
              {
                "ref": "uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4",
                "orientation": "-"
              },
              {
                "ref": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
                "orientation": "-"
              },
              {
                "ref": "uuid:61f99921-a94d-4e0d-8353-f027d76227c5",
                "orientation": "-"
              },
              {
                "ref": "uuid:aafd209b-cd13-401a-83f5-26751a02cffe",
                "orientation": "-"
              },
              {
                "ref": "uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -0.0,
          -0.0,
          -1.0
        ],
        "area": 88.0
      }
    },
    {
      "id": "uuid:91ce0c52-11c3-4e32-8bcc-dea958a3969e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:474fef44-eb6e-4e19-a871-433f9bac5650",
                "orientation": "-"
              },
              {
                "ref": "uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7",
                "orientation": "-"
              },
              {
                "ref": "uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03",
                "orientation": "-"
              },
              {
                "ref": "uuid:61f99921-a94d-4e0d-8353-f027d76227c5",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:56283886-1f4c-448c-b785-80fb9740a9cc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda",
                "orientation": "+"
              },
              {
                "ref": "uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4",
                "orientation": "+"
              },
              {
                "ref": "uuid:511c6e7d-728b-4f1f-9763-9461eb628586",
                "orientation": "-"
              },
              {
                "ref": "uuid:91cdc345-f745-4643-bc88-a24f8e2216b0",
                "orientation": "-"
              },
              {
                "ref": "uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -0.0
        ],
        "area": 18.0
      }
    },
    {
      "id": "uuid:f3338301-b0e3-401c-af23-41ac2ae8e969",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda",
                "orientation": "-"
              },
              {
                "ref": "uuid:7da1c2fe-f798-43cc-af44-ac63f968139c",
                "orientation": "-"
              },
              {
                "ref": "uuid:474fef44-eb6e-4e19-a871-433f9bac5650",
                "orientation": "+"
              },
              {
                "ref": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 6.0
      }
    },
    {
      "id": "uuid:a2117d6b-4621-4a6b-9809-9fab3dfc4ff0",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0",
                "orientation": "+"
              },
              {
                "ref": "uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985",
                "orientation": "+"
              },
              {
                "ref": "uuid:71af0dde-7fc9-4290-9624-119e91f422ea",
                "orientation": "+"
              },
              {
                "ref": "uuid:ad13a84c-df97-4b75-9dc1-1ce452249964",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:9d67557a-e130-4a47-b63d-c6a2bdf21fa2",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:c2a00070-f12b-42f9-b78c-b33daa500873",
                "orientation": "+"
              },
              {
                "ref": "uuid:ad13a84c-df97-4b75-9dc1-1ce452249964",
                "orientation": "-"
              },
              {
                "ref": "uuid:13dd8184-f73e-4d9f-9977-3e573274fccc",
                "orientation": "+"
              },
              {
                "ref": "uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -1.0,
          -0.0,
          -0.0
        ],
        "area": 30.0
      }
    },
    {
      "id": "uuid:d45fca44-8685-4146-92a5-b84d82fdc838",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:ed666061-98c5-439d-ab0d-5a792437a873",
                "orientation": "+"
              },
              {
                "ref": "uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f",
                "orientation": "+"
              },
              {
                "ref": "uuid:5a36c75b-053b-4d7b-b512-6777786d6180",
                "orientation": "+"
              },
              {
                "ref": "uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d",
                "orientation": "-"
              },
              {
                "ref": "uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 30.0
      }
    },
    {
      "id": "uuid:2497a842-0932-4fe5-ac1a-2f773473f338",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0",
                "orientation": "+"
              },
              {
                "ref": "uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78",
                "orientation": "-"
              },
              {
                "ref": "uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24",
                "orientation": "-"
              },
              {
                "ref": "uuid:5a36c75b-053b-4d7b-b512-6777786d6180",
                "orientation": "-"
              },
              {
                "ref": "uuid:13dd8184-f73e-4d9f-9977-3e573274fccc",
                "orientation": "-"
              },
              {
                "ref": "uuid:71af0dde-7fc9-4290-9624-119e91f422ea",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 32.0
      }
    },
    {
      "id": "uuid:04ea47e9-b4dd-4bed-a8f4-4802d1735c74",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:ed666061-98c5-439d-ab0d-5a792437a873",
                "orientation": "-"
              },
              {
                "ref": "uuid:61f99921-a94d-4e0d-8353-f027d76227c5",
                "orientation": "+"
              },
              {
                "ref": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
                "orientation": "-"
              },
              {
                "ref": "uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635",
                "orientation": "-"
              },
              {
                "ref": "uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0",
                "orientation": "-"
              },
              {
                "ref": "uuid:c2a00070-f12b-42f9-b78c-b33daa500873",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -0.0,
          -0.0,
          -1.0
        ],
        "area": 88.0
      }
    },
    {
      "id": "uuid:b5fd960f-0d14-4257-9182-40de738a7e50",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4",
                "orientation": "+"
              },
              {
                "ref": "uuid:242a8400-a076-4817-86c6-acd56087cec6",
                "orientation": "+"
              },
              {
                "ref": "uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0",
                "orientation": "-"
              },
              {
                "ref": "uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985",
                "orientation": "-"
              },
              {
                "ref": "uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          1.0,
          0.0,
          -0.0
        ],
        "area": 18.0
      }
    },
    {
      "id": "uuid:e119b096-e589-49bd-b1db-a1182dc2dade",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:474fef44-eb6e-4e19-a871-433f9bac5650",
                "orientation": "-"
              },
              {
                "ref": "uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3",
                "orientation": "-"
              },
              {
                "ref": "uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4",
                "orientation": "-"
              },
              {
                "ref": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 6.0
      }
    },
    {
      "id": "uuid:67842d3a-7c79-4f2a-8630-744711071e93",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:a604828d-a36b-4fac-ba6f-6160ade95301",
                "orientation": "-"
              },
              {
                "ref": "uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635",
                "orientation": "+"
              },
              {
                "ref": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
                "orientation": "+"
              },
              {
                "ref": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
                "orientation": "+"
              },
              {
                "ref": "uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          -0.0,
          -0.0,
          -1.0
        ],
        "area": 24.0
      }
    },
    {
      "id": "uuid:f1c1a636-d6ab-414c-a0aa-855fc7e85e1f",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280",
                "orientation": "+"
              },
              {
                "ref": "uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985",
                "orientation": "-"
              },
              {
                "ref": "uuid:a604828d-a36b-4fac-ba6f-6160ade95301",
                "orientation": "+"
              },
              {
                "ref": "uuid:511c6e7d-728b-4f1f-9763-9461eb628586",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          -1.0,
          0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:a22a6c54-306e-44bc-9b94-6c32c705e63e",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280",
                "orientation": "-"
              },
              {
                "ref": "uuid:91cdc345-f745-4643-bc88-a24f8e2216b0",
                "orientation": "-"
              },
              {
                "ref": "uuid:38499704-81f7-4d47-965f-435e0b7b0850",
                "orientation": "-"
              },
              {
                "ref": "uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 8.0
      }
    },
    {
      "id": "uuid:9ed21e0a-b062-4000-88e2-50bd9153e417",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:b6e30631-9768-4020-8947-c32137328216",
                "orientation": "+"
              },
              {
                "ref": "uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5",
                "orientation": "-"
              },
              {
                "ref": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
                "orientation": "-"
              },
              {
                "ref": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
                "orientation": "-"
              },
              {
                "ref": "uuid:af347f25-a547-477c-b246-cb810756d4dc",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          0.0,
          1.0
        ],
        "area": 16.0
      }
    },
    {
      "id": "uuid:802ff3d8-b8da-423f-8a02-7b2288485edd",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:38499704-81f7-4d47-965f-435e0b7b0850",
                "orientation": "+"
              },
              {
                "ref": "uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add",
                "orientation": "-"
              },
              {
                "ref": "uuid:b6e30631-9768-4020-8947-c32137328216",
                "orientation": "-"
              },
              {
                "ref": "uuid:fb03276b-4250-4d52-81e1-035a0bd92895",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          3.609557097661e-16,
          -1.0,
          0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:16c13b7b-aeda-4130-a793-d63f62bcc75b",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4",
                "orientation": "+"
              },
              {
                "ref": "uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa",
                "orientation": "+"
              },
              {
                "ref": "uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda",
                "orientation": "+"
              },
              {
                "ref": "uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94",
                "orientation": "-"
              },
              {
                "ref": "uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 12.0
      }
    },
    {
      "id": "uuid:786e8738-1690-426d-8e2f-f5e734336a67",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Face",
        "rings": [
          {
            "type": "Ring",
            "directed_references": [
              {
                "ref": "uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724",
                "orientation": "-"
              },
              {
                "ref": "uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b",
                "orientation": "+"
              },
              {
                "ref": "uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d",
                "orientation": "+"
              },
              {
                "ref": "uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1",
                "orientation": "-"
              },
              {
                "ref": "uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "normal": [
          0.0,
          1.0,
          0.0
        ],
        "area": 12.0
      }
    }
  ],
  "solids": [
    {
      "id": "uuid:758590d2-8cc6-4ff7-8fcc-d7ecd01b3498",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Solid",
        "shells": [
          {
            "type": "Shell",
            "directed_references": [
              {
                "ref": "uuid:4ac3b91b-eeb7-428c-b5e9-7e8a3f0998ae",
                "orientation": "+"
              },
              {
                "ref": "uuid:4a294022-4864-49c7-8cee-f9e43360bc4e",
                "orientation": "+"
              },
              {
                "ref": "uuid:01947f47-ee13-44a9-85a4-2bcb4881982a",
                "orientation": "+"
              },
              {
                "ref": "uuid:607a3363-3eb7-4ce6-a633-86d2e565692b",
                "orientation": "+"
              },
              {
                "ref": "uuid:3c1f5c4b-d842-40b6-a332-99d50015fa8f",
                "orientation": "+"
              },
              {
                "ref": "uuid:fe522919-1421-4fd1-9930-8c6551e3f2a5",
                "orientation": "+"
              },
              {
                "ref": "uuid:2387ae98-9236-42fe-9414-c45b99954c41",
                "orientation": "+"
              },
              {
                "ref": "uuid:4ba85faa-3935-4e89-a9f8-dcd647a5dbed",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "name": "Upper East",
        "levels": [
          2
        ],
        "volume": 168.0
      }
    },
    {
      "id": "uuid:82ce9302-e51d-48ff-a119-79bb5501ed1c",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Solid",
        "shells": [
          {
            "type": "Shell",
            "directed_references": [
              {
                "ref": "uuid:c55c88db-d187-4d7e-9aaa-b9d3dce52663",
                "orientation": "+"
              },
              {
                "ref": "uuid:dbd99467-ea83-4dff-b03f-eef2aad2687c",
                "orientation": "+"
              },
              {
                "ref": "uuid:0e55e87d-8475-4c92-89e7-d62f97ce9ec2",
                "orientation": "+"
              },
              {
                "ref": "uuid:6a5ff199-56a7-4e65-94b5-bfdf2ae3449d",
                "orientation": "+"
              },
              {
                "ref": "uuid:3c1f5c4b-d842-40b6-a332-99d50015fa8f",
                "orientation": "-"
              },
              {
                "ref": "uuid:e499fea3-19f7-4863-8a58-751caff7d884",
                "orientation": "+"
              },
              {
                "ref": "uuid:9e4c0c0e-6acf-401b-b35e-0e917ce3a5fc",
                "orientation": "+"
              },
              {
                "ref": "uuid:3f5c452f-9815-4b21-9b2d-0127ae80c385",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "name": "Upper West",
        "levels": [
          2
        ],
        "volume": 168.0
      }
    },
    {
      "id": "uuid:1070811c-70bd-4698-a08f-92c62e41aafc",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Solid",
        "shells": [
          {
            "type": "Shell",
            "directed_references": [
              {
                "ref": "uuid:66a430c0-123f-42df-9d11-64347362bcb3",
                "orientation": "+"
              },
              {
                "ref": "uuid:31d8f2b5-cc74-4f72-b230-d27dad0fd589",
                "orientation": "+"
              },
              {
                "ref": "uuid:65959e29-11cb-4568-904d-61c4a7c17b98",
                "orientation": "+"
              },
              {
                "ref": "uuid:e2efe498-c6d5-4f9c-ac07-4c1c9e406675",
                "orientation": "+"
              },
              {
                "ref": "uuid:5bcee2b5-be9b-47d6-9a8b-35dac021f661",
                "orientation": "+"
              },
              {
                "ref": "uuid:91ce0c52-11c3-4e32-8bcc-dea958a3969e",
                "orientation": "+"
              },
              {
                "ref": "uuid:56283886-1f4c-448c-b785-80fb9740a9cc",
                "orientation": "+"
              },
              {
                "ref": "uuid:f3338301-b0e3-401c-af23-41ac2ae8e969",
                "orientation": "+"
              },
              {
                "ref": "uuid:2387ae98-9236-42fe-9414-c45b99954c41",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "name": "Lower East",
        "levels": [
          1
        ],
        "volume": 264.0
      }
    },
    {
      "id": "uuid:74618bd4-0bbe-4490-92b3-27a4da496c39",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Solid",
        "shells": [
          {
            "type": "Shell",
            "directed_references": [
              {
                "ref": "uuid:a2117d6b-4621-4a6b-9809-9fab3dfc4ff0",
                "orientation": "+"
              },
              {
                "ref": "uuid:9d67557a-e130-4a47-b63d-c6a2bdf21fa2",
                "orientation": "+"
              },
              {
                "ref": "uuid:d45fca44-8685-4146-92a5-b84d82fdc838",
                "orientation": "+"
              },
              {
                "ref": "uuid:2497a842-0932-4fe5-ac1a-2f773473f338",
                "orientation": "+"
              },
              {
                "ref": "uuid:04ea47e9-b4dd-4bed-a8f4-4802d1735c74",
                "orientation": "+"
              },
              {
                "ref": "uuid:b5fd960f-0d14-4257-9182-40de738a7e50",
                "orientation": "+"
              },
              {
                "ref": "uuid:e119b096-e589-49bd-b1db-a1182dc2dade",
                "orientation": "+"
              },
              {
                "ref": "uuid:91ce0c52-11c3-4e32-8bcc-dea958a3969e",
                "orientation": "-"
              },
              {
                "ref": "uuid:9e4c0c0e-6acf-401b-b35e-0e917ce3a5fc",
                "orientation": "-"
              }
            ]
          }
        ]
      },
      "properties": {
        "name": "Lower West",
        "levels": [
          1
        ],
        "volume": 264.0
      }
    },
    {
      "id": "uuid:50453cb2-89bd-4432-8c7c-fdc2318febc2",
      "type": "Feature",
      "geometry": null,
      "topology": {
        "type": "Solid",
        "shells": [
          {
            "type": "Shell",
            "directed_references": [
              {
                "ref": "uuid:67842d3a-7c79-4f2a-8630-744711071e93",
                "orientation": "+"
              },
              {
                "ref": "uuid:f1c1a636-d6ab-414c-a0aa-855fc7e85e1f",
                "orientation": "+"
              },
              {
                "ref": "uuid:a22a6c54-306e-44bc-9b94-6c32c705e63e",
                "orientation": "+"
              },
              {
                "ref": "uuid:9ed21e0a-b062-4000-88e2-50bd9153e417",
                "orientation": "+"
              },
              {
                "ref": "uuid:802ff3d8-b8da-423f-8a02-7b2288485edd",
                "orientation": "+"
              },
              {
                "ref": "uuid:4ba85faa-3935-4e89-a9f8-dcd647a5dbed",
                "orientation": "-"
              },
              {
                "ref": "uuid:56283886-1f4c-448c-b785-80fb9740a9cc",
                "orientation": "-"
              },
              {
                "ref": "uuid:3f5c452f-9815-4b21-9b2d-0127ae80c385",
                "orientation": "-"
              },
              {
                "ref": "uuid:b5fd960f-0d14-4257-9182-40de738a7e50",
                "orientation": "-"
              },
              {
                "ref": "uuid:16c13b7b-aeda-4130-a793-d63f62bcc75b",
                "orientation": "+"
              },
              {
                "ref": "uuid:786e8738-1690-426d-8e2f-f5e734336a67",
                "orientation": "+"
              }
            ]
          }
        ]
      },
      "properties": {
        "name": "Stairwell",
        "levels": [
          1,
          2
        ],
        "volume": 120.0
      }
    }
  ]
}
```

#### ttl
```ttl
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix topo: <https://purl.org/geojson/topo#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<uuid:06babc8d-f0d6-43eb-bfad-931055bae084> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:20d3c864-4a8c-4440-b600-a1d424e92f51> <uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09> ) ] .

<uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:307b7db6-8014-4628-b80e-ff925bf71168> <uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d> ) ] .

<uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:11caaac5-b631-4bd8-a6af-f82cb6371071> <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> ) ] .

<uuid:13dd8184-f73e-4d9f-9977-3e573274fccc> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:8e503e04-ad51-423b-8102-708a845189b6> <uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1> ) ] .

<uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:caa6045e-4189-4571-8914-1189e51ac71e> <uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70> ) ] .

<uuid:242a8400-a076-4817-86c6-acd56087cec6> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e> <uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d> ) ] .

<uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e> <uuid:22138e52-65ef-4773-b69d-5ea2628fad7b> ) ] .

<uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> <uuid:fad324b9-801f-40f4-b65b-91f8753e9698> ) ] .

<uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0> <uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a> ) ] .

<uuid:38499704-81f7-4d47-965f-435e0b7b0850> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d> <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> ) ] .

<uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:22138e52-65ef-4773-b69d-5ea2628fad7b> <uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3> ) ] .

<uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717> <uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df> ) ] .

<uuid:4406e3f5-89dc-463b-84e4-487490f71f1a> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:c060c1dc-6544-4595-b583-72ecf603fd6d> <uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4> ) ] .

<uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3> <uuid:8087116e-84cc-44d1-8047-78dc3837d7e8> ) ] .

<uuid:474fef44-eb6e-4e19-a871-433f9bac5650> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:f34d9f2e-4180-41de-a613-46f78f4c178f> <uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a> ) ] .

<uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df> <uuid:793997c5-bcc4-4610-984b-6cf2c2997348> ) ] .

<uuid:4ad210b7-5de5-4732-af7c-978de28f988b> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6> <uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9> ) ] .

<uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3> <uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0> ) ] .

<uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4> <uuid:793997c5-bcc4-4610-984b-6cf2c2997348> ) ] .

<uuid:511c6e7d-728b-4f1f-9763-9461eb628586> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4> <uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6> ) ] .

<uuid:5a36c75b-053b-4d7b-b512-6777786d6180> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1> <uuid:e7300a01-f8c1-4351-9511-02790a5376b0> ) ] .

<uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:f34d9f2e-4180-41de-a613-46f78f4c178f> <uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70> ) ] .

<uuid:61f99921-a94d-4e0d-8353-f027d76227c5> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e> <uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a> ) ] .

<uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a> <uuid:206806a4-a2f8-4c04-858e-99d289858a40> ) ] .

<uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:e7300a01-f8c1-4351-9511-02790a5376b0> <uuid:307b7db6-8014-4628-b80e-ff925bf71168> ) ] .

<uuid:71af0dde-7fc9-4290-9624-119e91f422ea> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:793997c5-bcc4-4610-984b-6cf2c2997348> <uuid:8e503e04-ad51-423b-8102-708a845189b6> ) ] .

<uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ca62577e-8e24-4af2-88bf-33b34e25e606> <uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1> ) ] .

<uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3> <uuid:206806a4-a2f8-4c04-858e-99d289858a40> ) ] .

<uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70> <uuid:8087116e-84cc-44d1-8047-78dc3837d7e8> ) ] .

<uuid:745aa367-94b6-4949-a856-5271ec6672e9> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:e7300a01-f8c1-4351-9511-02790a5376b0> <uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd> ) ] .

<uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9> <uuid:20d3c864-4a8c-4440-b600-a1d424e92f51> ) ] .

<uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:8087116e-84cc-44d1-8047-78dc3837d7e8> <uuid:11caaac5-b631-4bd8-a6af-f82cb6371071> ) ] .

<uuid:7da1c2fe-f798-43cc-af44-ac63f968139c> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:f34d9f2e-4180-41de-a613-46f78f4c178f> <uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3> ) ] .

<uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0> <uuid:c611f840-2829-44b2-b367-3915ca7875a4> ) ] .

<uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> <uuid:22138e52-65ef-4773-b69d-5ea2628fad7b> ) ] .

<uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:c611f840-2829-44b2-b367-3915ca7875a4> <uuid:fad324b9-801f-40f4-b65b-91f8753e9698> ) ] .

<uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> <uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3> ) ] .

<uuid:8582d9c2-6053-495a-8413-f5493691c0de> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:c611f840-2829-44b2-b367-3915ca7875a4> <uuid:11caaac5-b631-4bd8-a6af-f82cb6371071> ) ] .

<uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:caa6045e-4189-4571-8914-1189e51ac71e> <uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e> ) ] .

<uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e> <uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3> ) ] .

<uuid:91cdc345-f745-4643-bc88-a24f8e2216b0> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> <uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4> ) ] .

<uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3> <uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70> ) ] .

<uuid:9238cbda-d019-4b57-8319-0cc355656802> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> <uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09> ) ] .

<uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:22138e52-65ef-4773-b69d-5ea2628fad7b> <uuid:e7300a01-f8c1-4351-9511-02790a5376b0> ) ] .

<uuid:a604828d-a36b-4fac-ba6f-6160ade95301> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df> <uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6> ) ] .

<uuid:aafd209b-cd13-401a-83f5-26751a02cffe> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:20d3c864-4a8c-4440-b600-a1d424e92f51> <uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e> ) ] .

<uuid:ad13a84c-df97-4b75-9dc1-1ce452249964> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:8e503e04-ad51-423b-8102-708a845189b6> <uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717> ) ] .

<uuid:af347f25-a547-477c-b246-cb810756d4dc> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9> <uuid:caa6045e-4189-4571-8914-1189e51ac71e> ) ] .

<uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:793997c5-bcc4-4610-984b-6cf2c2997348> <uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d> ) ] .

<uuid:b6e30631-9768-4020-8947-c32137328216> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9> <uuid:11caaac5-b631-4bd8-a6af-f82cb6371071> ) ] .

<uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9> <uuid:c060c1dc-6544-4595-b583-72ecf603fd6d> ) ] .

<uuid:c2a00070-f12b-42f9-b78c-b33daa500873> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ca62577e-8e24-4af2-88bf-33b34e25e606> <uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717> ) ] .

<uuid:c60507ba-226b-4e49-a702-e9afef899b23> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> <uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0> ) ] .

<uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9> <uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6> ) ] .

<uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:fad324b9-801f-40f4-b65b-91f8753e9698> <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> ) ] .

<uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6> <uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd> ) ] .

<uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df> <uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0> ) ] .

<uuid:ed666061-98c5-439d-ab0d-5a792437a873> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e> <uuid:ca62577e-8e24-4af2-88bf-33b34e25e606> ) ] .

<uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:22138e52-65ef-4773-b69d-5ea2628fad7b> <uuid:f34d9f2e-4180-41de-a613-46f78f4c178f> ) ] .

<uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0> <uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e> ) ] .

<uuid:f921656a-58e3-4375-bdff-ac8019f524cf> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd> <uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3> ) ] .

<uuid:fb03276b-4250-4d52-81e1-035a0bd92895> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d> <uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9> ) ] .

<uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6> <uuid:307b7db6-8014-4628-b80e-ff925bf71168> ) ] .

<uuid:fc877bbe-72a8-4e59-b959-010e6660984a> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09> <uuid:c060c1dc-6544-4595-b583-72ecf603fd6d> ) ] .

<uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e> <uuid:f34d9f2e-4180-41de-a613-46f78f4c178f> ) ] .

<uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4> a geojson:Feature ;
    geojson:topology [ a topo:Edge ;
            geojson:relatedFeatures ( <uuid:206806a4-a2f8-4c04-858e-99d289858a40> <uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6> ) ] .

<uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+00 1e+01 6e+00 ) ] .

<uuid:206806a4-a2f8-4c04-858e-99d289858a40> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 6e+00 0e+00 ) ] .

<uuid:20d3c864-4a8c-4440-b600-a1d424e92f51> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+01 1e+01 0e+00 ) ] .

<uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+01 1e+01 3e+00 ) ] .

<uuid:307b7db6-8014-4628-b80e-ff925bf71168> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+00 2e+00 3e+00 ) ] .

<uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+00 2e+00 6e+00 ) ] .

<uuid:8087116e-84cc-44d1-8047-78dc3837d7e8> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 6e+00 6e+00 ) ] .

<uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 0e+00 1e+01 3e+00 ) ] .

<uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 1e+01 6e+00 ) ] .

<uuid:8e503e04-ad51-423b-8102-708a845189b6> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 0e+00 0e+00 3e+00 ) ] .

<uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+01 0e+00 0e+00 ) ] .

<uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 6e+00 0e+00 ) ] .

<uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 0e+00 0e+00 0e+00 ) ] .

<uuid:c060c1dc-6544-4595-b583-72ecf603fd6d> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+01 0e+00 3e+00 ) ] .

<uuid:c611f840-2829-44b2-b367-3915ca7875a4> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 2e+00 6e+00 ) ] .

<uuid:ca62577e-8e24-4af2-88bf-33b34e25e606> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 0e+00 1e+01 0e+00 ) ] .

<uuid:caa6045e-4189-4571-8914-1189e51ac71e> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 6e+00 6e+00 ) ] .

<uuid:fad324b9-801f-40f4-b65b-91f8753e9698> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 2e+00 3e+00 ) ] .

<uuid:11caaac5-b631-4bd8-a6af-f82cb6371071> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 2e+00 6e+00 ) ] .

<uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1e+01 1e+01 0e+00 ) ] .

<uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1e+01 1e+01 6e+00 ) ] .

<uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1e+01 6e+00 6e+00 ) ] .

<uuid:793997c5-bcc4-4610-984b-6cf2c2997348> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 0e+00 3e+00 ) ] .

<uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 0e+00 3e+00 ) ] .

<uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 2e+00 6e+00 ) ] .

<uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 0e+00 0e+00 ) ] .

<uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.8e+01 1e+01 3e+00 ) ] .

<uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1e+01 6e+00 0e+00 ) ] .

<uuid:e7300a01-f8c1-4351-9511-02790a5376b0> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 2e+00 1e+01 3e+00 ) ] .

<uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 0e+00 0e+00 ) ] .

<uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 6e+00 3e+00 ) ] .

<uuid:22138e52-65ef-4773-b69d-5ea2628fad7b> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1e+01 1e+01 3e+00 ) ] .

<uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 6e+00 3e+00 ) ] .

<uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1.2e+01 2e+00 3e+00 ) ] .

<uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 8e+00 2e+00 3e+00 ) ] .

<uuid:f34d9f2e-4180-41de-a613-46f78f4c178f> a geojson:Feature ;
    geojson:geometry [ a geojson:Point ;
            geojson:coordinates ( 1e+01 6e+00 3e+00 ) ] .

[] a geojson:FeatureCollection ;
    topo:edges ( <uuid:c60507ba-226b-4e49-a702-e9afef899b23> <uuid:7dc1cc1c-8e7f-4666-9f52-4e6c2e6f57ac> <uuid:83ff2cdf-6c58-4e7b-ba55-e084eff8c569> <uuid:d69c596c-134e-4216-9bf6-d0f10e6886d8> <uuid:32e82eb1-93a4-4387-8cd0-9616ebf1e39b> <uuid:8582d9c2-6053-495a-8413-f5493691c0de> <uuid:120defbd-2e05-4ec3-ba3c-ffee086d2add> <uuid:4c2a6434-03b0-4aa2-85ea-a9fcaea41555> <uuid:830b9098-d914-4e8b-869d-4d20f1eb5c81> <uuid:3b72e45d-d351-46e4-a5b7-9ac9bc339d03> <uuid:921e2351-efbf-48be-85d3-eedc0dc2ddc0> <uuid:73f88b47-78ab-474d-9c62-73dfefd0dd5d> <uuid:7aa2a76d-9d5c-4540-9f2e-d8bcf36fadb5> <uuid:ed6b8b1c-7030-4d70-ab61-94cb3aa904a7> <uuid:5f17e211-e8b5-4a7c-85e4-798787fd82a5> <uuid:7da1c2fe-f798-43cc-af44-ac63f968139c> <uuid:46fd1def-a93e-4c99-9868-172cf1b40ff1> <uuid:856e43bc-ee35-44d0-b25e-ea94a53e1db6> <uuid:a5ed4867-4011-4db7-8425-cbe61a6d3a2d> <uuid:745aa367-94b6-4949-a856-5271ec6672e9> <uuid:f921656a-58e3-4375-bdff-ac8019f524cf> <uuid:6aab9ba2-327e-40df-96c2-0ea43c538c24> <uuid:fb28f3f2-8ea7-4c03-bff5-7352addba8b3> <uuid:e0416983-f0db-4c99-8a72-3f8b4615ab05> <uuid:07093c51-5d4e-42ad-941f-8eeb89e5ae78> <uuid:fb03276b-4250-4d52-81e1-035a0bd92895> <uuid:c97ac36d-9cf3-48ca-bb8f-c36cb335bebf> <uuid:af347f25-a547-477c-b246-cb810756d4dc> <uuid:21388b1b-dcba-46c0-8166-8ffc9c07e50b> <uuid:fc8ba01d-faa7-4407-ae92-32b584c8a6a3> <uuid:8601e9ea-c48f-4c00-a066-f950ed6b0724> <uuid:242a8400-a076-4817-86c6-acd56087cec6> <uuid:4ad210b7-5de5-4732-af7c-978de28f988b> <uuid:c12882ea-089f-4616-942c-ceb8fb4ac05e> <uuid:4406e3f5-89dc-463b-84e4-487490f71f1a> <uuid:511c6e7d-728b-4f1f-9763-9461eb628586> <uuid:79205d80-72e5-4bd8-9c03-9503e4e690cc> <uuid:06babc8d-f0d6-43eb-bfad-931055bae084> <uuid:fc877bbe-72a8-4e59-b959-010e6660984a> <uuid:aafd209b-cd13-401a-83f5-26751a02cffe> <uuid:2f3bbe39-01e3-4c96-8dea-377e38729a03> <uuid:9238cbda-d019-4b57-8319-0cc355656802> <uuid:91cdc345-f745-4643-bc88-a24f8e2216b0> <uuid:fe0704c2-5d2a-49a8-b507-e98c4047d8c4> <uuid:651bb558-f6d6-439f-a8e0-dd5c3385dc94> <uuid:61f99921-a94d-4e0d-8353-f027d76227c5> <uuid:474fef44-eb6e-4e19-a871-433f9bac5650> <uuid:736411fb-67f0-47c0-bf77-bf4f9048bcda> <uuid:3fef75ce-8c4c-4d89-a47f-65977debaee0> <uuid:48b52144-aaa0-42a1-8e7a-40bebfcf9985> <uuid:71af0dde-7fc9-4290-9624-119e91f422ea> <uuid:ad13a84c-df97-4b75-9dc1-1ce452249964> <uuid:c2a00070-f12b-42f9-b78c-b33daa500873> <uuid:13dd8184-f73e-4d9f-9977-3e573274fccc> <uuid:7355081e-9fa3-4fb5-ab10-c4efaa41d61f> <uuid:ed666061-98c5-439d-ab0d-5a792437a873> <uuid:5a36c75b-053b-4d7b-b512-6777786d6180> <uuid:b4c7d3ff-cf1f-40c1-8ea0-2cd2c09cc0e0> <uuid:36b10bf3-9e3a-49cb-9dc5-7e31ade26d17> <uuid:ec374b67-eb42-4c53-b5cc-0f919edb2635> <uuid:f0249395-1d12-42d1-bdaf-08c5cc29b2d4> <uuid:a604828d-a36b-4fac-ba6f-6160ade95301> <uuid:508f66b5-e0cb-489c-ae24-21bfb7c09280> <uuid:38499704-81f7-4d47-965f-435e0b7b0850> <uuid:b6e30631-9768-4020-8947-c32137328216> <uuid:90e3950e-40b2-4d9d-a135-1a4b708305aa> ) ;
    topo:faces ( [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] ) ;
    topo:points ( [ a geojson:FeatureCollection ;
                geojson:features <uuid:11caaac5-b631-4bd8-a6af-f82cb6371071>,
                    <uuid:16c35df5-bc63-4edd-8da5-dbcc5548a61e>,
                    <uuid:1d2a5d01-8547-4de6-abea-8f9ab994d35e>,
                    <uuid:1e20237c-9dfa-4251-9f3f-cc5e56a5becd>,
                    <uuid:206806a4-a2f8-4c04-858e-99d289858a40>,
                    <uuid:20d3c864-4a8c-4440-b600-a1d424e92f51>,
                    <uuid:22138e52-65ef-4773-b69d-5ea2628fad7b>,
                    <uuid:2b34e214-cba7-4a66-8443-ceb932c5ef09>,
                    <uuid:307b7db6-8014-4628-b80e-ff925bf71168>,
                    <uuid:3c08ae4e-7b27-4e95-8bfb-6b42451be8f6>,
                    <uuid:5e08b82a-8efb-447c-b5c2-54f8ff5788b3>,
                    <uuid:62a26df3-3e19-49bf-9ee4-24dbeb814a70>,
                    <uuid:793997c5-bcc4-4610-984b-6cf2c2997348>,
                    <uuid:7fe8cb9b-976e-4344-bf72-f3721d878ba4>,
                    <uuid:8087116e-84cc-44d1-8047-78dc3837d7e8>,
                    <uuid:87373f95-ee4b-4471-9980-f4a8258ee1e3>,
                    <uuid:8cda5c68-9c82-43b4-84d7-979efa36dfe1>,
                    <uuid:8d2be28b-8f31-46de-99cb-4d8709502cd0>,
                    <uuid:8e503e04-ad51-423b-8102-708a845189b6>,
                    <uuid:92bd9ed9-c138-45c3-b72c-a9ecb7f7cfe9>,
                    <uuid:9a1d8124-ca37-4abd-b07e-bff4c8eaa2f9>,
                    <uuid:9ef3d2ea-acea-4365-8bd5-2f8ef3036ed0>,
                    <uuid:a0ec1bfd-0f7a-4c42-bc71-bacdcd44071d>,
                    <uuid:a3b19f96-9bca-4c31-ac7e-4cb1615878df>,
                    <uuid:ad6d8fcc-402c-482e-8f1a-7492ccaead38>,
                    <uuid:b6d10150-f9d4-4f7e-b028-c4bbee8e7717>,
                    <uuid:b8412dad-b40a-4e35-9f42-f983e0fce39d>,
                    <uuid:c060c1dc-6544-4595-b583-72ecf603fd6d>,
                    <uuid:c611f840-2829-44b2-b367-3915ca7875a4>,
                    <uuid:ca62577e-8e24-4af2-88bf-33b34e25e606>,
                    <uuid:caa6045e-4189-4571-8914-1189e51ac71e>,
                    <uuid:d8d136c6-604c-4ad3-adf7-b0a7e04d034a>,
                    <uuid:e7300a01-f8c1-4351-9511-02790a5376b0>,
                    <uuid:f34d9f2e-4180-41de-a613-46f78f4c178f>,
                    <uuid:fad324b9-801f-40f4-b65b-91f8753e9698>,
                    <uuid:ff685e16-64f8-4f41-8a9e-7d8e83312fd6> ] ) ;
    topo:shells ( [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] [ a geojson:Feature ] ) .


```

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
description: A structured topology dataset with named arrays for each topological
  dimension. Points carry explicit coordinates; all higher-order features (edges,
  faces, shells, solids) use null geometry with topology defined via references or
  directed_references. Each array is restricted to its corresponding building block
  schema.
$defs:
  SolidFeatures:
    $anchor: SolidFeatures
    type: array
    items:
      allOf:
      - $ref: https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature/schema.yaml
      - properties:
          geometry:
            type: 'null'
          topology:
            properties:
              type:
                type: string
                const: Solid
            required:
            - type
            - references
  ShellFeatures:
    $anchor: ShellFeatures
    type: array
    items:
      allOf:
      - $ref: https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature/schema.yaml
      - properties:
          geometry:
            type: 'null'
          topology:
            properties:
              type:
                type: string
                const: Shell
            required:
            - type
            - directed_references
  FaceFeatures:
    $anchor: FaceFeatures
    type: array
    items:
      allOf:
      - $ref: https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature/schema.yaml
      - properties:
          geometry:
            type: 'null'
          topology:
            properties:
              type:
                type: string
                const: Face
            required:
            - type
            - directed_references
  RingFeatures:
    $anchor: RingFeatures
    type: array
    items:
      allOf:
      - $ref: https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature/schema.yaml
      - properties:
          geometry:
            type: 'null'
          topology:
            properties:
              type:
                type: string
                const: Ring
            required:
            - type
            - directed_references
  PointFeatures:
    $anchor: PointFeatures
    type: array
    items:
      properties:
        geometry:
          type: object
          required:
          - type
          - coordinates
          properties:
            type:
              type: string
              const: Point
            coordinates:
              type: array
              minItems: 2
      required:
      - geometry
  EdgeFeatures:
    $anchor: EdgeFeatures
    type: array
    items:
      allOf:
      - $ref: https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-line/schema.yaml
      - properties:
          topology:
            properties:
              references:
                minItems: 2
                maxItems: 2
type: object
required:
- type
properties:
  type:
    type: string
    const: FeatureCollection
  metadata:
    type: object
    description: Optional dataset metadata (units, coordinate precision, source info,
      etc.)
    additionalProperties: true
  points:
    type: array
    description: Point features providing base coordinate geometry for the topology
    items:
      oneOf:
      - $ref: '#PointFeatures'
      - allOf:
        - $ref: https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-collection/schema.yaml#FeatureCollectionOptions
        - properties:
            features:
              $ref: '#PointFeatures'
    x-jsonld-id: https://purl.org/geojson/topo#points
    x-jsonld-container: '@list'
  edges:
    oneOf:
    - $ref: '#EdgeFeatures'
    - type: array
      description: Edge (LineString) features referencing two point nodes via topology.references.
      items:
        allOf:
        - $ref: https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-collection/schema.yaml#FeatureCollectionOptions
        - properties:
            features:
              $ref: '#EdgeFeatures'
    x-jsonld-id: https://purl.org/geojson/topo#edges
    x-jsonld-container: '@list'
rings:
  type: array
  description: Rings connect edges in a directed
  items:
    allOf:
    - $ref: https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-collection/schema.yaml#FeatureCollectionOptions
    - properties:
        features:
          type: array
          items:
            $ref: https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-ring/schema.yaml
faces:
  type: array
  description: Face features whose boundary rings reference edges via directed_references.
    geometry is null.
  items:
    allOf:
    - $ref: https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-collection/schema.yaml#FeatureCollectionOptions
    - properties:
        features:
          type: array
          items:
            $ref: https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-face/schema.yaml
shells:
  type: array
  description: Shell features referencing faces via directed_references. geometry
    is null.
  items:
    allOf:
    - $ref: https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-collection/schema.yaml#FeatureCollectionOptions
    - properties:
        features:
          type: array
          items:
            $ref: https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-shell/schema.yaml
solids:
  type: array
  description: Solid features whose shells reference faces via directed_references.
    geometry is null.
  items:
    allOf:
    - $ref: https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-collection/schema.yaml#FeatureCollectionOptions
    - properties:
        features:
          $ref: '#SolidFeatures'
x-jsonld-extra-terms:
  Face: https://purl.org/geojson/topo#Face
  Ring: https://purl.org/geojson/topo#Ring
  Shell: https://purl.org/geojson/topo#Shell
  Solid: https://purl.org/geojson/topo#Solid
  faces:
    x-jsonld-id: https://purl.org/geojson/topo#faces
    x-jsonld-container: '@list'
  rings:
    x-jsonld-id: https://purl.org/geojson/topo#rings
    x-jsonld-container: '@list'
  shells:
    x-jsonld-id: https://purl.org/geojson/topo#shells
    x-jsonld-container: '@list'
  solids:
    x-jsonld-id: https://purl.org/geojson/topo#shells
    x-jsonld-container: '@list'
x-jsonld-prefixes:
  topo: https://purl.org/geojson/topo#
  geojson: https://purl.org/geojson/vocab#

```

Links to the schema:

* YAML version: [schema.yaml](https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-multi-collection/schema.json)
* JSON version: [schema.json](https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-multi-collection/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "Face": "topo:Face",
    "Ring": "topo:Ring",
    "Shell": "topo:Shell",
    "Solid": "topo:Solid",
    "faces": {
      "@id": "topo:faces",
      "@container": "@list"
    },
    "rings": {
      "@id": "topo:rings",
      "@container": "@list"
    },
    "shells": {
      "@id": "topo:shells",
      "@container": "@list"
    },
    "solids": {
      "@id": "topo:shells",
      "@container": "@list"
    },
    "points": {
      "@context": {
        "features": {
          "@context": {
            "id": "@id",
            "geometry": "geojson:geometry",
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
            "place": "dct:spatial"
          },
          "@id": "geojson:features",
          "@container": "@set"
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
        "featureType": "geojson:collectionFeatureType"
      },
      "@id": "topo:points",
      "@container": "@list"
    },
    "edges": {
      "@context": {
        "id": "@id",
        "geometry": "geojson:geometry",
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
        "topology": {
          "@context": {
            "references": {
              "@context": {
                "ref": {
                  "@type": "@id",
                  "@id": "topo:ref"
                }
              },
              "@id": "geojson:relatedFeatures",
              "@type": "@id",
              "@container": "@list"
            },
            "directed_references": {
              "@context": {
                "ref": {
                  "@type": "@id",
                  "@id": "topo:ref"
                }
              },
              "@id": "topo:directedReferences",
              "@container": "@list"
            }
          },
          "@type": "@id",
          "@id": "geojson:topology"
        }
      },
      "@id": "topo:edges",
      "@container": "@list"
    },
    "properties": "@nest",
    "type": "@type",
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
    "bbox": {
      "@container": "@list",
      "@id": "geojson:bbox"
    },
    "coordinates": {
      "@container": "@list",
      "@id": "geojson:coordinates"
    },
    "geometries": {
      "@id": "geojson:geometry",
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
    "ref": "topo:ref",
    "orientation": "topo:orientation",
    "Edge": "topo:Edge",
    "topo": "https://purl.org/geojson/topo#",
    "geojson": "https://purl.org/geojson/vocab#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "oa": "http://www.w3.org/ns/oa#",
    "dct": "http://purl.org/dc/terms/",
    "owlTime": "http://www.w3.org/2006/time#",
    "time": "http://www.w3.org/2006/time#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "csdm": "https://linked.data.gov.au/def/csdm/",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://surroundaustralia.github.io/topo-feature/build/annotated/geo/topo/features/topo-feature-multi-collection/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/surroundaustralia/topo-feature](https://github.com/surroundaustralia/topo-feature)
* Path: `_sources/features/topo-feature-multi-collection`

